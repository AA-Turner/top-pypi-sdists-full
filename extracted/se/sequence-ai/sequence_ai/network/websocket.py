# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
The server side of a WebSocket, for a uvicorn server, with nothing installed for it: what serve() runs each robot's
stream on (GET /stream).

    import uvicorn
    from sequence_ai.network import websocket

    uvicorn.run(app, ws=websocket.protocol())          # an ASGI app that takes websocket scopes

In one sentence: uvicorn reads a request that asks to upgrade (Upgrade: websocket) and hands its connection here → the
request is checked as RFC 6455 has it (a key, version 13) and the app is called with a websocket scope → the app's
websocket.accept answers 101 with the headers it names, a websocket.close before it answers 403 → each message the
client sends - masked frames, one or several - goes to the app as one websocket.receive, and the connection is read no
further until the app has taken it → each websocket.send goes as one frame, unmasked, as a server's go → a ping is
answered with a pong at once, a close with a close; the server pings the client every ws_ping_interval (uvicorn's
setting) and closes the connection when no pong comes within ws_ping_timeout.

WHY written here: a robot's stream needs binary messages and pings and nothing more of WebSocket, and uvicorn has no
WebSocket of its own - it uses websockets or wsproto where one is installed, and sequence-ai installs neither, so a
robot's install stays as small as it is. The robot's side is written the same way, in the same package.
WHY the connection is read no further until the app has taken a message: what a robot sends faster than its server
handles it waits in the robot's own queue, where what is not sent yet can still be left out, not in this server's
memory. WHY the client is pinged: a robot that went without closing its stream - its network gone - would otherwise hold
it for as long as the server runs.

Standard library only; numpy unmasks a frame four bytes at a time where it is installed.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import logging
import struct
import sys
from typing import Any, Iterator, Optional
from urllib.parse import unquote

__all__ = ["GUID", "MAX_MESSAGE_BYTES", "WebSocketProtocol", "accept_key", "frame", "protocol", "read_frames"]

log = logging.getLogger("uvicorn.error")

# RFC 6455's constant, joined to the client's key for the accept key the server answers with.
GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
# The largest message read when the server names none (uvicorn's ws_max_size names it): a bigger one closes the
# connection with 1009.
MAX_MESSAGE_BYTES = 16 << 20
# How long the server waits for the client's close after its own before it closes the connection itself.
CLOSE_WAIT_S = 2.0

_CONTINUATION, _TEXT, _BINARY, _CLOSE, _PING, _PONG = 0x0, 0x1, 0x2, 0x8, 0x9, 0xA


class _Gone(OSError):
    """The client went: what a websocket.send after the connection ended raises, as uvicorn's own protocols do."""


def accept_key(key: str) -> str:
    """The Sec-WebSocket-Accept a server answers the client's Sec-WebSocket-Key with (RFC 6455 section 4.2.2)."""
    return base64.b64encode(hashlib.sha1(key.encode("latin-1") + GUID).digest()).decode("latin-1")


def frame(opcode: int, payload: bytes) -> bytes:
    """One whole server frame: FIN, `opcode` and `payload`, unmasked, as a server's are."""
    n = len(payload)
    if n < 126:
        head = struct.pack(">BB", 0x80 | opcode, n)
    elif n < 1 << 16:
        head = struct.pack(">BBH", 0x80 | opcode, 126, n)
    else:
        head = struct.pack(">BBQ", 0x80 | opcode, 127, n)
    return head + payload


def _unmasked(data: bytes, mask: bytes) -> bytes:
    """`data` XORed with the 4-byte `mask`: four bytes at a time by numpy where it is installed, else each fourth byte
    at once through a translation table."""
    n = len(data)
    if not n:
        return b""
    np = sys.modules.get("numpy")
    if np is not None:
        whole = n - n % 4
        out = (np.frombuffer(data, np.uint32, whole // 4) ^ np.frombuffer(mask, np.uint32)[0]).tobytes()
        return out + bytes(b ^ mask[k] for k, b in enumerate(data[whole:]))
    out = bytearray(data)
    for k in range(4):
        out[k::4] = out[k::4].translate(_XOR[mask[k]])
    return bytes(out)


_XOR = tuple(bytes(b ^ k for b in range(256)) for k in range(256))


def read_frames(buf: bytearray, limit: int = MAX_MESSAGE_BYTES) -> Iterator[tuple[bool, int, bytes]]:
    """Each whole frame at the front of `buf`, taken out of it as it is read: (whether it is its message's last, its
    opcode, its payload unmasked). What is left in `buf` is a frame not all here yet. ValueError for a frame whose
    payload is over `limit`."""
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
        if n > limit:
            raise ValueError(f"a frame of {n} bytes, over the {limit} this server reads")
        mask = b""
        if second & 0x80:
            if len(buf) < at + 4:
                return
            mask, at = bytes(buf[at:at + 4]), at + 4
        if len(buf) < at + n:
            return
        payload = bytes(buf[at:at + n])
        del buf[:at + n]
        yield bool(first & 0x80), first & 0x0F, (_unmasked(payload, mask) if mask else payload)


class WebSocketProtocol(asyncio.Protocol):
    """One WebSocket connection of a uvicorn server (the module's docstring), made by uvicorn as a request upgrades:
    pass the class as uvicorn.Config(ws=...)."""

    def __init__(self, config: Any, server_state: Any, app_state: Optional[dict] = None,
                 _loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        if not config.loaded:
            config.load()
        self.config, self.app = config, config.loaded_app
        self.loop = _loop or asyncio.get_event_loop()
        self.connections, self.tasks = server_state.connections, server_state.tasks
        self.default_headers = list(getattr(server_state, "default_headers", ()) or ())
        self.app_state = dict(app_state or {})
        self.limit = int(getattr(config, "ws_max_size", None) or MAX_MESSAGE_BYTES)
        self.ping_every_s = getattr(config, "ws_ping_interval", None)
        self.pong_within_s = getattr(config, "ws_ping_timeout", None)
        self.transport: Any = None
        self.scope: Optional[dict] = None
        self.queue: asyncio.Queue = asyncio.Queue()
        self.request = bytearray()               # the upgrade request, until its headers end
        self.buf = bytearray()                   # what came of the frames after it
        self.parts: list = []                    # a message's frames so far
        self.kind = _BINARY                      # its opcode: binary or text
        self.accepted = False                    # 101 sent
        self.answered = False                    # 101 or a refusal sent: no HTTP answer may follow
        self.closing = False                     # a close sent, or the connection ending
        self.gone = False                        # the connection ended
        self.paused = False                      # reading paused while the app has a message to take
        self.writable = asyncio.Event()
        self.writable.set()
        self.ping_timer: Optional[asyncio.TimerHandle] = None
        self.pong_timer: Optional[asyncio.TimerHandle] = None

    # ── asyncio.Protocol ──────────────────────────────────────────────────────────────────────────────────────────
    def connection_made(self, transport: Any) -> None:  # type: ignore[override]
        """The upgraded connection, handed over by uvicorn's HTTP protocol."""
        self.connections.add(self)
        self.transport = transport

    def connection_lost(self, exc: Optional[BaseException]) -> None:
        """The connection ended: the app is told, if it is not already."""
        self._stop_pings()
        self.connections.discard(self)
        if not self.gone:
            self.gone = True
            self.queue.put_nowait({"type": "websocket.disconnect", "code": 1005 if self.accepted else 1006})
        self.writable.set()

    def data_received(self, data: bytes) -> None:
        """The upgrade request first, then frames."""
        if self.scope is None:
            self.request += data
            if b"\r\n\r\n" not in self.request:
                if len(self.request) > 64 * 1024:
                    self._refuse(400, b"the upgrade request's headers are over 64 KB")
                return
            head, _, rest = bytes(self.request).partition(b"\r\n\r\n")
            self.request = bytearray()
            if not self._connect(head):
                return
            data = rest
        self.buf += data
        try:
            for last, opcode, payload in read_frames(self.buf, self.limit):
                self._frame(last, opcode, payload)
                if self.gone:
                    return
        except ValueError as e:
            self._close(1009, str(e))

    def pause_writing(self) -> None:
        """The transport's buffer is full: websocket.send waits."""
        self.writable.clear()

    def resume_writing(self) -> None:
        """The transport's buffer has room again: websocket.send goes on."""
        self.writable.set()

    def shutdown(self) -> None:
        """The server stops: the app is told, and the client is sent a close (1012, the server restarting)."""
        self._stop_pings()
        if self.accepted and not self.closing:
            self.queue.put_nowait({"type": "websocket.disconnect", "code": 1012})
            self._write(frame(_CLOSE, struct.pack(">H", 1012)))
        elif not self.answered:
            self._refuse(503, b"the server is stopping")
        self.closing = True
        self.transport.close()

    # ── the upgrade ───────────────────────────────────────────────────────────────────────────────────────────────
    def _connect(self, head: bytes) -> bool:
        """The upgrade request read: its key and version checked and the app started with its scope. False when it was
        refused."""
        line, *lines = head.decode("latin-1").split("\r\n")
        parts = line.split(" ")
        headers = []
        for one in lines:
            name, _, value = one.partition(":")
            headers.append((name.strip().lower().encode("latin-1"), value.strip().encode("latin-1")))
        said = dict(headers)
        key = said.get(b"sec-websocket-key", b"").decode("latin-1")
        if len(parts) < 2 or parts[0] != "GET" or said.get(b"sec-websocket-version") != b"13" or not key:
            self._refuse(400, b"a WebSocket opens with GET, Sec-WebSocket-Version: 13 and a Sec-WebSocket-Key")
            return False
        self.key = key
        target = parts[1]
        raw_path, _, query = target.partition("?")
        from uvicorn.protocols.utils import get_local_addr, get_remote_addr, is_ssl

        root = getattr(self.config, "root_path", "") or ""
        self.scope = {
            "type": "websocket", "asgi": {"version": "3.0", "spec_version": "2.3"}, "http_version": "1.1",
            "scheme": "wss" if is_ssl(self.transport) else "ws", "server": get_local_addr(self.transport),
            "client": get_remote_addr(self.transport), "root_path": root, "path": root + unquote(raw_path),
            "raw_path": root.encode("latin-1") + raw_path.encode("latin-1"), "query_string": query.encode("latin-1"),
            "headers": headers, "subprotocols": [], "state": dict(self.app_state),
        }
        self.queue.put_nowait({"type": "websocket.connect"})
        task = self.loop.create_task(self._run())
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return True

    def _refuse(self, status: int, body: bytes) -> None:
        """An HTTP answer in place of the upgrade, and the connection closed."""
        self.answered = self.closing = True
        reason = {400: "Bad Request", 403: "Forbidden", 500: "Internal Server Error",
                  503: "Service Unavailable"}.get(status, "Error")
        self._write(f"HTTP/1.1 {status} {reason}\r\ncontent-type: text/plain; charset=utf-8\r\n"
                    f"content-length: {len(body)}\r\nconnection: close\r\n\r\n".encode("latin-1") + body)
        self.transport.close()

    # ── frames ────────────────────────────────────────────────────────────────────────────────────────────────────
    def _frame(self, last: bool, opcode: int, payload: bytes) -> None:
        if opcode == _PING:
            self._write(frame(_PONG, payload))
            return
        if opcode == _PONG:
            if self.pong_timer is not None:
                self.pong_timer.cancel()
                self.pong_timer = None
            return
        if opcode == _CLOSE:
            code = struct.unpack(">H", payload[:2])[0] if len(payload) >= 2 else 1005
            if not self.closing:
                self.closing = True
                self._write(frame(_CLOSE, payload[:2]))
            if not self.gone:
                self.gone = True
                self.queue.put_nowait({"type": "websocket.disconnect", "code": code})
            self.transport.close()
            return
        if opcode in (_TEXT, _BINARY):
            self.parts, self.kind = [payload], opcode
        elif opcode == _CONTINUATION and self.parts:
            self.parts.append(payload)
        else:
            self._close(1002, "a continuation with no message to continue")
            return
        if sum(len(p) for p in self.parts) > self.limit:
            self._close(1009, f"a message over the {self.limit} bytes this server reads")
            return
        if last:
            data, self.parts = b"".join(self.parts), []
            message = ({"type": "websocket.receive", "text": data.decode("utf-8", "replace")} if self.kind == _TEXT
                       else {"type": "websocket.receive", "bytes": data})
            self.queue.put_nowait(message)
            if not self.paused:
                self.paused = True
                self.transport.pause_reading()

    def _close(self, code: int, reason: str) -> None:
        """Close the connection from this side: the client sent what it may not (`code`)."""
        if not self.closing:
            self.closing = True
            self._write(frame(_CLOSE, struct.pack(">H", code) + reason.encode("utf-8")[:120]))
        if not self.gone:
            self.gone = True
            self.queue.put_nowait({"type": "websocket.disconnect", "code": code})
        self.transport.close()

    def _write(self, data: bytes) -> None:
        if not self.transport.is_closing():
            self.transport.write(data)

    # ── pings ─────────────────────────────────────────────────────────────────────────────────────────────────────
    def _ping_later(self) -> None:
        if self.ping_every_s:
            self.ping_timer = self.loop.call_later(float(self.ping_every_s), self._ping)

    def _ping(self) -> None:
        self.ping_timer = None
        if self.closing or self.transport.is_closing():
            return
        self._write(frame(_PING, b""))
        if self.pong_within_s and self.pong_timer is None:
            self.pong_timer = self.loop.call_later(float(self.pong_within_s), self._no_pong)
        self._ping_later()

    def _no_pong(self) -> None:
        self.pong_timer = None
        log.info("a WebSocket's client answered no ping in %s s: closed", self.pong_within_s)
        self._close(1011, "no pong")

    def _stop_pings(self) -> None:
        for timer in (self.ping_timer, self.pong_timer):
            if timer is not None:
                timer.cancel()
        self.ping_timer = self.pong_timer = None

    # ── ASGI ──────────────────────────────────────────────────────────────────────────────────────────────────────
    async def _run(self) -> None:
        try:
            await self.app(self.scope, self._receive, self._send)
        except _Gone:
            pass
        except BaseException:  # noqa: BLE001 - the app's own error: logged, and the client told as uvicorn tells it
            log.exception("Exception in ASGI application\n")
            if not self.answered:
                self._refuse(500, b"Internal Server Error")
        else:
            if not self.answered:
                log.error("ASGI callable returned without completing handshake.")
                self._refuse(500, b"Internal Server Error")
        if not self.closing and not self.gone:
            self._close(1000, "")
        elif not self.transport.is_closing():
            self.loop.call_later(CLOSE_WAIT_S, self.transport.close)

    async def _receive(self) -> dict:
        message = await self.queue.get()
        if self.paused and self.queue.empty() and not self.gone:
            self.paused = False
            self.transport.resume_reading()
        return message

    async def _send(self, message: dict) -> None:
        await self.writable.wait()
        if self.gone:
            raise _Gone("the client's connection ended")
        kind = message["type"]
        if not self.answered:
            if kind == "websocket.accept":
                self.answered = self.accepted = True
                headers = [*self.default_headers, *message.get("headers", ())]
                said = "".join(f"{k.decode('latin-1')}: {v.decode('latin-1')}\r\n" for k, v in headers
                               if k.lower() not in (b"upgrade", b"connection", b"sec-websocket-accept"))
                self._write(("HTTP/1.1 101 Switching Protocols\r\nupgrade: websocket\r\nconnection: Upgrade\r\n"
                             f"sec-websocket-accept: {accept_key(self.key)}\r\n{said}\r\n").encode("latin-1"))
                self._ping_later()
            elif kind == "websocket.close":
                self.gone = True
                self.queue.put_nowait({"type": "websocket.disconnect", "code": 1006})
                self._refuse(403, b"")
            else:
                raise RuntimeError(f"a WebSocket's first message is websocket.accept or websocket.close, not {kind}")
            return
        if kind == "websocket.send":
            if self.closing:
                return
            data = message.get("bytes")
            if data is not None:
                self._write(frame(_BINARY, bytes(data)))
            else:
                self._write(frame(_TEXT, str(message.get("text") or "").encode("utf-8")))
        elif kind == "websocket.close":
            if not self.closing:
                self.closing = True
                code = int(message.get("code") or 1000)
                self._write(frame(_CLOSE, struct.pack(">H", code) + str(message.get("reason") or "").encode()[:120]))
                self.loop.call_later(CLOSE_WAIT_S, self.transport.close)
        else:
            raise RuntimeError(f"not a message a WebSocket's app sends once it is accepted: {kind}")


def protocol() -> type:
    """The class to pass as uvicorn.Config(ws=...): uvicorn makes one for each connection that upgrades."""
    return WebSocketProtocol
