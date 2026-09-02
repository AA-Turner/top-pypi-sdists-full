"""macOS-only install-window state for the bootstrap LaunchDaemon's fast-retry.

This is a macOS launchd concept: the bootstrap LaunchDaemon's
``KeepAlive(SuccessfulExit=false)`` fast-retries ``aiwatch setup hooks install``
every ``ThrottleInterval`` until the postinstall stamp at ``INSTALL_STAMP_PATH``
ages out, at which point the install command softens its credential-gate exit to
0 so launchd idles. Windows has no equivalent — the ``AIWatchHooks`` Scheduled
Task is at-boot + hourly with no KeepAlive (Task Scheduler just records
``LastTaskResult`` and waits for the next tick), so there is no window to bound
and no stamp. The function returns ``NO_STAMP`` off macOS to keep that contract
explicit (the consumer then takes its strict exit-4 branch everywhere but macOS).
"""

from __future__ import annotations

import sys
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
    """``NO_STAMP`` off macOS or if missing/unreadable; ``INSIDE`` if mtime within window; else ``OUTSIDE``."""
    if sys.platform != "darwin":
        return InstallWindowState.NO_STAMP
    try:
        stamp_mtime = INSTALL_STAMP_PATH.stat().st_mtime
    except OSError:
        return InstallWindowState.NO_STAMP
    elapsed = (now if now is not None else time.time()) - stamp_mtime
    if elapsed < INSTALL_WINDOW_SECONDS:
        return InstallWindowState.INSIDE
    return InstallWindowState.OUTSIDE
