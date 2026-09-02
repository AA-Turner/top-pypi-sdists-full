"""
Tests for file_locking module.
"""

import os
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import agentic_devtools.file_locking as file_locking_module
from agentic_devtools.file_locking import (
    FileLockError,
    locked_file,
)


class _TrackingHandle:
    def __init__(self, inner_file, label: str, close_calls: list[str]) -> None:  # noqa: ANN001
        self._inner_file = inner_file
        self.name = inner_file.name
        self._label = label
        self._close_calls = close_calls

    def __getattr__(self, attr: str):  # noqa: ANN204
        return getattr(self._inner_file, attr)

    def close(self) -> None:
        self._close_calls.append(self._label)
        if self._label == "guard":
            self._inner_file.close()
            raise OSError("guard close failed")
        self._inner_file.close()


def _make_guard_tracking_openers(close_calls: list[str]):  # noqa: ANN201
    real_fdopen = os.fdopen
    real_open = open

    def tracking_fdopen(fd: int, mode: str, encoding: str | None = None):  # noqa: ANN201
        if encoding is None:
            inner = real_fdopen(fd, mode)
        else:
            inner = real_fdopen(fd, mode, encoding=encoding)
        return _TrackingHandle(inner, "target", close_calls)

    def open_with_guard_tracking(file_path, mode, encoding=None):  # noqa: ANN001, ANN201
        inner = real_open(file_path, mode, encoding=encoding)
        if str(file_path).endswith(".create.lock"):
            return _TrackingHandle(inner, "guard", close_calls)
        return inner

    return tracking_fdopen, open_with_guard_tracking


class TestLockedFile:
    """Tests for locked_file context manager."""

    def test_locked_file_read_write(self, tmp_path):
        """Test locked_file context manager for read/write."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("initial content")

        with locked_file(test_file, mode="r+", exclusive=True) as f:
            content = f.read()
            assert content == "initial content"

    def test_locked_file_creates_parent_dirs(self, tmp_path):
        """Test locked_file creates parent directories if needed."""
        test_file = tmp_path / "subdir" / "nested" / "test.txt"

        with locked_file(test_file, mode="w", exclusive=True) as f:
            f.write("test")

        assert test_file.exists()

    def test_locked_file_creates_file_if_needed(self, tmp_path):
        """Test locked_file creates an empty file for r+ mode when missing."""
        test_file = tmp_path / "new_file.json"
        assert not test_file.exists()

        with locked_file(test_file, mode="r+", exclusive=True, include_created=True) as locked:
            f, created = locked
            content = f.read()
            assert content == ""
            assert created is True
        assert test_file.exists()

    def test_locked_file_rplus_without_include_created_does_not_leave_creation_guard(self, tmp_path):
        """Test r+ mode without include_created does not create a persistent guard file."""
        test_file = tmp_path / "project.json"

        with locked_file(test_file, mode="r+", exclusive=True) as f:
            f.write("{}")
            f.flush()

        assert test_file.exists()
        assert not test_file.with_name("project.json.create.lock").exists()

    def test_locked_file_marks_preexisting_empty_file_as_not_created(self, tmp_path):
        """Test locked_file distinguishes a new file from an existing empty file."""
        test_file = tmp_path / "empty.json"
        test_file.write_text("")

        with locked_file(test_file, mode="r+", exclusive=True, include_created=True) as locked:
            f, created = locked
            assert f.read() == ""
            assert created is False

    def test_locked_file_releases_on_exit(self, tmp_path):
        """Test locked_file releases lock when exiting context."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        with locked_file(test_file, mode="r+"):
            pass

        # Should be able to lock again after context exits
        with locked_file(test_file, mode="r+"):
            pass

    def test_locked_file_releases_on_exception(self, tmp_path):
        """Test locked_file releases lock even on exception."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        with pytest.raises(ValueError):
            with locked_file(test_file, mode="r+"):
                raise ValueError("test error")

        # Should still be able to lock after exception
        with locked_file(test_file, mode="r+"):
            pass

    def test_locked_file_shared_lock(self, tmp_path):
        """Test locked_file with shared (non-exclusive) lock."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        with locked_file(test_file, mode="r", exclusive=False) as f:
            content = f.read()
            assert content == "content"

    def test_locked_file_rplus_binary_with_encoding_raises_before_open(self, tmp_path):
        """Test that r+b mode with a non-None encoding raises ValueError before opening fd."""
        test_file = tmp_path / "test.bin"
        # Must raise before any fd is created — no leak, and the file is not created.
        with pytest.raises(ValueError, match="binary mode"):
            with locked_file(test_file, mode="r+b", encoding="utf-8"):
                pass  # pragma: no cover

    def test_locked_file_rplus_fdopen_failure_closes_fd(self, tmp_path):
        """Test that the raw fd is closed when os.fdopen raises after os.open."""
        test_file = tmp_path / "test.txt"
        closed_fds: list[int] = []
        real_close = os.close

        def tracking_close(fd: int) -> None:
            closed_fds.append(fd)
            real_close(fd)

        with (
            patch(
                "agentic_devtools.file_locking.os.fdopen",
                side_effect=OSError("fdopen failed"),
            ),
            patch("agentic_devtools.file_locking.os.close", side_effect=tracking_close),
        ):
            with pytest.raises(OSError, match="fdopen failed"):
                with locked_file(test_file, mode="r+", encoding="utf-8"):
                    pass  # pragma: no cover

        assert len(closed_fds) == 1, "raw_fd must be closed exactly once on fdopen failure"

    def test_locked_file_retries_when_existing_file_disappears_before_reopen(self, tmp_path):
        """Test that locked_file retries when the file vanishes after FileExistsError."""
        test_file = tmp_path / "retry.txt"
        real_open = os.open
        call_count = 0

        def flaky_open(path: str, flags: int, mode: int = 0o666) -> int:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise FileExistsError
            if call_count == 2:
                raise FileNotFoundError
            return real_open(path, flags, mode)

        with patch("agentic_devtools.file_locking.os.open", side_effect=flaky_open):
            with locked_file(test_file, mode="r+", exclusive=True, include_created=True) as locked:
                f, created = locked
                assert f.read() == ""
                assert created is True

        assert call_count == 3
        assert test_file.exists()

    def test_locked_file_fails_after_bounded_create_delete_race_retries(self, tmp_path):
        """Test that locked_file stops retrying after repeated create/delete races."""
        test_file = tmp_path / "race.txt"
        call_count = 0

        def always_racy_open(path: str, flags: int, mode: int = 0o666) -> int:
            del path, flags, mode
            nonlocal call_count
            call_count += 1
            if call_count % 2:
                raise FileExistsError
            raise FileNotFoundError

        with patch("agentic_devtools.file_locking.os.open", side_effect=always_racy_open):
            with pytest.raises(RuntimeError, match="create/delete races"):
                with locked_file(test_file, mode="r+", exclusive=True, include_created=True):
                    pass  # pragma: no cover

        assert call_count == 20

    def test_locked_file_with_binary_mode(self, tmp_path):
        """Test locked_file with binary mode (no encoding)."""
        test_file = tmp_path / "binary.bin"
        test_file.write_bytes(b"binary data")

        with locked_file(test_file, mode="rb", exclusive=False, encoding=None) as f:
            content = f.read()
            assert content == b"binary data"

    def test_locked_file_write_only_mode(self, tmp_path):
        """Test locked_file with write-only mode."""
        test_file = tmp_path / "write.txt"

        with locked_file(test_file, mode="w", exclusive=True) as f:
            f.write("new content")

        assert test_file.read_text() == "new content"

    def test_locked_file_creates_deeply_nested_dirs(self, tmp_path):
        """Test locked_file creates multiple levels of parent directories."""
        test_file = tmp_path / "a" / "b" / "c" / "d" / "test.txt"

        with locked_file(test_file, mode="w", exclusive=True) as f:
            f.write("deep")

        assert test_file.exists()
        assert test_file.read_text() == "deep"

    def test_locked_file_rplus_with_no_encoding(self, tmp_path):
        """Test locked_file r+ mode with encoding=None uses os.fdopen without encoding arg."""
        test_file = tmp_path / "binary_rplus.bin"
        test_file.write_bytes(b"raw bytes")

        with locked_file(test_file, mode="r+b", exclusive=True, encoding=None) as f:
            content = f.read()
            assert content == b"raw bytes"

    def test_locked_file_acquires_creation_guard_before_target_file(self, tmp_path, monkeypatch):
        """Test r+ mode acquires creation guard lock before target-file lock."""
        test_file = tmp_path / "ledger.json"
        lock_order: list[str] = []
        unlock_order: list[str] = []
        real_fdopen = os.fdopen

        class _NamedHandle:
            def __init__(self, inner_file, name: str) -> None:  # noqa: ANN001
                self._inner_file = inner_file
                self.name = name

            def __getattr__(self, attr: str):  # noqa: ANN204
                return getattr(self._inner_file, attr)

        def named_fdopen(fd: int, mode: str, encoding: str | None = None):  # noqa: ANN201
            if encoding is None:
                inner = real_fdopen(fd, mode)
            else:
                inner = real_fdopen(fd, mode, encoding=encoding)
            return _NamedHandle(inner, str(test_file))

        def _handle_name(file_handle) -> str:  # noqa: ANN001
            name = file_handle.name
            if isinstance(name, (str, os.PathLike)):
                return Path(name).name
            return str(name)

        def fake_lock(file_handle, exclusive=True, timeout=5.0):  # noqa: ANN001, ARG001
            lock_order.append(_handle_name(file_handle))

        def fake_unlock(file_handle):  # noqa: ANN001
            unlock_order.append(_handle_name(file_handle))

        monkeypatch.setattr(file_locking_module, "lock_file", fake_lock)
        monkeypatch.setattr(file_locking_module, "unlock_file", fake_unlock)
        monkeypatch.setattr(file_locking_module.os, "fdopen", named_fdopen)

        with locked_file(test_file, mode="r+", exclusive=True, include_created=True) as locked:
            file_handle, created = locked
            assert created is True
            file_handle.write("{}")
            file_handle.flush()

        assert lock_order[0] == "ledger.json.create.lock"
        assert len(lock_order) == 2
        assert lock_order[1] == "ledger.json"
        assert unlock_order[0] == "ledger.json.create.lock"
        assert len(unlock_order) == 2
        assert unlock_order[1] == "ledger.json"

    def test_locked_file_closes_target_handle_when_target_lock_fails(self, tmp_path, monkeypatch):
        """Test target handle is closed when acquiring target lock raises."""
        test_file = tmp_path / "ledger.json"
        real_fdopen = os.fdopen
        closed: list[bool] = []

        class _TrackingHandle:
            def __init__(self, inner_file) -> None:  # noqa: ANN001
                self._inner_file = inner_file
                self.name = inner_file.name

            def __getattr__(self, attr: str):  # noqa: ANN204
                return getattr(self._inner_file, attr)

            def close(self) -> None:
                closed.append(True)
                self._inner_file.close()

        def tracking_fdopen(fd: int, mode: str, encoding: str | None = None):  # noqa: ANN201
            if encoding is None:
                inner = real_fdopen(fd, mode)
            else:
                inner = real_fdopen(fd, mode, encoding=encoding)
            return _TrackingHandle(inner)

        lock_calls = 0

        def lock_with_failure(file_handle, exclusive=True, timeout=5.0):  # noqa: ANN001, ARG001
            del file_handle
            nonlocal lock_calls
            lock_calls += 1
            if lock_calls == 2:
                raise FileLockError("target lock failed")

        monkeypatch.setattr(file_locking_module.os, "fdopen", tracking_fdopen)
        monkeypatch.setattr(file_locking_module, "lock_file", lock_with_failure)

        with pytest.raises(FileLockError, match="target lock failed"):
            with locked_file(test_file, mode="r+", exclusive=True, include_created=True):
                pass  # pragma: no cover

        assert closed == [True]

    def test_locked_file_closes_handle_when_unlock_raises(self, tmp_path, monkeypatch):
        """Test that file_handle.close() is called even when unlock_file raises on context exit."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        mock_handle = MagicMock()

        monkeypatch.setattr(file_locking_module, "lock_file", lambda *a, **kw: None)

        def _raise_oserror(fh):  # noqa: ANN001
            raise OSError("unlock boom")

        monkeypatch.setattr(file_locking_module, "unlock_file", _raise_oserror)

        with patch("builtins.open", return_value=mock_handle):
            with pytest.raises(OSError, match="unlock boom"):
                with locked_file(test_file, mode="r", exclusive=False):
                    pass

        mock_handle.close.assert_called_once()

    def test_locked_file_cleans_up_target_when_creation_guard_release_fails(self, tmp_path, monkeypatch):
        """Test target handle is unlocked and closed when creation-guard release raises."""
        test_file = tmp_path / "ledger.json"
        real_fdopen = os.fdopen
        unlock_calls: list[str] = []
        close_calls: list[str] = []

        class _TrackingHandle:
            def __init__(self, inner_file, label: str) -> None:  # noqa: ANN001
                self._inner_file = inner_file
                self.name = inner_file.name
                self._label = label

            def __getattr__(self, attr: str):  # noqa: ANN204
                return getattr(self._inner_file, attr)

            def close(self) -> None:
                close_calls.append(self._label)
                self._inner_file.close()

        def tracking_fdopen(fd: int, mode: str, encoding: str | None = None):  # noqa: ANN201
            if encoding is None:
                inner = real_fdopen(fd, mode)
            else:
                inner = real_fdopen(fd, mode, encoding=encoding)
            return _TrackingHandle(inner, "target")

        lock_calls = 0

        def fake_lock(file_handle, exclusive=True, timeout=5.0):  # noqa: ANN001, ARG001
            nonlocal lock_calls
            lock_calls += 1

        def fail_on_guard_unlock(file_handle):  # noqa: ANN001
            label = getattr(file_handle, "_label", None)
            if label is None:
                raise OSError("guard unlock failed")
            unlock_calls.append(label)

        monkeypatch.setattr(file_locking_module.os, "fdopen", tracking_fdopen)
        monkeypatch.setattr(file_locking_module, "lock_file", fake_lock)
        monkeypatch.setattr(file_locking_module, "unlock_file", fail_on_guard_unlock)

        with pytest.raises(OSError, match="guard unlock failed"):
            with locked_file(test_file, mode="r+", exclusive=True, include_created=True):
                pass  # pragma: no cover

        assert "target" in unlock_calls
        assert "target" in close_calls

    def test_locked_file_guard_release_failure_without_target_lock(self, tmp_path, monkeypatch):
        """Test guard-unlock failure when target lock was never acquired propagates correctly."""
        test_file = tmp_path / "ledger.json"
        real_fdopen = os.fdopen
        close_calls: list[str] = []

        class _TrackingHandle:
            def __init__(self, inner_file, label: str) -> None:  # noqa: ANN001
                self._inner_file = inner_file
                self.name = inner_file.name
                self._label = label

            def __getattr__(self, attr: str):  # noqa: ANN204
                return getattr(self._inner_file, attr)

            def close(self) -> None:
                close_calls.append(self._label)
                self._inner_file.close()

        def tracking_fdopen(fd: int, mode: str, encoding: str | None = None):  # noqa: ANN201
            if encoding is None:
                inner = real_fdopen(fd, mode)
            else:
                inner = real_fdopen(fd, mode, encoding=encoding)
            return _TrackingHandle(inner, "target")

        lock_calls = 0

        def fail_target_lock(file_handle, exclusive=True, timeout=5.0):  # noqa: ANN001, ARG001
            nonlocal lock_calls
            lock_calls += 1
            if lock_calls == 2:
                raise FileLockError("target lock failed")

        def fail_on_guard_unlock(file_handle):  # noqa: ANN001
            label = getattr(file_handle, "_label", None)
            if label is None:
                raise OSError("guard unlock also failed")

        monkeypatch.setattr(file_locking_module.os, "fdopen", tracking_fdopen)
        monkeypatch.setattr(file_locking_module, "lock_file", fail_target_lock)
        monkeypatch.setattr(file_locking_module, "unlock_file", fail_on_guard_unlock)

        with pytest.raises((FileLockError, OSError)):
            with locked_file(test_file, mode="r+", exclusive=True, include_created=True):
                pass  # pragma: no cover

        assert "target" in close_calls

    def test_locked_file_cleans_up_target_when_creation_guard_close_fails(self, tmp_path, monkeypatch):
        """Test target handle cleanup when creation-guard close raises after target lock."""
        test_file = tmp_path / "ledger.json"
        unlock_calls: list[str] = []
        close_calls: list[str] = []
        tracking_fdopen, open_with_guard_tracking = _make_guard_tracking_openers(close_calls)

        def recording_unlock(file_handle):  # noqa: ANN001
            label = getattr(file_handle, "_label", None)
            if isinstance(label, str):
                unlock_calls.append(label)

        monkeypatch.setattr(file_locking_module.os, "fdopen", tracking_fdopen)
        monkeypatch.setattr(file_locking_module, "lock_file", lambda *a, **kw: None)
        monkeypatch.setattr(file_locking_module, "unlock_file", recording_unlock)

        with patch("builtins.open", side_effect=open_with_guard_tracking):
            with pytest.raises(OSError, match="guard close failed"):
                with locked_file(test_file, mode="r+", exclusive=True, include_created=True):
                    pass  # pragma: no cover

        assert "target" in unlock_calls
        assert "target" in close_calls

    def test_locked_file_prefers_guard_unlock_error_when_guard_close_also_fails(self, tmp_path, monkeypatch):
        """Test guard-unlock error is preserved when guard close fails too."""
        test_file = tmp_path / "ledger.json"
        unlock_calls: list[str] = []
        close_calls: list[str] = []
        tracking_fdopen, open_with_guard_tracking = _make_guard_tracking_openers(close_calls)

        def fail_guard_unlock(file_handle):  # noqa: ANN001
            label = getattr(file_handle, "_label", None)
            if label == "guard":
                raise OSError("guard unlock failed")
            if isinstance(label, str):
                unlock_calls.append(label)

        monkeypatch.setattr(file_locking_module.os, "fdopen", tracking_fdopen)
        monkeypatch.setattr(file_locking_module, "lock_file", lambda *a, **kw: None)
        monkeypatch.setattr(file_locking_module, "unlock_file", fail_guard_unlock)

        with patch("builtins.open", side_effect=open_with_guard_tracking):
            with pytest.raises(OSError, match="guard unlock failed"):
                with locked_file(test_file, mode="r+", exclusive=True, include_created=True):
                    pass  # pragma: no cover

        assert "target" in unlock_calls
        assert "target" in close_calls

    def test_locked_file_passes_remaining_timeout_to_target_lock(self, tmp_path, monkeypatch):
        """Test that the target lock receives only the remaining budget, not the full timeout."""
        test_file = tmp_path / "ledger.json"
        timeouts_seen: list[float] = []
        elapsed_for_guard = 0.1
        real_time = time.monotonic

        call_count = 0
        base_time = real_time()

        def fake_monotonic() -> float:
            nonlocal call_count
            call_count += 1
            # Second call (after guard lock) simulates elapsed time
            if call_count >= 2:
                return base_time + elapsed_for_guard
            return base_time

        def recording_lock(file_handle, exclusive=True, timeout=5.0):  # noqa: ANN001
            timeouts_seen.append(timeout)

        monkeypatch.setattr(file_locking_module, "lock_file", recording_lock)
        monkeypatch.setattr(file_locking_module, "unlock_file", lambda fh: None)  # noqa: ARG005
        monkeypatch.setattr(file_locking_module.time, "monotonic", fake_monotonic)

        with locked_file(test_file, mode="r+", exclusive=True, include_created=True):
            pass

        # Guard lock received full timeout; target lock received reduced budget
        assert len(timeouts_seen) == 2
        assert timeouts_seen[0] == 5.0
        assert timeouts_seen[1] < 5.0
