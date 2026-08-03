"""Remote MCP preflight: real-error unwrapping and the 401 token self-heal."""

import asyncio

import httpx
import pytest

try:
    BaseExceptionGroup
except NameError:  # py3.10: exception groups live in the backport (pulled in via anyio)
    from exceptiongroup import BaseExceptionGroup, ExceptionGroup

from xpander_sdk.modules.backend.frameworks import agno as agno_module
from xpander_sdk.modules.backend.utils.mcp_connect import (
    extract_real_mcp_error,
    is_mcp_auth_error,
)
from xpander_sdk.modules.tools_repository.models.mcp import (
    MCPOAuthGetTokenResponse,
    MCPOAuthGetTokenTokenReadyResponse,
    MCPOAuthResponseType,
    MCPServerAuthType,
    MCPServerDetails,
)


def _http_error(status: int) -> httpx.HTTPStatusError:
    req = httpx.Request("POST", "https://api.fathom.ai/mcp")
    resp = httpx.Response(status, request=req)
    return httpx.HTTPStatusError(f"status {status}", request=req, response=resp)


class _User:
    id = "u1"


class _Input:
    user = _User()


class _FakeTask:
    input = _Input()


def _mcp(**overrides):
    base = dict(
        url="https://api.fathom.ai/mcp",
        name="Fathom MCP",
        auth_type=MCPServerAuthType.OAuth2,
        api_key="stale-token",
        headers={"Authorization": "Bearer stale-token"},
    )
    base.update(overrides)
    return MCPServerDetails(**base)


def test_extract_prefers_http_status_error_over_taskgroup_noise():
    inner = BaseExceptionGroup(
        "unhandled errors in a TaskGroup",
        [_http_error(401), GeneratorExit()],
    )
    outer = BaseExceptionGroup("wrapper", [inner])
    real = extract_real_mcp_error(outer)
    assert isinstance(real, httpx.HTTPStatusError)
    assert real.response.status_code == 401


def test_extract_falls_back_to_first_meaningful_leaf():
    group = ExceptionGroup("boom", [ValueError("dns fail")])
    assert isinstance(extract_real_mcp_error(group), ValueError)


def test_extract_returns_original_when_only_cancellation_noise():
    cancelled = asyncio.CancelledError("Cancelled via cancel scope deadbeef")
    group = BaseExceptionGroup("noise", [cancelled])
    assert extract_real_mcp_error(group) is group


def test_is_mcp_auth_error():
    assert is_mcp_auth_error(_http_error(401))
    assert is_mcp_auth_error(_http_error(403))
    assert not is_mcp_auth_error(_http_error(500))
    assert not is_mcp_auth_error(ValueError("nope"))


def _run_ensure(mcp, probe_results, auth_result=None, monkeypatch=None):
    probe_calls = []
    auth_calls = []

    async def _probe(url, headers=None, transport="streamable-http"):
        probe_calls.append(dict(headers or {}))
        return probe_results.pop(0)

    async def _auth(mcp_server, task, user_id, auth_events_callback=None, force_refresh=False):
        auth_calls.append(force_refresh)
        return auth_result

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    monkeypatch.setattr(agno_module, "authenticate_mcp_server", _auth)

    asyncio.run(
        agno_module._ensure_remote_mcp_ready(
            mcp=mcp, transport="streamable-http", task=_FakeTask()
        )
    )
    return probe_calls, auth_calls


def test_healthy_server_no_auth_calls(monkeypatch):
    probe_calls, auth_calls = _run_ensure(_mcp(), [None], monkeypatch=monkeypatch)
    assert len(probe_calls) == 1
    assert auth_calls == []


def test_auth_error_heals_token_and_reprobes(monkeypatch):
    token_ready = MCPOAuthGetTokenResponse(
        type=MCPOAuthResponseType.TOKEN_READY,
        data=MCPOAuthGetTokenTokenReadyResponse(access_token="fresh-token"),
    )
    mcp = _mcp()
    probe_calls, auth_calls = _run_ensure(
        mcp, [_http_error(401), None], auth_result=token_ready, monkeypatch=monkeypatch
    )
    assert auth_calls == [True]  # forced refresh
    assert len(probe_calls) == 2
    assert probe_calls[1]["Authorization"] == "Bearer fresh-token"
    assert mcp.api_key == "fresh-token"


def test_auth_error_heal_failure_skips_with_note(monkeypatch) -> None:
    """An unhealable auth error must skip with a reconnect note, never raise -
    a raise would sink every unrelated task on the agent."""
    mcp = _mcp()
    probe_calls = []

    async def _probe(url, headers=None, transport="streamable-http"):
        probe_calls.append(dict(headers or {}))
        return _http_error(401)

    async def _auth(*a, **k):
        return None

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    monkeypatch.setattr(agno_module, "authenticate_mcp_server", _auth)

    ready, note = asyncio.run(
        agno_module._ensure_remote_mcp_ready(mcp=mcp, transport="streamable-http", task=_FakeTask())
    )
    assert ready is False
    assert "sign-in required" in note
    assert "Fathom MCP" in note


def test_non_auth_error_skips_without_auth_attempt(monkeypatch):
    # A non-auth preflight failure (connection/timeout/5xx) now skips the tool
    # (returns False) instead of raising, so one bad server can't sink the rest.
    mcp = _mcp()
    probe_calls = []
    auth_calls = []

    async def _probe(url, headers=None, transport="streamable-http"):
        probe_calls.append(dict(headers or {}))
        return ValueError("connection refused")

    async def _auth(*a, **k):
        auth_calls.append(True)
        return None

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    monkeypatch.setattr(agno_module, "authenticate_mcp_server", _auth)

    ready, note = asyncio.run(
        agno_module._ensure_remote_mcp_ready(mcp=mcp, transport="streamable-http", task=_FakeTask())
    )
    assert ready is False       # skipped, not raised
    assert note is None          # generic unavailable-note, no specific remedy
    assert auth_calls == []      # no auth attempt for a non-auth error
    assert len(probe_calls) == 1


def test_bypass_header_auth_still_heals(monkeypatch):
    """App-supplied user_tokens headers can be stale too; 401 must still start the OAuth flow."""
    token_ready = MCPOAuthGetTokenResponse(
        type=MCPOAuthResponseType.TOKEN_READY,
        data=MCPOAuthGetTokenTokenReadyResponse(access_token="fresh-token"),
    )
    mcp = _mcp(api_key="__bypass__")
    probe_calls, auth_calls = _run_ensure(
        mcp, [_http_error(401), None], auth_result=token_ready, monkeypatch=monkeypatch
    )
    assert auth_calls == [True]
    assert probe_calls[1]["Authorization"] == "Bearer fresh-token"


def test_non_oauth_auth_type_heals_when_server_demands_auth(monkeypatch):
    """401 from the server wins over the configured auth_type; discovery decides support."""
    token_ready = MCPOAuthGetTokenResponse(
        type=MCPOAuthResponseType.TOKEN_READY,
        data=MCPOAuthGetTokenTokenReadyResponse(access_token="fresh-token"),
    )
    mcp = _mcp(auth_type=MCPServerAuthType._None, api_key=None, headers={})
    probe_calls, auth_calls = _run_ensure(
        mcp, [_http_error(401), None], auth_result=token_ready, monkeypatch=monkeypatch
    )
    assert auth_calls == [True]
    assert mcp.auth_type == MCPServerAuthType.OAuth2  # coerced so the backend runs discovery
    assert probe_calls[1]["Authorization"] == "Bearer fresh-token"


def test_strict_init_kill_switch(monkeypatch):
    monkeypatch.setenv("XPANDER_MCP_STRICT_INIT", "false")

    async def _probe(*a, **k):
        raise AssertionError("probe must not run when strict init is off")

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    asyncio.run(
        agno_module._ensure_remote_mcp_ready(
            mcp=_mcp(), transport="streamable-http", task=_FakeTask()
        )
    )
