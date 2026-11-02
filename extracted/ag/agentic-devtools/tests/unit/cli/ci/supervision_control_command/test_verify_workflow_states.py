"""Tests for the verify_workflow_states symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control_command import verify_workflow_states


def test_verify_workflow_states_raises_on_mismatch() -> None:
    with pytest.raises(RuntimeError, match="workflow state read-back mismatch"):
        verify_workflow_states({"loop.yml": False}, {"loop.yml": True})


def test_verify_workflow_states_raises_when_workflow_missing_from_observed() -> None:
    with pytest.raises(RuntimeError, match="workflow state read-back mismatch"):
        verify_workflow_states({"loop.yml": False}, {})


def test_verify_workflow_states_passes_on_exact_match() -> None:
    verify_workflow_states({"loop.yml": False}, {"loop.yml": False})
