"""Paced dispatch — a For each that sends in waves and stops on what it gathered (G3).

packages/matrx-graph/matrx_graph/executor/FEATURE.md § For each: `until`, `wave_size` and the item cap, 2026-11-02. A ``control.map`` with ``until`` and / or
``wave_size`` stamps every Send of its dispatch with the same ``pace``
(``{until, wave_size, scope, total}``, ``nodes/control/map.py::pace_of``). The scheduler keeps ONE
:class:`PacedDispatch` per ``(dispatch_id, target)`` and asks it before each item starts:

* **Waves.** Items go in index order. With ``wave_size`` the first wave is the first ``wave_size``
  items; the next wave opens only when every item of the one before has settled, and its size is
  read again over what came back. A size of 0 or less sends no more.
* **Until.** Read when an item gets its turn (after its concurrency slot, so it sees every result
  that landed while it waited) and at each wave boundary. Once true nothing new is sent: an item
  already working finishes and saves (the Stop semantics of packages/matrx-graph/matrx_graph/executor/FEATURE.md § Stop and Pause mid-wave); every item not yet started
  is skipped with :attr:`PacedDispatch.reason` and recorded like any skip, so a resume replays the
  same answer.
* **Stop / Pause** reach an item waiting for its wave through the scheduler's own control read.

The expression scope (``inputs`` in the sandbox): the dispatcher's other inputs (``scope``), plus
``results`` (each succeeded item's result, in item order), ``settled`` (``{item_index, status,
value}`` per settled item), ``sent`` (items started), ``total`` and ``items`` is NOT included — the
list itself lives in the payloads; ``total`` is its length.

An item that asks a question (interrupt) settles here as ``waiting``: it counts toward its wave being
done but adds no result.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from matrx_graph.errors import ExecutionError

logger = logging.getLogger("matrx_graph.executor.paced_dispatch")

#: How often an item waiting for its wave re-reads the run's Stop / Pause.
WAVE_STOP_POLL_SECONDS = 1.0  # protocol-constant: internal stop-poll tick, a latency/CPU trade-off with no admin-facing meaning

ADMIT = "admit"
HELD = "held"
UNTIL = "until"


class PacedDispatch:
    """The pace of one dispatch's items to one target."""

    def __init__(self, target: str, pace: dict[str, Any]) -> None:
        self.target = target
        self.until: str | None = pace.get("until") or None
        self.wave_size: str | None = pace.get("wave_size") or None
        #: Seconds before each wave after the first (``wave_gap``): a provider's spacing, paced
        #: visibly on the step. ``_not_before`` is when the open wave may start (monotonic clock).
        self.wave_gap: str | None = pace.get("wave_gap") or None
        self._not_before = 0.0
        self.scope: dict[str, Any] = dict(pace.get("scope") or {})
        self.total = int(pace.get("total") or 0)
        self._settled: dict[int, tuple[str, Any]] = {}
        self._started: set[int] = set()
        self._registered: set[int] = set()
        self._stopped: str | None = None
        self._wave_start = 0
        self._wave_end: int | None = None if self.wave_size else self.total
        self._changed = asyncio.Event()

    # -- the scope ---------------------------------------------------------------------------
    def _inputs(self) -> dict[str, Any]:
        ordered = sorted(self._settled.items())
        return {
            **self.scope,
            "results": [value for _i, (status, value) in ordered if status == "succeeded"],
            "settled": [{"item_index": i, "status": status, "value": value} for i, (status, value) in ordered],
            "sent": len(self._started),
            "total": self.total,
        }

    def _eval(self, expr: str, what: str) -> Any:
        from matrx_graph.nodes._sandbox import safe_eval  # lazy: the scheduler imports this module

        try:
            return safe_eval(expr, self._inputs())
        except ExecutionError as exc:
            raise ExecutionError(f"For each '{self.target}': its {what} {expr!r} could not be read: {exc}") from exc

    @property
    def reason(self) -> str:
        return self._stopped or "not sent"

    def until_met(self) -> bool:
        """True once nothing more may be sent (``until`` true, or a wave of 0)."""
        if self._stopped is not None:
            return True
        if self.until is not None and bool(self._eval(self.until, "'until'")):
            self._stopped = f"not sent: 'until' ({self.until}) was true after {len(self._settled)} item(s)"
            self._changed.set()
            return True
        return False

    def _open_next_wave(self) -> None:
        if self.wave_size is None:
            return
        while self._wave_end is None or (
            self._wave_end < self.total
            and all(i in self._settled for i in self._registered if self._wave_start <= i < self._wave_end)
        ):
            if self._wave_end is not None and self.until_met():
                return
            raw = self._eval(self.wave_size, "wave size")
            try:
                size = int(raw)
            except (TypeError, ValueError) as exc:
                raise ExecutionError(
                    f"For each '{self.target}': its wave size {self.wave_size!r} gave {raw!r}, not a whole number."
                ) from exc
            if size <= 0:
                self._stopped = f"not sent: the wave size ({self.wave_size}) was {size} after {len(self._settled)} item(s)"
                self._changed.set()
                return
            first_wave = self._wave_end is None
            self._wave_start = self._wave_end or 0
            self._wave_end = min(self.total, self._wave_start + size)
            if self.wave_gap is not None and not first_wave:
                raw_gap = self._eval(self.wave_gap, "wave gap")
                try:
                    gap = float(raw_gap or 0)
                except (TypeError, ValueError) as exc:
                    raise ExecutionError(
                        f"For each '{self.target}': its wave gap {self.wave_gap!r} gave {raw_gap!r}, not a number of seconds."
                    ) from exc
                self._not_before = time.monotonic() + max(0.0, gap)
            self._changed.set()
            if not any(self._wave_start <= i < self._wave_end for i in self._registered):
                # Nothing of this wave is in this leg (it settled in an earlier one): move on.
                if self._wave_end >= self.total:
                    return
                continue
            return

    # -- the item's side ---------------------------------------------------------------------
    def register(self, index: int) -> None:
        self._registered.add(index)

    async def admit(self, index: int, stop_requested: Callable[[bool], Awaitable[bool]]) -> str:
        """Wait for ``index``'s wave. ``ADMIT``, ``UNTIL`` (never send it) or ``HELD`` (Stop / Pause)."""
        self.register(index)
        if self._wave_end is None:
            self._open_next_wave()
        waited = False
        while True:
            if self._stopped is not None:
                return UNTIL
            wait_for = WAVE_STOP_POLL_SECONDS
            if self._wave_end is not None and index < self._wave_end:
                remaining = self._not_before - time.monotonic()
                if remaining <= 0:
                    return ADMIT
                wait_for = min(remaining, WAVE_STOP_POLL_SECONDS)
            if await stop_requested(waited):
                return HELD
            self._changed.clear()
            try:
                await asyncio.wait_for(self._changed.wait(), timeout=wait_for)
            except TimeoutError:
                pass
            waited = True

    def start(self, index: int) -> None:
        self._started.add(index)

    def settle(self, index: int, status: str, value: Any) -> None:
        if index in self._settled:
            return
        self._settled[index] = (status, value)
        if status == HELD and self._stopped is None:
            # A spend approval is pending: send nothing more (the code path stops launching paid work after its
            # first hold). Items not yet admitted get UNTIL and settle as not sent; admitted ones finish.
            self._stopped = f"not sent: a spend approval is pending after {len(self._settled)} item(s)"
            self._changed.set()
            return
        try:
            self._open_next_wave()
        finally:
            self._changed.set()


def settled_status(result: Any) -> tuple[str, Any]:
    """``(status, value)`` of a finished invocation result for the pace's scope."""
    if getattr(result, "interrupt", None) is not None:
        return "waiting", None
    if getattr(result, "error", None) is not None or getattr(result, "failure", None) is not None:
        return "failed", None
    if getattr(result, "user_skipped", False):
        return "skipped", None
    dump = getattr(result, "settled_dump", None)
    if dump is None and getattr(result, "output", None) is not None:
        try:
            dump = result.output.model_dump(mode="json")
        except Exception:  # noqa: BLE001 — a value the scope cannot read is None, never a crash
            dump = None
    if getattr(result, "held", False) and dump is None:
        return "held", None
    return "succeeded", dump
