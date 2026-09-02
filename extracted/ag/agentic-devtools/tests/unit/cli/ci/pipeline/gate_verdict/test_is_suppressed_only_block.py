"""Tests for is_suppressed_only_block in the gate_verdict module."""

from __future__ import annotations

from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_CONTENT_CHANGED,
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
    is_suppressed_only_block,
)


class TestIsSuppressedOnlyBlock:
    """Tests for is_suppressed_only_block."""

    def test_legacy_suppressed_reason_is_suppressed_only(self) -> None:
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=1,
            body_comment_count=0,
            suppressed_count=2,
        )
        assert is_suppressed_only_block(verdict) is True

    def test_new_ccr_not_approved_zero_body_comments_is_suppressed_only(self) -> None:
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_NEW_CCR_NOT_APPROVED,
            review_id=1,
            body_comment_count=0,
            suppressed_count=3,
        )
        assert is_suppressed_only_block(verdict) is True

    def test_new_ccr_not_approved_with_posted_comments_not_suppressed_only(self) -> None:
        """A 'Not ready to approve' with real posted comments is not suppressed-only."""
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_NEW_CCR_NOT_APPROVED,
            review_id=1,
            body_comment_count=2,
            suppressed_count=1,
        )
        assert is_suppressed_only_block(verdict) is False

    def test_new_ccr_not_approved_unparseable_body_count_not_suppressed_only(self) -> None:
        """A None body_comment_count is treated conservatively (fail-closed)."""
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_NEW_CCR_NOT_APPROVED,
            review_id=1,
            body_comment_count=None,
            suppressed_count=1,
        )
        assert is_suppressed_only_block(verdict) is False

    def test_zero_suppressed_count_not_suppressed_only(self) -> None:
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=1,
            body_comment_count=0,
            suppressed_count=0,
        )
        assert is_suppressed_only_block(verdict) is False

    def test_has_comments_reason_not_suppressed_only(self) -> None:
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_HAS_COMMENTS,
            review_id=1,
            body_comment_count=2,
            suppressed_count=1,
        )
        assert is_suppressed_only_block(verdict) is False

    def test_content_changed_reason_not_suppressed_only(self) -> None:
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_CONTENT_CHANGED,
            review_id=1,
            suppressed_count=1,
        )
        assert is_suppressed_only_block(verdict) is False

    def test_clean_passed_verdict_not_suppressed_only(self) -> None:
        verdict = CopilotGateVerdict(passed=True, reason=REASON_CLEAN, review_id=1)
        assert is_suppressed_only_block(verdict) is False

    def test_api_error_reason_not_suppressed_only(self) -> None:
        """REASON_API_ERROR with suppressed_count > 0 and body_comment_count=0 → False."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_API_ERROR

        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_API_ERROR,
            review_id=1,
            body_comment_count=0,
            suppressed_count=2,
        )
        assert is_suppressed_only_block(verdict) is False

    def test_synthetic_parse_failed_reason_not_suppressed_only(self) -> None:
        """REASON_SYNTHETIC_PARSE_FAILED with suppressed_count > 0 and body_comment_count=0 → False."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_SYNTHETIC_PARSE_FAILED

        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_SYNTHETIC_PARSE_FAILED,
            review_id=1,
            body_comment_count=0,
            suppressed_count=2,
        )
        assert is_suppressed_only_block(verdict) is False
