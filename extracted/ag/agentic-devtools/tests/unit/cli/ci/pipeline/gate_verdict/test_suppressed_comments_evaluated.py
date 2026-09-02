"""Tests for suppressed_comments_evaluated in the gate_verdict module."""

from __future__ import annotations

from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
    suppressed_comments_evaluated,
)


def _suppressed_verdict(review_id: int = 42) -> CopilotGateVerdict:
    return CopilotGateVerdict(
        passed=False,
        reason=REASON_SUPPRESSED_COMMENTS,
        review_id=review_id,
        body_comment_count=0,
        suppressed_count=2,
    )


class TestSuppressedCommentsEvaluated:
    """Tests for suppressed_comments_evaluated."""

    def test_marker_matches_head_unchanged_no_threads_returns_true(self) -> None:
        assert (
            suppressed_comments_evaluated(
                _suppressed_verdict(42),
                repair_satisfied_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is True
        )

    def test_new_ccr_suppressed_only_marker_matches_returns_true(self) -> None:
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_NEW_CCR_NOT_APPROVED,
            review_id=7,
            body_comment_count=0,
            suppressed_count=1,
        )
        assert (
            suppressed_comments_evaluated(
                verdict,
                repair_satisfied_review_id=7,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is True
        )

    def test_none_verdict_returns_false(self) -> None:
        assert (
            suppressed_comments_evaluated(
                None,
                repair_satisfied_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_passed_verdict_returns_false(self) -> None:
        verdict = CopilotGateVerdict(passed=True, reason=REASON_CLEAN, review_id=42)
        assert (
            suppressed_comments_evaluated(
                verdict,
                repair_satisfied_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_non_suppressed_only_reason_returns_false(self) -> None:
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_HAS_COMMENTS,
            review_id=42,
            body_comment_count=3,
            suppressed_count=1,
        )
        assert (
            suppressed_comments_evaluated(
                verdict,
                repair_satisfied_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_head_changed_returns_false(self) -> None:
        assert (
            suppressed_comments_evaluated(
                _suppressed_verdict(42),
                repair_satisfied_review_id=42,
                head_changed_since_review=True,
                unresolved_threads=0,
            )
            is False
        )

    def test_unresolved_threads_present_returns_false(self) -> None:
        assert (
            suppressed_comments_evaluated(
                _suppressed_verdict(42),
                repair_satisfied_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=1,
            )
            is False
        )

    def test_review_id_not_positive_returns_false(self) -> None:
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=0,
            body_comment_count=0,
            suppressed_count=2,
        )
        assert (
            suppressed_comments_evaluated(
                verdict,
                repair_satisfied_review_id=0,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_marker_missing_returns_false(self) -> None:
        assert (
            suppressed_comments_evaluated(
                _suppressed_verdict(42),
                repair_satisfied_review_id=None,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_marker_review_id_mismatch_returns_false(self) -> None:
        assert (
            suppressed_comments_evaluated(
                _suppressed_verdict(42),
                repair_satisfied_review_id=99,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_marker_review_id_zero_with_valid_verdict_id_returns_false(self) -> None:
        """repair_satisfied_review_id=0 must not match a valid verdict review_id > 0."""
        assert (
            suppressed_comments_evaluated(
                _suppressed_verdict(42),
                repair_satisfied_review_id=0,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )
