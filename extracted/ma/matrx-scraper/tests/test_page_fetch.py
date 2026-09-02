"""prepare_page_fetch — the on-demand single-page capture command.

The command must reuse the exact single-URL capture pipeline (list_mode,
max_pages=1, seeded with the requested URL) with scope mode "page_fetch",
and reject blank URLs before any infrastructure work happens.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from matrx_scraper.web_crawl.contracts import PageFetchRequest
from matrx_scraper.web_crawl.service import WebCrawlService


@pytest.mark.asyncio
async def test_page_fetch_builds_single_url_capture_request() -> None:
    service = WebCrawlService.__new__(WebCrawlService)
    service.prepare_start = AsyncMock(return_value="prepared")  # type: ignore[method-assign]

    result = await service.prepare_page_fetch(
        ctx=object(),
        site_id="site-1",
        url="  https://example.com/pricing  ",
    )

    assert result == "prepared"
    args, kwargs = service.prepare_start.await_args
    request = args[2]
    assert kwargs == {"page_fetch": True}
    assert request.seed_urls == ["https://example.com/pricing"]
    assert request.list_mode is True
    assert request.max_pages == 1
    assert request.max_depth == 0
    assert request.seed_from_sitemap is False
    assert request.capture_screenshots is True
    assert request.screenshot_kinds == ["viewport_desktop"]


@pytest.mark.asyncio
async def test_page_fetch_without_screenshot_uses_http_render() -> None:
    service = WebCrawlService.__new__(WebCrawlService)
    service.prepare_start = AsyncMock(return_value="prepared")  # type: ignore[method-assign]

    await service.prepare_page_fetch(
        ctx=object(),
        site_id="site-1",
        url="https://example.com/",
        capture_screenshot=False,
    )

    args, _ = service.prepare_start.await_args
    request = args[2]
    assert request.capture_screenshots is False
    assert request.screenshot_kinds == []


@pytest.mark.asyncio
async def test_page_fetch_rejects_blank_url() -> None:
    service = WebCrawlService.__new__(WebCrawlService)
    service.prepare_start = AsyncMock()  # type: ignore[method-assign]

    with pytest.raises(ValueError, match="url is required"):
        await service.prepare_page_fetch(ctx=object(), site_id="site-1", url="   ")
    service.prepare_start.assert_not_awaited()


def test_page_fetch_request_forbids_unknown_fields() -> None:
    with pytest.raises(Exception):
        PageFetchRequest(url="https://example.com/", nope=True)  # type: ignore[call-arg]
