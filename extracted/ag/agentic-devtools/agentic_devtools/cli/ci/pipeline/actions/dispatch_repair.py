"""Dispatch repair action — triggers AI repair on CI failure or actionable review."""

from __future__ import annotations

import logging

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
from agentic_devtools.cli.ci.pipeline.snapshot import (
    REPAIRABLE_REVIEW_STATES,
    DerivedState,
    PRStateSnapshot,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.review_thread_state import fetch_review_thread_states
from agentic_devtools.cli.github.ccr_review_format import parse_suppressed_count
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

logger = logging.getLogger(__name__)

#: Gate-verdict reasons that mean the HEAD Copilot review carries actionable
#: feedback in its *body* (posted comments, suppressed/low-confidence comments,
#: a new-CCR-format "Not ready to approve" verdict, or a declared suppressed
#: count whose entries could not be parsed).  Freshness reasons
#: (awaiting-fresh, content-changed) are deliberately excluded — they call for a
#: *new* review, not a repair dispatch.
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
    """Return the id of the actionable Copilot review, or ``0`` when none is actionable.

    A Copilot review is actionable when it carries feedback the repair agent
    should evaluate:

    * ``CHANGES_REQUESTED`` on HEAD, or
    * ``COMMENTED`` on HEAD with inline comments (unknown inline counts fail
      closed and are treated as actionable), or
    * a **content-blocking** gate verdict (posted comments, suppressed/low-confidence
      comments, or a new-CCR "Not ready to approve" heading) for a concrete review id.

    The third branch is intentionally format-, state-, and identity-agnostic: it
    fires regardless of the review's submitted state (``APPROVED``/``COMMENTED``)
    and regardless of whether the gate's effective ``review_id`` matches
    ``copilot_review_id``.  The private-preview CCR format can block the gate purely
    from the review body while exposing no inline comments through the API, and the
    effective review may be a prior-commit review selected by diff-hash freshness
    (whose id differs from ``copilot_review_id``) or a review submitted as
    ``APPROVED`` with body-only suppressed comments.  Without this branch such a PR
    is blocked by the gate yet never triggers repair — a permanent stall.

    It returns the gate verdict's ``review_id`` (not ``copilot_review_id``) so the
    dispatch fetches comments for, and dedups against, the review the gate actually
    evaluated.  Freshness reasons (awaiting-fresh, content-changed) are excluded —
    they call for a *new* review, not a repair dispatch.
    """
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
        return verdict.review_id
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
        if (declared_count := parse_suppressed_count(bodies.get(review_id, ""))) > 0
    }


def _has_stuck_prior_review_threads(snapshot: PRStateSnapshot) -> bool:
    """Return True when unresolved prior-review threads should trigger repair."""
    return (
        snapshot.ci_status == "passing"
        and snapshot.copilot_review_id == 0
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


def _load_repair_thread_states(
    provider: CIPlatformProvider,
    pr_number: int,
) -> set[int] | None:
    """Load optional thread state, returning None when the capability degrades."""
    result = fetch_review_thread_states(provider, pr_number)
    if result.degraded:
        logger.warning("PR #%d: %s — retaining possible repair candidates", pr_number, result.reason)
        return None
    return {comment_id for comment_id, (is_resolved, _has_reply) in result.states.items() if is_resolved}


def _select_repairable_thread_owner_reviews(
    provider: CIPlatformProvider,
    snapshot: PRStateSnapshot,
    repairable_reviews: list[ReviewInfo],
) -> tuple[list[ReviewInfo], dict[int, list[ReviewCommentInfo]]]:
    """Return reviews that own unresolved repairable threads, plus fetched comments."""
    thread_lookup = getattr(provider, "list_review_threads_by_thread_id", None)
    if not callable(thread_lookup):
        return repairable_reviews, {}

    try:
        thread_states = thread_lookup(snapshot.pr_number)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning(
            "PR #%d: Failed to derive repairable-thread ownership from thread state: %s",
            snapshot.pr_number,
            exc,
        )
        return repairable_reviews, {}

    if not isinstance(thread_states, dict):
        return repairable_reviews, {}

    # Validate the entire mapping before processing: fall back to all candidates on any
    # malformed entry so a mixed valid/malformed mapping never silently excludes an owning
    # review from the repair payload.
    for state in thread_states.values():
        if not (
            isinstance(state, tuple)
            and len(state) == 2
            and type(state[0]) is bool
            and isinstance(state[1], tuple)
            and all(type(c) is int and c >= 0 for c in state[1])
        ):
            logger.warning(
                "PR #%d: Malformed thread state entry detected; falling back to all repairable reviews.",
                snapshot.pr_number,
            )
            return repairable_reviews, {}

    unresolved_comment_ids = {comment_id for state in thread_states.values() if not state[0] for comment_id in state[1]}
    resolved_comment_ids = {
        comment_id
        for is_resolved, comment_ids in thread_states.values()
        for comment_id in comment_ids
        if is_resolved and comment_id > 0
    }
    if not unresolved_comment_ids:
        return repairable_reviews, {}

    owner_ids: set[int] = set()
    comments_by_review_id: dict[int, list[ReviewCommentInfo]] = {}
    fully_filtered_review_ids: set[int] = set()
    for review in repairable_reviews:
        try:
            comments = provider.list_review_comments(snapshot.pr_number, review.id)
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning(
                "PR #%d: Failed to derive repairable-thread ownership from review %d comments: %s",
                snapshot.pr_number,
                review.id,
                exc,
            )
            return repairable_reviews, {}
        filtered_comments = _filter_repair_comments(comments, resolved_comment_ids)
        comments_by_review_id[review.id] = filtered_comments
        if comments and not filtered_comments:
            fully_filtered_review_ids.add(review.id)
        if any(comment.id in unresolved_comment_ids for comment in filtered_comments if comment.id >= 0):
            owner_ids.add(review.id)

    if not owner_ids:
        if fully_filtered_review_ids:
            return [
                review for review in repairable_reviews if review.id not in fully_filtered_review_ids
            ], comments_by_review_id
        return repairable_reviews, comments_by_review_id
    return [review for review in repairable_reviews if review.id in owner_ids], comments_by_review_id


class DispatchRepairAction:
    """Dispatch a repair when CI fails or actionable review feedback exists.

    Preconditions:
    - CI failed OR actionable Copilot review on HEAD
      OR stuck unresolved threads from prior Copilot review(s)
    - Deduplication limit not exceeded
    - Cycle limit not exceeded

    Idempotency: Recent dispatch → skip.
    """

    runs_after_invalidation = True

    @property
    def name(self) -> str:
        return "dispatch_repair"

    def evaluate(self, snapshot: PRStateSnapshot, derived: DerivedState) -> ActionResult:
        """Evaluate whether repair dispatch is needed."""
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

        # CI pending check - don't dispatch repair while CI still running
        if snapshot.ci_status == "pending":
            preconditions["ci_not_pending"] = False
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                preconditions=preconditions,
                details="CI still pending — waiting",
            )
        preconditions["ci_not_pending"] = True

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            preconditions=preconditions,
            details=f"Repair needed (ci_failing={ci_failing}, review_actionable={review_actionable})",
        )

    def execute(
        self,
        provider: CIPlatformProvider,
        snapshot: PRStateSnapshot,
        derived: DerivedState,
    ) -> ActionResult:
        """Dispatch repair by posting @copilot comment."""
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
        repairable_owner_reviews = repairable_reviews
        ownership_comments_cache: dict[int, list[ReviewCommentInfo]] = {}
        if stuck_prior_threads and repairable_reviews:
            repairable_owner_reviews, ownership_comments_cache = _select_repairable_thread_owner_reviews(
                provider,
                snapshot,
                repairable_reviews,
            )
        stuck_fully_filtered_review_ids = (
            [review.id for review in repairable_reviews]
            if (
                stuck_prior_threads
                and not review_actionable
                and not repairable_owner_reviews
                and bool(ownership_comments_cache)
            )
            else []
        )
        ci_failing = snapshot.ci_status == "failing"
        ci_passing = snapshot.ci_status == "passing"
        # Use the *effective* actionable review id (the review the gate evaluated),
        # which may differ from ``copilot_review_id`` for a new-CCR review or a
        # prior-commit review selected by diff-hash freshness.
        # When effective review work is empty and there are no stuck prior threads,
        # the only repair reason is CI.  Clear the review context so that stale
        # review-ID deduplication cannot suppress a CI-only dispatch and so that
        # a CI-only repair is not associated with a stale review ID.
        review_context_id = actionable_review_id if (review_actionable or stuck_prior_threads) else 0
        if stuck_fully_filtered_review_ids:
            # Preserve a review context for shortfall-only dispatches so the trigger
            # marker and review-ID deduplication remain effective.
            review_context_id = stuck_fully_filtered_review_ids[0]
        # True when the multi-owner loop below already checked is_duplicate_trigger for the
        # chosen review_context_id; suppresses the redundant general check that follows.
        _review_context_dedup_checked = False
        if not review_actionable and stuck_prior_threads and repairable_owner_reviews:
            # Find the first owner review that does not already have an active trigger
            # marker.  Picking [0] blindly stalls the pipeline permanently when [0] is
            # already marked but a later owner has never been dispatched.
            chosen_id = 0
            all_owners_duplicated = True
            for _candidate in repairable_owner_reviews:
                try:
                    if not is_duplicate_trigger(provider, snapshot.pr_number, _candidate.id):
                        chosen_id = _candidate.id
                        all_owners_duplicated = False
                        _review_context_dedup_checked = True
                        break
                except Exception as _exc:
                    _raise_if_rate_limit(_exc)
                    logger.warning(
                        "PR #%d: Review-ID dedup check failed for candidate review %d: %s",
                        snapshot.pr_number,
                        _candidate.id,
                        _exc,
                    )
                    # Fail-open: use this candidate and proceed with dispatch.
                    # Mark as checked so the general dedup block below does not retry
                    # the same call on a transient API error.
                    chosen_id = _candidate.id
                    all_owners_duplicated = False
                    _review_context_dedup_checked = True
                    break
            if all_owners_duplicated:
                _all_ids = [r.id for r in repairable_owner_reviews]
                logger.info(
                    "PR #%d: Trigger comment already exists for all repairable owner reviews %s — skipping",
                    snapshot.pr_number,
                    _all_ids,
                )
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.SKIP,
                    details=f"Repair already dispatched for all repairable owner reviews: {_all_ids}",
                )
            # Invariant: all_owners_duplicated is False only when a candidate break set chosen_id.
            assert chosen_id > 0  # noqa: S101
            review_context_id = chosen_id
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

            # Check review-ID level deduplication (FR-012).
            # Applies to normal actionable reviews on HEAD and stuck prior-review thread
            # repairs.  Skipped when the multi-owner loop above already confirmed that
            # review_context_id is not duplicated, to avoid a redundant double call.
            if not _review_context_dedup_checked:
                try:
                    if is_duplicate_trigger(provider, snapshot.pr_number, review_context_id):
                        logger.info(
                            "PR #%d: Trigger comment already exists for review_id=%d — skipping",
                            snapshot.pr_number,
                            review_context_id,
                        )
                        return ActionResult(
                            name=self.name,
                            decision=ActionDecision.SKIP,
                            details=f"Repair already dispatched for review_id={review_context_id}",
                        )
                except Exception as exc:
                    _raise_if_rate_limit(exc)
                    logger.warning("PR #%d: Review-ID dedup check failed: %s", snapshot.pr_number, exc)
                    # Fail-open: proceed with dispatch on transient API failures; the
                    # review-ID dedup guard is best-effort and should not block repair.

        dedup_kwargs = {"max_dispatches": 1} if ci_failing and not (review_actionable or stuck_prior_threads) else {}

        # Check deduplication limits
        try:
            dedup_skip, dedup_count = check_deduplication(
                provider,
                snapshot.pr_number,
                snapshot.head_sha,
                **dedup_kwargs,
            )
        except Exception as exc:
            _raise_if_rate_limit(exc)
            logger.warning("PR #%d: Dedup check failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="Deduplication check failed",
            )

        if dedup_skip:
            logger.info(
                "PR #%d: Dedup limit reached (count=%d, sha=%s)",
                snapshot.pr_number,
                dedup_count,
                snapshot.head_sha[:8],
            )
            return ActionResult(
                name=self.name,
                decision=ActionDecision.SKIP,
                details=f"Dedup limit reached (count={dedup_count})",
                limit_reached=True,
            )

        # Check cycle limit
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
            )

        # Determine repair type
        review_repair_needed = review_actionable or stuck_prior_threads
        if ci_failing and review_repair_needed:
            repair_type = "both"
        elif review_repair_needed:
            repair_type = "review"
        else:
            repair_type = "ci"

        # Get actionable failed checks for context (same subset used by ci_status gating)
        actionable_failed_check_names = set(snapshot.ci_failed_checks)
        failed_checks = [cr for cr in snapshot.check_runs if cr.name in actionable_failed_check_names]

        # Get review comments if needed
        review_comments = []
        declared_author_comment_count = 0
        declared_author_comment_counts_by_review: dict[int, int] = {}
        if review_repair_needed and (review_context_id or stuck_fully_filtered_review_ids):
            if stuck_prior_threads:
                review_ids = [r.id for r in repairable_owner_reviews]
                if not review_ids and stuck_fully_filtered_review_ids:
                    review_ids = list(stuck_fully_filtered_review_ids)
                if isinstance(review_context_id, int) and review_context_id > 0 and review_context_id not in review_ids:
                    review_ids.append(review_context_id)
            else:
                review_ids = [review_context_id] if review_context_id is not None else []
            declared_author_comment_counts_by_review = _declared_suppressed_counts_by_review(snapshot, review_ids)
            declared_author_comment_count = sum(declared_author_comment_counts_by_review.values())
            seen_comment_keys: set[tuple[int, int]] = set()
            resolved_comment_ids = _load_repair_thread_states(provider, snapshot.pr_number)
            fetch_failed = False
            total_fetched_before_filter = 0
            for review_id in review_ids:
                try:
                    comments = ownership_comments_cache.get(review_id)
                    if comments is None:
                        comments = provider.list_review_comments(snapshot.pr_number, review_id)
                    total_fetched_before_filter += len(comments)
                    for comment in _filter_repair_comments(comments, resolved_comment_ids):
                        dedup_key = (review_id, comment.id) if comment.id < 0 else (0, comment.id)
                        if dedup_key in seen_comment_keys:
                            continue
                        seen_comment_keys.add(dedup_key)
                        review_comments.append(comment)
                except Exception as exc:
                    _raise_if_rate_limit(exc)
                    logger.warning("PR #%d: Failed to fetch review comments: %s", snapshot.pr_number, exc)
                    fetch_failed = True

            # Re-evaluate after agent-reply filtering: when all comments were
            # filtered out, CI is passing, and no suppressed findings were
            # declared, there is no repair work to do. Skip only when:
            # - all fetches succeeded (fail-open on transient errors),
            # - at least one comment was fetched before filtering (evidence
            #   that filtering actually removed something), OR the stuck-thread
            #   ownership pass already signalled full filtering (the cache
            #   stores already-filtered results, so total_fetched_before_filter
            #   would be zero for that path),
            # - in the stuck-prior-threads path the stuck-fully-filtered set
            #   must be non-empty (otherwise the dispatch is driven by owning
            #   reviews that still have live comments).
            if (
                not fetch_failed
                and not review_comments
                and ci_passing
                and declared_author_comment_count == 0
                and (total_fetched_before_filter > 0 or bool(stuck_fully_filtered_review_ids))
                and (not stuck_prior_threads or bool(stuck_fully_filtered_review_ids))
            ):
                logger.info(
                    "PR #%d: All review comments were filtered and CI is passing — skipping repair",
                    snapshot.pr_number,
                )
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.SKIP,
                    details="All review comments filtered, CI passing — no repair needed",
                )

        # Filter out comments already handled by ApplySuggestionsAction (FR-005, FR-006)
        exclusion_ctx: ExclusionContext | None = derived.get("exclusion_context")
        if exclusion_ctx and exclusion_ctx.resolved_comment_ids and review_comments:
            original_count = len(review_comments)
            review_comments = [rc for rc in review_comments if rc.id not in exclusion_ctx.resolved_comment_ids]
            filtered_count = original_count - len(review_comments)
            if filtered_count > 0:
                logger.info(
                    "PR #%d: Excluded %d review comments already auto-applied",
                    snapshot.pr_number,
                    filtered_count,
                )

            # Re-evaluate: if no review comments remain and CI is passing, skip repair
            # only when the review body did not declare any suppressed findings that
            # still need a shortfall notice. Otherwise the dispatch must still run so
            # the repair agent is told to fetch the unrecovered author comments.
            if not review_comments and ci_passing and declared_author_comment_count == 0:
                logger.info(
                    "PR #%d: All review comments were auto-applied and CI is passing — skipping repair",
                    snapshot.pr_number,
                )
                return ActionResult(
                    name=self.name,
                    decision=ActionDecision.SKIP,
                    details="All review comments auto-applied, CI passing — no repair needed",
                )

        # Dispatch the repair
        try:
            comment_id = provider.dispatch_repair(
                pr_number=snapshot.pr_number,
                head_sha=snapshot.head_sha,
                repair_type=repair_type,
                failed_checks=failed_checks,
                review_comments=review_comments,
                review_id=review_context_id,
                declared_author_comment_count=declared_author_comment_count,
                declared_author_comment_counts_by_review=declared_author_comment_counts_by_review,
            )
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.error("PR #%d: Repair dispatch failed: %s", snapshot.pr_number, exc)
            return ActionResult(
                name=self.name,
                decision=ActionDecision.FAILED,
                error=str(exc),
                details="dispatch_repair call failed",
            )

        logger.info(
            "PR #%d: Repair dispatched (type=%s, comment_id=%d)",
            snapshot.pr_number,
            repair_type,
            comment_id,
        )

        derived.set("repair_dispatched", True)

        return ActionResult(
            name=self.name,
            decision=ActionDecision.EXECUTE,
            details=f"Repair dispatched (type={repair_type}, comment_id={comment_id})",
        )
