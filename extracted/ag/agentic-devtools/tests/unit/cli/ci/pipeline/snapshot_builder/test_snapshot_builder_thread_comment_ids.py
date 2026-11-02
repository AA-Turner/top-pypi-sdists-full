"""Tests for build_pr_state_snapshot."""

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_unresolved_threads_fails_closed_when_same_comment_maps_to_two_threads(self) -> None:
        """A comment ID that appears in two different threads is a conflicting mapping; fail closed."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha"),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        # comment 101 appears in both thread-1 and thread-2 — conflicting mapping
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
            "thread-2": (True, (101,)),
        }
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_skips_negative_comment_ids(self) -> None:
        """Synthetic review-body entries are ignored when counting unresolved threads."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha"),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=-1, path="a.py", body="synthetic", html_url=""),
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is False

    def test_unresolved_threads_skips_repeated_comment_after_missing_thread_state(self) -> None:
        """A comment already counted as missing-thread-state is not double-counted on later reviews."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-1"),
            ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-2"),
        ]
        provider.list_review_comments.side_effect = [
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (102,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True
