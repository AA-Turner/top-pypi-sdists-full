from unittest.mock import MagicMock

import pytest
from cnvrgv2.modules.datasource import Datasource
from cnvrgv2.proxy import Proxy

bucket_files = [
    ['file1.txt', 'file2.txt'],
    ['file3.txt'],
    ['path2/'],
    ['path1/file1.txt', 'path1/file2.txt', 'path1/file3.txt']
]

bucket_files_without_path1 = [
    ['file1.txt', 'file2.txt'],
    ['file3.txt'],
    ['path2/'],
    ['file1.txt', 'file2.txt', 'file3.txt']
]
bucket_files_without_path2 = [
    ['file1.txt', 'file2.txt'],
    ['file3.txt'],
    [],
    ['path1/file1.txt', 'path1/file2.txt', 'path1/file3.txt']
]

file_path = 'my-file.txt'
normalized_file_name = 'normalized_path/' + file_path


# Pytest fixture to create the Datasource instance
@pytest.fixture(scope="function")
def datasource(empty_context, mocker):
    # Mock the API call globally for all tests
    mocker.patch.object(Proxy, 'call_api')
    ds = Datasource(context=empty_context, slug="test-slug")
    ds.name = 'test-name'
    ds.bucket_name = 'test-bucket-name'
    return ds


@pytest.fixture(scope="function")
def mock_datasource_client(mocker, datasource):
    """
    Fixture that patches the Datasource.get_s3_client method and returns the mock client.
    """
    client = MagicMock()
    mocker.patch.object(Datasource, 'get_s3_client', return_value=client)
    datasource._client = client
    return client


@pytest.fixture(scope="function")
def mock_datasource_files_downloader(mocker):
    mock_downloader = MagicMock()
    pages = [1, 2, 3]
    mock_downloader.page_iterator = pages
    return mocker.patch.object(Datasource, 'get_files_downloader', return_value=mock_downloader)


def s3_data():
    """
    Fixture that provides mock S3 data for testing.
    """
    data = []
    for files in bucket_files:
        obj = {'Contents': []}
        for file in files:
            obj['Contents'].append({'Key': file})
        data.append(obj)
    return data


@pytest.fixture(scope="function")
def mock_datasource_client_paginator(mocker, datasource, mock_datasource_client):
    mock_paginator = MagicMock()
    list_iter = s3_data()

    mock_paginator.paginate.return_value = iter(list_iter)
    mocker.patch.object(mock_datasource_client, 'get_paginator', return_value=mock_paginator)


@pytest.fixture(scope="function")
def mock_normalize_file_path(mocker):
    return mocker.patch.object(Datasource, '_normalize_file_path', return_value=normalized_file_name)
