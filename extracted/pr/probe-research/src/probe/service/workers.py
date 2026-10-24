"""Each recorded session's daemon worker, supervised by the service itself (plan Q3).

    the hand-off   a session's recorder runs here (`recorders.py`); the tap's
                   Supervisor in it (`tap.companion_supervisor`) finds its
                   session's link (`controls.workers`, a `Link`) and calls
                   `supervise(spec)`: what it would have spawned, and how to
                   read the session's switch. From then on the tap only drains
                   the SDK socket, and this module spawns, respawns and stops
                   the worker. One owner, never two: an older tap never calls
                   it (its own Supervisor spawns, as before), a `tap watch`
                   has no link, and the service spawns for no session whose
                   tap did not hand it over
    one supervisor per session, polled every POLL_S on one thread while any
                   session is supervised or a worker drains (no timer when none):
                     the switch wants a worker and none runs:
                       the updater holds worker starts (`barrier`)  -> none yet
                       another live worker holds the session lock   -> none
                         either; its `.handover` ask is kept fresh, so a
                         stopping holder hands over at its next model round
                       else, on a launch thread of that session's own (the
                         interpreter's stat, the log's open and the exec can
                         hang on a dead mount; this thread goes on stopping
                         and reaping the others meanwhile: `starting`),
                         `<the CLI's python> -I -c <probe's entry> daemon
                         worker ...` (runtime.json's interpreter, as
                         `client._spawn` starts the service), its own process
                         group, its output in `<state>/daemon/<sid>.log`, run
                         from that state folder: the worker enters the project
                         (`--cwd`, ENTER_CWD_ENV) itself, so a hung mount there
                         stalls that session alone; at most RESPAWNS_PER_MINUTE
                     it exited -- the tap supervisor's rules, by exit code:
                       0                      again at once
                       EXIT_RESPAWN_LATER     not before RESPAWN_LATER_S
                       EXIT_RETRY_LIBS        not before LIBS_RETRY_S
                       EXIT_DO_NOT_RESPAWN, 2 none until the switch moves
                       anything else          a crash: CRASH_BACKOFF_S,
                                              doubling per crash in a row, at
                                              most CRASH_BACKOFF_CAP_S
    release        the recorder's loop ended (its session ended, or the recorder
                   stopped): SIGTERM -- the worker finishes its queue on its own,
                   bounded, and is reaped meanwhile (`draining`). A service
                   that stops releases nothing: its workers run on, asked to
                   hand over to the next service's (`recorders.close`)
    the updater    stops workers at a safe point by their pids, as before
                   (`updater._stop_workers`); this only never starts one while
                   it holds starts, and starts the new one once it lets go

`service.status` `workers`: one row per session (`WorkerState`).

Stdlib only (plan S1).
"""

from __future__ import annotations

import contextlib
import json
import os
import signal
import subprocess
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from . import barrier, procid
from .protocol import WorkerState
from .watch import Family

RESPAWNS_PER_MINUTE = 5
#: The worker's exits (`probe.daemon.worker`; `tests/test_service_workers.py`
#: keeps them equal to the worker's and the tap supervisor's).
EXIT_DO_NOT_RESPAWN = 3
EXIT_CRASHED = 4
EXIT_RESPAWN_LATER = 5
EXIT_RETRY_LIBS = 6
#: A usage error: the CLI has no `daemon worker` (too old).
EXIT_NO_COMMAND = 2
#: Crashes in a row that are a `worker` report (crash-report plan B2).
REPORT_CRASHES = 3
RESPAWN_LATER_S = 5.0
LIBS_RETRY_S = 300.0
CRASH_BACKOFF_S = 30.0
CRASH_BACKOFF_CAP_S = 30 * 60.0
POLL_S = 2.0
#: A waiting supervisor re-touches the holder's `.handover` ask this often (the
#: worker trusts one younger than 10 s: `worker.HANDOVER_FRESH_S`).
HANDOVER_TOUCH_S = 2.0
#: Test-only overrides (API v1, "Lifecycle"). Nothing in production sets them.
POLL_ENV = "PROBE_SERVICE_WORKER_POLL_S"
BACKOFF_ENV = "PROBE_SERVICE_WORKER_BACKOFF_S"
#: Told to every worker (`probe.daemon.worker.SUPERVISOR_*`): this supervisor
#: follows the switch into inline itself, knows read-only inline, and retries
#: after EXIT_RETRY_LIBS -- as the tap's does.
SUPERVISOR_ENV = {"PROBE_TAP_FOLLOWS_INLINE": "1", "PROBE_TAP_READ_ONLY_INLINE": "1", "PROBE_TAP_RETRIES_LIBS": "1"}
#: `{"pid", "start", "sid"}` of this service (`probe.daemon.worker.SUPERVISOR_PID_ENV`):
#: the worker's supervisor by identity, so one started just before this service
#: exits (an update's restart) sees it gone -- exited, unreaped or its pid reused
#: -- and finishes and leaves; by `getppid()` alone, read after its imports, it
#: would take init for its parent.
SUPERVISOR_PID_ENV = "PROBE_DAEMON_SUPERVISOR"
#: "1" on every worker (`probe.daemon.worker.ENTER_CWD_ENV`): it is started from
#: its state folder, never the project's (a hung mount there would stall the
#: service), so it moves into `--cwd` itself -- with or without the identity.
ENTER_CWD_ENV = "PROBE_DAEMON_ENTER_CWD"
#: A start time this service could not read is read again after this, doubling
#: (a `ps` on macOS can time out once), at most START_RETRY_CAP_S.
START_RETRY_S = 5.0
START_RETRY_CAP_S = 300.0
#: `probe`'s console script, run by the CLI's own interpreter: the command line
#: keeps `daemon worker <sid>` (what the updater looks for), and `probe`'s
#: update barrier comes first, as for the tap's `probe daemon worker`.
ENTRY = "import sys; from probe._entry import main; sys.exit(main())"
MAX_ENV = 400


def _env_float(name: str, default: float) -> float:
    try:
        value = float(os.environ.get(name) or default)
    except ValueError:
        return default
    return value if value > 0 else default


def safe_sid(sid: str) -> str:
    """The session's file stem under `<state>/daemon` (`probe.daemon.store.store_path`)."""
    return "".join(c for c in sid if c.isalnum() or c in "-_") or "session"


def lock_held(path: Path) -> bool:
    """Does a live process hold this session lock (a worker, for its whole
    life)? A shared probe released at once, creating nothing. Unknown reads as
    free: the worker's own wait is bounded (`worker.LOCK_WAIT_S`)."""
    import fcntl

    try:
        handle = open(path, "rb")  # noqa: SIM115 -- closed below
    except OSError:
        return False
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
    except BlockingIOError:
        return True
    except OSError:
        return False
    else:
        with contextlib.suppress(OSError):
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return False
    finally:
        handle.close()


def held_for_update() -> bool:
    """Does the updater hold new worker starts (plan D7), or is its barrier up (X1)?"""
    try:
        return barrier.workers_held() or not barrier.wait(0)
    except Exception:  # noqa: BLE001 -- a broken barrier must not stop every worker
        return False


_own_start: dict = {}
_own_start_lock = threading.Lock()


def supervisor_value(sid: str) -> str:
    """SUPERVISOR_PID_ENV's value for a worker of `sid`: this process's pid,
    always, and its start time once it could be read (else null: the worker
    then tells it by pid and parent). The read (a `ps` on macOS) is made by one
    launch at a time, outside the lock: the others go on without it meanwhile.
    A failed read is tried again after START_RETRY_S, doubling to
    START_RETRY_CAP_S, never cached."""
    pid = os.getpid()
    with _own_start_lock:
        if _own_start.get("pid") != pid:
            _own_start.clear()
            _own_start.update(pid=pid, start=None, next=float("-inf"), wait=START_RETRY_S, reading=False)
        start = _own_start["start"]
        read = start is None and not _own_start["reading"] and time.monotonic() >= _own_start["next"]
        if read:
            _own_start["reading"] = True
    if read:
        got = None
        try:
            got = procid.start_time(pid)
        finally:
            with _own_start_lock:
                _own_start["reading"] = False
                if got:
                    _own_start["start"] = start = got
                else:
                    _own_start["next"] = time.monotonic() + _own_start["wait"]
                    _own_start["wait"] = min(START_RETRY_CAP_S, _own_start["wait"] * 2)
    return json.dumps({"pid": pid, "start": start, "sid": sid})


def cli_python() -> str | None:
    """The CLI's interpreter (runtime.json), as `client.ensure` starts the service with."""
    from . import client

    return client.runtime_python()


@dataclass
class Launch:
    """One start of a session's worker, on a thread of its own (`Supervisor._spawn`).
    A session has at most one under way, across its releases and recordings
    (`WorkerHost.reserve`): a launch hung on a dead mount is not joined by
    another each time the session comes back. `cancelled`: its session was
    released or the service stops -- a child it still yields is asked to stop
    (`late`) and drained, and the session's next launch waits for that one to go."""

    sid: str
    thread: threading.Thread | None = None
    cancelled: bool = False
    late: subprocess.Popen | None = None

    def busy(self) -> bool:
        if self.thread is not None and self.thread.is_alive():
            return True
        return self.late is not None and self.late.poll() is None


@dataclass
class Spec:
    """What a session's tap hands over (`Link.supervise`)."""

    sid: str
    transcript: str
    cwd: str
    source: str
    #: `<state>/probe/daemon`, under the session's own state folder.
    daemon_dir: Path
    #: The environment the tap would have spawned the worker with (the session's).
    env: dict
    #: `() -> (state, wanted)`: the session's switch as the tap reads it, and
    #: whether it wants a worker there. Runs on this module's thread.
    switch: Callable[[], tuple]


def parse_spec(raw: object) -> Spec | None:
    if not isinstance(raw, dict):
        return None
    sid, source, switch, env = raw.get("sid"), raw.get("source"), raw.get("switch"), raw.get("env")
    if not isinstance(sid, str) or not sid or len(sid) > 128 or "/" in sid:
        return None
    if not isinstance(source, str) or not source or len(source) > 64 or not source.replace("_", "").isalnum():
        return None
    for key in ("transcript", "cwd", "daemon_dir"):
        value = raw.get(key)
        if not isinstance(value, str) or not value.startswith("/") or len(value) > 4096 or "\0" in value:
            return None
    if not callable(switch):
        return None
    if not isinstance(env, dict) or len(env) > MAX_ENV or not all(
        isinstance(k, str) and isinstance(v, str) and "\0" not in k + v and "=" not in k for k, v in env.items()
    ):
        return None
    return Spec(sid, raw["transcript"], raw["cwd"], source, Path(raw["daemon_dir"]), dict(env), switch)


@dataclass
class Supervisor:
    """One session's worker: `companion_supervisor.Supervisor`'s rules, in the service."""

    spec: Spec
    owner: object
    log: Callable[[str], None] = lambda message: None
    clock: Callable[[], float] = time.monotonic
    child: subprocess.Popen | None = None
    spawn_times: list = field(default_factory=list)
    spawned: int = 0
    gave_up_in: str | None = None  # the switch state a give-up exit happened in
    crashes: int = 0  # in a row
    not_before: float = float("-inf")  # monotonic: no spawn before this
    last_exit: int | None = None
    state: str = WorkerState.IDLE
    released: bool = False
    #: False once the service stops: nothing more is started.
    may_start: Callable[[], bool] = lambda: True
    #: `(sid, child)`: a worker its launch started after the session was
    #: released, already asked to stop, for the host to reap.
    drain: Callable[[str, subprocess.Popen], None] = lambda sid, child: None
    #: A new Launch for the session, or None while one is still under way (the host's).
    reserve: Callable[[str], Launch | None] = lambda sid: Launch(sid)
    #: The service's watch (`watch.Watch.note`): a give-up or a crash loop is a report.
    incident: Callable[..., None] = lambda *args, **kwargs: None
    _touched: float = float("-inf")
    #: This supervisor's launch (`_spawn` on a thread of its own), or None.
    _launch: Launch | None = None
    #: Between the launch handing over its child and `terminate` taking it.
    _mutex: threading.Lock = field(default_factory=threading.Lock)

    @property
    def lock(self) -> Path:
        return self.spec.daemon_dir / f"{safe_sid(self.spec.sid)}.lock"

    @property
    def handover(self) -> Path:
        return self.spec.daemon_dir / f"{safe_sid(self.spec.sid)}.handover"

    @property
    def log_path(self) -> Path:
        return self.spec.daemon_dir / f"{self.spec.sid}.log"

    def _switch(self) -> tuple:
        try:
            state, wanted = self.spec.switch()
        except Exception:  # noqa: BLE001 -- unknown: nothing new starts; a running worker reads its switch itself
            return None, False
        return (state if isinstance(state, str) else None), bool(wanted)

    def wanted(self) -> bool:
        state, wanted = self._switch()
        if state != self.gave_up_in:
            self.gave_up_in = None
        else:
            return False
        return wanted

    def poll(self) -> None:
        """One look. Raises only on a bug (the host logs it)."""
        now = self.clock()
        launch = self._launch
        if launch is not None:
            if launch.thread is not None and launch.thread.is_alive():
                self.state = WorkerState.STARTING
                return
            self._launch = None
        child = self.child  # once: a release on another thread may clear it
        if child is not None:
            code = child.poll()
            if code is None:
                self.state = WorkerState.RUNNING
                return
            self._exited(code, now)
        if self.released:
            return
        if not self.wanted():
            self.state = WorkerState.GAVE_UP if self.gave_up_in is not None else WorkerState.IDLE
            return
        if now < self.not_before:
            self.state = WorkerState.BACKOFF
            return
        if held_for_update():
            self.state = WorkerState.HELD_FOR_UPDATE
            return
        if lock_held(self.lock):
            # Another live worker of this session: a previous service's or a
            # resumed session's finishing its queue, or one whose exit this
            # supervisor never saw. A second would only wait for it.
            self.state = WorkerState.WAITING_FOR_LOCK
            self._ask_handover(now)
            return
        self.spawn_times = [t for t in self.spawn_times if now - t < 60]
        if len(self.spawn_times) >= RESPAWNS_PER_MINUTE:
            self.state = WorkerState.BACKOFF
            return
        launch = self.reserve(self.spec.sid)
        if launch is None:
            # An earlier launch of this session (before a release, or another
            # recording's) is still under way, or its late child still drains.
            self.state = WorkerState.STARTING
            return
        self.spawn_times.append(now)
        self.state = WorkerState.STARTING
        launch.thread = threading.Thread(target=self._spawn, args=(now, launch),
                                         name=f"worker-launch-{self.spec.sid[:12]}", daemon=True)
        self._launch = launch
        launch.thread.start()

    def _exited(self, code: int, now: float) -> None:
        self.child = None
        self.last_exit = code
        sid = self.spec.sid
        if code in (EXIT_DO_NOT_RESPAWN, EXIT_NO_COMMAND):
            # Respawning cannot help (no key, a newer store, a CLI without the
            # command): none until the switch moves; the agent records.
            self.gave_up_in = self._switch()[0]
            self.log(f"worker: session {sid}'s worker exited {code}: not again until its switch moves")
            self._report(f"gave_up_exit_{code}")
        elif code == EXIT_RESPAWN_LATER:
            self.crashes = 0
            self.not_before = now + RESPAWN_LATER_S
        elif code == EXIT_RETRY_LIBS:
            self.crashes = 0
            self.not_before = now + LIBS_RETRY_S
        elif code == 0:
            self.crashes = 0
        else:
            self.crashes += 1
            first = _env_float(BACKOFF_ENV, CRASH_BACKOFF_S)
            wait = min(CRASH_BACKOFF_CAP_S, first * 2 ** (self.crashes - 1))
            self.not_before = now + wait
            self.log(f"worker: session {sid}'s worker crashed ({code}, {self.crashes} in a row); next try in {wait:.0f} s")
            if self.crashes >= REPORT_CRASHES:
                self._report("crash_loop")

    def _report(self, reason: str) -> None:
        """A `worker` report about this session (crash-report plan B2), with
        the session's own environment for its consent."""
        self.incident(Family.WORKER, reason, self.spec.sid, {
            "last_exit": self.last_exit, "crashes": self.crashes, "spawns": self.spawned,
            "gave_up_in": self.gave_up_in, "source": "supervisor",
        }, env=self.spec.env)

    def _ask_handover(self, now: float) -> None:
        if now - self._touched < HANDOVER_TOUCH_S:
            return
        self._touched = now
        with contextlib.suppress(OSError):
            # One dated ahead (a stopping service's, `recorders.HANDOVER_AHEAD_S`) stays.
            if self.handover.stat().st_mtime > time.time():
                return
        with contextlib.suppress(OSError):
            self.handover.touch()

    def _withdraw_ask(self) -> None:
        """Its session ended while it asked the lock's holder to hand over: the
        ask goes (as a waiting worker's does), or the holder would hand over to
        nobody instead of finishing its queue. One dated ahead is not ours."""
        if self._touched == float("-inf"):
            return
        self._touched = float("-inf")
        with contextlib.suppress(OSError):
            if self.handover.stat().st_mtime <= time.time():
                self.handover.unlink()

    def _argv(self, python: str) -> list[str]:
        s = self.spec
        return [python, "-I", "-c", ENTRY, "daemon", "worker", "--session-id", s.sid, "--transcript", s.transcript,
                "--cwd", s.cwd, "--source", s.source]

    def _spawn(self, now: float, launch: Launch | None = None) -> None:
        """The launch, on its own thread: everything here may block on a dead
        mount (the interpreter's stat, the log, the exec), and blocks this
        session alone."""
        launch = launch if launch is not None else Launch(self.spec.sid)
        sid = self.spec.sid
        python = cli_python()
        if python is None:
            self.gave_up_in = self._switch()[0]
            self.log(f"worker: no CLI interpreter (runtime.json) for session {sid}: the agent records")
            self._report("no_cli")
            return
        env = {**self.spec.env, **SUPERVISOR_ENV, ENTER_CWD_ENV: "1", SUPERVISOR_PID_ENV: supervisor_value(sid)}
        # Started in its own state folder (made for its log just below), never
        # the project's: the worker enters that itself (`--cwd`, ENTER_CWD_ENV).
        cwd = str(self.spec.daemon_dir)
        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            log_fd = os.open(self.log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
        except OSError as exc:
            self.log(f"worker: session {sid}'s log cannot be opened: {exc}")
            self._exited(-1, now)
            return
        if launch.cancelled or not self.may_start() or self.released:
            os.close(log_fd)
            return
        try:
            child = subprocess.Popen(  # noqa: S603 -- the CLI's own interpreter, probe's own entry
                self._argv(python),
                stdin=subprocess.DEVNULL,
                stdout=log_fd,
                stderr=log_fd,
                cwd=cwd,
                env=env,
                # Its own group: a signal to the service's must not cut its final cycle short.
                start_new_session=True,
                close_fds=True,
            )
        except OSError as exc:
            self.log(f"worker: session {sid}'s worker would not start: {exc}")
            self._exited(-1, now)
            return
        finally:
            os.close(log_fd)
        with self._mutex:
            # Released, or the service stopping, while it launched: no one else
            # will stop this child (`terminate` found none; a stopping service
            # stops none), and it may have missed the hand-over ask.
            late = launch.cancelled or self.released or not self.may_start()
            if not late:
                self.child = child
                self.spawned += 1
                self._touched = float("-inf")  # an ask made while it waited is the new worker's to clear
                self.state = WorkerState.RUNNING
        if late:
            launch.late = child
            with contextlib.suppress(ProcessLookupError, PermissionError, OSError):
                child.send_signal(signal.SIGTERM)
            self.drain(sid, child)
            self.log(f"worker: session {sid}'s worker started after its session ended or the service stopped "
                     f"(pid {child.pid}): asked to stop")
            return
        self.log(f"worker: session {sid}'s worker started (pid {child.pid})")

    def terminate(self) -> subprocess.Popen | None:
        """Its session ended: SIGTERM, never a wait (the worker's final cycle is
        bounded by the worker); a launch under way is cancelled. The child,
        still to reap, or None."""
        with self._mutex:
            if self._launch is not None:
                self._launch.cancelled = True
            child, self.child = self.child, None
        self._withdraw_ask()
        if child is None or child.poll() is not None:
            return None
        with contextlib.suppress(ProcessLookupError, PermissionError, OSError):
            child.send_signal(signal.SIGTERM)
        return child

    def public(self, now: float) -> dict:
        child = self.child  # once: the host's thread may clear it meanwhile
        return {
            "sid": self.spec.sid,
            "pid": child.pid if child is not None else None,
            "state": self.state,
            "spawns": self.spawned,
            "crashes": self.crashes,
            "last_exit": self.last_exit,
            "retry_in": round(self.not_before - now, 1) if self.not_before > now else None,
            "gave_up_in": self.gave_up_in,
        }


class Link:
    """A recording's handle on its session's worker (`controls.workers` in the
    tap). Called from the recorder's thread; never raises."""

    def __init__(self, host: WorkerHost, sid: str) -> None:
        self.host = host
        self.sid = sid

    def supervise(self, spec: dict) -> bool:
        """The service takes this session's worker over. False: the tap keeps
        its own (an invalid spec, a platform without the service's)."""
        try:
            return self.host.claim(self, spec)
        except Exception as exc:  # noqa: BLE001 -- the tap supervises, as before
            self.host.log(f"worker: session {self.sid} not taken over: {exc!r}")
            return False

    def release(self) -> None:
        """The recorder's loop ended (not paused): stop the worker."""
        with contextlib.suppress(Exception):
            self.host.release(self)


class WorkerHost:
    def __init__(
        self, *, log: Callable[[str], None], clock: Callable[[], float] = time.monotonic,
        incident: Callable[..., None] = lambda *args, **kwargs: None,
    ) -> None:
        self.log = log
        self.clock = clock
        #: The service's watch (`watch.Watch.note`), handed to each supervisor.
        self.incident = incident
        self._lock = threading.Lock()
        self._sessions: dict[str, Supervisor] = {}
        #: Released, their child still to be asked to stop (on the thread).
        self._ending: list[Supervisor] = []
        #: (sid, child): asked to stop, finishing their queue; reaped here.
        self._draining: list[tuple[str, subprocess.Popen]] = []
        #: sid -> its latest Launch, kept across releases and recordings (`reserve`).
        self._launches: dict[str, Launch] = {}
        self._wake = threading.Event()
        self._thread: threading.Thread | None = None
        self._closed = False

    def link(self, sid: str) -> Link:
        return Link(self, sid)

    def claim(self, link: Link, raw: object) -> bool:
        if os.name != "posix":
            return False
        spec = parse_spec(raw)
        if spec is None or spec.sid != link.sid:
            return False
        with self._lock:
            if self._closed:
                # Stopping: the worker that runs is asked to hand over to the
                # next service's, which starts one if none runs. Nothing here.
                return True
            current = self._sessions.get(spec.sid)
            if current is not None:
                # The same session again (its recorder restarted, a resume):
                # one supervisor, its child and counts kept.
                current.spec, current.owner = spec, link
            else:
                self._sessions[spec.sid] = Supervisor(
                    spec, link, log=self.log, clock=self.clock, may_start=lambda: not self._closed,
                    drain=self._drain, reserve=self.reserve, incident=self.incident,
                )
                self.log(f"worker: session {spec.sid}'s daemon worker is supervised here")
            if self._thread is None:
                self._thread = threading.Thread(target=self._run, name="worker-supervisor", daemon=True)
                self._thread.start()
        self._wake.set()
        return True

    def release(self, link: Link) -> None:
        with self._lock:
            current = self._sessions.get(link.sid)
            if current is None or current.owner is not link:
                return  # a newer recorder of the session holds it now
            current.released = True
            if current._launch is not None:
                current._launch.cancelled = True
            del self._sessions[link.sid]
            self._ending.append(current)
        self._wake.set()

    def reserve(self, sid: str) -> Launch | None:
        """A new Launch for `sid`, or None while its last one is busy (still
        running, or its late child not yet gone) or the service stops."""
        with self._lock:
            current = self._launches.get(sid)
            if self._closed or (current is not None and current.busy()):
                return None
            launch = self._launches[sid] = Launch(sid)
            return launch

    def supervised(self, sid: object) -> bool:
        with self._lock:
            return isinstance(sid, str) and sid in self._sessions

    def _drain(self, sid: str, child: subprocess.Popen) -> None:
        with self._lock:
            self._draining.append((sid, child))
        self._wake.set()

    def _stop_ending(self, ending: list[Supervisor]) -> None:
        for sup in ending:
            child = sup.terminate()
            if child is not None:
                self.log(f"worker: session {sup.spec.sid} ended: its worker (pid {child.pid}) finishes its queue")
                with self._lock:
                    self._draining.append((sup.spec.sid, child))

    def _run(self) -> None:
        """The host's thread. Once the service stops it polls no session (and
        starts nothing) but still stops the workers of sessions that end, and
        reaps; it dies with the process."""
        poll_s = _env_float(POLL_ENV, POLL_S)
        while True:
            self._wake.clear()
            with self._lock:
                sessions = [] if self._closed else list(self._sessions.values())
                ending, self._ending = self._ending, []
            idle = False
            try:
                for sup in sessions:
                    try:
                        sup.poll()
                    except Exception as exc:  # noqa: BLE001 -- one session's bug never stops another's
                        self.log(f"worker: session {sup.spec.sid}: supervisor poll failed: {exc!r}")
                # Released while this pass ran: a worker it started meanwhile is stopped too.
                self._stop_ending(ending + [sup for sup in sessions if sup.released])
                with self._lock:
                    self._draining = [(sid, child) for sid, child in self._draining if child.poll() is None]
                    # Done launches of sessions no longer here hold nothing back.
                    self._launches = {sid: launch for sid, launch in self._launches.items()
                                      if sid in self._sessions or launch.busy()}
                    idle = not self._sessions and not self._draining and not self._ending
            except Exception as exc:  # noqa: BLE001 -- the thread must outlive a bug: every session rides it
                self.log(f"worker: supervisor pass failed: {exc!r}")
            self._wake.wait(None if idle else poll_s)

    def close(self) -> None:
        """The service stops: no new starts. Running workers are left to hand
        over to the next service's (`recorders.close` asks them); a session
        that ends meanwhile still has its worker asked to stop (the thread
        goes on doing that). Idempotent."""
        with self._lock:
            self._closed = True
            ending, self._ending = self._ending, []
            for launch in self._launches.values():
                launch.cancelled = True
        self._stop_ending(ending)
        self._wake.set()

    def public(self) -> list:
        now = self.clock()
        with self._lock:
            sessions = list(self._sessions.values())
            draining = list(self._draining)
        rows = [sup.public(now) for sup in sessions]
        rows += [{"sid": sid, "pid": child.pid, "state": WorkerState.DRAINING} for sid, child in draining]
        return rows
