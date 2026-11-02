"""Explicit assignment-authenticated HTTP boundary for workflow workers."""

from __future__ import annotations

import http.client
import ipaddress
import json
import socket
from collections.abc import AsyncGenerator, AsyncIterator, Mapping
from functools import partial
from typing import BinaryIO
from contextlib import AbstractContextManager, asynccontextmanager, nullcontext, aclosing
from pathlib import Path
from urllib.parse import urlsplit

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.stage_timer import StageTimer
from labqoat.worker.async_scoped_api import AsyncScopedApi
from labqoat.net.http_connections import HttpConnections
from labqoat.worker.session.local_session_client import LocalSessionClient
from labqoat.worker.session.session_routes import SessionRoutes
from labqoat.net.transport_trust import TransportTrust
from labqoat.worker.completion_wait import CompletionWait
from labqoat.worker.worker_api_error import WorkerApiError
from labqoat.worker.worker_event_stream import WorkerEventStream


class ScopedApi:
    """Bound HTTP transfers to one explicit endpoint, credential set, and route prefix."""

    def __init__(
        self,
        base_url: str,
        headers: Mapping[str, str],
        prefix: str,
        timeout_seconds: float = 180.0,
        timing: StageTimer | None = None,
        local: LocalSessionClient | None = None,
    ) -> None:
        """Validate the endpoint and store explicit credentials without logging them."""
        self._url = urlsplit(base_url)
        self._validate_endpoint()
        self._timeout = timeout_seconds
        self._headers = dict(headers)
        self._prefix = prefix
        self._timing = timing
        self._resolved = False
        self._local = local
        self._connections = HttpConnections(self._connection)
        self._async = AsyncScopedApi(base_url, self._headers, prefix, timeout_seconds)

    def close(self) -> None:
        """Release idle sockets owned by this scoped synchronous client."""
        self._connections.close()

    async def child_completions(self, ids: list[str]) -> JsonDocument:
        """Observe a bounded group under one parent credential, resuming with unfinished child identities."""
        if self._local is not None:
            return await self._local.request_async("observe", {"ids": list(ids)})
        return await self._async.completion("/api/v1/worker/runs/completions", "children", {"ids": list(ids)})

    async def child_updates(self, ids: list[str]) -> AsyncGenerator[JsonDocument, None]:
        """Continuously push owned child results when a physical session was negotiated."""
        if self._local is None:
            yield await self.child_completions(ids)
            return
        async with aclosing(self._local.observe(ids)) as updates:
            async for update in updates:
                yield update

    def pool_deliveries(self, request: Mapping[str, JsonValue]) -> AsyncGenerator[JsonDocument, None]:
        """Stream physical assignments with a per-input bound accommodating the service's accepted request size."""
        return self._async.events(
            "/api/v1/worker/pool/deliveries", "compute_pool", request, 16_777_216, heartbeats=True
        )

    @asynccontextmanager
    async def async_session(self) -> AsyncIterator[None]:
        """Own pooled async I/O for one execution, closing it before its event loop exits."""
        async with self._async.lifetime():
            yield

    def _connection(self) -> http.client.HTTPConnection:
        """Construct a connection to the validated origin with the configured timeout."""
        url = self._url
        return TransportTrust.connection(
            url.scheme, str(url.hostname), url.port, timeout=self._timeout, blocksize=1048576
        )

    def json(self, method: str, path: str, document: Mapping[str, JsonValue] | None = None) -> JsonDocument:
        """Send a strict JSON request and require an object response."""
        if self._local is not None and (op := SessionRoutes.operation(method, path)) is not None:
            return self._local.request(op, document or {})
        body = (
            None
            if document is None
            else json.dumps(document, separators=(",", ":"), allow_nan=False, ensure_ascii=False).encode()
        )
        raw = self.request(method, path, body, "application/json")
        return JsonDocument.expect_dict(json.loads(raw))

    async def json_async(self, method: str, path: str, document: Mapping[str, JsonValue] | None = None) -> JsonDocument:
        """Use cancellable I/O for a keyed worker effect without blocking the authored event loop."""
        if self._local is not None and (op := SessionRoutes.operation(method, path)) is not None:
            return await self._local.request_async(op, document or {})
        return await self._async.json(method, path, document)

    async def completion_async(self, path: str, kind: str) -> JsonDocument:
        """Wait for service completion with a stream whose lifetime belongs to this coroutine, across reconnects."""
        return await CompletionWait.run_async(partial(self._async.completion, path, kind))

    def request(
        self, method: str, path: str, body: bytes | None = None, content_type: str = "application/octet-stream"
    ) -> bytes:
        """Send one scoped operation with no redirects or credential-bearing error text."""
        if not path.startswith(self._prefix) or ".." in path.split("?")[0]:
            raise ValueError("Worker requests must use assignment-scoped API paths")
        try:
            with self._connections.using() as connection:
                response = self._send(connection, method, path, body, content_type)
                with self._span("http.read", self._detail(method, path)):
                    content = response.read()
        except (OSError, http.client.HTTPException) as error:
            raise WorkerApiError("Worker API transport failed") from error
        if not 200 <= response.status < 300:
            raise WorkerApiError.from_response(response.status, content)
        return content

    def upload_file(self, path: str, source: Path, byte_size: int) -> bytes:
        """Stream one local file as an exact-length request body without buffering the whole file."""
        if not path.startswith(self._prefix) or ".." in path.split("?")[0] or byte_size < 0:
            raise ValueError("Worker upload requires a scoped path and nonnegative size")
        try:
            with self._connections.using() as connection, source.open("rb") as body:
                response = self._send(connection, "PUT", path, body, "application/octet-stream", byte_size)
                with self._span("http.read", self._detail("PUT", path)):
                    content = response.read()
        except (OSError, http.client.HTTPException) as error:
            raise WorkerApiError("Worker API upload failed") from error
        if not 200 <= response.status < 300:
            raise WorkerApiError.from_response(response.status, content)
        return content

    def _send(
        self,
        connection: http.client.HTTPConnection,
        method: str,
        path: str,
        body: bytes | BinaryIO | None,
        content_type: str,
        content_length: int | None = None,
    ) -> http.client.HTTPResponse:
        """Measure new connections separately while fully reusing an idle authenticated transport."""
        detail = self._detail(method, path)
        length = {} if content_length is None else {"Content-Length": str(content_length)}
        self._resolve()
        with self._span("http.connect", detail):
            if connection.sock is None:
                connection.connect()
        with self._span("http.send", detail):
            connection.request(
                method,
                self._url.path.rstrip("/") + path,
                body=body,
                headers=self._headers | {"Content-Type": content_type} | length,
            )
            return connection.getresponse()

    def download_to(self, path: str, destination: Path, byte_size: int) -> None:
        """Copy one bounded response to disk without buffering the whole asset."""
        if not path.startswith(self._prefix) or ".." in path.split("?")[0] or byte_size < 0:
            raise ValueError("Worker download requires a scoped path and nonnegative size")
        try:
            with self._connections.using() as connection:
                response = self._send(connection, "GET", path, None, "application/octet-stream")
                if not 200 <= response.status < 300:
                    raise WorkerApiError(f"Worker API returned HTTP {response.status}", response.status)
                with self._span("http.read", self._detail("GET", path)):
                    self._copy_response(response, destination, byte_size)
        except (OSError, http.client.HTTPException) as error:
            raise WorkerApiError("Worker API download failed") from error

    def completion(self, path: str, kind: str) -> JsonDocument:
        """Wait on authenticated SSE across reconnects; the enclosing execution owns its overall deadline."""
        if not path.startswith(self._prefix) or ".." in path.split("?")[0]:
            raise ValueError("Worker streams must use assignment-scoped API paths")
        return CompletionWait.run(partial(self._completion_once, path, kind))

    def _completion_once(self, path: str, kind: str) -> JsonDocument:
        """One connection to the completion stream."""
        url = self._url
        connection = TransportTrust.connection(url.scheme, str(url.hostname), url.port, timeout=self._timeout)
        try:
            connection.request("GET", self._url.path.rstrip("/") + path, headers=self._headers)
            response = connection.getresponse()
            if response.status != 200 or response.getheader("Content-Type", "").split(";")[0] != "text/event-stream":
                raise WorkerApiError("Worker completion stream was rejected", response.status)
            value = WorkerEventStream.complete(response, kind, float("inf"))
            return JsonDocument.expect_dict(value)
        except (OSError, http.client.HTTPException) as error:
            raise WorkerApiError("Worker completion transport failed") from error
        finally:
            connection.close()

    @staticmethod
    def _copy_response(response: http.client.HTTPResponse, destination: Path, expected_size: int) -> None:
        """Bound memory and reject both truncation and excess response contents."""
        received = 0
        with destination.open("wb") as output:
            while chunk := response.read(min(1024 * 1024, expected_size - received + 1)):
                received += len(chunk)
                if received > expected_size:
                    raise ValueError("Asset download exceeds its declared byte size")
                output.write(chunk)
        if received != expected_size:
            raise ValueError("Asset download does not match its declared byte size")

    def _resolve(self) -> None:
        """Warm and time name resolution once per bound client rather than once per request."""
        if self._timing is None or self._resolved:
            return
        with self._timing.span("http.dns"):
            socket.getaddrinfo(str(self._url.hostname), self._url.port, type=socket.SOCK_STREAM)
        self._resolved = True

    def _span(self, name: str, detail: str = "") -> AbstractContextManager[None]:
        """Time one transport phase only when the caller bound a stage timer."""
        if self._timing is None:
            return nullcontext()
        return self._timing.span(name, detail)

    @staticmethod
    def _detail(method: str, path: str) -> str:
        """Attribute a transport phase to exactly one scoped operation."""
        return f"{method}:{path.split('?', 1)[0]}"

    def _validate_endpoint(self) -> None:
        """Allow verified HTTPS or explicitly local HTTP worker endpoints."""
        if self._url.scheme not in {"http", "https"} or self._url.hostname is None:
            raise ValueError("Worker API requires an HTTP endpoint")
        if self._url.username is not None or self._url.query or self._url.fragment:
            raise ValueError("Worker API endpoint cannot contain credentials, query, or fragment")
        if self._url.scheme == "http" and not self._local_host(self._url.hostname):
            raise ValueError("Plain HTTP workers require an explicit local endpoint")

    @staticmethod
    def _local_host(host: str) -> bool:
        """Recognize loopback addresses and the Docker Desktop host gateway."""
        if host in {"localhost", "host.docker.internal"}:
            return True
        try:
            return ipaddress.ip_address(host).is_loopback
        except ValueError:
            return False
