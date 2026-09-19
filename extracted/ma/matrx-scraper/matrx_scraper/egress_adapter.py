"""The consumer side of residential egress: a loopback HTTP proxy that tunnels
each TCP connection over one WebSocket to the AI Matrx gateway.

Contract (the ONE source of truth for every repo):
`common-docs/systems/platform/residential-egress/FEATURE.md` § "The consumer-side
adapter". The gateway, the device leg and the helper binary live in other repos;
this module knows only two strings — a ticket and a consume URL — and turns them
into something httpx and Playwright already know how to use::

    adapter = await EgressAdapter.start(ticket, consume_url)
    try:
        response = await fetch(url, proxy=adapter.proxy_url)      # httpx / curl_cffi
        ...  # or Playwright: proxy={"server": adapter.proxy_url}
    finally:
        await adapter.close()

Why a local proxy rather than a transport plugin: every client we already use
(httpx, curl_cffi, Playwright, the browser pool) speaks `http://host:port` proxy
configuration, and none of them speak WebSocket tunnels. One loopback listener
makes the person's own computer look exactly like the datacenter proxy pool to
every caller, with no second code path to keep in step.

Two proxy shapes are served, which is all any of those clients emit:

* ``CONNECT host:port`` — every HTTPS request. Answered with
  ``HTTP/1.1 200 Connection Established`` once the gateway says the stream is
  open, and refused with a plain-English ``502`` when it is not.
* An absolute-URL request line (``GET http://example.com/a HTTP/1.1``) — plain
  HTTP. Rewritten to origin form and relayed to port 80 (or the URL's own port).

🚨 **The ticket is a bearer credential and is never logged, never put in a URL
query, and never repeated in an error message.** It travels only in the
`Authorization` header of the consumer WebSocket.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any
from urllib.parse import urlsplit, urlunsplit

logger = logging.getLogger(__name__)

#: Largest request head (request line + headers) this proxy will read from a
#: local client before giving up. A local client that sends more than this is
#: not one of ours.
MAX_REQUEST_HEAD_BYTES = 64 * 1024

#: Bytes read from the local socket per WebSocket frame. Matches the wire
#: protocol's own DATA cap so a frame is never split by the gateway.
READ_CHUNK_BYTES = 64 * 1024

#: How long the gateway has to answer the opening `{"ok":…}` before we give up.
OPEN_TIMEOUT_SECONDS = 30.0

#: Protocol version header, v1 of the contract.
EGRESS_PROTOCOL_HEADER = "X-Matrx-Egress-Protocol"
EGRESS_PROTOCOL_VERSION = "1"

_HOP_BY_HOP_REQUEST_HEADERS = frozenset(
    {"proxy-connection", "proxy-authorization", "connection", "keep-alive", "te", "upgrade"}
)


class EgressUnavailableError(RuntimeError):
    """The gateway refused to open a stream. Carries the gateway's sentence."""

    def __init__(self, error: str, message: str) -> None:
        super().__init__(message or error)
        self.error = error
        self.message = message or error


def _require_websockets() -> Any:
    """The websockets client, or a failure that says exactly what to install."""
    try:
        from websockets.asyncio.client import connect as ws_connect
    except ImportError as exc:  # pragma: no cover — declared dependency
        raise RuntimeError(
            "Residential egress needs the 'websockets' package, which this "
            "install does not have. Install matrx-scraper's dependencies "
            "(pip install 'matrx-scraper') and try again."
        ) from exc
    return ws_connect


def _consume_uri(consume_url: str, host: str, port: int) -> str:
    """The consumer URL for one stream. `host`/`port` only — never the ticket."""
    from urllib.parse import quote

    parts = urlsplit(consume_url)
    query = parts.query
    extra = f"host={quote(host, safe='')}&port={int(port)}"
    query = f"{query}&{extra}" if query else extra
    return urlunsplit((parts.scheme, parts.netloc, parts.path, query, ""))


class EgressAdapter:
    """A loopback HTTP proxy whose exit is the person's own computer.

    Created only through :meth:`start`; a bare constructor would leave a
    listener half-built. Every accepted connection is one WebSocket to the
    gateway and one TCP stream on the device.
    """

    def __init__(self, ticket: str, consume_url: str) -> None:
        self._ticket = ticket
        self._consume_url = consume_url
        self._server: asyncio.AbstractServer | None = None
        self._port: int | None = None
        self._connections: set[asyncio.Task[None]] = set()
        self._closed = False
        #: The computer's display name, as the gateway names it on the first
        #: stream. `None` until a stream has actually opened.
        self.device_name: str | None = None
        #: How many streams this adapter opened. Evidence, never a guess.
        self.streams_opened = 0

    # ── lifecycle ──────────────────────────────────────────────────────────

    @classmethod
    async def start(cls, ticket: str, consume_url: str) -> EgressAdapter:
        """Bind `127.0.0.1:<ephemeral>` and start serving. Never binds 0.0.0.0."""
        if not ticket:
            raise ValueError("an egress adapter needs a ticket")
        if not consume_url:
            raise ValueError("an egress adapter needs a consume url")
        adapter = cls(ticket, consume_url)
        adapter._server = await asyncio.start_server(
            adapter._handle_client, host="127.0.0.1", port=0
        )
        sockets = adapter._server.sockets or ()
        if not sockets:
            await adapter.close()
            raise RuntimeError("the egress adapter could not bind a local port")
        adapter._port = int(sockets[0].getsockname()[1])
        logger.info("residential egress adapter listening on 127.0.0.1:%s", adapter._port)
        return adapter

    @property
    def port(self) -> int:
        if self._port is None:
            raise RuntimeError("the egress adapter is not started")
        return self._port

    @property
    def proxy_url(self) -> str:
        """What httpx (`proxy=`) and Playwright (`proxy={"server": …}`) take."""
        return f"http://127.0.0.1:{self.port}"

    async def close(self) -> None:
        """Stop listening and end every stream still in flight. Idempotent."""
        if self._closed:
            return
        self._closed = True
        # Streams first, THEN the listener. `Server.wait_closed()` waits for
        # every handler task to finish (Python 3.12.1+), so closing the listener
        # while a tunnel is still piping deadlocks the caller forever — which is
        # exactly what `await adapter.close()` looked like in the first draft.
        current = asyncio.current_task()
        tasks = [task for task in self._connections if task is not current]
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        self._connections.clear()
        if self._server is not None:
            self._server.close()
            try:
                await self._server.wait_closed()
            except Exception:  # noqa: BLE001 — closing never raises upward
                logger.debug("egress adapter server close raised", exc_info=True)

    async def __aenter__(self) -> EgressAdapter:
        return self

    async def __aexit__(self, *_exc: Any) -> None:
        await self.close()

    # ── one local connection ───────────────────────────────────────────────

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        task = asyncio.current_task()
        if task is not None:
            self._connections.add(task)
        try:
            await self._serve_one(reader, writer)
        except asyncio.CancelledError:
            raise
        except Exception:  # noqa: BLE001 — one bad connection never stops the proxy
            logger.warning("egress adapter connection failed", exc_info=True)
        finally:
            if task is not None:
                self._connections.discard(task)
            try:
                writer.close()
            except Exception:  # noqa: BLE001
                pass

    async def _serve_one(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        head = await self._read_head(reader)
        if head is None:
            await _write_error(writer, 400, "The request to this local proxy was not readable.")
            return

        request_line, headers, leftover = head
        parts = request_line.split()
        if len(parts) < 3:
            await _write_error(writer, 400, "The request to this local proxy was not readable.")
            return
        method, target, version = parts[0], parts[1], parts[2]

        if method.upper() == "CONNECT":
            host, port = _split_authority(target, default_port=443)
            if not host:
                await _write_error(writer, 400, "The CONNECT target had no host in it.")
                return
            await self._tunnel(
                reader,
                writer,
                host=host,
                port=port,
                first_bytes=b"",
                on_open=b"HTTP/1.1 200 Connection Established\r\n\r\n",
            )
            return

        # Absolute-URL plain HTTP: rewrite to origin form for the real server.
        parsed = urlsplit(target)
        if not parsed.scheme or not parsed.netloc:
            await _write_error(
                writer,
                400,
                "This is a proxy: a plain HTTP request must carry the full address.",
            )
            return
        if parsed.scheme.lower() != "http":
            await _write_error(
                writer, 400, f"This proxy does not serve {parsed.scheme} requests directly."
            )
            return
        host, port = _split_authority(parsed.netloc, default_port=80)
        if not host:
            await _write_error(writer, 400, "The request address had no host in it.")
            return
        origin_form = urlunsplit(("", "", parsed.path or "/", parsed.query, "")) or "/"
        rebuilt = _rebuild_request(
            method=method,
            origin_form=origin_form,
            version=version,
            headers=headers,
            authority=parsed.netloc,
        )
        await self._tunnel(
            reader,
            writer,
            host=host,
            port=port,
            first_bytes=rebuilt + leftover,
            on_open=b"",
        )

    async def _read_head(
        self, reader: asyncio.StreamReader
    ) -> tuple[str, list[tuple[str, str]], bytes] | None:
        """Request line + headers, plus whatever body bytes arrived with them."""
        buffer = b""
        while b"\r\n\r\n" not in buffer:
            if len(buffer) > MAX_REQUEST_HEAD_BYTES:
                return None
            chunk = await reader.read(READ_CHUNK_BYTES)
            if not chunk:
                return None
            buffer += chunk
        head, _, leftover = buffer.partition(b"\r\n\r\n")
        lines = head.decode("latin-1").split("\r\n")
        request_line = lines[0]
        headers: list[tuple[str, str]] = []
        for line in lines[1:]:
            name, sep, value = line.partition(":")
            if sep:
                headers.append((name.strip(), value.strip()))
        return request_line, headers, leftover

    # ── one stream over the gateway ────────────────────────────────────────

    async def _tunnel(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        *,
        host: str,
        port: int,
        first_bytes: bytes,
        on_open: bytes,
    ) -> None:
        ws_connect = _require_websockets()
        uri = _consume_uri(self._consume_url, host, port)
        headers = {
            "Authorization": f"Bearer {self._ticket}",
            EGRESS_PROTOCOL_HEADER: EGRESS_PROTOCOL_VERSION,
        }
        try:
            connection = await asyncio.wait_for(
                ws_connect(uri, additional_headers=headers, max_size=None),
                timeout=OPEN_TIMEOUT_SECONDS,
            )
        except Exception as exc:  # noqa: BLE001 — the local client gets a sentence
            logger.warning(
                "residential egress could not reach the gateway for %s:%s (%s)",
                host,
                port,
                type(exc).__name__,
            )
            await _write_error(
                writer,
                502,
                "We could not reach the home connection gateway for this page.",
            )
            return

        try:
            try:
                greeting = await asyncio.wait_for(
                    connection.recv(), timeout=OPEN_TIMEOUT_SECONDS
                )
            except Exception as exc:  # noqa: BLE001
                raise EgressUnavailableError(
                    "no_greeting",
                    "The home connection gateway did not answer this request.",
                ) from exc
            opened = _read_greeting(greeting)
            self.streams_opened += 1
            if opened.get("device_name"):
                self.device_name = str(opened["device_name"])

            if on_open:
                writer.write(on_open)
                await writer.drain()
            if first_bytes:
                await connection.send(first_bytes)

            await self._pipe(reader, writer, connection)
        except EgressUnavailableError as exc:
            logger.info(
                "residential egress refused a stream to %s:%s (%s)", host, port, exc.error
            )
            await _write_error(writer, 502, exc.message)
        finally:
            try:
                await connection.close()
            except Exception:  # noqa: BLE001
                pass

    async def _pipe(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        connection: Any,
    ) -> None:
        """Bytes both ways until either end stops. Bounded in both directions:
        the socket leg drains before reading again, and the WebSocket leg is
        flow-controlled by the library's own receive buffer."""

        async def _socket_to_ws() -> None:
            while True:
                chunk = await reader.read(READ_CHUNK_BYTES)
                if not chunk:
                    return
                await connection.send(chunk)

        async def _ws_to_socket() -> None:
            async for message in connection:
                if isinstance(message, str):
                    # After the greeting every frame is binary. A TEXT frame
                    # here is the gateway ending the stream with a sentence.
                    logger.debug("egress gateway sent a text frame mid-stream")
                    return
                writer.write(message)
                await writer.drain()

        up = asyncio.create_task(_socket_to_ws())
        down = asyncio.create_task(_ws_to_socket())
        try:
            done, pending = await asyncio.wait(
                {up, down}, return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)
            for task in done:
                exc = task.exception()
                if exc is not None:
                    logger.debug("egress stream ended: %s", type(exc).__name__)
        finally:
            for task in (up, down):
                if not task.done():
                    task.cancel()
            try:
                writer.close()
            except Exception:  # noqa: BLE001
                pass


def _read_greeting(greeting: Any) -> dict[str, Any]:
    """The first TEXT frame, or a refusal carrying the gateway's own sentence."""
    if isinstance(greeting, bytes | bytearray):
        greeting = bytes(greeting).decode("utf-8", "replace")
    try:
        payload = json.loads(greeting)
    except Exception as exc:  # noqa: BLE001
        raise EgressUnavailableError(
            "bad_greeting", "The home connection gateway answered something we could not read."
        ) from exc
    if not isinstance(payload, dict) or not payload.get("ok"):
        error = str((payload or {}).get("error") or "refused")
        message = str(
            (payload or {}).get("message")
            or "The home computer could not open this connection."
        )
        raise EgressUnavailableError(error, message)
    return payload


def _split_authority(authority: str, *, default_port: int) -> tuple[str, int]:
    """`host:port` → (host, port), IPv6 literals included."""
    value = authority.strip()
    if value.startswith("["):
        host, _, rest = value[1:].partition("]")
        port = rest[1:] if rest.startswith(":") else ""
        return host, int(port) if port.isdigit() else default_port
    host, sep, port = value.rpartition(":")
    if not sep:
        return value, default_port
    if not port.isdigit():
        return value, default_port
    return host, int(port)


def _rebuild_request(
    *,
    method: str,
    origin_form: str,
    version: str,
    headers: list[tuple[str, str]],
    authority: str,
) -> bytes:
    lines = [f"{method} {origin_form} {version}"]
    seen_host = False
    for name, value in headers:
        lowered = name.lower()
        if lowered in _HOP_BY_HOP_REQUEST_HEADERS:
            continue
        if lowered == "host":
            seen_host = True
        lines.append(f"{name}: {value}")
    if not seen_host:
        lines.insert(1, f"Host: {authority}")
    return ("\r\n".join(lines) + "\r\n\r\n").encode("latin-1")


async def _write_error(writer: asyncio.StreamWriter, status: int, sentence: str) -> None:
    """A refusal a person could read, never a silent dropped socket."""
    reason = {400: "Bad Request", 502: "Bad Gateway"}.get(status, "Error")
    body = sentence.encode("utf-8")
    head = (
        f"HTTP/1.1 {status} {reason}\r\n"
        f"Content-Type: text/plain; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n\r\n"
    ).encode("latin-1")
    try:
        writer.write(head + body)
        await writer.drain()
    except Exception:  # noqa: BLE001 — the client may already be gone
        logger.debug("egress adapter could not write a refusal", exc_info=True)
