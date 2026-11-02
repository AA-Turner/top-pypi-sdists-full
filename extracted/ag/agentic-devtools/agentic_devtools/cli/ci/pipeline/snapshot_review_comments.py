"""Review-comment inventory helpers for PR snapshot collection."""

from __future__ import annotations

import logging

from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment
from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo, is_cloud_coding_agent_login
from agentic_devtools.cli.ci.pipeline.snapshot_utils import _raise_if_rate_limit
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.github.ccr_review_format import extract_ccr_findings, parse_suppressed_count

logger = logging.getLogger(__name__)


def _count_effective_review_comments(
    provider: CIPlatformProvider,
    pr_number: int,
    review: ReviewInfo,
    comments: list[ReviewCommentInfo] | None,
) -> tuple[int | None, bool | None]:
    """Count current-review comments left after reply and thread filtering.

    Returns:
        Tuple of ``(effective_count, filter_applied)``.
        ``(None, None)`` is returned whenever the provider cannot establish the
        complete inventory, preserving repair dispatch's fail-open behavior.
    """
    if comments is None:
        return None, None

    thread_lookup = getattr(provider, "list_review_threads_by_thread_id", None)
    if not callable(thread_lookup):
        return None, None
    try:
        thread_states = thread_lookup(pr_number)
    except Exception as exc:
        _raise_if_rate_limit(exc)
        logger.warning("PR #%d: Failed to derive effective review comments: %s", pr_number, str(exc)[:200])
        return None, None
    thread_index = _build_comment_thread_index(thread_states)
    if thread_index is None:
        return None, None

    resolved_comment_ids, known_comment_ids, _ = thread_index
    root_ids = {
        comment.id
        for comment in comments
        if type(comment.id) is int and comment.id > 0 and comment.in_reply_to_id is None
    }
    reply_ids = {
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
    answered_root_ids = _answered_root_comment_ids(comments, reply_ids)
    effective_count, filter_applied = _count_unfiltered_comments(
        comments,
        known_comment_ids,
        resolved_comment_ids,
        reply_ids,
        answered_root_ids,
    )
    if effective_count is None:
        return None, None

    # Synthetic suppressed entries are normally recovered by the provider. If
    # they are absent despite a declared count, the inventory is incomplete.
    suppressed_count = parse_suppressed_count(review.body)
    if not _has_complete_suppressed_coverage(review, comments, suppressed_count):
        return None, None
    return effective_count, filter_applied


def _build_comment_thread_index(
    thread_states: object,
) -> tuple[set[int], set[int], dict[int, str]] | None:
    """Validate provider thread state and index known and resolved comment IDs."""
    if not isinstance(thread_states, dict):
        return None
    resolved_comment_ids: set[int] = set()
    known_comment_ids: set[int] = set()
    comment_thread_ids: dict[int, str] = {}
    for thread_id, state in thread_states.items():
        if (
            not isinstance(thread_id, str)
            or not thread_id
            or not isinstance(state, tuple)
            or len(state) != 2
            or type(state[0]) is not bool
            or not isinstance(state[1], tuple)
            or any(type(comment_id) is not int for comment_id in state[1])
        ):
            return None
        for comment_id in state[1]:
            mapped_thread = comment_thread_ids.get(comment_id)
            if mapped_thread is not None and mapped_thread != thread_id:
                return None
            comment_thread_ids[comment_id] = thread_id
            known_comment_ids.add(comment_id)
            if state[0] and comment_id > 0:
                resolved_comment_ids.add(comment_id)
    return resolved_comment_ids, known_comment_ids, comment_thread_ids


def _answered_root_comment_ids(comments: list[ReviewCommentInfo], reply_ids: set[int]) -> set[int | None]:
    """Return root comment IDs with non-empty cloud-agent replies."""
    return {
        comment.in_reply_to_id
        for comment in comments
        if comment.id in reply_ids and isinstance(comment.body, str) and bool(comment.body.strip())
    }


def _count_unfiltered_comments(
    comments: list[ReviewCommentInfo],
    known_comment_ids: set[int],
    resolved_comment_ids: set[int],
    reply_ids: set[int],
    answered_root_ids: set[int | None],
) -> tuple[int | None, bool]:
    """Count comments remaining after thread, reply, and resolution filtering."""
    effective_count = 0
    filter_applied = False
    for comment in comments:
        if type(comment.id) is not int:
            return None, filter_applied
        if comment.id > 0:
            if comment.id not in known_comment_ids:
                return None, filter_applied
            if comment.id in resolved_comment_ids or comment.id in reply_ids or comment.id in answered_root_ids:
                filter_applied = True
                continue
            effective_count += 1
        elif comment.id < 0:
            effective_count += 1
        else:
            return None, filter_applied
    return effective_count, filter_applied


def _has_complete_suppressed_coverage(
    review: ReviewInfo,
    comments: list[ReviewCommentInfo],
    suppressed_count: int,
) -> bool:
    """Check suppressed review findings have recovered promotion markers."""
    if suppressed_count <= 0 or any(type(comment.id) is int and comment.id < 0 for comment in comments):
        return True
    explicitly_resolved = {
        finding.ordinal
        for finding in extract_ccr_findings(review.body).findings
        if finding.section == "suppressed" and finding.explicitly_resolved
    }
    promoted_markers = _promoted_suppression_markers(review, comments)
    expected_markers = {
        f"<!-- ccr-promoted:{review.id}:suppressed:{ordinal} -->"
        for ordinal in range(1, suppressed_count + 1)
        if ordinal not in explicitly_resolved
    }
    return expected_markers.issubset(promoted_markers)


def _promoted_suppression_markers(review: ReviewInfo, comments: list[ReviewCommentInfo]) -> set[str]:
    """Return trailing markers from normalized roots promoted for this review."""
    markers: set[str] = set()
    for comment in comments:
        if (
            type(comment.id) is not int
            or comment.id <= 0
            or comment.source_review_id != review.id
            or comment.in_reply_to_id is not None
            or not isinstance(comment.body, str)
        ):
            continue
        normalized_body = normalize_ai_pr_loop_comment(comment.body)
        lines = normalized_body.rstrip().splitlines() if normalized_body is not None else []
        if lines:
            markers.add(lines[-1])
    return markers
