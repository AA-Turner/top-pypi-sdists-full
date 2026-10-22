"""
Local py.test plugins

https://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-plugins
"""

import moto
import pytest

from tentaclio_s3 import clients


@pytest.fixture(scope="function")
def s3_client(s3_url):
    """Function level fixture due to cumbersome way of deleting non-empty AWS buckets"""
    with moto.mock_aws():
        with clients.S3Client(s3_url) as client:
            yield client
