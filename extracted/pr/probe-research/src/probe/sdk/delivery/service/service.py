"""DeliveryService: the Probe service a training process's SDK starts where it must (no machine service,
or an older one: plan D9, D28), `python -I -m probe.sdk.delivery.service`. Public, pure Python: it
answers `service.hello`, `service.status`, `service.stop` and the SDK's methods (`SdkMethods`), and
nothing of the machine's upkeep (no updater, timers, recorders, keeper units or hooks)."""

from __future__ import annotations

import asyncio
import contextlib
import os
import signal
import sys
import time

from probe.foundation.service_api import paths
from probe.foundation.service_api.params import need_bool, need_choice, need_str
from probe.foundation.service_api.vocabularies import (
    CLIENTS,
    Client,
    DELIVERY_CAPS,
    RefusedReason,
    ServiceRole,
    State,
    StopReason,
)
from probe.foundation.service_api.wire import (
    API_VERSION,
    FDS_FIELD,
    MAX_LINE_BYTES,
    OUTBOX_JOURNALS,
    ErrorCode,
    Method,
    RpcError,
    error,
    invalid_params,
    parse_request,
    result,
)

from . import callers
from .connection import Connection
from .fds import close_fds, need_fd_count, receive_fds
from .methods import SdkMethods

#: No keep-alive client this long (an SDK holds one while its process lives): the service exits.
GRACE_S = 5.0
#: After its start, it never idles out this long: the SDK that started it connects meanwhile.
DISCOVERY_S = 10.0
#: It looks this often for a machine install to hand over to (M1), and hands over only once no
#: request came for as long.
HANDOVER_CHECK_S = 30.0
#: Signalled while its clients hold it (a Slurm job's SIGTERM reaches every process of the job at
#: once, H2), it serves their closes at most this long (Slurm's KillWait default).
SIGNAL_GRACE_S = 30.0
#: Test-only overrides (the machine service reads the same, `service/server/main.py`).
GRACE_ENV = "PROBE_SERVICE_GRACE_S"
DISCOVERY_ENV = "PROBE_SERVICE_DISCOVERY_S"
#: A stopping service's marker (the machine service's `lifecycle.STOPPING_NAME`): a start that
#: finds the lock held waits for it to go instead of leaving as the duplicate.
STOPPING_NAME = "service.stopping"
STOPPING_WAIT_S = 5.0
#: A stopping service finishes the `api.call`s and `files.hash` jobs it took at most this long; its
#: socket and lock are let go first, so the next service starts meanwhile.
IN_FLIGHT_WAIT_S = 60.0
#: The log is cut over to `service.log.1` at start once it passes this.
MAX_LOG_BYTES = 256 * 1024


def _has_cli_install() -> bool:
    """This machine has a CLI install (`start.get_cli_python`): its machine service serves here.
    Blocking (a small read): a thread, or the handover's rare look."""
    from probe.foundation.service_api.start import get_cli_python

    return get_cli_python() is not None


def _forget_start(pid: int) -> None:
    """Take this service's own spawn out of `starts.json` (`start.forget_start`; never raises)."""
    from probe.foundation.service_api.start import forget_start

    forget_start(pid)


def _record_stop(reason: str, version: str) -> None:
    """Say why this service stopped in `last-stop.json` (`stop_record.record_stop`; never raises)."""
    from probe.foundation.service_api.stop_record import record_stop

    record_stop(reason, version)


def log(message: str) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with contextlib.suppress(OSError, ValueError):
        sys.stderr.write(f"[{stamp}] probe-service[{os.getpid()}]: {message}\n")
        sys.stderr.flush()


def get_version() -> str:
    try:
        from probe import __version__

        return str(__version__)
    except Exception:  # noqa: BLE001 -- never a reason not to serve
        return "0.0.0.dev0"


class DeliveryService:
    def __init__(self, *, grace_s: float = GRACE_S, discovery_s: float = DISCOVERY_S,
                 expected_uid: int | None = None, release=lambda: None) -> None:
        #: Lets go of this service's socket and lock (`run_delivery_service`): the first thing a
        #: stopping service does, so the next one starts while this one finishes what it took.
        self.release = release
        self.grace_s = grace_s
        self.discovery_s = discovery_s
        self.expected_uid = os.getuid() if expected_uid is None else expected_uid
        self.version = get_version()
        self.pid = os.getpid()
        self.started_at = time.time()
        #: The SDK's methods; a caller this service cannot rule out being more confined is fenced
        #: (D25, `callers.is_confined`, as the machine service's).
        self.sdk = SdkMethods(log=log, is_fenced=callers.is_confined_unlike_this_service)
        self.connections: set[Connection] = set()
        self.stop_reason: str | None = None
        self.state = State.DISCOVERING
        #: When the last request came (monotonic): it hands over only when quiet (M1).
        self.last_request_at = time.monotonic()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._done: asyncio.Future | None = None
        self._server: asyncio.AbstractServer | None = None
        self._grace_handle: asyncio.TimerHandle | None = None
        self._signal_handle: asyncio.TimerHandle | None = None
        self._discovering_until = 0.0
        self._handlers = {
            Method.HELLO: self._answer_hello, Method.STATUS: self._answer_status, Method.STOP: self._answer_stop,
            **self.sdk.get_handlers(),
        }

    # -- lifecycle --------------------------------------------------------------------------

    async def run(self, listen, *, on_ready=None) -> str:
        """Serve on the bound socket `listen` until idle, stopped or signalled; why it stopped."""
        self._loop = asyncio.get_running_loop()
        self._done = self._loop.create_future()
        self._discovering_until = time.monotonic() + self.discovery_s
        self._server = await asyncio.start_unix_server(self._handle, sock=listen, limit=MAX_LINE_BYTES + 1)
        self._loop.call_later(self.discovery_s, self._update_state)
        self._loop.call_later(HANDOVER_CHECK_S, self._check_handover)
        with contextlib.suppress(NotImplementedError, RuntimeError, ValueError):
            for name in ("SIGTERM", "SIGINT", "SIGHUP"):
                self._loop.add_signal_handler(getattr(signal, name), self._handle_signal)
        log(f"serving (api {API_VERSION}, version {self.version}, role {ServiceRole.DELIVERY}, "
            f"grace {self.grace_s}s, discovery {self.discovery_s}s)")
        if on_ready is not None:
            on_ready()
        # This box's runs, watched again when an earlier service died without handing them off.
        self._loop.run_in_executor(None, self.sdk.background.resume_watcher)
        try:
            return await self._done
        finally:
            await self._shutdown()

    def stop(self, reason: str) -> None:
        if self.stop_reason is not None or self._done is None:
            return
        self.stop_reason = reason
        self.sdk.is_stopping = True
        with contextlib.suppress(OSError):
            (paths.service_dir() / STOPPING_NAME).touch()
        # Its stop on record, as the machine service's: the service after it reads no crash (`watch.last_run`).
        _record_stop(reason, self.version)
        if reason in (StopReason.IDLE, StopReason.STOP):
            # A stop on purpose is no start for `ensure` to wait on or back off from (the machine
            # service's rule): a step aside's caller starts the machine service at once.
            _forget_start(self.pid)
        log(f"stopping ({reason})")
        if not self._done.done():
            self._done.set_result(reason)

    async def _shutdown(self) -> None:
        if self._server is not None:
            self._server.close()
        self.release()
        deadline = time.monotonic() + IN_FLIGHT_WAIT_S
        while self.sdk.count_in_flight() > 0 and self.connections and time.monotonic() < deadline:
            await asyncio.sleep(0.05)  # what it took, answered (H-3: a step aside finishes its work)
        from .background.background import FLUSH_S

        await asyncio.to_thread(self.sdk.close, FLUSH_S)
        for connection in list(self.connections):
            with contextlib.suppress(Exception):
                connection.writer.close()

    def _is_held(self) -> bool:
        return any(connection.keepalive for connection in self.connections)

    def _update_state(self) -> None:
        if self.stop_reason is not None or self._loop is None:
            return
        if time.monotonic() < self._discovering_until:
            return
        if self._is_held():
            self.state = State.RUNNING
            if self._grace_handle is not None:
                self._grace_handle.cancel()
                self._grace_handle = None
            return
        if self._signal_handle is not None:
            self.stop(StopReason.SIGNAL)  # signalled, and its clients let go: nothing left to serve
            return
        if self._grace_handle is None:
            self.state = State.GRACE
            self._grace_handle = self._loop.call_later(self.grace_s, self._end_grace)

    def _end_grace(self) -> None:
        self._grace_handle = None
        if self._is_held():
            self._update_state()
            return
        if self.sdk.count_in_flight() > 0:
            # An `api.call` or `files.hash` still running: its answer first, then another grace.
            self._grace_handle = self._loop.call_later(self.grace_s, self._end_grace)
            return
        self.stop(StopReason.IDLE)

    def _handle_signal(self) -> None:
        """SIGTERM, SIGINT or SIGHUP: stop. Still held by its clients, it first serves their closes
        (H2): it stops once they let go or after SIGNAL_GRACE_S; a second signal stops it at once."""
        if self._signal_handle is not None or not self._is_held():
            self.stop(StopReason.SIGNAL)
            return
        log(f"signalled: serving the clients' closes first (at most {SIGNAL_GRACE_S:g}s)")
        self._signal_handle = self._loop.call_later(SIGNAL_GRACE_S, self.stop, StopReason.SIGNAL)

    def _check_handover(self) -> None:
        """M1: it steps aside, once quiet, where its root has a machine install (`runtime.json`),
        so the next `ensure` starts or activates the machine service there."""
        if self.stop_reason is not None or self._loop is None:
            return
        if self._is_quiet() and _has_cli_install():
            log("a machine install is here: this delivery service hands over to its service")
            self.stop(StopReason.IDLE)
            return
        self._loop.call_later(HANDOVER_CHECK_S, self._check_handover)

    def _is_quiet(self) -> bool:
        """No request lately, nothing in flight, no telemetry queued."""
        return time.monotonic() - self.last_request_at >= HANDOVER_CHECK_S and self.sdk.count_in_flight() == 0

    # -- connections ------------------------------------------------------------------------

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        sock = writer.get_extra_info("socket")
        uid = callers.get_peer_uid(sock) if sock is not None else None
        if uid is not None and uid != self.expected_uid:
            log(f"refused a connection from uid {uid}")
            writer.close()
            return
        connection = Connection(writer, callers.get_peer_pid(sock) if sock is not None else None)
        self.connections.add(connection)
        try:
            while self.stop_reason is None:
                try:
                    line = await reader.readuntil(b"\n")
                except asyncio.IncompleteReadError:
                    break
                except asyncio.LimitOverrunError:
                    await connection.send(
                        error(None, RpcError(ErrorCode.INVALID_REQUEST, "invalid request: line over 1 MiB")))
                    break
                except (ConnectionError, OSError):
                    break
                if line.strip():
                    await connection.send(await self.dispatch(connection, line))
        finally:
            self.connections.discard(connection)
            with contextlib.suppress(Exception):
                writer.close()
            if connection.keepalive:
                self._update_state()

    async def dispatch(self, connection: Connection, line: bytes) -> dict:
        self.last_request_at = time.monotonic()
        try:
            id_, method, parameters = parse_request(line)
        except RpcError as exc:
            id_ = (exc.data or {}).get("id")
            exc.data = None
            return error(id_, exc)
        if not connection.hello and method != Method.HELLO:
            return error(id_, RpcError(ErrorCode.HELLO_REQUIRED, "hello_required: send service.hello first"))
        connection.request_id = id_
        handler = self._handlers.get(method)
        if (handler is None or (method == Method.HELLO and parameters.get("client") != Client.SDK)) \
                and await asyncio.to_thread(_has_cli_install):
            # H-3: a CLI, a hook or the app asks, and this machine has a CLI install: the machine
            # service is theirs. This one steps aside at once (its work taken finishes first).
            log(f"{method} from a {parameters.get('client') or 'client'} where a CLI is installed: "
                "this delivery service steps aside for the machine service")
            self.stop(StopReason.IDLE)
            # The caller retries against the machine service the next `ensure` starts (the CLI shim
            # does on `caller_gone`, as for any stopping service).
            return error(id_, RpcError(
                ErrorCode.REFUSED, "refused: the delivery service steps aside for this machine's service; connect again",
                {"reason": RefusedReason.CALLER_GONE},
            ))
        if handler is None:
            return error(id_, RpcError(
                ErrorCode.REFUSED, f"refused: a delivery service does not run {method}",
                {"reason": RefusedReason.ROLE, "role": ServiceRole.DELIVERY},
            ))
        try:
            if FDS_FIELD in parameters:
                count = need_fd_count(method, parameters[FDS_FIELD])
                try:
                    connection.fds = await receive_fds(connection.writer, id_, count)
                except (ConnectionError, TimeoutError, asyncio.TimeoutError) as exc:
                    return error(id_, RpcError(
                        ErrorCode.INVALID_PARAMS, f"invalid params: fds: {type(exc).__name__}: {exc}"))
            value = handler(connection, parameters)
            if asyncio.iscoroutine(value):
                value = await value
        except RpcError as exc:
            return error(id_, exc)
        except Exception as exc:  # noqa: BLE001 -- one bad request never stops the service
            log(f"internal error in {method}: {type(exc).__name__}: {exc}")
            return error(id_, RpcError(ErrorCode.REFUSED, "internal error", {"reason": RefusedReason.INTERNAL}))
        finally:
            close_fds(connection.fds)
        return result(id_, value)

    # -- hello, status, stop ----------------------------------------------------------------

    def _answer_hello(self, connection: Connection, parameters: dict) -> dict:
        client = need_choice(parameters, "client", CLIENTS)
        need_str(parameters, "client_version", max_len=64)
        api = parameters.get("api")
        if not isinstance(api, int) or isinstance(api, bool):
            raise invalid_params("api must be an integer")
        if api != API_VERSION:
            raise RpcError(ErrorCode.UNSUPPORTED_API, f"unsupported_api: this service speaks api {API_VERSION}",
                           {"supported": [API_VERSION]})
        connection.hello = True
        connection.client = client
        connection.keepalive = need_bool(parameters, "keepalive")
        self._update_state()
        return {
            "service_version": self.version,
            "api": API_VERSION,
            "pid": self.pid,
            "started_at": self.started_at,
            "state": self.state,
            "caps": sorted(DELIVERY_CAPS),
            "env": sys.prefix,
            "role": ServiceRole.DELIVERY,
            "outbox_journals": list(OUTBOX_JOURNALS),
        }

    def _answer_status(self, connection: Connection, parameters: dict) -> dict:
        return {
            "service_version": self.version,
            "pid": self.pid,
            "started_at": self.started_at,
            "state": self.state,
            "role": ServiceRole.DELIVERY,
            "clients": len(self.connections),
            **self.sdk.public(),
        }

    def _answer_stop(self, connection: Connection, parameters: dict) -> dict:
        self._loop.call_soon(self.stop, StopReason.STOP)
        return {"stopping": True}


# -- process entry ------------------------------------------------------------------------


def run_delivery_service() -> int:
    """`python -m probe.sdk.delivery.service`: one service per machine folder (its life-long lock);
    exits 0 when idle or as the duplicate."""
    try:
        sock_path = paths.ensure_dirs()
    except OSError as exc:
        log(f"cannot use {paths.service_dir()}: {exc}")
        return 1
    lock_fd = _take_lock()
    if lock_fd is None:
        return 0  # another service runs here: this one is the duplicate
    # Every process this service runs is under it: an SDK there sends its own HTTP (plan D10).
    os.environ[paths.SERVICE_ROLE_ENV] = ServiceRole.DELIVERY
    _write_holder(lock_fd)
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
    released: list = []

    def release() -> None:
        """Unlink only OUR socket, then let the lock go: a new service binds only after (L-5: before
        waiting on what this one still finishes, never after)."""
        if released:
            return
        released.append(True)
        with contextlib.suppress(OSError):
            st = os.stat(sock_path)
            if (st.st_dev, st.st_ino) == (bound.st_dev, bound.st_ino):
                os.unlink(sock_path)
        with contextlib.suppress(OSError):
            (paths.service_dir() / STOPPING_NAME).unlink()
        with contextlib.suppress(OSError):
            os.close(lock_fd)

    server = DeliveryService(grace_s=_get_float(GRACE_ENV, GRACE_S), discovery_s=_get_float(DISCOVERY_ENV, DISCOVERY_S),
                             release=release)
    try:
        reason = asyncio.run(server.run(listen))
    except Exception as exc:  # noqa: BLE001
        log(f"crashed: {exc!r}")
        reason = "crash"
    finally:
        release()
    log(f"exited ({reason})")
    return 0 if reason != "crash" else 1


def _take_lock() -> int | None:
    """The life-long `service.lock`, or None when another service holds it (one that is stopping
    lets go within moments: waited for)."""
    fd = os.open(paths.lock_path(), os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    deadline = time.monotonic() + STOPPING_WAIT_S
    while not paths.try_lock(fd):
        if not (paths.service_dir() / STOPPING_NAME).exists() or time.monotonic() >= deadline:
            os.close(fd)
            return None
        time.sleep(0.05)
    return fd


def _write_holder(fd: int) -> None:
    """`<pid> <start time>` in the lock file this service holds (the machine's guard reads it)."""
    from probe.foundation.service_api import procid

    with contextlib.suppress(OSError):
        os.ftruncate(fd, 0)
        os.lseek(fd, 0, os.SEEK_SET)
        os.write(fd, f"{os.getpid()} {procid.start_time(os.getpid()) or ''}\n".encode())


def _open_log() -> int | None:
    path = paths.log_path()
    with contextlib.suppress(OSError):
        if path.stat().st_size > MAX_LOG_BYTES:
            os.replace(path, path.with_name(path.name + ".1"))
    try:
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
    except OSError:
        return None


def _bind(path):
    """Bind the socket 0600 (this service holds the lock, so anything there is stale)."""
    import socket

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


def _get_float(name: str, default: float) -> float:
    try:
        return float(os.environ[name])
    except (KeyError, ValueError):
        return default
