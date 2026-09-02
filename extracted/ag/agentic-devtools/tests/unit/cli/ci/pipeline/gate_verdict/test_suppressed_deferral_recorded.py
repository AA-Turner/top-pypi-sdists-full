"""Tests for suppressed_deferral_recorded in the gate_verdict module."""

from __future__ import annotations

from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_HAS_COMMENTS,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
    suppressed_deferral_recorded,
)


def _suppressed_verdict(review_id: int = 42) -> CopilotGateVerdict:
    return CopilotGateVerdict(
        passed=False,
        reason=REASON_SUPPRESSED_COMMENTS,
        review_id=review_id,
        body_comment_count=0,
        suppressed_count=2,
    )


class TestSuppressedDeferralRecorded:
    """Tests for suppressed_deferral_recorded."""

    def test_matching_deferral_returns_true(self) -> None:
        assert (
            suppressed_deferral_recorded(
                _suppressed_verdict(42),
                deferred_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is True
        )

    def test_no_deferral_returns_false(self) -> None:
        assert (
            suppressed_deferral_recorded(
                _suppressed_verdict(42),
                deferred_review_id=None,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_deferral_for_other_review_returns_false(self) -> None:
        assert (
            suppressed_deferral_recorded(
                _suppressed_verdict(42),
                deferred_review_id=41,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_none_verdict_returns_false(self) -> None:
        assert (
            suppressed_deferral_recorded(
                None,
                deferred_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_passed_verdict_returns_false(self) -> None:
        verdict = CopilotGateVerdict(passed=True, reason=REASON_CLEAN, review_id=42)
        assert (
            suppressed_deferral_recorded(
                verdict,
                deferred_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_non_suppressed_only_block_returns_false(self) -> None:
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_HAS_COMMENTS,
            review_id=42,
            body_comment_count=2,
            suppressed_count=1,
        )
        assert (
            suppressed_deferral_recorded(
                verdict,
                deferred_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )

    def test_head_changed_returns_false(self) -> None:
        assert (
            suppressed_deferral_recorded(
                _suppressed_verdict(42),
                deferred_review_id=42,
                head_changed_since_review=True,
                unresolved_threads=0,
            )
            is False
        )

    def test_unresolved_threads_returns_false(self) -> None:
        assert (
            suppressed_deferral_recorded(
                _suppressed_verdict(42),
                deferred_review_id=42,
                head_changed_since_review=False,
                unresolved_threads=1,
            )
            is False
        )

    def test_missing_review_id_returns_false(self) -> None:
        assert (
            suppressed_deferral_recorded(
                _suppressed_verdict(0),
                deferred_review_id=0,
                head_changed_since_review=False,
                unresolved_threads=0,
            )
            is False
        )
