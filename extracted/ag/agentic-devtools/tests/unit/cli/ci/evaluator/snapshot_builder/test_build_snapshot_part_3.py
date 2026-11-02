"""Tests for build_snapshot()."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.evaluator.snapshot_builder import build_snapshot
from agentic_devtools.cli.ci.models import IssueCommentInfo, PRMetadata


class TestBuildSnapshot:
    """Tests for post-agent snapshot construction."""

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_ignores_stale_sentinel_when_latest_copilot_comment_has_no_marker(self, mock_lock_status):
        """Older sentinel comments must not mark the current cycle as complete."""
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
                body="<!-- copilot-agent-result --> old run",
                created_at="2026-05-20T00:00:00Z",
            ),
            IssueCommentInfo(
                id=2,
                author="copilot[bot]",
                body="cycle:7",
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_sentinel is False

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_detects_evaluator_synthesized_sentinel_for_current_head(self, mock_lock_status):
        """Sentinel posted by evaluator workflow token (not Copilot) is detected when scoped to current HEAD."""
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
        # Sentinel posted by workflow token (github-actions[bot]), not a Copilot login
        sentinel_body = (
            "<!-- copilot-agent-result -->\n"
            "**Post-Agent Evaluator**: Synthesized result summary. HEAD: `abc12345`. Threads remaining: 0."
        )
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="github-actions[bot]",
                body=sentinel_body,
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_sentinel is True

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_ignores_evaluator_sentinel_for_different_head(self, mock_lock_status):
        """Evaluator sentinel for a stale HEAD does not count as a current-cycle sentinel."""
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
        # Sentinel was posted for an older HEAD SHA
        stale_sentinel_body = (
            "<!-- copilot-agent-result -->\n"
            "**Post-Agent Evaluator**: Synthesized result summary. HEAD: `deadbeef`. Threads remaining: 0."
        )
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="github-actions[bot]",
                body=stale_sentinel_body,
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_sentinel is False

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_detects_repair_satisfied_marker_from_copilot(self, mock_lock_status):
        """Repair-satisfied marker in a Copilot comment sets has_repair_satisfied_marker."""
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
                body=("<!-- ai-pr-loop:repair-satisfied -->\n<!-- review-id:777 -->\nNo changes needed."),
                created_at="2026-05-21T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_repair_satisfied_marker is True
        assert snapshot.repair_satisfied_review_id == 777

    @patch("agentic_devtools.cli.ci.evaluator.snapshot_builder.check_lock_status")
    def test_uses_latest_repair_satisfied_marker_when_multiple_exist(self, mock_lock_status):
        """Most recent valid repair-satisfied marker wins when multiple comments exist."""
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
                body="<!-- ai-pr-loop:repair-satisfied -->\n<!-- review-id:111 -->",
                created_at="2026-05-21T00:00:00Z",
            ),
            IssueCommentInfo(
                id=2,
                author="copilot[bot]",
                body="<!-- ai-pr-loop:repair-satisfied -->\n<!-- review-id:222 -->",
                created_at="2026-05-22T00:00:00Z",
            ),
        ]
        mock_lock_status.return_value = MagicMock(is_locked=False, is_stale=False, holder="", age_seconds=0.0)

        snapshot = build_snapshot(provider, 42, "owner/repo")

        assert snapshot.has_repair_satisfied_marker is True
        assert snapshot.repair_satisfied_review_id == 222
