"""``load_desktop_tools`` — discovery tool for the matrx-local desktop (W7).

Copied from the canonical discovery-tool pattern in
``browser_discovery.py`` (per its own docstring instruction), adapted for
the ``matrx-local`` executor and the desktop mega-tool taxonomy.

The desktop's tool surface is 19 action-enum mega-tools (``local_file``,
``local_shell``, …) grouped into 2 categories: ``desktop`` (machine
control — files, shell, windows, input, media, OS apps) and
``desktop-web`` (internet access from the machine — browser, web,
network). Consolidated from the original 9-way ``desktop-*`` split on
2026-07-17; names are read live from the DB, so this list is
documentation, not code.
The model calls this tool with a category and the handler:

  1. Reads the active ``DesktopNativePayload`` off ``AppContext``
     (platform, loaded categories).
  2. Looks up the mega-tools in that category from ``ToolRegistry``
     (DB is the single source of truth).
  3. Filters OS-gated tools against the desktop's reported platform
     (``local_mac_apps`` needs darwin, ``local_windows_ps`` needs win32).
  4. Queues registry references via ``ctx.queue_tool_changes(...)`` and removes
     itself. The canonical merge resolves schema identity and request routing
     from registry bindings × the host-resolved active executor set.

On AIDream the loaded mega-tools are CLIENT tools, so their calls take the
client-delegation (suspend/resume) path and execute on the user's machine. In
Matrx Local the same process owns registered handlers for those tools, so they
stay registered and execute through the host's ``ExternalToolAdapter``.
"""

from __future__ import annotations

import time
from typing import Any

from matrx_utils import vcprint

from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolError, ToolResult
from matrx_ai.tools.specs import RegisteredToolSpec, ToolSpec

MATRX_LOCAL_EXECUTOR = "matrx-local"

# Mega-tools that only exist on one OS. The desktop reports its platform in
# state['desktop-native'].platform; mismatches are filtered with a reason.
_PLATFORM_GATED_TOOLS: dict[str, str] = {
    "local_mac_apps": "darwin",
    "local_windows_ps": "win32",
}

_category_names_cache: list[str] | None = None


def clear_caches() -> None:
    """Invalidate the lazy category cache (admin cache-bust after a
    migration edits the tool tables)."""
    global _category_names_cache
    _category_names_cache = None


def _is_matrx_local_tool(tool: ToolDefinition) -> bool:
    """True iff the tool has a binding to the ``matrx-local`` executor (or
    any sub-executor under it).

    Offline client hosts synthesize their bundled definitions with the
    explicit ``matrx_local`` source kind and have no server binding rows. That
    host-owned source marker is the authoritative fallback in that mode.
    """
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    bindings = registry.bindings_for_tool(tool.name)
    if not bindings:
        return tool.source_kind in {"matrx_local", "matrx-local"}
    for b in bindings:
        if b == MATRX_LOCAL_EXECUTOR or b.startswith(f"{MATRX_LOCAL_EXECUTOR}."):
            return True
    return False


def get_category_names() -> list[str]:
    """Sorted list of desktop categories from the registry (cached)."""
    global _category_names_cache
    if _category_names_cache is not None:
        return _category_names_cache

    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    cats = {t.category for t in registry.list_tools() if t.category and _is_matrx_local_tool(t)}
    if not cats:
        vcprint(
            "[load_desktop_tools] WARNING: no matrx-local categories found in "
            "registry. initialize_tool_system() may not have been called yet, "
            "or tool.binding has no matrx-local rows.",
            color="yellow",
        )
    _category_names_cache = sorted(cats)
    return _category_names_cache


def _registry_tools_for_category(category: str) -> list[ToolDefinition]:
    """The matrx-local-bound tools in ``category`` from ``ToolRegistry``.

    Raises loudly when the registry has NO matrx-local tools at all (startup
    misconfiguration); returns ``[]`` when the registry is populated but the
    category is genuinely empty.
    """
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    candidates = [t for t in registry.list_tools(category=category) if _is_matrx_local_tool(t)]
    if not candidates:
        all_local = [t for t in registry.list_tools() if _is_matrx_local_tool(t)]
        if not all_local:
            vcprint(
                {
                    "category": category,
                    "registry_total": registry.count,
                    "hint": (
                        "initialize_tool_system() must run before the first "
                        "request, and tool.binding must have active rows for "
                        "executor 'matrx-local' (the 19 mega-tools)."
                    ),
                },
                "[load_desktop_tools] FATAL ERROR: ToolRegistry has ZERO "
                "matrx-local-bound tools loaded.",
                color="red",
            )
            raise RuntimeError(
                "[load_desktop_tools] Registry has no matrx-local-bound tools. "
                "Call initialize_tool_system() at startup; check tool.binding "
                "rows for executor 'matrx-local'."
            )
    return candidates


def _discovered_spec(tool: ToolDefinition) -> ToolSpec:
    """Reference the registry definition; routing is resolved during merge."""
    return RegisteredToolSpec(name=tool.name)


def _read_desktop_state(ctx: ToolContext) -> dict[str, Any]:
    """Pull the ``desktop-native`` payload off the active AppContext."""
    from matrx_connect.context.app_context import try_get_app_context

    app_ctx = try_get_app_context()
    if app_ctx is None or not app_ctx.metadata:
        return {}

    canonical = app_ctx.metadata.get("client_capabilities_payloads")
    if isinstance(canonical, dict):
        payload = canonical.get("desktop-native")
        if isinstance(payload, dict):
            return payload

    direct = app_ctx.metadata.get("desktop-native")
    if isinstance(direct, dict):
        return direct

    return {}


def _hard_excluded_tool_names() -> frozenset[str]:
    from matrx_connect.context.app_context import try_get_app_context

    from matrx_ai.tools.merge import hard_excluded_tool_names

    return hard_excluded_tool_names(try_get_app_context())


async def load_desktop_tools(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Load the desktop mega-tools for ``category`` into the active toolset.

    Always succeeds at the protocol level (returns ToolResult with a
    ``success`` flag) so the model can read the routing decision. Failure
    modes: unknown category → the valid list; everything filtered →
    success=True with explanatory ``skipped_*`` lists.
    """
    from matrx_ai.tools._generated_declarations import LoadDesktopToolsArgs

    LoadDesktopToolsArgs.model_validate(args)
    started = time.time()

    category = (args.get("category") or "").strip()
    category_names = get_category_names()

    if not category:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="invalid_argument",
                message="category is required",
                suggested_action=f"Choose one of: {', '.join(category_names)}",
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name="load_desktop_tools",
            call_id=ctx.call_id,
        )

    if category not in category_names:
        from matrx_utils.suggest import suggestion_line

        hint = suggestion_line(category, category_names, noun="category")
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="unknown_category",
                message=f"Unknown category {category!r}." + (f" {hint}" if hint else ""),
                suggested_action=f"Valid categories: {', '.join(category_names)}",
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name="load_desktop_tools",
            call_id=ctx.call_id,
        )

    state = _read_desktop_state(ctx)
    platform: str = str(state.get("platform") or "")
    loaded_categories: list[str] = list(state.get("loaded_categories") or [])

    if category in loaded_categories:
        ctx.queue_tool_changes(add=[], remove=["load_desktop_tools"])
        vcprint(
            f"[load_desktop_tools] category={category!r} already in "
            "state['desktop-native'].loaded_categories — short-circuit.",
            color="cyan",
        )
        from matrx_ai.tools.kinds.tool_loading import DesktopToolsLoadResult

        return ToolResult(
            success=True,
            output=DesktopToolsLoadResult(
                category=category,
                already_loaded=True,
                message=(
                    f"Category {category!r} is already loaded — see existing "
                    "tools in the active toolset; no new tools queued."
                ),
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name="load_desktop_tools",
            call_id=ctx.call_id,
        )

    candidates = _registry_tools_for_category(category)

    discovered_specs: list[ToolSpec] = []
    skipped_platform: list[str] = []
    skipped_policy: list[str] = []
    hard_excluded_tools = _hard_excluded_tool_names()
    for tool in sorted(candidates, key=lambda t: t.name):
        # Host authority policy is absolute. Filter here so the tool result
        # truthfully reports what discovery queued; merge_request_tools applies
        # the same policy again during the drain as an independent backstop.
        if tool.name in hard_excluded_tools:
            skipped_policy.append(tool.name)
            continue
        needed = _PLATFORM_GATED_TOOLS.get(tool.name)
        if needed and platform and platform != needed:
            skipped_platform.append(tool.name)
            continue
        discovered_specs.append(_discovered_spec(tool))

    ctx.queue_tool_changes(
        add=discovered_specs,
        remove=["load_desktop_tools"],
    )

    vcprint(
        f"[load_desktop_tools] category={category} "
        f"queued={len(discovered_specs)}/{len(candidates)} "
        f"platform={platform or 'unknown'} "
        f"skipped_policy={skipped_policy or '[]'} "
        f"skipped_platform={skipped_platform or '[]'}",
        color="cyan",
    )

    from matrx_ai.tools.kinds.tool_loading import DesktopToolsLoadResult

    return ToolResult(
        success=True,
        output=DesktopToolsLoadResult(
            category=category,
            # This handler runs before the turn-boundary drain. These names are
            # queued intent, not claimed additions; the drain's RESOURCE_CHANGED
            # event reports the final applied/deduplicated delta.
            tools_queued=[s.name for s in discovered_specs],
            queued_count=len(discovered_specs),
            skipped_policy=skipped_policy,
            skipped_platform=skipped_platform,
        ),
        started_at=started,
        completed_at=time.time(),
        tool_name="load_desktop_tools",
        call_id=ctx.call_id,
    )
