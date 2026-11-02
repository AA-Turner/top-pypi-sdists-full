"""Bound retained command bytes and multiplex independent durable receipt futures."""

import asyncio
from collections.abc import Mapping, AsyncIterator, AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from functools import partial
from uuid import uuid4

from websockets.asyncio.client import ClientConnection

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.worker.session.session_frames import SessionFrames
from labqoat.worker.session.session_pending import SessionPending
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass
class SessionOutbox:
    """Replay pending operations with stable identities and promptly cancel abandoned observations."""

    pending: dict[str, SessionPending] = field(default_factory=dict, init=False)
    changed: asyncio.Event = field(default_factory=asyncio.Event, init=False)
    _capacity: asyncio.Semaphore = field(default_factory=partial(asyncio.Semaphore, 64), init=False)
    _observers: asyncio.Semaphore = field(default_factory=partial(asyncio.Semaphore, 32), init=False)
    _bytes: int = field(default=0, init=False)
    _resume: set[str] = field(default_factory=set, init=False)

    async def request(self, op: str, attempt: str, data: Mapping[str, JsonValue]) -> JsonDocument:
        """Hold a bounded slot until a committed receipt arrives or its owning caller leaves."""
        async with self._operation(op, attempt, data) as pending:
            return await pending.receipt

    async def observe(self, attempt: str, ids: list[str]) -> AsyncGenerator[JsonDocument, None]:
        """Keep one bounded subscription until all requested children have produced authoritative outcomes."""
        updates: asyncio.Queue[JsonDocument] = asyncio.Queue(1)
        async with self._observers, self._operation("observe", attempt, {"ids": list(ids)}, updates) as pending:
            while True:
                frame = await updates.get()
                yield SessionFrames.result(frame)
                if pending.finished and updates.empty():
                    return
                if updates.empty() and not pending.finished:
                    self._resume.add(JsonDocument.expect_scalar(pending.command["id"], str))
                    self.changed.set()

    @asynccontextmanager
    async def _operation(
        self, op: str, attempt: str, data: Mapping[str, JsonValue], updates: asyncio.Queue[JsonDocument] | None = None
    ) -> AsyncIterator[SessionPending]:
        """Own command identity, receipt state and the aggregate memory reservation together."""
        async with self._capacity:
            identity = str(uuid4())
            command = JsonDocument(id=identity, op=op, attempt=attempt, data=dict(data))
            size = len(SessionFrames.encode({"commands": [command]}).encode())
            if self._bytes + size > 67_108_864:
                raise WorkerApiError("Worker session pending data exceeds its limit", 429)
            future: asyncio.Future[JsonDocument] = asyncio.get_running_loop().create_future()
            pending = SessionPending(command, future, updates)
            self.pending[identity] = pending
            self._bytes += size
            self.changed.set()
            try:
                yield pending
            finally:
                del self.pending[identity]
                self._resume.discard(identity)
                self._bytes -= size
                self.changed.set()

    async def send(self, connection: ClientConnection) -> None:
        """Send each retained command once per connection, and revoke only abandoned observation tasks."""
        sent: dict[str, str] = {}
        while True:
            await self.changed.wait()
            self.changed.clear()
            sent = await self._controls(connection, sent)
            for key, pending in list(self.pending.items()):
                if key not in sent and pending.ready():
                    await connection.send(SessionFrames.encode({"commands": [pending.command]}))
                    sent[key] = JsonDocument.expect_scalar(pending.command["op"], str)

    async def _controls(self, connection: ClientConnection, sent: dict[str, str]) -> dict[str, str]:
        """Grant another result frame only after its predecessor has drained to the local caller."""
        cancelled = [key for key, op in sent.items() if key not in self.pending and op == "observe"]
        if cancelled:
            await connection.send(SessionFrames.encode({"cancel": list(cancelled)}))
        resume = list(self._resume.intersection(sent).intersection(self.pending))
        self._resume.clear()
        if resume:
            await connection.send(SessionFrames.encode({"resume": list(resume)}))
        return {key: op for key, op in sent.items() if key in self.pending}

    def receive(self, frame: JsonDocument) -> None:
        """Late receipts for cancelled local callers cannot settle a different operation."""
        identity = JsonDocument.expect_scalar(frame["id"], str)
        pending = self.pending.get(identity)
        if pending is None or pending.receipt.done():
            return
        pending.deliver(frame)
