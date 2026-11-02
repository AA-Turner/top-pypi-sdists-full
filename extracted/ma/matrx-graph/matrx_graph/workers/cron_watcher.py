"""Cron watcher — polls wf_trigger, enqueues due runs.

Intended to run in-process alongside the FastAPI app (registered as a
lifespan background task) OR as a standalone process alongside workers.
Either works; FOR UPDATE SKIP LOCKED on claim_due makes concurrent
watchers safe.

A ``fire_trigger`` callable is injected so this module doesn't depend on
the rest of aidream — the app supplies "given this trigger_row, create a
wf_run + enqueue a wf_job". The watcher only handles the scheduling
arithmetic.
"""

from __future__ import annotations

import asyncio
import logging

from matrx_utils import capture_error
from collections.abc import Awaitable, Callable
from datetime import datetime

from matrx_graph.db.trigger_store import TriggerRow, TriggerStore

logger = logging.getLogger(__name__)

FireTrigger = Callable[[TriggerRow], Awaitable[str]]
"""Host-app fire callable. Given a trigger row, should create a wf_run row
for this invocation, enqueue a wf_job, and return the run_id so the
watcher can record it on wf_trigger.last_run_id."""


class CronWatcher:
    """Periodically scans wf_trigger for due cron jobs and fires them.

    Claim semantics are built into TriggerStore.claim_due — it advances
    next_run_at atomically inside the same transaction that selects the
    rows, so a crash between claim and fire produces AT MOST one missed
    fire per trigger (the row is already advanced; a crashed watcher just
    doesn't get to enqueue the corresponding job).

    For at-least-once semantics across crashes we'd need a separate
    "in-flight" column and cleanup logic; for Phase 5b the at-most-once
    contract is documented and acceptable — cron workflows are generally
    idempotent by design.
    """

    def __init__(
        self,
        *,
        fire_trigger: FireTrigger,
        store: TriggerStore | None = None,
        poll_interval_seconds: float = 5.0,
        claim_limit: int = 100,
    ) -> None:
        self._fire = fire_trigger
        self._store = store or TriggerStore()
        self._poll_interval = poll_interval_seconds
        self._claim_limit = claim_limit
        self._stop_event = asyncio.Event()

    def stop(self) -> None:
        self._stop_event.set()

    async def run_forever(self) -> None:
        logger.info("cron watcher: started (poll=%ss)", self._poll_interval)
        while not self._stop_event.is_set():
            try:
                fired = await self._tick()
                if fired:
                    logger.info("cron watcher: fired %d trigger(s)", fired)
            except Exception as exc:  # noqa: BLE001 — watcher must never die
                logger.exception("cron watcher: tick failed; backing off")
                await capture_error(exc, kind="workflow_cron_tick_failed")
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self._poll_interval)
            except TimeoutError:
                pass
        logger.info("cron watcher: stopped")

    async def _tick(self, *, now: datetime | None = None) -> int:
        due = await self._store.claim_due(now=now, limit=self._claim_limit)
        if not due:
            return 0
        for trig in due:
            try:
                run_id = await self._fire(trig)
                await self._store.record_fire(trig.id, run_id)
            except Exception as exc:  # noqa: BLE001
                logger.exception(
                    "cron watcher: fire failed for trigger %s (%s)",
                    trig.name,
                    trig.id,
                )
                await capture_error(
                    exc,
                    kind="workflow_cron_fire_failed",
                    context={"trigger_id": trig.id, "trigger_name": trig.name},
                )
        return len(due)

    async def tick_once(self, *, now: datetime | None = None) -> int:
        """Single-tick entry for tests and manual "drain now" patterns."""
        return await self._tick(now=now)
