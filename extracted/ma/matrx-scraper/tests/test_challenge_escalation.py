"""A bot-protection challenge must reach the browser, whatever status it wears.

The bug this pins (FOUND_DEFECTS 2026-07-30): a Cloudflare interstitial served as
HTTP 503 was classified `bad_status` (the status check appends before the
challenge selectors) AND swallowed by the rate-limit requeue (503 ∈
RATE_LIMIT_STATUSES), so the browser escalation — the one fetch that recovers a
challenge — never ran. It was requeued 5× on the same HTTP client and hard-failed
as "RateLimited".

Two independent layers, each asserted here and each sufficient alone:
  1. Classification — a challenge signature outranks `bad_status` as the primary
     reason, so the escalation's own trigger sees it.
  2. Escalation — the crawler keys on ALL reasons, a challenge beats the
     rate-limit exclusion, and an exhausted rate limit still spends ONE browser
     navigation before failing the page (catches challenges whose signature we
     do not recognize yet).
"""

from __future__ import annotations

from typing import Any

import pytest

import matrx_scraper.scraper as scraper_module
from matrx_scraper.crawler import (
    RENDER_BROWSER_WITH_SCREENSHOT,
    RENDER_HTTP_FIRST,
    SiteCrawler,
    SiteCrawlerConfig,
)
from matrx_scraper.events import (
    CrawlPageFailedEvent,
    CrawlPageFetchedEvent,
)
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.queue_backend import InMemoryQueueBackend
from matrx_scraper.scraper import FailureReason, RequestType

from test_crawler import CapturingSink, _page_html


CHALLENGE_HTML = (
    "<html><head><title>Just a moment...</title></head>"
    '<body><div id="turnstile-wrapper">'
    '<iframe src="https://challenges.cloudflare.com/turnstile/v0/x"></iframe>'
    "</div></body></html>"
)


# ---------------------------------------------------------------------------
# Layer 1 — classification
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [403, 429, 503])
async def test_cloudflare_challenge_outranks_bad_status_at_any_status(
    monkeypatch: pytest.MonkeyPatch, status: int
) -> None:
    monkeypatch.setattr(scraper_module, "CURL_CFFI_AVAILABLE", True)
    monkeypatch.setattr(
        scraper_module,
        "_curl_cffi_get_sync",
        lambda *args, **kwargs: {
            "status_code": status,
            "headers": {"content-type": "text/html", "cf-ray": "abc123"},
            "response_url": "https://x.test/blocked",
            "redirect_chain": [],
            "content_type_raw": "text/html",
            "content": CHALLENGE_HTML,
            "content_bytes": None,
        },
    )

    response = await scraper_module.fetch(
        "https://x.test/blocked",
        use_curl_cffi=True,
        header_profile={"headers": {}, "impersonate": "chrome131"},
    )

    assert response.failed is True
    # The specific diagnosis wins the primary slot — NOT `bad_status`, which was
    # appended first and used to mask every challenge served with a status.
    assert response.failed_primary_reason == FailureReason.CLOUDFLARE_BLOCK
    # …and the status is still recorded, just not as the headline.
    assert any(FailureReason.BAD_STATUS in detail for detail in response.failed_reasons)


# ---------------------------------------------------------------------------
# Layer 2 — escalation decision
# ---------------------------------------------------------------------------


def _crawler(**config: Any) -> SiteCrawler:
    return SiteCrawler(
        run_id="challenge-escalation",
        config=SiteCrawlerConfig(base_url="https://x.test/", **config),
        event_sink=CapturingSink(),
        queue_backend=InMemoryQueueBackend(),
    )


def _result(status: int, *reasons: FailureReason) -> ScrapeResult:
    return ScrapeResult(
        url="https://x.test/p",
        response_url="https://x.test/p",
        success=False,
        content_type="html",
        status_code=status,
        failure_reason=reasons[0].value if reasons else None,
        failure_details=[{reason.value: "detail"} for reason in reasons],
    )


@pytest.mark.parametrize("status", [403, 429, 503])
def test_challenge_beats_the_rate_limit_exclusion(status: int) -> None:
    crawler = _crawler()
    challenge = _result(status, FailureReason.BAD_STATUS, FailureReason.CLOUDFLARE_BLOCK)
    assert crawler._is_challenge(challenge) is True
    assert crawler._browser_may_recover(challenge) is True


def test_plain_rate_limit_is_still_owned_by_the_throttle() -> None:
    crawler = _crawler()
    throttled = _result(503, FailureReason.BAD_STATUS)
    assert crawler._is_challenge(throttled) is False
    assert crawler._browser_may_recover(throttled) is False


def test_non_primary_challenge_reason_still_triggers_escalation() -> None:
    """The decision reads EVERY recorded reason, not just the primary label —
    belt to the classification braces above."""
    crawler = _crawler()
    result = _result(500, FailureReason.BAD_STATUS, FailureReason.BLOCKED)
    assert crawler._browser_may_recover(result) is True


# ---------------------------------------------------------------------------
# End to end — the page is actually crawled
# ---------------------------------------------------------------------------


def _install_scrape(
    monkeypatch: pytest.MonkeyPatch,
    http_result: Any,
    browser_result: Any,
) -> list[str]:
    """Fake `scrape` that answers differently per request type; records the order."""
    calls: list[str] = []

    async def allow_test_url(url: str) -> None:
        return None

    async def fake_scrape(url: str, **kwargs: Any) -> ScrapeResult:
        request_type = kwargs.get("request_type")
        if request_type == RequestType.BROWSER:
            calls.append("browser")
            return browser_result(url)
        calls.append("http")
        return http_result(url)

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)
    monkeypatch.setattr("matrx_scraper.crawler.scrape", fake_scrape)
    return calls


def _ok(url: str) -> ScrapeResult:
    return ScrapeResult(
        url=url,
        response_url=url,
        success=True,
        content_type="html",
        content_type_raw="text/html",
        status_code=200,
        raw_html=_page_html(),
        raw_text="Recovered by the browser",
    )


@pytest.mark.asyncio
async def test_cloudflare_503_is_recovered_by_the_browser_not_failed_as_rate_limited(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _install_scrape(
        monkeypatch,
        http_result=lambda url: ScrapeResult(
            url=url,
            response_url=url,
            success=False,
            content_type="html",
            status_code=503,
            failure_reason=FailureReason.CLOUDFLARE_BLOCK.value,
            failure_details=[
                {FailureReason.BAD_STATUS.value: "Status code 503"},
                {FailureReason.CLOUDFLARE_BLOCK.value: "Title indicates block"},
            ],
        ),
        browser_result=_ok,
    )

    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="cf-503-recovery",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            seed_urls=["https://x.test/blocked"],
            list_mode=True,
            render_mode=RENDER_HTTP_FIRST,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        browser_pool=object(),
    )

    await crawler.run()

    # The challenge escalates immediately. No requeue loop: the HTTP attempts are
    # the single fetch plus its proxy-bypass retry, never the 5 throttled rounds.
    assert calls[-1] == "browser"
    assert calls.count("browser") == 1
    assert calls.count("http") <= 2
    fetched = sink.of_type(CrawlPageFetchedEvent)
    assert [event.url for event in fetched] == ["https://x.test/blocked"]
    assert fetched[0].http_status == 200
    assert sink.of_type(CrawlPageFailedEvent) == []


@pytest.mark.asyncio
async def test_exhausted_rate_limit_spends_one_browser_attempt_before_failing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unrecognized block wearing a 503: throttling never clears it, so the
    crawl gets one browser navigation before the page is declared dead."""
    calls = _install_scrape(
        monkeypatch,
        http_result=lambda url: ScrapeResult(
            url=url,
            response_url=url,
            success=False,
            content_type="html",
            status_code=503,
            failure_reason=FailureReason.BAD_STATUS.value,
            failure_details=[{FailureReason.BAD_STATUS.value: "Status code 503"}],
        ),
        browser_result=_ok,
    )

    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="rate-limit-exhaustion-escalation",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            seed_urls=["https://x.test/throttled"],
            list_mode=True,
            render_mode=RENDER_HTTP_FIRST,
            host_rps=1000.0,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        browser_pool=object(),
    )

    await crawler.run()

    # The throttled rounds run first (initial + 5 requeues, each with its
    # proxy-bypass retry), then exactly ONE last-chance browser navigation.
    assert calls.count("http") >= 6
    assert calls.count("browser") == 1
    assert calls[-1] == "browser"
    fetched = sink.of_type(CrawlPageFetchedEvent)
    assert [event.url for event in fetched] == ["https://x.test/throttled"]
    assert sink.of_type(CrawlPageFailedEvent) == []


# ---------------------------------------------------------------------------
# The browser-capture path uses the SAME classifier (no second hand-rolled copy)
# ---------------------------------------------------------------------------


def _browser_crawler(pool: Any, sink: Any) -> SiteCrawler:
    from test_crawler import _RecordingPersister

    return SiteCrawler(
        run_id="browser-challenge",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            seed_urls=["https://x.test/guarded"],
            list_mode=True,
            render_mode=RENDER_BROWSER_WITH_SCREENSHOT,
            capture_screenshots=True,
            host_rps=1000.0,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        body_persister=_RecordingPersister(),
        browser_pool=pool,
        screenshot_kinds=["viewport_desktop"],
        strict_persistence=True,
    )


def _pool(status: int, html: str) -> Any:
    from matrx_scraper.browser_pool import CapturedScreenshot, FetchWithCaptureResult

    class Pool:
        size = 1

        async def fetch_with_capture(self, url: str, **kwargs: Any) -> FetchWithCaptureResult:
            return FetchWithCaptureResult(
                content=html,
                response_url=url,
                status_code=status,
                headers={"content-type": "text/html"},
                title="Just a moment..." if status >= 400 else "Guarded page",
                screenshots=[
                    CapturedScreenshot(kind=kind, width=1366, height=768, bytes=b"PNG")
                    for kind in kwargs["screenshot_kinds"]
                ],
            )

    return Pool()


@pytest.mark.asyncio
async def test_browser_captured_challenge_is_classified_not_labelled_rate_limited(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The browser path used to hand-roll `bad_status` for any >=400, so a
    rendered WAF interstitial at 503 was misread as a rate limit and requeued
    5× for nothing. It now runs the one shared classifier."""

    async def allow_test_url(url: str) -> None:
        return None

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)

    sink = CapturingSink()
    await _browser_crawler(_pool(503, CHALLENGE_HTML), sink).run()

    failed = sink.of_type(CrawlPageFailedEvent)
    assert [event.error_class for event in failed] == [FailureReason.CLOUDFLARE_BLOCK.value]


@pytest.mark.asyncio
async def test_healthy_page_with_a_turnstile_widget_is_not_marked_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A protected contact form is not a block. Classification runs ONLY on a
    failing response — a 200 that embeds Turnstile stays a good page."""

    async def allow_test_url(url: str) -> None:
        return None

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow_test_url)

    protected_form = _page_html().replace(
        "</body>",
        '<div id="turnstile-wrapper">'
        '<iframe src="https://challenges.cloudflare.com/turnstile/v0/x"></iframe>'
        "</div></body>",
    )
    sink = CapturingSink()
    await _browser_crawler(_pool(200, protected_form), sink).run()

    assert sink.of_type(CrawlPageFailedEvent) == []
    assert [event.url for event in sink.of_type(CrawlPageFetchedEvent)] == [
        "https://x.test/guarded"
    ]


@pytest.mark.asyncio
async def test_exhausted_rate_limit_still_fails_when_the_browser_cannot_help(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked(url: str) -> ScrapeResult:
        return ScrapeResult(
            url=url,
            response_url=url,
            success=False,
            content_type="html",
            status_code=503,
            failure_reason=FailureReason.BAD_STATUS.value,
            failure_details=[{FailureReason.BAD_STATUS.value: "Status code 503"}],
        )

    _install_scrape(monkeypatch, http_result=blocked, browser_result=blocked)

    sink = CapturingSink()
    crawler = SiteCrawler(
        run_id="rate-limit-exhaustion-terminal",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            seed_urls=["https://x.test/dead"],
            list_mode=True,
            render_mode=RENDER_HTTP_FIRST,
            host_rps=1000.0,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        browser_pool=object(),
    )

    await crawler.run()

    failed = sink.of_type(CrawlPageFailedEvent)
    assert [event.error_class for event in failed] == ["RateLimited"]
    assert sink.of_type(CrawlPageFetchedEvent) == []
