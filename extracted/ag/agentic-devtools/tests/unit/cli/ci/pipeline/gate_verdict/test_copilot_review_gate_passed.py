"""Tests for copilot_review_gate_passed in the gate_verdict module."""

from __future__ import annotations

from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_HAS_COMMENTS,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
    copilot_review_gate_passed,
)
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot


class TestCopilotReviewGatePassed:
    """Tests for the shared 'review has gone clean on HEAD' predicate."""

    def test_passing_verdict_passes(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_gate_verdict=CopilotGateVerdict(passed=True, reason=REASON_CLEAN),
        )
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is True

    def test_blocking_verdict_blocks(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_HAS_COMMENTS,
                review_id=7,
                body_comment_count=3,
            ),
        )
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False

    def test_suppressed_only_block_passes_when_repair_marker_matches(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            repair_satisfied_review_id=42,
            head_changed_since_review=False,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_SUPPRESSED_COMMENTS,
                review_id=42,
                body_comment_count=0,
                suppressed_count=2,
            ),
        )
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is True

    def test_suppressed_only_block_still_blocks_with_unresolved_threads(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            repair_satisfied_review_id=42,
            head_changed_since_review=False,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_SUPPRESSED_COMMENTS,
                review_id=42,
                body_comment_count=0,
                suppressed_count=2,
            ),
        )
        assert copilot_review_gate_passed(snapshot, unresolved_threads=1) is False

    def test_falls_back_to_clean_review_check_without_verdict(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, review_state="APPROVED")
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is True

    def test_falls_back_to_clean_review_check_without_verdict_and_blocks(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, review_state="CHANGES_REQUESTED")
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False

    def test_suppressed_only_block_passes_on_snapshot_deferral(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_changed_since_review=False,
            suppressed_deferral_review_id=42,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_SUPPRESSED_COMMENTS,
                review_id=42,
                body_comment_count=0,
                suppressed_count=2,
            ),
        )
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is True

    def test_suppressed_only_block_passes_on_same_run_deferral(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_changed_since_review=False,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_SUPPRESSED_COMMENTS,
                review_id=42,
                body_comment_count=0,
                suppressed_count=2,
            ),
        )
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0, deferred_review_id=42) is True

    def test_suppressed_only_block_still_blocks_without_any_evidence(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_changed_since_review=False,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_SUPPRESSED_COMMENTS,
                review_id=42,
                body_comment_count=0,
                suppressed_count=2,
            ),
        )
        assert copilot_review_gate_passed(snapshot, unresolved_threads=0) is False
