"""Tests for Agent class."""

import pytest

from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.plugins.mistralai import Agent
from mistralai.workflows.plugins.mistralai.connectors import connector
from mistralai.workflows.plugins.mistralai.connectors.constants import (
    MISTRALAI_PLUGIN_KEY,
    RESOLVED_CONNECTORS_KEY,
)
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs
from mistralai.workflows.plugins.mistralai.session.remote_session import RemoteSession

from .conftest import make_context


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

    @pytest.mark.parametrize("run_as", ["auto", "deployment", None])
    def test_agent_allows_uniform_run_as(self, run_as: str | None):
        """Agent construction allows connectors that share a single run_as."""
        agent = Agent(
            name="test-agent",
            connectors=[connector("jira", run_as=run_as), connector("github", run_as=run_as)],
        )
        assert agent.connectors is not None

    def test_agent_rejects_mixed_run_as(self):
        """Agent construction rejects connectors with differing run_as values."""
        slots = [connector("jira", run_as="auto"), connector("github", run_as="deployment")]
        with pytest.raises(ValueError, match="mixes connector run_as"):
            Agent(name="test-agent", connectors=slots)

    def test_agent_allows_omitted_run_as_alongside_explicit_deployment(self):
        """Omitted run_as means inherit, so it cannot conflict at construction time.

        The slot resolves against the preflight binding later; only explicit values
        can be judged before that.
        """
        slots = [connector("jira"), connector("github", run_as="deployment")]
        agent = Agent(name="test-agent", connectors=slots)
        assert agent.connectors is not None

    def test_agent_rejects_duplicate_connector_names(self):
        """Bindings are keyed by connector_name, so a name may appear at most once."""
        slots = [connector("github"), connector("github")]
        with pytest.raises(ValueError, match="duplicate connector_name"):
            Agent(name="test-agent", connectors=slots)

    def test_agent_reports_duplicate_name_rather_than_mixed_run_as(self):
        """The same name twice is a duplicate, not an identity conflict."""
        slots = [connector("github", run_as="auto"), connector("github", run_as="deployment")]
        with pytest.raises(ValueError, match="duplicate connector_name"):
            Agent(name="test-agent", connectors=slots)

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


class TestAgentConnectorValidation:
    """Tests for validating that agent connectors are resolved via @uses_connectors."""

    def test_raises_when_connector_not_resolved(self) -> None:
        """Agent with connectors raises when @uses_connectors was not applied."""
        ctx = make_context(bindings=[])
        agent = Agent(name="test-agent", connectors=[connector("github")])

        with define_context(ctx):
            with pytest.raises(ValueError, match="not resolved by the workflow") as exc_info:
                RemoteSession._resolve_conversation_run_as(agent)
            assert "github" in str(exc_info.value)
            assert "@uses_connectors" in str(exc_info.value)

    def test_raises_with_clear_message_listing_missing_connectors(self) -> None:
        """Error message includes all unresolved connector names."""
        ctx = make_context(bindings=[])
        github = connector("github")
        slack = connector("slack")
        agent = Agent(name="multi-agent", connectors=[github, slack])

        with define_context(ctx):
            with pytest.raises(ValueError, match="not resolved by the workflow") as exc_info:
                RemoteSession._resolve_conversation_run_as(agent)
            error_msg = str(exc_info.value)
            assert "github" in error_msg
            assert "slack" in error_msg
            assert "@uses_connectors" in error_msg

    def test_passes_when_all_connectors_resolved(self) -> None:
        """No error when all agent connectors have bindings from @uses_connectors."""
        ctx = make_context(
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
            RemoteSession._resolve_conversation_run_as(agent)

    def test_caller_supplied_extensions_do_not_resolve_agent_connector(self) -> None:
        """A forged binding in the caller-writable ``extensions`` is never read.

        Only the worker-only ``trusted_extensions`` channel resolves agent connectors,
        so a caller cannot steer connector identity by populating ``extensions``.
        """
        ctx = WorkflowContext(
            namespace="default",
            execution_id="test-exec-id",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    RESOLVED_CONNECTORS_KEY: {
                        "bindings": [
                            {
                                "connector_name": "github",
                                "connector_id": "forged",
                                "run_as": "deployment",
                                "status": "ready",
                            }
                        ]
                    }
                }
            },
        )
        agent = Agent(name="test-agent", connectors=[connector("github")])

        with define_context(ctx):
            with pytest.raises(ValueError, match="not resolved by the workflow"):
                RemoteSession._resolve_conversation_run_as(agent)

    def test_default_run_as_inherits_binding_run_as(self) -> None:
        """Agent connector slots without run_as inherit the resolved binding."""
        ctx = make_context(
            bindings=[
                {
                    "connector_name": "github",
                    "connector_id": "conn-gh",
                    "run_as": "deployment",
                    "status": "ready",
                }
            ]
        )
        agent = Agent(name="test-agent", connectors=[connector("github")])

        with define_context(ctx):
            assert RemoteSession._resolve_conversation_run_as(agent) == ConnectorRunAs.DEPLOYMENT

        # Resolution is read-only: the caller's slot is left untouched.
        assert agent.connectors is not None
        assert agent.connectors[0].run_as == ConnectorRunAs.AUTO
        assert agent.connectors[0].run_as_explicit is False

    def test_omitted_and_explicit_run_as_resolve_together(self) -> None:
        """An omitted slot inherits deployment and agrees with an explicit one."""
        ctx = make_context(
            bindings=[
                {"connector_name": "github", "connector_id": "conn-gh", "run_as": "deployment", "status": "ready"},
                {"connector_name": "slack", "connector_id": "conn-sl", "run_as": "deployment", "status": "ready"},
            ]
        )
        agent = Agent(name="test-agent", connectors=[connector("github"), connector("slack", run_as="deployment")])

        with define_context(ctx):
            assert RemoteSession._resolve_conversation_run_as(agent) == ConnectorRunAs.DEPLOYMENT

    @pytest.mark.parametrize(
        ("binding_run_as", "slot_run_as"),
        [
            pytest.param("deployment", "auto", id="auto-slot-rejects-deployment-binding"),
            pytest.param("auto", "deployment", id="deployment-slot-rejects-auto-binding"),
        ],
    )
    def test_explicit_run_as_must_match_binding_run_as(self, binding_run_as: str, slot_run_as: str) -> None:
        """Agent connector slots cannot override the preflighted run_as, in either direction."""
        ctx = make_context(
            bindings=[
                {
                    "connector_name": "github",
                    "connector_id": "conn-gh",
                    "run_as": binding_run_as,
                    "status": "ready",
                }
            ]
        )
        agent = Agent(name="test-agent", connectors=[connector("github", run_as=slot_run_as)])

        with define_context(ctx):
            with pytest.raises(ValueError, match="do not match the workflow preflight bindings") as exc_info:
                RemoteSession._resolve_conversation_run_as(agent)

        assert f"agent run_as='{slot_run_as}'" in str(exc_info.value)
        assert f"@uses_connectors run_as='{binding_run_as}'" in str(exc_info.value)

    def test_raises_for_partially_resolved_connectors(self) -> None:
        """Error when some connectors are resolved but not all."""
        ctx = make_context(bindings=[{"connector_name": "github", "connector_id": "conn-gh", "status": "ready"}])
        agent = Agent(name="test-agent", connectors=[connector("github"), connector("slack")])

        with define_context(ctx):
            with pytest.raises(ValueError, match="not resolved") as exc_info:
                RemoteSession._resolve_conversation_run_as(agent)
            error_msg = str(exc_info.value)
            assert "slack" in error_msg
            assert "github" not in error_msg or "slack" in error_msg

    def test_skips_validation_without_workflow_context(self) -> None:
        """No error outside a workflow context (e.g. LocalSession)."""
        agent = Agent(name="test-agent", connectors=[connector("github")])
        # No define_context — simulates running outside a workflow
        RemoteSession._resolve_conversation_run_as(agent)

    def test_skips_validation_for_agent_without_connectors(self) -> None:
        """No validation needed for agents without connectors."""
        ctx = make_context(bindings=[])
        agent = Agent(name="test-agent")

        with define_context(ctx):
            RemoteSession._resolve_conversation_run_as(agent)

    def test_no_extensions_in_context_raises(self) -> None:
        """When context has no connector extensions at all, raises for unresolved connectors."""
        ctx = make_context(bindings=None)
        agent = Agent(name="test-agent", connectors=[connector("github")])

        with define_context(ctx):
            with pytest.raises(ValueError, match="not resolved by the workflow"):
                RemoteSession._resolve_conversation_run_as(agent)
