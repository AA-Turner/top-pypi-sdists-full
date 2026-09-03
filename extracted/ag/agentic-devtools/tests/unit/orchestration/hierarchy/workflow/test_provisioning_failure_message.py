"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.workflow import (
    provisioning_failure_message,
)


def test_provisioning_failure_message() -> None:
    message = provisioning_failure_message(scope="subtask", capability="python_lint_typecheck")
    assert "python_lint_typecheck" in message
