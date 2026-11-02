"""Tests for build_pr_state_snapshot."""

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import SYNTHETIC_MARKER
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_unresolved_threads_fails_closed_when_review_comments_fetch_fails(self) -> None:
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
            ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha"),
        ]
        provider.list_review_comments.side_effect = RuntimeError("boom")
        provider.list_review_threads_by_thread_id.side_effect = RuntimeError("boom")
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_counts_across_all_prior_copilot_reviews(self) -> None:
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
            [
                ReviewCommentInfo(id=201, path="a.py", body="c", html_url=""),
                ReviewCommentInfo(id=202, path="a.py", body="d", html_url=""),
                ReviewCommentInfo(id=203, path="a.py", body="e", html_url=""),
            ],
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101, 102)),
            "thread-2": (False, (201, 202, 203)),
        }
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 2
        assert provider.list_review_comments.call_count == 2

    def test_unresolved_threads_counts_prior_trusted_synthetic_reviews(self) -> None:
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
                id=10,
                user="AMARSNIK_swica",
                state="COMMENTED",
                body=f"{SYNTHETIC_MARKER}\nsynthetic review",
                commit_sha="old-sha",
            ),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="a", html_url=""),
            ReviewCommentInfo(id=102, path="a.py", body="b", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 102))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        provider.list_review_comments.assert_called_once_with(1, 10)
