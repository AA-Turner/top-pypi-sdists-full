"""Tests for build_pr_state_snapshot."""

from unittest.mock import patch

from agentic_devtools.cli.ci.guards import REPAIR_SATISFIED_MARKER
from agentic_devtools.cli.ci.models import (
    IssueCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _suppressed_marker_provider


class TestBuildPrStateSnapshotSuppressedMarker:
    """Tests for build_pr_state_snapshot behavior."""

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_head_changed_true_when_latest_review_on_other_commit(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=42)
        provider = _suppressed_marker_provider(review_commit_sha="old-sha", head_sha="head-sha")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True
        # Passed verdict → marker branch skipped.
        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_head_changed_false_when_latest_review_on_head(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=42)
        provider = _suppressed_marker_provider(review_commit_sha="head-sha", head_sha="head-sha")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_head_changed_false_when_effective_synthetic_review_matches_head(self, mock_gate) -> None:
        """Trusted synthetic effective review on HEAD should not fail closed."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=41, synthetic=True)
        provider = _suppressed_marker_provider(head_sha="head-sha")
        provider.list_reviews.return_value = [
            ReviewInfo(
                id=41,
                user="AMARSNIK_swica",
                state="COMMENTED",
                body="<!-- synthetic-copilot-review -->",
                commit_sha="head-sha",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_head_changed_uses_effective_gate_review_instead_of_latest_review(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=41,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider(head_sha="head-sha")
        provider.list_reviews.return_value = [
            ReviewInfo(id=41, user="Copilot", state="COMMENTED", commit_sha="head-sha"),
            ReviewInfo(id=42, user="Copilot", state="COMMENTED", commit_sha="older-sha"),
        ]
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot-swe-agent[bot]",
                body=f"{REPAIR_SATISFIED_MARKER}\n<!-- review-id:41 -->",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False
        assert snapshot.repair_satisfied_review_id == 41
        provider.list_issue_comments.assert_called_once_with(1)

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_head_changed_fails_closed_when_effective_review_commit_sha_missing(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider(review_commit_sha="")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True
        assert snapshot.repair_satisfied_review_id is None
        provider.list_issue_comments.assert_not_called()

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_head_changed_fails_closed_when_no_copilot_reviews_in_fallback(self, mock_gate) -> None:
        """Fallback branch returns True (fail-closed) when no Copilot reviews exist."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=0)
        provider = _suppressed_marker_provider()
        provider.list_reviews.return_value = []

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_head_changed_fails_closed_when_fallback_review_has_no_commit_sha(self, mock_gate) -> None:
        """Fallback branch returns True (fail-closed) when the latest Copilot review has no commit SHA."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=0)
        provider = _suppressed_marker_provider()
        provider.list_reviews.return_value = [
            ReviewInfo(id=42, user="Copilot", state="COMMENTED", commit_sha=""),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_head_changed_false_when_fallback_review_matches_head(self, mock_gate) -> None:
        """Fallback branch returns False when the latest Copilot review matches HEAD."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=0)
        provider = _suppressed_marker_provider(review_commit_sha="head-sha", head_sha="head-sha")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_head_changed_true_when_fallback_review_on_other_commit(self, mock_gate) -> None:
        """Fallback branch returns True when the latest Copilot review targets a non-HEAD commit."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=0)
        provider = _suppressed_marker_provider(review_commit_sha="old-sha", head_sha="head-sha")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True
