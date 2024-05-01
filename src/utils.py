import boto3 

def get_boto3_client(service: str, region: str = "eu-central-1") -> boto3.client:
    """
    Get boto3 client with specified region
    """
    my_client = boto3.client(service, region_name=region)
    
    # Check on identity :  (For Debugging Purposes)
    #check_boto3_identity()
    
    return my_client

def check_boto3_identity():
    # Get current IAM identity
    identity = boto3.client('sts').get_caller_identity()

    # Extract user information
    user_arn = identity['Arn']
    user_name = user_arn.split('/')[-1]

    print("IAM User Name:", user_name)
    print("IAM User ARN:", user_arn)