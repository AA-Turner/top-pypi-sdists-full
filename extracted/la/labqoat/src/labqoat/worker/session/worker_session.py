"""One persistent duplex connection belongs to a physical supervisor, not authored invocation processes."""

import asyncio
import secrets
import time
from collections.abc import AsyncIterator, Mapping, AsyncGenerator
from contextlib import asynccontextmanager, aclosing
from dataclasses import dataclass, field
from functools import partial
from uuid import uuid4

from websockets.asyncio.client import ClientConnection
from websockets.exceptions import ConnectionClosed, InvalidHandshake, InvalidStatus

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.worker.session.session_endpoint import SessionEndpoint
from labqoat.worker.session.session_frames import SessionFrames
from labqoat.worker.session.session_outbox import SessionOutbox
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass
class WorkerSession:
    """Reconnect with unchanged command identities while bounding pending work and delivery buffering."""

    endpoint: SessionEndpoint
    attempt: str
    outbox: SessionOutbox = field(default_factory=SessionOutbox)
    deliveries: asyncio.Queue[JsonDocument | None] = field(default_factory=partial(asyncio.Queue, 128), init=False)
    _subscription: JsonDocument = field(init=False)
    _progress: float = field(default=0, init=False)
    _active: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        """Retain one delivery identity across every reconnect of this physical lifetime."""
        self._subscription = JsonDocument(
            id=str(uuid4()),
            op="delivery",
            attempt=self.attempt,
            data={"delivery_id": str(uuid4()), "secret": secrets.token_hex(32)},
        )

    @asynccontextmanager
    async def lifetime(self) -> AsyncIterator[None]:
        """Make unrecoverable transport loss terminate the physical supervisor and its owned invocations."""
        async with asyncio.TaskGroup() as tasks:
            task = tasks.create_task(self._run())
            try:
                yield
            finally:
                task.cancel()

    async def request(self, op: str, attempt: str, data: Mapping[str, JsonValue]) -> JsonDocument:
        """Share the supervisor's loop for bounded, independently fenced commands."""
        try:
            async with asyncio.timeout(None if op == "observe" else 180):
                return await self.outbox.request(op, attempt, data)
        except TimeoutError:
            raise WorkerApiError("Worker session command timed out") from None

    async def observe(self, attempt: str, ids: list[str]) -> AsyncGenerator[JsonDocument, None]:
        """Push completed subsets continuously while the owning parent retains its lease."""
        async with aclosing(self.outbox.observe(attempt, ids)) as updates:
            async for update in updates:
                yield update

    async def _run(self) -> None:
        """Recover transient disconnects within the assignment's existing lease-renewal margin."""
        started, delay = time.monotonic(), 0.1
        while True:
            try:
                async with self.endpoint.connect() as connection:
                    await self._connected(connection)
            except InvalidStatus as error:
                if error.response.status_code not in {408, 429} and error.response.status_code < 500:
                    raise WorkerApiError("Worker session handshake rejected", error.response.status_code) from None
            except (OSError, TimeoutError, ConnectionClosed):
                pass
            except InvalidHandshake:
                raise WorkerApiError("Worker session handshake is invalid", 502) from None
            if self._progress > started:
                started, delay = self._progress, 0.1
            if time.monotonic() - started >= 600:
                raise WorkerApiError("Worker session recovery deadline expired")
            await asyncio.sleep(delay)
            delay = min(delay * 2, 10)

    async def _connected(self, connection: ClientConnection) -> None:
        """Replay only after a supported server handshake and stop both directions on disconnect."""
        async with asyncio.timeout(10):
            ready = SessionFrames.decode(await connection.recv())
        if ready != {"event": "ready", "version": 1}:
            raise WorkerApiError("Worker session protocol is unsupported", 502)
        await connection.send(SessionFrames.encode({"commands": [self._subscription]}))
        self.outbox.changed.set()
        reader = asyncio.create_task(self._receive(connection))
        writer = asyncio.create_task(self.outbox.send(connection))
        connected_at = time.monotonic()
        try:
            completed, _pending = await asyncio.wait([reader, writer], return_when=asyncio.FIRST_COMPLETED)
            for task in completed:
                task.result()
        finally:
            reader.cancel()
            writer.cancel()
            await asyncio.gather(reader, writer, return_exceptions=True)
            if time.monotonic() - connected_at >= 30:
                self._progress = time.monotonic()

    async def _receive(self, connection: ClientConnection) -> None:
        """Demultiplex assignment pushes and durable receipts without blocking unrelated requests."""
        async for message in connection:
            frame = SessionFrames.decode(message)
            if frame.get("event") == "inputs":
                delivery = JsonDocument.expect_dict(frame["data"])
                self._active = bool(JsonDocument.expect_list(delivery["active"]))
                await self.deliveries.put(delivery)
            elif frame.get("event") == "closed":
                if self._active:
                    raise WorkerApiError("Physical worker authority was closed", 409)
                await self.deliveries.put(None)
            elif frame.get("id") == self._subscription["id"]:
                SessionFrames.result(frame)
            else:
                self.outbox.receive(frame)
            self._progress = time.monotonic()
