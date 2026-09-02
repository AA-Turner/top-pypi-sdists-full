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
    # within discovery_ttl_seconds).
    server_slug = (bundle.get("metadata") or {}).get("server_slug")
    if server_slug:
        try:
            from matrx_ai.tools.mcp_sync import sync_server

            await sync_server(server_slug, force=False)
        except Exception as exc:
            # Log but don't abort — fall through to read whatever members
            # are already cached. Better to expose stale tools than nothing.
            vcprint(
                f"[bundle_lister] sync_server({server_slug}) failed: {exc!r} "
                f"— serving cached members",
                color="yellow",
            )

    # Resolve bundle members through the RPC.
    members = await _resolve_bundle_members(bundle_name)

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
