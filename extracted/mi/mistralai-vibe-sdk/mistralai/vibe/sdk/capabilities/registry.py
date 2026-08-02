"""Registry helpers for client-handled SDK capabilities."""

import asyncio
import inspect
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import structlog
from pydantic import BaseModel

from mistralai.vibe.sdk.capabilities.authoring import (
    ClientToolDefinition,
    client_tool_error,
    client_tool_result,
)
from mistralai.vibe.sdk.capabilities.client_tool_context import (
    ClientToolExecutionContext,
    current_client_tool_context,
    exception_type,
    reset_client_tool_context,
    set_client_tool_context,
)
from mistralai.vibe.sdk.capabilities.types import ToolHandler, ToolResult
from mistralai.vibe.sdk.observability import otel
from mistralai.vibe.sdk.transports.events import CallbackCallEvent, CallbackResultEvent

logger = structlog.get_logger()

if TYPE_CHECKING:
    from mistralai.vibe.sdk.agent.sessions.types import (
        AsyncCallbackSession,
        SyncCallbackSession,
    )


@dataclass(slots=True)
class _ClientToolRegistryEntry:
    tool: ClientToolDefinition[Any]
    handler: ToolHandler[Any, Any]


@dataclass(slots=True)
class _ClientToolResponse:
    event: CallbackResultEvent | None
    failure_stage: str | None = None
    error_type: str | None = None
    raised_exception: Exception | None = None


class ClientToolRegistry:
    """Routes client-handled tool callback events to host-side handlers.

    Register each client tool with the same key used in ``AgentConfig.tools``.
    When a session yields a ``CallbackCallEvent``, pass it to this registry to
    validate the input, call the host implementation, validate the output, and
    send the corresponding callback result or error back to the session.
    """

    def __init__(self) -> None:
        self._entries: dict[str, _ClientToolRegistryEntry] = {}

    def register(
        self,
        name: str,
        tool: ClientToolDefinition[Any],
        handler: ToolHandler[Any, Any],
    ) -> "ClientToolRegistry":
        """Register a host-side implementation for the given tool key."""
        if not name.strip():
            raise ValueError("Client tool registry key cannot be empty")
        if name in self._entries:
            raise ValueError(f"Client tool already registered: {name}")

        self._entries[name] = _ClientToolRegistryEntry(tool=tool, handler=handler)
        return self

    def can_handle(self, event: CallbackCallEvent) -> bool:
        """Return true if this registry has a handler for the callback event."""
        return event.payload.name in self._entries

    def __bool__(self) -> bool:
        return bool(self._entries)

    async def handle_event(
        self,
        session: "AsyncCallbackSession",
        event: CallbackCallEvent,
    ) -> None:
        """Resolve a callback request and send its result on an async session."""
        context = ClientToolExecutionContext(event=event, call_mode="async")
        token = set_client_tool_context(context)
        try:
            with otel.start_span(context.span_name, context.attributes()) as span:
                try:
                    response = await self._resolve_event(event)
                    context.record_result(
                        failure_stage=response.failure_stage,
                        error_type=response.error_type,
                    )
                    if response.event is None:
                        return
                    try:
                        await session.send_message(response.event)
                    except asyncio.CancelledError:
                        context.mark_canceled()
                        raise
                    except Exception as exc:
                        context.mark_send_failed(exc)
                        logger.exception(
                            "vibe_sdk.client_tool.failed",
                            **context.log_context(),
                            failure_stage="send_message",
                        )
                        raise
                except asyncio.CancelledError:
                    context.mark_canceled()
                    raise
                finally:
                    _finish_tool_execution_span(span, context)
        finally:
            reset_client_tool_context(token)

    def handle_event_sync(
        self,
        session: "SyncCallbackSession",
        event: CallbackCallEvent,
    ) -> None:
        """Resolve a callback request and send its result on a sync session."""
        context = ClientToolExecutionContext(event=event, call_mode="sync")
        token = set_client_tool_context(context)
        try:
            with otel.start_span(context.span_name, context.attributes()) as span:
                try:
                    response = self._resolve_event_sync(event)
                    context.record_result(
                        failure_stage=response.failure_stage,
                        error_type=response.error_type,
                    )
                    if response.raised_exception is not None:
                        raise response.raised_exception
                    if response.event is None:
                        return
                    try:
                        session.send_message(response.event)
                    except Exception as exc:
                        context.mark_send_failed(exc)
                        logger.exception(
                            "vibe_sdk.client_tool.failed",
                            **context.log_context(),
                            failure_stage="send_message",
                        )
                        raise
                finally:
                    _finish_tool_execution_span(span, context)
        finally:
            reset_client_tool_context(token)

    async def _resolve_event(self, event: CallbackCallEvent) -> _ClientToolResponse:
        prepared = self._prepare_call(event)
        if isinstance(prepared, CallbackResultEvent):
            return _ClientToolResponse(
                event=prepared,
                failure_stage=self._preparation_failure_stage(event),
            )

        entry, args = prepared
        try:
            result = entry.handler(args)
            if inspect.isawaitable(result):
                result = await result
        except Exception as exc:
            context = current_client_tool_context()
            logger.exception(
                "vibe_sdk.client_tool.failed",
                **(context.log_context() if context is not None else _event_log_context(event)),
                failure_stage="handler",
            )
            return _ClientToolResponse(
                event=client_tool_error(event, str(exc)),
                failure_stage="handler",
                error_type=exception_type(exc),
            )

        return self._build_response(event, entry, result)

    def _resolve_event_sync(self, event: CallbackCallEvent) -> _ClientToolResponse:
        prepared = self._prepare_call(event)
        if isinstance(prepared, CallbackResultEvent):
            return _ClientToolResponse(
                event=prepared,
                failure_stage=self._preparation_failure_stage(event),
            )

        entry, args = prepared
        try:
            result = entry.handler(args)
        except Exception as exc:
            context = current_client_tool_context()
            logger.exception(
                "vibe_sdk.client_tool.failed",
                **(context.log_context() if context is not None else _event_log_context(event)),
                failure_stage="handler",
            )
            return _ClientToolResponse(
                event=client_tool_error(event, str(exc)),
                failure_stage="handler",
                error_type=exception_type(exc),
            )

        if inspect.isawaitable(result):
            close = getattr(result, "close", None)
            if callable(close):
                close()
            msg = (
                f"Client tool handler for '{event.payload.name}' returned an awaitable; "
                "use handle_event() or register a synchronous handler"
            )
            return _ClientToolResponse(
                event=None,
                failure_stage="handler_returned_awaitable",
                raised_exception=RuntimeError(msg),
            )

        return self._build_response(event, entry, result)

    def _build_response(
        self,
        event: CallbackCallEvent,
        entry: _ClientToolRegistryEntry,
        result: Any,
    ) -> _ClientToolResponse:
        try:
            return _ClientToolResponse(
                event=self._build_success_event(event, entry, result),
            )
        except Exception as exc:
            context = current_client_tool_context()
            logger.exception(
                "vibe_sdk.client_tool.failed",
                **(context.log_context() if context is not None else _event_log_context(event)),
                failure_stage="output_validation",
            )
            return _ClientToolResponse(
                event=client_tool_error(event, str(exc)),
                failure_stage="output_validation",
                error_type=exception_type(exc),
            )

    def _preparation_failure_stage(self, event: CallbackCallEvent) -> str:
        if event.payload.name not in self._entries:
            return "unsupported_tool"
        return "input_validation"

    def _prepare_call(
        self,
        event: CallbackCallEvent,
    ) -> tuple[_ClientToolRegistryEntry, BaseModel] | CallbackResultEvent:
        entry = self._entries.get(event.payload.name)
        if entry is None:
            return client_tool_error(event, f"Unsupported client tool: {event.payload.name}")

        raw_input = {} if event.payload.input is None else event.payload.input
        try:
            args = entry.tool.input_schema.model_validate(raw_input)
        except Exception as exc:
            return client_tool_error(event, str(exc))

        return entry, args

    def _build_success_event(
        self,
        event: CallbackCallEvent,
        entry: _ClientToolRegistryEntry,
        result: Any,
    ) -> CallbackResultEvent:
        if isinstance(result, ToolResult) and entry.tool.output_schema is not None:
            result = result.model_copy(
                update={"value": entry.tool.output_schema.model_validate(result.value)}
            )
        elif entry.tool.output_schema is not None:
            result = entry.tool.output_schema.model_validate(result)
        return client_tool_result(event, result)


def _finish_tool_execution_span(
    span: otel.Span,
    context: ClientToolExecutionContext,
) -> None:
    span.set_attributes(otel.otel_attributes(context.attributes()))
    if context.error_type is not None:
        span.set_status(otel.Status(otel.StatusCode.ERROR))


def _event_log_context(event: CallbackCallEvent) -> dict[str, object]:
    return {
        "tool_name": event.payload.name,
        "callback_id": event.payload.id,
    }
