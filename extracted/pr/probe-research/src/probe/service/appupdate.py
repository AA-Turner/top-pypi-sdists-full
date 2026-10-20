"""The desktop app's update: the service decides when, the app's own signed updater installs (plan D3, X4).

    find      /Applications/Probe.app, else ~/Applications/Probe.app
    gate      CFBundleIdentifier == ai.prbe.desktop, and ProbeBackgroundUpdate
              >= 1 in its Info.plist (the build has `--background-update`:
              prbe-ai/desktop #11; an older one would open hidden and stay)
    not now   while the app runs, in any instance (its own banner offers the
              update then), and a copy never opened: it still carries the
              `com.apple.quarantine` attribute, and launching it would put
              Gatekeeper's first-launch prompt in front of the researcher
    launch    open -n -g -j <app> --args --background-update. `-n`: without
              it, `open` on a Probe that is running or still starting starts
              no process and drops `--args` without a word
    result    `<service dir>/app-update.json`, written by the app when it quits
              (`{version_before, version_after, result: updated|current|failed,
              error, finished_at}`), read once its `finished_at` is this
              attempt's, for at most RESULT_TIMEOUT_S. `open` returns before
              the app is done, so its exit status says nothing about the update.
              `current` WITH an error is an app that found another of itself
              holding its lock ("Probe is already running"): it checked
              nothing, so it reads as `running`, asked again next cycle.

The service never downloads, verifies or swaps the bundle itself: the app's
updater checks the minisign signature with the key it ships.

Stdlib only; `plistlib` is imported when an app is found (the update cycle
preloads it before it replaces the CLI's env, plan R2).
"""

from __future__ import annotations

import asyncio
import calendar
import json
import os
import subprocess
import time
from pathlib import Path

from . import paths

BUNDLE_ID = "ai.prbe.desktop"
CAPABILITY_KEY = "ProbeBackgroundUpdate"
APP_NAME = "Probe.app"
BACKGROUND_FLAG = "--background-update"
#: The app's own bound (prbe-ai/desktop `background_update.rs`): its 10-minute
#: TIME_LIMIT, 60 s more for an install under way, 30 s for it on quit, and a
#: margin: an app still within its own limit is not a timeout.
RESULT_TIMEOUT_S = 12 * 60
POLL_S = 1.0
_PS_TIMEOUT_S = 5.0
#: Set by macOS on a download until its first launch is allowed.
QUARANTINE_XATTR = "com.apple.quarantine"


class Outcome:
    NOT_INSTALLED = "not_installed"  # no Probe.app, or one that is not ours
    NOT_CAPABLE = "not_capable"  # a build without --background-update
    RUNNING = "running"  # the app runs (or said it found itself running): its own banner updates it
    QUARANTINED = "quarantined"  # never opened: launching it would show Gatekeeper's prompt
    UPDATED = "updated"
    CURRENT = "current"
    FAILED = "failed"
    TIMEOUT = "timeout"  # no result for this attempt within RESULT_TIMEOUT_S


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


def capable(data: dict) -> bool:
    value = data.get(CAPABILITY_KEY)
    if isinstance(value, bool):
        return value
    try:
        return int(value) >= 1
    except (TypeError, ValueError):
        return False


def find() -> tuple[Path | None, dict | None]:
    """The first installed Probe.app that is ours, and its Info.plist."""
    for app in candidates():
        if not (app / "Contents" / "Info.plist").is_file():
            continue
        data = info(app)
        if data is not None and data.get("CFBundleIdentifier") == BUNDLE_ID:
            return app, data
    return None, None


def running(app: Path) -> bool:
    """Does any process run from inside this bundle? Unknown reads as yes:
    launching into a running app is the one thing this must never do."""
    prefixes = {f"{app}/Contents/MacOS/"}
    try:
        prefixes.add(f"{app.resolve()}/Contents/MacOS/")
    except OSError:
        pass
    try:
        out = subprocess.run(
            ["ps", "axww", "-o", "args="],
            capture_output=True,
            text=True,
            timeout=_PS_TIMEOUT_S,
            check=False,
            env={**os.environ, "LC_ALL": "C"},
        )
    except (OSError, subprocess.SubprocessError):
        return True
    if out.returncode != 0:
        return True
    return any(line.strip().startswith(tuple(prefixes)) for line in out.stdout.splitlines())


def quarantined(app: Path) -> bool:
    """Does the bundle still carry `com.apple.quarantine` (never opened)?

    `xattr -p` exits 0 when it does. No `xattr` at all is a system without
    quarantine (not macOS): no. Anything else unknown reads as yes, like
    `running`: a prompt nobody asked for is the thing to avoid."""
    try:
        out = subprocess.run(
            ["xattr", "-p", QUARANTINE_XATTR, str(app)],
            capture_output=True,
            timeout=_PS_TIMEOUT_S,
            check=False,
        )
    except FileNotFoundError:
        return False
    except (OSError, subprocess.SubprocessError):
        return True
    return out.returncode == 0


def _finished_at(raw: object) -> float | None:
    """RFC 3339 UTC to the second (`2026-10-19T05:30:07Z`) as epoch seconds."""
    if not isinstance(raw, str):
        return None
    text = raw.strip().replace("z", "Z")
    for pattern in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S+00:00"):
        try:
            return float(calendar.timegm(time.strptime(text, pattern)))
        except ValueError:
            continue
    return None


def read_result(since: float) -> dict | None:
    """The app's report for an attempt started at `since`, or None (absent,
    unreadable, or an earlier attempt's)."""
    try:
        data = json.loads(paths.app_update_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    finished = _finished_at(data.get("finished_at"))
    # To the second: an attempt started at 12.7 s may finish "at 12".
    if finished is None or finished < int(since):
        return None
    return data


async def update(*, timeout: float = RESULT_TIMEOUT_S, poll: float = POLL_S) -> dict:
    """Update the desktop app if it is installed, capable and closed.

    `{"outcome": Outcome, "app"?, "version_before"?, "version_after"?, "error"?}`.
    Never raises.
    """
    app, data = find()
    if app is None or data is None:
        return {"outcome": Outcome.NOT_INSTALLED}
    base = {"app": str(app), "version_before": data.get("CFBundleShortVersionString")}
    if not capable(data):
        return {**base, "outcome": Outcome.NOT_CAPABLE}
    if await asyncio.to_thread(quarantined, app):
        return {**base, "outcome": Outcome.QUARANTINED}
    if await asyncio.to_thread(running, app):
        return {**base, "outcome": Outcome.RUNNING}
    started = time.time()
    try:
        opener = await asyncio.create_subprocess_exec(
            "open",
            "-n",
            "-g",
            "-j",
            str(app),
            "--args",
            BACKGROUND_FLAG,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        _, err = await asyncio.wait_for(opener.communicate(), 60)
    except (OSError, asyncio.TimeoutError) as exc:
        return {**base, "outcome": Outcome.FAILED, "error": f"open could not launch the app: {exc}"}
    if opener.returncode != 0:
        said = err.decode("utf-8", "replace").strip()[:500]
        return {**base, "outcome": Outcome.FAILED, "error": f"open exited {opener.returncode}: {said}"}
    deadline = time.monotonic() + timeout
    while True:
        result = read_result(started)
        if result is not None:
            outcome = result.get("result")
            if outcome not in (Outcome.UPDATED, Outcome.CURRENT, Outcome.FAILED):
                outcome = Outcome.FAILED
            elif outcome == Outcome.CURRENT and result.get("error"):
                # Another Probe held the app's lock: nothing was checked.
                outcome = Outcome.RUNNING
            out = {
                **base,
                "outcome": outcome,
                "version_before": result.get("version_before") or base["version_before"],
                "version_after": result.get("version_after"),
            }
            if result.get("error"):
                out["error"] = str(result["error"])[:500]
            return out
        if time.monotonic() >= deadline:
            return {**base, "outcome": Outcome.TIMEOUT, "error": f"no result from the app within {int(timeout)} s"}
        await asyncio.sleep(poll)
