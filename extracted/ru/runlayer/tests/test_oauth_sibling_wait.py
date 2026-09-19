"""A second `runlayer run` whose cached callback port is held by a sibling's
pending browser login waits for that login instead of failing."""

import socket
import time
from collections.abc import Iterator

import anyio
import httpx
import pytest
from mcp.client.auth import OAuthClientProvider
from mcp.shared.auth import OAuthToken

from runlayer_cli import oauth as oauth_module
from runlayer_cli import oauth_guidance
from runlayer_cli.oauth import OAuth, OAuthCallbackPortInUseError

FRESH = OAuthToken(access_token="fresh-from-sibling", token_type="Bearer")


def _collision(port: int) -> OAuthCallbackPortInUseError:
    return OAuthCallbackPortInUseError(
        f"OAuth callback port {port} is already in use", port=port
    )


@pytest.fixture
def fast_poll(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(oauth_module, "_SIBLING_LOGIN_POLL_SECONDS", 0.02)
    monkeypatch.setattr(oauth_module, "_SIBLING_LOGIN_WAIT_SECONDS", 2.0)
    monkeypatch.setattr(oauth_module, "_SIBLING_TOKEN_SETTLE_SECONDS", 0.3)


@pytest.fixture
def occupied_port() -> Iterator[tuple[int, socket.socket]]:
    """A listening loopback socket standing in for the sibling's callback server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as holder:
        try:
            holder.bind(("127.0.0.1", 0))
        except PermissionError as e:
            pytest.skip(f"Loopback bind unavailable: {e}")
        holder.listen(1)
        yield holder.getsockname()[1], holder


def _install_colliding_flow(
    monkeypatch: pytest.MonkeyPatch, port: int
) -> list[httpx.Request]:
    """Parent flow that collides on the first attempt and succeeds on the second."""
    attempts: list[httpx.Request] = []

    async def flow(self, request):
        attempts.append(request)
        if len(attempts) == 1:
            raise _collision(port)
        assert "Authorization" not in request.headers
        await self._initialize()
        yield request

    monkeypatch.setattr(OAuthClientProvider, "async_auth_flow", flow)
    return attempts


def _oauth(tmp_path, port: int) -> OAuth:
    return OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=port,
    )


@pytest.mark.asyncio
async def test_adopts_sibling_token_and_retries(
    tmp_path, monkeypatch, fast_poll, occupied_port
):
    port, _holder = occupied_port
    attempts = _install_colliding_flow(monkeypatch, port)
    oauth = _oauth(tmp_path, port)
    oauth_guidance.mark_oauth_flow_started(
        port
    )  # what callback_handler does before binding
    stale = OAuthToken(access_token="stale-token", token_type="Bearer")
    await oauth.context.storage.set_tokens(stale)
    oauth.context.current_tokens = stale

    async def sibling_finishes_login():
        await anyio.sleep(0.1)
        await oauth.context.storage.set_tokens(FRESH)

    request = httpx.Request(
        "GET", "https://example.com/mcp", headers={"Authorization": "Bearer stale"}
    )
    async with anyio.create_task_group() as tg:
        tg.start_soon(sibling_finishes_login)
        gen = oauth.async_auth_flow(request)
        with anyio.fail_after(5):
            assert await gen.__anext__() is request

    assert len(attempts) == 2
    assert oauth.context.current_tokens == FRESH
    # The collision left the pending-login marker set; adopting a token means
    # no browser is awaited, so later timeouts must not blame the IdP.
    assert oauth_guidance.pending_oauth_flow_port() is None


@pytest.mark.asyncio
async def test_adopts_token_already_on_disk_without_waiting(
    tmp_path, monkeypatch, fast_poll, occupied_port
):
    """A sibling finished before we collided (a third process holds the port
    now): the fresh token on disk is adopted immediately."""
    port, _holder = occupied_port
    monkeypatch.setattr(oauth_module, "_SIBLING_LOGIN_WAIT_SECONDS", 30.0)
    attempts = _install_colliding_flow(monkeypatch, port)
    oauth = _oauth(tmp_path, port)
    oauth.context.current_tokens = OAuthToken(
        access_token="rejected-token", token_type="Bearer"
    )
    await oauth.context.storage.set_tokens(FRESH)

    gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
    with anyio.fail_after(2):
        await gen.__anext__()

    assert len(attempts) == 2
    assert oauth.context.current_tokens == FRESH


@pytest.mark.asyncio
async def test_adopts_fresh_token_on_disk_when_memory_is_empty(
    tmp_path, monkeypatch, fast_poll, occupied_port
):
    """First-time login raced by a sibling: nothing in memory, a fresh
    (unexpired) token on disk -> adopt it instead of waiting for a change."""
    port, _holder = occupied_port
    monkeypatch.setattr(oauth_module, "_SIBLING_LOGIN_WAIT_SECONDS", 30.0)
    attempts = _install_colliding_flow(monkeypatch, port)
    oauth = _oauth(tmp_path, port)
    assert oauth.context.current_tokens is None
    await oauth.context.storage.set_tokens(
        OAuthToken(
            access_token=FRESH.access_token, token_type="Bearer", expires_in=3600
        )
    )

    gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
    with anyio.fail_after(2):
        await gen.__anext__()

    assert len(attempts) == 2
    assert oauth.context.current_tokens is not None
    assert oauth.context.current_tokens.access_token == FRESH.access_token


@pytest.mark.asyncio
async def test_expired_token_on_disk_is_not_adopted(
    tmp_path, monkeypatch, fast_poll, occupied_port
):
    """After a failed refresh the SDK drops the token from memory but the file
    still holds the expired one; that must not count as a sibling's result."""
    port, _holder = occupied_port
    monkeypatch.setattr(oauth_module, "_SIBLING_LOGIN_WAIT_SECONDS", 0.2)
    attempts = _install_colliding_flow(monkeypatch, port)
    oauth = _oauth(tmp_path, port)
    await oauth.context.storage.set_tokens(
        OAuthToken(access_token="expired-token", token_type="Bearer", expires_in=1)
    )
    monkeypatch.setattr(
        oauth.context.storage, "get_token_expiry_time", lambda: time.time() - 60
    )

    gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
    with anyio.fail_after(5), pytest.raises(OAuthCallbackPortInUseError):
        await gen.__anext__()

    assert len(attempts) == 1


@pytest.mark.asyncio
async def test_port_freed_just_before_deadline_still_gets_settle_window(
    tmp_path, monkeypatch, fast_poll, occupied_port
):
    """The sibling's budget runs on the same clock as ours, so its release can
    land in the last second; the settle window must not be cut by the deadline."""
    port, holder = occupied_port
    monkeypatch.setattr(oauth_module, "_SIBLING_LOGIN_WAIT_SECONDS", 0.3)
    monkeypatch.setattr(oauth_module, "_SIBLING_TOKEN_SETTLE_SECONDS", 0.3)
    attempts = _install_colliding_flow(monkeypatch, port)
    oauth = _oauth(tmp_path, port)

    async def sibling_gives_up_late():
        await anyio.sleep(0.2)
        holder.close()

    async with anyio.create_task_group() as tg:
        tg.start_soon(sibling_gives_up_late)
        gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
        with anyio.fail_after(5):
            await gen.__anext__()

    assert len(attempts) == 2


@pytest.mark.asyncio
async def test_port_release_waits_for_the_token_to_settle(
    tmp_path, monkeypatch, fast_poll, occupied_port
):
    """The sibling frees the port before its token exchange lands; the token
    arriving inside the settle window wins over a second login."""
    port, holder = occupied_port
    attempts = _install_colliding_flow(monkeypatch, port)
    oauth = _oauth(tmp_path, port)

    async def sibling_releases_then_writes():
        await anyio.sleep(0.05)
        holder.close()
        await anyio.sleep(0.1)
        await oauth.context.storage.set_tokens(FRESH)

    async with anyio.create_task_group() as tg:
        tg.start_soon(sibling_releases_then_writes)
        gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
        with anyio.fail_after(5):
            await gen.__anext__()

    assert len(attempts) == 2
    assert oauth.context.current_tokens == FRESH


@pytest.mark.asyncio
async def test_runs_own_login_when_port_frees_up(
    tmp_path, monkeypatch, fast_poll, occupied_port
):
    port, holder = occupied_port
    attempts = _install_colliding_flow(monkeypatch, port)
    oauth = _oauth(tmp_path, port)

    async def sibling_gives_up():
        await anyio.sleep(0.05)
        holder.close()

    async with anyio.create_task_group() as tg:
        tg.start_soon(sibling_gives_up)
        gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
        with anyio.fail_after(5):
            await gen.__anext__()

    assert len(attempts) == 2
    assert oauth.context.current_tokens is None


@pytest.mark.asyncio
async def test_gives_up_when_port_stays_occupied(
    tmp_path, monkeypatch, fast_poll, occupied_port
):
    port, _holder = occupied_port
    monkeypatch.setattr(oauth_module, "_SIBLING_LOGIN_WAIT_SECONDS", 0.2)
    attempts = _install_colliding_flow(monkeypatch, port)
    oauth = _oauth(tmp_path, port)

    gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
    with anyio.fail_after(5), pytest.raises(OAuthCallbackPortInUseError):
        await gen.__anext__()

    assert len(attempts) == 1


@pytest.mark.asyncio
async def test_waits_only_once(tmp_path, monkeypatch, fast_poll):
    """A second collision after a wait propagates; no unbounded retry loop."""
    attempts: list[httpx.Request] = []

    async def always_colliding(self, request):
        attempts.append(request)
        raise _collision(53682)
        yield request  # pragma: no cover - makes this an async generator

    monkeypatch.setattr(OAuthClientProvider, "async_auth_flow", always_colliding)
    monkeypatch.setattr(oauth_module, "_callback_port_still_held", lambda port: False)
    oauth = _oauth(tmp_path, 53682)

    gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
    with anyio.fail_after(5), pytest.raises(OAuthCallbackPortInUseError):
        await gen.__anext__()

    assert len(attempts) == 2


def test_port_probe_reports_collision_only(occupied_port):
    port, _holder = occupied_port
    assert oauth_module._callback_port_still_held(port) is True
    assert oauth_module._callback_port_still_held(oauth_module.get_free_port()) is False
