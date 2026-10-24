"""A loopback HTTP proxy that forwards to ONE authenticated upstream proxy and
counts every byte that crosses it.

Why it exists: a paid proxy (DataImpulse, ~$1/GB) bills by traffic, and the
platform meters that traffic to points per run
(``common-docs/projects/cloud-computer/PLAN.md`` rulings 6 and 12). Chrome talks
to the upstream proxy itself when Playwright is handed ``proxy={server,
username, password}``, and then nothing on our side ever sees a byte count. So
the worker launches Chrome through THIS listener instead::

    meter = await MeteredUpstreamProxy.start("http://gw.example:823", user, password)
    launch_kwargs["proxy"] = {"server": meter.proxy_url}   # Chrome only
    ...
    meter.bytes_total  # what the heartbeat reports

Scope is Chrome alone: the listener binds ``127.0.0.1`` and only the browser is
launched through it, so a shell, an agent's coding traffic, or anything else on
the machine keeps the machine's own exit.

The two request shapes Chrome emits through a proxy are served, the same two the
residential :mod:`matrx_scraper.egress_adapter` serves:

* ``CONNECT host:port`` (every HTTPS request) — the head is forwarded with a
  ``Proxy-Authorization`` header added, then bytes are piped both ways.
* An absolute-URL request (plain HTTP) — forwarded the same way, with
  ``Connection: close`` so a reused connection never sends an unauthenticated
  second request.

🚨 The credentials are never logged and never echoed into an error message.
"""

from __future__ import annotations

import asyncio
import base64
import logging
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)

#: Largest request head this proxy reads from Chrome before refusing.
MAX_REQUEST_HEAD_BYTES = 64 * 1024
READ_CHUNK_BYTES = 64 * 1024

_DROPPED_HEADERS = frozenset({"proxy-authorization", "proxy-connection", "connection", "keep-alive"})


class MeteredUpstreamProxy:
    """Loopback listener → one upstream HTTP proxy, with a running byte count."""

    def __init__(self, upstream_host: str, upstream_port: int, authorization: str | None) -> None:
        self._upstream_host = upstream_host
        self._upstream_port = upstream_port
        self._authorization = authorization
        self._server: asyncio.AbstractServer | None = None
        self._port: int | None = None
        self._connections: set[asyncio.Task[None]] = set()
        self._closed = False
        #: Bytes sent to plus received from the upstream proxy, since start.
        self.bytes_total = 0
        #: Connections opened through the upstream. Evidence, never a guess.
        self.connections_opened = 0

    @classmethod
    async def start(
        cls, upstream: str, username: str | None = None, password: str | None = None
    ) -> MeteredUpstreamProxy:
        """Bind ``127.0.0.1:<ephemeral>``. Never binds 0.0.0.0."""
        parts = urlsplit(upstream if "://" in upstream else f"http://{upstream}")
        if parts.scheme not in {"http", ""} or not parts.hostname:
            raise ValueError("the metered proxy needs an http://host:port upstream")
        user = username if username is not None else parts.username
        secret = password if password is not None else parts.password
        authorization = None
        if user is not None and secret is not None:
            token = base64.b64encode(f"{user}:{secret}".encode()).decode("ascii")
            authorization = f"Basic {token}"
        proxy = cls(parts.hostname, int(parts.port or 80), authorization)
        proxy._server = await asyncio.start_server(proxy._handle_client, host="127.0.0.1", port=0)
        sockets = proxy._server.sockets or ()
        if not sockets:
            await proxy.close()
            raise RuntimeError("the metered proxy could not bind a local port")
        listening_port = int(sockets[0].getsockname()[1])
        proxy._port = listening_port
        logger.info("metered upstream proxy listening on 127.0.0.1:%s", listening_port)
        return proxy

    @property
    def proxy_url(self) -> str:
        if self._port is None:
            raise RuntimeError("the metered proxy is not started")
        return f"http://127.0.0.1:{self._port}"

    async def close(self) -> None:
        """Stop listening and end every connection in flight. Idempotent."""
        if self._closed:
            return
        self._closed = True
        for task in list(self._connections):
            task.cancel()
        if self._connections:
            await asyncio.gather(*self._connections, return_exceptions=True)
        if self._server is not None:
            self._server.close()
            try:
                await asyncio.wait_for(self._server.wait_closed(), timeout=5)
            except TimeoutError:
                logger.warning("metered proxy listener did not close within 5 s")

    # ── serving ────────────────────────────────────────────────────────────

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        task = asyncio.current_task()
        if task is not None:
            self._connections.add(task)
        try:
            await self._serve_one(reader, writer)
        except (asyncio.CancelledError, ConnectionError, asyncio.IncompleteReadError):
            pass
        except Exception:
            logger.exception("metered proxy connection failed")
        finally:
            if task is not None:
                self._connections.discard(task)
            writer.close()

    async def _serve_one(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        try:
            head = await reader.readuntil(b"\r\n\r\n")
        except asyncio.LimitOverrunError:
            await _write_error(writer, 431, "Request head too large.")
            return
        if len(head) > MAX_REQUEST_HEAD_BYTES:
            await _write_error(writer, 431, "Request head too large.")
            return
        rebuilt = self._rebuild_head(head)
        if rebuilt is None:
            await _write_error(writer, 400, "Malformed proxy request.")
            return
        try:
            # The OS connect timeout bounds this; Chrome's own request timeout
            # bounds the page.
            up_reader, up_writer = await asyncio.open_connection(
                self._upstream_host, self._upstream_port
            )
        except (OSError, TimeoutError):
            await _write_error(writer, 502, "The paid proxy could not be reached.")
            return
        self.connections_opened += 1
        try:
            up_writer.write(rebuilt)
            self.bytes_total += len(rebuilt)
            await up_writer.drain()
            await asyncio.gather(
                self._pipe(reader, up_writer), self._pipe(up_reader, writer)
            )
        finally:
            up_writer.close()

    def _rebuild_head(self, head: bytes) -> bytes | None:
        text = head.decode("latin-1")
        lines = text.split("\r\n")
        request_line = lines[0]
        parts = request_line.split(" ")
        if len(parts) != 3:
            return None
        method = parts[0].upper()
        headers = [
            line
            for line in lines[1:]
            if line and line.split(":", 1)[0].strip().lower() not in _DROPPED_HEADERS
        ]
        if method != "CONNECT":
            headers.append("Connection: close")
        if self._authorization is not None:
            headers.append(f"Proxy-Authorization: {self._authorization}")
        return ("\r\n".join([request_line, *headers]) + "\r\n\r\n").encode("latin-1")

    async def _pipe(self, source: asyncio.StreamReader, sink: asyncio.StreamWriter) -> None:
        try:
            while True:
                chunk = await source.read(READ_CHUNK_BYTES)
                if not chunk:
                    break
                self.bytes_total += len(chunk)
                sink.write(chunk)
                await sink.drain()
        except (ConnectionError, asyncio.CancelledError):
            pass
        finally:
            try:
                if sink.can_write_eof():
                    sink.write_eof()
            except (OSError, RuntimeError):
                pass


async def _write_error(writer: asyncio.StreamWriter, status: int, sentence: str) -> None:
    body = sentence.encode("utf-8")
    writer.write(
        f"HTTP/1.1 {status} Proxy Error\r\nContent-Type: text/plain; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n".encode("ascii")
        + body
    )
    try:
        await writer.drain()
    except ConnectionError:
        pass
