"""Where a local (stdio) MCP server runs, and what the late dynamic-tools collapse may take."""

import asyncio
from types import SimpleNamespace

import pytest

from xpander_sdk.modules.agents.models.agent import AgentDeploymentType
from xpander_sdk.modules.backend.frameworks import agno as agno_module
from xpander_sdk.modules.backend.utils import workspace_mcp
from xpander_sdk.modules.tools_repository.models.mcp import (
    MCPServerAuthType,
    MCPServerDetails,
    MCPServerType,
)

LIST_RESPONSE = {
    "server_key": "k",
    "tools": [
        {"name": f"t{i}", "description": "", "input_schema": {"type": "object"}}
        for i in range(60)
    ],
}


def _local_mcp(command: str = "npx -y some-mcp") -> MCPServerDetails:
    return MCPServerDetails(type=MCPServerType.Local, command=command, name="Some MCP")


def _remote_mcp(url: str = "https://a/mcp") -> MCPServerDetails:
    return MCPServerDetails(url=url, name=url, auth_type=MCPServerAuthType._None)


class _Repo:
    """The slice of the tools repository the resolver touches."""

    def __init__(self, catalog=None):
        self.functions = []
        self.dynamic_catalog_items = catalog or []
        self._dynamic_mcp_proxies = []
        self._dynamic_mcp_toolkits = []

    @property
    def dynamic_catalog(self):
        return self.dynamic_catalog_items + self._dynamic_mcp_proxies


def _agent(
    mcp_servers, *, deployment_type=AgentDeploymentType.Serverless, use_dynamic=False
):
    return SimpleNamespace(
        id="agent1",
        mcp_servers=list(mcp_servers),
        tools=_Repo(),
        graph=SimpleNamespace(items=[]),
        pre_auth_audiences=None,
        oidc_pre_auth_token_mcp_audience=None,
        configuration=None,
        deployment_type=deployment_type,
        workspace_tools_enabled=True,
        use_dynamic_tools=use_dynamic,
    )


@pytest.fixture
def bridge(monkeypatch):
    calls = []

    class _Client:
        async def make_request(self, path, method="GET", payload=None, **_):
            calls.append(path)
            if path.endswith("mcp_list_tools"):
                return LIST_RESPONSE
            return {"content": "ok", "is_error": False}

    monkeypatch.setattr(
        workspace_mcp, "APIClient", lambda configuration=None: _Client()
    )
    return calls


def test_a_serverless_agent_hosts_a_local_server_in_its_workspace(bridge):
    tools = asyncio.run(agno_module._resolve_agent_tools(agent=_agent([_local_mcp()])))

    assert len(tools) == 1
    assert isinstance(tools[0], workspace_mcp.WorkspaceMCPTools)
    assert any(p.endswith("mcp_list_tools") for p in bridge)


def test_a_container_agent_still_spawns_it_in_process(bridge, monkeypatch):
    built = []

    class _FakeMCPTools:
        def __init__(self, **kwargs):
            built.append(kwargs)
            self.functions = {}

    monkeypatch.setattr("agno.tools.mcp.MCPTools", _FakeMCPTools)
    tools = asyncio.run(
        agno_module._resolve_agent_tools(
            agent=_agent([_local_mcp()], deployment_type=AgentDeploymentType.Container)
        )
    )

    assert len(tools) == 1 and isinstance(tools[0], _FakeMCPTools)
    assert built[0]["transport"] == "stdio"
    assert bridge == []


def test_the_aws_server_is_still_skipped_on_cloud(bridge, monkeypatch):
    """The serverless guard has to outrank the workspace branch, or it stops applying."""
    monkeypatch.setattr(
        agno_module,
        "getenv",
        lambda k, d=None: "true" if k == "IS_XPANDER_CLOUD" else d,
    )
    notes = []
    tools = asyncio.run(
        agno_module._resolve_agent_tools(
            agent=_agent([_local_mcp("uvx awslabs.aws-api-mcp-server")]),
            skipped_notes=notes,
        )
    )

    assert tools == []
    assert bridge == []


def test_a_workspaceless_agent_gets_a_note_instead_of_a_crash(bridge):
    agent = _agent([_local_mcp()])
    agent.workspace_tools_enabled = False
    notes = []

    tools = asyncio.run(
        agno_module._resolve_agent_tools(agent=agent, skipped_notes=notes)
    )

    assert tools == []
    assert any("workspace" in n for n in notes)
    assert bridge == []


def test_the_late_collapse_hides_a_big_local_server(bridge):
    agent = _agent([_local_mcp()], use_dynamic=True)

    tools = asyncio.run(agno_module._resolve_agent_tools(agent=agent))

    assert (
        tools == []
    )  # 60 tools >= the default 50 gate, so they hide behind the meta-tools
    assert len(agent.tools._dynamic_mcp_proxies) == 60
    assert agent.tools._dynamic_mcp_toolkits


def test_the_late_collapse_never_drops_a_remote_server(bridge, monkeypatch):
    """A remote toolkit is unconnected here, so collapsing it would delete its tools."""

    async def _probe(url, headers=None, transport="streamable-http"):
        return None

    monkeypatch.setattr(agno_module, "probe_mcp_server", _probe)
    agent = _agent([_local_mcp(), _remote_mcp()], use_dynamic=True)

    tools = asyncio.run(agno_module._resolve_agent_tools(agent=agent))

    assert len(tools) == 1
    assert not isinstance(tools[0], workspace_mcp.WorkspaceMCPTools)
    assert len(agent.tools._dynamic_mcp_proxies) == 60
