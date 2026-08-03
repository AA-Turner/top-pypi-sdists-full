"""PRO-1992: bound the MCP preflight tail — timeout cap, negative cache, and
graceful skip (oauth-no-user / non-auth failure) that tells the agent via a note."""

import asyncio
from types import SimpleNamespace

import pytest

from xpander_sdk.modules.backend.frameworks import agno as agno_module
from xpander_sdk.modules.backend.utils import mcp_connect
from xpander_sdk.modules.backend.utils.mcp_connect import (
    PROBE_OVERALL_TIMEOUT,
    mark_probe_failed,
    probe_recently_failed,
)
from xpander_sdk.modules.tools_repository.models.mcp import (
    MCPServerAuthType,
    MCPServerDetails,
)


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    mcp_connect.clear_probe_cache()
    monkeypatch.setenv("XPANDER_MCP_STRICT_INIT", "true")
    yield
    mcp_connect.clear_probe_cache()


def _remote(url, auth_type=MCPServerAuthType._None, **kw):
    return MCPServerDetails(url=url, name=url, auth_type=auth_type, **kw)


def _agent(mcp_servers, agent_id="agent1"):
    return SimpleNamespace(
        id=agent_id,
        mcp_servers=list(mcp_servers),
        tools=SimpleNamespace(functions=["base_tool"]),
        graph=SimpleNamespace(items=[]),
        pre_auth_audiences=None,
        oidc_pre_auth_token_mcp_audience=None,
    )


def _task(user_id=None):
    user = SimpleNamespace(id=user_id) if user_id else None
    return SimpleNamespace(
        input=SimpleNamespace(user=user), mcp_servers=None, user_tokens=None
    )


def test_probe_timeout_default_capped():
    assert PROBE_OVERALL_TIMEOUT == 10  # was 60; caps the hot-path hang


def test_negative_cache_skips_reprobe(monkeypatch):
    monkeypatch.setattr(mcp_connect, "PROBE_CACHE_ENABLED", True)
    probes = []

    async def _probe(url, headers=None, transport="streamable-http"):
        probes.append(url)
        return ValueError("connection refused")  # non-auth failure

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    mcp = _remote("https://dead/mcp")

    r1 = asyncio.run(
        agno_module._ensure_remote_mcp_ready(
            mcp=mcp, transport="streamable-http", agent_id="a1"
        )
    )
    r2 = asyncio.run(
        agno_module._ensure_remote_mcp_ready(
            mcp=mcp, transport="streamable-http", agent_id="a1"
        )
    )

    assert r1 == (False, None) and r2 == (False, None)
    assert len(probes) == 1  # second call short-circuits on the negative cache
    assert probe_recently_failed("a1", mcp.url, mcp.headers)


@pytest.mark.asyncio
async def test_oauth_no_user_skips_tool_and_records_note(monkeypatch):
    async def _probe(*a, **k):
        raise AssertionError("should not probe an oauth MCP with no user")

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    mcp = _remote("https://needs-auth/mcp", auth_type=MCPServerAuthType.OAuth2)
    agent = _agent([mcp])
    notes = []

    tools = await agno_module._resolve_agent_tools(
        agent=agent, task=_task(user_id=None), skipped_notes=notes
    )

    assert tools == ["base_tool"]  # MCP skipped, base tools remain
    assert len(notes) == 1 and "requires a signed-in user" in notes[0]


@pytest.mark.asyncio
async def test_non_auth_failure_skips_that_tool_keeps_healthy(monkeypatch):
    async def _probe(url, headers=None, transport="streamable-http"):
        return ValueError("refused") if "bad" in url else None

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    agent = _agent([_remote("https://bad/mcp"), _remote("https://good/mcp")])
    notes = []

    tools = await agno_module._resolve_agent_tools(
        agent=agent, task=_task("u1"), skipped_notes=notes
    )

    # base tool + the one healthy MCP; the bad one is skipped, not fatal
    assert "base_tool" in tools
    assert len([t for t in tools if t != "base_tool"]) == 1
    assert len(notes) == 1 and "temporarily unavailable" in notes[0]


@pytest.mark.asyncio
async def test_all_healthy_no_notes(monkeypatch):
    async def _probe(*a, **k):
        return None

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    agent = _agent([_remote("https://good/mcp")])
    notes = []

    tools = await agno_module._resolve_agent_tools(
        agent=agent, task=_task("u1"), skipped_notes=notes
    )

    assert notes == []
    assert len([t for t in tools if t != "base_tool"]) == 1
