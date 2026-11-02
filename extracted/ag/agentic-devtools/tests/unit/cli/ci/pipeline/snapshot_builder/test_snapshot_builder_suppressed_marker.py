"""Tests for build_pr_state_snapshot."""

from unittest.mock import patch

from agentic_devtools.cli.ci.guards import REPAIR_SATISFIED_MARKER
from agentic_devtools.cli.ci.models import (
    IssueCommentInfo,
)
from agentic_devtools.cli.ci.pipeline.deferral import SUPPRESSED_DEFERRAL_SENTINEL
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_HAS_COMMENTS,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _suppressed_marker_provider


class TestBuildPrStateSnapshotSuppressedMarker:
    """Tests for build_pr_state_snapshot behavior."""

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_populated_for_suppressed_only_block(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot-swe-agent[bot]",
                body=f"{REPAIR_SATISFIED_MARKER}\n<!-- review-id:42 -->",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False
        assert snapshot.repair_satisfied_review_id == 42
        provider.list_issue_comments.assert_called_once_with(1)

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_none_when_no_marker(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.list_issue_comments.return_value = []

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_none_when_issue_comments_raise(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.list_issue_comments.side_effect = RuntimeError("boom")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_none_when_provider_lacks_method(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.list_issue_comments = None  # not callable → branch skipped

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_none_when_not_suppressed_only(self, mock_gate) -> None:
        """A non-suppressed-only block does not fetch issue comments."""
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_HAS_COMMENTS,
            review_id=42,
            body_comment_count=3,
            suppressed_count=0,
        )
        provider = _suppressed_marker_provider()

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.repair_satisfied_review_id is None
        provider.list_issue_comments.assert_not_called()

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_suppressed_deferral_review_id_populated_from_marker(self, mock_gate) -> None:
        """suppressed_deferral_review_id is populated when a deferral marker exists."""
        import json

        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        payload = json.dumps({"review_id": "42", "issue": 99, "active": True})
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot",
                body=f"{SUPPRESSED_DEFERRAL_SENTINEL}{payload} -->",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.suppressed_deferral_review_id == 42
        assert snapshot.suppressed_deferral_issue_number == 99

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_pr_token_login_exception_is_silenced(self, mock_gate) -> None:
        """get_pr_token_login raising falls back to static allowed set (fail-open)."""
        import json

        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.get_pr_token_login.side_effect = RuntimeError("token not set")
        payload = json.dumps({"review_id": "42", "issue": 99, "active": True})
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot",
                body=f"{SUPPRESSED_DEFERRAL_SENTINEL}{payload} -->",
            ),
        ]

        # Exception from get_pr_token_login must not propagate; marker still found
        # via the static allowed set (author "copilot" is always trusted).
        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.suppressed_deferral_review_id == 42

    @patch("agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict")
    def test_pr_token_login_not_callable_is_skipped(self, mock_gate) -> None:
        """When get_pr_token_login is not callable, skip token resolution gracefully."""
        import json

        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.get_pr_token_login = None  # not callable → branch skipped
        payload = json.dumps({"review_id": "42", "issue": 99, "active": True})
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot",
                body=f"{SUPPRESSED_DEFERRAL_SENTINEL}{payload} -->",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.suppressed_deferral_review_id == 42
