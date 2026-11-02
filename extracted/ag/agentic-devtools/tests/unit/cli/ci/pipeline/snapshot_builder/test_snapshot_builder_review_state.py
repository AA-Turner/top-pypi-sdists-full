"""Tests for build_pr_state_snapshot."""

from typing import cast

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_has_approval_on_head_uses_effective_latest_review_per_reviewer(self) -> None:
        """A superseded approval should not count as current approval on HEAD.

        Copilot's approval sets the generic ``has_approval_on_head`` flag; the only
        non-Copilot reviewer (alice) has a superseding CHANGES_REQUESTED so their
        earlier approval is not effective on HEAD.
        """
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(id=10, user="alice", state="APPROVED", commit_sha="head-sha"),
            ReviewInfo(id=11, user="alice", state="CHANGES_REQUESTED", commit_sha="head-sha"),
            ReviewInfo(id=12, user="Copilot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.has_approval_on_head is True
        assert snapshot.review_state == "APPROVED"
        assert snapshot.copilot_review_id == 12

    def test_copilot_review_fields_populated_for_synthetic_review_on_head(self) -> None:
        """Trusted synthetic Copilot reviews on HEAD populate the review id/state fields."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(
                id=12,
                user="AMARSNIK_swica",
                state="COMMENTED",
                commit_sha="head-sha",
                body="<!-- synthetic-copilot-review -->",
            ),
        ]
        provider.list_review_comments.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.review_state == "COMMENTED"
        assert snapshot.copilot_review_id == 12
        assert snapshot.copilot_review_inline_count == 0

    def test_copilot_review_selection_tolerates_missing_submitted_at(self) -> None:
        """Missing synthetic-review timestamps must not break latest-review selection."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(
                id=12,
                user="AMARSNIK_swica",
                state="COMMENTED",
                commit_sha="head-sha",
                body="<!-- synthetic-copilot-review -->",
                submitted_at=cast(str, None),
            ),
            ReviewInfo(
                id=13,
                user="Copilot",
                state="APPROVED",
                commit_sha="head-sha",
                submitted_at="2026-08-07T07:00:00Z",
            ),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.review_state == "APPROVED"
        assert snapshot.copilot_review_id == 13

    def test_has_approval_on_head_false_when_latest_effective_review_is_changes_requested(self) -> None:
        """If latest effective HEAD review is CHANGES_REQUESTED, approval should be false."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(id=10, user="alice", state="APPROVED", commit_sha="head-sha"),
            ReviewInfo(id=11, user="alice", state="CHANGES_REQUESTED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.has_approval_on_head is False
