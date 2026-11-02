"""Fetch and sanitize issue-comment and review-thread snapshot data."""

from __future__ import annotations

import logging

from ..models import COPILOT_COMMENT_LOGINS, IssueCommentInfo
from ..provider import CIPlatformProvider
from ..review_thread_state import fetch_review_thread_states
from . import snapshot_comment_sanitization, snapshot_control_markers
from .models import CommentInfo

logger = logging.getLogger(__name__)


def _get_review_thread_statuses(
    provider: CIPlatformProvider,
    pr_number: int,
) -> dict[int, tuple[bool, bool]]:
    """Map review comment IDs to (is_resolved, has_reply) when provider supports it.

    Returns an empty mapping when the provider cannot report review-thread state
    (missing capability or failed lookup). Callers then default every thread to
    ``is_resolved=False``, which fails closed: a provider that lacks the
    capability can never make threads look resolved.
    """
    result = fetch_review_thread_states(provider, pr_number)
    if result.degraded:
        logger.warning(
            "PR #%d: review-thread state unavailable (%s) — treating all threads as unresolved",
            pr_number,
            result.reason,
        )
    return result.states


def _get_latest_agent_comment(
    provider: CIPlatformProvider,
    pr_number: int,
    comments: list | None = None,
    *,
    persist_sanitized_body: bool = False,
) -> CommentInfo | None:
    """Get the latest Copilot-authored issue comment if supported by provider.

    When ``persist_sanitized_body`` is ``True``, any balanced-body rewrite is
    also patched back to the source issue comment so GitHub no longer renders
    the remainder of the comment as swallowed by an unterminated HTML comment.
    Persistence is best-effort: read paths keep working even if the PATCH fails.
    """
    if comments is None:
        list_issue_comments = getattr(provider, "list_issue_comments", None)
        if not callable(list_issue_comments):
            return None
        comments = list_issue_comments(pr_number)
    latest = _get_latest_copilot_issue_comment(comments)
    if latest is None:
        return None
    sanitized_body, inserted_positions = (
        snapshot_comment_sanitization._sanitize_unterminated_html_comments_with_insertions(latest.body)
    )
    persisted_body = (
        snapshot_control_markers._neutralize_synthesized_control_markers(sanitized_body, inserted_positions)
        if persist_sanitized_body and sanitized_body != latest.body
        else sanitized_body
    )
    if (
        persist_sanitized_body
        and persisted_body != latest.body
        and not snapshot_control_markers._introduces_control_marker(latest.body, persisted_body)
    ):
        update_comment = getattr(provider, "update_comment", None)
        if callable(update_comment):
            try:
                update_comment(latest.id, persisted_body)
            except Exception as exc:
                logger.warning(
                    "Failed to persist sanitized Copilot comment %d on PR #%d: %s",
                    latest.id,
                    pr_number,
                    exc,
                )
    return CommentInfo(
        id=latest.id,
        author=latest.author,
        body=persisted_body if persist_sanitized_body else sanitized_body,
        created_at=latest.created_at,
    )


def _get_latest_copilot_issue_comment(comments: list[IssueCommentInfo]) -> IssueCommentInfo | None:
    """Return the newest Copilot-authored issue comment from *comments*."""
    copilot_comments = [comment for comment in comments if comment.author in COPILOT_COMMENT_LOGINS]
    if not copilot_comments:
        return None
    return max(copilot_comments, key=lambda comment: (comment.created_at, comment.id))


def _has_evaluator_sentinel_comment(
    provider: CIPlatformProvider,
    pr_number: int,
    current_head_sha: str,
    comments: list | None = None,
) -> bool:
    """Return True when any issue comment is an evaluator-synthesized sentinel for the current HEAD.

    Evaluator-synthesized sentinels (from ``synthesize_sentinel()`` / ``verify_and_resolve()``)
    are posted via ``provider.post_comment()`` using the workflow token rather than a Copilot
    login, so they are not captured by ``_get_latest_agent_comment()``.  Scope the check to
    ``current_head_sha`` (first 8 chars) to avoid false positives from older cycle sentinels
    on the same PR.
    """
    if not current_head_sha:
        return False
    head_sha_short = current_head_sha[:8]
    if comments is None:
        list_issue_comments = getattr(provider, "list_issue_comments", None)
        if not callable(list_issue_comments):
            return False
        try:
            comments = list_issue_comments(pr_number)
        except Exception as exc:
            logger.warning("Failed to fetch issue comments for evaluator sentinel check on PR #%d: %s", pr_number, exc)
            return False
    return any(snapshot_control_markers._SENTINEL_MARKER in c.body and head_sha_short in c.body for c in comments)
