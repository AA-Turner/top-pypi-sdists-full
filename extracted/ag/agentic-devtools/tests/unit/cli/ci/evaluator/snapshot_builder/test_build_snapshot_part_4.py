"""Tests for build_snapshot()."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.evaluator.snapshot_builder import build_snapshot
from agentic_devtools.cli.ci.models import IssueCommentInfo, PRMetadata, ReviewCommentInfo


class TestBuildSnapshot:
    """Tests for post-agent snapshot construction."""

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    @patch("agentic_devtools.cli.ci.evaluator.snapshot_comments._get_review_thread_statuses")
    def test_repair_satisfied_review_id_fallback_populates_threads(self, mock_thread_status, mock_lock_status):
        """When no active review is listed, marker review-id is used to load review threads."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
        )
        provider.list_reviews.return_value = []
        provider.get_pr_diff.return_value = ""
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot[bot]",
                body="<!-- ai-pr-loop:repair-satisfied -->\n<!-- review-id:777 -->\nNo changes needed.",
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="src/main.py", body="Fix this", html_url="https://example.test/comment/101")
        ]
        mock_thread_status.return_value = {101: (False, True)}
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.review_id == 777
        assert snapshot.has_repair_satisfied_marker is True
        assert snapshot.repair_satisfied_review_id == 777
        assert len(snapshot.threads) == 1
        assert snapshot.threads[0].comment_id == 101
        assert snapshot.threads[0].has_reply is True
        provider.list_review_comments.assert_called_once_with(42, 777)

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_repair_satisfied_marker_ignored_without_review_id(self, mock_lock_status):
        """Repair-satisfied marker without review-id does not set the flag."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
        )
        provider.list_reviews.return_value = []
        provider.get_pr_diff.return_value = ""
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot[bot]",
                body="<!-- ai-pr-loop:repair-satisfied -->\nNo changes needed.",
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_repair_satisfied_marker is False
        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_repair_satisfied_marker_ignored_from_non_copilot(self, mock_lock_status):
        """Repair-satisfied marker from a non-Copilot user is ignored."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
        )
        provider.list_reviews.return_value = []
        provider.get_pr_diff.return_value = ""
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="malicious-user",
                body=("<!-- ai-pr-loop:repair-satisfied -->\n<!-- review-id:999 -->\nFake marker."),
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_repair_satisfied_marker is False
        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_repair_satisfied_scan_failure_defaults_to_false(self, mock_lock_status):
        """Exception during repair-satisfied scan defaults to False."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
        )
        provider.list_reviews.return_value = []
        provider.get_pr_diff.return_value = ""
        provider.list_issue_comments.side_effect = RuntimeError("API error")
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_repair_satisfied_marker is False
        assert snapshot.repair_satisfied_review_id is None
