"""Real loopback coverage for OAuth callback ownership and cancellation."""

import asyncio
import errno
import socket
import sys
from urllib.parse import parse_qs, urlparse

import anyio
import httpx
import pytest

import runlayer_cli.oauth as oauth_module
from runlayer_cli.oauth import OAuth, OAuthCallbackTimeoutError


@pytest.fixture
def anyio_backend():
    # Uvicorn and the SDK callback future run on asyncio.
    return "asyncio"


@pytest.fixture
def callback_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("127.0.0.1", 0))
        except PermissionError:
            pytest.skip("OS policy prevents loopback binding")
        return sock.getsockname()[1]


@pytest.fixture
async def callback_servers(monkeypatch):
    """Observe real servers and clean up listeners even on a regression."""
    servers = []
    original_factory = oauth_module.create_oauth_callback_server

    def record_server(**kwargs):
        server = original_factory(**kwargs)
        servers.append(server)
        return server

    monkeypatch.setattr(oauth_module, "create_oauth_callback_server", record_server)
    try:
        yield servers
        # Rebinding alone can succeed with a leaked listener on Windows.
        assert all(
            not listener.is_serving()
            for server in servers
            for listener in getattr(server, "servers", ())
        )
        assert all(
            task.done() for server in servers for task in server.server_state.tasks
        )
    finally:
        with anyio.fail_after(5, shield=True):
            for server in servers:
                if hasattr(server, "servers"):
                    await server.shutdown()


def assert_port_reusable(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        option = (
            socket.SO_EXCLUSIVEADDRUSE
            if sys.platform == "win32"
            else socket.SO_REUSEADDR
        )
        sock.setsockopt(socket.SOL_SOCKET, option, 1)
        sock.bind(("127.0.0.1", port))
        sock.listen(1)


async def wait_for_server(servers, count=1):
    with anyio.fail_after(5):
        while len(servers) < count or not servers[count - 1].started:
            await anyio.sleep(0.01)


async def send_callback(port, state="test-state"):
    async with httpx.AsyncClient(trust_env=False) as client:
        response = await client.get(
            f"http://127.0.0.1:{port}/callback",
            params={"code": "test-code", "state": state},
        )
        assert response.status_code == 200


@pytest.mark.anyio
@pytest.mark.parametrize(
    "cancel", [None, "scope", "task"], ids=["success", "scope-cancel", "task-cancel"]
)
async def test_callback_releases_port_before_returning(
    tmp_path, callback_port, callback_servers, cancel
):
    oauth = OAuth(
        mcp_url="https://mcp.example.test/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=callback_port,
    )
    finished = anyio.Event()
    cancelled = anyio.Event()
    results = []

    async def run_callback(*, task_status=anyio.TASK_STATUS_IGNORED):
        try:
            with anyio.CancelScope() as scope:
                task_status.started((scope, asyncio.current_task()))
                try:
                    results.append(await oauth.callback_handler())
                except anyio.get_cancelled_exc_class():
                    cancelled.set()
                    raise
        finally:
            finished.set()

    with anyio.fail_after(10):
        async with anyio.create_task_group() as tasks:
            scope, callback_task = await tasks.start(run_callback)
            await wait_for_server(callback_servers)
            if cancel == "scope":
                scope.cancel()
            elif cancel == "task":
                callback_task.cancel()
            else:
                await send_callback(callback_port)
            await finished.wait()

    assert cancelled.is_set() == bool(cancel)
    assert results == ([] if cancel else [("test-code", "test-state")])
    # No delay: callers may immediately reconnect on the persisted port.
    assert_port_reusable(callback_port)


@pytest.mark.anyio
async def test_callback_timeout_releases_port(
    tmp_path, monkeypatch, callback_port, callback_servers
):
    fail_after = anyio.fail_after

    def shorten_callback_timeout(delay, **kwargs):
        return fail_after(0.1 if delay == 300.0 else delay, **kwargs)

    monkeypatch.setattr(anyio, "fail_after", shorten_callback_timeout)
    oauth = OAuth(
        mcp_url="https://mcp.example.test/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=callback_port,
    )
    with fail_after(5):
        with pytest.raises(OAuthCallbackTimeoutError):
            await oauth.callback_handler()
    assert_port_reusable(callback_port)


@pytest.mark.anyio
async def test_callback_startup_deadline_is_not_reported_as_socket_error(
    tmp_path, monkeypatch, callback_port, callback_servers
):
    """TimeoutError is an OSError subclass; keep the shield deadline distinct."""
    fail_after = anyio.fail_after

    def shorten_startup_shield(delay, **kwargs):
        return fail_after(0.05 if delay == 2 else delay, **kwargs)

    monkeypatch.setattr(anyio, "fail_after", shorten_startup_shield)
    loop = asyncio.get_running_loop()
    create_server = loop.create_server

    async def slow_create_server(*args, **kwargs):
        await anyio.sleep(0.2)
        return await create_server(*args, **kwargs)

    monkeypatch.setattr(loop, "create_server", slow_create_server)
    oauth = OAuth(
        mcp_url="https://mcp.example.test/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=callback_port,
    )
    with fail_after(5):
        with pytest.raises(TimeoutError) as exc_info:
            await oauth.callback_handler()

    assert not isinstance(exc_info.value, RuntimeError)
    assert "could not start" not in str(exc_info.value)
    assert_port_reusable(callback_port)


@pytest.mark.anyio
async def test_cancellation_drains_stalled_callback_request(
    tmp_path, callback_port, callback_servers
):
    request_started = anyio.Event()
    request_finished = anyio.Event()

    async def stalled_response(scope, receive, send):
        request_started.set()
        try:
            await anyio.sleep_forever()
        finally:
            request_finished.set()

    oauth = OAuth(
        mcp_url="https://mcp.example.test/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=callback_port,
    )
    with anyio.fail_after(5):
        async with anyio.create_task_group() as tasks:
            tasks.start_soon(oauth.callback_handler)
            await wait_for_server(callback_servers)
            # Stall at the ASGI response boundary while Uvicorn owns a real request.
            callback_servers[0].config.app.routes[0].app = stalled_response
            async with await anyio.connect_tcp("127.0.0.1", callback_port) as client:
                await client.send(b"GET /callback HTTP/1.1\r\nHost: localhost\r\n\r\n")
                await request_started.wait()
                tasks.cancel_scope.cancel()

    assert request_finished.is_set()
    assert all(task.done() for task in callback_servers[0].server_state.tasks)
    assert_port_reusable(callback_port)


@pytest.mark.anyio
async def test_cancellation_during_callback_startup_releases_port(
    tmp_path, monkeypatch, callback_port, callback_servers
):
    startup_entered = anyio.Event()
    oauth = OAuth(
        mcp_url="https://mcp.example.test/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=callback_port,
    )

    async def pause_startup(*args, **kwargs):
        startup_entered.set()
        await anyio.sleep_forever()

    loop = asyncio.get_running_loop()
    monkeypatch.setattr(loop, "create_server", pause_startup)
    with anyio.fail_after(5):
        async with anyio.create_task_group() as tasks:
            tasks.start_soon(oauth.callback_handler)
            await startup_entered.wait()
            tasks.cancel_scope.cancel()

    assert_port_reusable(callback_port)


@pytest.mark.anyio
async def test_cancellation_during_listener_registration_closes_server(
    tmp_path, monkeypatch, callback_port, callback_servers
):
    loop = asyncio.get_running_loop()
    create_server = loop.create_server
    listener_created = anyio.Event()
    finish_registration = anyio.Event()
    listeners = []

    async def pause_after_create(*args, **kwargs):
        listener = await create_server(*args, **kwargs)
        listeners.append(listener)
        listener_created.set()
        await finish_registration.wait()
        return listener

    monkeypatch.setattr(loop, "create_server", pause_after_create)
    oauth = OAuth(
        mcp_url="https://mcp.example.test/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=callback_port,
    )

    async def run_callback(*, task_status=anyio.TASK_STATUS_IGNORED):
        with anyio.CancelScope() as scope:
            task_status.started(scope)
            await oauth.callback_handler()

    try:
        with anyio.fail_after(5):
            async with anyio.create_task_group() as tasks:
                scope = await tasks.start(run_callback)
                await listener_created.wait()
                scope.cancel()
                await anyio.sleep(0)
                finish_registration.set()
        assert all(not listener.is_serving() for listener in listeners)
        assert_port_reusable(callback_port)
    finally:
        # A failed regression must not leave the loop watching a closed/reused FD.
        for listener in listeners:
            listener.close()


@pytest.mark.anyio
@pytest.mark.parametrize("error_number", [errno.EACCES, errno.EADDRINUSE])
async def test_callback_startup_error_releases_port_and_preserves_cause(
    tmp_path, monkeypatch, callback_port, callback_servers, error_number
):
    original_error = OSError(error_number, "untrusted diagnostic detail")
    oauth = OAuth(
        mcp_url="https://mcp.example.test/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=callback_port,
    )

    async def fail_startup(*args, **kwargs):
        raise original_error

    loop = asyncio.get_running_loop()
    monkeypatch.setattr(loop, "create_server", fail_startup)
    with anyio.fail_after(5):
        with pytest.raises(RuntimeError) as exc_info:
            await oauth.callback_handler()

    message = str(exc_info.value)
    assert exc_info.value.__cause__ is original_error
    assert errno.errorcode[error_number] in message
    assert "startup" in message
    assert ("already in use" in message) == (error_number == errno.EADDRINUSE)
    assert "untrusted diagnostic detail" not in message
    assert_port_reusable(callback_port)


@pytest.mark.anyio
async def test_httpx_oauth_reconnects_on_cached_port_after_cancellation(
    tmp_path, callback_port, callback_servers
):
    """Exercise SDK discovery, authorization, callback, and token exchange."""
    mcp_url = "https://mcp.example.test/mcp"
    prm_url = "https://mcp.example.test/oauth/protected-resource"
    idp_url = "https://idp.example.test"
    browser_states = []
    token_exchanges = []

    async def browser_boundary(authorization_url):
        browser_states.append(parse_qs(urlparse(authorization_url).query)["state"][0])

    def remote_boundary(request):
        url = str(request.url)
        if url == mcp_url:
            if request.headers.get("Authorization") == "Bearer test-access-token":
                return httpx.Response(200, json={"connected": True})
            return httpx.Response(
                401,
                headers={"WWW-Authenticate": f'Bearer resource_metadata="{prm_url}"'},
            )
        if url == prm_url:
            return httpx.Response(
                200, json={"resource": mcp_url, "authorization_servers": [idp_url]}
            )
        if url == f"{idp_url}/.well-known/oauth-authorization-server":
            return httpx.Response(
                200,
                json={
                    "issuer": idp_url,
                    "authorization_endpoint": f"{idp_url}/authorize",
                    "token_endpoint": f"{idp_url}/token",
                },
            )
        if url == f"{idp_url}/token":
            token_exchanges.append(True)
            return httpx.Response(
                200,
                json={
                    "access_token": "test-access-token",
                    "token_type": "Bearer",
                    "expires_in": 3600,
                },
            )
        return httpx.Response(404)

    def make_oauth(**kwargs):
        oauth = OAuth(
            mcp_url=mcp_url,
            token_storage_cache_dir=tmp_path,
            manual_client_id="test-client",
            **kwargs,
        )
        oauth.context.redirect_handler = browser_boundary
        return oauth

    responses = []
    cancelled = anyio.Event()

    async def request(oauth, *, task_status=anyio.TASK_STATUS_IGNORED):
        with anyio.CancelScope() as scope:
            task_status.started(scope)
            try:
                async with httpx.AsyncClient(
                    auth=oauth,
                    transport=httpx.MockTransport(remote_boundary),
                    trust_env=False,
                ) as client:
                    responses.append(await client.get(mcp_url))
            except anyio.get_cancelled_exc_class():
                cancelled.set()
                raise

    with anyio.fail_after(10):
        async with anyio.create_task_group() as tasks:
            scope = await tasks.start(request, make_oauth(callback_port=callback_port))
            await wait_for_server(callback_servers)
            scope.cancel()

        assert cancelled.is_set()
        second_oauth = make_oauth()
        assert second_oauth.redirect_port == callback_port
        async with anyio.create_task_group() as tasks:
            await tasks.start(request, second_oauth)
            await wait_for_server(callback_servers, count=2)
            await send_callback(callback_port, state=browser_states[-1])

    assert len(browser_states) == 2
    assert len(token_exchanges) == 1
    assert len(responses) == 1
    assert responses[0].json() == {"connected": True}
    assert_port_reusable(callback_port)
