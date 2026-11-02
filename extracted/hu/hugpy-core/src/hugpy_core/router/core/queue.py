"""Central's queue above the boxes — PURE: tickets in, the ones to dispatch out.

Operator 2026-10-14: "the router needs to be accompanied by a queue mechanism".
A call whose allocated boxes are all busy or loading takes a ticket here instead of
piling onto a box; when a box's state changes (its link's event — nothing periodic)
the waiting tickets are walked in order and each whose candidate box is FREE is
dispatched to it. The order is the wrapper's own admission policy (serve/admission.py
on the box): time-to-output first — tickets WITH history (the model's measured load
and decode rates, from the mirrored call log) sorted by predicted time take the
slots of tickets WITHOUT history, which keep their arrival slots; a caller's own
tickets (a group) keep their arrival order; background work (grading, smoke tests,
benchmarks) never goes ahead of a real call; a ticket that waited its window goes
next; a head bypassed `bypass_max` times blocks later tickets from the boxes it
could use. Each box's own queue stays underneath as the last admission step.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple


@dataclass
class Ticket:
    id: str
    seq: int
    request_id: str
    model: str
    options: Optional[str]
    group: str                       # the caller (header X-Hugpy-Group, else its address)
    arrived_at: float
    boxes: List[str]                 # the allocated candidates, best first (the decision)
    background: bool = False
    max_wait_s: float = 120.0
    known: bool = False              # the model has decode history on a candidate box
    load_s: Optional[float] = None
    predicted_s: Optional[float] = None
    bypassed: int = 0
    bypassed_by: List[str] = field(default_factory=list)
    state: str = "waiting"           # waiting | dispatched | expired | left
    box: Optional[str] = None
    reason: str = ""


def eta_of(t: Ticket) -> float:
    return float(t.load_s or 0.0) + float(t.predicted_s or 0.0)


def eta_order(fg: List[Ticket]) -> List[Ticket]:
    """Time-to-output order: known tickets by eta take the slots of the unknown
    ones (which keep arrival order); a group's members keep their arrival order."""
    slots = sorted(fg, key=lambda t: t.seq)
    known = iter(sorted((t for t in slots if t.known), key=lambda t: (eta_of(t), t.seq)))
    out = [t if not t.known else next(known) for t in slots]
    for g in {t.group for t in out}:
        pos = [i for i, t in enumerate(out) if t.group == g]
        for i, m in zip(pos, sorted((out[i] for i in pos), key=lambda t: t.seq)):
            out[i] = m
    return out


def order(waiting: List[Ticket], now: float) -> List[Ticket]:
    """The dispatch order: aged tickets (waited their window) oldest first, then the
    eta order of the foreground, then the background in arrival order."""
    fg = [t for t in waiting if not t.background]
    bg = sorted((t for t in waiting if t.background), key=lambda t: t.seq)
    aged = sorted((t for t in fg if (now - t.arrived_at) >= t.max_wait_s), key=lambda t: t.seq)
    rest = eta_order([t for t in fg if t not in aged])
    return aged + rest + bg


def choose(waiting: List[Ticket], free: Callable[[str, str], bool], now: float,
           bypass_max: int = 3) -> List[Tuple[Ticket, str, str]]:
    """Which waiting tickets go now and where: [(ticket, box, reason)]. Walks the
    order; a ticket takes the first of its candidate boxes that is free (for its
    model) and not taken in this round. A ticket left waiting while a later one
    takes a box it could have used is bypassed; past `bypass_max` it holds those
    boxes for itself."""
    out, taken, held = [], set(), {}
    for t in waiting:                            # a head bypassed past the cap holds its boxes
        if t.state == "waiting" and t.bypassed >= bypass_max:
            for b in t.boxes:
                held.setdefault(b, t.id)
    for t in order(waiting, now):
        if t.state != "waiting":
            continue
        candidates = [b for b in t.boxes if b not in taken and held.get(b, t.id) == t.id]
        box = next((b for b in candidates if free(b, t.model)), None)
        if box is None:
            continue
        for w in waiting:
            if w is not t and w.state == "waiting" and box in w.boxes and w.seq < t.seq:
                w.bypassed += 1
                w.bypassed_by.append(t.id)
        taken.add(box)
        why = ("waited its window" if (now - t.arrived_at) >= t.max_wait_s and not t.background
               else (f"shortest time-to-output: eta {eta_of(t):.1f}s" if t.known else f"no history for {t.model}: arrival order"))
        out.append((t, box, why))
    return out


def snapshot(waiting: List[Ticket], now: float, *, policy: str, bypass_max: int) -> dict:
    ordered = order(waiting, now)
    return {"policy": policy, "bypass_max": bypass_max,
            "tickets": [{"id": t.id, "request_id": t.request_id, "model": t.model, "options": t.options,
                         "group": t.group, "background": t.background, "boxes": list(t.boxes), "known": t.known,
                         "eta_s": round(eta_of(t), 3) if t.known else None, "load_s": t.load_s,
                         "predicted_s": t.predicted_s, "bypassed": t.bypassed, "bypassed_by": list(t.bypassed_by),
                         "arrived_at": t.arrived_at, "waiting_s": round(now - t.arrived_at, 3),
                         "position": i + 1, "state": t.state, "box": t.box, "reason": t.reason or None}
                        for i, t in enumerate(ordered)]}


__all__ = ["Ticket", "eta_of", "eta_order", "order", "choose", "snapshot"]
