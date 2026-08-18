"""Streamable HTTP transport adapter."""

from __future__ import annotations

import asyncio
import contextlib
import uuid
from collections.abc import AsyncIterator, Callable
from typing import TYPE_CHECKING, Any

import httpx
import structlog
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse
from starlette.routing import Route

from mistralai.vibe.sdk.agent.execution.resources import (
    ResourcesScope,
    bind_execution_scope,
    stop_execution_scope,
)
from mistralai.vibe.sdk.execution_record.patching.json_patch import apply_patches
from mistralai.vibe.sdk.execution_record.state import TaskState

if TYPE_CHECKING:
    from mistralai.vibe.sdk.agent.tasks.core import Card, TaskCallback
    from mistralai.vibe.sdk.transports.channel import Channel
    from mistralai.vibe.sdk.transports.events import (
        DownstreamMessage,
        TaskStateUpdateEvent,
        UpstreamMessage,
    )

logger = structlog.get_logger()


def _serialize_downstream_message_as_sse(message: DownstreamMessage) -> str | None:
    from mistralai.vibe.sdk.transports.events import (
        CallbackCallEvent,
        TaskResultEvent,
        TaskStateUpdateEvent,
    )

    if not isinstance(message, TaskStateUpdateEvent | TaskResultEvent | CallbackCallEvent):
        return None

    data = message.model_dump_json()
    return f"event: {message.type}\ndata: {data}\n\n"


class StreamableHttpBinding:
    """Host-side binding that exposes a task as a Starlette ASGI app."""

    def __init__(
        self,
        task: Any,
        on_event: Callable[[TaskState, TaskStateUpdateEvent], None] | None = None,
    ) -> None:
        self._task = task
        self._on_event = on_event
        self._sessions: dict[str, Channel] = {}
        self._app = Starlette(
            routes=[
                Route("/definition", self._handle_definition, methods=["GET"]),
                Route("/run", self._handle_run, methods=["POST"]),
                Route("/send/{session_id}", self._handle_send, methods=["POST"]),
            ],
        )

    @property
    def app(self) -> Starlette:
        return self._app

    async def _handle_definition(self, request: Request) -> Response:
        return JSONResponse(self._task.card.model_dump())

    async def _handle_run(self, request: Request) -> Response:
        from mistralai.vibe.sdk.transports.events import TaskStateUpdateEvent

        body = await request.json()
        state = TaskState.model_validate(body)
        session_id = str(uuid.uuid4())

        scope = ResourcesScope()
        try:
            with bind_execution_scope(scope):
                channel = await self._task.run(state)
        except BaseException:
            await scope.aclose()
            raise
        self._sessions[session_id] = channel

        on_event = self._on_event

        async def event_generator() -> AsyncIterator[str]:
            nonlocal state
            try:
                with bind_execution_scope(scope):
                    async for message in channel:
                        if isinstance(message, TaskStateUpdateEvent) and on_event is not None:
                            state = apply_patches(state, message.payload.patches)
                            on_event(state, message)
                        if event := _serialize_downstream_message_as_sse(message):
                            with stop_execution_scope():
                                yield event
            except Exception:
                logger.exception("http.stream_error")
            finally:
                self._sessions.pop(session_id, None)
                try:
                    await channel.close()
                finally:
                    await scope.aclose()

        return StreamingResponse(
            content=event_generator(),
            media_type="text/event-stream",
            headers={
                "x-session-id": session_id,
                "cache-control": "no-cache",
            },
        )

    async def _handle_send(self, request: Request) -> Response:
        from mistralai.vibe.sdk.transports.events import (
            CallbackResultEvent,
            CallbackStateUpdateEvent,
        )

        session_id = request.path_params["session_id"]
        channel = self._sessions.get(session_id)
        if channel is None:
            return JSONResponse({"error": "unknown session"}, status_code=404)

        body = await request.json()
        msg_type = body.get("type")
        if msg_type == "callback_result":
            message = CallbackResultEvent.model_validate(body)
            await channel.send(message)
            return JSONResponse({"ok": True})
        if msg_type == "callback_state_update":
            message = CallbackStateUpdateEvent.model_validate(body)
            await channel.send(message)
            return JSONResponse({"ok": True})
        return JSONResponse(
            {"error": f"unsupported message type: {msg_type}"},
            status_code=422,
        )


class StreamableHttpChannel:
    """Client-side channel backed by SSE plus a POST side-channel."""

    def __init__(
        self,
        downstream: asyncio.Queue[DownstreamMessage | None],
        background_task: asyncio.Task[None],
        base_url: str,
        session_id_future: asyncio.Future[str],
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._downstream = downstream
        self._bg = background_task
        self._base_url = base_url
        self._session_id_future = session_id_future
        self._transport = transport

    async def __aiter__(self) -> AsyncIterator[DownstreamMessage]:
        while True:
            msg = await self._downstream.get()
            if msg is None:
                break
            yield msg
        if self._bg.done():
            exc = self._bg.exception()
            if exc is not None:
                raise exc

    async def send(self, message: UpstreamMessage) -> None:
        session_id = await self._session_id_future
        async with httpx.AsyncClient(transport=self._transport, base_url=self._base_url) as client:
            await client.post(
                f"/send/{session_id}",
                json=message.model_dump() if hasattr(message, "model_dump") else {},
            )

    async def close(self) -> None:
        self._bg.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._bg


class StreamableHttpRemoteTask:
    """Caller-side remote task over Streamable HTTP."""

    def __init__(
        self,
        base_url: str,
        name: str = "",
        description: str = "",
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        callbacks: list[TaskCallback] | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.callbacks: list[TaskCallback] = callbacks or []
        self._base_url = base_url
        self._transport = transport

    @classmethod
    async def connect(
        cls,
        base_url: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> StreamableHttpRemoteTask:
        from mistralai.vibe.sdk.agent.tasks.core import Card

        async with httpx.AsyncClient(transport=transport, base_url=base_url) as client:
            resp = await client.get("/definition")
            resp.raise_for_status()
            data = resp.json()
        defn = Card.model_validate(data)
        return cls(
            base_url=base_url,
            name=defn.name,
            description=defn.description,
            input_schema=defn.input_schema,
            output_schema=defn.output_schema,
            callbacks=defn.callbacks,
            transport=transport,
        )

    @property
    def card(self) -> Card:
        from mistralai.vibe.sdk.agent.tasks.core import Card

        return Card(
            name=self.name,
            description=self.description,
            input_schema=self.input_schema,
            output_schema=self.output_schema,
            callbacks=self.callbacks,
        )

    async def run(self, state: TaskState) -> Channel:
        downstream: asyncio.Queue[DownstreamMessage | None] = asyncio.Queue()
        session_id_future: asyncio.Future[str] = asyncio.get_running_loop().create_future()

        bg_task = asyncio.create_task(self._stream_bg(state, downstream, session_id_future))
        return StreamableHttpChannel(
            downstream=downstream,
            background_task=bg_task,
            base_url=self._base_url,
            session_id_future=session_id_future,
            transport=self._transport,
        )

    async def _stream_bg(
        self,
        state: TaskState,
        downstream: asyncio.Queue[DownstreamMessage | None],
        session_id_future: asyncio.Future[str],
    ) -> None:
        try:
            async with (
                httpx.AsyncClient(transport=self._transport, base_url=self._base_url) as client,
                client.stream("POST", "/run", json=state.model_dump(), timeout=None) as response,
            ):
                response.raise_for_status()

                session_id = response.headers.get("x-session-id", "")
                if not session_id_future.done():
                    session_id_future.set_result(session_id)

                await self._parse_sse_stream(response, downstream)
        except Exception as exc:
            if not session_id_future.done():
                session_id_future.set_exception(exc)
            raise
        finally:
            await downstream.put(None)

    async def _parse_sse_stream(
        self,
        response: httpx.Response,
        downstream: asyncio.Queue[DownstreamMessage | None],
    ) -> None:
        buffer = ""
        async for text in response.aiter_text():
            buffer += text
            while "\n\n" in buffer:
                event_text, buffer = buffer.split("\n\n", 1)
                event = self._parse_sse_event(event_text.strip())
                if event is not None:
                    await downstream.put(event)

        if buffer.strip():
            event = self._parse_sse_event(buffer.strip())
            if event is not None:
                await downstream.put(event)

    @staticmethod
    def _parse_sse_event(event_text: str) -> DownstreamMessage | None:
        from mistralai.vibe.sdk.transports.events import (
            CallbackCallEvent,
            TaskResultEvent,
            TaskStateUpdateEvent,
        )

        event_type = "history_update"
        data_parts: list[str] = []
        for line in event_text.split("\n"):
            if line.startswith("event: "):
                event_type = line[7:].strip()
            elif line.startswith("event:"):
                event_type = line[6:].strip()
            elif line.startswith("data: "):
                data_parts.append(line[6:])
            elif line.startswith("data:"):
                data_parts.append(line[5:])

        if not data_parts:
            return None

        data_str = "\n".join(data_parts)
        try:
            match event_type:
                case "history_update":
                    return TaskStateUpdateEvent.model_validate_json(data_str)
                case "task_result":
                    return TaskResultEvent.model_validate_json(data_str)
                case "callback_call":
                    return CallbackCallEvent.model_validate_json(data_str)
                case _:
                    return None
        except Exception:
            logger.warning("http.sse_parse_failed", data=data_str[:200])
            return None


__all__ = [
    "StreamableHttpBinding",
    "StreamableHttpChannel",
    "StreamableHttpRemoteTask",
]
