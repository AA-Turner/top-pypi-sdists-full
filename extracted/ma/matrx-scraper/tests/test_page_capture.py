from __future__ import annotations

import importlib
from types import SimpleNamespace

import pytest

from matrx_scraper import _ext
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.utils import url as url_utils

scrape_router = importlib.import_module("matrx_scraper.api.scrape_router")


class FakeCache:
    async def get(self, _key: str):
        return {"cached": True}


@pytest.mark.asyncio
async def test_backlink_screenshot_uses_direct_render_after_proxied_parse(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_kwargs: dict[str, object] = {}

    class FakeBrowserPool:
        async def fetch_with_capture(self, _url: str, **kwargs: object) -> SimpleNamespace:
            captured_kwargs.update(kwargs)
            return SimpleNamespace(
                response_url="https://publisher.example/article",
                screenshots=[],
                screenshot_failures=[],
            )

    async def public_url(value: str) -> str:
        return value

    monkeypatch.setattr(url_utils, "validate_public_http_url", public_url)
    monkeypatch.setattr(_ext, "has_ext", lambda _name: True)
    monkeypatch.setattr(
        _ext,
        "get_ext",
        lambda name: FakeBrowserPool() if name == "browser_pool" else object(),
    )

    result = await scrape_router._capture_backlink_screenshot(
        request=scrape_router.PageCaptureRequest(
            url="https://publisher.example/article",
            target_url="https://brand.example/service",
            capture_screenshot=True,
            organization_id="org-1",
            site_id="site-1",
            backlink_id="backlink-1",
        ),
        target_url="https://publisher.example/article",
        ctx=SimpleNamespace(user_id="user-1"),
    )

    assert result == {"screenshot_failure_reason": "browser returned no screenshot"}
    assert "proxy" not in captured_kwargs


@pytest.mark.asyncio
async def test_page_capture_returns_bounded_text_and_exact_target_links(monkeypatch) -> None:
    async def public_url(value: str) -> str:
        return value

    async def fake_scrape(*_args, **_kwargs) -> ScrapeResult:
        return ScrapeResult(
            url="https://publisher.example/article",
            success=True,
            status_code=200,
            response_url="https://publisher.example/article",
            title="Independent guide",
            content_type="text/html",
            ai_research_content="123456789",
            link_records=[
                {
                    "target_url": "https://brand.example/service/",
                    "anchor_text": "Brand service",
                },
                {
                    "target_url": "https://unrelated.example/",
                    "anchor_text": "Unrelated",
                },
            ],
        )

    monkeypatch.setattr(url_utils, "validate_public_http_url", public_url)
    monkeypatch.setattr(
        url_utils,
        "get_url_info",
        lambda _url: SimpleNamespace(unique_page_name="publisher-example-article"),
    )
    monkeypatch.setattr(_ext, "get_ext", lambda name: FakeCache() if name == "cache" else None)
    monkeypatch.setattr(_ext, "has_ext", lambda _name: False)
    monkeypatch.setattr("matrx_scraper.orchestrator.scrape", fake_scrape)
    monkeypatch.setattr(scrape_router, "PAGE_CAPTURE_MAX_TEXT_CHARS", 5)

    result = await scrape_router.page_capture(
        scrape_router.PageCaptureRequest(
            url="https://publisher.example/article",
            target_url="https://brand.example/service",
        ),
        ctx=SimpleNamespace(),
    )

    assert result.success is True
    assert result.from_cache is True
    assert result.char_count == 9
    assert result.content == "12345"
    assert result.content_truncated is True
    # Typed since CapturedLink replaced the untyped list[dict] on the wire.
    # Only the target-matching anchor survives, and the keys the extractor
    # didn't supply fall back to their declared defaults.
    assert result.links_to_target == [
        scrape_router.CapturedLink(
            target_url="https://brand.example/service/",
            anchor_text="Brand service",
        )
    ]
    assert result.links_to_target[0].link_type == "external"
    assert result.links_to_target[0].nofollow is False


@pytest.mark.asyncio
async def test_page_capture_preserves_underlying_failure_details(monkeypatch) -> None:
    async def public_url(value: str) -> str:
        return value

    async def fake_scrape(*_args, **_kwargs) -> ScrapeResult:
        return ScrapeResult(
            url="https://publisher.example/article",
            success=False,
            status_code=0,
            response_url="https://publisher.example/article",
            content_type="text/html",
            failure_reason="request_error",
            failure_details=[{"request_error": "connection reset by peer"}],
        )

    monkeypatch.setattr(url_utils, "validate_public_http_url", public_url)
    monkeypatch.setattr(
        url_utils,
        "get_url_info",
        lambda _url: SimpleNamespace(unique_page_name="publisher-example-article"),
    )
    monkeypatch.setattr(_ext, "get_ext", lambda name: FakeCache() if name == "cache" else None)
    monkeypatch.setattr(_ext, "has_ext", lambda _name: False)
    monkeypatch.setattr("matrx_scraper.orchestrator.scrape", fake_scrape)

    result = await scrape_router.page_capture(
        scrape_router.PageCaptureRequest(url="https://publisher.example/article"),
        ctx=SimpleNamespace(),
    )

    assert result.success is False
    assert result.failure_reason == "request_error"
    assert result.failure_details == [{"request_error": "connection reset by peer"}]
