"""Request review action — requests Copilot review when needed."""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.models import COPILOT_REVIEWER_LOGIN, ReviewInfo
from agentic_devtools.cli.ci.pipeline.delivery import has_verified_non_empty_pr_diff
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_CLEAN,
    SYNTHETIC_MARKER,
    TRUSTED_SYNTHETIC_USERS,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)

_EFFECTIVE_REVIEW_STATES = {"APPROVED", "CHANGES_REQUESTED", "COMMENTED"}
_TRUSTED_SYNTHETIC_USERS_CASEFOLDED = frozenset(user.casefold() for user in TRUSTED_SYNTHETIC_USERS)


class RequestReviewAction:
    """Request Copilot review when no eligible review exists on HEAD.

    After snapshot invalidation, the runner refreshes the snapshot. A clean
    carried-over review still suppresses duplicate requests.

    Preconditions:
    - PR is not draft; no repair dispatch, cycle limit, or repair escalation.
    - Thread inventory is known and no actionable threads remain.
    - CI passes or a same-run tree-preserving squash preserved green checks.
    - No effective or carried-over clean review, pending request, or active session.
    - Fresh PR diff evidence is non-empty.

    Idempotency: existing or pending review → skip.
    """

    @property
    def name(self) -> str:
        return "request_review"

    @property
    def runs_after_invalidation(self) -> bool:
        return True

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether Copilot review should be requested."""
        preconditions: dict[str, bool] = {}

        # Must not be draft
        is_draft = derived.is_draft
        preconditions["not_draft"] = not is_draft
        if is_draft:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="PR is a draft",
            )

        # Guard: never request review when repair was just dispatched
        repair_dispatched = derived.get("repair_dispatched", False)
        repair_limit_reached = derived.get("repair_limit_reached", False)
        preconditions["no_repair_dispatched"] = not repair_dispatched or repair_limit_reached
        if repair_dispatched and not repair_limit_reached:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Repair dispatched — deferring review request",
            )
        if derived.get("cycle_limit_reached", False):
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Repair cycle limit reached — human intervention required",
            )

        if derived.get("repair_escalation_needed", False):
            preconditions["no_repair_escalation_needed"] = False
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Repair deduplication limit exhausted with actionable work — human attention required",
            )

        # Review requests are suppressed by every actionable thread, including
        # threads owned by the gate verdict's review. Keep the gate-specific
        # unresolved count unchanged for approval and merge decisions.
        unresolved = derived.get("repairable_threads", snapshot.repairable_threads)
        thread_inventory_degraded = derived.get("unresolved_threads_degraded", snapshot.unresolved_threads_degraded)
        thread_inventory_known = not thread_inventory_degraded and type(unresolved) is int and unresolved >= 0
        preconditions["thread_inventory_known"] = thread_inventory_known
        preconditions["no_unresolved_threads"] = thread_inventory_known and unresolved == 0
        if not thread_inventory_known:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Actionable review-thread inventory is unknown — review request blocked",
            )
        if unresolved > 0:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"{unresolved} unresolved thread(s) — deferring review request",
            )

        # CI must be passing before requesting review.
        #
        # Relaxation (latency optimization): SquashAction sets the run-scoped
        # ``squash_preserved_green`` derived flag when a tree-preserving squash executed
        # in this run after green CI. In that case the pre-squash green result still
        # applies to the identical post-squash tree, so a review may be requested on the
        # new squashed HEAD without waiting for its checks to re-report. Requesting a
        # review is a non-gating side effect; ApproveAction and MergeAction keep their
        # own independent ``ci_passing`` gate on the real HEAD and are structurally
        # halted in the same run as a squash, so this can never approve or merge against
        # unreported checks. Every other request-review gate stays unchanged.
        squash_preserved_green = derived.get("squash_preserved_green", False)
        ci_passing = snapshot.ci_status == "passing" or squash_preserved_green
        preconditions["ci_passing"] = ci_passing
        if not ci_passing:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"CI is {snapshot.ci_status} — deferring review request",
            )

        # Only an exact current-HEAD CCR review (or trusted synthetic CCR review)
        # satisfies review-request idempotency. The generic Copilot snapshot
        # selection also includes coding-agent reviews and is not authoritative here.
        current_head_review = next(
            (review for review in snapshot.reviews if self._is_eligible_review(review, snapshot.head_sha)),
            None,
        )
        review_on_head = current_head_review is not None

        # A clean diff-equivalent carry-over is valid only when its source review
        # is present and has eligible CCR provenance.
        gate_verdict = snapshot.copilot_gate_verdict
        carried_over_sha = ""
        if (
            gate_verdict is not None
            and gate_verdict.passed
            and gate_verdict.reason == REASON_CLEAN
            and gate_verdict.carried_over_sha
            and gate_verdict.review_id > 0
        ):
            source_review = next(
                (review for review in snapshot.reviews if review.id == gate_verdict.review_id),
                None,
            )
            if source_review is not None and self._is_eligible_review(source_review, gate_verdict.carried_over_sha):
                carried_over_sha = gate_verdict.carried_over_sha
        has_effective_review = review_on_head or bool(carried_over_sha)
        preconditions["no_effective_review_on_head"] = not has_effective_review
        if has_effective_review:
            if review_on_head:
                assert current_head_review is not None
                details = f"CCR review exists on HEAD (state={current_head_review.state})"
            else:
                details = (
                    f"Clean Copilot review from {carried_over_sha[:12]} still applies "
                    "(PR diff unchanged) — no new review needed"
                )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=details,
            )

        # Check if Copilot is already requested
        copilot_already_requested = derived.copilot_review_pending
        preconditions["not_already_requested"] = not copilot_already_requested
        if copilot_already_requested:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Copilot review already requested",
            )

        # Guard: never request review when active coding session is in progress
        active_session = is_copilot_session_active_via_agent_task(
            snapshot.base_repo_full_name,
            snapshot.pr_number,
            head_branch=snapshot.head_branch,
            pr_id=snapshot.pr_id,
            head_sha=snapshot.head_sha,
            provider=derived.get("provider"),
        )
        preconditions["no_active_session"] = active_session is False
        if active_session is not False:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Copilot session active or inventory unavailable — review request blocked",
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details="No eligible CCR review on HEAD — requesting",
        )

    @staticmethod
    def _is_eligible_review(review: ReviewInfo, target_sha: str) -> bool:
        """Whether a review has trusted CCR provenance and targets ``target_sha``."""
        if review.state not in _EFFECTIVE_REVIEW_STATES or not review.commit_sha or review.commit_sha != target_sha:
            return False
        reviewer = review.user.casefold()
        return reviewer == COPILOT_REVIEWER_LOGIN.casefold() or (
            reviewer in _TRUSTED_SYNTHETIC_USERS_CASEFOLDED and SYNTHETIC_MARKER in review.body
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Request Copilot as a reviewer."""
        if not has_verified_non_empty_pr_diff(provider, snapshot.pr_number):
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="PR diff is empty or unknown — Copilot review request blocked",
            )

        try:
            provider.request_reviewer(snapshot.pr_number, COPILOT_REVIEWER_LOGIN)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning("PR #%d: Failed to request Copilot review: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="Failed to request Copilot review",
            )

        logger.info("PR #%d: Copilot review requested", snapshot.pr_number)
        derived.set("copilot_review_pending", True)
        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details="Copilot review requested",
        )
