"""Graph-building tests for connector resolution using the real connectors factory.

The core suite (`workflow_sdk/tests/test_graph_static_analysis.py`) cannot import the
connectors plugin, so it covers the hardening (a non-connectors `connector` factory is
ignored). These tests exercise the positive path with the genuine factory.
"""

from __future__ import annotations

from mistralai.workflows import workflow
from mistralai.workflows.core._graph import build_graph_dynamically
from mistralai.workflows.plugins.mistralai import Agent, Runner
from mistralai.workflows.plugins.mistralai.connectors import connector

BOUND_CONNECTOR = connector("bound_connector")


@workflow.define(name="dynamic_agent_real_connector_workflow")
class DynamicAgentRealConnectorWorkflow:
    @workflow.entrypoint
    async def run(self) -> None:
        await Runner.run(
            agent=Agent(
                name="connector-agent",
                connectors=[connector("inline_connector"), BOUND_CONNECTOR],
            ),
            inputs="hello",
        )


def test_dynamic_agent_resolves_inline_and_bound_real_connectors() -> None:
    graph = build_graph_dynamically(DynamicAgentRealConnectorWorkflow)

    agent_nodes = [node for node in graph.nodes if node.type == "agent"]

    assert len(agent_nodes) == 1
    assert agent_nodes[0].connectors == ["inline_connector", "bound_connector"]
