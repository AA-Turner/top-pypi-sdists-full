import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable, Mapping
from functools import partial
from typing import Any

import anyio
import sse_starlette
import sse_starlette.sse
import structlog.stdlib
from starlette.types import Message, Receive, Scope, Send

from langgraph_api.asyncio import aclosing
from langgraph_api.serde import json_dumpb

logger = structlog.stdlib.get_logger(__name__)
# Version 2 is listen_for_exit_signal and listen_for_disconnect
# Version 3 is _listen_for_exit_signal and _listen_for_disconnect
USE_PUBLIC_SSE = hasattr(sse_starlette.EventSourceResponse, "listen_for_disconnect")
# A client that stops reading but keeps the connection open would otherwise
# block a send forever, holding the stream generator and the run behind it.
# Long enough to flush one 28 MB event over a 2 Mbit/s link.
SEND_TIMEOUT_SECS = 120
HEARTBEAT_SECS = 5


class EventSourceResponse(sse_starlette.EventSourceResponse):
    def __init__(
        self,
        content: AsyncIterator[
            bytes | tuple[bytes, Any | bytes] | tuple[bytes, Any | bytes, bytes | None]
        ],
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        *,
        on_close: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            send_timeout=SEND_TIMEOUT_SECS,
        )
        self._on_close = on_close

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            async with anyio.create_task_group() as task_group:
                # https://trio.readthedocs.io/en/latest/reference-core.html#custom-supervisors
                async def wrap(func: Callable[[], Awaitable[None]]) -> None:
                    await func()
                    # noinspection PyAsyncCall
                    task_group.cancel_scope.cancel()

                task_group.start_soon(wrap, partial(self.stream_response, send))
                if USE_PUBLIC_SSE:
                    task_group.start_soon(wrap, self.listen_for_exit_signal)
                else:
                    task_group.start_soon(wrap, self._listen_for_exit_signal)

                if self.data_sender_callable:
                    task_group.start_soon(self.data_sender_callable)

                if USE_PUBLIC_SSE:
                    await wrap(partial(self.listen_for_disconnect, receive))
                else:
                    await wrap(partial(self._listen_for_disconnect, receive))
        except* sse_starlette.sse.SendTimeoutError:
            await logger.awarning("Closing a stream whose client stopped reading")
        finally:
            # The body never starts when the headers can't be sent, so a stream
            # an endpoint opened before building the response is released here.
            if self._on_close is not None:
                with anyio.CancelScope(shield=True):
                    await self._on_close()

        if self.background is not None:  # pragma: no cover, tested in StreamResponse
            await self.background()

    async def stream_response(self, send: Send) -> None:
        await self._send(
            send,
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            },
        )
        # A heartbeat that times out must end the response too: on an idle
        # thread stream it is the only send.
        async with anyio.create_task_group() as heartbeat:
            heartbeat.start_soon(self._heartbeat, send)
            async with aclosing(self.body_iterator) as body:
                try:
                    async for data in body:
                        await self._send(
                            send,
                            {
                                "type": "http.response.body",
                                "body": (
                                    json_to_sse(*data)
                                    if isinstance(data, tuple)
                                    else data
                                ),
                                "more_body": True,
                            },
                        )
                except sse_starlette.sse.SendTimeoutError:
                    raise
                except Exception as exc:
                    await logger.aexception("Error streaming response", exc_info=exc)
                    await self._send(
                        send,
                        {
                            "type": "http.response.body",
                            "body": json_to_sse(b"error", exc),
                            "more_body": True,
                        },
                    )
            heartbeat.cancel_scope.cancel()

        async with self._send_lock:
            self.active = False
            await self._send(
                send, {"type": "http.response.body", "body": b"", "more_body": False}
            )

    async def _heartbeat(self, send: Send) -> None:
        payload = sse_starlette.ServerSentEvent(comment="heartbeat").encode()
        while True:
            await asyncio.sleep(HEARTBEAT_SECS)
            await self._send(
                send, {"type": "http.response.body", "body": payload, "more_body": True}
            )

    async def _send(self, send: Send, message: Message) -> None:
        # uvicorn waits for the client to drain its buffer before every send, so
        # once a client stops reading, whichever send comes next blocks.
        with anyio.move_on_after(self.send_timeout) as timeout:
            await send(message)
        if timeout.cancelled_caught:
            raise sse_starlette.sse.SendTimeoutError()


SEP = b"\r\n"
EVENT = b"event: "
DATA = b"data: "
ID = b"id: "
BYTES_LIKE = (bytes, bytearray, memoryview)


def _sanitize_sse_field(value: bytes) -> bytes:
    return value.replace(b"\r", b"").replace(b"\n", b"")


def json_to_sse(event: bytes, data: Any | bytes, id: bytes | None = None) -> bytes:
    result = b"".join(
        (
            EVENT,
            _sanitize_sse_field(event),
            SEP,
            DATA,
            data if isinstance(data, BYTES_LIKE) else json_dumpb(data),
            SEP,
        )
    )

    if id is not None:
        result += b"".join((ID, _sanitize_sse_field(id), SEP))

    result += SEP
    return result
