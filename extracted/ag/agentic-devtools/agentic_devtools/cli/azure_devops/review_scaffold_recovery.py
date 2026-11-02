"""Recover review state from existing pull-request threads."""

import sys
from datetime import UTC, datetime
from typing import Any

from .config import AzureDevOpsConfig
from .review_scaffold_helpers import _get_file_name, _get_folder_for_path
from .review_scaffold_session_state import _create_session
from .review_state import (
    FileEntry,
    FolderGroup,
    OverallSummary,
    ReviewState,
    ReviewStatus,
    normalize_file_path,
    save_review_state,
)


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
