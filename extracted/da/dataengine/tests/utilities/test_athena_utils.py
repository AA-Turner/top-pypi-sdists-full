import pytest
from unittest.mock import patch, MagicMock
from dataengine.utilities import athena_utils

@pytest.fixture
def athena_client():
    with patch('boto3.client', autospec=True) as mock:
        yield mock.return_value

def configure_mock_for_success(mock_athena_client):
    # Setup paginator to simulate success
    paginator = MagicMock()
    mock_athena_client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {'ResultSet': {
            'Rows': [{'Data': [{'VarCharValue': 'id'}, {'VarCharValue': 'description'}]},
                     {'Data': [{'VarCharValue': '1'}, {'VarCharValue': 'Test'}]},
                     {'Data': [{'VarCharValue': '2'}, {'VarCharValue': 'Example'}]}],
            'ResultSetMetadata': {'ColumnInfo': [{'Name': 'id'}, {'Name': 'description'}]}
        }}]
    mock_athena_client.start_query_execution.return_value = {'QueryExecutionId': '12345'}
    mock_athena_client.get_query_execution.side_effect = [
        {'QueryExecution': {'Status': {'State': 'RUNNING'}}},
        {'QueryExecution': {'Status': {'State': 'SUCCEEDED'}}}]

def configure_mock_for_failure(mock_athena_client):
    # Setup to simulate a failure
    mock_athena_client.start_query_execution.return_value = {'QueryExecutionId': '12345'}
    mock_athena_client.get_query_execution.return_value = {
        'QueryExecution': {'Status': {'State': 'FAILED'}}}

def test_run_athena_query_success(athena_client):
    configure_mock_for_success(athena_client)
    df, success = athena_utils.run_athena_query(
        None, None, 'SELECT * FROM test_table',
        'test_database', 'primary', 'us-west-2')
    assert success
    assert not df.empty
    assert df.shape[0] == 2  # Two data rows
    assert list(df.columns) == ['id', 'description']
    assert df.iloc[0]['id'] == '1'
    assert df.iloc[0]['description'] == 'Test'
    assert df.iloc[1]['id'] == '2'
    assert df.iloc[1]['description'] == 'Example'

def test_run_athena_query_failure(athena_client):
    configure_mock_for_failure(athena_client)
    df, success = athena_utils.run_athena_query(
        None, None, 'SELECT * FROM test_table',
        'test_database', 'primary', 'us-west-2')
    assert not success
    assert df.empty
