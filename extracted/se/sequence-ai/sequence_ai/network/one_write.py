# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
Each HTTP response leaves a uvicorn server in one write.

    import uvicorn
    from sequence_ai.network.one_write import WholeResponse, one_write_http

    uvicorn.run(WholeResponse(app), http=one_write_http())

uvicorn writes a response in pieces: the status line and headers when the app sends `http.response.start`, then the
body, then the end of the message. A tunnel or proxy in front of the server can hold back every piece after the first
until the client has acknowledged the first, so each request takes one round trip more than it needs: a 2-byte GET took
twice the TCP round-trip time (RTT), and a response written whole took one. Measured behind such a tunnel, with a TCP
connect p50 of 89.5 ms: headers then body, with TCP_NODELAY set, GET p50 189.7 ms; the same response in one write, GET
p50 106.7 ms. The probes put the same server behind the same tunnel, one write against two, and only the number of
writes changed the time; why the tunnel holds the second piece is inferred from these measurements, not read from its
source. Not measured on a direct connection.

So the protocol uvicorn runs is given a transport that collects what is written to it during one iteration of the event
loop and sends it as one write at the next: a response's start, body and end are written one after another with nothing
awaited in between, so they are sent together, as one TLS record on a TLS server. A streamed response is still sent one
body message at a time, each one iteration later. Middleware that passes a response on between tasks (Starlette's
BaseHTTPMiddleware) separates its start from its body again: WholeResponse, the outermost middleware, holds the start
until the first body message.
"""
from __future__ import annotations

import asyncio
from typing import Iterable


class OneWriteTransport:
    """An asyncio transport that sends everything written to it within one iteration of the event loop as one write to
    the transport it wraps. Everything else (reading, closing, the peer's address, flow control) is delegated to the
    wrapped transport."""

    def __init__(self, transport: asyncio.Transport, loop: asyncio.AbstractEventLoop) -> None:
        self._transport, self._loop = transport, loop
        self._pending: list[bytes] = []

    def write(self, data: bytes) -> None:
        """Buffer `data` with what this iteration of the event loop already wrote: all of it is sent in one write."""
        # Nothing to send (h11 ends a Content-Length body with b""): no flush is scheduled for it.
        if not data:
            return
        # The first write of an iteration schedules the one flush; later writes only join it.
        if not self._pending:
            self._loop.call_soon(self._flush)
        self._pending.append(bytes(data))

    def writelines(self, chunks: Iterable[bytes]) -> None:
        """Buffer each chunk, as write() does."""
        for chunk in chunks:
            self.write(chunk)

    def _flush(self) -> None:
        """Send what was buffered as one write; it is dropped when the connection is already closing."""
        if not self._pending:
            return
        data, self._pending = b"".join(self._pending), []
        if not self._transport.is_closing():
            self._transport.write(data)

    def close(self) -> None:
        """Send what was written, then close the connection."""
        # A response that closes its connection (Connection: close, a 400) is sent before the connection closes.
        self._flush()
        self._transport.close()

    def abort(self) -> None:
        """Drop what was buffered and abort the connection."""
        # An abort sends nothing more.
        self._pending.clear()
        self._transport.abort()

    def get_write_buffer_size(self) -> int:
        """Bytes waiting to be sent: the wrapped transport's own and what is buffered here."""
        # uvicorn's flow control reads how much is waiting to be sent: what is buffered here counts too.
        return self._transport.get_write_buffer_size() + sum(len(p) for p in self._pending)

    def __getattr__(self, name: str):
        # get_extra_info, is_closing, pause_reading, resume_reading, ...: the wrapped transport's own.
        return getattr(self._transport, name)


class WholeResponse:
    """ASGI middleware, the outermost of an app's: a response's start is held until its first body message, and both are
    passed on one after the other in the same iteration of the event loop, so the one-write transport sends them as one
    write.
    WHY: an app's BaseHTTPMiddleware layers pass a response on through a stream between tasks, so its start and its body
    reach uvicorn in two iterations and are sent in two writes; a tunnel then holds the second until the first is
    acknowledged, which costs the round trip the transport above was written to save. Measured through a tunnel at an
    RTT of about 190 ms: an 8-byte echo took 188 to 193 ms, a bare uvicorn app's GET 191 to 195 ms, and the same GET
    through such layers 377.7 ms; on localhost that GET was sent in 2 writes (182 + 79 bytes). The writes were counted,
    and the round trips were measured with one server against the other on the same tunnel."""

    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        if scope.get("type") != "http":
            return await self.app(scope, receive, send)
        held = None

        async def whole(message) -> None:
            nonlocal held
            if message["type"] == "http.response.start":
                held = message
                return
            if held is not None:
                start, held = held, None
                await send(start)               # uvicorn writes it at once: the body joins it in this iteration
            await send(message)

        await self.app(scope, receive, whole)
        if held is not None:                    # a response that ended with no body message: its start is sent alone
            await send(held)


def one_write_http() -> type[asyncio.Protocol]:
    """The HTTP protocol uvicorn would select by itself (its "auto": httptools when installed, else h11), with each
    connection writing through a OneWriteTransport. Pass it as uvicorn.Config(http=...)."""
    try:
        from uvicorn.protocols.http.auto import AutoHTTPProtocol
    except ImportError as missing:
        raise ImportError("one_write_http() wraps uvicorn's HTTP protocol, and uvicorn is not installed: "
                          'pip install uvicorn') from missing

    from sequence_ai.network import tcp_link

    class OneWriteHTTPProtocol(AutoHTTPProtocol):  # type: ignore[misc, valid-type]
        def connection_made(self, transport) -> None:  # type: ignore[override]
            # Registered by its peer's address, so that a request on this connection can read its TCP_INFO and time its
            # upload by when its bytes arrived (tcp_link).
            self._sequence_ai_link = tcp_link.register(transport)
            # Every write the protocol makes for this connection (its responses, its 400s and 500s) goes through it.
            super().connection_made(OneWriteTransport(transport, asyncio.get_running_loop()))

        def data_received(self, data: bytes) -> None:
            if self._sequence_ai_link is not None:
                self._sequence_ai_link.came()
            super().data_received(data)

    return OneWriteHTTPProtocol
