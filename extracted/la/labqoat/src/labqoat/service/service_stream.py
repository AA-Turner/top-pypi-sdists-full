"""One caller's request, answered from the local server a chunk at a time in both directions."""

import asyncio
import json
from collections.abc import AsyncIterator, Awaitable, Callable

from labqoat.json_document import JsonDocument
from labqoat.net.async_http_client import AsyncHttpClient
from labqoat.net.http_error import HttpError
from labqoat.service.service_frame import ServiceFrame


class ServiceStream:
    """Carry one request to the local server and its response back, each chunk acknowledged before the next.

    A request whose local exchange fails for any reason is reset, which its caller sees as a gateway failure;
    a caller that goes away resets the stream from the other side, which cancels this one's work.
    """

    def __init__(self, number: int, client: AsyncHttpClient, send: Callable[[ServiceFrame], Awaitable[None]]) -> None:
        """Bind the stream's number, the client that reaches the local server and the tunnel's writer."""
        self._number = number
        self._client = client
        self._send = send
        self._body: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._acknowledged: asyncio.Queue[None] = asyncio.Queue()

    def receive(self, frame: ServiceFrame) -> None:
        """Take a frame the caller's side sent for this stream: an acknowledgement, a chunk, or the body's end."""
        if frame.kind == ServiceFrame.ACK:
            self._acknowledged.put_nowait(None)
        else:
            self._body.put_nowait(frame.payload if frame.kind == ServiceFrame.DATA else None)

    async def answer(self, head: bytes) -> None:
        """Forward the request and relay the response; a failure on this side resets the stream."""
        try:
            await self._exchange(JsonDocument.expect_dict(json.loads(head)))
        except (HttpError, KeyError, TypeError, ValueError) as error:
            reason = f"{type(error).__name__}: {error}".encode()[:512]
            await self._send(ServiceFrame(ServiceFrame.RESET, self._number, reason))

    async def _exchange(self, request: JsonDocument) -> None:
        """Send the request with the caller's body, if it has one, and stream what the server answers."""
        method = JsonDocument.expect_scalar(request["method"], str)
        path = JsonDocument.expect_scalar(request["path"], str)
        content = self._uploaded() if request["body"] is True else None
        target = self._client.stream(method, path, headers=self._headers(request), content=content)
        async with target as response:
            listed = [[name, value] for name, value in response.headers.multi_items()]
            head = json.dumps({"status": response.status_code, "headers": listed}).encode()
            await self._send(ServiceFrame(ServiceFrame.HEAD, self._number, head))
            async for chunk in response.aiter_raw():
                await self._relay(chunk)
        await self._send(ServiceFrame(ServiceFrame.FINISH, self._number))

    @staticmethod
    def _headers(request: JsonDocument) -> list[tuple[str, str]]:
        """Read the caller's headers as the ordered pairs they arrived in."""
        pairs = (JsonDocument.expect_list(pair) for pair in JsonDocument.expect_list(request["headers"]))
        return [
            (JsonDocument.expect_scalar(name, str), JsonDocument.expect_scalar(value, str)) for name, value in pairs
        ]

    async def _uploaded(self) -> AsyncIterator[bytes]:
        """Yield the caller's body; being asked for the next chunk acknowledges the one before."""
        while (chunk := await self._body.get()) is not None:
            yield chunk
            await self._send(ServiceFrame(ServiceFrame.ACK, self._number))

    async def _relay(self, received: bytes) -> None:
        """Send what the server wrote in frames the tunnel accepts, waiting for each to be taken."""
        for start in range(0, len(received), ServiceFrame.CHUNK):
            part = received[start : start + ServiceFrame.CHUNK]
            await self._send(ServiceFrame(ServiceFrame.DATA, self._number, part))
            await self._acknowledged.get()
