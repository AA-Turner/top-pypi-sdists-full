"""HTTP to a sandbox host, over its private unix socket or through a service that carries requests to it."""

import asyncio
import threading
import time
from collections.abc import AsyncIterator, Iterator, Mapping
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from typing import ClassVar

from labqoat.net.http_client import HttpClient
from labqoat.net.http_error import HttpError
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_response import SandboxResponse
from labqoat.sandbox.sandbox_retry import SandboxRetry
from labqoat.sandbox.sandbox_route import SandboxRoute
from labqoat.sandbox.sandbox_unavailable_error import SandboxUnavailableError


class _RetryError(Exception):
    """A failed request ``SandboxRetry`` lets be sent once more."""


class SandboxTransport:
    """Send requests without proxies or redirects, retrying only as ``SandboxRetry`` allows, reusing a blocking connection once its answer was read.

    Over the internet a new connection costs several round trips, so blocking requests share one pool, which
    takes back only connections whose answer was read in full and drops any that fail, so a request that may
    have started a process is never replayed. Each asynchronous request has its own connection, and cancelling
    one closes it at once instead of leaving a thread waiting for the answer. An answer is read as it
    arrives; ``timeout`` bounds each wait for more of it, not the whole answer. A body larger than one piece
    goes out a piece at a time with its whole length declared: one large write to a socket is slow inside a
    gVisor sandbox, where a worker runs.
    """

    CHUNK_BYTES: ClassVar[int] = 1_048_576

    def __init__(self, route: SandboxRoute, timeout: float) -> None:
        """Bind where the host answers and the default seconds to wait for an answer, without connecting."""
        self._route = route
        self._timeout = timeout
        self._pool: HttpClient | None = None
        self._pool_lock = threading.Lock()

    @property
    def socket_path(self) -> str | None:
        """The host's private socket, when this worker hosts the sandboxes it reaches."""
        return self._route.socket_path

    def send(self, request: SandboxRequest) -> bytes:
        """Return a successful response body; host failures and transport failures raise typed errors."""
        with self.stream(request) as body:
            return b"".join(body)

    async def send_async(self, request: SandboxRequest) -> bytes:
        """Send without blocking the event loop; cancellation abandons the request and closes its connection."""
        async with self.stream_async(request) as body:
            return b"".join([chunk async for chunk in body])

    @contextmanager
    def stream(self, request: SandboxRequest) -> Iterator[Iterator[bytes]]:
        """Open a successful response and hand over its body as the pieces that arrive; a failure raises first."""
        retry = SandboxRetry(self._route.socket_path is None)
        while True:
            try:
                with self._attempt(request, retry) as body:
                    yield body
                    return
            except _RetryError:
                time.sleep(SandboxRetry.PAUSE)

    @asynccontextmanager
    async def stream_async(self, request: SandboxRequest) -> AsyncIterator[AsyncIterator[bytes]]:
        """Open a response without blocking the event loop; see ``stream``."""
        retry = SandboxRetry(self._route.socket_path is None)
        while True:
            try:
                async with self._attempt_async(request, retry) as body:
                    yield body
                    return
            except _RetryError:
                await asyncio.sleep(SandboxRetry.PAUSE)

    @contextmanager
    def _attempt(self, request: SandboxRequest, retry: SandboxRetry) -> Iterator[Iterator[bytes]]:
        """Send the request once; a failure ``retry`` allows to be sent again raises ``_RetryError``."""
        content = self._chunks(request.source, request) if request.source is not None else self._cut(request.encoded())
        answered = False
        try:
            with self._shared().stream(
                request.method,
                request.path,
                params=dict(request.query),
                content=content,
                headers=self._headers(request),
                timeout=request.timeout or self._timeout,
            ) as response:
                if not 200 <= response.status_code < 300:
                    raise self._refused(request, retry, response.status_code, response.headers, response.read())
                answered = True
                yield response.iter_bytes()
        except HttpError as error:
            raise self._lost(request, retry, answered, error) from error

    @asynccontextmanager
    async def _attempt_async(self, request: SandboxRequest, retry: SandboxRetry) -> AsyncIterator[AsyncIterator[bytes]]:
        """Send the request once without blocking the event loop; see ``_attempt``."""
        encoded = request.encoded()
        content = (
            self._chunks_async(request.source, request) if request.source is not None else self._cut_async(encoded)
        )
        answered = False
        try:
            async with (
                self._route.client_async(request.timeout or self._timeout) as client,
                client.stream(
                    request.method,
                    request.path,
                    params=dict(request.query),
                    content=content,
                    headers=self._headers(request),
                ) as response,
            ):
                if not 200 <= response.status_code < 300:
                    body = await response.aread()
                    raise self._refused(request, retry, response.status_code, response.headers, body)
                answered = True
                yield response.aiter_bytes()
        except HttpError as error:
            raise self._lost(request, retry, answered, error) from error

    @staticmethod
    def _refused(
        request: SandboxRequest, retry: SandboxRetry, status: int, headers: Mapping[str, str], body: bytes
    ) -> Exception:
        """The failure an answer means, or ``_RetryError`` when the same request may be sent once more."""
        return _RetryError() if retry.refused(request, status, headers) else SandboxResponse.failure(status, body)

    def _lost(self, request: SandboxRequest, retry: SandboxRetry, answered: bool, error: HttpError) -> Exception:
        """A request that failed on the way: sent again when nothing of its answer was used and that is safe."""
        return _RetryError() if not answered and retry.lost(request) else self._unanswered(error)

    def _shared(self) -> HttpClient:
        """The one blocking client of this transport, opened on first use; threads may share it."""
        with self._pool_lock:
            if self._pool is None:
                self._pool = self._route.client(self._timeout)
            return self._pool

    def _headers(self, request: SandboxRequest) -> dict[str, str]:
        """Present what admits the caller, then what describes the request."""
        return {**self._route.headers, **request.headers()}

    def _unanswered(self, error: HttpError) -> SandboxUnavailableError:
        """Name the transport failure without claiming anything about the process it interrupted."""
        host = self._route.describe()
        return SandboxUnavailableError(
            f"Sandbox host at {host} did not answer: {type(error.__cause__ or error).__name__}"
        )

    def _cut(self, content: bytes | None) -> bytes | Iterator[bytes] | None:
        """Leave a small body whole and hand a large one over in pieces."""
        if content is None or len(content) <= self.CHUNK_BYTES:
            return content
        return self._pieces(content)

    def _cut_async(self, content: bytes | None) -> bytes | AsyncIterator[bytes] | None:
        """Leave a small body whole and hand a large one over in pieces to an asynchronous client."""
        if content is None or len(content) <= self.CHUNK_BYTES:
            return content
        return self._pieces_async(content)

    def _pieces(self, content: bytes) -> Iterator[bytes]:
        """Yield an in-memory body a piece at a time."""
        for start in range(0, len(content), self.CHUNK_BYTES):
            yield content[start : start + self.CHUNK_BYTES]

    async def _pieces_async(self, content: bytes) -> AsyncIterator[bytes]:
        """Yield an in-memory body a piece at a time to an asynchronous client."""
        for piece in self._pieces(content):
            yield piece

    def _chunks(self, source: Path, request: SandboxRequest) -> Iterator[bytes]:
        """Read the request's part of a local file in bounded pieces for a synchronous upload."""
        with source.open("rb") as file:
            file.seek(request.source_start)
            remaining = request.source_length
            while remaining and (chunk := file.read(min(self.CHUNK_BYTES, remaining))):
                remaining -= len(chunk)
                yield chunk

    async def _chunks_async(self, source: Path, request: SandboxRequest) -> AsyncIterator[bytes]:
        """Read the request's part of a local file off the event loop for an asynchronous upload."""
        with source.open("rb") as file:
            await asyncio.to_thread(file.seek, request.source_start)
            remaining = request.source_length
            while remaining and (chunk := await asyncio.to_thread(file.read, min(self.CHUNK_BYTES, remaining))):
                remaining -= len(chunk)
                yield chunk
