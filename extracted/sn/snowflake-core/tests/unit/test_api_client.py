from concurrent.futures import Future
from unittest import mock

import pytest

import snowflake.core._thread_pool as thread_pool

from snowflake.core._generated import ApiClient
from snowflake.core._internal.snowapi_parameters import SnowApiParameter, SnowApiParameters


@pytest.fixture(autouse=True)
def reset_pool():
    thread_pool.THREAD_POOL.reset()


def test_async_api_calls_are_submitted_to_the_pool(fake_root, event):
    fake_root.parameters.return_value = SnowApiParameters({SnowApiParameter.MAX_THREADS: "1"})
    api_client = ApiClient(fake_root)
    with mock.patch("snowflake.core._generated.api_client.ApiClient.request") as mocked_request:
        mocked_request.side_effect = lambda *args, **kwargs: event.wait()
        first_call = api_client.call_api(fake_root, "/api/v2/databases", "GET", async_req=True)
        second_call = api_client.call_api(fake_root, "/api/v2/databases", "GET", async_req=True)

    assert isinstance(first_call, Future)
    assert first_call.running()
    assert not first_call.done()

    assert isinstance(second_call, Future)
    assert not second_call.running()
    assert not second_call.done()


def test_parameters_to_url_query_encodes_special_characters(fake_root):
    api_client = ApiClient(fake_root)

    # Scalar value with &, # and = characters
    result = api_client.parameters_to_url_query(
        [("targetName", "VICTIM&targetDatabase=PROD#"), ("targetDatabase", "SAFE")],
        {},
    )
    assert result == "targetName=VICTIM%26targetDatabase%3DPROD%23&targetDatabase=SAFE"

    # Multi-collection values: v is a list, each element emitted as a separate key=value pair
    result = api_client.parameters_to_url_query(
        [("tag", ["a&b", "c#d"])],
        {"tag": "multi"},
    )
    assert result == "tag=a%26b&tag=c%23d"

    # Delimiter-joined collection: values are encoded, but the delimiter itself is not
    result = api_client.parameters_to_url_query(
        [("cols", ["a,b", "c"])],
        {"cols": "csv"},
    )
    assert result == "cols=a%2Cb,c"
