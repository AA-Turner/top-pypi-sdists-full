"""Additional-model review reply lifecycle."""

from datetime import datetime
from typing import Any

from .consolidated_review import render_model_review_reply
from .review_scaffold_comments import _patch_comment_content
from .review_scaffold_commit_state import _resolve_commit_thread_id
from .review_scaffold_replies import _post_reply
from .review_state import CommitComment, ReviewState, compute_aggregate_status


def _post_or_update_model_reply(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    existing_state: ReviewState,
    commit_hash: str | None,
    model_id: str,
    base_url: str,
    now: datetime,
) -> int | None:
    """Post (or update in place) an additional model's review reply.

    Implements the "different model, same commit" path: the joining model's
    review is posted as a **reply** within the commit's existing review thread
    (no ``--force-rereview`` needed). The reply's comment id is tracked on the
    commit registry's :class:`ModelCommentRef` so a subsequent run of the *same*
    additional model PATCHes the reply in place instead of posting a duplicate.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL (without thread id suffix).
        existing_state: Current review state (mutated: registry ref updated).
        commit_hash: The reviewed commit SHA.
        model_id: The additional reviewing model.
        base_url: PR root URL for building discussion links.
        now: Current time (for the registry timestamp).

    Returns:
        The reply comment id, or ``None`` when no thread could be resolved.
    """
    thread_id = _resolve_commit_thread_id(existing_state, commit_hash)
    if not thread_id:
        return None

    content = render_model_review_reply(existing_state, model_id, base_url)

    # Use the resolved commit hash (never the empty-string fallback) so the
    # registry key always identifies an actual commit.
    effective_hash = commit_hash or existing_state.commitHash
    if not effective_hash:
        return None

    entry = existing_state.commitComments.get(effective_hash)
    if entry is None:
        entry = CommitComment(
            commitHash=effective_hash,
            threadId=thread_id,
            status=existing_state.overallSummary.status,
        )
        existing_state.commitComments[effective_hash] = entry
    if entry.threadId <= 0:
        entry.threadId = thread_id
    ref = entry.upsert_model(model_id)

    if ref.commentId > 0:
        # Update the existing reply in place.  If the original comment is owned
        # by a different identity, _patch_comment_content falls back to posting
        # a new cross-identity reply and returns the new comment id; update the
        # registry so we don't create duplicates on subsequent runs.
        fallback_id = _patch_comment_content(requests_module, headers, threads_url, thread_id, ref.commentId, content)
        if fallback_id is not None:
            ref.commentId = fallback_id
        comment_id = ref.commentId
    else:
        comment_id = _post_reply(requests_module, headers, threads_url, thread_id, content)
        ref.commentId = comment_id

    ref.status = compute_aggregate_status([fe.status for fe in existing_state.files.values()])
    ref.timestamp = now.isoformat()
    entry.timestamp = now.isoformat()
    return comment_id
