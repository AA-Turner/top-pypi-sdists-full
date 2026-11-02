"""TLS functionality on independent local HTTPS connections, without benchmarks."""

import asyncio
from contextlib import asynccontextmanager
import ssl
import subprocess
from types import SimpleNamespace

from aiohttp import web
import pytest

from runta import ApiError
from runta._internal.async_http import _AsyncHttpClient
from runta._internal.rest_tls import _RestTLS
from runta._internal.tls_resumption import _MAX_SESSIONS


@pytest.fixture(scope="module")
def certificates(tmp_path_factory):
    directory = tmp_path_factory.mktemp("rest-tls")
    for name in ("trusted", "other"):
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                str(directory / f"{name}.key"),
                "-out",
                str(directory / f"{name}.pem"),
                "-days",
                "1",
                "-subj",
                "/CN=localhost",
                "-addext",
                "subjectAltName=DNS:localhost",
            ],
            check=True,
            capture_output=True,
        )
    return directory


@pytest.fixture
def trusted_ca(certificates, monkeypatch):
    monkeypatch.setattr("certifi.where", lambda: str(certificates / "trusted.pem"))
    return certificates


def server_context(certificates, version, name="trusted", tickets=2):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certificates / f"{name}.pem", certificates / f"{name}.key")
    context.minimum_version = context.maximum_version = version
    context.num_tickets = tickets
    return context


@asynccontextmanager
async def https_server(context, *, keepalive=False, block=None):
    seen = []

    async def handler(request):
        tls = request.transport.get_extra_info("ssl_object")
        seen.append((tls.version(), tls.session_reused, request.transport))
        if block is not None:
            await block.wait()
        return web.Response(headers={} if keepalive else {"Connection": "close"})

    app = web.Application()
    app.router.add_route("*", "/{tail:.*}", handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0, ssl_context=context)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]
    try:
        yield f"https://localhost:{port}", seen
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
@pytest.mark.parametrize("version", [ssl.TLSVersion.TLSv1_2, ssl.TLSVersion.TLSv1_3])
@pytest.mark.parametrize("trailing_dot", [False, True])
async def test_real_aiohttp_new_connections_resume(trusted_ca, version, trailing_dot):
    async with https_server(server_context(trusted_ca, version)) as (endpoint, seen):
        if trailing_dot:
            endpoint = endpoint.replace("localhost:", "localhost.:")
        http = _AsyncHttpClient(endpoint, "token")
        try:
            assert http._rest_tls is None
            for _ in range(3):
                assert await http.health()
            assert [reused for _, reused, _ in seen] == [False, True, True]
            assert len({id(transport) for _, _, transport in seen}) == 3
            assert all(
                actual == version.name.replace("TLSv1_", "TLSv1.")
                for actual, _, _ in seen
            )
            cache = http._rest_tls
            assert len(cache._sessions) == 1
        finally:
            await http.close()
        assert not cache._sessions
        assert not cache._contexts


@pytest.mark.asyncio
async def test_tls13_without_tickets_uses_full_handshakes(trusted_ca):
    async with https_server(
        server_context(trusted_ca, ssl.TLSVersion.TLSv1_3, tickets=0)
    ) as (endpoint, seen):
        http = _AsyncHttpClient(endpoint, "token")
        try:
            assert await http.health()
            assert await http.health()
            assert [reused for _, reused, _ in seen] == [False, False]
            assert not http._rest_tls._sessions
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_keepalive_uses_existing_connection(trusted_ca):
    async with https_server(
        server_context(trusted_ca, ssl.TLSVersion.TLSv1_3), keepalive=True
    ) as (endpoint, seen):
        http = _AsyncHttpClient(endpoint, "token")
        try:
            assert await http.health()
            assert await http.health()
            assert seen[0][2] is seen[1][2]
            assert [reused for _, reused, _ in seen] == [False, False]
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_origins_do_not_share_sessions(trusted_ca):
    async with (
        https_server(server_context(trusted_ca, ssl.TLSVersion.TLSv1_3)) as (
            first,
            seen_first,
        ),
        https_server(server_context(trusted_ca, ssl.TLSVersion.TLSv1_3)) as (
            second,
            seen_second,
        ),
    ):
        http = _AsyncHttpClient(first, "token")
        try:
            assert await http.health()
            await http._send({"method": "GET", "url": second + "/healthz"})
            assert await http.health()
            assert [reused for _, reused, _ in seen_first] == [False, True]
            assert [reused for _, reused, _ in seen_second] == [False]
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_concurrent_connections_consume_ticket_once(trusted_ca, monkeypatch):
    release = asyncio.Event()
    release.set()
    async with https_server(
        server_context(trusted_ca, ssl.TLSVersion.TLSv1_3, tickets=1), block=release
    ) as (endpoint, seen):
        http = _AsyncHttpClient(endpoint, "token")
        tasks = []
        try:
            assert await http.health()
            cache = http._rest_tls
            assert len(cache._sessions) == 1
            initial_ticket_id = next(iter(cache._sessions.values()))[1].id
            offered = []
            take = cache.take

            def observe_take(context):
                candidate = take(context)
                if candidate is not None:
                    offered.append(candidate.id)
                return candidate

            monkeypatch.setattr(cache, "take", observe_take)
            release.clear()
            tasks = [asyncio.create_task(http.health()) for _ in range(3)]
            for _ in range(200):
                if len(seen) == 4:
                    break
                await asyncio.sleep(0.01)
            assert len(seen) == 4
            # New tickets may arrive before all concurrent handshakes start.
            # They may resume later connections, but none may be offered twice.
            assert offered.count(initial_ticket_id) == 1
            assert len(offered) == len(set(offered))
            assert any(reused for _, reused, _ in seen[1:])
            release.set()
            assert all(await asyncio.gather(*tasks))
        finally:
            release.set()
            await asyncio.gather(*tasks, return_exceptions=True)
            await http.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["certificate", "hostname"])
async def test_certificate_and_hostname_checks_remain_enabled(trusted_ca, failure):
    context = server_context(
        trusted_ca,
        ssl.TLSVersion.TLSv1_3,
        name="other" if failure == "certificate" else "trusted",
    )
    async with https_server(context) as (endpoint, seen):
        http = _AsyncHttpClient(
            endpoint.replace("localhost", "127.0.0.1")
            if failure == "hostname"
            else endpoint,
            "token",
        )
        try:
            with pytest.raises(ApiError):
                await http.health()
            assert not seen
            assert not http._rest_tls._sessions
        finally:
            await http.close()


def test_expiry_capacity_origin_and_context_identity(trusted_ca, monkeypatch):
    monkeypatch.setattr("runta._internal.tls_resumption.time.time", lambda: 100)
    cache = _RestTLS()
    first = cache.context("localhost", 443)
    assert first is cache.context("localhost", 443)
    assert first is cache.context("LOCALHOST.", 443)
    second = cache.context("localhost", 444)
    assert first is not second
    expired = SimpleNamespace(time=90, timeout=10)
    cache.save(first, expired)
    assert not cache._sessions
    candidates = [
        SimpleNamespace(time=100, timeout=10, number=i)
        for i in range(_MAX_SESSIONS + 1)
    ]
    for candidate in candidates:
        cache.save(first, candidate)
    assert len(cache._sessions) == _MAX_SESSIONS
    assert cache.take(second) is None
    assert cache.take(first) is candidates[1]
    monkeypatch.setattr("runta._internal.tls_resumption.time.time", lambda: 110)
    assert cache.take(first) is None
    assert not cache._sessions


@pytest.mark.asyncio
async def test_server_rejects_ticket_without_replaying_request(trusted_ca):
    original = server_context(trusted_ca, ssl.TLSVersion.TLSv1_3)
    replacement = server_context(trusted_ca, ssl.TLSVersion.TLSv1_3)
    rotate = [False]

    def choose_context(*args, **kwargs):
        # Select the ticket keys before ClientHello/session processing begins.
        return ssl.SSLContext.wrap_bio(
            replacement if rotate[0] else original, *args, **kwargs
        )

    original.wrap_bio = choose_context
    async with https_server(original) as (endpoint, seen):
        http = _AsyncHttpClient(endpoint, "token")
        try:
            assert await http.health()
            rotate[0] = True
            assert await http.health()
            assert await http.health()
            assert [reused for _, reused, _ in seen] == [False, False, True]
        finally:
            await http.close()


@pytest.mark.asyncio
async def test_locally_rejected_candidate_falls_back_before_http(trusted_ca):
    async with https_server(server_context(trusted_ca, ssl.TLSVersion.TLSv1_3)) as (
        endpoint,
        seen,
    ):
        http = _AsyncHttpClient(endpoint, "token")
        other = _AsyncHttpClient(endpoint, "token")
        try:
            assert await http.health()
            assert await other.health()
            current = next(iter(http._rest_tls._contexts.values()))
            foreign = next(iter(other._rest_tls._contexts.values()))
            http._rest_tls.take(current)
            foreign_session = other._rest_tls.take(foreign)
            assert foreign_session is not None
            # Simulate an unusable cached session. OpenSSL rejects its context.
            http._rest_tls.save(current, foreign_session)
            assert await http.health()
            assert [reused for _, reused, _ in seen] == [False, False, False]
            assert len(http._rest_tls._sessions) == 1
        finally:
            await http.close()
            await other.close()


def test_tls13_ticket_is_captured_after_handshake_without_application_data(trusted_ca):
    cache = _RestTLS()
    client_context = cache.context("localhost", 443)
    client_context.minimum_version = client_context.maximum_version = (
        ssl.TLSVersion.TLSv1_3
    )
    server = server_context(trusted_ca, ssl.TLSVersion.TLSv1_3, tickets=1)
    ci, co, si, so = [ssl.MemoryBIO() for _ in range(4)]
    client = client_context.wrap_bio(ci, co, server_hostname="localhost")
    peer = server.wrap_bio(si, so, server_side=True)
    done = [False, False]
    for _ in range(100):
        for index, connection in enumerate((client, peer)):
            if not done[index]:
                try:
                    connection.do_handshake()
                    done[index] = True
                except (ssl.SSLWantReadError, ssl.SSLWantWriteError):
                    pass
        if co.pending:
            si.write(co.read())
        if so.pending:
            ci.write(so.read())
        if all(done):
            break
    assert all(done)
    assert not cache._sessions
    # Processing a ticket alone raises WantRead; it must still save the ticket.
    with pytest.raises(ssl.SSLWantReadError):
        client.read()
    assert len(cache._sessions) == 1
    context, ticket = next(iter(cache._sessions.values()))
    assert context is client_context
    assert ticket.has_ticket
    with pytest.raises(ssl.SSLWantReadError):
        client.read()
    assert len(cache._sessions) == 1


@pytest.mark.asyncio
async def test_cancel_and_close_clear_tls_resources(trusted_ca):
    release = asyncio.Event()
    release.set()
    async with https_server(
        server_context(trusted_ca, ssl.TLSVersion.TLSv1_3), block=release
    ) as (endpoint, seen):
        http = _AsyncHttpClient(endpoint, "token")
        task = None
        try:
            assert await http.health()
            release.clear()
            task = asyncio.create_task(http.health())
            for _ in range(200):
                if len(seen) == 2:
                    break
                await asyncio.sleep(0.01)
            assert len(seen) == 2
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert not http._session.connector._acquired
        finally:
            release.set()
            if task is not None:
                await asyncio.gather(task, return_exceptions=True)
            await http.close()
        assert http._session.closed
        assert not http._rest_tls._sessions
        assert not http._rest_tls._contexts
