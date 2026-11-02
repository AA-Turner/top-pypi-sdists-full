"""Tests for CopilotSessionSummary."""

from agentic_devtools.cli.ci.models import CopilotSessionSummary


def test_copilot_session_summary_defaults() -> None:
    """Constructs an immutable summary with the documented defaults."""
    summary = CopilotSessionSummary(task_id="task-1", session_id="session-1", pr_number=42, started_at="2026-01-01")

    assert summary.completed_at is None
    assert summary.status == "completed"
    assert summary.finishing_text == ""
