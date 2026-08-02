"""Capability authoring helpers for the Vibe SDK."""

import inspect
from collections.abc import Awaitable, Callable
from typing import Any, overload

from pydantic import BaseModel

from mistralai.vibe.sdk.agent.tasks.core import Card, TaskCallback
from mistralai.vibe.sdk.capabilities.adapters.local_function import ToolTaskConfig
from mistralai.vibe.sdk.capabilities.types import ToolHandler, ToolHandlerContext
from mistralai.vibe.sdk.capabilities.types import ToolResult as AnnotatedToolResult
from mistralai.vibe.sdk.execution_record.state import CompletedOutput, FailedOutput, TaskState
from mistralai.vibe.sdk.transports.events import (
    CallbackCallEvent,
    CallbackResultEvent,
    CallbackResultPayload,
)

_KEYWORD_PASSABLE_PARAMETER_KINDS = {
    inspect.Parameter.POSITIONAL_OR_KEYWORD,
    inspect.Parameter.KEYWORD_ONLY,
}


def _validate_handler_signature(
    handler: Callable[..., Any], *, has_ctx: bool, has_state: bool
) -> None:
    signature = inspect.signature(handler)
    expected_names = {"args"}
    if has_ctx:
        expected_names.add("ctx")
    if has_state:
        expected_names.add("state")
    parameter_names = set(signature.parameters)

    if parameter_names != expected_names:
        expected_list = ", ".join(sorted(expected_names))
        raise ValueError(
            f"Tool handlers must accept exactly these named parameters: {expected_list}"
        )

    for name in expected_names:
        parameter = signature.parameters[name]
        if parameter.kind not in _KEYWORD_PASSABLE_PARAMETER_KINDS:
            raise ValueError(f"Tool handler parameter {name!r} must be passable by keyword")


class ToolDefinition[ToolInput: BaseModel, ToolResult]:
    """Stable SDK wrapper for an author-defined tool function."""

    def __init__(
        self,
        *,
        name: str,
        description: str,
        input_schema: type[ToolInput],
        handler: ToolHandler[ToolInput, ToolResult],
        result_schema: type[BaseModel] | None = None,
        ctx_schema: type[ToolHandlerContext] | None = None,
        ctx: ToolHandlerContext | dict[str, Any] | None = None,
        snapshot_type: str | None = None,
        snapshot_schema: type[BaseModel] | None = None,
    ) -> None:
        if not name.strip():
            raise ValueError("Tool name cannot be empty")
        if "." in handler.__qualname__:
            raise ValueError("Decorated tools must be defined at module scope")

        if ctx is not None and ctx_schema is None:
            raise ValueError("Tools must provide ctx_schema when providing ctx")

        if snapshot_schema is not None and snapshot_type is None:
            raise ValueError("Tools must provide snapshot_type when providing snapshot_schema")

        _validate_handler_signature(
            handler,
            has_ctx=ctx_schema is not None,
            has_state=snapshot_type is not None,
        )

        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler
        self.result_schema = result_schema
        self.ctx_schema = ctx_schema
        self.snapshot_type = snapshot_type
        self.snapshot_schema = snapshot_schema
        self.ctx: ToolHandlerContext | None = None
        if ctx_schema is not None and ctx is not None:
            ctx_data = ctx.model_dump(mode="json") if isinstance(ctx, BaseModel) else ctx
            self.ctx = ctx_schema.model_validate(ctx_data)
        self.fn_path = f"{handler.__module__}.{handler.__name__}.invoke"

        self.__doc__ = handler.__doc__
        self.__module__ = handler.__module__
        self.__name__ = handler.__name__
        self.__qualname__ = handler.__name__
        self.__wrapped__ = handler

    def __call__(
        self, args: ToolInput, *, state: Any | None = None
    ) -> ToolResult | Awaitable[ToolResult]:
        handler_kwargs: dict[str, Any] = {"args": args}
        if self.ctx_schema is not None:
            if self.ctx is None:
                raise ValueError("Contextual tools require ctx before direct calls")
            handler_kwargs["ctx"] = self.ctx
        if self.snapshot_type is not None:
            if state is not None and self.snapshot_schema is not None:
                state = self.snapshot_schema.model_validate(state)
            handler_kwargs["state"] = state

        return self.handler(**handler_kwargs)

    async def invoke(self, *positional: Any, **kwargs: Any) -> Any:
        """Protocol-facing callable used by ToolTask via ``fn_path``."""
        expected_positional = 0
        if self.ctx_schema is not None:
            expected_positional += 1
        if self.snapshot_type is not None:
            expected_positional += 1
        if len(positional) > expected_positional:
            raise TypeError(
                f"Tool {self.name!r} accepts at most {expected_positional} positional argument(s)"
            )

        remaining = list(positional)
        handler_kwargs: dict[str, Any] = {}

        if self.ctx_schema is not None:
            raw_ctx = remaining.pop(0) if remaining else None
            raw_ctx_data = (
                raw_ctx.model_dump(mode="json") if isinstance(raw_ctx, BaseModel) else raw_ctx
            )
            if raw_ctx_data is not None:
                handler_kwargs["ctx"] = self.ctx_schema.model_validate(raw_ctx_data)
            elif self.ctx is not None:
                handler_kwargs["ctx"] = self.ctx
            else:
                raise ValueError("Contextual tool invocations require ctx")

        if self.snapshot_type is not None:
            state = remaining.pop(0) if remaining else None
            if state is not None and self.snapshot_schema is not None:
                state = self.snapshot_schema.model_validate(state)
            handler_kwargs["state"] = state

        handler_kwargs["args"] = self.input_schema.model_validate(kwargs)
        result = self.handler(**handler_kwargs)
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, AnnotatedToolResult):
            return result
        if isinstance(result, BaseModel):
            return result.model_dump(mode="json")
        return result

    def to_config(self) -> ToolTaskConfig:
        """Build a protocol-native config for this tool."""
        config = {
            "fn_path": self.fn_path,
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema.model_json_schema(),
        }
        if self.snapshot_type is not None:
            config["snapshot_type"] = self.snapshot_type
        if self.ctx_schema is not None:
            if self.ctx is not None:
                config["ctx"] = self.ctx.model_dump(mode="json")
            else:
                raise ValueError("Contextual tools require ctx before serialization")

        return ToolTaskConfig.model_validate(config)


class ClientToolDefinition[ToolInput: BaseModel]:
    """SDK wrapper for a tool whose implementation is provided by the host client."""

    def __init__(
        self,
        *,
        name: str,
        description: str,
        input_schema: type[ToolInput],
        output_schema: type[BaseModel] | None = None,
        handler: ToolHandler[ToolInput, Any] | None = None,
    ) -> None:
        if not name.strip():
            raise ValueError("Tool name cannot be empty")

        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.handler: ToolHandler[ToolInput, Any] | None = None

        if handler is not None:
            self._bind_handler(handler)

    def with_handler(
        self,
        handler: ToolHandler[ToolInput, Any],
    ) -> ToolHandler[ToolInput, Any]:
        """Bind a host-side handler and return the decorated function."""
        self._bind_handler(handler)
        return handler

    def _bind_handler(self, handler: ToolHandler[ToolInput, Any]) -> None:
        self.handler = handler
        metadata_source = getattr(handler, "func", handler)
        self.__doc__ = getattr(metadata_source, "__doc__", None)
        self.__module__ = getattr(metadata_source, "__module__", type(handler).__module__)
        self.__name__ = getattr(metadata_source, "__name__", type(handler).__name__)
        self.__qualname__ = getattr(metadata_source, "__qualname__", self.__name__)
        self.__wrapped__ = handler

    def to_callback(self) -> TaskCallback:
        """Build the protocol callback declaration backing this client-handled tool."""
        return TaskCallback(
            card=Card(
                name=self.name,
                description=self.description,
                input_schema=self.input_schema.model_json_schema(),
                output_schema=(
                    self.output_schema.model_json_schema()
                    if self.output_schema is not None
                    else None
                ),
            )
        )


def tool[ToolInput: BaseModel](
    *,
    name: str,
    description: str,
    input_schema: type[ToolInput],
    result_schema: type[BaseModel] | None = None,
    ctx_schema: type[ToolHandlerContext] | None = None,
    ctx: ToolHandlerContext | dict[str, Any] | None = None,
    snapshot_type: str | None = None,
    snapshot_schema: type[BaseModel] | None = None,
) -> "_ToolDecorator[ToolInput]":
    """Decorate a module-level function as an SDK tool definition."""
    return _ToolDecorator(
        name=name,
        description=description,
        input_schema=input_schema,
        result_schema=result_schema,
        ctx_schema=ctx_schema,
        ctx=ctx,
        snapshot_type=snapshot_type,
        snapshot_schema=snapshot_schema,
    )


class _ToolDecorator[ToolInput: BaseModel]:
    def __init__(
        self,
        *,
        name: str,
        description: str,
        input_schema: type[ToolInput],
        ctx_schema: type[ToolHandlerContext] | None,
        ctx: ToolHandlerContext | dict[str, Any] | None,
        result_schema: type[BaseModel] | None = None,
        snapshot_type: str | None = None,
        snapshot_schema: type[BaseModel] | None = None,
    ) -> None:
        self._name = name
        self._description = description
        self._input_schema = input_schema
        self._result_schema = result_schema
        self._ctx_schema = ctx_schema
        self._ctx = ctx
        self._snapshot_type = snapshot_type
        self._snapshot_schema = snapshot_schema

    @overload
    def __call__[ToolResult](
        self, handler: Callable[..., Awaitable[ToolResult]]
    ) -> ToolDefinition[ToolInput, ToolResult]: ...
    @overload
    def __call__[ToolResult](
        self, handler: Callable[..., ToolResult]
    ) -> ToolDefinition[ToolInput, ToolResult]: ...
    def __call__[ToolResult](
        self,
        handler: ToolHandler[ToolInput, ToolResult],
    ) -> ToolDefinition[ToolInput, ToolResult]:
        return ToolDefinition(
            name=self._name,
            description=self._description,
            input_schema=self._input_schema,
            handler=handler,
            result_schema=self._result_schema,
            ctx_schema=self._ctx_schema,
            ctx=self._ctx,
            snapshot_type=self._snapshot_type,
            snapshot_schema=self._snapshot_schema,
        )


def client_tool[ToolInput: BaseModel](
    *,
    name: str,
    description: str,
    input_schema: type[ToolInput],
    output_schema: type[BaseModel] | None = None,
) -> Callable[[ToolHandler[ToolInput, Any]], ClientToolDefinition[ToolInput]]:
    """Decorate a host-side function as a client-handled tool.

    When the agent calls this tool, sessions yield a ``CallbackCallEvent`` instead
    of invoking Python code through a protocol ``ToolTaskConfig``. Sessions resolve
    the callback automatically by calling the decorated host function.
    """

    def decorator(handler: ToolHandler[ToolInput, Any]) -> ClientToolDefinition[ToolInput]:
        return ClientToolDefinition(
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            handler=handler,
        )

    return decorator


def client_tool_result(event: CallbackCallEvent, result: Any) -> CallbackResultEvent:
    """Build the success event to send after handling a client tool callback."""
    annotations = None
    if isinstance(result, AnnotatedToolResult):
        annotations = result.annotations or None
        result = result.value
    value = result.model_dump(mode="json") if isinstance(result, BaseModel) else result
    return CallbackResultEvent(
        payload=CallbackResultPayload(
            id=event.payload.id,
            name=event.payload.name,
            state=TaskState(
                id=event.payload.id,
                input=event.payload.input,
                output=CompletedOutput(value=value, annotations=annotations),
            ),
            path=event.payload.path,
        )
    )


def client_tool_error(event: CallbackCallEvent, error: str) -> CallbackResultEvent:
    """Build the failure event to send after a client tool callback cannot complete."""
    return CallbackResultEvent(
        payload=CallbackResultPayload(
            id=event.payload.id,
            name=event.payload.name,
            state=TaskState(
                id=event.payload.id,
                input=event.payload.input,
                output=FailedOutput(error=error),
            ),
            path=event.payload.path,
        )
    )
