"""Agent context engine — resolves cascading context variables for AI agents.

Calls the ``resolve_full_context`` Supabase RPC and splits results into two
delivery tiers:

- **Tier 1 (direct):** Small, always-present variables injected into the
  system prompt via ``SystemInstruction.inject_context_block()``.
- **Tier 2 (tool-accessible / searchable):** Larger variables the agent pulls
  on demand via ``ctx_get`` or search tools.

Wired into all four entry routers (agents, conversations, chat, prompts) via
``aidream.services.conversation_context.context_utils.resolve_agent_context_block`` — failures are
swallowed (logged at WARNING) so a context-engine outage cannot break a
request.
"""

from __future__ import annotations

import copy
import json
import logging
import time
from collections import OrderedDict
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)

LEGACY_CONTEXT_CELL_SHAPE_ERROR_KIND = "context_resolver_legacy_cell_shape"


# ---------------------------------------------------------------------------
# Process-level cache for the resolve_full_context RPC result.
#
# The RPC is on the chat critical path (the "user context" block feeds the
# system prompt). Keyed by ALL its inputs — (user_id, entity_type, entity_id,
# scope_ids) — so a cache hit is exactly the same answer the DB would return,
# with a short TTL + invalidation on context writes (see
# invalidate_context_cache, wired from context_writeback). This collapses the
# RPC to ~0 on turn 2+ of a conversation. Ambient items (current_date/time/…)
# are re-applied fresh AFTER the cache on a deep copy, so they never go stale.
#
# FIRST-TURN acceleration (KD-5, 2026-07-05): a BRAND-NEW entity contributes
# nothing to the RPC result — the entity row isn't committed yet (route-entry
# lane queues the INSERT) and a just-created entity has no scope associations,
# so `resolve_full_context` is fully determined by (user_id, scope_ids). When
# the caller asserts ``entity_is_new=True``, the cache key replaces entity_id
# with a sentinel, so EVERY new conversation for the same user + scope
# selection shares one cached slice (verified against the live RPC definition
# 2026-07-05: all outputs derive from v_entity_scopes — entity associations +
# explicit p_scope_ids — and the entity-row org/project/task lookup, all of
# which are empty/NULL for a new entity). No DB function change required.
_NEW_ENTITY_SENTINEL = "__new_entity__"
_CONTEXT_TTL_SECONDS = 30.0
_CONTEXT_CACHE_MAX = 5000
# key -> (loaded_at_monotonic, resolved_dict)
_context_cache: OrderedDict[tuple[Any, ...], tuple[float, dict[str, Any]]] = OrderedDict()


def _context_cache_key(
    user_id: str,
    entity_type: str,
    entity_id: str,
    scope_ids: list[str] | None,
    *,
    entity_is_new: bool = False,
) -> tuple[Any, ...]:
    effective_entity = _NEW_ENTITY_SENTINEL if entity_is_new else entity_id
    return (user_id, entity_type, effective_entity, tuple(sorted(scope_ids or [])))


def invalidate_context_cache(user_id: str | None = None) -> None:
    """Drop cached context for ``user_id`` (or everything when None).

    Call after any write that changes a user's context items / scopes / values
    so the next resolve reflects it immediately (don't wait out the TTL).
    """
    if user_id is None:
        _context_cache.clear()
        return
    for k in [k for k in _context_cache if k[0] == user_id]:
        _context_cache.pop(k, None)


# ---------------------------------------------------------------------------
# Ambient (class 'ambient') System Context providers — computed per request,
# never stored.
#
# These are System Context Items (rows of context.system_context_item, the
# platform's third context source: what is simply TRUE) whose VALUE is computed
# at resolution time instead of read from storage: the current date, time, the
# running user's id, etc. They're real items (pickable + bindable), seeded once;
# this layer just overrides their value every request so they're always fresh —
# the opposite of a frozen variable, and the whole point of context.
#
# A provider is keyed by the item's `key`. To EXPOSE one, an admin seeds a
# System Context Item with that key; absent the seeded item, the provider is
# inert (nothing to bind to). UTC for now — per-user timezone is a later
# enhancement that needs the user's settings.
# ---------------------------------------------------------------------------
def _ambient_providers(user_id: str | None) -> dict[str, Callable[[], str]]:
    now = datetime.now(UTC)
    return {
        "current_date": lambda: now.date().isoformat(),
        "current_datetime": lambda: now.isoformat(timespec="seconds"),
        "current_time": lambda: now.strftime("%H:%M UTC"),
        "current_year": lambda: str(now.year),
        "current_user_id": lambda: user_id or "",
    }


def _as_cell_list(raw: Any, *, context_item_id: str) -> list[dict[str, Any]]:
    """Normalize one ``cell_values`` entry to the canonical LIST of cells.

    A concrete cell is identified by ``(context_item_id, scope_id)``, so an item that two
    active scopes of the same type both supply has TWO cells. The RPC returns a list per
    item; a bare dict means the database is still running the pre-2026-08-27 function that
    kept only the last scope's value — that is silent data loss, so it screams rather than
    degrading quietly. Delete this branch once every environment has the migration
    ``ctx_resolve_full_context_lossless_cells_per_scope``.
    """
    if isinstance(raw, list):
        return [c for c in raw if isinstance(c, dict)]
    if isinstance(raw, dict):
        return [raw]
    return []


async def _normalize_cell_values(raw_cells: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Normalize the RPC payload and capture one durable contract-drift incident."""
    legacy_item_ids = [item_id for item_id, raw in raw_cells.items() if isinstance(raw, dict)]
    if legacy_item_ids:
        message = (
            "resolve_full_context returned legacy single-cell values; the deployed database "
            "function can silently drop cells supplied by multiple active scopes"
        )
        logger.error(
            "[context_engine] %s; apply migration "
            "ctx_resolve_full_context_lossless_cells_per_scope (affected_items=%d)",
            message,
            len(legacy_item_ids),
        )
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            RuntimeError(message),
            kind=LEGACY_CONTEXT_CELL_SHAPE_ERROR_KIND,
            route="resolve_full_context",
            error_type="LegacyContextCellShape",
            error_text=message,
            context={
                "affected_item_count": len(legacy_item_ids),
                "required_migration": "ctx_resolve_full_context_lossless_cells_per_scope",
            },
        )
    return {
        item_id: _as_cell_list(raw, context_item_id=item_id) for item_id, raw in raw_cells.items()
    }


def _apply_ambient(
    user_id: str | None,
    variables: dict[str, Any],
    cell_values: dict[str, list[dict[str, Any]]],
) -> None:
    """Override the value of any resolved System item whose key matches an ambient provider.
    Mutates the freshly-deserialized RPC dicts in place (variables keyed by key, each
    carrying its own `cells` list; cell_values keyed by context_item_id UUID -> [cell, ...],
    each cell carrying its `key`)."""
    providers = _ambient_providers(user_id)
    for key, compute in providers.items():
        value = compute()
        # ONLY override System items (source == "system"). A user/org context item that
        # happens to share a reserved ambient key must NEVER be clobbered — guard on the
        # resolver-stamped source, not the key alone.
        entry = variables.get(key)
        if isinstance(entry, dict) and entry.get("source") == "system":
            entry["value"] = value
            # The entry's per-scope cells are what the prompt block renders when a key is
            # multi-valued — refreshing only the scalar would leave a stale ambient value
            # visible there.
            for cell in entry.get("cells") or []:
                if isinstance(cell, dict) and cell.get("source") == "system":
                    cell["value"] = value
        for cells in cell_values.values():
            for cell in cells:
                if cell.get("key") == key and cell.get("source") == "system":
                    cell["value"] = value


def _resolve_context_database() -> str:
    """The registered matrx-orm database/project name for the host's primary
    project. matrx-ai injects no host-specific constant (package boundary) —
    a single registered project is the norm, so the first name is correct;
    a host running multiple projects would need an explicit injection seam,
    not yet needed here.
    """
    from matrx_orm.core.config import get_all_database_project_names

    names = get_all_database_project_names()
    if not names:
        raise RuntimeError(
            "context_engine: no matrx-orm database registered — "
            "call matrx_orm.register_database(...) before resolving context."
        )
    return names[0]


async def build_agent_context(
    user_id: str,
    entity_type: str,
    entity_id: str,
    scope_ids: list[str] | None = None,
    *,
    entity_is_new: bool = False,
) -> AgentContext:
    """Resolve all context variables for ``user_id`` and return an AgentContext.

    Parameters
    ----------
    user_id:
        The authenticated user's UUID.
    entity_type:
        The type of entity to resolve context for (e.g. ``'conversation'``,
        ``'task'``, ``'project'``).
    entity_id:
        The UUID of the entity.
    scope_ids:
        Optional explicit active scope selections (``ctx_scopes`` ids) from
        the client's global picker. Unioned server-side with the entity's
        scope tags on the ``platform.associations`` spine; the RPC membership-validates them
        against ``user_id`` and drops foreign/unknown ids.
    entity_is_new:
        Caller asserts the entity was created THIS request (e.g. the
        conversation gate just queued its INSERT). The entity then contributes
        nothing to the RPC result, so the cache key uses a shared sentinel in
        place of ``entity_id`` — every first turn for the same user + scope
        selection hits one cached slice instead of always missing. Only assert
        this from a path that literally just created the entity.
    """
    # Process-cache the RPC result keyed by all inputs (short TTL + write
    # invalidation). A hit is the exact same answer; ambient items are applied
    # fresh below on the (deep-copied) result so they never go stale.
    cache_key = _context_cache_key(
        user_id, entity_type, entity_id, scope_ids, entity_is_new=entity_is_new
    )
    now = time.monotonic()
    cached = _context_cache.get(cache_key)
    if cached is not None and (now - cached[0]) < _CONTEXT_TTL_SECONDS:
        _context_cache.move_to_end(cache_key)
        resolved: dict[str, Any] = copy.deepcopy(cached[1])
    else:
        from matrx_orm import ArrayArg, call_function

        database = _resolve_context_database()
        # p_scope_ids uuid[] DEFAULT NULL::uuid[] — an empty/None scope_ids
        # binds ArrayArg(None), matching the SQL default exactly (same as
        # the old code's "omit the key" behavior via the PostgREST RPC).
        resolved = (
            await call_function(
                database,
                "public",
                "resolve_full_context",
                user_id,
                entity_type,
                entity_id,
                ArrayArg(scope_ids or None),
                mode="scalar",
            )
            or {}
        )
        if not isinstance(resolved, dict):
            # resolve_full_context RETURNS jsonb — the matrx-orm driver codec
            # decodes it to a dict before it ever reaches Python. A str here
            # means that codec is missing/broken (the exact 2026-07-13
            # regression). NEVER json.loads it here as a fallback — that would
            # silently mask a driver-level failure affecting every jsonb read.
            raise TypeError(
                f"[context_engine] resolve_full_context returned "
                f"{type(resolved).__name__}, expected dict — the matrx-orm "
                f"json/jsonb connection codec is missing or broken "
                f"(matrx_orm.core.async_db_manager._init_connection_default). "
                f"Fix the codec; do not decode at this call site."
            )
        # Store an independent copy so downstream in-place mutation
        # (_apply_ambient) can never corrupt the cached value.
        _context_cache[cache_key] = (now, copy.deepcopy(resolved))
        _context_cache.move_to_end(cache_key)
        while len(_context_cache) > _CONTEXT_CACHE_MAX:
            _context_cache.popitem(last=False)
    variables: dict[str, Any] = resolved.get("variables", {})
    context_scope: dict[str, Any] = resolved.get("context", {})
    scope_labels: dict[str, Any] = resolved.get("scope_labels", {})
    # Collision-proof cell map keyed by context_item_id (UUID) — the source for scope→agent
    # binding resolution, which must match by exact id, never by a key that can collide
    # across scope types. The VALUE is a LIST because context_item_id alone does not name a
    # concrete cell: a conversation attached to two Client scopes has two `primary_contact`
    # cells, one per scope. {context_item_id: [{key, value, type, description,
    # context_item_id, scope_id, scope_name, scope_type_id, source}, ...]}.
    raw_cells: dict[str, Any] = resolved.get("cell_values", {}) or {}
    cell_values = await _normalize_cell_values(raw_cells)

    # Ambient System items — override their value with the freshly computed one.
    _apply_ambient(user_id, variables, cell_values)

    tier1_direct: dict[str, Any] = {}
    tier2_tools: dict[str, Any] = {}
    tier2_searchable: dict[str, Any] = {}

    for key, var_data in variables.items():
        inject_as = var_data.get("inject_as", "direct")
        if inject_as == "direct":
            tier1_direct[key] = var_data
        elif inject_as == "tool_accessible":
            tier2_tools[key] = var_data
        elif inject_as == "searchable":
            tier2_searchable[key] = var_data

    return AgentContext(
        scope=context_scope,
        scope_labels=scope_labels,
        direct_variables=tier1_direct,
        tool_variables=tier2_tools,
        searchable_variables=tier2_searchable,
        cells_by_item_id=cell_values,
    )


def _render_prompt_value(value: Any) -> Any:
    """One rendering of a context value for the system-prompt block."""
    if isinstance(value, dict | list):
        return json.dumps(value)
    if isinstance(value, str):
        return value.strip('"')
    return value


class AgentContext:
    """Container for resolved context, split by delivery tier.

    Attributes
    ----------
    scope:
        The resolved scope IDs (user_id, organization_id, project_id, task_id)
        returned by the RPC.
    scope_labels:
        Human-readable scope labels (e.g. ``{"client": "Anthropic", "department": "SEO"}``).
    direct_variables:
        Tier 1 variables — always injected into the system prompt.
    tool_variables:
        Tier 2 variables — available on demand via get_context_variable tool.
    searchable_variables:
        Tier 2 variables — available via search_context tool.
    """

    def __init__(
        self,
        scope: dict[str, Any],
        scope_labels: dict[str, Any],
        direct_variables: dict[str, Any],
        tool_variables: dict[str, Any],
        searchable_variables: dict[str, Any],
        cells_by_item_id: dict[str, list[dict[str, Any]]] | None = None,
    ) -> None:
        self.scope = scope
        self.scope_labels = scope_labels
        self.direct_variables = direct_variables
        self.tool_variables = tool_variables
        self.searchable_variables = searchable_variables
        # context_item_id (UUID) -> [cell, ...] — one cell per ACTIVE SCOPE that supplies
        # this item, each carrying scope_id/scope_name. The collision-proof source for
        # scope→agent binding resolution: the id names the DEFINITION, and (id, scope_id)
        # names the concrete cell. Never collapse this to one cell — two active scopes of a
        # type legitimately carry two different values.
        self.cells_by_item_id = cells_by_item_id or {}

    def build_system_prompt_block(self) -> str:
        """Build the condensed XML block injected via SystemInstruction.inject_context_block().

        This is Tier 1 — always present, compact, critical. Contains scope IDs,
        scope labels, direct variables, and a compact list of available Tier 2 keys.
        """
        # Render the scope IDs first so we can tell whether the block carries any
        # signal at all. An empty `<agent_context><scope></scope></agent_context>`
        # shell is pure noise — it consumes prompt tokens, confuses readers, and
        # (historically) shadowed the deferred-context awareness block in the host.
        # When nothing meaningful is present, emit nothing.
        scope_lines: list[str] = []
        for key in ("organization_id", "project_id", "task_id"):
            val = self.scope.get(key)
            if val:
                label = key.replace("_id", "")
                scope_lines.append(f"    {label}: {val}")

        has_content = bool(
            scope_lines
            or self.scope_labels
            or self.direct_variables
            or self.tool_variables
            or self.searchable_variables
        )
        if not has_content:
            return ""

        lines: list[str] = ["<agent_context>"]

        lines.append("  <scope>")
        lines.extend(scope_lines)
        lines.append("  </scope>")

        if self.scope_labels:
            lines.append("  <scope_labels>")
            for label_key, label_val in self.scope_labels.items():
                if isinstance(label_val, list):
                    lines.append(f"    {label_key}: {', '.join(str(v) for v in label_val)}")
                else:
                    lines.append(f"    {label_key}: {label_val}")
            lines.append("  </scope_labels>")

        if self.direct_variables:
            lines.append("  <variables>")
            for key, var_data in self.direct_variables.items():
                # `variables` is keyed by the BARE item key, which is not unique: two scope
                # types can both define `status`, and two active scopes of one type both
                # define their own `case_number`. Render EVERY contributing cell, labelled by
                # its scope, instead of the single scalar — otherwise the model is shown one
                # client's contact details and never learns the other client exists.
                cells = [c for c in (var_data.get("cells") or []) if isinstance(c, dict)]
                if len(cells) > 1:
                    for cell in cells:
                        scope_name = cell.get("scope_name") or cell.get("source") or ""
                        rendered = _render_prompt_value(cell.get("value"))
                        lines.append(f"    {key} [{scope_name}]: {rendered}")
                    continue
                value = _render_prompt_value(var_data.get("value"))
                source = var_data.get("source", "")
                lines.append(f"    {key}: {value}  [{source}]")
            lines.append("  </variables>")

        if self.tool_variables or self.searchable_variables:
            lines.append("  <available_context>")
            if self.tool_variables:
                tool_keys = ", ".join(self.tool_variables.keys())
                lines.append(f"    Tool-accessible variables: {tool_keys}")
                lines.append("    Use get_context_variable(key) to access these.")
            if self.searchable_variables:
                search_keys = ", ".join(self.searchable_variables.keys())
                lines.append(f"    Searchable context: {search_keys}")
                lines.append("    Use search_context(query) to find relevant content.")
            lines.append("  </available_context>")

        lines.append("</agent_context>")
        return "\n".join(lines)

    def get_tool_variable(self, key: str) -> Any:
        """Return the value for a single Tier 2 tool-accessible variable."""
        var = self.tool_variables.get(key)
        if var:
            return var.get("value")
        return None

    def get_all_tool_variables(self) -> dict[str, Any]:
        """Return all Tier 2 tool-accessible variables as {key: value}."""
        return {k: v.get("value") for k, v in self.tool_variables.items()}

    def get_all_searchable_variables(self) -> dict[str, Any]:
        """Return all Tier 2 searchable variables as {key: value}."""
        return {k: v.get("value") for k, v in self.searchable_variables.items()}

    def to_scope_dict(self) -> dict[str, str | None]:
        """Return the active scope as a plain dict for AppContext.metadata storage."""
        return {
            "organization_id": self.scope.get("organization_id"),
            "project_id": self.scope.get("project_id"),
            "task_id": self.scope.get("task_id"),
        }
