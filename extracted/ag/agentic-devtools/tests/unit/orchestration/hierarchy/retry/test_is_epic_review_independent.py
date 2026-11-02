"""Unit tests for the FR-017 exactly-one-lifetime-retry policy."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.retry import (
    is_epic_review_independent,
)


def test_epic_review_independent_requires_complete_context_and_no_feature_dependency() -> None:
    assert is_epic_review_independent(
        epic_context_complete_before_feature_unavailable=True, epic_requires_feature_output=False
    )
    assert not is_epic_review_independent(
        epic_context_complete_before_feature_unavailable=False, epic_requires_feature_output=False
    )
    assert not is_epic_review_independent(
        epic_context_complete_before_feature_unavailable=True, epic_requires_feature_output=True
    )
