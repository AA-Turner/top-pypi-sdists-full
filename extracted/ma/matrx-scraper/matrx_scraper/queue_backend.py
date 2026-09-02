"""Crawl queue backend protocol.

The crawler iterates `enqueue` / `dequeue` / `mark_done` / `mark_failed` calls
through a `QueueBackend`. The default in-memory backend is enough for short
runs; the durable backend is `web_crawl/runtime_queue.py`, which persists the
frontier to `runtime.work_item` (anchored to a `web.crawl_session`) so
50,000-page crawls can resume after a crash. The host injects it as the
`work_queue_factory` ext.

(The retired `scraper.crawl_queue` backend went to `graveyard` with the rest of
the legacy crawl world on 2026-08-09 — there is ONE crawler now.)

This is intentionally a tiny surface — anything more goes in the host.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass
class QueueItem:
    url: str
    depth: int
    parent_url: str | None = None
    source: str = "link"  # 'seed' | 'sitemap' | 'link'


@runtime_checkable
class QueueBackend(Protocol):
    """Durable URL queue protocol.

    `enqueue` is idempotent — duplicate URLs (per run) must be silently dropped.
    `dequeue` blocks via async (semantics up to the implementation) but must
    return None when both queue is empty AND no items are in flight.
    """

    async def enqueue(self, item: QueueItem) -> bool:
        """Add a URL to the queue. Returns True if accepted, False if duplicate."""
        ...

    async def dequeue(self) -> QueueItem | None:
        """Pop the next queued URL, or return None when no work remains."""
        ...

    async def mark_done(self, url: str) -> None:
        """Mark a URL as successfully processed."""
        ...

    async def mark_failed(self, url: str, error: str, will_retry: bool = False) -> None:
        """Mark a URL as failed."""
        ...

    async def is_known(self, url: str) -> bool:
        """Return True if the URL has been seen (queued/in_flight/done/failed)."""
        ...

    async def known_urls(self, urls: list[str]) -> set[str]:
        """Set-shaped `is_known` — which of `urls` have already been seen.

        One round-trip for a whole page's link set. A per-link `is_known` loop
        is a defect: a marketing page carries 150-300 links, and serialising
        that many round-trips behind the fetch stalls the crawl frontier.
        """
        ...

    async def enqueue_many(self, items: list[QueueItem]) -> list[QueueItem]:
        """Set-shaped `enqueue` — returns the subset actually accepted."""
        ...

    async def counts(self) -> tuple[int, int]:
        """(queue_depth, in_flight_count) in ONE round-trip.

        The run loop polls this every tick; two separate COUNT queries doubled
        the poll cost for a number that is only ever read as a pair.
        """
        ...

    async def queue_depth(self) -> int:
        """Number of URLs still in 'queued' state."""
        ...

    async def in_flight_count(self) -> int:
        """Number of URLs currently in 'in_flight' state."""
        ...


class InMemoryQueueBackend:
    """Default backend — fine for runs that don't need crash recovery."""

    def __init__(self) -> None:
        self._queue: asyncio.Queue[QueueItem] = asyncio.Queue()
        self._known: set[str] = set()
        # url -> the QueueItem currently in flight. A dict (not a set) so a
        # `mark_failed(will_retry=True)` can re-enqueue the ORIGINAL item with
        # its depth/parent intact — a retry must not lose crawl-graph position.
        self._in_flight: dict[str, QueueItem] = {}
        self._lock = asyncio.Lock()

    async def enqueue(self, item: QueueItem) -> bool:
        async with self._lock:
            if item.url in self._known:
                return False
            self._known.add(item.url)
        await self._queue.put(item)
        return True

    async def dequeue(self) -> QueueItem | None:
        # Non-blocking dequeue; the crawler decides when to stop.
        try:
            item = self._queue.get_nowait()
        except asyncio.QueueEmpty:
            return None
        async with self._lock:
            self._in_flight[item.url] = item
        return item

    async def mark_done(self, url: str) -> None:
        async with self._lock:
            self._in_flight.pop(url, None)

    async def mark_failed(self, url: str, error: str, will_retry: bool = False) -> None:
        # will_retry MUST re-enqueue — the crawler uses it to back a rate-limited
        # (HTTP 429) URL off and try again. Dropping it here silently (the old
        # behavior) is why retries never happened. The url stays in `_known`, so
        # re-enqueue is a deliberate requeue, not a fresh discovery.
        async with self._lock:
            item = self._in_flight.pop(url, None)
        if will_retry and item is not None:
            await self._queue.put(item)

    async def is_known(self, url: str) -> bool:
        async with self._lock:
            return url in self._known

    async def known_urls(self, urls: list[str]) -> set[str]:
        async with self._lock:
            return {url for url in urls if url in self._known}

    async def enqueue_many(self, items: list[QueueItem]) -> list[QueueItem]:
        accepted: list[QueueItem] = []
        async with self._lock:
            for item in items:
                if item.url in self._known:
                    continue
                self._known.add(item.url)
                accepted.append(item)
        for item in accepted:
            await self._queue.put(item)
        return accepted

    async def counts(self) -> tuple[int, int]:
        async with self._lock:
            return self._queue.qsize(), len(self._in_flight)

    async def queue_depth(self) -> int:
        return self._queue.qsize()

    async def in_flight_count(self) -> int:
        async with self._lock:
            return len(self._in_flight)


__all__ = [
    "QueueBackend",
    "QueueItem",
    "InMemoryQueueBackend",
]
