"""Generate review prompts, snapshots, and queue manifests."""

import json
import os
import sys
from datetime import UTC
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ...state import get_state_dir, get_value, set_value
from ..git import get_diff_lines_info, get_diff_patch, normalize_ref_name
from .helpers import resolve_review_artifact_dir_name
from .review_prompt_formatting import _write_file_prompt, _write_unchanged_file_prompt
from .review_prompt_inventory import _load_branch_file_metadata
from .review_prompt_tracking import _normalize_path_for_comparison

if TYPE_CHECKING:
    from .review_state import SkippedFile


def _find_missing_branch_files(
    files_payload: list[dict[str, Any]],
    files_on_branch: set[str],
    normalized_branch_files: set[str],
    branch_file_change_types: dict[str, str],
    branch_rename_sources: dict[str, str],
) -> tuple[list[str], dict[str, str], dict[str, str]]:
    """Find branch paths omitted by the PR API and index their git metadata."""
    from ..workflows.base import _safe_print

    known_paths: set[str] = set()
    for file_detail in files_payload:
        raw_path = file_detail.get("path", "")
        if not isinstance(raw_path, str):
            _safe_print(
                f"Warning: Skipping PR file record with non-string path: {raw_path!r}",
                file=sys.stderr,
            )
            continue
        normalized_known_path = _normalize_path_for_comparison(raw_path)
        if normalized_known_path:
            known_paths.add(normalized_known_path)

    missing_normalized = sorted(normalized_branch_files - known_paths)
    if not missing_normalized:
        return [], {}, {}
    original_by_normalized = {_normalize_path_for_comparison(path): path for path in files_on_branch}
    change_type_by_normalized = {
        _normalize_path_for_comparison(path): change_type for path, change_type in branch_file_change_types.items()
    }
    rename_source_by_normalized = {
        _normalize_path_for_comparison(new_path): old_path for new_path, old_path in branch_rename_sources.items()
    }
    missing_paths = [original_by_normalized[normalized] for normalized in missing_normalized]
    _safe_print(
        f"Warning: {len(missing_paths)} file(s) changed on the branch were missing from the PR "
        f"file listing; adding them to the review queue: {', '.join(missing_paths)}",
        file=sys.stderr,
    )
    return missing_paths, change_type_by_normalized, rename_source_by_normalized


def _resolve_recovery_base_ref(pr_details: dict[str, Any], branch_diff_base_ref: str | None) -> str:
    """Choose the base ref for recovered-file diff metadata."""
    from ..workflows.base import _safe_print

    if branch_diff_base_ref:
        return branch_diff_base_ref
    raw_comparison = pr_details.get("comparison")
    comparison_info = raw_comparison if isinstance(raw_comparison, dict) else {}
    base_branch_raw = comparison_info.get("baseBranch")
    base_branch = normalize_ref_name(base_branch_raw) if isinstance(base_branch_raw, str) else ""
    if not base_branch:
        base_ref_raw = comparison_info.get("baseRef")
        base_ref_hint = base_ref_raw if isinstance(base_ref_raw, str) else ""
        if base_ref_hint.startswith("origin/"):
            base_branch = base_ref_hint.removeprefix("origin/")
        elif base_ref_hint.startswith("refs/heads/"):
            base_branch = base_ref_hint.removeprefix("refs/heads/")
    base_branch = normalize_ref_name(base_branch or "")
    if not base_branch:
        base_branch = "main"
        _safe_print(
            "Warning: Could not derive base branch from PR details "
            "(baseBranch missing and baseRef not a branch ref); "
            "falling back to origin/main for recovered-file metadata.",
            file=sys.stderr,
        )
    return f"origin/{base_branch}"


def _resolve_recovered_file_git_target(
    missing_path: str,
    normalized_path: str,
    change_type: str,
    rename_source_by_normalized: dict[str, str],
) -> tuple[str | list[str], str | None]:
    """Resolve the path pair needed to inspect a recovered rename."""
    git_lookup_path = missing_path.replace("\\", "/").lstrip("/")
    original_path = None
    if change_type == "rename":
        candidate_original_path = rename_source_by_normalized.get(normalized_path)
        if candidate_original_path:
            normalized_original_path = candidate_original_path.replace("\\", "/").lstrip("/")
            if normalized_original_path:
                original_path = candidate_original_path
                if normalized_original_path != git_lookup_path:
                    return [normalized_original_path, git_lookup_path], original_path
    return git_lookup_path, original_path


def _load_recovered_file_diff(
    missing_path: str,
    base_ref: str,
    git_lookup_target: str | list[str],
) -> tuple[bool, list[dict[str, Any]], list[dict[str, Any]], str | None]:
    """Read diff metadata and patch for a file absent from the PR API listing."""
    from ..workflows.base import _safe_print

    is_binary = False
    added_lines: list[dict[str, Any]] = []
    removed_lines: list[dict[str, Any]] = []
    patch = None
    try:
        diff_info = get_diff_lines_info(base_ref, "HEAD", git_lookup_target)
        is_binary = bool(diff_info.added.is_binary or diff_info.removed.is_binary)
        added_lines = [{"line": line.line_number, "content": line.content} for line in diff_info.added.lines]
        removed_lines = [{"line": line.line_number, "content": line.content} for line in diff_info.removed.lines]
    except Exception as exc:
        _safe_print(
            f"Warning: Could not load git diff metadata for recovered file '{missing_path}': {exc}",
            file=sys.stderr,
        )
        return is_binary, added_lines, removed_lines, patch

    if not is_binary:
        try:
            patch = get_diff_patch(base_ref, "HEAD", git_lookup_target)
        except Exception as exc:
            _safe_print(
                f"Warning: Could not load git patch for recovered file '{missing_path}': {exc}",
                file=sys.stderr,
            )
    return is_binary, added_lines, removed_lines, patch


def _recover_missing_branch_files(
    files_payload: list[dict[str, Any]],
    pr_details: dict[str, Any],
    files_on_branch: set[str] | None,
    normalized_branch_files: set[str] | None,
    branch_file_change_types: dict[str, str],
    branch_rename_sources: dict[str, str],
    branch_diff_base_ref: str | None,
) -> None:
    """Append synthetic API file records for branch changes missing from the PR response."""
    if files_on_branch is None or normalized_branch_files is None:
        return
    missing_paths, change_types, rename_sources = _find_missing_branch_files(
        files_payload,
        files_on_branch,
        normalized_branch_files,
        branch_file_change_types,
        branch_rename_sources,
    )
    if not missing_paths:
        return
    base_ref = _resolve_recovery_base_ref(pr_details, branch_diff_base_ref)
    for missing_path in missing_paths:
        normalized_path = _normalize_path_for_comparison(missing_path)
        change_type = change_types.get(normalized_path, "edit")
        git_lookup_target, original_path = _resolve_recovered_file_git_target(
            missing_path,
            normalized_path,
            change_type,
            rename_sources,
        )
        is_binary, added_lines, removed_lines, patch = _load_recovered_file_diff(
            missing_path,
            base_ref,
            git_lookup_target,
        )
        file_record: dict[str, Any] = {
            "path": missing_path,
            "changeType": change_type,
            "isBinary": is_binary,
            "addedLineCount": len(added_lines),
            "addedLines": added_lines,
            "removedLineCount": len(removed_lines),
            "removedLines": removed_lines,
            "patch": patch,
        }
        if original_path:
            file_record["originalPath"] = original_path
        files_payload.append(file_record)


def _load_pr_details(details_path: Path, pr_details: dict[str, Any] | None) -> dict[str, Any]:
    """Load the PR response artifact when the caller did not provide details."""
    if pr_details is not None:
        return pr_details
    if not details_path.exists():
        raise FileNotFoundError(f"PR details file not found: {details_path}. Run get_pull_request_details first.")
    with open(details_path, encoding="utf-8") as f:
        return json.load(f)


def _write_review_snapshots(
    prompts_dir: Path,
    files_payload: list[dict[str, Any]],
    threads_payload: list[Any],
) -> None:
    """Persist PR, thread, and Jira snapshots for the review session."""
    files_snapshot_path = prompts_dir / "pull-request-files.json"
    with open(files_snapshot_path, "w", encoding="utf-8") as f:
        json.dump({"files": files_payload}, f, indent=2)

    threads_snapshot_path = prompts_dir / "pull-request-threads.json"
    with open(threads_snapshot_path, "w", encoding="utf-8") as f:
        json.dump({"threads": threads_payload}, f, indent=2)

    state_dir = get_state_dir()
    jira_temp_path = state_dir / "temp-get-issue-details-response.json"
    jira_prompt_path = prompts_dir / "pull-request-jira-issue.json"
    if jira_temp_path.exists():  # pragma: no cover
        jira_prompt_path.write_text(jira_temp_path.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        jira_prompt_path.write_text("{}", encoding="utf-8")


def _generate_file_queue_entries(
    prompts_dir: Path,
    files_payload: list[dict[str, Any]],
    threads_payload: list[Any],
    normalized_branch_files: set[str] | None,
    normalized_unchanged: set[str],
    prior_state: Any,
    prior_commit_hash: str | None,
) -> tuple[int, int, list[dict[str, Any]], list[Any], list[dict[str, Any]]]:
    """Create per-file prompts and queue entries for in-scope PR files."""
    from .review_helpers import get_threads_for_file, normalize_repo_path
    from .review_state import (
        PROCESSING_PATH_INHERITED,
        SkippedFile,
        determine_processing_path,
    )

    prompts_generated = 0
    skipped_not_on_branch_count = 0
    queue_entries = []
    skipped_files: list[SkippedFile] = []
    filtered_files_payload: list[dict[str, Any]] = []

    for file_detail in files_payload:
        raw_file_path = file_detail.get("path", "")
        file_path = raw_file_path if isinstance(raw_file_path, str) else ""
        normalized_path = normalize_repo_path(file_path) or ""

        if normalized_branch_files is not None:
            normalized_for_comparison = _normalize_path_for_comparison(file_path)
            if normalized_for_comparison not in normalized_branch_files:
                from ..workflows.base import _safe_print

                _safe_print(f"Skipping file not on branch (likely from merged PR): {file_path}")
                skipped_not_on_branch_count += 1
                skipped_files.append(SkippedFile(path=file_path, reason="not_on_branch"))
                continue

        is_unchanged = bool(normalized_path and normalized_path.lower() in normalized_unchanged)
        prior_entry = prior_state.files.get(normalized_path) if prior_state and normalized_path else None
        processing_path = determine_processing_path(prior_entry, is_unchanged, prior_commit_hash)

        if processing_path == PROCESSING_PATH_INHERITED:
            prompt_path = _write_unchanged_file_prompt(prompts_dir, file_detail, prior_entry)
        else:
            threads_for_file = get_threads_for_file(threads_payload, file_path)
            prompt_path = _write_file_prompt(prompts_dir, file_detail, threads_for_file)

        prompts_generated += 1
        filtered_files_payload.append(file_detail)
        queue_entries.append(
            {
                "path": file_path,
                "normalizedPath": normalized_path,
                "promptFile": prompt_path.name,
                "promptPath": str(prompt_path),
                "status": "pending",
                "processingPath": processing_path,
            }
        )

    return prompts_generated, skipped_not_on_branch_count, queue_entries, skipped_files, filtered_files_payload


def _write_queue_manifest(
    prompts_dir: Path, pull_request_id: int, prompts_generated: int, queue_entries: list[Any]
) -> None:
    """Write the queue manifest consumed by the v2 setup pipeline."""
    from datetime import datetime

    queue_payload = {
        "pullRequestId": pull_request_id,
        "generatedUtc": datetime.now(UTC).isoformat(),
        "total": prompts_generated,
        "pending": queue_entries,
        "completed": [],
    }
    queue_path = prompts_dir / "queue.json"
    with open(queue_path, "w", encoding="utf-8") as f:
        json.dump(queue_payload, f, indent=2)


def _persist_filtered_pr_details(details_path: Path, pr_details: dict[str, Any]) -> None:
    """Atomically update the cached PR artifact to contain only queued files."""
    from ..workflows.base import _safe_print

    if not details_path.exists():
        return
    temp_details_path = details_path.with_name(f"{details_path.name}.tmp")
    try:
        with open(temp_details_path, "w", encoding="utf-8") as f:
            json.dump(pr_details, f, indent=2)
        os.replace(temp_details_path, details_path)
    except OSError as exc:
        _safe_print(
            f"Warning: Could not persist filtered PR details artifact: {exc}",
            file=sys.stderr,
        )
        try:
            temp_details_path.unlink(missing_ok=True)
        except OSError as cleanup_exc:
            _safe_print(
                f"Warning: Could not remove temporary PR details artifact: {cleanup_exc}",
                file=sys.stderr,
            )


def generate_review_prompts(
    pull_request_id: int,
    pr_details: dict | None = None,
    files_on_branch: set[str] | None = None,
    unchanged_files: set[str] | None = None,
) -> tuple[int, int, int, Path, list[SkippedFile]]:
    """
    Generate file review prompts from PR details.

    This function creates the queue.json manifest and individual file prompts
    for the PR review workflow. All in-scope files are reviewed every run;
    unchanged files receive a simplified prompt when valid prior state exists.

    Args:
        pull_request_id: PR ID
        pr_details: Full PR details payload. If None, loads from temp file.
        files_on_branch: Set of file paths that are actually changed on the branch.
            If None and files-on-branch.json exists, loads from that file.
            If provided, files not in this set will be filtered out (they likely
            came from recently merged PRs). Conversely, any file present in this
            set but missing from ``pr_details["files"]`` (a PR-API/git diff
            discrepancy) is recovered: a synthetic file entry is added so it
            still gets a prompt file and a queue entry, and a warning is
            printed so the recovery is never silent.
        unchanged_files: Set of file paths that have no changes since the last
            review. If None, treated as empty set (all files considered changed).

    Returns:
        Tuple of (prompts_generated, skipped_reviewed_count, skipped_not_on_branch_count,
        prompts_directory, skipped_files)
    """
    from .review_helpers import filter_threads
    from .review_state import load_review_state

    if unchanged_files is None:
        unchanged_files = set()

    temp_dir = get_state_dir()
    details_path = temp_dir / "temp-get-pull-request-details-response.json"
    commit_hash_short = get_value("review.commit_hash_short")
    dir_name = resolve_review_artifact_dir_name(
        pull_request_id,
        commit_hash_short,
        allow_discovery=False,
    )
    prompts_dir = temp_dir / "pull-request-review" / dir_name
    prompts_dir.mkdir(parents=True, exist_ok=True)
    set_value("review.artifact_dir_name", dir_name)
    set_value("review.artifact_dir_pr_id", str(pull_request_id))

    pr_details = _load_pr_details(details_path, pr_details)

    files_on_branch, branch_file_change_types, branch_rename_sources, branch_diff_base_ref = _load_branch_file_metadata(
        prompts_dir, files_on_branch
    )

    files_payload = pr_details.get("files", [])
    threads_payload = filter_threads(pr_details.get("threads", []))

    # Normalize the branch filter and restore any changes omitted by the PR API.
    normalized_branch_files: set[str] | None = None
    if files_on_branch is not None:
        normalized_branch_files = {_normalize_path_for_comparison(path) for path in files_on_branch}
    _recover_missing_branch_files(
        files_payload,
        pr_details,
        files_on_branch,
        normalized_branch_files,
        branch_file_change_types,
        branch_rename_sources,
        branch_diff_base_ref,
    )

    # Load prior review state for inheritance checks
    try:
        prior_state = load_review_state(pull_request_id)
    except FileNotFoundError:
        prior_state = None
    prior_commit_hash = prior_state.commitHash if prior_state else None

    # Normalize unchanged_files for comparison
    normalized_unchanged: set[str] = {f.lower() for f in unchanged_files}

    _write_review_snapshots(prompts_dir, files_payload, threads_payload)
    (
        prompts_generated,
        skipped_not_on_branch_count,
        queue_entries,
        skipped_files,
        filtered_files_payload,
    ) = _generate_file_queue_entries(
        prompts_dir,
        files_payload,
        threads_payload,
        normalized_branch_files,
        normalized_unchanged,
        prior_state,
        prior_commit_hash,
    )
    _write_queue_manifest(prompts_dir, pull_request_id, prompts_generated, queue_entries)

    # Keep pr_details in sync with the in-scope branch-filtered file list so
    # downstream consumers (e.g. manifest builder) generate rows only for files
    # that actually have prompt/queue entries.
    pr_details["files"] = filtered_files_payload
    _persist_filtered_pr_details(details_path, pr_details)

    return prompts_generated, 0, skipped_not_on_branch_count, prompts_dir, skipped_files
