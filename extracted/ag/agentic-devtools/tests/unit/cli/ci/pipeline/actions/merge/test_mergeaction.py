"""Tests for MergeAction."""

import json
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.merge import MergeAction
from agentic_devtools.cli.ci.pipeline.deferral import SUPPRESSED_DEFERRAL_SENTINEL
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _ready_snapshot(**overrides: object) -> PRStateSnapshot:
    """Return a snapshot with all merge preconditions satisfied."""
    defaults: dict = {
        "pr_number": 1,
        "is_draft": False,
        "has_approval_on_head": True,
        "has_approver_approval_on_head": True,
        "ci_status": "passing",
        "labels": ["ai-auto-merge-allowed"],
        "mergeable": True,
        "unresolved_threads": 0,
        "copilot_review_pending": False,
        "review_state": "APPROVED",
        "copilot_review_id": 99,
        "copilot_review_inline_count": 0,
    }
    defaults.update(overrides)
    return PRStateSnapshot(**defaults)


class TestMergeAction:
    """Tests for merge action evaluation."""

    def test_skip_when_draft(self) -> None:
        """Merge is skipped when PR is a draft."""
        snapshot = _ready_snapshot(is_draft=True)
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "draft" in result.details.lower()

    def test_skip_when_draft_via_derived(self) -> None:
        """Merge is skipped when is_draft is set on DerivedState (e.g., publish failed)."""
        snapshot = _ready_snapshot(is_draft=False)
        derived = DerivedState(snapshot)
        derived.set("is_draft", True)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "draft" in result.details.lower()

    def test_not_draft_via_derived_allows_proceed(self) -> None:
        """When derived marks is_draft=False (publish succeeded), not_draft precondition passes."""
        snapshot = _ready_snapshot(is_draft=True)
        derived = DerivedState(snapshot)
        derived.set("is_draft", False)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        # Should proceed past draft check; will fail at approval check
        assert result.preconditions.get("not_draft") is True

    def test_skip_when_not_approved(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=False,
            ci_status="passing",
            labels=["ai-auto-merge-allowed"],
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "not approved" in result.details.lower()

    def test_skip_when_repair_dispatched(self) -> None:
        """Merge is skipped after conflict repair is dispatched in the same run."""
        snapshot = _ready_snapshot()
        derived = DerivedState(snapshot)
        derived.set("repair_dispatched", True)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_repair_dispatched"] is False
        assert "repair dispatched" in result.details.lower()

    def test_skip_when_ci_not_passing(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=True,
            has_approver_approval_on_head=True,
            ci_status="pending",
            labels=["ai-auto-merge-allowed"],
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP

    def test_skip_when_ci_pending_even_with_squash_preserved_green(self) -> None:
        """MergeAction must NEVER consume squash_preserved_green — it gates on the real HEAD CI."""
        snapshot = _ready_snapshot(ci_status="pending")
        derived = DerivedState(snapshot)
        derived.set("squash_preserved_green", True)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["ci_passing"] is False

    def test_skip_when_ci_unknown_even_with_squash_preserved_green(self) -> None:
        """Unreported checks (ci_status='unknown') must block merge regardless of the squash flag."""
        snapshot = _ready_snapshot(ci_status="unknown")
        derived = DerivedState(snapshot)
        derived.set("squash_preserved_green", True)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["ci_passing"] is False

    def test_skip_when_no_label(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=True,
            has_approver_approval_on_head=True,
            ci_status="passing",
            labels=[],
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "label" in result.details.lower()

    def test_skip_when_not_mergeable(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=True,
            has_approver_approval_on_head=True,
            ci_status="passing",
            labels=["ai-auto-merge-allowed"],
            mergeable=False,
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "not mergeable" in result.details.lower()

    def test_skip_when_unresolved_threads(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=True,
            has_approver_approval_on_head=True,
            ci_status="passing",
            labels=["ai-auto-merge-allowed"],
            mergeable=True,
            unresolved_threads=1,
            repairable_threads=1,
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP

    def test_skip_when_thread_state_degraded(self) -> None:
        """Merge fails closed when the provider cannot report review-thread state."""
        snapshot = _ready_snapshot(unresolved_threads=1, repairable_threads=1, unresolved_threads_degraded=True)
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions.get("thread_state_known") is False
        assert "degraded / unknown" in result.details

    def test_skip_when_thread_state_degraded_even_with_zero_count(self) -> None:
        """A degraded lookup blocks merge even if the resolved count reads zero."""
        snapshot = _ready_snapshot(unresolved_threads=0, repairable_threads=0, unresolved_threads_degraded=True)
        derived = DerivedState(snapshot)
        derived.set("unresolved_threads", 0)  # e.g. ResolveThreadsAction ran this run
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions.get("thread_state_known") is False

    def test_thread_state_known_precondition_passes_by_default(self) -> None:
        """A provider that reports thread state clears the degraded precondition."""
        snapshot = _ready_snapshot()
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.preconditions.get("thread_state_known") is True

    def test_skip_when_only_copilot_approved(self) -> None:
        """Copilot's approval alone must not satisfy the approver-PAT merge gate."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            has_approval_on_head=True,  # Copilot approved → generic flag set
            has_approver_approval_on_head=False,  # ...but the approver PAT has not approved
            ci_status="passing",
            labels=["ai-auto-merge-allowed"],
            mergeable=True,
            unresolved_threads=0,
            repairable_threads=0,
            review_state="APPROVED",
            copilot_review_id=99,
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "not approved" in result.details.lower()

    def test_uses_precise_approver_signal_when_login_known(self) -> None:
        """When approver_login is set, has_approver_approval_on_head gates the merge."""
        snapshot = _ready_snapshot(
            approver_login="loop-bot",
            has_approver_approval_on_head=True,
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.preconditions.get("approved") is True

    def test_skip_when_approver_login_known_but_approver_not_approved(self) -> None:
        """Precise gate: skip when the approver-PAT has not yet approved, even if
        another reviewer has already approved on HEAD."""
        snapshot = _ready_snapshot(
            approver_login="loop-bot",
            has_approver_approval_on_head=False,
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "not approved" in result.details.lower()

    def test_skip_when_approver_login_unknown_and_approver_not_yet_approved(self) -> None:
        """Merge stays blocked until the precise approver approval is present."""
        snapshot = _ready_snapshot(
            approver_login="",
            has_approver_approval_on_head=False,
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions.get("approved") is False
        assert "not approved" in result.details.lower()

    def test_skip_when_derived_unresolved_threads_nonzero(self) -> None:
        """Merge is blocked when DerivedState overrides unresolved_threads to > 0."""
        snapshot = _ready_snapshot(unresolved_threads=0, repairable_threads=0)
        derived = DerivedState(snapshot)
        derived.set("unresolved_threads", 1)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "unresolved" in result.details.lower()

    def test_proceed_when_derived_clears_unresolved_threads(self) -> None:
        """Merge can proceed when DerivedState sets unresolved_threads to 0."""
        snapshot = _ready_snapshot(unresolved_threads=3, repairable_threads=3)  # stale snapshot value
        derived = DerivedState(snapshot)
        derived.set("unresolved_threads", 0)  # ResolveThreadsAction updated this
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.preconditions.get("no_unresolved_threads") is True

    def test_skip_when_review_pending(self) -> None:
        """Merge is skipped when Copilot review is still pending."""
        snapshot = _ready_snapshot(copilot_review_pending=True)
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "pending" in result.details.lower()

    def test_skip_when_review_pending_via_derived(self) -> None:
        """Merge is skipped when copilot_review_pending is set via derived state."""
        snapshot = _ready_snapshot(copilot_review_pending=False)
        derived = DerivedState(snapshot)
        derived.set("copilot_review_pending", True)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "pending" in result.details.lower()

    def test_skip_when_non_copilot_changes_requested_on_head(self) -> None:
        snapshot = _ready_snapshot(
            head_sha="head-sha",
            reviews=[ReviewInfo(id=20, user="alice", state="CHANGES_REQUESTED", commit_sha="head-sha")],
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "requested changes" in result.details.lower()

    def test_skip_when_no_copilot_review(self) -> None:
        """Merge is skipped when no Copilot review exists on HEAD."""
        snapshot = _ready_snapshot(review_state="", copilot_review_id=0)
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "no copilot review" in result.details.lower()

    def test_skip_when_review_changes_requested(self) -> None:
        """Merge is skipped when Copilot review is CHANGES_REQUESTED."""
        snapshot = _ready_snapshot(review_state="CHANGES_REQUESTED", copilot_review_id=5)
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "actionable" in result.details.lower()

    def test_skip_when_review_commented_with_inline(self) -> None:
        """Merge is skipped when Copilot review is COMMENTED with inline comments."""
        snapshot = _ready_snapshot(
            review_state="COMMENTED",
            copilot_review_id=5,
            copilot_review_inline_count=3,
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "actionable" in result.details.lower()

    def test_execute_when_all_conditions_met(self) -> None:
        snapshot = _ready_snapshot()
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_when_review_commented_no_inline(self) -> None:
        """COMMENTED with 0 inline comments is considered clean."""
        snapshot = _ready_snapshot(
            review_state="COMMENTED",
            copilot_review_id=5,
            copilot_review_inline_count=0,
        )
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_calls_provider(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = MergeAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        provider.merge_pr.assert_called_once_with(42, "sha123", "rebase")

    def test_execute_uses_squash_when_multi_commit(self) -> None:
        """MergeAction uses squash merge when commit_count > 1."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=3, title="Fix bug")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = MergeAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert "squash" in result.details.lower()
        provider.merge_pr.assert_called_once_with(42, "sha123", "squash", commit_title="Fix bug (#42)")

    def test_execute_uses_clean_fallback_title_for_squash(self) -> None:
        """Fallback squash title does not duplicate PR number when PR title is missing."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=3, title="")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = MergeAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        provider.merge_pr.assert_called_once_with(42, "sha123", "squash", commit_title="PR #42")

    def test_execute_uses_rebase_when_single_commit(self) -> None:
        """MergeAction uses rebase merge when commit_count == 1."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = MergeAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert "rebase" in result.details.lower()
        provider.merge_pr.assert_called_once_with(42, "sha123", "rebase")

    def test_execute_uses_rebase_when_commit_count_default(self) -> None:
        """MergeAction falls back to rebase when commit_count is default (1)."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = MergeAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        provider.merge_pr.assert_called_once_with(42, "sha123", "rebase")

    def test_execute_failed_when_provider_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.merge_pr.side_effect = RuntimeError("merge boom")
        action = MergeAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "merge_pr call failed" in result.details

    def test_execute_reraises_rate_limit_when_provider_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.merge_pr.side_effect = ProviderRateLimitError(provider="github")
        action = MergeAction()

        with pytest.raises(ProviderRateLimitError):
            action.execute(provider, snapshot, derived)

    def test_execute_reraises_explicit_rate_limit_from_merge(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.merge_pr.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            MergeAction().execute(provider, snapshot, derived)

    def test_execute_deletes_branch_after_merge(self) -> None:
        """MergeAction deletes the source branch after successful merge."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1, head_branch="feature/my-branch")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = MergeAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.delete_branch.assert_called_once_with("feature/my-branch")

    def test_execute_skips_branch_deletion_when_head_branch_empty(self) -> None:
        """MergeAction skips branch deletion when head_branch is empty."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1, head_branch="")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = MergeAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.delete_branch.assert_not_called()

    def test_execute_succeeds_when_branch_deletion_fails(self) -> None:
        """MergeAction still succeeds if branch deletion raises."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1, head_branch="feature/branch")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.delete_branch.side_effect = RuntimeError("branch already deleted")
        action = MergeAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert "merged" in result.details.lower()

    def test_execute_reraises_rate_limit_from_branch_deletion(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1, head_branch="feature/branch")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.delete_branch.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            MergeAction().execute(provider, snapshot, derived)

    # -----------------------------------------------------------------------
    # Gate verdict enforcement (new)
    # -----------------------------------------------------------------------

    def test_execute_when_gate_verdict_passed(self) -> None:
        """Gate verdict passed=True → action can proceed to EXECUTE."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import CopilotGateVerdict

        verdict = CopilotGateVerdict(passed=True, reason="clean", review_id=9)
        snapshot = _ready_snapshot(copilot_gate_verdict=verdict)
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions.get("gate_verdict_passed") is True

    def test_skip_when_gate_verdict_has_comments(self) -> None:
        """Gate verdict with HAS_COMMENTS blocks merge."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import (
            REASON_HAS_COMMENTS,
            CopilotGateVerdict,
        )

        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_HAS_COMMENTS,
            details="Review reports 2 comment(s)",
        )
        snapshot = _ready_snapshot(copilot_gate_verdict=verdict)
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert REASON_HAS_COMMENTS in result.details
        assert result.preconditions.get("gate_verdict_passed") is False

    def test_skip_when_gate_verdict_awaiting_fresh(self) -> None:
        """Gate verdict AWAITING_FRESH blocks merge."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import (
            REASON_AWAITING_FRESH,
            CopilotGateVerdict,
        )

        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_AWAITING_FRESH,
            details="No fresh review on HEAD",
        )
        snapshot = _ready_snapshot(copilot_gate_verdict=verdict)
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert REASON_AWAITING_FRESH in result.details

    def test_legacy_path_when_gate_verdict_none(self) -> None:
        """When copilot_gate_verdict is None, legacy checks are used (backward compat)."""
        snapshot = _ready_snapshot(copilot_gate_verdict=None)
        derived = DerivedState(snapshot)
        action = MergeAction()
        result = action.evaluate(snapshot, derived)
        # Legacy path: review_state=APPROVED, copilot_review_id=99 → EXECUTE
        assert result.decision == ActionDecision.EXECUTE
        assert "gate_verdict_passed" not in result.preconditions
        assert "has_copilot_review" in result.preconditions


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


class TestMergeActionSuppressedBypass:
    """Suppressed-only gate block is cleared for merge only by a valid repair-satisfied marker."""

    def test_execute_when_suppressed_evaluated_marker_matches(self) -> None:
        """Suppressed-only block + matching marker + unchanged HEAD → EXECUTE (merge)."""
        snapshot = _ready_snapshot(
            copilot_gate_verdict=_suppressed_only_verdict(5),
            repair_satisfied_review_id=5,
            head_changed_since_review=False,
        )
        result = MergeAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["suppressed_comments_evaluated"] is True

    def test_execute_when_new_ccr_suppressed_evaluated(self) -> None:
        """Format-agnostic: a new-CCR suppressed-only block is also cleared for merge."""
        snapshot = _ready_snapshot(
            copilot_gate_verdict=_suppressed_only_verdict(5, reason=REASON_NEW_CCR_NOT_APPROVED),
            repair_satisfied_review_id=5,
        )
        result = MergeAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["suppressed_comments_evaluated"] is True

    def test_skip_when_no_marker(self) -> None:
        snapshot = _ready_snapshot(
            copilot_gate_verdict=_suppressed_only_verdict(5),
            repair_satisfied_review_id=None,
        )
        result = MergeAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["suppressed_comments_evaluated"] is False
        assert REASON_SUPPRESSED_COMMENTS in result.details

    def test_skip_when_head_changed_since_review(self) -> None:
        snapshot = _ready_snapshot(
            copilot_gate_verdict=_suppressed_only_verdict(5),
            repair_satisfied_review_id=5,
            head_changed_since_review=True,
        )
        result = MergeAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["suppressed_comments_evaluated"] is False

    def test_skip_when_marker_review_id_mismatch(self) -> None:
        snapshot = _ready_snapshot(
            copilot_gate_verdict=_suppressed_only_verdict(5),
            repair_satisfied_review_id=99,
        )
        result = MergeAction().evaluate(snapshot, DerivedState(snapshot))
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
        snapshot = _ready_snapshot(copilot_gate_verdict=verdict, repair_satisfied_review_id=5)
        result = MergeAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["suppressed_comments_evaluated"] is False
        assert REASON_HAS_COMMENTS in result.details

    # -----------------------------------------------------------------------
    # Post-merge suppressed-triage dispatch
    # -----------------------------------------------------------------------

    def test_execute_dispatches_triage_when_deferral_keys_set(self) -> None:
        """MergeAction dispatches suppressed-comment triage after merge when DeferSuppressedAction keys are set."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        derived.set("suppressed_deferral_issue_number", 99)
        derived.set("suppressed_deferral_review_id", 777)
        provider = MagicMock()

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_suppressed_triage.assert_called_once_with(issue_number=99, pr_number=42, review_id=777)

    def test_execute_does_not_dispatch_triage_when_keys_absent(self) -> None:
        """MergeAction does not call dispatch_suppressed_triage when no deferral happened."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_suppressed_triage.assert_not_called()

    def test_execute_fails_when_triage_dispatch_fails(self) -> None:
        """A post-merge triage dispatch failure returns FAILED.

        On a re-trigger the snapshot will carry ``mergeable_state="merged"``;
        the execute path detects this, skips merge_pr, and retries dispatch.
        """
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        derived.set("suppressed_deferral_issue_number", 99)
        derived.set("suppressed_deferral_review_id", 777)
        provider = MagicMock()
        provider.dispatch_suppressed_triage.side_effect = RuntimeError("SPECKIT_PR_TOKEN not set")

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED

    def test_execute_retrigger_already_merged_retries_dispatch(self) -> None:
        """On a re-trigger after a post-merge dispatch failure, mergeable_state='merged'
        causes merge_pr to be skipped and dispatch to be attempted again."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="sha123",
            commit_count=1,
            mergeable_state="merged",
        )
        derived = DerivedState(snapshot)
        derived.set("suppressed_deferral_issue_number", 99)
        derived.set("suppressed_deferral_review_id", 777)
        provider = MagicMock()

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.merge_pr.assert_not_called()
        provider.dispatch_suppressed_triage.assert_called_once_with(issue_number=99, pr_number=42, review_id=777)

    def test_execute_retrigger_already_merged_dispatch_still_fails(self) -> None:
        """On a re-trigger with mergeable_state='merged', a persistent dispatch failure
        still returns FAILED so the operator is alerted."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="sha123",
            commit_count=1,
            mergeable_state="merged",
        )
        derived = DerivedState(snapshot)
        derived.set("suppressed_deferral_issue_number", 99)
        derived.set("suppressed_deferral_review_id", 777)
        provider = MagicMock()
        provider.dispatch_suppressed_triage.side_effect = RuntimeError("still failing")

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        provider.merge_pr.assert_not_called()

    def test_execute_recovers_deferral_from_issue_comments_when_not_in_derived(self) -> None:
        """MergeAction recovers suppressed deferral state from issue comments when the snapshot
        was built outside the suppressed-only blocked-verdict branch (e.g. after a CI repair)."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        payload = json.dumps({"review_id": "777", "issue": 99, "active": True})
        marker_body = f"{SUPPRESSED_DEFERRAL_SENTINEL}{payload} -->"
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=1, author="copilot", body=marker_body)]
        provider.get_pr_token_login.return_value = "copilot"

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_suppressed_triage.assert_called_once_with(issue_number=99, pr_number=42, review_id=777)

    def test_execute_does_not_dispatch_when_issue_comments_recovery_fails(self) -> None:
        """When recovering deferral state from issue comments fails, dispatch is skipped (fail-open)."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.side_effect = RuntimeError("network error")

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_suppressed_triage.assert_not_called()

    def test_execute_reraises_rate_limit_when_issue_comments_recovery_fails(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_issue_comments.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            MergeAction().execute(provider, snapshot, derived)

    def test_execute_reraises_rate_limit_when_pr_login_lookup_fails(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.get_pr_token_login.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            MergeAction().execute(provider, snapshot, derived)

    def test_execute_reraises_rate_limit_when_triage_dispatch_fails(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        derived.set("suppressed_deferral_issue_number", 99)
        derived.set("suppressed_deferral_review_id", 777)
        provider = MagicMock()
        provider.dispatch_suppressed_triage.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            MergeAction().execute(provider, snapshot, derived)

    def test_execute_skips_recovery_when_list_issue_comments_not_callable(self) -> None:
        """When provider has no list_issue_comments, recovery is skipped and no dispatch occurs."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock(spec=["merge_pr", "delete_remote_branch"])  # no list_issue_comments

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE

    def test_execute_recovers_without_get_pr_token_login(self) -> None:
        """Recovery succeeds using default trusted authors when get_pr_token_login is absent."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock(spec=["list_issue_comments", "merge_pr", "dispatch_suppressed_triage"])
        payload = json.dumps({"review_id": "777", "issue": 99, "active": True})
        marker_body = f"{SUPPRESSED_DEFERRAL_SENTINEL}{payload} -->"
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=1, author="copilot", body=marker_body)]

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_suppressed_triage.assert_called_once_with(issue_number=99, pr_number=42, review_id=777)

    def test_execute_recovers_when_get_pr_token_login_raises(self) -> None:
        """Recovery continues (with default trust set) when get_pr_token_login raises."""
        snapshot = PRStateSnapshot(pr_number=42, head_sha="sha123", commit_count=1)
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.get_pr_token_login.side_effect = RuntimeError("no token")
        payload = json.dumps({"review_id": "777", "issue": 99, "active": True})
        marker_body = f"{SUPPRESSED_DEFERRAL_SENTINEL}{payload} -->"
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=1, author="copilot", body=marker_body)]

        result = MergeAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_suppressed_triage.assert_called_once_with(issue_number=99, pr_number=42, review_id=777)
