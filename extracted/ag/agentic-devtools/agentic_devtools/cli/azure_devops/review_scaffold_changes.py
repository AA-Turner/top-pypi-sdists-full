"""Detect and validate file changes between review iterations."""

import sys
from dataclasses import dataclass, field
from typing import Any

from .config import AzureDevOpsConfig
from .review_state import ReviewState, normalize_file_path

_DIFF_WARNING_THRESHOLD = 5


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
