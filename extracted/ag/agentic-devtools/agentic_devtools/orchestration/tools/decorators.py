"""Decorator and auto-discovery for tool registration (FR-010).

The ``@tool_definition`` decorator annotates a function with tool
metadata.  ``auto_discover()`` scans a module for decorated functions
and registers them in a ``ConcreteToolRegistry``.
"""

from __future__ import annotations

import importlib
import inspect
from collections.abc import Callable
from typing import Any

from .definition import ToolDefinition
from .registry import ConcreteToolRegistry

_TOOL_DEFINITION_ATTR = "_tool_definition"


def tool_definition(
    *,
    name: str,
    description: str,
    category: str,
    input_schema: dict[str, Any],
    output_schema: dict[str, Any] | None = None,
    mutating: bool = False,
    timeout_seconds: float = 30.0,
    thread_safe: bool = True,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator that attaches a ``ToolDefinition`` to a function.

    Usage::

        @tool_definition(
            name="git_stage_all",
            description="Stage all changes",
            category="git",
            input_schema={"type": "object", "properties": {}},
            mutating=True,
        )
        def stage_all() -> dict:
            ...
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        defn = ToolDefinition(
            name=name,
            description=description,
            category=category,
            input_schema=input_schema,
            output_schema=(output_schema if output_schema is not None else {"type": "object"}),
            mutating=mutating,
            timeout_seconds=timeout_seconds,
            thread_safe=thread_safe,
        )
        setattr(fn, _TOOL_DEFINITION_ATTR, defn)
        return fn

    return decorator


def auto_discover(module_name: str, registry: ConcreteToolRegistry) -> int:
    """Scan *module_name* for functions with ``@tool_definition`` and register them.

    Returns the count of newly registered tools.
    """
    module = importlib.import_module(module_name)
    count = 0

    for _attr_name, obj in inspect.getmembers(module, inspect.isfunction):
        defn = getattr(obj, _TOOL_DEFINITION_ATTR, None)
        if defn is not None and isinstance(defn, ToolDefinition):
            if registry.get(defn.name) is None:
                registry.register(defn, fn=obj)
                count += 1

    return count
