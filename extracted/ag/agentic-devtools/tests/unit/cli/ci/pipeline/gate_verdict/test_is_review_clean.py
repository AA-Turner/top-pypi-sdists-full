"""Tests for is_review_clean in the gate_verdict module."""

from __future__ import annotations

from agentic_devtools.cli.ci.pipeline.gate_verdict import is_review_clean
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot


class TestIsReviewClean:
    """Tests for the legacy clean-review predicate."""

    def test_approved_review_is_clean(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, review_state="APPROVED")
        assert is_review_clean(snapshot) is True

    def test_commented_review_without_inline_comments_is_clean(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, review_state="COMMENTED", copilot_review_inline_count=0)
        assert is_review_clean(snapshot) is True

    def test_commented_review_with_inline_comments_is_not_clean(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, review_state="COMMENTED", copilot_review_inline_count=2)
        assert is_review_clean(snapshot) is False

    def test_changes_requested_review_is_not_clean(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, review_state="CHANGES_REQUESTED")
        assert is_review_clean(snapshot) is False

    def test_missing_review_is_not_clean(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1)
        assert is_review_clean(snapshot) is False
