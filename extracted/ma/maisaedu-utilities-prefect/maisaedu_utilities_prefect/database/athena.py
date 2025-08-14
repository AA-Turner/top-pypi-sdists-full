import io
import time
import boto3
import pandas as pd
from botocore.exceptions import ClientError

def aws_client_factory(
    aws_access_key: str,
    aws_secret_key: str,
    aws_region: str = 'us-east-1',
    type: str = 'athena'
):
    """
    Factory function to create and return initialized AWS Athena and S3 clients.

    Parameters:
    -------------
    aws_access_key: str
        AWS access key ID
    aws_secret_key: str
        AWS secret access key
    aws_region: str
        AWS region name (default: 'us-east-1')
    type: str
        Type of AWS client to create ('athena' or 's3'). Default is 'athena'.

    Returns:
    ---------
    boto3.client
        Initialized AWS client for Athena or S3 based on the type specified.
    """

    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    if type == 'athena':
        return session.client('athena')
    elif type == 's3':
        return session.client('s3')


def execute_query(athena_client, s3_client, query, database, output_location, workgroup = None, return_output_path=False, max_retries=30):
    """
    Execute a query in Athena and return the result as a DataFrame.
    
    Parameters:
    -------------
    athena_client: boto3.client
        Initialized Athena client
    s3_client: boto3.client
        Initialized S3 client
    query: str
        SQL query to execute
    database: str
        Athena database name
    output_location: str
        S3 path to store the result
    max_retries: int
        Maximum number of retries to wait for execution
    
    Returns:
    ---------
    pandas.DataFrame
        DataFrame with the query result
    """

    try:
        if workgroup is None:
            response = athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': database},
                ResultConfiguration={'OutputLocation': output_location},
            )
        else:
            response = athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': database},
                ResultConfiguration={'OutputLocation': output_location},
                WorkGroup=workgroup
            )
        execution_id = response['QueryExecutionId']
    except ClientError as e:
        raise RuntimeError(f"Error executing Athena query: {e}")

    retries = 0
    while retries < max_retries:
        try:
            status = athena_client.get_query_execution(QueryExecutionId=execution_id)
            state = status['QueryExecution']['Status']['State']
            if state == 'SUCCEEDED':
                break
            elif state in ['FAILED', 'CANCELLED']:
                raise RuntimeError(f"Query {execution_id} failed with state: {state}")
        except ClientError as e:
            raise RuntimeError(f"Error checking query status: {e}")
        retries += 1
        time.sleep(2)
    else:
        raise TimeoutError(f"Query took too long to execute. Max retries ({max_retries}) exceeded.")

    try:
        s3_path = status['QueryExecution']['ResultConfiguration']['OutputLocation']
        if return_output_path:
            return s3_path
        s3_path = s3_path.replace('s3://', '')
        bucket_name = s3_path.split('/', 1)[0]
        key = s3_path.split('/', 1)[1]
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read()
        df = pd.read_csv(io.BytesIO(content))
        return df
    except Exception as e:
        raise RuntimeError(f"Error getting query result: {e}")