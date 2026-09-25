import json

from concurrent.futures import Future
from unittest import mock

import pytest

import snowflake.core._thread_pool as thread_pool

from snowflake.core._generated import ApiClient
from snowflake.core._internal.snowapi_parameters import SnowApiParameter, SnowApiParameters
from snowflake.core.exceptions import InvalidResponseError


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


def _fake_response(status, location=None):
    response = mock.MagicMock()
    response.status = status
    response.getheader.return_value = location
    return response


def test_request_with_retry_rejects_userinfo_location_header(fake_root):
    api_client = ApiClient(fake_root)
    accepted = _fake_response(202, location="@attacker.example/api/v2/results/x")
    with mock.patch.object(ApiClient, "request", return_value=accepted):
        with pytest.raises(InvalidResponseError, match="Unexpected Location header"):
            api_client.request_with_retry(fake_root, "GET", "/api/v2/databases")


def test_request_with_retry_accepts_relative_location_header(fake_root):
    api_client = ApiClient(fake_root)
    accepted = _fake_response(202, location="/api/v2/results/x")
    done = _fake_response(200)
    with (
        mock.patch.object(ApiClient, "request", side_effect=[accepted, done]) as mocked_request,
        mock.patch("snowflake.core._generated.api_client.time.sleep"),
    ):
        result = api_client.request_with_retry(fake_root, "GET", "/api/v2/databases")
    assert result is done
    second_call_url = mocked_request.call_args_list[1].args[2]
    assert second_call_url == "http://localhost:80/api/v2/results/x"


def test_call_api_rejects_userinfo_large_results_link(fake_root):
    api_client = ApiClient(fake_root)
    malicious = mock.MagicMock()
    malicious.status = 200
    malicious.getheaders.return_value = {"Link": '<@attacker.example/api/v2/results/x?page=0>; rel="last"'}
    with mock.patch.object(ApiClient, "request_with_retry", return_value=malicious):
        with pytest.raises(InvalidResponseError, match="Unexpected large-results path"):
            api_client.call_api(fake_root, "/api/v2/databases", "GET", response_types_map={"200": "str"})


def test_call_api_fetches_large_results_chunk_with_relative_link(fake_root):
    api_client = ApiClient(fake_root)
    accepted = mock.MagicMock()
    accepted.status = 200
    accepted.getheaders.return_value = {"Link": '</api/v2/results/x?page=0>; rel="last"'}
    accepted.data = json.dumps({"result_handler": "abc", "message": "Large result set. Use provided Link header."})
    chunk = mock.MagicMock()
    chunk.status = 200
    with mock.patch.object(ApiClient, "request_with_retry", side_effect=[accepted, chunk]) as mocked_retry:
        result = api_client.call_api(
            fake_root, "/api/v2/databases", "GET", response_types_map={"200": "str"}, _return_http_data_only=True
        )
    assert result is chunk
    chunk_call_url = mocked_retry.call_args_list[1].args[2]
    assert chunk_call_url == "http://localhost:80/api/v2/results/x?page=0"
