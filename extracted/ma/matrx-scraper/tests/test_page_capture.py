from __future__ import annotations

import importlib
from types import SimpleNamespace

import pytest

from matrx_scraper import _ext
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.utils import url as url_utils

scrape_router = importlib.import_module("matrx_scraper.api.scrape_router")

#: The organization every one of these calls is ADMITTED for — it arrives on
#: the wire as `X-Organization-Id` and lands on the context
#: (matrx_connect.service_auth). `/page-capture` writes a durable parsed page
#: and can store a screenshot against it, so it never runs without one.
ORG_ID = "7f1d7b9e-3c9a-4a6d-9c3b-2a4b6d8e0f11"


def _ctx(organization_id: str | None = ORG_ID, user_id: str = "") -> SimpleNamespace:
    return SimpleNamespace(
        organization_id=organization_id,
        user_id=user_id,
        auth_type="token",
        is_authenticated=True,
    )


class FakeCache:
    """The cache contract: every read names the organization it acts in.

    `scraper.scrape_parsed_page` is org-scoped, so a cache LOOKUP that named no
    organization would be asking for whatever tenant's copy happened to be
    there. The last organization seen is recorded so a test can assert the
    admitted one reached the cache.
    """

    last_organization_id: str | None = None

    async def get(self, _key: str, *, organization_id: str | None = None):
        type(self).last_organization_id = organization_id
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
            organization_id=ORG_ID,
            site_id="site-1",
            backlink_id="backlink-1",
        ),
        target_url="https://publisher.example/article",
        ctx=_ctx(user_id="user-1"),
        organization_id=ORG_ID,
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
        ctx=_ctx(),
    )

    assert result.success is True
    assert result.from_cache is True
    # The cache lookup acted in the organization the CALL was admitted for.
    assert FakeCache.last_organization_id == ORG_ID
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
        ctx=_ctx(),
    )

    assert result.success is False
    assert result.failure_reason == "request_error"
    assert result.failure_details == [{"request_error": "connection reset by peer"}]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "full_page, expected_content, expected_scope",
    [
        (False, "The article body itself.", "main"),
        (True, "Nav Sponsor Staff bio Tags The article body itself.", "full"),
    ],
)
async def test_page_capture_returns_the_article_body_by_default(
    monkeypatch, full_page: bool, expected_content: str, expected_scope: str
) -> None:
    """THE MAIN-CONTENT LAW on the wire (see test_main_content_extraction.py).

    `content` is the article body unless the caller asks for the whole page,
    and `content_scope` always says which one it is — never silent.
    """

    async def public_url(value: str) -> str:
        return value

    async def fake_scrape(*_args, **_kwargs) -> ScrapeResult:
        return ScrapeResult(
            url="https://publisher.example/article",
            success=True,
            status_code=200,
            response_url="https://publisher.example/article",
            content_type="text/html",
            text_data="Nav Sponsor Staff bio Tags The article body itself.",
            main_content_text="The article body itself.",
            main_content_selector="article",
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
        scrape_router.PageCaptureRequest(
            url="https://publisher.example/article", full_page=full_page
        ),
        ctx=_ctx(),
    )

    assert result.content == expected_content
    assert result.content_scope == expected_scope
    assert result.char_count == len(expected_content)


@pytest.mark.asyncio
async def test_page_capture_falls_back_to_the_full_page_honestly(monkeypatch) -> None:
    """A non-article page has no main content — say "full", never a half page."""

    async def public_url(value: str) -> str:
        return value

    async def fake_scrape(*_args, **_kwargs) -> ScrapeResult:
        return ScrapeResult(
            url="https://publisher.example/pricing",
            success=True,
            status_code=200,
            response_url="https://publisher.example/pricing",
            content_type="text/html",
            text_data="Pricing table and plan comparison.",
        )

    monkeypatch.setattr(url_utils, "validate_public_http_url", public_url)
    monkeypatch.setattr(
        url_utils,
        "get_url_info",
        lambda _url: SimpleNamespace(unique_page_name="publisher-example-pricing"),
    )
    monkeypatch.setattr(_ext, "get_ext", lambda name: FakeCache() if name == "cache" else None)
    monkeypatch.setattr(_ext, "has_ext", lambda _name: False)
    monkeypatch.setattr("matrx_scraper.orchestrator.scrape", fake_scrape)

    result = await scrape_router.page_capture(
        scrape_router.PageCaptureRequest(url="https://publisher.example/pricing"),
        ctx=_ctx(),
    )

    assert result.content == "Pricing table and plan comparison."
    assert result.content_scope == "full"


@pytest.mark.asyncio
async def test_page_capture_refuses_a_context_with_no_organization(monkeypatch) -> None:
    """THE TENANT IS ON THE WIRE (2026-09-17). Before this, the scraper's
    service routers were mounted `organization_optional=True` and this route
    took its tenant from the request BODY — so a call that named none simply
    had no tenant, and nothing screamed."""
    from fastapi import HTTPException

    async def public_url(value: str) -> str:
        return value

    monkeypatch.setattr(url_utils, "validate_public_http_url", public_url)

    with pytest.raises(HTTPException) as excinfo:
        await scrape_router.page_capture(
            scrape_router.PageCaptureRequest(url="https://publisher.example/article"),
            ctx=_ctx(organization_id=None),
        )
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail["code"] == "organization_required"


@pytest.mark.asyncio
async def test_page_capture_refuses_a_body_naming_another_organization(monkeypatch) -> None:
    """A body value CONFIRMS the admitted organization; it never replaces it."""
    from fastapi import HTTPException

    async def public_url(value: str) -> str:
        return value

    monkeypatch.setattr(url_utils, "validate_public_http_url", public_url)

    with pytest.raises(HTTPException) as excinfo:
        await scrape_router.page_capture(
            scrape_router.PageCaptureRequest(
                url="https://publisher.example/article",
                organization_id="11111111-1111-4111-8111-111111111111",
            ),
            ctx=_ctx(),
        )
    assert excinfo.value.status_code == 409
    assert excinfo.value.detail["code"] == "organization_context_mismatch"


@pytest.mark.asyncio
async def test_backlink_screenshot_stores_against_the_admitted_organization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The file is stamped with the organization the CALL was admitted for —
    not with whatever the body carried."""
    seen: dict[str, object] = {}

    class FakeShot:
        bytes = b"png"
        width = 10
        height = 10

    class FakeBrowserPool:
        async def fetch_with_capture(self, _url: str, **_kwargs: object) -> SimpleNamespace:
            return SimpleNamespace(
                response_url="https://publisher.example/article",
                screenshots=[FakeShot()],
                screenshot_failures=[],
                content='<a data-matrx-backlink-matches="1"></a>',
            )

    async def public_url(value: str) -> str:
        return value

    class FakeFileService:
        def __init__(self, _fm: object) -> None:
            pass

        async def upload_with_intent(self, _data: bytes, **kwargs: object) -> dict[str, str]:
            seen["organization_id"] = kwargs["organization_id"]
            seen["metadata_organization_id"] = kwargs["metadata"]["organization_id"]
            return {"file_id": "file-1"}

    monkeypatch.setattr(url_utils, "validate_public_http_url", public_url)
    monkeypatch.setattr(_ext, "has_ext", lambda _name: True)
    monkeypatch.setattr(
        _ext,
        "get_ext",
        lambda name: FakeBrowserPool() if name == "browser_pool" else object(),
    )
    monkeypatch.setattr("matrx_files.service.FileService", FakeFileService)

    result = await scrape_router._capture_backlink_screenshot(
        request=scrape_router.PageCaptureRequest(
            url="https://publisher.example/article",
            target_url="https://brand.example/service",
            capture_screenshot=True,
            site_id="site-1",
            backlink_id="backlink-1",
        ),
        target_url="https://publisher.example/article",
        ctx=_ctx(user_id="user-1"),
        organization_id=ORG_ID,
    )

    assert result["screenshot_file_id"] == "file-1"
    assert seen["organization_id"] == ORG_ID
    assert seen["metadata_organization_id"] == ORG_ID
