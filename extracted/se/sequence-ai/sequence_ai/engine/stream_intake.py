# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A robot's requests on one WebSocket (GET /stream): its observations as it makes them, its acts and whatever else it
asks, written in the order the robot made them on one connection and each served by the server's app as that request is
served over HTTP - its acts answered first. What serve() runs in front of its app (engine.serve).

    app = StreamIntake(App(policy), headers=lambda: [(b"x-seq-act-formats", FORMAT.encode())])

In one sentence: an authorized upgrade to GET /stream is accepted with the headers every answer carries → each request
comes in pieces of at most PIECE_BYTES, msgpack {"i": its number, "m", "p", "h" (in its first piece), "b": a part of its
body, "more": true (on all but its last)} → once whole, the app serves it as that request - the same route, the same
answer - the connection's own Authorization on it: an act on a task of its own, every other request in turn on the
stream's one queue, while the next pieces are read → each answer goes back in pieces {"i", "s", "h" (its first), "b",
"more"}, an act's ahead of any other, so at most a piece of another answer is written before it - and a message the
server pushes to the robot, whole, {"t": ...}, ahead of them all → an observation post
the app answered 2xx is answered nothing: every answer names, in X-Seq-Stream-Through, the last request of the queue
served whose answer, if it had one, went before it - every post up to it is the robot's to count as taken. A message
with no number, {"t": ...}, is no request and has no answer (a heartbeat).

WHY one connection: an act and the observations before it, sent on connections of their own, reached the server in any
order, and an act that came first waited for a frame still on its way. On one connection what the robot sent first
arrives first.
WHY each request served as HTTP's: the app serves it as it serves every request - the same routes, the same checks, the
same answers - so a request over HTTP and one over the stream cannot drift apart.
WHY in pieces, an act's first: a camera frame of hundreds of KB on the one connection would hold every act behind it; in
pieces, an act waits for one piece at most.
WHY no answer to a post that went well: a tunnel in front of a server can hold a small piece of data back until the
robot has acknowledged the one before it, so an act answered within a round trip of a post's answer would wait for that
acknowledgment; one number on each answer says the same of every post before it.

The robot's side is sequence_ai/_core/worker_stream.py, the same protocol; network.stream puts it on connect().
"""
from __future__ import annotations

import asyncio
from collections import deque
from typing import Any, Callable, Optional

from ..network import msgpack_io

__all__ = ["FORMAT", "PATH", "PIECE_BYTES", "THROUGH_HEADER", "StreamIntake"]

PATH = "/stream"
# What the upgrade's answer names in X-Seq-Act-Formats: the robot's side opens a stream only to a server that names it.
FORMAT = "x-seq-stream/3"
# The most of a body one piece carries, either way: what an act's answer waits behind at most.
PIECE_BYTES = 16 * 1024
# What each answer names: the last request of the stream's queue served, every answer it had gone before.
THROUGH_HEADER = "x-seq-stream-through"
# The requests the stream's queue holds served or waiting before it reads no more: the robot's side waits then.
QUEUED = 64
# The connection's headers each request on it carries, as a request over HTTP would (StreamIntake's `carried`).
CARRIED = (b"authorization", b"user-agent", b"host", b"x-seq-robot")
# What frames a body over HTTP/1.1, which a message's own body length takes the place of.
_FRAMING = (b"content-length", b"transfer-encoding", b"connection", b"upgrade")
# Requests served on a task of their own, their answers first: what comes while one runs is taken meanwhile.
_ON_A_TASK = {("POST", "/act")}
_END = "/act/episode_end"
# Requests whose 2xx answer is none: the robot counts each taken from X-Seq-Stream-Through.
_SILENT = {("POST", "/observe")}


class _Outbox:
    """What goes back on one stream, in pieces of PIECE_BYTES at most: what the server pushes to the robot first (whole
    messages {"t": ...}), acts' answers next, the rest in the order the stream's queue served it - and, for each request
    of that queue answered nothing, the mark that it was served, which every answer after it carries (through)."""

    def __init__(self) -> None:
        self.pushed: deque = deque()           # packed messages pushed to the robot, each one whole
        self.control: deque = deque()          # [number, status, headers, body, at] of acts' answers
        self.bulk: deque = deque()             # the same of the queue's - status None: served, answered nothing
        self.through = 0
        self.ready = asyncio.Event()
        self.loop = asyncio.get_running_loop()

    def push(self, message: dict) -> None:
        """A message to the robot ahead of every answer - from any thread."""
        data = msgpack_io.pack(message)
        try:
            here = asyncio.get_running_loop()
        except RuntimeError:
            here = None
        if here is self.loop:
            self._pushed(data)
        elif not self.loop.is_closed():
            self.loop.call_soon_threadsafe(self._pushed, data)

    def _pushed(self, data: bytes) -> None:
        self.pushed.append(data)
        self.ready.set()

    def answer(self, number: int, reply: dict, *, control: bool) -> None:
        (self.control if control else self.bulk).append(
            [number, int(reply.get("s") or 500), list(reply.get("h") or ()), memoryview(bytes(reply.get("b") or b"")),
             0])
        self.ready.set()

    def served(self, number: int) -> None:
        self.bulk.append([number, None, None, None, 0])
        self.ready.set()

    def _next(self) -> Optional[bytes]:
        """The next piece to write - a pushed message, else an act's answer's if one waits - or None for none."""
        if self.pushed:
            return self.pushed.popleft()
        while self.bulk and self.bulk[0][1] is None:
            self.through = self.bulk.popleft()[0]          # served, answered nothing: counted, and the next
        queue = self.control if self.control else self.bulk
        if not queue:
            return None
        entry = queue[0]
        number, status, headers, body, at = entry
        part = body[at:at + PIECE_BYTES]
        piece: dict = {"i": number, "b": bytes(part)}
        if at == 0:
            piece.update(s=status, h=[*headers, [THROUGH_HEADER, str(self.through)]])
        entry[4] = at + len(part)
        if entry[4] < len(body):
            piece["more"] = True
        else:
            queue.popleft()
            if queue is self.bulk:
                self.through = number
        return msgpack_io.pack(piece)

    async def run(self, send: Callable, closed: asyncio.Event) -> None:
        """Write what is put here, a piece at a time, until the stream is closed."""
        while not closed.is_set():
            data = self._next()
            if data is None:
                self.ready.clear()
                await self.ready.wait()
                continue
            try:
                await send({"type": "websocket.send", "bytes": data})
            except Exception:  # noqa: BLE001 - the robot went: nothing more goes back
                closed.set()
                return


class StreamIntake:
    """
    ASGI middleware: a WebSocket to GET /stream, its messages served as requests by `app`, the rest of the server's app
    (the module's docstring); every other request passed on to `app` as it is.

    app         the server's ASGI app, which serves each request of the stream as it serves one over HTTP
    headers     what the upgrade's answer carries, as (name, value) bytes - or what returns them, read as each stream is
                accepted: FORMAT in X-Seq-Act-Formats among them
    authorized  given the upgrade's scope, whether it may open: False answers the upgrade 403. None: every one may (each
                request it carries is still checked by the app, the connection's Authorization on it)
    carried     the connection's headers each request on it carries, lowercased bytes: CARRIED unless given
    opened      called with the scope once a stream is accepted
    told        called with (the scope, the message, its size) for each message of the robot's that is no request,
                {"t": ...} - a heartbeat - as it comes; nothing answers it
    on_stream   called with (the scope, push) once a stream is accepted - push(message) sends the robot a message of
                its own, whole, ahead of every answer, from any thread - and returning what to call as the stream ends,
                or None
    None of them may hold the stream up.
    """

    def __init__(self, app: Any, *, headers: Any = (), authorized: Optional[Callable[[dict], bool]] = None,
                 carried: tuple = CARRIED, opened: Optional[Callable[[dict], None]] = None,
                 told: Optional[Callable[[dict, dict, int], None]] = None,
                 on_stream: Optional[Callable[[dict, Callable[[dict], None]], Any]] = None) -> None:
        self.app, self.headers, self.authorized = app, headers, authorized
        self.carried, self.opened, self.told, self.on_stream = tuple(carried), opened, told, on_stream

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope.get("type") != "websocket" or scope.get("path") != PATH:
            return await self.app(scope, receive, send)
        if (await receive()).get("type") != "websocket.connect":
            return
        if self.authorized is not None and not self.authorized(scope):
            await send({"type": "websocket.close", "code": 1008})          # refused: the upgrade answered 403
            return
        said = self.headers() if callable(self.headers) else self.headers
        await send({"type": "websocket.accept", "headers": list(said)})
        if self.opened is not None:
            self.opened(scope)
        carried = [(k, v) for k, v in scope.get("headers") or [] if k in self.carried]
        closed, acting, outbox = asyncio.Event(), set(), _Outbox()
        queue: asyncio.Queue = asyncio.Queue(maxsize=QUEUED)
        ended = self.on_stream(scope, outbox.push) if self.on_stream is not None else None

        async def serve(request: dict) -> dict:
            try:
                return await self._serve(scope, carried, request, closed)
            except Exception as exc:  # noqa: BLE001 - the app's own error, answered as a 500 over HTTP would be
                return {"s": 500, "h": [], "b": f"{type(exc).__name__}: {exc}"[:500].encode()}

        async def act(number: int, request: dict) -> None:
            outbox.answer(number, await serve(request), control=True)

        async def in_turn() -> None:
            """The stream's queue: every request but an act, served one after another in the order it came."""
            while True:
                number, request, route = await queue.get()
                if route[1] == _END and acting:
                    await asyncio.gather(*list(acting), return_exceptions=True)   # its act first, as over HTTP
                reply = await serve(request)
                if route in _SILENT and 200 <= int(reply.get("s") or 500) < 300:
                    outbox.served(number)
                else:
                    outbox.answer(number, reply, control=False)

        writer = asyncio.ensure_future(outbox.run(send, closed))
        server = asyncio.ensure_future(in_turn())
        parts: dict = {}
        try:
            while not closed.is_set():
                message = await receive()
                if message.get("type") == "websocket.disconnect":
                    break
                data = message.get("bytes")
                try:
                    piece = msgpack_io.unpack(data) if data is not None else None
                    if isinstance(piece, dict) and "i" not in piece and "t" in piece:
                        if self.told is not None:  # no request (a heartbeat): nothing answers it, no number goes by
                            self.told(scope, piece, len(data))
                        continue
                    number = int(piece["i"])
                    if number not in parts:
                        parts[number] = [str(piece["m"]).upper(), str(piece["p"]), piece.get("h") or (), []]
                    parts[number][3].append(bytes(piece.get("b") or b""))
                except Exception:  # noqa: BLE001 - one that does not read is answered so, and the next is read
                    outbox.answer(-1, {"s": 400, "h": [], "b": b"a message on the stream is a piece of a request: "
                                                                b"msgpack {i, m, p, h, b, more}"}, control=True)
                    continue
                if piece.get("more"):
                    continue
                method, path, headers, chunks = parts.pop(number)
                request = {"m": method, "p": path, "h": headers, "b": b"".join(chunks)}
                route = (method, path.split("?", 1)[0])
                if route in _ON_A_TASK:
                    task = asyncio.ensure_future(act(number, request))
                    acting.add(task)
                    task.add_done_callback(acting.discard)
                    continue
                await queue.put((number, request, route))
        finally:
            closed.set()
            if ended is not None:
                ended()
            outbox.ready.set()
            server.cancel()
            await asyncio.gather(writer, server, return_exceptions=True)

    async def _serve(self, ws_scope: dict, carried: list, request: dict, closed: asyncio.Event) -> dict:
        """One request of the stream served by the app as it comes over HTTP/1.1, its answer whole."""
        path, _, query = str(request["p"]).partition("?")
        own = [(str(k).lower().encode("latin-1"), str(v).encode("latin-1")) for k, v in request.get("h") or ()]
        own = [(k, v) for k, v in own if k not in _FRAMING]
        named = {k for k, _ in own}
        body = bytes(request.get("b") or b"")
        headers = [*own, *((k, v) for k, v in carried if k not in named), (b"content-length", str(len(body)).encode())]
        scope = {k: v for k, v in ws_scope.items() if k not in ("subprotocols", "extensions", "state")}
        scope.update({"type": "http", "http_version": "1.1", "method": str(request["m"]).upper(),
                      "scheme": "https" if ws_scope.get("scheme") == "wss" else "http", "path": path,
                      "raw_path": path.encode(), "query_string": query.encode(), "headers": headers})
        if "state" in ws_scope:
            scope["state"] = dict(ws_scope["state"])
        handed = False

        async def receive() -> dict:
            nonlocal handed
            if not handed:
                handed = True
                return {"type": "http.request", "body": body, "more_body": False}
            await closed.wait()                 # the request's client is there until the connection ends
            return {"type": "http.disconnect"}

        status, answered, chunks = 500, [], []

        async def respond(message: dict) -> None:
            nonlocal status, answered
            if message["type"] == "http.response.start":
                status, answered = int(message["status"]), list(message.get("headers") or ())
            elif message["type"] == "http.response.body":
                chunks.append(message.get("body", b""))

        await self.app(scope, receive, respond)
        return {"s": status, "h": [[k.decode("latin-1"), v.decode("latin-1")] for k, v in answered],
                "b": b"".join(chunks)}
