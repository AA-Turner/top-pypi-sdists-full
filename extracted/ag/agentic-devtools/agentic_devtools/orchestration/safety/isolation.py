"""Branch and worktree isolation guards (FR-007, FR-008).

Enforces that autonomous workflows cannot mutate protected branches
or write files outside the allowed worktree roots.
"""

from __future__ import annotations

import fnmatch
import logging
import pathlib
import subprocess

from .exceptions import BranchIsolationError, WorktreeIsolationError

logger = logging.getLogger(__name__)

# Default protected branch patterns
_DEFAULT_PROTECTED_BRANCHES: list[str] = ["main", "master"]

# Tools classified as git mutations (need branch isolation check)
GIT_MUTATION_TOOLS: frozenset[str] = frozenset({"git_save_work", "git_push", "git_force_push", "git_stage_all"})

# Tools that write files (need worktree isolation check)
FILE_WRITING_TOOLS: frozenset[str] = frozenset({"filesystem_write_file"})


class BranchIsolationGuard:
    """Prevents git mutations on protected branches (FR-007).

    Uses ``fnmatch.fnmatchcase`` for case-sensitive, platform-stable
    glob matching against protected branch patterns.
    """

    def __init__(self, protected_branches: list[str] | None = None) -> None:
        self._protected = protected_branches or list(_DEFAULT_PROTECTED_BRANCHES)

    @property
    def protected_branches(self) -> list[str]:
        """Return the list of protected branch patterns."""
        return list(self._protected)

    def check(self, tool_name: str, inputs: dict | None = None) -> None:
        """Check if the current branch is protected.

        Only checks for tools in GIT_MUTATION_TOOLS.

        Raises:
            BranchIsolationError: If on a protected branch.
        """
        if tool_name not in GIT_MUTATION_TOOLS:
            return

        branch = self._get_current_branch()
        for pattern in self._protected:
            if fnmatch.fnmatchcase(branch, pattern):
                raise BranchIsolationError(branch, pattern)

    def _get_current_branch(self) -> str:
        """Resolve the currently checked-out branch.

        Raises:
            BranchIsolationError: If in detached HEAD state.
        """
        try:
            proc = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=False,
                shell=False,
            )
            if proc.returncode != 0:
                raise BranchIsolationError("(unknown)", "(git error: " + proc.stderr.strip() + ")")
            branch = proc.stdout.strip()
            if branch == "HEAD":
                raise BranchIsolationError("HEAD", "(detached HEAD state)")
            return branch
        except FileNotFoundError:
            raise BranchIsolationError("(unknown)", "(git not available)") from None


class WorktreeIsolationGuard:
    """Prevents file writes outside allowed roots (FR-008).

    Reuses the ``_get_allowed_roots()`` pattern from builtins.py.
    Enforced unconditionally across all execution modes.
    """

    def __init__(self, allowed_roots: list[pathlib.Path] | None = None) -> None:
        self._allowed_roots = allowed_roots

    def _resolve_allowed_roots(self) -> list[pathlib.Path]:
        """Resolve allowed roots, using injected values or builtins helper."""
        if self._allowed_roots is not None:
            return self._allowed_roots
        from agentic_devtools.orchestration.tools.builtins import _get_allowed_roots

        return _get_allowed_roots()

    def check(self, tool_name: str, inputs: dict | None = None) -> None:
        """Validate that file-writing tools target allowed paths.

        Only checks for tools in FILE_WRITING_TOOLS.

        Raises:
            WorktreeIsolationError: If path is outside allowed roots.
        """
        if tool_name not in FILE_WRITING_TOOLS:
            return
        if inputs is None:
            return

        path_str = inputs.get("path") or inputs.get("file_path")
        if path_str is None:
            return

        allowed_roots = self._resolve_allowed_roots()
        if not allowed_roots:
            raise WorktreeIsolationError(path_str, [])

        try:
            resolved = pathlib.Path(path_str).resolve()
        except (OSError, TypeError, ValueError):
            raise WorktreeIsolationError(path_str, [str(r) for r in allowed_roots]) from None

        for root in allowed_roots:
            try:
                if resolved.is_relative_to(root):
                    return
            except (TypeError, ValueError):
                continue

        raise WorktreeIsolationError(path_str, [str(r) for r in allowed_roots])
