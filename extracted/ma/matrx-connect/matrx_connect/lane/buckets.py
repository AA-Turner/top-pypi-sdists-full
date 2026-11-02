from __future__ import annotations

import asyncio
from dataclasses import dataclass


# Default per-lane bucket caps. A "bucket" is a named asyncio.Semaphore
# scoped to one RequestLane — it caps fan-out PER REQUEST. The matrx-orm
# write_queue and asyncpg pool still cap GLOBAL concurrency above us.
DEFAULT_BUCKET_CAPS: dict[str, int] = {
    "db_write": 10,   # all DB writes — tool_logger, persistence, ctx_writeback
    "ai_api": 4,      # LLM provider calls when a tool issues sub-LLM calls
    "file_io": 8,     # cloud uploads, thumbnail generation
    "default": 16,    # anything without an explicit bucket
}


@dataclass(slots=True)
class BucketStats:
    """Live snapshot of one bucket's state — for /admin/lanes."""
    name: str
    capacity: int
    in_flight: int
    queued: int


class Bucket:
    """A named per-lane semaphore with live in_flight bookkeeping.

    Wraps asyncio.Semaphore so observability endpoints can answer "how many
    of bucket X are currently held" without polling asyncio internals.
    """

    __slots__ = ("name", "capacity", "_sem", "_in_flight", "_waiters")

    def __init__(self, name: str, capacity: int) -> None:
        if capacity < 1:
            raise ValueError(f"Bucket capacity must be >= 1, got {capacity} for {name!r}")
        self.name = name
        self.capacity = capacity
        self._sem = asyncio.Semaphore(capacity)
        self._in_flight = 0
        # Approximate queued count — _waiters is incremented before acquire,
        # decremented after. asyncio.Semaphore doesn't expose its waiter
        # count, so we track ourselves.
        self._waiters = 0

    async def acquire(self) -> None:
        self._waiters += 1
        try:
            await self._sem.acquire()
        finally:
            self._waiters -= 1
        self._in_flight += 1

    def release(self) -> None:
        if self._in_flight > 0:
            self._in_flight -= 1
        # If release is called without a paired acquire (caller bug), the
        # semaphore would over-release. Guard so a buggy caller can't
        # permanently expand the bucket.
        if self._sem._value < self.capacity:  # type: ignore[attr-defined]
            self._sem.release()

    def stats(self) -> BucketStats:
        return BucketStats(
            name=self.name,
            capacity=self.capacity,
            in_flight=self._in_flight,
            queued=self._waiters,
        )
