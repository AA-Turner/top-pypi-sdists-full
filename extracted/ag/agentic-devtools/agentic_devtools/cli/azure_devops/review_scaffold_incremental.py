"""Incrementally update review state for a new pull-request commit."""

import sys
from datetime import UTC, datetime
from typing import Any

from .config import AzureDevOpsConfig
from .consolidated_scaffold import upsert_consolidated_comment
from .review_scaffold_activity import _format_activity_log_entry, _post_activity_log_entry
from .review_scaffold_changes import detect_file_changes
from .review_scaffold_commit_state import _archive_commit_thread
from .review_scaffold_helpers import _get_file_name, _get_folder_for_path
from .review_scaffold_replies import _post_reply
from .review_scaffold_session_state import _create_session
from .review_state import FileEntry, FolderGroup, ReviewState, ReviewStatus, normalize_file_path, save_review_state
from .suggestion_verification import (
    categorize_all_suggestions,
    fetch_threads_lookup,
    has_unaddressed,
    partition_results,
    render_unaddressed_thread_comment,
)


def _record_blocked_suggestion_review(
    existing_state: ReviewState,
    unaddressed_list: list[Any],
    config: AzureDevOpsConfig,
    repo_id: str,
    model_id: str,
    commit_hash: str | None,
    now: datetime,
    short_new_hash: str,
    threads_url: str,
    requests_module: Any,
    headers: dict[str, str],
) -> None:
    """Persist the blocked session and its unaddressed-suggestion replies."""
    existing_state.commitHash = commit_hash
    for result in unaddressed_list:
        try:
            _post_reply(
                requests_module,
                headers,
                threads_url,
                result.suggestion.threadId,
                render_unaddressed_thread_comment(short_new_hash),
            )
        except Exception as exc:
            print(
                f"Warning: Could not post unaddressed comment on thread {result.suggestion.threadId}: {exc}",
                file=sys.stderr,
            )

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

    n_unaddr = len(unaddressed_list)
    session = _create_session(model_id, commit_hash=commit_hash, now=now)
    session.status = "failed"
    session.completedUtc = now.isoformat()
    existing_state.sessions.append(session)

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
    print(f"⛔ Review blocked: {n_unaddr} unaddressed suggestion(s). Address them and push a new commit.")


def _verify_suggestions_before_rescaffold(
    existing_state: ReviewState,
    changes: Any,
    dry_run: bool,
    commit_hash: str | None,
    model_id: str,
    now: datetime,
    short_new_hash: str,
    threads_url: str,
    config: AzureDevOpsConfig,
    repo_id: str,
    requests_module: Any,
    headers: dict[str, str],
) -> bool:
    """Return True when unaddressed suggestions block incremental scaffolding."""
    files_with_previous = {
        file_path: file_entry.previousSuggestions
        for file_path, file_entry in existing_state.files.items()
        if file_entry.previousSuggestions
    }
    if not files_with_previous or dry_run:
        return False

    threads_lookup = fetch_threads_lookup(requests_module, headers, threads_url)
    if threads_lookup is None:
        print("Warning: Could not fetch PR threads for verification. Proceeding.", file=sys.stderr)
        return False

    changed_set = frozenset(changes.new_files + changes.modified_files + changes.deleted_files)
    results = categorize_all_suggestions(files_with_previous, changed_set, threads_lookup)
    if not results:
        return False

    unaddressed_list, needs_review_list = partition_results(results)
    if has_unaddressed(results):
        _record_blocked_suggestion_review(
            existing_state,
            unaddressed_list,
            config,
            repo_id,
            model_id,
            commit_hash,
            now,
            short_new_hash,
            threads_url,
            requests_module,
            headers,
        )
        return True

    for result in needs_review_list:
        file_entry = existing_state.files.get(result.file_path)
        if file_entry:
            file_entry.suggestionVerificationStatus = "pending_verification"
    return False


def _apply_incremental_file_changes(existing_state: ReviewState, changes: Any) -> None:
    """Update inline file and folder state based on the detected changes."""
    for file_path in changes.new_files:
        folder = _get_folder_for_path(file_path)
        file_name = _get_file_name(file_path)
        existing_state.files[file_path] = FileEntry(
            threadId=0,
            commentId=0,
            folder=folder,
            fileName=file_name,
            status=ReviewStatus.UNREVIEWED.value,
        )

    for file_path in changes.modified_files:
        file_entry = existing_state.files.get(file_path)
        if file_entry:
            if file_entry.previousSuggestions is None:
                file_entry.previousSuggestions = list(file_entry.suggestions)
            elif file_entry.suggestions:
                file_entry.previousSuggestions.extend(file_entry.suggestions)
            file_entry.suggestions = []
            file_entry.status = ReviewStatus.UNREVIEWED.value
            file_entry.summary = None
            file_entry.modelId = None
            file_entry.providerType = None
            file_entry.latencyMs = None
            file_entry.finishReason = None
            file_entry.tokensUsed = None

    for file_path in changes.deleted_files:
        file_entry = existing_state.files.get(file_path)
        if file_entry:
            file_entry.status = ReviewStatus.APPROVED.value
            file_entry.summary = "File removed"

    _update_incremental_folder_groups(existing_state, changes)


def _update_incremental_folder_groups(existing_state: ReviewState, changes: Any) -> None:
    """Rebuild folder groups and retain empty folders for removed files."""
    all_current_files = set(changes.new_files + changes.modified_files + changes.unchanged_files)
    new_folders: dict[str, list[str]] = {}
    for file_path in sorted(all_current_files):
        folder = _get_folder_for_path(file_path)
        new_folders.setdefault(folder, []).append(file_path)
    for folder_name in existing_state.folders:
        if folder_name not in new_folders:
            new_folders[folder_name] = []
    existing_state.folders = {name: FolderGroup(files=folder_files) for name, folder_files in new_folders.items()}


def _update_incremental_metadata(
    existing_state: ReviewState,
    old_commit_hash: str,
    commit_hash: str | None,
    model_id: str,
    latest_iteration_id: int,
    rebase_conflicts: bool,
    now: datetime,
    config: AzureDevOpsConfig,
    repo_id: str,
    requests_module: Any,
    headers: dict[str, str],
) -> None:
    """Update commit metadata and refresh the consolidated review comment."""
    if commit_hash:
        if old_commit_hash and old_commit_hash != commit_hash:
            _archive_commit_thread(existing_state, old_commit_hash, now=now)
        existing_state.commitHash = commit_hash
    existing_state.modelId = model_id or existing_state.modelId
    existing_state.latestIterationId = latest_iteration_id
    existing_state.rebaseConflicts = rebase_conflicts

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


def _post_incremental_activity_log(
    existing_state: ReviewState,
    requests_module: Any,
    headers: dict[str, str],
    threads_url: str,
    model_id: str,
    short_new_hash: str,
    now: datetime,
    n_new: int,
    n_mod: int,
    n_del: int,
    n_unch: int,
) -> None:
    """Post an activity-log entry for the new review session when configured."""
    if not existing_state.activityLogThreadId:
        return

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
        existing_state.sessions[-1].sessionId,
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
        existing_state.sessions[-1].activityLogCommentId = reply_id
        save_review_state(existing_state)
    except Exception as exc:
        print(f"Warning: Could not post activity log entry: {exc}", file=sys.stderr)


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

    if _verify_suggestions_before_rescaffold(
        existing_state,
        changes,
        dry_run,
        commit_hash,
        model_id,
        now,
        short_new_hash,
        threads_url,
        config,
        repo_id,
        requests_module,
        headers,
    ):
        return existing_state

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

    _apply_incremental_file_changes(existing_state, changes)
    _update_incremental_metadata(
        existing_state,
        old_commit_hash,
        commit_hash,
        model_id,
        latest_iteration_id,
        rebase_conflicts,
        now,
        config,
        repo_id,
        requests_module,
        headers,
    )

    # Create new session
    session = _create_session(model_id, commit_hash=commit_hash, now=now)
    existing_state.sessions.append(session)

    save_review_state(existing_state)

    _post_incremental_activity_log(
        existing_state,
        requests_module,
        headers,
        threads_url,
        model_id,
        short_new_hash,
        now,
        n_new,
        n_mod,
        n_del,
        n_unch,
    )

    print(f"Incremental re-scaffolding complete for PR {pull_request_id}.")
    return existing_state
