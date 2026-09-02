"""Single-active-execution lock for workflow sessions (FR-009).

Prevents concurrent workflow executions for the same (state_dir, thread_id)
scope using a file-based lock. Only one workflow runner may hold the lock
at a time; a second attempt raises ``ExecutionLockError``.
"""

from __future__ import annotations

import hashlib
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

_LOCK_DIR = "locks"


class ExecutionLockError(RuntimeError):
    """Raised when a concurrent workflow execution is already active."""


class ExecutionLock:
    """File-based lock preventing concurrent workflow executions.

    The lock file is placed at
    ``<state_dir>/locks/<sha256(thread_id)>.lock``. Uses ``os.open`` with
    ``O_CREAT | O_EXCL`` for atomic creation.

    Args:
        state_dir: Worktree-scoped state directory.
        thread_id: Workflow thread identifier.
    """

    def __init__(self, state_dir: Path, thread_id: str) -> None:
        if not thread_id:
            raise ValueError("thread_id must be non-empty")
        self._lock_dir = state_dir / _LOCK_DIR
        safe_id = hashlib.sha256(thread_id.encode("utf-8")).hexdigest()
        self._lock_path = self._lock_dir / f"{safe_id}.lock"
        self._acquired = False

    @property
    def lock_path(self) -> Path:
        """Return the path to the lock file."""
        return self._lock_path

    @property
    def acquired(self) -> bool:
        """Return whether the lock is currently held."""
        return self._acquired

    def acquire(self) -> None:
        """Acquire the execution lock.

        Raises:
            ExecutionLockError: If the lock is already held by another process.
        """
        if self._acquired:
            return  # Idempotent re-acquire

        self._lock_dir.mkdir(parents=True, exist_ok=True)

        try:
            fd = os.open(str(self._lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            existing_pid = self._read_existing_lock_pid()
            pid_hint = f" (PID {existing_pid})" if existing_pid is not None else ""
            raise ExecutionLockError(
                f"Another workflow execution is already active for this scope{pid_hint}. Lock file: {self._lock_path}"
            )

        # Lock file created; write PID. Clean up the file on any failure so subsequent
        # runs are not permanently blocked by a stale lock.
        write_ok = False
        try:
            os.write(fd, f"{os.getpid()}\n".encode())
            write_ok = True
        finally:
            try:
                os.close(fd)
            except OSError:
                pass
            if not write_ok:
                try:
                    os.unlink(str(self._lock_path))
                except OSError:
                    logger.warning(
                        "Failed to remove stale lock file after write failure: %s",
                        self._lock_path,
                    )

        self._acquired = True
        logger.debug("Acquired execution lock: %s", self._lock_path)

    def _read_existing_lock_pid(self) -> int | None:
        """Read the PID recorded in an existing lock file held by another process.

        Returns:
            The PID as an integer, or None if the file is missing or unreadable.
        """
        try:
            text = self._lock_path.read_text(encoding="utf-8").strip()
            return int(text)
        except (OSError, ValueError):
            return None

    def release(self) -> None:
        """Release the execution lock (idempotent)."""
        if not self._acquired:
            return

        try:
            self._lock_path.unlink(missing_ok=True)
            logger.debug("Released execution lock: %s", self._lock_path)
        except OSError as exc:
            logger.warning("Failed to remove lock file %s: %s", self._lock_path, exc)
        finally:
            self._acquired = False

    def __enter__(self) -> ExecutionLock:
        """Acquire lock on context entry."""
        self.acquire()
        return self

    def __exit__(self, *args: object) -> None:
        """Release lock on context exit."""
        self.release()
