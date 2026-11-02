"""Tests for suppressed_deferral_snapshot_eligible in the gate_verdict module."""

from __future__ import annotations

from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_SUPPRESSED_COMMENTS,
    SUPPRESSED_FOLLOW_UP_LABEL,
    CopilotGateVerdict,
    suppressed_deferral_snapshot_eligible,
)


def _verdict(suppressed_count: int = 1, review_id: int = 42) -> CopilotGateVerdict:
    return CopilotGateVerdict(
        passed=False,
        reason=REASON_SUPPRESSED_COMMENTS,
        review_id=review_id,
        body_comment_count=0,
        suppressed_count=suppressed_count,
    )


class TestSuppressedDeferralSnapshotEligible:
    """Tests for the snapshot-only subset of the deferral conditions."""

    def test_snapshot_conditions_hold_returns_true(self) -> None:
        assert (
            suppressed_deferral_snapshot_eligible(
                _verdict(),
                head_changed_since_review=False,
                unresolved_threads=0,
                suppressed_paths=["specs/3672/spec.md"],
                changed_files=["specs/3672/spec.md"],
                pr_labels=[],
            )
            is True
        )

    def test_does_not_consider_provider_backed_conditions(self) -> None:
        """A PR whose linked issue carries the follow-up label still passes here.

        Condition 9's linked-issue half needs an API call, so it is deliberately
        deferred to ``suppressed_deferral_eligible``.
        """
        assert (
            suppressed_deferral_snapshot_eligible(
                _verdict(),
                head_changed_since_review=False,
                unresolved_threads=0,
                suppressed_paths=["specs/3672/spec.md"],
                changed_files=["specs/3672/spec.md"],
                pr_labels=["enhancement"],
            )
            is True
        )

    def test_pr_follow_up_label_returns_false(self) -> None:
        assert (
            suppressed_deferral_snapshot_eligible(
                _verdict(),
                head_changed_since_review=False,
                unresolved_threads=0,
                suppressed_paths=["specs/3672/spec.md"],
                changed_files=["specs/3672/spec.md"],
                pr_labels=[SUPPRESSED_FOLLOW_UP_LABEL],
            )
            is False
        )

    def test_none_verdict_returns_false(self) -> None:
        assert (
            suppressed_deferral_snapshot_eligible(
                None,
                head_changed_since_review=False,
                unresolved_threads=0,
                suppressed_paths=["specs/3672/spec.md"],
                changed_files=["specs/3672/spec.md"],
                pr_labels=[],
            )
            is False
        )
