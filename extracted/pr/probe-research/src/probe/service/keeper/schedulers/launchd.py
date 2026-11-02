"""macOS: a launchd agent."""

from __future__ import annotations

import contextlib
import os
from pathlib import Path
from probe.service.keeper.scheduler import INTERVAL_S, LABEL, _run, _write


# -- macOS: a launchd agent --------------------------------------------------------


def _plist_path() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def _plist(wrapper: str) -> str:
    """The launch agent: `/bin/sh <wrapper> keeper` every minute."""
    import plistlib

    return plistlib.dumps({
        "Label": LABEL,
        "ProgramArguments": ["/bin/sh", wrapper, "keeper"],
        "StartInterval": INTERVAL_S,
        "RunAtLoad": False,
        # The service it starts, and a rescue the lifeboat starts, must outlive
        # it (launchd kills a finished job's group).
        "AbandonProcessGroup": True,
        "ProcessType": "Background",
        "StandardOutPath": "/dev/null",
        "StandardErrorPath": "/dev/null",
    }).decode("utf-8")


def _install_launchd(wrapper: str) -> str:
    domain = f"gui/{os.getuid()}"
    probe = _run(["launchctl", "print", domain])
    if probe is None or probe.returncode != 0:
        return "no launchd GUI session"
    path = _plist_path()
    changed = _write(path, _plist(wrapper))
    loaded = _run(["launchctl", "print", f"{domain}/{LABEL}"])
    if changed and loaded is not None and loaded.returncode == 0:
        _run(["launchctl", "bootout", f"{domain}/{LABEL}"])
        loaded = None
    if loaded is None or loaded.returncode != 0:
        done = _run(["launchctl", "bootstrap", domain, str(path)])
        if done is None or done.returncode != 0:
            return f"launchctl bootstrap failed: {(done.stderr if done else '').strip()[:200]}"
    return "installed" if changed else "current"


def _remove_launchd() -> None:
    _run(["launchctl", "bootout", f"gui/{os.getuid()}/{LABEL}"])
    with contextlib.suppress(OSError):
        _plist_path().unlink()
