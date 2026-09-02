"""Tests for ApproveAction."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.approve import ApproveAction
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_AWAITING_FRESH,
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _clean_verdict(review_id: int = 1) -> CopilotGateVerdict:
    """Build a passing gate verdict for use in tests."""
    return CopilotGateVerdict(passed=True, reason="clean", review_id=review_id)


def _failing_verdict(reason: str = REASON_HAS_COMMENTS, details: str = "test block") -> CopilotGateVerdict:
    """Build a failing gate verdict for use in tests."""
    return CopilotGateVerdict(passed=False, reason=reason, details=details)


class TestApproveAction:
    """Tests for approve action evaluation."""

    def test_execute_when_non_copilot_already_approved(self) -> None:
        """A non-Copilot approval that is NOT the approver PAT does not short-circuit.

        ``has_approver_approval_on_head`` is False when the approver login is unknown
        (``approver_login=""``) even when another reviewer has approved on HEAD.
        The loop must still submit its own approval.
        """
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=True,
            has_approver_approval_on_head=False,  # approver identity not resolved
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_skip_when_approver_already_approved(self) -> None:
        """When the exact approver-PAT identity has already approved HEAD, skip (idempotent)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=True,
            approver_login="loop-bot",
            has_approver_approval_on_head=True,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "already approved" in result.details.lower()
        assert result.preconditions.get("no_approver_approval_on_head") is False

    def test_execute_when_only_copilot_approved(self) -> None:
        """A Copilot-only approval must NOT short-circuit the loop's own approval."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=True,  # Copilot approved → generic flag set
            has_approver_approval_on_head=False,  # approver PAT has not approved
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_skip_when_ci_not_passing(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, has_approval_on_head=False, ci_status="failing")
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "failing" in result.details.lower()

    def test_skip_when_repair_dispatched(self) -> None:
        """Approval is skipped after conflict repair is dispatched in the same run."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
        )
        derived = DerivedState(snapshot)
        derived.set("repair_dispatched", True)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_repair_dispatched"] is False
        assert "repair dispatched" in result.details.lower()

    def test_skip_when_ci_pending_even_with_squash_preserved_green(self) -> None:
        """ApproveAction must NEVER consume squash_preserved_green — it gates on the real HEAD CI."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=True,
            has_approver_approval_on_head=False,
            ci_status="pending",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
        )
        derived = DerivedState(snapshot)
        derived.set("squash_preserved_green", True)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["ci_passing"] is False

    def test_skip_when_review_not_clean(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=1,
            copilot_review_inline_count=2,
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "not clean" in result.details.lower()

    def test_skip_when_unresolved_threads(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=2,
            repairable_threads=2,
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "unresolved" in result.details.lower()

    def test_skip_when_derived_unresolved_threads_nonzero(self) -> None:
        """Approval is blocked when DerivedState overrides unresolved_threads to > 0."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
        )
        derived = DerivedState(snapshot)
        derived.set("unresolved_threads", 1)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "unresolved" in result.details.lower()

    def test_proceed_when_derived_clears_unresolved_threads(self) -> None:
        """Approval can proceed when DerivedState sets unresolved_threads to 0."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=2,
            repairable_threads=2,  # stale snapshot value
        )
        derived = DerivedState(snapshot)
        derived.set("unresolved_threads", 0)  # ResolveThreadsAction updated this
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        # Passes no_unresolved_threads; should proceed to EXECUTE
        assert result.preconditions.get("no_unresolved_threads") is True

    def test_skip_when_non_copilot_changes_requested_on_head(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            has_approval_on_head=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
            reviews=[
                ReviewInfo(id=10, user="alice", state="CHANGES_REQUESTED", commit_sha="head-sha"),
            ],
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "requested changes" in result.details.lower()

    def test_execute_when_all_conditions_met(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_calls_provider(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.approve_pr.return_value = True
        action = ApproveAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        provider.approve_pr.assert_called_once_with(42, "sha123", "Auto-approved by AI PR loop")
        assert derived.has_approval_on_head is True
        assert derived.has_approver_approval_on_head is True

    def test_execute_skips_when_provider_skips_approval(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.approve_pr.return_value = False
        action = ApproveAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions == {"approver_token_available": False}
        assert "skipped approval" in result.details.lower()
        assert derived.has_approval_on_head is False
        assert derived.has_approver_approval_on_head is False

    def test_execute_when_review_commented_and_inline_zero(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=1,
            copilot_review_inline_count=0,
            unresolved_threads=0,
            repairable_threads=0,
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_failed_when_provider_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.approve_pr.side_effect = RuntimeError("boom")
        action = ApproveAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "approve_pr call failed" in result.details

    def test_execute_reraises_rate_limit_when_provider_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.approve_pr.side_effect = ProviderRateLimitError(provider="github")
        action = ApproveAction()

        with pytest.raises(ProviderRateLimitError):
            action.execute(provider, snapshot, derived)

    # -----------------------------------------------------------------------
    # Gate verdict enforcement (new)
    # -----------------------------------------------------------------------

    def test_execute_when_gate_verdict_passed(self) -> None:
        """Gate verdict passed=True → action can proceed to EXECUTE."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
            copilot_gate_verdict=_clean_verdict(),
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions.get("gate_verdict_passed") is True

    def test_skip_when_gate_verdict_has_comments(self) -> None:
        """Gate verdict with HAS_COMMENTS → blocks approval."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            # review_state=APPROVED would pass legacy check, but gate says there are comments
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
            copilot_gate_verdict=_failing_verdict(
                reason=REASON_HAS_COMMENTS,
                details="Review reports 2 comment(s) posted (suppressed: 0)",
            ),
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert REASON_HAS_COMMENTS in result.details
        assert result.preconditions.get("gate_verdict_passed") is False

    def test_skip_when_gate_verdict_suppressed_comments(self) -> None:
        """Gate verdict with SUPPRESSED_COMMENTS → blocks approval."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=1,
            copilot_review_inline_count=0,  # 0 inline — legacy check would pass
            unresolved_threads=0,
            repairable_threads=0,
            copilot_gate_verdict=_failing_verdict(
                reason=REASON_SUPPRESSED_COMMENTS,
                details="1 suppressed/low-confidence comment(s)",
            ),
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert REASON_SUPPRESSED_COMMENTS in result.details

    def test_skip_when_gate_verdict_awaiting_fresh(self) -> None:
        """Gate verdict with AWAITING_FRESH → blocks approval."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
            copilot_gate_verdict=_failing_verdict(
                reason=REASON_AWAITING_FRESH,
                details="No fresh review on HEAD",
            ),
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert REASON_AWAITING_FRESH in result.details

    def test_legacy_path_when_gate_verdict_none(self) -> None:
        """When copilot_gate_verdict is None, legacy check is used (backward compat)."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
            unresolved_threads=0,
            repairable_threads=0,
            copilot_gate_verdict=None,  # explicitly None → legacy path
        )
        derived = DerivedState(snapshot)
        action = ApproveAction()
        result = action.evaluate(snapshot, derived)
        # Legacy path: APPROVED → clean → EXECUTE
        assert result.decision == ActionDecision.EXECUTE
        assert "gate_verdict_passed" not in result.preconditions
        assert "review_clean" in result.preconditions


def _suppressed_only_verdict(
    review_id: int = 5,
    *,
    reason: str = REASON_SUPPRESSED_COMMENTS,
) -> CopilotGateVerdict:
    """Build a suppressed-only blocking verdict (0 posted, suppressed > 0)."""
    return CopilotGateVerdict(
        passed=False,
        reason=reason,
        review_id=review_id,
        body_comment_count=0,
        suppressed_count=2,
        details="suppressed/low-confidence comment(s)",
    )


def _suppressed_snapshot(
    *,
    verdict: CopilotGateVerdict,
    repair_satisfied_review_id: int | None,
    head_changed_since_review: bool = False,
    unresolved_threads: int = 0,
    repairable_threads: int = 0,
) -> PRStateSnapshot:
    return PRStateSnapshot(
        pr_number=1,
        has_approval_on_head=False,
        ci_status="passing",
        review_state="APPROVED",
        copilot_review_id=5,
        copilot_review_inline_count=0,
        unresolved_threads=unresolved_threads,
        repairable_threads=repairable_threads,
        copilot_gate_verdict=verdict,
        repair_satisfied_review_id=repair_satisfied_review_id,
        head_changed_since_review=head_changed_since_review,
    )


class TestApproveActionSuppressedBypass:
    """Suppressed-only gate block is cleared only by a valid repair-satisfied marker."""

    def test_execute_when_suppressed_evaluated_marker_matches(self) -> None:
        """Suppressed-only block + matching marker + unchanged HEAD + 0 threads → EXECUTE."""
        snapshot = _suppressed_snapshot(verdict=_suppressed_only_verdict(5), repair_satisfied_review_id=5)
        result = ApproveAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["suppressed_comments_evaluated"] is True

    def test_execute_when_new_ccr_suppressed_evaluated(self) -> None:
        """Format-agnostic: a new-CCR suppressed-only block is also cleared by the marker."""
        verdict = _suppressed_only_verdict(5, reason=REASON_NEW_CCR_NOT_APPROVED)
        snapshot = _suppressed_snapshot(verdict=verdict, repair_satisfied_review_id=5)
        result = ApproveAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["suppressed_comments_evaluated"] is True

    def test_skip_when_no_marker(self) -> None:
        snapshot = _suppressed_snapshot(verdict=_suppressed_only_verdict(5), repair_satisfied_review_id=None)
        result = ApproveAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["suppressed_comments_evaluated"] is False
        assert REASON_SUPPRESSED_COMMENTS in result.details

    def test_skip_when_head_changed_since_review(self) -> None:
        snapshot = _suppressed_snapshot(
            verdict=_suppressed_only_verdict(5),
            repair_satisfied_review_id=5,
            head_changed_since_review=True,
        )
        result = ApproveAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["suppressed_comments_evaluated"] is False

    def test_skip_when_marker_review_id_mismatch(self) -> None:
        snapshot = _suppressed_snapshot(verdict=_suppressed_only_verdict(5), repair_satisfied_review_id=99)
        result = ApproveAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["suppressed_comments_evaluated"] is False

    def test_skip_when_unresolved_threads_present(self) -> None:
        snapshot = _suppressed_snapshot(
            verdict=_suppressed_only_verdict(5),
            repair_satisfied_review_id=5,
            unresolved_threads=1,
            repairable_threads=1,
        )
        result = ApproveAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["suppressed_comments_evaluated"] is False

    def test_skip_when_real_comments_even_with_marker(self) -> None:
        """A HAS_COMMENTS block is never cleared by the suppressed-only bypass."""
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_HAS_COMMENTS,
            review_id=5,
            body_comment_count=2,
            suppressed_count=1,
            details="2 comment(s) posted",
        )
        snapshot = _suppressed_snapshot(verdict=verdict, repair_satisfied_review_id=5)
        result = ApproveAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["suppressed_comments_evaluated"] is False
        assert REASON_HAS_COMMENTS in result.details
