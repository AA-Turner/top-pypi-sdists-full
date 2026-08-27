"""Joining a runtime MCP server back to its graph item, whose id keys task.user_tokens."""

from types import SimpleNamespace
from typing import Any

from xpander_sdk.modules.agents.models.agent import AgentGraphItemType
from xpander_sdk.modules.backend.frameworks.agno import _graph_item_for_mcp
from xpander_sdk.modules.tools_repository.models.mcp import MCPServerDetails

URL = "https://mcp.example.com/mcp"


def _node(node_id: str, **mcp_kwargs: Any) -> SimpleNamespace:
    """A graph node carrying MCP settings, shaped as the join reads it."""
    return SimpleNamespace(
        id=node_id,
        type=AgentGraphItemType.MCP,
        settings=SimpleNamespace(mcp_settings=MCPServerDetails(**mcp_kwargs)),
    )


def _agent(*nodes: SimpleNamespace) -> SimpleNamespace:
    """An agent whose graph holds exactly these nodes."""
    return SimpleNamespace(graph=SimpleNamespace(items=list(nodes)))


def test_the_id_survives_construction_from_a_payload() -> None:
    """Without the field pydantic drops it, and the join can never see it."""
    assert MCPServerDetails(**{"url": URL, "id": "reg-1"}).id == "reg-1"


def test_two_nodes_on_one_url_each_resolve_to_their_own() -> None:
    """The registry allows one url twice under two names; a url cannot tell them apart."""
    agent = _agent(
        _node("node-a", id="reg-a", url=URL), _node("node-b", id="reg-b", url=URL)
    )

    assert (
        _graph_item_for_mcp(agent, MCPServerDetails(id="reg-b", url=URL)).id == "node-b"
    )
    assert (
        _graph_item_for_mcp(agent, MCPServerDetails(id="reg-a", url=URL)).id == "node-a"
    )


def test_a_url_spelled_differently_still_joins_on_id() -> None:
    """The id is the join, so the url's spelling stops mattering once both sides carry one."""
    agent = _agent(_node("node-a", id="reg-a", url=URL))
    assert (
        _graph_item_for_mcp(agent, MCPServerDetails(id="reg-a", url=URL + "/")).id
        == "node-a"
    )


def test_an_id_matching_no_node_resolves_to_nothing() -> None:
    """Guessing by url would hand this server another node's token."""
    agent = _agent(
        _node("node-a", id="reg-a", url=URL), _node("node-b", id="reg-b", url=URL)
    )
    assert _graph_item_for_mcp(agent, MCPServerDetails(id="reg-gone", url=URL)) is None


def test_without_ids_it_falls_back_to_url_equality() -> None:
    """An old backend sends no id on either side and must keep resolving as it does today."""
    agent = _agent(_node("node-a", url=URL))
    assert _graph_item_for_mcp(agent, MCPServerDetails(url=URL)).id == "node-a"


def test_a_node_carrying_an_id_still_answers_a_server_without_one() -> None:
    """A task-supplied server has no id; the node's own id must not lock it out."""
    agent = _agent(_node("node-a", id="reg-a", url=URL))
    assert _graph_item_for_mcp(agent, MCPServerDetails(url=URL)).id == "node-a"


def test_an_ambiguous_url_resolves_to_nothing() -> None:
    """With no id to separate them, picking the first node would be a coin flip on credentials."""
    agent = _agent(
        _node("node-a", id="reg-a", url=URL), _node("node-b", id="reg-b", url=URL)
    )
    assert _graph_item_for_mcp(agent, MCPServerDetails(url=URL)) is None


def test_a_task_supplied_server_matches_nothing() -> None:
    """A server the agent's graph never had resolves to no node, so no token is injected."""
    agent = _agent(_node("node-a", id="reg-a", url=URL))
    other = MCPServerDetails(url="https://other.example.com/mcp")
    assert _graph_item_for_mcp(agent, other) is None


def test_an_agent_with_no_graph_matches_nothing() -> None:
    """The join is called before any graph is guaranteed to exist."""
    assert _graph_item_for_mcp(SimpleNamespace(), MCPServerDetails(url=URL)) is None


def test_a_node_with_no_url_is_not_matched_by_a_urlless_server() -> None:
    """Two servers with neither id nor url are indistinguishable; matching them would be a guess."""
    agent = _agent(_node("node-a", command="npx -y pkg"))
    assert _graph_item_for_mcp(agent, MCPServerDetails(command="npx -y pkg")) is None


def _gated_node(node_id: str, tool_names: list, **mcp_kwargs: Any) -> SimpleNamespace:
    """A graph node whose approval rule is on, scoped to these tool names."""
    node = _node(node_id, **mcp_kwargs)
    node.item_id = node_id
    node.name = mcp_kwargs.get("name") or node_id
    node.settings.hitl_options = SimpleNamespace(enabled=True, tool_names=tool_names)
    return node


def test_two_gated_nodes_on_one_url_keep_their_own_rule_keys() -> None:
    """Keyed only by url, the second node's scope is lost and its tools run ungated."""
    from xpander_sdk.modules.backend.frameworks.agno import _mcp_gated_servers

    agent = _agent(
        _gated_node("node-a", ["read"], id="reg-a", url=URL, name="A"),
        _gated_node("node-b", ["write"], id="reg-b", url=URL, name="B"),
    )
    gated = {
        item_id: (keys, scoped) for item_id, keys, scoped in _mcp_gated_servers(agent)
    }

    assert set(gated) == {"node-a", "node-b"}
    # the registry id is a key, so a same-url sibling cannot claim this node's rule
    assert "reg-a" in gated["node-a"][0] and "reg-b" in gated["node-b"][0]
    assert gated["node-a"][1] == ["read"] and gated["node-b"][1] == ["write"]
