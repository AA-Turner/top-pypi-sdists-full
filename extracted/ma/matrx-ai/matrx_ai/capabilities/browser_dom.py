"""``browser-dom`` capability — matrx-extend Chrome extension client bundle.

The first multi-tool capability registered against the unified injection
system (TOOL_INJECTION_REFACTOR.md). The Chrome extension carries many
browser-control tools across categories — too many to expose to the model
up front — so this capability advertises *one* discovery tool
(``load_chrome_tools``) plus the always-on set defined in the database.

Tool definitions and routing live exclusively in the database:
  - ``public.tool_def``     — canonical tool metadata (name, description,
                              parameters, source_kind, category, gating).
  - ``public.tool_binding`` — pure M2M join: ``(tool_id, executor_name)``.
                              Tools bound to the ``chrome-extension``
                              executor are the matrx-extend browser tools.
  - ``public.tool_surface_defaults`` — per-surface always_include_tools /
                              never_include_tools arrays for the
                              ``matrx-extend.browser`` surface; the host's
                              ``tool_resolve_for_request`` call honors these.

All lookups are lazy (first request after startup) so this module never
touches the DB at import time, and the registry is guaranteed to be
populated by the time any request arrives.
"""

from __future__ import annotations

from typing import Any, Literal

from matrx_utils import vcprint
from pydantic import BaseModel, Field

from matrx_ai.capabilities.models import Capability
from matrx_ai.tools.specs import InlineToolSpec, RegisteredToolSpec, ToolSpec

# ---------------------------------------------------------------------------
# Payload model — validates ``client.state["browser-dom"]`` on the wire.
# ---------------------------------------------------------------------------

DesktopBridgeStatus = Literal["native", "http", "none"]
SurfaceMode = Literal["assistant", "pilot"]
PermissionMode = Literal["ask", "act"]
TabStatus = Literal["loading", "complete"]


class BrowserDomPayload(BaseModel):
    """Runtime state from the Chrome extension that drives tool-routing
    decisions in ``load_chrome_tools``.

    Distinct from ``request.context`` (which is model-facing page facts —
    markdown, SEO, links, etc.). This payload is orchestration metadata
    consumed by server-side tool dispatchers, not the LLM.
    """

    current_url: str | None = None
    current_tab_id: int | None = None
    current_window_id: int | None = None
    page_title: str | None = None
    page_lang: str | None = None
    tab_status: TabStatus | None = None

    surface: SurfaceMode = Field(
        description="Which side-panel surface initiated the request. "
        "``assistant`` defaults to read-only categories; ``pilot`` advertises "
        "the full kit."
    )
    is_admin: bool = Field(
        description="True if the user is in ``admin.admins``. Discovery "
        "handler hard-blocks admin-only categories when False."
    )
    permission_mode: PermissionMode = Field(
        description="Per-agent gate the client enforces locally for "
        "action-tier tools. Server doesn't enforce; useful for prompt hints."
    )
    desktop_bridge: DesktopBridgeStatus = Field(
        description="Reachability of the matrx-local desktop bridge. "
        "``none`` strips ``desktop_run_command``."
    )
    onbox_ai_available: bool = Field(
        description="True if Chrome's on-device Gemini Nano is exposed. "
        "When False, ai_* tools still load but return availability hints."
    )
    optional_permissions_granted: list[str] = Field(
        default_factory=list,
        description="Optional Chrome permissions the user has granted at "
        "runtime. Discovery handler filters tools whose "
        "``required_optional_permissions`` aren't satisfied.",
    )

    open_tab_count: int | None = None
    extension_version: str = ""
    extension_id: str = ""
    loaded_categories: list[str] = Field(
        default_factory=list,
        description="Categories the agent has discovered earlier in this "
        "conversation, tracked client-side from RESOURCE_CHANGED events. "
        "Currently informational; the server may use it to detect "
        "re-discovery patterns once cross-request persistence ships.",
    )


# ---------------------------------------------------------------------------
# Surface identifier — the ``ui_surface.name`` for this capability.
# Executor identifier — the canonical client executor that runs these tools.
# ---------------------------------------------------------------------------

_MATRX_EXTEND_SURFACE = "matrx-extend.browser"
_CHROME_EXTENSION_EXECUTOR = "chrome-extension"
_NS_PREFIX = "matrx-extend:"


# ---------------------------------------------------------------------------
# Lazy DB-driven lookups — results cached after first call.
# The registry is populated by initialize_tool_system() at startup; by the
# time any request arrives and these are called, it is guaranteed to be ready.
# ---------------------------------------------------------------------------

_specs_cache: tuple[ToolSpec, ...] | None = None
_category_names_cache: list[str] | None = None
_admin_only_categories_cache: frozenset[str] | None = None


def clear_caches() -> None:
    """Invalidate every lazy cache so the next request rebuilds from the
    registry. Called by the admin cache-bust endpoint after a migration
    edits ``tool_def`` / ``tool_binding`` rows.
    """
    global _specs_cache, _category_names_cache, _admin_only_categories_cache
    _specs_cache = None
    _category_names_cache = None
    _admin_only_categories_cache = None


def _is_chrome_extension_tool(tool: Any) -> bool:
    """True iff the tool is bound to the ``chrome-extension`` executor (or
    any sub-executor under it, e.g. ``chrome-extension.pilot``).

    Replaces the legacy ``source_app == 'matrx-extend'`` test — in the new
    schema, ownership lives on the binding, not on a column.
    """
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    bindings = registry.bindings_for_tool(tool.name)
    if not bindings:
        return False
    for b in bindings:
        if b == _CHROME_EXTENSION_EXECUTOR or b.startswith(
            f"{_CHROME_EXTENSION_EXECUTOR}."
        ):
            return True
    return False


def _inline_kwargs_from_registry(local_name: str) -> dict[str, Any] | None:
    """Build ``InlineToolSpec`` kwargs for ``local_name`` from the registry row.

    Returns ``None`` when the tool is absent from the registry — this is a
    hard error: it means either initialize_tool_system() was not called, or
    the ``public.tool_def`` row is missing. The caller logs loudly and skips.
    """
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    # Tools are stored under their LOCAL name now (the 'matrx-extend:' namespace
    # was removed when the registry moved to one-row-per-tool). Look up the local
    # name first; fall back to the legacy namespaced key for any un-migrated env.
    tool = registry.get(local_name) or registry.get(_NS_PREFIX + local_name)
    if tool is None:
        return None

    properties: dict[str, Any] = {}
    required: list[str] = []
    for prop_name, prop_schema in (tool.parameters or {}).items():
        if isinstance(prop_schema, dict):
            cleaned = {k: v for k, v in prop_schema.items() if k != "required"}
            properties[prop_name] = cleaned
            if prop_schema.get("required"):
                required.append(prop_name)
        else:
            properties[prop_name] = {"type": prop_schema}

    return {
        "name": local_name,
        "description": tool.description or f"Browser tool: {local_name}",
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }


def _build_auto_load_specs() -> tuple[ToolSpec, ...]:
    """Build the always-on tool specs for the ``browser-dom`` capability.

    Per the two-input rule (common-docs/systems/agents/agent-tools/DECISIONS.md Part 1), the
    "always-on browser tools" set is defined as **every tool with an active
    binding to the ``chrome-extension`` executor**. The chrome-extension
    IS the runtime that dispatches them; the binding asserts that capability.
    No surface-defaults lookup is needed — surfaces shape *which* tools the
    AGENT sees per-page; the capability bundle defines the universe.

    ``load_chrome_tools`` is always prepended as a ``RegisteredToolSpec``
    (it has a real server-side Python handler). Every other always-on tool
    is client-side (Chrome extension); it gets an ``InlineToolSpec`` so
    its schema rides on the wire and the executor takes the client-delegation
    path unconditionally.
    """
    global _specs_cache
    if _specs_cache is not None:
        return _specs_cache

    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    # Collect tool names bound to chrome-extension (or any sub-executor).
    auto_load_names: list[str] = []
    for tool in registry.all_tools():
        if _is_chrome_extension_tool(tool):
            auto_load_names.append(tool.name)
    auto_load_names.sort()

    if not auto_load_names:
        vcprint(
            {
                "executor": _CHROME_EXTENSION_EXECUTOR,
                "hint": (
                    "Confirm tool_binding has rows for executor_name="
                    f"{_CHROME_EXTENSION_EXECUTOR!r}, and that "
                    "initialize_tool_system() was called before the first request."
                ),
            },
            "[browser-dom] CRITICAL: no tools bound to executor "
            f"{_CHROME_EXTENSION_EXECUTOR!r}. Agent will boot without "
            "always-on browser tools. Almost certainly a startup config error.",
            color="red",
        )

    specs: list[ToolSpec] = [RegisteredToolSpec(name="load_chrome_tools", delegate=False)]
    missing: list[str] = []

    for local_name in auto_load_names:
        kwargs = _inline_kwargs_from_registry(local_name)
        if kwargs is None:
            missing.append(local_name)
            vcprint(
                {
                    "tool": local_name,
                    "executor": _CHROME_EXTENSION_EXECUTOR,
                    "hint": (
                        "Tool has a chrome-extension binding but isn't in the "
                        "in-memory registry. Run initialize_tool_system()."
                    ),
                },
                f"[browser-dom] ERROR: chrome-extension tool {local_name!r} not in registry.",
                color="red",
            )
            continue
        specs.append(InlineToolSpec(**kwargs))

    if missing:
        vcprint(
            {"missing_tools": missing, "total_missing": len(missing)},
            "[browser-dom] FATAL: chrome-extension tools could not be resolved from registry. "
            "tool_binding has rows pointing at chrome-extension but tool_def rows are missing.",
            color="red",
        )

    _specs_cache = tuple(specs)
    vcprint(
        f"[browser-dom] Built always-on specs from chrome-extension bindings: "
        f"{len(_specs_cache)} tool(s) "
        f"({len(auto_load_names)} bound to chrome-extension + load_chrome_tools). "
        f"Cache will be reused for all future requests.",
        color="cyan",
    )
    return _specs_cache


def _read_always_include_tools(surface_name: str) -> list[str]:
    """Read ``tool_surface_defaults.always_include_tools`` for ``surface_name``
    via the host-injected manager. Returns a sorted list of canonical tool
    names.

    Returns ``[]`` when the manager isn't injected or the table is empty —
    callers log loudly so the missing data is obvious.
    """
    try:
        from matrx_ai.db._registry import get_instance

        mgr = get_instance("tool_surface_defaults_manager_instance")
    except Exception:
        return []

    # The manager's filter/fetch surface is sync-safe inside the registry's
    # synchronous build path; we use the asyncpg-backed sync wrapper that
    # matrx-orm exposes on every BaseManager. If only the async API exists,
    # callers must wrap this in an event loop themselves.
    try:
        rows = mgr.filter_items_sync(surface_name=surface_name)
    except Exception:
        try:
            import asyncio

            rows = asyncio.run(mgr.filter_items(surface_name=surface_name))
        except Exception:
            return []

    if not rows:
        return []
    row = rows[0]
    raw = getattr(row, "always_include_tools", None) or []
    return sorted(str(n) for n in raw if n)


def get_category_names() -> list[str]:
    """Return sorted list of matrx-extend category names from the registry.

    Used by ``load_chrome_tools`` for error messages and input validation.
    Cached after the first call.
    """
    global _category_names_cache
    if _category_names_cache is not None:
        return _category_names_cache

    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    cats = {
        t.category
        for t in registry.list_tools()
        if t.category and _is_chrome_extension_tool(t)
    }
    if not cats:
        vcprint(
            "[browser-dom] WARNING: no chrome-extension categories found in registry. "
            "initialize_tool_system() may not have been called yet.",
            color="yellow",
        )
    _category_names_cache = sorted(cats)
    return _category_names_cache


def get_admin_only_categories() -> frozenset[str]:
    """Return the set of categories where EVERY tool requires admin access.

    Derived from the registry's ``admin_only`` field on ``ToolDefinition``
    rows. A category is admin-only when all tools in it are admin-gated.
    Used by ``load_chrome_tools`` to reject non-admin access at the
    category level before evaluating individual tools.
    Cached after the first call.
    """
    global _admin_only_categories_cache
    if _admin_only_categories_cache is not None:
        return _admin_only_categories_cache

    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    per_cat: dict[str, bool] = {}
    for t in registry.list_tools():
        if not t.category or not _is_chrome_extension_tool(t):
            continue
        cat = t.category
        if cat not in per_cat:
            per_cat[cat] = True
        if not t.admin_only:
            per_cat[cat] = False

    _admin_only_categories_cache = frozenset(cat for cat, all_admin in per_cat.items() if all_admin)
    return _admin_only_categories_cache


# ---------------------------------------------------------------------------
# Capability constant — registered by built_in.py at module load.
# ``enabled_tools`` is left empty; the factory is called at request time
# when the registry is guaranteed to be populated.
# ---------------------------------------------------------------------------

BROWSER_DOM = Capability(
    name="browser-dom",
    description=(
        "Caller is the matrx-extend Chrome extension. The active tab + auth "
        "+ desktop-bridge + permission state is carried in "
        "state['browser-dom']. The agent boots with the always-on browser "
        "tool kit (defined in tool_surface_defaults.always_include_tools "
        "for surface matrx-extend.browser) plus ``load_chrome_tools``; "
        "calling the discovery tool with a category loads the relevant "
        "additional tools on demand."
    ),
    payload_model=BrowserDomPayload,
    enabled_tools_factory=_build_auto_load_specs,
    # Guest mode (2026-05-18): the extension allows unauthenticated users to
    # chat against builtin agents (anonymous Supabase sign-in mints a real
    # auth.users row, so all FKs resolve). The browser-dom payload carries
    # ``is_guest`` so the server-side ``load_chrome_tools`` discovery
    # handler can still filter which categories/tools are exposed to guests
    # versus signed-in users versus admins — that gate moved one layer in.
    # The capability itself is open to everyone.
    requires_auth=False,
)
