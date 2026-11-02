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

    def test_unresolved_threads_fails_closed_after_partial_aggregation(self) -> None:
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
            ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha-1"),
            ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-2"),
        ]
        provider.list_review_comments.side_effect = [
            [
                ReviewCommentInfo(id=101, path="a.py", body="a", html_url=""),
                ReviewCommentInfo(id=102, path="a.py", body="b", html_url=""),
            ],
            RuntimeError("boom"),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 102))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_excludes_resolved_threads(self) -> None:
        """Only unresolved threads should be counted."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix this", html_url=""),
            ReviewCommentInfo(id=102, path="a.py", body="also this", html_url=""),
            ReviewCommentInfo(id=103, path="a.py", body="and this", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101, 103)),
            "thread-2": (True, (102,)),
        }
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_counts_a_single_thread_with_multiple_comments_once(self) -> None:
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
            ReviewCommentInfo(id=101, path="a.py", body="fix this", html_url=""),
            ReviewCommentInfo(id=102, path="a.py", body="also this", html_url=""),
            ReviewCommentInfo(id=103, path="a.py", body="and this", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 102, 103))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_fails_closed_when_thread_state_lookup_is_not_implemented(self) -> None:
        """A NotImplemented thread-state lookup degrades to the blocking floor."""
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
        provider.list_review_threads_by_thread_id.side_effect = NotImplementedError()
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True
