# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2026 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
"""S3 part transfers through pyreqwest, a Rust HTTP client that releases the GIL.

With requests, every byte of a part passes through Python code that holds the GIL,
so a large transfer competes with the training loop that started it. pyreqwest
sends and receives in Rust and only takes the GIL to hand a chunk over.

Imported only when the transport is asked for and pyreqwest is installed; see
transport.get_s3_transport(). pyreqwest needs Python 3.11 or later.

Three things differ from requests and are handled here:

* **One client for the process.** A pyreqwest client is safe to share between
  threads and keeps its own connection pool, so every pool worker uses the same
  one instead of a session per thread. One is kept per combination of TLS
  settings, timeout and proxy environment variables.
* **fork().** pyreqwest runs on a Tokio runtime that cannot be used in a child
  forked after it started: a new client refuses to build, and the parent's
  panics. A transport used in such a child falls back to requests.
* **File parts are sent mapped.** A part of a file is sent from a memory mapping
  of its byte range, which pyreqwest takes without a copy, so the part needs the
  GIL once. Its progress then moves when it completes, not while it is sent.
  Windows, and files that cannot be mapped, stream the part in blocks instead.
* **Errors.** pyreqwest reports a failed connection, a timeout, a body cut off
  part way through, or a part body that could not be read as its own exception
  types. They are raised again as PyreqwestConnectionError, a ConnectionError,
  which is what the retry loops treat as a network failure, as requests does.
"""
import contextlib
import logging
import os
import threading
from datetime import timedelta
from typing import Any, Dict, Iterator, Mapping, Optional, Tuple, cast

from pyreqwest.client import SyncClient, SyncClientBuilder
from pyreqwest.exceptions import (
    ClientClosedError,
    RedirectError,
    RequestError,
    RequestPanicError,
    StatusError,
)

from ...connection import ca_certs
from .transport import RequestsTransport, S3Transport, TransportResponse, warn_once

LOGGER = logging.getLogger(__name__)

# How much of a streamed body pyreqwest may buffer ahead of the caller. As little as
# it allows, because whatever it holds when the connection drops is discarded, and
# because opening the response waits for the buffer to fill: a body cut off before
# that fails the request itself, losing even the bytes that did arrive. The
# kernel's socket buffer still keeps the connection busy while Python writes a
# chunk, so throughput is far above what one S3 connection delivers either way.
READ_AHEAD_BYTES = 1

# The block a file-backed part body is read in while it is being sent.
UPLOAD_CHUNK_BYTES = 1024 * 1024

# The environment variables requests reads a CA bundle from. comet_ml sets the
# first and the last itself when comet.include.custom_ca_bundle is configured.
CA_BUNDLE_ENVIRONMENT_VARIABLES = (
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    "SSL_CERT_FILE",
)

# The environment variables a client reads its proxies from, once, when it is built.
# requests reads them for every request, so a client is kept per combination of
# their values: a proxy set after the first transfer is used from the next one on.
PROXY_ENVIRONMENT_VARIABLES = tuple(
    variant
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY")
    for variant in (name, name.lower())
)

# pyreqwest errors that are not about the network, so retrying cannot help.
_NOT_NETWORK_ERRORS = (StatusError, RedirectError, RequestPanicError, ClientClosedError)


class PyreqwestConnectionError(ConnectionError):
    """A connection, timeout or body failure reported by pyreqwest.

    The original exception is the ``__cause__``.
    """


@contextlib.contextmanager
def _as_connection_errors() -> Iterator[None]:
    try:
        yield
    except _NOT_NETWORK_ERRORS:
        raise
    except RequestError as ex:
        # A body that ends early shows up as a bare RequestError or a
        # BodyDecodeError rather than a NetworkError, so everything not listed
        # above counts: none of it is fixed by giving up sooner.
        raise PyreqwestConnectionError(str(ex)) from ex


class PyreqwestTransport(S3Transport):
    """The S3Transport built on pyreqwest.

    Falls back to requests, for good, when no client can be built: a CA bundle
    that cannot be read, a TLS backend that fails to start, or a process forked
    after pyreqwest started.
    """

    def __init__(
        self,
        verify_tls: bool = True,
        custom_ca_bundle: Optional[str] = None,
        fallback: Optional[S3Transport] = None,
    ):
        """``custom_ca_bundle`` is comet.include.custom_ca_bundle, a file or a directory."""
        self._verify_tls = verify_tls
        self._custom_ca_bundle = custom_ca_bundle
        self._fallback = (
            fallback
            if fallback is not None
            else RequestsTransport(verify_tls=verify_tls)
        )
        self._ca_bundles: Optional[Tuple[str, ...]] = None
        self._failed = False

    def put(self, url: str, body: Any) -> TransportResponse:
        client = self._client(timeout=None)
        if client is None:
            return self._fallback.put(url, body)

        request = client.put(url)
        chunks = None
        # A part of a file comes mapped where it can be: pyreqwest sends the mapping
        # as it is, without a copy, so the part needs the GIL once rather than for
        # every block read. Measured with the main thread busy, about 8x the
        # throughput of reading the part through Python. Not on Windows, and not
        # where the file cannot be mapped; see FileRangeReader.map_range().
        map_range = getattr(body, "map_range", None)
        mapping = map_range() if callable(map_range) else None
        if mapping is not None:
            request = request.body_bytes(mapping.view)
        elif hasattr(body, "read"):
            # pyreqwest cannot tell the length of a streamed body and would send it
            # chunked, which S3 rejects on a presigned PUT.
            chunks = _BodyChunks(body)
            request = request.header("Content-Length", str(len(body))).body_stream(
                iter(chunks)
            )
        else:
            request = request.body_bytes(body)

        try:
            with _as_connection_errors():
                response = request.build().send()
                content = bytes(response.bytes())
        except Exception:
            if chunks is not None and chunks.error is not None:
                # pyreqwest passes the read error through as it is. Raised as a
                # connection error instead, which is how requests reports a body that
                # fails to read, so the part is retried the same way: the file may be
                # on a network filesystem that recovers.
                raise PyreqwestConnectionError(
                    "Could not read the part body: %r" % chunks.error
                ) from chunks.error
            raise
        finally:
            if mapping is not None:
                # Mapped again by the next attempt, if there is one.
                mapping.close()

        return PyreqwestResponse(
            status_code=response.status, headers=response.headers, content=content
        )

    def get(
        self, url: str, headers: Mapping[str, str], timeout: Optional[float]
    ) -> TransportResponse:
        client = self._client(timeout=timeout)
        if client is None:
            return self._fallback.get(url, headers, timeout)

        stream = (
            client.get(url)
            .headers(dict(headers))
            .streamed_read_buffer_limit(READ_AHEAD_BYTES)
            .build_streamed()
        )
        with _as_connection_errors():
            response = stream.__enter__()

        return PyreqwestStreamedResponse(stream, response)

    def _client(self, timeout: Optional[float]) -> Optional[SyncClient]:
        if self._failed:
            return None

        if _forked_after_runtime_started():
            warn_once(
                "pyreqwest-forked",
                "This process was forked after pyreqwest started, and pyreqwest "
                "cannot run in it. Direct S3 transfers in it use requests instead.",
                level=logging.DEBUG,
            )
            return None

        try:
            if self._ca_bundles is None:
                self._ca_bundles = (
                    ca_bundle_paths(self._custom_ca_bundle) if self._verify_tls else ()
                )
            return _shared_client(
                self._verify_tls, timeout, self._ca_bundles, _proxy_environment()
            )
        except Exception as ex:
            # Whatever stops a client from being built, requests can still do the
            # transfer, or fail it with the error the user would have got anyway.
            self._failed = True
            warn_once(
                "pyreqwest-setup",
                "Could not set up pyreqwest for direct S3 transfers, using requests "
                "instead: %r",
                ex,
            )
            return None


class PyreqwestResponse(TransportResponse):
    """A response read in full, as a part upload's is."""

    __slots__ = ["_status_code", "_headers", "_content"]

    def __init__(self, status_code: int, headers: Mapping[str, str], content: bytes):
        self._status_code = status_code
        self._headers = headers
        self._content = content

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def headers(self) -> Mapping[str, str]:
        return self._headers

    @property
    def text(self) -> str:
        return self._content.decode("utf-8", errors="replace")

    def iter_raw(self, chunk_size: int) -> Iterator[bytes]:
        for start in range(0, len(self._content), chunk_size):
            yield self._content[start : start + chunk_size]

    def read_error_text(self, limit: int = 1024) -> str:
        return self._content[:limit].decode("utf-8", errors="replace")

    def close(self) -> None:
        pass


class PyreqwestStreamedResponse(TransportResponse):
    """A response whose body is still arriving, held open until close()."""

    def __init__(self, stream: Any, response: Any):
        # The stream is a context manager; entering it sent the request.
        self._stream = stream
        self._response = response
        self._closed = False
        self._lock = threading.Lock()

    @property
    def status_code(self) -> int:
        return cast(int, self._response.status)

    @property
    def headers(self) -> Mapping[str, str]:
        return cast(Mapping[str, str], self._response.headers)

    @property
    def text(self) -> str:
        with _as_connection_errors():
            content = bytes(self._response.body_reader.bytes())
        return content.decode("utf-8", errors="replace")

    def iter_raw(self, chunk_size: int) -> Iterator[bytes]:
        # Blocks of at least chunk_size (the last one shorter), collected from the
        # pieces pyreqwest hands over as they arrive, about a hundred kilobytes each.
        #
        # Collected here rather than with read(chunk_size), which would cost the GIL
        # less but drops whatever it collected when the connection fails, where the
        # receivers resume from the first byte that did not arrive: a link that
        # keeps dropping within a chunk would then make no progress at all. When
        # the connection fails, what was collected is handed over before the error.
        #
        # Collected at all, rather than passed on piece by piece, because each piece
        # is written to the file and counted in Python: with the main thread busy,
        # every one of those waits for the GIL, and piece by piece did worse than
        # requests, which writes in blocks of chunk_size.
        reader = self._response.body_reader
        pending = bytearray()
        while True:
            try:
                with _as_connection_errors():
                    chunk = reader.read_chunk()
            except ConnectionError:
                if pending:
                    yield cast(bytes, pending)
                raise
            if chunk is None:
                if pending:
                    yield cast(bytes, pending)
                return
            pending += chunk
            if len(pending) >= chunk_size:
                # Handed over rather than copied; a new buffer takes its place.
                full, pending = pending, bytearray()
                yield cast(bytes, full)

    def read_error_text(self, limit: int = 1024) -> str:
        reader = self._response.body_reader
        head = b""
        try:
            while len(head) < limit:
                chunk = reader.read_chunk()
                if chunk is None:
                    break
                head += bytes(chunk)
        except Exception:
            pass
        return head[:limit].decode("utf-8", errors="replace")

    def close(self) -> None:
        # Leaving the stream twice is an error in pyreqwest, and both a part and
        # its receiver may close the same response.
        with self._lock:
            if self._closed:
                return
            self._closed = True
        self._stream.__exit__(None, None, None)


class _BodyChunks:
    """Feeds a file-backed part to pyreqwest, and keeps any error reading the file.

    So that put() can tell a file that failed to read from a failed request, and
    report it the way requests does.
    """

    def __init__(self, body: Any):
        self._body = body
        self.error: Optional[BaseException] = None

    def __iter__(self) -> Iterator[bytes]:
        while True:
            try:
                chunk = self._body.read(UPLOAD_CHUNK_BYTES)
            except Exception as ex:
                self.error = ex
                raise
            if not chunk:
                return
            yield chunk


def ca_bundle_paths(custom_ca_bundle: Optional[str]) -> Tuple[str, ...]:
    """The CA bundles to trust on top of pyreqwest's built-in roots.

    The same files requests would use: the bundle comet_ml merges from
    comet.include.custom_ca_bundle, and the ones named by the environment. requests
    trusts only such a bundle, while here it is added to the built-in roots, so it
    can only widen what is trusted. Corporate proxies that intercept TLS depend on
    it.
    """
    paths = []
    if custom_ca_bundle:
        merged = ca_certs.setup_ca_certs(custom_ca_bundle)
        if merged is not None:
            paths.append(merged)

    for name in CA_BUNDLE_ENVIRONMENT_VARIABLES:
        path = os.environ.get(name)
        if path and os.path.isdir(path):
            # requests trusts a hashed CA directory, which pyreqwest cannot load.
            # Raising here makes the transport fall back to requests.
            raise ValueError(
                "%s names a CA directory, which pyreqwest cannot load: %s"
                % (name, path)
            )
        if path and os.path.isfile(path) and path not in paths:
            paths.append(path)

    return tuple(paths)


_ProxyEnvironment = Tuple[Tuple[str, str], ...]
_ClientKey = Tuple[bool, Optional[float], Tuple[str, ...], _ProxyEnvironment]

_clients: Dict[_ClientKey, SyncClient] = {}
_clients_lock = threading.Lock()

# The process that started pyreqwest's runtime. Set before the first client is
# built, because building it may start the runtime even when it then fails.
_runtime_pid: Optional[int] = None


def _forked_after_runtime_started() -> bool:
    return _runtime_pid is not None and _runtime_pid != os.getpid()


def _proxy_environment() -> _ProxyEnvironment:
    return tuple(
        (name, os.environ[name])
        for name in PROXY_ENVIRONMENT_VARIABLES
        if name in os.environ
    )


def _shared_client(
    verify_tls: bool,
    timeout: Optional[float],
    ca_bundles: Tuple[str, ...],
    proxies: _ProxyEnvironment,
) -> SyncClient:
    """``proxies`` is only part of the key: the client reads them from the environment."""
    global _runtime_pid

    key = (verify_tls, timeout, ca_bundles, proxies)
    client = _clients.get(key)
    if client is not None:
        return client

    with _clients_lock:
        client = _clients.get(key)
        if client is None:
            if _runtime_pid is None:
                _runtime_pid = os.getpid()
            client = _build_client(verify_tls, timeout, ca_bundles)
            _clients[key] = client

    return client


def _build_client(
    verify_tls: bool, timeout: Optional[float], ca_bundles: Tuple[str, ...]
) -> SyncClient:
    builder = (
        SyncClientBuilder()
        # The default runtime is single-threaded, so every connection's TLS and I/O
        # shares one thread: measured on real S3, that capped uploads at about 2 GiB/s
        # whatever the concurrency.
        .runtime_multithreaded(True)
        # The callers read the status themselves.
        .error_for_status(False)
        # A range is a range of the stored object, so the body must arrive as
        # stored: decoding it would make every length and offset meaningless.
        .gzip(False)
        .brotli(False)
        .zstd(False)
        .deflate(False)
    )
    if timeout is not None:
        # As requests applies a timeout: to connecting, and to each read.
        builder = builder.connect_timeout(timedelta(seconds=timeout)).read_timeout(
            timedelta(seconds=timeout)
        )

    if not verify_tls:
        builder = builder.danger_accept_invalid_certs(True)
    else:
        for path in ca_bundles:
            with open(path, "rb") as bundle:
                builder = builder.add_root_certificate_pem(bundle.read())

    return builder.build()


def _reset_after_fork() -> None:
    # A thread of the parent may have held the lock at the moment of the fork,
    # and it would then never be released in the child.
    global _clients_lock
    _clients_lock = threading.Lock()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_after_fork)
