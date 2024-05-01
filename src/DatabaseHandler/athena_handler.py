# First level import 
import pandas as pd

# Second level import 
from utils import get_boto3_client
from .main_handler import DatabaseHandler

# Third party import 
from pyathena import connect as athena_connect

class AthenaHandler(DatabaseHandler):
    """
    This class represents a handler for Athena database
    """
    def __init__(self, database: str = "employees_activity", query_location: str = "s3://iceberg-track/result_queries/", region: str = "eu-central-1"):
        """
        Initialize the handler
        """
        self.database = database
        self.region = region
        self.query_location = query_location

    def connect(self):
        """
        Prepare pyAthena client & cursor.
        """
        self.pyathena_client = athena_connect(region_name = self.region, s3_staging_dir = self.query_location)

    def insert(self, data: dict) -> bool:
        """
        Insert data to the Athena database
        """
        pass
    
    def fetch(self, query: str) ->  pd.DataFrame:
        """
        Fetch data from the Athena database
        """
        
        with self.pyathena_client.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
        return pd.DataFrame(data, columns=columns)
    
    def close(self):
        """
        Close the connection
        """
        self.athena_client.close()