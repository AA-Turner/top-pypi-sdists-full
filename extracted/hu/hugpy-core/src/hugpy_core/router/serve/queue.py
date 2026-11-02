"""Central's queue in the running router: tickets wait on events, never on a clock.

A ticket is dispatched by `kick` — called when a box link reports a change (the
links' on_change callbacks), when a call leaves, and once on arrival. `free(box, model)` reads
the box as its link last saw it: the model resident, healthy and not busy; or not
resident on a box with nothing busy or loading (the box's own evict-to-fit then
places it). A ticket that waited its whole window answers 503 (queue_timeout).
Central persists tickets (persist) and predicts time-to-output (predict) when it
is here; the pure router keeps arrival order.
"""
from __future__ import annotations

import asyncio
import os
import time
import uuid
from typing import Callable, Dict, List, Optional

from aiohttp import web

from hugpy_core.router.core import queue as Q
from hugpy_core.router.imports import constants as C

QUEUE = web.AppKey("central_queue", object)


def free_by_registry(registry) -> Callable[[str, str], bool]:
    def free(box_name: str, model: str) -> bool:
        link = registry.link(box_name)
        if link is None:
            return False
        box = link.box()
        if not box.online or box.blocked:
            return False
        mine = next((r for r in box.residents if r.key == model), None)
        if mine is not None:
            return mine.healthy and mine.state in ("idle", "serving") and not mine.busy
        return not any(r.busy or r.state == "loading" for r in box.residents)
    return free


def is_background(body) -> bool:
    meta = (body or {}).get("metadata") if isinstance(body, dict) else None
    if not isinstance(meta, dict):
        return False
    return bool(meta.get("background")) or str(meta.get("intent") or "").lower() in ("grading", "smoke", "smoke-test", "benchmark")


class CentralQueue:
    def __init__(self, *, policy: Optional[str] = None, bypass_max: Optional[int] = None,
                 max_wait_s: Optional[float] = None, predict=None, persist=None, now=time.time):
        self.policy = (policy or os.environ.get(C.ENV_QUEUE_POLICY) or C.QUEUE_POLICY_DEFAULT).strip().lower()
        try:
            self.bypass_max = int(bypass_max if bypass_max is not None else os.environ.get(C.ENV_QUEUE_BYPASS_MAX, C.QUEUE_BYPASS_MAX_DEFAULT))
        except ValueError:
            self.bypass_max = C.QUEUE_BYPASS_MAX_DEFAULT
        try:
            self.max_wait_s = float(max_wait_s if max_wait_s is not None else os.environ.get(C.ENV_QUEUE_MAX_WAIT_S, C.QUEUE_MAX_WAIT_DEFAULT_S))
        except ValueError:
            self.max_wait_s = float(C.QUEUE_MAX_WAIT_DEFAULT_S)
        self.predict = predict          # (model, options, box, body) -> {known, load_s, output_s} | None
        self.persist = persist          # (event, ticket) -> None, never raises
        self._now = now
        self._seq = 0
        self._waiting: List[Q.Ticket] = []
        self._events: Dict[str, asyncio.Event] = {}
        self.on_change: Optional[Callable[[Q.Ticket, str], None]] = None     # (ticket, event) → central raises an event

    # ── tickets ──
    def ticket(self, request_id: str, model: str, options: Optional[str], group: str, boxes: List[str],
               body=None, background: Optional[bool] = None) -> Q.Ticket:
        self._seq += 1
        t = Q.Ticket(id="tk-" + uuid.uuid4().hex[:12], seq=self._seq, request_id=request_id, model=model,
                     options=options, group=group, arrived_at=self._now(), boxes=list(boxes),
                     background=is_background(body) if background is None else background, max_wait_s=self.max_wait_s)
        if self.predict is not None and boxes:
            try:
                p = self.predict(model, options, boxes[0], body) or {}
            except Exception:  # noqa: BLE001 — a prediction never blocks a call
                p = {}
            if p.get("known"):
                t.known, t.load_s, t.predicted_s = True, p.get("load_s"), p.get("output_s")
        self._waiting.append(t)
        self._events[t.id] = asyncio.Event()
        self._record("queued", t)
        return t

    async def wait(self, t: Q.Ticket, free: Callable[[str, str], bool]) -> Optional[str]:
        """Block until the ticket is dispatched (its box), or None after its window."""
        self.kick(free)
        if t.state == "dispatched":
            return t.box
        try:
            await asyncio.wait_for(self._events[t.id].wait(), timeout=max(0.0, t.max_wait_s - (self._now() - t.arrived_at)))
        except asyncio.TimeoutError:
            if t.state == "waiting":
                t.state, t.reason = "expired", f"no allocated box freed within {t.max_wait_s:.0f}s"
                self._drop(t)
                self._record("expired", t)
                return None
        return t.box

    def kick(self, free: Callable[[str, str], bool]) -> int:
        """Dispatch every waiting ticket whose candidate box is free; returns how many."""
        n = 0
        for t, box, why in Q.choose(self._waiting, free, self._now(), self.bypass_max):
            t.state, t.box, t.reason = "dispatched", box, why
            self._drop(t)
            self._events[t.id].set()
            self._record("dispatched", t)
            n += 1
        return n

    def leave(self, t: Q.Ticket, free: Optional[Callable[[str, str], bool]] = None) -> None:
        """The call on this ticket is over (any outcome): forget it, let the next one in."""
        self._events.pop(t.id, None)
        if t.state == "waiting":
            t.state = "left"
            self._drop(t)
            self._record("left", t)
        if free is not None:
            self.kick(free)

    def _drop(self, t: Q.Ticket) -> None:
        self._waiting = [w for w in self._waiting if w is not t]

    def _record(self, event: str, t: Q.Ticket) -> None:
        if self.persist is not None:
            try:
                self.persist(event, t)
            except Exception:  # noqa: BLE001
                pass
        if self.on_change is not None:
            try:
                self.on_change(t, event)
            except Exception:  # noqa: BLE001
                pass

    # ── reads ──
    def snapshot(self) -> dict:
        return Q.snapshot(self._waiting, self._now(), policy=self.policy, bypass_max=self.bypass_max)

    def position(self, t: Q.Ticket) -> Optional[int]:
        for i, w in enumerate(Q.order(self._waiting, self._now())):
            if w is t:
                return i + 1
        return None

    # ── the event wiring ──
    def attach(self, registry, free: Callable[[str, str], bool]) -> None:
        """Kick on every box link change (the links' on_change callbacks) — nothing periodic."""
        registry.on_change.append(lambda _link: self.kick(free))


__all__ = ["CentralQueue", "QUEUE", "free_by_registry", "is_background"]
