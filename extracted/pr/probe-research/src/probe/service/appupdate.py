"""The desktop app on this machine, for the update cycle's `app` step (plan D3, X4; "the service owns every update").

    find      /Applications/Probe.app, else ~/Applications/Probe.app, whose
              Info.plist says CFBundleIdentifier == ai.prbe.desktop
    version   its CFBundleShortVersionString

The service decides when the app checks for its update and records what it
did; the open app's own signed updater checks, downloads, verifies (minisign,
the key it ships) and swaps the bundle (`updater.py`: `update.check_now`'s
`app`, the `app.check` event, `update.app_result`). The service never launches
the app: a closed app is checked at its next launch. This module only reads the
installed bundle, to tell a closed app from none at all.

Stdlib only; `plistlib` is imported when an app is found (the update cycle
preloads it before it replaces the CLI's env, plan R2).
"""

from __future__ import annotations

from pathlib import Path

from . import paths

BUNDLE_ID = "ai.prbe.desktop"
APP_NAME = "Probe.app"


def candidates() -> list[Path]:
    return [Path("/Applications") / APP_NAME, paths.home() / "Applications" / APP_NAME]


def info(app: Path) -> dict | None:
    """The bundle's Info.plist, or None when it has none we can read."""
    import plistlib

    try:
        with open(app / "Contents" / "Info.plist", "rb") as handle:
            data = plistlib.load(handle)
    except (OSError, ValueError, plistlib.InvalidFileException):
        return None
    return data if isinstance(data, dict) else None


def find() -> tuple[Path | None, dict | None]:
    """The first installed Probe.app that is ours, and its Info.plist."""
    for app in candidates():
        if not (app / "Contents" / "Info.plist").is_file():
            continue
        data = info(app)
        if data is not None and data.get("CFBundleIdentifier") == BUNDLE_ID:
            return app, data
    return None, None


def installed() -> dict | None:
    """`{app, version}` of the installed Probe.app, or None when there is none.
    Never raises, never starts anything."""
    try:
        app, data = find()
    except Exception:  # noqa: BLE001 -- a diagnostic: unknown reads as none
        return None
    if app is None or data is None:
        return None
    version = data.get("CFBundleShortVersionString")
    return {"app": str(app), "version": version if isinstance(version, str) else None}
