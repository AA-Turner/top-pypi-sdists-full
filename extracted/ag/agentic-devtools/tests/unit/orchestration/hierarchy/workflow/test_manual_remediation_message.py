"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.workflow import (
    manual_remediation_message,
)


def test_manual_remediation_message() -> None:
    message = manual_remediation_message(scope="subtask", agent_id="subtask-1", cleanup_reason="disk full")
    assert "subtask-1" in message
    assert "disk full" in message
