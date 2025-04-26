from typing import Any
from unittest import mock
from unittest.mock import MagicMock

import pytest

from snowflake.core import PollingOperation, RESTConnection
from snowflake.core.spark_connect import SparkConnectResource
from snowflake.core.version import __version__ as VERSION

from ...utils import extra_params


BASE_URL = "http://localhost.me:80/api/v2"
API_CLIENT_REQUEST = "snowflake.core.spark_connect._generated.api_client.ApiClient.request"


@pytest.fixture
def spark_connect_resource():
    conn = RESTConnection("localhost.me", 80, "", False, "http")
    return SparkConnectResource(conn)


@pytest.mark.parametrize("method, fn", (
    ("execute-plan", "execute_plan"),
    ("analyze-plan", "analyze_plan"),
    ("config", "config"),
    ("add-artifacts", "add_artifacts"),
    ("artifact-status", "artifact_status"),
    ("reattach-execute", "reattach_execute"),
    ("release-execute", "release_execute"),
))
def test_spark_connect_methods(spark_connect_resource, method, fn):
    args = (
        spark_connect_resource.root,
        "POST",
        BASE_URL + f"/spark-connect/{method}",
    )
    kwargs = get_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        getattr(spark_connect_resource, fn)("")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = getattr(spark_connect_resource, fn + "_async")("")
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def get_params() -> dict[str, Any]:
    return extra_params(
        headers={
            "Accept": "application/json",
            "User-Agent": "python_api/" + VERSION,
            "Content-Type": "application/octet-stream",
        },
    )


def mock_http_response() -> MagicMock:
    m = MagicMock()
    m.data = bytearray()
    m.status = 200
    return m
