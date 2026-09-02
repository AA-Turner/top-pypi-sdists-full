"""OAuth error UX: actionable guidance for DCR rejections and pending-login timeouts.

Motivating incident: a customer saw the raw IdP body
``Registration failed: 403 {"errorCode":"E0000005","errorSummary":"Invalid session"}``
(Okta rejecting dynamic client registration) and, separately, a silent 30s
tools/list timeout while a browser OAuth login was waiting on a callback port
their IdP rejected. Neither error said what to do.
"""

from unittest.mock import MagicMock

import anyio
import httpx
import pytest
import mcp.types as mt
from fastmcp.server.middleware.middleware import MiddlewareContext
from mcp.client.auth import OAuthRegistrationError, OAuthTokenError
from mcp.shared.auth import OAuthToken

from runlayer_cli import oauth_guidance
from runlayer_cli.middleware import RunlayerMiddleware
from runlayer_cli.models import ServerDetails
from runlayer_cli.models_mcp import PostRequest
from runlayer_cli.oauth import OAuth, OAuthClientProvider


OKTA_403_MESSAGE = (
    'Registration failed: 403 {"errorCode":"E0000005",'
    '"errorSummary":"Invalid session","errorLink":"E0000005",'
    '"errorId":"oaeXYZ","errorCauses":[]}'
)


@pytest.fixture(autouse=True)
def _reset_pending_oauth_state():
    oauth_guidance.mark_oauth_flow_finished()
    yield
    oauth_guidance.mark_oauth_flow_finished()


# --- Registration (DCR) failure classification ---


def test_registration_403_classifies_with_remediation():
    guidance = oauth_guidance.classify_registration_failure(OKTA_403_MESSAGE)

    assert guidance is not None
    # Actionable remediation: manual OAuth app in the IdP + Runlayer settings.
    assert "Manual OAuth" in guidance
    assert "client ID" in guidance
    assert "identity provider" in guidance
    # Original status + IdP error code preserved for support.
    assert "403" in guidance
    assert "E0000005" in guidance


def test_registration_5xx_is_not_classified():
    assert (
        oauth_guidance.classify_registration_failure(
            "Registration failed: 502 upstream hiccup"
        )
        is None
    )


def test_unrecognized_message_is_not_classified():
    assert oauth_guidance.classify_registration_failure("something else") is None


def test_registration_detail_is_sanitized_and_truncated():
    long_tail = "x" * 1000
    message = (
        'Registration failed: 400 {"error":"invalid_client_metadata",'
        f'"client_secret":"hunter2","access_token":"eyJabc.def.ghi","pad":"{long_tail}"}}'
    )

    guidance = oauth_guidance.classify_registration_failure(message)

    assert guidance is not None
    assert "hunter2" not in guidance
    assert "eyJabc.def.ghi" not in guidance
    assert "[REDACTED]" in guidance
    assert long_tail not in guidance
    assert "[truncated]" in guidance


@pytest.mark.asyncio
async def test_async_auth_flow_translates_dcr_rejection(tmp_path, monkeypatch):
    """A 4xx DCR failure from the mcp SDK re-raises with actionable guidance."""

    async def failing_flow(self, request):
        raise OAuthRegistrationError(OKTA_403_MESSAGE)
        yield  # pragma: no cover - makes this an async generator

    monkeypatch.setattr(OAuthClientProvider, "async_auth_flow", failing_flow)
    oauth = OAuth(mcp_url="https://example.com/mcp", token_storage_cache_dir=tmp_path)

    gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
    with pytest.raises(OAuthRegistrationError) as exc_info:
        await gen.__anext__()

    message = str(exc_info.value)
    assert "Manual OAuth" in message
    assert "403" in message
    assert "E0000005" in message
    # Original exception kept in the chain for support/debugging.
    assert isinstance(exc_info.value.__cause__, OAuthRegistrationError)


@pytest.mark.asyncio
async def test_async_auth_flow_passes_through_non_4xx(tmp_path, monkeypatch):
    async def failing_flow(self, request):
        raise OAuthRegistrationError("Registration failed: 502 upstream hiccup")
        yield  # pragma: no cover - makes this an async generator

    monkeypatch.setattr(OAuthClientProvider, "async_auth_flow", failing_flow)
    oauth = OAuth(mcp_url="https://example.com/mcp", token_storage_cache_dir=tmp_path)

    gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
    with pytest.raises(OAuthRegistrationError) as exc_info:
        await gen.__anext__()

    assert str(exc_info.value) == "Registration failed: 502 upstream hiccup"


@pytest.mark.asyncio
async def test_async_auth_flow_retries_expired_authorization_code(
    tmp_path, monkeypatch
):
    """A consumed authorization code starts one fresh OAuth flow."""
    calls = 0
    fresh_token = OAuthToken(access_token="fresh-token", token_type="Bearer")

    async def intermittently_failing_flow(self, request):
        nonlocal calls
        calls += 1
        if calls == 1:
            await self.context.storage.set_tokens(fresh_token)
            raise OAuthTokenError(
                'Token exchange failed (400): {"error":"invalid_grant",'
                '"error_description":"Unknown or expired authorization code"}'
            )
        assert "Authorization" not in request.headers
        await self._initialize()
        yield request

    monkeypatch.setattr(
        OAuthClientProvider, "async_auth_flow", intermittently_failing_flow
    )
    browser_lockfile = tmp_path / "browser.lock"
    browser_lockfile.touch()
    monkeypatch.setattr(
        "runlayer_cli.oauth.get_browser_lockfile_path", lambda _: browser_lockfile
    )
    oauth = OAuth(mcp_url="https://example.com/mcp", token_storage_cache_dir=tmp_path)
    clear_tokens = MagicMock(wraps=oauth.context.storage.clear_tokens)
    monkeypatch.setattr(oauth.context.storage, "clear_tokens", clear_tokens)
    request = httpx.Request(
        "GET",
        "https://example.com/mcp",
        headers={"Authorization": "Bearer stale-token"},
    )

    gen = oauth.async_auth_flow(request)
    assert await gen.__anext__() is request
    assert calls == 2
    clear_tokens.assert_not_called()
    assert oauth.context.current_tokens == fresh_token
    assert await oauth.context.storage.get_tokens() == fresh_token
    assert not browser_lockfile.exists()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message",
    [
        'Token exchange failed (400): {"error":"invalid_client"}',
        (
            'Token exchange failed (400): {"error":"invalid_grant",'
            '"error_description":"Unknown or expired authorization code"}'
        ),
    ],
)
async def test_async_auth_flow_does_not_retry_other_or_repeated_token_errors(
    tmp_path, monkeypatch, message
):
    calls = 0

    async def failing_flow(self, request):
        nonlocal calls
        calls += 1
        raise OAuthTokenError(message)
        yield  # pragma: no cover - makes this an async generator

    monkeypatch.setattr(OAuthClientProvider, "async_auth_flow", failing_flow)
    oauth = OAuth(mcp_url="https://example.com/mcp", token_storage_cache_dir=tmp_path)

    gen = oauth.async_auth_flow(httpx.Request("GET", "https://example.com/mcp"))
    with pytest.raises(OAuthTokenError):
        await gen.__anext__()

    expected_calls = 2 if "authorization code" in message else 1
    assert calls == expected_calls


# --- Pending interactive OAuth flow state ---


def test_pending_flow_marker_lifecycle():
    assert oauth_guidance.pending_oauth_flow_port() is None

    oauth_guidance.mark_oauth_flow_started(53682)
    assert oauth_guidance.pending_oauth_flow_port() == 53682

    oauth_guidance.mark_oauth_flow_finished()
    assert oauth_guidance.pending_oauth_flow_port() is None


def test_pending_flow_marker_goes_stale(monkeypatch):
    oauth_guidance.mark_oauth_flow_started(53682)
    monkeypatch.setattr(oauth_guidance, "_PENDING_MAX_AGE_SECONDS", -1.0)
    assert oauth_guidance.pending_oauth_flow_port() is None


@pytest.mark.asyncio
async def test_redirect_handler_marks_flow_pending(tmp_path, monkeypatch):
    monkeypatch.setattr("runlayer_cli.oauth.should_open_browser", lambda url: False)
    oauth = OAuth(
        mcp_url="https://example.com/mcp",
        token_storage_cache_dir=tmp_path,
        callback_port=53682,
    )

    await oauth.redirect_handler("https://idp.example.com/authorize?x=y")

    assert oauth_guidance.pending_oauth_flow_port() == 53682


def test_oauth_pending_timeout_message_contents():
    message = oauth_guidance.oauth_pending_timeout_message(53682)

    assert "http://localhost:53682/callback" in message
    assert "--oauth-callback-port" in message
    assert "redirect URI" in message
    assert "error page" in message


# --- Middleware: tools/list timeout while OAuth login is pending ---


def _make_middleware() -> tuple[RunlayerMiddleware, MagicMock]:
    mock_client = MagicMock()
    mock_client.pre.return_value = MagicMock(
        status_code=200, json=lambda: {"correlation_id": "corr-oauth"}
    )
    mock_client.post.return_value = MagicMock(status_code=200, json=lambda: [])
    server = ServerDetails(
        id="server-123",
        name="Test Server",
        url="http://test.example.com",
        transport_type="streaming-http",
        transport_config={},
        deployment_mode="local",
        sync_required=False,
    )
    middleware = RunlayerMiddleware(
        runlayer_api_client=mock_client, proxy=MagicMock(), server=server
    )
    return middleware, mock_client


async def _list_tools_with(middleware: RunlayerMiddleware, call_next) -> list:
    mock_context = MagicMock(spec=MiddlewareContext)
    mock_context.message = mt.ListToolsRequest(method="tools/list")
    return await middleware.on_list_tools(mock_context, call_next)  # type: ignore


@pytest.mark.asyncio
async def test_list_timeout_during_pending_oauth_mentions_callback_port(monkeypatch):
    """The 30s upstream bound firing mid-OAuth explains the callback port."""
    from runlayer_cli import middleware as middleware_module

    monkeypatch.setattr(middleware_module, "_LIST_TOOLS_UPSTREAM_TIMEOUT_SECONDS", 0.05)
    oauth_guidance.mark_oauth_flow_started(53682)
    middleware, mock_client = _make_middleware()

    async def hanging_call_next(context):
        await anyio.sleep(5)

    result = await _list_tools_with(middleware, hanging_call_next)

    assert result == []
    post_payload = mock_client.post.call_args[0][1]
    assert isinstance(post_payload, PostRequest)
    assert post_payload.upstream_error is not None
    message = post_payload.upstream_error.message or ""
    assert "http://localhost:53682/callback" in message
    assert "--oauth-callback-port" in message


@pytest.mark.asyncio
async def test_list_timeout_without_pending_oauth_stays_bare(monkeypatch):
    from runlayer_cli import middleware as middleware_module

    monkeypatch.setattr(middleware_module, "_LIST_TOOLS_UPSTREAM_TIMEOUT_SECONDS", 0.05)
    middleware, mock_client = _make_middleware()

    async def hanging_call_next(context):
        await anyio.sleep(5)

    result = await _list_tools_with(middleware, hanging_call_next)

    assert result == []
    post_payload = mock_client.post.call_args[0][1]
    message = post_payload.upstream_error.message or ""
    assert "--oauth-callback-port" not in message


@pytest.mark.asyncio
async def test_non_timeout_unreachable_during_pending_oauth_stays_bare():
    """A plain connect failure isn't the OAuth-wait case; no port guidance."""
    oauth_guidance.mark_oauth_flow_started(53682)
    middleware, mock_client = _make_middleware()

    async def refusing_call_next(context):
        raise httpx.ConnectError("refused")

    result = await _list_tools_with(middleware, refusing_call_next)

    assert result == []
    post_payload = mock_client.post.call_args[0][1]
    message = post_payload.upstream_error.message or ""
    assert "--oauth-callback-port" not in message
