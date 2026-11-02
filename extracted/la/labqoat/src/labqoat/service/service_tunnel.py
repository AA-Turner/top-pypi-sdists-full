"""A serving worker's tunnel: the control plane sends callers' requests down it and takes the answers back."""

import asyncio
from contextlib import suppress
from functools import partial
from threading import Event
from typing import ClassVar

from websockets.asyncio.client import ClientConnection
from websockets.exceptions import WebSocketException

from labqoat.net.async_http_client import AsyncHttpClient
from labqoat.service.service_endpoint import ServiceEndpoint
from labqoat.service.service_frame import ServiceFrame
from labqoat.service.service_stream import ServiceStream
from labqoat.service.service_target import ServiceTarget


class ServiceTunnel:
    """Keep one tunnel open and answer every request it carries from the local server, each on its own task.

    The control plane lets go of tunnels when it is replaced, so a tunnel that closes is opened again; while
    it is closed the service is simply not served.
    """

    RETRY_SECONDS: ClassVar[float] = 1.0

    def __init__(self, endpoint: ServiceEndpoint, target: ServiceTarget, opened: Event) -> None:
        """Bind where the tunnel goes, what it serves, and the signal for its first opening."""
        self._endpoint = endpoint
        self._target = target
        self._opened = opened
        self._streams: dict[int, tuple[ServiceStream, asyncio.Task[None]]] = {}

    async def serve(self) -> None:
        """Serve until cancelled."""
        async with self._target.client() as client:
            while True:
                await self._opened_once(client)
                await asyncio.sleep(self.RETRY_SECONDS)

    async def _opened_once(self, client: AsyncHttpClient) -> None:
        """Hold one tunnel for as long as it lasts; a tunnel that cannot open or breaks simply ends."""
        with suppress(OSError, ValueError, WebSocketException):
            async with self._endpoint.connect() as connection:
                self._opened.set()
                await self._carry(connection, client)

    async def _carry(self, connection: ClientConnection, client: AsyncHttpClient) -> None:
        """Route frames to their streams until the tunnel closes, then abandon what was in flight."""
        try:
            async for message in connection:
                self._route(ServiceFrame.decode(message), connection, client)
        finally:
            abandoned = [task for _stream, task in self._streams.values()]
            for task in abandoned:
                task.cancel()
            await asyncio.gather(*abandoned, return_exceptions=True)

    def _route(self, frame: ServiceFrame, connection: ClientConnection, client: AsyncHttpClient) -> None:
        """Start a stream for a new request, end one its caller reset, and hand any other frame to its stream."""
        if frame.kind == ServiceFrame.OPEN:
            stream = ServiceStream(frame.stream, client, partial(self._write, connection))
            task = asyncio.create_task(stream.answer(frame.payload))
            self._streams[frame.stream] = (stream, task)
            task.add_done_callback(partial(self._finished, frame.stream))
        elif frame.stream in self._streams:
            stream, task = self._streams[frame.stream]
            if frame.kind == ServiceFrame.RESET:
                task.cancel()
            else:
                stream.receive(frame)

    def _finished(self, number: int, _task: asyncio.Task[None]) -> None:
        """Forget a stream whose work ended."""
        self._streams.pop(number, None)

    @staticmethod
    async def _write(connection: ClientConnection, frame: ServiceFrame) -> None:
        """Write one frame to the tunnel."""
        await connection.send(frame.encode())
