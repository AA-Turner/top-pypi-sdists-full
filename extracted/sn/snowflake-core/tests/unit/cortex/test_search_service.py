from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.cortex.search_service import QueryRequest

from ...utils import BASE_URL, extra_params


API_CLIENT_REQUEST = "snowflake.core.cortex.search_service._generated.api_client.ApiClient.request"


@pytest.fixture
def search_services(schema):
    return schema.cortex_search_services


@pytest.fixture
def search_service(search_services):
    return search_services["my_service"]


def test_search_collection(fake_root, search_services):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/cortex-search-services/my_service:query",
    )
    kwargs = extra_params(
        body={
            "columns": ["col1"],
            "limit": 10,
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = search_services.search_async("my_service", QueryRequest(columns=["col1"]))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_search(fake_root, search_service):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/cortex-search-services/my_service:query",
    )
    kwargs = extra_params(
        body={
            "query": "hi",
            "columns": ["col1"],
            "limit": 10,
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = search_service.search_async("hi", ["col1"])
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
