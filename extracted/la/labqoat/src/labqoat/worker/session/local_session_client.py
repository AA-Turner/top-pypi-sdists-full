"""Fresh invocations use scoped local IPC while the supervisor retains remote TLS state."""

import asyncio
import socket
from collections.abc import Mapping, AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.worker.session.local_frames import LocalFrames
from labqoat.worker.session.session_frames import SessionFrames
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass(frozen=True)
class LocalSessionClient:
    """Never receive physical credentials or choose an arbitrary delegated attempt."""

    path: str
    credential: str
    secret: str
    timeout: float = 180

    def request(self, op: str, data: Mapping[str, JsonValue]) -> JsonDocument:
        """Use a local operation-owned socket for synchronous authored threads."""
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
                connection.settimeout(self.timeout)
                connection.connect(self.path)
                connection.sendall(self._frame(op, data))
                with connection.makefile("rb") as source:
                    return SessionFrames.result(LocalFrames.read(source))
        except OSError as error:
            raise WorkerApiError("Local worker session disconnected") from error

    async def request_async(self, op: str, data: Mapping[str, JsonValue]) -> JsonDocument:
        """Close local observation sockets promptly when their coroutine is cancelled."""
        try:
            async with asyncio.timeout(None if op == "observe" else self.timeout), self._connection(op, data) as source:
                return SessionFrames.result(await LocalFrames.read_async(source))
        except TimeoutError as error:
            raise WorkerApiError("Local worker session disconnected") from error

    async def observe(self, ids: list[str]) -> AsyncGenerator[JsonDocument, None]:
        """Keep one local subscription open for all child outcomes under the parent's renewed lease."""
        async with self._connection("observe", {"ids": list(ids)}) as source:
            while True:
                frame = await LocalFrames.read_async(source)
                yield SessionFrames.result(frame)
                if frame.get("more") is not True:
                    return

    @asynccontextmanager
    async def _connection(self, op: str, data: Mapping[str, JsonValue]) -> AsyncIterator[asyncio.StreamReader]:
        """Bound connection establishment while preserving lease-owned waits after the request is sent."""
        try:
            async with asyncio.timeout(10):
                source, target = await asyncio.open_unix_connection(self.path)
            try:
                target.write(self._frame(op, data))
                await target.drain()
                yield source
            finally:
                target.close()
                await target.wait_closed()
        except (OSError, asyncio.IncompleteReadError) as error:
            raise WorkerApiError("Local worker session disconnected") from error

    def _frame(self, op: str, data: Mapping[str, JsonValue]) -> bytes:
        """Authenticate only this invocation and send one explicitly selected operation."""
        return LocalFrames.encode({"credential": self.credential, "secret": self.secret, "op": op, "data": dict(data)})
