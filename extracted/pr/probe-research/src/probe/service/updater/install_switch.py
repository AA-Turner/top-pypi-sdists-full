"""side-by-side installs: will this update switch the tool path, and which CLI version the next service runs."""

from __future__ import annotations
import sys
from pathlib import Path
from probe.service.updater.settings import log


def side_by_side() -> bool:
    """Will this update install the CLI beside the running one (D6)? Then a
    run or a daemon worker keeps its version, and nothing waits for them.
    Not the first switch, which moves the folder every running process reads
    its files through (`installs.needs_migration`): that one waits for a quiet
    machine, as an in-place update does. Unknown reads as no: the update waits
    as before."""
    try:
        from probe.shared.updates import installs

        return installs.usable() and not installs.needs_migration()
    except Exception:  # noqa: BLE001
        return False


def _switched() -> bool:
    """Does the tool path name a version env now (a side-by-side switch)?"""
    try:
        from probe.shared.updates import installs

        return installs.active() is not None
    except Exception:  # noqa: BLE001
        return False


def _resolved(prefix: str) -> Path:
    try:
        return Path(prefix).resolve()
    except OSError:
        return Path(prefix)


#: The env this process loaded its code from, resolved once at its start: a
#: service started through the tool path's link reads the link's NEW target
#: after a switch, while its code is still the old env's.
STARTED_ENV = _resolved(sys.prefix)


def _env_moved(started: Path | None = None) -> bool:
    """Does the tool path name another env than the one this service started
    from (`STARTED_ENV`), at the same version (a broken env rebuilt in a folder
    of its own, `<v>+g<N>`: plan R-T3)? Then this service is the old one, as
    after a version change, and restarts onto it."""
    try:
        from probe.shared.updates import installs

        active = installs.active()
        return active is not None and (started or STARTED_ENV) != active
    except Exception:  # noqa: BLE001
        return False


def runtime_follows_switch(installed: str) -> str | None:
    """The CLI version the next service runs, given `installed`: what
    runtime.json's interpreter answered. When the tool path names another env
    than runtime.json's, runtime.json went stale after the switch: a restart
    would start the env the switch replaced, and its guard would watch for the
    wrong version and switch a good update back (10-28, probe demo: 0.339.0 ->
    0.342.0 installed, the guard was started "for 0.339.0" and undid it). Then
    runtime.json is pointed at the tool path's env and that env's version is
    the answer. `installed` unchanged with no switch layout; None when they
    disagree and it cannot be put right here (the env's version unreadable,
    Probe being uninstalled): no restart then, since any would be watched for
    the wrong version. Blocking (may read that version): a thread. Never
    raises."""
    try:
        from probe.shared.updates import installs

        from ...foundation import service_api as client

        active = installs.active()
        python = client.runtime_python()
        same = active is None or python is None or _resolved(str(Path(python).parent.parent)) == active
    except Exception as exc:  # noqa: BLE001 -- nothing to check against: as before
        log(f"could not check runtime.json against the tool path: {exc!r}")
        return installed
    if same:
        return installed
    try:
        version = installs._dist_info_version(active)
        if not version or client.uninstall_barrier() is not None:
            log(f"runtime.json names {python} ({installed}) while the tool path names {active} "
                f"({version or 'version unreadable'}): no restart this time")
            return None
        client.write_runtime(str(installs.env_python(active)), version)
        log(f"runtime.json named {python} ({installed}) while the tool path names {active} ({version}): "
            f"pointed it at {version}")
        return version
    except Exception as exc:  # noqa: BLE001 -- they disagree: no restart on what may be stale
        log(f"could not point runtime.json at the tool path's env: {exc!r}")
        return None


def _guard_record() -> dict | None:
    """What the last switch's guard found (D5), or None."""
    try:
        from .. import guard

        return guard.read()
    except Exception:  # noqa: BLE001
        return None
