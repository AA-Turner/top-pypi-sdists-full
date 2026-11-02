"""Approve action — auto-approves PR when conditions are met."""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.github_api_error import GitHubApiError
from agentic_devtools.cli.ci.pipeline.actions.approval_entry import approval_entry_guard, preflight_block
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    copilot_review_gate_passed,
    suppressed_deferral_recorded,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.snapshot_reviews import has_non_copilot_changes_requested_on_head
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


class ApproveAction:
    """Approve the PR when all conditions are met.

    Preconditions:
    - No effective non-Copilot CHANGES_REQUESTED review on HEAD
    - Copilot review is clean on HEAD
    - CI passing
    - No unresolved threads

    Idempotency: when ``snapshot.approver_login`` is known (``AGDT_PR_APPROVER_PAT``
    resolved via ``GET /user``), the evaluate step short-circuits when that exact
    identity has already approved the current HEAD (``has_approver_approval_on_head``).
    Providers supporting read-only preflight must establish every required capability
    before identity idempotency or approval submission. Unknown effective review
    eligibility blocks approval, even when identity and repository role are known.
    Providers without optional preflight retain their legacy login-only behavior.

    Idempotency uses the precise approver identity, not incidental human approvals,
    so an unrelated review cannot satisfy the loop's required approval.
    """

    @property
    def name(self) -> str:
        return "approve"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether approval should be submitted."""
        preconditions: dict[str, bool] = {}

        entry_result = approval_entry_guard(snapshot, derived)
        if entry_result is not None:
            return entry_result
        if derived.get("provider") is not None:
            preconditions["live_head_matches_snapshot"] = True

        loop_controller = derived.get("loop_controller")
        loop_state = derived.get("loop_state")
        loop_observation = derived.get("loop_observation")
        if loop_controller is not None or loop_state is not None or loop_observation is not None:
            if not all(value is not None for value in (loop_controller, loop_state, loop_observation)):
                preconditions["loop_eligible"] = False
                return ActionResult(self.name, ActionDecision.SKIP, preconditions, "Incomplete governed loop state")
            decision = loop_controller.approval_eligible(loop_state, snapshot.pr_number, loop_observation)
            preconditions["loop_eligible"] = decision.eligible
            if not decision.eligible:
                return ActionResult(self.name, ActionDecision.SKIP, preconditions, f"Loop gate: {decision.reason}")

        if snapshot.approver_login and snapshot.author_login:
            preconditions["approver_is_not_author"] = (
                snapshot.approver_login.casefold() != snapshot.author_login.casefold()
            )
            if not preconditions["approver_is_not_author"]:
                return ActionResult(self.name, ActionDecision.SKIP, preconditions, "Approver is the PR author")

        repair_dispatched = derived.get("repair_dispatched", False)
        preconditions["no_repair_dispatched"] = not repair_dispatched
        if repair_dispatched:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Repair dispatched — deferring approval",
            )

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
                details="Copilot session active or inventory unavailable — approval blocked",
            )

        # Precise idempotency guard: skip only when the approver-PAT identity
        # (resolved at snapshot-build time via GET /user) has already approved the
        # current HEAD. Optional preflight has already blocked unknown capabilities.
        # Legacy providers without preflight retain the login-only path.
        if derived.has_approver_approval_on_head:
            preconditions["no_approver_approval_on_head"] = False
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Already approved by loop approver on current HEAD (idempotent)",
            )

        # No non-Copilot CHANGES_REQUESTED on HEAD
        has_human_changes_requested = has_non_copilot_changes_requested_on_head(snapshot.reviews, snapshot.head_sha)
        preconditions["no_human_changes_requested"] = not has_human_changes_requested
        if has_human_changes_requested:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="Non-Copilot reviewer requested changes on current HEAD",
            )

        # CI passing
        preconditions["ci_passing"] = snapshot.ci_status == "passing"
        if snapshot.ci_status != "passing":
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"CI is {snapshot.ci_status}",
            )

        # Shared gate predicate: this is the single source of truth used by squash too.
        # It handles the verdict path (including the fail-closed suppressed-only bypass)
        # and legacy fallback when no verdict is available.
        deferred_review_id = derived.get("suppressed_deferral_review_id")
        review_clean = copilot_review_gate_passed(
            snapshot,
            unresolved_threads=derived.unresolved_threads,
            deferred_review_id=deferred_review_id if isinstance(deferred_review_id, int) else None,
        )
        gate_verdict = snapshot.copilot_gate_verdict
        if gate_verdict is not None:
            preconditions["gate_verdict_passed"] = gate_verdict.passed
            if not gate_verdict.passed:
                deferral_cleared = suppressed_deferral_recorded(
                    gate_verdict,
                    deferred_review_id=deferred_review_id if isinstance(deferred_review_id, int) else None,
                    head_changed_since_review=snapshot.head_changed_since_review,
                    unresolved_threads=derived.unresolved_threads,
                )
                preconditions["suppressed_deferral_recorded"] = deferral_cleared
                preconditions["suppressed_comments_evaluated"] = review_clean and not deferral_cleared
                if review_clean:
                    logger.info(
                        "PR #%d: Suppressed-only gate block cleared by %s (review %d) — proceeding with approval",
                        snapshot.pr_number,
                        "suppressed-comment deferral" if deferral_cleared else "repair-satisfied marker",
                        gate_verdict.review_id,
                    )
        else:
            preconditions["review_clean"] = review_clean

        if not review_clean:
            if gate_verdict is not None:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.SKIP,
                    preconditions=preconditions,
                    details=f"Copilot gate: {gate_verdict.reason} — {gate_verdict.details}",
                )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=(
                    f"Copilot review is not clean "
                    f"(state={snapshot.review_state}, inline={snapshot.copilot_review_inline_count})"
                ),
            )

        # No unresolved threads — consult derived state so same-run ResolveThreadsAction
        # effects are visible (avoids a second workflow trigger after thread resolution).
        unresolved = derived.unresolved_threads
        preconditions["no_unresolved_threads"] = unresolved == 0
        if unresolved > 0:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=f"{unresolved} unresolved thread(s)",
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details="All conditions met for approval",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Submit PR approval."""
        blocked = preflight_block(snapshot.approver_preflight)
        if blocked is not None:
            return blocked
        try:
            live_head_sha = provider.get_pr_metadata(snapshot.pr_number).head_sha
            if live_head_sha != snapshot.head_sha:
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.SKIP,
                    details="Live head SHA diverged before approval",
                )
            approved = provider.approve_pr(
                snapshot.pr_number,
                snapshot.head_sha,
                "Auto-approved by AI PR loop",
            )
        except GitHubApiError as exc:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                details="Review submission rejected",
                capability="review_submission",
                http_status=exc.http_status,
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.error("PR #%d: Approval failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="approve_pr call failed",
            )

        if not approved:
            logger.warning("PR #%d: Approval was skipped by provider", snapshot.pr_number)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions={"approver_token_available": False},  # nosec B105 - approval-state flag, not a secret
                details="Provider skipped approval (missing approver token?)",
            )

        logger.info("PR #%d: Approved", snapshot.pr_number)
        # Record both the generic approval flag and the precise approver-PAT signal
        # so a same-run MergeAction sees the loop's approval on HEAD.
        derived.set("has_approval_on_head", True)
        derived.set("has_approver_approval_on_head", True)

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details="PR approved",
        )
