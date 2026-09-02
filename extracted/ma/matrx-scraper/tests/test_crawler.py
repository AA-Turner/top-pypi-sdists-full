"""Tests for SiteCrawler.

Two layers:
  1. **Unit** — `InMemoryQueueBackend` semantics, no network. Always run.
  2. **Integration** — small live crawl of https://raymarcleaners.com/ to
     confirm the full pipeline works end-to-end. Marked `@pytest.mark.network`
     and skipped by default to keep CI deterministic. Run with:

         uv run pytest packages/matrx-scraper/tests/test_crawler.py -v -m network

     Mock-server-based tests were tried but trip our content-filtering
     pipeline because the parser flags toy HTML as low_text_content. A real
     small site is the right level for an end-to-end smoke test.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_scraper.crawler import (
    PersistResult,
    RENDER_BROWSER_WITH_SCREENSHOT,
    RENDER_HTTP_ONLY,
    SiteCrawler,
    SiteCrawlerConfig,
)
from matrx_scraper.browser_pool import CapturedScreenshot, FetchWithCaptureResult
from matrx_scraper.events import (
    CrawlCompletedEvent,
    CrawlEvent,
    CrawlPageDiscoveredEvent,
    CrawlPageFailedEvent,
    CrawlPageFetchedEvent,
    CrawlPageParsedEvent,
    CrawlProgressEvent,
    CrawlStartedEvent,
    CrawlUrlClassifiedEvent,
    CrawlUrlsClassifiedEvent,
    CrawlWarningEvent,
)
from matrx_scraper.queue_backend import InMemoryQueueBackend, QueueItem


# ---------------------------------------------------------------------------
# Unit — queue backend (no network)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_in_memory_queue_dedupes() -> None:
    q = InMemoryQueueBackend()
    assert await q.enqueue(QueueItem("https://x.test/", 0, None, "seed")) is True
    assert await q.enqueue(QueueItem("https://x.test/", 0, None, "seed")) is False
    assert await q.queue_depth() == 1

    item = await q.dequeue()
    assert item is not None
    assert await q.queue_depth() == 0
    assert await q.in_flight_count() == 1
    await q.mark_done(item.url)
    assert await q.in_flight_count() == 0


@pytest.mark.asyncio
async def test_in_memory_queue_returns_none_when_empty() -> None:
    q = InMemoryQueueBackend()
    assert await q.dequeue() is None


@pytest.mark.asyncio
async def test_known_tracking() -> None:
    q = InMemoryQueueBackend()
    assert await q.is_known("https://x.test/a") is False
    await q.enqueue(QueueItem("https://x.test/a", 0, None, "seed"))
    assert await q.is_known("https://x.test/a") is True


@pytest.mark.asyncio
async def test_completion_disqualifies_coverage_when_page_cap_leaves_work() -> None:
    queue = InMemoryQueueBackend()
    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="cap-test",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            concurrency=1,
            seed_from_sitemap=False,
            seed_urls=["https://x.test/a", "https://x.test/b"],
            list_mode=True,
        ),
        event_sink=sink,
        queue_backend=queue,
    )

    async def process_without_network(item: QueueItem) -> None:
        crawler._pages_fetched += 1
        await queue.mark_done(item.url)

    crawler._process = process_without_network  # type: ignore[method-assign]
    await crawler.run()

    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.limit_reached is True
    assert completed.remaining_queue_depth == 1
    assert completed.coverage_complete is False


@pytest.mark.asyncio
async def test_completion_qualifies_coverage_only_after_clean_queue_drain() -> None:
    queue = InMemoryQueueBackend()
    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="drain-test",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=5,
            concurrency=1,
            seed_from_sitemap=False,
            seed_urls=["https://x.test/a"],
            list_mode=True,
        ),
        event_sink=sink,
        queue_backend=queue,
    )

    async def process_without_network(item: QueueItem) -> None:
        crawler._pages_fetched += 1
        await queue.mark_done(item.url)

    crawler._process = process_without_network  # type: ignore[method-assign]
    await crawler.run()

    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.limit_reached is False
    assert completed.remaining_queue_depth == 0
    assert completed.coverage_complete is True


@pytest.mark.asyncio
async def test_max_pages_is_hard_cap_under_higher_concurrency() -> None:
    queue = InMemoryQueueBackend()
    crawler = SiteCrawler(
        run_id="concurrent-cap-test",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=2,
            concurrency=8,
            seed_from_sitemap=False,
            seed_urls=[f"https://x.test/{index}" for index in range(10)],
            list_mode=True,
        ),
        event_sink=CapturingSink(),
        queue_backend=queue,
    )
    dispatched: list[str] = []

    async def process_without_network(item: QueueItem) -> None:
        dispatched.append(item.url)
        # Give all eight workers an opportunity to race for work. Without an
        # atomic pre-dispatch reservation, this deterministically exceeds two.
        await asyncio.sleep(0.01)
        crawler._pages_fetched += 1
        await queue.mark_done(item.url)

    crawler._process = process_without_network  # type: ignore[method-assign]
    await crawler.run()

    assert len(dispatched) == 2
    assert crawler._pages_reserved == 0
    assert await queue.in_flight_count() == 0
    assert await queue.queue_depth() == 8


@pytest.mark.asyncio
async def test_rejected_url_decision_is_emitted_for_the_crawl_ledger() -> None:
    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="ledger-test",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            seed_from_sitemap=False,
        ),
        event_sink=sink,
    )

    accepted, classification, outcome, reason_code = await crawler._classify_enqueue(
        "https://external.test/page",
        depth=1,
    )
    assert accepted is False
    await crawler._emit_url_decision(
        "https://external.test/page",
        normalized_url="https://external.test/page",
        depth=1,
        parent_url="https://x.test/",
        source="link",
        classification=classification,
        outcome=outcome,
        reason_code=reason_code,
    )

    decision = sink.of_type(CrawlUrlClassifiedEvent)[0]
    assert decision.classification == "external"
    assert decision.outcome == "excluded"
    assert decision.reason_code == "outside_site_scope"
    assert decision.is_in_scope is False


# ---------------------------------------------------------------------------
# Capturing sink — collects every event in memory
# ---------------------------------------------------------------------------


class CapturingSink:
    def __init__(self) -> None:
        self.events: list[CrawlEvent] = []

    async def emit(self, event: CrawlEvent) -> None:
        self.events.append(event)

    def of_type(self, *types: type) -> list[Any]:
        return [e for e in self.events if isinstance(e, types)]


class _RecordingPersister:
    def __init__(self) -> None:
        self.requests: list[Any] = []
        self.expected = 0
        self.captured = 0

    async def record_screenshots_expected(self, count: int) -> None:
        self.expected += count

    async def record_screenshots_captured(self, count: int) -> None:
        self.captured += count

    async def __call__(self, request: Any) -> PersistResult:
        self.requests.append(request)
        return PersistResult(
            body_file_id=f"body-{len(self.requests)}",
            screenshot_file_ids={
                shot.kind: f"shot-{len(self.requests)}-{shot.kind}" for shot in request.screenshots
            },
        )


def _page_html(*links: str) -> str:
    anchors = "".join(f'<a href="{link}">{link}</a>' for link in links)
    body = " ".join(["Useful crawl regression content"] * 80)
    return f"<html><head><title>Page</title></head><body>{body}{anchors}</body></html>"


@pytest.mark.asyncio
async def test_every_bfs_page_captures_and_persists_every_requested_screenshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def allow_test_url(url: str) -> None:
        return None

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)

    pages = {
        "https://x.test/": _page_html("/about", "/contact"),
        "https://x.test/about": _page_html(),
        "https://x.test/contact": _page_html(),
    }

    class BrowserPool:
        def __init__(self) -> None:
            self.urls: list[str] = []

        async def fetch_with_capture(self, url: str, **kwargs: Any) -> FetchWithCaptureResult:
            self.urls.append(url)
            kinds = kwargs["screenshot_kinds"]
            return FetchWithCaptureResult(
                content=pages[url],
                response_url=url,
                status_code=200,
                headers={"content-type": "text/html"},
                title="Page",
                screenshots=[
                    CapturedScreenshot(kind=kind, width=1366, height=768, bytes=b"PNG")
                    for kind in kinds
                ],
            )

    browser = BrowserPool()
    persister = _RecordingPersister()
    crawler = SiteCrawler(
        run_id="all-pages-screenshot-regression",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=3,
            concurrency=2,
            respect_robots=False,
            seed_from_sitemap=False,
            render_mode=RENDER_BROWSER_WITH_SCREENSHOT,
            capture_screenshots=True,
        ),
        event_sink=CapturingSink(),
        queue_backend=InMemoryQueueBackend(),
        body_persister=persister,
        browser_pool=browser,
        screenshot_kinds=["viewport_desktop", "full_page"],
        strict_persistence=True,
    )

    await crawler.run()

    assert set(browser.urls) == set(pages)
    assert {request.url for request in persister.requests} == set(pages)
    assert all(
        [shot.kind for shot in request.screenshots] == ["viewport_desktop", "full_page"]
        for request in persister.requests
    )
    assert persister.expected == 6
    assert persister.captured == 6


@pytest.mark.asyncio
async def test_missing_screenshot_kind_warns_and_retains_the_fetched_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def allow_test_url(url: str) -> None:
        return None

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    # Deterministic regardless of the host env: without a configured proxy
    # pool, get_required_random_proxy raises and the crawl emits an EXTRA
    # proxy-bypass warning, breaking the exact-one-warning assertion below.
    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy.test:8080")

    class IncompleteBrowserPool:
        async def fetch_with_capture(self, url: str, **kwargs: Any) -> FetchWithCaptureResult:
            kinds = (
                ["viewport_desktop"]
                if url.endswith("/broken")
                else ["viewport_desktop", "full_page"]
            )
            return FetchWithCaptureResult(
                content=_page_html(),
                response_url=url,
                status_code=200,
                headers={"content-type": "text/html"},
                title="Page",
                screenshots=[
                    CapturedScreenshot(kind=kind, width=1366, height=768, bytes=b"PNG")
                    for kind in kinds
                ],
            )

    sink = CapturingSink()
    persister = _RecordingPersister()
    crawler = SiteCrawler(
        run_id="missing-shot-regression",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=2,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            seed_urls=["https://x.test/broken", "https://x.test/healthy"],
            list_mode=True,
            render_mode=RENDER_BROWSER_WITH_SCREENSHOT,
            capture_screenshots=True,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        body_persister=persister,
        browser_pool=IncompleteBrowserPool(),
        screenshot_kinds=["viewport_desktop", "full_page"],
        strict_persistence=True,
    )

    await crawler.run()

    assert sink.of_type(CrawlPageFailedEvent) == []
    warnings = sink.of_type(CrawlWarningEvent)
    assert len(warnings) == 1
    assert "fetched page content was retained" in warnings[0].message
    assert warnings[0].context["missing"] == ["full_page"]
    completed = sink.of_type(CrawlCompletedEvent)
    assert len(completed) == 1
    assert completed[0].status == "completed"
    assert completed[0].pages_failed == 0
    assert completed[0].pages_fetched == 2
    assert [request.url for request in persister.requests] == [
        "https://x.test/broken",
        "https://x.test/healthy",
    ]
    assert [shot.kind for shot in persister.requests[0].screenshots] == ["viewport_desktop"]


@pytest.mark.asyncio
@pytest.mark.parametrize("proxy_status", [407, 520])
async def test_proxy_error_retries_browser_capture_directly(
    monkeypatch: pytest.MonkeyPatch,
    proxy_status: int,
) -> None:
    async def allow_test_url(url: str) -> None:
        return None

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr(
        "matrx_scraper.crawler.get_required_random_proxy",
        lambda: "http://rejected-proxy.test:8080",
    )

    class ProxyRejectingBrowserPool:
        def __init__(self) -> None:
            self.proxies: list[str | None] = []

        async def fetch_with_capture(self, url: str, **kwargs: Any) -> FetchWithCaptureResult:
            proxy = kwargs["proxy"]
            self.proxies.append(proxy)
            if proxy is not None:
                return FetchWithCaptureResult(
                    content="<html><body>Proxy request failed</body></html>",
                    response_url=url,
                    status_code=proxy_status,
                    headers={"content-type": "text/html"},
                    title="Proxy request failed",
                )
            kinds = kwargs["screenshot_kinds"]
            return FetchWithCaptureResult(
                content=_page_html(),
                response_url=url,
                status_code=200,
                headers={"content-type": "text/html"},
                title="Page",
                screenshots=[
                    CapturedScreenshot(kind=kind, width=1366, height=768, bytes=b"PNG")
                    for kind in kinds
                ],
            )

    sink = CapturingSink()
    persister = _RecordingPersister()
    browser = ProxyRejectingBrowserPool()
    crawler = SiteCrawler(
        run_id="proxy-auth-fallback",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=2,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            seed_urls=["https://x.test/first", "https://x.test/second"],
            list_mode=True,
            render_mode=RENDER_BROWSER_WITH_SCREENSHOT,
            capture_screenshots=True,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        body_persister=persister,
        browser_pool=browser,
        screenshot_kinds=["viewport_desktop"],
        strict_persistence=True,
    )

    await crawler.run()

    assert browser.proxies == ["http://rejected-proxy.test:8080", None, None]
    assert sink.of_type(CrawlPageFailedEvent) == []
    fetched = sink.of_type(CrawlPageFetchedEvent)
    assert len(fetched) == 2
    assert all(event.http_status == 200 for event in fetched)
    warnings = sink.of_type(CrawlWarningEvent)
    assert len(warnings) == 1
    assert warnings[0].context == {
        "url": "https://x.test/first",
        "proxy_status": proxy_status,
        "fallback": "direct",
        "proxy_circuit_open": True,
    }
    assert [request.url for request in persister.requests] == [
        "https://x.test/first",
        "https://x.test/second",
    ]


@pytest.mark.asyncio
async def test_kml_is_captured_as_xml_without_entering_the_html_browser_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.orchestrator import ScrapeResult

    async def allow_test_url(url: str) -> None:
        return None

    kml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
        "<name>Locations for Data Destruction Inc</name></Document></kml>"
    )
    proxy_attempts: list[bool] = []

    async def scrape_kml(url: str, **kwargs: Any) -> ScrapeResult:
        assert kwargs["request_type"].value == "normal"
        proxy_attempts.append(kwargs["use_proxy"])
        if kwargs["use_proxy"]:
            return ScrapeResult(
                url=url,
                response_url=url,
                success=False,
                content_type="html",
                content_type_raw="text/html",
                status_code=520,
                failure_reason="bad_status",
                raw_text="Proxy gateway failure",
            )
        return ScrapeResult(
            url=url,
            response_url=url,
            success=True,
            content_type="xml",
            content_type_raw="text/xml; charset=UTF-8",
            status_code=200,
            raw_body=kml,
            raw_text="Locations for Data Destruction Inc",
        )

    class BrowserMustNotRun:
        size = 1

        async def fetch_with_capture(self, url: str, **kwargs: Any) -> FetchWithCaptureResult:
            raise AssertionError(f"non-renderable KML entered browser capture: {url}")

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", scrape_kml)
    monkeypatch.setattr(
        "matrx_scraper.crawler.get_required_random_proxy",
        lambda: "http://intermittent-proxy.test:8080",
    )

    sink = CapturingSink()
    persister = _RecordingPersister()
    crawler = SiteCrawler(
        run_id="kml-regression",
        config=SiteCrawlerConfig(
            base_url="https://datadestruction.com/locations.kml",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            render_mode=RENDER_BROWSER_WITH_SCREENSHOT,
            capture_screenshots=True,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        body_persister=persister,
        browser_pool=BrowserMustNotRun(),
        screenshot_kinds=["viewport_desktop"],
        strict_persistence=True,
    )

    await crawler.run()

    assert not sink.of_type(CrawlPageFailedEvent)
    parsed = sink.of_type(CrawlPageParsedEvent)
    assert len(parsed) == 1
    assert parsed[0].page.mime_type == "xml"
    assert len(persister.requests) == 1
    assert persister.requests[0].body == kml
    assert persister.requests[0].mime_type == "text/xml; charset=UTF-8"
    assert proxy_attempts == [True, False]
    assert sink.of_type(CrawlWarningEvent)[0].context == {
        "url": "https://datadestruction.com/locations.kml",
        "proxy_status": 520,
        "fallback": "direct",
        "proxy_circuit_open": True,
    }
    completed = sink.of_type(CrawlCompletedEvent)
    assert len(completed) == 1
    assert completed[0].status == "completed"
    assert completed[0].pages_fetched == 1


@pytest.mark.asyncio
async def test_persistence_failure_isolated_to_page_and_crawl_continues(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.orchestrator import ScrapeResult

    async def allow_test_url(url: str) -> None:
        return None

    async def scrape_page(url: str, **kwargs: Any) -> ScrapeResult:
        return ScrapeResult(
            url=url,
            response_url=url,
            success=True,
            content_type="html",
            content_type_raw="text/html; charset=UTF-8",
            status_code=200,
            raw_html=_page_html(),
            raw_text="Useful crawl regression content",
        )

    class OneBadPagePersister:
        def __init__(self) -> None:
            self.urls: list[str] = []

        async def __call__(self, request: Any) -> PersistResult:
            self.urls.append(request.url)
            if request.url.endswith("/broken"):
                raise PermissionError("historical artifact is inaccessible")
            return PersistResult(page_id="page-ok", snapshot_id="snapshot-ok")

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", scrape_page)

    sink = CapturingSink()
    persister = OneBadPagePersister()
    crawler = SiteCrawler(
        run_id="persistence-page-isolation",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=2,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            seed_urls=["https://x.test/broken", "https://x.test/healthy"],
            list_mode=True,
            render_mode=RENDER_HTTP_ONLY,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        body_persister=persister,
        strict_persistence=True,
    )

    await crawler.run()

    assert persister.urls == ["https://x.test/broken", "https://x.test/healthy"]
    failed = sink.of_type(CrawlPageFailedEvent)
    assert len(failed) == 1
    assert failed[0].url == "https://x.test/broken"
    assert failed[0].error_class == "CrawlPersistenceError"
    warnings = sink.of_type(CrawlWarningEvent)
    assert warnings[0].context == {
        "url": "https://x.test/broken",
        "failure_scope": "page",
        "crawl_continued": True,
    }
    parsed = sink.of_type(CrawlPageParsedEvent)
    assert [event.page.url for event in parsed] == ["https://x.test/healthy"]
    completed = sink.of_type(CrawlCompletedEvent)
    assert len(completed) == 1
    assert completed[0].status == "completed"
    assert completed[0].pages_fetched == 1
    assert completed[0].pages_failed == 1
    assert completed[0].coverage_complete is False


@pytest.mark.asyncio
async def test_low_text_quality_signal_warns_but_page_is_persisted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.orchestrator import ScrapeResult

    async def allow_test_url(url: str) -> None:
        return None

    async def scrape_thin_page(url: str, **kwargs: Any) -> ScrapeResult:
        return ScrapeResult(
            url=url,
            response_url=url,
            success=True,
            content_type="html",
            content_type_raw="text/html; charset=UTF-8",
            status_code=200,
            raw_html="<html><head><title>Learn</title></head><body>Learn</body></html>",
            raw_text="Learn",
            failure_details=[{"low_text_content": "Text length 5"}],
        )

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", scrape_thin_page)

    sink = CapturingSink()
    persister = _RecordingPersister()
    crawler = SiteCrawler(
        run_id="low-text-quality-signal",
        config=SiteCrawlerConfig(
            base_url="https://x.test/learn",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            render_mode=RENDER_HTTP_ONLY,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        body_persister=persister,
        strict_persistence=True,
    )

    await crawler.run()

    assert sink.of_type(CrawlPageFailedEvent) == []
    warnings = sink.of_type(CrawlWarningEvent)
    assert len(warnings) == 1
    assert warnings[0].context["signal"] == "low_text_content"
    assert warnings[0].context["crawl_continued"] is True
    assert [request.url for request in persister.requests] == ["https://x.test/learn"]
    completed = sink.of_type(CrawlCompletedEvent)[0]
    assert completed.pages_fetched == 1
    assert completed.pages_failed == 0


@pytest.mark.asyncio
async def test_http_fetch_keeps_low_text_as_nonfatal_quality_detail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import matrx_scraper.scraper as scraper_module

    monkeypatch.setattr(scraper_module, "CURL_CFFI_AVAILABLE", True)
    monkeypatch.setattr(
        scraper_module,
        "_curl_cffi_get_sync",
        lambda *args, **kwargs: {
            "status_code": 200,
            "headers": {"content-type": "text/html; charset=UTF-8"},
            "response_url": "https://x.test/learn/",
            "redirect_chain": [],
            "content_type_raw": "text/html; charset=UTF-8",
            "content": (
                "<html><head><title>Learn</title></head>"
                "<body><header>Menu</header><main>Learn</main></body></html>"
            ),
            "content_bytes": None,
        },
    )

    response = await scraper_module.fetch(
        "https://x.test/learn",
        use_curl_cffi=True,
        header_profile={"headers": {}, "impersonate": "chrome131"},
    )

    assert response.status_code == 200
    assert response.failed is False
    assert response.failed_primary_reason is None
    assert any(
        scraper_module.FailureReason.LOW_TEXT_CONTENT in detail
        for detail in response.failed_reasons
    )


# ---------------------------------------------------------------------------
# Integration — small live crawl of raymarcleaners.com
# ---------------------------------------------------------------------------


TEST_SITE = "https://raymarcleaners.com/"


@pytest.mark.network
@pytest.mark.asyncio
async def test_live_small_site_crawl() -> None:
    """Crawl raymarcleaners.com (~10 pages) and verify the full pipeline.

    Asserts:
      * crawl_started + crawl_completed each fire exactly once
      * status is 'completed' (not 'failed' / 'canceled')
      * at least one page successfully parsed
      * BFS stays on raymarcleaners.com (no external pages fetched)
      * no silent failure: any errors come through CrawlPageFailedEvent
    """
    cfg = SiteCrawlerConfig(
        base_url=TEST_SITE,
        max_pages=15,
        concurrency=4,
        respect_robots=True,
        seed_from_sitemap=True,
        render_mode=RENDER_HTTP_ONLY,
        user_agent="MatrxScraperBot/test (+https://aimatrx.com)",
        follow_subdomains=False,
    )
    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="raymar-test",
        config=cfg,
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
    )
    await asyncio.wait_for(crawler.run(), timeout=180.0)

    started = sink.of_type(CrawlStartedEvent)
    completed = sink.of_type(CrawlCompletedEvent)
    fetched = sink.of_type(CrawlPageFetchedEvent)
    parsed = sink.of_type(CrawlPageParsedEvent)
    discovered = sink.of_type(CrawlPageDiscoveredEvent)
    failed = sink.of_type(CrawlPageFailedEvent)

    assert len(started) == 1, "crawl_started should fire exactly once"
    assert len(completed) == 1, "crawl_completed should fire exactly once"
    assert completed[0].status == "completed", (
        f"expected completed status, got {completed[0].status!r} — failures: "
        f"{[(e.url, e.error_class, e.error_message) for e in failed]}"
    )
    assert len(parsed) >= 1, "at least one page should have been parsed"
    assert len(discovered) >= 1
    # Boundary check — no external domain leakage
    for ev in fetched:
        assert "raymarcleaners.com" in ev.url, f"crawler crossed boundary: {ev.url}"


@pytest.mark.network
@pytest.mark.asyncio
async def test_live_small_site_does_not_silently_swallow_errors() -> None:
    """Any failures during the crawl must show up as CrawlPageFailedEvent.

    With the legacy `except Exception: pass` the crawler would swallow errors;
    the new code never does. We don't assert that a failure happens (the site
    might be perfectly reachable) — only that anything that DOES go wrong is
    surfaced through the typed event vocabulary.
    """
    cfg = SiteCrawlerConfig(
        base_url=TEST_SITE,
        max_pages=10,
        concurrency=4,
        respect_robots=True,
        render_mode=RENDER_HTTP_ONLY,
    )
    sink = CapturingSink()
    crawler = SiteCrawler(run_id="raymar-error-test", config=cfg, event_sink=sink)
    await asyncio.wait_for(crawler.run(), timeout=180.0)

    completed = sink.of_type(CrawlCompletedEvent)
    failed = sink.of_type(CrawlPageFailedEvent)

    # crawl_completed fires regardless of partial failures
    assert len(completed) == 1
    # If any pages failed, the count in the completion event must equal the
    # number of failure events emitted — proves no silent swallowing.
    assert completed[0].pages_failed == len(failed)


# ---------------------------------------------------------------------------
# Host scope: www/apex equivalence (unconditional) vs subdomains (gated)
# ---------------------------------------------------------------------------


def test_www_and_apex_are_the_same_site_bidirectionally() -> None:
    from matrx_scraper.crawler import _is_same_host

    # Site registered as apex; sitemap serves www URLs (the production
    # "hundreds of URLs go by, only 4 fetched" bug).
    assert _is_same_host("https://www.acme.example/page", "acme.example", False)
    # Site registered as www; apex URLs are equally in scope.
    assert _is_same_host("https://acme.example/page", "www.acme.example", False)
    # Identical hosts still trivially match.
    assert _is_same_host("https://acme.example/", "acme.example", False)
    assert _is_same_host("https://www.acme.example/", "www.acme.example", False)


def test_other_subdomains_still_honor_follow_subdomains() -> None:
    from matrx_scraper.crawler import _is_same_host

    assert not _is_same_host("https://blog.acme.example/", "acme.example", False)
    assert _is_same_host("https://blog.acme.example/", "acme.example", True)
    assert not _is_same_host("https://blog.acme.example/", "www.acme.example", False)
    assert _is_same_host("https://blog.acme.example/", "www.acme.example", True)
    # A lookalike prefix is NOT www-equivalent.
    assert not _is_same_host("https://wwwx.acme.example/", "acme.example", False)
    # A different registrable domain never matches.
    assert not _is_same_host("https://www.other.example/", "acme.example", True)


# ---------------------------------------------------------------------------
# Registrable domain — real Public Suffix List, offline snapshot
# ---------------------------------------------------------------------------


def test_registrable_domain_respects_multi_label_public_suffixes() -> None:
    from matrx_scraper.crawler import _registrable_domain

    # co.uk / com.au are public suffixes — two different .co.uk sites must
    # NEVER share a registrable domain (the old last-two-labels heuristic
    # returned "co.uk" for both).
    assert _registrable_domain("example.co.uk") == "example.co.uk"
    assert _registrable_domain("evil.co.uk") == "evil.co.uk"
    assert _registrable_domain("example.co.uk") != _registrable_domain("evil.co.uk")
    assert _registrable_domain("shop.example.com.au") == "example.com.au"
    # github.io is a private-registry public suffix: every project site is
    # its own registrable domain.
    assert _registrable_domain("alice.github.io") == "alice.github.io"
    assert _registrable_domain("bob.github.io") == "bob.github.io"
    assert _registrable_domain("alice.github.io") != _registrable_domain("bob.github.io")


def test_registrable_domain_subdomains_of_same_site_still_match() -> None:
    from matrx_scraper.crawler import _registrable_domain

    assert _registrable_domain("blog.example.co.uk") == "example.co.uk"
    assert _registrable_domain("www.example.com") == "example.com"
    assert _registrable_domain("example.com") == "example.com"
    assert _registrable_domain("deep.nested.sub.example.com") == "example.com"


def test_registrable_domain_handles_non_psl_hosts() -> None:
    from matrx_scraper.crawler import _registrable_domain

    # Test/internal TLDs keep the last-two-labels fallback so subdomain
    # matching still works for them.
    assert _registrable_domain("blog.acme.example") == "acme.example"
    assert _registrable_domain("localhost") == "localhost"
    # IP literals are their own identity, never sliced by labels.
    assert _registrable_domain("127.0.0.1") == "127.0.0.1"


def test_same_host_public_suffix_never_bridges_two_sites() -> None:
    from matrx_scraper.crawler import _is_same_host

    # Even with follow_subdomains, a different co.uk registrant is external.
    assert not _is_same_host("https://evil.co.uk/", "example.co.uk", True)
    assert not _is_same_host("https://bob.github.io/", "alice.github.io", True)
    # True subdomains of the same registrant still match.
    assert _is_same_host("https://blog.example.co.uk/", "example.co.uk", True)


# ---------------------------------------------------------------------------
# Include/exclude pattern compilation — defensive skip must be loud
# ---------------------------------------------------------------------------


def test_compile_patterns_reports_invalid_patterns() -> None:
    from matrx_scraper.crawler import _compile_patterns

    compiled, invalid = _compile_patterns([r"^/blog/", r"[unclosed", r"\d+"])
    assert [p.pattern for p in compiled] == [r"^/blog/", r"\d+"]
    assert len(invalid) == 1
    assert invalid[0]["pattern"] == "[unclosed"
    assert invalid[0]["error"]


@pytest.mark.asyncio
async def test_invalid_pattern_emits_durable_crawl_warning() -> None:
    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="run-patterns",
        config=SiteCrawlerConfig(
            base_url="https://acme.example/",
            max_pages=1,
            list_mode=True,
            seed_urls=[],
            include_patterns=["[unclosed"],
            render_mode=RENDER_HTTP_ONLY,
        ),
        event_sink=sink,
    )
    assert crawler._invalid_patterns and crawler._invalid_patterns[0]["kind"] == "include"
    await crawler.run()
    warnings = sink.of_type(CrawlWarningEvent)
    assert any("WIDER than requested" in w.message and "[unclosed" in w.message for w in warnings)


# ---------------------------------------------------------------------------
# Regression — crawl throughput invariants
#
# Both tests below pin bugs that made a real 5,000-page crawl fetch 15 pages in
# 10 minutes. Neither failure is visible in output correctness — the crawl still
# produces the right rows, just orders of magnitude too slowly — so only a test
# that counts EVENTS can catch a regression.
# ---------------------------------------------------------------------------


def _crawler_for_invariants(sink: CapturingSink, **overrides: Any) -> SiteCrawler:
    config = SiteCrawlerConfig(
        base_url="https://x.test/",
        render_mode=RENDER_HTTP_ONLY,
        progress_every_n_pages=5,
        progress_every_seconds=3600.0,  # isolate the count gate from the timer
        **overrides,
    )
    return SiteCrawler(
        run_id="run-invariants",
        config=config,
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
    )


@pytest.mark.asyncio
async def test_navigation_discovery_does_not_promote_oembed_resources_to_pages() -> None:
    from matrx_scraper.orchestrator import ScrapeResult

    sink = CapturingSink()
    crawler = _crawler_for_invariants(sink)
    page_url = "https://x.test/post"
    real_page = "https://x.test/about"
    oembed_resource = "https://x.test/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fx.test%2Fpost"
    result = ScrapeResult(
        url=page_url,
        response_url=page_url,
        success=True,
        content_type="html",
        status_code=200,
        raw_html=(
            "<html><head>"
            f'<link rel="alternate" type="application/json+oembed" href="{oembed_resource}">'
            "</head><body>"
            f'<a href="{real_page}">About</a>'
            "</body></html>"
        ),
    )
    item = QueueItem(page_url, 0, None, "seed")
    summary = crawler._build_summary(result, item, 10, 100, None)

    assert [link.target_url for link in summary.links] == [real_page]
    await crawler._enqueue_links(summary, item)

    assert await crawler.queue.is_known(real_page)
    assert not await crawler.queue.is_known(oembed_resource)
    decisions = sink.of_type(CrawlUrlsClassifiedEvent)
    assert len(decisions) == 1
    assert decisions[0].accepted == 1


@pytest.mark.asyncio
async def test_progress_does_not_re_emit_while_page_count_is_unchanged() -> None:
    """A stalled fetch count must not emit progress on every poll.

    The run loop calls `_maybe_emit_progress` every 100ms. A `pages_fetched % N
    == 0` gate is a LEVEL test, so a count that merely sits on a multiple of N
    re-fires forever (~10 events/sec), flooding the event sink's ordering lock
    and starving the crawl. The gate must be an EDGE test.
    """
    sink = CapturingSink()
    crawler = _crawler_for_invariants(sink)
    crawler._started_at = 0.0

    crawler._pages_fetched = 5
    await crawler._maybe_emit_progress()
    assert len(sink.of_type(CrawlProgressEvent)) == 1, "first crossing must emit"

    # The count sits on a multiple of 5 across many polls — as it does whenever
    # a slow page is in flight. Not one further event may be emitted.
    for _ in range(50):
        await crawler._maybe_emit_progress()
    assert len(sink.of_type(CrawlProgressEvent)) == 1, (
        "progress re-emitted while pages_fetched was unchanged — the modulo level-test regressed"
    )

    crawler._pages_fetched = 10
    await crawler._maybe_emit_progress()
    assert len(sink.of_type(CrawlProgressEvent)) == 2, "advancing by N must emit"


@pytest.mark.asyncio
async def test_one_page_emits_one_classification_event_for_any_link_count() -> None:
    """Per-page event count is O(1), never O(links).

    Every event costs a full DB transaction under a global ordering lock, so an
    event per discovered link makes crawl throughput a function of link count.
    A page with 400 links must cost exactly the same number of events as a page
    with 4.
    """
    sink = CapturingSink()
    crawler = _crawler_for_invariants(sink, follow_subdomains=False)

    links = [f"https://x.test/page-{i}" for i in range(400)]
    links += [f"https://other.test/off-{i}" for i in range(100)]  # out of scope
    links += ["mailto:someone@x.test", "javascript:void(0)"]  # unparseable scheme

    accepted = await crawler._classify_and_enqueue_batch(
        links, depth=1, parent_url="https://x.test/", source="link"
    )

    batched = sink.of_type(CrawlUrlsClassifiedEvent)
    assert len(batched) == 1, f"expected exactly 1 batched event, got {len(batched)}"
    assert not sink.of_type(CrawlUrlClassifiedEvent), (
        "per-link url_classified events regressed — this is the O(links) storm"
    )

    event = batched[0]
    assert accepted == 400
    assert event.accepted == 400
    assert event.total == 502, "every decision must reach the durable ledger"
    assert event.by_reason["outside_site_scope"] == 100
    assert event.by_reason["unsupported_scheme"] == 2
    assert len(event.decisions) == 502

    # The wire copy carries the counts but not the ledger payload.
    assert event.for_wire().decisions == []
    assert event.for_wire().total == 502


@pytest.mark.asyncio
async def test_batch_enqueue_counts_each_url_once() -> None:
    """Duplicate links on one page must not inflate pages_discovered."""
    sink = CapturingSink()
    crawler = _crawler_for_invariants(sink)

    accepted = await crawler._classify_and_enqueue_batch(
        ["https://x.test/same"] * 25, depth=1, parent_url="https://x.test/", source="link"
    )
    assert accepted == 1
    assert crawler._pages_discovered == 1

    # A second page linking the same URL discovers nothing new.
    again = await crawler._classify_and_enqueue_batch(
        ["https://x.test/same"], depth=1, parent_url="https://x.test/other", source="link"
    )
    assert again == 0
    assert crawler._pages_discovered == 1


# The legal `web.crawl_url.outcome` values (constraint crawl_url_outcome_valid,
# verified live 2026-07-23). `accepted` is deliberately NOT here: an accepted
# URL's ledger row is written later at fetch time with its terminal outcome, so
# accepted decisions must be filtered out of classification-time persistence.
# A CheckViolationError from this exact gap stopped a live crawl.
_LEGAL_CRAWL_URL_OUTCOMES = frozenset(
    {
        "discovered",
        "captured",
        "redirected",
        "skipped",
        "excluded",
        "failed",
        "duplicate",
        "cancelled",
    }
)


@pytest.mark.asyncio
async def test_persistable_decision_outcomes_are_all_db_legal() -> None:
    """Every decision that reaches the ledger must carry a DB-legal outcome.

    Only `accepted` may be non-legal, and only because it is filtered out before
    persistence (its row is written later as `captured`). Any other non-legal
    outcome is a live CheckViolationError waiting to happen.
    """
    sink = CapturingSink()
    crawler = _crawler_for_invariants(sink, follow_subdomains=False)

    # Pre-seed one URL so the second appearance classifies as a duplicate.
    await crawler.queue.enqueue(QueueItem("https://x.test/known", 0, None, "seed"))

    links = [
        "https://x.test/fresh",  # accepted
        "https://x.test/known",  # duplicate (already queued)
        "https://other.test/off",  # excluded — outside scope
        "mailto:x@x.test",  # skipped — unsupported scheme
    ]
    await crawler._classify_and_enqueue_batch(
        links, depth=1, parent_url="https://x.test/", source="link"
    )
    event = sink.of_type(CrawlUrlsClassifiedEvent)[0]

    outcomes = {d.outcome for d in event.decisions}
    assert "accepted" in outcomes, "the accepted URL must still appear in the event for counts"
    persistable = {d.outcome for d in event.decisions if d.outcome != "accepted"}
    illegal = persistable - _LEGAL_CRAWL_URL_OUTCOMES
    assert not illegal, f"crawler emits DB-illegal ledger outcome(s): {illegal}"
    # And the specific values we expect from this batch.
    assert persistable == {"duplicate", "excluded", "skipped"}


# ---------------------------------------------------------------------------
# Regression — HTTP 429 (rate limit) handling
#
# A 429 is the origin saying "slow down", not "this page is broken". Treating
# it as a permanent failure meant the instant a crawl tripped a host's rate
# limit, every remaining URL failed too. The throughput fix EXPOSED this: a
# fast crawl trips the limit immediately where a slow one never did.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_in_memory_requeues_on_will_retry() -> None:
    """mark_failed(will_retry=True) must put the URL back on the queue.

    The old set-based backend silently dropped it, so retries never happened.
    """
    q = InMemoryQueueBackend()
    await q.enqueue(QueueItem("https://x.test/a", 2, "https://x.test/", "link"))
    item = await q.dequeue()
    assert item is not None
    assert await q.queue_depth() == 0

    await q.mark_failed(item.url, "http_429", will_retry=True)
    assert await q.queue_depth() == 1, "will_retry must requeue"
    assert await q.in_flight_count() == 0

    requeued = await q.dequeue()
    assert requeued is not None
    # The ORIGINAL item comes back — depth/parent preserved, not a fresh crawl.
    assert requeued.depth == 2
    assert requeued.parent_url == "https://x.test/"

    # A terminal failure (will_retry=False) does NOT requeue.
    await q.mark_failed(requeued.url, "gone", will_retry=False)
    assert await q.queue_depth() == 0


def test_throttle_host_compounds_and_floors() -> None:
    from matrx_scraper.rate_limiter import HostRateLimiter

    rl = HostRateLimiter(default_rps=4.0, default_burst=8.0)
    rps1, _ = rl.throttle_host("https://iopbm.com/a", factor=0.5, min_rps=0.5)
    assert rps1 == 2.0
    rps2, _ = rl.throttle_host("https://iopbm.com/b", factor=0.5, min_rps=0.5)
    assert rps2 == 1.0  # compounds per 429 on the same host
    # Floors — never throttles to zero (which would stall the host forever).
    for _ in range(10):
        rpsn, _ = rl.throttle_host("https://iopbm.com/c", factor=0.5, min_rps=0.5)
    assert rpsn == 0.5


@pytest.mark.asyncio
async def test_rate_limited_page_throttles_requeues_then_fails_after_cap() -> None:
    """A persistently-429 URL: warn+requeue up to the cap, then ONE terminal fail.

    It must never emit a page_fetched (a throttled response fetched nothing) and
    must not inflate the failed counter until retries are actually exhausted.
    """
    from matrx_scraper.crawler import MAX_RATE_LIMIT_RETRIES
    from matrx_scraper.host_pacing import PacingKnobs
    from matrx_scraper.events import CrawlWarningEvent
    from matrx_scraper.orchestrator import ScrapeResult

    sink = CapturingSink()
    queue = InMemoryQueueBackend()
    crawler = SiteCrawler(
        run_id="rl-test",
        config=SiteCrawlerConfig(
            base_url="https://iopbm.com/",
            render_mode=RENDER_HTTP_ONLY,
            seed_from_sitemap=False,
            host_rps=200.0,
        ),
        event_sink=sink,
        queue_backend=queue,
        # This test is ABOUT rate-limit behaviour, so it opts out of the
        # suite-wide fast-knob fixture and runs the real ramp. Values are
        # the shipped defaults except for a rate high enough that the token
        # bucket never makes the test wait.
        pacing_knobs=PacingKnobs(floor_rps=100.0, max_rps=100.0, min_rps=25.0),
    )

    async def always_429(url: str, **kwargs: Any) -> ScrapeResult:
        return ScrapeResult(
            success=False,
            url=url,
            response_url=url,
            content_type="text/html",
            status_code=429,
            failure_reason="bad_status",
        )

    import matrx_scraper.crawler as crawler_module

    crawler_module.scrape = always_429  # type: ignore[assignment]

    # Drive one URL through _process MAX+1 times (simulating the requeue loop).
    for _ in range(MAX_RATE_LIMIT_RETRIES + 1):
        await queue.enqueue(QueueItem("https://iopbm.com/p", 0, None, "seed"))
        item = await queue.dequeue()
        assert item is not None
        await crawler._process(item)

    # No page was ever "fetched".
    assert not sink.of_type(CrawlPageFetchedEvent), "a 429 is not a fetch"
    # Exactly MAX warnings (one per throttled retry) then exactly one terminal fail.
    assert len(sink.of_type(CrawlWarningEvent)) == MAX_RATE_LIMIT_RETRIES
    failures = sink.of_type(CrawlPageFailedEvent)
    assert len(failures) == 1
    assert failures[0].error_class == "RateLimited"
    assert crawler._pages_failed == 1  # only the terminal failure counts

    # The host was actually slowed. Since 2026-08-20 the CRAWL's own rate is
    # owned by the per-host ramp (which also records the rate that provoked the
    # limit as a ceiling it will not climb back into), while the process-wide
    # throttle factor is what teaches the OTHER lanes. Both must fire.
    from matrx_scraper.rate_limiter import host_key, shared_throttles

    host = host_key("https://iopbm.com/p")
    assert crawler._rate_limiter._overrides[host][0] < 100.0
    ramp = crawler._ramps[host]
    assert ramp.discovered_limit_rps is not None
    assert ramp.current_rps < 100.0
    assert shared_throttles().get(host, 1.0) < 1.0, (
        "a 429 the crawler learned must still slow the research/SEO lanes"
    )


# ---------------------------------------------------------------------------
# http_first browser escalation on blocked/failed HTTP fetches
# ---------------------------------------------------------------------------
#
# The non-screenshot path fetches over plain HTTP. Bot-protected hosts
# (Cloudflare/WAF/TLS-fingerprint checks) reject that client while happily
# serving a real browser — the screenshot path, being browser-driven, crawled
# the same sites fine, which is exactly the asymmetry reported in production
# ("screenshots on works, screenshots off struggles"). http_first must
# escalate a blocked/transport-failed HTTP fetch to the browser, not only a
# thin-but-successful one.


@pytest.mark.asyncio
async def test_http_first_escalates_blocked_fetch_to_browser(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.orchestrator import ScrapeResult
    from matrx_scraper.scraper import RequestType

    sink = CapturingSink()
    queue = InMemoryQueueBackend()
    crawler = SiteCrawler(
        run_id="fallback-test",
        config=SiteCrawlerConfig(
            base_url="https://iopbm.com/",
            seed_from_sitemap=False,
            respect_robots=False,
        ),
        event_sink=sink,
        queue_backend=queue,
        browser_pool=object(),  # presence gates the fallback; fake scrape below
    )

    calls: list[str] = []

    async def blocked_then_browser_ok(url: str, **kwargs: Any) -> ScrapeResult:
        request_type = kwargs.get("request_type")
        calls.append(str(request_type))
        if request_type == RequestType.BROWSER:
            return ScrapeResult(
                success=True,
                url=url,
                response_url=url,
                content_type="html",
                status_code=200,
                raw_html=(
                    "<html><head><title>Rendered</title></head>"
                    "<body><main><h1>Rendered</h1><p>real content</p></main></body></html>"
                ),
            )
        return ScrapeResult(
            success=False,
            url=url,
            response_url=url,
            content_type="html",
            status_code=403,
            failure_reason="cloudflare_block",
            failure_details=[{"cloudflare_block": "Title indicates block: Just a moment..."}],
        )

    import matrx_scraper.crawler as crawler_module

    monkeypatch.setattr(crawler_module, "scrape", blocked_then_browser_ok)

    await queue.enqueue(QueueItem("https://iopbm.com/blocked-page", 0, None, "seed"))
    item = await queue.dequeue()
    assert item is not None
    await crawler._process(item)

    assert calls == [str(RequestType.NORMAL), str(RequestType.BROWSER)]
    warnings = sink.of_type(CrawlWarningEvent)
    assert any((w.context or {}).get("fallback") == "browser" for w in warnings), (
        "the escalation must be loud — a silent recovery hides the block from the log"
    )
    fetched = sink.of_type(CrawlPageFetchedEvent)
    assert len(fetched) == 1 and fetched[0].http_status == 200
    assert not sink.of_type(CrawlPageFailedEvent)
    assert crawler._pages_fetched == 1
    assert crawler._pages_failed == 0


@pytest.mark.asyncio
async def test_http_first_does_not_browser_retry_a_plain_404(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A real 404 fails identically in a browser — re-rendering every dead
    link would double the cost of a crawl with a broken link graph."""
    from matrx_scraper.orchestrator import ScrapeResult
    from matrx_scraper.scraper import RequestType

    sink = CapturingSink()
    queue = InMemoryQueueBackend()
    crawler = SiteCrawler(
        run_id="no-fallback-404",
        config=SiteCrawlerConfig(
            base_url="https://iopbm.com/",
            seed_from_sitemap=False,
            respect_robots=False,
        ),
        event_sink=sink,
        queue_backend=queue,
        browser_pool=object(),
    )

    async def always_404(url: str, **kwargs: Any) -> ScrapeResult:
        if kwargs.get("request_type") == RequestType.BROWSER:
            raise AssertionError("a plain 404 must not enter the browser")
        return ScrapeResult(
            success=False,
            url=url,
            response_url=url,
            content_type="html",
            status_code=404,
            failure_reason="bad_status",
            failure_details=[{"bad_status": "Status code 404"}],
        )

    import matrx_scraper.crawler as crawler_module

    monkeypatch.setattr(crawler_module, "scrape", always_404)

    await queue.enqueue(QueueItem("https://iopbm.com/gone", 0, None, "seed"))
    item = await queue.dequeue()
    assert item is not None
    await crawler._process(item)

    failures = sink.of_type(CrawlPageFailedEvent)
    assert len(failures) == 1
    # The terminal failure carries the diagnosable detail, not just the label.
    assert "Status code 404" in failures[0].error_message


@pytest.mark.asyncio
async def test_http_first_keeps_original_failure_when_browser_also_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.orchestrator import ScrapeResult
    from matrx_scraper.scraper import RequestType

    sink = CapturingSink()
    queue = InMemoryQueueBackend()
    crawler = SiteCrawler(
        run_id="fallback-both-fail",
        config=SiteCrawlerConfig(
            base_url="https://iopbm.com/",
            seed_from_sitemap=False,
            respect_robots=False,
        ),
        event_sink=sink,
        queue_backend=queue,
        browser_pool=object(),
    )

    async def both_fail(url: str, **kwargs: Any) -> ScrapeResult:
        if kwargs.get("request_type") == RequestType.BROWSER:
            return ScrapeResult(
                success=False,
                url=url,
                response_url=url,
                content_type="html",
                status_code=0,
                failure_reason="request_error",
                failure_details=[{"request_error": "browser timeout"}],
            )
        return ScrapeResult(
            success=False,
            url=url,
            response_url=url,
            content_type="html",
            status_code=0,
            failure_reason="request_error",
            failure_details=[{"request_error": "connection reset by peer"}],
        )

    import matrx_scraper.crawler as crawler_module

    monkeypatch.setattr(crawler_module, "scrape", both_fail)

    await queue.enqueue(QueueItem("https://iopbm.com/unreachable", 0, None, "seed"))
    item = await queue.dequeue()
    assert item is not None
    await crawler._process(item)

    failures = sink.of_type(CrawlPageFailedEvent)
    assert len(failures) == 1
    # The ORIGINAL transport diagnosis survives — the browser's own failure
    # must not overwrite what actually happened on the wire.
    assert "connection reset by peer" in failures[0].error_message
    assert crawler._pages_failed == 1
