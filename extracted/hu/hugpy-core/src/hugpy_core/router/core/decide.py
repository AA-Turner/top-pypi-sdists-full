"""The routing decision — pure: facts in, ranked boxes out.

Ported from hugpy-core's relay/pick.py (0.1.70), with the facts swapped (box links
instead of hugpy_wrapper Postgres) and one precision rule added:

1. **Pin** (`alloc.worker`) is a contract: that box or a refusal with the reason —
   never rerouted.
2. **Eligible**: online, the call's pool, not blocked, not already tried for this call.
3. **Serving-first**: a box where the model is resident, healthy and not loading AND
   its known request identity matches — legacy suffix and structured JSON knobs.
   This is an advisory shortcut; Wrapper resolves defaults and confirms whether
   reuse is possible. Idle before busy, then most recently used.
4. **Allocation path** (operator 2026-10-14: "allocation is known prior to a call's
   placement… the router is not supposed to be blind"): with central's derived
   allocation, a box qualifies only when its allocation for the model says the
   call's options FIT (the wrapper's own verdict: the fit map per quant per option);
   a box with no verdict yet, or none that fits, is refused with that reason. Ranked:
   not busy/loading first, then the room the box reports, then least recently
   picked, then name. Without an allocation (the pure router of the tests) the
   catalog rule stands: boxes whose catalog holds the model, ranked by room.
5. **Refusal**: nothing qualifies — every box's reason, so the caller sees why.

The caller (serve/proxy.py) sends the call to the FIRST box only; a refusal before
the first byte is recorded as a fact against the allocation and returned, never
re-sent to another box.
"""
from __future__ import annotations

from typing import Dict, Iterable, Optional, Set, Tuple

from hugpy_core.router.core.types import Box, CallSpec, Decision, Resident

Contracts = Dict[Tuple[str, str], object]           # (box, model) -> last completed request identity
Allocation = Dict[Tuple[str, str], dict]             # (box, model) -> central's model_workers row

MODE_TOKENS = ("gpu-only", "max-gpu", "max-ram", "ram-only", "moe",
               "gpu-max", "ram-max", "ram-swap", "disk_mmap-only", "disk_mmap-max")


def options_fit(alloc: dict, options: Optional[str]) -> Tuple[Optional[bool], str]:
    """Whether the call's options fit on the box by its allocation: (True/False, why),
    or (None, why) when the box has no feasibility verdict for the model yet. The
    options are the wrapper's variant syntax (`quant@mode@4bit…`, any order)."""
    fit = alloc.get("fit") or {}
    if not isinstance(fit, dict) or not fit:
        fa = alloc.get("fits_any")
        if fa is None:
            return None, "no feasibility verdict yet"
        return (True, "fits (any option)") if fa else (False, "nothing fits")
    tokens = [t.strip().lower() for t in (options or "").split("@") if t.strip()]
    by_lower = {q.lower(): q for q in fit}
    quant = next((t for t in tokens if t in by_lower), None)
    modes = [t for t in tokens if t in MODE_TOKENS]
    bnb = "4bit" in tokens
    if bnb:
        keys = ["4bit-" + m for m in (modes or ["gpu-only", "max-gpu"]) if m in ("gpu-only", "max-gpu")]
    else:
        keys = modes
    tables = [(by_lower[quant], fit[by_lower[quant]])] if quant else list(fit.items())
    for q, table in tables:
        table = table if isinstance(table, dict) else {}
        from hugpy_core.intake.schema import cell
        ok = any(bool(cell(table, k)) for k in keys) if keys else any(bool(v) for v in table.values())
        if ok:
            return True, "fits as " + q + (" " + "/".join(keys) if keys else "")
    want = (quant or "any quant") + ((" " + "/".join(keys)) if keys else "")
    return False, f"{want} does not fit"


def _resident(box: Box, model: str) -> Optional[Resident]:
    for r in box.residents:
        if r.key == model:
            return r
    return None


def _serving(r: Optional[Resident]) -> bool:
    return r is not None and r.healthy and r.state in ("idle", "serving")


def _contract_ok(box: Box, call: CallSpec, contracts: Contracts) -> bool:
    """Only a known request identity can use the resident-match shortcut.

    Legacy in-memory entries describe suffix-only requests. Matching requests
    remain advisory: Wrapper resolves defaults and rechecks the live contract.
    """
    key = (box.name, call.model)
    if key not in contracts:
        return False
    prior = contracts[key]
    if isinstance(prior, tuple):
        if len(prior) == 3:
            return (box.observation_identity is not None
                    and prior == (*call.contract_key, box.observation_identity))
        if box.observation_identity is not None:
            return False  # an unscoped legacy entry cannot confirm this process
        return prior == call.contract_key
    if box.observation_identity is not None:
        return False
    return call.knobs_json == "{}" and prior == call.options


def _why_not(box: Box, call: CallSpec, tried: Set[str]) -> Optional[str]:
    if box.name in tried:
        return "already tried for this call"
    if not box.online:
        return "offline"
    if box.blocked:
        return "blocked by the operator"
    if (box.pool or "") != (call.pool or ""):
        return f"pool {box.pool!r} (call wants {call.pool!r})"
    if call.model not in box.models and _resident(box, call.model) is None:
        return "does not have the model"
    return None


def _allocated(box: Box, call: CallSpec, allocation: Allocation) -> Tuple[bool, str]:
    """(qualifies, why) for the allocation path on this box."""
    a = allocation.get((box.name, call.model))
    if a is None:
        return False, "not in central's allocation yet (no derivation for this box and model)"
    if a.get("available") is False:
        return False, "central marks it unavailable"
    fits, why = options_fit(a, call.options)
    if fits and a.get("needs_copy"):
        return False, "allocation: " + why + " — but the box holds no copy of the file (a transfer is needed)"
    if fits:
        return True, "allocated: " + why
    return False, "allocation: " + why


def decide(call: CallSpec, boxes: Iterable[Box], contracts: Optional[Contracts] = None,
           tried: Optional[Set[str]] = None, allocation: Optional[Allocation] = None) -> Decision:
    contracts = contracts or {}
    tried = set(tried or ())
    boxes = list(boxes)
    d = Decision()

    if call.pin:
        box = next((b for b in boxes if b.name == call.pin), None)
        if box is None:
            d.refused[call.pin] = "requested box is not known to this router"
        else:
            reason = _why_not(box, call, tried)
            if reason is None and allocation is not None and not (
                    _serving(_resident(box, call.model)) and _contract_ok(box, call, contracts)):
                ok, why = _allocated(box, call, allocation)
                reason = None if ok else why
            if reason:
                d.refused[box.name] = reason
            else:
                d.boxes, d.path = [box.name], "pin"
                d.why[box.name] = "pinned by the call"
        if not d.ok:
            d.path = "refused"
        return d

    eligible = []
    for b in boxes:
        reason = _why_not(b, call, tried)
        if reason:
            d.refused[b.name] = reason
        else:
            eligible.append(b)

    # A wildcard with no allocation is a last route, even when it happens to
    # have a resident. A normal allocated worker gets first refusal.
    fallback = [b for b in eligible if allocation is not None and b.wildcard
                and (b.name, call.model) not in allocation]
    serving = [b for b in eligible if b not in fallback
               and _serving(_resident(b, call.model)) and _contract_ok(b, call, contracts)]
    serving.sort(key=lambda b: (_resident(b, call.model).busy, -_resident(b, call.model).last_used, b.name))
    for b in serving:
        r = _resident(b, call.model)
        d.why[b.name] = "serving it now" + (" (busy)" if r.busy else "") + \
            (f" with {call.options!r}" if call.options else "")

    if allocation is None:
        loadable = [b for b in eligible if b not in serving and call.model in b.models]
        loadable.sort(key=lambda b: (-(b.room_gpu or 0), b.last_picked, b.name))
        for b in loadable:
            r = _resident(b, call.model)
            d.why[b.name] = ("loaded with other settings — the box reloads it" if _serving(r) else "can load it") + \
                (f"; room {b.room_gpu:,} B" if b.room_gpu is not None else "")
    else:
        loadable, detail = [], {}
        for b in eligible:
            if b in serving or b in fallback:
                continue
            ok, why = _allocated(b, call, allocation)
            if ok:
                loadable.append(b)
                detail[b.name] = why
            else:
                d.refused[b.name] = why

        def _busy(b):
            a = allocation.get((b.name, call.model)) or {}
            return bool(a.get("busy")) or bool(a.get("loading"))
        loadable.sort(key=lambda b: (_busy(b), -(b.room_gpu or 0), b.last_picked, b.name))
        for b in loadable:
            r = _resident(b, call.model)
            d.why[b.name] = detail[b.name] + ("; loaded with other settings — the box reloads it" if _serving(r) else "") + \
                (f"; room {b.room_gpu:,} B" if b.room_gpu is not None else "")

    if not serving and not loadable and fallback:
        fallback.sort(key=lambda b: (
            not (_serving(_resident(b, call.model)) and _contract_ok(b, call, contracts)),
            -(b.room_gpu or 0), b.last_picked, b.name))
        for b in fallback:
            d.why[b.name] = "wildcard: no central allocation for this model"
    else:
        fallback = []
    d.boxes = [b.name for b in serving] + [b.name for b in loadable] + [b.name for b in fallback]
    d.path = "serving" if serving else ("load" if loadable else ("wildcard" if fallback else "refused"))
    for b in eligible:
        if b.name not in d.boxes and b.name not in d.refused:
            d.refused[b.name] = "has neither the model loaded nor in its catalog"
    return d
