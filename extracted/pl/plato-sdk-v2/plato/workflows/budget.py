"""USD budget ceiling + Chronos cost source for workflows.

The workflow runtime enforces a hard USD ceiling: ``agent()`` raises
``BudgetExceededError`` once ``spent() >= total``. Spend is sourced from the
session's OTel spans, NOT ``AsyncChronos.get_metrics`` — get_metrics now also
drains the full span stream (no 1000-span cap anymore), but this module needs
the per-execution grouping below, not just session totals.

``ChronosCostSource`` drains ALL spans via ``fetch_all_spans_async`` (cursor
streaming, dedupe) and groups them per-execution using the canonical cost-node
pattern in ``analysis.py`` (``_build_execution`` at :461-477: prefer the
``atif.agent.cost_usd`` rollup node, fall back to summing ``atif.step.cost_usd``).
It reuses ``analyze_session`` so the grouping stays identical to the rest of the
SDK — critically avoiding a flat sum over all spans, which double-counts because
each per-model ``atif.cost.{model}`` span also carries ``atif.agent.cost_usd``
(otel.py:755-764).
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import math
from typing import Protocol, runtime_checkable

import httpx

from plato.chronos.analysis import analyze_session, fetch_all_spans_async
from plato.workflows.errors import BudgetExceededError

logger = logging.getLogger(__name__)

__all__ = [
    "CostSource",
    "Budget",
    "ChronosCostSource",
    "BudgetRefresher",
]

_DEFAULT_REFRESH_INTERVAL_S = 30.0


@runtime_checkable
class CostSource(Protocol):
    """Source of the session's ABSOLUTE spend in USD."""

    async def refresh(self) -> float: ...


class Budget:
    """USD spend ceiling with a serve-mode delta baseline.

    ``total_usd`` is the hard ceiling (``None`` = unlimited). ``baseline_usd`` is
    the session's absolute spend captured when this workflow started, so serve
    mode (one session-wide cost pot, many submissions) attributes only the delta
    to each workflow. Spend is monotonic — a momentary lower reading from ingest
    lag never rolls the cached value back.
    """

    def __init__(self, total_usd: float | None, baseline_usd: float = 0.0) -> None:
        self._total = total_usd
        self._baseline = baseline_usd
        self._cached_absolute = baseline_usd

    @property
    def total(self) -> float | None:
        return self._total

    def spent(self) -> float:
        """USD spent by THIS workflow (absolute cached spend minus baseline)."""
        return max(0.0, self._cached_absolute - self._baseline)

    def remaining(self) -> float:
        """USD left before the ceiling; ``inf`` when unlimited."""
        if self._total is None:
            return math.inf
        return self._total - self.spent()

    def check(self) -> None:
        """Raise ``BudgetExceededError`` when the ceiling is reached."""
        if self._total is None:
            return
        if self.spent() >= self._total:
            raise BudgetExceededError(f"Workflow budget exceeded: spent ${self.spent():.4f} of ${self._total:.4f}")

    def update_spent(self, absolute_usd: float) -> None:
        """Update the cached ABSOLUTE session spend (monotonic)."""
        if absolute_usd > self._cached_absolute:
            self._cached_absolute = absolute_usd


class ChronosCostSource:
    """Absolute session spend from all OTel spans via the cost-node grouping.

    The caller supplies an authenticated ``httpx.AsyncClient`` (base URL + bearer
    auth already configured) and the Plato ``session_id``.
    """

    def __init__(self, http: httpx.AsyncClient, session_id: str) -> None:
        self._http = http
        self._session_id = session_id

    async def refresh(self) -> float:
        spans = await fetch_all_spans_async(self._http, self._session_id)
        if not spans:
            return 0.0
        analysis = analyze_session(spans, self._session_id)
        return float(analysis.token_summary.cost_usd)


class BudgetRefresher:
    """Background poller that keeps a ``Budget`` current from a ``CostSource``.

    Polls every ``interval_s`` (default 30s). ``refresh_now()`` is the forced
    out-of-band entry point — the workflow runtime's ``on_call_complete`` hook
    is wired to it so spend is re-read after every completed agent call instead
    of waiting out the poll interval; concurrent callers (a parallel wave
    completing) coalesce onto a single in-flight source read. ``request_refresh()``
    wakes the background loop without blocking. Poll failures (ingest hiccups)
    are logged and never kill the loop.
    """

    def __init__(
        self,
        budget: Budget,
        source: CostSource,
        *,
        interval_s: float = _DEFAULT_REFRESH_INTERVAL_S,
    ) -> None:
        self._budget = budget
        self._source = source
        self._interval_s = interval_s
        self._task: asyncio.Task | None = None
        self._stop = asyncio.Event()
        self._wake = asyncio.Event()
        self._inflight: asyncio.Task[None] | None = None

    async def refresh_now(self) -> float:
        """Force an authoritative refresh and return this workflow's spend.

        Concurrent callers share one in-flight source refresh (a 30-wide wave
        completing must not stack 30 full span drains). The shared task is
        shielded so one cancelled awaiter cannot cancel the refresh for the
        rest.
        """
        inflight = self._inflight
        if inflight is None or inflight.done():
            inflight = asyncio.create_task(self._refresh_once())
            self._inflight = inflight
        await asyncio.shield(inflight)
        return self._budget.spent()

    async def _refresh_once(self) -> None:
        absolute = await self._source.refresh()
        self._budget.update_spent(absolute)

    def request_refresh(self) -> None:
        """Wake the background loop for an out-of-band refresh (non-blocking)."""
        self._wake.set()

    async def start(self) -> None:
        """Launch the background poll loop (idempotent)."""
        if self._task is None:
            self._stop.clear()
            self._task = asyncio.create_task(self._loop())

    async def stop(self) -> None:
        """Stop the background loop and await its exit."""
        self._stop.set()
        self._wake.set()
        if self._task is not None:
            try:
                await self._task
            finally:
                self._task = None
        if self._inflight is not None:
            self._inflight.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await self._inflight
            self._inflight = None

    async def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                await asyncio.wait_for(self._wake.wait(), timeout=self._interval_s)
            except TimeoutError:
                pass
            self._wake.clear()
            if self._stop.is_set():
                break
            try:
                await self.refresh_now()
            except Exception:
                logger.warning("Budget refresh failed; will retry", exc_info=True)
