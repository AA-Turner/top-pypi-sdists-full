"""Request review action — requests Copilot review when needed."""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.models import COPILOT_REVIEWER_LOGIN
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)

_EFFECTIVE_REVIEW_STATES = {"APPROVED", "COMMENTED", "CHANGES_REQUESTED"}


class RequestReviewAction:
    """Request Copilot review when no effective review exists on HEAD.

    This action is the pipeline's explicit mechanism for requesting Copilot reviews.
    The pipeline does not rely on push events to trigger reviews — it requests them
    explicitly through this action.

    After a squash (which invalidates the snapshot), this action runs on the
    refreshed snapshot to request review on the new squashed HEAD. The
    ``runs_after_invalidation = True`` property enables this, and the pipeline
    runner refreshes the snapshot before re-evaluating. When that squash (or a
    rebase) left the PR diff unchanged and the gate verdict carried a **clean**
    prior-commit review over to the new HEAD, no new review is requested — the
    carried-over review already covers the identical diff.

    Preconditions:
    - PR is not draft (uses DerivedState)
    - Repair was not dispatched in this pipeline run
    - No unresolved review threads
    - CI is passing, OR a tree-preserving squash executed in this run
      (``squash_preserved_green``)
    - No effective Copilot review on HEAD, and no **passing** gate verdict that
      carried a prior-commit review over to HEAD (``carried_over_sha``)
    - Copilot not already requested as reviewer
    - No active Copilot coding session

    Idempotency: Review exists or pending → skip.
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
        repair_dispatched = getattr(derived, "repair_dispatched", False)
        preconditions["no_repair_dispatched"] = not repair_dispatched
        if repair_dispatched:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Repair dispatched — deferring review request",
            )

        # Guard: block review request when unresolved review threads exist
        unresolved = derived.unresolved_threads
        preconditions["no_unresolved_threads"] = unresolved == 0
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

        # Check if Copilot already has an effective review on HEAD.
        #
        # ``review_state``/``copilot_review_id`` are HEAD-filtered at snapshot-build
        # time, so a rebase or squash that moves HEAD without changing the diff drops
        # them even though the gate verdict already determined the prior review still
        # applies (identical diff content hash) and carried it over. Consult that
        # carry-over decision so a clean review is not re-requested for zero new
        # information.
        #
        # The carry-over skip is conditioned on BOTH the carry-over AND
        # ``gate_verdict.passed``. A carried-over *blocking* verdict must keep the
        # normal repair/review path open: DispatchRepairAction can be dedup- or
        # cycle-limited, and a fresh review id is exactly what resets its dedup key.
        # Skipping here on a blocking carry-over too would let approve/merge stay
        # gated forever with no action able to unstick them.
        gate_verdict = snapshot.copilot_gate_verdict
        carried_over_sha = gate_verdict.carried_over_sha if gate_verdict is not None and gate_verdict.passed else ""
        review_on_head = snapshot.review_state in _EFFECTIVE_REVIEW_STATES and snapshot.copilot_review_id > 0
        has_effective_review = review_on_head or bool(carried_over_sha)
        preconditions["no_effective_review_on_head"] = not has_effective_review
        if has_effective_review:
            if review_on_head:
                details = f"Copilot review exists on HEAD (state={snapshot.review_state})"
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
        active_session = is_copilot_session_active_via_agent_task(snapshot.base_repo_full_name, snapshot.pr_number)
        preconditions["no_active_session"] = not active_session
        if active_session:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Copilot session active — deferring review request",
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details="No Copilot review on HEAD — requesting",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Request Copilot as a reviewer."""
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
