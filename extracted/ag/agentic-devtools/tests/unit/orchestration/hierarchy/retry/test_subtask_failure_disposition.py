"""Unit tests for subtask_failure_disposition."""

from agentic_devtools.orchestration.hierarchy.retry import Disposition, subtask_failure_disposition


def test_subtask_failure_disposition_isolable_vs_non_isolable() -> None:
    assert subtask_failure_disposition(isolable=True) == Disposition.ISOLABLE_SUBTASK_FAILURE_PARTIAL
    assert subtask_failure_disposition(isolable=False) == Disposition.NON_ISOLABLE_SUBTASK_FAILURE_STOPPED
