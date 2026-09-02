"""``load_chrome_tools`` — discovery tool for the matrx-extend Chrome extension.

The Chrome extension carries many browser-control tools across categories.
Giving the model all of them up front would blow the context window and
degrade tool selection quality. Instead, the ``browser-dom`` capability
advertises just this one discovery tool. The model calls it with a category,
and the handler:

  1. Reads the active ``BrowserDomPayload`` off ``AppContext`` (auth,
     granted permissions, desktop-bridge availability).
  2. Looks up the tools in that category from ``ToolRegistry`` (the DB is
     the single source of truth — no JSON fallback).
  3. Filters out admin-only tools when the user isn't admin, optional-
     permission-gated tools when the user hasn't granted them, and
     ``desktop_run_command`` when the desktop bridge is unreachable.
  4. Queues a tool-set mutation via ``ctx.queue_tool_changes(...)`` —
     adds the filtered set, removes itself. The orchestrator drains the
     mutation between turns and the model's next API call sees the new
     toolset.

This is the canonical example of the discovery-tool pattern. Future
capability bundles that need to expose large tool catalogs can copy
this shape verbatim.
"""

from __future__ import annotations

import time
from typing import Any

from matrx_utils import vcprint

from matrx_ai.capabilities.browser_dom import (
    get_admin_only_categories,
    get_category_names,
)
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolError, ToolResult

_DESKTOP_GATED_TOOLS: frozenset[str] = frozenset({"desktop_run_command"})

# Legacy namespace prefix. matrx-extend tools used to be stored as
# "matrx-extend:<local>"; the registry moved to bare local names. Kept
# here only for ``removeprefix`` defensive handling of stale rows.
_NS_PREFIX = "matrx-extend:"
_CHROME_EXTENSION_EXECUTOR = "chrome-extension"


def _is_chrome_extension_tool(tool: ToolDefinition) -> bool:
    """True iff the tool has a binding to the ``chrome-extension`` executor
    (or any sub-executor under it). Replaces the legacy
    ``source_app == 'matrx-extend'`` check.
    """
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    bindings = registry.bindings_for_tool(tool.name)
    if not bindings:
        return False
    for b in bindings:
        if b == _CHROME_EXTENSION_EXECUTOR or b.startswith(f"{_CHROME_EXTENSION_EXECUTOR}."):
            return True
    return False


def _registry_routing_for_category(
    category: str,
) -> tuple[
    dict[str, dict[str, Any]],
    list[str],
]:
    """Return ``(per-tool metadata dict, ordered local-name list)`` for
    ``category`` from ``ToolRegistry``.

    The registry is the ONLY source of truth — there is no JSON fallback.
    If the registry has no chrome-extension-bound rows, this raises a loud
    runtime error because either ``initialize_tool_system()`` was not called
    or the database is empty, both of which are hard failures that must not
    be silently swallowed.

    Metadata shape: ``{local_name: {admin_only, required_optional_permissions}}``
    — same dict interface ``_filter_tools`` consumes.
    """
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    # Identify browser tools by binding to the chrome-extension executor,
    # NOT by a name prefix. (The registry stores tools under their bare
    # canonical name; ownership lives on tool_binding, not on a column.)
    candidates: list[ToolDefinition] = [
        t for t in registry.list_tools(category=category) if _is_chrome_extension_tool(t)
    ]

    if not candidates:
        # Distinguish "no tools in this category" from "registry empty entirely".
        all_chrome_ext = [t for t in registry.list_tools() if _is_chrome_extension_tool(t)]
        if not all_chrome_ext:
            vcprint(
                {
                    "category": category,
                    "registry_total": registry.count,
                    "hint": (
                        "initialize_tool_system() / initialize_tool_system_sync() "
                        "must be called before the first request. "
                        "Check that public.tool_def is seeded and that the "
                        "browser tools have tool_binding rows pointing at "
                        "executor 'chrome-extension'."
                    ),
                },
                "[load_chrome_tools] FATAL ERROR: ToolRegistry has ZERO "
                "chrome-extension-bound tools loaded. The registry was not "
                "populated before this request arrived. All browser tool "
                "discovery will fail until the registry is initialised.",
                color="red",
            )
            raise RuntimeError(
                "[load_chrome_tools] Registry has no chrome-extension-bound tools. "
                "Call initialize_tool_system() at startup before serving requests. "
                "Check that public.tool_def is seeded."
            )
        # Registry is populated but this category genuinely has no tools.
        return {}, []

    routing: list[str] = []
    metadata: dict[str, dict[str, Any]] = {}
    for tool in candidates:
        # removeprefix is a no-op for the current local names and still strips a
        # legacy 'matrx-extend:' prefix if one is ever present — never slice a
        # fixed width (that corrupts short local names like 'find').
        local_name = tool.name.removeprefix(_NS_PREFIX)
        routing.append(local_name)

        required_perms: list[str] = []
        admin_only = bool(tool.admin_only)
        for gate_spec in tool.gating or []:
            if not isinstance(gate_spec, dict):
                continue
            gate = gate_spec.get("gate")
            if gate == "is_admin":
                admin_only = True
            elif gate == "has_optional_permission":
                args = gate_spec.get("args") or {}
                perm = args.get("permission")
                if perm:
                    required_perms.append(perm)

        metadata[local_name] = {
            "tier": tool.tier,
            "category": tool.category,
            "admin_only": admin_only,
            "required_optional_permissions": required_perms,
        }

    return metadata, routing


def _read_browser_dom_state(ctx: ToolContext) -> dict[str, Any]:
    """Pull the ``browser-dom`` payload off the active AppContext."""
    from matrx_connect.context.app_context import try_get_app_context

    app_ctx = try_get_app_context()
    if app_ctx is None or not app_ctx.metadata:
        return {}

    canonical = app_ctx.metadata.get("client_capabilities_payloads")
    if isinstance(canonical, dict):
        payload = canonical.get("browser-dom")
        if isinstance(payload, dict):
            return payload

    direct = app_ctx.metadata.get("browser-dom")
    if isinstance(direct, dict):
        return direct

    return {}


def _categories_present_in_active_toolset(client_tools: list[str]) -> set[str]:
    """Project the active client-tool name list back to the set of
    matrx-extend categories at least one of those tools belongs to.

    Used by the consistency check: the extension's client-side
    ``loaded_categories`` list should be a subset of this set on every
    turn after the first load. When it isn't, something has drifted.
    """
    if not client_tools:
        return set()
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    active_set = set(client_tools)
    present: set[str] = set()
    for local_name in active_set:
        tool = registry.get(_NS_PREFIX + local_name) or registry.get(local_name)
        if tool and tool.category:
            present.add(tool.category)
    return present


def _warn_on_loaded_categories_drift(claimed_loaded: list[str]) -> None:
    """Log a WARNING if the extension's ``loaded_categories`` claim
    disagrees with what's actually in the active toolset for this request.

    Defensive observation only — does NOT reject the request.
    """
    from matrx_connect.context.app_context import try_get_app_context

    app_ctx = try_get_app_context()
    if app_ctx is None:
        return

    actual_categories = _categories_present_in_active_toolset(list(app_ctx.client_tools or []))
    actual_no_core = actual_categories - {"core"}
    claimed_no_core = {c for c in claimed_loaded if c != "core"}

    missing_in_active = sorted(claimed_no_core - actual_no_core)
    if missing_in_active:
        vcprint(
            f"[load_chrome_tools] WARNING: client claims "
            f"loaded_categories={sorted(claimed_no_core)!r} but server "
            f"projection has no tools for category(ies) "
            f"{missing_in_active!r} in active toolset (actual="
            f"{sorted(actual_no_core)!r}). Likely client/server drift; "
            f"servicing request anyway.",
            color="yellow",
        )


def _filter_tools(
    candidate_names: list[str],
    *,
    is_admin: bool,
    granted: frozenset[str],
    desktop_status: str,
    metadata_source: dict[str, dict[str, Any]],
) -> tuple[list[str], dict[str, list[str]]]:
    """Apply admin / permission / desktop-bridge filters.

    Returns ``(passed, skipped_by_reason)`` where ``skipped_by_reason`` is
    a structured dict so the model gets a clear "why" for each missing
    tool.

    ``metadata_source`` is required and must come from the registry. Passing
    an empty dict is valid (no tools) but passing None is a programming error.
    """
    passed: list[str] = []
    skipped_admin: list[str] = []
    skipped_missing_perm: list[str] = []
    skipped_desktop: list[str] = []

    for name in candidate_names:
        meta = metadata_source.get(name)
        if not meta:
            vcprint(
                {
                    "tool": name,
                    "hint": "Tool is in category routing but has no metadata entry. "
                    "This indicates a data integrity issue in tool_def/tool_binding.",
                },
                f"[load_chrome_tools] ERROR: tool {name!r} has no metadata — skipping. "
                "This should never happen when the registry is populated from the DB.",
                color="red",
            )
            continue

        if meta.get("admin_only") and not is_admin:
            skipped_admin.append(name)
            continue

        required = meta.get("required_optional_permissions") or []
        if required:
            required_set = frozenset(required)
            if not required_set.issubset(granted):
                skipped_missing_perm.append(name)
                continue

        if name in _DESKTOP_GATED_TOOLS and desktop_status == "none":
            skipped_desktop.append(name)
            continue

        passed.append(name)

    return passed, {
        "skipped_admin_only": skipped_admin,
        "skipped_missing_permission": skipped_missing_perm,
        "skipped_desktop_unavailable": skipped_desktop,
    }


def _chrome_extension_executor_live(ctx: ToolContext) -> tuple[bool, list[str]]:
    """True iff this request's resolved active client-executor set includes
    the ``chrome-extension`` executor (or any dot-descendant). Returns the
    active set too, for error messages.

    This is the canonical routing authority resolved once at the request
    edge (``ACTIVE_TOOL_EXECUTORS_KEY``) — the same input
    ``merge_request_tools`` uses for delegation. When the extension is not
    among the live executors, every tool this discovery tool would load is
    physically unrunnable (they only execute inside the matrx-extend
    Chrome extension), so the load must refuse instead of queueing tools
    that would delegate to a client that can never answer.
    """
    from matrx_connect.context.app_context import try_get_app_context

    from matrx_ai.tools.merge import active_tool_executors

    active = active_tool_executors(try_get_app_context())
    live = any(
        k == _CHROME_EXTENSION_EXECUTOR or k.startswith(f"{_CHROME_EXTENSION_EXECUTOR}.")
        for k in active
    )
    return live, sorted(active)


async def load_chrome_tools(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Load the relevant subset of Chrome-extension tools for ``category``.

    Always succeeds at the protocol level (returns ToolResult with
    ``success`` flag) so the model can read the routing decision instead
    of seeing an exception. Failure modes:

      - No Chrome-extension client on this request → success=False; the
        tools this loads cannot run anywhere else, so nothing is queued.
      - Unknown category → success=False with the valid category list.
      - Admin-only category for a non-admin user → success=False naming
        the permission gap.
      - All candidates filtered out → success=True with empty
        ``tools_loaded`` and explanatory ``skipped_*`` lists; the model
        can decide whether to ask the user or try a different category.
    """
    from matrx_ai.tools._generated_declarations import LoadChromeToolsArgs

    LoadChromeToolsArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    started = time.time()

    extension_live, active_kinds = _chrome_extension_executor_live(ctx)
    if not extension_live:
        # Remove the loader so the model doesn't keep retrying a tool that
        # can never work on this surface.
        ctx.queue_tool_changes(add=[], remove=["load_chrome_tools"])
        vcprint(
            f"[load_chrome_tools] REFUSED — no chrome-extension client on this "
            f"request (active client executors: {active_kinds or '[]'}). The "
            f"tools this loader provides run ONLY inside the matrx-extend "
            f"Chrome extension; loading them here would delegate calls to a "
            f"client that can never answer (the 2026-08-21 stuck-'delegated' "
            f"incident). Loader removed from the active toolset.",
            color="red",
        )
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="client_unavailable",
                message=(
                    "The browser tools this loads run inside the Matrx Chrome "
                    "extension, and no Chrome-extension client is connected to "
                    "this conversation. They cannot run on this surface."
                ),
                suggested_action=(
                    "Do not retry this tool here. If server-side browsing tools "
                    "(the action-dispatched cloud_browser tool) are in your toolset, "
                    "use those; otherwise tell the user this conversation's "
                    "surface has no browser control."
                ),
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name="load_chrome_tools",
            call_id=ctx.call_id,
        )

    category = (args.get("category") or "").strip()
    category_names = get_category_names()

    if not category:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="invalid_argument",
                message="category is required",
                suggested_action=(f"Choose one of: {', '.join(category_names)}"),
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name="load_chrome_tools",
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
                suggested_action=(f"Valid categories: {', '.join(category_names)}"),
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name="load_chrome_tools",
            call_id=ctx.call_id,
        )

    state = _read_browser_dom_state(ctx)
    is_admin = bool(state.get("is_admin", False))
    granted = frozenset(state.get("optional_permissions_granted") or [])
    desktop_status: str = state.get("desktop_bridge", "none")
    loaded_categories: list[str] = list(state.get("loaded_categories") or [])

    if loaded_categories:
        _warn_on_loaded_categories_drift(loaded_categories)

    if category in loaded_categories:
        ctx.queue_tool_changes(add=[], remove=["load_chrome_tools"])
        vcprint(
            f"[load_chrome_tools] category={category!r} already in "
            f"client.state['browser-dom'].loaded_categories — short-circuit "
            f"(no re-load).",
            color="cyan",
        )
        from matrx_ai.tools.kinds.tool_loading import ChromeToolsLoadResult

        return ToolResult(
            success=True,
            output=ChromeToolsLoadResult(
                category=category,
                already_loaded=True,
                message=(
                    f"Category {category!r} is already loaded — see existing "
                    f"tools in the active toolset; no new tools queued."
                ),
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name="load_chrome_tools",
            call_id=ctx.call_id,
        )

    admin_only_cats = get_admin_only_categories()
    if category in admin_only_cats and not is_admin:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="forbidden",
                message=(
                    f"Category {category!r} is admin-only and the current user is not an admin."
                ),
                suggested_action=(
                    "Pick a non-admin category or ask the user to authenticate as an administrator."
                ),
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name="load_chrome_tools",
            call_id=ctx.call_id,
        )

    # Registry is the only source of truth — no JSON fallback.
    # _registry_routing_for_category raises loudly if the registry has no
    # matrx-extend tools at all (startup misconfiguration).
    metadata_source, candidates = _registry_routing_for_category(category)

    passed, skipped = _filter_tools(
        candidates,
        is_admin=is_admin,
        granted=granted,
        desktop_status=desktop_status,
        metadata_source=metadata_source,
    )

    # Queue REGISTERED references, never inline copies (mirrors
    # load_desktop_tools). A registered spec keeps its tool_binding rows, so
    # the merge primitive's single routing authority
    # (resolve_executor_binding × active executors) decides delegation —
    # republishing these as InlineToolSpec stripped the bindings and let
    # them delegate to clients that could never answer. Registered adds also
    # persist through UnifiedConfig.dynamic_tools, so a resumed conversation
    # rebuilds the loaded set instead of silently losing it.
    from matrx_ai.tools.registry import ToolRegistry
    from matrx_ai.tools.specs import RegisteredToolSpec

    registry = ToolRegistry.get_instance()
    loaded_specs: list[RegisteredToolSpec] = []
    missing_from_catalog: list[str] = []
    for name in passed:
        tool = registry.get(name) or registry.get(_NS_PREFIX + name)
        if tool is None:
            missing_from_catalog.append(name)
            vcprint(
                {
                    "tool": name,
                    "category": category,
                    "hint": "Tool is in tool_binding category routing but has no "
                    "corresponding tool_def row bound to executor 'chrome-extension'. "
                    "This is a data integrity error in the database.",
                },
                f"[load_chrome_tools] ERROR: tool {name!r} passed filters but "
                "has no registry entry — it will NOT be loaded. "
                "The model will never see this tool.",
                color="red",
            )
            continue
        loaded_specs.append(RegisteredToolSpec(name=tool.name))

    ctx.queue_tool_changes(
        add=loaded_specs,
        remove=["load_chrome_tools"],
    )

    vcprint(
        f"[load_chrome_tools] category={category} "
        f"source=registry "
        f"loaded={len(loaded_specs)}/{len(candidates)} "
        f"is_admin={is_admin} desktop={desktop_status} "
        f"granted={sorted(granted) if granted else '[]'} "
        f"missing_from_catalog={missing_from_catalog or '[]'}",
        color="cyan",
    )

    from matrx_ai.tools.kinds.tool_loading import ChromeToolsLoadResult

    return ToolResult(
        success=True,
        output=ChromeToolsLoadResult(
            category=category,
            tools_loaded=[s.name for s in loaded_specs],
            count=len(loaded_specs),
            missing_from_catalog=missing_from_catalog,
            **skipped,
        ),
        started_at=started,
        completed_at=time.time(),
        tool_name="load_chrome_tools",
        call_id=ctx.call_id,
    )
