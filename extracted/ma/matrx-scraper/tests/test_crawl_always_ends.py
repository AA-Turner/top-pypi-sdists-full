"""A crawl always reaches a terminal state, and a page past its deadline is fenced.

The live defect this pins (web.crawl_session 8beb27cd…, goliveinspain.com,
2026-10-12): two workers claimed sitemap URLs at 07:32:06 and never returned
from `_process`. Their durable claims expired at the 600 s item lease, other
workers re-claimed and fetched both pages at 07:42, and the frontier read
0 queued / 0 in flight from then on. But the wedged workers still held their
page-slot reservations, and the run loop's stop condition requires
`_pages_reserved == 0` — so it never broke. For 13+ hours it wrote a
`crawl_progress` row every 5 s and held the site's crawl lane (every new crawl 409).

Pinned here:
  1. The deadline is charged to the page's OWN work only and is derived from
     the claim lease knob, which the frontier gets too; held claims are renewed
     while the crawl lives, so a long 429 pause never expires one. The
     concurrency slot belongs to the claim: an abandoned task cannot keep it.
  2. Past its deadline an item task is fenced: nothing it does later lands
     (events, counters, frontier settles, persists).
  3. A failure is counted only when the deadline settle actually took the
     claim — a page that settled itself in the race is not a failure.
  4. The stall breaker ends a crawl whose wedged worker is out of the item
     deadline's reach — whatever the queue depth, whether or not its claim
     still reads in flight; frontier reads and claims are bounded in time.
"""

from __future__ import annotations

import asyncio
from dataclasses import replace

import pytest

import matrx_scraper.crawler as crawler_mod
from matrx_scraper.crawler import (
    CRAWL_KNOB_MIRRORS,
    ITEM_LEASE_MARGIN_SECONDS,
    ClaimFenced,
    CrawlKnobs,
    SiteCrawler,
    SiteCrawlerConfig,
)
from matrx_scraper.events import CrawlCompletedEvent, CrawlPageFailedEvent, CrawlWarningEvent
from matrx_scraper.queue_backend import InMemoryQueueBackend, QueueItem

from test_crawler import CapturingSink

# Generous outer bound: without the fix `run()` never returns at all.
RUN_BOUND_S = 10.0
# A lease this short gives a page-work deadline of LEASE / 2 (too short for the margin).
LEASE_S = 0.6
DEADLINE_S = LEASE_S / 2


@pytest.fixture
def short_lease(monkeypatch: pytest.MonkeyPatch) -> None:
    base = CrawlKnobs.load()
    monkeypatch.setattr(
        CrawlKnobs, "load", classmethod(lambda cls: replace(base, item_lease_seconds=LEASE_S))
    )
    monkeypatch.setattr(crawler_mod, "STALL_GRACE_SECONDS", 0.3)


def _crawler(
    queue: InMemoryQueueBackend,
    sink: CapturingSink,
    urls: list[str],
    *,
    concurrency: int = 2,
    body_persister: object = None,
) -> SiteCrawler:
    return SiteCrawler(
        run_id="always-ends",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            seed_urls=urls,
            list_mode=True,
            seed_from_sitemap=False,
            respect_robots=False,
            concurrency=concurrency,
            max_pages=50,
            progress_every_seconds=1.0,
            adaptive_pacing=False,
            host_rps=1000.0,
            host_burst=1000.0,
        ),
        event_sink=sink,
        queue_backend=queue,
        body_persister=body_persister,  # type: ignore[arg-type]
    )


def _deadline_notices(sink: CapturingSink) -> list[object]:
    warnings = [w for w in sink.of_type(CrawlWarningEvent) if "deadline" in w.message]
    failed = [f for f in sink.of_type(CrawlPageFailedEvent) if f.error_class == "ItemDeadlineExceeded"]
    return [*warnings, *failed]


# --- 1. the deadline: own work only, derived from the lease knob ------------


def test_deadline_is_the_lease_knob_minus_the_margin_and_the_frontier_gets_the_lease() -> None:
    runtime_queue = pytest.importorskip("matrx_scraper.web_crawl.runtime_queue")
    # The knob's seeded value IS the durable frontier's default lease.
    assert CRAWL_KNOB_MIRRORS["crawl.item_lease_seconds"] == runtime_queue.DEFAULT_ITEM_LEASE_SECONDS

    class LeaseRecordingQueue(InMemoryQueueBackend):
        lease: int | None = None

        def set_lease_seconds(self, lease_seconds: int) -> None:
            self.lease = lease_seconds

    queue = LeaseRecordingQueue()
    crawler = _crawler(queue, CapturingSink(), [])
    crawler._knobs = replace(crawler._knobs, item_lease_seconds=900.0)
    crawler._apply_item_lease()
    assert queue.lease == 900
    assert crawler._item_deadline_seconds() == 900.0 - ITEM_LEASE_MARGIN_SECONDS
    assert crawler._item_deadline_seconds() < queue.lease


@pytest.mark.asyncio
async def test_no_claim_expires_while_a_page_waits_out_a_long_429_pause(short_lease: None) -> None:
    """A Retry-After far longer than the claim lease must not expire the claim:
    the frontier reaper would re-pend it (duplicate fetch, then dead-letters)."""
    pytest.importorskip("matrx_runtime")
    from datetime import UTC, datetime

    from matrx_runtime.store import InMemoryExecutionStore

    from matrx_scraper.web_crawl.runtime_queue import RuntimeWorkQueueBackend

    store = InMemoryExecutionStore()
    queue = RuntimeWorkQueueBackend(store, "exec-pause", holder="proc:1")
    sink = CapturingSink()
    crawler = _crawler(queue, sink, ["https://x.test/a"], concurrency=1)  # type: ignore[arg-type]
    pages: list[str] = []

    async def page_work(item: QueueItem) -> None:
        pages.append(item.url)
        crawler._pages_fetched += 1
        await crawler.queue.mark_done(item.url)

    crawler._process_page = page_work  # type: ignore[method-assign]
    # The site said "come back in 3 s" — 3x the 1 s lease the frontier gets.
    crawler._knobs = replace(crawler._knobs, item_lease_seconds=1.0)
    crawler._pause.record_limit(3.0)

    reclaimed = 0
    reaping = True

    async def frontier_reaper() -> None:
        nonlocal reclaimed
        while reaping:
            reclaimed += await store.reclaim_expired_work_items(now=datetime.now(UTC))
            await asyncio.sleep(0.05)

    reaper = asyncio.create_task(frontier_reaper())
    try:
        await asyncio.wait_for(crawler.run(), timeout=RUN_BOUND_S)
    finally:
        reaping = False
        await reaper

    assert reclaimed == 0
    assert pages == ["https://x.test/a"]
    items = await store.list_work_items("exec-pause")
    assert [i.attempts for i in items] == [1]
    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.status == "completed"


@pytest.mark.asyncio
async def test_a_task_that_swallows_its_cancel_does_not_keep_the_concurrency_slot(
    short_lease: None,
) -> None:
    """Reviewer probe: concurrency 1, page A swallows CancelledError, page B
    queued. The abandoned task kept the slot, B waited on it forever (its
    deadline never started), and the stall breaker stood down — run() hung."""
    queue = InMemoryQueueBackend()
    sink = CapturingSink()
    crawler = _crawler(queue, sink, ["https://x.test/a", "https://x.test/b"], concurrency=1)
    finished = False

    async def page_work(item: QueueItem) -> None:
        if item.url.endswith("/a"):
            while not finished:  # a wedge that swallows cancellation (a shielded call)
                try:
                    await asyncio.sleep(0.05)
                except asyncio.CancelledError:
                    continue
            return
        crawler._pages_fetched += 1
        await crawler.queue.mark_done(item.url)

    crawler._process_page = page_work  # type: ignore[method-assign]
    try:
        await asyncio.wait_for(crawler.run(), timeout=RUN_BOUND_S)
    finally:
        finished = True
        await asyncio.sleep(0.1)

    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.pages_fetched == 1  # B
    failed = sink.of_type(CrawlPageFailedEvent)
    assert [(f.url, f.error_class) for f in failed] == [("https://x.test/a", "ItemDeadlineExceeded")]
    assert crawler._semaphore._value == 1  # every slot returned


@pytest.mark.asyncio
async def test_item_that_always_wedges_fails_after_its_retries_and_the_run_ends(
    short_lease: None,
) -> None:
    queue = InMemoryQueueBackend()
    sink = CapturingSink()
    crawler = _crawler(queue, sink, ["https://x.test/wedge"])
    calls = 0

    async def process(item: QueueItem) -> None:
        nonlocal calls
        calls += 1
        crawler._begin_page_work()
        await asyncio.Event().wait()

    crawler._process = process  # type: ignore[method-assign]
    await asyncio.wait_for(crawler.run(), timeout=RUN_BOUND_S)

    assert calls == crawler._knobs.max_retries_per_url + 1
    failed = sink.of_type(CrawlPageFailedEvent)
    assert [f.error_class for f in failed] == ["ItemDeadlineExceeded"]
    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.pages_failed == 1
    assert completed.coverage_complete is False
    assert await queue.in_flight_count() == 0
    assert await queue.queue_depth() == 0


# --- 2. the fence ------------------------------------------------------------


@pytest.mark.asyncio
async def test_an_abandoned_item_task_cannot_write_after_its_deadline(short_lease: None) -> None:
    """A task blocked past its deadline (a thread, a browser) wakes up later and
    tries to emit, count, settle and persist — while the requeued item already
    belongs to another worker. Every one of those writes is dropped."""

    class RecordingQueue(InMemoryQueueBackend):
        def __init__(self) -> None:
            super().__init__()
            self.done: list[str] = []

        async def mark_done(self, url: str) -> None:
            self.done.append(url)
            await super().mark_done(url)

    persisted: list[str] = []

    async def persister(url: str) -> str:
        persisted.append(url)
        return url

    queue = RecordingQueue()
    sink = CapturingSink()
    crawler = _crawler(queue, sink, ["https://x.test/p"], concurrency=1, body_persister=persister)
    release = asyncio.Event()
    late: dict[str, object] = {}
    calls = 0

    async def process(item: QueueItem) -> None:
        nonlocal calls
        calls += 1
        crawler._begin_page_work()
        if calls == 1:
            try:
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                # Like a thread / subprocess browser: the cancel cannot stop it.
                await release.wait()
            await crawler._emit(CrawlWarningEvent(run_id=crawler.run_id, message="LATE WRITE"))
            crawler._pages_fetched += 1
            await crawler.queue.mark_done(item.url)
            try:
                await crawler.body_persister(item.url)  # type: ignore[misc]
            except ClaimFenced:
                late["persist_refused"] = True
            late["finished"] = True
            return
        crawler._pages_fetched += 1
        await crawler.body_persister(item.url)  # type: ignore[misc]
        await crawler.queue.mark_done(item.url)

    crawler._process = process  # type: ignore[method-assign]
    await asyncio.wait_for(crawler.run(), timeout=RUN_BOUND_S)

    release.set()
    for _ in range(100):
        if late.get("finished"):
            break
        await asyncio.sleep(0.01)
    assert late == {"persist_refused": True, "finished": True}
    assert calls == 2
    assert [w for w in sink.of_type(CrawlWarningEvent) if w.message == "LATE WRITE"] == []
    assert crawler._pages_fetched == 1
    assert queue.done == ["https://x.test/p"]
    assert persisted == ["https://x.test/p"]


# --- 3. the race: a page that settled itself is not a failure ---------------


@pytest.mark.asyncio
async def test_a_page_that_settled_its_claim_before_the_deadline_settle_is_not_a_failure(
    short_lease: None,
) -> None:
    """The production shape too: the frontier settles, the worker never returns."""
    queue = InMemoryQueueBackend()
    sink = CapturingSink()
    crawler = _crawler(queue, sink, ["https://x.test/ok", "https://x.test/settled-then-stuck"])

    async def process(item: QueueItem) -> None:
        crawler._begin_page_work()
        crawler._pages_fetched += 1
        await crawler.queue.mark_done(item.url)
        if item.url.endswith("/settled-then-stuck"):
            await asyncio.Event().wait()

    crawler._process = process  # type: ignore[method-assign]
    await asyncio.wait_for(crawler.run(), timeout=RUN_BOUND_S)

    assert crawler._pages_reserved == 0
    assert _deadline_notices(sink) == []
    assert crawler._deadline_attempts == {}
    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.status == "completed"
    assert completed.pages_failed == 0
    assert completed.pages_fetched == 2
    assert completed.remaining_queue_depth == 0


# --- 4. the stall breaker ----------------------------------------------------


@pytest.mark.asyncio
async def test_worker_wedged_before_its_claim_stops_the_run_as_stalled(short_lease: None) -> None:
    class HangingClaimQueue(InMemoryQueueBackend):
        hang_next = True

        async def dequeue(self) -> QueueItem | None:
            if self.hang_next:
                self.hang_next = False
                await asyncio.Event().wait()
            return await super().dequeue()

    queue = HangingClaimQueue()
    sink = CapturingSink()
    crawler = _crawler(queue, sink, ["https://x.test/a"])

    async def process(item: QueueItem) -> None:
        crawler._begin_page_work()
        crawler._pages_fetched += 1
        await crawler.queue.mark_done(item.url)

    crawler._process = process  # type: ignore[method-assign]
    await asyncio.wait_for(crawler.run(), timeout=RUN_BOUND_S)

    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.status == "stopped"
    assert completed.stop_reason == "stalled_worker"
    assert completed.error_message and "stalled" in completed.error_message
    assert completed.pages_fetched == 1


@pytest.mark.asyncio
async def test_worker_wedged_while_its_claim_reads_in_flight_still_stops_the_run(
    short_lease: None,
) -> None:
    """The claim committed, then the worker hung: in flight forever, beyond the
    item deadline's reach. The breaker must not wait for in-flight to read 0."""

    class ClaimThenHangQueue(InMemoryQueueBackend):
        async def dequeue(self) -> QueueItem | None:
            item = await super().dequeue()
            if item is not None:
                await asyncio.Event().wait()
            return item

    queue = ClaimThenHangQueue()
    sink = CapturingSink()
    crawler = _crawler(queue, sink, ["https://x.test/a"], concurrency=1)
    crawler._process = None  # type: ignore[assignment,method-assign]  # never reached

    await asyncio.wait_for(crawler.run(), timeout=RUN_BOUND_S)

    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.status == "stopped"
    assert completed.stop_reason == "stalled_worker"
    assert "1 page(s) still claimed" in (completed.error_message or "")


@pytest.mark.asyncio
async def test_every_claim_hanging_with_work_still_queued_stops_the_run(
    short_lease: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every worker hangs in dequeue() (a DB call) while pages are queued."""
    monkeypatch.setattr(crawler_mod, "QUEUE_CALL_TIMEOUT_SECONDS", 0.2, raising=False)

    class HangingDequeueQueue(InMemoryQueueBackend):
        async def dequeue(self) -> QueueItem | None:
            await asyncio.Event().wait()
            return None

    queue = HangingDequeueQueue()
    sink = CapturingSink()
    crawler = _crawler(queue, sink, ["https://x.test/a", "https://x.test/b"])

    await asyncio.wait_for(crawler.run(), timeout=RUN_BOUND_S)

    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.status == "stopped"
    assert completed.stop_reason == "stalled_worker"
    assert completed.remaining_queue_depth == 2


@pytest.mark.asyncio
async def test_a_frontier_read_that_never_answers_stops_the_run(
    short_lease: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`counts()` hangs once the crawl is under way — the run loop's own read."""
    monkeypatch.setattr(crawler_mod, "QUEUE_CALL_TIMEOUT_SECONDS", 0.2, raising=False)

    class HangingCountsQueue(InMemoryQueueBackend):
        hang = False

        async def dequeue(self) -> QueueItem | None:
            self.hang = True
            return await super().dequeue()

        async def counts(self) -> tuple[int, int]:
            if self.hang:
                await asyncio.Event().wait()
            return await super().counts()

    queue = HangingCountsQueue()
    sink = CapturingSink()
    crawler = _crawler(queue, sink, ["https://x.test/a"], concurrency=1)

    async def process(item: QueueItem) -> None:
        crawler._begin_page_work()
        crawler._pages_fetched += 1
        await crawler.queue.mark_done(item.url)

    crawler._process = process  # type: ignore[method-assign]
    await asyncio.wait_for(crawler.run(), timeout=RUN_BOUND_S)

    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.pages_fetched == 1
    assert completed.stop_reason == "stalled_worker"


# --- final edges ---------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize("interval", [0.4, 0.9])
async def test_a_slow_but_healthy_host_is_never_judged_stalled(
    short_lease: None, interval: float
) -> None:
    """Reviewer probe: a host paced slower than deadline + grace (0.6 s here)."""
    queue = InMemoryQueueBackend()
    sink = CapturingSink()
    urls = [f"https://x.test/{i}" for i in range(5)]
    crawler = SiteCrawler(
        run_id="slow",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            seed_urls=urls,
            list_mode=True,
            seed_from_sitemap=False,
            respect_robots=False,
            concurrency=2,
            max_pages=50,
            adaptive_pacing=False,
            host_rps=1.0 / interval,
            host_burst=1.0,
        ),
        event_sink=sink,
        queue_backend=queue,
    )
    crawler._rate_limiter.max_wait_seconds = 60

    async def page_work(item: QueueItem) -> None:
        crawler._pages_fetched += 1
        await crawler.queue.mark_done(item.url)

    crawler._process_page = page_work  # type: ignore[method-assign]
    await asyncio.wait_for(crawler.run(), timeout=20)

    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert (completed.status, completed.stop_reason, completed.pages_fetched) == ("completed", None, 5)


@pytest.mark.asyncio
async def test_an_abandoned_task_cannot_pause_stop_or_deproxy_the_crawl() -> None:
    import contextvars

    from matrx_scraper.crawler import _CLAIM_FENCE, _ClaimFence

    crawler = _crawler(InMemoryQueueBackend(), CapturingSink(), [])
    fence = _ClaimFence()
    fence.expired = True
    ctx = contextvars.copy_context()
    ctx.run(_CLAIM_FENCE.set, fence)

    async def zombie() -> None:
        assert crawler._record_crawl_pause(30.0) == 0.0
        await crawler._stop_for_rate_limits("too many 429s")
        await crawler._emit_proxy_bypass("https://x.test/a", status=502)

    await asyncio.create_task(zombie(), context=ctx)

    assert crawler._pause.remaining() == 0
    assert crawler._stop_reason is None
    assert crawler._proxy_disabled is False
    # The same writes from a live task still land.
    assert crawler._record_crawl_pause(30.0) > 0
