"""ToolTask — wraps a plain function as a Task.

Backed by ToolModule (a trivial one-step StateModule):

    Initialize → [CallFunction effect] → FunctionComplete → CompletedOutput

Handles sync and async functions. On exception, produces FailedOutput.
Inherits execute()/run() from ModuleTask[ToolTaskConfig].
"""

import importlib
import inspect
import json
from collections.abc import Callable
from copy import deepcopy
from functools import reduce
from typing import Any, Literal

import structlog
from pydantic import BaseModel, ConfigDict, field_validator

from mistralai.vibe.sdk.agent.execution.loop import EffectRegistry, StateModule, StateSink
from mistralai.vibe.sdk.agent.tasks.core import StatefulTask
from mistralai.vibe.sdk.agent.tasks.runtime import ModuleTask, TaskConfigBase
from mistralai.vibe.sdk.capabilities.types import ToolResult
from mistralai.vibe.sdk.execution_record.snapshots import latest_snapshot, make_snapshot_entry
from mistralai.vibe.sdk.execution_record.state import (
    CompletedOutput,
    FailedOutput,
    TaskState,
)

logger = structlog.get_logger()


def _import_dotted_path(dotted_path: str) -> Any:
    """Import a callable from a dotted path like ``json.JSONEncoder.encode``.

    Tries progressively shorter module paths until one imports, then
    walks the remaining segments via getattr. Handles class methods,
    nested classes, and other non-top-level callables that
    ``rsplit('.', 1)`` cannot resolve.
    """
    parts = dotted_path.split(".")
    # Try longest module path first, shorten until import succeeds
    for i in range(len(parts), 0, -1):
        module_path = ".".join(parts[:i])
        try:
            mod = importlib.import_module(module_path)
        except (ImportError, ModuleNotFoundError):
            continue
        if i == len(parts):
            return mod
        return reduce(getattr, parts[i:], mod)
    msg = f"Cannot import '{dotted_path}': no importable module prefix found"
    raise ImportError(msg)


# ---------------------------------------------------------------------------
# Serializable task config
# ---------------------------------------------------------------------------


class ToolTaskConfig[ContextT](TaskConfigBase):
    """Config for reconstructing a ToolTask from a dotted import path."""

    type: Literal["tool"] = "tool"
    fn_path: str  # e.g. "myapp.tools.web_search"
    name: str
    description: str = ""
    input_schema: dict[str, Any] | None = None
    ctx: ContextT | None = None
    snapshot_type: str | None = None


# ---------------------------------------------------------------------------
# Actions and effects
# ---------------------------------------------------------------------------


class ToolInitialize(BaseModel):
    """Seed action for ToolModule."""


class ToolContext(BaseModel):
    """Fallback model for serialized tool contexts."""

    model_config = ConfigDict(extra="allow")


def _coerce_tool_context(ctx: ToolContext | dict[str, Any] | None) -> ToolContext | None:
    if ctx is None or isinstance(ctx, ToolContext):
        return ctx
    if isinstance(ctx, dict):
        return ToolContext.model_validate(ctx)

    msg = "Tool ctx must be a dict or None"
    raise TypeError(msg)


class CallFunction(BaseModel):
    """Effect: call the wrapped function.

    Carries state for argument extraction and fn_path for
    reconstruction on the activity path.
    """

    state: TaskState
    fn_path: str | None = None
    ctx: ToolContext | None = None
    snapshot_type: str | None = None

    @field_validator("ctx", mode="before")
    @classmethod
    def _validate_ctx(cls, ctx: Any) -> ToolContext | None:
        return _coerce_tool_context(ctx)


class FunctionComplete(BaseModel):
    """Action: function completed. Carries the output state."""

    output_state: TaskState


# ---------------------------------------------------------------------------
# Effect handler registry
# ---------------------------------------------------------------------------

_tool_registry = EffectRegistry()


@_tool_registry.handles(CallFunction)
async def _handle_call_function(
    effect: CallFunction,
    sink: StateSink,
    fn: Callable[..., Any] | None = None,
) -> list[FunctionComplete]:
    """Call the wrapped function, return FunctionComplete.

    On the local path, the module injects ``fn`` directly.
    On the workflow activity path, ``fn`` is None and the handler
    imports the function from ``effect.fn_path``.
    """
    state = effect.state
    try:
        if fn is None:
            if effect.fn_path is None:
                msg = "No fn and no fn_path on CallFunction effect"
                raise ValueError(msg)
            fn = _import_dotted_path(effect.fn_path)

        assert fn is not None

        positional: list[Any] = []
        if effect.ctx is not None:
            positional.append(effect.ctx)
        if effect.snapshot_type is not None:
            positional.append(deepcopy(latest_snapshot(state, effect.snapshot_type)))

        args = state.input
        if isinstance(args, dict):
            result = fn(*positional, **args)
        elif args is not None:
            result = fn(*positional, args)
        else:
            result = fn(*positional)

        if inspect.isawaitable(result):
            result = await result

        # TODO(HAR-399): Make ToolResult the default response for all tools.
        annotations = None
        if isinstance(result, ToolResult):
            annotations = result.annotations or None
            result = result.value

        if isinstance(result, BaseModel):
            output_value = result.model_dump(mode="json")
        elif isinstance(result, str):
            output_value = result
        else:
            try:
                output_value = json.loads(json.dumps(result, default=str))
            except (TypeError, ValueError):
                output_value = str(result)

        new_state = state.model_copy(
            update={
                "output": CompletedOutput(value=output_value, annotations=annotations),
            }
        )
    except Exception as e:
        logger.exception("tool.execution_failed")
        new_state = state.model_copy(update={"output": FailedOutput(error=str(e))})

    return [FunctionComplete(output_state=new_state)]


# ---------------------------------------------------------------------------
# ToolModule — trivial one-step StateModule
# ---------------------------------------------------------------------------


class ToolModule(StateModule):
    """StateModule for a function-wrapping tool task.

    One-step lifecycle: Initialize → CallFunction → FunctionComplete → done.
    """

    effect_handlers = _tool_registry
    initial_action_type = ToolInitialize

    def __init__(
        self,
        fn: Callable[..., Any] | None,
        fn_path: str | None = None,
        ctx: ToolContext | dict[str, Any] | None = None,
    ) -> None:
        self._fn = fn
        self._fn_path = fn_path
        self._ctx = _coerce_tool_context(ctx)

    def reduce(self, state: TaskState, action: Any) -> tuple[TaskState, list[Any]]:
        match action:
            case ToolInitialize():
                return (
                    state,
                    [
                        CallFunction(
                            state=state,
                            fn_path=self._fn_path,
                            ctx=self._ctx,
                        )
                    ],
                )
            case FunctionComplete(output_state=output_state):
                return (output_state, [])
        return (state, [])

    async def handle_effect(self, effect: Any, sink: StateSink) -> list[Any]:
        handler = self.effect_handlers.get(type(effect))
        if handler is None:
            return []
        if isinstance(effect, CallFunction):
            result: list[Any] = await handler(effect, sink, fn=self._fn)
            return result
        result = await handler(effect, sink)
        return result


# ---------------------------------------------------------------------------
# ToolTask — ModuleTask wrapping a plain function
# ---------------------------------------------------------------------------


class ToolTask(ModuleTask[ToolTaskConfig]):
    """Wraps a plain function as a Task backed by ToolModule.

    The simplest task pattern. Given a function, it calls fn(state.input)
    and produces CompletedOutput or FailedOutput. Handles both sync and
    async functions.

    Inherits execute(), run(), and card metadata from ModuleTask.
    """

    def __init__(
        self,
        fn: Callable[..., Any] | None,
        name: str = "",
        description: str = "",
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        ctx: ToolContext | dict[str, Any] | None = None,
        fn_path: str | None = None,
        snapshot_type: str | None = None,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
        )
        self.fn = fn
        if fn_path is not None:
            self.fn_path = fn_path
        elif fn is not None:
            self.fn_path = f"{fn.__module__}.{fn.__qualname__}"
        else:
            self.fn_path = ""
        self.ctx = _coerce_tool_context(ctx)
        if snapshot_type is not None:
            self.snapshot_type = snapshot_type

    def create_module(self) -> ToolModule:
        if isinstance(self, StatefulTask):
            return StatefulToolModule(
                fn=self.fn,
                fn_path=self.fn_path,
                ctx=self.ctx,
                snapshot_type=self.snapshot_type,
            )

        return ToolModule(fn=self.fn, fn_path=self.fn_path, ctx=self.ctx)

    @classmethod
    def from_config(cls, config: Any, **kwargs: Any) -> "ToolTask":
        if not isinstance(config, ToolTaskConfig):
            config = ToolTaskConfig.model_validate(config)
        return cls(
            fn=None,
            name=config.name,
            description=config.description,
            input_schema=config.input_schema,
            ctx=config.ctx,
            fn_path=config.fn_path,
            snapshot_type=config.snapshot_type,
        )


# ---------------------------------------------------------------------------
# StatefulToolModule — snapshot-carrying tool module (used when snapshot_type set)
# ---------------------------------------------------------------------------


class StatefulToolModule(ToolModule):
    """ToolModule variant that reads and writes a typed snapshot.

    On initialize, the snapshot is read and injected positionally into the
    function (after ``ctx`` when configured), ahead of the user input shape.
    On successful completion, the returned value is written back as the next
    snapshot appended to the child history. A failed run writes no snapshot.
    """

    def __init__(
        self,
        fn: Callable[..., Any] | None,
        fn_path: str | None = None,
        ctx: ToolContext | dict[str, Any] | None = None,
        snapshot_type: str = "",
    ) -> None:
        super().__init__(fn=fn, fn_path=fn_path, ctx=ctx)
        self._snapshot_type = snapshot_type

    def reduce(self, state: TaskState, action: Any) -> tuple[TaskState, list[Any]]:
        match action:
            case ToolInitialize():
                return (
                    state,
                    [
                        CallFunction(
                            state=state,
                            fn_path=self._fn_path,
                            ctx=self._ctx,
                            snapshot_type=self._snapshot_type,
                        )
                    ],
                )
            case FunctionComplete(output_state=output_state):
                if isinstance(output_state.output, CompletedOutput):
                    snapshot = make_snapshot_entry(self._snapshot_type, output_state.output.value)
                    written = output_state.model_copy(
                        update={"history": [*output_state.history, snapshot]}
                    )
                    return (written, [])
                return (output_state, [])
        return (state, [])
