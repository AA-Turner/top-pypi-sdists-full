"""Tests for build_pr_state_snapshot."""

import logging

import pytest

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_unresolved_threads_deduplicates_same_thread_across_reviews(self) -> None:
        """The same unresolved thread appearing in multiple prior reviews is only counted once."""
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
            ReviewInfo(id=11, user="Copilot", state="COMMENTED", commit_sha="old-sha-2"),
        ]
        provider.list_review_comments.side_effect = [
            [ReviewCommentInfo(id=101, path="a.py", body="fix this", html_url="")],
            [ReviewCommentInfo(id=101, path="a.py", body="fix this", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_fails_closed_when_thread_statuses_omit_comments(self) -> None:
        """Incomplete thread-state data degrades without inflating by comment count."""
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
            ReviewCommentInfo(id=101, path="a.py", body="unresolved", html_url=""),
            ReviewCommentInfo(id=102, path="a.py", body="not in thread data", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_logs_when_thread_statuses_omit_a_comment(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A comment absent from thread-state data emits a diagnostic warning."""
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
            ReviewCommentInfo(id=102, path="a.py", body="not in thread data", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.pipeline.snapshot_thread_count"):
            snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads_degraded is True
        assert "review-thread state omitted comment 102" in caplog.text

    def test_unresolved_threads_degrades_and_logs_when_comments_fetch_fails(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A review whose comments cannot be listed degrades the count and logs it."""
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
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
        provider.list_review_threads_by_thread_id.return_value = {}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.pipeline.snapshot_thread_count"):
            snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True
        assert "failed to list review comments for review 10" in caplog.text

    def test_unresolved_threads_combined_fail_and_omitted_entry_is_not_inflated(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Two-review mixed case: one fetch fails and another has an omitted thread-state entry.

        The failed fetch contributes no fabricated thread, so the total is the single
        candidate thread whose state was omitted — blocking (non-zero) and degraded,
        but never inflated beyond what was actually observed.
        """
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
            ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha"),
        ]
        provider.list_review_comments.side_effect = [
            RuntimeError("network error"),
            [ReviewCommentInfo(id=200, path="a.py", body="needs work", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.pipeline.snapshot_thread_count"):
            snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True
