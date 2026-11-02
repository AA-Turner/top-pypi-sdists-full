"""Tests for build_snapshot()."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.evaluator.snapshot_builder import build_snapshot
from agentic_devtools.cli.ci.models import IssueCommentInfo, PRMetadata, ReviewCommentInfo, ReviewInfo


class TestBuildSnapshot:
    """Tests for post-agent snapshot construction."""

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_comments._get_review_thread_statuses")
    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_populates_thread_fields_and_latest_agent_comment(self, mock_lock_status, mock_thread_status):
        """Snapshot includes line numbers, resolution/reply state, and latest agent comment."""
        provider = MagicMock()
        provider.find_comment.return_value = None
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
        )
        provider.list_reviews.return_value = [
            ReviewInfo(id=7, user="Copilot", state="COMMENTED", commit_sha="review-sha"),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(
                id=101,
                path="src/main.py",
                body="Fix this",
                html_url="https://example.test/comment/101",
                start_line=10,
                end_line=12,
            )
        ]
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="dev",
                body="human comment",
                created_at="2026-05-20T00:00:00Z",
            ),
            IssueCommentInfo(
                id=2,
                author="copilot[bot]",
                body="fixed",
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        provider.get_commit_range_diff.return_value = "diff --git a/src/main.py b/src/main.py"
        mock_thread_status.return_value = {101: (True, True)}
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.review_id == 7
        assert snapshot.review_commit_sha == "review-sha"
        assert snapshot.head_changed_since_review is True
        assert len(snapshot.threads) == 1
        assert snapshot.threads[0].start_line == 10
        assert snapshot.threads[0].end_line == 12
        assert snapshot.threads[0].is_resolved is True
        assert snapshot.threads[0].has_reply is True
        assert snapshot.latest_agent_comment is not None
        assert snapshot.latest_agent_comment.id == 2
        assert snapshot.latest_agent_comment.author == "copilot[bot]"
        assert snapshot.has_sentinel is False
        assert snapshot.diff_text.startswith("diff --git")
        provider.list_issue_comments.assert_called_once_with(42)

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_comments._get_review_thread_statuses")
    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_skips_suppressed_review_comments(self, mock_lock_status, mock_thread_status):
        provider = MagicMock()
        provider.find_comment.return_value = None
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
        )
        provider.list_reviews.return_value = [
            ReviewInfo(id=7, user="Copilot", state="COMMENTED", commit_sha="review-sha"),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=-1, path="src/suppressed.py", body="suppressed", html_url="", is_suppressed=True),
            ReviewCommentInfo(id=101, path="src/main.py", body="visible", html_url="https://example.test/comment/101"),
        ]
        provider.list_issue_comments.return_value = []
        provider.get_commit_range_diff.return_value = ""
        mock_thread_status.return_value = {101: (False, False)}
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert len(snapshot.threads) == 1
        assert snapshot.threads[0].comment_id == 101

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_comments._get_review_thread_statuses", return_value={})
    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_handles_missing_optional_sources(self, mock_lock_status, _mock_thread_status):
        """Snapshot gracefully handles providers without issue-comment and diff support."""
        provider = MagicMock()
        provider.find_comment.return_value = None
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
        )
        provider.list_reviews.return_value = []
        provider.get_pr_diff.side_effect = NotImplementedError("unsupported")
        del provider.list_issue_comments
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.review_id == 0
        assert snapshot.latest_agent_comment is None
        assert snapshot.diff_text == ""
        assert snapshot.threads == ()

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    @patch(
        "agentic_devtools.cli.ci.evaluator.snapshot_comments._get_review_thread_statuses",
        side_effect=RuntimeError("thread status failed"),
    )
    def test_logs_and_continues_when_optional_fetches_fail(
        self,
        _mock_thread_status,
        mock_lock_status,
    ):
        """Snapshot still builds when optional metadata fetches fail."""
        provider = MagicMock()
        provider.find_comment.return_value = None
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
        )
        provider.list_reviews.return_value = [
            ReviewInfo(id=7, user="Copilot", state="COMMENTED", commit_sha="review-sha"),
        ]
        provider.list_review_comments.side_effect = RuntimeError("review comments failed")
        provider.get_commit_range_diff.return_value = ""
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.review_id == 7
        assert snapshot.threads == ()
        assert snapshot.latest_agent_comment is None
