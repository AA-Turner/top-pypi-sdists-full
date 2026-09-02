"""CHAOS ACCEPTANCE TEST — kill the crawler mid-crawl, prove the resume finishes it.

The durable-work-queue standard's non-negotiable proof
(common-docs/policies/durable-work-queue-standard.md): *durability is unproven
until a chaos test kills the process mid-run and the job still finishes with zero
dropped and zero duplicated items.* This is that test, and it is the one that was
missing — which is precisely why a resume bug (the event sink restarting its
sequence at 0) reached production and permanently FAILED the two live sessions it
was supposed to rescue.

What it exercises, with no DB and no network: the REAL `SiteCrawler` driving the
REAL durable frontier (`RuntimeWorkQueueBackend` over the in-memory RML store),
killed mid-crawl, then a SECOND crawler — a restarted process, fresh in-memory
state, new holder — claiming the SAME batch execution and draining it.

The guarantee under test is at-least-once, and the test says so precisely:
  * ZERO DROPPED — unconditional. Every page is persisted and every work item is
    settled SUCCEEDED. A page the crash swallowed is a hard failure.
  * ZERO DUPLICATED — for every item the dead process SETTLED. A page it had
    fetched but not yet settled may legitimately be re-fetched (its lease
    expires, the reaper returns it); that count is bounded by what was in flight
    at the moment of death, and the test pins that bound rather than waving at it.

Not covered here (different layers, covered elsewhere): the DB-backed session
reload and the monotonic ledger/event sequence seeding — `test_web_crawl_resume.py`
plus `service.prepare_resume`.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

pytest.importorskip("matrx_runtime")

from matrx_runtime import WorkItemState  # noqa: E402
from matrx_runtime.store import InMemoryExecutionStore  # noqa: E402

from matrx_scraper.crawler import (  # noqa: E402
    PersistResult,
    RENDER_HTTP_ONLY,
    SiteCrawler,
    SiteCrawlerConfig,
)
from matrx_scraper.events import CrawlPageFetchedEvent  # noqa: E402
from matrx_scraper.orchestrator import ScrapeResult  # noqa: E402
from matrx_scraper.web_crawl.runtime_queue import (  # noqa: E402
    DEFAULT_ITEM_LEASE_SECONDS,
    RuntimeWorkQueueBackend,
)

EXECUTION_ID = "chaos-batch-execution"
SITE = "https://chaos.test/"
PAGE_COUNT = 12
KILL_AFTER = 4


def _urls() -> list[str]:
    return [SITE] + [f"{SITE}page-{i}" for i in range(1, PAGE_COUNT)]


def _html(*links: str) -> str:
    anchors = "".join(f'<a href="{link}">{link}</a>' for link in links)
    body = " ".join(["Durable crawl chaos regression content"] * 80)
    return f"<html><head><title>Page</title></head><body>{body}{anchors}</body></html>"


class _Persister:
    """Shared across BOTH runs — the only place that can see a duplicate."""

    def __init__(self) -> None:
        self.urls: list[str] = []

    async def __call__(self, request: Any) -> PersistResult:
        self.urls.append(request.url)
        return PersistResult(page_id="page", snapshot_id="snapshot")


class _KillSwitch:
    """Event sink that trips once the crawl has really made progress."""

    def __init__(self, after: int) -> None:
        self.after = after
        self.fetched = 0
        self.tripped = asyncio.Event()

    async def emit(self, event: Any) -> None:
        if isinstance(event, CrawlPageFetchedEvent):
            self.fetched += 1
            if self.fetched >= self.after:
                self.tripped.set()


class _Sink:
    async def emit(self, event: Any) -> None:
        return None


def _crawler(queue: RuntimeWorkQueueBackend, sink: Any, persister: _Persister) -> SiteCrawler:
    return SiteCrawler(
        run_id="chaos",
        config=SiteCrawlerConfig(
            base_url=SITE,
            max_pages=PAGE_COUNT,
            concurrency=2,
            respect_robots=False,
            seed_from_sitemap=False,
            render_mode=RENDER_HTTP_ONLY,
            host_rps=1000.0,
        ),
        event_sink=sink,
        queue_backend=queue,
        body_persister=persister,
        strict_persistence=True,
        retain_results=False,
    )


@pytest.mark.asyncio
async def test_process_death_mid_crawl_is_a_non_event(monkeypatch: pytest.MonkeyPatch) -> None:
    all_urls = _urls()
    # The homepage links every other page; a fresh crawler rediscovers the same
    # graph, so ONLY the durable frontier can prevent re-fetching finished work.
    pages = {SITE: _html(*all_urls[1:])} | {url: _html() for url in all_urls[1:]}

    async def allow_test_url(url: str) -> None:
        return None

    async def fake_scrape(url: str, **kwargs: Any) -> ScrapeResult:
        # Yield to the loop so the kill lands mid-flight, not between pages.
        await asyncio.sleep(0)
        return ScrapeResult(
            url=url,
            response_url=url,
            success=True,
            content_type="html",
            content_type_raw="text/html",
            status_code=200,
            raw_html=pages[url],
            raw_text="Durable crawl chaos regression content",
        )

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", fake_scrape)

    store = InMemoryExecutionStore()
    persister = _Persister()

    # --- Run 1: the process that dies -------------------------------------
    kill_switch = _KillSwitch(after=KILL_AFTER)
    doomed_queue = RuntimeWorkQueueBackend(store, EXECUTION_ID, holder="proc-A:pid-1")
    doomed = _crawler(doomed_queue, kill_switch, persister)

    run = asyncio.create_task(doomed.run())
    await asyncio.wait_for(kill_switch.tripped.wait(), timeout=10)
    # SIGKILL: the task dies, nothing is drained, in-flight claims are abandoned.
    run.cancel()
    await asyncio.gather(run, return_exceptions=True)

    counts = await store.work_item_counts(EXECUTION_ID)
    assert counts[WorkItemState.SUCCEEDED] >= 1, "the dead run settled nothing to resume past"
    unfinished = counts[WorkItemState.PENDING] + counts[WorkItemState.IN_PROGRESS]
    assert unfinished > 0, "the crawl finished before the kill — not a chaos test"
    settled_before_death = counts[WorkItemState.SUCCEEDED]
    persisted_before_death = list(persister.urls)

    # The dead process's leases expire; the item reaper returns its claims.
    # (Production: the same `reclaim_expired_work_items` sweep, on the clock.)
    future = datetime.now(UTC) + timedelta(seconds=DEFAULT_ITEM_LEASE_SECONDS + 1)
    in_flight_at_death = await store.reclaim_expired_work_items(now=future)

    # --- Run 2: the restarted process -------------------------------------
    # Fresh crawler, fresh in-memory everything, NEW holder — the only thing
    # carried across the restart is the durable frontier.
    resumed_queue = RuntimeWorkQueueBackend(store, EXECUTION_ID, holder="proc-B:pid-2")
    resumed = _crawler(resumed_queue, _Sink(), persister)
    await asyncio.wait_for(resumed.run(), timeout=30)

    # --- ZERO DROPPED ------------------------------------------------------
    assert set(persister.urls) == set(all_urls)
    counts = await store.work_item_counts(EXECUTION_ID)
    assert counts[WorkItemState.SUCCEEDED] == PAGE_COUNT
    assert counts[WorkItemState.PENDING] == 0
    assert counts[WorkItemState.IN_PROGRESS] == 0
    assert counts[WorkItemState.FAILED] == 0
    assert counts[WorkItemState.DEAD_LETTER] == 0

    # --- ZERO DUPLICATED, for everything the dead process settled ----------
    duplicates = {url for url in persister.urls if persister.urls.count(url) > 1}
    assert len(duplicates) <= in_flight_at_death, (
        "a page was re-fetched that was NOT in flight when the process died — "
        "the resume re-handed out settled work"
    )
    # The strong half of the guarantee: a SETTLED page is never re-crawled.
    settled_urls = set(persisted_before_death[:settled_before_death])
    assert not (settled_urls & duplicates)


@pytest.mark.asyncio
async def test_resumed_crawler_claims_the_same_execution_not_a_fresh_frontier() -> None:
    """The load-bearing mechanic behind the test above, isolated: a restarted
    process pointed at the same batch execution sees the surviving frontier —
    not an empty queue it would refill from scratch."""
    store = InMemoryExecutionStore()
    from matrx_scraper.queue_backend import QueueItem

    dead = RuntimeWorkQueueBackend(store, EXECUTION_ID, holder="proc-A:pid-1")
    await dead.enqueue_many(
        [QueueItem(url=u, depth=0, parent_url=None, source="seed") for u in _urls()]
    )
    claimed = await dead.dequeue()
    assert claimed is not None

    reborn = RuntimeWorkQueueBackend(store, EXECUTION_ID, holder="proc-B:pid-2")
    pending, in_flight = await reborn.counts()
    assert pending == PAGE_COUNT - 1
    assert in_flight == 1
    # Still leased by the dead process — a live claim is never stolen.
    assert await reborn.is_known(claimed.url) is True

    future = datetime.now(UTC) + timedelta(seconds=DEFAULT_ITEM_LEASE_SECONDS + 1)
    assert await store.reclaim_expired_work_items(now=future) == 1
    pending, in_flight = await reborn.counts()
    assert pending == PAGE_COUNT
    assert in_flight == 0
