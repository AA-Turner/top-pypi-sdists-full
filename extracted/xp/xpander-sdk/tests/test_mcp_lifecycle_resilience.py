"""MCP lifecycle: transport/type coherence coercion and non-blocking init -
a broken server is skipped with a note, never a run-killing raise."""

import asyncio
from types import SimpleNamespace

import pytest

from xpander_sdk.modules.backend.frameworks import agno as agno_module
from xpander_sdk.modules.backend.utils import mcp_connect
from xpander_sdk.modules.tools_repository.models.mcp import (
    MCPServerAuthType,
    MCPServerDetails,
    MCPServerTransport,
    MCPServerType,
)


@pytest.fixture(autouse=True)
def _clean_probe_cache():
    mcp_connect.clear_probe_cache()
    yield
    mcp_connect.clear_probe_cache()


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
    user_tokens = None
    mcp_servers = None


class TestTransportTypeCoherence:
    """Mirror of xpander_dev_utils' AIAgentGraphItemMCPSettings coercion - keep in sync."""

    def test_local_with_http_transport_coerced_to_stdio(self) -> None:
        mcp = MCPServerDetails(
            type=MCPServerType.Local,
            command="echo hi",
            transport=MCPServerTransport.HTTP_Transport,
        )
        assert mcp.transport == MCPServerTransport.STDIO

    def test_remote_with_stdio_transport_coerced_to_http(self) -> None:
        mcp = MCPServerDetails(
            type=MCPServerType.Remote,
            url="https://x/mcp",
            transport=MCPServerTransport.STDIO,
        )
        assert mcp.transport == MCPServerTransport.HTTP_Transport

    def test_coherent_pairs_untouched(self) -> None:
        sse = MCPServerDetails(url="https://x/mcp", transport=MCPServerTransport.SSE)
        assert sse.transport == MCPServerTransport.SSE
        local = MCPServerDetails(
            type=MCPServerType.Local, command="echo", transport=MCPServerTransport.STDIO
        )
        assert local.transport == MCPServerTransport.STDIO

    def test_legacy_raw_dict_still_parses(self) -> None:
        mcp = MCPServerDetails(
            **{"type": "local", "command": "echo", "transport": "streamable-http"}
        )
        assert mcp.transport == MCPServerTransport.STDIO

    def test_explicit_null_transport_normalized(self) -> None:
        mcp = MCPServerDetails(**{"type": "remote", "url": "https://x/mcp", "transport": None})
        assert mcp.transport == MCPServerTransport.HTTP_Transport


class TestNonBlockingInit:
    def test_local_without_command_skips_with_note(self) -> None:
        mcp = MCPServerDetails(type=MCPServerType.Local, name="broken-local", command=None)
        agent = _fake_agent([mcp])
        notes: list = []
        tools = asyncio.run(
            agno_module._resolve_agent_tools(agent=agent, skipped_notes=notes)
        )
        assert tools == []
        assert any("broken-local" in n and "misconfigured" in n for n in notes)

    def test_ghost_remote_without_url_skips_with_note(self) -> None:
        mcp = MCPServerDetails(type=MCPServerType.Remote, name="ghost", url=None)
        agent = _fake_agent([mcp])
        notes: list = []
        tools = asyncio.run(
            agno_module._resolve_agent_tools(agent=agent, skipped_notes=notes)
        )
        assert tools == []
        assert any("ghost" in n and "no longer available" in n for n in notes)

    def test_unhealed_auth_error_skips_with_reconnect_note(self, monkeypatch) -> None:
        import httpx

        req = httpx.Request("POST", "https://bria/mcp")
        err_401 = httpx.HTTPStatusError(
            "status 401", request=req, response=httpx.Response(401, request=req)
        )

        async def _probe(url, headers=None, transport="streamable-http"):
            return err_401

        async def _auth(*a, **k):
            return None

        monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
        monkeypatch.setattr(agno_module, "authenticate_mcp_server", _auth)

        mcp = MCPServerDetails(
            url="https://bria/mcp", name="Bria", auth_type=MCPServerAuthType._None,
            api_key="stale",
        )
        agent = _fake_agent([mcp])
        notes: list = []
        tools = asyncio.run(
            agno_module._resolve_agent_tools(
                agent=agent, task=_FakeTask(), skipped_notes=notes
            )
        )
        assert tools == []
        assert any("Bria" in n and "sign-in required" in n for n in notes)

    def test_token_refresh_timeout_skips_with_auth_note(self, monkeypatch) -> None:
        """A hung OAuth refresh must hit the cap and skip, not stall tool assembly."""
        import httpx

        req = httpx.Request("POST", "https://slow/mcp")
        err_401 = httpx.HTTPStatusError(
            "status 401", request=req, response=httpx.Response(401, request=req)
        )

        async def _probe(url, headers=None, transport="streamable-http"):
            return err_401

        async def _hung_auth(*a, **k):
            await asyncio.sleep(60)

        monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
        monkeypatch.setattr(agno_module, "authenticate_mcp_server", _hung_auth)
        monkeypatch.setattr(agno_module, "MCP_TOKEN_REFRESH_TIMEOUT_SECONDS", 0.05)

        mcp = MCPServerDetails(url="https://slow/mcp", name="Slow", api_key="stale")
        ready, note = asyncio.run(
            agno_module._ensure_remote_mcp_ready(
                mcp=mcp, transport="streamable-http", task=_FakeTask()
            )
        )
        assert ready is False
        assert "sign-in required" in note

    def test_one_raising_server_does_not_sink_the_others(self, monkeypatch) -> None:
        """The incident shape: one bad org MCP must not kill the whole tool build."""
        real_ensure = agno_module._ensure_remote_mcp_ready

        async def _ensure(mcp, transport, **kwargs):
            if "bad" in (mcp.url or ""):
                raise RuntimeError("boom during preflight")
            return await real_ensure(mcp=mcp, transport=transport, **kwargs)

        async def _probe(url, headers=None, transport="streamable-http"):
            return None  # healthy

        monkeypatch.setattr(agno_module, "_ensure_remote_mcp_ready", _ensure)
        monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)

        servers = [
            MCPServerDetails(url="https://good-1/mcp", name="good-1"),
            MCPServerDetails(url="https://bad/mcp", name="bad-server"),
            MCPServerDetails(url="https://good-2/mcp", name="good-2"),
        ]
        agent = _fake_agent(servers)
        notes: list = []
        tools = asyncio.run(
            agno_module._resolve_agent_tools(agent=agent, skipped_notes=notes)
        )
        assert len(tools) == 2
        assert any("bad-server" in n and "misconfigured or unreachable" in n for n in notes)
