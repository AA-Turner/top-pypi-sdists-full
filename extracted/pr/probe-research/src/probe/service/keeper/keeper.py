"""The OS keeper: the system starts the Probe service again after a crash (plan D35).

Once the service records sessions itself (A2), a service that dies (an OOM
kill, a crash) stops every hosted session's recording until something starts
it again; the hooks do at the next prompt or turn end, which a long autonomous
turn may not have. So the system's own scheduler runs this every minute:

    Linux    a systemd user timer (`probe-service-keeper.timer` + `.service`,
             `~/.config/systemd/user/`), when a user manager answers
    macOS    a launchd agent (`ai.prbe.probe-service-keeper`, StartInterval 60,
             `~/Library/LaunchAgents/`), when the GUI domain exists
    Windows  a Task Scheduler task for this user (`Probe service keeper`,
             every minute, `pythonw.exe`: no window)

`python -I -m probe.service.keeper`: when `recorders.json` names a session
whose agent still runs and no service answers, start one (`client.ensure`);
it resumes every session it recorded. Otherwise nothing, and exit. Cheap: a
file read and a socket connect, once a minute.

On Linux and macOS the unit does not run that python itself: it runs the
lifeboat's frozen wrapper, `/bin/sh ~/.local/state/probe/lifeboat/lifeboat.sh
keeper` (plan fool-proof-updates B2, `lifeboat.py`), which runs the lifeboat's
own hand-off (outside every release: it rescues a machine whose installed
updater is broken) and then this keeper with the active release's python.
The unit text names only that fixed path, never a release's files, so no
release can point it anywhere else; its writer is digest-pinned
(`tests/test_lifeboat.py`). Windows keeps its direct task (no `/bin/sh`).

"Answers" is a `service.hello` reply within HELLO_TIMEOUT_S, not a connect: a
wedged loop still takes connections into its backlog (crash-report plan B3).
A needed service that has not answered for DOWN_REPORT_S (none, `ensure`'s
back-off, or wedged) is reported to the Probe team once (`service_down`, the
same `probe.core.run report` the service runs, with the machine's consent:
`watch.decide_machine`), at most every REPORT_EVERY_S; `keeper.json` keeps
since when, and service.log gets one line per change.

The service installs it when it starts (`install`, idempotent: rewritten only
when its text changed), the lifeboat first, never under a test's HOME (only
the account's own home folder), never with PROBE_SERVICE_KEEPER=0; Uninstall
removes both (`remove`). The lifeboat alone is also installed, with the same
guards, by every update that succeeded and every `probe doctor`
(`install_lifeboat`): where no service ever runs (a pod under no_new_privs)
its sessions' starts still run it. It never runs the service itself: who starts the service, and how
it stops when idle, is unchanged.

Stdlib only.
"""

from __future__ import annotations

import contextlib
import json
import os
import sys
from collections.abc import Mapping
from pathlib import Path

from ..updater import lifeboat
from ...foundation.service_api import paths, procid
from probe.service.keeper.check import Down, _answers, _settle, _uninstalling
from probe.service.keeper.home import _own_home
from probe.service.keeper.schedulers.launchd import _install_launchd, _remove_launchd
from probe.service.keeper.schedulers.systemd import _install_systemd, _remove_systemd
from probe.service.keeper.schedulers.windows_task import _install_schtasks, _remove_schtasks

ENV = "PROBE_SERVICE_KEEPER"


def wanted() -> bool:
    return os.name in ("posix", "nt") and os.environ.get(ENV, "1") != "0" and _own_home()


def _python() -> str | None:
    """The interpreter Windows' keeper task runs: the tool path's (a switch
    moves it to each new version), else the one the service runs now.
    Elsewhere the lifeboat's wrapper finds it (env.json's `active_python`)."""
    with contextlib.suppress(Exception):
        from probe.shared.updates import installs

        stable = installs.env_python(installs.tool_env())
        if stable.exists():
            return str(stable)
    from ...foundation import service_api as client

    return client.runtime_python()


# -- the two ends ------------------------------------------------------------------


OFF_NAME = "keeper-off"


def _off_path() -> Path:
    return paths.root_dir() / OFF_NAME


def allow() -> None:
    """A setup installs Probe again: the next service may install the keeper."""
    with contextlib.suppress(OSError):
        _off_path().unlink()


#: Past this, a lock that never comes is a failure ("failed: ..."), not a hang.
LOCK_WAIT_S = 30.0


def _locked():
    """One install or removal at a time (the service's start races Uninstall)."""
    import time

    paths.private_dir(paths.root_dir())
    handle = open(paths.root_dir() / "keeper.lock", "a")  # noqa: SIM115 -- closed by the caller
    deadline = time.monotonic() + LOCK_WAIT_S
    while not paths.try_lock(handle.fileno()):  # fcntl, or msvcrt on Windows
        if time.monotonic() >= deadline:
            handle.close()
            raise TimeoutError("keeper.lock")
        time.sleep(0.05)
    return handle


def install(login: Mapping | None = None) -> str:
    """Make sure the system runs the keeper (from the service's start), the
    lifeboat first (env.json with `login`'s index settings: the login shell's).
    Returns what happened. Never raises. Never after an Uninstall (`remove`),
    until a setup allows it again (`allow`)."""
    if not wanted():
        return "not wanted"
    if _uninstalling():
        return "not wanted (uninstalling)"
    try:
        with _locked():
            if _off_path().exists():
                return "not wanted (uninstalled)"
            boat = lifeboat.install(login)
            units = _install()
            return units if boat in ("current", "unsupported") else f"{units} (lifeboat: {boat})"
    except Exception as exc:  # noqa: BLE001 -- the hooks still start the service
        return f"failed: {exc!r}"[:300]


def refresh_lifeboat() -> str:
    """`install_lifeboat` from outside the service (every update whose CLI
    step ended ok, `probe doctor`), env.json's index settings the login
    shell's when it answers (asked with a clean environment, never the
    caller's: an agent sandbox's proxy is not the machine's), else the last
    ones kept. Never raises."""
    if not wanted():
        return "not wanted"
    return install_lifeboat(lifeboat.login_env())


def install_lifeboat(login: Mapping | None = None) -> str:
    """The lifeboat alone, with `install`'s guards and lock: a machine where
    no service runs gets one too, which its sessions' starts run
    (`hooks/dispatch.py`). `login`: the login shell's variables for env.json's
    index settings, None to keep the last ones. Returns what happened.
    Never raises."""
    if not wanted():
        return "not wanted"
    if _uninstalling():
        return "not wanted (uninstalling)"
    try:
        with _locked():
            if _off_path().exists():
                return "not wanted (uninstalled)"
            return lifeboat.install(login)
    except Exception as exc:  # noqa: BLE001 -- the update and doctor go on without it
        return f"failed: {exc!r}"[:300]


def _install() -> str:
    """The units, once the lifeboat's wrapper is there: a unit never names a
    file that is missing (units an older release wrote stay until then)."""
    try:
        if os.name == "nt":
            python = _python()
            return "no interpreter" if python is None else _install_schtasks(python)
        wrapper = lifeboat.wrapper_path()
        if not wrapper.is_file():
            return "no lifeboat"
        if sys.platform == "darwin":
            return _install_launchd(str(wrapper))
        if sys.platform.startswith("linux"):
            return _install_systemd(str(wrapper))
        return "unsupported"
    except Exception as exc:  # noqa: BLE001 -- the hooks still start the service
        return f"failed: {exc!r}"[:300]


def remove(*, mark_off: bool = True) -> None:
    """Uninstall: the system no longer runs the keeper (nor the lifeboat, whose
    folder goes), and no service installs either again until a setup allows it. Only for this account's own
    home (never a test's: its user manager is the real account's). Never raises.
    `mark_off=False` (`probe uninstall`, whose barrier keeps them from coming
    back while it runs): no `keeper-off` left behind for a reinstall to trip on."""
    if not _own_home():
        return
    with contextlib.suppress(Exception):
        with _locked():
            if mark_off:
                paths.private_dir(paths.root_dir())
                _off_path().touch()
            if sys.platform == "darwin":
                _remove_launchd()
            elif sys.platform.startswith("linux"):
                _remove_systemd()
            elif os.name == "nt":
                _remove_schtasks()
            lifeboat.remove()


def needed() -> bool:
    """Does a session the service recorded still have its agent running? Not
    one held because Probe is off for it (an open gap, its switch still
    `off`): Probe off keeps no service running. Once its switch reads on, it
    is needed again, so the service comes back and records it from there."""
    from ..sessions import capture_gate
    from ..sessions.recorders.restarts import RECORDERS_NAME

    try:
        data = json.loads((paths.service_dir() / RECORDERS_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    for session in (data.get("sessions") or []) if isinstance(data, dict) else []:
        owner = session.get("owner") if isinstance(session, dict) else None
        if isinstance(owner, dict) and capture_gate.is_open(capture_gate.gaps_of(session)) \
                and capture_gate.is_off(session):
            continue
        if isinstance(owner, dict):
            with contextlib.suppress(KeyError, TypeError, ValueError):
                if procid.alive(int(owner["pid"]), str(owner["start_time"])) is not False:
                    return True
    return False


def main() -> int:
    if _uninstalling():
        return 0  # nothing to keep: Probe is being uninstalled
    if not needed():
        _settle(None)
        return 0
    from ...foundation import service_api as client

    down = _answers()
    if down is None:
        _settle(None)
        return 0
    started = client.ensure()
    if started == client.Ensured.BACKOFF:
        down = Down.BACKOFF
    _settle(down, started)
    return 0


if __name__ == "__main__":
    sys.exit(main())
