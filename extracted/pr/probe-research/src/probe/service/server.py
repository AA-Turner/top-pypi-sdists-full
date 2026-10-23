"""The Probe service: one light process per user per machine, alive only while used.

    first agent session ──ensure──> python -m probe.service
                                      │ service.lock (flock, held for life)
                                      │ service.sock (unix stream, 0600, JSON-RPC 2.0 lines)
                                      │ discovering (15 s) -> running <-> grace (5 s) -> exit
                                      │
            tap watch / pi ──register/heartbeat──> registry ──pid watch──> owner exit
            desktop app    ──hello keepalive────> held alive while connected (D1)

            app / CLI      ──action.run─────────> actions.py ──> python -m probe.core.run <action>
                           ──status.get─────────> statuscache.py (a child, cached 30 s)
            CLI            ──manifest.refresh───> manifest.py (a child refreshes the CLI's cache)
                           ──run.hold/release───> runholds.py (a `probe exec`'s run: the quiet check)
                           ──recorders.finish───> recorders.py (`probe capture off` for one agent)
            (schedule, check_now) ──────────────> updater.py: CLI + plugins, app, self

Nothing here runs on a timer while idle: owners are watched by the kernel
(pidfd on Linux, kqueue on macOS; a 2 s poll only where neither works), and the
only timers are the discovery end, the grace, a heartbeat-only owner's TTL and
the 6-hourly update check. No model calls, no uploads, no capture, no CLI
import: heavy work stays in the per-session workers, and every action, status
read and update runs in a `probe.core.run` child (plan R9, X7; `children.py`).

Stdlib only on the start path (plan S1, Q3; `tests/test_service_import_budget.py`).
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import select
import signal
import socket
import struct
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path

from . import caller, paths
from . import updater as updater_mod
from .actions import ActionManager
from .hookhosts import DRAIN_S, UNHOSTED_LANES, HookHosts, Via, run_event, timed_out_answer
from .hookqueue import HookQueue
from .manifest import ManifestRefresher
from .recorders import RecorderHost
from .runholds import RUNS_NAME, Hold, RunHolds
from .protocol import (
    API_VERSION,
    Action,
    CLIENTS,
    MAX_LINE_BYTES,
    METHODS,
    MODES,
    TOPICS,
    CHECK_TRIGGERS,
    Client,
    EndReason,
    ErrorCode,
    Method,
    RefusedReason,
    RpcError,
    State,
    StopReason,
    Topic,
    CheckTrigger,
    encode,
    error,
    event,
    invalid_params,
    need_bool,
    need_choice,
    need_context,
    need_hook_queue,
    need_hook_run,
    need_int,
    need_owner,
    need_state_dir,
    need_str,
    need_wait,
    parse_request,
    result,
    BASE_URL_ENV,
    Mode,
)
from .registry import HEARTBEAT_TTL_S, Outcome, Registry, Session
from .statuscache import StatusCache
from .updater import Updater, preload

#: Seconds without a live session (or keep-alive client) before the service exits.
GRACE_S = 5.0
#: Seconds after start in which the service never idles out: registrants of a
#: restarted service re-send within this window (plan X6).
DISCOVERY_S = 15.0
#: Test-only overrides (API v1, "Lifecycle"). Nothing in production sets them.
GRACE_ENV = "PROBE_SERVICE_GRACE_S"
DISCOVERY_ENV = "PROBE_SERVICE_DISCOVERY_S"
TTL_ENV = "PROBE_SERVICE_TTL_S"
#: Where neither pidfd nor kqueue can watch a pid, poll it this often.
POLL_S = 2.0
#: A subscriber whose unread events pass this is dropped, not buffered forever.
MAX_SUBSCRIBER_BUFFER = 4 * 1024 * 1024
#: `hooks.run` events running at once, at most: each holds a thread while its
#: routes run (a caller waits 300 ms by default; a later one waits its turn,
#: within its own wait).
MAX_HOOK_RUNS = 8
#: `hooks.run` events taken in at once (running, or queued for a thread): past
#: it a request is refused at once, so stalled folder checks (a hung network
#: mount) never queue without limit. A queued event whose caller's wait has
#: passed is dropped unrun.
MAX_PENDING_HOOK_RUNS = 2 * MAX_HOOK_RUNS
#: `hooks.run`'s answer may land this long after its deadline: an event that
#: ended right at it still has its output read (`hookhosts.DRAIN_S`).
ANSWER_GRACE_S = DRAIN_S + 0.05
#: Host starts (`hooks.host`, a `hooks.run` warm-up) on their own threads, and
#: at most this many taken in at once.
HOST_START_THREADS = 2
MAX_PENDING_HOST_STARTS = 4
#: `hooks.queue` stores (a file write each) on one thread of their own, at
#: most this many taken in at once: past it a dispatcher runs its routes itself.
MAX_PENDING_QUEUE_STORES = 8
#: What a `hooks.queue` answer waits for its store, at most (the dispatcher
#: itself waits 300 ms, then writes the event beside it: one id runs once).
QUEUE_STORE_WAIT_S = 5.0
#: What a `hooks.host` caller waits for its host start, at most.
HOST_START_WAIT_S = 5.0
#: A folder's warm host is started for `hooks.run` at most this often (a host
#: that will not stay up is not started again on every tool call): the
#: dispatcher's own `ASK_EVERY_S`.
WARM_EVERY_S = 30.0
#: The log is cut over to `service.log.1` at start once it passes this.
MAX_LOG_BYTES = 256 * 1024
#: Created while the service stops, so a new instance that finds the lock still
#: held waits for it instead of exiting (the old one is about to let go).
STOPPING_NAME = "service.stopping"
STOPPING_WAIT_S = 3.0
#: While another process holds the pre-machine-key folder's lock (a service
#: from before the key, still running), look again this often (plan D8).
LEGACY_RETRY_S = 10.0
LEGACY_RETRY_ENV = "PROBE_SERVICE_LEGACY_RETRY_S"


_session_envs: dict | None = None


def session_envs() -> dict:
    """`{harness id: its session-id variable}`, from the harness registry
    (light: stdlib only). Read once; empty if the registry cannot be."""
    global _session_envs
    if _session_envs is None:
        try:
            from probe.harness import get_registry

            _session_envs = {h.id: h.session_env for h in get_registry().all() if h.session_env}
        except Exception as exc:  # noqa: BLE001 -- a context then just cannot name a session
            log(f"harness registry unreadable: {exc!r}")
            _session_envs = {}
    return _session_envs


def session_env_names() -> frozenset:
    """Every coding agent's session-id variable, which a request's `context`
    may set (`protocol.CONTEXT_ENV`)."""
    return frozenset(session_envs().values())


def _version() -> str:
    try:
        from probe import __version__

        return str(__version__)
    except Exception:  # noqa: BLE001 -- never a reason not to serve
        return "0.0.0.dev0"


def log(message: str) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        sys.stderr.write(f"[{stamp}] probe-service[{os.getpid()}]: {message}\n")
        sys.stderr.flush()
    except (OSError, ValueError):
        pass


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if value >= 0 else default


def peer_uid(sock: socket.socket) -> int | None:
    """The connecting process's uid, where the platform says (plan A6, S6).

    Linux: SO_PEERCRED. macOS: LOCAL_PEERCRED (SOL_LOCAL 0, option 1), which
    Python does not name but `getsockopt` reaches: a `struct xucred` whose
    first two u_ints are its version and the uid. Elsewhere None, and the 0600
    socket in a 0700 folder is the only check.
    """
    try:
        if hasattr(socket, "SO_PEERCRED"):
            raw = sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
            return struct.unpack("3i", raw)[1]
        if sys.platform == "darwin":
            raw = sock.getsockopt(0, 1, 76)
            return struct.unpack("II", raw[:8])[1]
    except OSError:
        return None
    return None


class PidWatcher:
    """Calls back once when a pid exits. Event-driven where the kernel can be asked."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self._pidfds: dict[object, int] = {}
        self._kq = None
        self._kq_keys: dict[int, set] = {}
        self._callbacks: dict[object, tuple[int, str, Callable[[], None]]] = {}
        self._polled: set = set()
        self._poll_handle: asyncio.TimerHandle | None = None
        if hasattr(select, "kqueue") and hasattr(select, "KQ_FILTER_PROC"):
            try:
                self._kq = select.kqueue()
                loop.add_reader(self._kq.fileno(), self._drain_kqueue)
            except (OSError, NotImplementedError, ValueError):
                self._kq = None

    @property
    def mechanism(self) -> str:
        if hasattr(os, "pidfd_open"):
            return "pidfd"
        return "kqueue" if self._kq is not None else "poll"

    def watch(self, key: object, pid: int, start: str, callback: Callable[[], None]) -> None:
        self.cancel(key)
        self._callbacks[key] = (pid, start, callback)
        if hasattr(os, "pidfd_open"):
            try:
                fd = os.pidfd_open(pid)
            except ProcessLookupError:
                self.loop.call_soon(self._fire, key)
                return
            except OSError:
                self._poll(key)
                return
            self._pidfds[key] = fd
            self.loop.add_reader(fd, self._fire, key)
            return
        if self._kq is not None:
            keys = self._kq_keys.setdefault(pid, set())
            if not keys:
                try:
                    self._kq.control(
                        [
                            select.kevent(
                                pid,
                                filter=select.KQ_FILTER_PROC,
                                flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT,
                                fflags=select.KQ_NOTE_EXIT,
                            )
                        ],
                        0,
                        0,
                    )
                except ProcessLookupError:
                    del self._kq_keys[pid]
                    self.loop.call_soon(self._fire, key)
                    return
                except OSError:
                    del self._kq_keys[pid]
                    self._poll(key)
                    return
            keys.add(key)
            return
        self._poll(key)

    def _poll(self, key: object) -> None:
        self._polled.add(key)
        if self._poll_handle is None:
            self._poll_handle = self.loop.call_later(POLL_S, self._poll_tick)

    def _poll_tick(self) -> None:
        from . import procid

        self._poll_handle = None
        for key in list(self._polled):
            pid, start, _ = self._callbacks.get(key, (0, "", None))
            if procid.alive(pid, start) is False:
                self._fire(key)
        if self._polled:
            self._poll_handle = self.loop.call_later(POLL_S, self._poll_tick)

    def _drain_kqueue(self) -> None:
        try:
            events = self._kq.control(None, 64, 0)
        except OSError:
            return
        for ev in events:
            for key in list(self._kq_keys.pop(int(ev.ident), ())):
                self._fire(key)

    def _fire(self, key: object) -> None:
        entry = self._callbacks.get(key)
        self.cancel(key)
        if entry is not None:
            try:
                entry[2]()
            except Exception as exc:  # noqa: BLE001
                log(f"owner-exit callback failed: {exc!r}")

    def cancel(self, key: object) -> None:
        entry = self._callbacks.pop(key, None)
        fd = self._pidfds.pop(key, None)
        if fd is not None:
            with contextlib.suppress(Exception):
                self.loop.remove_reader(fd)
            with contextlib.suppress(OSError):
                os.close(fd)
        self._polled.discard(key)
        if entry is not None and self._kq is not None:
            pid = entry[0]
            keys = self._kq_keys.get(pid)
            if keys is not None:
                keys.discard(key)
                if not keys:
                    del self._kq_keys[pid]
                    with contextlib.suppress(OSError):
                        self._kq.control(
                            [select.kevent(pid, filter=select.KQ_FILTER_PROC, flags=select.KQ_EV_DELETE)],
                            0,
                            0,
                        )

    def close(self) -> None:
        for key in list(self._callbacks):
            self.cancel(key)
        if self._poll_handle is not None:
            self._poll_handle.cancel()
        if self._kq is not None:
            with contextlib.suppress(Exception):
                self.loop.remove_reader(self._kq.fileno())
            self._kq.close()


class Connection:
    def __init__(self, writer: asyncio.StreamWriter, peer_pid: int | None = None) -> None:
        self.writer = writer
        #: The connecting process, as the kernel says (plan D9); None where it cannot.
        self.peer_pid = peer_pid
        #: Its start time when it connected: the same process later, or not.
        self.peer_start: str | None = None
        self.hello = False
        self.client: str | None = None
        self.keepalive = False
        self.topics: set = set()
        self.after_reply: Callable[[], None] | None = None

    def send_nowait(self, message: dict) -> bool:
        transport = self.writer.transport
        if transport is None or transport.is_closing():
            return False
        if transport.get_write_buffer_size() > MAX_SUBSCRIBER_BUFFER:
            transport.abort()
            return False
        self.writer.write(encode(message))
        return True

    async def send(self, message: dict) -> None:
        if self.send_nowait(message):
            with contextlib.suppress(ConnectionError, OSError):
                await self.writer.drain()


class Service:
    def __init__(
        self,
        *,
        registry: Registry,
        grace_s: float = GRACE_S,
        discovery_s: float = DISCOVERY_S,
        expected_uid: int | None = None,
        legacy: LegacyDoor | None = None,
    ) -> None:
        self.registry = registry
        #: The pre-machine-key socket, for clients from before the key (plan D8).
        self.legacy = legacy
        self.grace_s = grace_s
        self.discovery_s = discovery_s
        self.expected_uid = os.getuid() if expected_uid is None else expected_uid
        self.version = _version()
        self.pid = os.getpid()
        self.started_at = time.time()
        self.state = State.DISCOVERING
        self.connections: set[Connection] = set()
        self.stop_reason: str | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._done: asyncio.Future | None = None
        self._server: asyncio.AbstractServer | None = None
        self._discovering_until = 0.0  # monotonic
        self._discovery_handle: asyncio.TimerHandle | None = None
        self._grace_handle: asyncio.TimerHandle | None = None
        self._expiry_handle: asyncio.TimerHandle | None = None
        self.watcher: PidWatcher | None = None
        self.status_cache = StatusCache()
        #: Warm hook hosts, one per plugin folder sessions use (plan A0).
        self.hookhosts = HookHosts(log)
        #: `hooks.run`'s threads (plan D38), started on the first, and its slots.
        self._hook_runs = None
        self._hook_slots = threading.BoundedSemaphore(MAX_PENDING_HOOK_RUNS)
        #: Host starts' threads and slots: a folder check and a process start
        #: block, so neither runs on this loop.
        self._host_starts = None
        self._host_slots = threading.BoundedSemaphore(MAX_PENDING_HOST_STARTS)
        #: Warm-ups under way (asyncio keeps only a weak reference to a task).
        self._warming: set = set()
        #: plugin folder -> when `hooks.run` last started its host (monotonic).
        self._warmed: dict = {}
        #: Hook events' record-keeping routes, queued to run once (plan D36):
        #: stored on `_queue_stores`' thread, run on the queue's own.
        self.hook_queue = HookQueue(
            log, version=self.version, warm=self._warm_soon, changed=self._queue_changed
        )
        self._queue_stores = None
        self._queue_slots = threading.BoundedSemaphore(MAX_PENDING_QUEUE_STORES)
        #: Sessions this service records itself, one thread each (plan A2).
        self.recorders = RecorderHost(log=log, loop_getter=lambda: self._loop, changed=self._recorders_changed)
        #: The runs a `probe exec` wraps here (`run.hold`), beside the registry.
        self.runs = RunHolds(registry.path.parent / RUNS_NAME)
        #: The CLI's release-manifest refreshes (`manifest.refresh`).
        self.manifest = ManifestRefresher(changed=self.reevaluate)
        #: An update installed a new CLI while an action ran: stop once it ends.
        self._restart_pending = False
        self.actions = ActionManager(
            emit=self._emit, changed=self._changed, holder=self.mutating_holder, finished=self._action_finished
        )
        self.updater = Updater(
            version=self.version,
            emit=self._emit,
            changed=self._cycle_changed,
            stop=self._restart_for_update,
            action_running=lambda: self.actions.running is not None,
            discovering=lambda: self.discovering,
            daemon_session=self.registry.daemon_unseen,
            state_dirs=self.registry.state_dirs,
            run_held=self.runs.live,
        )
        updater_mod.set_hosted(self.recorders.live)

    # -- lifecycle -----------------------------------------------------------

    async def run(self, listen: socket.socket, *, on_ready: Callable[[], None] | None = None) -> str:
        """Serve on `listen` until idle, stopped or signalled. Returns why it stopped."""
        self._loop = asyncio.get_running_loop()
        self._done = self._loop.create_future()
        # Before anything below can ask what holds the service (an action the
        # last service left unfinished ends during `actions.load`).
        self._discovering_until = time.monotonic() + self.discovery_s
        self.watcher = PidWatcher(self._loop)
        for session in self.registry.load():
            self._watch(session)
        for hold in self.runs.load():
            self._watch_hold(hold)
        self._schedule_expiry()
        self.actions.load(self.watcher.watch)
        self.updater.attach(self._loop)
        # Before the socket opens, so no `hooks.queue` finds it unready; what a
        # dispatcher queued while no service ran starts running now.
        self.hook_queue.start()
        self._server = await asyncio.start_unix_server(self._handle, sock=listen, limit=MAX_LINE_BYTES + 1)
        if self.legacy is not None:
            await self.legacy.open(self._loop, self._handle)
        if self.discovery_s > 0:
            self._discovery_handle = self._loop.call_later(self.discovery_s, self._discovery_over)
        else:
            self._discovery_over()
        with contextlib.suppress(NotImplementedError, RuntimeError, ValueError):
            for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
                self._loop.add_signal_handler(sig, self.stop, StopReason.SIGNAL)
        log(
            f"serving (api {API_VERSION}, version {self.version}, pid watch {self.watcher.mechanism}, "
            f"{len(self.registry.sessions)} session(s) restored, grace {self.grace_s}s, "
            f"discovery {self.discovery_s}s)"
        )
        if on_ready is not None:
            on_ready()
        # The sessions the last service recorded, from their saved progress
        # (after `on_ready`: the tap's import is no part of the start path).
        self._loop.call_soon(self._resume_recorders)
        # The CLI versions this machine's processes run from, for a home other
        # machines share (`installs.prune`).
        self._loop.run_in_executor(None, _mark_versions)
        # The OS keeper (D35): the system starts the service again after a crash.
        self._loop.run_in_executor(None, _keep)
        try:
            return await self._done
        finally:
            await self._shutdown()

    def _discovery_over(self) -> None:
        self._discovery_handle = None
        self._discovering_until = 0.0
        # `probe status`'s `service.state` changes with it (`status.get`'s cache).
        self.status_cache.invalidate()
        self.reevaluate()
        # No updates while discovering (X6): the registry is still filling up.
        self.updater.after_discovery()

    @property
    def discovering(self) -> bool:
        return time.monotonic() < self._discovering_until

    def holds(self) -> bool:
        """Is anything keeping the service alive (plan D1, R3; API v1 "Alive")?
        A live session, a keep-alive client (the app's window), an action in
        progress, an update cycle (for at most its hold), a session's recorder
        still finishing (its last pass and FINALIZE), a manifest refresh in
        flight (at most its child's timeout), or queued hook events not yet run
        (each bounded by its lane's budget). A run hold does not: with no
        service there is no updater to keep off the run."""
        if self.registry.alive_count() > 0 or self.recorders.alive() or self.manifest.in_flight():
            return True
        if self.hook_queue.pending() > 0:
            return True  # queued hook events still to run (plan D36)
        if self.actions.running is not None or self.updater.holding():
            return True
        return any(conn.keepalive for conn in self.connections)

    def mutating_holder(self) -> dict | None:
        """What holds the one mutating slot (plan A5): an action, or the update
        step that replaces the CLI's env. None when it is free."""
        return self.actions.busy_holder() or self.updater.busy_holder()

    def _changed(self) -> None:
        """An action started or ended: what holds the service, and what
        `probe status` would say, may have changed."""
        self.status_cache.invalidate()
        if self._restart_pending and self.actions.running is None:
            self.stop(StopReason.UPDATE)
            return
        self.reevaluate()

    def _cycle_changed(self) -> None:
        """An update cycle started or ended: what holds the service may have
        changed, and so may every version `probe status` reports."""
        self.status_cache.invalidate()
        self.reevaluate()

    def _recorders_changed(self) -> None:
        self.status_cache.invalidate()
        self.reevaluate()

    def _resume_recorders(self) -> None:
        if self.stop_reason is not None:
            return
        try:
            resumed = self.recorders.resume(self._register_saved)
        except Exception as exc:  # noqa: BLE001 -- capture falls back to `tap watch` on the next prompt
            log(f"recorder: resuming failed: {exc!r}")
            return
        if resumed:
            log(f"recorder: {resumed} session(s) resumed")
        self.reevaluate()

    def _register_saved(self, params: dict) -> None:
        """A resumed recorder's session, unless the registry kept it."""
        sid = params.get("sid")
        if any(s.sid == sid for s in self.registry.sessions.values()):
            return
        self._register(None, {**params, "generation": int(time.time() * 1000)})

    def _action_finished(self, action: str) -> None:
        if action == Action.UPDATE:
            self.updater.after_update_action()

    def _restart_for_update(self, reason: str) -> None:
        """An update cycle installed a new CLI: this service is old code. Not
        under a running action, though, whose child would lose the rest of its
        events and read as stopped with the service: the action holds the one
        mutating slot meanwhile, and the stop follows the moment it ends."""
        if self.actions.running is not None:
            if not self._restart_pending:
                log("a new CLI is installed: restarting once the running action ends")
            self._restart_pending = True
            return
        self.stop(reason)

    def reevaluate(self) -> None:
        if self.stop_reason is not None or self._loop is None:
            return
        if self.discovering:
            self.state = State.DISCOVERING
            return
        if self.holds():
            self.state = State.RUNNING
            if self._grace_handle is not None:
                self._grace_handle.cancel()
                self._grace_handle = None
            return
        if self._grace_handle is None:
            self.state = State.GRACE
            self._grace_handle = self._loop.call_later(self.grace_s, self._grace_over)

    def _grace_over(self) -> None:
        self._grace_handle = None
        if self.holds():
            self.reevaluate()
            return
        self.stop("idle")

    def stop(self, reason: str) -> None:
        if self.stop_reason is not None or self._done is None:
            return
        self.stop_reason = reason
        with contextlib.suppress(OSError):
            (paths.service_dir() / STOPPING_NAME).touch()
        log(f"stopping ({reason})")
        self._emit(Topic.SERVICE_STOPPING, {"reason": reason})
        with contextlib.suppress(Exception):
            self.updater.before_exit(reason)
        with contextlib.suppress(Exception):
            from . import guard

            guard.record_stop(reason, self.version)
        if reason in (StopReason.UPDATE, StopReason.TAP_UPDATE):
            with contextlib.suppress(Exception):
                from . import client

                # Its parent too: on Windows a venv's python is a launcher's child.
                client.forget_start(os.getpid(), os.getppid())
        self.updater.close()
        if not self._done.done():
            self._done.set_result(reason)

    async def _shutdown(self) -> None:
        for handle in (self._discovery_handle, self._grace_handle, self._expiry_handle):
            if handle is not None:
                handle.cancel()
        if self._server is not None:
            self._server.close()
        if self.legacy is not None:
            self.legacy.close()
        for conn in list(self.connections):
            with contextlib.suppress(Exception):
                await asyncio.wait_for(conn.writer.drain(), 0.2)
            with contextlib.suppress(Exception):
                conn.writer.close()
        if self.watcher is not None:
            self.watcher.close()
        self.hookhosts.close()
        self.hook_queue.close()
        for pool in (self._hook_runs, self._host_starts, self._queue_stores):
            if pool is not None:
                pool.shutdown(wait=False, cancel_futures=True)
        # Every recorder pauses (after the connections closed: a recorder's link
        # cannot end its session in the registry saved below).
        with contextlib.suppress(Exception):
            await self.recorders.close()
        self.actions.close()
        self.registry.save()

    # -- sessions ------------------------------------------------------------

    def _watch(self, session: Session) -> None:
        if session.owner is None or self.watcher is None:
            return
        key = (session.sid, session.generation)
        self.watcher.watch(
            key,
            session.owner["pid"],
            session.owner["start_time"],
            lambda: self._owner_exited(session.sid, session.generation),
        )

    def _owner_exited(self, sid: str, generation: int) -> None:
        dropped = self.registry.drop(sid, generation)
        if dropped is not None:
            log(f"session {sid} (generation {generation}): owner {dropped.owner['pid']} exited")
            self._emit(Topic.SESSION_ENDED, {"sid": sid, "generation": generation, "reason": EndReason.OWNER_EXIT})
            self._session_gone()
        self.reevaluate()

    def _session_gone(self) -> None:
        self.status_cache.invalidate()
        self.updater.session_ended()

    def _schedule_expiry(self) -> None:
        if self._loop is None:
            return
        if self._expiry_handle is not None:
            self._expiry_handle.cancel()
            self._expiry_handle = None
        due = self.registry.next_expiry()
        if due is not None:
            delay = max(0.0, due - time.time()) + 0.01
            self._expiry_handle = self._loop.call_later(delay, self._expire)

    def _expire(self) -> None:
        self._expiry_handle = None
        for session in self.registry.expired():
            if self.registry.drop(session.sid, session.generation) is not None:
                log(f"session {session.sid}: heartbeat lapsed")
                self._emit(
                    Topic.SESSION_ENDED,
                    {"sid": session.sid, "generation": session.generation, "reason": EndReason.EXPIRED},
                )
                self._session_gone()
        self._schedule_expiry()
        self.reevaluate()

    # -- events --------------------------------------------------------------

    def _emit(self, topic: str, payload: dict) -> None:
        message = event(topic, payload)
        for conn in list(self.connections):
            if topic in conn.topics:
                conn.send_nowait(message)

    # -- connections ---------------------------------------------------------

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        sock = writer.get_extra_info("socket")
        uid = peer_uid(sock) if sock is not None else None
        if uid is not None and uid != self.expected_uid:
            log(f"refused a connection from uid {uid}")
            writer.close()
            return
        conn = Connection(writer, caller.peer_pid(sock) if sock is not None else None)
        if conn.peer_pid is not None and os.path.isdir("/proc/self"):
            # Linux: one /proc read. Elsewhere it would be a `ps` per connection
            # on the loop: there `_action_run` checks only that the pid exists.
            from . import procid

            conn.peer_start = procid.start_time(conn.peer_pid)
        self.connections.add(conn)
        try:
            while self.stop_reason is None:
                try:
                    line = await reader.readuntil(b"\n")
                except asyncio.IncompleteReadError:
                    break
                except asyncio.LimitOverrunError:
                    await conn.send(
                        error(None, RpcError(ErrorCode.INVALID_REQUEST, "invalid request: line over 1 MiB"))
                    )
                    break
                except (ConnectionError, OSError):
                    break
                if not line.strip():
                    continue
                reply = await self.dispatch(conn, line)
                await conn.send(reply)
                if conn.after_reply is not None:
                    action, conn.after_reply = conn.after_reply, None
                    action()
        finally:
            self.connections.discard(conn)
            with contextlib.suppress(Exception):
                writer.close()
            if conn.keepalive:
                self.reevaluate()

    async def dispatch(self, conn: Connection, line: bytes) -> dict:
        try:
            id_, method, params = parse_request(line)
        except RpcError as exc:
            id_ = (exc.data or {}).get("id")
            exc.data = None
            return error(id_, exc)
        if not conn.hello and method != Method.HELLO:
            return error(id_, RpcError(ErrorCode.HELLO_REQUIRED, "hello_required: send service.hello first"))
        if method not in METHODS:
            return error(id_, RpcError(ErrorCode.UNKNOWN_METHOD, f"unknown method: {method}"))
        handler = self._handlers()[method]
        try:
            value = handler(conn, params)
            if asyncio.iscoroutine(value):
                value = await value
        except RpcError as exc:
            return error(id_, exc)
        except Exception as exc:  # noqa: BLE001 -- one bad request never stops the service
            log(f"{method} failed: {exc!r}")
            return error(id_, RpcError(ErrorCode.REFUSED, "internal error", {"reason": RefusedReason.INTERNAL}))
        return result(id_, value)

    def _handlers(self) -> dict:
        return {
            Method.HELLO: self._hello,
            Method.STATUS: self._status,
            Method.STOP: self._stop,
            Method.SESSION_REGISTER: self._register,
            Method.SESSION_END: self._end,
            Method.SESSION_LIST: self._list,
            Method.EVENTS_SUBSCRIBE: self._subscribe,
            Method.STATUS_GET: self._status_get,
            Method.ACTION_RUN: self._action_run,
            Method.ACTION_STATUS: lambda conn, params: self.actions.status(params),
            Method.ACTION_EVENTS: lambda conn, params: self.actions.events(params),
            Method.ACTION_CANCEL: lambda conn, params: self.actions.cancel(params),
            Method.UPDATE_STATUS: lambda conn, params: self.updater.public(),
            Method.UPDATE_CHECK_NOW: self._check_now,
            Method.HOOKS_HOST: self._hooks_host,
            Method.HOOKS_RUN: self._hooks_run,
            Method.HOOKS_QUEUE: self._hooks_queue,
            Method.SESSION_RECORD: self._record,
            Method.SESSION_RECORDING: lambda conn, params: {"recording": self.recorders.recording(params.get("sid"))},
            Method.SESSION_FINISH: lambda conn, params: self.recorders.finish(params),
            Method.RECORDERS_FINISH: self._recorders_finish,
            Method.RUN_HOLD: self._run_hold,
            Method.RUN_RELEASE: self._run_release,
            Method.MANIFEST_REFRESH: self._manifest_refresh,
        }

    # -- methods -------------------------------------------------------------

    def _hello(self, conn: Connection, params: dict) -> dict:
        client = need_choice(params, "client", CLIENTS)
        need_str(params, "client_version", max_len=64)
        api = params.get("api")
        if not isinstance(api, int) or isinstance(api, bool):
            raise invalid_params("api must be an integer")
        if api != API_VERSION:
            raise RpcError(
                ErrorCode.UNSUPPORTED_API,
                f"unsupported_api: this service speaks api {API_VERSION}",
                {"supported": [API_VERSION]},
            )
        keepalive = need_bool(params, "keepalive")
        conn.hello = True
        conn.client = client
        conn.keepalive = keepalive
        self.reevaluate()
        return {
            "service_version": self.version,
            "api": API_VERSION,
            "pid": self.pid,
            "started_at": self.started_at,
            "state": self.state,
        }

    def _status(self, conn: Connection, params: dict) -> dict:
        until = None
        if self.discovering:
            until = self.started_at + self.discovery_s
        return {
            "service_version": self.version,
            "pid": self.pid,
            "started_at": self.started_at,
            "state": self.state,
            "sessions": self.registry.alive_count(),
            "app_clients": sum(1 for c in self.connections if c.hello and c.client == Client.APP),
            "update": self.updater.public(),
            "actions": {"running": self.actions.busy_holder()},
            "discovering_until": until,
            "hook_hosts": self.hookhosts.public(),
            "hook_queue": self.hook_queue.public(),
            "recorders": self.recorders.public(),
            "runs": self.runs.public(),
        }

    def _stop(self, conn: Connection, params: dict) -> dict:
        if self.updater.in_progress():
            raise RpcError(ErrorCode.REFUSED, "refused: an update is running", {"reason": RefusedReason.UPDATING})
        if self.actions.running is not None:
            raise RpcError(
                ErrorCode.REFUSED, "refused: an action is running", {"reason": RefusedReason.ACTION_RUNNING}
            )
        conn.after_reply = lambda: self.stop(StopReason.STOP)
        return {"stopping": True}

    def _register(self, conn: Connection, params: dict) -> dict:
        sid = need_str(params, "sid", max_len=128)
        harness = need_str(params, "harness", max_len=64)
        mode = need_choice(params, "mode", MODES)
        owner = need_owner(params)
        generation = need_int(params, "generation")
        state_dir = need_state_dir(params)
        reg = self.registry.register(sid, harness, mode, owner, generation, state_dir)
        now = time.time()
        if reg.outcome in (Outcome.NEW, Outcome.REPLACED):
            if reg.previous is not None and self.watcher is not None:
                self.watcher.cancel((reg.previous.sid, reg.previous.generation))
            self._watch(reg.session)
            log(
                f"session {sid} registered ({reg.outcome}, {harness}, {mode}, generation {generation}, "
                f"owner {owner['pid'] if owner else 'heartbeat'})"
            )
            self._emit(
                Topic.SESSION_STARTED,
                {
                    "sid": sid,
                    "harness": harness,
                    "mode": mode,
                    "generation": generation,
                    "alive": reg.session.alive(now, self.registry.ttl),
                },
            )
            self.status_cache.invalidate()
        self._schedule_expiry()
        self.reevaluate()
        return {"alive": reg.session.alive(now, self.registry.ttl) if reg.outcome != Outcome.DEAD else False}

    async def _hooks_host(self, conn: Connection, params: dict) -> dict:
        """`hooks.host` (plan A0): never for a caller in a sandbox, whose events
        (and the interpreter it names) would run outside it. The start itself
        (a folder check, a process start) runs on a thread (`_start_host`)."""
        if caller.sandboxed(conn.peer_pid):
            return {"refused": "a caller in a sandbox"}
        return await self._start_host(params)

    def _pool(self, name: str, workers: int):
        pool = getattr(self, name)
        if pool is None:
            from concurrent.futures import ThreadPoolExecutor

            pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix=name.strip("_").replace("_", "-"))
            setattr(self, name, pool)
        return pool

    async def _offload(self, pool: str, workers: int, slots, busy: str, wait: float, fn, *args):
        """`fn(*args)` on one of `pool`'s threads, never this loop: `(True,
        its value)`, or `(False, None)` when it is not done within `wait`.

        Admission is a slot of `slots`, taken here (`{"refused": busy}` at once
        when none is free) and given back only by the thread, when it has run
        the item: so the pool never holds more work items than there are slots,
        however many callers come and go while its threads are stalled. A
        caller past its wait gives up on the answer but never cancels the item
        (a cancelled item would keep its place in the queue with its slot
        given back); `fn` drops work whose deadline passed the moment a thread
        takes it (`hookhosts.run_event`)."""
        if not slots.acquire(blocking=False):
            return True, {"refused": busy}
        once = threading.Lock()  # the slot goes back exactly once

        def give_back() -> None:
            if once.acquire(blocking=False):
                slots.release()

        def held():
            try:
                return fn(*args)
            finally:
                give_back()

        try:
            future = asyncio.wrap_future(self._pool(pool, workers).submit(held))
        except RuntimeError:
            # Shut down (the service is stopping), or no thread would start for
            # an item already queued: that item still gives its slot back when
            # it runs, so never twice (a second release raises ValueError).
            give_back()
            return True, {"refused": "the service could not take it (stopping, or no thread would start)"}
        done, _ = await asyncio.wait({future}, timeout=max(wait, 0.0))
        if done:
            return True, future.result()
        future.add_done_callback(_settled)
        return False, None

    async def _start_host(self, params: dict) -> dict:
        done, answer = await self._offload(
            "_host_starts", HOST_START_THREADS, self._host_slots, "busy: too many host starts in flight",
            HOST_START_WAIT_S, self.hookhosts.host, params,
        )
        return answer if done else {"refused": "the host is still starting"}

    async def _hooks_run(self, conn: Connection, params: dict) -> dict:
        """`hooks.run` (plan D38): one hook event of a harness that has no hooks
        of its own (pi), run for a Probe plugin folder exactly as its dispatcher
        runs it (`hookhosts.run_event`), and the merged output back. Same
        caller checks as `hooks.host`: the peer's uid (every connection), never
        a caller in a sandbox (or one whose pid the kernel will not name), whose
        event would run outside it with the environment it sent; and only a
        complete Probe plugin folder, checked on the thread (it reads files
        the request names: never on this loop, which every client waits on).
        A folder that had no warm host gets one for its next event."""
        request = need_hook_run(params)
        request["deadline"] = time.monotonic() + request["timeout_s"]
        if caller.sandboxed(conn.peer_pid):
            return {"refused": "a caller in a sandbox"}
        # The folder's check reads files the request names: on the thread too,
        # and the answer by the deadline whatever that check costs.
        done, answer = await self._offload(
            "_hook_runs", MAX_HOOK_RUNS, self._hook_slots, "busy: too many hook events in flight",
            request["deadline"] - time.monotonic() + ANSWER_GRACE_S, run_event, request, conn.peer_pid,
        )
        if not done:
            return timed_out_answer()
        if "refused" in answer:
            return answer
        if answer.get("via") != Via.HOST and request["lane"] not in UNHOSTED_LANES and self.stop_reason is None:
            root = request["root"]
            asyncio.get_running_loop().call_soon(lambda: self._warm(root))
        # Past what a client reads in one line: stderr goes first, then stdout,
        # each marked cut, so an intact stdout keeps its verdict while it fits.
        for stream in ("stderr", "stdout"):
            if len(encode(result(0, answer))) <= MAX_LINE_BYTES:
                break
            answer = {**answer, stream: "", f"{stream}_truncated": True, "truncated": True}
        return answer

    async def _hooks_queue(self, conn: Connection, params: dict) -> dict:
        """`hooks.queue` (plan D36): a session's dispatcher that no warm host
        took an event from ran there only what the agent waits on, and hands
        this the event's record-keeping routes, to run once by its id
        (`hookqueue.HookQueue`: `{"queued": true, "duplicate": bool}`, or
        `{"refused": why}`, and the dispatcher then runs them itself). Never
        from a caller in a sandbox (as `hooks.run`: the event would run outside
        it, with the environment it sent). Stored on a thread (a file write),
        run on the queue's own, never on this loop."""
        item = need_hook_queue(params)
        if caller.sandboxed(conn.peer_pid):
            return {"refused": "a caller in a sandbox"}
        done, answer = await self._offload(
            "_queue_stores", 1, self._queue_slots, "busy: too many hook events queued at once",
            QUEUE_STORE_WAIT_S, self.hook_queue.store, item,
        )
        if not done:
            # Still being written, and its caller long gone (it wrote the
            # event beside it, or ran it): the store goes on and runs it once.
            log(f"hooks.queue {item['id']}: still storing after {QUEUE_STORE_WAIT_S}s")
            return {"queued": True, "duplicate": False}
        return answer

    def _queue_changed(self) -> None:
        """From any thread: queued hook events started or stopped holding the service."""
        loop = self._loop
        if loop is not None and not loop.is_closed():
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self.reevaluate)

    def _warm_soon(self, root: str) -> None:
        """From the queue's thread: `root`'s warm host for its next event."""
        loop = self._loop
        if loop is not None and not loop.is_closed():
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self._warm, root)

    def _warm(self, root: str) -> None:
        """Start `root`'s warm host for its next `hooks.run` (`hooks.host`), at
        most every WARM_EVERY_S, on a thread (`_start_host`): never waited on."""
        now, last = time.monotonic(), self._warmed.get(root)
        if self.stop_reason is not None or (last is not None and now - last < WARM_EVERY_S):
            return
        self._warmed[root] = now
        task = asyncio.ensure_future(self._warm_task(root))
        self._warming.add(task)
        task.add_done_callback(self._warming.discard)

    async def _warm_task(self, root: str) -> None:
        try:
            await self._start_host({"root": root})
        except Exception as exc:  # noqa: BLE001 -- only the next event's speed is at stake
            log(f"hook host for {root} would not start: {exc!r}")

    def _record(self, conn: Connection, params: dict) -> dict:
        """`session.record` (plan A2): `session.register`, then this session's
        recorder on a thread here. `{recording: false, ...}` (the tap then
        starts its own `tap watch`) when it cannot be: off POSIX, a caller in a
        sandbox, no owner, no loadable tap, or a newer tap than the one loaded
        (`restart: true`: the service restarts onto it, the caller asks the
        next one)."""
        if caller.sandboxed(conn.peer_pid):
            # Its recorder would run here, outside that sandbox, with the
            # environment (PATH included) the caller sent.
            return {"recording": False, "reason": "sandboxed"}
        refused = self.recorders.check(params)
        if refused is not None:
            if refused.get("restart"):
                self._restart_for_update(StopReason.TAP_UPDATE)
            return refused
        if not self.recorders.live(params.get("sid")):
            # Recorded here already: its link keeps the registration (a second
            # generation from here would make the link step back for good).
            registered = self._register(conn, params)
            if registered.get("alive") is False:
                return {"recording": False, "reason": "owner_gone"}
        return self.recorders.record(params)

    def _end(self, conn: Connection, params: dict) -> dict:
        sid = need_str(params, "sid", max_len=128)
        generation = need_int(params, "generation")
        removed = self.registry.end(sid, generation)
        if removed is not None:
            if self.watcher is not None:
                self.watcher.cancel((removed.sid, removed.generation))
            log(f"session {sid} ended")
            self._emit(Topic.SESSION_ENDED, {"sid": sid, "generation": removed.generation, "reason": EndReason.END})
            self._session_gone()
            self._schedule_expiry()
            self.reevaluate()
        return {}

    def _list(self, conn: Connection, params: dict) -> dict:
        return {"sessions": self.registry.listing()}

    def _subscribe(self, conn: Connection, params: dict) -> dict:
        topics = params.get("topics")
        if not isinstance(topics, list) or not topics or not all(isinstance(t, str) for t in topics):
            raise invalid_params("topics must be a non-empty list of topic names")
        unknown = sorted(set(topics) - TOPICS)
        if unknown:
            raise invalid_params(f"unknown topics {unknown}")
        conn.topics |= set(topics)
        return {}

    async def _status_get(self, conn: Connection, params: dict) -> dict:
        refresh = need_bool(params, "refresh")
        max_age = params.get("max_age")
        if max_age is not None and (
            not isinstance(max_age, (int, float)) or isinstance(max_age, bool) or not 0 <= max_age <= 3600
        ):
            raise invalid_params("max_age must be a number of seconds from 0 to 3600")
        return await self.status_cache.get(self._context(params), refresh=refresh, max_age=max_age)

    def _context(self, params: dict) -> dict:
        """The request's context as the child's environment, its endpoint
        checked (plan D10): the CLI config's stored token follows
        `PROBE_BASE_URL`, so a child runs only with an https endpoint that
        config already names. Anything else is refused, and the app runs the
        CLI itself, with its own environment, as it does on any refusal."""
        env = need_context(params, session_env_names())
        url = env.get(BASE_URL_ENV)
        if url is not None and not caller.known_endpoint(url, env):
            raise invalid_params(
                "base_url must be an https endpoint this machine's Probe CLI is already signed in to"
            )
        return env

    def _caller_session(self, conn: Connection, env: dict) -> Session | None:
        """The registered session the caller runs inside (plan D9), or None:
        its process ancestry passes a session's owner (pid and start time),
        or (Linux) its environment names a registered session. A session
        found this way that the context did not name joins `env` under its
        harness's variable, so `probe.core.run` refuses what it refuses there."""
        names = session_envs()
        found: Session | None = None
        if conn.peer_pid is not None:
            owners = self.registry.owners()
            if owners:
                for pid, start in caller.ancestry(conn.peer_pid):
                    found = owners.get((pid, start))
                    if found is not None:
                        break
            if found is None:
                carried = caller.environ(conn.peer_pid, frozenset(names.values()))
                for value in carried.values():
                    candidate = self.registry.sessions.get(value)
                    if candidate is not None and candidate.alive(time.time(), self.registry.ttl):
                        found = candidate
                        break
        if found is not None:
            name = names.get(found.harness)
            if name and not any(env.get(n) for n in names.values()):
                env[name] = found.sid
        return found

    def _action_run(self, conn: Connection, params: dict) -> dict:
        env = self._context(params)
        if conn.peer_pid is not None:
            from . import procid

            if conn.peer_start:
                gone = procid.alive(conn.peer_pid, conn.peer_start) is False
            else:
                try:
                    os.kill(conn.peer_pid, 0)
                    gone = False
                except ProcessLookupError:
                    gone = True
                except OSError:
                    gone = False
            if gone:
                # The process that connected is gone (a connection handed to a
                # child, which kept the session's environment): who calls can no
                # longer be checked, so nothing changes on its say (plan D9).
                raise RpcError(
                    ErrorCode.REFUSED,
                    "refused: the process that opened this connection has exited; connect again",
                    {"reason": RefusedReason.CALLER_GONE},
                )
        inside = self._caller_session(conn, env)
        if inside is not None and inside.mode == Mode.DAEMON:
            log(f"refused {params.get('action')!r} from inside session {inside.sid}, which the Probe daemon records")
            raise RpcError(
                ErrorCode.REFUSED,
                "refused: Probe's settings cannot be changed from inside a coding agent's session the "
                "Probe daemon records; run it from your own terminal or the Probe app",
                {"reason": RefusedReason.DAEMON_SESSION, "sid": inside.sid},
            )
        if params.get("action") == Action.UPDATE:
            # Before the files it imports from are replaced (R2), as a cycle does.
            try:
                preload()
            except Exception as exc:  # noqa: BLE001 -- a person's Update still runs
                log(f"preload before the update action failed: {exc!r}")
        return self.actions.run(params, env)

    def _check_now(self, conn: Connection, params: dict) -> dict:
        trigger = params.get("trigger", CheckTrigger.CLI)
        if trigger not in CHECK_TRIGGERS:
            raise invalid_params(f"trigger must be one of {sorted(CHECK_TRIGGERS)}")
        return self.updater.check_now(trigger)

    async def _recorders_finish(self, conn: Connection, params: dict) -> dict:
        """`recorders.finish` (`probe capture off` for one agent): every
        recorder of `harness` finishes, as `session.finish` does for one;
        `{finished: [sid], unfinished: [sid]}`, the second still finishing
        after `wait` seconds."""
        harness = need_str(params, "harness", max_len=64)
        wait = need_wait(params)
        await self._refuse_sandboxed(conn)
        sessions = self.registry.sessions

        def harness_of(sid: str) -> str | None:
            session = sessions.get(sid)
            return session.harness if session is not None else None

        answer = await self.recorders.finish_harness(harness, wait, harness_of)
        asked = len(answer["finished"]) + len(answer["unfinished"])
        if asked:
            # The stopper's side of the record (`probe.cli.capture` journals the
            # `tap watch` processes it signals; these it asks here).
            log(
                f"recorders.finish: {asked} recorder(s) of {harness} asked to finish (caller pid "
                f"{conn.peer_pid}); {len(answer['unfinished'])} still finishing after {wait:g} s"
            )
        return answer

    async def _run_hold(self, conn: Connection, params: dict) -> dict:
        """`run.hold`: a `probe exec` holds `run` for as long as `owner` runs.
        `{held: true}`, else `{held: false, reason}` (`owner_gone`,
        `not_caller`, `too_many`, `updating`): its run lock still says it runs.
        Never for a caller in a sandbox (or one the kernel will not name): its
        hold would persist outside it and keep updates off."""
        run = need_str(params, "run", max_len=256)
        owner = need_owner(params)
        if owner is None:
            raise invalid_params("owner must be {pid, start_time}: a hold ends with its process")
        await self._refuse_sandboxed(conn)
        peer = conn.peer_pid

        def check() -> str | None:
            if self.runs.owner_alive(owner["pid"], owner["start_time"]) is False:
                return "owner_gone"
            # The caller holds for itself (or a process it runs under), never
            # for an unrelated one it could keep updates off for.
            if peer is not None and owner["pid"] != peer and (owner["pid"], owner["start_time"]) not in (
                caller.ancestry(peer)
            ):
                return "not_caller"
            return None

        # `ps` on macOS: off the loop.
        refused = await asyncio.to_thread(check)
        if refused is not None:
            return {"held": False, "reason": refused}
        if self.updater.applying:
            # The update's last look is behind it: it would never see this hold.
            return {"held": False, "reason": "updating"}
        hold, new = self.runs.add(run, owner)
        if hold is None:
            return {"held": False, "reason": "too_many"}
        if new:
            self._watch_hold(hold)
            log(f"run {run} held by pid {owner['pid']}")
            self.status_cache.invalidate()
        return {"held": True}

    async def _run_release(self, conn: Connection, params: dict) -> dict:
        """`run.release`: the caller's holds of `run` go from the listing (only
        `owner`'s, when named). `{released: n}`; releasing what is not held,
        or not the caller's, is not an error. Only a hold whose owner is the
        caller or a process it runs under is released, as `run.hold` admits
        it; never from a caller in a sandbox.

        Its process still holds updates off until it exits (`runs.releasing`,
        watched as the hold was): the releasing `probe exec` is still cleaning
        up, importing from the env an update replaces. The deferred update is
        retried at that exit, not now."""
        run = need_str(params, "run", max_len=256)
        owner = params.get("owner")
        pid = None
        if owner is not None:
            pid = owner.get("pid") if isinstance(owner, dict) else None
            if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 1:
                raise invalid_params("owner must be {pid, start_time} or left out")
        await self._refuse_sandboxed(conn)
        chain = set(await asyncio.to_thread(caller.ancestry, conn.peer_pid))  # `ps` on macOS
        gone = self.runs.release(run, chain, pid)
        if gone:
            log(f"run {run} released (its process still holds updates off until it exits)")
            self.status_cache.invalidate()
        return {"released": len(gone)}

    def _watch_hold(self, hold: Hold) -> None:
        if self.watcher is None:
            return
        self.watcher.watch(hold.key, hold.owner["pid"], hold.owner["start_time"], lambda: self._hold_exited(hold))

    def _hold_exited(self, hold: Hold) -> None:
        if self.runs.drop(hold):
            log(f"run {hold.run}: its process {hold.owner['pid']} exited")
            self._run_gone()

    def _run_gone(self) -> None:
        """A run is over: a deferred update gets another try, as when a session ends."""
        self.status_cache.invalidate()
        self.updater.session_ended()

    async def _manifest_refresh(self, conn: Connection, params: dict) -> dict:
        """`manifest.refresh`: the CLI's cached release manifest, refreshed by
        a child with the request's context; `{outcome, done, result}`."""
        env = self._context(params)
        wait = need_wait(params)
        await self._refuse_sandboxed(conn)
        return await self.manifest.refresh(env, wait=wait)

    async def _refuse_sandboxed(self, conn: Connection) -> None:
        """Refuse a caller in a sandbox (as `hooks.host` and `session.record`
        do): a child this runs would fetch and write outside it, with the
        context it chose, and a recorder it stops is outside it too. The CLI
        then does it itself, inside. Unknown counts as sandboxed."""
        if await asyncio.to_thread(caller.sandboxed, conn.peer_pid):
            raise RpcError(
                ErrorCode.REFUSED, "refused: a caller in a sandbox", {"reason": RefusedReason.SANDBOXED}
            )


def _settled(future: asyncio.Future) -> None:
    """An answer nobody waits for any more: read, so it is never reported unread."""
    if not future.cancelled():
        future.exception()


class LegacyDoor:
    """The socket clients from before the machine key connect to (plan D8).

    A session started before the update that brought the key runs a tap, and
    a desktop app not yet updated computes, `~/.local/state/probe/service/
    service.sock`. This service serves that path too whenever it holds that
    folder's `service.lock`, exactly as the service of that time did, so those
    clients register, read status and run actions here. While another process
    holds it (a service from before the key, still running), it looks again
    every LEGACY_RETRY_S. One per HOME: on a shared home folder, one machine's
    service serves the old clients, as before the key."""

    def __init__(self) -> None:
        self.fd: int | None = None
        self.server: asyncio.AbstractServer | None = None
        self.bound: tuple[int, int] | None = None
        self.path = paths.legacy_socket_path()
        self._retry: asyncio.TimerHandle | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._handler: Callable | None = None
        self.retry_s = _env_float(LEGACY_RETRY_ENV, LEGACY_RETRY_S)

    async def open(self, loop: asyncio.AbstractEventLoop, handler: Callable) -> None:
        self._loop, self._handler = loop, handler
        await self._try()

    async def _try(self) -> None:
        self._retry = None
        if self.server is not None or self._loop is None:
            return
        fd = _take_lock(paths.legacy_lock_path(), wait_for_stopping=False)
        if fd is None:
            self._retry = self._loop.call_later(self.retry_s, lambda: asyncio.ensure_future(self._try()))
            return
        try:
            paths.private_dir(self.path.parent)
            listen = _bind(self.path)
            st = os.stat(self.path)
            self.server = await asyncio.start_unix_server(self._handler, sock=listen, limit=MAX_LINE_BYTES + 1)
        except OSError as exc:
            log(f"cannot serve the pre-machine-key socket {self.path}: {exc}")
            os.close(fd)
            self._retry = self._loop.call_later(self.retry_s, lambda: asyncio.ensure_future(self._try()))
            return
        self.fd = fd
        self.bound = (st.st_dev, st.st_ino)
        log(f"also serving {self.path} (clients from before the machine key)")

    def close(self) -> None:
        if self._retry is not None:
            self._retry.cancel()
            self._retry = None
        if self.server is not None:
            self.server.close()
            self.server = None
        # Unlink only OUR socket, and before the lock goes, as `run_service` does.
        with contextlib.suppress(OSError):
            st = os.stat(self.path)
            if self.bound is not None and (st.st_dev, st.st_ino) == self.bound:
                os.unlink(self.path)
        if self.fd is not None:
            with contextlib.suppress(OSError):
                os.close(self.fd)
            self.fd = None


# -- process entry ------------------------------------------------------------


def _open_log() -> int | None:
    path = paths.log_path()
    try:
        if path.stat().st_size > MAX_LOG_BYTES:
            os.replace(path, path.with_name(path.name + ".1"))
    except OSError:
        pass
    try:
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
    except OSError:
        return None


def _take_lock(path: Path | None = None, *, wait_for_stopping: bool = True) -> int | None:
    """The life-long `service.lock` (this machine's, unless `path` names
    another), or None when another service holds it."""
    import fcntl

    try:
        fd = os.open(path or paths.lock_path(), os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    except OSError:
        if path is None:
            raise
        return None
    deadline = None
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd
        except BlockingIOError:
            # A service that is stopping lets go within moments; one that runs
            # does not, and then this instance is the duplicate and leaves.
            if not wait_for_stopping or not (paths.service_dir() / STOPPING_NAME).exists():
                os.close(fd)
                return None
            if deadline is None:
                deadline = time.monotonic() + STOPPING_WAIT_S
            if time.monotonic() >= deadline:
                os.close(fd)
                return None
            time.sleep(0.05)


def _keep() -> None:
    with contextlib.suppress(Exception):
        from . import keeper

        outcome = keeper.install()
        if outcome not in ("current", "not wanted"):
            log(f"keeper: {outcome}")


def _mark_versions() -> None:
    with contextlib.suppress(Exception):
        from probe._shared import installs

        if installs.versions_root().is_dir():
            installs.mark_in_use()


def _name_holder(fd: int) -> None:
    """Write `<pid> <start time>` into the lock file this service holds: the
    guard (D5) finds a replacement that hangs without answering there, and
    stops that exact process (`guard.holder`). Never raises."""
    from . import procid

    with contextlib.suppress(OSError):
        os.ftruncate(fd, 0)
        os.pwrite(fd, f"{os.getpid()} {procid.start_time(os.getpid()) or ''}\n".encode(), 0)


def _bind(path: Path) -> socket.socket:
    """Bind the socket 0600 (we hold service.lock, so anything there is stale)."""
    with contextlib.suppress(FileNotFoundError):
        os.unlink(path)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    old = os.umask(0o177)
    try:
        sock.bind(str(path))
    finally:
        os.umask(old)
    os.chmod(path, 0o600)
    sock.listen(64)
    sock.setblocking(False)
    return sock


def run_service() -> int:
    """`python -m probe.service`: one instance; exits 0 when idle or as a duplicate."""
    try:
        sock_path = paths.ensure_dirs()
    except OSError as exc:
        log(f"cannot use {paths.service_dir()}: {exc}")
        return 1
    lock_fd = _take_lock()
    if lock_fd is None:
        return 0  # another service runs: this one is the duplicate
    _name_holder(lock_fd)
    log_fd = _open_log()
    if log_fd is not None and not os.isatty(2):
        os.dup2(log_fd, 1)
        os.dup2(log_fd, 2)
    with contextlib.suppress(OSError):
        (paths.service_dir() / STOPPING_NAME).unlink()
    try:
        listen = _bind(sock_path)
    except OSError as exc:
        log(f"cannot bind {sock_path}: {exc}")
        return 1
    bound = os.stat(sock_path)
    registry = Registry(paths.registry_path(), ttl=_env_float(TTL_ENV, HEARTBEAT_TTL_S))
    service = Service(
        registry=registry,
        grace_s=_env_float(GRACE_ENV, GRACE_S),
        discovery_s=_env_float(DISCOVERY_ENV, DISCOVERY_S),
        legacy=LegacyDoor(),
    )
    try:
        reason = asyncio.run(service.run(listen))
    except Exception as exc:  # noqa: BLE001
        log(f"crashed: {exc!r}")
        reason = "crash"
    finally:
        # Unlink only OUR socket, and before the lock goes (process exit): a new
        # service can bind only after that, so this never removes its socket.
        with contextlib.suppress(OSError):
            st = os.stat(sock_path)
            if (st.st_dev, st.st_ino) == (bound.st_dev, bound.st_ino):
                os.unlink(sock_path)
        with contextlib.suppress(OSError):
            (paths.service_dir() / STOPPING_NAME).unlink()
    log(f"exited ({reason})")
    return 0 if reason != "crash" else 1


__all__ = ["LegacyDoor", "PidWatcher", "Registry", "Service", "peer_uid", "run_service"]
