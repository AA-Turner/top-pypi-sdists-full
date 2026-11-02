"""Tool registry implementation (FR-001).

``ConcreteToolRegistry`` provides registration, lookup, category
filtering, and an invoke facade for registered tools.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from .definition import ToolDefinition
from .result import ToolResult

# Type alias for tool functions
ToolFunction = Callable[..., Any]


class ConcreteToolRegistry:
    """Registry of available tools with metadata and invocation support.

    Enforces unique tool names, supports category filtering, and provides
    an ``invoke()`` facade that satisfies the ``ToolRegistry`` Protocol.
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}
        self._functions: dict[str, ToolFunction] = {}

    def register(self, definition: ToolDefinition, *, fn: ToolFunction) -> None:
        """Register a tool with its definition and implementation function.

        Raises:
            TypeError: If ``fn`` is not callable.
            ValueError: If a tool with the same name is already registered.
        """
        if not callable(fn):
            raise TypeError(f"Tool implementation for {definition.name!r} must be callable, got {type(fn).__name__!r}")
        if definition.name in self._tools:
            raise ValueError(f"Tool already registered: {definition.name!r}")
        self._tools[definition.name] = definition
        self._functions[definition.name] = fn

    def get(self, name: str) -> ToolDefinition | None:
        """Look up a tool definition by name, or return None."""
        return self._tools.get(name)

    def get_function(self, name: str) -> ToolFunction | None:
        """Look up a tool function by name, or return None."""
        return self._functions.get(name)

    def list_all(self) -> dict[str, ToolDefinition]:
        """Return a flat mapping of all registered tools."""
        return dict(self._tools)

    def get_categories(self) -> list[str]:
        """Return sorted list of all registered category names."""
        return sorted({d.category for d in self._tools.values()})

    def get_tools(self, *, category: str) -> list[ToolDefinition]:
        """Return tools filtered by category."""
        return [d for d in self._tools.values() if d.category == category]

    def list_by_category(self) -> dict[str, list[ToolDefinition]]:
        """Return tools grouped by category."""
        result: dict[str, list[ToolDefinition]] = {}
        for d in self._tools.values():
            result.setdefault(d.category, []).append(d)
        return result

    def invoke(self, tool_name: str, **kwargs: Any) -> Any:
        """Invoke a registered tool by name (Protocol-compatible facade).

        Returns a JSON-serializable dict representing a ``ToolResult``
        envelope.  Returns a ``not_found`` error envelope when the tool is
        not registered (consistent with ``ToolExecutor.invoke()``).
        """
        definition = self._tools.get(tool_name)
        if definition is None:
            result = ToolResult(
                success=False,
                error_type="not_found",
                error_message=f"Tool not registered: {tool_name!r}",
            )
            return json.loads(result.to_json())

        fn = self._functions[tool_name]
        try:
            output = fn(**kwargs)
            # Detect domain-level failures encoded as {"success": False, ...}.
            # Mirrors the same detection in ToolExecutor._execute_with_timeout()
            # so callers that bypass ToolExecutor get consistent failure signals.
            # `is False` is intentional: only an explicit False boolean signals
            # a domain failure; falsy values like None or 0 are not treated as
            # failures so valid outputs that happen to be falsy are not suppressed.
            if isinstance(output, dict) and output.get("success") is False:
                error_msg = str(
                    output.get("error")
                    or output.get("error_message")
                    or output.get("message")
                    or output.get("stderr")
                    or "tool reported failure"
                )
                result = ToolResult(
                    success=False,
                    output=output,
                    error_type="execution_error",
                    error_message=error_msg,
                )
            else:
                result = ToolResult(success=True, output=output)
        except Exception as exc:  # noqa: BLE001
            result = ToolResult(
                success=False,
                error_type="execution_error",
                error_message=str(exc),
            )

        return json.loads(result.to_json())
