"""Count unresolved review threads for snapshot gates and repair dispatch."""

from __future__ import annotations

import logging
import re

from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment
from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    CopilotGateVerdict,
    is_copilot_or_synthetic_review,
    select_prior_actionable_reviews,
)
from agentic_devtools.cli.ci.pipeline.snapshot_thread_inventory import (
    ThreadState,
    _index_thread_comments,
    _load_thread_states,
)
from agentic_devtools.cli.ci.pipeline.snapshot_utils import _raise_if_rate_limit
from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)
REPAIRABLE_REVIEW_STATES = frozenset({"CHANGES_REQUESTED", "COMMENTED", "APPROVED"})


def _effective_thread_owner_verdict_id(
    verdict_review_id: int | None,
    verdict: CopilotGateVerdict | None,
) -> int | None:
    """Resolve the effective thread-owner review ID for merge-gate provenance."""
    if verdict is not None:
        return verdict.review_id if verdict.review_id > 0 else None
    return verdict_review_id if verdict_review_id is not None and verdict_review_id > 0 else None


def count_unresolved_prior_threads(
    provider: CIPlatformProvider,
    pr_number: int,
    reviews: list[ReviewInfo],
    verdict_review_id: int | None,
    *,
    verdict: CopilotGateVerdict | None = None,
) -> tuple[int, int, bool, bool]:
    """Count blocking and repairable Copilot review threads.

    Returns ``(blocking_count, repairable_count, degraded, unknown_provenance)``.
    Missing or malformed provider inventories fail closed with conservative floors.
    """
    effective_review_id = _effective_thread_owner_verdict_id(verdict_review_id, verdict)
    unknown_provenance = effective_review_id is None
    if unknown_provenance:
        logger.warning(
            "PR #%d: no concrete thread-owner provenance for prior actionable reviews; "
            "falling back to count-all (conservative floor — not a query failure)",
            pr_number,
        )
    repairable_reviews = [
        review
        for review in reviews
        if is_copilot_or_synthetic_review(review) and review.state in REPAIRABLE_REVIEW_STATES
    ]
    if not repairable_reviews:
        return 0, 0, False, unknown_provenance

    blocking_review_ids = {review.id for review in select_prior_actionable_reviews(reviews, effective_review_id)}
    thread_states = _load_thread_states(provider, pr_number)
    if thread_states is None:
        return (1 if blocking_review_ids else 0), 1, True, unknown_provenance
    comment_to_thread = _index_thread_comments(thread_states, pr_number)
    if comment_to_thread is None:
        return (1 if blocking_review_ids else 0), 1, True, unknown_provenance

    totals = _count_review_inventories(
        provider,
        pr_number,
        repairable_reviews,
        blocking_review_ids,
        thread_states,
        comment_to_thread,
    )
    return _apply_inventory_floors(*totals, unknown_provenance)


def _is_promoted_root(review: ReviewInfo, comment: ReviewCommentInfo) -> bool:
    """Identify an authenticated promoted CCR root owned by this review."""
    if (
        comment.id <= 0
        or comment.source_review_id != review.id
        or comment.in_reply_to_id is not None
        or not isinstance(comment.body, str)
    ):
        return False
    normalized_body = normalize_ai_pr_loop_comment(comment.body)
    body_lines = normalized_body.rstrip().splitlines() if normalized_body is not None else []
    return (
        bool(body_lines) and re.fullmatch(rf"<!-- ccr-promoted:{review.id}:[a-z_]+:\d+ -->", body_lines[-1]) is not None
    )


def _count_one_review(
    provider: CIPlatformProvider,
    pr_number: int,
    review: ReviewInfo,
    is_blocking: bool,
    thread_states: dict[str, ThreadState],
    comment_to_thread: dict[int, str],
    counted_blocking: set[str],
    counted_repairable: set[str],
) -> tuple[int, int, bool, bool]:
    """Count unresolved threads in one review and report incomplete inventories."""
    blocking_count = 0
    repairable_count = 0
    blocking_unknown = False
    repairable_unknown = False
    try:
        comments = provider.list_review_comments(pr_number, review.id)
        for comment in comments:
            if comment.id < 0:
                continue
            thread_id = comment_to_thread.get(comment.id)
            if thread_id is None:
                logger.warning("PR #%d: review-thread state omitted comment %d — failing closed", pr_number, comment.id)
                repairable_unknown = True
                blocking_unknown = blocking_unknown or is_blocking
                continue
            is_resolved = thread_states[thread_id][0]
            if is_resolved:
                continue
            if thread_id not in counted_repairable:
                counted_repairable.add(thread_id)
                repairable_count += 1
            if (is_blocking or _is_promoted_root(review, comment)) and thread_id not in counted_blocking:
                counted_blocking.add(thread_id)
                blocking_count += 1
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning(
            "PR #%d: failed to list review comments for review %d (%s) — failing closed",
            pr_number,
            review.id,
            str(exc)[:200],
        )
        blocking_unknown = is_blocking
        repairable_unknown = True
    return blocking_count, repairable_count, blocking_unknown, repairable_unknown


def _count_review_inventories(
    provider: CIPlatformProvider,
    pr_number: int,
    reviews: list[ReviewInfo],
    blocking_review_ids: set[int],
    thread_states: dict[str, ThreadState],
    comment_to_thread: dict[int, str],
) -> tuple[int, int, bool, bool]:
    """Aggregate unresolved thread counts across actionable Copilot reviews."""
    blocking_count = 0
    repairable_count = 0
    blocking_unknown = False
    repairable_unknown = False
    counted_blocking: set[str] = set()
    counted_repairable: set[str] = set()
    for review in reviews:
        result = _count_one_review(
            provider,
            pr_number,
            review,
            review.id in blocking_review_ids,
            thread_states,
            comment_to_thread,
            counted_blocking,
            counted_repairable,
        )
        blocking_count += result[0]
        repairable_count += result[1]
        blocking_unknown = blocking_unknown or result[2]
        repairable_unknown = repairable_unknown or result[3]
    return blocking_count, repairable_count, blocking_unknown, repairable_unknown


def _apply_inventory_floors(
    blocking_count: int,
    repairable_count: int,
    blocking_unknown: bool,
    repairable_unknown: bool,
    unknown_provenance: bool,
) -> tuple[int, int, bool, bool]:
    """Apply fail-closed count floors when review inventories are incomplete."""
    if not blocking_unknown and not repairable_unknown:
        return blocking_count, repairable_count, False, unknown_provenance
    if repairable_unknown and repairable_count == 0:
        logger.warning(
            "No unresolved repairable threads were measured and at least one review inventory "
            "is unknown — applying the repairable floor of 1 unresolved thread"
        )
        repairable_count = 1
    if blocking_unknown:
        blocking_count = max(1, blocking_count)
    return blocking_count, repairable_count, True, unknown_provenance
