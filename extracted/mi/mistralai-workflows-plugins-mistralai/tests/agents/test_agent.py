"""Tests for Agent class."""

from typing import Any

import pytest

from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.plugins.mistralai import Agent
from mistralai.workflows.plugins.mistralai.connectors import connector
from mistralai.workflows.plugins.mistralai.connectors.constants import (
    MISTRALAI_PLUGIN_KEY,
    RESOLVED_CONNECTORS_KEY,
)
from mistralai.workflows.plugins.mistralai.session.remote_session import RemoteSession


class TestAgent:
    def test_agent_creation_with_defaults(self):
        """Test creating an agent with default values."""
        agent = Agent(name="test-agent")
        assert agent.name == "test-agent"
        assert agent.model == "mistral-medium-latest"
        assert agent.tools is None
        assert agent.handoffs is None
        assert agent.mcp_clients is None
        assert agent.connectors is None

    def test_agent_creation_with_custom_model(self):
        """Test creating an agent with a custom model."""
        agent = Agent(name="test-agent", model="mistral-large-latest")
        assert agent.model == "mistral-large-latest"

    def test_agent_creation_with_instructions(self):
        """Test creating an agent with instructions."""
        instructions = "You are a helpful assistant."
        agent = Agent(name="test-agent", instructions=instructions)
        assert agent.instructions == instructions

    def test_agent_hash(self):
        """Test that agents can be hashed (for use in dicts/sets)."""
        agent1 = Agent(name="test-agent")
        agent2 = Agent(name="test-agent")
        assert hash(agent1) != hash(agent2)

    def test_agent_creation_with_connectors(self):
        """Test creating an agent with connector slots."""
        github = connector("github_app")
        slack = connector("slack")
        agent = Agent(name="test-agent", connectors=[github, slack])
        assert agent.connectors is not None
        assert len(agent.connectors) == 2
        assert agent.connectors[0].connector_name == "github_app"
        assert agent.connectors[1].connector_name == "slack"

    def test_agent_rejects_credentials_name(self):
        """Agent construction rejects connectors with credentials_name."""
        slot = connector("jira", credentials_name="jira_sa")
        with pytest.raises(ValueError, match="credentials_name"):
            Agent(name="test-agent", connectors=[slot])

    def test_iterate_agents_deeply_single_agent(self):
        """Test iterating over a single agent with no handoffs."""
        agent = Agent(name="test-agent")
        agents = list(Agent.iterate_agents_deeply_in_handoffs(agent))
        assert len(agents) == 1
        assert agents[0] is agent

    def test_iterate_agents_deeply_with_handoffs(self):
        """Test iterating over agents with handoffs."""
        child1 = Agent(name="child1")
        child2 = Agent(name="child2")
        parent = Agent(name="parent", handoffs=[child1, child2])

        agents = list(Agent.iterate_agents_deeply_in_handoffs(parent))
        assert len(agents) == 3
        assert parent in agents
        assert child1 in agents
        assert child2 in agents

    def test_iterate_agents_deeply_avoids_cycles(self):
        """Test that iteration handles circular handoffs."""
        agent1 = Agent(name="agent1")
        agent2 = Agent(name="agent2")
        agent1.handoffs = [agent2]
        agent2.handoffs = [agent1]

        agents = list(Agent.iterate_agents_deeply_in_handoffs(agent1))
        assert len(agents) == 2


def _make_context(bindings: list[dict[str, Any]] | None = None) -> WorkflowContext:
    trusted_extensions: dict[str, Any] = {}
    if bindings is not None:
        trusted_extensions[MISTRALAI_PLUGIN_KEY] = {RESOLVED_CONNECTORS_KEY: {"bindings": bindings}}
    return WorkflowContext(
        namespace="default",
        execution_id="test-exec-id",
        trusted_extensions=trusted_extensions,
    )


class TestAgentConnectorValidation:
    """Tests for validating that agent connectors are resolved via @uses_connectors."""

    def test_raises_when_connector_not_resolved(self) -> None:
        """Agent with connectors raises when @uses_connectors was not applied."""
        ctx = _make_context(bindings=[])
        agent = Agent(name="test-agent", connectors=[connector("github")])

        with define_context(ctx):
            with pytest.raises(ValueError, match="not resolved by the workflow") as exc_info:
                RemoteSession._validate_connector_bindings(agent)
            assert "github" in str(exc_info.value)
            assert "@uses_connectors" in str(exc_info.value)

    def test_raises_with_clear_message_listing_missing_connectors(self) -> None:
        """Error message includes all unresolved connector names."""
        ctx = _make_context(bindings=[])
        github = connector("github")
        slack = connector("slack")
        agent = Agent(name="multi-agent", connectors=[github, slack])

        with define_context(ctx):
            with pytest.raises(ValueError, match="not resolved by the workflow") as exc_info:
                RemoteSession._validate_connector_bindings(agent)
            error_msg = str(exc_info.value)
            assert "github" in error_msg
            assert "slack" in error_msg
            assert "@uses_connectors" in error_msg

    def test_passes_when_all_connectors_resolved(self) -> None:
        """No error when all agent connectors have bindings from @uses_connectors."""
        ctx = _make_context(
            bindings=[
                {"connector_name": "github", "connector_id": "conn-gh", "status": "ready"},
                {"connector_name": "slack", "connector_id": "conn-sl", "status": "ready"},
            ]
        )
        github = connector("github")
        slack = connector("slack")
        agent = Agent(name="test-agent", connectors=[github, slack])

        with define_context(ctx):
            # Should not raise
            RemoteSession._validate_connector_bindings(agent)

    def test_raises_for_partially_resolved_connectors(self) -> None:
        """Error when some connectors are resolved but not all."""
        ctx = _make_context(bindings=[{"connector_name": "github", "connector_id": "conn-gh", "status": "ready"}])
        agent = Agent(name="test-agent", connectors=[connector("github"), connector("slack")])

        with define_context(ctx):
            with pytest.raises(ValueError, match="not resolved") as exc_info:
                RemoteSession._validate_connector_bindings(agent)
            error_msg = str(exc_info.value)
            assert "slack" in error_msg
            assert "github" not in error_msg or "slack" in error_msg

    def test_skips_validation_without_workflow_context(self) -> None:
        """No error outside a workflow context (e.g. LocalSession)."""
        agent = Agent(name="test-agent", connectors=[connector("github")])
        # No define_context — simulates running outside a workflow
        RemoteSession._validate_connector_bindings(agent)

    def test_skips_validation_for_agent_without_connectors(self) -> None:
        """No validation needed for agents without connectors."""
        ctx = _make_context(bindings=[])
        agent = Agent(name="test-agent")

        with define_context(ctx):
            RemoteSession._validate_connector_bindings(agent)

    def test_no_extensions_in_context_raises(self) -> None:
        """When context has no connector extensions at all, raises for unresolved connectors."""
        ctx = _make_context(bindings=None)
        agent = Agent(name="test-agent", connectors=[connector("github")])

        with define_context(ctx):
            with pytest.raises(ValueError, match="not resolved by the workflow"):
                RemoteSession._validate_connector_bindings(agent)
