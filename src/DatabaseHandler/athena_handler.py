
# Second level import 
from utils import get_boto3_client
from .main_handler import DatabaseHandler

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
        Prepare boto3 client.
        """
        self.athena_client = get_boto3_client("athena", self.region)
    
    def insert(self, data: dict) -> bool:
        """
        Insert data to the Athena database
        """
        pass
    
    def fetch(self, query: str) -> dict:
        """
        Fetch data from the Athena database
        """
        response = self.athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': self.database},
            ResultConfiguration={'OutputLocation': self.query_location}
        )
        query_execution_id = response['QueryExecutionId']

        # Wait for the query to complete
        status = None
        while status not in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            response = self.athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            status = response['QueryExecution']['Status']['State']
            print('Query status:', status)
            if status == 'FAILED':
                print('Query failed:', response['QueryExecution']['Status']['StateChangeReason'])
            else:
                print('Query succeeded!')

        # Once the query is complete, you can fetch the results if needed
        # For example:
        if status == 'SUCCEEDED':
            results = self.athena_client.get_query_results(QueryExecutionId=query_execution_id)
            for row in results['ResultSet']['Rows']:
                print([field['VarCharValue'] for field in row['Data']])
    
    def close(self):
        """
        Close the connection
        """
        self.athena_client.close()