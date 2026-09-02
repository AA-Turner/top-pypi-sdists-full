"""The per-crawl User-Agent override must reach the WIRE — on BOTH fetch paths.

A UA that applies to only one render mode is worse than no UA at all: the same
crawl would then present two different identities depending on whether the page
happened to need the browser, and a customer's WAF allowlist would let half the
crawl through. So these tests assert against a REAL socket — the header the
server actually received — never against an intermediate kwarg dict.

Three properties, each pinned end to end:

1. Set the override → every transport sends exactly it (httpx, curl_cffi, and
   a real headless Chromium context).
2. Omit the override → every transport sends exactly what it sent before this
   field existed. The override is opt-in, not a silent behaviour change.
3. An empty / whitespace override is "no override", NEVER an empty
   `User-Agent:` header — an empty UA is its own blocked signal.
"""

from __future__ import annotations

import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from matrx_scraper.browser_pool import (
    DESKTOP_PROFILE,
    MOBILE_PROFILE,
    PlaywrightBrowserPool,
)
from matrx_scraper.scraper import HEADER_PROFILES, RequestType, fetch
from matrx_scraper.user_agents import (
    MATRX_CRAWLER_USER_AGENT,
    MAX_USER_AGENT_LENGTH,
    InvalidUserAgentError,
    normalize_user_agent,
    preset_value,
    presets_payload,
)
from matrx_scraper.web_crawl.contracts import CrawlStartRequest

OVERRIDE = "MatrxCrawlerTest/9.9 (+https://aimatrx.com/test)"

_BODY = b"<!doctype html><html><head><title>ua</title></head><body>hello</body></html>"


class _RecordingHandler(BaseHTTPRequestHandler):
    """Records the User-Agent header of every request it serves."""

    received: list[str | None] = []

    def do_GET(self) -> None:  # noqa: N802 - stdlib API
        type(self).received.append(self.headers.get("User-Agent"))
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(_BODY)))
        self.end_headers()
        self.wfile.write(_BODY)

    def log_message(self, *args: object) -> None:  # silence test output
        return


@pytest.fixture
def ua_server():
    """A real local HTTP server that reports the UA header it was sent."""

    class Handler(_RecordingHandler):
        received: list[str | None] = []

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}/", Handler.received
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


# ---------------------------------------------------------------------------
# normalize_user_agent — the one gate
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("blank", [None, "", "   ", "\t  "])
def test_blank_override_is_no_override_never_an_empty_header(blank: str | None) -> None:
    assert normalize_user_agent(blank) is None


def test_override_is_stripped_but_otherwise_preserved() -> None:
    assert normalize_user_agent("  Bot/1.0 (+https://x.test)  ") == "Bot/1.0 (+https://x.test)"


@pytest.mark.parametrize(
    "bad",
    [
        "Bot/1.0\r\nX-Injected: yes",  # header injection
        "Bot/1.0\nX-Injected: yes",
        "Bot\x00/1.0",  # NUL
        "Bot\x7f/1.0",  # DEL
        "Bot\x85/1.0",  # C1
    ],
)
def test_control_characters_are_rejected(bad: str) -> None:
    with pytest.raises(InvalidUserAgentError):
        normalize_user_agent(bad)


def test_a_newline_cannot_hide_behind_the_strip() -> None:
    """`"x\\n".strip()` is clean — the check must run on the ORIGINAL value."""
    with pytest.raises(InvalidUserAgentError):
        normalize_user_agent("Bot/1.0\n")


def test_length_is_bounded() -> None:
    assert normalize_user_agent("a" * MAX_USER_AGENT_LENGTH)
    with pytest.raises(InvalidUserAgentError):
        normalize_user_agent("a" * (MAX_USER_AGENT_LENGTH + 1))


def test_non_latin1_is_rejected_here_not_mid_crawl() -> None:
    with pytest.raises(InvalidUserAgentError):
        normalize_user_agent("Bot/1.0 \U0001f600")


def test_normalization_is_idempotent() -> None:
    once = normalize_user_agent("  Bot/1.0  ")
    assert normalize_user_agent(once) == once


# ---------------------------------------------------------------------------
# Presets — the affordance a non-technical user actually picks from
# ---------------------------------------------------------------------------


def test_default_preset_means_no_override_not_our_bot_ua() -> None:
    assert preset_value("default") is None
    assert preset_value("matrx") == MATRX_CRAWLER_USER_AGENT


def test_unknown_preset_raises_rather_than_degrading_to_no_override() -> None:
    with pytest.raises(InvalidUserAgentError):
        preset_value("gooooglebot")


def test_every_preset_value_survives_the_request_contract() -> None:
    """A preset a UI offers but the API rejects is a dead button."""
    for preset in presets_payload():
        assert CrawlStartRequest(user_agent=preset["value"]).user_agent == preset["value"]


def test_presets_are_human_labelled() -> None:
    for preset in presets_payload():
        assert preset["label"] and not preset["label"].startswith("Mozilla/")
        assert preset["description"]


# ---------------------------------------------------------------------------
# The request contract
# ---------------------------------------------------------------------------


def test_request_default_is_no_override() -> None:
    assert CrawlStartRequest().user_agent is None


def test_request_normalizes_blank_to_none() -> None:
    assert CrawlStartRequest(user_agent="   ").user_agent is None


def test_request_rejects_a_control_character() -> None:
    with pytest.raises(ValueError, match="control characters"):
        CrawlStartRequest(user_agent="Bot/1.0\nX: y")


def test_preset_round_trips_through_a_saved_preset_config() -> None:
    """`web.crawl_preset.config` IS a CrawlStartRequest — the override is
    saved and restored with everything else, for free."""
    saved = CrawlStartRequest(user_agent=OVERRIDE).model_dump()
    assert CrawlStartRequest.model_validate(saved).user_agent == OVERRIDE


# ---------------------------------------------------------------------------
# WIRE PROOF — HTTP transport
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("use_curl_cffi", [False, True])
def test_http_fetch_sends_the_override_on_the_wire(ua_server, use_curl_cffi: bool) -> None:
    url, received = ua_server
    response = asyncio.run(
        fetch(
            url,
            request_type=RequestType.NORMAL,
            use_curl_cffi=use_curl_cffi,
            user_agent=OVERRIDE,
        )
    )
    assert response.status_code == 200
    assert received == [OVERRIDE]


@pytest.mark.parametrize("use_curl_cffi", [False, True])
def test_http_fetch_without_override_is_byte_identical(ua_server, use_curl_cffi: bool) -> None:
    """No override → the profile's own UA, unchanged. Pinned against an
    explicit profile so the assertion does not depend on the random pick."""
    url, received = ua_server
    profile = HEADER_PROFILES[0]
    asyncio.run(
        fetch(
            url,
            request_type=RequestType.NORMAL,
            use_curl_cffi=use_curl_cffi,
            header_profile=profile,
        )
    )
    assert received == [profile["headers"]["User-Agent"]]


@pytest.mark.parametrize("blank", ["", "   "])
def test_http_fetch_blank_override_never_sends_an_empty_ua(ua_server, blank: str) -> None:
    url, received = ua_server
    profile = HEADER_PROFILES[0]
    asyncio.run(
        fetch(
            url,
            request_type=RequestType.NORMAL,
            use_curl_cffi=False,
            header_profile=profile,
            user_agent=blank,
        )
    )
    assert received == [profile["headers"]["User-Agent"]]


def test_http_fetch_keeps_the_rest_of_the_profile_headers(ua_server) -> None:
    """The override changes WHO we say we are, not the whole request."""
    url, _ = ua_server
    captured: dict[str, str] = {}

    class Capturing(_RecordingHandler):
        def do_GET(self) -> None:  # noqa: N802
            captured.update(dict(self.headers))
            super().do_GET()

    server = HTTPServer(("127.0.0.1", 0), Capturing)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        asyncio.run(
            fetch(
                f"http://{host}:{port}/",
                request_type=RequestType.NORMAL,
                use_curl_cffi=False,
                header_profile=HEADER_PROFILES[0],
                user_agent=OVERRIDE,
            )
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    assert captured.get("User-Agent") == OVERRIDE
    assert captured.get("Accept-Language") == HEADER_PROFILES[0]["headers"]["Accept-Language"]


# ---------------------------------------------------------------------------
# WIRE PROOF — browser transport (a real headless Chromium context)
# ---------------------------------------------------------------------------


def _chromium_available() -> bool:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return False

    async def _probe() -> bool:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                await browser.close()
            return True
        except Exception:
            return False

    return asyncio.run(_probe())


chromium = pytest.mark.skipif(not _chromium_available(), reason="headless Chromium is unavailable")


@chromium
def test_browser_fetch_sends_the_override_on_the_wire(ua_server) -> None:
    url, received = ua_server

    async def run() -> None:
        pool = PlaywrightBrowserPool(pool_size=1)
        await pool.start()
        try:
            await pool.fetch(url, user_agent=OVERRIDE)
        finally:
            await pool.stop()

    asyncio.run(run())
    assert received and received[0] == OVERRIDE


@chromium
def test_browser_fetch_without_override_is_unchanged(ua_server) -> None:
    """No override → whatever headless Chromium sends today. We do not assert
    the exact string (it moves with the bundled browser), only that it is the
    untouched Chrome UA and emphatically not empty."""
    url, received = ua_server

    async def run() -> None:
        pool = PlaywrightBrowserPool(pool_size=1)
        await pool.start()
        try:
            await pool.fetch(url)
        finally:
            await pool.stop()

    asyncio.run(run())
    assert received and received[0]
    assert received[0] != OVERRIDE
    assert "Chrome" in received[0]


@chromium
def test_browser_capture_sends_the_override_on_the_wire(ua_server) -> None:
    """`fetch_with_capture` is the screenshot path — the one that used a DEVICE
    profile UA. The override must beat the profile there too."""
    url, received = ua_server

    async def run() -> None:
        pool = PlaywrightBrowserPool(pool_size=1)
        await pool.start()
        try:
            await pool.fetch_with_capture(
                url,
                screenshot_kinds=["viewport_desktop"],
                user_agent=OVERRIDE,
            )
        finally:
            await pool.stop()

    asyncio.run(run())
    assert received and received[0] == OVERRIDE


@chromium
def test_browser_capture_without_override_uses_the_device_profile_ua(ua_server) -> None:
    url, received = ua_server

    async def run() -> None:
        pool = PlaywrightBrowserPool(pool_size=1)
        await pool.start()
        try:
            await pool.fetch_with_capture(url, screenshot_kinds=["viewport_desktop"])
        finally:
            await pool.stop()

    asyncio.run(run())
    assert received and received[0] == DESKTOP_PROFILE.user_agent


@chromium
def test_override_applies_to_every_device_profile_in_one_capture(ua_server) -> None:
    """Desktop and mobile kinds are SEPARATE navigations with separate
    contexts. A UA that only reached the first navigation would make one crawl
    present two identities."""
    url, received = ua_server

    async def run() -> None:
        pool = PlaywrightBrowserPool(pool_size=1)
        await pool.start()
        try:
            await pool.fetch_with_capture(
                url,
                screenshot_kinds=["viewport_desktop", "viewport_mobile"],
                user_agent=OVERRIDE,
            )
        finally:
            await pool.stop()

    asyncio.run(run())
    assert len(received) >= 2
    assert set(received) == {OVERRIDE}


def test_override_replaces_only_the_ua_never_the_device_geometry() -> None:
    """A mobile screenshot taken "as Googlebot" is still a MOBILE screenshot."""
    kwargs = MOBILE_PROFILE.context_kwargs(OVERRIDE)
    assert kwargs["user_agent"] == OVERRIDE
    assert kwargs["is_mobile"] is True
    assert kwargs["has_touch"] is True
    assert kwargs["device_scale_factor"] == MOBILE_PROFILE.device_scale_factor
    assert kwargs["viewport"] == MOBILE_PROFILE.viewport

    untouched = MOBILE_PROFILE.context_kwargs()
    assert untouched["user_agent"] == MOBILE_PROFILE.user_agent


# ---------------------------------------------------------------------------
# The crawler forwards ONE resolved identity to BOTH render modes
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_crawler_forwards_the_override_to_the_http_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.crawler import (
        RENDER_HTTP_ONLY,
        SiteCrawler,
        SiteCrawlerConfig,
    )
    from matrx_scraper.orchestrator import ScrapeResult
    from matrx_scraper.queue_backend import InMemoryQueueBackend

    async def allow(url: str) -> None:
        return None

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow)

    seen: list[str | None] = []

    async def fake_scrape(url: str, **kwargs: object) -> ScrapeResult:
        seen.append(kwargs.get("user_agent"))
        return ScrapeResult(
            url=url,
            response_url=url,
            success=True,
            content_type="html",
            status_code=200,
            raw_html=_BODY.decode(),
        )

    monkeypatch.setattr("matrx_scraper.crawler.scrape", fake_scrape)

    crawler = SiteCrawler(
        run_id="ua-http",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            render_mode=RENDER_HTTP_ONLY,
            capture_screenshots=False,
            user_agent_override=OVERRIDE,
        ),
        queue_backend=InMemoryQueueBackend(),
    )
    await crawler.run()

    assert seen == [OVERRIDE]


@pytest.mark.asyncio
async def test_crawler_forwards_the_same_override_to_the_browser_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Same config, other render mode → the SAME identity on the wire. This is
    the property that makes the override safe: a crawl cannot present one UA
    over HTTP and a different one when it escalates to the browser."""
    from matrx_scraper.browser_pool import FetchWithCaptureResult
    from matrx_scraper.crawler import (
        RENDER_BROWSER_WITH_SCREENSHOT,
        SiteCrawler,
        SiteCrawlerConfig,
    )
    from matrx_scraper.queue_backend import InMemoryQueueBackend

    async def allow(url: str) -> None:
        return None

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow)

    seen: list[str | None] = []

    class BrowserPool:
        async def fetch_with_capture(self, url: str, **kwargs: object) -> FetchWithCaptureResult:
            seen.append(kwargs.get("user_agent"))
            return FetchWithCaptureResult(
                content=_BODY.decode(),
                response_url=url,
                status_code=200,
                headers={"content-type": "text/html"},
                title="ua",
            )

    crawler = SiteCrawler(
        run_id="ua-browser",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            render_mode=RENDER_BROWSER_WITH_SCREENSHOT,
            capture_screenshots=True,
            user_agent_override=OVERRIDE,
        ),
        queue_backend=InMemoryQueueBackend(),
        browser_pool=BrowserPool(),
        screenshot_kinds=["viewport_desktop"],
    )
    await crawler.run()

    assert seen == [OVERRIDE]


@pytest.mark.asyncio
async def test_crawler_without_an_override_passes_none_to_the_transports(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Omitted → the transports get `None` and keep their own defaults."""
    from matrx_scraper.crawler import (
        RENDER_HTTP_ONLY,
        SiteCrawler,
        SiteCrawlerConfig,
    )
    from matrx_scraper.orchestrator import ScrapeResult
    from matrx_scraper.queue_backend import InMemoryQueueBackend

    async def allow(url: str) -> None:
        return None

    monkeypatch.setattr("matrx_scraper.crawler.validate_public_http_url", allow)

    seen: list[str | None] = []

    async def fake_scrape(url: str, **kwargs: object) -> ScrapeResult:
        seen.append(kwargs.get("user_agent"))
        return ScrapeResult(
            url=url,
            response_url=url,
            success=True,
            content_type="html",
            status_code=200,
            raw_html=_BODY.decode(),
        )

    monkeypatch.setattr("matrx_scraper.crawler.scrape", fake_scrape)

    crawler = SiteCrawler(
        run_id="ua-none",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            max_pages=1,
            concurrency=1,
            respect_robots=False,
            seed_from_sitemap=False,
            render_mode=RENDER_HTTP_ONLY,
            capture_screenshots=False,
        ),
        queue_backend=InMemoryQueueBackend(),
    )
    await crawler.run()

    assert seen == [None]


def test_override_also_governs_robots_and_sitemap_identity() -> None:
    """Robots matching and sitemap discovery must agree with the page fetches.
    Crawling "as Googlebot" while evaluating robots.txt as MatrxScraperBot
    would apply one site's rules to another site's identity."""
    from matrx_scraper.crawler import SiteCrawler, SiteCrawlerConfig
    from matrx_scraper.queue_backend import InMemoryQueueBackend

    crawler = SiteCrawler(
        run_id="ua-robots",
        config=SiteCrawlerConfig(
            base_url="https://x.test/",
            respect_robots=True,
            user_agent_override=OVERRIDE,
        ),
        queue_backend=InMemoryQueueBackend(),
    )
    assert crawler.user_agent == OVERRIDE
    assert crawler._robots is not None
    assert crawler._robots.user_agent == OVERRIDE

    default_crawler = SiteCrawler(
        run_id="ua-robots-default",
        config=SiteCrawlerConfig(base_url="https://x.test/", respect_robots=True),
        queue_backend=InMemoryQueueBackend(),
    )
    assert default_crawler.user_agent == SiteCrawlerConfig.user_agent
    assert default_crawler._user_agent_override is None
