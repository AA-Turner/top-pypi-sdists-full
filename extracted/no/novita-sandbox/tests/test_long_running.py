import json

import httpx
import pytest
import pytest_asyncio

from novita_sandbox.core import AsyncSandbox, Sandbox
from novita_sandbox.core.api.client.client import AuthenticatedClient
from novita_sandbox.core.sandbox_async import sandbox_api as async_api
from novita_sandbox.core.sandbox_sync import sandbox_api as sync_api


@pytest_asyncio.fixture
async def create_requests(monkeypatch):
    requests = []

    def handle(request):
        assert request.method == "POST"
        assert request.url.path == "/sandboxes"
        requests.append(json.loads(request.content))
        return httpx.Response(
            201,
            json={
                "sandboxID": "sandbox-id",
                "envdVersion": "0.5.7",
                "templateID": "base",
                "clientID": "client-id",
            },
        )

    transport = httpx.MockTransport(handle)
    sync_client = httpx.Client(base_url="https://test.invalid", transport=transport)
    async_client = httpx.AsyncClient(base_url="https://test.invalid", transport=transport)
    client = AuthenticatedClient(base_url="https://test.invalid", token="test-key")
    client.set_httpx_client(sync_client)
    client.set_async_httpx_client(async_client)
    monkeypatch.setattr(sync_api, "get_api_client", lambda _: client)
    monkeypatch.setattr(async_api, "get_api_client", lambda _: client)
    yield requests
    sync_client.close()
    await async_client.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize("domain", ["sandbox.novita.ai", "us-phx-1.sandbox.novita.ai"])
@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("timeout", [None, 90, 0])
@pytest.mark.parametrize("idle_timeout", [None, "60", "0", ""])
async def test_long_running_preserves_explicit_idle_timeout(
    create_requests, domain, asynchronous, timeout, idle_timeout
):
    metadata = {"long_running": "true", "purpose": "worker"}
    if idle_timeout is not None:
        metadata["idle_timeout"] = idle_timeout
    original_metadata = metadata.copy()
    kwargs = dict(
        api_key="test-key", debug=False, domain=domain, metadata=metadata, timeout=timeout
    )
    if asynchronous:
        await AsyncSandbox.create("base", **kwargs)
    else:
        Sandbox.create("base", **kwargs)

    assert len(create_requests) == 1
    body = create_requests[0]
    assert "timeout" not in body
    assert body["metadata"] == original_metadata
    assert metadata == original_metadata
    if idle_timeout is None:
        assert "idle_timeout" not in body["metadata"]
    else:
        assert body["metadata"]["idle_timeout"] == idle_timeout


@pytest.mark.asyncio
@pytest.mark.parametrize("domain", ["sandbox.novita.ai", "us-phx-1.sandbox.novita.ai"])
@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("long_running", [None, "false", "TRUE", "1", ""])
async def test_other_metadata_preserves_timeouts(
    create_requests, domain, asynchronous, long_running
):
    metadata = {"idle_timeout": "60"}
    if long_running is not None:
        metadata["long_running"] = long_running
    kwargs = dict(
        api_key="test-key", debug=False, domain=domain, metadata=metadata, timeout=90
    )
    if asynchronous:
        await AsyncSandbox.create("base", **kwargs)
    else:
        Sandbox.create("base", **kwargs)

    assert len(create_requests) == 1
    assert create_requests[0]["timeout"] == 90
    assert create_requests[0]["metadata"] == metadata
