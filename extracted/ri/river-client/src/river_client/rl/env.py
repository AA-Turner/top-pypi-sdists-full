"""Async environments and signature-derived tools. Execution stays with the user."""

from __future__ import annotations

import asyncio
import inspect
import json
import math
import time
import types
from dataclasses import dataclass
from typing import Annotated, Literal, Union, get_args, get_origin, get_type_hints

from river_client.renderers import Message


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
    """A tool or environment failure that should stop the rollout.

    Raise this for unavailable external services instead of returning a tool
    error to the model. ``TimeoutError`` and ``ConnectionError`` also stop the
    rollout rather than becoming task rewards.
    """


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

    async def on_turn(self, traj) -> list[Message] | None:
        """Return new environment messages after the latest model turn.

        The default executes tool calls and returns their results, or ``None``
        when the model has no more tool calls. Overrides should return only
        new messages, without re-rendering prior model output. Use
        ``traj.rewrite`` explicitly if you need to compact the conversation.
        """
        message = traj.messages[-1]
        calls = message.get("tool_calls", [])
        if not calls:
            if message.get("unparsed_tool_calls"):
                return [
                    {
                        "role": "tool",
                        "content": "Tool call could not be parsed. Please retry with valid arguments.",
                    }
                ]
            return None
        registry = {t.spec["name"]: t for t in self.tools}

        async def execute(call):
            started = time.monotonic()
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
            except (InfrastructureError, TimeoutError, ConnectionError):
                raise
            except Exception as exc:
                traj.metrics["tool_errors"] = traj.metrics.get("tool_errors", 0) + 1
                content = f"Tool error ({type(exc).__name__}): {exc}"
            traj.metrics["tool_seconds"] = (
                traj.metrics.get("tool_seconds", 0) + time.monotonic() - started
            )
            return {
                "role": "tool",
                "content": content,
                "name": name,
                "tool_call_id": call.get("id") or "",
            }

        tasks = [asyncio.create_task(execute(call)) for call in calls]
        try:
            return list(await asyncio.gather(*tasks))
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

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
