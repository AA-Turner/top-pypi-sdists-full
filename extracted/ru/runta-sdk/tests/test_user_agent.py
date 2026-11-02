"""REST and WebSocket transports identify the installed SDK distribution."""

import asyncio
from importlib.metadata import version

import httpx
import pytest
from websockets.asyncio.server import serve

from runta._internal.sync_http import _SyncHttpClient
from runta._internal.streaming_transfer import _async_socket, _sync_socket


def test_sync_rest_user_agent():
    requests = []

    def handle(request):
        requests.append(request)
        return httpx.Response(200, json={})

    client = _SyncHttpClient("http://runta.test", "token")
    client._client._httpx_args["transport"] = httpx.MockTransport(handle)
    try:
        client._client.get_httpx_client().get("/healthz")
        assert requests[0].headers["User-Agent"] == (
            f"runta-python-sdk/{version('runta-sdk')}"
        )
        assert requests[0].headers["Authorization"] == "Bearer token"
    finally:
        client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
async def test_websocket_handshake_user_agent(sync):
    seen = []

    async def handle(socket):
        seen.append(socket.request.headers)
        await socket.close()

    async with serve(handle, "127.0.0.1", 0) as server:
        endpoint = f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"
        if sync:

            def connect():
                with _sync_socket(endpoint, "token", "runtime-id", 2):
                    pass

            await asyncio.to_thread(connect)
        else:
            async with _async_socket(endpoint, "token", "runtime-id", 2):
                pass
    assert len(seen) == 1
    assert seen[0].get_all("User-Agent") == [f"runta-python-sdk/{version('runta-sdk')}"]
    assert seen[0]["Authorization"] == "Bearer token"


@pytest.mark.parametrize("source_available", [False, True])
def test_source_only_version_fallback(monkeypatch, tmp_path, source_available):
    from importlib.metadata import PackageNotFoundError
    from runta._internal import user_agent

    def missing(_name):
        raise PackageNotFoundError("runta-sdk")

    source = tmp_path / "src/runta/_internal/user_agent.py"
    source.parent.mkdir(parents=True)
    source.touch()
    if source_available:
        (tmp_path / "pyproject.toml").write_text('[project]\nversion = "1.2.3.dev4"\n')
    monkeypatch.setattr(user_agent, "version", missing)
    monkeypatch.setattr(user_agent, "__file__", str(source))
    assert user_agent._sdk_version() == (
        "1.2.3.dev4" if source_available else "unknown"
    )
