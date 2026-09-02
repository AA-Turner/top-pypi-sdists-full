"""Tests for get_effective_head_reviews in snapshot module."""

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot import get_effective_head_reviews


class TestGetEffectiveHeadReviews:
    """Tests for get_effective_head_reviews."""

    def test_ignores_older_duplicate_review(self) -> None:
        """Lower review.id for same reviewer should not replace the latest review."""
        reviews = [
            ReviewInfo(id=20, user="alice", state="APPROVED", commit_sha="head-sha"),
            ReviewInfo(id=19, user="alice", state="CHANGES_REQUESTED", commit_sha="head-sha"),
        ]

        effective = get_effective_head_reviews(reviews, "head-sha")

        assert len(effective) == 1
        assert effective[0].id == 20
        assert effective[0].state == "APPROVED"

    def test_collapses_copilot_aliases_case_insensitively(self) -> None:
        """Copilot aliases should collapse to one effective reviewer regardless of case."""
        reviews = [
            ReviewInfo(id=12, user="Copilot", state="COMMENTED", commit_sha="head-sha"),
            ReviewInfo(id=13, user="COPILOT", state="APPROVED", commit_sha="head-sha"),
        ]

        effective = get_effective_head_reviews(reviews, "head-sha")

        assert len(effective) == 1
        assert effective[0].id == 13
        assert effective[0].state == "APPROVED"

    def test_collapses_non_copilot_case_insensitively(self) -> None:
        """Non-Copilot reviewer logins should also collapse case-insensitively."""
        reviews = [
            ReviewInfo(id=20, user="Alice", state="COMMENTED", commit_sha="head-sha"),
            ReviewInfo(id=21, user="alice", state="APPROVED", commit_sha="head-sha"),
        ]

        effective = get_effective_head_reviews(reviews, "head-sha")

        assert len(effective) == 1
        assert effective[0].id == 21
        assert effective[0].state == "APPROVED"
