# First Level import :
from dataclasses import dataclass
import json 
from datetime import datetime

# Second level import
from DataAnalyzer.enums import enum_type_activity
from DatabaseHandler import AthenaHandler, Spark_OS_Handler

# Third Level import :
from pyspark.rdd import RDD
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame
from pyspark.sql.functions import current_timestamp, expr, broadcast, unix_timestamp, col, round

@dataclass
class MyAnalyzer:
    """
    This Class will be responsible for loading data and analyzing it. 
    """
    __spark : SparkSession
    _hour_range_time : int = 1
    
    def __post_init__(self):
        """
        Load the data, filter it and make it ready for analysis.
        """
        # Preparing data
        self._data = self.load_data()
        self.load_categories()
        
        # Saving the data as temp view for later use:
        self._data.createOrReplaceTempView("activity_logs") 
    
    def load_data(self) -> SparkDataFrame:
        """
        Load data from the daily parquet files.
        """
        now = datetime.now()
        
        # Load today's Data :
        today_data = self.__spark.read.parquet(f"s3://iceberg-track/topics/data_lake/activity_logs/data/*/start_date_day={now.date()}")
        
        # Get current timestamp
        current_time = current_timestamp()

        # Calculate the timestamp for one hour ago
        one_hour_ago = expr(f"current_timestamp() - INTERVAL {self._hour_range_time} HOUR")

        # Filter the DataFrame to get rows from the last hour
        last_hour_data = today_data.filter(today_data["start_date"] > one_hour_ago)
        
        return last_hour_data
    
    def load_categories(self) -> bool :
        """
        From enum prepare a spark dataframe to use it for brodcasting.
        """
        res = []
        # Formatting into easier format to use later.
        for category in enum_type_activity:
            res.append({
                "activity" : category.name,
                "category" : category.value["category"],
                "complexity" : category.value["complexity"]
            })
            
        # Create a DataFrame from the list of dictionaries
        self.categories = self.__spark.createDataFrame(res)
        
        return True
    
    def preprocessing_pipeline(self) -> None:
        """
        Add activity details to our main dataframe using the categories enums that we have loaded previously.
        """
        ## We will generate the activity details : 
        # Using broadcast to avoid shuffling we'll join the self._data with self.categories based on activity : 
        self._data = self._data.join(broadcast(self.categories), self._data["action"] == self.categories["activity"])
        
        # For activities that are not in the enum, we'll set the category and complexity to "unknown"
        self._data = self._data.fillna("unknown", subset=["category", "complexity"])
        
        ## Calculate the total minutes of the activity
        self.calculate_total_minute_activity()
        
        ## Get the deparment name : 
        self.get_department_name()
        
        # Remove column id from self._data, it's useless :
        self._data = self._data.drop("id")
        
        # Update tmp view : 
        self._data.createOrReplaceTempView("activity_logs") 
    
    def calculate_total_minute_activity(self) -> None : 
        """
        Add a column with end_date - start_date to calculate the total minutes of the activity.
        """
        # Convert string to timestamp
        self._data = self._data.withColumn("start_date", col("start_date").cast("timestamp")).withColumn("end_date", col("end_date").cast("timestamp"))

        # Calculate the difference in minutes
        self._data = self._data.withColumn("duration_minutes",
                        round((unix_timestamp("end_date") - unix_timestamp("start_date")) / 60))
            
    def employee_have_left(self) -> None:
        """
        Get list of employees that have left the office in the last hour and save them as list to be inserted later into logging db.
        """
        employees_left = self.__spark.sql("SELECT * FROM activity_logs WHERE action = 'left'")
        
        # Get a list of dict with employees_id and end_date : 
        self.employees_left = employees_left.select("employees_id", "end_date").collect()
        
    def load_department(self) -> None:
        """
        Load the department data from the database.
        """
        # Init database handler:
        athena_handler = AthenaHandler()
        athena_handler.connect()
        
        # First we'll need to load available department from database:
        query = 'SELECT id,name as department_name FROM "employees_activity"."department" '
        self.departments = athena_handler.fetch(query)
        
        # Creating a spark dataframe from the pandas dataframe to use brodcast merge.
        self.departments = self.__spark.createDataFrame(self.departments)
        
        # Closing client
        athena_handler.close()
    
    def get_department_name(self) -> None:
        """
        Get the department name for each employee.
        """
        # Load existing department from AthenaDB : 
        self.load_department()
        
        # Get the department name for each employee
        self._data = self._data.join(broadcast(self.departments), self._data["department_id"] == self.departments["id"])
    
    def generate_statistics(self, save: bool) -> dict:
        """
        Generate statistics for the last hour, if save is true, we'll insert the data into the database.
        """
        # Stats per department :
        stats_per_department = self.__spark.sql("SELECT department_name, sum(complexity) as total_complexity FROM activity_logs GROUP BY department_name")
        
        # Generate working hours for each employee :
        working_hours = self.__spark.sql("SELECT employees_id, sum(duration_minutes) as total_minutes FROM activity_logs where category = 'work' GROUP BY employees_id")
        
        if save:
            # Init database handler:
            os_handler = Spark_OS_Handler(self.__spark, "employees_activity")
            os_handler.connect()
            
            # Insert the data into the database
            os_handler.insert(self._data)
            os_handler.insert(stats_per_department, "stats_per_department")
            os_handler.insert(working_hours, "working_hours")
            
            # Close the connection
            os_handler.close()
        

