"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.workflow import (
    reduced_scope_message,
)


def test_reduced_scope_message_with_missing_level() -> None:
    message = reduced_scope_message(scope="orchestrator", stage="composition", missing_level="epic")
    assert "epic unavailable" in message


def test_reduced_scope_message_without_missing_level() -> None:
    message = reduced_scope_message(scope="orchestrator", stage="composition", missing_level=None)
    assert "reduced scope" in message
