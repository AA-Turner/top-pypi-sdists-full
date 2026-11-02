"""
A robot's requests to its own worker on one WebSocket: its observations' posts, its
acts and its episodes' ends, written in the order they were handed over - its acts ahead - and answered on the same
connection. It is the one way a robot's requests reach its worker: there is no other to fall back on.

In one sentence: as the robot connects, one TLS connection is opened to its worker and upgraded (GET /stream, the
robot's secret and session on it), the upgrade's answer saying what the worker takes (X-Seq-Act-Formats) → each request
goes in pieces of PIECE_BYTES at most, msgpack {"i": its number, "m", "p", "h" (its first), "b": a part of its body, "more": true (all but its last)},
written by the one thread that owns the socket - an act's ahead of any other but the piece being written, the rest in
the order handed over, and only while the connection's unsent bytes are few (TCP_NOTSENT_LOWAT), so a backlog waits
here, where what is not written yet can still be left out (observe_stream: a policy that reads the latest alone) → the
worker serves each as the HTTP request it carries and answers it in pieces {"i", "s", "h", "b", "more"} - an
observation post that went well, with nothing: every answer names the last it served of them (X-Seq-Stream-Through),
each post up to it taken → an answer is an httpx.Response to its caller (StreamRouted), and a post is done when taken
or answered (observe_stream, which waits for none).

WHY one way alone: {the user 10-30: "no we want to delete, we dont want to support any previous version, we need to keep
clean"} and a second way is a second thing to go wrong: a robot whose loop observed before its worker's first answer
stayed on connections of its own for good, a teleop console refused it, and nothing said so (worker 4's dev check 10-30).
WHY one connection: an act and the observations before it went on connections of their own, and the act often reached
the worker first and waited - a session's first act about 4.5 round trips, an act waiting 8.6 s for a frame still on
its way (plan 111 section 2). On one connection what the robot handed over first arrives first.
WHY one thread owns the socket: a TLS connection read on one thread and written on another at once is no use OpenSSL
promises; one thread reads whatever comes and writes what is queued, by select, and every other thread only queues and
waits.
WHY written here: the stream needs binary messages and pings, nothing else of WebSocket - no new dependency of the
robot's install for that.
WHY in pieces, an act's first: a camera frame of hundreds of KB on the one connection held every act behind it; in
pieces, an act waits for one at most.
WHY no answer to a post that went well: the tunnel in front of a worker holds a small piece of data back until the robot
acknowledged the one before it: an act answered within a round trip
of a post's answer waited for that acknowledgment. {dev 10-27, worker 4: a 1 ms policy's act p50 76-96 ms on one stream
answering every post, 47-58 ms on eight connections}
"""
from __future__ import annotations

import base64
import hashlib
import os
import selectors
import socket
import ssl
import struct
import sys
import threading
import time
from collections import deque
from typing import Any, Callable, Optional
from urllib.parse import urlsplit

import httpx

from . import msgpack_io as _msgpack

PATH = "/stream"




AFTER = "seq.after"







AHEAD_BYTES = 256 * 1024
_GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


_NOTSENT_LOWAT = getattr(socket, "TCP_NOTSENT_LOWAT", {"darwin": 0x201, "linux": 25}.get(sys.platform))
_LOWAT_BYTES = 16 * 1024


ROOM_BYTES = 64 * 1024

_WRITE_BYTES = 64 * 1024


PIECE_BYTES = 16 * 1024

THROUGH_HEADER = "x-seq-stream-through"



FORMAT = "x-seq-stream/3"


_NOT_SENT = frozenset(("host", "connection", "content-length", "transfer-encoding", "accept-encoding", "authorization",
                       "x-seq-session", "user-agent", "keep-alive", "upgrade"))


class StreamClosed(Exception):
    """The stream ended: the worker closed it, the connection broke, or the robot's side closed it."""


class StreamRefused(StreamClosed):
    """The stream was not opened: something answered the upgrade with `status`, not 101 - its worker (401, 403: its
    secret; 404: built before it took one), or a proxy on the way that lets no WebSocket through."""

    def __init__(self, status: int, line: str) -> None:
        super().__init__(line)
        self.status = status


class NotOpened(httpx.ConnectError):
    """The stream did not open, or not in time, and nothing says more of why than that the worker was not reached. Its
    message carries no secret (worker_link), so it may ride what the robot is told."""


class Unwritten(Exception):
    """A request that never left: given up before the stream wrote it, or the stream ended first - the worker never saw
    it, so it may go on the next stream."""



_XOR = tuple(bytes(b ^ k for b in range(256)) for k in range(256))


def _masked(data: bytes, mask: bytes) -> bytes:
    """`data` XORed with the 4-byte `mask` (RFC 6455 5.3): four bytes at a time by numpy where the robot's process has it
    imported already (a 16 KB piece in about 5 us), else each fourth byte at once by a translation table (about 50 us).
    Every byte the robot sends its worker goes through it, on the stream's one thread and holding the interpreter: as
    one integer, as it was, a 16 KB piece took 150 us, a 100 KB camera frame 1 ms, which the act behind it waited for,
    and every other thread of the robot's with it. {dev 10-30, worker 4: at RTT 22 ms an act on the stream p50 2.4 ms
    slower than one on a connection of its own; a 100 KB frame 1.4 ms from its first byte written to its last}"""
    n = len(data)
    if not n:
        return b""
    np = sys.modules.get("numpy")
    if np is not None:
        try:
            whole = n - n % 4
            out = (np.frombuffer(data, np.uint32, whole // 4) ^ np.frombuffer(mask, np.uint32)[0]).tobytes()
            return out + bytes(b ^ mask[k] for k, b in enumerate(data[whole:]))
        except Exception:
            pass
    out = bytearray(data)
    for k in range(4):
        out[k::4] = out[k::4].translate(_XOR[mask[k]])
    return bytes(out)


def _frame(opcode: int, payload: bytes) -> bytes:
    """One whole client frame: FIN, `opcode`, masked as a client's must be."""
    n = len(payload)
    if n < 126:
        head = struct.pack(">BB", 0x80 | opcode, 0x80 | n)
    elif n < 1 << 16:
        head = struct.pack(">BBH", 0x80 | opcode, 0x80 | 126, n)
    else:
        head = struct.pack(">BBQ", 0x80 | opcode, 0x80 | 127, n)
    mask = os.urandom(4)
    return head + mask + _masked(payload, mask)


def open_stream(base_url: str, context: ssl.SSLContext, headers: dict, *, timeout_s: float,
                options: Optional[list] = None, quiet_s: Optional[float] = None,
                on_quiet: Optional[Callable[[], None]] = None, path: str = PATH,
                on_push: Optional[Callable[[dict], None]] = None,
                on_end: Optional[Callable[[str], None]] = None, trace: Any = None) -> "WorkerStream":
    """Open the stream to the worker at `base_url`: its TCP connect with `options` (the worker transport's keepalive and
    BBR) and TCP_NOTSENT_LOWAT, its TLS handshake checked by `context`, then the upgrade - GET `path` (/stream; a teleop
    console's /teleop) with `headers` (the robot's secret, its session). StreamRefused when something answers it with
    anything but 101, StreamClosed when no answer came or it does not accept the key, and what the connect or handshake
    raised. `quiet_s`/`on_quiet`: its watch for a line gone silent; `on_push`/`on_end`: what the worker pushes and the
    stream's end (WorkerStream). `trace`: told as its TCP connect and TLS handshake begin and end, by httpcore's names
    (worker_transport._ConnectionTrace)."""
    def told(event: str) -> None:
        if trace is not None:
            trace(event, {})

    parts = urlsplit(base_url)
    host, port = parts.hostname or "", parts.port or 443
    deadline = time.monotonic() + timeout_s
    told("connection.connect_tcp.started")
    raw = socket.create_connection((host, port), timeout=timeout_s)
    told("connection.connect_tcp.complete")
    try:
        raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        for option in (options or ()):
            try:
                raw.setsockopt(*option)
            except OSError:
                pass
        if _NOTSENT_LOWAT is not None:
            try:
                raw.setsockopt(socket.IPPROTO_TCP, _NOTSENT_LOWAT, _LOWAT_BYTES)
            except OSError:
                pass
        told("connection.start_tls.started")
        sock = context.wrap_socket(raw, server_hostname=host)
        told("connection.start_tls.complete")
    except BaseException:
        raw.close()
        raise
    try:
        key = base64.b64encode(os.urandom(16)).decode()
        said = {str(k).lower(): str(v) for k, v in headers.items()}
        lines = [f"GET {path} HTTP/1.1", f"Host: {said.pop('host', f'{host}:{port}')}", "Upgrade: websocket",
                 "Connection: Upgrade", f"Sec-WebSocket-Key: {key}", "Sec-WebSocket-Version: 13",
                 *(f"{k}: {v}" for k, v in said.items() if k not in ("connection", "upgrade", "content-type"))]
        sock.sendall(("\r\n".join(lines) + "\r\n\r\n").encode("latin-1"))
        got = bytearray()
        while b"\r\n\r\n" not in got:
            sock.settimeout(max(0.001, deadline - time.monotonic()))
            chunk = sock.recv(4096)
            if not chunk or len(got) > 64 * 1024:
                raise StreamClosed("the worker closed the connection before it answered the stream's opening")
            got += chunk
        head, _, rest = bytes(got).partition(b"\r\n\r\n")
        status_line, *header_lines = head.decode("latin-1").split("\r\n")
        answered = {}
        for line in header_lines:
            name, _, value = line.partition(":")
            answered[name.strip().lower()] = value.strip()
        status = status_line.split(" ", 2)[1] if len(status_line.split(" ")) > 1 else ""
        accept = base64.b64encode(hashlib.sha1(key.encode() + _GUID).digest()).decode()
        if status != "101":
            raise StreamRefused(int(status) if status.isdigit() else 0, status_line.strip()[:80])
        if answered.get("sec-websocket-accept") != accept:
            raise StreamClosed(f"the worker did not open the stream ({status_line.strip()[:80]})")
        return WorkerStream(sock, answered, rest, quiet_s=quiet_s, on_quiet=on_quiet, on_push=on_push, on_end=on_end)
    except BaseException:
        sock.close()
        raise


class _Pending:
    """One request on the stream: begun, written (sent), answered or counted taken (done), or failed. `control`: an act,
    ahead of everything else; `silent`: an observation post, answered only when it went wrong - counted taken once an
    answer names it served (X-Seq-Stream-Through). `on_done(pending)` is called once it is done, from the stream's own
    thread."""

    __slots__ = ("number", "trace", "control", "silent", "on_done", "sent", "done", "begun", "taken", "dropped",
                 "answer", "error", "began_at", "sent_at")

    def __init__(self, number: int, trace: Any, control: bool, silent: bool,
                 on_done: Optional[Callable[["_Pending"], None]]) -> None:
        self.number, self.trace, self.control, self.silent, self.on_done = number, trace, control, silent, on_done
        self.sent, self.done = threading.Event(), threading.Event()
        self.begun = False
        self.taken = False
        self.dropped = False
        self.answer: Optional[tuple[int, list, bytes]] = None
        self.error: Optional[BaseException] = None
        self.began_at: Optional[float] = None
        self.sent_at: Optional[float] = None

    def _event(self, phase: str) -> None:
        if self.trace is not None:
            try:
                self.trace(f"http11.send_request_headers.{phase}", {})
            except Exception:
                pass

    def _finish(self) -> None:
        self.done.set()
        if self.on_done is not None:
            try:
                self.on_done(self)
            except Exception:
                pass


class _Socket:
    """What httpcore's network stream answers for the connection's socket (worker_transport._congestion_of)."""

    def __init__(self, sock: socket.socket) -> None:
        self._sock = sock

    def get_extra_info(self, name: str) -> Any:
        return self._sock if name == "socket" else None


class WorkerStream:
    """One open stream (module docstring): requests in, answers out, one thread on the socket. `quiet_s`/`on_quiet`: the
    stream's watch for a line gone silent - `on_quiet()` is called once, on a thread of its own, when no act's answer
    came for `quiet_s` (from the opening, or the last act's answer), and again only after another came. `on_push`: each
    whole message the worker pushes, {"t": ...} (a teleop robot's who drives and a person's chunks; a console's all),
    called on the stream's own thread - it must not wait; `on_end(why)`: once, as the stream ends."""

    def __init__(self, sock: socket.socket, said: dict, rest: bytes = b"", *, quiet_s: Optional[float] = None,
                 on_quiet: Optional[Callable[[], None]] = None, on_push: Optional[Callable[[dict], None]] = None,
                 on_end: Optional[Callable[[str], None]] = None) -> None:

        self.said = said
        self._sock = sock
        self._lock = threading.Lock()
        self._room = threading.Condition(self._lock)
        self._frames: deque = deque()
        self._control: deque = deque()
        self._bulk: deque = deque()
        self._last_bulk: dict = {}
        self._out_bytes = 0
        self.bulk_written = 0
        self._buf = memoryview(b"")
        self._marks: deque = deque()
        self._buf_sent = 0
        self._waiting: dict[int, _Pending] = {}
        self._answers: dict[int, list] = {}
        self._next = 1
        self._closed: Optional[str] = None
        self._in = bytearray(rest)
        self._parts: list = []
        self._read_wants_write = False
        self.last_sent = time.monotonic()
        self._quiet_s, self._on_quiet = quiet_s, on_quiet
        self._on_push, self._on_end = on_push, on_end
        self._last_control, self._quiet_said = time.monotonic(), False
        self._net = _Socket(sock)
        self._wake_r, self._wake_w = socket.socketpair()
        self._wake_r.setblocking(False)
        self._wake_w.setblocking(False)
        self._thread = threading.Thread(target=self._run, daemon=True, name="seq-stream")
        self._thread.start()

    @property
    def alive(self) -> bool:
        return self._closed is None

    @property
    def why_closed(self) -> Optional[str]:
        return self._closed

    def submit(self, method: str, path: str, headers: list, body: bytes, trace: Any = None, *, control: bool = False,
               silent: bool = False, on_done: Optional[Callable[[_Pending], None]] = None, key: Optional[str] = None,
               after: Optional[str] = None) -> _Pending:
        """Queue one request behind every one handed over before it - an act (`control`) behind the acts alone, and
        the requests queued before it under `after` (its episode's observation posts, each queued under its `key`) -
        and never wait. StreamClosed once the stream ended."""
        body = memoryview(bytes(body))
        head = {"m": method, "p": path, "h": headers}
        with self._lock:
            if self._closed is not None:
                raise StreamClosed(self._closed)
            pending = _Pending(self._next, trace, control, silent, on_done)
            self._next += 1
            self._waiting[pending.number] = pending
            if control:
                self._control.append([pending, head, body, 0, self._last_bulk.get(after) if after else None])
            else:
                self._bulk.append([pending, head, body, 0, key])
                self._out_bytes += len(body)
                if key is not None:
                    self._last_bulk[key] = pending
        self._wake()
        return pending

    def answer(self, pending: _Pending, *, write_s: float, read_s: Optional[float]) -> tuple[int, list, bytes]:
        """The answer to `pending`: (status, headers, body). Unwritten when it was not begun within `write_s` - then it
        is never written - or the stream ended before it was; StreamClosed when the stream ended after it was written;
        TimeoutError when, written, it was not answered within `read_s` (None: as long as it takes)."""
        if not pending.sent.wait(max(0.0, write_s)):
            with self._lock:
                if not pending.begun:
                    pending.dropped = True
                    self._waiting.pop(pending.number, None)
                    raise Unwritten("the stream did not write it in time")
            pending.sent.wait(read_s)
        if pending.error is not None and not pending.begun:
            raise Unwritten(str(pending.error))
        if not pending.done.wait(read_s):
            with self._lock:
                self._waiting.pop(pending.number, None)
            raise TimeoutError("no answer in time")
        if pending.error is not None:
            raise pending.error
        assert pending.answer is not None
        return pending.answer

    def room(self, timeout_s: float = 0.0) -> bool:
        """Whether the backlog not yet written is under ROOM_BYTES - waited for up to `timeout_s`; True once the stream
        ended, so a caller waiting on it goes on to meet that."""
        end = time.monotonic() + timeout_s
        with self._room:
            while self._closed is None and self._out_bytes >= ROOM_BYTES:
                left = end - time.monotonic()
                if left <= 0:
                    return False
                self._room.wait(left)
            return True

    def ping(self) -> None:
        """A ping, ahead of what waits (keep-warm, worker_transport._keep_warm); answered by the worker's WebSocket
        itself. Nothing once the stream ended, nor while one waits."""
        with self._lock:
            if self._closed is not None or self._frames:
                return
            self._frames.append(_frame(0x9, b""))
        self._wake()

    def send_message(self, message: dict) -> None:
        """One whole message to the worker, {"t": ...} - a teleop console's - ahead of everything waiting: a stop never
        waits behind a request. StreamClosed once the stream ended."""
        frame = _frame(0x2, _msgpack.pack(message))
        with self._lock:
            if self._closed is not None:
                raise StreamClosed(self._closed)
            self._frames.append(frame)
        self._wake()

    def close(self, why: str = "the robot's side closed the stream") -> None:
        """End the stream: its connection closed, every request still waiting failed."""
        self._end(why, wait=True)

    def handle(self, request: httpx.Request) -> httpx.Response:
        """One httpx request over the stream, answered as an httpx.Response - an act, or a question of whether the
        worker is there, ahead of everything but the piece being written: its timeouts as httpx's - written within its
        pool and write bounds (Unwritten past them: never sent), answered within its read bound - and httpx's own errors
        for the rest."""
        body = request.read()
        headers = [[k, v] for k, v in request.headers.multi_items() if k.lower() not in _NOT_SENT]
        path = request.url.raw_path.decode("latin-1")
        bounds = request.extensions.get("timeout") or {}
        write_s = (bounds.get("pool") or 0.0) + (bounds.get("write") or bounds.get("connect") or 30.0)
        read_s = bounds.get("read")
        route = (request.method, path.split("?", 1)[0])
        control = route in (("POST", "/act"), ("GET", "/ping"))
        try:
            pending = self.submit(request.method, path, headers, body, request.extensions.get("trace"),
                                  control=control, after=request.extensions.get(AFTER))
        except StreamClosed as exc:
            raise Unwritten(str(exc)) from None
        try:
            status, said, content = self.answer(pending, write_s=write_s, read_s=read_s)
        except StreamClosed as exc:
            raise httpx.ReadError(f"the stream to the worker ended: {exc}", request=request) from None
        except TimeoutError:
            raise httpx.ReadTimeout("the worker did not answer on the stream in time", request=request) from None
        return httpx.Response(status, headers=[(k, v) for k, v in said if k.lower() != "transfer-encoding"],
                              content=content, request=request, extensions={"network_stream": self._net})



    def _wake(self) -> None:
        try:
            self._wake_w.send(b"\0")
        except OSError:
            pass

    def _run(self) -> None:
        sock = self._sock
        selector = selectors.DefaultSelector()
        try:
            sock.setblocking(False)
            selector.register(self._wake_r, selectors.EVENT_READ)
            selector.register(sock, selectors.EVENT_READ)
            self._parse()
            while True:
                with self._lock:
                    if self._closed is not None:
                        return
                    writing = bool(self._buf) or bool(self._frames or self._control or self._bulk)
                    writing = writing or self._read_wants_write
                selector.modify(sock, selectors.EVENT_READ | (selectors.EVENT_WRITE if writing else 0))
                for key, events in selector.select(self._quiet_left()):
                    if key.fileobj is self._wake_r:
                        try:
                            while self._wake_r.recv(4096):
                                pass
                        except (BlockingIOError, OSError):
                            pass
                        continue
                    if events & selectors.EVENT_READ or self._read_wants_write:
                        self._read()
                    if events & selectors.EVENT_WRITE:
                        self._write()
                self._watch_quiet()
        except Exception as exc:
            self._end(f"{type(exc).__name__}: {exc}"[:300])
        finally:
            self._end("the stream ended")
            selector.close()
            for s in (sock, self._wake_r, self._wake_w):
                try:
                    s.close()
                except OSError:
                    pass

    def _quiet_left(self) -> Optional[float]:
        """How long the select may wait before the line's silence is due to be said: None when it is not watched."""
        if self._quiet_s is None or self._on_quiet is None or self._quiet_said:
            return None
        return max(0.0, self._last_control + self._quiet_s - time.monotonic())

    def _watch_quiet(self) -> None:
        if self._quiet_left() == 0.0:
            self._quiet_said = True
            threading.Thread(target=self._say_quiet, daemon=True, name="seq-stream-quiet").start()

    def _say_quiet(self) -> None:
        try:
            self._on_quiet()
        except Exception:
            pass

    def _read(self) -> None:
        self._read_wants_write = False
        while True:
            try:
                data = self._sock.recv(65536)
            except (ssl.SSLWantReadError, BlockingIOError):
                return
            except ssl.SSLWantWriteError:
                self._read_wants_write = True
                return
            if not data:
                raise StreamClosed("the worker closed the connection")
            self._in += data
            self._parse()

    def _parse(self) -> None:
        buf = self._in
        while len(buf) >= 2:
            first, second = buf[0], buf[1]
            n, at = second & 0x7F, 2
            if n == 126:
                if len(buf) < 4:
                    return
                n, at = struct.unpack(">H", bytes(buf[2:4]))[0], 4
            elif n == 127:
                if len(buf) < 10:
                    return
                n, at = struct.unpack(">Q", bytes(buf[2:10]))[0], 10
            mask = b""
            if second & 0x80:
                if len(buf) < at + 4:
                    return
                mask, at = bytes(buf[at:at + 4]), at + 4
            if len(buf) < at + n:
                return
            payload = bytes(buf[at:at + n])
            del buf[:at + n]
            if mask:
                payload = _masked(payload, mask)
            self._frame_in(first & 0x80, first & 0x0F, payload)

    def _frame_in(self, fin: int, opcode: int, payload: bytes) -> None:
        if opcode == 0x9:
            with self._lock:
                self._frames.append(_frame(0xA, payload))
            return
        if opcode == 0xA:
            return
        if opcode == 0x8:
            code = struct.unpack(">H", payload[:2])[0] if len(payload) >= 2 else 1005
            raise StreamClosed(f"the worker closed the stream ({code})")
        if opcode in (0x1, 0x2):
            self._parts = [payload]
        elif opcode == 0x0:
            self._parts.append(payload)
        if fin and self._parts:
            message, self._parts = b"".join(self._parts), []
            self._deliver(message)

    def _deliver(self, message: bytes) -> None:
        """One piece of an answer: once its last came, its request is answered - then every observation post it names
        served counted taken (X-Seq-Stream-Through), a post's refusal having come before any answer that names it."""
        piece = _msgpack.unpack(message)
        if isinstance(piece, dict) and "t" in piece and "i" not in piece:

            if self._on_push is not None:
                try:
                    self._on_push(piece)
                except Exception:
                    pass
            return
        if not isinstance(piece, dict) or not isinstance(piece.get("i"), int) or piece["i"] < 0:
            raise StreamClosed(f"the worker could not read a request on the stream: {str(piece)[:200]}")
        number = piece["i"]
        got = self._answers.setdefault(number, [None, [], []])
        if "s" in piece:
            got[0], got[1] = int(piece.get("s") or 500), list(piece.get("h") or ())
        got[2].append(bytes(piece.get("b") or b""))
        if piece.get("more"):
            return
        del self._answers[number]
        status, headers, parts = got
        said = [(str(k), str(v)) for k, v in headers]
        with self._lock:
            pending = self._waiting.pop(number, None)
        if pending is not None:
            pending.answer = (status or 500, said, b"".join(parts))
            if pending.control:
                self._last_control, self._quiet_said = time.monotonic(), False
            pending._finish()
        through = next((v for k, v in said if k.lower() == THROUGH_HEADER), None)
        if through is not None and through.strip().lstrip("-").isdigit():
            self._taken(int(through))

    def _taken(self, through: int) -> None:
        """Every observation post up to request `through` the worker served, answered nothing: taken."""
        with self._lock:
            done = sorted((n for n, p in self._waiting.items() if p.silent and n <= through))
            taken = [self._waiting.pop(n) for n in done]
        for pending in taken:
            pending._finish()

    def _control_ready(self) -> bool:
        """Whether the first act waiting may go now (under self._lock): what it follows (AFTER) is placed for writing,
        or what is left to write of it and of what is queued before it is AHEAD_BYTES at most."""
        if not self._control:
            return False
        after = self._control[0][4]
        if after is None or after.taken or after.dropped or after.error is not None:
            return True
        left = 0
        for pending, _, body, at, _ in self._bulk:
            if not pending.dropped:
                left += len(body) - at
            if pending is after or left > AHEAD_BYTES:
                break
        return left <= AHEAD_BYTES

    def _piece_of(self, queue: deque) -> Optional[tuple[_Pending, bytes, bool, int]]:
        """The next piece of `queue`'s first request (under self._lock): (its request, its frame, whether it is its
        last, the bulk's bytes it carries); None once a request given up before it began is passed and none is left."""
        while queue:
            entry = queue[0]
            pending, head, body, at, key = entry
            if at == 0 and pending.dropped:
                queue.popleft()
                if queue is self._bulk:
                    self._out_bytes -= len(body)
                continue
            part = body[at:at + PIECE_BYTES]
            piece: dict = {"i": pending.number, "b": bytes(part)}
            if at == 0:
                piece.update(head)
                pending.begun = True
            entry[3] = at + len(part)
            last = entry[3] >= len(body)
            if last:
                queue.popleft()
                pending.taken = True
                if queue is self._bulk and key is not None and self._last_bulk.get(key) is pending:
                    del self._last_bulk[key]
            else:
                piece["more"] = True
            bulk = len(part) if queue is self._bulk else 0
            self._out_bytes -= bulk
            return pending, _frame(0x2, _msgpack.pack(piece)), last, bulk
        return None

    def _fill(self) -> bool:
        """The next write (under self._lock): WebSocket's own frames first, then an act's piece - once what it follows
        is placed - else the rest's next piece; and behind that piece, in the same write, every act's piece that may go
        then (one following its episode's last observation goes with it). False for nothing to write."""
        frames, marks, size = [], [], 0

        def put(got) -> None:
            nonlocal size
            pending, frame, last, bulk = got
            frames.append(frame)
            size += len(frame)
            marks.append((size, pending, last, bulk))

        if self._frames:
            frame = self._frames.popleft()
            frames.append(frame)
            size = len(frame)
            marks.append((size, None, False, 0))
        else:
            got = self._piece_of(self._control) if self._control_ready() else None
            if got is None:
                got = self._piece_of(self._bulk)
            if got is None:
                return False
            put(got)
        while self._control_ready() and size < _WRITE_BYTES:
            got = self._piece_of(self._control)
            if got is None:
                break
            put(got)
        self._buf, self._buf_sent, self._marks = memoryview(b"".join(frames)), 0, deque(marks)
        return True

    def _write(self) -> None:
        while True:
            if not self._buf:
                with self._lock:
                    filled = self._fill()
                    self._room.notify_all()
                if not filled:
                    return
                for _, pending, _, _ in self._marks:
                    if pending is not None and pending.began_at is None:
                        pending.began_at = time.monotonic()
                        pending._event("started")
            try:
                sent = self._sock.send(self._buf[:_WRITE_BYTES])
            except (ssl.SSLWantWriteError, ssl.SSLWantReadError, BlockingIOError):
                return
            self._buf, self._buf_sent = self._buf[sent:], self._buf_sent + sent
            while self._marks and self._marks[0][0] <= self._buf_sent:
                _, done, last, bulk = self._marks.popleft()
                self.last_sent = time.monotonic()
                self.bulk_written += bulk
                if done is not None and last:
                    done.sent_at = self.last_sent
                    done._event("complete")
                    done.sent.set()

    def _end(self, why: str, *, wait: bool = False) -> None:
        """The stream ended (`why`): every request not answered is told - one not begun as Unwritten, so it may go on the
        next stream - and nothing more is queued. `wait`: the robot's own close, its thread given a moment to end."""
        with self._lock:
            first = self._closed is None
            if first:
                self._closed = why
            waiting, self._waiting = list(self._waiting.values()), {}
            self._room.notify_all()
        for pending in waiting:
            pending.error = StreamClosed(why) if pending.begun else Unwritten(why)
            pending.sent.set()
            pending._finish()
        if first:
            self._wake()
            if self._on_end is not None:
                try:
                    self._on_end(why)
                except Exception:
                    pass
            if wait and threading.current_thread() is not self._thread:
                self._thread.join(timeout=1.0)


class StreamRouted(httpx.BaseTransport):
    """An httpx transport that sends every request over the robot's stream (`route`: the open one, waited for while it
    opens, what its opening met raised). A request the stream ended before it wrote goes on the next one: the worker
    never saw it."""

    def __init__(self, route: Callable[[httpx.Request], WorkerStream]) -> None:
        self._route = route

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        for _ in range(2):
            try:
                return self._route(request).handle(request)
            except Unwritten as exc:
                unwritten = str(exc)
        raise httpx.ConnectError(f"the stream to the worker ended before this request was written: {unwritten}",
                                 request=request)

    def close(self) -> None:
        pass
