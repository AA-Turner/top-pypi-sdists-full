from concurrent.futures import Future
from unittest import mock

import pytest

import snowflake.core._thread_pool as thread_pool

from snowflake.core._internal.snowapi_parameters import SnowApiParameter, SnowApiParameters
from snowflake.core.database._generated import ApiClient


@pytest.fixture(autouse=True)
def reset_pool():
    thread_pool.THREAD_POOL.reset()


def test_async_api_calls_are_submitted_to_the_pool(fake_root, event):
    fake_root.parameters.return_value = SnowApiParameters({SnowApiParameter.MAX_THREADS: "1"})
    api_client = ApiClient(fake_root)
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        mocked_request.side_effect = lambda *args, **kwargs: event.wait()
        first_call = api_client.call_api(fake_root, "/api/v2/databases", "GET", async_req=True)
        second_call = api_client.call_api(fake_root, "/api/v2/databases", "GET", async_req=True)

    assert isinstance(first_call, Future)
    assert first_call.running()
    assert not first_call.done()

    assert isinstance(second_call, Future)
    assert not second_call.running()
    assert not second_call.done()
