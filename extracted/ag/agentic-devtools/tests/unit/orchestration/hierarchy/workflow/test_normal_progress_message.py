"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.workflow import (
    normal_progress_message,
)


def test_normal_progress_message() -> None:
    message = normal_progress_message(scope="subtask", stage="implementation")
    assert "subtask" in message
    assert "in progress" in message
