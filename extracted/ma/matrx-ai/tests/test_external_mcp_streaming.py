from __future__ import annotations

import asyncio
import json

import httpx
import pytest

from matrx_ai.tools import external_mcp
from matrx_ai.tools.external_mcp import ExternalMCPClient


class _SseStream(httpx.AsyncByteStream):
    def __init__(self, chunks: list[bytes], *, tail_error: Exception | None = None) -> None:
        self.chunks = chunks
        self.tail_error = tail_error
        self.closed = False

    async def __aiter__(self):
        for chunk in self.chunks:
            yield chunk
        if self.tail_error is not None:
            raise self.tail_error

    async def aclose(self) -> None:
        self.closed = True


async def _post(stream: httpx.AsyncByteStream, *, operation_timeout: float = 1.0):
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            stream=stream,
            request=request,
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        return await ExternalMCPClient(timeout=operation_timeout)._post_rpc(
            client,
            "https://mcp.example.test/mcp",
            {"jsonrpc": "2.0", "id": 7, "method": "tools/list", "params": {}},
            {"Accept": "application/json, text/event-stream"},
        )


@pytest.mark.asyncio
async def test_sse_returns_matching_response_and_closes_without_waiting_for_eof() -> None:
    payload = {"jsonrpc": "2.0", "id": 7, "result": {"tools": []}}
    stream = _SseStream(
        [f"data: {json.dumps(payload)}\n\n".encode()],
        tail_error=httpx.ReadTimeout("SSE connection remains open"),
    )
    result, _, _ = await _post(stream)
    assert result == payload
    assert stream.closed is True


@pytest.mark.asyncio
async def test_sse_ignores_progress_requests_and_mismatched_response_ids() -> None:
    expected = {"jsonrpc": "2.0", "id": 7, "result": {"tools": []}}
    stream = _SseStream(
        [
            b'data: {"jsonrpc":"2.0","method":"notifications/progress"}\n\n',
            b'data: {"jsonrpc":"2.0","id":"7","result":{"wrong_type":true}}\n\n',
            b'data: {"jsonrpc":"2.0","id":8,"result":{"wrong_id":true}}\n\n',
            b'data: {"jsonrpc":"2.0","id":99,"method":"sampling/createMessage"}\n\n',
            f"data: {json.dumps(expected)}\n\n".encode(),
        ]
    )
    result, _, _ = await _post(stream)
    assert result == expected
    assert stream.closed is True


@pytest.mark.asyncio
async def test_sse_assembles_multiline_data_at_blank_event_boundary() -> None:
    stream = _SseStream(
        [
            b'data: {"jsonrpc":"2.0",\n',
            b'data: "id":7,\n',
            b'data: "result":{"tools":[]}}\n\n',
        ]
    )
    result, _, _ = await _post(stream)
    assert result == {"jsonrpc": "2.0", "id": 7, "result": {"tools": []}}


@pytest.mark.asyncio
async def test_sse_rejects_oversized_single_event(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(external_mcp, "MCP_SSE_EVENT_MAX_BYTES", 24)
    stream = _SseStream([b"data: " + b"x" * 30 + b"\n\n"])
    with pytest.raises(RuntimeError, match="event exceeded"):
        await _post(stream)
    assert stream.closed is True


@pytest.mark.asyncio
async def test_sse_rejects_oversized_cumulative_stream(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(external_mcp, "MCP_RPC_RESPONSE_MAX_BYTES", 40)
    stream = _SseStream([b": keepalive 1234567890\n\n", b": keepalive 1234567890\n\n"])
    with pytest.raises(RuntimeError, match="cumulative size"):
        await _post(stream)
    assert stream.closed is True


@pytest.mark.asyncio
async def test_sse_rejects_excessive_event_count(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(external_mcp, "MCP_SSE_MAX_EVENTS", 1)
    stream = _SseStream(
        [
            b'data: {"jsonrpc":"2.0","method":"notifications/progress"}\n\n',
            b'data: {"jsonrpc":"2.0","id":7,"result":{}}\n\n',
        ]
    )
    with pytest.raises(RuntimeError, match="event count"):
        await _post(stream)
    assert stream.closed is True


@pytest.mark.asyncio
async def test_sse_has_absolute_deadline_despite_slow_drip() -> None:
    class _SlowDrip(httpx.AsyncByteStream):
        def __init__(self) -> None:
            self.closed = False

        async def __aiter__(self):
            while True:
                await asyncio.sleep(0.01)
                yield b": keepalive\n\n"

        async def aclose(self) -> None:
            self.closed = True

    stream = _SlowDrip()
    with pytest.raises(TimeoutError):
        await _post(stream, operation_timeout=0.035)
    assert stream.closed is True


@pytest.mark.asyncio
async def test_json_response_is_bounded_and_request_correlated() -> None:
    payload = {"jsonrpc": "2.0", "id": 7, "result": {"tools": []}}

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result, _, _ = await ExternalMCPClient()._post_rpc(
            client, "https://example.test", {"id": 7}, {"Accept": "application/json"}
        )
    assert result == payload


@pytest.mark.asyncio
async def test_post_rpc_follows_same_origin_308_and_returns_canonical_endpoint() -> None:
    requests: list[str] = []
    payload = {"jsonrpc": "2.0", "id": 7, "result": {"tools": []}}

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(str(request.url))
        if request.url.path == "/mcp":
            return httpx.Response(308, headers={"location": "/mcp/"}, request=request)
        return httpx.Response(200, json=payload, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result, _, canonical_url = await ExternalMCPClient()._post_rpc(
            client,
            "https://docs.livekit.io/mcp",
            {"jsonrpc": "2.0", "id": 7, "method": "tools/list", "params": {}},
            {"Accept": "application/json"},
        )

    assert result == payload
    assert canonical_url == "https://docs.livekit.io/mcp/"
    assert requests == ["https://docs.livekit.io/mcp", "https://docs.livekit.io/mcp/"]


@pytest.mark.asyncio
async def test_send_reuses_canonical_endpoint_for_initialized_and_tool_call() -> None:
    requests: list[tuple[str, str, dict[str, str]]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        requests.append((request.url.path, body["method"], dict(request.headers)))
        if request.url.path == "/mcp":
            return httpx.Response(308, headers={"location": "/mcp/"}, request=request)
        if body["method"] == "initialize":
            return httpx.Response(
                200,
                headers={"mcp-session-id": "session-1"},
                json={
                    "jsonrpc": "2.0",
                    "id": body["id"],
                    "result": {"protocolVersion": "2025-06-18"},
                },
                request=request,
            )
        if body["method"] == "notifications/initialized":
            return httpx.Response(202, request=request)
        return httpx.Response(
            200,
            json={"jsonrpc": "2.0", "id": body["id"], "result": {"tools": []}},
            request=request,
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        client_mcp = ExternalMCPClient()
        session_id, protocol_version, canonical_url = await client_mcp._handshake(
            client,
            "https://docs.livekit.io/mcp",
            {"Authorization": "Bearer trusted-token"},
        )
        data, _, _ = await client_mcp._post_rpc(
            client,
            canonical_url,
            client_mcp._build_request("tools/list", {}),
            {
                "Authorization": "Bearer trusted-token",
                "MCP-Protocol-Version": protocol_version,
                "Mcp-Session-Id": session_id or "",
            },
        )

    assert data["result"] == {"tools": []}
    assert [(path, method) for path, method, _ in requests] == [
        ("/mcp", "initialize"),
        ("/mcp/", "initialize"),
        ("/mcp/", "notifications/initialized"),
        ("/mcp/", "tools/list"),
    ]
    assert all(headers["authorization"] == "Bearer trusted-token" for _, _, headers in requests)
    assert all(headers["content-type"].startswith("application/json") for _, _, headers in requests)


@pytest.mark.asyncio
async def test_post_rpc_refuses_cross_origin_redirect_before_forwarding_headers() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(308, headers={"location": "https://evil.example/mcp"}, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(RuntimeError, match="different origin"):
            await ExternalMCPClient()._post_rpc(
                client,
                "https://mcp.example.test/mcp",
                {"jsonrpc": "2.0", "id": 7, "method": "tools/list", "params": {}},
                {"Authorization": "Bearer should-not-leak"},
            )

    assert len(requests) == 1


@pytest.mark.asyncio
async def test_post_rpc_redirect_chain_obeys_one_absolute_deadline() -> None:
    """Redirect hops cannot multiply the configured RPC timeout."""

    async def handler(request: httpx.Request) -> httpx.Response:
        await asyncio.sleep(0.03)
        return httpx.Response(308, headers={"location": "/mcp/"}, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(TimeoutError):
            await ExternalMCPClient(timeout=0.05)._post_rpc(
                client,
                "https://mcp.example.test/mcp",
                {"jsonrpc": "2.0", "id": 7, "method": "tools/list", "params": {}},
                {"Authorization": "Bearer trusted-token"},
            )


@pytest.mark.asyncio
async def test_json_rejects_mismatched_id_and_oversized_body(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    responses = [
        {"jsonrpc": "2.0", "id": "7", "result": {}},
        {"jsonrpc": "2.0", "id": 7, "result": {"padding": "x" * 100}},
    ]

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=responses.pop(0), request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        mcp = ExternalMCPClient()
        with pytest.raises(RuntimeError, match="mismatched"):
            await mcp._post_rpc(
                client, "https://example.test", {"id": 7}, {"Accept": "application/json"}
            )
        monkeypatch.setattr(external_mcp, "MCP_RPC_RESPONSE_MAX_BYTES", 40)
        with pytest.raises(RuntimeError, match="maximum size"):
            await mcp._post_rpc(
                client, "https://example.test", {"id": 7}, {"Accept": "application/json"}
            )
