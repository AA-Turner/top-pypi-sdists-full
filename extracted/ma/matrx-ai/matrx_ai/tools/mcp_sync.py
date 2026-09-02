"""MCP server tool catalog sync.

The single function every trigger funnels through:

  - **Bundle-load discovery** (Option 1): ``bundle:list_<slug>`` lister
    fires → calls ``sync_server(slug)`` cache-first → reads members.
  - **Direct tool inclusion** (Option 2): merge primitive sees a tool name
    ``mcp.<slug>.<remote>`` that isn't in ``tool_def`` → triggers
    ``sync_server(slug)`` inline.
  - **Bundle membership** (Option 3): same as Option 2 from the merge
    primitive's POV.
  - **Admin add**: when a ``tool_mcp_server`` row is inserted, the admin
    handler fires ``asyncio.create_task(sync_server(slug))``.
  - **Background sweep**: ``ToolLifecycleManager.start_background_sweep()``
    walks every active server every N hours.
  - **Manual refresh**: admin endpoint calls ``sync_server(slug,
    force=True)``.

Stale-while-revalidate caching: serve from the DB even when stale, queue
a background refresh. **Never block on a remote call when usable cache
exists**, except when ``force=True``.

The DB rows in ``public.tool_def`` are the cache. Freshness is tracked
on ``tool_mcp_server.last_synced_at`` with per-server TTL via
``discovery_ttl_seconds``.

This module is the matrx-ai-package surface for MCP sync. Hosts use it
via the standard injection pattern — no aidream references here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from matrx_utils import vcprint

from matrx_ai.tools.external_mcp import ExternalMCPClient

#: Transports ``ExternalMCPClient`` actually speaks. Legacy SSE still has no
#: client implementation and is rejected loudly instead of failing opaquely.
SUPPORTED_TRANSPORTS = frozenset({"http", "streamable_http", "streamable-http", "stdio"})


@dataclass
class SyncResult:
    """Return value from ``sync_server``. Counts and per-tool deltas for
    the caller to log / surface in admin UIs."""

    slug: str
    cache_hit: bool = False
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: int = 0

    inserted: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    deactivated: list[str] = field(default_factory=list)
    error: str | None = None
    upstream_status: int | None = None


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


async def sync_server(slug: str, *, force: bool = False) -> SyncResult:
    """Sync a single MCP server's tool catalog into ``public.tool_def`` +
    ``tool_binding``.

    Parameters
    ----------
    slug:
        Server slug (PK on ``tool_mcp_server``).
    force:
        Bypass the cache freshness check. Used by the manual-refresh
        admin endpoint.

    Behavior:
      1. Read the server row (URL, transport, auth_strategy, last_synced_at,
         discovery_ttl_seconds, id).
      2. If cache is fresh (``now() - last_synced_at < discovery_ttl_seconds``)
         and not ``force``, return early with ``cache_hit=True``.
      3. Call ``ExternalMCPClient.discover_tools(server_url)`` →
         ``[ToolDefinition, ...]`` shaped for our internal model (but with
         bare local names).
      4. Hand the discovered spec list to the ``tool_register_mcp_discovered``
         RPC, which atomically:
            - UPSERTs a row in ``public.tool_def`` with canonical name
              ``mcp.<slug>.<local>``, ``source_kind='mcp_discovered'``,
              ``managed_by_server_id=<server.id>``.
            - UPSERTs a ``public.tool_binding`` row to executor
              ``mcp.<slug>``.
            - Soft-deletes (``is_active=false``) any tool row in the DB
              whose canonical name is ``mcp.<slug>.*`` but no longer in
              the remote catalog.
      5. UPDATE ``tool_mcp_server.last_synced_at = now()``,
         ``last_sync_error = NULL`` on success (or store the error
         message on failure).

    Failure paths:
      - Remote fetch failure → store ``last_sync_error``, return
        SyncResult with ``error`` set. Existing cached rows are NOT
        deactivated (could be a temporary outage).
      - DB write failure → propagate the exception; the caller decides.

    Idempotent. Re-running with no remote changes upserts identical
    rows (no false ``updated`` entries unless a column actually changed).
    """
    started = datetime.now(UTC)
    result = SyncResult(slug=slug, started_at=started)

    try:
        server = await _fetch_mcp_server(slug)
        if server is None:
            result.error = f"unknown server slug: {slug!r}"
            result.completed_at = datetime.now(UTC)
            return result

        # ---- Cache freshness check ----
        if not force and _is_cache_fresh(server):
            result.cache_hit = True
            result.completed_at = datetime.now(UTC)
            result.duration_ms = int(
                (result.completed_at - started).total_seconds() * 1000
            )
            vcprint(
                f"[mcp_sync] cache hit for {slug!r} "
                f"(last_synced_at={server.get('last_synced_at')}, "
                f"ttl={server.get('discovery_ttl_seconds')}s)",
                color="cyan",
            )
            return result

        # ---- Transport gate ----
        transport = str(server.get("transport") or "http").strip().lower()
        if transport not in SUPPORTED_TRANSPORTS:
            result.error = (
                f"unsupported MCP transport {transport!r} for server {slug!r}: "
                "ExternalMCPClient speaks JSON-RPC 2.0 over plain HTTP POST "
                "only. Fix the tool.mcp_server row (transport + endpoint_url) "
                f"or implement the {transport!r} transport in ExternalMCPClient "
                "before this server can sync."
            )
            await _record_sync_error(slug, result.error)
            result.completed_at = datetime.now(UTC)
            vcprint(f"[mcp_sync] REJECTED {slug!r}: {result.error}", color="red")
            return result

        endpoint = server.get("endpoint_url")
        stdio_config: dict[str, Any] | None = None
        if transport == "stdio":
            stdio_config = await _fetch_default_mcp_config(server["id"])
            if stdio_config is None:
                result.error = f"stdio server {slug!r} has no tool.mcp_config launch recipe"
                await _record_sync_error(slug, result.error)
                result.completed_at = datetime.now(UTC)
                return result
        elif not endpoint:
            result.error = (
                f"server {slug!r} has no endpoint_url; can't discover tools"
            )
            await _record_sync_error(slug, result.error)
            result.completed_at = datetime.now(UTC)
            return result

        # ---- Remote discovery ----
        client = ExternalMCPClient()
        try:
            remote_tools = await client.discover_tools(
                endpoint,
                auth=_resolve_server_auth(server),
                transport=transport,
                command=stdio_config.get("command") if stdio_config else None,
                args=list(stdio_config.get("args") or []) if stdio_config else None,
            )
        except Exception as exc:
            result.error = f"discover_tools failed: {exc!r}"
            # Preserve provider classification across the package/host boundary.
            # Diagnostic strings are not an API control-flow contract.
            try:
                import httpx

                if isinstance(exc, httpx.HTTPStatusError):
                    result.upstream_status = exc.response.status_code
            except ImportError:  # pragma: no cover - optional transport dependency
                pass
            await _record_sync_error(slug, result.error)
            result.completed_at = datetime.now(UTC)
            return result

        # Build the spec list the RPC consumes. The RPC handles canonical
        # naming, source_kind, managed_by_server_id, binding, and the
        # soft-delete sweep atomically — no per-tool round-trips here.
        metadata = server.get("metadata") or {}
        raw_allowlist = metadata.get("tool_allowlist") if isinstance(metadata, dict) else None
        allowlist = {str(name) for name in (raw_allowlist or []) if name}
        specs: list[dict[str, Any]] = []
        for tool_def in remote_tools:
            local_name = tool_def.name or ""
            if not local_name:
                continue
            local_only = client._strip_namespace(local_name)
            if allowlist and local_only not in allowlist:
                continue
            specs.append(
                {
                    "name": local_only,
                    "description": tool_def.description or local_only,
                    "parameters": tool_def.parameters or {},
                    "output_schema": tool_def.output_schema,
                    "tier": tool_def.tier,
                    "category": tool_def.category,
                }
            )

        delta = await _register_mcp_discovered(server["id"], specs)
        result.inserted = sorted(delta.get("inserted", []))
        result.updated = sorted(delta.get("updated", []))
        result.deactivated = sorted(delta.get("deactivated", []))

        # ---- Stamp last_synced_at ----
        await _stamp_synced(slug)

        result.completed_at = datetime.now(UTC)
        result.duration_ms = int(
            (result.completed_at - started).total_seconds() * 1000
        )
        vcprint(
            f"[mcp_sync] {slug!r}: +{len(result.inserted)} inserted, "
            f"~{len(result.updated)} updated, "
            f"-{len(result.deactivated)} deactivated, "
            f"{result.duration_ms}ms",
            color="green",
        )
        return result

    except Exception as exc:
        result.error = repr(exc)
        result.completed_at = datetime.now(UTC)
        try:
            await _record_sync_error(slug, result.error)
        except Exception:
            pass
        vcprint(
            f"[mcp_sync] {slug!r} FAILED: {result.error}",
            color="red",
        )
        return result


# ---------------------------------------------------------------------------
# Cache freshness
# ---------------------------------------------------------------------------


def _is_cache_fresh(server: dict[str, Any]) -> bool:
    """Return True iff ``now() - last_synced_at < discovery_ttl_seconds``.

    A NULL ``last_synced_at`` always returns False — never synced means
    we need the first run.
    """
    last = server.get("last_synced_at")
    if last is None:
        return False
    if not isinstance(last, datetime):
        return False
    ttl = int(server.get("discovery_ttl_seconds") or 18000)
    age = (
        datetime.now(UTC) - last.replace(tzinfo=UTC)
        if last.tzinfo is None
        else datetime.now(UTC) - last
    ).total_seconds()
    return age < ttl


def _resolve_server_auth(server: dict[str, Any]) -> dict[str, Any] | None:
    """Build the auth dict ``ExternalMCPClient`` consumes.

    Today this is a placeholder — the per-user auth lookup
    (``tool_mcp_user_conn``) doesn't run inside the sync path because
    sync is server-wide, not per-user. The discovery call typically
    only needs an OAuth client credential (server-level) or no auth at
    all. Per-user auth kicks in at ``call_tool`` time.
    """
    auth_strategy = str(server.get("auth_strategy") or "")
    if auth_strategy in ("none", "env"):
        return None
    # OAuth/discovery flows are user-specific; sync-time discovery uses
    # whatever public introspection the server allows.
    return None


# ---------------------------------------------------------------------------
# DB read/write helpers — ORM managers + the new RPC primitive
# ---------------------------------------------------------------------------


async def _fetch_mcp_server(slug: str) -> dict[str, Any] | None:
    """Fetch a single ``tool_mcp_server`` row by slug via the host-injected
    manager. Returns the row as a dict or None.
    """
    try:
        from matrx_ai.db._registry import get_instance

        mgr = get_instance("tool_mcp_server_manager_instance")
    except Exception:
        return None
    try:
        rows = await mgr.filter_items(slug=slug)
    except Exception as exc:
        vcprint(
            f"[mcp_sync] tool_mcp_server fetch for {slug!r} failed: {exc!r}",
            color="red",
        )
        return None
    if not rows:
        return None
    item = rows[0]
    return item.to_dict() if hasattr(item, "to_dict") else dict(item)


async def _fetch_default_mcp_config(server_id: str) -> dict[str, Any] | None:
    """Resolve the canonical local launch recipe for a stdio MCP server."""
    try:
        from matrx_ai.db._registry import get_instance

        mgr = get_instance("tool_mcp_config_manager_instance")
        rows = await mgr.filter_items(server_id=server_id, is_default=True)
        if not rows:
            rows = await mgr.filter_items(server_id=server_id)
    except Exception as exc:
        vcprint(
            f"[mcp_sync] tool.mcp_config fetch for {server_id!r} failed: {exc!r}",
            color="red",
        )
        return None
    if not rows:
        return None
    item = rows[0]
    return item.to_dict() if hasattr(item, "to_dict") else dict(item)


async def _snapshot_managed_tools(server_id: str) -> dict[str, dict[str, Any]] | None:
    """Snapshot the ``tool.definition`` rows managed by one MCP server.

    Returns ``{canonical_name: watched_columns}`` or ``None`` when the host
    hasn't injected the ToolDefinition model (standalone package install) —
    the sync still runs, but the delta report degrades to empty, loudly.
    """
    try:
        from matrx_ai.db._registry import get_model

        model = get_model("ToolDefinition")
        rows = await model.filter(managed_by_server_id=server_id).all()
    except Exception as exc:
        vcprint(
            "[mcp_sync] delta snapshot unavailable (ToolDefinition model not "
            f"injected?): {exc!r} — sync proceeds, but the catalog-drift "
            "report for this run will be empty.",
            color="red",
        )
        return None
    return {
        str(row.name): {
            "is_active": bool(row.is_active),
            "description": row.description,
            "parameters": row.parameters,
            "output_schema": row.output_schema,
        }
        for row in rows
    }


async def _register_mcp_discovered(
    server_id: str, specs: list[dict[str, Any]]
) -> dict[str, list[str]]:
    """Call the ``tool_register_mcp_discovered(p_server_id uuid, p_tool_specs jsonb)
    RETURNS integer`` RPC (upserts tool_def + tool_binding rows, soft-deletes
    dropped ones, returns a row COUNT — not a delta breakdown).

    Because the RPC returns only a count, the real per-tool delta is derived
    here by diffing the server's ``tool.definition`` rows before and after
    the call. Any drift between the stored rows and the remote catalog is
    thereby RECONCILED (the RPC updates the rows) and reported loudly — a
    non-empty delta logs a ``COERCED``-style line naming every changed tool.
    (Previously the delta was always empty: the old code expected a dict from
    an integer-returning function, so every sync report showed "0 changes".)
    """
    from matrx_orm import call_function
    from matrx_orm.core.config import get_all_database_project_names

    names = get_all_database_project_names()
    if not names:
        raise RuntimeError(
            "mcp_sync: no matrx-orm database registered — "
            "call matrx_orm.register_database(...) before syncing MCP tools."
        )
    database = names[0]
    before = await _snapshot_managed_tools(server_id)
    await call_function(
        database,
        "public",
        "tool_register_mcp_discovered",
        server_id,
        specs,
        mode="scalar",
    )
    if before is None:
        return {"inserted": [], "updated": [], "deactivated": []}
    after = await _snapshot_managed_tools(server_id) or {}

    inserted = [name for name in after if name not in before]
    deactivated = [
        name
        for name, state in after.items()
        if name in before and before[name]["is_active"] and not state["is_active"]
    ]
    updated = [
        name
        for name, state in after.items()
        if name in before and state["is_active"] and before[name] != state
    ]
    if inserted or updated or deactivated:
        vcprint(
            "[mcp_sync] COERCED: tool.definition reconciled to the remote MCP "
            f"catalog for server {server_id}: "
            f"inserted={sorted(inserted)} updated={sorted(updated)} "
            f"deactivated={sorted(deactivated)}",
            color="yellow",
        )
    return {"inserted": inserted, "updated": updated, "deactivated": deactivated}


async def _stamp_synced(slug: str) -> None:
    try:
        from matrx_ai.db._registry import get_instance

        mgr = get_instance("tool_mcp_server_manager_instance")
        rows = await mgr.filter_items(slug=slug)
        if not rows:
            return
        await mgr.update_item_fields(
            str(rows[0].id),
            last_synced_at=datetime.now(UTC).isoformat(),
            last_sync_error=None,
        )
    except Exception as exc:
        vcprint(
            f"[mcp_sync] _stamp_synced({slug!r}) failed: {exc!r}",
            color="yellow",
        )


async def _record_sync_error(slug: str, error: str) -> None:
    try:
        from matrx_ai.db._registry import get_instance

        mgr = get_instance("tool_mcp_server_manager_instance")
        rows = await mgr.filter_items(slug=slug)
        if not rows:
            return
        await mgr.update_item_fields(
            str(rows[0].id),
            last_sync_error=error[:1000],
        )
    except Exception as exc:
        vcprint(
            f"[mcp_sync] _record_sync_error({slug!r}) failed: {exc!r}",
            color="yellow",
        )
