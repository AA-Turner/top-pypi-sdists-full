"""MCP preflight: concurrent probing, cross-task reuse cache, and stale re-probe/heal."""

import asyncio
import time
from types import SimpleNamespace

import pytest

from xpander_sdk.modules.backend.frameworks import agno as agno_module
from xpander_sdk.modules.backend.utils import mcp_connect
from xpander_sdk.modules.tools_repository.models.mcp import (
    MCPOAuthGetTokenResponse,
    MCPOAuthGetTokenTokenReadyResponse,
    MCPOAuthResponseType,
    MCPServerAuthType,
    MCPServerDetails,
)


@pytest.fixture(autouse=True)
def _clean_probe_cache():
    mcp_connect.clear_probe_cache()
    yield
    mcp_connect.clear_probe_cache()


def _remote_mcp(url: str, name: str = None) -> MCPServerDetails:
    return MCPServerDetails(
        url=url, name=name or url, auth_type=MCPServerAuthType._None
    )


def _fake_agent(mcp_servers, agent_id: str = "agent1") -> SimpleNamespace:
    """Minimal duck-typed agent covering only what _resolve_agent_tools reads."""
    return SimpleNamespace(
        id=agent_id,
        mcp_servers=list(mcp_servers),
        tools=SimpleNamespace(functions=[]),
        graph=SimpleNamespace(items=[]),
        pre_auth_audiences=None,
        oidc_pre_auth_token_mcp_audience=None,
    )


class _User:
    id = "u1"


class _Input:
    user = _User()


class _FakeTask:
    input = _Input()


def test_probes_run_concurrently_wall_time_is_max_not_sum(monkeypatch):
    """Two servers' preflights overlap: wall-time tracks the slowest probe, not the sum."""
    delay = 0.3
    probe_calls = []

    async def _probe(url, headers=None, transport="streamable-http"):
        probe_calls.append(url)
        await asyncio.sleep(delay)
        return None

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    agent = _fake_agent([_remote_mcp("https://a/mcp"), _remote_mcp("https://b/mcp")])

    start = time.monotonic()
    tools = asyncio.run(agno_module._resolve_agent_tools(agent=agent))
    elapsed = time.monotonic() - start

    assert len(probe_calls) == 2
    # serial would be ~2*delay; concurrent stays well under 1.8*delay
    assert elapsed < delay * 1.8
    assert len(tools) == 2  # one MCPTools per server


def test_one_probe_per_server_per_task(monkeypatch):
    """A single build probes each distinct server exactly once."""
    probe_calls = []

    async def _probe(url, headers=None, transport="streamable-http"):
        probe_calls.append(url)
        return None

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    agent = _fake_agent([_remote_mcp("https://a/mcp"), _remote_mcp("https://b/mcp")])

    asyncio.run(agno_module._resolve_agent_tools(agent=agent))

    assert sorted(probe_calls) == ["https://a/mcp", "https://b/mcp"]


def test_reuse_cache_skips_probe_on_repeat_task(monkeypatch):
    """A second task for the same agent/server/token reuses the healthy marker (no re-probe)."""
    monkeypatch.setattr(mcp_connect, "PROBE_CACHE_ENABLED", True)
    probe_calls = []

    async def _probe(url, headers=None, transport="streamable-http"):
        probe_calls.append(url)
        return None

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    agent = _fake_agent([_remote_mcp("https://a/mcp")])

    asyncio.run(agno_module._resolve_agent_tools(agent=agent))
    asyncio.run(agno_module._resolve_agent_tools(agent=agent))

    assert probe_calls == ["https://a/mcp"]  # only the first task pays the probe


def test_expired_marker_triggers_reprobe(monkeypatch):
    """Once the reuse window lapses (server idle-timeout), the next task re-probes."""
    monkeypatch.setattr(mcp_connect, "PROBE_CACHE_ENABLED", True)
    probe_calls = []

    async def _probe(url, headers=None, transport="streamable-http"):
        probe_calls.append(url)
        return None

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    agent = _fake_agent([_remote_mcp("https://a/mcp")])

    asyncio.run(agno_module._resolve_agent_tools(agent=agent))
    assert len(probe_calls) == 1

    # age every healthy marker past its TTL
    for key in list(mcp_connect._probe_ready_until):
        mcp_connect._probe_ready_until[key] = time.monotonic() - 1.0

    asyncio.run(agno_module._resolve_agent_tools(agent=agent))
    assert len(probe_calls) == 2


def test_stale_marker_then_auth_error_heals_and_recaches(monkeypatch):
    """After the window lapses, a now-401 server is re-probed, healed, and re-marked."""
    monkeypatch.setattr(mcp_connect, "PROBE_CACHE_ENABLED", True)
    token_ready = MCPOAuthGetTokenResponse(
        type=MCPOAuthResponseType.TOKEN_READY,
        data=MCPOAuthGetTokenTokenReadyResponse(access_token="fresh-token"),
    )
    probe_results = [None, _http_401(), None]  # ok -> (expire) -> 401 -> healed ok
    probe_calls = []
    auth_calls = []

    async def _probe(url, headers=None, transport="streamable-http"):
        probe_calls.append(dict(headers or {}))
        return probe_results.pop(0)

    async def _auth(
        mcp_server, task, user_id, auth_events_callback=None, force_refresh=False
    ):
        auth_calls.append(force_refresh)
        return token_ready

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    monkeypatch.setattr(agno_module, "authenticate_mcp_server", _auth)

    mcp = _remote_mcp("https://a/mcp")

    async def _ensure():
        await agno_module._ensure_remote_mcp_ready(
            mcp=mcp, transport="streamable-http", task=_FakeTask(), agent_id="agent1"
        )

    asyncio.run(_ensure())
    assert mcp_connect.probe_recently_ok("agent1", mcp.url, mcp.headers)

    # expire the marker, then a stale token gets healed on the forced re-probe
    for key in list(mcp_connect._probe_ready_until):
        mcp_connect._probe_ready_until[key] = time.monotonic() - 1.0

    asyncio.run(_ensure())

    assert auth_calls == [True]
    assert mcp.api_key == "fresh-token"
    assert len(probe_calls) == 3
    # the refreshed token re-establishes a healthy marker under its new key
    assert mcp_connect.probe_recently_ok("agent1", mcp.url, mcp.headers)


def _http_401():
    import httpx

    req = httpx.Request("POST", "https://a/mcp")
    return httpx.HTTPStatusError(
        "401", request=req, response=httpx.Response(401, request=req)
    )
