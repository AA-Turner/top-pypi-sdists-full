"""Tests for ExecutionLock — FR-009 single-active-execution."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

from agentic_devtools.orchestration.execution_lock import ExecutionLock, ExecutionLockError


class TestExecutionLock:
    """Tests for ExecutionLock lifecycle."""

    def test_acquire_creates_lock_file(self, tmp_path: Path) -> None:
        lock = ExecutionLock(tmp_path, "thread-1")
        lock.acquire()
        try:
            assert lock.lock_path.exists()
            assert lock.acquired is True
        finally:
            lock.release()

    def test_acquire_creates_lock_file_with_owner_only_permissions(self, tmp_path: Path) -> None:
        lock = ExecutionLock(tmp_path, "thread-1")
        lock.acquire()
        try:
            mode = lock.lock_path.stat().st_mode & 0o777
            assert mode == 0o600
        finally:
            lock.release()

    def test_release_removes_lock_file(self, tmp_path: Path) -> None:
        lock = ExecutionLock(tmp_path, "thread-1")
        lock.acquire()
        lock.release()
        assert not lock.lock_path.exists()
        assert lock.acquired is False

    def test_context_manager_acquires_and_releases(self, tmp_path: Path) -> None:
        lock = ExecutionLock(tmp_path, "thread-1")
        with lock:
            assert lock.acquired is True
            assert lock.lock_path.exists()
        assert lock.acquired is False
        assert not lock.lock_path.exists()

    def test_concurrent_acquisition_rejected(self, tmp_path: Path) -> None:
        lock1 = ExecutionLock(tmp_path, "thread-1")
        lock2 = ExecutionLock(tmp_path, "thread-1")
        lock1.acquire()
        try:
            with pytest.raises(ExecutionLockError, match="already active"):
                lock2.acquire()
        finally:
            lock1.release()

    def test_release_is_idempotent(self, tmp_path: Path) -> None:
        lock = ExecutionLock(tmp_path, "thread-1")
        lock.acquire()
        lock.release()
        lock.release()  # Should not raise
        assert lock.acquired is False

    def test_reacquire_is_idempotent(self, tmp_path: Path) -> None:
        lock = ExecutionLock(tmp_path, "thread-1")
        lock.acquire()
        try:
            lock.acquire()  # Should not raise (idempotent re-acquire)
            assert lock.acquired is True
        finally:
            lock.release()

    def test_lock_path_derivation(self, tmp_path: Path) -> None:
        thread_id = "work-on-issue-PROJ-123"
        lock = ExecutionLock(tmp_path, thread_id)
        expected = tmp_path / "locks" / f"{hashlib.sha256(thread_id.encode('utf-8')).hexdigest()}.lock"
        assert lock.lock_path == expected

    def test_lock_path_uses_portable_digest_for_special_characters(self, tmp_path: Path) -> None:
        thread_id = "work-on-issue-7:ABC--worktree-feature:42"
        lock = ExecutionLock(tmp_path, thread_id)

        assert lock.lock_path.name == f"{hashlib.sha256(thread_id.encode('utf-8')).hexdigest()}.lock"
        assert len(lock.lock_path.stem) == 64
        assert set(lock.lock_path.stem) <= set("0123456789abcdef")

    def test_lock_path_stays_portable_for_long_control_character_thread_id(self, tmp_path: Path) -> None:
        thread_id = "thread-\x00-\x1f-" + ("x" * 512)
        lock = ExecutionLock(tmp_path, thread_id)

        assert len(lock.lock_path.name.encode("utf-8")) <= 255
        assert lock.lock_path == ExecutionLock(tmp_path, thread_id).lock_path

    def test_different_thread_ids_independent(self, tmp_path: Path) -> None:
        lock1 = ExecutionLock(tmp_path, "thread-1")
        lock2 = ExecutionLock(tmp_path, "thread-2")
        lock1.acquire()
        try:
            lock2.acquire()  # Should succeed — different thread_id
            lock2.release()
        finally:
            lock1.release()

    def test_empty_thread_id_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            ExecutionLock(tmp_path, "")

    def test_creates_lock_directory(self, tmp_path: Path) -> None:
        state_dir = tmp_path / "deep" / "path"
        # state_dir doesn't exist yet — acquire should create locks/ subdir
        lock = ExecutionLock(state_dir, "t1")
        lock.acquire()
        try:
            assert lock.lock_path.exists()
        finally:
            lock.release()

    def test_release_handles_oserror_gracefully(self, tmp_path: Path) -> None:
        """Release handles OSError (e.g., permission denied) without raising."""
        from unittest.mock import patch

        lock = ExecutionLock(tmp_path, "thread-1")
        lock.acquire()
        assert lock.acquired is True

        with patch("pathlib.Path.unlink", side_effect=OSError("permission denied")):
            lock.release()  # Should not raise

        # Lock is released (acquired flag cleared) even on OSError
        assert lock.acquired is False

    def test_error_includes_existing_pid(self, tmp_path: Path) -> None:
        """ExecutionLockError message includes the PID from the existing lock file."""
        lock1 = ExecutionLock(tmp_path, "thread-1")
        lock2 = ExecutionLock(tmp_path, "thread-1")
        lock1.acquire()
        try:
            with pytest.raises(ExecutionLockError) as exc_info:
                lock2.acquire()
            # The error message should contain the PID that wrote the lock
            assert str(os.getpid()) in str(exc_info.value)
        finally:
            lock1.release()

    def test_stale_lock_cleaned_up_on_write_failure(self, tmp_path: Path) -> None:
        """If os.write() fails after creating the lock file, the file is removed."""
        from unittest.mock import patch

        lock = ExecutionLock(tmp_path, "thread-fail")
        with patch("os.write", side_effect=OSError("disk full")):
            with pytest.raises(OSError, match="disk full"):
                lock.acquire()

        # Lock file must not remain after the failed acquire
        assert not lock.lock_path.exists()
        # Lock is not marked as acquired
        assert lock.acquired is False

    def test_stale_lock_cleanup_warning_on_unlink_failure(self, tmp_path: Path) -> None:
        """When both write and unlink fail, a warning is logged and the exception propagates."""
        from unittest.mock import patch

        lock = ExecutionLock(tmp_path, "thread-fail")
        with (
            patch("os.write", side_effect=OSError("disk full")),
            patch("os.unlink", side_effect=OSError("permission denied")),
        ):
            with pytest.raises(OSError, match="disk full"):
                lock.acquire()

        assert lock.acquired is False

    def test_close_oserror_does_not_prevent_release(self, tmp_path: Path) -> None:
        """If os.close() raises OSError after a successful write, the error is swallowed and lock is acquired."""
        from unittest.mock import patch

        lock = ExecutionLock(tmp_path, "thread-close-err")
        # Patch os.close to raise; write succeeds so write_ok=True, close OSError is swallowed
        with patch("os.close", side_effect=OSError("close error")):
            lock.acquire()

        # Lock is acquired despite the close() error
        assert lock.acquired is True
        lock.release()

    def test_error_message_without_pid_when_lock_unreadable(self, tmp_path: Path) -> None:
        """If the existing lock file is unreadable, error is raised without PID hint."""
        from unittest.mock import patch

        lock1 = ExecutionLock(tmp_path, "thread-1")
        lock2 = ExecutionLock(tmp_path, "thread-1")
        lock1.acquire()
        try:
            with patch("pathlib.Path.read_text", side_effect=OSError("unreadable")):
                with pytest.raises(ExecutionLockError, match="already active"):
                    lock2.acquire()
        finally:
            lock1.release()
