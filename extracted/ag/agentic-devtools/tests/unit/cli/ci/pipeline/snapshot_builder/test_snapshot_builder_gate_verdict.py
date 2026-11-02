"""Tests for build_pr_state_snapshot."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_API_ERROR,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from agentic_devtools.cli.ci.pipeline.snapshot_reviews import has_non_copilot_changes_requested_on_head
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_inline_count_unknown_when_head_commented_review_comments_fetch_fails(self) -> None:
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
            ReviewInfo(id=12, user="Copilot", state="COMMENTED", commit_sha="head-sha"),
        ]
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.review_state == "COMMENTED"
        assert snapshot.copilot_review_id == 12
        assert snapshot.copilot_review_inline_count == -1

    def test_head_commented_review_inline_count_is_comment_count(self) -> None:
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
            ReviewInfo(id=12, user="Copilot", state="COMMENTED", commit_sha="head-sha"),
        ]
        provider.list_review_comments.return_value = [MagicMock(), MagicMock(), MagicMock()]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.copilot_review_inline_count == 3

    def test_has_non_copilot_changes_requested_on_head_false_when_none(self) -> None:
        assert has_non_copilot_changes_requested_on_head([], "head-sha") is False

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_gate_verdict_exception_results_in_failed_closed_verdict(self, mock_gate) -> None:
        """When evaluate_copilot_gate_verdict raises, gate verdict is failed-closed."""
        mock_gate.side_effect = RuntimeError("unexpected gate error")
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
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.copilot_gate_verdict is not None
        assert snapshot.copilot_gate_verdict.passed is False
        assert snapshot.copilot_gate_verdict.reason == REASON_API_ERROR
