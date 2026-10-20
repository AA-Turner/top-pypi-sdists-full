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
import time
from collections.abc import Callable
from pathlib import Path

from . import paths
from .actions import ActionManager
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
    need_int,
    need_owner,
    need_str,
    parse_request,
    result,
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
#: The log is cut over to `service.log.1` at start once it passes this.
MAX_LOG_BYTES = 256 * 1024
#: Created while the service stops, so a new instance that finds the lock still
#: held waits for it instead of exiting (the old one is about to let go).
STOPPING_NAME = "service.stopping"
STOPPING_WAIT_S = 3.0


_session_env_names: frozenset | None = None


def session_env_names() -> frozenset:
    """Every coding agent's session-id variable, from the harness registry
    (light: stdlib only), which a request's `context` may set
    (`protocol.CONTEXT_ENV`). Read once; empty if the registry cannot be."""
    global _session_env_names
    if _session_env_names is None:
        try:
            from probe.harness import get_registry

            _session_env_names = frozenset(h.session_env for h in get_registry().all() if h.session_env)
        except Exception as exc:  # noqa: BLE001 -- a context then just cannot name a session
            log(f"harness registry unreadable: {exc!r}")
            _session_env_names = frozenset()
    return _session_env_names


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
    def __init__(self, writer: asyncio.StreamWriter) -> None:
        self.writer = writer
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
    ) -> None:
        self.registry = registry
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
            daemon_session=self.registry.daemon_alive,
        )

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
        self._schedule_expiry()
        self.actions.load(self.watcher.watch)
        self.updater.attach(self._loop)
        self._server = await asyncio.start_unix_server(self._handle, sock=listen, limit=MAX_LINE_BYTES + 1)
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
        try:
            return await self._done
        finally:
            await self._shutdown()

    def _discovery_over(self) -> None:
        self._discovery_handle = None
        self._discovering_until = 0.0
        self.reevaluate()
        # No updates while discovering (X6): the registry is still filling up.
        self.updater.after_discovery()

    @property
    def discovering(self) -> bool:
        return time.monotonic() < self._discovering_until

    def holds(self) -> bool:
        """Is anything keeping the service alive (plan D1, R3; API v1 "Alive")?
        A live session, a keep-alive client (the app's window), an action in
        progress, or an update cycle (for at most its hold)."""
        if self.registry.alive_count() > 0:
            return True
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
        self.updater.close()
        if not self._done.done():
            self._done.set_result(reason)

    async def _shutdown(self) -> None:
        for handle in (self._discovery_handle, self._grace_handle, self._expiry_handle):
            if handle is not None:
                handle.cancel()
        if self._server is not None:
            self._server.close()
        for conn in list(self.connections):
            with contextlib.suppress(Exception):
                await asyncio.wait_for(conn.writer.drain(), 0.2)
            with contextlib.suppress(Exception):
                conn.writer.close()
        if self.watcher is not None:
            self.watcher.close()
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
        conn = Connection(writer)
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
        reg = self.registry.register(sid, harness, mode, owner, generation)
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
        return await self.status_cache.get(need_context(params, session_env_names()), refresh=refresh, max_age=max_age)

    def _action_run(self, conn: Connection, params: dict) -> dict:
        if params.get("action") == Action.UPDATE:
            # Before the files it imports from are replaced (R2), as a cycle does.
            try:
                preload()
            except Exception as exc:  # noqa: BLE001 -- a person's Update still runs
                log(f"preload before the update action failed: {exc!r}")
        return self.actions.run(params, need_context(params, session_env_names()))

    def _check_now(self, conn: Connection, params: dict) -> dict:
        trigger = params.get("trigger", CheckTrigger.CLI)
        if trigger not in CHECK_TRIGGERS:
            raise invalid_params(f"trigger must be one of {sorted(CHECK_TRIGGERS)}")
        return self.updater.check_now(trigger)


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


def _take_lock() -> int | None:
    """The life-long `service.lock`, or None when another service holds it."""
    import fcntl

    fd = os.open(paths.lock_path(), os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    deadline = None
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd
        except BlockingIOError:
            # A service that is stopping lets go within moments; one that runs
            # does not, and then this instance is the duplicate and leaves.
            if not (paths.service_dir() / STOPPING_NAME).exists():
                os.close(fd)
                return None
            if deadline is None:
                deadline = time.monotonic() + STOPPING_WAIT_S
            if time.monotonic() >= deadline:
                os.close(fd)
                return None
            time.sleep(0.05)


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


__all__ = ["PidWatcher", "Registry", "Service", "peer_uid", "run_service"]
