"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.workflow import (
    rejection_message,
)


def test_rejection_message_includes_violation_and_action() -> None:
    message = rejection_message(scope="feature", stage="review", violation_ref="FR-006", corrective_action="fix it")
    assert "FR-006" in message
    assert "fix it" in message
