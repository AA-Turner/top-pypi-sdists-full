"""Resolve threads action — resolves review threads not owned by the gate verdict."""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot import (
    DerivedState,
    PRStateSnapshot,
    count_unresolved_prior_threads,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)


class ResolveThreadsAction:
    """Resolve unresolved Copilot review threads not owned by the gate verdict.

    Preconditions:
    - Unresolved threads exist from reviews not owned by the gate verdict

    Thread resolution is independent of CI status and pending review state.
    Whether a code change addresses a review comment is logically independent
    of whether CI passes or whether a new review has been requested.

    Idempotency: Already-resolved threads are skipped (per-thread).
    """

    @property
    def name(self) -> str:
        return "resolve_threads"

    @property
    def runs_after_invalidation(self) -> bool:
        return True

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether thread resolution should be attempted."""
        preconditions: dict[str, bool] = {}

        # Unresolved threads exist
        has_threads = snapshot.unresolved_threads > 0
        preconditions["has_unresolved_threads"] = has_threads
        if not has_threads:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="No unresolved threads from reviews not owned by the gate verdict",
            )

        # Skip SDK evaluation when autofix just ran in THIS iteration but no
        # repair has been dispatched. The remaining threads haven't been
        # addressed by any code change — evaluating them wastes tokens.
        autofix_just_ran = derived.get("autofix_applied_this_iteration", False)
        repair_dispatched = derived.get("repair_dispatched", False)
        if autofix_just_ran and not repair_dispatched:
            preconditions["autofix_without_repair"] = True
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=(
                    "Skipping thread evaluation — autofix just applied but no "
                    "repair dispatched yet; remaining threads have not been addressed"
                ),
            )

        # Skip evaluation when CI is pending/unknown AND no repair has been
        # dispatched. If CI hasn't completed, the repair agent hasn't run
        # yet, so non-autofixed threads can't have been addressed.
        # This prevents token waste on subsequent iterations where CI is
        # still running after an autofix commit.
        ci_status = snapshot.ci_status
        ci_actionable = ci_status in ("passing", "failing")
        if not ci_actionable and not repair_dispatched:
            preconditions["ci_not_actionable"] = True
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=(
                    f"Skipping thread evaluation — CI is '{ci_status}' and no "
                    "repair dispatched; threads cannot have been addressed yet"
                ),
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details=f"{snapshot.unresolved_threads} unresolved thread(s) not owned by the gate verdict",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Execute thread resolution via finalize_post_repair.

        Delegates to the provider's finalize_post_repair which handles
        SDK verification and per-thread resolve/keep-open decisions.
        """
        # Find actionable Copilot or trusted synthetic reviews not already owned by
        # the gate verdict (provenance scoped to the verdict's review_id, not HEAD's
        # commit SHA, so squash/takeover cannot change this selection).
        from agentic_devtools.cli.ci.pipeline.gate_verdict import select_prior_actionable_reviews

        verdict = snapshot.copilot_gate_verdict
        verdict_review_id = verdict.review_id if verdict is not None and verdict.review_id > 0 else None
        prior_reviews = select_prior_actionable_reviews(snapshot.reviews, verdict_review_id)

        if not prior_reviews:
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="No prior Copilot or synthetic reviews found (race condition)",
            )

        prior_reviews.sort(key=lambda r: r.id, reverse=True)
        resolved = 0
        unresolved = 0
        suppressed = 0
        skipped_reviews: list[str] = []
        finalization_errors: list[str] = []
        hard_failures: list[tuple[int, str]] = []

        for prior_review in prior_reviews:
            try:
                result = provider.finalize_post_repair(
                    pr_number=snapshot.pr_number,
                    base_branch=snapshot.base_branch,
                    head_branch=snapshot.head_branch,
                    head_sha=snapshot.head_sha,
                    review_id=prior_review.id,
                )
            except Exception as exc:
                if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                    raise
                logger.error(
                    "PR #%d: Thread resolution failed for review %s: %s", snapshot.pr_number, prior_review.id, exc
                )
                hard_failures.append((prior_review.id, str(exc)))
                continue

            finalization_errors.extend(result.errors)

            if result.skipped or result.reason == "no_comments":
                skipped_reviews.append(f"#{prior_review.id}:{result.reason or 'unknown'}")
                continue

            resolved += result.resolved_count
            unresolved += result.unresolved_count
            suppressed += result.suppressed_count

        if len(hard_failures) == len(prior_reviews):
            failure_msgs = [f"#{rid}: {err}" for rid, err in hard_failures]
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error="; ".join(failure_msgs),
                details=f"All {len(prior_reviews)} prior reviews failed finalization: {', '.join(failure_msgs)}",
            )

        # Update derived state so downstream actions (approve, merge) see the
        # post-resolution count within the same pipeline run.
        #
        # The per-review counts returned by finalize_post_repair() are NOT a
        # count over the same domain as snapshot.unresolved_threads: they are
        # summed across reviews without cross-review de-duplication.
        # Combining the two produced a monotonically growing phantom count.
        # Instead, re-query the authoritative post-resolution count from the
        # same source the snapshot uses. The provider's thread-signals cache is
        # invalidated by the resolve/unresolve mutations, so this observes the
        # post-resolution state.
        requeried_blocking, requeried_repairable, degraded, unknown_provenance = count_unresolved_prior_threads(
            provider,
            snapshot.pr_number,
            snapshot.reviews,
            verdict_review_id,
            verdict=verdict,
        )
        if degraded:
            # Thread state is unavailable — fail closed with the conservative
            # pre-re-query estimate and the helper's degraded sentinel rather
            # than trusting an unknown count.
            unresolved_total = max(requeried_blocking, unresolved, snapshot.unresolved_threads - resolved, 0)
            # ``resolved`` is a per-review aggregate and can double-count the same
            # underlying thread across reviews. Preserve the previously measured
            # repairable inventory when re-query is degraded instead of subtracting
            # this non-deduplicated value.
            repairable_total = max(requeried_repairable, snapshot.repairable_threads, 0)
        else:
            unresolved_total = requeried_blocking
            repairable_total = requeried_repairable

        derived.set("unresolved_threads", unresolved_total)
        derived.set("repairable_threads", repairable_total)
        # Propagate the re-query's degraded and unknown_provenance status so downstream
        # actions (approve, merge) know whether the thread count is authoritative.
        # A failed re-query after a healthy snapshot must mark state as degraded
        # (not leave the snapshot's False in place); a successful re-query
        # replaces whatever the snapshot held.
        derived.set("unresolved_threads_degraded", degraded)
        derived.set("unresolved_threads_unknown_provenance", unknown_provenance)

        details = f"Resolved {resolved} thread(s), {unresolved_total} left open"
        if suppressed:
            # Informational only: synthetic suppressed entries have no thread and
            # never contribute to the blocking count.
            details = f"{details}; {suppressed} suppressed comment(s) not counted"
        if skipped_reviews:
            details = f"{details}; skipped {len(skipped_reviews)} prior review(s): {', '.join(skipped_reviews)}"
        if hard_failures:
            failure_msgs = [f"#{rid}: {err}" for rid, err in hard_failures]
            details = f"{details}; hard failures: {', '.join(failure_msgs)}"
        if finalization_errors:
            details = f"{details}; finalization errors: {', '.join(finalization_errors)}"

        # Log the same rendered text that lands in the PR comment so the Actions
        # log and the comment can be cross-read without translation.
        logger.info(
            "PR #%d: %s (%d prior review(s))",
            snapshot.pr_number,
            details,
            len(prior_reviews),
        )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details=details,
        )
