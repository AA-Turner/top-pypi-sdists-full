"""Generic bundle-lister handler.

A single Python implementation that every ``bundle:list_<name>`` tool row
points at. Resolution flow:

  1. The handler is invoked with no args.
  2. Reads ``ctx.tool_name`` to identify which lister fired (e.g.
     ``bundle:list_supabase``).
  3. Looks up the matching ``tool_bundle`` row → bundle id + metadata.
  4. If the bundle is an auto-managed MCP bundle (``metadata.server_slug``
     is set) and the cached members are stale or missing, fires a
     ``mcp_sync.sync_server(slug)`` call (cache-aware; usually a no-op).
  5. Resolves the bundle members through the
     ``tool_resolve_bundle(p_bundle_name)`` RPC → list of ``tool_def``
     rows for the bundle's members.
  6. For each member, fetches the canonical ``ToolDefinition`` from the
     registry. Builds a ``RegisteredToolSpec`` for server-runnable tools
     or ``InlineToolSpec`` for client-delegated ones (heuristic: tool_type
     ``EXTERNAL_HANDLER`` → inline, else registered).
  7. Writes **identity** alias-map entries (``{canonical: canonical}``)
     into ``AppContext.metadata['tool_aliases']`` so dispatch lookups stay
     uniform with every other load path.
  8. Calls ``ctx.queue_tool_changes(add=specs, remove=[ctx.tool_name])`` —
     the lister removes itself once it's done loading.

Members are exposed under their **canonical names**, not rebranded to
``<bundle>:<local_alias>``. The rebranding half of Decision 26
(TOOL_REGISTRY_REDESIGN.md) was never load-bearing and is structurally
incompatible with the merge primitive: ``merge_request_tools`` keys
registered specs by registry UUID and stores canonical names in
``config.tools``, so a rebranded name was silently discarded before the
model ever saw it — while a rebranded ``InlineToolSpec`` (colon in the
name) crashed ``CustomTool`` validation outright. Canonical names go out
provider-safe via the wire-name seam (``matrx_ai.config.wire_names``).
If per-bundle rebranding is ever truly needed, it must be built through
the merge primitive, not around it.

The handler is generic over every bundle. Per-bundle behavior is data-
driven through ``tool_bundle.metadata``.
"""

from __future__ import annotations

import time
from typing import Any

from matrx_utils import vcprint

from matrx_ai.tools.declared import NoArgs, tool_family
from matrx_ai.tools.kinds.tooling import ToolBundleListing
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.specs import InlineToolSpec, RegisteredToolSpec


@tool_family(
    name_prefix="bundle:list_",
    source_kind="native",
    executor="matrx-ai-core",
    args=NoArgs,
)
async def list_bundle_tools(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Generic discovery handler for any ``bundle:list_<name>`` lister.

    Reads ``ctx.tool_name`` to identify the calling lister, fetches the
    bundle's members through the ``tool_resolve_bundle`` RPC, queues them
    as the new active toolset, and removes itself.
    """
    started = time.time()
    lister_name = ctx.tool_name or ""

    # ``ctx.tool_name`` is the lister's canonical name. By convention,
    # it's ``bundle:list_<bundle_name>``. Extract the bundle name.
    if not lister_name.startswith("bundle:list_"):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="invalid_lister",
                message=(
                    f"list_bundle_tools invoked from a non-lister tool "
                    f"{lister_name!r}. Listers must follow the "
                    f"'bundle:list_<name>' naming convention."
                ),
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name=lister_name,
            call_id=ctx.call_id,
        )

    bundle_name = lister_name[len("bundle:list_") :]

    # Look up the bundle row (id + metadata).
    bundle = await _fetch_bundle_by_name(bundle_name)
    if bundle is None:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="bundle_not_found",
                message=(
                    f"No bundle named {bundle_name!r} in tool_bundle. The "
                    f"lister tool {lister_name!r} is registered but its "
                    f"backing bundle is missing — likely a stale tool row "
                    f"after a bundle was deleted."
                ),
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name=lister_name,
            call_id=ctx.call_id,
        )

    # If this is an MCP-auto-managed bundle, ensure the catalog is fresh
    # (cache-aware; sync_server short-circuits when last_synced_at is
    # within discovery_ttl_seconds). Discovery runs with the CALLING USER's
    # connection auth when the host injected ``mcp_auth_resolver`` — a server
    # whose auth_strategy is not ``none`` (GitHub) answers 401 to an anonymous
    # ``tools/list``, so without this its catalog could never populate.
    server_slug = (bundle.get("metadata") or {}).get("server_slug")
    sync_error: str | None = None
    if server_slug:
        try:
            from matrx_ai.tools.mcp_sync import sync_server

            discovery_auth = await _resolve_user_discovery_auth(server_slug, ctx)
            sync_result = await sync_server(
                server_slug, force=False, discovery_auth=discovery_auth
            )
            sync_error = sync_result.error
        except Exception as exc:
            # Log but don't abort — fall through to read whatever members
            # are already cached. Better to expose stale tools than nothing.
            sync_error = repr(exc)
            vcprint(
                f"[bundle_lister] sync_server({server_slug}) failed: {exc!r} "
                f"— serving cached members",
                color="yellow",
            )

    # Resolve bundle members. An MCP-managed bundle's members are the server's
    # live ``tool.definition`` rows (``managed_by_server_id``) — the catalog
    # sync maintains those rows and writes no ``platform.associations``
    # membership edge, so the edge walk below found 0 members for EVERY MCP
    # bundle (2026-09-13 census: 0 edges across all synced servers).
    if server_slug:
        members = await _resolve_mcp_bundle_members(server_slug)
    else:
        members = await _resolve_bundle_members(bundle_name)

    if server_slug and not members:
        # Nothing to load — say so, with the reason, instead of returning a
        # successful empty listing the model cannot act on.
        reason = sync_error or (
            f"the {server_slug!r} MCP server exposes no tools for this connection"
        )
        vcprint(
            f"[bundle_lister] bundle={bundle_name} server_slug={server_slug} "
            f"produced NO tools: {reason}",
            color="red",
        )
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="mcp_no_tools",
                message=(
                    f"The {server_slug} MCP is attached but produced no tools: {reason}. "
                    "Tell the user; do not retry this lister."
                ),
            ),
            started_at=started,
            completed_at=time.time(),
            tool_name=lister_name,
            call_id=ctx.call_id,
        )

    # Resolve each member to a ToolSpec. Members load under their CANONICAL
    # names (see the module docstring for why the <bundle>:<alias> rebranding
    # was removed); the alias map gets identity entries so dispatch lookups
    # stay uniform with every other load path.
    from matrx_ai.tools.tool_aliases import add_identity_aliases

    add_specs: list = []
    skipped_unresolved: list[str] = []

    for canonical_name, _local_alias in members:
        spec = _build_spec_for(canonical_name)
        if spec is None:
            skipped_unresolved.append(canonical_name)
            continue
        add_specs.append(spec)

    # Write the identity alias entries to the active AppContext.
    from matrx_connect.context.app_context import try_get_app_context

    app_ctx = try_get_app_context()
    if app_ctx is not None:
        add_identity_aliases(app_ctx, [s.name for s in add_specs])

    # Queue the load (and remove self).
    ctx.queue_tool_changes(add=add_specs, remove=[lister_name])

    vcprint(
        f"[bundle_lister] bundle={bundle_name} "
        f"loaded={len(add_specs)}/{len(members)} "
        f"skipped_unresolved={skipped_unresolved or '[]'} "
        f"server_slug={server_slug or '-'}",
        color="cyan",
    )

    return ToolResult(
        success=True,
        # The result declares its own kind (KINDS_EVERYWHERE_PLAN §10d-C): the
        # executor reads ``__kind`` off the payload and verifies it against the
        # live catalog, so this one shape is typed and routable for all 43
        # ``bundle:list_*`` listers this handler serves.
        output=ToolBundleListing(
            bundle=bundle_name,
            tools_loaded=[s.name for s in add_specs],
            count=len(add_specs),
            skipped_unresolved=skipped_unresolved,
            server_slug=server_slug,
        ).model_dump(mode="json"),
        started_at=started,
        completed_at=time.time(),
        tool_name=lister_name,
        call_id=ctx.call_id,
    )


# ---------------------------------------------------------------------------
# DB read helpers — host-injected ORM managers + RPC primitives.
# ---------------------------------------------------------------------------


async def _fetch_bundle_by_name(name: str) -> dict[str, Any] | None:
    """Fetch a single ``tool_bundle`` row by name via the host-injected
    manager. Returns the row as a dict or None.
    """
    try:
        from matrx_ai.db._registry import get_instance

        mgr = get_instance("tool_bundle_manager_instance")
    except Exception:
        return None
    try:
        rows = await mgr.filter_items(name=name, is_active=True)
    except Exception as exc:
        vcprint(
            f"[bundle_lister] tool_bundle fetch for {name!r} failed: {exc!r}",
            color="red",
        )
        return None
    if not rows:
        return None
    item = rows[0]
    return item.to_dict() if hasattr(item, "to_dict") else dict(item)


async def _resolve_user_discovery_auth(server_slug: str, ctx: ToolContext) -> dict[str, Any] | None:
    """The calling user's connection auth for ``server_slug`` via the host's
    ``mcp_auth_resolver`` seam (``async (slug, user_id) -> dict | None``), or
    ``None`` when the host injected no resolver / the user has no connection.
    Never stored; used for this discovery call only."""
    from matrx_ai._ext import get_ext, has_ext

    if not has_ext("mcp_auth_resolver"):
        return None
    try:
        user_id = ctx.user_id
    except Exception:  # noqa: BLE001 — no app context bound (headless call)
        return None
    if not user_id:
        return None
    try:
        return await get_ext("mcp_auth_resolver")(server_slug, user_id)
    except Exception as exc:  # noqa: BLE001 — discovery falls back to server-level auth
        vcprint(
            f"[bundle_lister] mcp_auth_resolver({server_slug!r}) failed: {exc!r} "
            "— discovering with server-level auth",
            color="yellow",
        )
        return None


async def _resolve_mcp_bundle_members(server_slug: str) -> list[tuple[str, str]]:
    """Members of an MCP-managed bundle: every active ``tool.definition`` row
    whose ``managed_by_server_id`` is the server's id, as
    ``[(canonical_name, local_alias), ...]``. Reloads the in-memory registry
    when a freshly synced row is not in it yet (first sync of a server
    inside a live request)."""
    from matrx_ai.tools.registry import ToolRegistry

    try:
        from matrx_ai.db._registry import get_instance, get_model

        server_mgr = get_instance("tool_mcp_server_manager_instance")
        definition_model = get_model("ToolDefinition")
    except Exception as exc:  # noqa: BLE001 — host did not inject the tool tables
        vcprint(
            f"[bundle_lister] MCP member resolution unavailable for {server_slug!r}: {exc!r}",
            color="red",
        )
        return []
    servers = await server_mgr.filter_items(slug=server_slug)
    if not servers:
        return []
    server_id = str(servers[0].id)
    rows = await definition_model.filter(managed_by_server_id=server_id, is_active=True).all()
    names = sorted(str(row.name) for row in rows)
    if not names:
        return []
    registry = ToolRegistry.get_instance()
    if any(registry.get(name) is None for name in names):
        await registry.reload_from_database()
    prefix = f"mcp.{server_slug}."
    return [(name, name[len(prefix):] if name.startswith(prefix) else name) for name in names]


async def _resolve_bundle_members(bundle_name: str) -> list[tuple[str, str]]:
    """Returns ``[(canonical_name, local_alias), ...]`` for every member
    of the given bundle, via the ``tool_resolve_bundle(p_bundle_name)``
    RPC. The RPC returns ``SETOF tool_def`` rows; we additionally read
    the bundle's member edges (the old ``tool`` schema ``bundle_member`` table,
    retired to graveyard — membership now lives in ``platform.associations``:
    ``source_type='tool' -> target_type='tool_bundle', role='member'``) to
    recover ``local_alias`` (the RPC doesn't carry it in the tool_def
    projection). ``local_alias`` now rides the edge's ``metadata`` and the
    display order rides ``position`` (was the ``sort_order`` column).
    """
    try:
        from matrx_ai.db._registry import get_instance

        assoc_mgr = get_instance("associations_manager_instance")
        bundle_mgr = get_instance("tool_bundle_manager_instance")
    except Exception:
        return []

    bundle_rows = await bundle_mgr.filter_items(name=bundle_name, is_active=True)
    if not bundle_rows:
        return []
    bundle_id = bundle_rows[0].id

    try:
        member_rows = await assoc_mgr.filter_items(
            source_type="tool",
            target_type="tool_bundle",
            target_id=bundle_id,
            role="member",
        )
    except Exception as exc:
        vcprint(
            f"[bundle_lister] tool_bundle_member (platform.associations) fetch for "
            f"{bundle_name!r} failed: {exc!r}",
            color="red",
        )
        return []

    if not member_rows:
        return []

    # We need to map tool_id → canonical_name. Use the in-memory registry's
    # reverse map; failing that, fall back to a direct lookup via the
    # tool_def manager.
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    out: list[tuple[str, str]] = []
    for m in sorted(
        member_rows,
        key=lambda r: (
            getattr(r, "position", 0) or 0,
            (getattr(r, "metadata", None) or {}).get("local_alias", ""),
        ),
    ):
        tool_id = str(m.source_id)
        canonical = registry._tools_by_id.get(tool_id)
        if canonical is None:
            # The registry hasn't loaded yet, or this row is for an inactive
            # tool. Skip — the lister logs the unresolved tool to the caller.
            continue
        local_alias = (getattr(m, "metadata", None) or {}).get("local_alias") or canonical
        out.append((canonical, local_alias))
    return out


def _build_spec_for(canonical_name: str):
    """Construct the right ToolSpec kind for a canonical tool name.

    ``EXTERNAL_HANDLER`` (client-delegated) tools become ``InlineToolSpec``
    so the merge primitive routes them to client_tools. Everything else
    becomes ``RegisteredToolSpec`` — the executor dispatches via the
    registry.
    """
    from matrx_ai.tools.models import ToolType
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    tool = registry.get(canonical_name)
    if tool is None:
        return None

    if tool.tool_type == ToolType.EXTERNAL_HANDLER:
        # Build an inline spec so the model sees the schema at request time
        # and the merge primitive treats it as client-delegated.
        return InlineToolSpec(
            name=canonical_name,
            description=tool.description or canonical_name,
            input_schema=_params_to_input_schema(tool.parameters or {}),
        )
    return RegisteredToolSpec(name=canonical_name, tool_id=tool.tool_id)


def _params_to_input_schema(params: dict[str, Any]) -> dict[str, Any]:
    """Inverse of the seed scripts' parameter packing — reconstruct a
    JSON Schema ``{type: object, properties, required}`` from the flat
    ``ToolDefinition.parameters`` shape."""
    properties: dict[str, Any] = {}
    required: list[str] = []
    for prop_name, prop_schema in params.items():
        if isinstance(prop_schema, dict):
            cleaned = {k: v for k, v in prop_schema.items() if k != "required"}
            properties[prop_name] = cleaned
            if prop_schema.get("required"):
                required.append(prop_name)
        else:
            properties[prop_name] = {"type": prop_schema}
    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }
