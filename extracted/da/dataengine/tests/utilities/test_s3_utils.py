import tempfile
import datetime
import pytest
import boto3
from moto import mock_aws
import numpy as np
import pandas as pd
from dataengine.utilities import s3_utils

# Setup global variables
ACCESS_KEY = "testing"
SECRET_KEY = "testing"
BUCKET_NAME = "my-bucket"


@pytest.fixture
def aws_credentials():
    """Mock AWS Credentials for moto."""
    import os
    os.environ['AWS_ACCESS_KEY_ID'] = ACCESS_KEY
    os.environ['AWS_SECRET_ACCESS_KEY'] = SECRET_KEY
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture
def s3_client(aws_credentials):
    with mock_aws():
        conn = boto3.client("s3", region_name="us-east-1")
        yield conn


def setup_s3_bucket(s3_client):
    s3_client.create_bucket(Bucket=BUCKET_NAME)
    s3_client.put_object(
        Bucket=BUCKET_NAME, Key='test_textfile', Body=b'test_content')
    s3_client.put_object(
        Bucket=BUCKET_NAME, Key='test_csv', Body="col1,col2\n1,2\n3,4")
    s3_client.put_object(
        Bucket=BUCKET_NAME, Key='test_size', Body=b'a' * 1024 * 10000)


def test_is_valid_s3_url():
    # Test valid S3 URL
    assert s3_utils.is_valid_s3_url("s3://my-bucket/my_prefix") == True
    # Test valid S3 URL pointing to bucket root
    assert s3_utils.is_valid_s3_url("s3://my-bucket/") == True
    # Test invalid scheme
    assert s3_utils.is_valid_s3_url("http://my-bucket/my_prefix") == False
    # Test missing netloc (bucket)
    assert s3_utils.is_valid_s3_url("s3:///my_prefix") == False
    # Test missing path
    # Could be True, depending on our requirements
    assert s3_utils.is_valid_s3_url("s3://my-bucket") == False
    # Test completely invalid URL
    assert s3_utils.is_valid_s3_url("not_a_valid_url") == False
    # Test empty string
    assert s3_utils.is_valid_s3_url("") == False


def test_parse_url():
    # Test with typical valid S3 URL
    s3_url = 's3://my-bucket/my_prefix'
    prefix, bucket = s3_utils.parse_url(s3_url)
    assert prefix == 'my_prefix'
    assert bucket == 'my-bucket'
    # Test with valid S3 URL pointing to bucket root
    s3_url = 's3://my-bucket/'
    prefix, bucket = s3_utils.parse_url(s3_url)
    assert prefix == ''
    assert bucket == 'my-bucket'
    # Test with invalid scheme
    s3_url = 'http://my-bucket/my_prefix'
    prefix, bucket = s3_utils.parse_url(s3_url)
    assert prefix is None
    assert bucket is None
    # Test with missing netloc (bucket)
    s3_url = 's3:///my_prefix'
    prefix, bucket = s3_utils.parse_url(s3_url)
    assert prefix is None
    assert bucket is None
    # Test with missing path
    s3_url = 's3://my-bucket'
    prefix, bucket = s3_utils.parse_url(s3_url)
    assert prefix is None  # Or '' depending on your requirements
    assert bucket is None  # Or 'my-bucket' depending on your requirements
    # Test completely invalid URL
    s3_url = 'not_a_valid_url'
    prefix, bucket = s3_utils.parse_url(s3_url)
    assert prefix is None
    assert bucket is None
    # Test with empty string
    s3_url = ''
    prefix, bucket = s3_utils.parse_url(s3_url)
    assert prefix is None
    assert bucket is None


def test_read_file(s3_client):
    setup_s3_bucket(s3_client)
    s3_prefix = 'test_textfile'
    result = s3_utils.read_file(ACCESS_KEY, SECRET_KEY, s3_prefix, BUCKET_NAME)
    assert result == b'test_content'


def test_read_df(s3_client):
    setup_s3_bucket(s3_client)
    s3_prefix = 'test_csv'
    # Get the test csv from the mocked bucket as a pandas DataFrame
    df = s3_utils.read_df(ACCESS_KEY, SECRET_KEY, s3_prefix, BUCKET_NAME)
    # Verify that the DataFrame is as expected
    expected_df = pd.DataFrame({'col1': [1, 3], 'col2': [2, 4]})
    pd.testing.assert_frame_equal(df, expected_df)


def test_write_bytes(s3_client):
    setup_s3_bucket(s3_client)
    # Setup test data
    s3_prefix = 'test_write_bytes'
    bytes_object = b"test_data"
    # Run the function
    success = s3_utils.write_bytes(
        ACCESS_KEY, SECRET_KEY, s3_prefix, BUCKET_NAME, bytes_object)
    # Verify the function return
    assert success == True
    # Verify that the object was written to S3
    written_data = s3_utils.read_file(
        ACCESS_KEY, SECRET_KEY, s3_prefix, BUCKET_NAME)
    assert written_data == bytes_object


def test_write_pandas_df_csv(s3_client):
    setup_s3_bucket(s3_client)
    # Setup args
    prefix = "test_write_dataframe.csv"
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    # Write DataFrame to S3
    success = s3_utils.write_pandas_df(
        ACCESS_KEY, SECRET_KEY, f's3://{BUCKET_NAME}/{prefix}', df)
    assert success == True
    # Verify that the DataFrame was written to S3
    written_df = s3_utils.read_df(
        ACCESS_KEY, SECRET_KEY, prefix, BUCKET_NAME)
    pd.testing.assert_frame_equal(written_df, df)


def test_write_pandas_df_parquet(s3_client):
    setup_s3_bucket(s3_client)
    # Setup args
    prefix = "test_write_dataframe.parquet"
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    # Write DataFrame to S3
    success = s3_utils.write_pandas_df(
        ACCESS_KEY, SECRET_KEY, f's3://{BUCKET_NAME}/{prefix}', df,
        file_format="parquet")
    assert success == True
    # TODO: Add verification that the DataFrame was written to S3


def test_write_pandas_df_unsupported_format(s3_client):
    setup_s3_bucket(s3_client)
    # Setup args
    prefix = "test_write_dataframe.unsupported"
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    # Write DataFrame to S3
    success = s3_utils.write_pandas_df(
        ACCESS_KEY, SECRET_KEY, f's3://{BUCKET_NAME}/{prefix}',
        df, file_format="unsupported")
    assert success == False


def test_write_dict(s3_client):
    setup_s3_bucket(s3_client)
    # Setup args
    prefix = "test_dict.yaml"
    test_dict = {'key': 'value', 'another_key': 123}
    # Write dict to s3
    success = s3_utils.write_dict(
        ACCESS_KEY, SECRET_KEY, f's3://{BUCKET_NAME}/{prefix}', test_dict)

    assert success == True


def test_write_zip(s3_client):
    setup_s3_bucket(s3_client)
    # Setup args
    prefix = "test_zip.zip"
    test_files = {
        'file1.txt': b'This is file1', 'file2.txt': b'This is file2'}
    # Write zip to s3
    success = s3_utils.write_zip(
        ACCESS_KEY, SECRET_KEY, f's3://{BUCKET_NAME}/{prefix}', test_files)

    assert success == True


def test_write_local_file(s3_client):
    setup_s3_bucket(s3_client)
    # Create a temporary file
    with tempfile.NamedTemporaryFile() as tmpfile:
        tmpfile.write(b"Some content")
        tmpfile.seek(0)  # Reset file pointer to beginning
        # Write temprary file
        success = s3_utils.write_local_file(
            ACCESS_KEY, SECRET_KEY, 'test_local_file', BUCKET_NAME,
            tmpfile.name)

    assert success == True


def test_check_s3_path_valid(s3_client):
    setup_s3_bucket(s3_client)
    assert s3_utils.check_s3_path(
        ACCESS_KEY, SECRET_KEY, 'test_textfile', BUCKET_NAME
    ) == True


def test_check_s3_path_invalid(s3_client):
    setup_s3_bucket(s3_client)
    assert s3_utils.check_s3_path(
        ACCESS_KEY, SECRET_KEY, 'nonexistent_file.txt', BUCKET_NAME
    ) == False


def test_check_s3_path_with_glob(s3_client):
    setup_s3_bucket(s3_client)
    assert s3_utils.check_s3_path(
        ACCESS_KEY, SECRET_KEY, 'test_*', BUCKET_NAME
    ) == True


def test_check_s3_path_invalid_glob(s3_client):
    setup_s3_bucket(s3_client)
    assert s3_utils.check_s3_path(
        ACCESS_KEY, SECRET_KEY, 'nonexistent*', BUCKET_NAME
    ) == False


def test_get_responses(s3_client):
    setup_s3_bucket(s3_client)
    responses = s3_utils.get_responses(
        ACCESS_KEY, SECRET_KEY, 'test', BUCKET_NAME)
    assert len(responses) == 3
    assert [file["Key"] for file in responses] == [
        'test_csv', 'test_size', 'test_textfile']


def test_get_responses_empty(s3_client):
    setup_s3_bucket(s3_client)
    responses = s3_utils.get_responses(
        ACCESS_KEY, SECRET_KEY, 'nonexistent_file', BUCKET_NAME)
    assert len(responses) == 0


def test_get_s3_prefix_size(s3_client):
    setup_s3_bucket(s3_client)
    size_gb = s3_utils.get_s3_prefix_size(
        ACCESS_KEY, SECRET_KEY, ['test_size'], BUCKET_NAME)
    assert np.isclose(size_gb, 0.01, atol=1e-9)


def test_get_s3_prefix_size_empty(s3_client):
    setup_s3_bucket(s3_client)
    size_gb = s3_utils.get_s3_prefix_size(
        ACCESS_KEY, SECRET_KEY, ['nonexistent_file'], BUCKET_NAME)
    assert size_gb == 0.0


def test_copy_file_success(s3_client):
    setup_s3_bucket(s3_client)
    assert s3_utils.copy_file(
        ACCESS_KEY, SECRET_KEY, 'test_textfile', 'test_textfile_copy',
        BUCKET_NAME
    ) == True


def test_copy_file_fail(s3_client):
    setup_s3_bucket(s3_client)
    assert s3_utils.copy_file(
        ACCESS_KEY, SECRET_KEY, 'nonexistent_file', 'nonexistent_file_copy',
        BUCKET_NAME
    ) == False


def test_copy_s3_files_success(s3_client):
    setup_s3_bucket(s3_client)
    key_map = {
        'test_textfile': 'test_textfile_copy',
        'test_csv': 'test_csv_copy'}
    assert s3_utils.copy_s3_files(
        ACCESS_KEY, SECRET_KEY, key_map, BUCKET_NAME, worker_count=2,
        max_retries=1
    ) == True


def test_copy_s3_files_partial_failure(s3_client):
    setup_s3_bucket(s3_client)
    key_map = {
        'test_textfile': 'test_textfile_copy',
        'nonexistent_file': 'nonexistent_file_copy'}
    assert s3_utils.copy_s3_files(
        ACCESS_KEY, SECRET_KEY, key_map, BUCKET_NAME, worker_count=2,
        max_retries=1
    ) == False


def test_find_latest_s3_path_no_data(s3_client):
    bucket_name = "test-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    # Define parameters
    dt = datetime.datetime.now()
    hour = 16
    path = f"s3://{bucket_name}/data/{{date_str}}/{{hour}}/file.csv"
    # Run test
    paths = s3_utils.find_latest_s3_path(
        path=path, dt=dt, hour=hour,
        aws_access_key=ACCESS_KEY, aws_secret_key=SECRET_KEY)
    # Assert
    assert paths == []


def test_find_latest_s3_path_with_data(s3_client):
    # Setup
    bucket_name = "test-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    # Create mock objects
    dt = datetime.datetime.utcnow()
    hour = dt.hour
    path = f"s3://{bucket_name}/data/{{date_str}}/{{lz_hour}}/file.csv"
    formatted_path = path.format(
        date_str=dt.date().isoformat(), lz_hour=f"{hour:02d}")
    s3_client.put_object(
        Bucket=bucket_name, Key=f"data/{dt.date().isoformat()}/{hour:02d}/file.csv",
        Body="")
    # Run test
    paths = s3_utils.find_latest_s3_path(
        path=path, dt=dt, hour=hour,
        aws_access_key=ACCESS_KEY, aws_secret_key=SECRET_KEY)
    # Assert
    assert paths == [formatted_path]


def test_find_latest_s3_path_with_star_hour(s3_client):
    # Setup
    bucket_name = "test-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    # Create mock objects
    dt = datetime.datetime.now()
    path = f"s3://{bucket_name}/data/{{date_str}}/{{hour}}/file.csv"
    hour_to_create = 15
    formatted_path = path.format(
        date_str=dt.date().isoformat(), hour=f"{hour_to_create:02d}")
    s3_client.put_object(
        Bucket=bucket_name, Key=f"data/{dt.date().isoformat()}/{hour_to_create:02d}/file.csv",
        Body="")
    # Run test
    paths = s3_utils.find_latest_s3_path(
        path=path, dt=dt, hour="*",
        aws_access_key=ACCESS_KEY, aws_secret_key=SECRET_KEY)
    # Assert
    assert formatted_path in paths
    assert len(paths) == 1
