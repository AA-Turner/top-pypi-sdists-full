"""Async environments and signature-derived tools. Execution stays with the user."""

from __future__ import annotations

import asyncio
import copy
import inspect
import json
import math
import time
import types
from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from dataclasses import dataclass
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Annotated,
    Literal,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

if TYPE_CHECKING:
    from .trajectory import Trajectory

from river_client.renderers import Message

from .config import _integer


def _schema(annotation):
    origin, args = get_origin(annotation), get_args(annotation)
    if origin is Annotated:
        return {**_schema(args[0]), "description": str(args[1])}
    if origin in (Union, types.UnionType):
        return {"anyOf": [_schema(arg) for arg in args]}
    if origin is Literal:
        return {"enum": list(args)}
    if origin is list:
        return {"type": "array", "items": _schema(args[0])}
    if origin is dict and args[0] is str:
        return {"type": "object", "additionalProperties": _schema(args[1])}
    names = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        type(None): "null",
    }
    if annotation in names:
        return {"type": names[annotation]}
    raise TypeError(
        f"unsupported tool annotation {annotation!r}; use JSON-compatible types"
    )


def _validate(value, schema):
    if "anyOf" in schema:
        return any(_validate(value, option) for option in schema["anyOf"])
    if "enum" in schema:
        return any(
            type(value) is type(item) and value == item for item in schema["enum"]
        )
    kind = schema["type"]
    if kind == "object":
        return isinstance(value, dict) and all(
            isinstance(k, str) and _validate(v, schema["additionalProperties"])
            for k, v in value.items()
        )
    if kind == "array":
        return isinstance(value, list) and all(
            _validate(v, schema["items"]) for v in value
        )
    if kind == "number":
        return type(value) in (int, float) and math.isfinite(value)
    return (
        type(value)
        is {"string": str, "integer": int, "boolean": bool, "null": type(None)}[kind]
    )


@dataclass(frozen=True)
class Tool:
    """Callable tool with a model-facing argument schema.

    Attributes:
        function: Async Python function called when the tool is selected.
        spec: Tool description and JSON-compatible argument schema.
        signature: Python signature used to bind tool arguments.
    """

    function: object
    spec: dict
    signature: inspect.Signature

    async def __call__(self, **kwargs):
        bound = self.signature.bind(**kwargs)
        bound.apply_defaults()
        for name, value in bound.arguments.items():
            if not _validate(value, self.spec["parameters"]["properties"][name]):
                raise ValueError(f"invalid argument for {self.spec['name']}.{name}")
        result = await self.function(**bound.arguments)
        if not isinstance(result, str):
            raise TypeError(
                "tools must return a string; custom multimodal results belong in Env.on_turn"
            )
        return result


def tool(function) -> Tool:
    """Derive a River ToolSpec from an async function's signature and docstring."""
    if not inspect.iscoroutinefunction(function):
        raise TypeError("@tool requires an async function")
    signature = inspect.signature(function)
    hints = get_type_hints(function, include_extras=True)
    properties, required = {}, []
    for name, parameter in signature.parameters.items():
        if parameter.kind not in (
            parameter.POSITIONAL_OR_KEYWORD,
            parameter.KEYWORD_ONLY,
        ):
            raise TypeError("tools require named parameters, without *args or **kwargs")
        properties[name] = _schema(hints.get(name, parameter.annotation))
        if parameter.default is parameter.empty:
            required.append(name)
        else:
            if not _validate(parameter.default, properties[name]):
                raise TypeError(f"invalid default for tool parameter {name}")
            properties[name]["default"] = parameter.default
    return Tool(
        function,
        {
            "name": function.__name__,
            "description": inspect.getdoc(function) or "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
        },
        signature,
    )


class InfrastructureError(RuntimeError):
    """An environment failure, not a model-visible task error.

    Like every tool exception, this reaches ``Env.on_error``. The default
    handler raises it rather than returning an observation, leaving the rollout
    unscored. An override can choose a different action for any exception type.
    """


class ErrorAction(Enum):
    """Terminal decisions returned by ``Env.on_error``."""

    RAISE = "raise"
    DROP = "drop"


@dataclass(frozen=True)
class Recover:
    """Explicit replacement for a failed environment operation's result.

    For a tool failure, supply a string observation; dispatch preserves the
    tool name and call ID. For ``on_turn``, supply messages, a ``TurnResult``,
    or explicitly ``None`` to finish and grade normally. For ``reward`` or
    ``on_truncated``, supply a finite reward. Bare ``None`` is not a decision.
    """

    result: str | list[Message] | TurnResult | float | None


class ErrorOperation(Enum):
    """Environment operation whose failure reached ``Env.on_error``."""

    TOOL = "tool"
    ON_TURN = "on_turn"
    REWARD = "reward"
    ON_TRUNCATED = "on_truncated"


@dataclass(frozen=True)
class ErrorContext:
    """Context for a tool, turn, or grading failure.

    ``trajectory`` is live state, not a rollback snapshot. ``cause`` is the
    truncation cause for ``on_truncated``. ``tool_call`` is a copy of the failed
    call for ``TOOL`` (``None`` if parsing failed); both are otherwise ``None``.
    ``row`` is ``None`` when
    calling ``Env.on_turn`` directly, outside a rollout engine.
    """

    operation: ErrorOperation
    trajectory: Trajectory
    row: object
    cause: str | None = None
    tool_call: dict | None = None


class _HandledToolError(Exception):
    """Carry a terminal tool decision past the turn boundary, without rehandling."""

    def __init__(self, error, context, decision):
        self.error, self.context, self.decision = error, context, decision
        super().__init__(str(error))


@dataclass
class _ToolErrorScope:
    row: object
    invoke: Callable[[Exception, ErrorContext], Awaitable[ErrorAction | Recover]]
    active: tuple[Exception, ErrorContext] | None = None


# A shared Env can serve several trajectories concurrently. Bind engine context
# to the callback task, not the environment instance or serialized trajectory.
_tool_error_scope: ContextVar[_ToolErrorScope | None] = ContextVar(
    "rl_tool_error_scope", default=None
)


def _drop_trajectory(error: Exception, context: ErrorContext):
    traj = context.trajectory
    traj.failure = {
        "operation": context.operation.value,
        "type": type(error).__name__,
        "message": str(error),
    }
    traj.reward, traj.done, traj.phase = None, True, "dropped"
    traj.active_turn_max_tokens = None


@dataclass(frozen=True)
class TurnResult:
    """``Env.on_turn`` result that also sets the next turn's token cap.

    Attributes:
        messages: New environment messages, or ``[]`` after ``traj.rewrite``.
        max_turn_tokens: Cap on generated tokens in the next turn. It replaces
            ``Budget.max_turn_tokens`` for that turn only; ``None`` keeps the
            budget's cap.
    """

    messages: list[Message]
    max_turn_tokens: int | None = None

    def __post_init__(self):
        if not isinstance(self.messages, list):
            raise TypeError(
                "TurnResult.messages must be a list; return None to end the rollout"
            )
        if self.max_turn_tokens is not None:
            _integer(self.max_turn_tokens, "max_turn_tokens", 1)


class Env:
    """Define the prompts, tools, rewards, and turn transitions for a rollout.

    Pass a shared instance to ``RolloutEngine`` for stateless tasks, or a
    factory that creates a private environment for each trajectory. Override
    ``reset`` and ``reward``; the default ``on_turn`` executes declared tools.

    Attributes:
        tools: Tools available to the model during each turn.
        recovery: How unfinished trajectories resume after a checkpoint:
            ``"drop"`` (default), ``"stateless"``, or ``"snapshot"``.
    """

    tools: tuple[Tool, ...] | list[Tool] = ()
    recovery: Literal["drop", "stateless", "snapshot"] = "drop"

    async def reset(self, row) -> list[Message]:
        """Return the initial conversation messages for a dataset row."""
        raise NotImplementedError

    async def reward(self, traj, row) -> float:
        """Return the final reward for a completed trajectory."""
        raise NotImplementedError

    async def on_turn(self, traj) -> list[Message] | TurnResult | None:
        """Return new environment messages after the latest model turn.

        The default executes tool calls and returns their results, or ``None``
        when the model has no more tool calls. Overrides should return only
        new messages, without re-rendering prior model output. Use
        ``traj.rewrite`` explicitly if you need to compact the conversation.
        Return a ``TurnResult`` to give the next turn its own token cap.
        """
        message = traj.messages[-1]
        calls = message.get("tool_calls", [])
        if not calls and not message.get("unparsed_tool_calls"):
            return None
        registry = {t.spec["name"]: t for t in self.tools}
        scope = _tool_error_scope.get()
        error_lock = asyncio.Lock()

        async def observation(error, call):
            context = ErrorContext(
                ErrorOperation.TOOL,
                traj,
                scope.row if scope is not None else None,
                tool_call=copy.deepcopy(call),
            )
            # Serialize policy callbacks within this dispatch. Sibling tools may
            # still be running; do not cancel successful work just to observe an
            # error, and never rerun a tool after recovery.
            async with error_lock:
                if scope is not None:
                    scope.active = error, context
                try:
                    decision = await (
                        self.on_error(error, context)
                        if scope is None
                        else scope.invoke(error, context)
                    )
                    if decision is ErrorAction.RAISE or decision is ErrorAction.DROP:
                        raise _HandledToolError(error, context, decision)
                    if not isinstance(decision, Recover) or not isinstance(
                        decision.result, str
                    ):
                        raise TypeError(
                            "tool on_error must return ErrorAction or Recover(str)"
                        ) from error
                    return decision.result
                except _HandledToolError:
                    raise
                except Exception as failure:
                    if failure is not error:
                        failure.__context__ = error
                    raise _HandledToolError(
                        failure, context, ErrorAction.RAISE
                    ) from None
                finally:
                    if scope is not None:
                        scope.active = None

        async def execute(call):
            started = time.monotonic()
            if call is None:
                content = await observation(
                    ValueError("Tool call could not be parsed"), None
                )
                traj.metrics["tool_errors"] = traj.metrics.get("tool_errors", 0) + 1
                return {"role": "tool", "content": content}
            name = call["function"]["name"]
            traj.metrics["tool_calls"] = traj.metrics.get("tool_calls", 0) + 1
            key = f"tool_calls/{name}"
            traj.metrics[key] = traj.metrics.get(key, 0) + 1
            try:
                arguments = call["function"].get("arguments", {})
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)
                if not isinstance(arguments, dict):
                    raise ValueError("tool arguments must be a JSON object")  # noqa: TRY004 - malformed configuration/tool value
                if name not in registry:
                    raise ValueError(f"tool {name!r} is not available")
                content = await registry[name](**arguments)
            except Exception as error:
                content = await observation(error, call)
                traj.metrics["tool_errors"] = traj.metrics.get("tool_errors", 0) + 1
            traj.metrics["tool_seconds"] = (
                traj.metrics.get("tool_seconds", 0) + time.monotonic() - started
            )
            return {
                "role": "tool",
                "content": content,
                "name": name,
                "tool_call_id": call.get("id") or "",
            }

        tasks = [asyncio.create_task(execute(call)) for call in calls or [None]]
        try:
            return list(await asyncio.gather(*tasks))
        except _HandledToolError as handled:
            if scope is not None:
                raise
            if handled.decision is ErrorAction.DROP:
                _drop_trajectory(handled.error, handled.context)
                return None
            failure = handled.error
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
        # Outside the except block so the private carrier does not become the
        # public exception's context when on_turn is called without an engine.
        raise failure

    async def on_error(
        self, error: Exception, context: ErrorContext
    ) -> ErrorAction | Recover:
        """Choose which failures become observations, propagate, or end unscored.

        For ``TOOL``, the default returns ``Recover(str)`` with a tool-error
        observation, except for ``InfrastructureError`` which it raises. Other
        operations default to ``ErrorAction.RAISE``. Override either policy;
        dispatch never classifies exceptions before this hook sees them.

        Return ``ErrorAction.DROP`` to exclude the rollout from training, or
        ``Recover(result)`` to supply a replacement result for the operation.
        No operation is automatically retried and side effects are not rolled
        back. Continuing requires a coherent environment/trajectory.

        Cancellation, internal stop signals, SDK result-validation errors,
        and errors from this handler bypass the hook. Factory, reset, restore,
        snapshot, and close failures also propagate without invoking it.
        """
        if context.operation is ErrorOperation.TOOL and not isinstance(
            error, InfrastructureError
        ):
            return Recover(f"Tool error ({type(error).__name__}): {error}")
        return ErrorAction.RAISE

    async def on_truncated(self, traj, row, cause: str) -> float:
        """Override for task-specific partial credit. Default is explicit zero."""
        return 0.0

    async def snapshot(self, traj):
        """Capture private environment state for ``recovery="snapshot"``."""
        raise NotImplementedError(
            "snapshot recovery requires Env.snapshot and Env.restore"
        )

    async def restore(self, traj, state):
        """Restore private state captured by ``snapshot`` after a restart."""
        raise NotImplementedError(
            "snapshot recovery requires Env.snapshot and Env.restore"
        )

    async def close(self):
        """Release resources owned by a per-trajectory environment factory."""


def elide_middle(text, tokenizer, limit):
    ids = tokenizer.encode(text, add_special_tokens=False)
    if len(ids) <= limit:
        return text, False
    # The marker itself counts against the limit. Tiny caps omit it.
    marker = tokenizer.encode("\n[tool output elided]\n", add_special_tokens=False)
    if len(marker) >= limit:
        marker = []
    keep = limit - len(marker)
    head = (keep + 1) // 2
    tail = keep - head
    result = tokenizer.decode(ids[:head] + marker + (ids[-tail:] if tail else []))
    # Decoding environment text is allowed; ensure retokenization still fits.
    while len(tokenizer.encode(result, add_special_tokens=False)) > limit and result:
        result = result[:-1]
    return result, True
