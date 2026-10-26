"""The daemon host: every recorded session's Probe daemon worker in ONE process.

Plan `~/plans/daemon-in-service/PLAN.md` (H1-H15). The Probe service starts it
(`probe.service.daemonhost`) as its one child; an old tap's `probe daemon worker`
reaches it through the proxy (`probe.daemon.proxy`).

    service DaemonHost ──host.sock──>  this process
      start {run, sid, transcript,       ├─ one thread + asyncio loop per run:
             cwd, source, daemon_dir,    │    `worker.run_session` -> exit code,
             env, draining, finish_by}   │    its env, slots and lease token its
      stop {run}  retire                 │    own (`runctx`), its logs routed to
      <- started / exited {code} / beat  │    its own files (`RunLogRouter`)
                                         ├─ control thread: connections, beats
                                         └─ faulthandler -> host-crash-<pid>.log,
                                            thread ids -> host-threads-<pid>.json

A run's OWNER is the connection that started it: its exit code goes there, and
when that connection closes the run's supervisor is gone -- the worker finishes
its queue, or hands over when asked, exactly as a per-process worker whose
supervisor exited. The host has no respawn policy: the owner's supervisor keeps
its own (the service's `workers.Supervisor`, an old tap's own).

Isolation (plan H10): a run blocks only its own thread; the control thread
never touches a session's files; log records go through handlers of the run's
own (one lock each), never one shared lock.

Stops: SIGTERM asks every run to stop (each finishes or hands over). `retire`
does the same and takes no new run (a host being replaced, H14). A host that has
lost every owner exits once its runs are done, and after FINISH_CAP_S plus a
margin at the latest (its runs' own cap), so a host the service no longer owns
never runs on.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import faulthandler
import json
import logging
import os
import selectors
import signal
import socket
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from probe.daemon import runctx

log = logging.getLogger("probe.daemon.host")

PROTOCOL = 1
#: A message is one JSON line, at most this long (a session's environment rides it).
MAX_LINE = 4 * 1024 * 1024
#: The watcher looks at every run's files this often (plan M2).
WATCH_S = 1.0
#: Every this many watcher passes, each run's watched files are asked again.
WATCH_REFRESH_PASSES = 30
#: A send to a connection that does not read gives up after this.
SEND_TIMEOUT_S = 5.0
#: The service is told how each run is doing this often (`beat`).
BEAT_S = 5.0
#: With no run and no owner connected, the host leaves after this.
IDLE_EXIT_S = 30.0
#: `daemonhost.HANDOVER_AHEAD_S`: a stopped host's live runs see their hand-over ask fresh this long.
HANDOVER_AHEAD_S = 180.0
#: A host whose owners have all gone ends this long after the last one left,
#: however its runs are doing (their own finish cap is `worker.FINISH_CAP_S`).
ORPHAN_MARGIN_S = 120.0
#: The marker in a host's command line (`probe.service.updater` and `ps` tell it by this).
ARGV_MARK = "daemon-host"
ENTRY = "import sys; from probe.daemon.host import main; sys.exit(main())"
#: Each run's log handlers, kept in its slots (`RunLogRouter`).
LOG_HANDLERS_SLOT = "probe.daemon.host.log_handlers"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


class RunLogRouter(logging.Handler):
    """The host's one root handler: a record goes to the handlers of the run it
    was made in (`runctx`), else to the host's own stream. `handle` takes no lock
    of its own: each run's file handlers lock themselves, so a run whose log
    folder hangs never holds another run's records."""

    def __init__(self, fallback: logging.Handler) -> None:
        super().__init__(logging.NOTSET)
        self.fallback = fallback

    def handle(self, record: logging.LogRecord) -> bool:  # noqa: D102 -- see the class
        if not self.filter(record):
            return False
        self.emit(record)
        return True

    def emit(self, record: logging.LogRecord) -> None:
        run = runctx.current()
        handlers = run.slots.get(LOG_HANDLERS_SLOT) if run is not None else None
        if not handlers:
            if record.levelno >= self.fallback.level:
                self.fallback.handle(record)
            return
        for handler in handlers:
            if record.levelno >= handler.level:
                handler.handle(record)


def _finishing(run) -> bool:
    """Is `run` finishing its session's queue (its session ended, its owner left,
    or a stop already asked of it), not a live run to hand over? `stopper.asked`
    is set at once, before the run's loop has begun stopping."""
    stopper = getattr(run, "stopper", None)
    return bool(run.draining or getattr(run, "owner_gone", False) or getattr(stopper, "asked", False)
                or getattr(run.worker, "stopping", False))


def _date_handover(run, until: float) -> None:
    """`run`'s session's `.handover` (the file its worker reads, `mailbox.handover_path`),
    dated `until`: the worker hands over at its next model round."""
    safe = "".join(c for c in run.sid if c.isalnum() or c in "-_") or "session"
    marker = Path(run.daemon_dir) / f"{safe}.handover"
    with contextlib.suppress(OSError):
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
        os.utime(marker, (until, until))


def run_handlers(sid: str, daemon_dir: Path, level: str) -> list[logging.Handler]:
    """A run's log files: the per-process worker's own (`trace.log_handlers`'s
    `worker.log`, at `level`) and, in place of its stderr, the session's
    `<daemon_dir>/<sid>.log` (warnings and worse), the file a per-process
    worker's supervisor gives it."""
    from probe.daemon import trace as trace_mod

    formatter = logging.Formatter(LOG_FORMAT)
    handlers: list[logging.Handler] = []
    for handler in trace_mod.log_handlers(sid):
        if isinstance(handler, logging.FileHandler):
            handler.setLevel(level)
            handler.setFormatter(formatter)
            handlers.append(handler)
        else:
            handler.close()  # the host's stderr is no session's
    try:
        daemon_dir.mkdir(parents=True, exist_ok=True)
        # As the per-process worker's supervisor opens it: 0600, never through a symlink.
        fd = os.open(daemon_dir / f"{sid}.log", os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0),
                     0o600)
        own = logging.StreamHandler(os.fdopen(fd, "a", encoding="utf-8"))
    except OSError:
        pass
    else:
        own.setLevel(logging.WARNING)
        own.setFormatter(formatter)
        handlers.append(own)
    return handlers


def _close_run_client(loop) -> None:
    """The run's model HTTP client (`model._http`, the run's own in the host),
    closed on its loop before the loop goes: its keepalive sockets would outlive
    the run (a process per session freed them at exit)."""
    model = sys.modules.get("probe.daemon.model")
    client = model._http.get() if model is not None else None
    if client is None:
        return
    with contextlib.suppress(Exception):
        loop.run_until_complete(client.aclose())
    model._http.set(None)


def run_loop(ctx: runctx.Run, coro, on_thread=None) -> int:
    """`asyncio.run` for one run: its own loop and default executor (whose threads
    enter the run, `runctx.executor`)."""
    loop = asyncio.new_event_loop()
    executor = runctx.executor(ctx, on_thread=on_thread)
    loop.set_default_executor(executor)
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        try:
            _close_run_client(loop)
            tasks = [t for t in asyncio.all_tasks(loop) if not t.done()]
            for task in tasks:
                task.cancel()
            if tasks:
                loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            loop.run_until_complete(loop.shutdown_asyncgens())
            # Never waited for: a thread stuck on a dead mount must not keep the run from
            # ending (its exit, its lock) on any Python (3.10's shutdown joins it).
            executor.shutdown(wait=False, cancel_futures=True)
        finally:
            asyncio.set_event_loop(None)
            loop.close()


def run_hosted(*, sid: str, transcript: str, cwd: str, source: str, daemon_dir: Path, env: dict, stopper,
               supervisor_gone, on_worker=lambda worker: None, on_thread=None) -> int:
    """One session's worker run, as the host runs it: its own environment (paths
    made absolute against its folder, H2), its own slots and lease token, its log
    records into its own files, `worker.run_session`'s exit code. Never raises."""
    from probe.daemon import worker as worker_mod

    ctx = runctx.Run(sid, env=runctx.absolute_paths(env, cwd))
    try:
        with runctx.enter(ctx):
            level = os.environ.get("PROBE_DAEMON_LOG", "INFO")
            try:
                handlers = run_handlers(sid, daemon_dir, level)
            except Exception:  # noqa: BLE001 -- no files: the host's own log
                handlers = []
            ctx.slots[LOG_HANDLERS_SLOT] = handlers
            try:
                hooks = worker_mod.RunHooks(
                    say=lambda text: logging.getLogger("probe.daemon").warning("%s", text),
                    supervisor_gone=supervisor_gone, hosted=True,
                    run=lambda coro: run_loop(ctx, coro, on_thread), on_worker=on_worker)
                return worker_mod.run_session(worker_mod.Session(sid, Path(transcript), Path(cwd), source), hooks,
                                              stopper)
            finally:
                ctx.slots.pop(LOG_HANDLERS_SLOT, None)
                for handler in handlers:
                    with contextlib.suppress(Exception):
                        handler.close()
    except BaseException as exc:  # noqa: BLE001 -- one run's failure is its own crash, never the host's
        log.error("session %s's run failed outside the worker: %s: %s", sid, type(exc).__name__, exc)
        return worker_mod.EXIT_CRASHED


@dataclass(eq=False)
class Conn:
    sock: socket.socket
    peer_pid: int | None
    role: str = ""
    buf: bytearray = field(default_factory=bytearray)
    runs: set = field(default_factory=set)
    closed: bool = False
    lock: threading.Lock = field(default_factory=threading.Lock)
    #: Called when a send fails (the host wakes its control loop to close it).
    on_broken: object = None

    def send(self, obj: dict) -> bool:
        data = (json.dumps(obj, separators=(",", ":")) + "\n").encode()
        with self.lock:
            if self.closed:
                return False
            try:
                self.sock.sendall(data)  # its timeout (SEND_TIMEOUT_S) bounds a stuck reader
                return True
            except OSError:
                self.closed = True  # the control loop closes it: its runs' owner has gone
                if self.on_broken is not None:
                    self.on_broken()
                return False


@dataclass(eq=False)
class HostRun:
    run_id: str
    sid: str
    transcript: str
    cwd: str
    source: str
    daemon_dir: Path
    env: dict
    owner: Conn
    draining: bool = False
    finish_by: float | None = None
    owner_gone: bool = False
    stopper: object = None
    worker: object = None
    #: The run's own context (`runctx.Run`), once its worker exists.
    ctx: object = None
    thread: threading.Thread | None = None
    ticked_at: float = 0.0
    cpu_s: float = 0.0
    #: What the watcher looks at for this run, and what it saw last (plan M2).
    watch: list = field(default_factory=list)
    seen: tuple | None = None
    started_at: float = field(default_factory=time.monotonic)

    def tick(self) -> None:
        self.ticked_at = time.monotonic()
        self.cpu_s = time.thread_time()


def _stat_key(path: str) -> tuple | None:
    try:
        st = os.stat(path)
    except OSError:
        return None
    return st.st_size, st.st_mtime_ns


def _valid_sid(sid: object) -> bool:
    return isinstance(sid, str) and 0 < len(sid) <= 128 and "/" not in sid and "\0" not in sid


def _abs(value: object) -> bool:
    return isinstance(value, str) and value.startswith("/") and len(value) <= 4096 and "\0" not in value


def parse_start(msg: dict) -> dict | None:
    """The fields a `start` needs, checked, or None."""
    run_id, sid, source, env = msg.get("run"), msg.get("sid"), msg.get("source"), msg.get("env")
    if not isinstance(run_id, str) or not 0 < len(run_id) <= 128 or not _valid_sid(sid):
        return None
    if not isinstance(source, str) or not source.replace("_", "").isalnum() or len(source) > 64:
        return None
    if not all(_abs(msg.get(key)) for key in ("transcript", "cwd", "daemon_dir")):
        return None
    if not isinstance(env, dict) or len(env) > 2000 or not all(
            isinstance(k, str) and isinstance(v, str) and "\0" not in k + v for k, v in env.items()):
        return None
    finish_by = msg.get("finish_by")
    if finish_by is not None and not isinstance(finish_by, (int, float)):
        return None
    return {"run_id": run_id, "sid": sid, "transcript": msg["transcript"], "cwd": msg["cwd"], "source": source,
            "daemon_dir": Path(msg["daemon_dir"]), "env": dict(env), "draining": bool(msg.get("draining")),
            "finish_by": float(finish_by) if finish_by is not None else None}


class Host:
    def __init__(self, folder: Path, sock_path: Path) -> None:
        self.folder = folder
        self.sock_path = sock_path
        self.sel = selectors.DefaultSelector()
        self.lock = threading.Lock()
        self.runs: dict[str, HostRun] = {}
        self.conns: set[Conn] = set()
        self.retiring = False
        self.stopping = False
        self.idle_since: float | None = time.monotonic()
        self.orphaned_since: float | None = None
        self.had_owner = False
        self._threads: dict[int, str] = {}
        self._files_lock = threading.Lock()
        self._children: dict[int, dict] = {}
        self._listener: socket.socket | None = None
        self._sock_ino: int | None = None
        self._last_beat = 0.0
        #: SIGTERM or SIGINT came: the control loop stops every run (`signalled`).
        self._stop_asked = False
        self._wake_r, self._wake_w = socket.socketpair()
        self._wake_w.setblocking(False)  # a wake never waits, in a signal handler least of all

    # -- files --------------------------------------------------------------
    @property
    def info_path(self) -> Path:
        return self.folder / "host.json"

    @property
    def threads_path(self) -> Path:
        return self.folder / f"host-threads-{os.getpid()}.json"  # each host's own: a replaced one runs beside

    @property
    def children_path(self) -> Path:
        return self.folder / f"host-children-{os.getpid()}.json"

    def _write_json(self, path: Path, obj: dict) -> None:
        """Replace `path` with `obj`: one writer at a time (run threads write these
        together), each from its own temp file, so the newest lands whole."""
        tmp = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
        with self._files_lock:
            try:
                tmp.write_text(json.dumps(obj), encoding="utf-8")
                os.replace(tmp, path)
            except OSError:
                with contextlib.suppress(OSError):
                    tmp.unlink()

    def note_thread(self, sid: str | None, ident: int | None = None) -> None:
        """This thread (or `ident`) runs `sid`'s work (None: no more): for a crash's attribution."""
        ident = threading.get_ident() if ident is None else ident
        with self._files_lock:
            with self.lock:
                if sid is None:
                    self._threads.pop(ident, None)
                else:
                    self._threads[ident] = sid
                snapshot = {hex(k): v for k, v in self._threads.items()}
            self._write_threads(snapshot)

    def _write_threads(self, snapshot: dict) -> None:
        tmp = self.threads_path.with_name(f".{self.threads_path.name}.{os.getpid()}.tmp")
        try:
            tmp.write_text(json.dumps({"pid": os.getpid(), "threads": snapshot}), encoding="utf-8")
            os.replace(tmp, self.threads_path)
        except OSError:
            with contextlib.suppress(OSError):
                tmp.unlink()

    def note_child(self, sid: str, pid: int) -> None:
        """A run started a tool in a process group of its own (`probe`, the shell):
        if this host dies, the service ends that group before the run starts again
        (plan H15), so a write still going never overlaps its own retry."""
        from probe.service import procid

        start = procid.start_time(pid)
        self._save_children(lambda children: children.__setitem__(pid, {"sid": sid, "start": start}))

    def forget_child(self, pid: int) -> None:
        self._save_children(lambda children: children.pop(pid, None))

    def _save_children(self, change) -> None:
        """`change` the children map and write it: snapshot and write under one
        lock, so the newest map is the one on disk (the service reads it after a
        crash to end the tools, H15)."""
        with self._files_lock:
            with self.lock:
                change(self._children)
                snapshot = {str(k): v for k, v in self._children.items()}
            tmp = self.children_path.with_name(f".{self.children_path.name}.{os.getpid()}.tmp")
            try:
                tmp.write_text(json.dumps({"pid": os.getpid(), "children": snapshot}), encoding="utf-8")
                os.replace(tmp, self.children_path)
            except OSError:
                with contextlib.suppress(OSError):
                    tmp.unlink()

    def track_children(self) -> None:
        """Every `asyncio.create_subprocess_exec(start_new_session=True)` a run makes
        is noted while it runs (`note_child`): the daemon's own spawn sites stay as
        they are."""
        real = asyncio.create_subprocess_exec
        host = self

        async def tracked(*args, **kwargs):
            proc = await real(*args, **kwargs)
            run = runctx.current()
            if run is not None and kwargs.get("start_new_session"):
                try:
                    await asyncio.to_thread(host.note_child, run.session_id, proc.pid)
                except Exception:  # noqa: BLE001 -- bookkeeping never fails the tool
                    log.warning("could not note tool process %s", proc.pid)
                except BaseException:
                    # Cancelled before its caller got it: nobody else could ever end it.
                    with contextlib.suppress(OSError):
                        os.killpg(proc.pid, signal.SIGKILL)
                    raise

                async def forget() -> None:
                    try:
                        await proc.wait()
                    except Exception:  # noqa: BLE001 -- forgotten either way
                        pass
                    finally:  # cancelled too: the run's loop ends with its tools' waits
                        host.forget_child(proc.pid)

                asyncio.get_running_loop().create_task(forget())
            return proc

        asyncio.create_subprocess_exec = tracked

    # -- serving ------------------------------------------------------------
    def watch(self) -> None:
        """The watcher (its own thread, plan M2): every WATCH_S, each run's files'
        sizes and times; a run whose files changed is poked. A stat that hangs (a
        dead mount) stops these pokes for every run until it returns, never a
        run: each still polls every IDLE_POLL_S."""
        passes = 0
        while not self.stopping:
            time.sleep(WATCH_S)
            passes += 1
            with self.lock:
                runs = [r for r in self.runs.values() if r.worker is not None and r.watch]
            for run in runs:
                if passes % WATCH_REFRESH_PASSES == 0 and run.ctx is not None:
                    with contextlib.suppress(Exception), runctx.enter(run.ctx):  # its paths, in its environment
                        run.watch = [str(p) for p in run.worker.wake_paths()]  # a helper agent's new log
                seen = tuple(_stat_key(path) for path in run.watch)
                if run.seen is not None and seen != run.seen:
                    with contextlib.suppress(Exception):
                        run.worker.poke()
                run.seen = seen

    def bind(self) -> None:
        self.folder.mkdir(parents=True, exist_ok=True)
        with contextlib.suppress(OSError):
            os.chmod(self.folder, 0o700)
        from probe.service import paths

        # 0700, ours and not a symlink: on the /tmp fallback another local user may
        # have made the folder first (the service's own socket is served the same way).
        paths.private_dir(self.sock_path.parent)
        with contextlib.suppress(FileNotFoundError):
            self.sock_path.unlink()  # a dead host's, or a previous one's this replaces
        listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        listener.bind(str(self.sock_path))
        os.chmod(self.sock_path, 0o600)
        listener.listen(64)
        listener.setblocking(False)
        self._listener = listener
        self._sock_ino = self.sock_path.stat().st_ino
        self.sel.register(listener, selectors.EVENT_READ, "listen")
        self.sel.register(self._wake_r, selectors.EVENT_READ, "wake")
        from probe import __version__

        from probe.service import procid

        self._write_json(self.info_path, {"pid": os.getpid(), "start": procid.start_time(os.getpid()),
                                          "version": str(__version__), "socket": str(self.sock_path),
                                          "protocol": PROTOCOL, "prefix": sys.prefix})

    def wake(self) -> None:
        with contextlib.suppress(OSError):
            self._wake_w.send(b"x")

    def serve(self) -> int:
        while True:
            for key, _mask in self.sel.select(timeout=1.0):
                try:
                    if key.data == "listen":
                        self._accept()
                    elif key.data == "wake":
                        with contextlib.suppress(OSError):
                            self._wake_r.recv(4096)
                    else:
                        self._read(key.data)
                except Exception:  # noqa: BLE001 -- the control thread outlives a bug: every run rides it
                    log.exception("daemon host: a control step failed")
            if self._stop_asked and not self.stopping:
                self.stop_all()
            with self.lock:
                broken = [c for c in self.conns if c.closed]
            for conn in broken:
                self._close(conn)  # a send to it failed: its runs' owner has gone
            now = time.monotonic()
            if now - self._last_beat >= BEAT_S:
                self._last_beat = now
                self._beat()
            done = self._should_exit(now)
            if done:
                self._cleanup()
                return 0

    def _should_exit(self, now: float) -> bool:
        with self.lock:
            runs = len(self.runs)
            owners = [c for c in self.conns if not c.closed]
        if runs == 0:
            if self.stopping or self.retiring:
                return True
            if not owners and self.had_owner:
                return True  # nobody left to start a run here
            if self.idle_since is None:
                self.idle_since = now
            return now - self.idle_since >= IDLE_EXIT_S
        self.idle_since = None
        if owners:
            self.orphaned_since = None
            return False
        if self.orphaned_since is None:
            self.orphaned_since = now
            log.info("every owner has gone: the runs finish or hand over, then this host leaves")
        from probe.daemon import worker as worker_mod

        if now - self.orphaned_since >= worker_mod.FINISH_CAP_S + ORPHAN_MARGIN_S:
            log.warning("runs still going %.0f s after the last owner left: leaving",
                        now - self.orphaned_since)
            return True
        return False

    def _cleanup(self) -> None:
        for path in (self.threads_path, self.children_path, self.runs_path,
                     self.folder / f"host-crash-{os.getpid()}.log"):
            with contextlib.suppress(OSError):
                path.unlink()  # a clean exit: nothing for the service to read
        with contextlib.suppress(OSError):
            if self._sock_ino is not None and self.sock_path.stat().st_ino == self._sock_ino:
                self.sock_path.unlink()  # ours, not a newer host's at the same path
        with contextlib.suppress(OSError, ValueError):
            if json.loads(self.info_path.read_text(encoding="utf-8")).get("pid") == os.getpid():
                self.info_path.unlink()

    def _accept(self) -> None:
        try:
            sock, _ = self._listener.accept()
        except OSError:
            return
        from probe.service import caller

        from probe.service.background import other_network

        pid = caller.peer_pid(sock)
        if caller.sandboxed(pid) or other_network(pid):
            # The host starts daemon work with the environment it is handed: a
            # caller in a sandbox (an agent's own shell) may not (plan S6).
            with contextlib.suppress(OSError):
                sock.sendall(b'{"op":"refused","reason":"sandboxed"}\n')
                sock.close()
            return
        # A timeout, never non-blocking: sends from run threads wait at most
        # SEND_TIMEOUT_S; reads happen only once the selector says data is there.
        sock.settimeout(SEND_TIMEOUT_S)
        conn = Conn(sock=sock, peer_pid=pid, on_broken=self.wake)
        with self.lock:
            self.conns.add(conn)
        self.sel.register(sock, selectors.EVENT_READ, conn)

    def _read(self, conn: Conn) -> None:
        try:
            data = conn.sock.recv(65536)
        except (BlockingIOError, socket.timeout):
            return
        except OSError:
            data = b""
        if not data:
            self._close(conn)
            return
        conn.buf += data
        if len(conn.buf) > MAX_LINE and b"\n" not in conn.buf:
            conn.send({"op": "error", "error": "line too long"})
            self._close(conn)
            return
        while b"\n" in conn.buf:
            line, _, rest = bytes(conn.buf).partition(b"\n")
            conn.buf = bytearray(rest)
            try:
                msg = json.loads(line)
            except ValueError:
                conn.send({"op": "error", "error": "not JSON"})
                continue
            if isinstance(msg, dict):
                self._handle(conn, msg)

    def _close(self, conn: Conn) -> None:
        with contextlib.suppress(Exception):
            self.sel.unregister(conn.sock)
        with conn.lock:
            conn.closed = True
        with contextlib.suppress(OSError):
            conn.sock.close()
        with self.lock:
            self.conns.discard(conn)
            owned = [self.runs[r] for r in conn.runs if r in self.runs]
        for run in owned:
            run.owner_gone = True  # its supervisor is gone (the worker's own rule follows)
            with contextlib.suppress(Exception):
                if run.worker is not None and hasattr(run.worker, "poke"):
                    run.worker.poke()  # an idle run looks now, not at its next idle poll

    def _handle(self, conn: Conn, msg: dict) -> None:
        op = msg.get("op")
        if op == "hello":
            role = msg.get("role")
            conn.role = role if role in ("service", "proxy", "test") else "proxy"
            if conn.role == "service" and conn.peer_pid is not None and conn.peer_pid != os.getppid():
                conn.role = "proxy"  # only the service that started this host is its owner
            if conn.role == "service":
                self.had_owner = True
            from probe import __version__

            conn.send({"op": "hello", "pid": os.getpid(), "version": str(__version__), "protocol": PROTOCOL})
        elif op == "start":
            self._start(conn, msg)
        elif op == "stop" and isinstance(msg.get("sid"), str) and conn.role == "service":
            with self.lock:
                runs = [r for r in self.runs.values() if r.sid == msg["sid"]]
            for run in runs:  # every run of that session here (an old tap's has no other owner to ask it)
                if run.stopper is not None:
                    run.stopper.request()
        elif op == "stop":
            with self.lock:
                run = self.runs.get(msg.get("run"))
            # Its owner's (a proxy stops its own run) or the service's: never another caller's.
            if run is not None and run.stopper is not None and (run.owner is conn or conn.role == "service"):
                run.stopper.request()
        elif op == "retire":
            if conn.role == "service":
                until = msg.get("handover_until")
                self.retire(handover_until=float(until) if isinstance(until, (int, float)) else None)
        elif op == "status":
            # Every session's runs: the service's to see; a proxy sees its own.
            status = self._status()
            if conn.role != "service":
                status["runs"] = [r for r in status["runs"] if r["run"] in conn.runs]
            conn.send(status)
        else:
            conn.send({"op": "error", "error": f"unknown op {op!r}"})

    def _start(self, conn: Conn, msg: dict) -> None:
        spec = parse_start(msg)
        if spec is None:
            conn.send({"op": "exited", "run": msg.get("run"), "code": 2, "reason": "invalid"})
            return
        from probe.daemon import worker as worker_mod

        if self.retiring or self.stopping or worker_mod.install_replaced():
            # Not here: a host being replaced or stopping ("retiring": the run starts
            # again in the current host), or one whose CLI was reinstalled under it
            # ("stale", its next read of its own files could be the new version's,
            # H9: the service replaces it).
            reason = "retiring" if self.retiring or self.stopping else "stale"
            conn.send({"op": "exited", "run": spec["run_id"], "code": 0, "reason": reason})
            return
        with self.lock:
            if spec["run_id"] in self.runs:
                conn.send({"op": "error", "error": "run exists", "run": spec["run_id"]})
                return
            run = HostRun(**spec, owner=conn)
            run.stopper = worker_mod.Stopper()
            self.runs[run.run_id] = run
            conn.runs.add(run.run_id)
            self.had_owner = True
            self.idle_since = None
        if run.draining:
            run.stopper.request()
        run.thread = threading.Thread(target=self._run, args=(run,), name=f"run-{run.sid[:12]}", daemon=True)
        run.thread.start()
        conn.send({"op": "started", "run": run.run_id, "pid": os.getpid()})

    def retire(self, *, handover_until: float | None = None) -> None:
        """Take no new run; every run begins stopping (H14). With `handover_until`:
        each live run (not one finishing an ended session's queue) hands over,
        its `.handover` dated that far ahead, to the next worker of its session."""
        self.retiring = True
        with self.lock:
            runs = list(self.runs.values())
        live = [run for run in runs if not _finishing(run)] if handover_until is not None else []
        if live:
            # A session's files are never touched on the control thread (a hung mount
            # would stop every run's beats): the markers are dated on a thread of their own.
            threading.Thread(target=lambda: [_date_handover(run, handover_until) for run in live],
                             name="handover-markers", daemon=True).start()
        for run in runs:
            if run.stopper is not None:
                run.stopper.request()
        self.wake()

    def stop_all(self) -> None:
        """SIGTERM: stop every run, each live one handing over (the service that
        started this host left, or an updater asked)."""
        self.stopping = True
        self.retire(handover_until=time.time() + HANDOVER_AHEAD_S)

    def signalled(self) -> None:
        """SIGTERM or SIGINT: every run begins stopping. Done by the control loop,
        never in the handler: that runs on the control thread, which it may have
        interrupted inside the host's lock."""
        self._stop_asked = True
        self.wake()

    # -- a run ----------------------------------------------------------------
    def _run(self, run: HostRun) -> None:
        from probe.daemon import worker as worker_mod

        code = worker_mod.EXIT_CRASHED
        idents = {threading.get_ident()}

        def on_thread() -> None:  # one of the run's executor threads, as it starts
            idents.add(threading.get_ident())
            self.note_thread(run.sid)

        self.note_thread(run.sid)
        try:
            code = run_hosted(sid=run.sid, transcript=run.transcript, cwd=run.cwd, source=run.source,
                              daemon_dir=run.daemon_dir, env=run.env, stopper=run.stopper,
                              supervisor_gone=lambda: run.owner_gone, on_worker=lambda w: self._bind(run, w),
                              on_thread=on_thread)
        finally:
            for ident in list(idents):  # its executor threads ended with its loop
                self.note_thread(None, ident)
            self._finish(run, code)

    def _bind(self, run: HostRun, worker) -> None:
        run.worker = worker
        run.ctx = runctx.current()  # the watcher asks its paths again in it
        worker.on_tick = run.tick
        worker.wakeable = True
        try:
            run.watch = [str(p) for p in worker.wake_paths()]  # in the run's own environment
        except Exception:  # noqa: BLE001 -- unwatched: it polls every IDLE_POLL_S when idle
            run.watch = []
        if run.finish_by is not None:
            # A draining run moved from a host that died: the deadline it had (H14).
            worker.finish_by = run.finish_by

    def _finish(self, run: HostRun, code: int) -> None:
        with self.lock:
            self.runs.pop(run.run_id, None)
            run.owner.runs.discard(run.run_id)
        run.owner.send({"op": "exited", "run": run.run_id, "code": int(code)})
        self.wake()

    # -- beats ------------------------------------------------------------------
    def _status(self) -> dict:
        now = time.monotonic()
        with self.lock:
            runs = list(self.runs.values())
        return {"op": "beat", "pid": os.getpid(), "retiring": self.retiring, "runs": [
            {"run": r.run_id, "sid": r.sid, "draining": _finishing(r),
             "tick_age_s": round(now - r.ticked_at, 1) if r.ticked_at else None, "cpu_s": round(r.cpu_s, 2),
             "up_s": round(now - r.started_at, 1)} for r in runs]}

    def _beat(self) -> None:
        with self.lock:
            owners = [c for c in self.conns if c.role == "service" and not c.closed]
        beat = self._status()
        # Also on file, for whoever is not this host's service (a later service, the
        # update guard): which runs are finishing an ended session's queue (never
        # handed over: no successor would record the tail) and which are live.
        self._save_runs({"pid": os.getpid(), "runs": [{"sid": r["sid"], "draining": r["draining"]}
                                                     for r in beat["runs"]]})
        for conn in owners:
            conn.send(beat)

    @property
    def runs_path(self) -> Path:
        return self.folder / f"host-runs-{os.getpid()}.json"

    def _save_runs(self, data: dict) -> None:
        with self._files_lock:
            tmp = self.runs_path.with_name(f".{self.runs_path.name}.{os.getpid()}.tmp")
            try:
                tmp.write_text(json.dumps(data), encoding="utf-8")
                os.replace(tmp, self.runs_path)
            except OSError:
                with contextlib.suppress(OSError):
                    tmp.unlink()


def _raise_open_files() -> None:
    """Every session's stores, logs and sockets are this one process's: its soft
    open-file limit goes to the hard one (macOS defaults to 256), at most 10,240."""
    with contextlib.suppress(Exception):
        import resource

        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        want = 10_240 if hard == resource.RLIM_INFINITY else min(hard, 10_240)
        if soft != resource.RLIM_INFINITY and soft < want:
            resource.setrlimit(resource.RLIMIT_NOFILE, (want, hard))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="probe daemon-host")
    parser.add_argument("mark", nargs="?")
    parser.add_argument("--folder")
    parser.add_argument("--socket")
    #: One session's run in this process and nothing else (the replay bench runs
    #: each fixture through the host's own run path this way).
    parser.add_argument("--one", action="store_true")
    parser.add_argument("--session-id")
    parser.add_argument("--transcript")
    parser.add_argument("--cwd")
    parser.add_argument("--source", default=None)
    args = parser.parse_args(argv)
    if os.name != "posix":
        print("probe daemon-host: POSIX only", file=sys.stderr)
        return 2
    if not args.one and not (args.folder and args.socket):
        parser.error("--folder and --socket (or --one with a session)")
    os.environ.setdefault("PYDANTIC_AI_NO_BANNER", "1")
    folder = Path(args.folder) if args.folder else None
    if folder is not None:
        folder.mkdir(parents=True, exist_ok=True)
        # Its own dump file: a replaced host may still be finishing beside this one.
        crash = open(folder / f"host-crash-{os.getpid()}.log", "a", encoding="utf-8")  # noqa: SIM115 -- for the process's life
        faulthandler.enable(file=crash, all_threads=True)
    else:
        faulthandler.enable(all_threads=True)
    _raise_open_files()
    process_env = dict(os.environ)
    runctx.install()
    # OpenSSL's default loader reads these from the C environment, which a run's own
    # never reaches (each run's are in its own mapping, where `sdk/tls.py` reads them):
    # the host keeps none, or a run that sets none would trust the host's.
    for name in ("SSL_CERT_FILE", "SSL_CERT_DIR"):
        os.environ.base.pop(name, None)  # type: ignore[attr-defined] -- ContextEnviron's process mapping
    stream = logging.StreamHandler()  # the host's own: <folder>/host.log (the service's redirect)
    stream.setFormatter(logging.Formatter(LOG_FORMAT))
    stream.setLevel(logging.INFO)
    root = logging.getLogger()
    root.handlers[:] = [RunLogRouter(stream)]
    root.setLevel(os.environ.get("PROBE_DAEMON_LOG", "INFO"))
    from probe.daemon import trace as trace_mod

    trace_mod.quiet_noisy_loggers()
    logging.captureWarnings(True)
    with contextlib.suppress(Exception):
        import pydantic_ai

        pydantic_ai.BANNER_ENABLED = False  # type: ignore[attr-defined]
    if args.one:
        return _one(args, process_env)
    host = Host(folder, Path(args.socket))
    host.track_children()
    threading.Thread(target=host.watch, name="watcher", daemon=True).start()
    signal.signal(signal.SIGTERM, lambda _s, _f: host.signalled())
    signal.signal(signal.SIGINT, lambda _s, _f: host.signalled())
    try:
        host.bind()
    except OSError as exc:
        log.error("the daemon host cannot listen on %s: %s", args.socket, exc)
        return 1
    log.info("daemon host %s listening on %s", os.getpid(), args.socket)
    code = host.serve()
    # Never the interpreter's exit: it joins every thread, and one of a run stuck on
    # a dead mount would keep this host up for good. Its own log is flushed first
    # (a run's handlers may be held by such a thread: not waited for).
    with contextlib.suppress(Exception):
        stream.flush()
    os._exit(code)


def _one(args: argparse.Namespace, env: dict) -> int:
    """`--one`: this session's run, SIGTERM its stop, the parent's exit its owner
    leaving -- what a per-process worker is, through the host's run path."""
    from probe.daemon import worker as worker_mod

    if not (args.session_id and args.transcript and args.cwd):
        print("probe daemon-host --one: --session-id, --transcript and --cwd", file=sys.stderr)
        return 2
    stopper = worker_mod.Stopper()
    signal.signal(signal.SIGTERM, lambda _s, _f: stopper.request())
    signal.signal(signal.SIGINT, lambda _s, _f: stopper.request())
    parent = os.getppid()
    xdg = env.get("XDG_STATE_HOME")
    state = Path(xdg) if xdg else Path(env.get("HOME") or Path.home()) / ".local" / "state"
    from probe.harness import registry

    return run_hosted(sid=args.session_id, transcript=os.path.abspath(args.transcript), cwd=os.path.abspath(args.cwd),
                      source=args.source or registry.load().default, daemon_dir=state / "probe" / "daemon", env=env, stopper=stopper,
                      supervisor_gone=lambda: os.getppid() != parent)


if __name__ == "__main__":
    raise SystemExit(main())
