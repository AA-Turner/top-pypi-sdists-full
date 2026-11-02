"""Worktree setup capability helpers."""

from __future__ import annotations

import os
from pathlib import Path


class WorktreeStateContext:
    """Context manager for cross-worktree state resolution.

    Saves the current CWD and state-related env vars, clears them, and
    changes to *worktree_path* so that ``get_state_dir()`` /
    ``get_state_file_path()`` resolve from the target worktree's
    ``.agdt/runtime-bootstrap.json``. On exit it makes a best-effort
    attempt to restore the original CWD and env vars.

    Usage::

        with WorktreeStateContext(worktree_path):
            state_dir = get_state_dir()   # resolves in worktree context
    """

    _ENV_VARS = ("AGENTIC_DEVTOOLS_STATE_DIR", "AGDT_AI_HELPERS_STATE_DIR")

    def __init__(self, worktree_path: str) -> None:
        self.worktree_path = worktree_path
        self._previous_cwd: str = ""
        self._previous_env: dict[str, str | None] = {}

    def __enter__(self) -> WorktreeStateContext:
        self._previous_cwd = os.getcwd()
        for var in self._ENV_VARS:
            self._previous_env[var] = os.environ.pop(var, None)
        try:
            os.chdir(self.worktree_path)
        except Exception:
            # Restore env vars before re-raising since __exit__ won't run.
            self._restore_env_vars()
            raise
        return self

    def __exit__(self, *exc_info: object) -> None:
        try:
            os.chdir(self._previous_cwd)
        except OSError:
            pass

        self._restore_env_vars()

    def _restore_env_vars(self) -> None:
        for var in self._ENV_VARS:
            try:
                prev = self._previous_env.get(var)
                if prev is not None:
                    os.environ[var] = prev
                else:
                    os.environ.pop(var, None)
            except Exception:
                pass


def _resolve_state_context_in_worktree(
    worktree_path: str,
    *,
    include_run_id: bool = False,
) -> tuple[Path | None, str]:
    """Resolve workflow state using the target worktree context."""
    try:
        with WorktreeStateContext(worktree_path):
            from agentic_devtools.state import get_state_file_path

            state_file_path = get_state_file_path()
            run_id = ""
            if include_run_id:
                from agentic_devtools.state import get_value

                run_id_value = get_value("agdt_run_id")
                run_id = run_id_value.strip() if isinstance(run_id_value, str) else ""
            return state_file_path, run_id
    except Exception:
        return None, ""
