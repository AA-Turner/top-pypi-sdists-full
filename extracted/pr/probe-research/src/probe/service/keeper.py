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

"Answers" is a `service.hello` reply within HELLO_TIMEOUT_S, not a connect: a
wedged loop still takes connections into its backlog (crash-report plan B3).
A needed service that has not answered for DOWN_REPORT_S (none, `ensure`'s
back-off, or wedged) is reported to the Probe team once (`service_down`, the
same `probe.core.run report` the service runs, with the machine's consent:
`watch.decide_machine`), at most every REPORT_EVERY_S; `keeper.json` keeps
since when, and service.log gets one line per change.

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
import time
from pathlib import Path

from . import paths, procid

ENV = "PROBE_SERVICE_KEEPER"
NAME = "probe-service-keeper"
LABEL = "ai.prbe.probe-service-keeper"
INTERVAL_S = 60
TIMEOUT_S = 10


def _windows_profile() -> str | None:
    try:
        import ctypes
        from ctypes import wintypes

        userenv = ctypes.WinDLL("userenv")
        k32 = ctypes.WinDLL("kernel32")
        adv = ctypes.WinDLL("advapi32")
        k32.GetCurrentProcess.restype = wintypes.HANDLE
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        adv.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
        userenv.GetUserProfileDirectoryW.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        token = wintypes.HANDLE()
        if not adv.OpenProcessToken(k32.GetCurrentProcess(), 0x0008, ctypes.byref(token)):
            return None
        size = wintypes.DWORD(1024)
        buf = ctypes.create_unicode_buffer(size.value)
        ok = userenv.GetUserProfileDirectoryW(token, buf, ctypes.byref(size))
        k32.CloseHandle(token)
        return buf.value if ok else None
    except (OSError, AttributeError):
        return None


def _own_home() -> bool:
    """HOME is this account's home folder (not a test's, not a sandbox's)."""
    if os.name == "nt":
        profile = _windows_profile()
        return bool(profile) and os.path.normcase(os.path.realpath(profile)) == os.path.normcase(
            os.path.realpath(str(Path.home())))
    try:
        import pwd

        return os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir) == os.path.realpath(str(Path.home()))
    except (ImportError, KeyError, OSError):
        return False


def wanted() -> bool:
    return os.name in ("posix", "nt") and os.environ.get(ENV, "1") != "0" and _own_home()


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


# -- Windows: a Task Scheduler task ----------------------------------------------------

def _task_name() -> str:
    """Task names are machine-wide: one per Windows user (by their SID)."""
    import hashlib

    try:
        from . import winpipe

        who = hashlib.sha256(winpipe.user_sid().encode("utf-8")).hexdigest()[:12]
    except Exception:  # noqa: BLE001
        who = hashlib.sha256(os.environ.get("USERNAME", "user").encode("utf-8")).hexdigest()[:12]
    return f"Probe service keeper {who}"


def _task_marker() -> Path:
    return paths.root_dir() / "keeper-task.txt"


def _task_xml(runner: str) -> str:
    """The task: every minute, indefinitely, only while this user is logged
    on, and on battery too (`schtasks /SC MINUTE` would take the AC-only
    defaults, and a laptop on battery would never start the service again)."""
    from xml.sax.saxutils import escape

    return (
        '<?xml version="1.0" encoding="UTF-16"?>\n'
        '<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">\n'
        "  <RegistrationInfo><Description>Start the Probe service again when it stopped while recording"
        "</Description></RegistrationInfo>\n"
        "  <Triggers><TimeTrigger><Repetition><Interval>PT1M</Interval>"
        "<StopAtDurationEnd>false</StopAtDurationEnd></Repetition>"
        "<StartBoundary>2026-01-01T00:00:00</StartBoundary><Enabled>true</Enabled></TimeTrigger></Triggers>\n"
        '  <Principals><Principal id="Author"><LogonType>InteractiveToken</LogonType>'
        "<RunLevel>LeastPrivilege</RunLevel></Principal></Principals>\n"
        "  <Settings><MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>"
        "<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>"
        "<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>"
        "<StartWhenAvailable>true</StartWhenAvailable>"
        "<RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>"
        "<IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings>"
        "<AllowStartOnDemand>true</AllowStartOnDemand><Enabled>true</Enabled><Hidden>true</Hidden>"
        "<RunOnlyIfIdle>false</RunOnlyIfIdle><ExecutionTimeLimit>PT5M</ExecutionTimeLimit>"
        "<Priority>7</Priority></Settings>\n"
        f'  <Actions Context="Author"><Exec><Command>{escape(runner)}</Command>'
        "<Arguments>-I -m probe.service.keeper</Arguments></Exec></Actions>\n"
        "</Task>\n"
    )


def _install_schtasks(python: str) -> str:
    windowless = Path(python).with_name("pythonw.exe")
    runner = str(windowless) if windowless.exists() else python
    xml = _task_xml(runner)
    try:
        if _task_marker().read_text(encoding="utf-8") == xml:
            listed = _run(["schtasks", "/Query", "/TN", _task_name()])
            if listed is not None and listed.returncode == 0:
                return "current"
    except OSError:
        pass
    definition = paths.root_dir() / f".keeper-task.{os.getpid()}.xml"
    try:
        definition.write_text(xml, encoding="utf-16")  # what schtasks reads (with its BOM)
        done = _run(["schtasks", "/Create", "/F", "/TN", _task_name(), "/XML", str(definition)])
    finally:
        with contextlib.suppress(OSError):
            definition.unlink()
    if done is None or done.returncode != 0:
        return f"schtasks /Create failed: {((done.stderr or done.stdout) if done else '').strip()[:200]}"
    with contextlib.suppress(OSError):
        _write(_task_marker(), xml)
    return "installed"


def _remove_schtasks() -> None:
    _run(["schtasks", "/Delete", "/F", "/TN", _task_name()])
    with contextlib.suppress(OSError):
        _task_marker().unlink()


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
        if os.name == "nt":
            return _install_schtasks(python)
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
            elif os.name == "nt":
                _remove_schtasks()


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


#: The keeper's record of a service that does not answer (crash-report plan B3).
STATE_NAME = "keeper.json"
#: A service answers when its `service.hello` reply comes within this: a
#: connect alone passes a wedged loop, whose socket still queues connections.
HELLO_TIMEOUT_S = 2.0
#: Needed and not answering this long: one `service_down` report ...
DOWN_REPORT_S = 300.0
#: ... and at most one in this long (the report's own dedupe window).
REPORT_EVERY_S = 6 * 3600.0


class Down:
    """Why no service answers (`service_down`'s `reason`)."""

    NO_SERVICE = "no_service"  # nothing to connect to
    WEDGED = "wedged"  # it takes the connection, never answers the hello
    BACKOFF = "backoff"  # `ensure` started 3 in a minute already: it starts none


def _answers() -> str | None:
    """None when a service replies to `service.hello` within HELLO_TIMEOUT_S;
    else why not (Down)."""
    from . import client
    from .protocol import Client

    conn = client.connect(HELLO_TIMEOUT_S)
    if conn is None:
        return Down.NO_SERVICE
    try:
        conn.hello(Client.CLI, "keeper")
        return None
    except client.ServiceError:
        return None  # it answered (another API, a refusal): it is up
    except (OSError, ValueError):
        return Down.WEDGED
    finally:
        conn.close()


def _log(message: str) -> None:
    """One line in service.log, with the keeper's own prefix (its stdout goes
    nowhere under launchd). Never raises."""
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with contextlib.suppress(OSError):
        fd = os.open(paths.log_path(), os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            os.write(fd, f"[{stamp}] probe-service-keeper[{os.getpid()}]: {message}\n".encode("utf-8", "replace"))
        finally:
            os.close(fd)


def _state() -> dict:
    from .watch import read_json

    data = read_json(paths.service_dir() / STATE_NAME)
    return data if isinstance(data, dict) else {}


def _save(state: dict) -> bool:
    """False when it could not be written (a full disk): nothing that depends
    on it being kept (the last report's time) may go on as if it were."""
    from .watch import write_json

    with contextlib.suppress(OSError):
        paths.private_dir(paths.service_dir())
    return write_json(paths.service_dir() / STATE_NAME, state)


#: The keeper's runs this far apart in wall OR monotonic time (a sleep, which
#: monotonic time does not count; a reboot, which restarts it; a timer that
#: stopped) do not add up: the minutes down are counted again from there.
GAP_S = 3 * INTERVAL_S
#: Monotonic time (the system's, shared by every process of one boot), a seam for tests.
_monotonic = time.monotonic


def _settle(down: str | None, started: str | None = None, *, now: float | None = None) -> None:
    """Keep `keeper.json`: since when a needed service has not answered, why,
    and for how long while the machine was awake (`down_for`: consecutive runs
    at most GAP_S apart in both clocks); one log line per change; past
    DOWN_REPORT_S of that, the `service_down` report (at most every
    REPORT_EVERY_S, and only once that is saved)."""
    now = time.time() if now is None else now
    mono = _monotonic()
    state = _state()
    since = state.get("down_since")
    if down is None:
        if isinstance(since, (int, float)):
            _log(f"the service answers again (after {max(0.0, now - since) / 60:.0f} min)")
            reported = state.get("reported_at")
            _save({"reported_at": reported} if isinstance(reported, (int, float)) else {})
        return
    checked, checked_mono, down_for = state.get("checked_at"), state.get("checked_mono"), state.get("down_for")
    numbers = all(isinstance(v, (int, float)) for v in (since, checked, checked_mono, down_for))
    if numbers and 0 <= now - checked <= GAP_S and 0 <= mono - checked_mono <= GAP_S:
        down_for = down_for + (mono - checked_mono)
        if state.get("reason") != down:
            _log(f"a session needs the service and none answers ({down}); ensure: {started}")
    else:
        if numbers:
            _log(f"none answers ({down}) after a gap (a sleep, a reboot): the minutes are counted again")
        else:
            _log(f"a session needs the service and none answers ({down}); ensure: {started}")
        since, down_for = now, 0.0
    state.update(down_since=since, reason=down, checked_at=now, checked_mono=mono, down_for=down_for,
                 ensure=started)
    reported = state.get("reported_at")
    due = down_for >= DOWN_REPORT_S and not (
        isinstance(reported, (int, float)) and 0 <= now - reported < REPORT_EVERY_S
    )
    if due:
        state["reported_at"] = now  # before the child: a keeper run next minute starts no second one
    saved = _save(state)
    if due and not saved:
        _log(f"service_down ({down}) not reported: the keeper's state could not be saved")
    elif due:
        _report(down, down_for, started)


def _report(down: str, seconds: float, started: str | None) -> None:
    """`service_down` (crash-report plan B3), with the machine's consent: every
    live session's (hosted ones by their environment, registered ones by their
    `report_env`), else the login shell's variables and the CLI config's."""
    from . import watch

    if not watch.reports_enabled():
        return
    try:
        live = watch.sessions_on_disk()
        login = None
        if not live:
            import asyncio

            login = asyncio.run(watch.login_env())
        allowed, why = watch.decide_machine(live, watch.config_base_url(), login)
    except Exception as exc:  # noqa: BLE001 -- unknown consent: no report
        allowed, why = False, f"consent unknown ({exc!r})"
    if not allowed:
        _log(f"service_down ({down}) not reported: {why}")
        return
    params = {
        "auto": True, "family": watch.Family.SERVICE_DOWN, "reason": down, "sid": None, "env": {},
        "facts": watch.bounded_facts({"down_s": round(seconds), "ensure": started, "sessions": len(live)}),
    }
    try:
        code, value = watch.report_blocking(params)
        said = watch.outcome(code, value)
    except OSError as exc:
        said = f"could not start: {exc}"
    _log(f"report service_down ({down}): {said}")


def main() -> int:
    if not needed():
        _settle(None)
        return 0
    from . import client

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
