"""JSON-RPC over byte streams with Content-Length framing (LSP-style).

Shared by both sides of the linter sidecar IPC: the editor (client.py) and the
child process (server.py). Same framing as the pyrefly LSP integration
(controllers/language_server.py), hardened for this use case:

- pending requests FAIL IMMEDIATELY when the connection dies (EOF/corruption)
  instead of waiting for their full timeout;
- bidirectional: either side can issue requests while others are in flight
  (matched by id); incoming requests/notifications go to a dispatch callback;
- writes are serialized under a lock so concurrent frames never interleave.
"""

import json
import threading
from typing import Any, Callable, Dict, Optional

PROTOCOL_VERSION = 1

_HEADER_TERMINATOR = b"\r\n\r\n"
_CONTENT_LENGTH = "content-length"


class ProtocolError(Exception):
    """The byte stream does not contain a well-formed frame."""


class ConnectionClosed(Exception):
    """The peer is gone (EOF, broken pipe, or corrupted stream)."""


class RpcError(Exception):
    """The peer answered with a JSON-RPC error response."""

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class StopPump(Exception):
    """Raised by a dispatch callback to end pump() cleanly (e.g. shutdown)."""


def encode_frame(msg: dict) -> bytes:
    body = json.dumps(msg).encode("utf-8")
    header = ("Content-Length: %d\r\n\r\n" % len(body)).encode("ascii")
    return header + body


def _read_exactly(stream, n: int) -> bytes:
    chunks = []
    remaining = n
    while remaining > 0:
        chunk = stream.read(remaining)
        if not chunk:
            break
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def read_frame(stream) -> Optional[dict]:
    """Read one framed JSON message.

    Returns None on clean EOF (no bytes before the next frame). Raises
    ProtocolError on any malformed or truncated frame.
    """
    header = b""
    while _HEADER_TERMINATOR not in header:
        byte = stream.read(1)
        if not byte:
            if not header:
                return None
            raise ProtocolError("EOF inside frame header: %r" % header[:128])
        header += byte
        if len(header) > 4096:
            raise ProtocolError("frame header too large / missing terminator")

    content_length = None
    for line in header.split(b"\r\n"):
        if b":" not in line:
            continue
        name, _, value = line.partition(b":")
        if name.decode("ascii", "replace").strip().lower() == _CONTENT_LENGTH:
            try:
                content_length = int(value.strip())
            except ValueError:
                raise ProtocolError("invalid Content-Length: %r" % value[:64])
            break
    if content_length is None or content_length < 0:
        raise ProtocolError("missing Content-Length header: %r" % header[:128])

    body = _read_exactly(stream, content_length)
    if len(body) != content_length:
        raise ProtocolError(
            "EOF inside frame body (%d of %d bytes)" % (len(body), content_length)
        )
    try:
        msg = json.loads(body)
    except ValueError:
        raise ProtocolError("frame body is not valid JSON: %r" % body[:128])
    if not isinstance(msg, dict):
        raise ProtocolError("frame body is not a JSON object")
    return msg


class _Pending:
    __slots__ = ("event", "result", "error", "callback")

    def __init__(self):
        self.event = threading.Event()
        self.result: Any = None
        self.error: Optional[Exception] = None
        # Runs on the PUMP thread, before the waiter wakes — gives callers a
        # hook that observes results in pipe order (the client uses it to
        # apply mirror updates without cross-thread reordering).
        self.callback: Optional[Callable[[Any], None]] = None


class RpcFuture:
    """Handle for an in-flight request issued with request_async()."""

    def __init__(self, channel: "RpcChannel", rid: int, pending: _Pending, method: str):
        self._channel = channel
        self._rid = rid
        self._pending = pending
        self._method = method

    def wait(self, timeout: Optional[float] = None) -> Any:
        if not self._pending.event.wait(timeout):
            with self._channel._state_lock:
                self._channel._pending.pop(self._rid, None)
            raise TimeoutError(
                "no response for %r after %.1fs" % (self._method, timeout or -1.0)
            )
        if self._pending.error is not None:
            raise self._pending.error
        return self._pending.result


class RpcChannel:
    """One endpoint of a bidirectional JSON-RPC link over binary streams."""

    def __init__(self, reader, writer):
        self._reader = reader
        self._writer = writer
        self._write_lock = threading.Lock()
        self._state_lock = threading.Lock()
        self._pending: Dict[int, _Pending] = {}
        self._next_id = 0
        self._closed = False

    # ── outgoing ────────────────────────────────────────────────

    def _write_frame(self, msg: dict) -> None:
        data = encode_frame(msg)
        try:
            with self._write_lock:
                self._writer.write(data)
                self._writer.flush()
        except Exception as e:
            self._shutdown_pending()
            raise ConnectionClosed("write to peer failed: %s" % e) from e

    def request_async(
        self,
        method: str,
        params: Optional[dict] = None,
        on_result: Optional[Callable[[Any], None]] = None,
    ) -> RpcFuture:
        with self._state_lock:
            if self._closed:
                raise ConnectionClosed("channel is closed")
            self._next_id += 1
            rid = self._next_id
            pending = _Pending()
            pending.callback = on_result
            self._pending[rid] = pending

        msg = {"jsonrpc": "2.0", "id": rid, "method": method}
        if params is not None:
            msg["params"] = params
        try:
            self._write_frame(msg)
        except ConnectionClosed:
            with self._state_lock:
                self._pending.pop(rid, None)
            raise
        return RpcFuture(self, rid, pending, method)

    def request(
        self,
        method: str,
        params: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        return self.request_async(method, params).wait(timeout)

    def notify(self, method: str, params: Optional[dict] = None) -> None:
        msg: dict = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self._write_frame(msg)

    def respond(self, req_id: Any, result: Any) -> None:
        self._write_frame({"jsonrpc": "2.0", "id": req_id, "result": result})

    def respond_error(self, req_id: Any, message: str, code: int = -32603) -> None:
        self._write_frame(
            {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": code, "message": message},
            }
        )

    # ── incoming ────────────────────────────────────────────────

    def pump(self, dispatch: Callable[[dict], None]) -> None:
        """Blocking read loop.

        Responses are resolved internally (matched by id; unknown ids are
        dropped). Every other message — requests and notifications — goes to
        ``dispatch``. Returns on clean EOF or when dispatch raises StopPump;
        re-raises ProtocolError on stream corruption. In every exit path all
        pending requests are failed with ConnectionClosed so no caller is left
        waiting for a full timeout.
        """
        try:
            while True:
                msg = read_frame(self._reader)
                if msg is None:
                    return
                if "id" in msg and "method" not in msg:
                    self._resolve(msg)
                    continue
                try:
                    dispatch(msg)
                except StopPump:
                    return
                except Exception:
                    # A broken dispatch must not kill the connection; the
                    # peer's request times out / is retried at its layer.
                    continue
        finally:
            self._shutdown_pending()

    def _resolve(self, msg: dict) -> None:
        with self._state_lock:
            pending = self._pending.pop(msg["id"], None)
        if pending is None:
            return  # late response after timeout — drop
        if "error" in msg:
            error = msg.get("error") or {}
            pending.error = RpcError(
                error.get("code", -32603), str(error.get("message", "unknown error"))
            )
        else:
            pending.result = msg.get("result")
            if pending.callback is not None:
                try:
                    pending.callback(pending.result)
                except Exception:
                    pass
        pending.event.set()

    # ── teardown ────────────────────────────────────────────────

    def _shutdown_pending(self) -> None:
        with self._state_lock:
            self._closed = True
            pending = list(self._pending.values())
            self._pending.clear()
        for entry in pending:
            entry.error = ConnectionClosed("connection closed with request in flight")
            entry.event.set()

    def close(self) -> None:
        self._shutdown_pending()
        for stream in (self._writer, self._reader):
            try:
                stream.close()
            except Exception:
                pass
