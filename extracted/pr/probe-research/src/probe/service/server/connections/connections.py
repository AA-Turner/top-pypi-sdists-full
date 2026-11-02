"""serve a connection: peer uid, JSON-RPC dispatch through the method table, events to subscribers and the app."""

from __future__ import annotations

import asyncio
import contextlib
import os
import socket
import struct
import sys
from collections.abc import Callable

from ...actions import caller
from ....foundation.service_api import paths
from ....foundation.service_api.wire import (
    METHODS,
    ErrorCode,
    Method,
    RpcError,
    encode,
    error,
    event,
    parse_request,
    result)
from ....foundation.service_api.vocabularies import (
    SESSION_TOPICS,
    Client,
    RefusedReason,
    Topic,
    need_app_result)
from ...watch.incident import Family
from ...watch.bounds import log_traceback
from probe.service.server.lifecycle import _lifeboat_after
from probe.service.server.policy import (
    CONFINED_ANSWERS,
    DAEMON_HOST_METHOD,
    LOCAL_METHODS,
    METHOD_POLICY,
    Policy,
    log,
    screen,
)
#: A subscriber whose unread events pass this is dropped, not buffered forever.
MAX_SUBSCRIBER_BUFFER = 4 * 1024 * 1024


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


class Connection:
    def __init__(self, writer: asyncio.StreamWriter, peer_pid: int | None = None) -> None:
        self.writer = writer
        #: The connecting process, as the kernel says (plan D9); None where it cannot.
        self.peer_pid = peer_pid
        #: Its start time when it connected: the same process later, or not.
        self.peer_start: str | None = None
        #: `{pid, start_time}` once a registry change asked (`_caller_of`).
        self.peer_identity: dict | None = None
        #: In the order connections came (the service numbers them): the
        #: newest app connection is the one `app.check` goes to.
        self.serial = 0
        self.hello = False
        self.client: str | None = None
        self.keepalive = False
        self.topics: set = set()
        #: The sessions its SESSION_TOPICS subscription is for: sid -> the
        #: state folder it named (None: the default). Empty: every live one.
        self.sessions: dict = {}
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


class ConnectionsMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    # -- events --------------------------------------------------------------

    def _emit(self, topic: str, payload: dict) -> None:
        """To every subscriber of `topic`; `app.check` goes to one app only (`_send_app_check`)."""
        message = event(topic, payload)
        scoped = topic in SESSION_TOPICS
        for conn in list(self.connections):
            if topic in conn.topics and (not scoped or not conn.sessions or payload.get("sid") in conn.sessions):
                conn.send_nowait(message)

    def _updater_emit(self, topic: str, payload: dict) -> None:
        """The updater's events; at a cycle's end, the lifeboat's part (plan
        fool-proof-updates B1, B5): its `current/` copy becomes known-good
        when this cycle proved it, and what it did is reported."""
        self._emit(topic, payload)
        if topic == Topic.UPDATE_DONE and self._loop is not None:
            self._loop.run_in_executor(None, _lifeboat_after, dict(payload))
            self.statepost.look_for_acted()

    def _app_connections(self) -> list:
        """The desktop app's open connections (`service.hello` client `app`)."""
        return [c for c in self.connections if c.hello and c.client == Client.APP]

    def _app_listeners(self) -> list:
        """The app connections that take `app.check`."""
        return [c for c in self._app_connections() if Topic.APP_CHECK in c.topics]

    def _app_target(self) -> int | None:
        """The one app connection a hand-off goes to: the newest that takes `app.check`."""
        listeners = self._app_listeners()
        return max(c.serial for c in listeners) if listeners else None

    def _send_app_check(self, serial: int, payload: dict) -> bool:
        """`app.check` to that one connection; False when it is gone or closing."""
        for conn in self._app_listeners():
            if conn.serial == serial:
                return conn.send_nowait(event(Topic.APP_CHECK, payload))
        return False

    # -- connections ---------------------------------------------------------

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        sock = writer.get_extra_info("socket")
        uid = peer_uid(sock) if sock is not None else None
        if uid is not None and uid != self.expected_uid:
            log(f"refused a connection from uid {uid}")
            writer.close()
            return
        if paths.WINDOWS:
            from ....foundation.service_api import winpipe

            peer = winpipe.peer_of(writer)  # the pipe's DACL lets only this user in
        else:
            peer = caller.peer_pid(sock) if sock is not None else None
        conn = Connection(writer, peer)
        conn.serial = next(self._serials)
        if conn.peer_pid is not None and os.path.isdir("/proc/self"):
            # Linux: one /proc read. Elsewhere it would be a `ps` per connection
            # on the loop: there `_action_run` checks only that the pid exists.
            from ....foundation.service_api import procid

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
            if conn.client == Client.APP:
                # The app check it was handed and never reported is failed (due again).
                self.updater.app_gone(conn.serial)
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
        if method not in METHODS and method not in LOCAL_METHODS:
            return error(id_, RpcError(ErrorCode.UNKNOWN_METHOD, f"unknown method: {method}"))
        if METHOD_POLICY.get(method, Policy.WORK) == Policy.WORK:
            # Before the handler, whatever it checks itself: one rule for
            # every method that runs or stores work (`Policy.WORK`). Inline,
            # as the hook methods always checked: /proc reads on Linux, a
            # `sandbox_check` call on macOS, never a process.
            refusal = screen(conn.peer_pid, conn.peer_start)
            if refusal is not None:
                answer = CONFINED_ANSWERS.get(method)
                if answer is not None:
                    return result(id_, dict(answer))
                if refusal == RefusedReason.CALLER_GONE:
                    return error(id_, RpcError(
                        ErrorCode.REFUSED,
                        "refused: the process that opened this connection has exited; connect again",
                        {"reason": RefusedReason.CALLER_GONE},
                    ))
                return error(id_, RpcError(
                    ErrorCode.REFUSED, "refused: a caller in a sandbox", {"reason": RefusedReason.SANDBOXED}
                ))
        handler = self._handlers()[method]
        try:
            value = handler(conn, params)
            if asyncio.iscoroutine(value):
                value = await value
        except RpcError as exc:
            return error(id_, exc)
        except Exception as exc:  # noqa: BLE001 -- one bad request never stops the service
            self._internal_error(method, exc)
            return error(id_, RpcError(ErrorCode.REFUSED, "internal error", {"reason": RefusedReason.INTERNAL}))
        return result(id_, value)

    def _internal_error(self, method: str, exc: Exception) -> None:
        """A handler's own exception (a bug, answered `internal error`): logged
        with its traceback, and one event of `service_error` (plan B2)."""
        import traceback

        text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        log_traceback(log, f"{method} failed: {exc!r}", text, gate=self._tracebacks,
                      key=("request", method, type(exc).__name__))
        self.watch.note(Family.SERVICE_ERROR, "request_error", facts={
            "method": method, "type": type(exc).__name__, "traceback": text,
        })

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
            Method.UPDATE_APP_RESULT: lambda conn, params: self.updater.app_result(need_app_result(params)),
            Method.HOOKS_HOST: self._hooks_host,
            Method.HOOKS_RUN: self._hooks_run,
            Method.HOOKS_QUEUE: self._hooks_queue,
            Method.SESSION_RECORD: self._record,
            Method.SESSION_RECORDING: self._recording,
            Method.SESSION_FINISH: lambda conn, params: self.recorders.finish(params),
            Method.RECORDERS_FINISH: self._recorders_finish,
            DAEMON_HOST_METHOD: self._daemon_host,
            Method.RUN_HOLD: self._run_hold,
            Method.RUN_RELEASE: self._run_release,
            Method.MANIFEST_REFRESH: self._manifest_refresh,
            Method.MAILBOX_POST: self._mailbox_post,
            Method.MAILBOX_CLAIM: self._mailbox_claim,
            Method.MAILBOX_ANSWER: self._mailbox_answer,
            Method.DESKTOP_REQUEST: self._desktop_request,
            Method.OUTBOX_DRAIN: self._outbox_drain,
            Method.BOX_WATCH: self._box_watch,
            Method.TELEMETRY_SEND: self._telemetry_send,
            Method.STATUSLINE_REFRESH: self._statusline_refresh,
            Method.NOTES_SYNC: self._notes_sync,
            Method.IMPORT_START: self._import_start,
        }
