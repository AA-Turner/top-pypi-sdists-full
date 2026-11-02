"""The supervisor owns a private bounded Unix socket for delegated invocation control."""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress, aclosing
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory

from labqoat.json_document import JsonDocument
from labqoat.worker.child_result_frame import ChildResultFrame
from labqoat.worker.session.local_frames import LocalFrames
from labqoat.worker.session.session_credentials import SessionCredentials
from labqoat.worker.session.worker_session import WorkerSession
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass
class SessionBridge:
    """Delegate bounded operations while preserving independent process and assignment lifetimes."""

    session: WorkerSession
    credentials: SessionCredentials = field(default_factory=SessionCredentials)
    path: str = field(default="", init=False)
    _tasks: set[asyncio.Task[None]] = field(default_factory=set, init=False)

    @asynccontextmanager
    async def lifetime(self) -> AsyncIterator[None]:
        """Remove private IPC state and cancel outstanding local waits on every supervisor exit."""
        with TemporaryDirectory(prefix="labqoat-session-") as directory:
            self.path = str(Path(directory) / "control.sock")
            server = await asyncio.start_unix_server(self._accept, path=self.path)
            try:
                async with server:
                    yield
            finally:
                for task in self._tasks:
                    task.cancel()
                await asyncio.gather(*self._tasks, return_exceptions=True)
                self.path = ""

    def register(self, envelope: JsonDocument) -> JsonDocument:
        """Deliver the private local endpoint alongside this input's existing scoped credentials."""
        self.credentials.register(envelope)
        return JsonDocument(envelope | {"session_socket": self.path})

    def _accept(self, source: asyncio.StreamReader, target: asyncio.StreamWriter) -> None:
        """Bound accepted local connections before reading any credential-bearing payload."""
        if len(self._tasks) >= 128:
            target.close()
            return
        task = asyncio.create_task(self._serve(source, target))
        self._tasks.add(task)
        task.add_done_callback(partial(self._closed, target))

    def _closed(self, target: asyncio.StreamWriter, task: asyncio.Task[None]) -> None:
        """Release even a socket whose task was cancelled before its first scheduling turn."""
        target.close()
        self._tasks.discard(task)

    async def _serve(self, source: asyncio.StreamReader, target: asyncio.StreamWriter) -> None:
        """A disconnected invocation loses its local waiter, never its durable remote operation."""
        try:
            async with asyncio.timeout(10):
                request = await LocalFrames.read_async(source)
            async with asyncio.timeout(None if request.get("op") == "observe" else 180):
                await self._exchange(source, target, request)
        except (OSError, asyncio.IncompleteReadError, TimeoutError, WorkerApiError, ValueError, TypeError):
            pass
        finally:
            target.close()
            with suppress(OSError):
                await target.wait_closed()

    async def _exchange(
        self, source: asyncio.StreamReader, target: asyncio.StreamWriter, request: JsonDocument
    ) -> None:
        """Race observation completion against local disconnect without retaining orphaned server subscriptions."""
        operation = asyncio.create_task(self._dispatch(target, request))
        disconnected = asyncio.create_task(source.read(1))
        try:
            completed, _pending = await asyncio.wait([operation, disconnected], return_when=asyncio.FIRST_COMPLETED)
            if operation in completed:
                operation.result()
                return
            raise WorkerApiError("Local worker session caller disconnected")
        finally:
            operation.cancel()
            disconnected.cancel()
            await asyncio.gather(operation, disconnected, return_exceptions=True)

    async def _dispatch(self, target: asyncio.StreamWriter, request: JsonDocument) -> None:
        """Forward streamed outcomes independently from ordinary one-receipt commands."""
        try:
            if request.get("op") == "observe":
                await self._stream(target, request)
            else:
                await self._emit(target, await self._execute(request))
        except WorkerApiError as error:
            await self._emit(
                target, JsonDocument(error=error.code or "session_command_rejected", status=error.status or 503)
            )
        except (KeyError, TypeError, ValueError):
            await self._emit(target, JsonDocument(error="invalid_session_command", status=400))

    async def _stream(self, target: asyncio.StreamWriter, request: JsonDocument) -> None:
        """A single authenticated local wait receives all owned children without repeated subscription setup."""
        attempt = self.credentials.resolve(request)
        data = JsonDocument.expect_dict(request["data"])
        ids = [JsonDocument.expect_scalar(item, str) for item in JsonDocument.expect_list(data["ids"])]
        remaining = set(ids)
        async with aclosing(self.session.observe(attempt, ids)) as updates:
            async for update in updates:
                remaining.difference_update(ChildResultFrame.capture(update, remaining))
                await self._emit(target, JsonDocument(data=update, more=bool(remaining)))

    @staticmethod
    async def _emit(target: asyncio.StreamWriter, reply: JsonDocument) -> None:
        """Apply the same byte framing and backpressure to receipts and streamed subsets."""
        target.write(LocalFrames.encode(reply))
        await target.drain()

    async def _execute(self, request: JsonDocument) -> JsonDocument:
        """Return sanitized receipts; only registered local credentials can select remote input authority."""
        try:
            attempt = self.credentials.resolve(request)
            op = JsonDocument.expect_scalar(request["op"], str)
            data = JsonDocument.expect_dict(request["data"])
            return JsonDocument(data=await self.session.request(op, attempt, data))
        except WorkerApiError as error:
            return JsonDocument(error=error.code or "session_command_rejected", status=error.status or 503)
        except (KeyError, ValueError, TypeError):
            return JsonDocument(error="invalid_session_command", status=400)
