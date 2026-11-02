"""Tests for the AgentPicks sentinel."""

from agentic_devtools.cli.azure_devops.review_reviewer_models import AGENT_PICKS, AgentPicks


class TestAgentPicks:
    """Tests for AgentPicks and the AGENT_PICKS sentinel."""

    def test_constant_is_instance(self):
        """AGENT_PICKS is an instance of AgentPicks."""
        assert isinstance(AGENT_PICKS, AgentPicks)

    def test_repr_is_stable_label(self):
        """repr renders a stable, log-friendly label."""
        assert repr(AGENT_PICKS) == "AGENT_PICKS"
