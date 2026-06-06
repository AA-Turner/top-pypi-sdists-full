"""Tests for ``runlayer_cli.install_window`` — drives the bootstrap LaunchDaemon's bounded fast-retry."""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import patch

from runlayer_cli.install_window import (
    INSTALL_WINDOW_SECONDS,
    InstallWindowState,
    install_window_state,
)


def _patch_stamp_path(path: Path):
    return patch("runlayer_cli.install_window.INSTALL_STAMP_PATH", path)


class TestInstallWindowState:
    def test_no_stamp_when_file_missing(self, tmp_path):
        with _patch_stamp_path(tmp_path / "missing"):
            assert install_window_state() is InstallWindowState.NO_STAMP

    def test_inside_when_stamp_younger_than_window(self, tmp_path):
        stamp = tmp_path / ".install-time"
        stamp.touch()
        now = stamp.stat().st_mtime + 60
        with _patch_stamp_path(stamp):
            assert install_window_state(now=now) is InstallWindowState.INSIDE

    def test_outside_when_stamp_older_than_window(self, tmp_path):
        stamp = tmp_path / ".install-time"
        stamp.touch()
        now = stamp.stat().st_mtime + INSTALL_WINDOW_SECONDS + 1
        with _patch_stamp_path(stamp):
            assert install_window_state(now=now) is InstallWindowState.OUTSIDE

    def test_boundary_at_exact_window_is_outside(self, tmp_path):
        """Strict ``<`` comparison: elapsed == window → OUTSIDE."""
        stamp = tmp_path / ".install-time"
        stamp.touch()
        now = stamp.stat().st_mtime + INSTALL_WINDOW_SECONDS
        with _patch_stamp_path(stamp):
            assert install_window_state(now=now) is InstallWindowState.OUTSIDE

    def test_no_stamp_when_stat_raises(self, tmp_path):
        bogus = tmp_path / ".install-time"

        class _Path:
            def stat(self):
                raise PermissionError("unreadable")

        with patch("runlayer_cli.install_window.INSTALL_STAMP_PATH", _Path()):
            assert install_window_state() is InstallWindowState.NO_STAMP

        # Sanity: real path works once present.
        bogus.touch()
        with _patch_stamp_path(bogus):
            assert install_window_state(now=time.time()) is InstallWindowState.INSIDE

    def test_default_now_uses_wall_clock(self, tmp_path):
        """No injected ``now`` ⇒ uses ``time.time()``; freshly touched stamp ⇒ INSIDE."""
        stamp = tmp_path / ".install-time"
        stamp.touch()
        with _patch_stamp_path(stamp):
            assert install_window_state() is InstallWindowState.INSIDE
