"""Per-commit scaffolding for the consolidated PR review comment.

This is the I/O layer that creates and updates **one consolidated review
comment thread per reviewed commit** (rendered by
:func:`~agentic_devtools.cli.azure_devops.consolidated_review.render_commit_review_comments`).

Architecture overview
---------------------
* **One thread per commit** — each reviewed commit gets its own top-level
  Azure DevOps thread.  The thread id is stored in
  ``ReviewState.overallSummary`` for the current commit and archived into
  ``ReviewState.commitComments`` (keyed by full SHA) when a new commit is
  observed.
* **Continuation replies** — when the fully-rendered content would exceed
  ``SMART_CUTOFF_CHARS`` (50 000 chars), the overflow is posted as ordered
  reply comments within the same thread (``… (continued N)`` payloads).
  ``_reconcile_continuations`` reconciles the live thread replies with the
  rendered list, PATCHing existing continuations in order, POSTing new ones,
  and retiring stale ones; it updates ``continuationCommentIds`` in state.
* **Commit-hash-based recovery** — :func:`find_consolidated_thread` scans
  the PR's existing threads for the ``v2`` consolidated marker to recover a
  thread id after state loss.  It selects the newest (highest-id) comment
  carrying the marker within each thread, and prefers the highest thread id
  when multiple threads qualify.
* **Cross-identity fallback** — when a ``PATCH`` returns 403 (the comment
  was created by a different Azure DevOps identity), the module falls back
  to posting a reply with the updated content so the review stays current.
  The cross-identity fallback is intentionally **not** used for retirement
  of stale continuations (best-effort cleanup only).

This module is part of the live ``agdt-review-pull-request`` scaffolding
flow.  Code suggestions continue to be posted as separate line-anchored
threads; only the summary/file content is consolidated here.

No backwards compatibility: only the ``v2`` consolidated marker is
recognised; legacy ``v1`` per-thread comments are ignored.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import Any

from .config import AzureDevOpsConfig
from .consolidated_review import (
    extract_commit_hash_from_marker,
    extract_continuation_seq_from_marker,
    is_consolidated_comment,
    is_continuation_comment,
    render_commit_review_comments,
)
from .helpers import build_pr_base_url, patch_comment, patch_thread_status, post_thread_reply
from .review_state import CommitComment, ReviewState, compute_aggregate_status


def upsert_consolidated_comment(
    state: ReviewState,
    config: AzureDevOpsConfig,
    repo_id: str,
    requests_module: Any,
    headers: dict[str, str],
    dry_run: bool = False,
    *,
    force_in_progress: bool = False,
) -> ReviewState:
    """Create or update the single consolidated review comment for a PR.

    The consolidated comment lives in one thread tracked by
    ``state.overallSummary`` (``threadId`` / ``commentId``):

    - **First call** (``threadId == 0``): POSTs a new thread with the rendered
      consolidated content and resolves it to ``closed`` so it does not block
      PR completion, then records the new thread/comment ids on *state*.
    - **Subsequent calls**: PATCHes the existing comment in place.

    The rendered content already carries the ``v2`` consolidated marker, so no
    marker is added here.

    This function performs HTTP I/O and mutates *state* in memory; it does **not**
    persist *state* to disk — the caller is responsible for saving.

    Args:
        state: The review state to render and whose ``overallSummary`` tracks
            the consolidated thread.
        config: Azure DevOps configuration.
        repo_id: Repository ID (GUID).
        requests_module: The ``requests`` module (injected for testability).
        headers: Auth headers for API calls.
        dry_run: When ``True``, print the intended action and make no API calls.
        force_in_progress: When ``True``, render the lightweight in-progress
            headline even if every file has a terminal status (forwarded to
            :func:`render_commit_review_comments`). Used by the live progress
            refresh so it never prematurely renders the full content.

    Returns:
        The (possibly mutated) *state*.
    """
    base_url = build_pr_base_url(config, state.prId)
    comments = render_commit_review_comments(state, base_url, force_in_progress=force_in_progress)
    content = comments[0]
    continuations = comments[1:]

    if dry_run:
        action = "create" if state.overallSummary.threadId == 0 else "update"
        print(
            f"[DRY RUN] Would {action} the consolidated review comment for PR {state.prId} "
            f"({len(content)} chars, {len(continuations)} continuation(s))."
        )
        return state

    if state.overallSummary.threadId == 0:
        threads_url = config.build_api_url(repo_id, "pullRequests", state.prId, "threads")
        thread_body = {
            "comments": [{"content": content, "commentType": "text"}],
            "status": "active",
        }
        response = requests_module.post(threads_url, headers=headers, json=thread_body, timeout=30)
        response.raise_for_status()
        result = response.json()
        thread_id = result["id"]
        comment_id = result["comments"][0]["id"]
        state.overallSummary.threadId = thread_id
        state.overallSummary.commentId = comment_id

        # Resolve the informational thread to "closed" so it does not show as an
        # open item / block merge when "All comments must be resolved" is set.
        try:
            patch_thread_status(
                requests_module=requests_module,
                headers=headers,
                config=config,
                repo_id=repo_id,
                pull_request_id=state.prId,
                thread_id=thread_id,
                status="closed",
            )
        except Exception as exc:
            print(f"Warning: Could not resolve thread {thread_id}: {exc}", file=sys.stderr)
    else:
        # Best-effort re-discovery when commentId is invalid (e.g. state was partially
        # saved after a previous cross-identity reply whose id was never recorded).
        if state.overallSummary.commentId <= 0:
            try:
                thread_url = config.build_api_url(
                    repo_id, "pullRequests", state.prId, "threads", state.overallSummary.threadId
                )
                thread_resp = requests_module.get(thread_url, headers=headers, timeout=30)
                thread_resp.raise_for_status()
                non_deleted = [c for c in thread_resp.json().get("comments", []) if not c.get("isDeleted")]
                # Prefer the newest non-deleted comment that carries the v2
                # consolidated marker so cross-identity fallback replies are
                # rediscovered instead of older root comments. Fall back to the
                # first non-deleted comment when no marker comment is found
                # (e.g. a different identity created the thread or the marker
                # was stripped by a later edit).
                marker_comment = _latest_consolidated_comment(non_deleted)
                found = marker_comment or (non_deleted[0] if non_deleted else None)
                if found:
                    state.overallSummary.commentId = int(found["id"])
            except Exception as exc:
                print(
                    f"Warning: Could not re-discover comment id for thread {state.overallSummary.threadId}: {exc}",
                    file=sys.stderr,
                )
            # If re-discovery still left commentId <= 0 (GET failed or returned no comments),
            # fall back to 1 — ADO always assigns id=1 to the first comment in a new thread.
            if state.overallSummary.commentId <= 0:
                state.overallSummary.commentId = 1

        result = patch_comment(
            requests_module=requests_module,
            headers=headers,
            config=config,
            repo_id=repo_id,
            pull_request_id=state.prId,
            thread_id=state.overallSummary.threadId,
            comment_id=state.overallSummary.commentId,
            new_content=content,
            reply_on_forbidden=True,
        )
        # When patch_comment falls back to a cross-identity reply (403), the returned
        # dict is the new reply comment — record its id so the next update targets it
        # instead of the original (forbidden) comment, preventing reply spam.
        new_id = result.get("id")
        if new_id:
            try:
                new_id_int = int(new_id)
                if new_id_int != state.overallSummary.commentId:
                    state.overallSummary.commentId = new_id_int
            except (TypeError, ValueError):
                pass  # Non-numeric id from API; keep current commentId.

    _sync_commit_registry(state)
    _reconcile_continuations(
        state=state,
        config=config,
        repo_id=repo_id,
        requests_module=requests_module,
        headers=headers,
        continuations=continuations,
    )

    return state


def _sync_commit_registry(state: ReviewState) -> None:
    """Mirror the current commit's root thread into ``state.commitComments``.

    Records (or updates) the :class:`CommitComment` entry for
    ``state.commitHash`` and the current model so the "Previous reviews" index
    and re-review routing can find this commit's thread. The first model's
    ``commentId`` is kept in sync with ``overallSummary`` (the thread root).
    """
    commit_hash = state.commitHash
    if not commit_hash:
        return
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = state.commitComments.get(commit_hash)
    if entry is None:
        entry = CommitComment(commitHash=commit_hash)
        state.commitComments[commit_hash] = entry
    entry.threadId = state.overallSummary.threadId
    entry.status = state.overallSummary.status
    entry.timestamp = timestamp

    model_id = state.modelId or "unknown"
    ref = entry.upsert_model(model_id)
    # The current model owns the thread root for now (single-model common case);
    # different-model reply routing is layered on top in review_scaffold.
    if not entry.models or entry.models[0] is ref:
        ref.commentId = state.overallSummary.commentId
    ref.status = compute_aggregate_status([fe.status for fe in state.files.values()])
    ref.timestamp = timestamp


def _reconcile_continuations(
    *,
    state: ReviewState,
    config: AzureDevOpsConfig,
    repo_id: str,
    requests_module: Any,
    headers: dict[str, str],
    continuations: list[str],
) -> None:
    """Create/update/retire continuation reply comments to match the render.

    The rendered review may exceed :data:`SMART_CUTOFF_CHARS` and roll over into
    continuation comments. This reconciles the live thread replies with the
    rendered list:

    - **Extra renders**: PATCH existing continuation replies in order; POST new
      replies for any beyond what is already tracked.
    - **Fewer renders** (e.g. reverting to the lightweight in-progress comment):
      PATCH the now-stale continuation replies to a short tombstone so their
      outdated content no longer appears, while preserving their ids.

    Continuation ids are tracked on the current model's ref in the per-commit
    registry, so recovery and subsequent updates target the same replies.
    """
    commit_hash = state.commitHash
    if not commit_hash:
        return
    entry = state.commitComments.get(commit_hash)
    if entry is None:
        return
    ref = entry.get_model(state.modelId or "unknown")
    if ref is None:
        return
    thread_id = entry.threadId
    if thread_id <= 0:
        return

    existing_ids = list(ref.continuationCommentIds)
    updated_ids: list[int] = []

    for index, payload in enumerate(continuations):
        if index < len(existing_ids):
            comment_id = existing_ids[index]
            result = patch_comment(
                requests_module=requests_module,
                headers=headers,
                config=config,
                repo_id=repo_id,
                pull_request_id=state.prId,
                thread_id=thread_id,
                comment_id=comment_id,
                new_content=payload,
                reply_on_forbidden=True,
            )
            new_id = _coerce_id(result.get("id"))
            updated_ids.append(new_id if new_id else comment_id)
        else:
            result = post_thread_reply(
                requests_module=requests_module,
                headers=headers,
                config=config,
                repo_id=repo_id,
                pull_request_id=state.prId,
                thread_id=thread_id,
                content=payload,
            )
            new_id = _coerce_id(result.get("id"))
            if new_id:
                updated_ids.append(new_id)

    # Retire any continuation replies that are no longer needed by replacing
    # their (now stale) content with a short tombstone. Their ids are kept so we
    # can reuse them if the review grows again.
    # reply_on_forbidden=False: if retirement is blocked by a 403 (cross-identity
    # ownership), we skip the tombstone rather than posting a fallback reply on
    # every run, which would otherwise create unbounded cross-identity replies.
    for stale_id in existing_ids[len(continuations) :]:
        try:
            patch_comment(
                requests_module=requests_module,
                headers=headers,
                config=config,
                repo_id=repo_id,
                pull_request_id=state.prId,
                thread_id=thread_id,
                comment_id=stale_id,
                new_content="*(rolled up into the review above)*",
                reply_on_forbidden=False,
            )
        except Exception as exc:  # pragma: no cover - best effort cleanup
            print(f"Warning: Could not retire continuation comment {stale_id}: {exc}", file=sys.stderr)
        updated_ids.append(stale_id)

    ref.continuationCommentIds = updated_ids


def _coerce_id(value: Any) -> int:
    """Return *value* as a positive int, or 0 when it is missing/non-numeric."""
    try:
        coerced = int(value)
    except (TypeError, ValueError):
        return 0
    return coerced if coerced > 0 else 0


def _latest_consolidated_comment(comments: list[dict]) -> dict | None:
    """Return the newest non-deleted consolidated-marker comment in *comments*."""
    marker_comments = [
        comment
        for comment in comments
        if not comment.get("isDeleted") and is_consolidated_comment(comment.get("content"))
    ]
    if not marker_comments:
        return None
    return max(marker_comments, key=lambda comment: _coerce_id(comment.get("id")))


def _is_newer_thread_candidate(candidate: tuple[int, int], existing: tuple[int, int]) -> bool:
    """Return ``True`` when *candidate* comes from a newer thread/comment pair.

    Tuple ordering is intentional here: thread id is compared first, with
    comment id acting as a deterministic tie-breaker within the same thread.
    """
    return candidate > existing


def find_consolidated_thread(
    threads: list[dict],
    commit_hash: str | None = None,
) -> tuple[int, int] | None:
    """Locate the consolidated review thread for the given commit.

    Scans *threads* for non-deleted threads that contain a non-deleted comment
    carrying the consolidated marker. Within each thread, the newest
    consolidated-marker comment (highest comment id) is selected so cross-
    identity fallback replies are preferred over older root comments. When
    *commit_hash* is provided, returns the thread whose marker embeds that exact
    commit SHA. When no commit-specific match is found — or when *commit_hash*
    is ``None`` — returns the newest consolidated thread (highest thread id) as
    a deterministic fallback.

    With the "one top-level thread per reviewed commit" design, multiple
    consolidated threads can coexist on the same PR, so "first match" is
    deliberately avoided.

    Args:
        threads: PR thread dicts as returned by the Azure DevOps threads API.
        commit_hash: Full commit SHA to prefer (``None`` → newest-thread
            fallback).

    Returns:
        ``(thread_id, comment_id)`` of the consolidated comment, or ``None``
        when no consolidated comment is present.
    """
    candidates: list[tuple[int, int]] = []
    candidates_by_commit: dict[str, tuple[int, int]] = {}

    for thread in threads:
        if thread.get("isDeleted"):
            continue
        comments = thread.get("comments") or []
        comment = _latest_consolidated_comment(comments)
        if comment is not None:
            tid = int(thread["id"])
            cid = int(comment["id"])
            candidate = (tid, cid)
            candidates.append(candidate)
            embedded = extract_commit_hash_from_marker(comment.get("content") or "")
            if embedded and _is_newer_thread_candidate(candidate, candidates_by_commit.get(embedded, (0, 0))):
                candidates_by_commit[embedded] = candidate

    if not candidates:
        return None

    if commit_hash and commit_hash in candidates_by_commit:
        return candidates_by_commit[commit_hash]

    # Fall back to the newest candidate thread.
    return max(candidates)


def find_continuation_comment_ids(thread: dict) -> list[int]:
    """Return ordered continuation reply comment ids within *thread*.

    Scans a single thread dict for non-deleted comments carrying the ``v2``
    continuation marker. When multiple non-deleted comments share the same
    sequence number (which can occur when a cross-identity 403 on a PATCH causes
    ``_reconcile_continuations`` to fall back to posting a new reply rather than
    patching the existing one, leaving the old comment in place alongside the new
    fallback reply), only the comment with the **highest id** for that sequence
    slot is kept. The returned list is sorted by sequence number so the chain is
    always in the correct render order regardless of the API's raw comment
    ordering.

    Args:
        thread: A single PR thread dict as returned by the Azure DevOps threads
            API.

    Returns:
        Continuation comment ids in sequence order (empty when none present).
    """
    # Map seq → best comment id for that slot. When duplicates share the same
    # seq (cross-identity fallback created a second reply for that position),
    # keep the highest comment id (most recent post) so future PATCH attempts
    # target the current comment and the chain remains unambiguous.
    best_by_seq: dict[int, int] = {}
    unsequenced: list[int] = []
    for comment in thread.get("comments") or []:
        if comment.get("isDeleted"):
            continue
        content = comment.get("content")
        if not is_continuation_comment(content):
            continue
        seq = extract_continuation_seq_from_marker(content)
        comment_id = int(comment["id"])
        if seq is None:
            # No seq token — rare/impossible for v2 markers; collect separately
            # and append after sequenced entries so the chain stays predictable.
            unsequenced.append(comment_id)
        elif seq not in best_by_seq or comment_id > best_by_seq[seq]:
            best_by_seq[seq] = comment_id
    return [best_by_seq[seq] for seq in sorted(best_by_seq)] + unsequenced
