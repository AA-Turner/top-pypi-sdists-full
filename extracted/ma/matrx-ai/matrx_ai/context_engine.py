"""Agent context engine — resolves cascading context variables for AI agents.

Calls the ``resolve_full_context`` Supabase RPC and splits results into two
delivery tiers:

- **Tier 1 (direct):** Small, always-present variables injected into the
  system prompt via ``SystemInstruction.inject_context_block()``.
- **Tier 2 (tool-accessible / searchable):** Larger variables the agent pulls
  on demand via ``ctx_get`` or search tools.

Wired into all four entry routers (agents, conversations, chat, prompts) via
``aidream.services.conversation_context.resolve_agent_context_blocks``. A
context-engine outage still cannot BREAK a request — but as of DD-247 it can no
longer hide either: the resolver screams to ``system_error`` and puts an
``<active_context><unavailable>`` block in the turn, so the model is told it has
no context instead of answering as though the user had selected nothing.
"""

from __future__ import annotations

import copy
import json
import logging
import time
from collections import OrderedDict
from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)

LEGACY_CONTEXT_CELL_SHAPE_ERROR_KIND = "context_resolver_legacy_cell_shape"
CONTEXT_RESOLVER_FAILURE_KIND = "context_resolver_failed"


class ContextResolverUnavailable(Exception):
    """An injected resolver deliberately declines this turn without failing it."""


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
    system_item_refs: list[str] | tuple[str, ...] | None = None,
) -> tuple[Any, ...]:
    # The System refs are an INPUT of the resolver (lane CONTEXT-VALUES-NAMED-2: it reads only
    # the System items they name), so they are part of the key — two turns naming different
    # System items never share one cached answer.
    effective_entity = _NEW_ENTITY_SENTINEL if entity_is_new else entity_id
    return (
        user_id,
        entity_type,
        effective_entity,
        tuple(sorted(scope_ids or [])),
        tuple(sorted(system_item_refs or [])),
    )


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
# inert (nothing to bind to).
#
# THE PERSON'S CLOCK (lane CONTEXT-VALUES-NAMED-2, chair ruling b): `current_timezone` is the
# timezone of the person running the turn, read from the ONE timezone ladder
# (`communication.person_notification_window` — what they declared, what their browser reported
# through /api/person/timezone, their profile, their work location, their organization's
# default), UTC when nothing answers. `current_date` and `current_datetime` are rendered in it,
# the date-time with its UTC offset shown. `current_time` stays UTC and says so.
# ---------------------------------------------------------------------------
#: The ambient keys whose value depends on the person's timezone — the ladder is read only when
#: one of these was named.
TIMEZONE_AMBIENT_KEYS: frozenset[str] = frozenset(
    {"current_date", "current_datetime", "current_timezone"}
)


def _ambient_providers(user_id: str | None, timezone: str = "UTC") -> dict[str, Callable[[], str]]:
    now = datetime.now(UTC)
    try:
        local = now.astimezone(ZoneInfo(timezone))
    except (ZoneInfoNotFoundError, ValueError):
        timezone, local = "UTC", now
    return {
        "current_date": lambda: local.date().isoformat(),
        "current_datetime": lambda: local.isoformat(timespec="seconds"),
        "current_timezone": lambda: timezone,
        "current_time": lambda: now.strftime("%H:%M UTC"),
        "current_year": lambda: str(now.year),
        "current_user_id": lambda: user_id or "",
    }


_TIMEZONE_TTL_SECONDS = 300.0
_timezone_cache: dict[tuple[str, str], tuple[float, str]] = {}


async def person_timezone(user_id: str | None, organization_id: str | None) -> str:
    """The IANA timezone of the person running the turn — ONE source,
    ``communication.person_notification_window`` — or ``"UTC"`` when nothing answers.

    Memoised per (person, organization) for five minutes. An unreadable ladder answers UTC and
    says so in the log; it never fails the turn."""
    if not user_id:
        return "UTC"
    key = (str(user_id), str(organization_id or ""))
    hit = _timezone_cache.get(key)
    now = time.monotonic()
    if hit is not None and now - hit[0] < _TIMEZONE_TTL_SECONDS:
        return hit[1]
    tz = "UTC"
    try:
        from matrx_orm import call_function

        rows = await call_function(
            _resolve_context_database(),
            "communication",
            "person_notification_window",
            str(user_id),
            str(organization_id) if organization_id else None,
            "sms",
            mode="rows",
        )
        row = rows[0] if isinstance(rows, list) and rows else None
        candidate = row.get("timezone") if isinstance(row, dict) else None
        if candidate:
            ZoneInfo(str(candidate))
            tz = str(candidate)
    except Exception as exc:  # noqa: BLE001 — announced; the turn is answered in UTC
        logger.warning(
            "[context_engine] could not read the timezone of person %s (%r); the date and time "
            "this turn carries are in UTC and say so.",
            user_id,
            exc,
        )
    _timezone_cache[key] = (now, tz)
    return tz


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


# ---------------------------------------------------------------------------
# A SYSTEM ITEM REACHES AN AGENT ONLY WHEN SOMETHING NAMES IT
# (lane CONTEXT-VALUES-NAMED; Arman, 2026-09-25: "It must be named in context values or
# variables or it should not be fed … these will grow to thousands … some of them will also
# trigger api calls or other fetching").
#
# THE NAMING REACHES THE DATABASE (lane CONTEXT-VALUES-NAMED-2, chair ruling c). Both resolvers
# (``public.resolve_full_context`` and the record store's ``custom.resolve_context``) take
# ``p_system_item_refs`` — :meth:`SystemContextNames.refs`, the same list on both sides — and
# read ONLY those System rows (``context.named_system_context_items``); nothing is read for an
# item nobody named. The answer still passes through ``agent_context_from_resolved``, which
# applies the same naming again (a resolver that over-answers is filtered, never trusted), and an
# ambient (computed) item is computed only when it survived. Organization / scope context is
# untouched — only cells the resolver stamped ``source: "system"``.
#
# Who names an item: an agent's variable or context-slot binding to it (by id), the platform's
# declared default list below, or an explicit pick (the context inspector). Nothing else.
# ---------------------------------------------------------------------------

#: THE DEFAULT LIST IS A KNOB (chair ruling a, lane CONTEXT-VALUES-NAMED-2): the System items
#: every agent run is handed without naming them are the platform knob
#: ``context/system_item_defaults`` (keys, not ids, so the list is portable across databases),
#: read through the host's reader (:func:`configure_system_item_defaults`).
SYSTEM_ITEM_DEFAULTS_KNOB: tuple[str, str] = ("context", "system_item_defaults")

#: KNOB MIRROR of platform.feature_knob "context" "system_item_defaults" — the registered default,
#: answered only when no host reader is bound or the row cannot be read (announced).
PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS: tuple[str, ...] = (
    "current_date",
    "current_datetime",
    "current_timezone",
)

#: What an item named by the default list says it was named by.
PLATFORM_DEFAULT_NAMER = "the platform's default list"

_defaults_reader: Callable[[], Awaitable[Any]] | None = None
_defaults_announced = False


def configure_system_item_defaults(reader: Callable[[], Awaitable[Any]] | None) -> None:
    """Bind (or unbind) the host's async reader of ``context/system_item_defaults``. The host's
    knob cache is the memo; this package never caches the list itself."""
    global _defaults_reader, _defaults_announced
    _defaults_reader = reader
    _defaults_announced = False


async def platform_default_system_item_keys() -> tuple[str, ...]:
    """The keys of the System items every agent receives without naming them — the knob's
    value, or its registered default (announced) when it cannot be read."""
    global _defaults_announced
    if _defaults_reader is None:
        if not _defaults_announced:
            _defaults_announced = True
            logger.warning(
                "[context_engine] no host reader is bound for the knob %s/%s; every agent is "
                "handed the registered default list %s (bind one with "
                "configure_system_item_defaults()).",
                *SYSTEM_ITEM_DEFAULTS_KNOB,
                list(PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS),
            )
        return PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS
    try:
        raw = await _defaults_reader()
    except Exception as exc:  # noqa: BLE001 — announced; the registered default answers
        logger.error(
            "[context_engine] the knob %s/%s could not be read (%r); every agent is handed the "
            "registered default list %s until it can.",
            *SYSTEM_ITEM_DEFAULTS_KNOB,
            exc,
            list(PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS),
        )
        return PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except ValueError:
            raw = None
    if not isinstance(raw, list) or not all(isinstance(k, str) for k in raw):
        logger.error(
            "[context_engine] the knob %s/%s holds %r, which is not a list of System item keys; "
            "every agent is handed the registered default list %s until it is fixed.",
            *SYSTEM_ITEM_DEFAULTS_KNOB,
            raw,
            list(PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS),
        )
        return PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS
    return tuple(dict.fromkeys(k.strip() for k in raw if k.strip()))


class NamedSystemItem(BaseModel):
    """One naming: ``ref`` is a System item's id or key, ``by`` says who named it."""

    model_config = ConfigDict(frozen=True)

    ref: str
    by: str


class SystemContextNames(BaseModel):
    """THE NAMING CONTRACT — which System items one turn may receive, and who named each.

    One typed shape for every path: the run path, the scope bindings, the preview and both
    sides of the compare all hand this object to :func:`agent_context_from_resolved`. Empty
    (:meth:`none`) means no System item at all.
    """

    model_config = ConfigDict(frozen=True)

    items: tuple[NamedSystemItem, ...] = ()
    #: The platform's default list is part of this naming, not yet read from its knob.
    #: :meth:`resolved` reads it and folds its keys into ``items``.
    with_platform_defaults: bool = False

    @classmethod
    def none(cls) -> SystemContextNames:
        return cls()

    @classmethod
    def platform_defaults(cls) -> SystemContextNames:
        """The platform's default list — read from the knob ``context/system_item_defaults``
        when the naming is :meth:`resolved`, never frozen here."""
        return cls(with_platform_defaults=True)

    def naming(self, refs: Any, *, by: str) -> SystemContextNames:
        """This set plus ``refs`` (ids or keys), each named by ``by``."""
        added = [
            NamedSystemItem(ref=str(r).strip(), by=by)
            for r in (refs or [])
            if r is not None and str(r).strip()
        ]
        merged = list(self.items)
        for item in added:
            if item not in merged:
                merged.append(item)
        return SystemContextNames(
            items=tuple(merged), with_platform_defaults=self.with_platform_defaults
        )

    def merged(self, other: SystemContextNames | None) -> SystemContextNames:
        if other is None:
            return self
        merged = list(self.items)
        for item in other.items:
            if item not in merged:
                merged.append(item)
        return SystemContextNames(
            items=tuple(merged),
            with_platform_defaults=self.with_platform_defaults or other.with_platform_defaults,
        )

    async def resolved(self) -> SystemContextNames:
        """This naming with the platform's default list read from its knob and folded in (the
        defaults first, as they always were). Idempotent."""
        if not self.with_platform_defaults:
            return self
        keys = await platform_default_system_item_keys()
        return SystemContextNames().naming(keys, by=PLATFORM_DEFAULT_NAMER).merged(
            SystemContextNames(items=self.items)
        )

    def refs(self) -> list[str]:
        """THE LIST BOTH RESOLVERS ARE HANDED (``p_system_item_refs``) — every named id or key,
        once, sorted. Call on a :meth:`resolved` naming; an unresolved default list is refused
        rather than silently dropped."""
        if self.with_platform_defaults:
            raise RuntimeError(
                "SystemContextNames.refs() on a naming whose platform default list was not read "
                "yet — await .resolved() first."
            )
        return sorted({item.ref for item in self.items})

    def named_by(self, *, key: str | None, context_item_id: str | None) -> list[str]:
        """Who named this System item — empty when nobody did."""
        wanted = {str(v) for v in (key, context_item_id) if v}
        out: list[str] = []
        for item in self.items:
            if item.ref in wanted and item.by not in out:
                out.append(item.by)
        return out

    def admits(self, *, key: str | None, context_item_id: str | None) -> bool:
        return bool(self.named_by(key=key, context_item_id=context_item_id))


#: The naming in force for a resolution that was not handed one explicitly. Unset = the
#: platform's declared default list (a caller that names nothing gets the defaults, never all).
_system_names_var: ContextVar[SystemContextNames | None] = ContextVar(
    "matrx_ai_system_context_names", default=None
)


async def system_names_in_force(names: SystemContextNames | None = None) -> SystemContextNames:
    """The naming a resolution uses, resolved: ``names`` when given, else the one in force
    (:func:`naming_system_items`), else the platform's default list — never every item."""
    chosen = names if names is not None else _system_names_var.get()
    if chosen is None:
        chosen = SystemContextNames.platform_defaults()
    return await chosen.resolved()


@contextmanager
def naming_system_items(names: SystemContextNames | None) -> Iterator[None]:
    """Resolve context inside this block with ``names`` as the System naming.

    For callers that reach :func:`agent_context_from_resolved` through a seam they do not own
    (``resolve_active_selection`` → ``build_agent_context``)."""
    token = _system_names_var.set(names)
    try:
        yield
    finally:
        _system_names_var.reset(token)


def _is_system_cell(cell: Any) -> bool:
    return isinstance(cell, dict) and cell.get("source") == "system"


def _admit_named_system_items(
    variables: dict[str, Any],
    cell_values: dict[str, list[dict[str, Any]]],
    names: SystemContextNames,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Drop every System cell nobody named. Returns (delivered, withheld keys).

    ``delivered`` is ``[{key, context_item_id, named_by}]``. Mutates both maps in place.
    A scope item that shares a System key keeps its own cells and value — only the System
    cell goes (the resolvers fold a System cell into a same-key scope entry's ``cells``)."""
    delivered: dict[str, dict[str, Any]] = {}
    withheld: list[str] = []

    def _admit(cell: dict[str, Any], item_id: str | None) -> bool:
        key = str(cell.get("key") or "")
        cid = str(cell.get("context_item_id") or item_id or "")
        by = names.named_by(key=key, context_item_id=cid)
        if by:
            delivered.setdefault(key, {"key": key, "context_item_id": cid or None, "named_by": by})
            return True
        if key and key not in withheld:
            withheld.append(key)
        return False

    for item_id in list(cell_values):
        cells = cell_values[item_id]
        kept = [c for c in cells if not _is_system_cell(c) or _admit(c, item_id)]
        if kept:
            cell_values[item_id] = kept
        else:
            del cell_values[item_id]

    for key in list(variables):
        entry = variables[key]
        if not isinstance(entry, dict):
            continue
        cells = entry.get("cells")
        if isinstance(cells, list):
            entry["cells"] = [
                c for c in cells if not _is_system_cell(c) or _admit(c, c.get("context_item_id"))
            ]
        if entry.get("source") == "system":
            system_cells = [c for c in (entry.get("cells") or []) if _is_system_cell(c)]
            if not system_cells and not names.named_by(key=key, context_item_id=None):
                del variables[key]
                if key not in withheld:
                    withheld.append(key)
    withheld = [k for k in withheld if k not in delivered]
    return list(delivered.values()), withheld


def _present_system_keys(
    variables: dict[str, Any], cell_values: dict[str, list[dict[str, Any]]]
) -> set[str]:
    return {
        key
        for key, entry in variables.items()
        if isinstance(entry, dict) and entry.get("source") == "system"
    } | {
        str(c.get("key"))
        for cells in cell_values.values()
        for c in cells
        if _is_system_cell(c)
    }


def _apply_ambient(
    user_id: str | None,
    variables: dict[str, Any],
    cell_values: dict[str, list[dict[str, Any]]],
    *,
    timezone: str = "UTC",
) -> None:
    """Override the value of any resolved System item whose key matches an ambient provider.
    Mutates the freshly-deserialized RPC dicts in place (variables keyed by key, each
    carrying its own `cells` list; cell_values keyed by context_item_id UUID -> [cell, ...],
    each cell carrying its `key`).

    A provider is CALLED only for an ambient item that is still present — i.e. one that was
    named (:func:`_admit_named_system_items` runs first). An unnamed computed item is never
    evaluated. ``timezone`` is the person's (:func:`person_timezone`); the date and date-time
    are rendered in it."""
    present = _present_system_keys(variables, cell_values)
    if not present:
        return
    providers = _ambient_providers(user_id, timezone)
    for key, compute in providers.items():
        if key not in present:
            continue
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


# ---------------------------------------------------------------------------
# THE MERGE-FIELD RESOLVER SEAM.
#
# DYN-23: one resolver produces resolved context for the prompt, tool arguments,
# workflow branches and the screen. That resolver lives in `matrx-records`, which
# already imports this package's tool contracts — so importing it HERE would close a
# cycle between two siblings, which the package graph forbids for good reason.
#
# So it is injected. `matrx_records.merge.context_bridge.producer` is what the host wires
# in (one line at startup, behind the unified-data campaign's OFF switch); with nothing
# wired, `build_agent_context` behaves exactly as it does today and says so at the one
# place where the difference is visible (no provenance, no on-screen explanation).
#
# The producer's contract: async, keyword-only `(user_id, scope, variables, cells,
# entity_type, entity_id)`, returning {"direct": {...}, "tool_accessible": {...},
# "searchable": {...}}.
# ---------------------------------------------------------------------------
_merge_producer: Callable[..., Any] | None = None


#: WHICH RESOLVER ANSWERS THIS TURN (lane SC-2'). The host may wire ONE chooser that, for a
#: turn, returns the record store's answer (``custom.resolve_context``, the same shape as
#: ``public.resolve_full_context``) when the turn's organization has chosen the new path, or
#: ``None`` for the old path. Unwired — and for every organization that has not chosen — the old
#: resolver answers exactly as it always has. The per-organization knob behind it defaults to the
#: OLD path until the owner validates the copy (SCOPES-CONTEXT rev 2: nothing flips until then).
_path_chooser: Callable[..., Any] | None = None


def configure_context_path(chooser: Callable[..., Any] | None) -> None:
    """Wire (or unwire) the chooser that may answer a turn from the record store instead."""
    global _path_chooser
    _path_chooser = chooser


def configure_context_resolver(producer: Callable[..., Any] | None) -> None:
    """Wire (or unwire) the ONE merge-field resolver this engine consumes."""
    global _merge_producer
    _merge_producer = producer
    logger.info(
        "[context_engine] merge-field resolver %s",
        "wired — every context value now resolves through one ladder with one "
        "provenance row" if producer is not None else "removed",
    )


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
    use_cache: bool = True,
    path: str = "chosen",
    system_names: SystemContextNames | None = None,
) -> AgentContext:
    """Resolve all context variables for ``user_id`` and return an AgentContext.

    ``path`` — ``"chosen"`` (default) lets the host's path chooser answer from the record store
    when the turn's organization has chosen the new path; ``"old"`` always asks the current
    context system (the compare's old side).

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
    # WHICH System items this resolution may read (lane CONTEXT-VALUES-NAMED-2): decided HERE,
    # before either resolver runs, and handed to both as ``p_system_item_refs`` — the database
    # reads only the named rows. The same naming then filters the answer in
    # agent_context_from_resolved, so the two can never disagree.
    names = await system_names_in_force(system_names)
    system_item_refs = names.refs()
    # Process-cache the RPC result keyed by all inputs (short TTL + write
    # invalidation). A hit is the exact same answer; ambient items are applied
    # fresh below on the (deep-copied) result so they never go stale.
    cache_key = _context_cache_key(
        user_id,
        entity_type,
        entity_id,
        scope_ids,
        entity_is_new=entity_is_new,
        system_item_refs=system_item_refs,
    )
    now = time.monotonic()
    # ``use_cache=False`` is for a caller that must see THIS instant's answer — the agent-context
    # compare (lane SC-3'), where a thirty-second-old cached value on one side and a fresh read on
    # the other would read as a difference between the two resolvers that is really the cache's.
    cached = _context_cache.get(cache_key) if use_cache else None
    from_the_store: dict[str, Any] | None = None
    if _path_chooser is not None and path != "old":
        try:
            from_the_store = await _path_chooser(
                user_id=user_id,
                entity_type=entity_type,
                entity_id=entity_id,
                scope_ids=list(scope_ids or []),
                system_item_refs=system_item_refs,
            )
        except Exception as exc:  # noqa: BLE001 — announced, then the old path answers
            logger.error(
                "[context_engine] the record store's context path failed for this turn (%r); the "
                "current context system answered instead. This is a degraded answer and it is "
                "being reported as one.",
                exc,
                exc_info=True,
            )
            from matrx_connect.streaming.error_capture import capture_error

            await capture_error(
                exc,
                kind=CONTEXT_RESOLVER_FAILURE_KIND,
                route="build_agent_context.context_path",
                error_type=type(exc).__name__,
                error_text="The record store's context path failed; the current context system answered.",
                user_id=user_id,
                context={"entity_type": entity_type},
            )
            from_the_store = None
    if from_the_store is not None:
        resolved = from_the_store
    elif cached is not None and (now - cached[0]) < _CONTEXT_TTL_SECONDS:
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
                # p_system_item_refs text[] — ALWAYS an explicit array: '{}' reads no System item,
                # while NULL (an old caller that does not know the argument) is the knob's
                # default list (chair ruling, cvn3). This caller always knows what it names.
                ArrayArg(list(system_item_refs), "text"),
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
    return await agent_context_from_resolved(
        user_id, resolved, entity_type=entity_type, entity_id=entity_id, system_names=names
    )


async def agent_context_from_resolved(
    user_id: str,
    resolved: dict[str, Any],
    *,
    entity_type: str,
    entity_id: str,
    system_names: SystemContextNames | None = None,
) -> AgentContext:
    """Everything that happens to a resolver's answer after it comes back — ONE body.

    ``system_names`` — which System items this turn may receive (:class:`SystemContextNames`).
    Not passed: the naming in force (:func:`naming_system_items`); none in force: the platform's
    declared default list. An unnamed System item is dropped here, before anything evaluates it.

    ``resolved`` is ``public.resolve_full_context``'s answer, or the record store's twin of
    it (``custom.resolve_context``, the same shape — lane SC-3'). The ambient refresh, the
    injected merge-field producer and the tier split all run HERE and only here, so the two
    resolvers can be compared with exactly one difference between them: which resolver
    answered. Mutates ``resolved`` in place; pass a copy when it must be kept.
    """
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

    # A System item reaches the agent only when something named it — dropped BEFORE the
    # ambient refresh, so an unnamed computed item is never computed.
    names = await system_names_in_force(system_names)
    system_delivered, system_withheld = _admit_named_system_items(variables, cell_values, names)

    # Ambient System items — override their value with the freshly computed one. The person's
    # timezone is read only when a date, date-time or timezone item survived the naming.
    timezone = "UTC"
    if TIMEZONE_AMBIENT_KEYS & _present_system_keys(variables, cell_values):
        timezone = await person_timezone(user_id, context_scope.get("organization_id"))
    _apply_ambient(user_id, variables, cell_values, timezone=timezone)

    # THE ONE PRODUCER (DYN-23). When a merge-field resolver is wired, every variable
    # and every context cell is resolved through it — one ladder, one memo, one
    # provenance row each — and the tiers below are what it decided. Prompt substitution
    # becomes the LAST RENDERER of values that were already decided, never the design.
    producer = _merge_producer
    if producer is not None:
        try:
            resolved_tiers = await producer(
                user_id=user_id,
                scope=context_scope,
                variables=variables,
                cells=cell_values,
                # WHICH THING THIS TURN IS ABOUT. The RPC's `context` map carries the
                # user, the organization, the project and the task, and deliberately not
                # the entity itself — but an attachment set ("the Files on THIS
                # conversation") is addressed by exactly that. Passed beside the scope
                # rather than merged into it, so nothing downstream starts treating a
                # conversation id as a resolved scope.
                entity_type=entity_type,
                entity_id=entity_id,
            )
        except ContextResolverUnavailable as exc:
            # A host may deliberately leave an injected capability inactive (for
            # example, while a feature campaign is OFF). That is the same behavior
            # as no resolver being wired: continue with the established tier split.
            logger.info(
                "[context_engine] merge-field resolver is unavailable for this turn "
                "(%s); using the direct tier split.",
                exc,
            )
        except Exception as exc:  # noqa: BLE001 — announced, never silent
            logger.error(
                "[context_engine] the merge-field resolver refused this turn (%r). "
                "Falling back to the direct tier split below, which does NOT record "
                "provenance and cannot explain a value on screen. This is a degraded "
                "answer and it is being reported as one.",
                exc,
                exc_info=True,
            )
            from matrx_connect.streaming.error_capture import capture_error

            await capture_error(
                exc,
                kind=CONTEXT_RESOLVER_FAILURE_KIND,
                route="build_agent_context",
                error_type=type(exc).__name__,
                error_text="The injected context resolver failed; the direct tier split was used.",
                user_id=user_id,
                context={"entity_type": entity_type},
            )
        else:
            return AgentContext(
                scope=context_scope,
                scope_labels=scope_labels,
                direct_variables=resolved_tiers.get("direct", {}),
                tool_variables=resolved_tiers.get("tool_accessible", {}),
                searchable_variables=resolved_tiers.get("searchable", {}),
                cells_by_item_id=cell_values,
                system_delivered=system_delivered,
                system_withheld=system_withheld,
            )

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
        else:
            # A VALUE THAT BELONGS TO NO TIER IS A DEFECT, NEVER A SILENT DROP (DYN-17).
            # This is the live bug in as many words: the engine tiers into
            # direct/tool_accessible/searchable while the RPC emits `reference`, so a
            # `reference` value fell into none of the three and vanished with nothing
            # said anywhere. It is delivered as `direct` — present and usable — and the
            # mismatch is reported so somebody fixes the emitter.
            logger.warning(
                "[context_engine] context value %r asks to be delivered as %r, which is "
                "not one of the three tiers (direct, tool_accessible, searchable). It "
                "was delivered DIRECTLY rather than dropped. Remedy: the emitter of that "
                "value should name a real tier — see DYN-17.",
                key,
                inject_as,
            )
            tier1_direct[key] = var_data

    return AgentContext(
        scope=context_scope,
        scope_labels=scope_labels,
        direct_variables=tier1_direct,
        tool_variables=tier2_tools,
        searchable_variables=tier2_searchable,
        cells_by_item_id=cell_values,
        system_delivered=system_delivered,
        system_withheld=system_withheld,
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
        system_delivered: list[dict[str, Any]] | None = None,
        system_withheld: list[str] | None = None,
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
        #: The System items this turn received — ``[{key, context_item_id, named_by}]`` — and
        #: the keys of those it did not, because nothing named them (lane CONTEXT-VALUES-NAMED).
        self.system_delivered = list(system_delivered or [])
        self.system_withheld = list(system_withheld or [])

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
