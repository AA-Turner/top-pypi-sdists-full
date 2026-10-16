"""Crawl lanes — interactive work never queues behind bulk crawls.

One scraper process runs every crawl on one event loop and one default thread
pool. Measured 2026-10-15 (MKT-150): with 7-10 full 500-page crawls running,
the crawl progress ticks (every 5 s by design) stretched to 10-51 s — 412 of
2,065 ticks in one hour over 10 s, none the hour before with 2-4 crawls — and a
one-page Smart Add initialization took 9 minutes (24 s of it a page audit run
on the event loop, 3.5 min between fetch and parse).

Two lanes, both bounded by ``platform.feature_knob`` rows (feature
``knowledge.scraper``):

* ``interactive`` — a person is waiting (site initialization, homepage
  bootstrap). Takes page slots from the process-wide cap only and runs its CPU
  work on the loop's default thread pool.
* ``bulk`` — background crawls. Also hold one of ``crawl.bulk_page_slots``
  page slots, and run their CPU work (parse, audit) on a separate pool of
  ``crawl.bulk_cpu_threads`` threads, so they can never fill the default pool an
  interactive parse needs.

The lane rides a context variable the crawler sets for its own run; tasks it
spawns inherit it. Outside a crawl the lane is ``interactive`` — the behaviour
every caller had before lanes existed.
"""

from __future__ import annotations

import asyncio
import contextvars
import functools
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Literal

from matrx_scraper.parser.knobs import parser_knob

CrawlLane = Literal["interactive", "bulk"]
LANE_INTERACTIVE: CrawlLane = "interactive"
LANE_BULK: CrawlLane = "bulk"

#: KNOB MIRROR: knowledge.scraper.crawl.bulk_page_slots — pages background
#: crawls may work at once, together, in one scraper process. The process-wide
#: cap (crawler.GLOBAL_PAGE_CONCURRENCY_CAP, 24) minus this is what is always
#: left for a person waiting on an initialization.
BULK_PAGE_SLOTS_MIRROR = 12
#: KNOB MIRROR: knowledge.scraper.crawl.bulk_cpu_threads — threads background
#: crawls parse and audit pages on. Interactive work keeps the default pool.
BULK_CPU_THREADS_MIRROR = 2

_LANE: contextvars.ContextVar[CrawlLane] = contextvars.ContextVar(
    "matrx_scraper_crawl_lane", default=LANE_INTERACTIVE
)


def current_lane() -> CrawlLane:
    return _LANE.get()


def set_lane(lane: CrawlLane) -> contextvars.Token[CrawlLane]:
    return _LANE.set(lane)


def reset_lane(token: contextvars.Token[CrawlLane]) -> None:
    _LANE.reset(token)


def _positive_int(key: str, mirror: int) -> int:
    try:
        value = int(parser_knob(key, mirror))
    except (TypeError, ValueError):
        value = mirror
    return max(1, value)


# One bulk executor and one bulk page semaphore per (event loop, knob value):
# an admin's change to either knob takes effect for the next page that asks,
# and a semaphore never crosses event loops (tests run many).
_bulk_executor: ThreadPoolExecutor | None = None
_bulk_executor_size = 0
_bulk_slots: asyncio.Semaphore | None = None
_bulk_slots_key: tuple[Any, int] | None = None


def _bulk_pool() -> ThreadPoolExecutor:
    global _bulk_executor, _bulk_executor_size
    size = _positive_int("crawl.bulk_cpu_threads", BULK_CPU_THREADS_MIRROR)
    if _bulk_executor is None or _bulk_executor_size != size:
        old = _bulk_executor
        _bulk_executor = ThreadPoolExecutor(max_workers=size, thread_name_prefix="crawl-bulk-cpu")
        _bulk_executor_size = size
        if old is not None:
            # Work already queued on the old pool finishes; nothing new lands there.
            old.shutdown(wait=False)
    return _bulk_executor


def bulk_page_slots() -> asyncio.Semaphore:
    """The semaphore every bulk-lane page holds alongside the process-wide cap."""
    global _bulk_slots, _bulk_slots_key
    size = _positive_int("crawl.bulk_page_slots", BULK_PAGE_SLOTS_MIRROR)
    key = (asyncio.get_running_loop(), size)
    if _bulk_slots is None or _bulk_slots_key != key:
        # A resize starts a fresh semaphore; pages holding the old one release
        # into it harmlessly, so the new limit governs from the next page on.
        _bulk_slots = asyncio.Semaphore(size)
        _bulk_slots_key = key
    return _bulk_slots


async def run_cpu[T](fn: Callable[..., T], /, *args: Any, **kwargs: Any) -> T:
    """Run CPU-bound ``fn`` off the event loop, on this lane's thread pool."""
    if current_lane() != LANE_BULK:
        return await asyncio.to_thread(fn, *args, **kwargs)
    ctx = contextvars.copy_context()
    call = functools.partial(ctx.run, fn, *args, **kwargs)
    return await asyncio.get_running_loop().run_in_executor(_bulk_pool(), call)


__all__ = [
    "BULK_CPU_THREADS_MIRROR",
    "BULK_PAGE_SLOTS_MIRROR",
    "LANE_BULK",
    "LANE_INTERACTIVE",
    "CrawlLane",
    "bulk_page_slots",
    "current_lane",
    "reset_lane",
    "run_cpu",
    "set_lane",
]
