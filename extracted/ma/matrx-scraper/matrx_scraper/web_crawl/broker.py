"""Bounded active-session replay broker.

Durability lives in ``web.crawl_event``. This broker is only an internal live
fan-out primitive; stored-event replay is never exposed by the Python service.
"""

from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass

from matrx_scraper.events import CrawlEvent

_CLOSED = object()


@dataclass
class BrokerSubscription:
    replay: list[CrawlEvent]
    watermark: int
    memory_covers: bool
    queue: asyncio.Queue[CrawlEvent | object]


class CrawlEventBroker:
    def __init__(self, session_id: str, *, replay_size: int = 2_000) -> None:
        self.session_id = session_id
        self._events: deque[CrawlEvent] = deque(maxlen=replay_size)
        self._subscribers: set[asyncio.Queue[CrawlEvent | object]] = set()
        self._closed = False
        self._lock = asyncio.Lock()

    async def publish(self, event: CrawlEvent) -> None:
        async with self._lock:
            if self._closed:
                raise RuntimeError(f"crawl broker {self.session_id} is closed")
            self._events.append(event)
            subscribers = tuple(self._subscribers)
        for queue in subscribers:
            queue.put_nowait(event)

    async def subscribe(self, after_sequence: int) -> BrokerSubscription:
        queue: asyncio.Queue[CrawlEvent | object] = asyncio.Queue()
        async with self._lock:
            sequences = [int(event.sequence or 0) for event in self._events]
            oldest = sequences[0] if sequences else 1
            watermark = sequences[-1] if sequences else 0
            memory_covers = after_sequence >= oldest - 1
            replay = (
                [event for event in self._events if int(event.sequence or 0) > after_sequence]
                if memory_covers
                else []
            )
            if self._closed:
                queue.put_nowait(_CLOSED)
            else:
                self._subscribers.add(queue)
        return BrokerSubscription(
            replay=replay,
            watermark=watermark,
            memory_covers=memory_covers,
            queue=queue,
        )

    async def unsubscribe(self, subscription: BrokerSubscription) -> None:
        async with self._lock:
            self._subscribers.discard(subscription.queue)

    async def close(self) -> None:
        async with self._lock:
            if self._closed:
                return
            self._closed = True
            subscribers = tuple(self._subscribers)
            self._subscribers.clear()
        for queue in subscribers:
            queue.put_nowait(_CLOSED)

    @staticmethod
    def is_closed_item(item: CrawlEvent | object) -> bool:
        return item is _CLOSED


class CrawlBrokerRegistry:
    _instance: CrawlBrokerRegistry | None = None

    def __init__(self) -> None:
        self._brokers: dict[str, CrawlEventBroker] = {}
        self._lock = asyncio.Lock()

    @classmethod
    def get_instance(cls) -> CrawlBrokerRegistry:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def create(self, session_id: str) -> CrawlEventBroker:
        async with self._lock:
            if session_id in self._brokers:
                raise RuntimeError(f"crawl session {session_id} is already active")
            broker = CrawlEventBroker(session_id)
            self._brokers[session_id] = broker
            return broker

    def get(self, session_id: str) -> CrawlEventBroker | None:
        return self._brokers.get(session_id)

    async def remove(
        self,
        session_id: str,
        broker: CrawlEventBroker,
    ) -> None:
        async with self._lock:
            if self._brokers.get(session_id) is broker:
                self._brokers.pop(session_id, None)


__all__ = ["BrokerSubscription", "CrawlBrokerRegistry", "CrawlEventBroker"]
