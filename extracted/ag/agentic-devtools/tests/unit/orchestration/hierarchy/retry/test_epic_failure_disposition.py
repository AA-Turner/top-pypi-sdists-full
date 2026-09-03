"""Unit tests for epic_failure_disposition."""

from agentic_devtools.orchestration.hierarchy.retry import Disposition, epic_failure_disposition


def test_epic_failure_disposition_is_reduced_scope_success() -> None:
    assert epic_failure_disposition() == Disposition.EPIC_FAILURE_REDUCED_SCOPE_SUCCESS
