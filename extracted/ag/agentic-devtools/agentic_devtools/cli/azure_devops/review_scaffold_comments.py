"""Azure DevOps review comment update helpers."""

from typing import Any

from .review_scaffold_replies import _append_path_to_url, _post_cross_identity_reply, _post_reply
from .review_templates import rewrite_header_for_subsequent


def _get_thread_comments(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    thread_id: int,
) -> list[dict[str, Any]]:
    """GET a thread and return its comments list.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL.
        thread_id: Thread to fetch.

    Returns:
        List of comment dicts from the API response.
    """
    url = _append_path_to_url(threads_url, thread_id)
    response = requests_module.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json().get("comments", [])


def _patch_comment_content(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    thread_id: int,
    comment_id: int,
    new_content: str,
    cross_identity: bool = False,
) -> int | None:
    """PATCH a single comment's content, falling back to reply on 403.

    When ``cross_identity`` is True or a 403 is received, posts the content
    as a reply to the thread instead of editing the original comment.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL.
        thread_id: Thread containing the comment.
        comment_id: Comment to update.
        new_content: New markdown content.
        cross_identity: If True, skip PATCH and post reply directly.

    Returns:
        The new reply comment ID when the 403 fallback posts a reply;
        ``None`` when the content was updated in place via PATCH.
    """
    if cross_identity:
        return _post_cross_identity_reply(requests_module, headers, threads_url, thread_id, new_content)

    url = _append_path_to_url(threads_url, thread_id, "comments", comment_id)
    response = requests_module.patch(url, headers=headers, json={"content": new_content}, timeout=30)
    if response.status_code == 403:
        # Cross-identity ownership — fall back to reply
        return _post_cross_identity_reply(requests_module, headers, threads_url, thread_id, new_content)
    response.raise_for_status()
    return None


def _demote_main_comment(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    thread_id: int,
    comment_id: int,
    new_main_content: str,
    commit_hash: str | None = None,
    commit_url: str | None = None,
) -> int:
    """Read current main comment, post it as reply, PATCH main with new content.

    Steps:
      1. GET the thread to read current main comment content.
      2. POST current content as a reply (preserving it as history).
         The reply header is rewritten from ``## ... Summary`` to
         ``### Commit: ...`` using ``rewrite_header_for_subsequent()``.
      3. PATCH the main comment with ``new_main_content``.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL.
        thread_id: Thread whose main comment is being demoted.
        comment_id: The main comment ID (usually 1).
        new_main_content: New content for the main comment.
        commit_hash: Commit hash for the reply header. When provided,
            the demoted reply uses a compact commit-scoped heading.
        commit_url: Commit URL for the reply header link.

    Returns:
        The comment ID of the newly-created reply (the demoted content).
    """
    # Step 1: Read current main comment content
    comments = _get_thread_comments(requests_module, headers, threads_url, thread_id)
    old_content = ""
    for comment in comments:
        if comment.get("id") == comment_id:
            old_content = comment.get("content", "")
            break

    # Step 2: Post old content as a reply (with header rewritten for subsequent format)
    reply_content = rewrite_header_for_subsequent(old_content, commit_hash, commit_url)
    reply_id = _post_reply(requests_module, headers, threads_url, thread_id, reply_content)

    # Step 3: PATCH main comment with new content.
    # If the identity that created the thread differs from the caller's identity,
    # _patch_comment_content falls back to posting a reply on 403.  Log a warning
    # so callers are aware that the main comment pointer may now be stale.
    patch_fallback_id = _patch_comment_content(
        requests_module, headers, threads_url, thread_id, comment_id, new_main_content
    )
    if patch_fallback_id is not None:
        import sys

        print(
            f"Warning: Could not PATCH main comment {comment_id} in thread {thread_id} "
            f"(cross-identity ownership); new content posted as reply {patch_fallback_id}. "
            "Stored comment ID may be stale.",
            file=sys.stderr,
        )

    return reply_id
