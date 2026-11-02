"""Tests for AgentTaskSessionLifecycle."""

from agentic_devtools.cli.ci.models import AgentTaskSessionLifecycle


def test_agent_task_session_lifecycle_defaults_optional_timestamps() -> None:
    """Allows absent start and idle timestamps to use the parent task clock."""
    session = AgentTaskSessionLifecycle("session-1", "idle")

    assert session.started_at == ""
    assert session.idle_at == ""
