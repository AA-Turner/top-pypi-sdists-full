"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.workflow import (
    blocked_message,
)


def test_blocked_message() -> None:
    message = blocked_message(scope="subtask", stage="write", attempted_path="secret.py")
    assert "secret.py" in message
