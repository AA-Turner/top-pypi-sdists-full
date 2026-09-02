"""The truncation gate: a run that stops with work left must never say 'complete'."""

from __future__ import annotations
import pytest

from matrx_scraper.crawler import (  # noqa: E402
    PersistResult,
    RENDER_HTTP_ONLY,
    SiteCrawler,
    SiteCrawlerConfig,
)
from matrx_scraper.events import CrawlCompletedEvent, CrawlWarningEvent  # noqa: E402
from matrx_scraper.orchestrator import ScrapeResult  # noqa: E402
from matrx_scraper.queue_backend import InMemoryQueueBackend  # noqa: E402

SITE = "https://trunc.test/"
HTML = "<html><head><title>T</title></head><body>" + ("word " * 200) + "</body></html>"


class _Sink:
    def __init__(self) -> None:
        self.completed: CrawlCompletedEvent | None = None
        self.warnings: list[CrawlWarningEvent] = []

    async def emit(self, e) -> None:  # noqa: ANN001
        if isinstance(e, CrawlCompletedEvent):
            self.completed = e
        elif isinstance(e, CrawlWarningEvent):
            self.warnings.append(e)


class _P:
    async def __call__(self, r):  # noqa: ANN001
        return PersistResult(page_id="p", snapshot_id="s")


def _crawler(queue, sink, *, max_pages: int = 10, seeds: list[str] | None = None):  # noqa: ANN001
    return SiteCrawler(
        run_id="r",
        event_sink=sink,
        queue_backend=queue,
        body_persister=_P(),
        strict_persistence=True,
        retain_results=False,
        config=SiteCrawlerConfig(
            base_url=SITE,
            max_pages=max_pages,
            max_depth=0,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            list_mode=True,
            seed_urls=seeds or [SITE],
            render_mode=RENDER_HTTP_ONLY,
            host_rps=1000.0,
        ),
    )


@pytest.fixture(autouse=True)
def _net(monkeypatch):  # noqa: ANN001
    async def ok(u):  # noqa: ANN001
        return None

    async def fake_scrape(url, **kw):  # noqa: ANN001
        return ScrapeResult(
            url=url,
            response_url=url,
            success=True,
            content_type="html",
            content_type_raw="text/html",
            status_code=200,
            raw_html=HTML,
            raw_text="word " * 200,
        )

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", ok)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", fake_scrape)


@pytest.mark.asyncio
async def test_normal_run_still_reports_completed() -> None:
    """The gate must not cry wolf on a clean crawl."""
    sink = _Sink()
    await _crawler(InMemoryQueueBackend(), sink).run()
    assert sink.completed.status == "completed"
    assert sink.completed.error_message is None
    assert not [w for w in sink.warnings if (w.context or {}).get("truncated")]


class _LyingQueue(InMemoryQueueBackend):
    """Reports an empty frontier to the run loop, leftovers to the final tally.

    This is not a contrivance — it is the EXACT production signature. The
    truncated page_fetch runs ended with `counts()` reporting nothing in flight
    (which is why the loop exited) while the durable frontier still held a
    claimed item. Whatever caused that disagreement, the completion tally must
    not launder it into a success.
    """

    def __init__(self, *, left_queued: int = 0, left_in_flight: int = 0) -> None:
        super().__init__()
        self._left_queued = left_queued
        self._left_in_flight = left_in_flight
        self._drained = False

    async def counts(self) -> tuple[int, int]:
        real = await super().counts()
        if real == (0, 0):
            self._drained = True
        return real

    async def queue_depth(self) -> int:
        return self._left_queued if self._drained else await super().queue_depth()

    async def in_flight_count(self) -> int:
        return self._left_in_flight if self._drained else await super().in_flight_count()


@pytest.mark.asyncio
async def test_abandoned_in_flight_work_is_failed_not_complete() -> None:
    """THE bug, exactly: the loop exits believing the frontier is empty while an
    item is still claimed. That run is FAILED — which also keeps it eligible for
    the crash-resume sweep instead of being buried as a success."""
    sink = _Sink()
    await _crawler(_LyingQueue(left_in_flight=1), sink).run()
    assert sink.completed.status == "failed", (
        "a run that abandoned in-flight work must NOT report success"
    )
    assert "truncated" in (sink.completed.error_message or "").lower()
    assert sink.completed.coverage_complete is False
    assert [w for w in sink.warnings if (w.context or {}).get("truncated")], (
        "truncation must SCREAM, not just flip a field"
    )


@pytest.mark.asyncio
async def test_leftover_queued_work_is_failed_too() -> None:
    """Same rule for work never claimed at all."""
    sink = _Sink()
    await _crawler(_LyingQueue(left_queued=3), sink).run()
    assert sink.completed.status == "failed"
    assert "3 queued" in (sink.completed.error_message or "")


@pytest.mark.asyncio
async def test_hitting_the_page_budget_is_not_truncation() -> None:
    """Legitimate leftover work: the crawl hit max_pages. Still 'completed'."""
    queue = InMemoryQueueBackend()
    sink = _Sink()
    crawler = _crawler(queue, sink, max_pages=1, seeds=[SITE, f"{SITE}b", f"{SITE}c"])
    await crawler.run()
    assert sink.completed.status == "completed"
    assert sink.completed.limit_reached is True
    assert sink.completed.error_message is None


@pytest.mark.asyncio
async def test_user_cancel_is_not_truncation() -> None:
    """A cancel is a deliberate choice and keeps its own status."""
    queue = InMemoryQueueBackend()
    sink = _Sink()
    crawler = _crawler(queue, sink, seeds=[SITE, f"{SITE}b", f"{SITE}c"])
    crawler.cancel()
    await crawler.run()
    assert sink.completed.status == "canceled"
    assert sink.completed.error_message is None
