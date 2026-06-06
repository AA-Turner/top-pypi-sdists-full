"""macOS install-window state for the bootstrap LaunchDaemon's fast-retry."""

from __future__ import annotations

import time
from enum import Enum
from pathlib import Path

INSTALL_STAMP_PATH = Path("/var/db/com.runlayer.aiwatch/.install-time")
INSTALL_WINDOW_SECONDS = 10 * 60


class InstallWindowState(str, Enum):
    NO_STAMP = "no_stamp"
    INSIDE = "inside"
    OUTSIDE = "outside"


def install_window_state(*, now: float | None = None) -> InstallWindowState:
    """``NO_STAMP`` if missing/unreadable; ``INSIDE`` if mtime within window; else ``OUTSIDE``."""
    try:
        stamp_mtime = INSTALL_STAMP_PATH.stat().st_mtime
    except OSError:
        return InstallWindowState.NO_STAMP
    elapsed = (now if now is not None else time.time()) - stamp_mtime
    if elapsed < INSTALL_WINDOW_SECONDS:
        return InstallWindowState.INSIDE
    return InstallWindowState.OUTSIDE
