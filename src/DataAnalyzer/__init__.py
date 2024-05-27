# First Level import :
from dataclasses import dataclass
import json 
from datetime import datetime

# Second level import
from enums import enum_type_activity

# Third Level import :
from pyspark.rdd import RDD
from pyspark.broadcast import Broadcast
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame
from pyspark.sql.functions import current_timestamp, expr

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
    
    def load_data(self, path: str) -> SparkDataFrame:
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