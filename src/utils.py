import boto3 

def get_boto3_client(service: str, region: str = "eu-central-1") -> boto3.client:
    """
    Get boto3 client with specified region
    """
    return boto3.client(service, region_name=region)