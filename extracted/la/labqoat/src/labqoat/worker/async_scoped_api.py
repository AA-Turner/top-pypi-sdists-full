"""Native asynchronous assignment transport with operation-owned connection cleanup."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator, AsyncIterator, Mapping
from contextlib import aclosing, asynccontextmanager
from dataclasses import dataclass, field

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.net.async_http_client import AsyncHttpClient
from labqoat.net.client_identity import ClientIdentity
from labqoat.net.http_error import HttpError
from labqoat.net.response import Response
from labqoat.net.transport_trust import TransportTrust
from labqoat.worker.async_worker_event_stream import AsyncWorkerEventStream
from labqoat.worker.async_http_lease import AsyncHttpLease
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass
class AsyncScopedApi:
    """Use the validated scoped endpoint without proxy inheritance, redirects, or leaked cancellation threads."""

    base_url: str
    headers: Mapping[str, str]
    prefix: str
    timeout: float
    _sessions: dict[asyncio.AbstractEventLoop, AsyncHttpLease] = field(default_factory=dict, init=False)

    @asynccontextmanager
    async def lifetime(self) -> AsyncIterator[AsyncHttpLease]:
        """Own a lazy transport scope without loading HTTP backends for executions that never use them."""
        loop = asyncio.get_running_loop()
        lease = self._sessions.get(loop)
        if lease is None:
            lease = AsyncHttpLease()
            self._sessions[loop] = lease
        lease.users += 1
        try:
            yield lease
        finally:
            lease.users -= 1
            if lease.users == 0:
                del self._sessions[loop]
                if lease.client is not None:
                    await lease.client.aclose()

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncHttpClient]:
        """Initialize verified HTTP only on first I/O and reuse it until the final scope owner exits."""
        async with self.lifetime() as lease:
            if lease.client is None:
                lease.client = AsyncHttpClient(
                    headers=ClientIdentity.HEADERS, timeout=self.timeout, context=TransportTrust.context()
                )
            yield lease.client

    def _url(self, path: str) -> str:
        """Permit only the same worker paths used by the synchronous assignment boundary."""
        if not path.startswith(self.prefix) or ".." in path.split("?")[0]:
            raise ValueError("Worker requests must use assignment-scoped API paths")
        return self.base_url.rstrip("/") + path

    async def json(self, method: str, path: str, document: Mapping[str, JsonValue] | None) -> JsonDocument:
        """Accept one durable effect; cancellation closes local I/O and callers reattach using its stable key."""
        url = self._url(path)
        body = None if document is None else json.dumps(document, separators=(",", ":"), allow_nan=False).encode()
        try:
            async with self.session() as client:
                response = await client.request(
                    method, url, content=body, headers=dict(self.headers) | {"Content-Type": "application/json"}
                )
                if not 200 <= response.status_code < 300:
                    raise WorkerApiError.from_response(response.status_code, response.content)
                return JsonDocument.expect_dict(response.json())
        except HttpError as error:
            raise WorkerApiError("Worker API transport failed") from error

    async def completion(self, path: str, kind: str, document: Mapping[str, JsonValue] | None = None) -> JsonDocument:
        """A cancelled wait releases its stream immediately; remote child ownership remains with the service."""
        async with aclosing(self.events(path, kind, document)) as events:
            return await anext(events)

    async def events(
        self,
        path: str,
        kind: str,
        document: Mapping[str, JsonValue] | None,
        maximum: int | None = None,
        heartbeats: bool = False,
    ) -> AsyncGenerator[JsonDocument, None]:
        """Keep one verified connection open for bounded deliveries until its consumer closes or cancels it."""
        async with (
            self._response(path, document) as response,
            aclosing(AsyncWorkerEventStream.events(response.aiter_bytes(), kind, maximum, heartbeats)) as events,
        ):
            async for event in events:
                yield event

    @asynccontextmanager
    async def _response(self, path: str, document: Mapping[str, JsonValue] | None) -> AsyncIterator[Response]:
        """Validate and own streaming HTTP while sanitizing transport failures during both opening and reading."""
        url = self._url(path)
        body = None if document is None else json.dumps(document, separators=(",", ":"), allow_nan=False).encode()
        fields = dict(self.headers) | ({} if body is None else {"Content-Type": "application/json"})
        try:
            async with (
                self.session() as client,
                client.stream("GET" if body is None else "POST", url, content=body, headers=fields) as response,
            ):
                if (
                    response.status_code != 200
                    or response.headers.get("content-type", "").split(";")[0] != "text/event-stream"
                ):
                    raise WorkerApiError("Worker completion stream was rejected", response.status_code)
                yield response
        except HttpError as error:
            raise WorkerApiError("Worker completion transport failed") from error
