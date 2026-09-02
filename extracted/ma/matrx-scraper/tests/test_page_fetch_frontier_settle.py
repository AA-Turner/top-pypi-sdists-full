"""Every terminal outcome of a crawl run settles its frontier — including teardown.

The live defect this pins (176 failed `page_fetch` sessions in two days,
one every 10 minutes, all one 404 URL): a single-URL run's only worker
reserved its page slot, and the run loop's page-budget stop condition
(`fetched + reserved >= max_pages and inflight == 0`) fired before the
worker's durable claim was VISIBLE to `counts()` (a DB read racing the
claim's commit). The loop tore the worker down mid-item, nothing settled
the claim, and the truncation gate — correctly — recorded the run FAILED
with "1 item(s) in flight and 0 queued, after fetching 0 of 1".

Two independent layers, each asserted here, each sufficient alone:
  1. The run loop never stops for the page budget while any worker holds a
     reserved slot (`_pages_reserved > 0` means work is possibly invisible).
  2. A worker cancelled mid-item requeues its claim (will_retry) before the
     CancelledError propagates, so even a torn-down worker strands nothing.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_scraper.crawler import SiteCrawler, SiteCrawlerConfig
from matrx_scraper.events import (
    CrawlCompletedEvent,
    CrawlPageFailedEvent,
)
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.queue_backend import InMemoryQueueBackend, QueueItem

from test_crawler import CapturingSink


def _result_404(url: str) -> ScrapeResult:
    return ScrapeResult(
        url=url,
        response_url=url,
        success=False,
        content_type="html",
        status_code=404,
        failure_reason="bad_status",
        failure_details=[{"bad_status": "Status code 404"}],
    )


def _page_fetch_crawler(queue: InMemoryQueueBackend, sink: CapturingSink) -> SiteCrawler:
    """The exact shape `prepare_page_fetch` runs: one URL, max_pages=1, list mode."""
    return SiteCrawler(
        run_id="page-fetch-settle",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            seed_urls=["https://x.test/gone"],
            max_pages=1,
            max_depth=0,
            concurrency=1,
            list_mode=True,
            seed_from_sitemap=False,
            respect_robots=False,
        ),
        event_sink=sink,
        queue_backend=queue,
    )


class SlowClaimQueue(InMemoryQueueBackend):
    """A frontier whose claim is INVISIBLE for a moment — the durable reality.

    `RuntimeWorkQueueBackend.dequeue` is a DB round-trip; until its UPDATE
    commits, `counts()` still reports the item as pending with nothing in
    flight. This emulation holds the item un-claimed for `delay` seconds so
    the run loop's stop conditions race it exactly like production did.
    """

    def __init__(self, delay: float = 0.35) -> None:
        super().__init__()
        self._delay = delay

    async def dequeue(self) -> QueueItem | None:
        if self._queue.qsize() > 0:
            await asyncio.sleep(self._delay)
        return await super().dequeue()


@pytest.mark.asyncio
async def test_single_url_404_run_settles_frontier_and_completes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The offline repro from the handoff ledger: a page_fetch whose only URL 404s
    must end `completed` (pages_failed=1) with an EMPTY frontier — never a
    truncation-gate failure with the item still in flight."""

    async def allow_test_url(url: str) -> None:
        return None

    async def always_404(url: str, **kwargs: Any) -> ScrapeResult:
        return _result_404(url)

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", always_404)

    queue = InMemoryQueueBackend()
    sink = CapturingSink()
    await _page_fetch_crawler(queue, sink).run()

    completed = sink.of_type(CrawlCompletedEvent)
    assert len(completed) == 1
    assert completed[0].status == "completed"
    assert completed[0].error_message is None
    assert completed[0].pages_failed == 1
    assert await queue.counts() == (0, 0)
    assert len(sink.of_type(CrawlPageFailedEvent)) == 1


@pytest.mark.asyncio
async def test_page_budget_stop_waits_for_invisible_claim(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """THE race. With the claim invisible for 350ms, the old stop condition
    (`fetched + reserved >= max_pages and inflight == 0`) broke out of the run
    loop on its first tick, cancelled the worker mid-claim, and stranded the
    item in flight. The loop must wait for reserved slots to resolve."""

    async def allow_test_url(url: str) -> None:
        return None

    async def always_404(url: str, **kwargs: Any) -> ScrapeResult:
        return _result_404(url)

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", always_404)

    queue = SlowClaimQueue()
    sink = CapturingSink()
    await _page_fetch_crawler(queue, sink).run()

    completed = sink.of_type(CrawlCompletedEvent)
    assert len(completed) == 1
    # The one URL was actually processed — not torn down un-fetched.
    assert completed[0].status == "completed", completed[0].error_message
    assert completed[0].pages_failed == 1
    assert await queue.counts() == (0, 0)


@pytest.mark.asyncio
async def test_cancelled_worker_requeues_its_in_flight_item(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Layer 2: a worker torn down mid-fetch settles its claim back to pending
    before the CancelledError propagates — a resumed run finds the URL STILL
    TO DO instead of leased to a dead process."""

    fetch_started = asyncio.Event()

    async def allow_test_url(url: str) -> None:
        return None

    async def hang_forever(url: str, **kwargs: Any) -> ScrapeResult:
        fetch_started.set()
        await asyncio.sleep(3600)
        raise AssertionError("unreachable")

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", hang_forever)

    queue = InMemoryQueueBackend()
    sink = CapturingSink()
    run_task = asyncio.create_task(_page_fetch_crawler(queue, sink).run())
    await asyncio.wait_for(fetch_started.wait(), timeout=5)
    assert (await queue.counts())[1] == 1  # claimed, mid-fetch

    run_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await run_task

    # Back on the frontier as pending work — nothing in flight, nothing lost.
    assert await queue.counts() == (1, 0)


class DeadLetteringQueue(InMemoryQueueBackend):
    """A frontier reporting that the store's attempt budget parked one item."""

    async def dead_letter_count(self) -> int:
        return 1


@pytest.mark.asyncio
async def test_dead_letters_break_coverage_complete(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A dead-lettered item was neither fetched nor counted failed — a run
    carrying one must never claim `coverage_complete`."""

    async def allow_test_url(url: str) -> None:
        return None

    async def scrape_ok(url: str, **kwargs: Any) -> ScrapeResult:
        return ScrapeResult(
            url=url,
            response_url=url,
            success=True,
            content_type="html",
            content_type_raw="text/html; charset=UTF-8",
            status_code=200,
            raw_html="<html><head><title>t</title></head><body>ok</body></html>",
            raw_text="ok",
        )

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", scrape_ok)

    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="dead-letter-coverage",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            seed_urls=["https://x.test/only"],
            max_pages=1,
            concurrency=1,
            list_mode=True,
            seed_from_sitemap=False,
            respect_robots=False,
        ),
        event_sink=sink,
        queue_backend=DeadLetteringQueue(),
    )
    await crawler.run()

    completed = sink.of_type(CrawlCompletedEvent)
    assert len(completed) == 1
    assert completed[0].status == "completed"
    # A clean run over the same queue WITHOUT dead-letters is coverage-complete
    # (pinned elsewhere); the dead-letter is the only thing withholding it here.
    assert completed[0].coverage_complete is False
