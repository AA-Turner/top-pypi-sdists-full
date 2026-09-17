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
    """An operational failure; never turn it into a task reward or tool result.

    Tool providers should wrap backend-specific transport/unavailability errors
    in this exception. TimeoutError and ConnectionError also propagate.
    """


class Env:
    """Use an instance for stateless environments, a factory for private sandboxes.

    ``on_turn`` returns only NEW environment-authored messages, or None to finish.
    It may explicitly call ``traj.rewrite`` to compact history. Never re-render a
    generated assistant message. Recovery defaults to dropping unfinished work;
    opt into ``stateless`` or ``snapshot`` only when the environment supports it.
    """

    tools: tuple[Tool, ...] | list[Tool] = ()
    recovery: Literal["drop", "stateless", "snapshot"] = "drop"

    async def reset(self, row) -> list[Message]:
        raise NotImplementedError

    async def reward(self, traj, row) -> float:
        raise NotImplementedError

    async def on_turn(self, traj) -> list[Message] | None:
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
        raise NotImplementedError(
            "snapshot recovery requires Env.snapshot and Env.restore"
        )

    async def restore(self, traj, state):
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
