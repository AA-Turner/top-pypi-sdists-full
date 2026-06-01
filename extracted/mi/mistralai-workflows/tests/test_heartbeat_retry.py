"""Unit tests for the heartbeat retry policy via PrivateWorkerClient."""

import json
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.worker_client.errors import SDKDefaultError
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

HEARTBEAT_RESPONSE = {"workflow_registration_refs": [], "all_active": True}
_HEARTBEAT_REQUEST = httpx.Request("POST", "http://test/v1/workflows/workers/heartbeat")


def _make_response(status_code: int, body: dict | None = None, headers: dict | None = None) -> httpx.Response:
    content = json.dumps(body or HEARTBEAT_RESPONSE).encode()
    merged_headers = {"content-type": "application/json", **(headers or {})}
    response = httpx.Response(status_code, content=content, headers=merged_headers)
    response.request = _HEARTBEAT_REQUEST
    return response


@pytest.fixture
def client() -> PrivateWorkerClient:
    return get_worker_client(base_url="http://test")


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [408, 413, 429, 500, 502, 503, 504])
async def test_heartbeat_retries_on_transient_error(client: PrivateWorkerClient, status_code: int) -> None:
    """Heartbeat retries on transient status codes and succeeds on the next attempt."""
    responses = [_make_response(status_code), _make_response(200)]
    send_mock = AsyncMock(side_effect=responses)

    with patch.object(client.sdk_configuration.async_client, "send", send_mock):
        with patch("mistralai.workflows.worker_client.utils.retries.asyncio.sleep", new_callable=AsyncMock):
            await client.heartbeat_async(workflow_registration_refs=[])

    assert send_mock.call_count == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 422])
async def test_heartbeat_does_not_retry_on_client_errors(client: PrivateWorkerClient, status_code: int) -> None:
    """Heartbeat does not retry on non-transient 4xx errors."""
    send_mock = AsyncMock(return_value=_make_response(status_code))

    with patch.object(client.sdk_configuration.async_client, "send", send_mock):
        with pytest.raises((SDKDefaultError, Exception)):
            await client.heartbeat_async(workflow_registration_refs=[])

    assert send_mock.call_count == 1


@pytest.mark.asyncio
async def test_heartbeat_respects_retry_after_header(client: PrivateWorkerClient) -> None:
    """Heartbeat uses the Retry-After header value as the sleep duration."""
    responses = [
        _make_response(429, headers={"retry-after": "7"}),
        _make_response(200),
    ]
    send_mock = AsyncMock(side_effect=responses)
    sleep_calls: list[float] = []

    async def capture_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)

    with patch.object(client.sdk_configuration.async_client, "send", send_mock):
        with patch("mistralai.workflows.worker_client.utils.retries.asyncio.sleep", side_effect=capture_sleep):
            await client.heartbeat_async(workflow_registration_refs=[])

    assert sleep_calls[0] == pytest.approx(7.0)


@pytest.mark.asyncio
async def test_heartbeat_retries_on_network_error(client: PrivateWorkerClient) -> None:
    """Heartbeat retries on connection errors (retry_connection_errors=True)."""
    send_mock = AsyncMock(side_effect=[httpx.NetworkError("refused"), _make_response(200)])

    with patch.object(client.sdk_configuration.async_client, "send", send_mock):
        with patch("mistralai.workflows.worker_client.utils.retries.asyncio.sleep", new_callable=AsyncMock):
            await client.heartbeat_async(workflow_registration_refs=[])

    assert send_mock.call_count == 2
