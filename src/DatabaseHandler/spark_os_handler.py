import os
from dotenv import load_dotenv

# Second level import
from .main_handler import DatabaseHandler

# Third Level import :
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame

load_dotenv()
class Spark_OS_Handler(DatabaseHandler):
    """
    This class represents a handler for Athena database
    """
    def __init__(self, spark_session: SparkSession, index: str, region: str = "eu-central-1"):
        """
        Initialize the handler
        """
        self.spark_session = spark_session
        self.index = index
        self.region = region

    def connect(self):
        """
        Prepare OpenSearch configuration
        """
        self.__os_config = {
                        "opensearch.nodes": os.environ['OS_HOST'],
                        "opensearch.net.http.auth.user": os.environ['OS_USER'], 
                        "opensearch.net.http.auth.pass":  os.environ['OS_PW'],  
                        "opensearch.resource": self.index, 
                        "opensearch.nodes.resolve.hostname": True,
                        "opensearch.net.ssl" : "true",
                        'opensearch.nodes.wan.only' : 'true',
                        "opensearch.port": "443",
                        "inferSchema": "true",
                        "opensearch.spark.dataframe.write.null": "true"
                    }

    def insert(self, data: SparkDataFrame, index_name: str = None) -> bool:
        """
        Insert data to the Athena database
        """
        if index_name: # In case needed to update the index.
            self.__os_config["opensearch.resource"] = index_name
        
        data.write\
            .format("org.opensearch.spark.sql")\
            .options(**self.__os_config)\
            .mode("append")\
            .save("pyspark_idx")
            
        return True
    
    def fetch(self, query: str) ->  SparkDataFrame:
        """
        Fetch data from the OS database
        """
        
        pass
    
    def close(self):
        """
        Close the connection
        """
        pass