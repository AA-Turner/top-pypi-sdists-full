"""Unit tests for feature_failure_disposition."""

from agentic_devtools.orchestration.hierarchy.retry import Disposition, feature_failure_disposition


def test_feature_failure_disposition_independent_vs_stopped() -> None:
    assert (
        feature_failure_disposition(epic_review_independent=True)
        == Disposition.FEATURE_FAILURE_INDEPENDENT_EPIC_CONTINUES
    )
    assert feature_failure_disposition(epic_review_independent=False) == Disposition.FEATURE_FAILURE_STOPPED
