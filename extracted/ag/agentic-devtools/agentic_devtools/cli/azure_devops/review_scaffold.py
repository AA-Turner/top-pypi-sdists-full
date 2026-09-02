"""Scaffolding for the consolidated PR review comment.

Creates a single consolidated review thread upfront before the agent begins
reviewing files.  The entire review — overall progress, per-file verdicts
grouped by folder, code suggestions, and the activity log — is rendered into
that one comment and updated in-place (PATCH) as each file is reviewed.

The thread is initially closed after creation to avoid leaving a fresh
informational thread in the active state.  Subsequent cascade updates
(triggered by file-review commands) re-open or close the thread according
to the aggregate review status: ``unreviewed`` / ``in-progress`` /
``needs-work`` → ``active``; ``approved`` → ``closed``.

Code suggestions remain separate line-anchored threads and are also embedded
inline in the consolidated comment so the full review can be reconstructed
from that one thread.

Session management, commit-hash-based idempotency, and incremental
re-scaffolding (new pushes after a partial review) are also handled here.
"""

import sys
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from .config import AzureDevOpsConfig
from .consolidated_review import render_model_review_reply
from .consolidated_scaffold import upsert_consolidated_comment
from .helpers import build_cross_identity_reply_content, build_pr_base_url, patch_thread_status
from .marker import build_marker
from .review_state import (
    CommitComment,
    FileEntry,
    FolderGroup,
    OverallSummary,
    ReviewSession,
    ReviewState,
    ReviewStatus,
    compute_aggregate_status,
    load_review_state,
    normalize_file_path,
    save_review_state,
)
from .review_templates import rewrite_header_for_subsequent
from .suggestion_verification import (
    categorize_all_suggestions,
    fetch_threads_lookup,
    has_unaddressed,
    partition_results,
    render_unaddressed_thread_comment,
)

# Stale session threshold: sessions older than this are considered crashed.
STALE_SESSION_THRESHOLD = timedelta(hours=2)
_DIFF_WARNING_THRESHOLD = 5


def _get_folder_for_path(file_path: str) -> str:
    """Get the top-level folder name for a file path.

    Args:
        file_path: Repository file path (with or without leading slash).

    Returns:
        Top-level folder name, or "root" for root-level files.
    """
    from .review_helpers import get_root_folder

    normalized = normalize_file_path(file_path)
    return get_root_folder(normalized.lstrip("/"))


def _get_file_name(file_path: str) -> str:
    """Get the base file name from a file path.

    Args:
        file_path: Repository file path.

    Returns:
        Base file name (last path segment).
    """
    normalized = normalize_file_path(file_path)
    return normalized.split("/")[-1]


# build_pr_base_url is defined in helpers.py; re-exported here for backward compat.
# _build_pr_base_url is the backward-compatible alias used by internal callers.
_build_pr_base_url = build_pr_base_url


# ---------------------------------------------------------------------------
# FileChangeResult — differential file detection result
# ---------------------------------------------------------------------------


@dataclass
class FileChangeResult:
    """Result of differential file detection between two commits.

    Categorises every file in the PR as new, modified, deleted, or unchanged
    relative to a previous scaffolding run.
    """

    new_files: list[str] = field(default_factory=list)
    modified_files: list[str] = field(default_factory=list)
    deleted_files: list[str] = field(default_factory=list)
    unchanged_files: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Reply / demotion helpers
# ---------------------------------------------------------------------------


def _append_path_to_url(base_url: str, *segments: str | int) -> str:
    """Append path segments to a URL, preserving any query string.

    If ``base_url`` contains a query string (e.g. ``?api-version=7.0``),
    the new segments are inserted before it.  Trailing/leading slashes are
    normalised to avoid double-slash artifacts.

    Args:
        base_url: The base URL (may include a query string).
        *segments: Path segments to append (converted to str).

    Returns:
        URL with segments appended before the query string, or the
        original *base_url* unchanged when no segments are provided.
    """
    if not segments:
        return base_url

    if "?" in base_url:
        path_part, query_part = base_url.split("?", 1)
    else:
        path_part, query_part = base_url, None

    normalized_base = path_part.rstrip("/")
    suffix = "/".join(str(s).strip("/") for s in segments)

    new_path = f"{normalized_base}/{suffix}" if suffix else normalized_base

    if query_part is not None:
        return f"{new_path}?{query_part}"
    return new_path


def _post_reply(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    thread_id: int,
    content: str,
) -> int:
    """Post a reply to an existing thread.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL (without thread ID suffix).
        thread_id: Thread to reply to.
        content: Reply content (markdown).

    Returns:
        The new comment ID.
    """
    url = _append_path_to_url(threads_url, thread_id, "comments")
    body = {"content": content, "commentType": "text"}
    response = requests_module.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return response.json()["id"]


def _post_cross_identity_reply(
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    thread_id: int,
    content: str,
) -> int:
    """Post a cross-identity update reply to an existing thread.

    Used when the original thread comment is owned by a different identity
    and cannot be PATCHed. Posts the full content as a reply prefixed with
    a cross-identity-update marker.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        threads_url: Base threads URL.
        thread_id: Thread to reply to.
        content: Full scaffold content to post.

    Returns:
        The new reply comment ID.
    """
    return _post_reply(requests_module, headers, threads_url, thread_id, build_cross_identity_reply_content(content))


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


# ---------------------------------------------------------------------------
# Activity log helpers
# ---------------------------------------------------------------------------


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
    session: "ReviewSession",
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


# ---------------------------------------------------------------------------
# Session management helpers
# ---------------------------------------------------------------------------


def _resolve_commit_thread_id(existing_state: ReviewState, commit_hash: str | None) -> int:
    """Return the review thread id for *commit_hash*.

    Prefers the per-commit registry entry (``commitComments``) so re-review
    replies land in the dedicated thread for that commit; falls back to the
    overall-summary thread for states that predate the per-commit registry.

    Args:
        existing_state: Current review state.
        commit_hash: Commit hash whose thread is wanted.

    Returns:
        The thread id, or ``0`` when none can be resolved.
    """
    if commit_hash:
        entry = existing_state.commitComments.get(commit_hash)
        if entry is not None and entry.threadId > 0:
            return entry.threadId
    return existing_state.overallSummary.threadId


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


def _build_rereview_skip_message(short_hash: str, model_id: str, pull_request_id: int) -> str:
    """Build the reply posted when a duplicate review is skipped.

    The message explains that the commit was already reviewed by this model and
    provides the ``--force-rereview`` command that overrides the skip and
    re-runs the review, updating the existing comment in place.

    Args:
        short_hash: Short commit hash (first 7 characters).
        model_id: Reviewing model identifier.
        pull_request_id: PR ID (used to build the rerun command).

    Returns:
        Markdown reply content.
    """
    return (
        f"{build_marker('rereview-skipped')}\n"
        f"### 🔁 Re-review requested — skipped\n"
        f"\n"
        f"Another review of commit `{short_hash}` by **{model_id}** was requested, "
        f"but it was **skipped** because this commit has already been reviewed by this model.\n"
        f"\n"
        f"To force a fresh review that overrides this skip and updates the review "
        f"comment in place, run:\n"
        f"\n"
        f"```bash\n"
        f"agdt-initiate-pull-request-review-workflow --pull-request-id {pull_request_id} --force-rereview\n"
        f"```\n"
    )


def _check_session_status(
    existing_state: ReviewState,
    commit_hash: str | None,
    model_id: str,
    now: datetime | None = None,
) -> str:
    """Determine the review session status for a given commit + model.

    Args:
        existing_state: Current review state.
        commit_hash: Current commit hash (may be None).
        model_id: Current model identifier.
        now: Current time (injectable for testing).

    Returns:
        One of: "first_review", "already_reviewed", "in_progress",
        "resume_stale", "different_model", "different_commit".
    """
    if now is None:
        now = datetime.now(UTC)

    # Normalise None → "" for comparison so that two unknown hashes match.
    effective_old = existing_state.commitHash or ""
    effective_new = commit_hash or ""

    if effective_old == effective_new:
        # Filter by both model and commit hash — sessions accumulate across
        # commits, so we must scope to the current commit to avoid false
        # "already_reviewed" from sessions recorded for prior commits.
        current_hash = commit_hash or ""
        matching_sessions = [
            s for s in existing_state.sessions if s.modelId == model_id and (s.commitHash or "") == current_hash
        ]

        # First, prefer any completed session regardless of insertion order.
        for session in matching_sessions:
            if session.status == "completed":
                return "already_reviewed"

        # No completed session; next, look for in-progress sessions.
        has_stale_in_progress = False
        for session in matching_sessions:
            if session.status == "in_progress":
                started = datetime.fromisoformat(session.startedUtc)
                if now - started < STALE_SESSION_THRESHOLD:
                    return "in_progress"
                has_stale_in_progress = True

        if has_stale_in_progress:
            return "resume_stale"

        # No active/completed sessions for this model — check if a different
        # model has sessions *for the current commit*.  Sessions accumulate across
        # commits (audit trail), so we must scope this check to avoid false
        # positives from sessions created for prior commits.
        if any(s.modelId != model_id and (s.commitHash or "") == current_hash for s in existing_state.sessions):
            return "different_model"
        return "first_review"

    # Different commit hash — handled by caller (incremental re-scaffolding)
    return "different_commit"


def _mark_stale_sessions_failed(
    existing_state: ReviewState,
    commit_hash: str,
    model_id: str,
    now: datetime | None = None,
) -> list[ReviewSession]:
    """Mark all stale in-progress sessions as failed for a commit + model.

    Args:
        existing_state: Review state (mutated in-place).
        commit_hash: Current commit hash.
        model_id: Current model identifier.
        now: Current time (injectable for testing).

    Returns:
        Sessions that were transitioned from in_progress to failed.
    """
    if now is None:
        now = datetime.now(UTC)
    transitioned: list[ReviewSession] = []
    for session in existing_state.sessions:
        if (
            session.modelId == model_id
            and session.status == "in_progress"
            and (session.commitHash or "") == (commit_hash or "")
        ):
            started = datetime.fromisoformat(session.startedUtc)
            if now - started >= STALE_SESSION_THRESHOLD:
                session.status = "failed"
                session.completedUtc = now.isoformat()
                transitioned.append(session)
    return transitioned


def _reset_files_for_rereview(existing_state: ReviewState, model_id: str) -> None:
    """Reset every file to ``unreviewed`` for a forced re-review.

    Rotates each file's current suggestions into the ``previousSuggestions``
    audit trail (once per re-review cycle), clears summaries, and resets the
    **forcing model's** verdict so the agent reviews the commit afresh. Other
    models' verdicts are preserved as an audit trail so the "different-model
    reply" semantics remain intact. Mutates *existing_state* in place.

    Args:
        existing_state: Review state to reset (mutated in place).
        model_id: Current model identifier (only this model's verdict is reset).
    """
    for fe in existing_state.files.values():
        if fe.previousSuggestions is None:
            fe.previousSuggestions = list(fe.suggestions)
        elif fe.suggestions:
            fe.previousSuggestions.extend(fe.suggestions)
        fe.suggestions = []
        fe.status = ReviewStatus.UNREVIEWED.value
        fe.summary = None
        fe.modelId = None
        fe.providerType = None
        fe.latencyMs = None
        fe.finishReason = None
        fe.tokensUsed = None
    # All files are now unreviewed — reset the overall status to in-progress so
    # the persisted state is consistent with the rendered headline and so any
    # subsequent archive of this commit records the correct (non-terminal) status.
    existing_state.overallSummary.status = ReviewStatus.IN_PROGRESS.value


def _create_session(
    model_id: str,
    commit_hash: str | None = None,
    now: datetime | None = None,
) -> ReviewSession:
    """Create a new ReviewSession with in_progress status.

    Args:
        model_id: AI model identifier.
        commit_hash: Commit hash this session is reviewing.
        now: Current time (injectable for testing).

    Returns:
        A new ReviewSession.
    """
    if now is None:
        now = datetime.now(UTC)
    return ReviewSession(
        sessionId=uuid.uuid4().hex,
        modelId=model_id,
        startedUtc=now.isoformat(),
        status="in_progress",
        commitHash=commit_hash,
    )


# ---------------------------------------------------------------------------
# Differential file detection
# ---------------------------------------------------------------------------


def detect_file_changes(
    existing_state: ReviewState,
    current_files: list[str],
    config: AzureDevOpsConfig,
    repo_id: str,
    pull_request_id: int,
    old_commit_hash: str,
    new_commit_hash: str,
    requests_module: Any,
    headers: dict[str, str],
) -> FileChangeResult:
    """Detect file changes between two commits for incremental re-scaffolding.

    Primary detection uses the Azure DevOps iterations API. Secondary
    validation uses local ``git diff`` when available.

    Args:
        existing_state: Previous review state.
        current_files: File paths in the new iteration (normalised).
        config: Azure DevOps configuration.
        repo_id: Repository ID (GUID).
        pull_request_id: PR ID.
        old_commit_hash: Previous commit hash.
        new_commit_hash: New commit hash.
        requests_module: requests module for HTTP calls.
        headers: Auth headers.

    Returns:
        FileChangeResult categorising every file.
    """
    existing_file_set = set(existing_state.files.keys())
    current_file_set = {normalize_file_path(f) for f in current_files}

    # Get iteration changes from Azure DevOps
    iteration_changed_files: set = set()
    try:
        # Get latest iteration
        iterations_url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "iterations")
        resp = requests_module.get(iterations_url, headers=headers, timeout=30)
        resp.raise_for_status()
        iterations = resp.json().get("value", [])
        if iterations:
            latest_iteration_id = max(it.get("id", 0) for it in iterations)
            # Get iteration changes
            changes_url = config.build_api_url(
                repo_id, "pullRequests", pull_request_id, "iterations", latest_iteration_id, "changes"
            )
            changes_resp = requests_module.get(changes_url, headers=headers, timeout=30)
            changes_resp.raise_for_status()
            change_entries = changes_resp.json().get("changeEntries", [])
            for entry in change_entries:
                item = entry.get("item", {})
                path = item.get("path", "")
                if path:
                    iteration_changed_files.add(normalize_file_path(path))
    except Exception as exc:
        print(f"Warning: Could not fetch iteration changes: {exc}", file=sys.stderr)

    # Categorise files
    result = FileChangeResult()
    for f in sorted(current_file_set):
        if f not in existing_file_set:
            result.new_files.append(f)
        elif f in iteration_changed_files:
            result.modified_files.append(f)
        else:
            result.unchanged_files.append(f)

    for f in sorted(existing_file_set):
        if f not in current_file_set:
            result.deleted_files.append(f)

    # Secondary validation via git diff
    _validate_with_git_diff(result, old_commit_hash, new_commit_hash, iteration_changed_files, current_file_set)

    return result


def _validate_diff_against_iterations(
    result: FileChangeResult,
    iteration_changed_files: set[str],
    git_changed: set[str],
    current_file_set: set[str],
) -> None:
    """Record every discrepancy and summarize groups larger than five on stderr.

    All individual file warnings are appended to ``result.validation_warnings``.
    Only files in ``current_file_set`` are considered for either comparison.
    """
    # Compare: files in git diff but not in iteration changes
    git_only = sorted((git_changed & current_file_set) - iteration_changed_files)
    for f in git_only:
        msg = f"File {f} changed in git diff but not in iterations API"
        result.validation_warnings.append(msg)
    if len(git_only) <= _DIFF_WARNING_THRESHOLD:
        for f in git_only:
            print(f"Warning: File {f} changed in git diff but not in iterations API", file=sys.stderr)
    else:
        print(f"Warning: {len(git_only)} files changed in git diff but not in iterations API", file=sys.stderr)

    # Compare: files in iteration changes but not in git diff
    iterations_only = sorted((iteration_changed_files & current_file_set) - git_changed)
    for f in iterations_only:
        msg = f"File {f} changed in iterations API but not in git diff"
        result.validation_warnings.append(msg)
    if len(iterations_only) <= _DIFF_WARNING_THRESHOLD:
        for f in iterations_only:
            print(f"Warning: File {f} changed in iterations API but not in git diff", file=sys.stderr)
    else:
        print(
            f"Warning: {len(iterations_only)} files changed in iterations API but not in git diff",
            file=sys.stderr,
        )


def _validate_with_git_diff(
    result: FileChangeResult,
    old_commit_hash: str,
    new_commit_hash: str,
    iteration_changed_files: set,
    current_file_set: set,
) -> None:
    """Cross-validate file changes with local git diff.

    Adds warnings to ``result.validation_warnings`` on discrepancies.
    Always proceeds with the iterations API result as the source of truth.

    Args:
        result: FileChangeResult to add warnings to.
        old_commit_hash: Previous commit hash.
        new_commit_hash: New commit hash.
        iteration_changed_files: Files changed according to iterations API.
        current_file_set: Current file paths in the PR.
    """
    from ..subprocess_utils import run_safe

    try:
        proc = run_safe(
            ["git", "diff", f"{old_commit_hash}..{new_commit_hash}", "--name-only"],
            capture_output=True,
            text=True,
            shell=False,
        )
        if proc.returncode != 0:
            result.validation_warnings.append("git diff unavailable")
            return

        git_changed = {normalize_file_path(line) for line in proc.stdout.strip().splitlines() if line.strip()}

        _validate_diff_against_iterations(result, iteration_changed_files, git_changed, current_file_set)
    except Exception:
        result.validation_warnings.append("git diff unavailable")


def _print_dry_run_plan(
    pull_request_id: int,
    files: list[str],
    folders: dict[str, list[str]],
) -> None:
    """Print the scaffolding plan without making API calls.

    Folder-level threads have been eliminated; file threads, the overall
    PR summary thread, and a Review Activity Log thread are created
    (N + 3 thread-creation POST calls in total; additional non-POST calls
    may be made when initializing the activity log).

    Args:
        pull_request_id: Pull request ID.
        files: List of file paths.
        folders: Mapping of folder name to list of file paths.
    """
    print(f"[DRY RUN] Scaffolding plan for PR {pull_request_id}:")
    for file_path in files:
        normalized = normalize_file_path(file_path)
        print(f"  [DRY RUN] Would create file summary thread for {normalized}")
    for folder_name in folders:
        print(f"  [DRY RUN] Would group files under folder: {folder_name}")
    print("  [DRY RUN] Would create overall PR summary thread")
    print("  [DRY RUN] Would create Review Activity Log thread")
    api_calls = len(files) + 3
    print(f"  [DRY RUN] Total API calls: {api_calls}")


def scaffold_review_threads(
    pull_request_id: int,
    files: list[str],
    config: AzureDevOpsConfig,
    repo_id: str,
    repo_name: str,
    latest_iteration_id: int,
    requests_module: Any,
    headers: dict[str, str],
    dry_run: bool = False,
    commit_hash: str | None = None,
    model_id: str | None = None,
    rebase_conflicts: bool = False,
    force_rereview: bool = False,
) -> ReviewState | None:
    """Scaffold a per-commit consolidated review thread and initialise file state.

    Creates **one top-level Azure DevOps thread per reviewed commit** rather than
    per-file or per-PR threads.  File content is rendered inline within that
    single commit thread (lightweight headline while in progress; full content
    once all files are reviewed).  Code suggestions continue to be posted as
    separate line-anchored threads.

    Commit-hash-based idempotency:
      - Same commit, same model, review complete, no ``force_rereview``
        → skip; post a ``rereview-skipped`` reply on the commit thread.
      - Same commit, same model, review complete, ``force_rereview=True``
        → reset file state to ``unreviewed``, re-render the commit comment
        in place.
      - Same commit, same model, in progress (< 2h) → abort, post warning.
      - Same commit, same model, stale session (≥ 2h) → resume.
      - Same commit, different model → post (or update in place) a
        ``model-review`` reply within the existing commit thread; no
        ``force_rereview`` flag needed.
      - Different commit → archive the prior commit into ``commitComments``
        and POST a fresh thread for the new commit.

    An absent or incomplete state file (``overallSummary.threadId == 0``)
    triggers a full re-scaffold from scratch.

    Args:
        pull_request_id: PR ID.
        files: List of file paths to scaffold threads for.
        config: Azure DevOps configuration.
        repo_id: Repository ID (GUID).
        repo_name: Repository name.
        latest_iteration_id: Latest iteration ID for the PR.
        requests_module: Injected requests module (for testability).
        headers: Auth headers dict.
        dry_run: If True, print the plan without making API calls.
        commit_hash: Commit hash (``lastMergeSourceCommit.commitId``) from
            the Azure DevOps PR API.
        model_id: AI model identifier that initiated scaffolding.
        rebase_conflicts: True if rebase conflicts were detected during checkout.
        force_rereview: When ``True``, override the same-commit/same-model
            skip and re-review from scratch.

    Returns:
        ReviewState with the consolidated thread recorded.  Returns the
        existing state when scaffolding is skipped (already reviewed by the
        same model on the same commit) or when the different-model path
        completes without re-scaffolding.  Returns ``None`` when
        ``dry_run=True`` or when a recent same-model session is already in
        progress (aborted to avoid duplicate reviews).
    """
    effective_model = model_id or "unknown"
    now = datetime.now(UTC)

    # -------------------------------------------------------------------
    # Idempotency check: load existing state and decide on action
    # -------------------------------------------------------------------
    existing_state: ReviewState | None = None
    try:
        existing_state = load_review_state(pull_request_id)
    except FileNotFoundError:
        pass

    if existing_state is not None and existing_state.overallSummary.threadId != 0:
        # Complete state exists — use commit-hash-based idempotency
        status = _check_session_status(existing_state, commit_hash, effective_model, now=now)
        threads_url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads")
        base_url = build_pr_base_url(config, pull_request_id)
        short_hash = (commit_hash or "unknown")[:7]

        # Update rebase-conflict status to reflect the current checkout,
        # regardless of which idempotency path is taken below.  Paths that
        # already call save_review_state() (resume_stale, different_model)
        # will include the updated value automatically; paths that skip
        # saving (already_reviewed, first_review) get an explicit save when
        # the value has changed.
        rebase_conflicts_changed = existing_state.rebaseConflicts != rebase_conflicts
        existing_state.rebaseConflicts = rebase_conflicts

        if status == "already_reviewed" and not force_rereview:
            print(
                f"Commit {short_hash} already reviewed by {effective_model} for PR {pull_request_id}. "
                f"Skipping (pass --force-rereview to override)."
            )
            # Post a skip notice as a reply on the commit's review thread so the
            # reviewer can see why nothing happened and how to force a re-review.
            if not dry_run:
                commit_thread_id = _resolve_commit_thread_id(existing_state, commit_hash)
                if commit_thread_id > 0:
                    try:
                        _post_reply(
                            requests_module,
                            headers,
                            threads_url,
                            commit_thread_id,
                            _build_rereview_skip_message(short_hash, effective_model, pull_request_id),
                        )
                    except Exception as exc:
                        print(f"Warning: Could not post re-review skip notice: {exc}", file=sys.stderr)
            if rebase_conflicts_changed and not dry_run:
                save_review_state(existing_state)
            return existing_state

        if status == "already_reviewed" and force_rereview:
            # Forced re-review: reset this commit's files to unreviewed (rotating
            # any suggestions into the audit trail), open a fresh session, and
            # re-render the existing comment in place so the agent reviews again.
            print(
                f"Force re-review requested for commit {short_hash} by {effective_model} "
                f"(PR {pull_request_id}); resetting review state and updating the comment in place."
            )
            if dry_run:
                return existing_state
            _reset_files_for_rereview(existing_state, effective_model)
            session = _create_session(effective_model, commit_hash=commit_hash, now=now)
            existing_state.sessions.append(session)
            try:
                upsert_consolidated_comment(
                    state=existing_state,
                    config=config,
                    repo_id=repo_id,
                    requests_module=requests_module,
                    headers=headers,
                )
            except Exception as exc:
                print(f"Warning: Could not update consolidated review comment: {exc}", file=sys.stderr)
            save_review_state(existing_state)
            return existing_state

        if status == "in_progress":
            # Find the active session for the warning message
            active_session = None
            for s in existing_state.sessions:
                if (
                    s.modelId == effective_model
                    and s.status == "in_progress"
                    and (s.commitHash or "") == (commit_hash or "")
                ):
                    active_session = s
                    break
            active_id = active_session.sessionId if active_session else "unknown"
            active_start = active_session.startedUtc if active_session else "unknown"
            print(
                f"Review already in progress for commit {short_hash} by {effective_model} "
                f"(session {active_id}). Aborting.",
            )
            if not dry_run and existing_state.activityLogThreadId:
                seq = len(existing_state.sessions) + 1
                detail = (
                    f"A review session is currently in progress "
                    f"(session `{active_id}` started at {active_start}). Aborting."
                )
                entry = _format_activity_log_entry(
                    "⚠️",
                    "In Progress",
                    now.isoformat(),
                    effective_model,
                    short_hash,
                    "n/a",
                    detail,
                    seq,
                )
                try:
                    _post_activity_log_entry(
                        requests_module,
                        headers,
                        threads_url,
                        existing_state.activityLogThreadId,
                        entry,
                    )
                except Exception as exc:
                    print(f"Warning: Could not post activity log entry: {exc}", file=sys.stderr)
            if rebase_conflicts_changed and not dry_run:
                save_review_state(existing_state)
            return None

        if status == "resume_stale":
            reviewed = sum(1 for fe in existing_state.files.values() if fe.status != ReviewStatus.UNREVIEWED.value)
            total = len(existing_state.files)
            print(f"Resuming stale review session for PR {pull_request_id} ({reviewed}/{total} files reviewed).")
            if dry_run:
                return existing_state

            transitioned_sessions = _mark_stale_sessions_failed(
                existing_state,
                commit_hash or "",
                effective_model,
                now=now,
            )
            # Update activity log comments for sessions just marked failed
            if existing_state.activityLogThreadId:
                for s in transitioned_sessions:
                    if s.activityLogCommentId is not None:
                        try:
                            seq_idx = existing_state.sessions.index(s) + 1
                            fallback_id = _update_activity_log_comment_status(
                                requests_module,
                                headers,
                                threads_url,
                                existing_state.activityLogThreadId,
                                s.activityLogCommentId,
                                "❌",
                                "Failed",
                                s,
                                commit_hash,
                                seq_idx,
                                "Session timed out (stale).",
                            )
                            if fallback_id is not None:
                                s.activityLogCommentId = fallback_id
                        except Exception as exc:
                            print(f"Warning: Could not update activity log for failed session: {exc}", file=sys.stderr)
            stale_id = "unknown"
            if transitioned_sessions:
                stale_id = transitioned_sessions[-1].sessionId
            else:
                for s in reversed(existing_state.sessions):
                    if (
                        s.modelId == effective_model
                        and s.status == "failed"
                        and (s.commitHash or "") == (commit_hash or "")
                    ):
                        stale_id = s.sessionId
                        break
            new_session = _create_session(effective_model, commit_hash=commit_hash, now=now)
            existing_state.sessions.append(new_session)
            save_review_state(existing_state)
            if existing_state.activityLogThreadId:
                seq = len(existing_state.sessions)
                detail = f"Resuming incomplete review session `{stale_id}` ({reviewed}/{total} files reviewed)."
                entry = _format_activity_log_entry(
                    "🔄",
                    "Resuming",
                    now.isoformat(),
                    effective_model,
                    short_hash,
                    new_session.sessionId,
                    detail,
                    seq,
                )
                try:
                    reply_id = _post_activity_log_entry(
                        requests_module,
                        headers,
                        threads_url,
                        existing_state.activityLogThreadId,
                        entry,
                    )
                    new_session.activityLogCommentId = reply_id
                    save_review_state(existing_state)
                except Exception as exc:
                    print(f"Warning: Could not post activity log entry: {exc}", file=sys.stderr)
            return existing_state

        if status == "different_model":
            print(f"Additional reviewer ({effective_model}) joining review for PR {pull_request_id}.")
            if dry_run:
                return existing_state
            new_session = _create_session(effective_model, commit_hash=commit_hash, now=now)
            existing_state.sessions.append(new_session)
            save_review_state(existing_state)
            # Post the additional model's review as a reply within the commit's
            # existing review thread (no --force-rereview needed). Re-runs of the
            # same additional model update this reply in place.
            try:
                _post_or_update_model_reply(
                    requests_module,
                    headers,
                    threads_url,
                    existing_state,
                    commit_hash,
                    effective_model,
                    base_url,
                    now,
                )
                save_review_state(existing_state)
            except Exception as exc:
                print(f"Warning: Could not post additional-model review reply: {exc}", file=sys.stderr)
            if existing_state.activityLogThreadId:
                seq = len(existing_state.sessions)
                entry = _format_activity_log_entry(
                    "🤝",
                    "Additional Reviewer",
                    now.isoformat(),
                    effective_model,
                    short_hash,
                    new_session.sessionId,
                    "Additional reviewer joining existing review for this commit.",
                    seq,
                )
                try:
                    reply_id = _post_activity_log_entry(
                        requests_module,
                        headers,
                        threads_url,
                        existing_state.activityLogThreadId,
                        entry,
                    )
                    new_session.activityLogCommentId = reply_id
                    save_review_state(existing_state)
                except Exception as exc:
                    print(f"Warning: Could not post activity log entry: {exc}", file=sys.stderr)
            return existing_state

        if status == "different_commit":
            # Incremental re-scaffolding
            return _incremental_rescaffold(
                existing_state=existing_state,
                pull_request_id=pull_request_id,
                files=files,
                config=config,
                repo_id=repo_id,
                repo_name=repo_name,
                latest_iteration_id=latest_iteration_id,
                requests_module=requests_module,
                headers=headers,
                dry_run=dry_run,
                commit_hash=commit_hash,
                model_id=effective_model,
                now=now,
                rebase_conflicts=rebase_conflicts,
            )

        # status == "first_review" — same commit, no sessions recorded.
        # If the state is already complete (all threads exist), skip scaffolding.
        # This is the backward-compat path for states created before session
        # tracking was introduced.
        if status == "first_review":
            print(f"Scaffolding already exists for PR {pull_request_id}. Skipping.")
            if rebase_conflicts_changed and not dry_run:
                save_review_state(existing_state)
            return existing_state

    elif existing_state is not None and existing_state.overallSummary.threadId == 0:
        print(f"Incomplete scaffolding detected for PR {pull_request_id}. Re-scaffolding from scratch.")

    # -------------------------------------------------------------------
    # First-time scaffolding (or incomplete state re-scaffold)
    # -------------------------------------------------------------------
    # Before creating new threads, check if the PR already has agdt-marker
    # threads (e.g., from a prior review session whose state.json was lost).
    # If found, recover state from them to avoid creating duplicate threads.
    if not dry_run:
        recovered = _try_recover_state_from_pr_threads(
            pull_request_id=pull_request_id,
            files=files,
            config=config,
            repo_id=repo_id,
            repo_name=repo_name,
            latest_iteration_id=latest_iteration_id,
            requests_module=requests_module,
            headers=headers,
            commit_hash=commit_hash,
            model_id=effective_model,
            now=now,
            rebase_conflicts=rebase_conflicts,
        )
        if recovered is not None:
            return recovered

    return _fresh_scaffold(
        pull_request_id=pull_request_id,
        files=files,
        config=config,
        repo_id=repo_id,
        repo_name=repo_name,
        latest_iteration_id=latest_iteration_id,
        requests_module=requests_module,
        headers=headers,
        dry_run=dry_run,
        commit_hash=commit_hash,
        model_id=effective_model,
        now=now,
        rebase_conflicts=rebase_conflicts,
    )


# ---------------------------------------------------------------------------
# Internal: recover state from existing PR threads (duplicate prevention)
# ---------------------------------------------------------------------------


def _try_recover_state_from_pr_threads(
    pull_request_id: int,
    files: list[str],
    config: AzureDevOpsConfig,
    repo_id: str,
    repo_name: str,
    latest_iteration_id: int,
    requests_module: Any,
    headers: dict[str, str],
    commit_hash: str | None,
    model_id: str,
    now: datetime | None = None,
    rebase_conflicts: bool = False,
) -> ReviewState | None:
    """Attempt to recover review state from existing agdt-marker threads on the PR.

    When ``review-state.json`` is missing (e.g., different worktree scope or
    state directory was cleaned), this function fetches all threads from the PR,
    filters for agdt-review markers, and reconstructs a ReviewState from them.
    This prevents creating duplicate scaffold threads.

    Args:
        (same as scaffold_review_threads)

    Returns:
        Recovered ReviewState if agdt threads were found on the PR, else None.
    """
    if now is None:
        now = datetime.now(UTC)

    from .consolidated_scaffold import find_consolidated_thread

    threads_url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads")

    try:
        response = requests_module.get(threads_url, headers=headers, timeout=30)
        response.raise_for_status()
        all_threads = response.json().get("value", [])
    except Exception as exc:
        print(f"Warning: Could not fetch PR threads for recovery check: {exc}", file=sys.stderr)
        return None

    found = find_consolidated_thread(all_threads, commit_hash=commit_hash)
    if found is None:
        # No existing consolidated comment (v2) on the PR — nothing to recover.
        # Legacy v1 per-thread comments are intentionally ignored.
        return None

    consolidated_thread_id, consolidated_comment_id = found
    print(
        f"Found existing consolidated review comment (thread {consolidated_thread_id}) "
        f"on the PR (any identity). Reusing it instead of creating a new one."
    )

    # Rebuild file entries (all reset to unreviewed). Per-file content is rendered
    # inline in the single consolidated comment, so no per-file threads exist.
    file_entries: dict[str, FileEntry] = {}
    for file_path in files:
        normalized = normalize_file_path(file_path)
        file_entry = FileEntry(
            threadId=0,
            commentId=0,
            folder=_get_folder_for_path(file_path),
            fileName=_get_file_name(file_path),
            status=ReviewStatus.UNREVIEWED.value,
        )
        file_entries[normalized] = file_entry

    # Build folder groups
    folders: dict[str, list[str]] = {}
    for file_path in files:
        folder = _get_folder_for_path(file_path)
        normalized = normalize_file_path(file_path)
        folders.setdefault(folder, []).append(normalized)
    folder_groups = {k: FolderGroup(files=v) for k, v in folders.items()}

    # Create session
    session = _create_session(model_id, commit_hash=commit_hash, now=now)

    # Build recovered state pointing at the existing consolidated comment.
    recovered_state = ReviewState(
        prId=pull_request_id,
        repoId=repo_id,
        repoName=repo_name,
        project=config.project,
        organization=config.organization,
        latestIterationId=latest_iteration_id,
        scaffoldedUtc=now.isoformat(),
        overallSummary=OverallSummary(threadId=consolidated_thread_id, commentId=consolidated_comment_id),
        folders=folder_groups,
        files=file_entries,
        commitHash=commit_hash,
        modelId=model_id,
        activityLogThreadId=0,
        sessions=[session],
        rebaseConflicts=rebase_conflicts,
    )

    # Do NOT call upsert_consolidated_comment here.  Recovery only reuses the
    # thread/comment IDs so future file-review PATCH calls target the correct
    # thread; it must not overwrite the existing consolidated comment content,
    # because recovered_state has all files reset to "unreviewed" and a PATCH at
    # this point would permanently erase review history that is still visible on
    # the PR.
    save_review_state(recovered_state)

    return recovered_state


# ---------------------------------------------------------------------------
# Internal: first-time full scaffolding
# ---------------------------------------------------------------------------


def _fresh_scaffold(
    pull_request_id: int,
    files: list[str],
    config: AzureDevOpsConfig,
    repo_id: str,
    repo_name: str,
    latest_iteration_id: int,
    requests_module: Any,
    headers: dict[str, str],
    dry_run: bool,
    commit_hash: str | None,
    model_id: str,
    now: datetime | None = None,
    rebase_conflicts: bool = False,
) -> ReviewState | None:
    """Perform a first-time full scaffolding of all review threads.

    Creates file threads, overall summary, activity log thread, and
    the initial session record.

    Args:
        (same as scaffold_review_threads)

    Returns:
        ReviewState, or None in dry-run mode.
    """
    if now is None:
        now = datetime.now(UTC)

    # Group files by top-level folder
    folders: dict[str, list[str]] = {}
    for file_path in files:
        folder = _get_folder_for_path(file_path)
        normalized = normalize_file_path(file_path)
        folders.setdefault(folder, []).append(normalized)

    if dry_run:
        _print_dry_run_plan(pull_request_id, files, folders)
        return None

    scaffolded_utc = now.isoformat()

    # Create initial session
    session = _create_session(model_id, commit_hash=commit_hash, now=now)

    def _build_state(
        file_entries: dict[str, FileEntry],
        folder_groups: dict[str, FolderGroup],
        overall_thread_id: int = 0,
        overall_comment_id: int = 0,
        activity_log_thread_id: int = 0,
    ) -> ReviewState:
        return ReviewState(
            prId=pull_request_id,
            repoId=repo_id,
            repoName=repo_name,
            project=config.project,
            organization=config.organization,
            latestIterationId=latest_iteration_id,
            scaffoldedUtc=scaffolded_utc,
            overallSummary=OverallSummary(threadId=overall_thread_id, commentId=overall_comment_id),
            folders=folder_groups,
            files=file_entries,
            commitHash=commit_hash,
            modelId=model_id,
            activityLogThreadId=activity_log_thread_id,
            sessions=[session],
            rebaseConflicts=rebase_conflicts,
        )

    # Build file entries WITHOUT per-file threads. In the consolidated review
    # model there is a single review comment (tracked by overallSummary); each
    # file's status/summary/suggestions are rendered inline in that one comment,
    # so file-summary threads are no longer created (threadId/commentId stay 0).
    file_entries: dict[str, FileEntry] = {}
    for file_path in files:
        normalized = normalize_file_path(file_path)
        folder = _get_folder_for_path(file_path)
        file_name = _get_file_name(file_path)
        file_entry = FileEntry(
            threadId=0,
            commentId=0,
            folder=folder,
            fileName=file_name,
            status=ReviewStatus.UNREVIEWED.value,
        )
        file_entries[normalized] = file_entry

    # Build lightweight folder groups
    folder_groups: dict[str, FolderGroup] = {}
    for folder_name, folder_files in folders.items():
        folder_groups[folder_name] = FolderGroup(files=folder_files)

    # Create the single consolidated review comment. This POSTs one thread,
    # records its thread/comment ids on overallSummary, and initially resolves it
    # to "closed" to avoid leaving a fresh informational thread in the active
    # (merge-blocking) state. Note: subsequent cascade updates from file verdicts
    # may change the thread status: "unreviewed", "in-progress", and "needs-work"
    # set it back to "active" (merge-blocking), while "approved" keeps it "closed".
    # The activity log and per-file detail are rendered inline from state, so no
    # separate activity-log or file-summary threads are created.
    review_state = _build_state(file_entries, folder_groups)
    upsert_consolidated_comment(
        state=review_state,
        config=config,
        repo_id=repo_id,
        requests_module=requests_module,
        headers=headers,
        dry_run=False,
    )
    save_review_state(review_state)

    print(f"Scaffolding complete. Review state saved for PR {pull_request_id}.")
    return review_state


# ---------------------------------------------------------------------------
# Internal: resolve all scaffold threads to "closed" status
# ---------------------------------------------------------------------------


def _resolve_scaffold_threads(
    requests_module: Any,
    headers: dict[str, str],
    config: AzureDevOpsConfig,
    repo_id: str,
    pull_request_id: int,
    file_entries: dict[str, FileEntry],
    overall_thread_id: int,
    activity_log_thread_id: int,
) -> None:
    """Resolve all scaffold threads so they don't block PR merging.

    All scaffold threads (file summary, overall summary, activity log) are
    informational and should be in "closed" status.  They get updated via
    PATCH as the review progresses but should never block merge.

    Args:
        requests_module: requests module for HTTP calls.
        headers: Auth headers.
        config: Azure DevOps configuration.
        repo_id: Repository ID.
        pull_request_id: PR ID.
        file_entries: Dict of file path to FileEntry (for thread IDs).
        overall_thread_id: Overall summary thread ID.
        activity_log_thread_id: Activity log thread ID.
    """
    thread_ids_to_resolve = []

    # Collect file thread IDs
    for fe in file_entries.values():
        if fe.threadId:
            thread_ids_to_resolve.append(fe.threadId)

    # Overall summary thread
    if overall_thread_id:
        thread_ids_to_resolve.append(overall_thread_id)

    # Activity log thread
    if activity_log_thread_id:
        thread_ids_to_resolve.append(activity_log_thread_id)

    for thread_id in thread_ids_to_resolve:
        try:
            patch_thread_status(
                requests_module=requests_module,
                headers=headers,
                config=config,
                repo_id=repo_id,
                pull_request_id=pull_request_id,
                thread_id=thread_id,
                status="closed",
            )
        except Exception as exc:
            print(f"Warning: Could not resolve thread {thread_id}: {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Internal: incremental re-scaffolding on new commit
# ---------------------------------------------------------------------------


def _archive_commit_thread(
    state: ReviewState,
    old_commit_hash: str,
    now: datetime | None = None,
) -> None:
    """Archive the just-reviewed commit's thread, then reset the comment pointer.

    Implements the *new top-level thread per reviewed commit* model: before a
    new commit is rendered, the prior commit's consolidated thread is recorded
    in :attr:`ReviewState.commitComments` (so it appears in the "Previous
    reviews" index with a jump link), and ``overallSummary`` is reset to
    ``threadId == 0`` so the next :func:`upsert_consolidated_comment` call POSTs
    a brand-new thread for the incoming commit instead of patching the old one.

    Args:
        state: The review state being re-scaffolded for a new commit.
        old_commit_hash: The commit hash whose thread is being archived.
        now: Current time used to stamp the archived entry's timestamp fields.
            Defaults to ``datetime.now(UTC)`` when omitted.
    """
    if now is None:
        now = datetime.now(UTC)

    entry = state.commitComments.get(old_commit_hash)
    if entry is None:
        entry = CommitComment(commitHash=old_commit_hash)
        state.commitComments[old_commit_hash] = entry

    if state.overallSummary.threadId:
        entry.threadId = state.overallSummary.threadId
        entry.status = state.overallSummary.status
        entry.timestamp = now.isoformat()
        model_id = state.modelId or "unknown"
        ref = entry.upsert_model(model_id)
        # The archived commit's first model owns the thread root comment.
        if not entry.models or entry.models[0] is ref:
            ref.commentId = state.overallSummary.commentId
        ref.status = compute_aggregate_status([fe.status for fe in state.files.values()])
        ref.timestamp = now.isoformat()

    # Reset the consolidated-comment pointer so a fresh thread is created for
    # the incoming commit.
    state.overallSummary.threadId = 0
    state.overallSummary.commentId = 0
    state.overallSummary.status = ReviewStatus.IN_PROGRESS.value


def _incremental_rescaffold(
    existing_state: ReviewState,
    pull_request_id: int,
    files: list[str],
    config: AzureDevOpsConfig,
    repo_id: str,
    repo_name: str,
    latest_iteration_id: int,
    requests_module: Any,
    headers: dict[str, str],
    dry_run: bool,
    commit_hash: str | None,
    model_id: str,
    now: datetime | None = None,
    rebase_conflicts: bool = False,
) -> ReviewState | None:
    """Perform incremental re-scaffolding for a new commit.

    Detects file changes between old and new commit, then:
      - New files: scaffold new threads.
      - Modified files: demote old comment, re-scaffold with fresh unreviewed.
      - Deleted files: demote old comment, mark as removed.
      - Unchanged files: no action.
    Updates folder groups, overall summary, and posts activity log entry.

    Args:
        (same as scaffold_review_threads + existing_state)

    Returns:
        Updated ReviewState, or None in dry-run mode.
    """
    if now is None:
        now = datetime.now(UTC)

    old_commit_hash = existing_state.commitHash or ""
    short_new_hash = (commit_hash or "unknown")[:7]

    threads_url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads")

    normalised_files = [normalize_file_path(f) for f in files]

    changes = detect_file_changes(
        existing_state,
        normalised_files,
        config,
        repo_id,
        pull_request_id,
        old_commit_hash,
        commit_hash or "",
        requests_module,
        headers,
    )

    n_new = len(changes.new_files)
    n_mod = len(changes.modified_files)
    n_del = len(changes.deleted_files)
    n_unch = len(changes.unchanged_files)

    print(
        f"Incremental re-scaffolding for PR {pull_request_id}: "
        f"{n_new} new, {n_mod} modified, {n_del} deleted, {n_unch} unchanged files."
    )

    # -------------------------------------------------------------------
    # Suggestion verification gate
    # -------------------------------------------------------------------
    files_with_previous = {
        fp: fe.previousSuggestions for fp, fe in existing_state.files.items() if fe.previousSuggestions
    }
    if files_with_previous and not dry_run:
        threads_lookup = fetch_threads_lookup(requests_module, headers, threads_url)
        if threads_lookup is not None:
            changed_set = frozenset(changes.new_files + changes.modified_files + changes.deleted_files)
            verification_results = categorize_all_suggestions(files_with_previous, changed_set, threads_lookup)
            if verification_results:
                unaddressed_list, needs_review_list = partition_results(verification_results)
                if has_unaddressed(verification_results):
                    # Reflect the new head commit in the consolidated marker/content
                    # before re-rendering the blocked state comment.
                    existing_state.commitHash = commit_hash
                    # --- Abort gate: post comments on unaddressed threads ---
                    for r in unaddressed_list:
                        try:
                            _post_reply(
                                requests_module,
                                headers,
                                threads_url,
                                r.suggestion.threadId,
                                render_unaddressed_thread_comment(short_new_hash),
                            )
                        except Exception as exc:
                            print(
                                f"Warning: Could not post unaddressed comment on thread {r.suggestion.threadId}: {exc}",
                                file=sys.stderr,
                            )

                    # Re-render the single consolidated review comment to reflect
                    # the blocked state. The unaddressed suggestions are also posted
                    # as replies on their own line-anchored threads above.
                    try:
                        upsert_consolidated_comment(
                            state=existing_state,
                            config=config,
                            repo_id=repo_id,
                            requests_module=requests_module,
                            headers=headers,
                        )
                    except Exception as exc:
                        print(f"Warning: Could not update consolidated review comment: {exc}", file=sys.stderr)

                    # Record abort-gated session unconditionally (consistent with
                    # resume_stale and different_model paths which always create a
                    # session regardless of activityLogThreadId).
                    n_unaddr = len(unaddressed_list)
                    session = _create_session(model_id, commit_hash=commit_hash, now=now)
                    # Mark this abort-gated session as a terminal failure so it is not treated
                    # as an in-progress or resumable session by _check_session_status().
                    session.status = "failed"
                    session.completedUtc = now.isoformat()
                    existing_state.sessions.append(session)

                    # Post activity log entry (only if activity log thread exists)
                    if existing_state.activityLogThreadId:
                        seq = len(existing_state.sessions)
                        detail = f"Review blocked: {n_unaddr} unaddressed suggestion(s)."
                        entry = _format_activity_log_entry(
                            "⛔",
                            "Blocked",
                            now.isoformat(),
                            model_id,
                            short_new_hash,
                            session.sessionId,
                            detail,
                            seq,
                        )
                        try:
                            reply_id = _post_activity_log_entry(
                                requests_module,
                                headers,
                                threads_url,
                                existing_state.activityLogThreadId,
                                entry,
                            )
                            session.activityLogCommentId = reply_id
                        except Exception as exc:
                            print(f"Warning: Could not post activity log: {exc}", file=sys.stderr)

                    save_review_state(existing_state)
                    print(
                        f"⛔ Review blocked: {n_unaddr} unaddressed suggestion(s). Address them and push a new commit."
                    )
                    return existing_state

                # All are needs_review — set verification status on affected files
                for r in needs_review_list:
                    fe = existing_state.files.get(r.file_path)
                    if fe:
                        fe.suggestionVerificationStatus = "pending_verification"
        else:
            print("Warning: Could not fetch PR threads for verification. Proceeding.", file=sys.stderr)

    if dry_run:
        print(f"[DRY RUN] Would re-scaffold PR {pull_request_id} for commit {short_new_hash}")
        for f in changes.new_files:
            print(f"  [DRY RUN] New file: {f}")
        for f in changes.modified_files:
            print(f"  [DRY RUN] Modified file: {f}")
        for f in changes.deleted_files:
            print(f"  [DRY RUN] Deleted file: {f}")
        for f in changes.unchanged_files:
            print(f"  [DRY RUN] Unchanged file: {f}")
        return None

    # Process new files — add inline file entries (no per-file thread).
    for file_path in changes.new_files:
        folder = _get_folder_for_path(file_path)
        file_name = _get_file_name(file_path)
        new_file_entry = FileEntry(
            threadId=0,
            commentId=0,
            folder=folder,
            fileName=file_name,
            status=ReviewStatus.UNREVIEWED.value,
        )
        existing_state.files[file_path] = new_file_entry

    # Process modified files — reset their inline state for re-review.
    for file_path in changes.modified_files:
        fe = existing_state.files.get(file_path)
        if fe:
            # Reset file state (rotate suggestions to the audit trail)
            if fe.previousSuggestions is None:
                fe.previousSuggestions = list(fe.suggestions)
            elif fe.suggestions:
                fe.previousSuggestions.extend(fe.suggestions)
            fe.suggestions = []
            fe.status = ReviewStatus.UNREVIEWED.value
            fe.summary = None
            fe.modelId = None
            fe.providerType = None
            fe.latencyMs = None
            fe.finishReason = None
            fe.tokensUsed = None

    # Process deleted files — mark resolved inline.
    for file_path in changes.deleted_files:
        fe = existing_state.files.get(file_path)
        if fe:
            fe.status = ReviewStatus.APPROVED.value
            fe.summary = "File removed"

    # Update folder groups
    all_current_files = set(changes.new_files + changes.modified_files + changes.unchanged_files)
    new_folders: dict[str, list[str]] = {}
    for f in sorted(all_current_files):
        folder = _get_folder_for_path(f)
        new_folders.setdefault(folder, []).append(f)
    # Keep existing empty folder groups for deleted files
    for folder_name in existing_state.folders:
        if folder_name not in new_folders:
            new_folders[folder_name] = []
    existing_state.folders = {k: FolderGroup(files=v) for k, v in new_folders.items()}

    # Update commit hash, iteration, and rebase conflict status.
    # rebaseConflicts must be set before rendering the consolidated comment so the
    # warning banner is included in the posted comment.
    #
    # New top-level thread per reviewed commit: archive the prior commit's thread
    # into the per-commit registry and reset the comment pointer so the upsert
    # below POSTs a fresh thread for the new commit instead of patching the old.
    # Guard: only archive and update commitHash when commit_hash is a real value;
    # when it is None (hash unknown), preserve the existing commitHash and skip
    # the archive to avoid creating an unassociated per-commit thread.
    if commit_hash:
        if old_commit_hash and old_commit_hash != commit_hash:
            _archive_commit_thread(existing_state, old_commit_hash, now=now)
        existing_state.commitHash = commit_hash
    existing_state.modelId = model_id or existing_state.modelId
    existing_state.latestIterationId = latest_iteration_id
    existing_state.rebaseConflicts = rebase_conflicts

    # Re-render the single consolidated review comment to reflect the new commit
    # (changed files reset to unreviewed, suggestions rotated, status recomputed).
    try:
        upsert_consolidated_comment(
            state=existing_state,
            config=config,
            repo_id=repo_id,
            requests_module=requests_module,
            headers=headers,
        )
    except Exception as exc:
        print(f"Warning: Could not update consolidated review comment: {exc}", file=sys.stderr)

    # Create new session
    session = _create_session(model_id, commit_hash=commit_hash, now=now)
    existing_state.sessions.append(session)

    save_review_state(existing_state)

    # Post activity log entry
    if existing_state.activityLogThreadId:
        seq = len(existing_state.sessions)
        if n_new == 0 and n_mod == 0 and n_del == 0:
            detail = "New commit detected (rebase). No file content changes. Previous review preserved."
            emoji, status_text = "🔁", "Rebase"
        else:
            detail = (
                f"New commit detected. Incremental re-scaffolding: "
                f"{n_new} new, {n_mod} modified, {n_del} deleted, {n_unch} unchanged files."
            )
            emoji, status_text = "🔀", "New Commit"
        entry = _format_activity_log_entry(
            emoji,
            status_text,
            now.isoformat(),
            model_id,
            short_new_hash,
            session.sessionId,
            detail,
            seq,
        )
        try:
            reply_id = _post_activity_log_entry(
                requests_module,
                headers,
                threads_url,
                existing_state.activityLogThreadId,
                entry,
            )
            session.activityLogCommentId = reply_id
            save_review_state(existing_state)
        except Exception as exc:
            print(f"Warning: Could not post activity log entry: {exc}", file=sys.stderr)

    print(f"Incremental re-scaffolding complete for PR {pull_request_id}.")
    return existing_state
