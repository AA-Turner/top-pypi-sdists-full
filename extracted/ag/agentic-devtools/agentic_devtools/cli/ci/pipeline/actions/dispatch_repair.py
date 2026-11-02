"""Dispatch repair action — triggers AI repair on CI failure or actionable review."""

from __future__ import annotations

import logging
import re

from agentic_devtools.cli.ci.guards import (
    check_cycle_limit,
    check_deduplication,
    is_duplicate_trigger,
)
from agentic_devtools.cli.ci.models import (
    ReviewCommentInfo,
    ReviewInfo,
    is_cloud_coding_agent_login,
)
from agentic_devtools.cli.ci.pipeline.actions import critique_dispatch, critique_task_binding
from agentic_devtools.cli.ci.pipeline.deferral import read_active_suppressed_deferral
from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    REASON_UNPARSED_SUPPRESSION,
    is_copilot_or_synthetic_review,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.repair_attempts import RepairAttemptTracker
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.snapshot_thread_count import REPAIRABLE_REVIEW_STATES
from agentic_devtools.cli.ci.provider import (
    CIPlatformProvider,
    RepairDispatchBookkeepingRateLimitError,
    RepairDispatchNotAttemptedError,
)
from agentic_devtools.cli.ci.repair_accounting import (
    RepairDispatchLedger,
    repair_hold_observation_key,
    repair_observation_key,
    repair_work_key,
)
from agentic_devtools.cli.github import ccr_review_format
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)

#: Body verdicts, posted/suppressed feedback, and unparsed suppression are repairable;
#: freshness-only reasons require a new review.
_CONTENT_BLOCKING_GATE_REASONS: frozenset[str] = frozenset(
    {
        REASON_HAS_COMMENTS,
        REASON_SUPPRESSED_COMMENTS,
        REASON_NEW_CCR_NOT_APPROVED,
        REASON_UNPARSED_SUPPRESSION,
    }
)


def _raise_if_rate_limit(exc: Exception) -> None:
    """Re-raise provider rate-limit errors so caller can persist cooldown and pause."""
    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
        raise


def _actionable_copilot_review_id(snapshot: PRStateSnapshot) -> int:
    """Return the actionable Copilot review id, or ``0`` when none needs repair.

    Candidates are current-head changes requests, ``COMMENTED`` reviews with inline
    comments, or content-blocking body verdicts tied to their evaluated review.
    Freshness-only verdicts require a new review, not repair.
    """
    critique = critique_dispatch.critique_headline(snapshot)
    if critique is not None:
        return critique[0]
    if snapshot.review_state == "CHANGES_REQUESTED" and snapshot.copilot_review_id > 0:
        return snapshot.copilot_review_id
    if (
        snapshot.review_state == "COMMENTED"
        and snapshot.copilot_review_id > 0
        and snapshot.copilot_review_inline_count != 0
    ):
        return snapshot.copilot_review_id
    verdict = snapshot.copilot_gate_verdict
    if (
        verdict is not None
        and not verdict.passed
        and verdict.reason in _CONTENT_BLOCKING_GATE_REASONS
        and verdict.review_id > 0
    ):
        return critique_dispatch.actionable_review_id(snapshot, verdict.review_id)
    return 0


def _has_effective_review_work(snapshot: PRStateSnapshot, actionable_review_id: int) -> bool:
    """Return whether an actionable review still has work after state filtering."""
    if actionable_review_id <= 0:
        return False
    if snapshot.effective_review_comment_count is None:
        return True
    if snapshot.effective_review_comment_count_review_id != actionable_review_id:
        return True
    if snapshot.effective_review_comment_count > 0:
        return True
    critique = critique_dispatch.critique_headline(snapshot)
    if critique is not None and critique[0] == actionable_review_id:
        return True
    verdict = snapshot.copilot_gate_verdict
    # A new-CCR body with no known posted comments may carry feedback that is not
    # represented by inline comments. Keep that case fail-open; a positive posted
    # count is safe to skip only when filtering definitely removed fetched comments.
    if verdict is not None and verdict.reason in {REASON_HAS_COMMENTS, REASON_NEW_CCR_NOT_APPROVED}:
        if verdict.body_comment_count in {None, 0}:
            return True
        return snapshot.effective_review_comment_filter_applied is not True
    return bool(verdict is not None and verdict.reason in {REASON_SUPPRESSED_COMMENTS, REASON_UNPARSED_SUPPRESSION})


def _list_repairable_copilot_reviews(snapshot: PRStateSnapshot) -> list[ReviewInfo]:
    """Return Copilot/synthetic reviews that can own repairable unresolved threads."""
    return [
        review
        for review in snapshot.reviews
        if is_copilot_or_synthetic_review(review) and review.state in REPAIRABLE_REVIEW_STATES
    ]


def _declared_suppressed_counts_by_review(snapshot: PRStateSnapshot, review_ids: list[int]) -> dict[int, int]:
    """Return declared suppressed-comment counts per review, excluding reviews with zero count.

    Args:
        snapshot: PR state snapshot carrying the review bodies.
        review_ids: Reviews whose comments this dispatch carries.

    Returns:
        Mapping from review id to its declared count. Reviews that declare zero (or
        whose body is absent) are omitted.
    """
    bodies = {review.id: review.body for review in snapshot.reviews}
    return {
        review_id: declared_count
        for review_id in review_ids
        if (declared_count := ccr_review_format.parse_suppressed_count(bodies.get(review_id, ""))) > 0
    }


def _recovered_suppressed_occurrences(review_id: int, comments: list[ReviewCommentInfo], review_body: str) -> set[int]:
    """Account for suppression replaced by provider-authenticated native roots.

    Native roots need the originating review metadata and terminal suppression
    marker; neither a positive ID nor API minimization proves this origin.
    Explicitly resolved body entries can be omitted by the provider altogether.
    Use occurrence ordinals to avoid counting both a synthetic and its promotion.
    """
    findings = ccr_review_format.extract_ccr_findings(review_body, source_review_id=review_id).findings
    occurrences = {
        finding.ordinal
        for finding in findings
        if finding.section == "suppressed"
        and finding.explicitly_resolved
        # Match the provider's exclusion of parser echoes of structured entries.
        and not (
            finding.path == ccr_review_format.UNKNOWN_FILE
            and "\n" not in finding.body
            and any(
                other.section == "suppressed"
                and other.path != ccr_review_format.UNKNOWN_FILE
                and finding.body != other.body
                and finding.body in other.body
                for other in findings
            )
        )
    }
    marker_pattern = re.compile(rf"<!-- ccr-promoted:{review_id}:suppressed:([1-9]\d*) -->")
    for comment in comments:
        if comment.id < 0:
            occurrences.add(-comment.id)
        elif comment.source_review_id == review_id and comment.in_reply_to_id is None:
            lines = comment.body.rstrip().splitlines()
            if lines and (match := marker_pattern.fullmatch(lines[-1])):
                occurrences.add(int(match[1]))
    return occurrences


def _has_stuck_prior_review_threads(snapshot: PRStateSnapshot) -> bool:
    """Return True when unresolved repairable review threads should trigger repair."""
    return (
        snapshot.ci_status == "passing"
        and snapshot.repairable_threads > 0
        and bool(_list_repairable_copilot_reviews(snapshot))
    )


def _filter_repair_comments(
    comments: list[ReviewCommentInfo],
    resolved_comment_ids: set[int] | None = None,
) -> list[ReviewCommentInfo]:
    """Return eligible original findings and synthetic suppressed entries.

    Cloud Coding Agent replies are valid only when their positive parent ID is
    present in this same review's comment collection. Thread state is optional:
    when unavailable, roots are retained so dispatch remains fail-open.
    """
    # Root IDs: only comments that are themselves top-level (no parent).
    # Using all positive IDs would let a nested CCA reply point to another
    # reply and suppress it as an "answered root".
    root_ids = {
        comment.id
        for comment in comments
        if type(comment.id) is int and comment.id > 0 and comment.in_reply_to_id is None
    }

    # All Cloud Coding Agent replies with a valid *root* parent — these are never emitted.
    all_reply_ids = {
        comment.id
        for comment in comments
        if (
            type(comment.id) is int
            and comment.id > 0
            and is_cloud_coding_agent_login(comment.author_login)
            and type(comment.in_reply_to_id) is int
            and comment.in_reply_to_id > 0
            and comment.in_reply_to_id in root_ids
        )
    }

    # Roots answered by a non-empty Cloud Coding Agent reply are suppressed.
    # Body validity decides root suppression; it does not control reply removal.
    response_parent_ids = {
        comment.in_reply_to_id
        for comment in comments
        if (comment.id in all_reply_ids and isinstance(comment.body, str) and bool(comment.body.strip()))
    }

    filtered: list[ReviewCommentInfo] = []
    for comment in comments:
        if type(comment.id) is int and comment.id > 0 and comment.id in all_reply_ids:
            continue
        if type(comment.id) is int and comment.id > 0 and comment.id in response_parent_ids:
            continue
        if (
            resolved_comment_ids is not None
            and type(comment.id) is int
            and comment.id > 0
            and comment.id in resolved_comment_ids
        ):
            continue
        filtered.append(comment)
    return filtered


class DispatchRepairAction:
    """Dispatch a repair when CI fails or actionable review feedback exists.

    Preconditions:
    - CI failed OR actionable Copilot review on HEAD
      OR stuck unresolved threads from prior Copilot review(s)
    - Deduplication limit not exceeded
    - Cycle limit not exceeded

    Idempotency: Durable finding/HEAD reservation → skip and escalate if unresolved.
    """

    runs_after_invalidation = True
    runs_on_prior_failure: bool = True

    @property
    def name(self) -> str:
        return "dispatch_repair"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether repair dispatch is needed."""
        if derived.get("repair_dispatched", False):
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="Repair already dispatched in this derived state",
            )
        preconditions: dict[str, bool] = {}

        # CI failed OR actionable review OR unresolved prior-review threads are stuck
        ci_failing = snapshot.ci_status == "failing"
        actionable_review_id = _actionable_copilot_review_id(snapshot)
        review_actionable_raw = actionable_review_id > 0
        review_actionable = _has_effective_review_work(snapshot, actionable_review_id)
        effective_review_work = review_actionable
        stuck_prior_threads = _has_stuck_prior_review_threads(snapshot)
        needs_repair = ci_failing or review_actionable or stuck_prior_threads
        preconditions["ci_failing"] = ci_failing
        preconditions["review_actionable"] = review_actionable_raw
        preconditions["effective_review_work"] = effective_review_work
        preconditions["stuck_prior_threads"] = stuck_prior_threads
        preconditions["needs_repair"] = needs_repair
        if not needs_repair:
            if review_actionable_raw and not effective_review_work:
                details = (
                    "No effective review work remains "
                    f"(effective_review_comment_count={snapshot.effective_review_comment_count}, CI passing)"
                )
            else:
                critique_dispatch.log_noncritique_overview(snapshot)
                details = (
                    "No repair needed "
                    f"(ci_status={snapshot.ci_status}, review_actionable={review_actionable}, "
                    f"stuck_prior_threads={stuck_prior_threads})"
                )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details=details,
            )

        if snapshot.ci_status == "pending":
            preconditions["ci_not_pending"] = False
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="CI still pending — waiting",
            )
        preconditions["ci_not_pending"] = True

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
                details="Copilot session active or inventory unavailable — repair dispatch blocked",
            )

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details=(
                f"Repair candidate (ci_failing={ci_failing}, review_actionable={review_actionable}); "
                "durable attempt eligibility checked during execution"
            ),
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Fail closed on missing dedup, finding or required thread evidence."""
        try:
            return self._execute(provider, snapshot, derived)
        except Exception as exc:
            _raise_if_rate_limit(exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="Repair reservation or required evidence failed",
            )

    def _execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Dispatch repair by posting @copilot comment."""
        skip_result = critique_dispatch.zero_findings_repair_skip(
            self.name, snapshot, _has_stuck_prior_review_threads(snapshot)
        )
        if skip_result is not None:
            return skip_result
        actionable_review_id = _actionable_copilot_review_id(snapshot)
        review_actionable_raw = actionable_review_id > 0
        review_actionable = _has_effective_review_work(snapshot, actionable_review_id)
        stuck_prior_threads = _has_stuck_prior_review_threads(snapshot)
        if (
            snapshot.ci_status == "passing"
            and review_actionable_raw
            and not review_actionable
            and not stuck_prior_threads
        ):
            logger.info(
                "PR #%d: No effective review work remains (effective_review_comment_count=%s) — skipping repair",
                snapshot.pr_number,
                snapshot.effective_review_comment_count,
            )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details=(
                    "No effective review work remains "
                    f"(effective_review_comment_count={snapshot.effective_review_comment_count}, CI passing)"
                ),
            )

        # Check for active deferral marker — if apply_suggestions posted one,
        # skip dispatch to give the autofix path another chance next iteration.
        if snapshot.copilot_review_id > 0:
            try:
                from agentic_devtools.cli.ci.pipeline.deferral import (
                    deactivate_deferral_marker,
                    read_active_deferral,
                )

                active_deferral = read_active_deferral(provider, snapshot.pr_number, snapshot.copilot_review_id)
                if active_deferral is not None:
                    # Deactivate marker after consuming it. If that fails,
                    # proceed with repair dispatch to avoid leaving the PR in
                    # a permanent skip loop behind an active marker.
                    if deactivate_deferral_marker(
                        provider,
                        snapshot.pr_number,
                        snapshot.copilot_review_id,
                    ):
                        logger.info(
                            "PR #%d: Active autofix deferral marker found for review %d — "
                            "skipping dispatch to allow autofix retry",
                            snapshot.pr_number,
                            snapshot.copilot_review_id,
                        )
                        return ActionResult(
                            name=self.name,
                            decision=ActionDecision.SKIP,
                            details="Deferred: active autofix deferral marker consumed",
                        )
                    logger.warning(
                        "PR #%d: Active autofix deferral marker for review %d could not be deactivated; "
                        "proceeding with repair dispatch",
                        snapshot.pr_number,
                        snapshot.copilot_review_id,
                    )
            except Exception as exc:
                _raise_if_rate_limit(exc)
                logger.warning(
                    "PR #%d: Deferral check failed (proceeding with dispatch): %s",
                    snapshot.pr_number,
                    exc,
                )

        repairable_reviews = _list_repairable_copilot_reviews(snapshot)
        repairable_reviews.sort(
            key=lambda r: (
                r.submitted_at if isinstance(r.submitted_at, str) else "",
                r.id,
            ),
            reverse=True,
        )
        attempts = RepairAttemptTracker(provider, snapshot.pr_number, snapshot.head_sha)
        candidate_ids = [r.id for r in repairable_reviews] if stuck_prior_threads else []
        if review_actionable and actionable_review_id not in candidate_ids:
            candidate_ids.append(actionable_review_id)
        review_comments: list[ReviewCommentInfo] = []
        declared_author_comment_counts_by_review: dict[int, int] = {}
        pending_attempts: set[str] = set()
        resolved_ids = attempts.resolved_ids() if candidate_ids else set()
        exclusion_ctx: ExclusionContext | None = derived.get("exclusion_context")
        if exclusion_ctx:
            resolved_ids |= exclusion_ctx.resolved_comment_ids
        raw_declared_counts = _declared_suppressed_counts_by_review(snapshot, candidate_ids)
        review_bodies = {review.id: review.body for review in snapshot.reviews}
        review_context_id = 0
        seen_keys: set[str] = set()
        exhaustion_review_context_id = 0
        exhaustion_review_comments: list[ReviewCommentInfo] = []
        exhaustion_author_comment_counts_by_review: dict[int, int] = {}
        comments_by_review = {
            review_id: provider.list_review_comments(snapshot.pr_number, review_id) for review_id in candidate_ids
        }
        has_identified_findings = any(
            attempts.finding_key(review_id, comment) is not None
            for review_id, comments in comments_by_review.items()
            for comment in comments
        )
        for review_id in candidate_ids:
            raw_comments = comments_by_review[review_id]
            unresolved_comments = _filter_repair_comments(raw_comments, resolved_ids)
            unresolved_review_keys = {
                key for comment in unresolved_comments if (key := attempts.finding_key(review_id, comment)) is not None
            }
            comments = attempts.filter_review(review_id, raw_comments, resolved_ids)
            finding_aware = any(attempts.finding_key(review_id, c) is not None for c in raw_comments)
            eligible_comments = _filter_repair_comments(comments, resolved_ids)
            review_keys = {key for c in eligible_comments if (key := attempts.finding_key(review_id, c)) is not None}
            declared_count = raw_declared_counts.get(review_id, 0)
            recovered_count = len(
                _recovered_suppressed_occurrences(review_id, raw_comments, review_bodies.get(review_id, ""))
            )
            shortfall = max(0, declared_count - recovered_count)
            unresolved_shortfall = shortfall
            body_only_work = (
                not raw_comments
                and recovered_count == 0
                and (not has_identified_findings or review_id == actionable_review_id)
            )
            # Opaque body work uses a durable review/HEAD fallback instead of a TTL retry.
            if body_only_work or shortfall > 0:
                attempt_result, shortfall = critique_task_binding.register_attempt_and_reconcile(
                    provider,
                    snapshot,
                    attempts.attempted,
                    review_id,
                    body_only_work,
                    stuck_prior_threads,
                    attempts,
                    review_keys,
                    finding_aware,
                    shortfall,
                    is_duplicate_trigger,
                    unresolved_comments,
                    unresolved_shortfall,
                    self.name,
                )
                if attempt_result is not None:
                    return attempt_result
            if unresolved_review_keys or unresolved_shortfall > 0 or body_only_work:
                if not exhaustion_review_context_id:
                    exhaustion_review_context_id = review_id
                exhaustion_review_comments.extend(unresolved_comments)
                author_count = sum(c.id < 0 for c in unresolved_comments) + unresolved_shortfall
                if author_count > 0:
                    exhaustion_author_comment_counts_by_review[review_id] = author_count
            if review_keys:
                review_context_id = review_context_id or review_id
                pending_attempts.update(review_keys)
                # Only unresolved synthetic entries count as author work; promoted roots do not.
                author_count = sum(c.id < 0 for c in eligible_comments) + shortfall
                if author_count > 0:
                    declared_author_comment_counts_by_review[review_id] = author_count
                for comment in eligible_comments:
                    key = attempts.finding_key(review_id, comment)
                    if key is None or key not in seen_keys:
                        review_comments.append(comment)
                        if key is not None:
                            seen_keys.add(key)
        ci_key = "ci"
        ci_work = snapshot.ci_status == "failing" and ci_key not in attempts.attempted
        if ci_work:
            pending_attempts.add(ci_key)

        scope_review_context_id = review_context_id
        scope_review_comments = review_comments
        scope_author_comment_counts_by_review = declared_author_comment_counts_by_review
        if not pending_attempts and not scope_review_context_id and exhaustion_review_context_id:
            scope_review_context_id = exhaustion_review_context_id
            scope_review_comments = exhaustion_review_comments
            scope_author_comment_counts_by_review = exhaustion_author_comment_counts_by_review

        actionable_failed_check_names = set(snapshot.ci_failed_checks)
        failed_checks = [cr for cr in snapshot.check_runs if cr.name in actionable_failed_check_names]
        declared_author_comment_count = sum(scope_author_comment_counts_by_review.values())
        work_key_checks = failed_checks if ci_work or scope_review_context_id == 0 else []
        work_key = repair_work_key(
            scope_review_context_id, scope_review_comments, work_key_checks, scope_author_comment_counts_by_review
        )
        ledger = RepairDispatchLedger(
            provider, snapshot.pr_number, snapshot.head_sha, scope_review_context_id, work_key
        )
        cap = 1 if scope_review_context_id == 0 else 3

        def exhausted_result(dedup_count: int) -> ActionResult:
            unresolved_finding_keys = pending_attempts - {ci_key}
            escalation_needed = bool(unresolved_finding_keys and not snapshot.unresolved_threads_degraded)
            if escalation_needed:
                for key in sorted(unresolved_finding_keys):
                    attempts.escalate(
                        key,
                        reason=(
                            "actionable repair remains, but the per-HEAD repair deduplication "
                            "limit is exhausted. Human attention is required; no automatic "
                            "review request or repair retry will be made."
                        ),
                    )
            exhaustion_marker = ""
            try:
                observation = repair_observation_key(provider, snapshot)
                exhaustion_marker = f"<!-- repair-dispatch:exhausted:{snapshot.head_sha}:{observation} -->"
            except Exception as exc:
                _raise_if_rate_limit(exc)
                logger.warning("Cannot fingerprint exhausted work; persisting a scoped watchdog hold: %s", exc)
                try:
                    observation = repair_hold_observation_key(provider, snapshot)
                    exhaustion_marker = f"<!-- repair-dispatch:exhausted-hold:{snapshot.head_sha}:{observation} -->"
                except Exception as hold_exc:
                    _raise_if_rate_limit(hold_exc)
                    logger.warning("Cannot fingerprint held work; using a HEAD-scoped fail-closed hold: %s", hold_exc)
                    exhaustion_marker = f"<!-- repair-dispatch:exhausted-hold:{snapshot.head_sha}:unavailable -->"
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details=(
                    f"Repair budget exhausted: HEAD={snapshot.head_sha}, "
                    f"review={scope_review_context_id}, work={work_key}, confirmed={dedup_count}/{cap}; "
                    f"remaining work: {len(scope_review_comments)} findings, {len(failed_checks)} failing checks, "
                    f"{declared_author_comment_count} declared suppressed findings. "
                    "Human recovery: inspect prior task/trigger evidence and address remaining findings; "
                    "a new HEAD or changed actionable work gets an independent budget. "
                    "Approval and merge remain blocked by unresolved findings."
                ),
                limit_reached=True,
                dedup_limit_reached=True,
                repair_exhaustion_marker=exhaustion_marker,
                escalation_needed=escalation_needed,
            )

        if not pending_attempts:
            try:
                binding_failure = critique_task_binding.reconcile_ledger_task_binding(
                    provider,
                    snapshot,
                    attempts.attempted,
                    ledger,
                    self.name,
                )
                if binding_failure is not None:
                    return binding_failure
                dedup_skip, dedup_count = check_deduplication(
                    provider,
                    snapshot.pr_number,
                    snapshot.head_sha,
                    max_dispatches=cap,
                    review_id=scope_review_context_id,
                    work_key=work_key,
                )
            except Exception as exc:
                _raise_if_rate_limit(exc)
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error=str(exc),
                    details="Deduplication check failed; reconcile repair accounting before retry",
                )
            if dedup_skip:
                return exhausted_result(dedup_count)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details="No unattempted findings remain for this HEAD",
            )
        ci_failing = ci_work
        if review_context_id > 0:
            # Check for an active suppressed-comment deferral marker only when the
            # deferred review is the sole repair reason.  CI failures and stuck
            # prior-review threads must still dispatch repair even if the current
            # suppressed-only review round was deferred to triage.
            if review_actionable and not ci_failing and not stuck_prior_threads:
                try:
                    if read_active_suppressed_deferral(provider, snapshot.pr_number, actionable_review_id):
                        logger.info(
                            "PR #%d: Suppressed comments of review %d were deferred to a triage issue — "
                            "skipping repair dispatch",
                            snapshot.pr_number,
                            actionable_review_id,
                        )
                        return ActionResult(
                            name=self.name,
                            decision=ActionDecision.SKIP,
                            details="Deferred: suppressed comments handed to a triage issue",
                        )
                except Exception as exc:
                    _raise_if_rate_limit(exc)
                    logger.warning(
                        "PR #%d: Suppressed deferral check failed (proceeding with dispatch): %s",
                        snapshot.pr_number,
                        exc,
                    )

        try:
            cycle_reached, cycle_count = check_cycle_limit(provider, snapshot.pr_number)
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning("PR #%d: Cycle limit check failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="Cycle limit check failed",
            )

        if cycle_reached:
            logger.info("PR #%d: Cycle limit reached (count=%d)", snapshot.pr_number, cycle_count)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details=f"Cycle limit reached (count={cycle_count})",
                limit_reached=True,
                cycle_limit_reached=True,
            )

        review_repair_needed = review_context_id > 0
        if ci_failing and review_repair_needed:
            repair_type = "both"
        elif review_repair_needed:
            repair_type = "review"
        else:
            repair_type = "ci"

        # Get actionable failed checks for context (same subset used by ci_status gating)
        try:
            binding_failure = critique_task_binding.reconcile_ledger_task_binding(
                provider,
                snapshot,
                attempts.attempted,
                ledger,
                self.name,
            )
            if binding_failure is not None:
                return binding_failure
            dedup_skip, dedup_count = check_deduplication(
                provider,
                snapshot.pr_number,
                snapshot.head_sha,
                max_dispatches=cap,
                review_id=scope_review_context_id,
                work_key=work_key,
            )
        except Exception as exc:
            _raise_if_rate_limit(exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="Deduplication check failed; reconcile repair accounting before retry",
            )
        if dedup_skip:
            return exhausted_result(dedup_count)

        # Persist the creation intent before reserving findings so a failed
        # intent write cannot consume the attempt budget.
        try:
            ledger.begin()
        except Exception as exc:
            _raise_if_rate_limit(exc)
            try:
                ledger.retire_pending()
            except Exception as accounting_exc:
                _raise_if_rate_limit(accounting_exc)
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error=f"{exc}; intent retirement failed: {accounting_exc}",
                    details="Repair skipped: durable creation intent could not be confirmed or retired",
                    definitive_no_mutation=True,
                )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="Repair skipped: durable creation intent could not be confirmed",
                definitive_no_mutation=True,
            )

        try:
            attempts.reserve(pending_attempts)
        except Exception as exc:
            try:
                persisted_attempts = RepairAttemptTracker(provider, snapshot.pr_number, snapshot.head_sha)
                reserved_keys = pending_attempts & persisted_attempts.attempted
                if reserved_keys:
                    persisted_attempts.release(reserved_keys)
                ledger.retire_pending()
            except Exception as accounting_exc:
                _raise_if_rate_limit(accounting_exc)
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error=f"{exc}; intent retirement failed: {accounting_exc}",
                    details="Repair finding reservation failed and its durable intent could not be retired",
                    definitive_no_mutation=True,
                )
            _raise_if_rate_limit(exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="Repair finding reservation could not be confirmed",
                definitive_no_mutation=True,
            )

        bookkeeping_audit = getattr(provider, "_bookkeeping_audit", None)
        audit_start = len(bookkeeping_audit) if isinstance(bookkeeping_audit, list) else 0
        critique_marker: tuple[int, int, int] | None = None
        try:
            critique_marker, critique_prompt = critique_dispatch.create_critique_dispatch_marker(
                provider, snapshot, review_context_id, pending_attempts
            )
            receipt = provider.dispatch_repair(
                pr_number=snapshot.pr_number,
                head_sha=snapshot.head_sha,
                repair_type=repair_type,
                failed_checks=work_key_checks,
                review_comments=review_comments,
                review_id=review_context_id,
                declared_author_comment_count=declared_author_comment_count,
                declared_author_comment_counts_by_review=declared_author_comment_counts_by_review,
                **critique_dispatch.critique_repair_parameters(critique_prompt),
            )
        except Exception as exc:
            if isinstance(exc, RepairDispatchBookkeepingRateLimitError):
                derived.set("repair_dispatched", True)
                critique_task_binding.record_receipt_and_bind_critique_task(
                    ledger,
                    provider,
                    snapshot,
                    critique_marker,
                    exc.receipt,
                    self.name,
                    suppress_binding_errors=True,
                )
                raise
            if isinstance(exc, RepairDispatchNotAttemptedError):
                try:
                    critique_dispatch.cancel_critique_task_marker_if_present(provider, snapshot, critique_marker)
                    attempts.release(pending_attempts)
                    ledger.retire_pending()
                except Exception as accounting_exc:
                    _raise_if_rate_limit(accounting_exc)
                    return ActionResult(
                        name=self.name,
                        decision=ActionDecision.FAILED,
                        error=f"{exc}; intent retirement failed: {accounting_exc}",
                        details=(
                            "Repair failed before creation, but its task marker, durable intent, or finding "
                            "reservation could not be retired"
                        ),
                        definitive_no_mutation=True,
                    )
                cause = exc.__cause__
                if isinstance(cause, ProviderRateLimitError) and cause.is_rate_limit:
                    raise cause
                logger.error("PR #%d: Repair dispatch failed before creation: %s", snapshot.pr_number, exc)
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.FAILED,
                    error=str(exc),
                    details="dispatch_repair failed before any creation attempt",
                    definitive_no_mutation=True,
                )
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.error("PR #%d: Repair dispatch failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="dispatch_repair call failed; creation may be unresolved",
            )

        logger.info("PR #%d: Repair dispatched (type=%s, receipt=%s)", snapshot.pr_number, repair_type, receipt)

        derived.set("repair_dispatched", True)
        accounting_error, binding_failure = critique_task_binding.record_receipt_and_bind_critique_task(
            ledger,
            provider,
            snapshot,
            critique_marker,
            receipt,
            self.name,
        )
        if accounting_error is not None:
            return critique_task_binding.confirmed_receipt_accounting_failure(
                self.name,
                receipt,
                accounting_error,
                binding_failure,
            )
        return critique_dispatch.dispatched_repair_result(
            self.name,
            repair_type,
            receipt,
            bookkeeping_audit,
            audit_start,
            binding_failure,
        )
