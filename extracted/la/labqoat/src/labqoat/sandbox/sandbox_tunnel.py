"""A port inside a sandbox, reachable from its worker at a local address."""

import asyncio
from contextlib import suppress
from threading import Thread
from types import TracebackType
from typing import ClassVar

from websockets.asyncio.client import ClientConnection, unix_connect
from websockets.exceptions import WebSocketException


class SandboxTunnel:
    """Listen on a local port and carry each connection to a port inside the sandbox.

    Every connection to ``url`` becomes one connection to the sandbox's port, carried over the worker's private
    sandbox socket, so any HTTP client, database driver or gRPC channel can use it. Only the worker that owns
    the sandbox has that socket. The sandbox must have been created with ``ports=[...]``; the tunnel stops when
    closed or when the worker exits.
    """

    HOST: ClassVar[str] = "127.0.0.1"
    PIECE_BYTES: ClassVar[int] = 65_536
    GRACE_SECONDS: ClassVar[float] = 1.0

    def __init__(self, socket_path: str, path: str, port: int) -> None:
        """Start listening on a free local port at once."""
        self.remote_port = port
        self._socket_path = socket_path
        self._uri = f"ws://sandbox{path}"
        self._loop = asyncio.new_event_loop()
        self._thread = Thread(target=self._loop.run_forever, name=f"labqoat-tunnel-{port}", daemon=True)
        self._thread.start()
        listening = asyncio.run_coroutine_threadsafe(self._listen(), self._loop)
        self._server: asyncio.Server | None = listening.result()
        self.port: int = self._server.sockets[0].getsockname()[1]

    @property
    def url(self) -> str:
        """``http://127.0.0.1:PORT``: the sandbox's port as this worker reaches it."""
        return f"http://{self.HOST}:{self.port}"

    def close(self) -> None:
        """Stop listening and end every carried connection."""
        if self._server is not None:
            asyncio.run_coroutine_threadsafe(self._shutdown(self._server), self._loop).result()
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join()
            self._loop.close()
            self._server = None

    @classmethod
    async def _shutdown(cls, server: asyncio.Server) -> None:
        """Stop accepting, let connections whose clients left finish, then end the rest."""
        server.close()
        current = asyncio.current_task()
        carried = [task for task in asyncio.all_tasks() if task is not current]
        if carried:
            await asyncio.wait(carried, timeout=cls.GRACE_SECONDS)
        for task in carried:
            task.cancel()
        await asyncio.gather(*carried, return_exceptions=True)

    def __enter__(self) -> "SandboxTunnel":
        """Use the tunnel for a block."""
        return self

    def __exit__(
        self, kind: type[BaseException] | None, error: BaseException | None, trace: TracebackType | None
    ) -> None:
        """Close the tunnel."""
        self.close()

    async def _listen(self) -> asyncio.Server:
        """Accept local connections on a free port of the loopback address."""
        return await asyncio.start_server(self._carry, self.HOST, 0)

    async def _carry(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Carry one local connection to the sandbox's port until either side closes."""
        with suppress(OSError, WebSocketException):
            async with unix_connect(self._socket_path, self._uri, max_size=None, compression=None) as remote:
                upload = asyncio.ensure_future(self._upload(reader, remote))
                download = asyncio.ensure_future(self._download(remote, writer))
                _done, pending = await asyncio.wait({upload, download}, return_when=asyncio.FIRST_COMPLETED)
                for task in pending:
                    task.cancel()
        writer.close()

    async def _upload(self, reader: asyncio.StreamReader, remote: ClientConnection) -> None:
        """Send what the local client writes."""
        while piece := await reader.read(self.PIECE_BYTES):
            await remote.send(piece)

    @staticmethod
    async def _download(remote: ClientConnection, writer: asyncio.StreamWriter) -> None:
        """Write what the sandbox's port answers."""
        async for message in remote:
            writer.write(message if isinstance(message, bytes) else message.encode())
            await writer.drain()
