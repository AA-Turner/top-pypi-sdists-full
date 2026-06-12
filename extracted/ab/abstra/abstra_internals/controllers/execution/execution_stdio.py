import math
import socket
import struct
import sys
import threading
from typing import Callable, List, Literal, Optional, Union

import flask_sock

from abstra_internals.controllers.main import MainController
from abstra_internals.controllers.sdk.sdk_context import (
    SDKContextStore,
)
from abstra_internals.entities.execution import Execution
from abstra_internals.env_masker import GLOBAL_MASKER
from abstra_internals.environment import (
    IS_PRODUCTION,
    WORKER_LOG_TO_QUEUE,
    web_editor_uses_db,
)
from abstra_internals.interface.sdk.user_exceptions import ExecutionNotFound
from abstra_internals.logger import AbstraLogger

# A WS client that cannot accept a send within this window is treated as stuck
# and dropped, so it cannot block broadcast() for every other listener. Applied
# via setsockopt(SO_SNDTIMEO) — NOT socket.settimeout, which also bounds recv();
# simple_websocket's reader thread blocks on recv() forever to detect close, so
# settimeout would tear the WS down. On a blocking socket the kernel returns
# EAGAIN on expiry (OSError(EWOULDBLOCK), not socket.timeout); broadcast()'s
# `except Exception` catches it either way. register() is reached only from the
# editor stdio route, never in abstra-server/abstra-worker.
#
# Note: simple_websocket's send() is a single sock.send() (not sendall) and
# ignores the returned count, so a partial write near the deadline returns
# without raising — a stuck client may receive one corrupted frame before being
# dropped on the next broadcast. Bounded and self-healing (it only affects the
# already-stuck client); a full fix would require patching simple_websocket.
_SEND_TIMEOUT_SECONDS = 2.0
# Pack into struct timeval (tv_sec, tv_usec). Derive BOTH fields from the float
# so sub-second values stay honest: the naive int(seconds) packing would
# truncate e.g. 0.5 to tv_sec=0/tv_usec=0, which the kernel reads as "no
# timeout" (block forever), silently reverting this fix. "ll" matches the editor
# pod's Linux x86_64 timeval (two 64-bit longs); register() never runs elsewhere.
_timeout_frac, _timeout_whole = math.modf(_SEND_TIMEOUT_SECONDS)
_SO_SNDTIMEO_VALUE = struct.pack(
    "ll", int(_timeout_whole), int(_timeout_frac * 1_000_000)
)


class BroadcastController:
    listeners: List[flask_sock.Server] = []
    _lock = threading.Lock()

    @classmethod
    def register(cls, listener: flask_sock.Server):
        # Bound only the *send* side of the underlying socket so a stuck listener
        # (TCP send buffer full because the client stopped acking) cannot block
        # broadcast() for every other listener. See the comment above
        # _SEND_TIMEOUT_SECONDS for why settimeout() is NOT used.
        try:
            sock = getattr(listener, "sock", None)
            if sock is not None:
                sock.setsockopt(
                    socket.SOL_SOCKET, socket.SO_SNDTIMEO, _SO_SNDTIMEO_VALUE
                )
        except Exception:
            # Defensive: exotic WSGI server / test double without a usable
            # setsockopt — register without the bound. broadcast()'s snapshot +
            # failure cleanup still survives whatever send() raises.
            pass
        with cls._lock:
            cls.listeners.append(listener)

    @classmethod
    def unregister(cls, listener: flask_sock.Server):
        with cls._lock:
            if listener in cls.listeners:
                cls.listeners.remove(listener)

    @classmethod
    def _reclaim(cls, listener: flask_sock.Server) -> None:
        # Half-close the socket so simple_websocket's reader thread (blocked in
        # recv()) wakes on EOF, exits and calls sock.close() itself — freeing the
        # thread+fd instead of leaking until TCP keepalive. shutdown(), not
        # close(): close() cannot reliably unblock a recv() in another thread on
        # Linux, and listener.close() would issue another blocking send through
        # the wedged socket. Defensive for test doubles / already-dead sockets.
        try:
            sock = getattr(listener, "sock", None)
            if sock is not None:
                sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass

    @classmethod
    def broadcast(cls, *, msg: str):
        # Lock-free no-op in abstra-server/abstra-worker, which never register a
        # listener. The racy read is benign: a listener registering in this
        # window simply catches the next broadcast (same snapshot semantics as
        # below).
        if not cls.listeners:
            return

        # Snapshot under the lock so concurrent register/unregister cannot race
        # with the iteration below.
        with cls._lock:
            snapshot = list(cls.listeners)

        # Send outside the lock: send() can block on the underlying socket, and
        # holding cls._lock during IO would pile register/unregister up behind a
        # slow listener.
        failed: List[flask_sock.Server] = []
        for listener in snapshot:
            try:
                listener.send(msg)
            except Exception:
                failed.append(listener)

        if not failed:
            return

        # Reclaim outside the lock (shutdown() may do IO): freeing each wedged
        # socket lets its reader thread exit instead of leaking thread+fd.
        for listener in failed:
            cls._reclaim(listener)

        # Apply removals under the lock. The "in cls.listeners" guard makes this
        # idempotent if a listener was already unregistered between the snapshot
        # and now.
        with cls._lock:
            for listener in failed:
                if listener in cls.listeners:
                    cls.listeners.remove(listener)

    def __init__(
        self,
        *,
        main_controller: MainController,
        sys_stdout_write,
        sys_stderr_write,
    ):
        self.execution_logs_repository = main_controller.execution_logs_repository
        self.execution_repository = main_controller.execution_repository
        self.sys_stdout_write = sys_stdout_write
        self.sys_stderr_write = sys_stderr_write

    def patched_stderr_write(self, raw: Union[str, bytearray]) -> int:
        return self._handle_stdio("stderr", self.sys_stderr_write, raw)

    def patched_stdout_write(self, raw: Union[str, bytearray]) -> int:
        return self._handle_stdio("stdout", self.sys_stdout_write, raw)

    def _handle_stdio(
        self,
        std_type: Literal["stdout", "stderr"],
        sys_write: Callable,
        raw: Union[str, bytearray],
    ):
        text = raw.decode("utf-8") if not isinstance(raw, str) else raw

        try:
            execution = self.get_current_execution()

            text = self.mask(text)
            text = self.tag(text, execution)

            self.send_stdio(execution, std_type, text)
        except Exception as e:
            AbstraLogger.capture_exception(e)
        finally:
            sys_write(text)
            sys.stdout.flush()
            return len(text)

    def get_current_execution(self) -> Optional[Execution]:
        try:
            return SDKContextStore.get_execution()
        except ExecutionNotFound:
            return None

    def send_stdio(
        self,
        execution: Optional[Execution],
        std_type: Literal["stderr", "stdout"],
        text: str,
    ):
        if not execution:
            return

        # Don't persist/stream whitespace-only writes: print() emits the content
        # and its trailing "\n" as SEPARATE writes (and arg separators too), so
        # each print would otherwise create a junk "\n"/" " log row. The frontend
        # already discards whitespace-only log messages (services/log.ts: it
        # returns early when msg.log.trim() === ''), rendering one entry per
        # event, so skipping these here changes nothing visible — it only keeps
        # the spurious rows out of storage. The real stdout echo (sys_write in
        # _handle_stdio) is unaffected, so terminal/Docker output is unchanged.
        if not text.strip():
            return

        self.execution_logs_repository.insert_stdio(
            execution.id, execution.stage_id, std_type, text
        )

        # Persistence above always runs. The RabbitMQ broadcast below is the
        # legacy live-streaming path; on the DB path the editor poller streams
        # logs instead, so it is bypassed (the env var is ignored in DB mode).
        # Kept as explicit module-level reads (not the worker_logs_via_queue
        # helper) so existing tests can patch WORKER_LOG_TO_QUEUE here.
        if WORKER_LOG_TO_QUEUE and not web_editor_uses_db():
            self._send_stdio_via_queue(execution, std_type, text)

    def _send_stdio_via_queue(
        self,
        execution: Execution,
        std_type: Literal["stderr", "stdout"],
        text: str,
    ):
        from abstra_internals.controllers.execution.execution_conn import (
            get_stdio_buffer,
        )

        buffer = get_stdio_buffer()
        if buffer is None:
            return

        try:
            buffer.add(
                {
                    "type": std_type,
                    "log": text,
                    "execution_id": execution.id,
                    "stage_id": execution.stage_id,
                }
            )
        except Exception:
            pass

    def mask(self, raw: str) -> str:
        if IS_PRODUCTION:
            return GLOBAL_MASKER.mask(raw)
        return raw

    def tag(self, raw: str, execution: Optional[Execution]) -> str:
        if not execution:
            return raw

        if not raw.strip():
            return raw

        short_id = execution.id.split(sep="-")[0]
        prefix = f"[RUN {short_id}] "

        lines = raw.splitlines(keepends=True)
        if len(lines) <= 1:
            return f"{prefix}{raw}"

        tagged_lines = []
        for line in lines:
            tagged_lines.append(f"{prefix}{line}")

        return "".join(tagged_lines)
