"""prepare_page_fetch — the on-demand single-page capture command.

SUT: `WebCrawlService.prepare_page_fetch`. It OWNS the request it hands to
`prepare_start`: exactly one URL (trimmed), no discovery (list mode, one page,
depth 0, no sitemap seeding), robots ignored for a page the user explicitly
asked for, and the screenshot choice mapped to the render mode. It also owns
refusing a blank URL before any session work. `prepare_start` (session row,
host boundary, run lease) is its dependency and is doubled; the request that
reaches it is the contract.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from matrx_scraper.crawler import RENDER_BROWSER_WITH_SCREENSHOT, RENDER_HTTP_FIRST
from matrx_scraper.web_crawl.contracts import CrawlStartRequest, PageFetchRequest
from matrx_scraper.web_crawl.service import WebCrawlService


def _service_with_recorded_start() -> tuple[WebCrawlService, AsyncMock, object]:
    prepared = object()
    service = WebCrawlService.__new__(WebCrawlService)
    start = AsyncMock(return_value=prepared)
    service.prepare_start = start  # type: ignore[method-assign]
    return service, start, prepared


@pytest.mark.asyncio
async def test_page_fetch_hands_prepare_start_one_trimmed_url_with_no_discovery() -> None:
    service, start, prepared = _service_with_recorded_start()
    ctx = object()

    result = await service.prepare_page_fetch(
        ctx=ctx,  # type: ignore[arg-type]
        site_id="site-1",
        url="  https://example.com/pricing  ",
    )

    assert result is prepared
    start.assert_awaited_once()
    (ctx_arg, site_arg, request), kwargs = start.await_args
    assert ctx_arg is ctx
    assert site_arg == "site-1"
    assert kwargs == {"page_fetch": True}
    assert isinstance(request, CrawlStartRequest)
    assert request.seed_urls == ["https://example.com/pricing"]
    assert request.list_mode is True
    assert request.max_pages == 1
    assert request.max_depth == 0
    assert request.concurrency == 1
    assert request.seed_from_sitemap is False
    # A page the user explicitly asked for is fetched even if robots.txt disallows crawlers.
    assert request.respect_robots is False


@pytest.mark.parametrize(
    ("capture_screenshot", "render_mode", "screenshot_kinds"),
    [
        (True, RENDER_BROWSER_WITH_SCREENSHOT, ["viewport_desktop"]),
        (False, RENDER_HTTP_FIRST, []),
    ],
)
@pytest.mark.asyncio
async def test_page_fetch_render_mode_follows_the_screenshot_choice(
    capture_screenshot: bool, render_mode: str, screenshot_kinds: list[str]
) -> None:
    service, start, _prepared = _service_with_recorded_start()

    await service.prepare_page_fetch(
        ctx=object(),  # type: ignore[arg-type]
        site_id="site-1",
        url="https://example.com/",
        capture_screenshot=capture_screenshot,
    )

    (_ctx, _site, request), _kwargs = start.await_args
    assert request.render_mode == render_mode
    assert request.capture_screenshots is capture_screenshot
    assert request.screenshot_kinds == screenshot_kinds


@pytest.mark.asyncio
async def test_page_fetch_captures_a_screenshot_by_default() -> None:
    service, start, _prepared = _service_with_recorded_start()

    await service.prepare_page_fetch(
        ctx=object(),  # type: ignore[arg-type]
        site_id="site-1",
        url="https://example.com/",
    )

    (_ctx, _site, request), _kwargs = start.await_args
    assert request.render_mode == RENDER_BROWSER_WITH_SCREENSHOT
    assert request.screenshot_kinds == ["viewport_desktop"]


@pytest.mark.parametrize("blank", ["", "   ", "\n\t "])
@pytest.mark.asyncio
async def test_page_fetch_refuses_a_blank_url_before_any_session_is_prepared(blank: str) -> None:
    service, start, _prepared = _service_with_recorded_start()

    with pytest.raises(ValueError, match="url is required"):
        await service.prepare_page_fetch(
            ctx=object(),  # type: ignore[arg-type]
            site_id="site-1",
            url=blank,
        )
    start.assert_not_awaited()


def test_page_fetch_request_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError, match="nope"):
        PageFetchRequest(url="https://example.com/", nope=True)  # type: ignore[call-arg]
