"""Functional transport checks against a local server; no performance measurements."""

from importlib.metadata import version
import asyncio
import gzip
import socket
import ssl
from contextlib import asynccontextmanager
from types import SimpleNamespace

import aiohttp
from aiohttp import web
import httpx
import pytest

from runta import ApiError, AsyncRunta
from runta._internal.async_http import _AsyncHttpClient
from runta._internal.retry import retryable_http_error


@asynccontextmanager
async def serve(handler):
    app = web.Application()
    app.router.add_route("*", "/{tail:.*}", handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
async def test_shared_session_encoding_binary_json_headers_and_compression(monkeypatch):
    seen = []

    async def handler(request):
        seen.append(
            (request.raw_path, request.headers, await request.read(), request.transport)
        )
        return web.Response(
            body=gzip.compress(b'{"ok":true}'),
            headers=[
                ("Content-Encoding", "gzip"),
                ("X-Multi", "one"),
                ("X-Multi", "two"),
                ("Set-Cookie", "session=one; Path=/"),
            ],
        )

    monkeypatch.setenv("HTTP_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:1")
    async with serve(handler) as endpoint:
        http = _AsyncHttpClient(endpoint + "/prefix", "token")
        try:
            assert http._session is None
            response = await http._send(
                {
                    "method": "PUT",
                    "url": "/v2/runtimes/id%2Fname/files",
                    "params": {"path": "/目录/a+b %", "revision": 3},
                    "content": b"\x00binary\xff",
                    "headers": {"Content-Type": "application/octet-stream"},
                }
            )
            assert response.json() == {"ok": True}
            assert response.headers.get_list("x-multi") == ["one", "two"]
            assert seen[0][0].startswith("/prefix/v2/runtimes/id%2Fname/files?")
            assert dict(httpx.URL(endpoint + seen[0][0]).params) == {
                "path": "/目录/a+b %",
                "revision": "3",
            }
            assert seen[0][1]["Authorization"] == "Bearer token"
            assert (
                seen[0][1]["User-Agent"] == f"runta-python-sdk/{version('runta-sdk')}"
            )
            assert seen[0][2] == b"\x00binary\xff"
            session = http._session
            await http._send(
                {
                    "method": "POST",
                    "url": "/json",
                    "json": {"text": "你好", "value": None},
                }
            )
            assert (
                seen[1][2]
                == httpx.Request(
                    "POST", endpoint, json={"text": "你好", "value": None}
                ).content
            )
            assert seen[1][1]["Cookie"] == "session=one"
            assert session.connector._ssl.verify_mode == ssl.CERT_REQUIRED
            assert session.connector._ssl.check_hostname
            assert seen[0][3] is seen[1][3]
            assert http._session is session
            assert http._client._async_client is None
            assert session._retry_connection is False
            assert session.trust_env is False
        finally:
            await http.close()
        assert session.closed


@pytest.mark.asyncio
async def test_redirect_is_not_followed():
    paths = []

    async def handler(request):
        paths.append(request.path)
        return web.Response(status=302, headers={"Location": "/target"})

    async with serve(handler) as endpoint:
        http = _AsyncHttpClient(endpoint, "token")
        try:
            response = await http._send({"method": "GET", "url": "/redirect"})
            assert response.status_code == 302
            assert paths == ["/redirect"]
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_total_timeout_includes_continuously_arriving_body():
    async def handler(request):
        response = web.StreamResponse()
        await response.prepare(request)
        try:
            for _ in range(20):
                await response.write(b"x")
                await asyncio.sleep(0.02)
        except (ConnectionResetError, RuntimeError):
            pass
        return response

    async with serve(handler) as endpoint:
        http = _AsyncHttpClient(endpoint, "token", timeout=1)
        try:
            with pytest.raises(ApiError) as raised:
                await http._send({"method": "GET", "url": "/slow"}, _timeout=0.08)
            assert isinstance(raised.value.__cause__, asyncio.TimeoutError)
            assert retryable_http_error(raised.value)
            assert not http._session.connector._acquired
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_pool_timeout_and_cancellation_release_resources():
    arrived = asyncio.Event()
    release = asyncio.Event()

    async def handler(request):
        arrived.set()
        await release.wait()
        return web.Response()

    async with serve(handler) as endpoint:
        http = _AsyncHttpClient(endpoint, "token", connection_pool_maxsize=1)
        first = asyncio.create_task(http.health())
        try:
            await asyncio.wait_for(arrived.wait(), 2)
            with pytest.raises(ApiError) as raised:
                await http._send({"method": "GET", "url": "/waiting"}, _timeout=0.05)
            assert isinstance(raised.value.__cause__, asyncio.TimeoutError)
            waiting = asyncio.create_task(http.health())
            await asyncio.sleep(0)
            waiting.cancel()
            with pytest.raises(asyncio.CancelledError):
                await waiting
            first.cancel()
            with pytest.raises(asyncio.CancelledError):
                await first
            assert not http._session.connector._acquired
            release.set()
            assert await http.health()
        finally:
            release.set()
            first.cancel()
            await asyncio.gather(first, return_exceptions=True)
            await http.close()


@pytest.mark.asyncio
async def test_close_unused_and_repeated_close_never_create_session():
    http = _AsyncHttpClient("http://localhost", "token")
    await http.close()
    await http.close()
    assert http._session is None
    with pytest.raises(RuntimeError, match="closed"):
        await http.health()


@pytest.mark.asyncio
async def test_cross_loop_use_and_close_are_rejected():
    http = _AsyncHttpClient("http://localhost", "token")
    http._get_session()

    async def other_loop():
        with pytest.raises(RuntimeError, match="owning event loop"):
            await http.health()
        with pytest.raises(RuntimeError, match="owning event loop"):
            await http.close()

    try:
        await asyncio.to_thread(lambda: asyncio.run(other_loop()))
        assert not http._session.closed
    finally:
        await http.close()


@pytest.mark.asyncio
async def test_persistent_disconnect_does_not_send_hidden_retry():
    requests = []
    handlers = set()

    async def handler(reader, writer):
        task = asyncio.current_task()
        handlers.add(task)
        try:
            requests.append(await reader.readuntil(b"\r\n\r\n"))
            writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")
            await writer.drain()
            requests.append(await reader.readuntil(b"\r\n\r\n"))
            # Lose the response after receiving the second request.
        except asyncio.IncompleteReadError:
            pass
        finally:
            writer.close()
            await writer.wait_closed()
            handlers.remove(task)

    server = await asyncio.start_server(handler, "127.0.0.1", 0)
    endpoint = f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"
    try:
        async with AsyncRunta(endpoint=endpoint, token="token") as client:
            assert await client.health()
            with pytest.raises(ApiError) as raised:
                await client.health()
            assert isinstance(raised.value.__cause__, aiohttp.ServerDisconnectedError)
            assert len(requests) == 2
    finally:
        server.close()
        await server.wait_closed()
        await asyncio.gather(*list(handlers))


@pytest.mark.asyncio
async def test_truncated_body_maps_to_retryable_api_error():
    async def handler(request):
        response = web.StreamResponse(headers={"Content-Length": "100"})
        await response.prepare(request)
        await response.write(b"partial")
        request.transport.close()
        return response

    async with serve(handler) as endpoint:
        http = _AsyncHttpClient(endpoint, "token")
        try:
            with pytest.raises(ApiError) as raised:
                await http.health()
            assert isinstance(raised.value.__cause__, aiohttp.ClientPayloadError)
            assert retryable_http_error(raised.value)
        finally:
            await http.close()


KEY = SimpleNamespace(host="host", port=443, ssl=True, is_ssl=True)


@pytest.mark.parametrize(
    ("cause", "expected"),
    [
        (TimeoutError(), True),
        (asyncio.TimeoutError(), True),
        (aiohttp.ServerDisconnectedError(), True),
        (aiohttp.ClientPayloadError("truncated"), True),
        (
            aiohttp.ClientConnectorError(KEY, ConnectionRefusedError(111, "refused")),
            True,
        ),
        (
            aiohttp.ClientConnectorDNSError(
                KEY, socket.gaierror(socket.EAI_AGAIN, "temporary")
            ),
            True,
        ),
        (
            aiohttp.ClientConnectorDNSError(
                KEY, socket.gaierror(socket.EAI_NONAME, "unknown")
            ),
            False,
        ),
        (
            aiohttp.ClientConnectorDNSError(
                KEY, socket.gaierror(socket.EAI_FAIL, "permanent")
            ),
            False,
        ),
        (aiohttp.ClientConnectorSSLError(KEY, ssl.SSLError("TLS")), False),
        (
            aiohttp.ClientConnectorCertificateError(
                KEY, ssl.SSLCertVerificationError("certificate")
            ),
            False,
        ),
        (aiohttp.InvalidURL("invalid"), False),
        (ValueError("JSON"), False),
    ],
)
def test_aiohttp_retry_classification(cause, expected):
    error = ApiError("failed")
    error.__cause__ = cause
    assert retryable_http_error(error) is expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cause",
    [
        aiohttp.ServerDisconnectedError(),
        aiohttp.ClientPayloadError("truncated"),
        aiohttp.ClientConnectorDNSError(
            KEY, socket.gaierror(socket.EAI_NONAME, "unknown")
        ),
        aiohttp.ClientConnectorCertificateError(
            KEY, ssl.SSLCertVerificationError("certificate")
        ),
        aiohttp.InvalidURL("invalid"),
        asyncio.TimeoutError(),
    ],
)
async def test_send_preserves_network_error_cause(cause):
    http = _AsyncHttpClient("http://localhost", "token")

    async def fail(request, timeout):
        raise cause

    http._send_request = fail
    try:
        with pytest.raises(ApiError) as raised:
            await http._send({"method": "GET", "url": "/"})
        assert raised.value.__cause__ is cause
    finally:
        await http.close()


@pytest.mark.asyncio
async def test_expired_deadline_does_not_disable_timeout_or_create_session():
    http = _AsyncHttpClient("http://localhost", "token")
    try:
        with pytest.raises(ApiError) as raised:
            await http._send({"method": "GET", "url": "/"}, _timeout=0)
        assert isinstance(raised.value.__cause__, TimeoutError)
        assert http._session is None
    finally:
        await http.close()


@pytest.mark.asyncio
async def test_malformed_response_maps_to_retryable_protocol_error():
    async def handler(reader, writer):
        try:
            await reader.readuntil(b"\r\n\r\n")
            writer.write(b"HTTP/1.1 invalid OK\r\nContent-Length: 0\r\n\r\n")
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(handler, "127.0.0.1", 0)
    endpoint = f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"
    try:
        async with AsyncRunta(endpoint=endpoint, token="token") as client:
            with pytest.raises(ApiError) as raised:
                await client.health()
            assert retryable_http_error(raised.value)
    finally:
        server.close()
        await server.wait_closed()
