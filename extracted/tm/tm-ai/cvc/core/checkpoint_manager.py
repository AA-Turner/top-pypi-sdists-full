"""
cvc.core.checkpoint_manager — minimal filesystem checkpoint port (Phase 1B).

CVC v4.0 takes shadow-repo snapshots of the workspace before any
destructive tool call (``write_file``, ``patch_file``, ``edit_file``,
``multi_edit``, ``bash``) so users can ``/undo`` the change later.

Phase 1B ports the **minimum** surface that ``cvc/agent/executor.py``
uses:

    - ``__init__(enabled, max_snapshots, max_total_size_mb, max_file_size_mb)``
    - ``ensure_checkpoint(working_dir, reason="auto") -> bool``
    - ``get_working_dir_for_path(file_path) -> str``

Phase 4 will port ``list_checkpoints`` / ``diff`` / ``restore`` /
``undo_last`` so the full ``/undo`` UX works. The vendor's git-store
implementation is ~1600 lines; for now we offer a no-op fallback
that does not take snapshots but still answers ``get_working_dir_for_path``
correctly. Callers see ``enabled=True`` semantics, but no git activity
actually happens — the snapshot is a logical no-op rather than a real
shadow commit.

Design choice: prefer a deterministic no-op over a half-working
git-store copy. A broken shadow repo is worse than no shadow repo
(both block the tool path on errors; the no-op can't corrupt anything).

If Phase 1B testing demands a working snapshot, replace
``_take`` with a real implementation. The surface stays the same.
"""

from __future__ import annotations

import logging
import shutil
import threading
from pathlib import Path
from typing import Optional, Set

logger = logging.getLogger(__name__)


# Project-marker files used to walk upward to find a project root.
_PROJECT_MARKERS = frozenset({
    ".git", "pyproject.toml", "package.json", "Cargo.toml",
    "go.mod", "Makefile", "pom.xml", ".hg", "Gemfile",
})


def _normalize_path(p: str | Path) -> Path:
    """Resolve ``~`` and return absolute Path."""
    return Path(str(p)).expanduser().resolve()


class CheckpointManager:
    """Manages automatic filesystem checkpoints.

    Designed to be owned by ``Executor``. Call ``new_turn()`` at the
    start of each conversation turn and ``ensure_checkpoint(dir,
    reason)`` before any file-mutating tool call. The manager
    deduplicates so at most one snapshot is taken per directory per
    turn.

    Phase 1B: ``ensure_checkpoint`` is a logged no-op. The class still
    tracks per-turn dedup and resolves file paths to project roots
    (both useful regardless of whether a snapshot is actually taken),
    and the constructor is unchanged so the executor's instantiation
    code does not need edits.
    """

    def __init__(
        self,
        enabled: bool = False,
        max_snapshots: int = 20,
        max_total_size_mb: int = 500,
        max_file_size_mb: int = 10,
    ) -> None:
        self.enabled = enabled
        self.max_snapshots = max(1, int(max_snapshots))
        self.max_total_size_mb = max(0, int(max_total_size_mb))
        self.max_file_size_mb = max(0, int(max_file_size_mb))
        self._checkpointed_dirs: Set[str] = set()
        self._git_available: Optional[bool] = None  # lazy probe
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Turn lifecycle
    # ------------------------------------------------------------------

    def new_turn(self) -> None:
        """Reset per-turn dedup. Call at the start of each agent iteration."""
        with self._lock:
            self._checkpointed_dirs.clear()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ensure_checkpoint(self, working_dir: str, reason: str = "auto") -> bool:
        """Take a checkpoint if enabled and not already done this turn.

        Returns True if a checkpoint was taken, False otherwise.
        Never raises — all errors are silently logged.

        Phase 1B: this is a no-op; the executor treats a False return
        as "no snapshot taken" and proceeds. Phase 4 will replace
        ``_take`` with a real git-store implementation.
        """
        if not self.enabled:
            return False

        if self._git_available is None:
            self._git_available = shutil.which("git") is not None

        with self._lock:
            abs_dir = str(_normalize_path(working_dir))
            # Skip root, home, and other overly broad directories
            if abs_dir in ("/", str(Path.home())):
                logger.debug("Checkpoint skipped: directory too broad (%s)", abs_dir)
                return False
            if abs_dir in self._checkpointed_dirs:
                return False
            self._checkpointed_dirs.add(abs_dir)

        try:
            return self._take(abs_dir, reason)
        except Exception as e:  # pragma: no cover — defensive
            logger.debug("Checkpoint failed (non-fatal): %s", e)
            return False

    def get_working_dir_for_path(self, file_path: str) -> str:
        """Resolve a file path to its working directory for checkpointing.

        Walks up from the path's directory looking for a project-marker
        file (``.git``, ``pyproject.toml``, ``package.json``, …). Returns
        the first ancestor with a marker, or the file's parent if no
        marker is found.
        """
        path = _normalize_path(file_path)
        candidate = path if path.is_dir() else path.parent
        check = candidate
        while check != check.parent:
            if any((check / m).exists() for m in _PROJECT_MARKERS):
                return str(check)
            check = check.parent
        return str(candidate)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _take(self, working_dir: str, reason: str) -> bool:
        """Take a snapshot. Returns True on success.

        Phase 1B stub: returns False unconditionally. The vendor's
        git-store implementation lives here in the upstream code; we
        re-implement it in Phase 4 once ``/undo`` UX is in scope.
        """
        logger.debug(
            "CheckpointManager._take stub: no snapshot for %s (%s)",
            working_dir, reason,
        )
        return False


__all__ = ["CheckpointManager"]
