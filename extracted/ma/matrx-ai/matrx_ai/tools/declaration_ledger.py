"""The conversation's tool-declaration ledger: the provider ``tools`` array is
append-only for the life of a conversation, and every exception is DELIBERATE and
recorded.

Why: on Anthropic the cached prefix is ``tools -> system -> messages``. Any change
at tool position N throws away everything after it, so removing, reordering or
re-describing ONE tool mid-conversation re-writes the whole conversation at the
cache-write price. Measured on real jobs (common-docs
``systems/agents/projects/agent-evaluation/reports/tool-list-cache-stability.md``): a loop-guard
removal of ``records`` re-wrote 170,818 tokens (92.3 cents) in one request, and a
desktop authority gate flipping ``local_file``/``local_shell`` in and out changed
the list 7-8 times in one turn.

Many upstream paths legitimately change the EFFECTIVE toolset (loop guard,
discovery loaders, authority exclusions, delegation/capability filters, the
re-merge after suspend/resume or crash recovery). The fix lives at the one
boundary every translator uses (``BaseTranslator.build_provider_tools``):

* the array is in ONE ORDER (static seal P0.2, D16: one platform-guaranteed order at the source),
  in TWO TIERS: the agent's AUTHORED tools first, sorted by name, then every tool a platform source
  added (surface/app tools, bundles, discovery, sandbox fs/shell, context tools), sorted by name
  (``order_key``). Tools head the cached prefix (Anthropic: tools -> system -> messages), so with
  one flat name order a platform tool that sorts early (``apply_surface_write``, ``data``) moved
  every authored tool after it and gave one agent a new cached prefix per app it ran in (Badass
  Agent: 6 variants in 32 h, 5 from platform tools; lane 6, 2026-11-17). Tiered, the authored run
  is byte-identical whatever the surface adds, and a cache mark at its end (``prompt_warm``) is
  read across every variant. The same set of declarations is still the same bytes on every path — built fresh, reloaded
  from the jsonb record, on another worker, with or without a conversation id. Each declaration's
  keys are in the one canonical order too (``matrx_ai.config.canonical_order``); the members of a
  schema's ``properties`` keep the order the tool's source gave them (the model writes arguments in
  that order) and are frozen per conversation by the record's sent JSON text;
* a declaration no longer offered stays declared (RETAINED); a call to it is
  refused by the executor with a reason (``retained_reason``);
* a declaration seen for the first time is ADDED at its sorted place IN ITS TIER. Before P0.2 it was
  appended at the end; on Anthropic (tools -> system -> messages) both re-write everything after the
  tools, so the sorted place costs at most the tools after it, and buys an order no path can disagree
  on. A platform tool never lands inside the authored run. Tier membership is sticky for the
  conversation (``_Ledger.authored``, recorded as ``authored: true``), so a retained authored tool
  keeps its place.

The array changes in place ONLY as a deliberate, recorded cache break (an event
drained by the orchestrator: ``capture_error`` + a client warning):

* ``tool_definition_updated`` — a still-offered tool's description/schema changed
  (a new MCP server version): the new bytes are adopted in place, once;
* ``tool_name_reassigned`` — a recycled name now names a different target (agent
  projections ``custom_tool_N`` are numbered per request): the declaration must
  describe what the executor will actually run;
* ``tool_ceiling_eviction`` — appending would exceed the provider's tool-count
  limit (``matrx_ai.providers.tool_count_limits``): the longest-withdrawn retained
  tools are dropped first. A request the provider would refuse is never sent
  because of the ledger.

Execution authority is unchanged: what may run is decided from the live config
(``allowed_tools``), so keeping a declaration never re-enables a tool.

Scope and memory:
* keyed by (conversation_id, provider) from the ambient AppContext;
* a call with NO declarations passes through untouched (whole-belt provider
  limits); a call with no conversation id is never tracked;
* ``tool_belt_replaced`` — a call sharing NO name with the conversation's
  ledger (an agent switch mid-conversation) replaces the array: a deliberate,
  recorded and announced cache break;
* durable: the record rides ``UnifiedConfig.tool_declarations``
  (``cx_conversation.config``) with a monotonically increasing ``seq``; the
  orchestrator hydrates before every send (the NEWER of memory and record wins)
  and exports after it; a loop's end keeps the ledger (``end_loop``) so a
  follow-up turn on this worker appends even before the record reaches the row;
  the LRU bound caps memory and ``forget_conversation`` releases it outright.
"""

from __future__ import annotations

import copy
import hashlib
import json
import threading
from collections import OrderedDict
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.canonical_order import canonical_json

#: LRU bound on tracked (conversation, provider) ledgers per worker. A ledger
#: outlives its loop (``end_loop``) so the next turn on this worker appends to
#: it; this bound is what releases memory.
MAX_TRACKED_CONVERSATIONS = 256

#: Reason given when a retained tool is called and no remover recorded why.
DEFAULT_UNAVAILABLE_REASON = (
    "it is not available in this turn (no reason was recorded for its removal, so this is "
    "not a withdrawal by its source)"
)

EVENT_DEFINITION_UPDATED = "tool_definition_updated"
EVENT_NAME_REASSIGNED = "tool_name_reassigned"
EVENT_CEILING_EVICTION = "tool_ceiling_eviction"
EVENT_BELT_REPLACED = "tool_belt_replaced"
EVENT_NATIVE_WITHDRAWN = "native_tool_withdrawn"

#: Ledger key prefix for a provider-native declaration (no function name): ``<type>``, the
#: same name the wire guard (``cache_guard._declaration_identity``) gives it, so a recorded
#: break excuses exactly what the guard sees. Never a legal tool name (``<`` fails every
#: provider's name pattern), so it cannot collide with one.
_NATIVE_PREFIX = "<"


def order_key(name: str, authored: frozenset[str] | set[str]) -> tuple[int, str]:
    """THE ONE ORDER (P0.2, two tiers): the agent's authored tools first, then every platform-added
    tool; by name inside each tier. ``authored`` holds WIRE names."""
    return (0 if name in authored else 1, name)


def _native_key(decl: dict[str, Any], taken: set[str]) -> str:
    kind = decl.get("type") if isinstance(decl, dict) else None
    base = f"{_NATIVE_PREFIX}{kind or 'nameless'}>"
    key, n = base, 1
    while key in taken:
        n += 1
        key = f"{base}#{n}"
    return key


def _is_native_key(name: str) -> bool:
    return name.startswith(_NATIVE_PREFIX)


@dataclass
class _Ledger:
    order: list[str] = field(default_factory=list)
    declarations: dict[str, dict[str, Any]] = field(default_factory=dict)
    digests: dict[str, str] = field(default_factory=dict)
    #: Target identity per name, when the name can be recycled (agent projections).
    identities: dict[str, str] = field(default_factory=dict)
    #: name -> ``seq`` at which it was first withdrawn (oldest are evicted first).
    retained_since: dict[str, int] = field(default_factory=dict)
    #: Bumped on every change to the array; the newer of memory and record wins.
    seq: int = 0
    #: Set by a deliberate break, consumed by the wire guard so it does not
    #: re-scream a change the ledger already captured.
    deliberate_break: bool = False
    #: Tool names the recorded break covers (``None`` = the whole belt). The wire
    #: guard excuses ONLY a change confined to these names, so a second, unrecorded
    #: change riding the same request still screams (adversarial M5, 2026-10-18).
    deliberate_scope: set[str] | None = field(default_factory=set)
    #: Wire names the agent authored in this conversation (sticky: a retained authored tool keeps
    #: its tier). The first tier of THE ONE ORDER (``order_key``).
    authored: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class StabilizeResult:
    declarations: list[dict[str, Any]]
    appended: tuple[str, ...] = ()
    retained: tuple[str, ...] = ()
    events: tuple[dict[str, Any], ...] = ()
    applied: bool = False


_LEDGERS: OrderedDict[tuple[str, str], _Ledger] = OrderedDict()
#: conversation_id -> {wire name: reason}.
_UNAVAILABLE_REASONS: OrderedDict[str, dict[str, str]] = OrderedDict()
#: conversation_id -> deliberate-break events not yet announced.
_PENDING_EVENTS: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
_LOCK = threading.Lock()


def _digest(decl: dict[str, Any]) -> str:
    raw = json.dumps(decl, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8", "replace")).hexdigest()


def _wire(name: str) -> str:
    from matrx_ai.config.wire_names import to_wire_name

    return to_wire_name(name)


def current_conversation_id() -> str | None:
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except Exception:
        return None
    conversation_id = getattr(ctx, "conversation_id", None) if ctx is not None else None
    return str(conversation_id) if conversation_id else None


def projected_tool_identities() -> dict[str, str]:
    """Wire name -> stable target identity for this request's agent projections.

    ``custom_tool_N`` names are allocated per request, so the same name can name
    a different agent on a later request; the identity tells the ledger which.
    """
    try:
        from matrx_connect.context.app_context import try_get_app_context

        from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY

        ctx = try_get_app_context()
        projected = (getattr(ctx, "metadata", None) or {}).get(PROJECTED_AGENT_TOOLS_KEY) or {}
    except Exception:
        return {}
    out: dict[str, str] = {}
    for name, dumped in projected.items():
        if isinstance(dumped, dict):
            target = dumped.get("prompt_id") or dumped.get("agent_id") or ""
            out[_wire(str(name))] = f"{target}:{bool(dumped.get('prompt_is_version', False))}"
    return out


def _touch(key: tuple[str, str]) -> _Ledger:
    ledger = _LEDGERS.get(key)
    if ledger is None:
        ledger = _Ledger()
        _LEDGERS[key] = ledger
        while len(_LEDGERS) > MAX_TRACKED_CONVERSATIONS:
            _LEDGERS.popitem(last=False)
    else:
        _LEDGERS.move_to_end(key)
    return ledger


def _queue_events(conversation_id: str, events: list[dict[str, Any]]) -> None:
    if not events:
        return
    pending = _PENDING_EVENTS.setdefault(conversation_id, [])
    pending.extend(events)
    _PENDING_EVENTS.move_to_end(conversation_id)
    while len(_PENDING_EVENTS) > MAX_TRACKED_CONVERSATIONS:
        _PENDING_EVENTS.popitem(last=False)


def _canonical_or_copy(decl: dict[str, Any]) -> dict[str, Any]:
    """``canonical_json(decl)``; when that cannot be built (a schema nested past the recursion
    limit, a value it cannot copy) the declaration as it was kept before P0.2 — a plain copy —
    so the canonical order never changes what a send does."""
    try:
        return canonical_json(decl)
    except Exception as exc:  # noqa: BLE001 — the one order never fails a send
        _say_canonical_failure(exc)
        return copy.deepcopy(decl)


_CANONICAL_FAILURES: set[str] = set()


def _say_canonical_failure(exc: BaseException) -> None:
    mark = type(exc).__name__
    if mark in _CANONICAL_FAILURES:
        return
    _CANONICAL_FAILURES.add(mark)
    vcprint(
        f"[tools] canonical key order not applied to a declaration (sent as built; said once): {mark}: {exc}",
        color="red",
    )


def canonical_tool_array(
    declarations: list[dict[str, Any]],
    *,
    name_of: Callable[[dict[str, Any]], str | None],
    authored: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """THE ONE ORDER for a tools array with no ledger: authored tools first, then platform-added
    ones, by name inside each tier (``order_key``; a provider-native tool by its ``<type>`` key,
    exactly as the ledger keys it), each declaration's keys canonical. The ledger produces the same
    order, so a tracked and an untracked send of one set are the same bytes."""
    tier = frozenset(authored or ())
    keyed: list[tuple[str, dict[str, Any]]] = []
    taken: set[str] = set()
    for decl in declarations:
        name = name_of(decl)
        if name is None:
            name = _native_key(decl, taken)
            taken.add(name)
        keyed.append((name, decl))
    keyed.sort(key=lambda pair: order_key(pair[0], tier))
    return [_canonical_or_copy(decl) for _, decl in keyed]


def held_names(provider: str, conversation_id: str | None = None) -> frozenset[str]:
    """The declaration names this conversation's ledger already sends for ``provider`` (read-only).

    A name in here stays in the tools list for the life of the conversation, so a caller that would
    otherwise deliver it elsewhere (late tools) must not deliver it twice."""
    conversation_id = conversation_id or current_conversation_id()
    if not conversation_id:
        return frozenset()
    ledger = _LEDGERS.get((conversation_id, provider))
    return frozenset(ledger.order) if ledger is not None else frozenset()


def authored_names(provider: str, conversation_id: str | None = None) -> frozenset[str]:
    """The wire names this conversation's ledger holds in the AUTHORED tier for ``provider`` (read-only;
    the wire guard reads it to judge an insert against THE ONE ORDER)."""
    conversation_id = conversation_id or current_conversation_id()
    if not conversation_id:
        return frozenset()
    ledger = _LEDGERS.get((conversation_id, provider))
    return frozenset(ledger.authored) if ledger is not None else frozenset()


def stabilize_declarations(
    provider: str,
    declarations: list[dict[str, Any]],
    *,
    name_of: Callable[[dict[str, Any]], str | None],
    conversation_id: str | None = None,
    max_tools: int | None = None,
    identities: dict[str, str] | None = None,
    authored: Iterable[str] | None = None,
) -> StabilizeResult:
    """Return the conversation-stable ``tools`` array for this request.

    ``declarations`` are provider-formatted, wire-named declarations the current
    request would send; ``name_of`` extracts a name (``None`` for provider-native
    tools, which ride at the end untracked). ``max_tools`` is the provider's
    tool-count ceiling (None = no known ceiling). ``identities`` maps a recyclable
    wire name to its current target (defaults to this request's agent projections).
    ``authored`` holds the wire names of the agent's own tools: they lead the array (``order_key``).
    """
    conversation_id = conversation_id or current_conversation_id()
    if not declarations:
        return StabilizeResult(declarations=declarations)
    if not conversation_id:
        # Untracked (no conversation): still the one order, so the bytes never depend on how the
        # list was built.
        return StabilizeResult(
            declarations=canonical_tool_array(declarations, name_of=name_of, authored=authored)
        )

    named: list[tuple[str, dict[str, Any]]] = []
    native: list[tuple[str, dict[str, Any]]] = []
    for decl in declarations:
        name = name_of(decl)
        if name is None:
            native.append((_native_key(decl, {k for k, _ in native}), decl))
        else:
            named.append((name, decl))
    if not named and not native:
        return StabilizeResult(declarations=declarations)
    if identities is None:
        identities = projected_tool_identities()

    key = (conversation_id, provider)
    events: list[dict[str, Any]] = []
    with _LOCK:
        ledger = _LEDGERS.get(key)
        current_names = {name for name, _ in named}
        native_names = {name for name, _ in native}
        ledger_named = {n for n in ledger.order if not _is_native_key(n)} if ledger is not None else set()
        if named and ledger_named and not (current_names & ledger_named):
            # A WHOLE-BELT SWAP inside a conversation that already has a ledger
            # (an agent switch mid-conversation). Keeping every old declaration
            # would grow the array without bound and describe tools nobody
            # offers; the new belt replaces it. That throws away the cached
            # prefix, so it is a DELIBERATE, recorded and announced break —
            # never a silent one (adversarial I2, 2026-10-18).
            events.append(
                {
                    "kind": EVENT_BELT_REPLACED,
                    "provider": provider,
                    "previous_tools": [n for n in ledger.order if not _is_native_key(n)],
                    "tools": [name for name, _ in named],
                }
            )
            seq = ledger.seq
            ledger = _Ledger(seq=seq)
            _LEDGERS[key] = ledger
            _LEDGERS.move_to_end(key)
            # The swapped-out tools' refusal reasons no longer apply.
            _UNAVAILABLE_REASONS.pop(conversation_id, None)
        ledger = _touch(key)
        changed = bool(events)
        authored_now = {name for name in (authored or ()) if isinstance(name, str)}
        if not authored_now <= ledger.authored:
            ledger.authored |= authored_now
            changed = True

        # A PROVIDER-NATIVE tool (no function name: web search, code execution) holds its
        # position like any other declaration — riding untracked at the END, it was pushed
        # down by every appended tool and re-wrote the cached prefix from that position on
        # (system_error prompt_cache_tool_list_changed / tool_inserted_before_existing_tools,
        # 2026-11-01..04). It is never RETAINED once withdrawn: the provider runs it itself,
        # so keeping it declared would keep it callable. Its withdrawal is a recorded break.
        withdrawn_native = [n for n in ledger.order if _is_native_key(n) and n not in native_names]
        if withdrawn_native:
            for victim in withdrawn_native:
                ledger.order.remove(victim)
                for store in (ledger.declarations, ledger.digests, ledger.identities, ledger.retained_since):
                    store.pop(victim, None)
            events.append({"kind": EVENT_NATIVE_WITHDRAWN, "provider": provider, "tools": withdrawn_native})
            changed = True

        appended: list[str] = []
        for name, decl in [*named, *native]:
            digest = _digest(decl)
            identity = identities.get(name)
            if name not in ledger.declarations:
                ledger.order.append(name)
                ledger.declarations[name] = _canonical_or_copy(decl)
                ledger.digests[name] = digest
                if identity is not None:
                    ledger.identities[name] = identity
                appended.append(name)
                changed = True
                continue
            prior_identity = ledger.identities.get(name)
            if identity is not None and prior_identity is not None and identity != prior_identity:
                kind = EVENT_NAME_REASSIGNED
            elif ledger.digests[name] != digest:
                kind = EVENT_DEFINITION_UPDATED
            else:
                kind = None
            if kind is not None:
                # Deliberate cache break: the declaration must describe what the
                # executor will actually run. Position is kept.
                ledger.declarations[name] = _canonical_or_copy(decl)
                ledger.digests[name] = digest
                if identity is not None:
                    ledger.identities[name] = identity
                events.append({"kind": kind, "tool": name, "provider": provider})
                changed = True

        # Withdrawn bookkeeping: a tool offered again stops being retained.
        for name in list(ledger.retained_since):
            if name in current_names:
                ledger.retained_since.pop(name, None)
                changed = True
        for name in ledger.order:
            if _is_native_key(name):
                continue
            if name not in current_names and name not in ledger.retained_since:
                ledger.retained_since[name] = ledger.seq + 1
                changed = True

        # Provider ceiling: drop the longest-withdrawn retained tools first.
        total = len(ledger.order)
        if max_tools is not None and total > max_tools:
            evictable = sorted(ledger.retained_since, key=lambda n: (ledger.retained_since[n], ledger.order.index(n)))
            evicted: list[str] = []
            while total > max_tools and evictable:
                victim = evictable.pop(0)
                ledger.order.remove(victim)
                for store in (ledger.declarations, ledger.digests, ledger.identities, ledger.retained_since):
                    store.pop(victim, None)
                evicted.append(victim)
                total -= 1
            if evicted:
                events.append(
                    {
                        "kind": EVENT_CEILING_EVICTION,
                        "provider": provider,
                        "tools": evicted,
                        "ceiling": max_tools,
                        "still_over": total > max_tools,
                    }
                )
                changed = True

        # THE ONE ORDER: authored tier first, by name inside each tier, whatever order the
        # declarations arrived in (P0.2, ``order_key``).
        ledger.order.sort(key=lambda name: order_key(name, ledger.authored))
        retained = [name for name in ledger.order if name in ledger.retained_since]
        if changed:
            ledger.seq += 1
        if events:
            ledger.deliberate_break = True
            if any(e.get("kind") == EVENT_BELT_REPLACED for e in events):
                ledger.deliberate_scope = None
            elif ledger.deliberate_scope is not None:
                for e in events:
                    ledger.deliberate_scope.update(e.get("tools") or [])
                    if e.get("tool"):
                        ledger.deliberate_scope.add(e["tool"])
            _queue_events(conversation_id, events)
        out = [_canonical_or_copy(ledger.declarations[name]) for name in ledger.order]
        # A tool offered again loses its old refusal reason, so a later
        # withdrawal for another cause is never refused with the stale one.
        reasons = _UNAVAILABLE_REASONS.get(conversation_id)
        if reasons:
            for name in list(reasons):
                if name in current_names:
                    reasons.pop(name, None)

    for event in events:
        vcprint(
            {"conversation_id": conversation_id, **event},
            "[tools] DELIBERATE prompt-cache break on the tools array (recorded)",
            color="yellow",
        )
    return StabilizeResult(
        declarations=out,
        appended=tuple(appended),
        retained=tuple(retained),
        events=tuple(events),
        applied=True,
    )


def consume_deliberate_break(conversation_id: str | None, provider: str | None) -> bool:
    """True once after the ledger made a deliberate, already-captured break."""
    return consume_deliberate_scope(conversation_id, provider) is not _NO_BREAK


_NO_BREAK: Any = object()


def consume_deliberate_scope(conversation_id: str | None, provider: str | None) -> Any:
    """The names the ledger's recorded break covers, consumed once.

    Returns ``_NO_BREAK`` when nothing was recorded, ``None`` for a whole-belt
    replacement (every change is covered), else the ``set`` of tool names the
    break touched. The wire guard excuses only a change confined to that set."""
    if not conversation_id:
        return _NO_BREAK
    with _LOCK:
        ledger = _LEDGERS.get((str(conversation_id), str(provider or "")))
        if ledger is None or not ledger.deliberate_break:
            return _NO_BREAK
        ledger.deliberate_break = False
        scope = None if ledger.deliberate_scope is None else set(ledger.deliberate_scope)
        ledger.deliberate_scope = set()
        return scope


def drain_events(conversation_id: str | None) -> list[dict[str, Any]]:
    """Deliberate-break events not yet announced (the orchestrator announces them)."""
    if not conversation_id:
        return []
    with _LOCK:
        return _PENDING_EVENTS.pop(str(conversation_id), [])


def note_unavailable(
    names: Iterable[str], reason: str, *, conversation_id: str | None = None
) -> None:
    """Record WHY tools were withdrawn, so a call to a retained declaration is
    refused with that reason instead of a generic one."""
    conversation_id = conversation_id or current_conversation_id()
    if not conversation_id:
        return
    with _LOCK:
        reasons = _UNAVAILABLE_REASONS.get(conversation_id)
        if reasons is None:
            reasons = {}
            _UNAVAILABLE_REASONS[conversation_id] = reasons
            while len(_UNAVAILABLE_REASONS) > MAX_TRACKED_CONVERSATIONS:
                _UNAVAILABLE_REASONS.popitem(last=False)
        else:
            _UNAVAILABLE_REASONS.move_to_end(conversation_id)
        for name in names:
            if isinstance(name, str) and name:
                reasons[_wire(name)] = reason


def retained_reason(*names: str, conversation_id: str | None = None) -> str | None:
    """If any of ``names`` is a declaration this conversation still sends but no
    longer offers, the refusal reason; else ``None``."""
    conversation_id = conversation_id or current_conversation_id()
    if not conversation_id:
        return None
    wires = {_wire(n) for n in names if isinstance(n, str) and n}
    with _LOCK:
        hit = None
        for (conv, _provider), ledger in _LEDGERS.items():
            if conv != conversation_id:
                continue
            found = wires & set(ledger.retained_since)
            if found:
                hit = next(iter(found))
                break
        if hit is None:
            return None
        return (_UNAVAILABLE_REASONS.get(conversation_id) or {}).get(
            hit, DEFAULT_UNAVAILABLE_REASON
        )


# ── DURABLE RECORD ───────────────────────────────────────────────────────────
# Rides ``UnifiedConfig.tool_declarations`` (``cx_conversation.config``).
# Stored shape: ``{provider: {"seq": n, "tools": [{"name", "wire" (the declaration as JSON text: its
# sent key order, which jsonb does not keep; "declaration", the object, only when no text could be
# made — and on records written before 2026-11-13, which still load),
# "identity"?, "retained_since"?}]}}``. A bare list (the first stored shape) reads
# as ``seq`` 0.

ToolDeclarationRecord = dict[str, Any]


def _record_seq(entry: Any) -> int:
    return int(entry.get("seq") or 0) if isinstance(entry, dict) else 0


def _record_tools(entry: Any) -> list[Any]:
    if isinstance(entry, dict):
        tools = entry.get("tools")
        return tools if isinstance(tools, list) else []
    return entry if isinstance(entry, list) else []


#: Record item key holding a declaration as JSON TEXT, so its key order survives jsonb.
WIRE_KEY = "wire"


def _declaration_of(item: dict[str, Any]) -> Any:
    """The declaration as it was sent: from its JSON text when recorded, else the stored object."""
    wire = item.get(WIRE_KEY)
    if isinstance(wire, str):
        try:
            decl = json.loads(wire)
        except ValueError:
            decl = None
        if isinstance(decl, dict):
            return decl
    return item.get("declaration")


def hydrate_from_record(
    conversation_id: str | None, record: ToolDeclarationRecord | None
) -> bool:
    """Seed memory from the persisted record. The NEWER of the two (by ``seq``)
    wins: a conversation that moved to another server and back resumes with the
    array the other server last sent. Returns True when anything was restored."""
    if not conversation_id or not isinstance(record, dict):
        return False
    restored = False
    with _LOCK:
        for provider, entry in record.items():
            key = (str(conversation_id), str(provider))
            existing = _LEDGERS.get(key)
            seq = _record_seq(entry)
            if existing is not None and existing.seq >= seq:
                continue
            ledger = _Ledger(seq=seq)
            for item in _record_tools(entry):
                if not isinstance(item, dict):
                    continue
                name = item.get("name")
                decl = _declaration_of(item)
                if not isinstance(name, str) or not isinstance(decl, dict) or name in ledger.declarations:
                    continue
                ledger.order.append(name)
                ledger.declarations[name] = copy.deepcopy(decl)
                ledger.digests[name] = _digest(decl)
                if isinstance(item.get("identity"), str):
                    ledger.identities[name] = item["identity"]
                if isinstance(item.get("retained_since"), int):
                    ledger.retained_since[name] = item["retained_since"]
                if item.get("authored") is True:
                    ledger.authored.add(name)
            if ledger.order:
                # A record written before P0.2 holds the old append order, and one written before
                # the tiers holds one flat name order: re-sorted here, once (the next send names
                # the authored tier again).
                ledger.order.sort(key=lambda name: order_key(name, ledger.authored))
                _LEDGERS[key] = ledger
                _LEDGERS.move_to_end(key)
                restored = True
        while len(_LEDGERS) > MAX_TRACKED_CONVERSATIONS:
            _LEDGERS.popitem(last=False)
    if restored:
        # The array the provider last saw is the record's (another worker sent it and recorded any break
        # there), so the wire guard's memory of this worker's own older block is stale.
        from matrx_ai.providers.cache_guard import forget_tool_declarations

        forget_tool_declarations(str(conversation_id))
    return restored


def export_record(conversation_id: str | None) -> ToolDeclarationRecord | None:
    """The persistable record for ``conversation_id`` (None when there is none)."""
    if not conversation_id:
        return None
    with _LOCK:
        out: ToolDeclarationRecord = {}
        for (conv, provider), ledger in _LEDGERS.items():
            if conv != str(conversation_id) or not ledger.order:
                continue
            tools = []
            for name in ledger.order:
                # THE EXACT KEY ORDER SENT (jsonb reorders object keys): a follow-up turn on
                # another worker re-sends these bytes, never the jsonb-ordered copy (static seal
                # finding 2026-11-12: input_schema keys moved and broke the tools prefix). The wire
                # text IS the declaration: the object copy is written only when no text could be
                # made (each tool stored once; records written before still load).
                item: dict[str, Any] = {"name": name}
                try:
                    item[WIRE_KEY] = json.dumps(ledger.declarations[name], ensure_ascii=False, default=str)
                except Exception:  # noqa: BLE001 — never lose the declaration: keep the object
                    item["declaration"] = copy.deepcopy(ledger.declarations[name])
                if name in ledger.identities:
                    item["identity"] = ledger.identities[name]
                if name in ledger.retained_since:
                    item["retained_since"] = ledger.retained_since[name]
                if name in ledger.authored:
                    item["authored"] = True
                tools.append(item)
            out[provider] = {"seq": ledger.seq, "tools": tools}
    return out or None


def record_is_newer(candidate: Any, stored: Any) -> bool:
    """True when ``candidate`` carries a higher ``seq`` than ``stored`` for any
    provider (a write that would not move any provider forward is skipped)."""
    if not isinstance(candidate, dict):
        return False
    stored = stored if isinstance(stored, dict) else {}
    return any(_record_seq(entry) > _record_seq(stored.get(provider)) for provider, entry in candidate.items())


def newer_record(held: Any, stored: Any) -> ToolDeclarationRecord | None:
    """Per provider, the entry with the higher ``seq`` of ``held`` (this
    server's copy) and ``stored`` (the conversation row). A server that last
    ran this conversation turns ago holds an older array than the row when
    another server appended since (adversarial I1, 2026-10-18)."""
    held = held if isinstance(held, dict) else {}
    stored = stored if isinstance(stored, dict) else {}
    out: ToolDeclarationRecord = {}
    for provider in [*held, *(p for p in stored if p not in held)]:
        mine, theirs = held.get(provider), stored.get(provider)
        out[provider] = copy.deepcopy(theirs if _record_seq(theirs) > _record_seq(mine) else mine)
    return out or None


def end_loop(conversation_id: str) -> None:
    """A loop for ``conversation_id`` ended on this worker: drop its undrained
    events (they belong to that loop) but KEEP its ledger, so the next turn
    here appends to the array this worker last sent even when the durable
    record has not reached the row (or the turn's path never loads it). The
    LRU bound caps memory; ``hydrate_from_record`` lets a newer record win."""
    with _LOCK:
        _PENDING_EVENTS.pop(str(conversation_id), None)


def forget_conversation(conversation_id: str) -> None:
    """Release a conversation's in-memory state (its record stays durable)."""
    with _LOCK:
        for key in [k for k in _LEDGERS if k[0] == str(conversation_id)]:
            _LEDGERS.pop(key, None)
        _UNAVAILABLE_REASONS.pop(str(conversation_id), None)
        _PENDING_EVENTS.pop(str(conversation_id), None)


def reset_for_tests() -> None:
    with _LOCK:
        _LEDGERS.clear()
        _UNAVAILABLE_REASONS.clear()
        _PENDING_EVENTS.clear()
