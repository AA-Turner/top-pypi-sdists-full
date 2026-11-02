"""Track reviewed files and unchanged-file state."""

import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ..subprocess_utils import run_safe


def _detect_unchanged_files(
    pull_request_id: int,
    pr_details: dict[str, Any],
) -> set[str]:
    """Return files unchanged since the prior review commit."""
    from .review_helpers import normalize_repo_path
    from .review_state import load_review_state

    current_files = _collect_current_files(pr_details, normalize_repo_path)
    if not current_files:
        return set()

    try:
        prior_state = load_review_state(pull_request_id)
    except FileNotFoundError:
        return set()

    prior_commit_hash = prior_state.commitHash
    if not prior_commit_hash:
        return set()
    current_commit_hash = _get_current_review_commit(pr_details)
    if not current_commit_hash:
        return set()
    if prior_commit_hash == current_commit_hash:
        return current_files

    changed_files = _get_changed_files_between_commits(prior_commit_hash, current_commit_hash, normalize_repo_path)
    if changed_files is None:
        return set()
    return current_files - changed_files


def _collect_current_files(
    pr_details: dict[str, Any],
    normalize_repo_path: Callable[[str], str | None],
) -> set[str]:
    """Collect normalized paths from the current PR payload."""
    current_files: set[str] = set()
    for file_detail in pr_details.get("files", []):
        raw_path = file_detail.get("path", "")
        if not raw_path:
            continue
        normalized = normalize_repo_path(raw_path)
        if normalized:
            current_files.add(normalized)
    return current_files


def _get_current_review_commit(pr_details: dict[str, Any]) -> str | None:
    """Extract the source commit id from the PR response."""
    pr_info = pr_details.get("pullRequest", pr_details)
    last_merge = pr_info.get("lastMergeSourceCommit")
    if not isinstance(last_merge, dict):
        return None
    current_commit_hash = last_merge.get("commitId")
    if not isinstance(current_commit_hash, str) or not current_commit_hash.strip():
        return None
    return current_commit_hash.strip()


def _get_changed_files_between_commits(
    prior_commit_hash: str,
    current_commit_hash: str,
    normalize_repo_path: Callable[[str], str | None],
) -> set[str] | None:
    """Return changed paths, or None when git could not compare the commits."""
    diff_proc = run_safe(
        ["git", "diff", "--name-only", f"{prior_commit_hash}..{current_commit_hash}"],
        capture_output=True,
        text=True,
        shell=False,
    )
    if diff_proc.returncode != 0:
        print(
            "Warning: Could not diff prior vs current commit for unchanged-file detection; "
            "treating all files as changed.",
            file=sys.stderr,
        )
        return None

    changed_files: set[str] = set()
    for path in diff_proc.stdout.splitlines():
        if not path.strip():
            continue
        normalized = normalize_repo_path(path.strip())
        if normalized:
            changed_files.add(normalized)
    return changed_files


def _normalize_path_for_comparison(path: str) -> str:
    """
    Normalize a file path for comparison.

    Strips leading slashes and normalizes to forward slashes.

    Args:
        path: File path to normalize

    Returns:
        Normalized path for comparison
    """
    if not path:
        return ""
    return path.strip().replace("\\", "/").lstrip("/").lower()


def _persist_processing_paths_to_review_state(pull_request_id: int, prompts_dir: Path) -> None:
    """Best-effort persistence of queue processingPath metadata into review-state.json."""
    from ..workflows.base import _safe_print

    queue_path = prompts_dir / "queue.json"
    if not queue_path.exists():
        return

    try:
        with open(queue_path, encoding="utf-8") as f:
            queue_payload = json.load(f)
    except OSError, ValueError:
        return

    pending_entries = queue_payload.get("pending")
    if not isinstance(pending_entries, list) or not pending_entries:
        return

    from .review_helpers import normalize_repo_path

    processing_by_path = _build_processing_path_map(pending_entries, normalize_repo_path)
    if not processing_by_path:
        return
    _apply_processing_path_map(pull_request_id, processing_by_path, _safe_print)


def _build_processing_path_map(
    pending_entries: list[Any],
    normalize_repo_path: Callable[[str], str | None],
) -> dict[str, str]:
    """Map normalized file paths to their queue processing-path values."""
    processing_by_path: dict[str, str] = {}
    for entry in pending_entries:
        if not isinstance(entry, dict):
            continue
        processing_path = entry.get("processingPath")
        if not isinstance(processing_path, str) or not processing_path:
            continue
        normalized_path = entry.get("normalizedPath")
        if not isinstance(normalized_path, str) or not normalized_path:
            raw_path = entry.get("path")
            normalized_path = normalize_repo_path(raw_path) if isinstance(raw_path, str) else None
        if not normalized_path:
            continue
        processing_by_path[normalized_path] = processing_path
    return processing_by_path


def _apply_processing_path_map(
    pull_request_id: int,
    processing_by_path: dict[str, str],
    safe_print: Callable[..., None],
) -> None:
    """Persist mapped queue metadata without making review setup fail."""
    try:
        from .review_state import FileLockError, read_modify_write_review_state

        with read_modify_write_review_state(pull_request_id) as state:
            for path, file_entry in state.files.items():
                file_entry.processingPath = processing_by_path.get(path)
    except (FileNotFoundError, FileLockError, OSError, ValueError) as exc:
        safe_print(
            "Warning: Could not persist processing path metadata to review-state.json; "
            f"continuing without processing-path audit trail: {exc}",
            file=sys.stderr,
        )
