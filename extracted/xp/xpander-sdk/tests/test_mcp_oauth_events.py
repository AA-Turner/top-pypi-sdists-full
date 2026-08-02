"""PRO-1986: MCP OAuth AuthEvents must carry server identity so the app can
correlate a token_ready/token_issue back to the right server when several MCP
servers authenticate concurrently."""

from types import SimpleNamespace

import pytest

from xpander_sdk.modules.backend.utils import mcp_oauth
from xpander_sdk.modules.tools_repository.models.mcp import (
    MCPOAuthGetTokenGenericResponse,
    MCPOAuthGetTokenLoginRequiredResponse,
    MCPOAuthGetTokenResponse,
    MCPOAuthGetTokenTokenReadyResponse,
    MCPOAuthResponseType,
    MCPServerAuthType,
    MCPServerDetails,
)

# Run every async test in this module even when asyncio_mode is STRICT.
pytestmark = pytest.mark.asyncio

SERVER_URL = "https://mcp.example.com/sse"
SERVER_NAME = "Example MCP"


def _mcp(name=SERVER_NAME) -> MCPServerDetails:
    return MCPServerDetails(
        url=SERVER_URL, name=name, auth_type=MCPServerAuthType.OAuth2
    )


def _task() -> SimpleNamespace:
    return SimpleNamespace(agent_id="agent1")


@pytest.fixture
def captured(monkeypatch):
    """Capture every event handed to push_event (network stubbed out)."""
    events = []

    async def _fake_push_event(task, event, event_type, auth_events_callback=None):
        events.append(event)

    monkeypatch.setattr(mcp_oauth, "push_event", _fake_push_event)
    return events


async def test_token_ready_event_carries_server_identity(captured, monkeypatch):
    """Already-ready path emits token_ready with server_url/server_name populated."""

    async def _fake_get_token(mcp_server, task, user_id, **kwargs):
        return MCPOAuthGetTokenResponse(
            type=MCPOAuthResponseType.TOKEN_READY,
            data=MCPOAuthGetTokenTokenReadyResponse(access_token="secret-token"),
        )

    monkeypatch.setattr(mcp_oauth, "get_token", _fake_get_token)

    await mcp_oauth.authenticate_mcp_server(
        mcp_server=_mcp(), task=_task(), user_id="u1"
    )

    assert len(captured) == 1
    emitted = captured[0]
    assert emitted.type == MCPOAuthResponseType.TOKEN_READY
    assert emitted.data.server_url == SERVER_URL
    assert emitted.data.server_name == SERVER_NAME
    assert emitted.data.access_token == "REDACTED"  # never leak the token


async def test_login_then_token_ready_event_carries_server_identity(
    captured, monkeypatch
):
    """login_required → poll → token_ready: the token_ready event is keyed by server."""
    calls = {"n": 0}

    async def _fake_get_token(mcp_server, task, user_id, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            return MCPOAuthGetTokenResponse(
                type=MCPOAuthResponseType.LOGIN_REQUIRED,
                data=MCPOAuthGetTokenLoginRequiredResponse(
                    url="https://login.example.com",
                    server_url=SERVER_URL,
                    server_name=SERVER_NAME,
                ),
            )
        return MCPOAuthGetTokenResponse(
            type=MCPOAuthResponseType.TOKEN_READY,
            data=MCPOAuthGetTokenTokenReadyResponse(access_token="secret-token"),
        )

    monkeypatch.setattr(mcp_oauth, "get_token", _fake_get_token)
    monkeypatch.setattr(mcp_oauth, "POLLING_INTERVAL", 0)  # don't sleep in tests

    await mcp_oauth.authenticate_mcp_server(
        mcp_server=_mcp(), task=_task(), user_id="u1"
    )

    # first event = login_required (already keyed), second = token_ready (now keyed)
    assert [e.type for e in captured] == [
        MCPOAuthResponseType.LOGIN_REQUIRED,
        MCPOAuthResponseType.TOKEN_READY,
    ]
    ready = captured[1]
    assert ready.data.server_url == SERVER_URL
    assert ready.data.server_name == SERVER_NAME
    assert ready.data.access_token == "REDACTED"


async def test_token_issue_response_carries_server_identity(monkeypatch):
    """On failure the returned token_issue also carries server identity."""

    async def _boom(mcp_server, task, user_id, **kwargs):
        raise RuntimeError("discovery failed")

    monkeypatch.setattr(mcp_oauth, "get_token", _boom)

    result = await mcp_oauth.authenticate_mcp_server(
        mcp_server=_mcp(), task=_task(), user_id="u1"
    )

    assert result.type == MCPOAuthResponseType.TOKEN_ISSUE
    assert isinstance(result.data, MCPOAuthGetTokenGenericResponse)
    assert result.data.server_url == SERVER_URL
    assert result.data.server_name == SERVER_NAME


async def test_server_name_falls_back_to_url_when_unnamed(captured, monkeypatch):
    """server_name defaults to the url when the MCP server has no name."""

    async def _fake_get_token(mcp_server, task, user_id, **kwargs):
        return MCPOAuthGetTokenResponse(
            type=MCPOAuthResponseType.TOKEN_READY,
            data=MCPOAuthGetTokenTokenReadyResponse(access_token="secret-token"),
        )

    monkeypatch.setattr(mcp_oauth, "get_token", _fake_get_token)

    await mcp_oauth.authenticate_mcp_server(
        mcp_server=_mcp(name=None), task=_task(), user_id="u1"
    )

    assert captured[0].data.server_name == SERVER_URL
