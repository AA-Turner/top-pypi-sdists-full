"""Tests for RequestReviewAction."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.pipeline.actions.request_review import RequestReviewAction
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_API_ERROR,
    REASON_AWAITING_FRESH,
    REASON_CLEAN,
    REASON_CONTENT_CHANGED,
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

_PATCH_DETECTOR = "agentic_devtools.cli.ci.pipeline.actions.request_review.is_copilot_session_active_via_agent_task"

_PRIOR_SHA = "b" * 40


class TestRequestReviewAction:
    """Tests for request review action evaluation and execution."""

    def test_runs_after_invalidation(self) -> None:
        """RequestReviewAction opts in to run after snapshot invalidation."""
        action = RequestReviewAction()
        assert action.runs_after_invalidation is True

    def test_skip_when_draft(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, is_draft=True)
        derived = DerivedState(snapshot)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP

    def test_skip_when_ci_not_passing(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, is_draft=False, ci_status="pending")
        derived = DerivedState(snapshot)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "ci is pending" in result.details.lower()

    def test_skip_when_review_exists(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "review exists" in result.details.lower()

    def test_skip_when_already_requested(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=True,
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "already requested" in result.details.lower()

    def test_skip_when_derived_pending_review_is_true(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
        )
        derived = DerivedState(snapshot)
        derived.set("copilot_review_pending", True)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "already requested" in result.details.lower()

    def test_skip_when_repair_dispatched(self) -> None:
        """Review request is blocked when repair was just dispatched."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
        )
        derived = DerivedState(snapshot)
        derived.set("repair_dispatched", True)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "repair dispatched" in result.details.lower()

    def test_skip_when_active_session(self) -> None:
        """Review request is blocked when Copilot coding session is active."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
            base_repo_full_name="owner/repo",
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=True) as mock_detector:
            result = action.evaluate(snapshot, derived)
            mock_detector.assert_called_once_with("owner/repo", 1)
        assert result.decision == ActionDecision.SKIP
        assert "session active" in result.details.lower()

    def test_skip_when_unresolved_threads(self) -> None:
        """Review request is blocked when unresolved threads exist."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
            unresolved_threads=3,
            repairable_threads=3,
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_unresolved_threads"] is False
        assert "unresolved thread" in result.details.lower()

    def test_execute_when_derived_clears_unresolved_threads(self) -> None:
        """Review request can proceed after ResolveThreadsAction updates derived state."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
            unresolved_threads=3,
            repairable_threads=3,
        )
        derived = DerivedState(snapshot)
        derived.set("unresolved_threads", 0)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_when_no_review(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_when_ci_pending_but_squash_preserved_green(self) -> None:
        """A tree-preserving squash this run relaxes the ci_passing gate on the new HEAD."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="pending",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
        )
        derived = DerivedState(snapshot)
        derived.set("squash_preserved_green", True)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["ci_passing"] is True

    def test_squash_preserved_green_still_skips_when_repair_dispatched(self) -> None:
        """The relaxation only satisfies ci_passing — a repair dispatch still defers review."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="pending",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
        )
        derived = DerivedState(snapshot)
        derived.set("squash_preserved_green", True)
        derived.set("repair_dispatched", True)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "repair dispatched" in result.details.lower()

    def test_squash_preserved_green_still_skips_when_unresolved_threads(self) -> None:
        """The relaxation only satisfies ci_passing — unresolved threads still defer review."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="pending",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
            unresolved_threads=2,
            repairable_threads=2,
        )
        derived = DerivedState(snapshot)
        derived.set("squash_preserved_green", True)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "unresolved thread" in result.details.lower()

    def test_squash_preserved_green_still_skips_when_active_session(self) -> None:
        """The relaxation only satisfies ci_passing — an active session still defers review."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="pending",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
            base_repo_full_name="owner/repo",
        )
        derived = DerivedState(snapshot)
        derived.set("squash_preserved_green", True)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=True):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "session active" in result.details.lower()

    def test_squash_preserved_green_still_skips_when_review_exists(self) -> None:
        """The relaxation only satisfies ci_passing — an existing review still defers request."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="pending",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_pending=False,
        )
        derived = DerivedState(snapshot)
        derived.set("squash_preserved_green", True)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "review exists" in result.details.lower()

    def test_execute_calls_provider(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = RequestReviewAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        provider.request_reviewer.assert_called_once()

    def test_execute_sets_derived_pending(self) -> None:
        """execute() must set derived.copilot_review_pending so downstream actions gate correctly."""
        snapshot = PRStateSnapshot(pr_number=42, copilot_review_pending=False)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = RequestReviewAction()
        action.execute(provider, snapshot, derived)
        assert derived.copilot_review_pending is True
        # Snapshot itself must remain unchanged (frozen)
        assert snapshot.copilot_review_pending is False

    def test_execute_failed_when_provider_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.request_reviewer.side_effect = RuntimeError("request failed")
        action = RequestReviewAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "Failed to request Copilot review" in result.details

    def test_execute_reraises_rate_limit_when_provider_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.request_reviewer.side_effect = ProviderRateLimitError(provider="github")
        action = RequestReviewAction()

        with pytest.raises(ProviderRateLimitError):
            action.execute(provider, snapshot, derived)


class TestRequestReviewActionGateVerdictCarryOver:
    """Tests for the gate-verdict carry-over guard in RequestReviewAction.evaluate."""

    @staticmethod
    def _snapshot(
        verdict: CopilotGateVerdict | None,
        *,
        review_state: str = "",
        copilot_review_id: int = 0,
    ) -> PRStateSnapshot:
        """Build a snapshot whose only blocking factor may be the gate verdict.

        ``review_state``/``copilot_review_id`` default to empty, mirroring the
        HEAD-filtered snapshot after a rebase or squash moved HEAD away from the
        reviewed commit.
        """
        return PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state=review_state,
            copilot_review_id=copilot_review_id,
            copilot_review_pending=False,
            copilot_gate_verdict=verdict,
        )

    def test_skip_when_clean_review_carried_over_to_new_head(self) -> None:
        """A clean prior review the gate carried over must not trigger a new request."""
        verdict = CopilotGateVerdict(
            passed=True,
            reason=REASON_CLEAN,
            review_id=100,
            carried_over_sha=_PRIOR_SHA,
        )
        snapshot = self._snapshot(verdict)
        derived = DerivedState(snapshot)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_effective_review_on_head"] is False
        assert _PRIOR_SHA[:12] in result.details
        assert "still applies" in result.details

    def test_head_review_details_take_precedence_over_carry_over(self) -> None:
        """A review on HEAD keeps its own skip reason even when a carry-over exists."""
        verdict = CopilotGateVerdict(
            passed=True,
            reason=REASON_CLEAN,
            review_id=100,
            carried_over_sha=_PRIOR_SHA,
        )
        snapshot = self._snapshot(verdict, review_state="APPROVED", copilot_review_id=100)
        derived = DerivedState(snapshot)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "review exists on HEAD" in result.details

    def test_execute_when_passing_verdict_has_no_carry_over(self) -> None:
        """A passing verdict without a carry-over does not suppress the review request."""
        verdict = CopilotGateVerdict(passed=True, reason=REASON_CLEAN, review_id=100)
        snapshot = self._snapshot(verdict)
        derived = DerivedState(snapshot)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["no_effective_review_on_head"] is True

    @pytest.mark.parametrize(
        "reason",
        [
            REASON_HAS_COMMENTS,
            REASON_SUPPRESSED_COMMENTS,
            REASON_NEW_CCR_NOT_APPROVED,
            REASON_CONTENT_CHANGED,
            REASON_AWAITING_FRESH,
            REASON_API_ERROR,
        ],
    )
    def test_execute_when_carried_over_verdict_is_blocking(self, reason: str) -> None:
        """A carried-over review that does not pass the gate still allows a new request.

        Regression guard for the permanent-stall failure mode: ``DispatchRepairAction``
        can be dedup- or cycle-limited, and a fresh review id is what resets its dedup
        key.  If ``request_review`` also skipped on a *blocking* carry-over, approve and
        merge would stay gated with no action able to unstick the PR.
        """
        verdict = CopilotGateVerdict(
            passed=False,
            reason=reason,
            review_id=100,
            carried_over_sha=_PRIOR_SHA,
        )
        snapshot = self._snapshot(verdict)
        derived = DerivedState(snapshot)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["no_effective_review_on_head"] is True
