"""Native asyncio HTTP/1.1 with keep-alive reuse and cancellation that closes the connection at once."""

from __future__ import annotations

import ssl
import time
from collections.abc import AsyncIterable, AsyncIterator, Awaitable, Iterable, Mapping
from contextlib import asynccontextmanager

from labqoat.net.async_connection import AsyncBody, AsyncConnection
from labqoat.net.headers import Headers
from labqoat.net.request import AsyncHandler, Request
from labqoat.net.response import Response
from labqoat.net.transport_trust import TransportTrust
from labqoat.net.url import Url

Fields = Mapping[str, str] | Iterable[tuple[str, str]] | None


class AsyncHttpClient:
    """Send requests from one event loop; a connection returns to the pool only after its answer ended cleanly.

    Nothing is followed, retried or taken from the environment. A cancelled request closes its connection.
    HTTPS verifies against ``context``, the ``certifi`` bundle by default. ``connect_timeout`` bounds opening
    a connection when ``timeout``, which bounds every later wait, is longer or absent.
    """

    IDLE_SECONDS = 20.0

    def __init__(
        self,
        base_url: str = "",
        *,
        headers: Fields = None,
        timeout: float | None = 30.0,
        connect_timeout: float | None = None,
        context: ssl.SSLContext | None = None,
        unix_socket: str | None = None,
        handler: AsyncHandler | None = None,
    ) -> None:
        """Configure where relative paths go and what every request carries, without connecting."""
        self._base = base_url.rstrip("/")
        self._headers = Headers(headers)
        self._timeout = timeout
        self._connect_timeout = timeout if connect_timeout is None else connect_timeout
        self._context = context
        self._socket = unix_socket
        self._handler = handler
        self._idle: dict[tuple[str, str, int | None], list[AsyncConnection]] = {}
        self.is_closed = False

    async def request(
        self,
        method: str,
        url: str,
        *,
        content: AsyncBody = None,
        headers: Fields = None,
        params: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> Response:
        """Send one request and read its whole answer; ``timeout`` overrides the client's for this request."""
        async with self.stream(
            method, url, content=content, headers=headers, params=params, timeout=timeout
        ) as response:
            await response.aread()
        return response

    @asynccontextmanager
    async def stream(
        self,
        method: str,
        url: str,
        *,
        content: AsyncBody = None,
        headers: Fields = None,
        params: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> AsyncIterator[Response]:
        """Send one request and yield its answer with the body still to read; leaving early drops the connection."""
        target = Url.parse(url if "://" in url else self._base + url, params)
        fields = self._headers.merged(headers)
        wait = self._timeout if timeout is None else timeout
        if self._handler is not None:
            request = Request(method, target, fields, await self._joined(content), wait)
            answered = await self._answered(self._handler, request)
            answered.request = answered.request or request
            try:
                yield answered
            finally:
                await answered.aclose()
            return
        connection = await self._connection(target)
        try:
            await connection.send(method, target, fields, content, wait)
            status, received, body = await connection.receive(method, wait)
            response = Response(status, headers=received.multi_items(), stream=body)
            try:
                yield response
            finally:
                await response.aclose()
        finally:
            self._settle(target, connection)

    async def aclose(self) -> None:
        """Close every idle connection; a later request opens new ones."""
        self.is_closed = True
        idle, self._idle = self._idle, {}
        for connections in idle.values():
            for connection in connections:
                connection.close()

    async def __aenter__(self) -> AsyncHttpClient:
        """Use the client for a block."""
        return self

    async def __aexit__(self, exc_type: object, exc: object, traceback: object) -> None:
        """Close the client after a block."""
        await self.aclose()

    async def _connection(self, target: Url) -> AsyncConnection:
        """Reuse a recent idle connection the server has not closed, or open a new one."""
        idle = self._idle.get((target.scheme, target.host, target.port), [])
        while idle:
            connection = idle.pop()
            fresh = time.monotonic() - connection.idle_since < self.IDLE_SECONDS
            if fresh and not connection.reader.at_eof() and not connection.writer.is_closing():
                return connection
            connection.close()
        context = None
        if target.scheme == "https":
            context = self._context or TransportTrust.bundled()
        return await AsyncConnection.open(target, self._socket, context, self._connect_timeout)

    def _settle(self, target: Url, connection: AsyncConnection) -> None:
        """Keep a connection whose answer ended cleanly; close any other."""
        if not connection.reusable:
            connection.close()
            return
        connection.reusable = False
        connection.idle_since = time.monotonic()
        self._idle.setdefault((target.scheme, target.host, target.port), []).append(connection)

    @staticmethod
    async def _answered(handler: AsyncHandler, request: Request) -> Response:
        """A handler's answer, awaited when the handler is asynchronous."""
        answered = handler(request)
        return await answered if isinstance(answered, Awaitable) else answered

    @staticmethod
    async def _joined(content: AsyncBody) -> bytes:
        """The whole body a handler sees."""
        if content is None or isinstance(content, bytes):
            return content or b""
        if isinstance(content, AsyncIterable):
            return b"".join([chunk async for chunk in content])
        raise TypeError("An asynchronous request body must be bytes or an asynchronous iterable")
