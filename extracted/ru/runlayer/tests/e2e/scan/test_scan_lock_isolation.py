"""Regression tests for the ``isolated_scan_run_lock`` autouse fixture.

Full rationale on the fixture in ``tests/conftest.py``.
"""

from pathlib import Path

import pytest

from runlayer_cli import paths
from runlayer_cli.scan import run_lock
from runlayer_cli.scan.run_lock import acquire_scan_run_lock

pytestmark = pytest.mark.no_backend_e2e


def test_scan_lock_dir_is_isolated_per_test(
    isolated_scan_run_lock: Path, tmp_path: Path
) -> None:
    """The lock must resolve to the fixture's per-test dir, never real home."""
    assert run_lock.get_runlayer_dir() == isolated_scan_run_lock
    assert isolated_scan_run_lock.is_relative_to(tmp_path)
    assert run_lock.get_runlayer_dir() != Path.home() / ".runlayer"


def test_lock_acquires_despite_home_lock_contention(
    isolated_scan_run_lock: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate a concurrent worker holding the home-derived lock.

    Hermetic: HOME/USERPROFILE point at a fresh fake home, so nothing outside
    this test can hold the contending lock and no real-home files are touched.
    Pre-fix, the default lock path resolved to the home-derived path and this
    acquire returned None (the CI collision); the fixture must keep them apart.
    """
    fake_home = tmp_path / "fake-home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setenv("USERPROFILE", str(fake_home))

    home_lock = paths.get_runlayer_dir() / "aiwatch-scan.lock"
    holder = acquire_scan_run_lock(home_lock)
    assert holder is not None  # fresh fake home: nothing else can hold it
    try:
        lock = acquire_scan_run_lock()
        assert lock is not None, "default lock path collided with the home lock"
        lock.close()
    finally:
        holder.close()

    assert (isolated_scan_run_lock / "aiwatch-scan.lock").exists()
    assert not (fake_home / ".runlayer-scan-lock").exists()
