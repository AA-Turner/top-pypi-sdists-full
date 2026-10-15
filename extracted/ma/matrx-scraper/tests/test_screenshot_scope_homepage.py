"""A brand crawl screenshots the HOMEPAGE (plus an explicit list), never every page.

Arman, 2026-10-14: a browser render with desktop and mobile screenshots on
EVERY page held Ritual Coffee's crawl at ~2 pages a minute. Under
`screenshot_scope="homepage"` only the site root and `screenshot_urls` go
through the browser capture; every other page takes the plain HTTP path.

The control (`scope="all"`) runs the SAME crawl and must capture every page —
so this test fails if the scope knob is ignored, not merely if it is absent.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_scraper.browser_pool import CapturedScreenshot, FetchWithCaptureResult
from matrx_scraper.crawler import RENDER_HTTP_FIRST, SiteCrawler, SiteCrawlerConfig
from matrx_scraper.events import CrawlCompletedEvent, CrawlPageFailedEvent
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.queue_backend import InMemoryQueueBackend
from matrx_scraper.web_crawl.contracts import CrawlStartRequest

from test_crawler import CapturingSink, _page_html, _RecordingPersister

HOME = "https://x.test/"
LISTED = "https://x.test/team"
PAGES = [HOME, "https://x.test/about", "https://x.test/contact", LISTED, "https://x.test/shop"]


async def _crawl(monkeypatch: pytest.MonkeyPatch, *, scope: str) -> tuple[list[str], list[str], CapturingSink]:
    async def allow(url: str) -> None:
        return None

    http_urls: list[str] = []

    async def scrape(url: str, **kwargs: Any) -> ScrapeResult:
        assert kwargs["request_type"].value == "normal", f"{url} asked the HTTP path for a browser"
        http_urls.append(url)
        html = _page_html()
        return ScrapeResult(
            url=url,
            response_url=url,
            success=True,
            content_type="html",
            content_type_raw="text/html",
            status_code=200,
            raw_body=html,
            raw_text=" ".join(["Useful crawl regression content"] * 80),
        )

    class BrowserPool:
        size = 5

        def __init__(self) -> None:
            self.urls: list[str] = []

        async def fetch_with_capture(self, url: str, **kwargs: Any) -> FetchWithCaptureResult:
            self.urls.append(url)
            return FetchWithCaptureResult(
                content=_page_html(),
                response_url=url,
                status_code=200,
                headers={"content-type": "text/html"},
                title="Page",
                screenshots=[
                    CapturedScreenshot(kind=k, width=1366, height=768, bytes=b"PNG")
                    for k in kwargs["screenshot_kinds"]
                ],
            )

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", scrape)
    monkeypatch.setattr("matrx_scraper.crawler.get_required_random_proxy", lambda: "http://p.test:1")

    browser = BrowserPool()
    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id=f"screenshot-scope-{scope}",
        config=SiteCrawlerConfig(
            base_url=HOME,
            max_pages=len(PAGES),
            concurrency=3,
            respect_robots=False,
            seed_from_sitemap=False,
            render_mode=RENDER_HTTP_FIRST,
            capture_screenshots=True,
            screenshot_scope=scope,
            screenshot_urls=[LISTED],
            seed_urls=PAGES,
            list_mode=True,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        body_persister=_RecordingPersister(),
        browser_pool=browser,
        screenshot_kinds=["desktop_full", "mobile_full"],
        strict_persistence=True,
    )
    await crawler.run()
    return browser.urls, http_urls, sink


@pytest.mark.asyncio
async def test_homepage_scope_screenshots_only_the_homepage_and_listed_pages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    shot_urls, http_urls, sink = await _crawl(monkeypatch, scope="homepage")

    assert sorted(shot_urls) == sorted([HOME, LISTED])
    assert sorted(http_urls) == sorted(set(PAGES) - {HOME, LISTED})
    assert not sink.of_type(CrawlPageFailedEvent)
    completed = sink.of_type(CrawlCompletedEvent)
    assert completed and completed[0].pages_fetched == len(PAGES)


@pytest.mark.asyncio
async def test_control_all_scope_screenshots_every_page(monkeypatch: pytest.MonkeyPatch) -> None:
    shot_urls, http_urls, _ = await _crawl(monkeypatch, scope="all")

    assert sorted(shot_urls) == sorted(PAGES)
    assert http_urls == []


def test_request_contract_carries_the_scope_knob() -> None:
    request = CrawlStartRequest(screenshot_scope="homepage", screenshot_urls=[LISTED])
    assert request.model_dump()["screenshot_scope"] == "homepage"
    assert CrawlStartRequest().screenshot_scope == "all"
    with pytest.raises(ValueError):
        CrawlStartRequest(screenshot_scope="every_other_page")
