"""The conversation's tool-declaration ledger: the provider ``tools`` array is
append-only for the life of a conversation, and every exception is DELIBERATE and
recorded.

Why: on Anthropic the cached prefix is ``tools -> system -> messages``. Any change
at tool position N throws away everything after it, so removing, reordering or
re-describing ONE tool mid-conversation re-writes the whole conversation at the
cache-write price. Measured on real jobs (common-docs
``projects/agent-evaluation/reports/tool-list-cache-stability.md``): a loop-guard
removal of ``records`` re-wrote 170,818 tokens (92.3 cents) in one request, and a
desktop authority gate flipping ``local_file``/``local_shell`` in and out changed
the list 7-8 times in one turn.

Many upstream paths legitimately change the EFFECTIVE toolset (loop guard,
discovery loaders, authority exclusions, delegation/capability filters, the
re-merge after suspend/resume or crash recovery). The fix lives at the one
boundary every translator uses (``BaseTranslator.build_provider_tools``):

* a declaration seen once stays in its first position;
* a declaration no longer offered stays declared (RETAINED); a call to it is
  refused by the executor with a reason (``retained_reason``);
* a declaration seen for the first time is APPENDED after every earlier one.

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
  and exports after it; ``forget_conversation`` releases memory when a loop ends,
  so a worker holds ledgers only for loops in flight (plus an LRU bound).
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

#: LRU bound on tracked (conversation, provider) ledgers per worker. Ledgers are
#: released when their loop ends (``forget_conversation``); this only bounds a
#: worker with many loops in flight.
MAX_TRACKED_CONVERSATIONS = 256

#: Reason given when a retained tool is called and no remover recorded why.
DEFAULT_UNAVAILABLE_REASON = (
    "it is no longer available in this conversation (the source that provided it "
    "withdrew it)"
)

EVENT_DEFINITION_UPDATED = "tool_definition_updated"
EVENT_NAME_REASSIGNED = "tool_name_reassigned"
EVENT_CEILING_EVICTION = "tool_ceiling_eviction"
EVENT_BELT_REPLACED = "tool_belt_replaced"


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


def stabilize_declarations(
    provider: str,
    declarations: list[dict[str, Any]],
    *,
    name_of: Callable[[dict[str, Any]], str | None],
    conversation_id: str | None = None,
    max_tools: int | None = None,
    identities: dict[str, str] | None = None,
) -> StabilizeResult:
    """Return the conversation-stable ``tools`` array for this request.

    ``declarations`` are provider-formatted, wire-named declarations the current
    request would send; ``name_of`` extracts a name (``None`` for provider-native
    tools, which ride at the end untracked). ``max_tools`` is the provider's
    tool-count ceiling (None = no known ceiling). ``identities`` maps a recyclable
    wire name to its current target (defaults to this request's agent projections).
    """
    conversation_id = conversation_id or current_conversation_id()
    if not conversation_id or not declarations:
        return StabilizeResult(declarations=declarations)

    named: list[tuple[str, dict[str, Any]]] = []
    nameless: list[dict[str, Any]] = []
    for decl in declarations:
        name = name_of(decl)
        if name is None:
            nameless.append(decl)
        else:
            named.append((name, decl))
    if not named:
        return StabilizeResult(declarations=declarations)
    if identities is None:
        identities = projected_tool_identities()

    key = (conversation_id, provider)
    events: list[dict[str, Any]] = []
    with _LOCK:
        ledger = _LEDGERS.get(key)
        current_names = {name for name, _ in named}
        if ledger is not None and ledger.order and not (current_names & set(ledger.order)):
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
                    "previous_tools": list(ledger.order),
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

        appended: list[str] = []
        for name, decl in named:
            digest = _digest(decl)
            identity = identities.get(name)
            if name not in ledger.declarations:
                ledger.order.append(name)
                ledger.declarations[name] = copy.deepcopy(decl)
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
                ledger.declarations[name] = copy.deepcopy(decl)
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
            if name not in current_names and name not in ledger.retained_since:
                ledger.retained_since[name] = ledger.seq + 1
                changed = True

        # Provider ceiling: drop the longest-withdrawn retained tools first.
        total = len(ledger.order) + len(nameless)
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
        out = [copy.deepcopy(ledger.declarations[name]) for name in ledger.order]
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
        declarations=out + nameless,
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
# Stored shape: ``{provider: {"seq": n, "tools": [{"name", "declaration",
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
                decl = item.get("declaration")
                if not isinstance(name, str) or not isinstance(decl, dict) or name in ledger.declarations:
                    continue
                ledger.order.append(name)
                ledger.declarations[name] = copy.deepcopy(decl)
                ledger.digests[name] = _digest(decl)
                if isinstance(item.get("identity"), str):
                    ledger.identities[name] = item["identity"]
                if isinstance(item.get("retained_since"), int):
                    ledger.retained_since[name] = item["retained_since"]
            if ledger.order:
                _LEDGERS[key] = ledger
                _LEDGERS.move_to_end(key)
                restored = True
        while len(_LEDGERS) > MAX_TRACKED_CONVERSATIONS:
            _LEDGERS.popitem(last=False)
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
                item: dict[str, Any] = {
                    "name": name,
                    "declaration": copy.deepcopy(ledger.declarations[name]),
                }
                if name in ledger.identities:
                    item["identity"] = ledger.identities[name]
                if name in ledger.retained_since:
                    item["retained_since"] = ledger.retained_since[name]
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
