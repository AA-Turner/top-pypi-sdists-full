"""Tests for build_snapshot()."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.evaluator.snapshot_builder import build_snapshot
from agentic_devtools.cli.ci.models import IssueCommentInfo, PRMetadata


class TestBuildSnapshot:
    """Tests for post-agent snapshot construction."""

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_omits_current_evaluator_lock_holder(self, mock_lock_status):
        """Snapshot does not treat the current evaluator's lock as contention."""
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
        provider.get_pr_diff.return_value = ""
        mock_lock_status.return_value = MagicMock(
            is_locked=True,
            is_stale=False,
            holder="token-123",
            age_seconds=12.0,
        )

        snapshot = build_snapshot(provider, 42, "owner/repo", current_lock_token="token-123")

        assert snapshot.lock_holder == ""
        assert snapshot.lock_age_seconds == 12.0

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_detects_latest_copilot_sentinel_for_current_head(self, mock_lock_status):
        """Latest Copilot sentinel counts only when it matches the current HEAD SHA."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="abc12345def67890",
            base_branch="main",
        )
        provider.list_reviews.return_value = []
        provider.get_pr_diff.return_value = ""
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot[bot]",
                body="<!-- copilot-agent-result -->\nHEAD: `abc12345`. Done.",
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_sentinel is True

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_ignores_latest_copilot_sentinel_for_stale_head(self, mock_lock_status):
        """Latest Copilot sentinel from an older HEAD must not complete the current cycle."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="newheadsha123456",
            base_branch="main",
        )
        provider.list_reviews.return_value = []
        provider.get_pr_diff.return_value = ""
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot[bot]",
                body="<!-- copilot-agent-result -->\nHEAD: `deadbeef`. Done.",
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_sentinel is False

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_sanitized_truncated_sentinel_does_not_count_as_completion(self, mock_lock_status):
        """Sentinel detection uses the original body so sanitization cannot synthesize completion."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="abc12345def67890",
            base_branch="main",
        )
        provider.list_reviews.return_value = []
        provider.get_pr_diff.return_value = ""
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot[bot]",
                body="> <!-- copilot-agent-result\nHEAD: `abc12345`. Done.",
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_sentinel is False
        assert snapshot.latest_agent_comment is not None
        assert snapshot.latest_agent_comment.body == "> <!-- copilot-agent-result -->\nHEAD: `abc12345`. Done."

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_persist_sanitized_comment_does_not_create_completion_across_runs(self, mock_lock_status):
        """Persistence neutralizes a synthetic completion marker so later runs stay incomplete."""
        provider = MagicMock()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=42,
            title="PR",
            head_branch="feature",
            head_sha="abc12345def67890",
            base_branch="main",
        )
        provider.list_reviews.return_value = []
        provider.get_pr_diff.return_value = ""
        comments = [
            IssueCommentInfo(
                id=1,
                author="copilot[bot]",
                body="<!-- copilot-agent-result\nHEAD: `abc12345`. Done.",
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        provider.list_issue_comments.side_effect = lambda _pr_number: list(comments)
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        first = build_snapshot(provider, 42, "owner/repo", persist_sanitized_comment=True)
        second = build_snapshot(provider, 42, "owner/repo", persist_sanitized_comment=True)

        assert first.has_sentinel is False
        assert second.has_sentinel is False
        assert first.latest_agent_comment is not None
        assert first.latest_agent_comment.body == "&lt;!-- copilot-agent-result -->\nHEAD: `abc12345`. Done."
        provider.update_comment.assert_called()
