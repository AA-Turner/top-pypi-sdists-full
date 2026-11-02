"""Tests for RequestReviewAction."""

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import AgentTaskInventory, AgentTaskLifecycle, ReviewInfo
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
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun
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
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="APPROVED",
                    commit_sha="head-sha",
                )
            ],
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

    def test_skip_when_repair_cycle_limit_reached(self) -> None:
        """Review request is blocked when the global repair cycle limit is reached."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
        )
        derived = DerivedState(snapshot)
        derived.set("cycle_limit_reached", True)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "human intervention" in result.details.lower()

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
            head_branch="copilot/issue-1-fix",
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        derived.set("provider", provider)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=True) as mock_detector:
            result = action.evaluate(snapshot, derived)
            mock_detector.assert_called_once_with(
                "owner/repo",
                1,
                head_branch="copilot/issue-1-fix",
                pr_id=None,
                head_sha=snapshot.head_sha,
                provider=provider,
            )
        assert result.decision == ActionDecision.SKIP
        assert "session active" in result.details.lower()

    def test_skip_when_session_inventory_unavailable(self) -> None:
        """Review request is blocked when session inventory is unavailable."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
            base_repo_full_name="owner/repo",
            head_branch="copilot/issue-1-fix",
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=None) as mock_detector:
            result = action.evaluate(snapshot, derived)
            mock_detector.assert_called_once_with(
                "owner/repo",
                1,
                head_branch="copilot/issue-1-fix",
                pr_id=None,
                head_sha=snapshot.head_sha,
                provider=None,
            )
        assert result.decision == ActionDecision.SKIP
        assert "inventory unavailable" in result.details.lower()

    def test_expired_task_with_detail_404_no_longer_blocks_request_review(self) -> None:
        """A scoped 404 for a demonstrably expired task does not hold the review guard."""
        now = datetime.now(UTC)

        class ExpiredTaskProvider:
            def list_pr_agent_task_lifecycles(self, pr_number: int, *, head_branch: str, head_sha: str):
                return AgentTaskInventory(
                    (
                        AgentTaskLifecycle(
                            task_id="task-expired",
                            repository="owner/repo",
                            pr_number=pr_number,
                            head_branch=head_branch,
                            state="in_progress",
                            created_at=(now - timedelta(minutes=90)).isoformat(),
                        ),
                    ),
                    complete=False,
                    incomplete_reasons=("task-detail:task-expired",),
                )

            def list_correlated_cloud_writer_runs(
                self,
                pr_number: int,
                *,
                head_branch: str,
                tasks: tuple[AgentTaskLifecycle, ...],
                head_sha: str,
            ) -> list[WorkflowRun]:
                return []

        snapshot = PRStateSnapshot(
            pr_number=42,
            is_draft=False,
            ci_status="passing",
            review_state="",
            copilot_review_id=0,
            copilot_review_pending=False,
            base_repo_full_name="owner/repo",
            head_branch="copilot/pr-42",
            head_sha="a" * 40,
        )
        action = RequestReviewAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector._github_lifecycle_provider",
            return_value=ExpiredTaskProvider(),
        ):
            result = action.evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["no_active_session"] is True

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
        derived.set("repairable_threads", 0)
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

    def test_execute_when_review_targets_stale_head(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_pending=False,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="APPROVED",
                    commit_sha="stale-sha",
                )
            ],
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE

    def test_skip_when_review_targets_current_head(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_pending=False,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="APPROVED",
                    commit_sha="head-sha",
                )
            ],
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP

    def test_skip_when_commented_review_targets_head_without_repair_exhaustion(self) -> None:
        """A COMMENTED review on HEAD suppresses review requests so repairs can proceed."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_pending=False,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="COMMENTED",
                    commit_sha="head-sha",
                )
            ],
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_effective_review_on_head"] is False

    def test_skip_when_commented_review_has_clean_gate_verdict(self) -> None:
        """A clean gate verdict proves a COMMENTED review has no actionable feedback."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_pending=False,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=True,
                reason=REASON_CLEAN,
                review_id=100,
            ),
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="COMMENTED",
                    commit_sha="head-sha",
                )
            ],
        )
        derived = DerivedState(snapshot)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_effective_review_on_head"] is False

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
            head_sha="head-sha",
            is_draft=False,
            ci_status="pending",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_pending=False,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="APPROVED",
                    commit_sha="head-sha",
                )
            ],
        )
        derived = DerivedState(snapshot)
        derived.set("squash_preserved_green", True)
        action = RequestReviewAction()
        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "review exists" in result.details.lower()

    def test_execute_suppresses_request_when_diff_is_not_verified(self, verified_pr_provider: MagicMock) -> None:
        snapshot = PRStateSnapshot(pr_number=42)
        derived = DerivedState(snapshot)
        provider = verified_pr_provider
        provider.list_pr_files_complete.return_value = None
        action = RequestReviewAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        provider.request_reviewer.assert_not_called()

    def test_execute_sets_derived_pending(self, verified_pr_provider: MagicMock) -> None:
        """execute() must set derived.copilot_review_pending so downstream actions gate correctly."""
        snapshot = PRStateSnapshot(pr_number=42, copilot_review_pending=False)
        derived = DerivedState(snapshot)
        provider = verified_pr_provider
        action = RequestReviewAction()
        action.execute(provider, snapshot, derived)
        assert derived.copilot_review_pending is True
        # Snapshot itself must remain unchanged (frozen)
        assert snapshot.copilot_review_pending is False

    def test_execute_failed_when_provider_raises(self, verified_pr_provider: MagicMock) -> None:
        snapshot = PRStateSnapshot(pr_number=42)
        derived = DerivedState(snapshot)
        provider = verified_pr_provider
        provider.request_reviewer.side_effect = RuntimeError("request failed")
        action = RequestReviewAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "Failed to request Copilot review" in result.details

    def test_execute_reraises_rate_limit_when_provider_raises(self, verified_pr_provider: MagicMock) -> None:
        snapshot = PRStateSnapshot(pr_number=42)
        derived = DerivedState(snapshot)
        provider = verified_pr_provider
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
        head_sha: str = "",
        reviews: list[ReviewInfo] | None = None,
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
            head_sha=head_sha,
            reviews=reviews or [],
        )

    def test_skip_when_clean_review_carried_over_to_new_head(self) -> None:
        """A clean prior review the gate carried over must not trigger a new request."""
        verdict = CopilotGateVerdict(
            passed=True,
            reason=REASON_CLEAN,
            review_id=100,
            carried_over_sha=_PRIOR_SHA,
        )
        snapshot = self._snapshot(
            verdict,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="APPROVED",
                    commit_sha=_PRIOR_SHA,
                )
            ],
        )
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
        snapshot = self._snapshot(
            verdict,
            review_state="APPROVED",
            copilot_review_id=100,
            head_sha="head-sha",
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="APPROVED",
                    commit_sha="head-sha",
                )
            ],
        )
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
        ("review_user", "review_sha", "expected"),
        [
            ("copilot-swe-agent[bot]", "head-sha", ActionDecision.EXECUTE),
            ("Copilot", "head-sha", ActionDecision.EXECUTE),
            ("copilot[bot]", "head-sha", ActionDecision.EXECUTE),
            ("copilot-pull-request-reviewer[bot]", "", ActionDecision.EXECUTE),
            ("copilot-pull-request-reviewer[bot]", "stale-sha", ActionDecision.EXECUTE),
            ("copilot-pull-request-reviewer[bot]", "head-sha", ActionDecision.SKIP),
        ],
    )
    def test_current_review_requires_ccr_identity_and_exact_head(
        self,
        review_user: str,
        review_sha: str,
        expected: ActionDecision,
    ) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            reviews=[
                ReviewInfo(
                    id=99,
                    user="copilot-pull-request-reviewer[bot]",
                    state="CHANGES_REQUESTED",
                    commit_sha="stale-sha",
                ),
                ReviewInfo(id=100, user=review_user, state="COMMENTED", commit_sha=review_sha),
            ],
        )
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == expected
        assert result.preconditions["no_effective_review_on_head"] is (expected == ActionDecision.EXECUTE)

    @pytest.mark.parametrize(
        ("body", "review_sha", "expected"),
        [
            ("<!-- synthetic-copilot-review -->", "head-sha", ActionDecision.SKIP),
            ("", "head-sha", ActionDecision.EXECUTE),
            ("<!-- synthetic-copilot-review -->", "", ActionDecision.EXECUTE),
        ],
    )
    def test_trusted_synthetic_review_requires_marker_and_exact_head(
        self,
        body: str,
        review_sha: str,
        expected: ActionDecision,
    ) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            reviews=[
                ReviewInfo(
                    id=100,
                    user="AMARSNIK_swica",
                    state="COMMENTED",
                    body=body,
                    commit_sha=review_sha,
                )
            ],
        )
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == expected

    def test_untrusted_synthetic_review_does_not_suppress_request(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            reviews=[
                ReviewInfo(
                    id=100,
                    user="untrusted-user",
                    state="COMMENTED",
                    body="<!-- synthetic-copilot-review -->",
                    commit_sha="head-sha",
                )
            ],
        )
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE

    def test_current_copilot_review_and_verdict_review_threads_block_request(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            unresolved_threads=0,
            repairable_threads=1,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="CHANGES_REQUESTED",
                    commit_sha="head-sha",
                )
            ],
        )
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_unresolved_threads"] is False
        assert "no_effective_review_on_head" not in result.preconditions

    def test_thread_inventory_degradation_blocks_request(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            is_draft=False,
            ci_status="passing",
            unresolved_threads=0,
            repairable_threads=0,
            unresolved_threads_degraded=True,
        )
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_unresolved_threads"] is False

    def test_invalid_thread_inventory_blocks_request(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, is_draft=False, ci_status="passing")
        derived = DerivedState(snapshot)
        derived.set("repairable_threads", None)
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["thread_inventory_known"] is False

    def test_repair_escalation_blocks_request(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, is_draft=False, ci_status="passing")
        derived = DerivedState(snapshot)
        derived.set("repair_escalation_needed", True)
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_repair_escalation_needed"] is False

    def test_non_effective_review_state_does_not_suppress_request(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head-sha",
            is_draft=False,
            ci_status="passing",
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state="PENDING",
                    commit_sha="head-sha",
                )
            ],
        )
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE

    def test_non_ccr_cannot_carry_clean_verdict_over_to_head(self) -> None:
        verdict = CopilotGateVerdict(
            passed=True,
            reason=REASON_CLEAN,
            review_id=100,
            carried_over_sha=_PRIOR_SHA,
        )
        snapshot = self._snapshot(
            verdict,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-swe-agent[bot]",
                    state="APPROVED",
                    commit_sha=_PRIOR_SHA,
                )
            ],
        )
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["no_effective_review_on_head"] is True

    def test_trusted_synthetic_clean_review_can_be_carried_over(self) -> None:
        verdict = CopilotGateVerdict(
            passed=True,
            reason=REASON_CLEAN,
            review_id=100,
            carried_over_sha=_PRIOR_SHA,
        )
        snapshot = self._snapshot(
            verdict,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="AMARSNIK_swica",
                    state="APPROVED",
                    body="<!-- synthetic-copilot-review -->",
                    commit_sha=_PRIOR_SHA,
                )
            ],
        )
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_effective_review_on_head"] is False

    def test_unknown_carried_review_cannot_suppress_request(self) -> None:
        verdict = CopilotGateVerdict(
            passed=True,
            reason=REASON_CLEAN,
            review_id=100,
            carried_over_sha=_PRIOR_SHA,
        )
        snapshot = self._snapshot(verdict)
        with patch(_PATCH_DETECTOR, return_value=False):
            result = RequestReviewAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE

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

    @pytest.mark.parametrize("review_state", ["CHANGES_REQUESTED", "APPROVED", "COMMENTED"])
    def test_skip_when_repair_limit_reached_and_head_review_is_blocked(self, review_state: str) -> None:
        """A blocked CCR review on HEAD remains effective after repair exhaustion."""
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=100,
        )
        snapshot = self._snapshot(
            verdict,
            review_state=review_state,
            copilot_review_id=100,
            head_sha="head-sha",
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot-pull-request-reviewer[bot]",
                    state=review_state,
                    commit_sha="head-sha",
                )
            ],
        )
        derived = DerivedState(snapshot)
        derived.set("repair_limit_reached", True)
        action = RequestReviewAction()

        with patch(_PATCH_DETECTOR, return_value=False):
            result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["no_effective_review_on_head"] is False
