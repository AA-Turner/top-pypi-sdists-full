"""Tests for _profile_lock."""

from __future__ import annotations

import threading
import time

import pytest

from agentic_devtools.cli.github.browser_apply_autofix import _profile_lock
from agentic_devtools.file_locking import FileLockError


class TestProfileLock:
    """Tests for the process-safe profile lock context manager."""

    def test_acquires_and_releases_lock(self, tmp_path) -> None:
        profile_dir = tmp_path / "browser-profile"

        with _profile_lock(profile_dir, timeout=5.0):
            pass

        # The lock file is left behind (empty) but no longer held, so a
        # second acquisition succeeds immediately.
        with _profile_lock(profile_dir, timeout=5.0):
            pass

    def test_second_concurrent_acquisition_blocks_until_released(self, tmp_path) -> None:
        profile_dir = tmp_path / "browser-profile"
        first_acquired = threading.Event()
        release_first = threading.Event()
        second_acquired = threading.Event()

        def hold_first() -> None:
            with _profile_lock(profile_dir, timeout=5.0):
                first_acquired.set()
                release_first.wait(timeout=5.0)

        thread = threading.Thread(target=hold_first)
        thread.start()
        assert first_acquired.wait(timeout=5.0)

        def acquire_second() -> None:
            with _profile_lock(profile_dir, timeout=5.0):
                second_acquired.set()

        second_thread = threading.Thread(target=acquire_second)
        second_thread.start()

        # The second acquisition must not succeed while the first holds it.
        time.sleep(0.2)
        assert not second_acquired.is_set()

        release_first.set()
        thread.join(timeout=5.0)
        second_thread.join(timeout=5.0)
        assert second_acquired.is_set()

    def test_raises_when_lock_cannot_be_acquired_within_timeout(self, tmp_path) -> None:
        profile_dir = tmp_path / "browser-profile"
        first_acquired = threading.Event()
        release_first = threading.Event()

        def hold_first() -> None:
            with _profile_lock(profile_dir, timeout=5.0):
                first_acquired.set()
                release_first.wait(timeout=5.0)

        thread = threading.Thread(target=hold_first)
        thread.start()
        assert first_acquired.wait(timeout=5.0)

        with pytest.raises(FileLockError):
            with _profile_lock(profile_dir, timeout=0.05):
                pass

        release_first.set()
        thread.join(timeout=5.0)
