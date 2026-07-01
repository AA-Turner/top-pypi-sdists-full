"""
cvc.core.tools — minimal tool registry for CVC v4.0.

CVC v4.0 ships with an **empty** built-in tool registry. The tool system
exists so skills (Phase 2) and bundled plugins can register their own
tools. Native CVC tools (``read_file``, ``patch``, ``search_files``,
``terminal``, ``process``, …) are exposed as Python functions and
dispatched directly by ``cvc/agent/executor.py`` — they do NOT go
through this registry.

This module is a CVC-native port of the API surface used by the 4
caller files in Phase 1B. It is intentionally minimal — no MCP, no
alias, no dynamic schema overrides, no TTL-cached ``check_fn``. Those
concerns are deferred until a Phase that actually needs them.

Public surface (must match what caller files import):

    discover_builtin_tools()         -> list[str]
    ToolRegistry(...)
        .register(name, toolset, schema, handler, check_fn=None, ...)
        .get_all_tool_names()         -> list[str]
        .get_definitions(names, quiet=False) -> list[dict]
        .dispatch(name, args, **kw)   -> str
        .get_toolset_for_tool(name)   -> str | None
    tool_error(message, **extra)     -> str
    tool_result(data=None, **kwargs) -> str
    @register_tool(name=..., toolset=..., schema=..., ...)

The class is a singleton — every ``cvc.core.tools.registry`` reference
points to the same instance, matching the vendor's contract.
"""

from __future__ import annotations

import json
import logging
import threading
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Discover
# ---------------------------------------------------------------------------

def discover_builtin_tools() -> List[str]:
    """Discover and register CVC's built-in tools.

    Phase 1B has zero built-in tools. The function exists so callers
    can invoke it the same way they invoke the vendor's equivalent;
    skills and external plugins (Phase 2+) will populate the registry
    via ``@register_tool`` after this returns ``[]``.
    """
    # Intentionally empty — see module docstring.
    return []


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

class ToolEntry:
    """Metadata for a single registered tool."""

    __slots__ = (
        "name", "toolset", "schema", "handler", "check_fn",
        "requires_env", "is_async", "description",
    )

    def __init__(
        self,
        name: str,
        toolset: str,
        schema: Dict[str, Any],
        handler: Callable[..., Any],
        check_fn: Optional[Callable[[], bool]] = None,
        requires_env: Optional[List[str]] = None,
        is_async: bool = False,
        description: str = "",
    ) -> None:
        self.name = name
        self.toolset = toolset
        self.schema = schema
        self.handler = handler
        self.check_fn = check_fn
        self.requires_env = requires_env or []
        self.is_async = is_async
        self.description = description or str(schema.get("description", ""))


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class ToolRegistry:
    """Singleton registry that collects tool schemas + handlers.

    The constructor is cheap; the *module-level* ``registry`` instance
    is the actual singleton callers use. Skills and plugins call
    ``registry.register(...)`` or ``@register_tool(...)`` at import time
    to add themselves.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, ToolEntry] = {}
        self._lock = threading.RLock()

    # -- Registration --------------------------------------------------------

    def register(
        self,
        name: str,
        toolset: str,
        schema: Dict[str, Any],
        handler: Callable[..., Any],
        check_fn: Optional[Callable[[], bool]] = None,
        requires_env: Optional[List[str]] = None,
        is_async: bool = False,
        description: str = "",
        **kwargs: Any,  # ignore vendor extras (emoji, max_result_size_chars, …)
    ) -> None:
        """Register a tool. Re-registering with the same toolset is a no-op;
        registering under a different toolset is rejected (matches vendor
        policy of preventing silent shadowing).
        """
        with self._lock:
            existing = self._tools.get(name)
            if existing and existing.toolset != toolset:
                logger.error(
                    "Tool registration REJECTED: '%s' (toolset '%s') would "
                    "shadow existing tool from toolset '%s'",
                    name, toolset, existing.toolset,
                )
                return
            self._tools[name] = ToolEntry(
                name=name,
                toolset=toolset,
                schema=schema,
                handler=handler,
                check_fn=check_fn,
                requires_env=requires_env or [],
                is_async=is_async,
                description=description or str(schema.get("description", "")),
            )

    def deregister(self, name: str) -> None:
        """Remove a tool from the registry."""
        with self._lock:
            self._tools.pop(name, None)

    # -- Schema retrieval ----------------------------------------------------

    def get_definitions(
        self,
        tool_names: Set[str] | List[str],
        quiet: bool = False,
    ) -> List[Dict[str, Any]]:
        """Return OpenAI-format tool schemas for the requested tool names.

        Tools whose ``check_fn()`` returns False (or raises) are skipped.
        """
        result: List[Dict[str, Any]] = []
        names = set(tool_names)
        with self._lock:
            entries = {n: self._tools[n] for n in names if n in self._tools}
        for name in sorted(entries):
            entry = entries[name]
            if entry.check_fn is not None:
                try:
                    if not bool(entry.check_fn()):
                        if not quiet:
                            logger.debug("Tool %s unavailable (check failed)", name)
                        continue
                except Exception:
                    if not quiet:
                        logger.debug("Tool %s check raised; skipped", name)
                    continue
            schema = {**entry.schema, "name": entry.name}
            result.append({"type": "function", "function": schema})
        return result

    # -- Dispatch ------------------------------------------------------------

    def dispatch(self, name: str, args: Dict[str, Any], **kwargs: Any) -> str:
        """Execute a tool handler by name. Returns a JSON string.

        Unknown tools and exceptions both come back as
        ``{"error": "..."}`` so the agent's tool loop can keep going.
        """
        with self._lock:
            entry = self._tools.get(name)
        if entry is None:
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            return entry.handler(args or {}, **kwargs)
        except Exception as e:
            logger.exception("Tool %s dispatch error: %s", name, e)
            return json.dumps({
                "error": f"Tool execution failed: {type(e).__name__}: {e}",
            })

    # -- Query helpers -------------------------------------------------------

    def get_all_tool_names(self) -> List[str]:
        """Return sorted list of all registered tool names."""
        with self._lock:
            return sorted(self._tools.keys())

    def get_toolset_for_tool(self, name: str) -> Optional[str]:
        """Return the toolset a tool belongs to, or None."""
        with self._lock:
            entry = self._tools.get(name)
        return entry.toolset if entry else None

    def get_entry(self, name: str) -> Optional[ToolEntry]:
        """Return the raw ToolEntry, or None."""
        with self._lock:
            return self._tools.get(name)

    def is_toolset_available(self, toolset: str) -> bool:
        """A toolset is available iff any of its tools' check_fns return True.

        Returns True when no tool in the toolset has a check_fn.
        """
        with self._lock:
            entries = [e for e in self._tools.values() if e.toolset == toolset]
        if not entries:
            return True
        for e in entries:
            if e.check_fn is None:
                return True
            try:
                if bool(e.check_fn()):
                    return True
            except Exception:
                continue
        return False


# ---------------------------------------------------------------------------
# Module-level singleton — matches the vendor's ``registry`` symbol.
# ---------------------------------------------------------------------------

registry = ToolRegistry()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def tool_error(message: Any, **extra: Any) -> str:
    """Return a JSON error string for tool handlers.

    >>> tool_error("file not found")
    '{"error": "file not found"}'
    """
    result = {"error": str(message)}
    if extra:
        result.update(extra)
    return json.dumps(result, ensure_ascii=False)


def tool_result(data: Any = None, **kwargs: Any) -> str:
    """Return a JSON result string for tool handlers.

    Accepts a dict positional arg *or* keyword arguments (not both):

    >>> tool_result(success=True, count=42)
    '{"success": true, "count": 42}'
    """
    if data is not None:
        return json.dumps(data, ensure_ascii=False)
    return json.dumps(kwargs, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Decorator
# ---------------------------------------------------------------------------

def register_tool(
    name: str,
    toolset: str,
    schema: Dict[str, Any],
    check_fn: Optional[Callable[[], bool]] = None,
    requires_env: Optional[List[str]] = None,
    is_async: bool = False,
    description: str = "",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Class/function decorator that registers a callable as a tool.

    Usage::

        @register_tool(
            name="my_tool",
            toolset="custom",
            schema={
                "name": "my_tool",
                "description": "…",
                "parameters": {"type": "object", "properties": {}},
            },
        )
        def my_tool(args: dict) -> str:
            return tool_result(ok=True)
    """
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        registry.register(
            name=name,
            toolset=toolset,
            schema=schema,
            handler=fn,
            check_fn=check_fn,
            requires_env=requires_env,
            is_async=is_async,
            description=description,
        )
        return fn
    return deco


__all__ = [
    "ToolEntry",
    "ToolRegistry",
    "discover_builtin_tools",
    "register_tool",
    "registry",
    "tool_error",
    "tool_result",
]
