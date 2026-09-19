"""Shared worktree-path resolution for configurable sibling worktree folders.

The worktree folder location is derived from:

- the main repository root or its parent directory,
- the normalized issue key, and
- the optional ``worktree_folder`` project-config key.

The setting is intentionally machine-independent: only a single relative child
folder name is accepted. Absolute paths, nested paths, traversal segments, and
Windows-invalid/reserved names are rejected before any filesystem or git
mutation occurs.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from agentic_devtools.cli.config.project_config import get_effective_project_config_raw_value
from agentic_devtools.cli.git.branch_naming import normalize_issue_key

DEFAULT_WORKTREE_FOLDER = "wt"
WORKTREE_FOLDER_CONFIG_KEY = "worktree_folder"
_MISSING = object()
_WINDOWS_INVALID_CHARACTERS = frozenset('<>:"|?*')
_WINDOWS_RESERVED_STEMS = frozenset(
    {
        "CON",
        "CONIN$",
        "CONOUT$",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
)


@dataclass(frozen=True)
class WorktreePathResolution:
    """Resolved worktree location for a single issue key."""

    repos_parent: str
    worktree_path: str
    normalized_issue_key: str
    worktree_folder: str | None
    configured_parent_dir: str | None


def _is_windows_style_path(path_text: str) -> bool:
    """Return whether *path_text* should be interpreted with Windows semantics."""
    windows_path = PureWindowsPath(path_text)
    return bool(windows_path.drive) or path_text.startswith("\\\\") or "\\" in path_text


def _path_cls(path_text: str) -> type[PurePosixPath] | type[PureWindowsPath]:
    """Return the pure path class matching *path_text* semantics."""
    return PureWindowsPath if _is_windows_style_path(path_text) else PurePosixPath


def _join_path(base: str, *parts: str) -> str:
    """Join path segments using the same path flavor as *base*."""
    path_obj: PurePosixPath | PureWindowsPath = _path_cls(base)(base)
    for part in parts:
        path_obj = path_obj / part
    return str(path_obj)


def _validate_worktree_folder_name(value: str) -> str:
    """Validate and normalize a configured worktree-folder name."""
    windows_path = PureWindowsPath(value)
    posix_path = PurePosixPath(value)

    if windows_path.drive or windows_path.root or posix_path.is_absolute():
        raise ValueError(
            "project.json key 'worktree_folder' must be a single relative folder name; "
            "absolute or drive-qualified paths are not allowed"
        )
    if value in {".", ".."}:
        raise ValueError(
            "project.json key 'worktree_folder' must be a single relative folder name; '.' and '..' are not allowed"
        )
    if "/" in value or "\\" in value:
        raise ValueError(
            "project.json key 'worktree_folder' must be a single relative folder name; path separators are not allowed"
        )
    if any(ord(character) < 32 for character in value):
        raise ValueError("project.json key 'worktree_folder' contains control characters")
    if any(character in _WINDOWS_INVALID_CHARACTERS for character in value):
        raise ValueError("project.json key 'worktree_folder' contains characters invalid in Windows folder names")
    if value.endswith("."):
        raise ValueError("project.json key 'worktree_folder' must not end with '.'")

    reserved_stem = value.split(".", 1)[0].rstrip(" ").upper().translate(str.maketrans("¹²³", "123"))
    if reserved_stem in _WINDOWS_RESERVED_STEMS:
        raise ValueError(f"project.json key 'worktree_folder' uses reserved Windows device name {reserved_stem!r}")
    return value


def _resolve_worktree_folder(raw_value: Any, *, key_present: bool) -> str | None:
    """Resolve the effective configured worktree-folder behavior."""
    if not key_present:
        return DEFAULT_WORKTREE_FOLDER
    if raw_value is None:
        return None
    if isinstance(raw_value, bool):
        raise ValueError(
            "project.json key 'worktree_folder' must be a string, null, or absent; booleans are not allowed"
        )
    if not isinstance(raw_value, str):
        raise ValueError(
            f"project.json key 'worktree_folder' must be a string, null, or absent; got {type(raw_value).__name__}"
        )

    stripped_value = raw_value.strip()
    if not stripped_value:
        return None
    return _validate_worktree_folder_name(stripped_value)


def _reject_configured_parent_matching_git_root(
    configured_parent_dir: str,
    worktree_folder: str,
    git_root: Any,
    *,
    repos_parent: str | None = None,
) -> None:
    """Raise if *configured_parent_dir* resolves to *git_root* itself.

    A ``worktree_folder`` value equal to the main checkout's own basename (for
    example ``worktree_folder: "acme"`` when the repo root is ``/repos/acme``)
    would nest new worktrees inside the main checkout instead of under a
    sibling container. Comparison uses Windows case-insensitive semantics when
    either path is Windows-style (:class:`~pathlib.PureWindowsPath` equality
    already folds case).
    """
    repos_parent = repos_parent or str(Path(configured_parent_dir).parent)
    if git_root is not None:
        path_cls = _path_cls(configured_parent_dir)
    else:
        path_cls = None
    if path_cls is not None and path_cls(configured_parent_dir) == path_cls(str(git_root)):
        raise ValueError(
            "project.json key 'worktree_folder' "
            f"{worktree_folder!r} resolves to the main checkout directory "
            f"({git_root}); choose a folder name that does not collide with "
            "the repository root's own name"
        )
    if os.name != "nt" and _is_windows_style_path(repos_parent):
        return
    try:
        resolved_repos_parent = Path(repos_parent).resolve()
        resolved_configured_parent = Path(configured_parent_dir).resolve()
        resolved_git_root = Path(str(git_root)).resolve() if git_root is not None else None
    except RuntimeError as exc:
        raise ValueError("project.json key 'worktree_folder' could not be resolved") from exc
    if resolved_git_root is not None and resolved_configured_parent == resolved_git_root:
        raise ValueError(
            "project.json key 'worktree_folder' resolves to the main checkout directory "
            f"({git_root}); choose a folder name that does not collide with the repository root's own name"
        )
    try:
        resolved_configured_parent.relative_to(resolved_repos_parent)
    except ValueError as exc:
        raise ValueError("project.json key 'worktree_folder' resolves outside the repository parent directory") from exc
    if resolved_configured_parent == resolved_repos_parent:
        raise ValueError(
            "project.json key 'worktree_folder' must resolve to a child of the repository parent directory"
        )


def validate_worktree_folder_setting(repo_root: str | Path) -> str | None:
    """Validate the configured ``worktree_folder`` setting without an issue key.

    Performs the same type/shape validation and main-checkout basename
    collision check as :func:`resolve_worktree_path`, but does not require an
    issue key. Callers that only need to fail fast on an invalid configuration
    before taking a fast path that never reaches full path resolution (for
    example, a registered-worktree porcelain match) can use this instead.

    Returns:
        The effective worktree-folder name, or ``None`` when the setting opts
        out of the sibling-folder layout.
    """
    repo_root_text = str(repo_root)
    if not repo_root_text:
        raise ValueError("Repository root is required to resolve a worktree path")

    path_cls = _path_cls(repo_root_text)
    repos_parent = str(path_cls(repo_root_text).parent)

    raw_value = get_effective_project_config_raw_value(
        WORKTREE_FOLDER_CONFIG_KEY,
        git_root=Path(repo_root_text),
        default=_MISSING,
    )
    worktree_folder = _resolve_worktree_folder(raw_value, key_present=raw_value is not _MISSING)
    if worktree_folder is not None:
        configured_parent_dir = _join_path(repos_parent, worktree_folder)
        _reject_configured_parent_matching_git_root(
            configured_parent_dir,
            worktree_folder,
            repo_root_text,
            repos_parent=repos_parent,
        )
    return worktree_folder


def resolve_worktree_path_from_parent(
    repos_parent: str | Path,
    issue_key: str,
    *,
    git_root: Path | None = None,
) -> WorktreePathResolution:
    """Resolve the configured worktree path from a repository-parent directory."""
    repos_parent_text = str(repos_parent)
    if not repos_parent_text:
        raise ValueError("Repository parent directory is required to resolve a worktree path")

    raw_value = get_effective_project_config_raw_value(
        WORKTREE_FOLDER_CONFIG_KEY,
        git_root=git_root,
        default=_MISSING,
    )
    worktree_folder = _resolve_worktree_folder(raw_value, key_present=raw_value is not _MISSING)
    normalized_issue_key = normalize_issue_key(issue_key)

    configured_parent_dir = None
    if worktree_folder is None:
        worktree_path = _join_path(repos_parent_text, normalized_issue_key)
    else:
        configured_parent_dir = _join_path(repos_parent_text, worktree_folder)
        _reject_configured_parent_matching_git_root(
            configured_parent_dir,
            worktree_folder,
            git_root,
            repos_parent=repos_parent_text,
        )
        worktree_path = _join_path(configured_parent_dir, normalized_issue_key)

    return WorktreePathResolution(
        repos_parent=repos_parent_text,
        worktree_path=worktree_path,
        normalized_issue_key=normalized_issue_key,
        worktree_folder=worktree_folder,
        configured_parent_dir=configured_parent_dir,
    )


def resolve_worktree_path(repo_root: str | Path, issue_key: str) -> WorktreePathResolution:
    """Resolve the configured worktree path from the main repository root."""
    repo_root_text = str(repo_root)
    if not repo_root_text:
        raise ValueError("Repository root is required to resolve a worktree path")

    path_cls = _path_cls(repo_root_text)
    repos_parent = str(path_cls(repo_root_text).parent)
    return resolve_worktree_path_from_parent(repos_parent, issue_key, git_root=Path(repo_root_text))
