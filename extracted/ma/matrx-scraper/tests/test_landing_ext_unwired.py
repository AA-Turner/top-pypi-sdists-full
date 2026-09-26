"""No silent producer: every page a scraper route reads becomes a Source, or says why not.

SOURCE-CONVERGENCE §3 / §7 (Phase 1b guard). The landing door is an injected extension point
(``configure_ext(source_landing=...)``). These tests pin the contract at every result boundary:

* with NO hook registered, a successful parse RAISES ``SourceLandingNotConfigured`` — at the
  package helper, at ``/page-capture``, at ``/batch``, at ``/content/save`` and inside the
  streaming service — never a quiet scrape that produced no Source;
* ``use_cache=false`` still lands (landing is at the result boundary, not inside ``cache.set``);
* a wired hook that FAILS for one page is announced on that page's result as a notice, and the
  scrape still answers;
* every result payload carries ``processed_document_id``.
"""

from __future__ import annotations

import importlib
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper import _ext
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.source_landing import (
    SourceLandingFailed,
    SourceLandingNotConfigured,
    land_page_result,
)

scrape_router = importlib.import_module("matrx_scraper.api.scrape_router")
ext_router = importlib.import_module("matrx_scraper.api.ext_router")

ORG_ID = "7f1d7b9e-3c9a-4a6d-9c3b-2a4b6d8e0f11"
USER_ID = "4cf62e4e-2679-484a-a652-8ee8ce4ef9f2"
DOC_ID = "11111111-2222-4333-8444-555555555555"

PAGE_MD = "# Widgets\nWidgets are small.\n## Pricing\nThey cost one dollar.\n### Bulk\nTen for nine."


def _result(**overrides: Any) -> ScrapeResult:
    fields: dict[str, Any] = {
        "url": "https://example.com/widgets/",
        "response_url": "https://example.com/widgets/#top",
        "success": True,
        "content_type": "text/html",
        "title": "Widgets",
        "markdown_renderable": PAGE_MD,
        "links": {"internal": ["https://example.com/a"], "external": []},
        "images": [{"src": "https://example.com/w.png", "alt": "a widget"}],
        "cms": "wordpress",
        "engine": "http",
        "raw_html": "<html><h1>Widgets</h1></html>",
    }
    fields.update(overrides)
    return ScrapeResult(**fields)


def _ctx(user_id: str = USER_ID) -> SimpleNamespace:
    return SimpleNamespace(organization_id=ORG_ID, user_id=user_id, auth_type="token", is_authenticated=True)


class RecordingHook:
    def __init__(self, fail: Exception | None = None) -> None:
        self.calls: list[dict[str, Any]] = []
        self.fail = fail

    async def __call__(self, landing: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(landing)
        if self.fail is not None:
            raise self.fail
        return {"processed_document_id": DOC_ID, "source_id": "spp-1", "notices": [], "kept": landing["keep"]}


class FakeCache:
    def __init__(self) -> None:
        self.gets = 0

    async def get(self, *_a: Any, **_k: Any) -> None:
        self.gets += 1
        return None


@pytest.fixture
def registry(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """A clean ext registry for one test — nothing leaks from the host or another test."""
    fresh: dict[str, Any] = {}
    monkeypatch.setattr(_ext, "_registry", fresh)
    return fresh


@pytest.fixture
def page_capture_env(monkeypatch: pytest.MonkeyPatch, registry: dict[str, Any]) -> dict[str, Any]:
    """`/page-capture` with the network faked: public-URL check passes, scrape returns a page."""
    seen: dict[str, Any] = {}

    async def _public(url: str) -> str:
        return url

    async def _scrape(url: str, **kwargs: Any) -> ScrapeResult:
        seen["cache"] = kwargs.get("cache")
        return _result()

    monkeypatch.setattr("matrx_scraper.utils.url.validate_public_http_url", _public)
    monkeypatch.setattr("matrx_scraper.orchestrator.scrape", _scrape)
    registry["cache"] = FakeCache()
    registry["domain_config"] = object()
    return seen


# ── the package helper ─────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_unwired_hook_raises_at_the_result_boundary(registry: dict[str, Any]) -> None:
    with pytest.raises(SourceLandingNotConfigured, match="configure_ext\\(source_landing"):
        await land_page_result(_result(), organization_id=ORG_ID, user_id=USER_ID, origin_client="web")


@pytest.mark.asyncio
async def test_a_wired_hook_lands_the_parse_as_sections_with_structured_raw_fields(registry: dict[str, Any]) -> None:
    hook = RecordingHook()
    registry["source_landing"] = hook
    outcome = await land_page_result(_result(), organization_id=ORG_ID, user_id=USER_ID, origin_client="web")

    assert outcome["processed_document_id"] == DOC_ID
    landing = hook.calls[0]
    assert landing["source_kind"] == "scrape_parsed_page" and landing["source_id"] is None
    assert landing["canonical_identity"] == "https://example.com/widgets"
    assert [p["locator"]["heading_path"] for p in landing["portions"]] == [
        ["Widgets"],
        ["Widgets", "Pricing"],
        ["Widgets", "Pricing", "Bulk"],
    ]
    assert all(p["kind"] == "section" for p in landing["portions"])
    assert landing["structured"]["links"]["internal"] == ["https://example.com/a"]
    assert landing["structured"]["images"][0]["alt"] == "a widget"
    assert landing["structured"]["cms"] == "wordpress"
    assert landing["provenance"] == {
        **landing["provenance"],
        "origin_client": "web",
        "capture_method": "http",
        "user_id": USER_ID,
    }
    assert landing["original"]["mime_type"] == "text/html"
    assert landing["visibility"] == "personal" and landing["keep"] is False


@pytest.mark.asyncio
async def test_a_failed_landing_is_a_notice_on_the_result_never_swallowed(registry: dict[str, Any]) -> None:
    registry["source_landing"] = RecordingHook(
        fail=SourceLandingFailed("attach_target_unreachable", "Nope, not there.", remedy="pick_another")
    )
    outcome = await land_page_result(_result(), organization_id=ORG_ID, user_id=USER_ID, origin_client="web")
    assert outcome["processed_document_id"] is None
    assert outcome["notices"] == [
        {"code": "attach_target_unreachable", "message": "Nope, not there.", "remedy": "pick_another"}
    ]

    registry["source_landing"] = RecordingHook(fail=ConnectionError("socket closed"))
    outcome = await land_page_result(_result(), organization_id=ORG_ID, user_id=USER_ID, origin_client="web")
    assert outcome["processed_document_id"] is None
    assert outcome["notices"][0]["code"] == "source_not_landed"
    assert "ConnectionError" in outcome["notices"][0]["message"]


@pytest.mark.asyncio
async def test_a_request_with_no_person_is_told_why_it_did_not_land(registry: dict[str, Any]) -> None:
    hook = RecordingHook()
    registry["source_landing"] = hook
    outcome = await land_page_result(_result(), organization_id=ORG_ID, user_id=None, origin_client="web")
    assert hook.calls == []
    assert outcome["notices"][0]["code"] == "source_needs_a_person"


# ── /page-capture ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_page_capture_with_no_hook_raises(page_capture_env: dict[str, Any]) -> None:
    request = scrape_router.PageCaptureRequest(url="https://example.com/widgets/", use_cache=False)
    with pytest.raises(SourceLandingNotConfigured):
        await scrape_router.page_capture(request=request, ctx=_ctx())


@pytest.mark.asyncio
async def test_page_capture_with_use_cache_false_still_lands(
    page_capture_env: dict[str, Any], registry: dict[str, Any]
) -> None:
    hook = RecordingHook()
    registry["source_landing"] = hook
    request = scrape_router.PageCaptureRequest(url="https://example.com/widgets/", use_cache=False)

    result = await scrape_router.page_capture(request=request, ctx=_ctx())

    assert page_capture_env["cache"] is None, "use_cache=false must bypass the cache"
    assert len(hook.calls) == 1
    assert result.processed_document_id == DOC_ID
    assert result.notices == []


# ── the streaming service (quick-scrape / search-and-scrape) ──────────────────────────────────


class RecordingEmitter:
    def __init__(self) -> None:
        self.data: list[Any] = []

    async def send_data(self, payload: Any) -> None:
        self.data.append(payload)


@pytest.mark.asyncio
async def test_streamed_pages_land_and_carry_their_source_id(
    monkeypatch: pytest.MonkeyPatch, registry: dict[str, Any]
) -> None:
    from matrx_scraper import service as service_mod

    async def _stream(urls: list[str], **kwargs: Any):
        assert kwargs["cache"] is None
        for _ in urls:
            yield _result()

    monkeypatch.setattr(service_mod, "scrape_many_stream", _stream)
    hook = RecordingHook()
    registry["source_landing"] = hook
    emitter = RecordingEmitter()
    svc = service_mod.ScrapeService(emitter=emitter, organization_id=ORG_ID, acting_user_id=USER_ID)
    svc.urls = ["https://example.com/widgets/"]
    svc.use_cache = False
    svc.land_as = "web"

    await svc.quick_scrape_stream()

    page = emitter.data[0].results[0].model_dump()
    assert page["processed_document_id"] == DOC_ID
    assert page["notices"] == []
    assert hook.calls[0]["provenance"]["origin_client"] == "web"


@pytest.mark.asyncio
async def test_streamed_pages_with_no_hook_raise(monkeypatch: pytest.MonkeyPatch, registry: dict[str, Any]) -> None:
    from matrx_scraper import service as service_mod

    async def _stream(urls: list[str], **kwargs: Any):
        yield _result()

    monkeypatch.setattr(service_mod, "scrape_many_stream", _stream)
    svc = service_mod.ScrapeService(emitter=RecordingEmitter(), organization_id=ORG_ID, acting_user_id=USER_ID)
    svc.urls = ["https://example.com/widgets/"]
    svc.land_as = "web"
    with pytest.raises(SourceLandingNotConfigured):
        await svc.quick_scrape_stream()


def test_every_streaming_scrape_route_lands_as_web() -> None:
    """The three streaming routes that read pages each set ``land_as`` — a route that forgot it
    would be a producer that silently makes no Sources."""
    import inspect

    for fn in (
        scrape_router._run_quick_scrape,
        scrape_router._run_search_and_scrape,
        scrape_router._run_search_and_scrape_limited,
    ):
        assert 'service.land_as = "web"' in inspect.getsource(fn), fn.__name__


# ── /batch and /content/save ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_batch_lands_every_successful_page_with_keep_and_targets(
    monkeypatch: pytest.MonkeyPatch, registry: dict[str, Any]
) -> None:
    async def _many(urls: list[str], **_kwargs: Any) -> list[ScrapeResult]:
        return [_result(), _result(success=False, url="https://example.com/x", response_url="")]

    monkeypatch.setattr(ext_router, "scrape_many", _many)
    hook = RecordingHook()
    registry["source_landing"] = hook
    target = {"entity_type": "project", "entity_id": "22222222-2222-4222-8222-222222222222"}
    request = ext_router.BatchScrapeRequest(urls=["https://example.com/widgets/"], keep=True, attach_to=[target])

    response = await ext_router.batch_scrape(request=request, ctx=_ctx())

    assert response.results[0]["processed_document_id"] == DOC_ID
    assert "processed_document_id" not in response.results[1]
    assert hook.calls[0]["keep"] is True and hook.calls[0]["attach_to"] == [target]


@pytest.mark.asyncio
async def test_batch_with_no_hook_raises(monkeypatch: pytest.MonkeyPatch, registry: dict[str, Any]) -> None:
    async def _many(urls: list[str], **_kwargs: Any) -> list[ScrapeResult]:
        return [_result()]

    monkeypatch.setattr(ext_router, "scrape_many", _many)
    with pytest.raises(SourceLandingNotConfigured):
        await ext_router.batch_scrape(request=ext_router.BatchScrapeRequest(urls=["https://e.com"]), ctx=_ctx())


def _save(**overrides: Any) -> Any:
    fields: dict[str, Any] = {
        "url": "https://example.com/widgets/",
        "page_name": "example_com__widgets",
        "content": {"markdown_renderable": PAGE_MD, "title": "Widgets", "links": {"internal": []}},
    }
    fields.update(overrides)
    return ext_router.ContentSaveRequest(**fields)


@pytest.mark.asyncio
async def test_content_save_lands_desktop_captures_as_local_residential(registry: dict[str, Any]) -> None:
    hook = RecordingHook()
    registry["source_landing"] = hook
    answer = await ext_router.content_save(request=_save(), ctx=_ctx())
    assert answer["processed_document_id"] == DOC_ID and answer["status"] == "saved"
    prov = hook.calls[0]["provenance"]
    assert (prov["origin_client"], prov["capture_method"], prov["user_id"]) == ("local", "residential", USER_ID)
    assert hook.calls[0]["visibility"] == "personal"


@pytest.mark.asyncio
async def test_content_save_from_the_extension_is_own_browser(registry: dict[str, Any]) -> None:
    hook = RecordingHook()
    registry["source_landing"] = hook
    await ext_router.content_save(request=_save(origin_client="extension", keep=True), ctx=_ctx())
    prov = hook.calls[0]["provenance"]
    assert (prov["origin_client"], prov["capture_method"]) == ("extension", "own_browser")
    assert hook.calls[0]["keep"] is True


@pytest.mark.asyncio
async def test_content_save_with_no_hook_raises(registry: dict[str, Any]) -> None:
    with pytest.raises(SourceLandingNotConfigured):
        await ext_router.content_save(request=_save(), ctx=_ctx())


@pytest.mark.asyncio
async def test_content_save_refuses_nobody(registry: dict[str, Any]) -> None:
    from fastapi import HTTPException

    registry["source_landing"] = RecordingHook()
    with pytest.raises(HTTPException) as excinfo:
        await ext_router.content_save(request=_save(), ctx=_ctx(user_id=""))
    assert excinfo.value.status_code == 401


# ── the hosted service's HTTP hook ────────────────────────────────────────────────────────────


class _Resp:
    def __init__(self, status: int, body: dict[str, Any]) -> None:
        self.status_code = status
        self._body = body
        self.text = str(body)

    def json(self) -> dict[str, Any]:
        return self._body


class _Client:
    sent: list[dict[str, Any]] = []
    answer: _Resp = _Resp(201, {"processed_document_id": DOC_ID})

    def __init__(self, *a: Any, **k: Any) -> None:
        pass

    async def __aenter__(self) -> _Client:
        return self

    async def __aexit__(self, *a: Any) -> None:
        return None

    async def post(self, url: str, json: dict[str, Any], headers: dict[str, str]) -> _Resp:
        _Client.sent.append({"url": url, "headers": headers})
        return _Client.answer


def _landing() -> dict[str, Any]:
    return {"organization_id": ORG_ID, "provenance": {"user_id": USER_ID}}


@pytest.mark.asyncio
async def test_http_hook_forwards_the_persons_jwt(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_scraper.server import source_landing_http as mod

    _Client.sent = []
    _Client.answer = _Resp(201, {"processed_document_id": DOC_ID})
    monkeypatch.setattr(mod.httpx, "AsyncClient", _Client)
    monkeypatch.setattr(
        mod, "_context", lambda: SimpleNamespace(token="jwt-abc", metadata={"jwt_claims": {"sub": USER_ID}})
    )
    hook = mod.make_http_landing_hook(aidream_url="https://aidream.test/", service_token="svc")
    assert (await hook(_landing()))["processed_document_id"] == DOC_ID
    sent = _Client.sent[0]
    assert sent["url"] == "https://aidream.test/api/sources/land"
    assert sent["headers"]["Authorization"] == "Bearer jwt-abc"
    assert sent["headers"]["X-Organization-Id"] == ORG_ID
    assert "X-Matrx-User-Id" not in sent["headers"]


@pytest.mark.asyncio
async def test_http_hook_uses_the_bridge_when_there_is_no_login(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_scraper.server import source_landing_http as mod

    _Client.sent = []
    _Client.answer = _Resp(201, {"processed_document_id": DOC_ID})
    monkeypatch.setattr(mod.httpx, "AsyncClient", _Client)
    monkeypatch.setattr(mod, "_context", lambda: SimpleNamespace(token=None, metadata={}))
    hook = mod.make_http_landing_hook(aidream_url="https://aidream.test", service_token="svc")
    await hook(_landing())
    sent = _Client.sent[0]
    assert sent["url"] == "https://aidream.test/api/sources/internal/land"
    assert sent["headers"]["Authorization"] == "Bearer svc"
    assert sent["headers"]["X-Matrx-User-Id"] == USER_ID


@pytest.mark.asyncio
async def test_http_hook_unconfigured_fails_loudly_with_the_remedy(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_scraper.server import source_landing_http as mod

    hook = mod.make_http_landing_hook(aidream_url="", service_token="")
    with pytest.raises(SourceLandingFailed) as excinfo:
        await hook(_landing())
    assert excinfo.value.code == "landing_not_configured"
    assert "AIDREAM_URL" in excinfo.value.remedy


@pytest.mark.asyncio
async def test_http_hook_carries_the_doors_refusal(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_scraper.server import source_landing_http as mod

    # The shape aidream's error handler actually sends: the refusal's fields at the TOP LEVEL
    # beside the envelope (aidream/api/errors.py http_exception_handler), never under `detail`.
    _Client.answer = _Resp(
        403,
        {
            "error": "attach_target_unreachable",
            "code": "attach_target_unreachable",
            "message": "No.",
            "remedy": "pick",
            "retryable": False,
            "user_message": "No.",
            "details": None,
            "request_id": "r1",
        },
    )
    monkeypatch.setattr(mod.httpx, "AsyncClient", _Client)
    monkeypatch.setattr(mod, "_context", lambda: SimpleNamespace(token="jwt", metadata={"jwt_claims": {"sub": USER_ID}}))
    hook = mod.make_http_landing_hook(aidream_url="https://aidream.test", service_token="")
    with pytest.raises(SourceLandingFailed) as excinfo:
        await hook(_landing())
    assert excinfo.value.as_notice() == {"code": "attach_target_unreachable", "message": "No.", "remedy": "pick"}


@pytest.mark.asyncio
async def test_http_hook_still_reads_a_bare_fastapi_refusal(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_scraper.server import source_landing_http as mod

    _Client.answer = _Resp(409, {"detail": {"code": "person_mismatch", "message": "Not you.", "remedy": "sign_in"}})
    monkeypatch.setattr(mod.httpx, "AsyncClient", _Client)
    monkeypatch.setattr(mod, "_context", lambda: SimpleNamespace(token="jwt", metadata={"jwt_claims": {"sub": USER_ID}}))
    hook = mod.make_http_landing_hook(aidream_url="https://aidream.test", service_token="")
    with pytest.raises(SourceLandingFailed) as excinfo:
        await hook(_landing())
    assert excinfo.value.code == "person_mismatch" and excinfo.value.remedy == "sign_in"
