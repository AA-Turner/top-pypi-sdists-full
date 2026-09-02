"""External tool handler registry for ai.

When the ai package is consumed as a package by an external application (e.g. Matrx Local),
some tools in the database have implementations that live in the host application, not
in this codebase. These tools carry ``source_kind != "ai"`` in the database.

The ``ExternalHandlerRegistry`` allows host applications to register async callables
that the executor will dispatch to when the AI model calls one of those tools. The result
flows back through the same guardrails, streaming, persistence, and model-feedback
pipeline as any native tool -- the model cannot tell the difference.

----

There are three integration patterns, from simplest to most flexible:

Pattern 1 — ``ExternalToolAdapter`` (recommended for most apps)
----------------------------------------------------------------
Subclass ``ExternalToolAdapter``, decorate methods with ``@external_tool``, and call
``register()`` once at startup. The adapter auto-dispatches every decorated method::

    from matrx_ai.tools import ExternalToolAdapter, external_tool, ToolContext

    class MyTools(ExternalToolAdapter):
        source_kind = "matrx_local"

        @external_tool("screenshot")
        async def take_screenshot(self, args: dict, ctx: ToolContext) -> dict:
            return {"image": await capture_screen(args.get("region"))}

        @external_tool("open_file")
        async def open_file(self, args: dict, ctx: ToolContext) -> dict:
            return {"content": await read_file(args["path"])}

    MyTools().register()   # call once at app startup


Pattern 2 — ``register_external_tool_handler`` (per-tool, plain functions)
---------------------------------------------------------------------------
Register individual async functions, one per tool::

    from matrx_ai.tools import register_external_tool_handler, ToolContext, ToolResult

    async def handle_screenshot(args: dict, ctx: ToolContext) -> ToolResult:
        image_data = await take_local_screenshot(args.get("region"))
        return ToolResult(success=True, output=image_data,
                          tool_name=ctx.tool_name, call_id=ctx.call_id)

    register_external_tool_handler("screenshot", handle_screenshot)


Pattern 3 — ``register_external_app_handler`` (single dispatcher for all tools)
---------------------------------------------------------------------------------
Register one async function that receives every tool call for a source_kind::

    from matrx_ai.tools import register_external_app_handler, ToolContext, ToolResult

    async def matrx_local_dispatcher(args: dict, ctx: ToolContext) -> ToolResult:
        result_data = await local_tool_router(ctx.tool_name, args)
        return ToolResult(success=True, output=result_data,
                          tool_name=ctx.tool_name, call_id=ctx.call_id)

    register_external_app_handler("matrx_local", matrx_local_dispatcher)


Resolution order (per execution)
---------------------------------
1. Exact tool-name match  →  Pattern 2 / adapter per-tool handlers
2. App-level fallback     →  Pattern 3 / adapter app-level dispatcher
3. No handler found       →  structured error returned to the model (not a crash)

----

Handler return values
----------------------
Handlers may return any of the following — all are normalised automatically:

- ``ToolResult``          — passed through as-is (preferred)
- ``dict``                — wrapped as ``ToolResult(success=True, output=...)``
                            (if dict has ``"status": "error"`` it becomes a failure)
- ``str`` / any other     — wrapped as ``ToolResult(success=True, output=value)``

----

Register handlers *before* the first AI request that could trigger the tool.
The registry is a process-level singleton; registrations persist for the lifetime
of the process.
"""

from __future__ import annotations

import functools
import traceback
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from matrx_utils import vcprint

from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

ExternalToolHandler = Callable[[dict[str, Any], ToolContext], Awaitable[ToolResult]]

_F = TypeVar("_F", bound=Callable[..., Awaitable[Any]])


class ExternalHandlerRegistry:
    """Process-level singleton that maps tool names / source-app names to async callables.

    Thread-safety: Registration is expected to happen at startup (single-threaded);
    reads during request handling are concurrent but safe because dicts in CPython
    have GIL-protected reads.  For truly concurrent registration, callers should
    synchronise externally.
    """

    _instance: ExternalHandlerRegistry | None = None

    def __init__(self) -> None:
        # tool_name → handler (highest priority)
        self._tool_handlers: dict[str, ExternalToolHandler] = {}
        # source_kind → catch-all handler for every tool from that app
        self._app_handlers: dict[str, ExternalToolHandler] = {}

    @classmethod
    def get_instance(cls) -> ExternalHandlerRegistry:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, tool_name: str, handler: ExternalToolHandler) -> None:
        """Register a handler for one specific tool by name.

        Takes priority over any app-level handler for the same tool.
        Calling this again with the same ``tool_name`` replaces the previous handler.
        """
        if not callable(handler):
            raise TypeError(f"Handler for tool '{tool_name}' must be callable, got {type(handler)}")
        self._tool_handlers[tool_name] = handler
        vcprint(
            f"[ExternalHandlerRegistry] Registered handler for tool: {tool_name}",
            color="cyan",
        )

    def register_app_handler(self, source_kind: str, handler: ExternalToolHandler) -> None:
        """Register a catch-all handler for every tool owned by ``source_kind``.

        This is the simplest integration point: one async function receives every
        tool call from the given app, with ``ctx.tool_name`` identifying which
        specific tool was invoked.

        Calling this again with the same ``source_kind`` replaces the previous handler.
        """
        if not callable(handler):
            raise TypeError(
                f"App handler for source_kind '{source_kind}' must be callable, got {type(handler)}"
            )
        self._app_handlers[source_kind] = handler
        vcprint(
            f"[ExternalHandlerRegistry] Registered app-level handler for source_kind: {source_kind}",
            color="cyan",
        )

    def unregister(self, tool_name: str) -> bool:
        """Remove the per-tool handler for ``tool_name``. Returns True if one existed."""
        existed = tool_name in self._tool_handlers
        self._tool_handlers.pop(tool_name, None)
        return existed

    def unregister_app_handler(self, source_kind: str) -> bool:
        """Remove the app-level handler for ``source_kind``. Returns True if one existed."""
        existed = source_kind in self._app_handlers
        self._app_handlers.pop(source_kind, None)
        return existed

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def get_handler(
        self, tool_name: str, source_kind: str | None
    ) -> ExternalToolHandler | None:
        """Resolve the best handler for a tool call.

        Resolution order:
        1. Exact tool-name match (``register`` / ``register_external_tool_handler``)
        2. App-level fallback (``register_app_handler`` / ``register_external_app_handler``)
        3. ``None`` — caller should surface a structured error to the model
        """
        if tool_name in self._tool_handlers:
            return self._tool_handlers[tool_name]
        if source_kind and source_kind in self._app_handlers:
            return self._app_handlers[source_kind]
        return None

    def has_handler(self, tool_name: str, source_kind: str | None) -> bool:
        """Return True if any handler would be found for this tool."""
        return self.get_handler(tool_name, source_kind) is not None

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def registered_tools(self) -> list[str]:
        return list(self._tool_handlers.keys())

    @property
    def registered_apps(self) -> list[str]:
        return list(self._app_handlers.keys())

    def __repr__(self) -> str:
        return (
            f"ExternalHandlerRegistry("
            f"tools={self.registered_tools}, "
            f"apps={self.registered_apps})"
        )


# ------------------------------------------------------------------
# Decorator for use with ExternalToolAdapter
# ------------------------------------------------------------------

def external_tool(tool_name: str) -> Callable[[_F], _F]:
    """Decorator that marks an ``ExternalToolAdapter`` method as the handler for a tool.

    Args:
        tool_name: The exact tool name as stored in the ``tools`` database table.

    Usage::

        class MyTools(ExternalToolAdapter):
            source_kind = "matrx_local"

            @external_tool("screenshot")
            async def take_screenshot(self, args: dict, ctx: ToolContext) -> dict:
                return {"image": await capture_screen(args.get("region"))}

    The method may return any value — ``ToolResult``, ``dict``, ``str``, or anything
    else.  The adapter normalises the return value before it reaches the model.

    The ``self`` argument receives the adapter instance, giving methods access to any
    shared state or configuration stored on the class.
    """
    def decorator(func: _F) -> _F:
        func._external_tool_name = tool_name  # type: ignore[attr-defined]

        @functools.wraps(func)
        async def wrapper(self: ExternalToolAdapter, args: dict[str, Any], ctx: ToolContext) -> Any:
            return await func(self, args, ctx)

        wrapper._external_tool_name = tool_name  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorator


# ------------------------------------------------------------------
# High-level adapter class
# ------------------------------------------------------------------

class ExternalToolAdapter:
    """High-level base class for integrating host-application tools with the ai package.

    Subclass this, set ``source_kind``, decorate methods with ``@external_tool``,
    then call ``register()`` once at application startup.  The adapter auto-discovers
    all decorated methods and registers them — no manual per-tool registration needed.

    The adapter registers in two ways simultaneously:
    - Each ``@external_tool``-decorated method is registered as a per-tool handler
      (highest priority, exact name match).
    - The adapter itself is registered as the app-level fallback dispatcher
      (catches any tool from ``source_kind`` that has no specific handler).

    This means you can mix decorated methods with undecorated ones for custom routing
    by overriding ``dispatch()``.

    Minimal example::

        from matrx_ai.tools import ExternalToolAdapter, external_tool, ToolContext

        class MatrxLocalTools(ExternalToolAdapter):
            source_kind = "matrx_local"

            @external_tool("screenshot")
            async def take_screenshot(self, args: dict, ctx: ToolContext) -> dict:
                image = await capture_screen(args.get("region"))
                return {"image_base64": image}

            @external_tool("open_file")
            async def open_file(self, args: dict, ctx: ToolContext) -> dict:
                content = await read_file(args["path"])
                return {"content": content}

        MatrxLocalTools().register()

    Advanced — custom dispatch for unregistered tools::

        class MatrxLocalTools(ExternalToolAdapter):
            source_kind = "matrx_local"

            @external_tool("screenshot")
            async def take_screenshot(self, args: dict, ctx: ToolContext) -> dict:
                ...

            async def dispatch(self, args: dict, ctx: ToolContext) -> ToolResult:
                # Called for any tool from source_kind NOT covered by @external_tool.
                # ctx.tool_name tells you which tool was invoked.
                result = await self._route_to_local_impl(ctx.tool_name, args)
                return ToolResult(success=True, output=result,
                                  tool_name=ctx.tool_name, call_id=ctx.call_id)
    """

    #: Must be set on the subclass to the value of the ``source_kind`` DB column.
    source_kind: str = ""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Collect all @external_tool-decorated methods at class definition time.
        cls._tool_methods: dict[str, str] = {}
        for attr_name in dir(cls):
            method = getattr(cls, attr_name, None)
            tool_name = getattr(method, "_external_tool_name", None)
            if tool_name is not None:
                cls._tool_methods[tool_name] = attr_name

    def register(self, registry: ExternalHandlerRegistry | None = None) -> None:
        """Register all decorated methods, the app-level dispatcher, and the
        conversation-cleanup callback with the ``ToolLifecycleManager``.

        Call once at application startup.

        Args:
            registry: Override the registry instance (defaults to the global singleton).
                      Useful in tests.
        """
        if not self.source_kind:
            raise ValueError(
                f"{type(self).__name__}.source_kind must be set to the database source_kind value "
                "(e.g. 'matrx_local') before calling register()."
            )

        reg = registry or ExternalHandlerRegistry.get_instance()

        # Register each decorated method as a per-tool handler.
        for tool_name, method_name in self.__class__._tool_methods.items():
            method = getattr(self, method_name)
            reg.register(tool_name, self._make_handler(method, tool_name))

        # Register the adapter itself as the app-level fallback.
        reg.register_app_handler(self.source_kind, self._app_dispatcher)

        # Wire on_conversation_end into ToolLifecycleManager so conversation-scoped
        # resources (session pools, caches, etc.) are cleaned up automatically.
        try:
            from matrx_ai.tools.lifecycle import ToolLifecycleManager

            lifecycle = ToolLifecycleManager.get_instance()
            lifecycle.register_external_adapter_cleanup(self._on_conversation_end)
        except Exception:
            pass  # lifecycle is optional — adapter still functions without it

        vcprint(
            {
                "source_kind": self.source_kind,
                "registered_tools": list(self.__class__._tool_methods.keys()),
            },
            f"[ExternalToolAdapter] {type(self).__name__} registered",
            color="cyan",
        )

    def _make_handler(
        self, method: Callable[..., Awaitable[Any]], tool_name: str
    ) -> ExternalToolHandler:
        """Wrap a decorated method as a normalised ``ExternalToolHandler``."""
        async def handler(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
            import time

            started_at = time.time()
            try:
                raw = await method(args, ctx)
            except Exception as exc:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="external_handler_error",
                        message=str(exc),
                        traceback=traceback.format_exc(),
                        is_retryable=False,
                        suggested_action="The tool implementation raised an unexpected exception.",
                    ),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name=tool_name,
                    call_id=ctx.call_id,
                )
            return await _normalise_result(raw, tool_name, ctx.call_id, started_at)

        return handler

    async def _app_dispatcher(self, args: dict[str, Any], ctx: ToolContext) -> ToolResult:
        """App-level fallback: routes to ``dispatch()`` for tools not covered by ``@external_tool``."""
        return await self.dispatch(args, ctx)

    async def _on_conversation_end(self, conversation_id: str) -> None:
        """Called by ToolLifecycleManager when a conversation ends or times out.

        Routes to ``on_conversation_end()`` which subclasses should override to
        clean up conversation-scoped resources (session pools, open connections, etc.).
        """
        try:
            await self.on_conversation_end(conversation_id)
        except Exception as exc:
            vcprint(
                f"[ExternalToolAdapter] on_conversation_end raised for conversation "
                f"'{conversation_id}': {exc}",
                color="red",
            )

    async def on_conversation_end(self, conversation_id: str) -> None:
        """Override to clean up conversation-scoped resources when a conversation ends.

        This is called automatically by ``ToolLifecycleManager`` when a
        conversation ends (either explicitly via ``cleanup_conversation()`` or via the
        idle-timeout sweep after 30 minutes of inactivity).

        Use this to release any state keyed by ``conversation_id`` — session pools,
        open browser instances, background processes, file handles, etc.

        Example::

            class MatrxLocalTools(ExternalToolAdapter):
                source_kind = "matrx_local"

                def __init__(self):
                    self._sessions: dict[str, ToolSession] = {}

                async def on_conversation_end(self, conversation_id: str) -> None:
                    session = self._sessions.pop(conversation_id, None)
                    if session:
                        await session.cleanup()
        """

    async def dispatch(self, args: dict[str, Any], ctx: ToolContext) -> ToolResult:
        """Override to handle tools from ``source_kind`` that have no ``@external_tool`` handler.

        The default implementation returns an informative error so the model knows the
        tool is not implemented in this adapter.  Override for custom routing logic.
        """
        import time

        decorated = list(self.__class__._tool_methods.keys())
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="not_implemented",
                message=(
                    f"Tool '{ctx.tool_name}' (source_kind='{self.source_kind}') has no handler "
                    f"in {type(self).__name__}. "
                    f"Decorated tools: {decorated or 'none'}. "
                    f"Override dispatch() or add @external_tool('{ctx.tool_name}') to a method."
                ),
                is_retryable=False,
                suggested_action=(
                    "This tool is not available in the current environment. "
                    "Inform the user and suggest an alternative approach."
                ),
            ),
            started_at=time.time(),
            completed_at=time.time(),
            tool_name=ctx.tool_name,
            call_id=ctx.call_id,
        )


# ------------------------------------------------------------------
# Internal normalisation helper (shared by adapter + invoke_external_handler)
# ------------------------------------------------------------------

async def _normalise_result(
    raw: Any,
    tool_name: str,
    call_id: str,
    started_at: float,
) -> ToolResult:
    """Convert any handler return value to a ``ToolResult``.

    Image-shaped outputs (a dict with ``media_type`` starting with
    ``image/`` and a ``*_base64`` blob) are funneled through
    ``image_outputs.normalize_tool_output_async`` so the master image
    lands in cloud storage and the rewritten output carries a
    ``MediaRef``-shaped dict instead of raw bytes.

    Scope — this is the EXTERNAL-HANDLER entry to that funnel, not the
    system's only cloud-write path. It covers tool results that arrive as a
    handler return value (sandbox, MCP, desktop). The funnel's other callers
    reach it directly: ``aidream/services/ai_execution/tool_results.py`` for
    client-delegated results posted to ``/tool_results``, and server-side
    tools like ``aidream/services/cloud_browser/tools.py::cloud_browser`` (action=screenshot).
    AI image
    GENERATION does not pass through here at all — it persists in
    ``providers/base_media.py::_persist_asset`` and emits an ``ImageContent``
    block carrying the ``file_id``.
    """
    import time

    from matrx_ai.tools.image_outputs import normalize_tool_output_async

    if isinstance(raw, ToolResult):
        raw.started_at = raw.started_at or started_at
        raw.completed_at = raw.completed_at or time.time()
        raw.tool_name = raw.tool_name or tool_name
        raw.call_id = raw.call_id or call_id
        if raw.success and raw.output is not None:
            raw.output = await normalize_tool_output_async(
                raw.output, tool_name=raw.tool_name or tool_name
            )
        return raw

    if isinstance(raw, dict) and raw.get("status") == "error":
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=str(raw.get("error", raw.get("result", "Unknown error"))),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=call_id,
        )

    output = await normalize_tool_output_async(raw, tool_name=tool_name)
    return ToolResult(
        success=True,
        output=output,
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=call_id,
    )


# ------------------------------------------------------------------
# Module-level helpers — the primary public API for host applications
# ------------------------------------------------------------------

def register_external_tool_handler(
    tool_name: str, handler: ExternalToolHandler
) -> None:
    """Register an async handler for a single named tool.

    The handler signature must be::

        async def my_handler(args: dict, ctx: ToolContext) -> ToolResult: ...

    Args:
        tool_name: Exact name of the tool as stored in the ``tools`` database table.
        handler:   Async callable that executes the tool and returns a ``ToolResult``.

    This registration takes priority over any app-level handler registered via
    ``register_external_app_handler``.
    """
    ExternalHandlerRegistry.get_instance().register(tool_name, handler)


def register_external_app_handler(
    source_kind: str, handler: ExternalToolHandler
) -> None:
    """Register a catch-all async handler for all tools owned by ``source_kind``.

    The handler receives every tool call for tools whose ``source_kind`` column in
    the database matches the given string.  Use ``ctx.tool_name`` inside the handler
    to route to the correct local implementation.

    The handler signature must be::

        async def my_dispatcher(args: dict, ctx: ToolContext) -> ToolResult: ...

    Args:
        source_kind: Value of the ``source_kind`` DB column for the tools this handles
                    (e.g. ``"matrx_local"``).
        handler:    Async callable that dispatches to the appropriate local tool.
    """
    ExternalHandlerRegistry.get_instance().register_app_handler(source_kind, handler)


async def invoke_external_handler(
    tool_name: str,
    source_kind: str | None,
    args: dict[str, Any],
    ctx: ToolContext,
) -> ToolResult:
    """Invoke the registered handler for a tool, returning a normalised ``ToolResult``.

    This is called internally by ``ToolExecutor._execute_external_handler``.
    It handles:
    - handler lookup (with graceful error if none registered)
    - invocation with timeout guard inherited from the executor
    - normalisation of raw return values into ``ToolResult``
    - exception capture → structured ``ToolResult`` with error details
    """
    import time

    registry = ExternalHandlerRegistry.get_instance()
    handler = registry.get_handler(tool_name, source_kind)

    if handler is None:
        app_label = f"'{source_kind}'" if source_kind else "unknown"
        vcprint(
            {
                "tool_name": tool_name,
                "source_kind": source_kind,
                "registered_tools": registry.registered_tools,
                "registered_apps": registry.registered_apps,
            },
            f"[ExternalHandlerRegistry] No handler registered for tool '{tool_name}' (source_kind={app_label})",
            color="red",
        )
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="no_handler",
                message=(
                    f"Tool '{tool_name}' (source_kind={app_label}) requires an external handler "
                    f"that has not been registered. "
                    f"Call register_external_tool_handler('{tool_name}', handler) or "
                    f"register_external_app_handler({app_label}, handler) at startup."
                ),
                is_retryable=False,
                suggested_action=(
                    "This tool cannot be executed in the current environment. "
                    "Inform the user and suggest an alternative approach."
                ),
            ),
            started_at=time.time(),
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=ctx.call_id,
        )

    started_at = time.time()
    try:
        raw_result = await handler(args, ctx)
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="external_handler_error",
                message=str(exc),
                traceback=traceback.format_exc(),
                is_retryable=False,
                suggested_action="The external tool handler raised an unexpected exception. Check the host application logs.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=ctx.call_id,
        )

    return await _normalise_result(raw_result, tool_name, ctx.call_id, started_at)
