"""Real async WebSocket TLS handshakes; no performance measurements."""

import asyncio
from contextlib import asynccontextmanager
import ssl
from urllib.parse import urlsplit

from aiohttp import web
import pytest
from websockets.exceptions import InvalidStatus

from test_rest_tls import certificates as certificates, server_context
from runta import AsyncRunta, AsyncRuntime, RuntimeInfo
from runta._internal.async_http import _AsyncHttpClient
from runta._internal.rest_tls import _RestTLS
from runta._internal.streaming_transfer import _async_socket, _WebSocketTLS


@pytest.fixture
def system_ca(certificates, monkeypatch):
    monkeypatch.setenv("SSL_CERT_FILE", str(certificates / "trusted.pem"))
    monkeypatch.setenv("SSL_CERT_DIR", str(certificates / "empty"))
    return certificates


@asynccontextmanager
async def websocket_server(context=None, *, reject=False):
    seen = []
    active = set()

    async def handler(request):
        transport = request.transport
        tls = transport.get_extra_info("ssl_object")
        seen.append((tls.session_reused if tls else False, transport))
        assert request.headers["Authorization"] == "Bearer token"
        if reject:
            return web.Response(status=503)
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        active.add(ws)
        try:
            async for message in ws:
                await ws.send_str(message.data)
        finally:
            active.discard(ws)
        return ws

    app = web.Application()
    app.router.add_get("/{tail:.*}", handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0, ssl_context=context)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]
    try:
        yield f"{'https' if context else 'http'}://localhost:{port}", seen, active
    finally:
        for ws in list(active):
            await ws.close()
        await runner.cleanup()


async def exchange(http, endpoint=None, runtime_id="runtime-1"):
    async with _async_socket(
        endpoint or http.endpoint,
        http.token,
        runtime_id,
        2,
        _tls=http._websocket_tls,
    ) as socket:
        await socket.send("hello")
        assert await socket.recv() == "hello"
        return socket.transport.get_extra_info("ssl_object")


@pytest.mark.asyncio
@pytest.mark.parametrize("version", [ssl.TLSVersion.TLSv1_2, ssl.TLSVersion.TLSv1_3])
async def test_real_websocket_connections_resume(system_ca, version):
    async with websocket_server(server_context(system_ca, version)) as (
        endpoint,
        seen,
        _,
    ):
        http = _AsyncHttpClient(endpoint, "token")
        try:
            assert http._websocket_tls._resumption is None
            for runtime_id in ("runtime-1", "runtime-2", "runtime-1"):
                tls = await exchange(http, runtime_id=runtime_id)
                assert tls.version() == version.name.replace("TLSv1_", "TLSv1.")
            assert [reused for reused, _ in seen] == [False, True, True]
            assert len({id(transport) for _, transport in seen}) == 3
            assert http._session is None
            assert http._rest_tls is None
            cache = http._websocket_tls._resumption
            assert len(cache._sessions) == 1
        finally:
            await http.close()
        assert not cache._sessions and not cache._contexts
        with pytest.raises(RuntimeError, match="closed"):
            await exchange(http)
        await http.close()


@pytest.mark.asyncio
async def test_no_ticket_uses_full_handshake(system_ca):
    async with websocket_server(
        server_context(system_ca, ssl.TLSVersion.TLSv1_3, tickets=0)
    ) as (endpoint, seen, _):
        http = _AsyncHttpClient(endpoint, "token")
        try:
            await exchange(http)
            await exchange(http)
            assert [reused for reused, _ in seen] == [False, False]
            assert not http._websocket_tls._resumption._sessions
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_origin_and_rest_caches_are_isolated(system_ca, monkeypatch):
    async with (
        websocket_server(server_context(system_ca, ssl.TLSVersion.TLSv1_3)) as (
            first,
            seen_first,
            _,
        ),
        websocket_server(server_context(system_ca, ssl.TLSVersion.TLSv1_3)) as (
            second,
            seen_second,
            _,
        ),
    ):
        http = _AsyncHttpClient(first, "token")
        try:
            await exchange(http)
            await exchange(http, second)
            await exchange(http)
            assert [r for r, _ in seen_first] == [False, True]
            assert [r for r, _ in seen_second] == [False]
            monkeypatch.setattr("certifi.where", lambda: str(system_ca / "trusted.pem"))
            http._rest_tls = _RestTLS()
            url = urlsplit(first)
            rest_context = http._rest_tls.context(url.hostname, url.port)
            ws_cache = http._websocket_tls._resumption
            assert rest_context is not ws_cache.context(url.hostname, url.port)
            assert not http._rest_tls._sessions
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_concurrent_ticket_consumption(system_ca, monkeypatch):
    async with websocket_server(
        server_context(system_ca, ssl.TLSVersion.TLSv1_3, tickets=1)
    ) as (endpoint, seen, _):
        http = _AsyncHttpClient(endpoint, "token")
        try:
            await exchange(http)
            cache = http._websocket_tls._resumption
            initial = next(iter(cache._sessions.values()))[1].id
            offered = []
            take = cache.take

            def observe(context):
                session = take(context)
                if session:
                    offered.append(session.id)
                return session

            monkeypatch.setattr(cache, "take", observe)
            await asyncio.gather(*(exchange(http) for _ in range(3)))
            assert len(seen) == 4
            assert offered.count(initial) == 1
            assert len(offered) == len(set(offered))
            assert any(reused for reused, _ in seen[1:])
        finally:
            await http.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["certificate", "hostname"])
async def test_certificate_checks(system_ca, failure):
    context = server_context(
        system_ca,
        ssl.TLSVersion.TLSv1_3,
        name="other" if failure == "certificate" else "trusted",
    )
    async with websocket_server(context) as (endpoint, seen, _):
        http = _AsyncHttpClient(
            endpoint.replace("localhost", "127.0.0.1")
            if failure == "hostname"
            else endpoint,
            "token",
        )
        try:
            with pytest.raises(ssl.SSLCertVerificationError):
                await exchange(http)
            assert not seen
            assert not http._websocket_tls._resumption._sessions
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_upgrade_failure_does_not_reconnect(system_ca):
    async with websocket_server(
        server_context(system_ca, ssl.TLSVersion.TLSv1_3), reject=True
    ) as (endpoint, seen, _):
        http = _AsyncHttpClient(endpoint, "token")
        try:
            with pytest.raises(InvalidStatus):
                await exchange(http)
            assert len(seen) == 1
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_server_rejects_old_ticket(system_ca):
    original = server_context(system_ca, ssl.TLSVersion.TLSv1_3)
    replacement = server_context(system_ca, ssl.TLSVersion.TLSv1_3)
    rotate = [False]

    def choose(*args, **kwargs):
        return ssl.SSLContext.wrap_bio(
            replacement if rotate[0] else original, *args, **kwargs
        )

    original.wrap_bio = choose
    async with websocket_server(original) as (endpoint, seen, _):
        http = _AsyncHttpClient(endpoint, "token")
        try:
            await exchange(http)
            rotate[0] = True
            await exchange(http)
            await exchange(http)
            assert [r for r, _ in seen] == [False, False, True]
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_unusable_session_falls_back_without_extra_upgrade(system_ca):
    async with websocket_server(server_context(system_ca, ssl.TLSVersion.TLSv1_3)) as (
        endpoint,
        seen,
        _,
    ):
        http = _AsyncHttpClient(endpoint, "token")
        other = _AsyncHttpClient(endpoint, "token")
        try:
            await exchange(http)
            await exchange(other)
            url = urlsplit(endpoint)
            cache = http._websocket_tls._resumption
            current = cache.context(url.hostname, url.port)
            foreign_cache = other._websocket_tls._resumption
            foreign = foreign_cache.context(url.hostname, url.port)
            cache.take(current)
            cache.save(current, foreign_cache.take(foreign))
            await exchange(http)
            assert [r for r, _ in seen] == [False, False, False]
        finally:
            await http.close()
            await other.close()


@pytest.mark.asyncio
async def test_cancellation_releases_socket(system_ca):
    async with websocket_server(server_context(system_ca, ssl.TLSVersion.TLSv1_3)) as (
        endpoint,
        _,
        active,
    ):
        http = _AsyncHttpClient(endpoint, "token")
        connected = asyncio.Event()

        async def wait():
            async with _async_socket(
                endpoint, "token", "runtime", 2, _tls=http._websocket_tls
            ) as ws:
                connected.set()
                await ws.recv()

        task = asyncio.create_task(wait())
        try:
            await asyncio.wait_for(connected.wait(), 2)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            for _ in range(100):
                if not active:
                    break
                await asyncio.sleep(0.01)
            assert not active
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
            await http.close()
        assert not http._websocket_tls._resumption._sessions


@pytest.mark.asyncio
async def test_plain_websocket_and_unused_close_do_not_create_tls():
    async with websocket_server() as (endpoint, _, _):
        http = _AsyncHttpClient(endpoint, "token")
        await exchange(http)
        assert http._websocket_tls._resumption is None
        await http.close()
    unused = _AsyncHttpClient("https://localhost", "token")
    await unused.close()
    assert unused._websocket_tls._resumption is None
    with pytest.raises(RuntimeError, match="closed"):
        unused._websocket_tls.context("localhost", 443)


def test_websocket_first_use_binds_loop():
    http = _AsyncHttpClient("https://localhost", "token")
    first = asyncio.new_event_loop()
    second = asyncio.new_event_loop()

    async def bind():
        http._websocket_tls.prepare()

    async def rest():
        http._get_session()

    try:
        first.run_until_complete(bind())
        with pytest.raises(RuntimeError, match="owning event loop"):
            second.run_until_complete(bind())
        with pytest.raises(RuntimeError, match="owning event loop"):
            second.run_until_complete(rest())
        with pytest.raises(RuntimeError, match="owning event loop"):
            second.run_until_complete(http.close())
        first.run_until_complete(http.close())
    finally:
        first.close()
        second.close()


def test_sync_websocket_context_is_unchanged():
    tls = _WebSocketTLS()
    context = tls.context()
    assert context is tls.context()
    assert context.sslobject_class is ssl.SSLObject


@pytest.mark.asyncio
async def test_runtime_handles_share_owner_tls(system_ca):
    async with websocket_server(server_context(system_ca, ssl.TLSVersion.TLSv1_3)) as (
        endpoint,
        seen,
        _,
    ):
        async with AsyncRunta(endpoint=endpoint, token="token") as client:
            for runtime_id in ("one", "two"):
                info = RuntimeInfo.from_json(
                    {
                        "id": runtime_id,
                        "display_name": runtime_id,
                        "resources": {
                            "requests": {"vcpus": 1, "memory_mib": 1024},
                            "limits": {"memory_mib": 1024},
                        },
                        "status": "running",
                    }
                )
                runtime = AsyncRuntime._from_info(client, info)
                assert runtime._client._http is client._http
                await exchange(runtime._client._http, runtime_id=runtime.id)
            assert [r for r, _ in seen] == [False, True]


@pytest.mark.asyncio
async def test_websocket_trust_uses_system_ca(system_ca, monkeypatch):
    def unexpected_certifi():
        raise AssertionError("WebSocket must retain the system CA source")

    monkeypatch.setattr("certifi.where", unexpected_certifi)
    async with websocket_server(server_context(system_ca, ssl.TLSVersion.TLSv1_3)) as (
        endpoint,
        _,
        _,
    ):
        http = _AsyncHttpClient(endpoint, "token")
        try:
            await exchange(http)
        finally:
            await http.close()
