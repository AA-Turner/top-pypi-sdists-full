"""
cvc.sdk.events — Real-time event bus for the hive mind.

Provides in-process pub/sub with both synchronous and async subscribers,
per-subscriber asyncio queues for cross-process bridging (WebSocket/SSE),
event history replay for late-joining agents, and filter-based subscriptions.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Callable

logger = logging.getLogger("cvc.sdk.events")

# Standard event names
COMMIT_CREATED = "commit.created"
AGENT_TARGETED = "agent.targeted"
BRANCH_UPDATED = "branch.updated"
SQUAD_MERGED = "squad.merged"
AGENT_REGISTERED = "agent.registered"
SYNC_COMPLETED = "sync.completed"

ALL_EVENTS = [
    COMMIT_CREATED,
    AGENT_TARGETED,
    BRANCH_UPDATED,
    SQUAD_MERGED,
    AGENT_REGISTERED,
    SYNC_COMPLETED,
]

EventCallback = Callable[[dict[str, Any]], Any]


@dataclass
class EventEnvelope:
    """Immutable envelope wrapping a single event emission."""

    event: str
    data: dict[str, Any]
    timestamp: float = field(default_factory=time.time)


class Subscription:
    """
    An asyncio-queue-based subscription for cross-process consumers.

    Each ``Subscription`` maintains its own bounded ``asyncio.Queue``.
    The WebSocket/SSE bridge drains events from the queue and sends
    them over the wire.
    """

    def __init__(
        self,
        subscriber_id: str,
        events: list[str] | None = None,
        *,
        agent_filter: str | None = None,
        maxsize: int = 256,
    ) -> None:
        self.subscriber_id = subscriber_id
        self.events: set[str] | None = set(events) if events else None
        self.agent_filter = agent_filter
        self.queue: asyncio.Queue[EventEnvelope] = asyncio.Queue(maxsize=maxsize)
        self.created_at = time.time()
        self._active = True

    @property
    def active(self) -> bool:
        return self._active

    def cancel(self) -> None:
        self._active = False

    def accepts(self, envelope: EventEnvelope) -> bool:
        """Check whether this subscription should receive the event."""
        if not self._active:
            return False
        if self.events is not None and envelope.event not in self.events:
            return False
        if self.agent_filter:
            # Only accept events relevant to this agent
            target = envelope.data.get("target_agent_id") or envelope.data.get("agent_id")
            if target != self.agent_filter:
                return False
        return True

    async def get(self, timeout: float | None = None) -> EventEnvelope:
        """Wait for the next event (with optional timeout)."""
        if timeout is not None:
            return await asyncio.wait_for(self.queue.get(), timeout=timeout)
        return await self.queue.get()

    def get_nowait(self) -> EventEnvelope | None:
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    def drain(self) -> list[EventEnvelope]:
        """Drain all pending events from the queue."""
        items: list[EventEnvelope] = []
        while True:
            try:
                items.append(self.queue.get_nowait())
            except asyncio.QueueEmpty:
                break
        return items


class EventBus:
    """
    In-process event bus with sync/async pub/sub and queue-based subscriptions.

    Three consumption models:

    1. **Sync callbacks** — ``bus.on("event", fn)`` — called inline during ``emit()``.
    2. **Async callbacks** — ``bus.on_async("event", fn)`` — gathered during ``emit_async()``.
    3. **Queue subscriptions** — ``bus.subscribe(...)`` — events pushed to an
       ``asyncio.Queue`` that WebSocket/SSE handlers drain.

    Also maintains a bounded event history for late-joining subscribers.
    """

    def __init__(self, *, history_size: int = 500) -> None:
        self._sync_handlers: dict[str, list[EventCallback]] = defaultdict(list)
        self._async_handlers: dict[str, list[Callable]] = defaultdict(list)
        self._subscriptions: dict[str, Subscription] = {}
        self._history: deque[EventEnvelope] = deque(maxlen=history_size)

    # -- Subscribe (callback) ----------------------------------------------

    def on(self, event: str, callback: EventCallback) -> None:
        """Register a synchronous event handler."""
        self._sync_handlers[event].append(callback)

    def on_async(self, event: str, callback: Callable) -> None:
        """Register an async event handler."""
        self._async_handlers[event].append(callback)

    def off(self, event: str, callback: EventCallback | None = None) -> None:
        """Remove a specific handler, or all handlers for the event."""
        if callback is None:
            self._sync_handlers.pop(event, None)
            self._async_handlers.pop(event, None)
        else:
            if event in self._sync_handlers:
                try:
                    self._sync_handlers[event].remove(callback)
                except ValueError:
                    pass
            if event in self._async_handlers:
                try:
                    self._async_handlers[event].remove(callback)
                except ValueError:
                    pass

    # -- Subscribe (queue) -------------------------------------------------

    def subscribe(
        self,
        subscriber_id: str,
        events: list[str] | None = None,
        *,
        agent_filter: str | None = None,
        replay: bool = False,
    ) -> Subscription:
        """
        Create a queue-based subscription.

        If *replay* is True, the subscription's queue is pre-filled with
        matching events from the history buffer.
        """
        sub = Subscription(subscriber_id, events, agent_filter=agent_filter)
        self._subscriptions[subscriber_id] = sub

        if replay:
            for envelope in self._history:
                if sub.accepts(envelope):
                    try:
                        sub.queue.put_nowait(envelope)
                    except asyncio.QueueFull:
                        break

        logger.info("Subscription created: %s (events=%s, agent=%s)", subscriber_id, events, agent_filter)
        return sub

    def unsubscribe(self, subscriber_id: str) -> None:
        """Remove a queue-based subscription."""
        sub = self._subscriptions.pop(subscriber_id, None)
        if sub:
            sub.cancel()
            logger.info("Subscription removed: %s", subscriber_id)

    @property
    def subscriptions(self) -> dict[str, Subscription]:
        return dict(self._subscriptions)

    # -- Emit --------------------------------------------------------------

    def emit(self, event: str, data: dict[str, Any] | None = None) -> None:
        """Fire an event — sync callbacks + queue subscriptions."""
        payload = data or {}
        payload.setdefault("event", event)
        envelope = EventEnvelope(event=event, data=payload)
        self._history.append(envelope)

        # Sync handlers
        for handler in self._sync_handlers.get(event, []):
            try:
                handler(payload)
            except Exception:
                logger.exception("Error in sync handler for %s", event)
        # Wildcard handlers
        for handler in self._sync_handlers.get("*", []):
            try:
                handler(payload)
            except Exception:
                logger.exception("Error in wildcard handler for %s", event)

        # Push to queue subscriptions
        self._fan_out(envelope)

    async def emit_async(self, event: str, data: dict[str, Any] | None = None) -> None:
        """Fire an event — sync + async callbacks + queue subscriptions."""
        payload = data or {}
        payload.setdefault("event", event)
        envelope = EventEnvelope(event=event, data=payload)
        self._history.append(envelope)

        # Fire sync handlers first
        for handler in self._sync_handlers.get(event, []):
            try:
                handler(payload)
            except Exception:
                logger.exception("Error in sync handler for %s", event)
        for handler in self._sync_handlers.get("*", []):
            try:
                handler(payload)
            except Exception:
                logger.exception("Error in wildcard handler for %s", event)

        # Then async handlers
        tasks = []
        for handler in self._async_handlers.get(event, []):
            tasks.append(handler(payload))
        for handler in self._async_handlers.get("*", []):
            tasks.append(handler(payload))
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in results:
                if isinstance(r, Exception):
                    logger.exception("Error in async handler for %s: %s", event, r)

        # Push to queue subscriptions
        self._fan_out(envelope)

    def _fan_out(self, envelope: EventEnvelope) -> None:
        """Push event to all matching queue subscriptions."""
        dead: list[str] = []
        for sid, sub in self._subscriptions.items():
            if not sub.active:
                dead.append(sid)
                continue
            if sub.accepts(envelope):
                try:
                    sub.queue.put_nowait(envelope)
                except asyncio.QueueFull:
                    logger.warning("Subscription %s queue full — dropping event %s", sid, envelope.event)
        # Cleanup dead subscriptions
        for sid in dead:
            self._subscriptions.pop(sid, None)

    # -- History -----------------------------------------------------------

    @property
    def history(self) -> list[EventEnvelope]:
        """Return a copy of the event history."""
        return list(self._history)

    def history_for(self, event: str | None = None, *, limit: int = 50) -> list[EventEnvelope]:
        """Return recent events from history, optionally filtered by type."""
        if event is None:
            return list(self._history)[-limit:]
        return [e for e in self._history if e.event == event][-limit:]
