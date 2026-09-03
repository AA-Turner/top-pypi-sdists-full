"""Unit tests for Disposition values."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.retry import Disposition


def test_disposition_values_are_stable() -> None:
    assert Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED.value == "non_isolable_subtask_failure_stopped"
