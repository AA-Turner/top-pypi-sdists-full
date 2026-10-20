"""A crawl with a time budget stops cleanly when it is spent and says why.

Live defect (Smart Add, Radiance Medical Spa, 2026-10-16): a brand crawl with only a 500-page cap ran over 55
minutes (162 fetched, 41 queued) while a person waited for their products. `time_budget_seconds` ends it
`stopped` with stop_reason `time_budget`; with no budget the crawl is unchanged.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_scraper.crawler import SiteCrawler, SiteCrawlerConfig
from matrx_scraper.events import CrawlCompletedEvent, CrawlWarningEvent
from matrx_scraper.queue_backend import InMemoryQueueBackend, QueueItem

from test_crawler import CapturingSink

URLS = [f"https://x.test/p{i}" for i in range(40)]


def _crawler(sink: CapturingSink, **extra: object) -> SiteCrawler:
    crawler = SiteCrawler(
        run_id="budget",
        config=SiteCrawlerConfig(
            base_url="https://x.test/", seed_urls=URLS, list_mode=True, seed_from_sitemap=False,
            respect_robots=False, concurrency=1, max_pages=100, progress_every_seconds=1.0,
            adaptive_pacing=False, host_rps=1000.0, host_burst=1000.0, **extra,  # type: ignore[arg-type]
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
    )

    async def process(item: QueueItem) -> None:
        crawler._begin_page_work()
        await asyncio.sleep(0.25)
        crawler._pages_fetched += 1
        await crawler.queue.mark_done(item.url)

    crawler._process = process  # type: ignore[method-assign]
    return crawler


@pytest.mark.asyncio
async def test_a_spent_time_budget_stops_the_crawl_cleanly_and_records_why() -> None:
    sink = CapturingSink()
    crawler = _crawler(sink, time_budget_seconds=1)
    await asyncio.wait_for(crawler.run(), timeout=15)

    done = sink.of_type(CrawlCompletedEvent)[0]
    assert done.status == "stopped"
    assert done.stop_reason == "time_budget"
    assert 0 < done.pages_fetched < len(URLS)
    assert done.remaining_queue_depth > 0
    assert done.error_message and "time budget" in done.error_message
    assert any((w.context or {}).get("stop_reason") == "time_budget" for w in sink.of_type(CrawlWarningEvent))


@pytest.mark.asyncio
async def test_no_budget_means_the_crawl_runs_to_the_end() -> None:
    sink = CapturingSink()
    crawler = _crawler(sink)
    crawler.config.seed_urls = URLS[:3]
    await asyncio.wait_for(crawler.run(), timeout=15)
    done = sink.of_type(CrawlCompletedEvent)[0]
    assert done.stop_reason is None
    assert done.status == "completed"


def test_the_start_request_carries_the_budget() -> None:
    from matrx_scraper.web_crawl.contracts import CrawlStartRequest

    assert CrawlStartRequest().time_budget_seconds is None
    assert CrawlStartRequest(time_budget_seconds=600).time_budget_seconds == 600
    with pytest.raises(ValueError):
        CrawlStartRequest(time_budget_seconds=0)
