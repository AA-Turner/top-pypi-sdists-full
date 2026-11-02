"""Load git change metadata used to build pull-request review prompts."""

import json
from pathlib import Path
from typing import Any


def _normalize_branch_change_types(raw_change_types: Any) -> dict[str, str]:
    """Normalize git name-status values for files-on-branch metadata."""
    if not isinstance(raw_change_types, dict):
        return {}
    normalized_types = {}
    for raw_path, raw_change_type in raw_change_types.items():
        if not isinstance(raw_path, str) or not isinstance(raw_change_type, str):
            continue
        normalized_path = raw_path.replace("\\", "/").strip()
        if not normalized_path:
            continue
        normalized_change_type = raw_change_type.strip().lower()
        if normalized_change_type in {"a", "add"}:
            normalized_types[normalized_path] = "add"
        elif normalized_change_type in {"d", "delete"}:
            normalized_types[normalized_path] = "delete"
        elif normalized_change_type.startswith("r"):
            normalized_types[normalized_path] = "rename"
        elif normalized_change_type in {"m", "edit", "modify"}:
            normalized_types[normalized_path] = "edit"
    return normalized_types


def _normalize_branch_rename_sources(raw_rename_sources: Any) -> dict[str, str]:
    """Normalize source and destination paths in git rename metadata."""
    if not isinstance(raw_rename_sources, dict):
        return {}
    normalized_sources = {}
    for raw_new_path, raw_old_path in raw_rename_sources.items():
        if not isinstance(raw_new_path, str) or not isinstance(raw_old_path, str):
            continue
        normalized_new_path = raw_new_path.replace("\\", "/").strip()
        normalized_old_path = raw_old_path.replace("\\", "/").strip()
        if normalized_new_path and normalized_old_path:
            normalized_sources[normalized_new_path] = normalized_old_path
    return normalized_sources


def _load_branch_file_metadata(
    prompts_dir: Path,
    files_on_branch: set[str] | None,
) -> tuple[set[str] | None, dict[str, str], dict[str, str], str | None]:
    """Load changed-path filters and git metadata from the inventory artifact."""
    files_on_branch_path = prompts_dir / "files-on-branch.json"
    if not files_on_branch_path.exists():
        return files_on_branch, {}, {}, None

    with open(files_on_branch_path, encoding="utf-8") as f:
        files_data = json.load(f)
    if files_on_branch is None:
        files_on_branch = set(files_data.get("files", []))
        print(f"Loaded {len(files_on_branch)} files from files-on-branch.json")
    branch_file_change_types = _normalize_branch_change_types(files_data.get("change_types", {}))
    branch_rename_sources = _normalize_branch_rename_sources(files_data.get("rename_sources", {}))
    raw_diff_base_ref = files_data.get("diff_base_ref")
    if isinstance(raw_diff_base_ref, str) and raw_diff_base_ref.strip():
        branch_diff_base_ref = raw_diff_base_ref.strip()
    else:
        branch_diff_base_ref = None
    return files_on_branch, branch_file_change_types, branch_rename_sources, branch_diff_base_ref
