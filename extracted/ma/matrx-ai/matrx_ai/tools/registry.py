from __future__ import annotations

import asyncio
import importlib
import traceback
from collections.abc import Awaitable, Callable
from typing import Any

from matrx_connect.context.events import WarningPayload
from matrx_utils import detached_task, vcprint
from pydantic import BaseModel

from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.tool_def_db import get_tool_def_manager
from matrx_ai.tools.vfs_routing import (
    FS_EDIT_TOOL_DEFINITION,
    is_vfs_globally_enabled,
    remap,
    should_route_to_vfs,
)

# Canonical server-side executor names that mean "run inside one of our own
# Python processes". The registry uses this to decide whether a `tool_def`
# row with `source_kind='native'` should be treated as LOCAL (callable in
# this codebase) — any binding to one of these executors means we resolve
# the implementation through ``function_path`` / module import.
_SERVER_EXECUTORS: frozenset[str] = frozenset({"matrx-ai-core", "aidream"})

TOOL_REGISTRY_DEFINITION_LOAD_FAILED_KIND = "tool_registry_definition_load_failed"


async def _capture_definition_load_failure(
    exc: BaseException, *, tool_name: str, tool_id: str | None, source_kind: str | None
) -> None:
    """Capture one rejected registry row without retaining its provider schema."""
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        exc,
        kind=TOOL_REGISTRY_DEFINITION_LOAD_FAILED_KIND,
        route="tool_registry.load",
        error_type=type(exc).__name__,
        context={
            "tool_name": tool_name,
            "tool_id": tool_id,
            "source_kind": source_kind,
        },
    )


def _schedule_definition_load_failure(
    exc: BaseException, *, tool_name: str, row: dict[str, Any]
) -> None:
    """Persist async startup/reload failures when an event loop is available."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    detached_task(
        _capture_definition_load_failure(
            exc,
            tool_name=tool_name,
            tool_id=str(row["id"]) if row.get("id") else None,
            source_kind=str(row["source_kind"]) if row.get("source_kind") else None,
        ),
        name="capture_tool_registry_definition_load_failure",
    )


class ToolRegistry:
    """Singleton registry: loads tool definitions from the database and
    resolves implementations at startup.

    Design principles:
      - Database is the *metadata* authority (name, description, params, etc.)
      - Code is the *execution* authority (the actual callable)
      - Routing decisions (server vs client vs MCP) live in Python code,
        keyed on the active executor set for the current request.
    """

    _instance: ToolRegistry | None = None

    def __init__(self) -> None:
        # Canonical name → ToolDefinition.
        self._tools: dict[str, ToolDefinition] = {}
        # Tool UUID → canonical name (for UUID-form lookups at the edge).
        self._tools_by_id: dict[str, str] = {}
        # Canonical tool name → set of executor names bound to it (from
        # ``tool_binding`` rows with ``is_active=true``). Empty / missing
        # means the tool has no executors and cannot dispatch anywhere.
        # Used by ``resolve_executor_binding`` to compute the per-request
        # routing decision under the canonical policy (client > MCP > server).
        self._bindings_by_tool: dict[str, set[str]] = {}
        # Executor name → parent_executor_name (from ``tool_executor`` rows).
        # Drives ``client_kinds_for_executor`` — the surface→executor chain
        # walk that decides which client executor names are ACTIVE for a
        # request. None / missing parent ends the chain.
        self._executor_parents: dict[str, str | None] = {}
        self._loaded: bool = False

    @classmethod
    def get_instance(cls) -> ToolRegistry:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def clear(self) -> None:
        """Wipe every in-memory index so the next ``load_from_database`` call
        rebuilds from scratch. Used by the admin cache-bust endpoint after a
        migration that adds/removes/edits ``tool.definition`` rows.
        """
        self._tools.clear()
        self._tools_by_id.clear()
        self._bindings_by_tool.clear()
        self._executor_parents.clear()
        self._loaded = False

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    async def load_from_database(self) -> int:
        """Load all active tools — host tool source first, then the ORM path.

        A configured ``tool_source`` seam (explicit, or derived from
        ``server_url`` + ``source_app`` — see ``matrx_ai.tools.tool_source``)
        is checked BEFORE the ORM base, so a client host never touches
        ``get_base("ToolDefBase")``. Returns the number of tools loaded.
        """
        source = self._resolve_tool_source()
        if source is not None:
            rows = await self._fetch_tools_from_source(source)
            loaded = self._load_rows(rows)
            await self._load_bindings_from_source(source)
            await self._load_executors_from_source(source)
            return loaded
        rows = await self._fetch_tools_async()
        loaded = self._load_rows(rows)
        await self._load_bindings_async()
        await self._load_executors_async()
        return loaded

    async def reload_from_database(self) -> int:
        """Rebuild DB-backed indexes off to the side, then swap atomically.

        ``clear(); await load_from_database()`` exposes an empty/partially loaded
        process-global registry to concurrent requests. A cache notification is
        asynchronous by definition, so reloads must leave the previous coherent
        snapshot serving until the replacement is complete.
        """
        replacement = type(self)()
        loaded = await replacement.load_from_database()
        self._tools = replacement._tools
        self._tools_by_id = replacement._tools_by_id
        self._bindings_by_tool = replacement._bindings_by_tool
        self._executor_parents = replacement._executor_parents
        self._loaded = replacement._loaded
        return loaded

    def load_from_database_sync(self) -> int:
        """Load all active tools (sync entry) — host tool source first.

        Uses the ORM's synchronous wrappers when no event loop is running.
        """
        source = self._resolve_tool_source()
        if source is not None:
            import asyncio

            try:
                asyncio.get_running_loop()
            except RuntimeError:
                rows = asyncio.run(self._fetch_tools_from_source(source))
                loaded = self._load_rows(rows)
                asyncio.run(self._load_bindings_from_source(source))
                asyncio.run(self._load_executors_from_source(source))
                return loaded
            vcprint(
                "[ToolRegistry] load_from_database_sync called with a tool_source "
                "configured INSIDE a running event loop — use the async "
                "load_from_database() / initialize_tool_system() instead.",
                color="red",
            )
            raise RuntimeError(
                "load_from_database_sync cannot drive an async tool_source from "
                "inside a running event loop — call the async "
                "load_from_database() / initialize_tool_system() instead."
            )
        rows = self._fetch_tools_via_orm_sync()
        loaded = self._load_rows(rows)
        self._load_bindings_sync()
        self._load_executors_sync()
        return loaded

    @staticmethod
    def _resolve_tool_source() -> Any | None:
        """The configured/derived host tool source, or None (ORM path)."""
        from matrx_ai.tools.tool_source import get_tool_source

        return get_tool_source()

    @staticmethod
    async def _fetch_tools_from_source(source: Any) -> list[dict[str, Any]]:
        """Fetch rows from the host tool source; scream + [] on failure."""
        try:
            rows = await source.list_tools()
        except Exception as exc:
            vcprint(
                {"error": str(exc), "traceback": traceback.format_exc()},
                "[ToolRegistry] Host tool_source fetch failed. No tools will be "
                "available from the source.",
                color="red",
            )
            return []
        return [row for row in rows or [] if isinstance(row, dict)]

    async def _load_bindings_from_source(self, source: Any) -> None:
        """Optional duck-typed ``list_bindings()`` on a host tool source.

        A source that can serve ``tool.binding`` rows (tool_id +
        executor_name) lets ``resolve_executor_binding`` work on a client
        host; sources without it leave the map empty (server-side routing).
        """
        method = getattr(source, "list_bindings", None)
        if not callable(method):
            return
        try:
            items = await method()
        except Exception as exc:
            vcprint(
                f"[ToolRegistry] tool_source.list_bindings failed: {exc!r} — "
                f"skipping binding map; tools route server-only",
                color="yellow",
            )
            return
        self._index_bindings(list(items or []))

    async def _load_executors_from_source(self, source: Any) -> None:
        """Optional duck-typed ``list_executors()`` on a host tool source."""
        method = getattr(source, "list_executors", None)
        if not callable(method):
            return
        try:
            items = await method()
        except Exception as exc:
            vcprint(
                f"[ToolRegistry] tool_source.list_executors failed: {exc!r} — "
                f"executor parent chains unavailable",
                color="yellow",
            )
            return
        self._index_executors(list(items or []))

    def _load_rows(self, rows: list[dict[str, Any]]) -> int:
        if not rows:
            vcprint(
                "[ToolRegistry] Database returned 0 tool rows. No tools will be available.",
                color="red",
            )
            self._loaded = True
            return 0

        # Pull the in-process @tool registry — DB rows no longer carry
        # function_path, so the implementation has to be looked up through
        # DeclaredTool.func. Lazy import so the registry stays operational
        # even when the declarations module hasn't been loaded yet.
        # ``get_effective_declared`` resolves both singly-declared tools AND
        # generic-family members (e.g. ``bundle:list_*`` → one shared handler),
        # so a data-only bundle row dispatches with zero per-bundle code.
        try:
            from matrx_ai.tools.declared import get_effective_declared
        except Exception:
            get_effective_declared = None  # type: ignore[assignment]

        count = 0
        failed: list[str] = []
        host_precedence_kept: list[str] = []
        flipped_to_external: list[str] = []
        for row in rows:
            tool_name = row.get("name", "?")
            try:
                tool_def = self._row_to_definition(row)
                if tool_def.tool_type == ToolType.LOCAL:
                    # Bridge DB → code: pick up the function_path + callable
                    # from the in-memory @tool declaration (or matching family)
                    # when present so the executor can dispatch this tool.
                    dt = get_effective_declared(tool_def.name) if get_effective_declared else None
                    if dt is not None:
                        tool_def.function_path = dt.function_path
                        tool_def._callable = dt.func
                    self._apply_vfs_routing(tool_def)
                    if not tool_def._callable and tool_def.function_path:
                        # VFS routing may have rewritten the path; resolve.
                        tool_def._callable = self._resolve_callable(tool_def.function_path)
                # EXTERNAL_HANDLER, AGENT, and EXTERNAL_MCP tools have no local
                # callable to resolve — their execution is delegated at runtime.

                # ── HOST-EXECUTOR PRECEDENCE (the source_kind defusal) ──────
                # A row that resolves to LOCAL with NO callable and NO
                # function_path cannot dispatch anywhere on its own. It must
                # NEVER clobber an execution path the host already has:
                #   1. An existing registry entry that CAN execute (a host-
                #      registered EXTERNAL_HANDLER def, a resolved callable)
                #      keeps its execution; the row only contributes identity
                #      (tool_id) so UUID lookups resolve.
                #   2. Otherwise, a host-registered ExternalHandlerRegistry
                #      handler for this name flips the def to
                #      EXTERNAL_HANDLER so dispatch reaches that handler.
                # Without this, a server/DB load on a client host turns every
                # host-executed tool into `no_viable_executor` at once.
                if not self._is_executable(tool_def):
                    existing = self._tools.get(tool_def.name)
                    if existing is not None and self._is_executable(existing):
                        if tool_def.tool_id:
                            if not existing.tool_id:
                                existing.tool_id = tool_def.tool_id
                            self._tools_by_id[tool_def.tool_id] = existing.name
                        host_precedence_kept.append(tool_def.name)
                        count += 1
                        continue
                    from matrx_ai.tools.external_handlers import (
                        ExternalHandlerRegistry,
                    )

                    if ExternalHandlerRegistry.get_instance().has_handler(
                        tool_def.name, tool_def.source_kind
                    ):
                        tool_def.tool_type = ToolType.EXTERNAL_HANDLER
                        flipped_to_external.append(tool_def.name)

                self._tools[tool_def.name] = tool_def
                if tool_def.tool_id:
                    self._tools_by_id[tool_def.tool_id] = tool_def.name
                count += 1
            except Exception as exc:
                failed.append(tool_name)
                _schedule_definition_load_failure(exc, tool_name=tool_name, row=row)
                vcprint(
                    {
                        "tool": tool_name,
                        "function_path": row.get("function_path", ""),
                        "error": str(exc),
                        "traceback": traceback.format_exc(),
                    },
                    f"[ToolRegistry] Failed to load tool: {tool_name}",
                    color="red",
                )

        if failed:
            vcprint(
                failed,
                f"[ToolRegistry] {len(failed)} tool(s) failed to load",
                color="red",
            )

        if host_precedence_kept:
            vcprint(
                sorted(host_precedence_kept),
                f"[ToolRegistry] {len(host_precedence_kept)} row(s) had no "
                f"execution path — kept the host-registered executable "
                f"definition (host-executor precedence)",
                color="cyan",
            )
        if flipped_to_external:
            vcprint(
                sorted(flipped_to_external),
                f"[ToolRegistry] {len(flipped_to_external)} row(s) had no "
                f"execution path but a registered external handler — typed "
                f"EXTERNAL_HANDLER so dispatch reaches the host handler",
                color="cyan",
            )

        self._scream_on_wire_collisions()

        count += self._maybe_inject_fs_edit()

        self._loaded = True
        return count

    def _scream_on_wire_collisions(self) -> None:
        """Loudly report any pair of loaded canonical names that collapse to
        the same provider WIRE form (``:`` → ``__``). Both rows stay loaded
        (refusing one at load would arbitrarily break a live tool), but the
        model-called wire name is ambiguous at dispatch until one row is
        renamed — a data defect in ``tool.definition`` that must be fixed at
        the source, hence the scream.
        """
        from matrx_ai.config.wire_names import to_wire_name

        by_wire: dict[str, list[str]] = {}
        for name in self._tools:
            by_wire.setdefault(to_wire_name(name), []).append(name)
        collisions = {w: ns for w, ns in by_wire.items() if len(ns) > 1}
        if collisions:
            vcprint(
                collisions,
                "🚨 [ToolRegistry] WIRE-NAME COLLISION AMONG LOADED TOOLS — the "
                "listed canonical names serialize to the SAME provider wire name; "
                "dispatch of the model's call is ambiguous (first match wins). "
                "RENAME one row in tool.definition — ':' and '__' collapse to the "
                "same wire spelling.",
                color="red",
            )

    @staticmethod
    def _is_executable(tool_def: ToolDefinition) -> bool:
        """Whether this definition carries an execution path of its own.

        Non-LOCAL types delegate at runtime (external handler / MCP / agent)
        and always count as executable. A LOCAL def needs a resolved callable
        or a function_path — otherwise the executor rejects it with
        ``no_viable_executor``.
        """
        if tool_def.tool_type != ToolType.LOCAL:
            return True
        return bool(tool_def._callable) or bool((tool_def.function_path or "").strip())

    def load_from_definitions(self, definitions: list[ToolDefinition]) -> int:
        """Load tool definitions directly (host backfill / tests).

        Applies the same host-executor precedence as ``_load_rows``: an
        incoming definition with no execution path never clobbers an existing
        executable entry under the same name.
        """
        count = 0
        for tool_def in definitions:
            if tool_def.tool_type == ToolType.LOCAL and tool_def._callable is None:
                try:
                    self._apply_vfs_routing(tool_def)
                    if tool_def.function_path:
                        tool_def._callable = self._resolve_callable(tool_def.function_path)
                except Exception as exc:
                    vcprint(
                        f"Could not resolve callable for '{tool_def.name}': {exc}\n{traceback.format_exc()}",
                        "[ToolRegistry] Callable resolution failed",
                        color="red",
                    )
                    continue
            if not self._is_executable(tool_def):
                existing = self._tools.get(tool_def.name)
                if existing is not None and self._is_executable(existing):
                    if tool_def.tool_id:
                        if not existing.tool_id:
                            existing.tool_id = tool_def.tool_id
                        self._tools_by_id[tool_def.tool_id] = existing.name
                    count += 1
                    continue
            self._tools[tool_def.name] = tool_def
            if tool_def.tool_id:
                self._tools_by_id[tool_def.tool_id] = tool_def.name
            count += 1
        count += self._maybe_inject_fs_edit()
        self._loaded = True
        return count

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_local(
        self,
        name: str,
        func: Callable[..., Awaitable[Any]],
        description: str = "",
        category: str | None = None,
        tags: list[str] | None = None,
        **overrides: Any,
    ) -> ToolDefinition:
        """Register a local tool from a Python function.

        If the function's first parameter is a Pydantic ``BaseModel``, its
        JSON Schema is auto-generated for the ``parameters`` field.
        """
        import inspect

        sig = inspect.signature(func)
        params = list(sig.parameters.values())

        parameters: dict[str, Any] = overrides.pop("parameters", {})
        if not parameters and params:
            first_param = params[0]
            annotation = first_param.annotation
            if annotation is not inspect.Parameter.empty:
                try:
                    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
                        parameters = self._pydantic_to_param_dict(annotation)
                except TypeError:
                    pass

        tool_def = ToolDefinition(
            name=name,
            description=description or func.__doc__ or "",
            parameters=parameters,
            tool_type=ToolType.LOCAL,
            function_path=f"{func.__module__}.{func.__qualname__}",
            category=category,
            tags=tags or [],
            **overrides,
        )
        tool_def._callable = func
        self._tools[name] = tool_def
        return tool_def

    def register(self, tool_def: ToolDefinition) -> None:
        """Register a pre-built ToolDefinition (e.g. from agent-as-tool setup)."""
        self._tools[tool_def.name] = tool_def
        if tool_def.tool_id:
            self._tools_by_id[tool_def.tool_id] = tool_def.name

    def ensure_registered(
        self,
        name: str,
        *,
        description: str = "",
        parameters: dict[str, Any] | None = None,
        tool_id: str | None = None,
        source_kind: str | None = None,
        category: str | None = None,
    ) -> ToolDefinition:
        """Idempotently ensure ``name`` is in the registry; register if missing.

        Returns the ``ToolDefinition`` either way. Used by every code path
        that **dynamically injects** a tool into the active tool set
        (capability resolution, discovery handlers, request-supplied inline
        tools). Without this guarantee, the executor's lookup at dispatch
        time fails for any tool that wasn't already loaded from the
        ``public.tool_def`` table at startup — which is exactly the
        ``Tool 'take_screenshot' not found in registry`` failure class.

        Idempotence: if a ``ToolDefinition`` already exists under ``name``
        the existing entry is returned unchanged. Only when nothing is
        registered does the helper synthesize a new entry from the
        supplied fields.

        The synthesized definition uses ``tool_type=LOCAL`` with no
        callable and no function_path — the only valid execution path for
        a tool registered this way is **client delegation** via
        ``ctx.client_tools``. Callers that intend the tool to execute
        server-side must register a real ToolDefinition via
        ``register_local`` / ``register`` instead.

        Wire-squatting guard: a name whose WIRE form (``:`` → ``__``, see
        ``matrx_ai.config.wire_names``) collides with a DIFFERENT existing
        registry entry's wire form is REFUSED. Registering it would make the
        model-called wire name ambiguous at dispatch — the squatter would
        direct-hit in ``_normalize_called_name`` and shadow the canonical
        tool for the whole process (this registry is a process-global
        singleton shared across all users/requests). The merge primitive
        rejects such specs earlier with a clean request error; this raise is
        the independent second layer.
        """
        existing = self._tools.get(name)
        if existing is not None:
            return existing

        from matrx_ai.config.wire_names import to_wire_name

        wire = to_wire_name(name)
        for other in self._tools:
            if other != name and to_wire_name(other) == wire:
                vcprint(
                    {"refused_name": name, "existing_name": other, "shared_wire_name": wire},
                    "🚨 [ToolRegistry] WIRE-SQUATTING REFUSED — ensure_registered was "
                    "asked to register a name whose provider wire form collides with "
                    "an existing tool. Accepting it would shadow the existing tool at "
                    "dispatch for the entire process. The requesting tool must be "
                    "renamed.",
                    color="red",
                )
                raise ValueError(
                    f"Tool name {name!r} collides on the provider wire form "
                    f"({wire!r}) with existing registry tool {other!r}. Rename the "
                    f"tool — ':' and '__' collapse to the same wire spelling."
                )

        synthesized = ToolDefinition(
            name=name,
            tool_id=tool_id,
            description=description,
            parameters=parameters or {},
            tool_type=ToolType.LOCAL,
            function_path="",
            source_kind=source_kind or "agent_authored",
            category=category,
        )
        self._tools[name] = synthesized
        if synthesized.tool_id:
            self._tools_by_id[synthesized.tool_id] = name
        vcprint(
            f"[ToolRegistry] ensure_registered: synthesized entry for "
            f"{name!r} (was missing — dynamically injected by an upstream "
            f"merge / capability / discovery path)",
            color="cyan",
        )
        return synthesized

    def unregister(self, name: str) -> bool:
        tool_def = self._tools.pop(name, None)
        if tool_def and tool_def.tool_id:
            self._tools_by_id.pop(tool_def.tool_id, None)
        return tool_def is not None

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    def get(self, name_or_id: str) -> ToolDefinition | None:
        resolved = self._resolve_tool_name(name_or_id)
        return self._tools.get(resolved) if resolved else None

    def _resolve_tool_name(self, name_or_id: str) -> str | None:
        """Resolve a tool name or UUID to the canonical tool name, or None if not found."""
        if name_or_id in self._tools:
            return name_or_id
        if name_or_id in self._tools_by_id:
            return self._tools_by_id[name_or_id]
        return None

    def get_provider_tools(self, tool_names: list[str], provider: str) -> list[dict[str, Any]]:
        if not self._loaded:
            vcprint(
                {
                    "requested_tools": tool_names,
                    "provider": provider,
                    "registry_loaded": self._loaded,
                    "registry_count": len(self._tools),
                },
                "[ToolRegistry] Registry was never loaded! Tools will not be included in the request.",
                color="red",
            )

        # ── GUARD: tool IDs must NEVER reach the provider boundary ───────────
        # Tool IDs (DB UUIDs) are resolved to NAMES at the edge (the single tool
        # write-path, merge_request_tools). A raw UUID arriving here means a
        # UnifiedConfig was built bypassing that conversion — a real bug. We do
        # NOT silently resolve it (that hides the bug); we scream in red with the
        # full payload and RAISE, so it gets fixed at the source. See
        # common-docs/systems/agents/agent-tools/STATE.md.
        import re as _re

        _uuid_re = _re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        )
        _id_leaks = [n for n in tool_names if isinstance(n, str) and _uuid_re.match(n)]
        if _id_leaks:
            vcprint(
                {
                    "tool_id_leaks": _id_leaks,
                    "all_requested_tools": tool_names,
                    "provider": provider,
                },
                "[ToolRegistry] 🚨🚨🚨 TOOL ID(s) REACHED THE PROVIDER BOUNDARY 🚨🚨🚨\n"
                "Tool IDs (DB UUIDs) must be resolved to NAMES at the EDGE "
                "(merge_request_tools) — a raw UUID here means a UnifiedConfig was built "
                "that bypassed the edge conversion. This is NOT auto-resolved on purpose "
                "(that would hide the bug). FIX THE CALLER to pass tool names, not IDs.",
                color="red",
            )
            raise ValueError(
                f"Tool IDs reached the provider boundary (must be tool names): "
                f"{_id_leaks}. Resolve IDs→names at the edge. See common-docs/systems/agents/agent-tools/STATE.md."
            )

        # Projected agent tools (``custom_tool_N``) are NEVER in the registry by
        # design — a projected agent's ``ToolDefinition`` lives on the request's
        # ``AppContext.metadata[PROJECTED_AGENT_TOOLS_KEY]`` (agent_projection).
        # The executor's DISPATCH path already consults that map first; the
        # provider-DECLARATION path (here) must do the SAME, or a handoff/
        # reference/agent-as-tool passed via ``request.tools`` is silently dropped
        # and the model never sees it (it can't call a tool it isn't offered).
        # This is the second, independent layer that makes the projection reach
        # BOTH the model (declaration) and dispatch (execution).
        from matrx_ai.tools.agent_projection import lookup_projected_tool

        resolved = [self._resolve_tool_name(n) for n in tool_names]
        out: list[dict[str, Any]] = []
        missing: list[str] = []
        for name, r in zip(tool_names, resolved):
            if r is not None:
                out.append(self._tools[r].get_provider_format(provider))
                continue
            projected = lookup_projected_tool(name)
            if projected is not None:
                out.append(projected.get_provider_format(provider))
                continue
            missing.append(name)
        if missing:
            vcprint(
                {
                    "missing_tools": missing,
                    "requested_tools": tool_names,
                    "provider": provider,
                    "available_tools": list(self._tools.keys())[:20],
                    "registry_count": len(self._tools),
                },
                f"[ToolRegistry] {len(missing)} requested tool(s) not found in registry",
                color="red",
            )
            self._emit_missing_tools_warning(missing, tool_names, provider)

        return out

    def _emit_missing_tools_warning(
        self, missing: list[str], requested: list[str], provider: str
    ) -> None:
        """Fire-and-forget: emit a warning to the client stream for missing tools."""
        try:
            from matrx_ai.context.app_context import get_app_context

            ctx = get_app_context()
            emitter = ctx.emitter
            if emitter is None:
                return

            async def _warn() -> None:
                await emitter.send_warning(
                    WarningPayload(
                        code="tools_missing",
                        system_message=f"{len(missing)} requested tool(s) not found in registry and will not be available to the model.",
                        user_message="Some tools configured for this request are not registered and will be unavailable.",
                        level="medium",
                        recoverable=True,
                        metadata={
                            "missing_tools": missing,
                            "requested_tools": requested,
                            "provider": provider,
                            "registry_count": len(self._tools),
                        },
                    )
                )

            loop = asyncio.get_event_loop()
            if loop.is_running():
                from matrx_utils import detached_task

                detached_task(_warn(), name="tool_registry_missing_warning")
        except Exception:
            pass

    def list_tools(
        self,
        category: str | None = None,
        tags: list[str] | None = None,
        tool_type: ToolType | None = None,
        active_only: bool = True,
    ) -> list[ToolDefinition]:
        result: list[ToolDefinition] = []
        for t in self._tools.values():
            if active_only and not t.is_active:
                continue
            if category and t.category != category:
                continue
            if tags and not set(tags).issubset(set(t.tags)):
                continue
            if tool_type is not None and t.tool_type != tool_type:
                continue
            result.append(t)
        return result

    def list_tool_names(self) -> list[str]:
        return list(self._tools.keys())

    @property
    def loaded(self) -> bool:
        return self._loaded

    @property
    def count(self) -> int:
        return len(self._tools)

    def bindings_for_tool(self, tool_name: str) -> set[str]:
        """Return the set of executor names bound to ``tool_name`` (from
        ``tool_binding`` rows with ``is_active=true``).

        Empty set means the tool has no executors and cannot dispatch anywhere.
        """
        return set(self._bindings_by_tool.get(tool_name, set()))

    def client_bindings_for_tool(self, tool_name: str) -> set[str]:
        """Return the tool's configured client executor bindings.

        A non-empty result means the tool has a known executor, even when none
        of those client executors is live for the current server-side request.
        """
        return {
            binding
            for binding in self._bindings_by_tool.get(tool_name, set())
            if _is_client_executor(binding)
        }

    def all_tools(self) -> list[ToolDefinition]:
        """Snapshot of every tool currently in the registry. Order is by name."""
        return [self._tools[k] for k in sorted(self._tools)]

    def resolve_executor_binding(self, tool_name: str, active_executors: set[str]) -> str:
        """The SINGLE authority for routing a registered tool to an executor.

        Returns ``"surface"`` (client delegation) when the tool has a binding
        to one of this request's active CLIENT executors, ``"server"`` otherwise.

        Policy (resolved in Python, NOT from DB columns): client > MCP > server.
        A tool is delegated to the client iff one of its ``tool_binding`` rows
        names a client executor that is in ``active_executors`` for this request.
        Otherwise it runs server-side (either via an MCP executor binding, or
        via a server executor binding — both dispatch happens via the executor's
        own runtime).

        ``active_executors`` is the set of executor names the caller has decided
        are live for this request (server executors are always present; client
        executors only when a client is actually connected; MCP executors only
        for users with active connections to those servers). Empty set ⇒ all
        registered tools fall back to server-side dispatch.
        """
        bindings = self._bindings_by_tool.get(tool_name)
        if not bindings:
            return "server"

        # Client executors take priority. We treat any executor that begins
        # with one of the canonical client executor prefixes as a client
        # binding. Hardcoded names (per the canonical-executor list) plus
        # any sub-executor under them (e.g. ``matrx-user.chat``).
        for binding in bindings:
            if binding not in active_executors:
                continue
            if _is_client_executor(binding):
                return "surface"

        return "server"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    async def _fetch_tools_async() -> list[dict[str, Any]]:
        try:
            items = await get_tool_def_manager().filter_items(is_active=True)
            return [item.to_dict() for item in items]
        except Exception as exc:
            vcprint(
                {
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                },
                "[ToolRegistry] Failed to fetch tools from database. No tools will be available.",
                color="red",
            )
            return []

    @staticmethod
    def _fetch_tools_via_orm_sync() -> list[dict[str, Any]]:
        try:
            items = get_tool_def_manager().filter_items_sync(is_active=True)
            return [item.to_dict() if hasattr(item, "to_dict") else item for item in items]
        except Exception as exc:
            vcprint(
                {
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                },
                "[ToolRegistry] Failed to fetch tools from database (sync). No tools will be available.",
                color="red",
            )
            return []

    async def _load_bindings_async(self) -> None:
        """Populate ``self._bindings_by_tool`` from ``tool.binding``.

        ``tool_binding`` is the pure M2M join — tool_id, executor_name,
        is_active. No flags, no priorities, no surfaces; routing decisions
        happen in code, NOT from rows.

        Tolerates the table not existing yet and tolerates the base not
        being injected by the host — in either case the registry stays
        operational with an empty map (everything routes server-side).
        """
        try:
            from matrx_ai.tools.tool_binding_db import (
                tool_binding_manager_instance as bindings_manager,
            )
        except Exception:
            return
        try:
            items = await bindings_manager.filter_items(is_active=True)
        except Exception as exc:
            vcprint(
                f"[ToolRegistry] tool_binding fetch failed: {exc!r} — "
                f"skipping binding map; tools route server-only",
                color="yellow",
            )
            return
        self._index_bindings(items)

    def _load_bindings_sync(self) -> None:
        try:
            from matrx_ai.tools.tool_binding_db import (
                tool_binding_manager_instance as bindings_manager,
            )
        except Exception:
            return
        try:
            items = bindings_manager.filter_items_sync(is_active=True)
        except Exception as exc:
            vcprint(
                f"[ToolRegistry] tool_binding sync fetch failed: {exc!r} — "
                f"skipping binding map; tools route server-only",
                color="yellow",
            )
            return
        self._index_bindings(items)

    async def _load_executors_async(self) -> None:
        """Populate ``self._executor_parents`` from ``tool.executor``.

        Same tolerance contract as the bindings loader — a missing table or
        un-injected base leaves the map empty, and ``client_kinds_for_executor``
        falls back to dot-notation prefix ancestry so surface delegation still
        resolves.
        """
        try:
            from matrx_ai.tools.tool_executor_db import (
                tool_executor_manager_instance as executors_manager,
            )
        except Exception:
            return
        try:
            items = await executors_manager.filter_items(is_active=True)
        except Exception as exc:
            vcprint(
                f"[ToolRegistry] tool_executor fetch failed: {exc!r} — "
                f"executor parent chains unavailable; falling back to "
                f"dot-notation ancestry only",
                color="yellow",
            )
            return
        self._index_executors(items)

    def _load_executors_sync(self) -> None:
        try:
            from matrx_ai.tools.tool_executor_db import (
                tool_executor_manager_instance as executors_manager,
            )
        except Exception:
            return
        try:
            items = executors_manager.filter_items_sync(is_active=True)
        except Exception as exc:
            vcprint(
                f"[ToolRegistry] tool_executor sync fetch failed: {exc!r} — "
                f"executor parent chains unavailable; falling back to "
                f"dot-notation ancestry only",
                color="yellow",
            )
            return
        self._index_executors(items)

    def _index_executors(self, items: list[Any]) -> None:
        parents: dict[str, str | None] = {}
        for item in items:
            row = item.to_dict() if hasattr(item, "to_dict") else item
            name = row.get("name")
            if not name:
                continue
            parent = row.get("parent_executor_name")
            parents[str(name)] = str(parent) if parent else None
        self._executor_parents = parents
        vcprint(
            f"[Tools] Indexed {len(parents)} executor(s) for parent-chain resolution",
            color="green",
        )

    def client_kinds_for_executor(self, executor_name: str) -> set[str]:
        """Executor name → every executor name considered ACTIVE for a request
        whose surface is bound to ``executor_name``.

        This is the missing half of the surface→executor delegation chain
        (``tool_merge._resolve_active_client_kinds`` calls this; it was lost
        in the 2026-05-27 tool_* cutover and every surface-routed client tool
        silently fell back to server-side → ``no_viable_executor``).

        The set is the executor itself plus its ancestors, from BOTH sources:
          - the ``tool_executor.parent_executor_name`` self-FK chain
            (max depth 3 per the table contract), and
          - dot-notation prefixes (``matrx-user.chat`` → ``matrx-user``) as a
            structural fallback so a missing/stale executor row can't silently
            kill delegation again.

        So a tool bound to an ancestor (e.g. ``matrx-user``) delegates from a
        child surface executor (``matrx-user.chat``). Total function — never
        raises, never returns empty for a non-empty input.
        """
        kinds: set[str] = set()
        current: str | None = executor_name
        depth = 0
        while current and current not in kinds and depth <= 3:
            kinds.add(current)
            current = self._executor_parents.get(current)
            depth += 1
        # Dot-notation structural ancestry (naming convention: sub-executors
        # are ``parent.child``). Complements the DB chain; harmless overlap.
        parts = executor_name.split(".")
        for i in range(1, len(parts)):
            kinds.add(".".join(parts[:i]))
        return kinds

    def _index_bindings(self, items: list[Any]) -> None:
        """Build ``tool_name → {executor_name, ...}`` from tool_binding rows.

        Rows for unknown tool_ids are skipped with a warning — they shouldn't
        happen since ``tool_binding.tool_id`` has a FK to ``tool_def.id``, but
        if a tool was loaded before its dependent rows arrived we drop them
        rather than synthesise a fake entry.
        """
        index: dict[str, set[str]] = {}
        unknown_count = 0
        for item in items:
            row = item.to_dict() if hasattr(item, "to_dict") else item
            tool_id = row.get("tool_id")
            executor_name = row.get("executor_name")
            if not tool_id or not executor_name:
                continue
            tool_name = self._tools_by_id.get(str(tool_id))
            if tool_name is None:
                unknown_count += 1
                continue
            index.setdefault(tool_name, set()).add(executor_name)
        self._bindings_by_tool = index
        if unknown_count:
            vcprint(
                f"[ToolRegistry] {unknown_count} tool_binding row(s) "
                f"reference unknown tool_ids; ignored",
                color="yellow",
            )
        vcprint(
            f"[Tools] Indexed {sum(len(s) for s in index.values())} bindings "
            f"across {len(index)} tools",
            color="green",
        )

    @staticmethod
    def _row_to_definition(row: dict[str, Any]) -> ToolDefinition:
        """Convert a ``tool.definition`` row to a ``ToolDefinition``.

        The dropped columns (``function_path``, ``source_app``, ``privileged``,
        ``deactivated_at``) no longer drive tool typing. Routing happens at
        request time via the tool-binding map. The only thing the row needs
        to say about its implementation is ``source_kind`` — one of:
          - ``native``           → first-party server tool; function path
                                   lives in code (``ToolDefinition.function_path``
                                   set by the implementer when registering /
                                   carried in code metadata, not the DB).
          - ``mcp_discovered``   → discovered from an external MCP server;
                                   ``managed_by_server_id`` is set; dispatch
                                   goes through the MCP executor.
          - ``admin_authored`` / ``agent_authored`` → custom tools created
                                   in the admin UI or by an agent; treated
                                   like ``native`` if they have a
                                   ``function_path``, otherwise client-only.
        """
        tool_name = row.get("name", "?")
        source_kind: str = row.get("source_kind") or "native"
        managed_by_server_id = row.get("managed_by_server_id")

        # The DB no longer carries function_path; first-party tools resolve
        # their callable via the ``@tool`` decorator's registration path
        # (handled by ``load_from_definitions``) or via code metadata that
        # the host attaches before / after the registry's DB load. Until that
        # bridge lands, native tool rows without a callable will fail
        # dispatch with ``no_viable_executor`` — which is the correct,
        # observable behaviour for a tool whose code isn't wired.
        function_path: str = row.get("function_path", "") or ""
        prompt_id: str | None = None

        if source_kind == "mcp_discovered" or managed_by_server_id:
            tool_type = ToolType.EXTERNAL_MCP
        elif function_path.startswith("agent:"):
            tool_type = ToolType.AGENT
            prompt_id = function_path.split(":", 1)[1]
        elif function_path.startswith("mcp:"):
            tool_type = ToolType.EXTERNAL_MCP
        elif source_kind in ("admin_authored", "agent_authored") and not function_path:
            # Custom tool with no server-side implementation — client-only.
            tool_type = ToolType.EXTERNAL_HANDLER
        else:
            tool_type = ToolType.LOCAL
            if source_kind not in ("native", "admin_authored", "agent_authored"):
                vcprint(
                    f"[ToolRegistry] Tool '{tool_name}' has unrecognized source_kind "
                    f"{source_kind!r}; treating as local. "
                    f"Valid values: 'native' | 'mcp_discovered' | 'admin_authored' | 'agent_authored'.",
                    color="yellow",
                )

        raw_annotations = row.get("annotations")
        # MCP's ToolAnnotations wire shape is one object. Older first-party
        # registry rows use a list of policy objects. Preserve the internal
        # list contract while accepting both canonical persisted shapes.
        if isinstance(raw_annotations, dict):
            annotations = [raw_annotations]
        elif isinstance(raw_annotations, list):
            annotations = raw_annotations
        elif raw_annotations is None:
            annotations = []
        else:
            raise TypeError("tool annotations must be an object, list, or null")

        guardrails = annotations
        guardrail_config: dict[str, Any] = {}
        if isinstance(guardrails, list):
            for ann in guardrails:
                if isinstance(ann, dict):
                    guardrail_config.update(ann)

        raw_params = row.get("parameters") or {}
        required_params: list[str] = []
        if (
            isinstance(raw_params, dict)
            and raw_params.get("type") == "object"
            and "properties" in raw_params
        ):
            # Unwrapping a full JSON schema to the internal key→property
            # notation LOSES two things unless carried explicitly:
            #   1. the top-level ``required: [...]`` list (the internal
            #      per-property bool can't express it for object-typed
            #      params) → carried on ToolDefinition.required_params;
            #   2. ``anyOf`` optionals (``{"anyOf": [{"type": "integer"},
            #      {"type": "null"}]}``) — the schema builder would default
            #      the missing ``type`` to "string" and providers would see
            #      the wrong type → normalized to the first non-null member.
            # Without both, every row-served tool loses its required flags
            # and mistypes optionals — the model omits mandatory args and
            # burns provider turns on invalid_arguments.
            params = {
                key: ToolRegistry._normalize_schema_property(value)
                for key, value in raw_params["properties"].items()
            }
            raw_required = raw_params.get("required")
            if isinstance(raw_required, list):
                required_params = [str(k) for k in raw_required]
        else:
            params = raw_params

        return ToolDefinition(
            name=row["name"],
            tool_id=row.get("id"),
            description=row.get("description", ""),
            parameters=params,
            output_schema=row.get("output_schema"),
            annotations=annotations,
            side_effect_class=row.get("side_effect_class"),
            tool_type=tool_type,
            function_path=function_path,
            required_params=required_params,
            source_kind=source_kind,
            managed_by_server_id=str(managed_by_server_id) if managed_by_server_id else None,
            category=row.get("category"),
            tags=row.get("tags") or [],
            icon=row.get("icon"),
            is_active=row.get("is_active", True),
            semver=row.get("semver", "1.0.0"),
            version=row.get("version", 1),
            tier=row.get("tier"),
            admin_only=bool(row.get("admin_only", False)),
            # Without this mapping the DB flag is INERT: every loaded tool
            # gets the model default False and both repeat-guards
            # (duplicate + loop) fire on declared pollers like agent_plan —
            # exactly what blocked the poll that would have returned the
            # finished results on 2026-07-07.
            dedupe_exempt=bool(row.get("dedupe_exempt", False)),
            gating=row.get("gating") or [],
            prompt_id=prompt_id,
            max_calls_per_conversation=guardrail_config.get("max_calls_per_conversation"),
            max_calls_per_minute=guardrail_config.get("max_calls_per_minute"),
            cost_cap_per_call=guardrail_config.get("cost_cap_per_call"),
            timeout_seconds=guardrail_config.get("timeout_seconds", 120.0),
            must_complete=bool(guardrail_config.get("must_complete", False)),
            max_client_wait_seconds=row.get("max_client_wait_seconds"),
        )

    @staticmethod
    def _normalize_schema_property(prop: Any) -> Any:
        """Normalize one JSON-schema property to the internal notation.

        ``anyOf`` optionals (``{"anyOf": [{"type": "integer"},
        {"type": "null"}]}``) carry no top-level ``type``; the schema builder
        would default them to "string". Lift the first non-null member's type
        (and its structural keys when absent on the wrapper) so providers see
        the real type. Everything else passes through untouched.
        """
        if not isinstance(prop, dict) or "type" in prop:
            return prop
        any_of = prop.get("anyOf")
        if not isinstance(any_of, list):
            return prop
        for member in any_of:
            if isinstance(member, dict) and member.get("type") not in (None, "null"):
                normalized = dict(prop)
                normalized["type"] = member["type"]
                for key in ("items", "enum", "properties", "required", "minimum", "maximum"):
                    if key not in normalized and key in member:
                        normalized[key] = member[key]
                return normalized
        return prop

    @staticmethod
    def _apply_vfs_routing(tool_def: ToolDefinition) -> None:
        # Mutates tool_def in place when the routing rule fires. We capture the
        # original path on a private attr so observability/log tooling can tell
        # the swap happened.
        original = tool_def.function_path
        if not should_route_to_vfs(original, tool_def.source_kind):
            return
        new_path = remap(original)
        if new_path == original:
            return
        tool_def._original_function_path = original
        tool_def._routed_to_vfs = True
        tool_def.function_path = new_path
        vcprint(
            {
                "tool": tool_def.name,
                "from": original,
                "to": new_path,
                "source_kind": tool_def.source_kind,
            },
            "[ToolRegistry] Routed tool to VFS implementation",
            color="cyan",
        )

    def _maybe_inject_fs_edit(self) -> int:
        # fs_edit has no real-disk equivalent; only register it when VFS is on
        # (or someone explicitly routed it via source_kind=native in the DB,
        # in which case it will already be present and we skip).
        if not is_vfs_globally_enabled():
            return 0
        if "fs_edit" in self._tools:
            return 0
        try:
            tool_def = ToolDefinition(**FS_EDIT_TOOL_DEFINITION)
            tool_def._callable = self._resolve_callable(tool_def.function_path)
            self._tools[tool_def.name] = tool_def
            if tool_def.tool_id:
                self._tools_by_id[tool_def.tool_id] = tool_def.name
            return 1
        except Exception as exc:
            vcprint(
                {
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                },
                "[ToolRegistry] Failed to inject synthetic fs_edit tool",
                color="red",
            )
            return 0

    @staticmethod
    def _resolve_callable(function_path: str) -> Callable[..., Awaitable[Any]]:
        if (
            not function_path
            or function_path.startswith("agent:")
            or function_path.startswith("mcp:")
        ):
            raise ValueError(f"Cannot resolve non-local function_path: {function_path}")
        # Remap legacy aidream `ai.` paths → `matrx_ai.`
        if function_path.startswith("ai."):
            function_path = "matrx_ai." + function_path[3:]
        # Normalize legacy bare sub-package paths → fully-qualified `matrx_ai.` paths
        _LEGACY_FLAT_PREFIXES = (
            "tools.",
            "agents.",
            "config.",
            "context.",
            "db.",
            "instructions.",
            "media.",
            "orchestrator.",
            "processing.",
            "providers.",
            "utils.",
            "agent_runners.",
        )
        if any(function_path.startswith(p) for p in _LEGACY_FLAT_PREFIXES):
            function_path = f"matrx_ai.{function_path}"
        module_path, func_name = function_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)
        return func

    @staticmethod
    def _pydantic_to_param_dict(model_cls: type[BaseModel]) -> dict[str, Any]:
        """Convert a Pydantic model into the internal parameter dict format."""
        schema = model_cls.model_json_schema()
        params: dict[str, Any] = {}
        properties = schema.get("properties", {})

        for field_name, field_schema in properties.items():
            param: dict[str, Any] = {
                "type": field_schema.get("type", "string"),
                "description": field_schema.get("description", ""),
            }
            for prop in (
                "items",
                "enum",
                "default",
                "minimum",
                "maximum",
                "minItems",
                "maxItems",
                "properties",
            ):
                if prop in field_schema:
                    param[prop] = field_schema[prop]
            params[field_name] = param
        return params

    # ------------------------------------------------------------------
    # MCP Server registration
    # ------------------------------------------------------------------

    async def register_mcp_server(
        self,
        server_url: str,
        server_name: str,
        mcp_client: Any | None = None,
    ) -> list[str]:
        """Connect to a remote MCP server, discover tools, register them."""
        if mcp_client is None:
            from matrx_ai.tools.external_mcp import ExternalMCPClient

            mcp_client = ExternalMCPClient()

        remote_tools = await mcp_client.discover_tools(server_url)
        registered: list[str] = []
        for tool_def in remote_tools:
            tool_def.tool_type = ToolType.EXTERNAL_MCP
            tool_def.mcp_server_url = server_url
            namespaced = f"mcp.{server_name}.{tool_def.name}"
            tool_def.name = namespaced
            self._tools[namespaced] = tool_def
            registered.append(namespaced)

        return registered


# Canonical client executor names (and prefix-roots). These are the executors
# that run INSIDE a client browser / desktop / extension, NOT inside one of
# our own server processes.
_CLIENT_EXECUTOR_ROOTS: frozenset[str] = frozenset(
    {
        "matrx-local",
        "chrome-extension",
        "matrx-user",
    }
)


def _is_client_executor(executor_name: str) -> bool:
    """True if ``executor_name`` is a client-side runtime (one a user's
    device runs), False for server runtimes (``matrx-ai-core``, ``aidream``)
    and MCP servers (``mcp.<slug>``).

    Recognizes both the bare canonical name (``chrome-extension``) and any
    sub-executor under it (``chrome-extension.pilot``).
    """
    if executor_name in _CLIENT_EXECUTOR_ROOTS:
        return True
    return any(executor_name.startswith(f"{root}.") for root in _CLIENT_EXECUTOR_ROOTS)
