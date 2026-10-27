"""The daemon host the Probe service starts: every session's daemon worker in ONE
child process (plan `~/plans/daemon-in-service/PLAN.md`, S1-S6, H11-H14).

    WorkerHost's Supervisor --start(spec)--> DaemonHost --host.sock--> `probe.daemon.host`
      a HostedRun (poll / pid / send_signal: what the Supervisor used of a Popen)
    the same policy, backoff and status rows as a worker process; only the child differs

    spawn      lazily, on the first run: `<CLI python> -I -c <host entry> daemon-host`,
               its own process group, output in `<service>/daemon-host/host.log`
    health     beats every 5 s: none for HUNG_S with runs going -> SIGKILL (a host
               whose control thread cannot run holds every run's lock)
    memory     over HOST_RSS_BUDGET (400 MB + 100 MB a run) -> replaced, at most every
               REPLACE_GAP_S
    replace    (memory, a CLI reinstalled under it): the next run starts in a new host;
               every LIVE run of the old one is asked to hand over (its `.handover`
               dated ahead, then `retire`: each yields at its next model round, and its
               Supervisor starts it again, in the new host); a draining run finishes
               where it is. The old host leaves when its last run ends
    death      the run whose thread was current in the crash (`host-crash-<pid>.log`,
               `host-threads-<pid>.json`, each host's own) exits EXIT_CRASHED (its Supervisor backs off); every
               other run exits 0 (started again at once, its conversation resumed from
               disk); a draining run starts again in the new host with the deadline it
               had. A death nobody can be blamed for twice in UNATTRIBUTED_WINDOW_S:
               every run then counts a crash
    off        `PROBE_DAEMON_HOST=off` in the service's environment, or an `off`
               file in `<service>/daemon-host/`: a worker process per session, as before

Stdlib only (plan S1): the host itself imports the daemon; this never does.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import select
import signal
import socket
import struct
import subprocess
import threading
import time
import uuid
from collections.abc import Callable
from pathlib import Path

from . import paths, procid

DIRNAME = "daemon-host"
KILL_ENV = "PROBE_DAEMON_HOST"
OFF_FILE = "off"
#: `probe.daemon.host.ENTRY` and `ARGV_MARK` (tests keep them equal).
HOST_ENTRY = "import sys; from probe.daemon.host import main; sys.exit(main())"
ARGV_MARK = "daemon-host"
#: `probe.daemon.worker.EXIT_CRASHED` / `FINISH_CAP_S` (tests keep them equal).
EXIT_CRASHED = 4
FINISH_CAP_S = 35 * 60.0
#: `recorders.HANDOVER_AHEAD_S`: a replaced host's live runs see their ask fresh this long.
HANDOVER_AHEAD_S = 180.0
START_TIMEOUT_S = 20.0
ACK_TIMEOUT_S = 10.0
#: A message to the host waits this long for room in its socket; a host that
#: stopped reading longer is killed (`poll`).
SEND_TIMEOUT_S = 10.0
#: The longest one blocking send() may take before it returns what it sent (whole seconds).
SEND_SLICE_S = 1
HUNG_S = 60.0
#: `host.MAX_LINE`: the longest message the host reads (a test keeps them equal).
MAX_LINE = 4 * 1024 * 1024
RSS_CHECK_S = 30.0
RSS_BASE_MB = 400
RSS_PER_RUN_MB = 100
RSS_ENV = "PROBE_DAEMON_HOST_RSS_MB"
REPLACE_GAP_S = 30 * 60.0
UNATTRIBUTED_WINDOW_S = 600.0
#: How often the service looks at its hosts (`DaemonHost._watch`).
WATCH_S = 2.0
#: A replaced or orphaned host still running this long after it was retired is killed.
RETIRED_CAP_S = FINISH_CAP_S + 120.0
MAX_SOCKET_PATH = paths.MAX_SOCKET_PATH
_CURRENT_THREAD = re.compile(rb"Current thread (0x[0-9a-fA-F]+)")


class HostUnavailable(RuntimeError):
    """No host could be started or reached: the session gets a worker process."""


def folder() -> Path:
    return paths.service_dir() / DIRNAME


def socket_path() -> Path:
    """`<service>/daemon-host/host.sock`, or `/tmp/probe-<uid>/daemon-host-<hash>.sock`
    when that is too long for a UNIX socket (as `paths._socket_in`)."""
    path = folder() / "host.sock"
    if len(os.fsencode(str(path))) <= MAX_SOCKET_PATH:
        return path
    digest = hashlib.sha256(os.fsencode(str(folder()))).hexdigest()[:16]
    return Path("/tmp") / f"probe-{os.getuid()}" / f"daemon-host-{digest}.sock"


def enabled() -> bool:
    if os.name != "posix":
        return False  # Windows keeps a worker process per session (R3 parked)
    if (os.environ.get(KILL_ENV) or "").strip().lower() in ("off", "0", "false", "no"):
        return False
    try:
        return not (folder() / OFF_FILE).exists()
    except OSError:
        return True


def _rss_mb(pid: int) -> float | None:
    try:
        for line in Path(f"/proc/{pid}/status").read_text(encoding="utf-8").splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) / 1024.0
    except (OSError, ValueError, IndexError):
        pass
    try:
        out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True, timeout=5,
                             check=False).stdout.strip()
        return int(out) / 1024.0 if out else None
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def _rss_budget(runs: int) -> float:
    try:
        override = float(os.environ.get(RSS_ENV) or 0)
    except ValueError:
        override = 0.0
    return override if override > 0 else float(RSS_BASE_MB + RSS_PER_RUN_MB * max(1, runs))


class HostedRun:
    """A session's worker run in the host, as its Supervisor sees it: `poll()`,
    `pid` and `send_signal()`, what it used of a `subprocess.Popen`."""

    def __init__(self, proc: _Proc, run_id: str, spec: dict) -> None:
        self._proc = proc
        self.run_id = run_id
        self.spec = spec
        self.sid: str = spec["sid"]
        self._pid = proc.pid
        self._returncode: int | None = None
        self.started = threading.Event()
        #: SIGTERMed (its session ended): finishing its queue, until about this.
        self.draining = bool(spec.get("draining"))
        self.finish_by: float | None = spec.get("finish_by")
        #: Started again in another host (a draining run whose host died): that one answers.
        self._moved: HostedRun | None = None
        #: The host's word with its exit ("stale", "retiring", "invalid"), if any.
        self.reason: str | None = None

    @property
    def pid(self) -> int:
        """The host's pid (of the host it moved to: `WorkerHost.pids`, #3361)."""
        return self._moved.pid if self._moved is not None else self._pid

    @property
    def returncode(self) -> int | None:
        return self._moved.returncode if self._moved is not None else self._returncode

    def poll(self) -> int | None:
        return self.returncode

    def send_signal(self, sig: int) -> None:
        if self._moved is not None:
            self._moved.send_signal(sig)
            return
        if sig == signal.SIGTERM and not self.draining:
            self.draining = True
            self.finish_by = time.time() + FINISH_CAP_S
        self._proc.send({"op": "stop", "run": self.run_id})

    def request_stop(self) -> None:
        """Stop for a hand-over (an update): not a session's end, so never
        `draining` (a host dying meanwhile does not move it as a queue to finish)."""
        if self._moved is not None:
            self._moved.request_stop()
            return
        self._proc.send({"op": "stop", "run": self.run_id})

    def _exit(self, code: int) -> None:
        if self._returncode is None:
            self._returncode = int(code)
        self.started.set()


class _Proc:
    """One host process and the service's connection to it."""

    def __init__(self, popen: subprocess.Popen, sock: socket.socket) -> None:
        self.popen = popen
        self.pid = popen.pid
        self.sock = sock
        self.lock = threading.Lock()
        #: One writer at a time on the socket (never `lock`: a status read must not
        #: wait behind a send to a host that stopped reading).
        self.send_lock = threading.Lock()
        self.runs: dict[str, HostedRun] = {}
        self.last_beat = time.monotonic()
        self.beat: dict = {}
        self.retired_at: float | None = None
        self.rss_mb: float | None = None
        self.rss_at = 0.0
        self.dead = False
        #: A send found it not reading for SEND_TIMEOUT_S: killed at the next look (`poll`).
        self.stuck = False
        #: Killed for silence (HUNG_S or stuck): once, whichever thread looked.
        self.killed_hung = False
        #: Killed by its reader because it closed the service's connection while it ran:
        #: the service's own kill, never a crash of every run.
        self.killed_by_service = False
        self.started_at = time.monotonic()
        # MSG_DONTWAIT alone does not bound a send everywhere: macOS's send()
        # ignores it, and a send to a host that stopped reading blocked for good
        # (agent-ci service-macos). A send timeout bounds each blocking send at
        # SEND_SLICE_S and leaves the reader's recv on the same socket blocking.
        with contextlib.suppress(OSError, AttributeError):
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, struct.pack("ll", SEND_SLICE_S, 0))

    def send(self, obj: dict) -> bool:
        """`obj` to the host, within SEND_TIMEOUT_S (plus at most one SEND_SLICE_S):
        a host that stopped reading is killed, never waited for (the reader's recv
        shares the socket, so only a SEND timeout is set on it)."""
        data = memoryview((json.dumps(obj, separators=(",", ":")) + "\n").encode())
        deadline = time.monotonic() + SEND_TIMEOUT_S
        with self.send_lock:
            while data:
                if self.dead or self.stuck:
                    return False
                try:
                    sent = self.sock.send(data, socket.MSG_DONTWAIT)
                except (BlockingIOError, InterruptedError):
                    sent = 0
                except OSError:
                    return False
                data = data[sent:]
                if data:
                    left = deadline - time.monotonic()
                    if left <= 0:
                        self.stuck = True
                        return False
                    waiter = select.poll()
                    waiter.register(self.sock, select.POLLOUT)
                    waiter.poll(min(left, 1.0) * 1000)
        return True

    def live_runs(self) -> list[HostedRun]:
        with self.lock:
            return [r for r in self.runs.values() if r._returncode is None and r._moved is None]

    def runs_seen(self) -> int:
        """Every run this host carries: the service's own and those an old tap
        started through the proxy (only the host's beat lists them)."""
        return max(len(self.live_runs()), len((self.beat or {}).get("runs") or []))

    def beat_sids(self) -> set:
        return {r.get("sid") for r in ((self.beat or {}).get("runs") or []) if isinstance(r, dict)}


class DaemonHost:
    def __init__(self, *, log: Callable[[str], None], incident: Callable[..., None] = lambda *a, **k: None,
                 python: Callable[[], str | None] | None = None) -> None:
        self.log = log
        self.incident = incident
        self._python = python
        self._lock = threading.RLock()
        self._current: _Proc | None = None
        #: Set while a caller starts a host (`_ensure`): the others wait for it.
        self._starting: threading.Event | None = None
        self._retired: list[_Proc] = []
        self._unattributed: list[float] = []
        self._replaced_at = float("-inf")
        #: The service stops (`close`): no host starts from here on.
        self._closed = False
        self._watchdog: threading.Thread | None = None
        self._replace_reason: str | None = None

    # -- the process ---------------------------------------------------------------
    def available(self) -> bool:
        return enabled()

    def close(self) -> None:
        """The service stops: no host starts, no run moves (one would outlive
        the service unowned). Its hosts' runs hand over to the next one's."""
        with self._lock:
            self._closed = True

    def _watch(self) -> None:
        """`poll` every WATCH_S while this service has a host: the watchdog runs
        whether or not any session is supervised here (an old tap's runs)."""
        while True:
            time.sleep(WATCH_S)
            with self._lock:
                if self._current is None and not self._retired and self._starting is None:
                    self._watchdog = None
                    return
            try:
                self.poll()
            except Exception as exc:  # noqa: BLE001 -- the watchdog outlives a bug
                self.log(f"daemon host: watchdog pass failed: {exc!r}")

    def _python_path(self) -> str | None:
        if self._python is not None:
            return self._python()
        from . import client

        return client.runtime_python()

    def _ensure(self) -> _Proc:
        """The current host, started if need be. The start (up to START_TIMEOUT_S)
        runs OUTSIDE the lock, one at a time: `public` (every `service.status`, on
        the service's loop) never waits for a host to start."""
        while True:
            with self._lock:
                if self._closed:
                    raise HostUnavailable("the service is stopping")
                proc = self._current
                if proc is not None and not proc.dead and proc.popen.poll() is None and proc.retired_at is None:
                    return proc
                starting = self._starting
                if starting is None:
                    starting = self._starting = threading.Event()
                    break
            if not starting.wait(START_TIMEOUT_S + ACK_TIMEOUT_S):
                raise HostUnavailable("another start of the host did not finish")
            # Started by the other caller (the next pass returns it), or it failed (this one tries).
        try:
            proc = self._spawn()
            with self._lock:
                self._current = proc
            return proc
        finally:
            with self._lock:
                self._starting = None
            starting.set()

    def _spawn(self) -> _Proc:
        python = self._python_path()
        if python is None:
            raise HostUnavailable("no CLI interpreter (runtime.json)")
        where = folder()
        sock_path = socket_path()
        try:
            where.mkdir(parents=True, exist_ok=True)
            os.chmod(where, 0o700)
            if sock_path.parent != where:
                paths.private_dir(sock_path.parent)  # the /tmp fallback: ours, 0700, not a symlink
            log_fd = os.open(where / "host.log", os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0),
                             0o600)
        except OSError as exc:
            raise HostUnavailable(f"its folder: {exc}") from exc
        from . import client

        try:
            popen = subprocess.Popen(  # noqa: S603 -- the CLI's own interpreter, probe's own module
                [python, "-I", "-c", HOST_ENTRY, ARGV_MARK, "--folder", str(where), "--socket", str(sock_path)],
                stdin=subprocess.DEVNULL, stdout=log_fd, stderr=log_fd, cwd=str(where), env=client._clean_env(),
                start_new_session=True, close_fds=True)
        except OSError as exc:
            raise HostUnavailable(f"would not start: {exc}") from exc
        finally:
            os.close(log_fd)
        deadline = time.monotonic() + START_TIMEOUT_S
        sock = None
        while time.monotonic() < deadline:
            if popen.poll() is not None:
                raise HostUnavailable(f"exited {popen.returncode} at start (see {where / 'host.log'})")
            sock = self._connect(sock_path, popen.pid)
            if sock is not None:
                break
            time.sleep(0.1)
        if sock is None:
            with contextlib.suppress(OSError):
                popen.kill()
            raise HostUnavailable(f"did not answer within {START_TIMEOUT_S:.0f} s")
        proc = _Proc(popen, sock)
        threading.Thread(target=self._read, args=(proc,), name=f"daemon-host-{popen.pid}", daemon=True).start()
        with self._lock:
            if self._watchdog is None:
                self._watchdog = threading.Thread(target=self._watch, name="daemon-host-watchdog", daemon=True)
                self._watchdog.start()
        self.log(f"daemon host: started (pid {popen.pid})")
        return proc

    @staticmethod
    def _connect(path: Path, pid: int) -> socket.socket | None:
        """A connection to the host `pid` (never an older host still bound there)."""
        try:
            paths.require_private(path.parent)  # never trust a listener in a folder another user made
        except OSError:
            return None
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(ACK_TIMEOUT_S)
        try:
            sock.connect(str(path))
            sock.sendall(b'{"op":"hello","role":"service"}\n')
            buf = b""
            while b"\n" not in buf:
                chunk = sock.recv(65536)
                if not chunk:
                    raise OSError("closed")
                buf += chunk
            hello = json.loads(buf.split(b"\n", 1)[0])
            if not isinstance(hello, dict) or hello.get("op") != "hello" or hello.get("pid") != pid:
                raise OSError("another host")
        except (OSError, ValueError):
            with contextlib.suppress(OSError):
                sock.close()
            return None
        sock.settimeout(None)
        return sock

    def _read(self, proc: _Proc) -> None:
        """The host's messages, until it closes; then its runs' exits. Never
        ends early on a bad message, and a closed connection always means a
        dead host: one still running then is killed first (its runs would else
        run twice, its tools be ended under them)."""
        buf = b""
        try:
            while True:
                try:
                    chunk = proc.sock.recv(65536)
                except OSError:
                    chunk = b""
                if not chunk:
                    break
                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    try:
                        msg = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(msg, dict):
                        try:
                            self._on_message(proc, msg)
                        except Exception as exc:  # noqa: BLE001 -- the reader outlives a bug: every run rides it
                            self.log(f"daemon host {proc.pid}: a message failed: {exc!r}")
        finally:
            with contextlib.suppress(subprocess.TimeoutExpired):
                proc.popen.wait(timeout=10)
            if proc.popen.poll() is None:
                proc.killed_by_service = True
                self._kill(proc)
                with contextlib.suppress(subprocess.TimeoutExpired):
                    proc.popen.wait(timeout=5)
            self._died(proc)

    def _check_memory(self, proc: _Proc) -> None:
        proc.rss_mb = _rss_mb(proc.pid)
        runs = proc.runs_seen()
        if proc.rss_mb is not None and proc is self._current and runs and proc.rss_mb > _rss_budget(runs):
            if time.monotonic() - self._replaced_at >= REPLACE_GAP_S:
                self._replaced_at = time.monotonic()
                self.replace(f"its memory ({proc.rss_mb:.0f} MB) passed {_rss_budget(runs):.0f} MB", proc=proc)

    def _later(self, fn, *args, **kwargs) -> None:
        """`fn` off the reader's thread (it touches every run's files and sends)."""
        threading.Thread(target=fn, args=args, kwargs=kwargs, name="daemon-host-later", daemon=True).start()

    def _on_message(self, proc: _Proc, msg: dict) -> None:
        op = msg.get("op")
        with proc.lock:
            run = proc.runs.get(msg.get("run")) if isinstance(msg.get("run"), str) else None
        if op == "started" and run is not None:
            run.started.set()
        elif op == "exited" and run is not None:
            code = msg.get("code")
            run.reason = msg.get("reason") if isinstance(msg.get("reason"), str) else None
            run._exit(code if isinstance(code, int) else EXIT_CRASHED)
            with proc.lock:
                proc.runs.pop(run.run_id, None)  # its Supervisor keeps the HostedRun
                rows = (proc.beat or {}).get("runs") or []
                proc.beat = {**(proc.beat or {}), "runs": [r for r in rows if r.get("run") != run.run_id]}
            if run.reason == "stale":
                # Its CLI was reinstalled under it: the next run starts in a new host.
                self._later(self.replace, "the CLI was reinstalled under the daemon host", proc=proc)
            elif run.reason == "retiring":
                # It takes no new run (signalled, or retired by an earlier service):
                # a new host takes the next one.
                self._later(self.replace, "it takes no new run", proc=proc)
        elif op == "beat":
            proc.last_beat = time.monotonic()
            proc.beat = msg
            if msg.get("retiring") and proc is self._current:
                self._later(self.replace, "it takes no new run", proc=proc)
            if time.monotonic() - proc.rss_at >= RSS_CHECK_S:
                proc.rss_at = time.monotonic()
                self._later(self._check_memory, proc)  # `ps` on macOS: never on the reader's thread

    def _died(self, proc: _Proc) -> None:
        """The host exited (or its connection broke): every run still going ends."""
        with proc.lock:
            if proc.dead:
                return
            proc.dead = True
            runs = [r for r in proc.runs.values() if r._returncode is None and r._moved is None]
        with contextlib.suppress(OSError):
            proc.sock.close()
        with self._lock:
            if self._current is proc:
                self._current = None
            if proc in self._retired:
                self._retired.remove(proc)
        code = proc.popen.poll()
        self._end_children(proc)
        crashed = self._attribute(proc)
        if not runs:
            if code not in (0, None) and proc.retired_at is None:
                self.log(f"daemon host {proc.pid} exited {code} with no run")
            self._forget_files(proc)
            return
        now = time.time()
        # An unexplained death counts toward every run's backoff (a silent host too: a run
        # that hangs its host again and again must back off; nobody can tell which). Not
        # the service's own kill of a host that closed its connection.
        if crashed is None and code not in (0, None) and proc.retired_at is None and not proc.killed_by_service:
            with self._lock:
                self._unattributed = [t for t in self._unattributed if now - t < UNATTRIBUTED_WINDOW_S] + [now]
                unattributed = len(self._unattributed)
        else:
            unattributed = 0
        blame_all = crashed is None and unattributed >= 2
        self.log(f"daemon host {proc.pid} exited {code}: {len(runs)} runs ended"
                 + (f"; the crash was in session {crashed}'s run" if crashed else ""))
        env = next((r.spec.get("env") for r in runs if crashed is not None and r.sid == crashed), None)
        self.incident("worker", "host_exited", crashed, {"exit": code, "runs": len(runs), "attributed": bool(crashed)},
                      **({"env": env} if env is not None else {}))
        moving = []
        for run in runs:
            if crashed is not None and run.sid == crashed:
                run._exit(EXIT_CRASHED)
            elif run.draining and (run.finish_by or 0) > now:
                moving.append(run)
            else:
                run._exit(EXIT_CRASHED if blame_all else 0)
        for run in moving:  # after the others: a new host's start must not hold their restarts
            self._move_draining(run)
        self._forget_files(proc)

    def _forget_files(self, proc: _Proc) -> None:
        """A dead host's own files, once read (its runs ended, its tools ended)."""
        for name in (f"host-crash-{proc.pid}.log", f"host-threads-{proc.pid}.json", f"host-children-{proc.pid}.json",
                     f"host-runs-{proc.pid}.json"):
            with contextlib.suppress(OSError):
                (folder() / name).unlink()

    def _end_children(self, proc: _Proc) -> None:
        """The tools the dead host's runs had started (each its own process group,
        `host-children-<pid>.json`) are ended before any run starts again (plan H15): a
        write still going must not overlap its own retry. TERM, then KILL."""
        try:
            data = json.loads((folder() / f"host-children-{proc.pid}.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        if not isinstance(data, dict) or data.get("pid") != proc.pid:
            return
        alive = []
        for raw, info in (data.get("children") or {}).items():
            try:
                pid = int(raw)
            except ValueError:
                continue
            start = info.get("start") if isinstance(info, dict) else None
            if pid > 1 and start and procid.alive(pid, start):
                alive.append(pid)
        for pid in alive:
            with contextlib.suppress(OSError):
                os.killpg(pid, signal.SIGTERM)
        deadline = time.monotonic() + 5.0
        while alive and time.monotonic() < deadline:
            time.sleep(0.2)
            alive = [pid for pid in alive if _group_alive(pid)]
        for pid in alive:
            with contextlib.suppress(OSError):
                os.killpg(pid, signal.SIGKILL)
        if alive or data.get("children"):
            self.log(f"daemon host {proc.pid}: ended its runs' tools ({len(data.get('children') or {})} recorded)")

    def _attribute(self, proc: _Proc) -> str | None:
        """The session whose run's thread was current in this host's crash, if any."""
        where = folder()
        try:
            with open(where / f"host-crash-{proc.pid}.log", "rb") as handle:
                text = handle.read(1024 * 1024)
        except OSError:
            return None
        found = _CURRENT_THREAD.findall(text)
        if not found:
            return None
        try:
            data = json.loads((where / f"host-threads-{proc.pid}.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        if not isinstance(data, dict) or data.get("pid") != proc.pid:
            return None
        threads = {int(k, 16): v for k, v in (data.get("threads") or {}).items() if isinstance(v, str)}
        return threads.get(int(found[-1], 16))

    def _move_draining(self, run: HostedRun) -> None:
        """A draining run whose host died: started again in a new host, to finish
        the queue by the deadline it had (O2)."""
        try:
            new = self.start(run.spec, draining=True, finish_by=run.finish_by)
        except HostUnavailable as exc:
            self.log(f"daemon host: session {run.sid}'s queue could not move ({exc}); the next worker finishes it")
            run._exit(0)
            return
        run._moved = new

    # -- runs ------------------------------------------------------------------------
    def start(self, spec: dict, *, draining: bool = False, finish_by: float | None = None) -> HostedRun:
        """Start one run: `spec` = {sid, transcript, cwd, source, daemon_dir, env}."""
        message = {"op": "start", "sid": spec["sid"], "transcript": spec["transcript"], "cwd": spec["cwd"],
                   "source": spec["source"], "daemon_dir": str(spec["daemon_dir"]), "env": spec["env"],
                   "draining": draining, "finish_by": finish_by}
        if len(json.dumps(message, separators=(",", ":"))) + 100 > MAX_LINE:
            raise HostUnavailable("its start is too big for the host's line")  # this session's worker runs as a process
        proc = self._ensure()
        run_id = uuid.uuid4().hex
        spec = {**spec, "draining": draining, "finish_by": finish_by}
        run = HostedRun(proc, run_id, spec)
        with proc.lock:
            proc.runs[run_id] = run
        if not proc.send({**message, "run": run_id}):
            with proc.lock:
                proc.runs.pop(run_id, None)
            raise HostUnavailable("its connection is gone")
        if not run.started.wait(ACK_TIMEOUT_S):
            # This start's fallback, never the host's kill: a host that is truly
            # hung stops beating and `poll` kills it (HUNG_S).
            with proc.lock:
                proc.runs.pop(run_id, None)
            proc.send({"op": "stop", "run": run_id})
            self.log(f"daemon host {proc.pid}: no answer to a start in {ACK_TIMEOUT_S:.0f} s; "
                     f"session {spec['sid']}'s worker runs as a process")
            raise HostUnavailable(f"no answer to a start in {ACK_TIMEOUT_S:.0f} s")
        if run.reason == "invalid":
            raise HostUnavailable("the host refused the start")  # a process worker says what is wrong
        return run

    def _kill(self, proc: _Proc) -> None:
        with contextlib.suppress(OSError):
            os.killpg(proc.pid, signal.SIGKILL)
        with contextlib.suppress(OSError):
            proc.popen.kill()

    def replace(self, reason: str, *, proc: _Proc | None = None) -> None:
        """The next run starts in a new host; the current one's live runs hand over
        to it (H14), its draining runs finish where they are. With `proc`: only if
        that one is still the current host."""
        with self._lock:
            current = self._current
            if current is None or current.retired_at is not None or (proc is not None and proc is not current):
                return
            proc = current
            proc.retired_at = time.monotonic()
            self._current = None
            self._retired.append(proc)
            self._replaced_at = time.monotonic()
            self._replace_reason = reason
        self.log(f"daemon host {proc.pid}: replaced ({reason}); its runs hand over to the next host")
        ahead = time.time() + HANDOVER_AHEAD_S
        for run in proc.live_runs():
            if run.draining:
                continue
            marker = Path(run.spec["daemon_dir"]) / f"{_safe_sid(run.sid)}.handover"
            with contextlib.suppress(OSError):
                marker.parent.mkdir(parents=True, exist_ok=True)
                marker.touch()
                os.utime(marker, (ahead, ahead))
        proc.send({"op": "retire", "handover_until": ahead})

    def poll(self) -> None:
        """One look (the WorkerHost's thread, every pass): a hung host is killed, a
        retired one that outlived its cap too."""
        now = time.monotonic()
        with self._lock:
            procs = ([self._current] if self._current is not None else []) + list(self._retired)
        for proc in procs:
            if proc.dead:
                continue
            if proc.popen.poll() is not None:
                continue  # its reader thread sees the close and ends its runs
            if proc.stuck or (proc.runs_seen() and now - proc.last_beat > HUNG_S):
                with proc.lock:
                    if proc.killed_hung:
                        continue  # the other look already killed it
                    proc.killed_hung = True
                why = (f"not reading its messages for {SEND_TIMEOUT_S:.0f} s" if proc.stuck
                       else f"no beat for {now - proc.last_beat:.0f} s")
                self.log(f"daemon host {proc.pid}: {why}; killing it")
                self.incident("worker", "host_hung", None, {"silent_s": round(now - proc.last_beat)})
                self._kill(proc)
            elif proc.retired_at is not None and now - proc.retired_at > RETIRED_CAP_S:
                self.log(f"daemon host {proc.pid}: still running {RETIRED_CAP_S:.0f} s after it was replaced; killing it")
                self._kill(proc)

    def session_draining(self, sid: str) -> bool | None:
        """`sid`'s runs in this service's hosts, from their last beats: True when
        every one is finishing (stopping), False when one is live, None when none
        is there."""
        with self._lock:
            procs = ([self._current] if self._current is not None else []) + list(self._retired)
        rows = [r for p in procs if not p.dead for r in ((p.beat or {}).get("runs") or [])
                if isinstance(r, dict) and r.get("sid") == sid]
        return all(bool(r.get("draining")) for r in rows) if rows else None

    def stop_session(self, sid: str) -> bool:
        """Ask every host of this service to stop `sid`'s runs (one an old tap
        started through the proxy has no Supervisor here). True when asked."""
        with self._lock:
            procs = ([self._current] if self._current is not None else []) + list(self._retired)
        listed = False
        for proc in procs:
            if not proc.dead and proc.send({"op": "stop", "sid": sid}):  # a run started since the last beat too
                listed = listed or sid in proc.beat_sids()
        return listed

    def runs(self) -> int:
        """Runs still going in this service's hosts (the service stays while there are)."""
        with self._lock:
            procs = ([self._current] if self._current is not None else []) + list(self._retired)
        return sum(p.runs_seen() for p in procs if not p.dead)

    def address(self) -> dict:
        """For an old tap's `probe daemon worker` (the proxy): where the host listens."""
        proc = self._ensure()
        return {"socket": str(socket_path()), "pid": proc.pid}

    def public(self) -> dict:
        with self._lock:
            proc = self._current
            retired = [p.pid for p in self._retired if not p.dead]
        if proc is None:
            return {"enabled": enabled(), "pid": None, "runs": 0, "retired": retired,
                    "replaced": self._replace_reason}
        beat_age = round(time.monotonic() - proc.last_beat, 1)
        return {"enabled": enabled(), "pid": proc.pid, "runs": len(proc.live_runs()), "rss_mb": proc.rss_mb and
                round(proc.rss_mb, 1), "beat_age_s": beat_age, "retired": retired, "replaced": self._replace_reason}

    def run_info(self, run: HostedRun) -> dict:
        """The host's last word on one run (`service.status` rows)."""
        for row in (run._proc.beat or {}).get("runs") or []:
            if isinstance(row, dict) and row.get("run") == run.run_id:
                return row
        return {}


def host_runs_on_file(pid: int) -> dict | None:
    """The daemon host `pid`'s runs as it last wrote them (`host-runs-<pid>.json`,
    every beat): {sid: finishing an ended session's queue}. None when unreadable."""
    try:
        data = json.loads((folder() / f"host-runs-{pid}.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("pid") != pid:
        return None
    return {r.get("sid"): bool(r.get("draining")) for r in data.get("runs") or [] if isinstance(r, dict)}


def _safe_sid(sid: str) -> str:
    return "".join(c for c in sid if c.isalnum() or c in "-_") or "session"


def _group_alive(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return True
    return True
