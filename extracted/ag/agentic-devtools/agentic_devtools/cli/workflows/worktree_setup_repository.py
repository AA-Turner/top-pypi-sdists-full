"""Worktree setup capability helpers."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from agentic_devtools.state import BOOTSTRAP_FILENAME, IDENTITY_CACHE_FILENAME


@dataclass
class WorktreeSetupResult:
    """Result of worktree setup operation."""

    success: bool
    worktree_path: str
    branch_name: str
    error_message: str | None = None
    vscode_opened: bool = False
    target_setup_status: str | None = None
    target_setup_exit_code: str | None = None
    target_setup_error: str | None = None
    created_worktree: bool = False
    created_branch: bool = False
    copilot_trust_added: bool = False


@dataclass
class WorktreeSetupScriptResult:
    """Outcome of the optional target-repository setup script."""

    status: str
    exit_code: int | None = None
    error_message: str | None = None
    category: str | None = None


def is_in_worktree() -> bool:
    """
    Check if we're currently in a git worktree (not the main repo).

    Returns:
        True if in a worktree, False if in main repo or not in a git repo.
    """
    try:
        # git rev-parse --is-inside-work-tree returns "true" if in a work tree
        # git worktree list shows all worktrees
        # Simplest check: compare git-dir to git-common-dir
        result_dir = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        result_common = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result_dir.returncode != 0 or result_common.returncode != 0:
            return False

        git_dir = Path(result_dir.stdout.strip()).resolve()
        git_common_dir = Path(result_common.stdout.strip()).resolve()

        # In main repo: git_dir == ".git" (resolves to same as git_common_dir)
        # In worktree: git_dir is a file pointing elsewhere, or is different path
        # The git-dir in a worktree points to .git/worktrees/<name>
        return git_dir != git_common_dir

    except FileNotFoundError, OSError:
        return False


def get_current_branch() -> str | None:
    """
    Get the current git branch name.

    Returns:
        The current branch name, or None if not in a git repo or detached HEAD.
    """
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip() or None
        return None
    except FileNotFoundError, OSError:  # pragma: no cover
        return None


def get_worktree_branch(worktree_path: str) -> str | None:
    """Return the currently checked-out branch name for ``worktree_path``."""
    try:
        result = subprocess.run(
            ["git", "-C", worktree_path, "branch", "--show-current"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip() or None
        return None
    except FileNotFoundError, OSError:  # pragma: no cover
        return None


def switch_to_main_branch() -> bool:
    """
    Switch to the main branch.

    Returns:
        True if switch was successful, False otherwise.
    """
    try:
        result = subprocess.run(
            ["git", "switch", "main"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError, OSError:
        return False


def get_main_repo_root() -> str | None:
    """
    Get the root directory of the main git repository (not worktree).

    For worktrees, this returns the path to the main repository.
    For the main repo, this returns the repo root.

    Returns:
        The absolute path to the main repo root, or None if not in a git repo.
    """
    try:
        # First, get the common git directory (shared between main repo and worktrees)
        result = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            return None

        git_common_dir = result.stdout.strip()

        # The git-common-dir is usually .git in main repo or path/to/main/.git for worktrees
        # We need the parent of the .git directory
        git_path = Path(git_common_dir).resolve()

        # If it ends with .git, go to parent
        if git_path.name == ".git":
            return str(git_path.parent)

        # For worktrees, git-common-dir points to main/.git directly
        return str(git_path.parent)

    except FileNotFoundError, OSError:
        return None


def get_repos_parent_dir() -> str | None:
    """
    Get the parent directory where repos are stored.

    This is typically one level up from the main repo root (e.g., c:\\repos).

    Returns:
        The absolute path to the repos parent directory, or None if not determinable.
    """
    main_repo = get_main_repo_root()
    if main_repo:
        return str(Path(main_repo).parent)
    return None


def _propagate_agdt_cache(worktree_path: str, worktree_key: str | None = None, *, strict: bool = False) -> None:
    """Copy identity.json and runtime-bootstrap.json from the main repo into the new worktree.

    When *worktree_key* is provided, ``runtime-bootstrap.json`` is written with
    ``{"worktree_key": "<worktree_key>"}`` instead of being copied from the main
    repo, ensuring the worktree gets the correct key even if the main repo's
    bootstrap file has a stale value.

    Non-fatal by default: ``OSError`` and ``ValueError`` exceptions are logged to
    stderr and the worktree setup continues.  Pass ``strict=True`` to re-raise
    instead, which allows callers that require the cache to be propagated (e.g.
    ``propagate_agdt_cache``) to signal failure.
    """
    try:
        main_repo = get_main_repo_root()
        if not main_repo:
            if strict:
                raise ValueError("Cannot propagate AGDT cache: unable to resolve main repository root")
            return

        main_repo_path = Path(main_repo)
        src_identity = main_repo_path / ".agdt" / IDENTITY_CACHE_FILENAME
        src_bootstrap = main_repo_path / ".agdt" / BOOTSTRAP_FILENAME

        # If there is nothing to propagate and no explicit worktree_key override,
        # retain the previous no-op behaviour and avoid creating .agdt/ at all.
        if worktree_key is None and not src_identity.is_file() and not src_bootstrap.is_file():
            return

        dst_agdt = Path(worktree_path) / ".agdt"
        dst_agdt.mkdir(parents=True, exist_ok=True)

        # Best-effort copy of identity.json; failure here should not block
        # propagation of the runtime bootstrap file.
        if src_identity.is_file():
            shutil.copy2(str(src_identity), str(dst_agdt / IDENTITY_CACHE_FILENAME))

        # Propagate runtime-bootstrap.json so that the worktree resolves
        # to the correct scoped state directory. This is independent of
        # whether identity.json was present or successfully copied.
        dst_bootstrap = dst_agdt / BOOTSTRAP_FILENAME
        if worktree_key is not None:
            bootstrap_data = json.dumps({"worktree_key": worktree_key})
            dst_bootstrap.write_text(bootstrap_data, encoding="utf-8")
        elif src_bootstrap.is_file():
            shutil.copy2(str(src_bootstrap), str(dst_bootstrap))
    except (OSError, ValueError) as exc:
        if strict:
            raise
        print(
            f"Warning: failed to propagate AGDT cache (identity/bootstrap) to worktree: {exc}",
            file=sys.stderr,
        )


def propagate_agdt_cache(worktree_path: str, worktree_key: str | None = None) -> None:
    """Public entry-point for propagating identity.json and runtime-bootstrap.json.

    Delegates to :func:`_propagate_agdt_cache` in strict mode so that callers
    (e.g. ``orchestrator_commands``) receive failures as exceptions instead of
    silently-swallowed warnings.  ``OSError`` and ``ValueError`` propagate to
    the caller unchanged.
    """
    _propagate_agdt_cache(worktree_path, worktree_key=worktree_key, strict=True)
