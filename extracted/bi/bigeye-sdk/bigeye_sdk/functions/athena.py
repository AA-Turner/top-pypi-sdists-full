import time
from typing import List, Union

import boto3

from bigeye_sdk.class_ext.enum_ext import StrEnum
from bigeye_sdk.log import get_logger

log = get_logger(__name__)

def run_athena_query(database_name: str, s3_query_result_uri: str, query: str, region: str = "us-west-2") -> str:
    """
    Assumes asynchronous query result to accommodate lambda runtime time limits.
    Args:
        s3_query_result_uri:
        database_name:
        query: String Query with no semicolon

    Returns: QueryExecutionId to be used with get_athena_query_result

    """
    client = boto3.client('athena', region_name=region)

    log.info(query)

    query_start = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database_name
        },
        ResultConfiguration={'OutputLocation': s3_query_result_uri}
    )

    return query_start['QueryExecutionId']


def run_athena_queries(database_name: str, s3_query_result_uri: str, queries: List[str]) -> List[str]:
    """

    Args:
        s3_query_result_uri:
        database_name:
        queries: List of string queries with no semicolon

    Returns: List of QueryExecutionId to be used with get_athena_query_result

    """
    return [run_athena_query(database_name, s3_query_result_uri, q) for q in queries]


class AthenaQueryExecutionStatus(StrEnum):
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'


def get_athena_query_status(query_execution_id: str, await_results: bool = False,
                              max_retries: int = 1, retry_pause: int = 5,
                            region: str = 'us-west-2') -> AthenaQueryExecutionStatus:
    """

    Args:
        retry_pause: Number of seconds to pause before retry.
        max_retries: Max number of retries
        query_execution_id: Query execution ID.
        await_results: Bool whether to wait for result.

    Returns: Status State (str)

    Exception: Throws an exception if the execution status is 'FAILED' or 'CANCELLED'
    """
    client = boto3.client('athena', region_name=region)

    query_execution: dict = client.get_query_execution(QueryExecutionId=query_execution_id)
    status_obj = query_execution['QueryExecution']['Status']
    status = AthenaQueryExecutionStatus(status_obj['State'])

    if await_results:
        retries = 0

        while status != AthenaQueryExecutionStatus.SUCCEEDED or retries < max_retries:
            query_execution: dict = client.get_query_execution(QueryExecutionId=query_execution_id)
            status_obj = query_execution['QueryExecution']['Status']
            status = AthenaQueryExecutionStatus(status_obj['State'])
            if status in [AthenaQueryExecutionStatus.FAILED, AthenaQueryExecutionStatus.CANCELLED]:
                raise Exception(f'Execution ID {query_execution_id} has {status}.  {status_obj}')
            retries += 1
            if status != AthenaQueryExecutionStatus.SUCCEEDED:
                time.sleep(retry_pause)

    return status


def get_athena_queries_result(query_execution_id: str, await_results: bool = False,
                              max_retries: int = 1, retry_pause: int = 5) -> Union[List[dict],
                                                                                   AthenaQueryExecutionStatus]:
    """

    Args:
        retry_pause: Number of seconds to pause before retry.
        max_retries: Max number of retries
        query_execution_id: Query execution ID.
        await_results: Bool whether to wait for result.

    Returns: List of responses (List[dict]) or Status State (str)
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_query_results

    Exception: Throws an exception if the execution status is 'FAILED' or 'CANCELLED'

    """
    client = boto3.client('athena')

    status: AthenaQueryExecutionStatus = get_athena_query_status(query_execution_id, await_results,
                                                                 max_retries, retry_pause)

    if status != AthenaQueryExecutionStatus.SUCCEEDED:
        return status

    response = client.get_query_results(
        QueryExecutionId='string'
    )

    rs: List[dict] = [response]

    while 'NextToken' in response:
        r = client.get_query_results(
            QueryExecutionId='string'
        )
        rs.append(r)

    return rs