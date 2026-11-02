"""Tests for copilot_review_gate_passed in the gate_verdict module."""

from __future__ import annotations

from agentic_devtools.cli.ci.models import COPILOT_REVIEWER_LOGIN, ReviewInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
    copilot_review_gate_passed,
)
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


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

    @staticmethod
    def _critique_snapshot(
        headline: str,
        *,
        adjudicated_headline: str = "",
        adjudicated_head: str = "",
        adjudicated_verdict: str = "",
        head_changed: bool = False,
        classification: str = "critique",
    ) -> PRStateSnapshot:
        head_sha = "a" * 40
        review = ReviewInfo(
            id=100,
            user=COPILOT_REVIEWER_LOGIN,
            state="COMMENTED",
            body=(f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings"),
            commit_sha=head_sha,
        )
        return PRStateSnapshot(
            pr_number=1,
            head_sha=head_sha,
            reviews=[review],
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            effective_review_comment_filter_applied=False,
            head_changed_since_review=head_changed,
            critique_adjudicated_review_id=99 if adjudicated_headline else None,
            critique_adjudicated_head_sha=adjudicated_head,
            critique_adjudicated_headline=adjudicated_headline,
            critique_adjudicated_verdict=adjudicated_verdict,
            critique_headline_classification=classification,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_NEW_CCR_NOT_APPROVED,
                review_id=100,
                body_comment_count=0,
            ),
        )

    def test_approval_only_zero_finding_overview_clears_headline_block(self) -> None:
        snapshot = self._critique_snapshot(
            "This PR is ready for human approval.",
            classification="approval_worthy",
        )

        assert copilot_review_gate_passed(snapshot, unresolved_threads=0)

    def test_human_review_only_sentence_clears_headline_block_with_critique_heading(self) -> None:
        snapshot = self._critique_snapshot(
            "Broad modernization and limited baseline verification require final human review.",
            classification="approval_worthy",
        )

        assert copilot_review_gate_passed(snapshot, unresolved_threads=0)

    def test_critique_headline_remains_blocked_without_rebuttal(self) -> None:
        snapshot = self._critique_snapshot("The parser still loses findings.")

        assert not copilot_review_gate_passed(snapshot, unresolved_threads=0)

    def test_matching_rebuttal_clears_only_the_same_head_and_headline(self) -> None:
        headline = "The parser still loses findings."
        snapshot = self._critique_snapshot(
            headline,
            adjudicated_headline=headline,
            adjudicated_head="a" * 40,
            adjudicated_verdict="rebutted",
        )

        assert copilot_review_gate_passed(snapshot, unresolved_threads=0)
        assert not copilot_review_gate_passed(snapshot, unresolved_threads=1)

    def test_rebuttal_does_not_clear_a_changed_head_or_different_headline(self) -> None:
        headline = "The parser still loses findings."
        changed_head = self._critique_snapshot(
            headline,
            adjudicated_headline=headline,
            adjudicated_head="b" * 40,
            adjudicated_verdict="rebutted",
        )
        changed_review = self._critique_snapshot(
            "A different concern remains.",
            adjudicated_headline=headline,
            adjudicated_head="a" * 40,
            adjudicated_verdict="rebutted",
        )

        assert not copilot_review_gate_passed(changed_head, unresolved_threads=0)
        assert not copilot_review_gate_passed(changed_review, unresolved_threads=0)
