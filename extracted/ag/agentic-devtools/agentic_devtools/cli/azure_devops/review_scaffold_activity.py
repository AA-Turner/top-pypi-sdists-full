"""Review activity log formatting and update helpers."""

from typing import Any

from .marker import build_marker
from .review_scaffold_comments import _patch_comment_content
from .review_scaffold_replies import _post_reply
from .review_state import ReviewSession


def _format_activity_log_entry(
    status_emoji: str,
    status_text: str,
    timestamp: str,
    model_name: str,
    short_hash: str,
    session_id: str,
    detail_message: str,
    sequence_number: int,
) -> str:
    """Format an activity log entry.

    Args:
        status_emoji: Emoji for the status (e.g. "🆕", "⚠️").
        status_text: Status text (e.g. "New Review", "Already Reviewed").
        timestamp: ISO 8601 UTC timestamp.
        model_name: AI model name.
        short_hash: Short commit hash (first 7 characters).
        session_id: Session UUID.
        detail_message: Detail message body.
        sequence_number: Incrementing sequence number for ordering.

    Returns:
        Formatted markdown string.
    """
    return (
        f"{build_marker('activity-log-entry')}\n"
        f"### Review Session — {status_emoji} {status_text}\n"
        f"\n"
        f"*Logged at:* {timestamp}\n"
        f"*Model:* **{model_name}**\n"
        f"*Commit:* `{short_hash}`\n"
        f"*Session ID:* `{session_id}`\n"
        f"\n"
        f"{detail_message}\n"
        f"\n"
        f"<!-- activity-seq:{sequence_number} -->\n"
    )


def _post_activity_log_entry(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    thread_id: int,
    entry_content: str,
) -> int:
    """Post a new activity log entry as a reply to the activity log thread.

    The header comment ("Review Activity Log") remains pinned as the main
    (top-level) comment.  New entries are posted as replies.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL.
        thread_id: Activity log thread ID.
        entry_content: Formatted markdown for the new entry.

    Returns:
        The comment ID of the newly-created reply.
    """
    return _post_reply(requests_module, headers, threads_url, thread_id, entry_content)


def _update_activity_log_comment_status(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    thread_id: int,
    comment_id: int,
    status_emoji: str,
    status_text: str,
    session: ReviewSession,
    commit_hash: str | None,
    sequence_number: int,
    detail_message: str,
) -> int | None:
    """Update an existing activity log comment to reflect a terminal status.

    Re-renders the entry via ``_format_activity_log_entry`` with the terminal
    status emoji/text and PATCHes the comment in-place.  If the PATCH is
    blocked by a 403 (cross-identity ownership), a reply is posted instead and
    its comment ID is returned so callers can update their stored pointer.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL.
        thread_id: Activity log thread ID.
        comment_id: Comment ID of the activity log reply to update.
        status_emoji: Emoji for the terminal status (e.g. "\u2705", "\u274c").
        status_text: Status text (e.g. "Completed", "Failed").
        session: The ReviewSession whose entry is being updated.
        commit_hash: Commit hash for display.
        sequence_number: Original sequence number of the entry.
        detail_message: Updated detail message body.

    Returns:
        The new reply comment ID when the 403 fallback posts a reply (callers
        should persist this as the new ``activityLogCommentId``);
        ``None`` when the content was updated in place via PATCH.
    """
    short_hash = (commit_hash or "unknown")[:7]
    updated_content = _format_activity_log_entry(
        status_emoji,
        status_text,
        session.startedUtc,
        session.modelId,
        short_hash,
        session.sessionId,
        detail_message,
        sequence_number,
    )
    return _patch_comment_content(requests_module, headers, threads_url, thread_id, comment_id, updated_content)
