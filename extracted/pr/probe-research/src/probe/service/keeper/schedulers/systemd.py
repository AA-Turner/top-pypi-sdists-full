"""Linux: a systemd user timer + oneshot."""

from __future__ import annotations

import contextlib
import os
from pathlib import Path
from probe.service.keeper.scheduler import INTERVAL_S, NAME, START_TIMEOUT_S, _run, _write


# -- Linux: a systemd user timer --------------------------------------------------


def _systemd_dir() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    return (Path(base) if base else Path.home() / ".config") / "systemd" / "user"


# The two unit writers below are FROZEN with the lifeboat's wrapper: their text
# for a fixed path is digest-pinned (`tests/test_lifeboat.py`, FROZEN_UNITS).
# Change them deliberately: every keeper on every machine runs what they write.


def _systemd_units(wrapper: str) -> dict[str, str]:
    """The timer and its oneshot, `/bin/sh <wrapper> keeper` (systemd's own
    quoting: backslash and `"` escaped, `%` and `$` doubled)."""
    quoted = wrapper.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%").replace("$", "$$")
    return {
        f"{NAME}.service": (
            "[Unit]\nDescription=Start the Probe service again when it stopped while recording\n\n"
            f'[Service]\nType=oneshot\nExecStart=/bin/sh "{quoted}" keeper\n'
            # The service it starts, and a rescue the lifeboat starts, must
            # outlive it: by default systemd stops every process of the unit
            # once the oneshot exits.
            "KillMode=process\n"
            # A oneshot has no start timeout by default: a wrapper stuck past
            # every bound of its own (each child's, given up 30 s after it)
            # must not hold the timer's next run off for good.
            f"TimeoutStartSec={START_TIMEOUT_S}\n"
        ),
        f"{NAME}.timer": (
            "[Unit]\nDescription=Check the Probe service every minute while it records\n\n"
            f"[Timer]\nOnBootSec={INTERVAL_S}s\nOnUnitActiveSec={INTERVAL_S}s\nAccuracySec=10s\n\n"
            "[Install]\nWantedBy=timers.target\n"
        ),
    }


def systemd_manager() -> bool:
    """Does this user's systemd manager answer (Linux)? The keeper's units
    need one; a container or an SSH login without a user session has none."""
    probe = _run(["systemctl", "--user", "show-environment"])
    return probe is not None and probe.returncode == 0


def _install_systemd(wrapper: str) -> str:
    if not systemd_manager():
        return "no systemd user manager"
    folder = _systemd_dir()
    changed = False
    for name, text in _systemd_units(wrapper).items():
        changed = _write(folder / name, text) or changed
    if changed:
        _run(["systemctl", "--user", "daemon-reload"])
    active = _run(["systemctl", "--user", "is-active", f"{NAME}.timer"])
    if changed or active is None or active.stdout.strip() != "active":
        done = _run(["systemctl", "--user", "enable", "--now", f"{NAME}.timer"])
        if done is None or done.returncode != 0:
            return f"systemctl enable failed: {(done.stderr if done else '').strip()[:200]}"
    return "installed" if changed else "current"


def _remove_systemd() -> None:
    _run(["systemctl", "--user", "disable", "--now", f"{NAME}.timer"])
    for name in (f"{NAME}.service", f"{NAME}.timer"):
        with contextlib.suppress(OSError):
            (_systemd_dir() / name).unlink()
    _run(["systemctl", "--user", "daemon-reload"])
