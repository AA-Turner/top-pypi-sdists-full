"""
AWS Athena Utility Methods
"""
import time
from typing import Tuple, Optional
import pandas as pd
import boto3
import numpy as np

QUERY_STATUSES = ['SUCCEEDED', 'FAILED', 'CANCELLED']

def run_athena_query(
        access_key: str, secret_key: str, query: str, database: str,
        workgroup: str, region: Optional[str] = None, sleep_time: int = 1
    ) -> Tuple[pd.DataFrame, bool]:
    """
    Executes an Athena query and fetches the results into a Pandas DataFrame.
    Handles pagination to overcome the 1000 records limit.

    Args:
        access_key (str): AWS access key ID.
        secret_key (str): AWS secret access key.
        query (str): The SQL query string to execute.
        database (str): The Athena database to query against.
        workgroup (str): The Athena workgroup to use.
        region (str, optional): AWS region name.
        sleep_time (int, optional):
            Time in seconds to wait before checking query status again.

    Returns:
        Tuple[pd.DataFrame, bool]:
            A tuple containing the query result as a Pandas DataFrame and a
            boolean indicating query success.
    """
    success = False
    df = pd.DataFrame()
    # Establish a connection to Athena
    athena_client = boto3.client(
        'athena', aws_access_key_id=access_key,
        aws_secret_access_key=secret_key, region_name=region)
    # Start the query and obtain the execution ID
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        WorkGroup=workgroup)
    query_execution_id = response['QueryExecutionId']
    # Poll for query completion
    while True:
        status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        query_status = status['QueryExecution']['Status']['State']
        if query_status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(sleep_time)
    # Process results if query succeeded
    if query_status == 'SUCCEEDED':
        success = True
        paginator = athena_client.get_paginator('get_query_results')
        result_iterator = paginator.paginate(
            QueryExecutionId=query_execution_id)
        rows = []
        for result in result_iterator:
            for row in result['ResultSet']['Rows']:
                rows.append(row['Data'])
        # Check if there are any rows returned and handle header
        if rows:
            # Extract headers
            headers = [col['VarCharValue'] for col in rows[0]]
            data = [
                [value.get('VarCharValue', np.nan) for value in row]
                # Skip the header row for data rows
                for row in rows[1:]]
            df = pd.DataFrame(data, columns=headers)
    else:
        print(
            f"Query failed with status '{query_status}': {query_execution_id}"
        )

    return df, success
