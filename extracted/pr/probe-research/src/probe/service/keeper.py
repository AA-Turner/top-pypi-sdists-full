"""The OS keeper: the system starts the Probe service again after a crash (plan D35).

Once the service records sessions itself (A2), a service that dies (an OOM
kill, a crash) stops every hosted session's recording until something starts
it again; the hooks do at the next prompt or turn end, which a long autonomous
turn may not have. So the system's own scheduler runs this every minute:

    Linux    a systemd user timer (`probe-service-keeper.timer` + `.service`,
             `~/.config/systemd/user/`), when a user manager answers
    macOS    a launchd agent (`ai.prbe.probe-service-keeper`, StartInterval 60,
             `~/Library/LaunchAgents/`), when the GUI domain exists

`python -I -m probe.service.keeper`: when `recorders.json` names a session
whose agent still runs and no service answers, start one (`client.ensure`);
it resumes every session it recorded. Otherwise nothing, and exit. Cheap: a
file read and a socket connect, once a minute.

The service installs it when it starts (`install`, idempotent: rewritten only
when its interpreter changed), never under a test's HOME (only the account's
own home folder), never with PROBE_SERVICE_KEEPER=0; Uninstall removes it
(`remove`). It never runs the service itself: who starts the service, and how
it stops when idle, is unchanged.

Stdlib only.
"""

from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
from pathlib import Path

from . import paths, procid

ENV = "PROBE_SERVICE_KEEPER"
NAME = "probe-service-keeper"
LABEL = "ai.prbe.probe-service-keeper"
INTERVAL_S = 60
TIMEOUT_S = 10


def _own_home() -> bool:
    """HOME is this account's home folder (not a test's, not a sandbox's)."""
    try:
        import pwd

        return os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir) == os.path.realpath(str(Path.home()))
    except (ImportError, KeyError, OSError):
        return False


def wanted() -> bool:
    return os.name == "posix" and os.environ.get(ENV, "1") != "0" and _own_home()


def _manager_env() -> dict:
    """The environment `systemctl --user` needs to find this user's manager:
    the service runs with a clean one (`client._clean_env`), without
    XDG_RUNTIME_DIR or the session bus, so they are filled in from
    `/run/user/<uid>` when that is this user's."""
    env = dict(os.environ)
    if hasattr(os, "getuid"):
        runtime = Path(env.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}")
        try:
            if runtime.is_dir() and runtime.stat().st_uid == os.getuid():
                env["XDG_RUNTIME_DIR"] = str(runtime)
                bus = runtime / "bus"
                if "DBUS_SESSION_BUS_ADDRESS" not in env and bus.exists():
                    env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path={bus}"
        except OSError:
            pass
    return env


def _run(argv: list[str]) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=TIMEOUT_S, check=False,
                              stdin=subprocess.DEVNULL, env=_manager_env())
    except (OSError, subprocess.SubprocessError):
        return None


def _python() -> str | None:
    """The interpreter the keeper runs: the tool path's (a switch moves it to
    each new version), else the one the service runs now."""
    with contextlib.suppress(Exception):
        from probe._shared import installs

        stable = installs.env_python(installs.tool_env())
        if stable.exists():
            return str(stable)
    from . import client

    return client.runtime_python()


def _write(path: Path, text: str) -> bool:
    """Write `text` when it differs. True when it changed."""
    try:
        if path.read_text(encoding="utf-8") == text:
            return False
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)
    return True


# -- Linux: a systemd user timer --------------------------------------------------


def _systemd_dir() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    return (Path(base) if base else Path.home() / ".config") / "systemd" / "user"


def _systemd_units(python: str) -> dict[str, str]:
    quoted = python.replace("\\", "\\\\").replace('"', '\\"')
    return {
        f"{NAME}.service": (
            "[Unit]\nDescription=Start the Probe service again when it stopped while recording\n\n"
            f'[Service]\nType=oneshot\nExecStart="{quoted}" -I -m probe.service.keeper\n'
            # The service it starts must outlive it: by default systemd stops
            # every process of the unit once the oneshot exits.
            "KillMode=process\n"
        ),
        f"{NAME}.timer": (
            "[Unit]\nDescription=Check the Probe service every minute while it records\n\n"
            f"[Timer]\nOnBootSec={INTERVAL_S}s\nOnUnitActiveSec={INTERVAL_S}s\nAccuracySec=10s\n\n"
            "[Install]\nWantedBy=timers.target\n"
        ),
    }


def _install_systemd(python: str) -> str:
    probe = _run(["systemctl", "--user", "show-environment"])
    if probe is None or probe.returncode != 0:
        return "no systemd user manager"
    folder = _systemd_dir()
    changed = False
    for name, text in _systemd_units(python).items():
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


# -- macOS: a launchd agent --------------------------------------------------------


def _plist_path() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def _plist(python: str) -> str:
    import plistlib

    return plistlib.dumps({
        "Label": LABEL,
        "ProgramArguments": [python, "-I", "-m", "probe.service.keeper"],
        "StartInterval": INTERVAL_S,
        "RunAtLoad": False,
        # The service it starts must outlive it (launchd kills a finished job's group).
        "AbandonProcessGroup": True,
        "ProcessType": "Background",
        "StandardOutPath": "/dev/null",
        "StandardErrorPath": "/dev/null",
    }).decode("utf-8")


def _install_launchd(python: str) -> str:
    domain = f"gui/{os.getuid()}"
    probe = _run(["launchctl", "print", domain])
    if probe is None or probe.returncode != 0:
        return "no launchd GUI session"
    path = _plist_path()
    changed = _write(path, _plist(python))
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


# -- the two ends ------------------------------------------------------------------


OFF_NAME = "keeper-off"


def _off_path() -> Path:
    return paths.root_dir() / OFF_NAME


def allow() -> None:
    """A setup installs Probe again: the next service may install the keeper."""
    with contextlib.suppress(OSError):
        _off_path().unlink()


def _locked():
    """One install or removal at a time (the service's start races Uninstall)."""
    import fcntl

    paths.private_dir(paths.root_dir())
    handle = open(paths.root_dir() / "keeper.lock", "a")  # noqa: SIM115 -- closed by the caller
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    return handle


def install() -> str:
    """Make sure the system runs the keeper (from the service's start). Returns
    what happened. Never raises. Never after an Uninstall (`remove`), until a
    setup allows it again (`allow`)."""
    if not wanted():
        return "not wanted"
    try:
        with _locked():
            if _off_path().exists():
                return "not wanted (uninstalled)"
            return _install()
    except Exception as exc:  # noqa: BLE001 -- the hooks still start the service
        return f"failed: {exc!r}"[:300]


def _install() -> str:
    try:
        python = _python()
        if python is None:
            return "no interpreter"
        if sys.platform == "darwin":
            return _install_launchd(python)
        if sys.platform.startswith("linux"):
            return _install_systemd(python)
        return "unsupported"
    except Exception as exc:  # noqa: BLE001 -- the hooks still start the service
        return f"failed: {exc!r}"[:300]


def remove() -> None:
    """Uninstall: the system no longer runs the keeper, and no service
    installs it again until a setup allows it. Only for this account's own
    home (never a test's: its user manager is the real account's). Never raises."""
    if not _own_home():
        return
    with contextlib.suppress(Exception):
        with _locked():
            paths.private_dir(paths.root_dir())
            _off_path().touch()
            if sys.platform == "darwin":
                _remove_launchd()
            elif sys.platform.startswith("linux"):
                _remove_systemd()


def needed() -> bool:
    """Does a session the service recorded still have its agent running?"""
    from .recorders import RECORDERS_NAME

    try:
        data = json.loads((paths.service_dir() / RECORDERS_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    for session in (data.get("sessions") or []) if isinstance(data, dict) else []:
        owner = session.get("owner") if isinstance(session, dict) else None
        if isinstance(owner, dict):
            with contextlib.suppress(KeyError, TypeError, ValueError):
                if procid.alive(int(owner["pid"]), str(owner["start_time"])) is not False:
                    return True
    return False


def main() -> int:
    if os.name != "posix" or not needed():
        return 0
    from . import client

    conn = client.connect(0.5)
    if conn is not None:
        conn.close()
        return 0
    client.ensure()
    return 0


if __name__ == "__main__":
    sys.exit(main())
