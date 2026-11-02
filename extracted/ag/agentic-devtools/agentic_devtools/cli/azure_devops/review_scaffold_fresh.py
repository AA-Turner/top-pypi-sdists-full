"""Create initial review scaffold state and threads."""

import sys
from datetime import UTC, datetime
from typing import Any

from .config import AzureDevOpsConfig
from .consolidated_scaffold import upsert_consolidated_comment
from .helpers import patch_thread_status
from .review_scaffold_helpers import _get_file_name, _get_folder_for_path, _print_dry_run_plan
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
