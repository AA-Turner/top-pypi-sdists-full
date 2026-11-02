"""Tests for build_pr_state_snapshot."""

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_has_approver_approval_on_head_true_when_approver_login_matches(self) -> None:
        """Precise approver-identity check: approver login resolves and matches reviewer."""
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
            ReviewInfo(id=13, user="loop-bot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = "loop-bot"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == "loop-bot"
        assert snapshot.has_approver_approval_on_head is True

    def test_has_approver_approval_on_head_true_case_insensitive(self) -> None:
        """Approver login comparison is case-insensitive."""
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
            ReviewInfo(id=13, user="Loop-Bot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = "loop-bot"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.has_approver_approval_on_head is True

    def test_has_approver_approval_on_head_false_when_login_empty(self) -> None:
        """When approver login cannot be resolved, flag stays False."""
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
            ReviewInfo(id=13, user="some-human", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = ""  # PAT not configured

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == ""
        assert snapshot.has_approver_approval_on_head is False

    def test_has_approver_approval_on_head_false_when_approver_has_not_approved(self) -> None:
        """Known approver login but no matching APPROVED review ⇒ flag stays False."""
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
            ReviewInfo(id=12, user="Copilot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = "loop-bot"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == "loop-bot"
        assert snapshot.has_approver_approval_on_head is False

    def test_has_approver_approval_on_head_false_when_review_has_empty_commit_sha(self) -> None:
        """Approver APPROVED review with empty commit_sha fails closed and is not treated as HEAD approval."""
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
            ReviewInfo(id=13, user="loop-bot", state="APPROVED", commit_sha=""),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = "loop-bot"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == "loop-bot"
        assert snapshot.has_approver_approval_on_head is False
