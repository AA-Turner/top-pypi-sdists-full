"""Event watcher — polls workflow.trigger_event, fires due event triggers.

The sibling of CronWatcher, one lane over: cron fires come from time,
event fires come from data changes captured durably by
``workflow.emit_trigger_events()`` (migration 0111). Same deployment
posture — runs on the workflow worker (role by entrypoint), multiple
replicas are safe (``TriggerEventStore.claim_due`` is FOR UPDATE SKIP
LOCKED + lease-fenced), and the durable queue means the poll IS the
reconcile: nothing is lost while the worker is down, it drains on boot.

A ``fire_event`` callable is injected so this module doesn't depend on the
rest of the host app — the app supplies "given (trigger_row, event_row),
create a wf_run + enqueue a wf_job".
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from datetime import datetime

from matrx_utils import capture_error

from matrx_graph.db.store_change import StoreChangeRefused
from matrx_graph.db.trigger_event_store import TriggerEventRow, TriggerEventStore
from matrx_graph.db.trigger_store import TriggerRow, TriggerStore

logger = logging.getLogger(__name__)

FireEvent = Callable[[TriggerRow, TriggerEventRow], Awaitable[str]]
"""Host-app fire callable. Given the parent trigger row and the claimed
event row, should create a wf_run for this fire, enqueue a wf_job, and
return the run_id."""


class EventWatcher:
    """Periodically claims due workflow.trigger_event rows and fires them.

    Failure semantics per event: a failed fire goes back to pending with
    exponential backoff and dead-letters after max_attempts (the store owns
    that state machine); an event whose parent trigger is gone or no longer
    an active event trigger is dead-lettered immediately with the reason.
    The watcher itself never dies on a fire error.
    """

    def __init__(
        self,
        *,
        fire_event: FireEvent,
        store: TriggerEventStore | None = None,
        trigger_store: TriggerStore | None = None,
        poll_interval_seconds: float = 5.0,
        claim_limit: int = 50,
        lease_seconds: int = 600,
    ) -> None:
        self._fire = fire_event
        self._store = store or TriggerEventStore()
        self._trigger_store = trigger_store or TriggerStore()
        self._poll_interval = poll_interval_seconds
        self._claim_limit = claim_limit
        self._lease_seconds = lease_seconds
        self._stop_event = asyncio.Event()

    def stop(self) -> None:
        self._stop_event.set()

    async def run_forever(self) -> None:
        logger.info("event watcher: started (poll=%ss)", self._poll_interval)
        while not self._stop_event.is_set():
            try:
                fired = await self._tick()
                if fired:
                    logger.info("event watcher: processed %d event(s)", fired)
            except Exception as exc:  # noqa: BLE001 — watcher must never die
                logger.exception("event watcher: tick failed; backing off")
                await capture_error(exc, kind="workflow_event_tick_failed")
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self._poll_interval)
            except TimeoutError:
                pass
        logger.info("event watcher: stopped")

    async def _tick(self, *, now: datetime | None = None) -> int:
        events = await self._store.claim_due(
            now=now, limit=self._claim_limit, lease_seconds=self._lease_seconds
        )
        if not events:
            return 0

        triggers: dict[str, TriggerRow | None] = {}
        for ev in events:
            if ev.trigger_id not in triggers:
                triggers[ev.trigger_id] = await self._trigger_store.load(ev.trigger_id)

        for ev in events:
            trigger = triggers.get(ev.trigger_id)
            if trigger is None or trigger.kind != "event" or not trigger.is_active:
                if trigger is None:
                    reason = "trigger not found or deleted"
                elif trigger.kind != "event":
                    reason = f"trigger kind is {trigger.kind}, not event"
                else:
                    reason = "trigger is inactive"
                await self._store.mark_dead(ev.id, error=reason)
                continue
            try:
                run_id = await self._fire(trigger, ev)
                await self._store.mark_fired(ev.id, run_id)
                await self._trigger_store.record_fire(trigger.id, run_id)
            except StoreChangeRefused as refused:
                # No real record change backs this event (a fabricated or mismatched
                # trigger_event row, or a change that already ran). Dead-lettered with the
                # sentence, never retried, never a run (lane 11 round 3).
                logger.warning(
                    "event watcher: store change refused for trigger %s event %s: %s",
                    trigger.id, ev.id, refused,
                )
                await self._store.mark_dead(ev.id, error=str(refused))
            except Exception as exc:  # noqa: BLE001
                logger.exception(
                    "event watcher: fire failed for trigger %s (%s) event %s",
                    trigger.name,
                    trigger.id,
                    ev.id,
                )
                try:
                    await self._store.mark_failed(ev.id, error=f"{type(exc).__name__}: {exc}")
                except Exception:  # noqa: BLE001 — settle failure must not kill the loop
                    logger.exception("event watcher: mark_failed itself failed for %s", ev.id)
                await capture_error(
                    exc,
                    kind="workflow_event_fire_failed",
                    context={
                        "trigger_id": trigger.id,
                        "trigger_name": trigger.name,
                        "event_id": ev.id,
                        "entity_key": ev.entity_key,
                    },
                )
        return len(events)

    async def tick_once(self, *, now: datetime | None = None) -> int:
        """Single-tick entry for tests and manual "drain now" patterns."""
        return await self._tick(now=now)
