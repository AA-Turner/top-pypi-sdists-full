"""Tests for ``_acquire_hierarchy_lock``."""

import os
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.speckit import scaffold_new_feature
from agentic_devtools.cli.speckit.scaffold_new_feature import _acquire_hierarchy_lock


@pytest.mark.skipif(os.name == "nt", reason="Uses the Unix advisory-lock implementation")
def test_keeps_lock_held_until_descriptor_is_closed(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_fd = _acquire_hierarchy_lock(lock_path)
    try:
        with pytest.raises(ValueError, match="Could not acquire hierarchy lock"):
            _acquire_hierarchy_lock(lock_path, timeout_seconds=0)
        assert lock_path.exists()
    finally:
        os.close(lock_fd)

    assert lock_path.exists()


def test_uses_windows_advisory_lock(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    msvcrt = SimpleNamespace(LK_NBLCK=1, locking=lambda *_args: None)
    with (
        patch.object(os, "name", "nt"),
        patch.dict(sys.modules, {"msvcrt": msvcrt}),
    ):
        lock_fd = _acquire_hierarchy_lock(lock_path)
    os.close(lock_fd)


def test_reuses_existing_empty_lock_file(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.touch()

    lock_fd = _acquire_hierarchy_lock(lock_path, timeout_seconds=0)
    try:
        assert lock_path.exists()
    finally:
        os.close(lock_fd)

    assert lock_path.exists()


def test_rejects_symlink_lock_path(tmp_path: Path) -> None:
    target = tmp_path / "real.lock"
    target.write_text("", encoding="utf-8")
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.symlink_to(target)

    with pytest.raises(ValueError, match="Refusing to use a symlinked hierarchy lock"):
        _acquire_hierarchy_lock(lock_path, timeout_seconds=0)


def test_rejects_symlink_lock_path_without_onofollow(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "real.lock"
    target.write_text("", encoding="utf-8")
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.symlink_to(target)
    monkeypatch.delattr(scaffold_new_feature.os, "O_NOFOLLOW", raising=False)

    with pytest.raises(ValueError, match="Refusing to use a symlinked hierarchy lock"):
        _acquire_hierarchy_lock(lock_path, timeout_seconds=0)


def test_times_out_when_lock_file_cannot_be_opened(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    with patch("agentic_devtools.cli.speckit.scaffold_new_feature.os.open", side_effect=OSError):
        with pytest.raises(ValueError, match="Could not acquire hierarchy lock"):
            _acquire_hierarchy_lock(lock_path, timeout_seconds=0)


def test_retries_after_advisory_lock_failure(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    fcntl = SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=Mock(side_effect=OSError))
    with (
        patch.object(os, "name", "posix"),
        patch.dict(sys.modules, {"fcntl": fcntl}),
        patch(
            "agentic_devtools.cli.speckit.scaffold_new_feature.time.monotonic",
            side_effect=[0.0, 0.0, 1.0],
        ),
        patch("agentic_devtools.cli.speckit.scaffold_new_feature.time.sleep"),
    ):
        with pytest.raises(ValueError, match="Could not acquire hierarchy lock"):
            _acquire_hierarchy_lock(lock_path, timeout_seconds=0.5)


def test_recovers_stale_directory_lock(tmp_path: Path) -> None:
    """A legacy bash mkdir-based lock is removed so the file lock can be acquired."""
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    os.utime(lock_path, (0, 0))
    lock_fd = _acquire_hierarchy_lock(lock_path, stale_after_seconds=1)
    os.close(lock_fd)
    assert lock_path.is_file()


def test_does_not_reclaim_fresh_directory_lock(tmp_path: Path) -> None:
    """A fresh legacy directory lock is treated as held until timeout."""
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    with pytest.raises(ValueError, match="Could not acquire hierarchy lock"):
        _acquire_hierarchy_lock(lock_path, timeout_seconds=0)


@pytest.mark.skipif(os.name == "nt", reason="Uses the Unix directory-lock wait path")
def test_times_out_when_directory_lock_cannot_be_removed(tmp_path: Path) -> None:
    """A non-empty stale directory lock causes a timeout rather than a crash."""
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    (lock_path / "sentinel").write_text("", encoding="utf-8")  # make non-empty so rmdir fails
    os.utime(lock_path, (0, 0))
    with pytest.raises(ValueError, match="Could not acquire hierarchy lock"):
        _acquire_hierarchy_lock(lock_path, timeout_seconds=0, stale_after_seconds=1)


def test_does_not_reclaim_directory_with_live_owner(tmp_path: Path) -> None:
    """A live PID protects an old directory lock from stale recovery."""
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    (lock_path / ".owner").write_text(f'{{"pid": {os.getpid()}, "created_at": 0}}', encoding="utf-8")
    with pytest.raises(ValueError, match="Could not acquire hierarchy lock"):
        _acquire_hierarchy_lock(lock_path, timeout_seconds=0, stale_after_seconds=1)
    assert lock_path.is_dir()


def test_reclaims_directory_with_dead_owner(tmp_path: Path) -> None:
    """A stale directory with a dead owner is atomically reclaimed."""
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_path.mkdir()
    (lock_path / ".owner").write_text('{"pid": 99999999, "created_at": 0}', encoding="utf-8")
    lock_fd = _acquire_hierarchy_lock(lock_path, stale_after_seconds=1)
    os.close(lock_fd)
    assert lock_path.is_file()


def test_writes_pid_and_timestamp_metadata_to_file_lock(tmp_path: Path) -> None:
    """A newly acquired file lock records its owner metadata for stale recovery."""
    lock_path = tmp_path / ".hierarchy.yml.lock"
    lock_fd = _acquire_hierarchy_lock(lock_path)
    os.close(lock_fd)
    metadata = lock_path.read_text(encoding="utf-8")
    assert '"pid":' in metadata
    assert '"created_at":' in metadata


def test_metadata_write_failure_propagates_as_oserror(tmp_path: Path) -> None:
    """A disk-write failure in _write_hierarchy_lock_metadata propagates as OSError rather than
    being retried as contention and misreported as 'Could not acquire hierarchy lock'."""
    lock_path = tmp_path / ".hierarchy.yml.lock"
    write_error = OSError("disk full")
    with patch(
        "agentic_devtools.cli.speckit.scaffold_new_feature._write_hierarchy_lock_metadata",
        side_effect=write_error,
    ):
        with pytest.raises(OSError, match="disk full"):
            _acquire_hierarchy_lock(lock_path, timeout_seconds=0)
