"""Who still uses this Probe install, and stopping every Probe process (clean-uninstall plan U-T2, U-T4).

Scope (owner decision D2 = A): before anything is changed, `probe uninstall`
lists what still uses this install and refuses (exit 2) unless `--force`:

    sessions      agent sessions the Probe service records (`sessions.json`,
                  `recorders.json`), their agent process still running
    daemon        the daemon host (`daemon-host/host.json`) and daemon workers
                  (a held `<state>/daemon/<sid>.lock`)
    runs          training runs holding a run lock (`<state>/runs/*.flock` or a
                  live lease) and `probe exec` holds (`runs.json`)
    machines      another machine's service folder in a shared home that was
                  active in the last OTHER_MACHINE_RECENT_S, or a version
                  folder another machine marked in use as recently

and it refuses from inside a session Probe records (any agent, any profile:
the session it would tear down is the one running it), `--force` excepted.

Stop (phase "stopping", after the keeper and the lifeboat are gone): the
desktop app is asked to quit (macOS), the service is asked to stop and, if it
will not, stopped by its lock holder's identity; then the daemon host, the
capture uploaders, import workers and every other process that runs from this
install's code. A process is ours only by identity -- its (pid, start time)
re-read before every signal, and its command line naming this install's env
or shims (or, on Linux, a Probe module run with this HOME) -- never by name
alone. SIGTERM, a grace, then SIGKILL; what survives is reported. With
`--force` training runs holding a run lock get SIGTERM too (never SIGKILL: the
SDK flushes what it queued on the way out), so the drain that follows sends it.
"""

from __future__ import annotations

import contextlib
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from probe._compat import StrEnum

#: Another machine's service folder active this recently uses this install.
OTHER_MACHINE_RECENT_S = 24 * 3600.0
#: How long a stopped process has between SIGTERM and SIGKILL.
STOP_GRACE_S = 10.0
#: A training run SIGTERMed by `--force` gets this long to flush and exit.
RUN_GRACE_S = 30.0
#: How long the service has to stop on request before it is signalled.
SERVICE_STOP_WAIT_S = 5.0


class UserKind(StrEnum):
    SESSION = "session"
    DAEMON = "daemon"
    RUN = "run"
    MACHINE = "machine"


@dataclass(frozen=True)
class User:
    kind: str
    label: str
    pid: int | None = None
    start: str | None = None

    def as_json(self) -> dict:
        return {"kind": self.kind, "label": self.label, "pid": self.pid}


@dataclass(frozen=True)
class Proc:
    pid: int
    start: str
    argv: tuple = field(default_factory=tuple)

    def label(self) -> str:
        return f"pid {self.pid} ({' '.join(self.argv[:3])[:120]})"


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _alive(pid, start) -> bool:
    from probe.service import procid

    try:
        return procid.alive(int(pid), str(start)) is not False
    except (TypeError, ValueError):
        return False


def _owners(data, key: str = "sessions") -> list[dict]:
    rows = data.get(key) if isinstance(data, dict) else None
    return [r for r in rows or [] if isinstance(r, dict)]


def recorded_sessions() -> list[dict]:
    """`{sid, harness, pid, start}` of every session the service records whose
    agent still runs (from its files: the service may be down)."""
    from probe.service import paths
    from probe.service.recorders import RECORDERS_NAME

    found: dict[str, dict] = {}
    sources = (_read_json(paths.registry_path()), _read_json(paths.service_dir() / RECORDERS_NAME))
    for data in sources:
        for row in _owners(data):
            owner = row.get("owner")
            sid = row.get("sid")
            if not isinstance(owner, dict) or not isinstance(sid, str) or sid in found:
                continue
            if row.get("mode") == "off":
                continue
            if _alive(owner.get("pid"), owner.get("start_time")):
                found[sid] = {"sid": sid, "harness": row.get("harness"), "pid": owner.get("pid"),
                              "start": owner.get("start_time")}
    return list(found.values())


def recorded_session_here() -> str | None:
    """The recorded agent session this process runs inside, or None: its
    session id names one Probe records, or an ancestor of it owns one."""
    from probe.sdk import agent_session, session_marker
    from probe.service import caller

    sessions = recorded_sessions()
    sid = agent_session.session_id_from_env()
    if sid:
        if any(s["sid"] == sid for s in sessions):
            return sid
        with contextlib.suppress(Exception):
            if session_marker.session_profile(sid) is not None or (session_marker.sessions_dir() / f"{sid}.json").exists():
                return sid
    with contextlib.suppress(Exception):
        lineage = set(caller.ancestry(os.getpid()))
        for session in sessions:
            if (session["pid"], session["start"]) in lineage:
                return session["sid"]
    return None


def _daemon_host() -> dict | None:
    from probe.service import paths
    from probe.service.daemonhost import DIRNAME

    data = _read_json(paths.service_dir() / DIRNAME / "host.json")
    if isinstance(data, dict) and _alive(data.get("pid"), data.get("start")):
        return data
    return None


def _state_roots() -> list[Path]:
    from probe.cli import uninstall_plan

    return uninstall_plan.state_roots()


def _workers() -> list[str]:
    from probe.service import updater

    try:
        found = updater.live_workers(_state_roots())
    except Exception:  # noqa: BLE001
        return []
    return [w.sid for w in found or []]


def _run_locks() -> list[dict]:
    """Training runs holding a run lock: {run, pid, at} (pid None for a lease)."""
    from probe._shared import run_lock

    out = []
    for root in _state_roots():
        folder = root / run_lock.RUNS_DIRNAME
        try:
            entries = sorted(folder.iterdir())
        except OSError:
            continue
        now = time.time()
        for entry in entries[: run_lock.MAX_SCAN_ENTRIES]:
            if entry.name.endswith(run_lock.FLOCK_SUFFIX) and run_lock._flock_is_held(entry):  # noqa: SLF001
                data = _read_json(entry) or {}
                out.append({"run": str(data.get("run") or entry.stem), "pid": data.get("pid"), "at": data.get("at")})
            elif entry.name.endswith(run_lock.LEASE_SUFFIX) and run_lock._lease_is_live(entry, now):  # noqa: SLF001
                out.append({"run": entry.name[: -len(run_lock.LEASE_SUFFIX)], "pid": None, "at": None})
    return out


def _exec_holds() -> list[dict]:
    from probe.service import paths
    from probe.service.runholds import RUNS_NAME

    out = []
    for row in _owners(_read_json(paths.service_dir() / RUNS_NAME), "holds"):
        owner = row.get("owner")
        if isinstance(owner, dict) and _alive(owner.get("pid"), owner.get("start_time")):
            out.append({"run": row.get("run"), "pid": owner.get("pid"), "start": owner.get("start_time")})
    return out


def _newest_mtime(folder: Path) -> float:
    newest = 0.0
    with contextlib.suppress(OSError):
        newest = folder.stat().st_mtime
        for child in list(folder.iterdir())[:200]:
            with contextlib.suppress(OSError):
                newest = max(newest, child.lstat().st_mtime)
    return newest


def other_machines(now: float | None = None) -> list[str]:
    """Other machines in this shared home that used Probe recently."""
    from probe._shared import installs
    from probe.cli import uninstall_plan
    from probe.service import paths

    now = time.time() if now is None else now
    found = [d.name for d in uninstall_plan.other_machine_dirs()
             if now - _newest_mtime(d) < OTHER_MACHINE_RECENT_S]
    mine = installs.USED_PREFIX + paths.machine_key()
    for tools in uninstall_plan.tool_dirs():
        with contextlib.suppress(OSError):
            for folder in installs.versions_root(tools).iterdir():
                if not folder.is_dir():
                    continue
                for mark in folder.glob(installs.USED_PREFIX + "*"):
                    key = mark.name[len(installs.USED_PREFIX):]
                    with contextlib.suppress(OSError):
                        if mark.name != mine and key not in found and now - mark.stat().st_mtime < OTHER_MACHINE_RECENT_S:
                            found.append(key)
    return found


def live_users() -> list[User]:
    """Everything that still uses this install (see the module docstring),
    never this process or its parent chain: the desktop app that runs
    `probe uninstall --yes --json` is not a user of what it removes."""
    users = [user for user in _live_users() if user.pid is None or user.pid not in _self_and_ancestors()]
    return users


def _live_users() -> list[User]:
    users: list[User] = []
    for session in recorded_sessions():
        users.append(User(UserKind.SESSION, f"{session.get('harness') or 'agent'} session {session['sid']} "
                                            f"(pid {session['pid']})", session["pid"], session["start"]))
    host = _daemon_host()
    if host is not None:
        users.append(User(UserKind.DAEMON, f"the Probe daemon host (pid {host.get('pid')})",
                          host.get("pid"), host.get("start")))
    for sid in _workers():
        users.append(User(UserKind.DAEMON, f"a Probe daemon worker (session {sid})"))
    for run in _run_locks():
        pid = f" (pid {run['pid']})" if run.get("pid") else ""
        users.append(User(UserKind.RUN, f"training run {run['run']}{pid}", run.get("pid")))
    for hold in _exec_holds():
        users.append(User(UserKind.RUN, f"`probe exec` run {hold['run']} (pid {hold['pid']})",
                          hold["pid"], hold["start"]))
    for key in other_machines():
        users.append(User(UserKind.MACHINE, f"another computer sharing this home folder (Probe machine key {key})"))
    return users


# -- processes ---------------------------------------------------------------------------


def _self_and_ancestors() -> set[int]:
    from probe.service import procid

    seen = {os.getpid()}
    pid = os.getpid()
    for _ in range(64):
        info = procid.proc(pid)
        if info is None or info.ppid <= 1:
            break
        pid = info.ppid
        seen.add(pid)
    return seen


def processes() -> list[tuple[int, list[str], str]] | None:
    """(pid, argv, executable) of every process of this user; None when they
    cannot be listed. The executable is `/proc/<pid>/exe` on Linux and `ps`'s
    `comm` on macOS ("" when unknown)."""
    proc = Path("/proc")
    if proc.is_dir() and Path("/proc/self/cmdline").exists():
        out = []
        uid = os.getuid()
        for entry in proc.iterdir():
            if not entry.name.isdigit():
                continue
            with contextlib.suppress(OSError):
                if entry.stat().st_uid != uid:
                    continue
                raw = (entry / "cmdline").read_bytes()
                if not raw:
                    continue
                exe = ""
                with contextlib.suppress(OSError):
                    exe = os.readlink(entry / "exe")
                out.append((int(entry.name), [a.decode("utf-8", "replace") for a in raw.split(b"\0") if a], exe))
        return out
    if os.name == "nt":
        return None
    listed: dict[int, list] = {}
    for column in ("command", "comm"):
        try:
            done = subprocess.run(["ps", "-axww", "-o", f"pid=,uid=,{column}="], capture_output=True, text=True,
                                  timeout=10, check=False)
        except (OSError, subprocess.SubprocessError):
            return None
        if done.returncode != 0:
            return None
        uid = os.getuid()
        for line in done.stdout.splitlines():
            parts = line.split(None, 2)
            if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit() and int(parts[1]) == uid:
                row = listed.setdefault(int(parts[0]), [[], ""])
                if column == "command":
                    row[0] = parts[2].split()
                else:
                    row[1] = parts[2].strip()
    return [(pid, argv, exe) for pid, (argv, exe) in listed.items() if argv]


def _under(path: str, roots: list[str]) -> bool:
    return any(path == r or path.startswith(r.rstrip("/") + "/") for r in roots)


def ours(argv: list[str], exe: str, roots: list[str]) -> bool:
    """Is this process Probe's: is its EXECUTABLE in this install (`roots`:
    the env generations and the tool path)? Its argv[0] as given (an env's
    `bin/python` is a link to the interpreter it was made from) or resolved,
    or the kernel's own record of it. Never an argument: `less` or `vim` on a
    file inside an env is not Probe's."""
    candidates = set()
    if argv and os.path.isabs(argv[0]):
        candidates.update({os.path.normpath(argv[0]), os.path.realpath(argv[0])})
    if exe and os.path.isabs(exe):
        candidates.update({os.path.normpath(exe), os.path.realpath(exe)})
    spelled = list(roots) + [os.path.realpath(r) for r in roots]
    return any(_under(candidate, spelled) for candidate in candidates)


def find(roots: list[str]) -> list[Proc]:
    """Every process of this install's (see `ours`), never this one or its ancestors."""
    from probe.service import procid

    listed = processes()
    if listed is None:
        return []
    skip = _self_and_ancestors()
    found = []
    for pid, argv, exe in listed:
        if pid in skip or not ours(argv, exe, roots):
            continue
        start = procid.start_time(pid)
        if start:
            found.append(Proc(pid, start, tuple(argv)))
    return found


def _signal(proc: Proc, sig: int) -> bool:
    """Signal `proc` only while it is still that process. True when sent."""
    from probe.service import procid

    if procid.start_time(proc.pid) != proc.start:
        return False
    try:
        os.kill(proc.pid, sig)
    except (ProcessLookupError, PermissionError):
        return False
    return True


def _gone(proc: Proc) -> bool:
    from probe.service import procid

    return procid.alive(proc.pid, proc.start) is False


def stop(procs: list[Proc], *, grace: float = STOP_GRACE_S, kill: bool = True) -> list[Proc]:
    """SIGTERM each, wait up to `grace`, SIGKILL what is left (`kill`). Returns
    the ones still running."""
    for proc in procs:
        _signal(proc, signal.SIGTERM)
    deadline = time.monotonic() + grace
    left = [p for p in procs if not _gone(p)]
    while left and time.monotonic() < deadline:
        time.sleep(0.1)
        left = [p for p in left if not _gone(p)]
    if left and kill and hasattr(signal, "SIGKILL"):
        for proc in left:
            _signal(proc, signal.SIGKILL)
        deadline = time.monotonic() + 2.0
        while left and time.monotonic() < deadline:
            time.sleep(0.05)
            left = [p for p in left if not _gone(p)]
    return left


def run_by_desktop_app() -> bool:
    """Is this `probe uninstall` the desktop app's own (it sets
    PROBE_DESKTOP_HUMAN=1 on every CLI run)? Then the app quits itself once the
    run succeeds, and is never asked to from here."""
    from probe._shared.telemetry import DESKTOP_HUMAN_ENV

    return os.environ.get(DESKTOP_HUMAN_ENV) == "1"


def quit_desktop_app(lines: list[str]) -> None:
    """macOS: ask the desktop app to quit, best effort (it would start the
    service again). Never when the app runs this uninstall itself."""
    if sys.platform != "darwin" or run_by_desktop_app():
        return
    from probe.cli import uninstall_plan

    try:
        running = subprocess.run(["pgrep", "-x", "Probe"], capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.SubprocessError):
        return
    if running.returncode != 0:
        return
    try:
        subprocess.run(["osascript", "-e", f'tell application id "{uninstall_plan.DESKTOP_BUNDLE_ID}" to quit'],
                       capture_output=True, text=True, timeout=15, check=False)
        lines.append("Asked the Probe desktop app to quit.")
    except (OSError, subprocess.SubprocessError):
        lines.append("! could not ask the Probe desktop app to quit; quit it from its menu.")


def stop_service(lines: list[str]) -> bool:
    """Ask the service to stop; if it will not (it refuses while an action or
    an update runs, and this uninstall may BE its action), stop its lock holder.
    True when one was running."""
    from probe import __version__
    from probe.service import client, guard, procid
    from probe.service.protocol import Client, Method

    holder = guard.holder()
    if holder is None and client.connect(0.5) is None:
        return False
    with contextlib.suppress(Exception):
        client.call(Method.STOP, client=Client.CLI, client_version=__version__)
    deadline = time.monotonic() + SERVICE_STOP_WAIT_S
    while holder is not None and time.monotonic() < deadline and procid.alive(*holder) is not False:
        time.sleep(0.1)
    if holder is not None and procid.alive(*holder) is not False:
        left = stop([Proc(holder[0], holder[1], ("probe service",))])
        lines.append("! the Probe service did not stop" if left else "Stopped the Probe service.")
    else:
        lines.append("Stopped the Probe service.")
    return True


def stop_daemon_host(lines: list[str]) -> bool:
    host = _daemon_host()
    if host is None:
        return False
    left = stop([Proc(int(host["pid"]), str(host.get("start") or ""), ("daemon-host",))])
    lines.append("! the Probe daemon host did not stop" if left else "Stopped the Probe daemon host.")
    return True


def tap_watchers() -> list[Proc]:
    """The capture uploaders their pid files (`<prefix>-watcher-<sid>.pid`)
    name, each only while it is still that uploader: its command line runs
    `tap watch` for that session (the tap's own check, `session-start.sh`) and
    it started before the pid file was written (a reused pid did not)."""
    from probe.cli import capture
    from probe.harness import get_registry
    from probe.service import procid

    folder = Path(capture._pid_dir())  # noqa: SLF001 - the tests' override included
    found = []
    for prefix in sorted({harness.capture.watcher_prefix for harness in get_registry().captured()}):
        for pid_file in folder.glob(f"{prefix}-watcher-*.pid"):
            sid = pid_file.name[len(f"{prefix}-watcher-"):-len(".pid")]
            try:
                st = pid_file.stat()
                if hasattr(os, "getuid") and st.st_uid != os.getuid():
                    continue
                pid = int(pid_file.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                continue
            if pid <= 1 or pid in _self_and_ancestors():
                continue
            argv = _argv(pid)
            line = " ".join(argv)
            if "tap watch" not in line or sid not in line:
                continue
            began = _started_at(pid)
            if began is None or began > st.st_mtime + 5.0:
                continue
            start = procid.start_time(pid)
            if start:
                found.append(Proc(pid, start, tuple(argv)))
    return found


def _argv(pid: int) -> list[str]:
    try:
        return [a.decode("utf-8", "replace") for a in Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0") if a]
    except OSError:
        pass
    try:
        out = subprocess.run(["ps", "-ww", "-p", str(pid), "-o", "command="], capture_output=True, text=True,
                             timeout=5, check=False).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return out.split()


def training_processes() -> list[Proc]:
    """`--force`: the processes holding a run lock, each only while its start
    is no later than the lock it holds (the pid not reused since)."""
    from probe.service import procid

    found = []
    for run in _run_locks():
        pid, at = run.get("pid"), run.get("at")
        if not isinstance(pid, int) or pid <= 1 or pid in _self_and_ancestors():
            continue
        if not isinstance(at, (int, float)) or isinstance(at, bool):
            continue
        began = _started_at(pid)
        if began is None or began > at + 2.0:
            continue  # unknown, or a process younger than the lock: not the run that took it
        start = procid.start_time(pid)
        if start:
            found.append(Proc(pid, start, (f"training run {run['run']}",)))
    return found


def _started_at(pid: int) -> float | None:
    """When `pid` started, in epoch seconds; None when it cannot be read."""
    try:
        raw = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8", errors="replace")
        ticks = int(raw[raw.rfind(")") + 2:].split()[19])
        boot = next(int(line.split()[1]) for line in Path("/proc/stat").read_text().splitlines()
                    if line.startswith("btime "))
        return boot + ticks / os.sysconf("SC_CLK_TCK")
    except (OSError, ValueError, IndexError, StopIteration):
        pass
    try:
        out = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)], capture_output=True, text=True, timeout=5,
                             check=False, env={**os.environ, "LC_ALL": "C"}).stdout.strip()
        return time.mktime(time.strptime(out, "%a %b %d %H:%M:%S %Y")) if out else None
    except (OSError, subprocess.SubprocessError, ValueError, OverflowError):
        return None


def sweep_roots(plan: dict) -> list[str]:
    """Where a Probe process of this install has its executable: the env
    generations, the version folders and the tool path."""
    roots = list(plan.get("env_generations", []))
    for item in plan.get("paths", []):
        if item.get("stage") == "finish" and item.get("kind") in ("dir", "link") and not item.get("empty_only"):
            roots.append(item["path"])
    return list(dict.fromkeys(roots))


def stop_everything(plan: dict, *, force: bool, lines: list[str], stopped: list | None = None) -> list[Proc]:
    """Phase "stopping"'s processes (the keeper and lifeboat are gone first,
    by the caller). Nothing here outlasts a call-off: what stops starts again
    (an import job resumes, an uploader with the next session). `stopped` gets
    one phrase per kind of thing stopped, for the line a call-off prints.
    Returns what still runs."""
    stopped = [] if stopped is None else stopped
    quit_desktop_app(lines)
    if stop_service(lines):
        stopped.append("the Probe service")
    if stop_daemon_host(lines):
        stopped.append("the Probe daemon host")
    watchers = tap_watchers()
    if watchers:
        left = stop(watchers)
        lines.append(f"Stopped {len(watchers) - len(left)} capture uploader(s).")
        stopped.append(f"{len(watchers)} capture uploader(s)")
    if force:
        runs = training_processes()
        if runs:
            left = stop(runs, grace=RUN_GRACE_S, kill=False)
            lines.append(f"Asked {len(runs)} training run(s) to stop (--force)"
                         + (f"; {len(left)} still running" if left else "") + ".")
            stopped.append(f"{len(runs)} training run(s), sent SIGTERM by --force")
    roots = sweep_roots(plan)
    found = find(roots)
    left = stop(found) if found else []
    if found:
        lines.append(f"Stopped {len(found) - len(left)} other Probe process(es).")
        stopped.append(f"{len(found)} other Probe process(es), import workers among them")
    survivors = [p for p in find(roots) if not _gone(p)]
    for proc in survivors:
        lines.append(f"! still running: {proc.label()}")
    return survivors
