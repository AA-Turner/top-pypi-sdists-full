"""Blocking HTTP/1.1 with pooled keep-alive connections per origin."""

from __future__ import annotations

import http.client
import ssl
from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from functools import partial
from threading import Lock
from typing import TypeAlias

from labqoat.net.environment_proxy import EnvironmentProxy
from labqoat.net.failures import Failures
from labqoat.net.headers import Headers
from labqoat.net.http_connections import HttpConnections
from labqoat.net.http_error import HttpError
from labqoat.net.request import Handler, Request
from labqoat.net.response import Response
from labqoat.net.transport_trust import TransportTrust
from labqoat.net.unix_connection import UnixConnection
from labqoat.net.url import Url

Body: TypeAlias = bytes | Iterable[bytes] | None
Fields: TypeAlias = Mapping[str, str] | Iterable[tuple[str, str]] | None


class HttpClient:
    """Send requests and reuse a connection once its answer has been read in full.

    Nothing is followed or retried. A body without a declared length goes out chunked. HTTPS verifies against
    ``context``, the ``certifi`` bundle by default; only a client built with ``proxy`` honors ``HTTPS_PROXY``.
    A ``handler`` answers every request in place of the network.
    """

    READ_BYTES = 65_536

    def __init__(
        self,
        base_url: str = "",
        *,
        headers: Fields = None,
        timeout: float | None = 30.0,
        context: ssl.SSLContext | None = None,
        unix_socket: str | None = None,
        handler: Handler | None = None,
        proxy: bool = False,
    ) -> None:
        """Configure where relative paths go and what every request carries, without connecting."""
        self._base = base_url.rstrip("/")
        self._headers = Headers(headers)
        self._timeout = timeout
        self._context = context
        self._socket = unix_socket
        self._handler = handler
        self._proxy = proxy
        self._pools: dict[tuple[str, str, int | None], HttpConnections] = {}
        self._lock = Lock()

    def request(
        self,
        method: str,
        url: str,
        *,
        content: Body = None,
        headers: Fields = None,
        params: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> Response:
        """Send one request and read its whole answer; ``timeout`` overrides the client's for this request."""
        with self.stream(method, url, content=content, headers=headers, params=params, timeout=timeout) as response:
            response.read()
        return response

    @contextmanager
    def stream(
        self,
        method: str,
        url: str,
        *,
        content: Body = None,
        headers: Fields = None,
        params: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> Iterator[Response]:
        """Send one request and yield its answer with the body still to read; leaving early drops the connection."""
        target = Url.parse(url if "://" in url else self._base + url, params)
        fields = self._headers.merged(headers)
        if self._handler is not None:
            wait = self._timeout if timeout is None else timeout
            request = Request(method, target, fields, self._joined(content), wait)
            answered = self._handler(request)
            answered.request = answered.request or request
            try:
                yield answered
            finally:
                answered.close()
            return
        with self._pool(target).using() as connection:
            raw = self._send(connection, method, target, fields, content, timeout)
            response = Response(raw.status, headers=raw.getheaders(), stream=self._body(raw))
            try:
                yield response
            finally:
                response.close()
                if not raw.isclosed():
                    connection.close()

    def close(self) -> None:
        """Close every idle connection; a later request opens new ones."""
        with self._lock:
            pools, self._pools = list(self._pools.values()), {}
        for pool in pools:
            pool.close()

    def __enter__(self) -> HttpClient:
        """Use the client for a block."""
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        """Close the client after a block."""
        self.close()

    def _send(
        self,
        connection: http.client.HTTPConnection,
        method: str,
        target: Url,
        fields: Headers,
        content: Body,
        timeout: float | None,
    ) -> http.client.HTTPResponse:
        """Connect if needed, then send the request and read the answer's status and fields."""
        with Failures.translated():
            if connection.sock is None:
                connection.connect()
            connection.sock.settimeout(self._timeout if timeout is None else timeout)
            connection.request(method, target.target, body=content, headers=dict(fields.multi_items()))
            return connection.getresponse()

    def _body(self, raw: http.client.HTTPResponse) -> Iterator[bytes]:
        """Yield the body as each read returns it, so a stream of events arrives without waiting for a full buffer."""
        while True:
            with Failures.translated():
                chunk = raw.read1(self.READ_BYTES)
            if not chunk:
                break
            yield chunk
        if raw.length:
            raise HttpError("HTTP connection closed before the answer ended")

    def _pool(self, target: Url) -> HttpConnections:
        """The idle connections to the target's origin."""
        key = (target.scheme, target.host, target.port)
        with self._lock:
            pool = self._pools.get(key)
            if pool is None:
                pool = self._pools[key] = HttpConnections(partial(self._connection, target))
            return pool

    def _connection(self, target: Url) -> http.client.HTTPConnection:
        """A connection to the target's origin, through the socket, directly, or through the proxy."""
        if self._socket is not None:
            return UnixConnection(self._socket, target.authority, self._timeout)
        if target.scheme == "http":
            return http.client.HTTPConnection(target.host, target.port, timeout=self._timeout)
        context = self._context or TransportTrust.bundled()
        proxy = EnvironmentProxy.for_host(target.host) if self._proxy else None
        if proxy is None:
            return http.client.HTTPSConnection(target.host, target.port, timeout=self._timeout, context=context)
        connection = http.client.HTTPSConnection(proxy.host, proxy.port, timeout=self._timeout, context=context)
        connection.set_tunnel(target.host, target.port, headers=proxy.headers())
        return connection

    @staticmethod
    def _joined(content: Body) -> bytes:
        """The whole body a handler sees."""
        if content is None or isinstance(content, bytes):
            return content or b""
        return b"".join(content)
