"""Guards for the 2026-09-17 acquisition-frontier block hunt.

Every test here fails on the code as it stood that morning. They pin four
things the hunt proved were missing, each as a POLICY at the level every
caller inherits rather than as a property of one endpoint:

1. `orchestrator.scrape()` hands a failed HTTP fetch to the server browser,
   resolving the browser pool from the ext registry — the exact gap that made
   the capability present and unreachable.
2. A result with no content in it is never a success, and a page served for a
   different resource than was asked for is named (the Pinterest decoy).
3. A proxy pool that REFUSES to carry a request is our outage, not the site's
   wall: the request is retried directly, announced, and remembered.
4. A missing OCR engine is a named deployment fact, not a per-document error.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper import _ext, content_sanity, escalation, orchestrator, proxy_health, scraper


# ─────────────────────────── helpers ───────────────────────────


def _result(
    *,
    url: str = "https://example.com/page",
    response_url: str | None = None,
    success: bool = True,
    text: str = "",
    content_type: str = "html",
    failure_reason: str | None = None,
) -> orchestrator.ScrapeResult:
    return orchestrator.ScrapeResult(
        url=url,
        response_url=response_url or url,
        success=success,
        content_type=content_type,
        text_data=text or None,
        failure_reason=failure_reason,
    )


class _Pool:
    """A server browser that returns real, rendered content."""

    def __init__(self, html: str = "<html><body>" + ("listing " * 400) + "</body></html>"):
        self.html = html
        self.calls: list[str] = []

    async def fetch(self, url: str, **_kwargs: Any):
        self.calls.append(url)
        return self.html, url, 200, {"content-type": "text/html"}, "Rendered"


@pytest.fixture(autouse=True)
def _isolate(monkeypatch: pytest.MonkeyPatch):
    proxy_health.reset_for_tests()
    monkeypatch.delenv("SCRAPER_BROWSER_ESCALATION", raising=False)
    monkeypatch.delenv("SCRAPER_DIRECT_FALLBACK", raising=False)
    yield
    proxy_health.reset_for_tests()


def _patch_http(monkeypatch: pytest.MonkeyPatch, result: orchestrator.ScrapeResult) -> None:
    """Make the plain HTTP path produce `result`, leaving the browser path real."""

    async def _fetch(url, request_type=scraper.RequestType.NORMAL, proxy=None, **_kw):
        return SimpleNamespace(request_url=url, response_url=url, failed=not result.success)

    monkeypatch.setattr(orchestrator, "fetch", _fetch)
    real_build = orchestrator._build_result_from_response

    def _build(response, fast):
        # The BROWSER leg goes through the REAL parser — the whole point is
        # that a rendered page produces genuinely more content than the stub.
        if getattr(response, "request_type", None) == scraper.RequestType.BROWSER:
            return real_build(response, fast)
        return result

    monkeypatch.setattr(orchestrator, "_build_result_from_response", _build)


# ───────────────── 1. the hand-off every caller inherits ─────────────────


@pytest.mark.asyncio
async def test_blocked_http_scrape_hands_off_to_the_server_browser(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Zillow: `bad_status` for the HTTP client, 1,061 listings for the browser.

    Before this guard, `orchestrator.scrape()` returned the failure and a human
    had to know the browser existed and reach for it by hand.
    """
    blocked = _result(success=False, failure_reason="bad_status")
    _patch_http(monkeypatch, blocked)
    pool = _Pool()

    got = await orchestrator.scrape(
        "https://example.com/page", use_proxy=False, browser_pool=pool
    )

    assert pool.calls == ["https://example.com/page"], "the browser was never asked"
    assert got.success is True
    assert got.engine == escalation.ENGINE_BROWSER
    assert got.escalated is True
    assert got.escalation_reason == "bad_status"
    # Announced, never silent — and in words a non-technical person can read.
    assert got.escalation_note and "server browser" in got.escalation_note


@pytest.mark.asyncio
async def test_hand_off_resolves_the_browser_pool_from_the_ext_registry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """THE root cause: `ScrapeService` never passed a `browser_pool`, so the
    general path had nothing to hand off to while the same process had a fully
    wired pool the crawler used all day."""
    _patch_http(monkeypatch, _result(success=False, failure_reason="cloudflare_block"))
    pool = _Pool()
    monkeypatch.setitem(_ext._registry, "browser_pool", pool)
    # No delay in the test: the cloudflare path takes one cheap retry first.
    monkeypatch.setattr(orchestrator, "CHALLENGE_RETRY_DELAY_SECONDS", 0)

    got = await orchestrator.scrape("https://example.com/page", use_proxy=False)

    assert pool.calls, "the registered browser pool was never used"
    assert got.escalated is True


@pytest.mark.asyncio
async def test_escalation_can_be_turned_off_by_setting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_http(monkeypatch, _result(success=False, failure_reason="bad_status"))
    pool = _Pool()
    monkeypatch.setenv("SCRAPER_BROWSER_ESCALATION", "0")

    got = await orchestrator.scrape(
        "https://example.com/page", use_proxy=False, browser_pool=pool
    )

    assert pool.calls == []
    assert got.escalated is False
    assert got.engine == escalation.ENGINE_HTTP


@pytest.mark.asyncio
async def test_escalation_never_spends_a_browser_on_a_pdf(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_http(
        monkeypatch,
        _result(success=False, failure_reason="bad_status", content_type="pdf"),
    )
    pool = _Pool()

    await orchestrator.scrape("https://example.com/a.pdf", use_proxy=False, browser_pool=pool)

    assert pool.calls == []


@pytest.mark.asyncio
async def test_a_browser_result_that_is_not_better_never_overwrites_the_answer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """NYT answered 403 to BOTH engines. The honest outcome is the site's wall,
    plus a statement that we tried the browser too — never a fabricated win."""
    _patch_http(monkeypatch, _result(success=False, failure_reason="bad_status"))
    pool = _Pool(html="<html><body></body></html>")

    got = await orchestrator.scrape(
        "https://example.com/page", use_proxy=False, browser_pool=pool
    )

    assert pool.calls, "the browser should still have been tried"
    assert got.success is False
    assert got.escalated is False
    assert got.escalation_note and "did not return more content" in got.escalation_note


@pytest.mark.asyncio
async def test_a_host_with_no_browser_says_so_instead_of_failing_silently(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_http(monkeypatch, _result(success=False, failure_reason="bad_status"))
    monkeypatch.delitem(_ext._registry, "browser_pool", raising=False)
    monkeypatch.setattr("matrx_scraper.browser_pool.PLAYWRIGHT_AVAILABLE", False)

    got = await orchestrator.scrape("https://example.com/page", use_proxy=False)

    assert got.escalation_reason == "bad_status"
    assert got.escalation_note and "no browser available" in got.escalation_note


# ───────────────── 2. the content-sanity gate ─────────────────


def test_a_successful_scrape_with_no_text_is_not_a_success() -> None:
    """arXiv's own PDF and a real SCOTUS opinion both came back "success",
    "Untitled Page", 0 characters, with no error shown to the user."""
    verdict = content_sanity.assess(_result(text=""))
    assert verdict.failure_reason == content_sanity.EMPTY_CONTENT
    assert verdict.message and "could not read any text" in verdict.message


def test_content_served_for_a_different_resource_is_named() -> None:
    """Pinterest answered a request for @abeautifulmess with goldencoveco's
    empty profile — a wrong answer dressed as a success."""
    verdict = content_sanity.assess(
        _result(
            url="https://www.pinterest.com/abeautifulmess/",
            response_url="https://www.pinterest.com/goldencoveco/",
            text="",
        )
    )
    assert verdict.failure_reason == content_sanity.WRONG_RESOURCE
    assert verdict.redirected_off_requested_path is True


@pytest.mark.parametrize(
    ("requested", "landed"),
    [
        ("http://example.com/a", "https://example.com/a"),
        ("https://example.com/a", "https://www.example.com/a/"),
        ("https://example.com/A", "https://example.com/a"),
    ],
)
def test_ordinary_url_normalisation_is_never_called_a_different_resource(
    requested: str, landed: str
) -> None:
    assert content_sanity.resource_changed(requested, landed) is False


def test_a_thin_page_is_flagged_but_not_failed() -> None:
    verdict = content_sanity.assess(_result(text="Loading..."))
    assert verdict.failure_reason is None
    assert verdict.warning == content_sanity.THIN_CONTENT


@pytest.mark.asyncio
async def test_the_gate_applies_to_every_caller_of_scrape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_http(monkeypatch, _result(success=True, text=""))
    monkeypatch.delitem(_ext._registry, "browser_pool", raising=False)
    monkeypatch.setattr("matrx_scraper.browser_pool.PLAYWRIGHT_AVAILABLE", False)

    got = await orchestrator.scrape("https://example.com/page", use_proxy=False)

    assert got.success is False
    assert got.failure_reason == content_sanity.EMPTY_CONTENT
    assert got.failure_message, "a screen must have plain English to show"


# ───────────────── 3. the proxy pool is ours, not the site's ─────────────────


def _failed(reason: scraper.FailureReason) -> SimpleNamespace:
    return SimpleNamespace(
        failed=True, failed_primary_reason=reason, failed_reasons=[{reason: "failed"}]
    )


def _ok() -> SimpleNamespace:
    return SimpleNamespace(failed=False, failed_primary_reason=None, failed_reasons=[])


@pytest.mark.asyncio
async def test_a_pool_that_refuses_every_proxy_falls_back_to_a_direct_fetch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`CONNECT tunnel failed, response 403` on SEC EDGAR, the FDA, OSHA, the
    IRS, eCFR, PubMed and docs.stripe.com is our vendor declining the
    destination. Those sites were reachable the whole time."""
    seen: list[str | None] = []

    async def fake_fetch(url, request_type, proxy=None, **_kw):
        seen.append(proxy)
        return _ok() if proxy is None else _failed(scraper.FailureReason.PROXY_ERROR)

    monkeypatch.setenv("DATACENTER_PROXIES", "http://p1,http://p2")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr("matrx_utils.vcprint", lambda *a, **k: None)

    response = await scraper.fetch_normally_with_proxy("https://www.sec.gov/edgar")

    assert seen == ["http://p1", "http://p2", None]
    assert response.failed is False
    assert response.proxy_bypassed is True, "a bypass must never be silent"


@pytest.mark.asyncio
async def test_a_refused_host_is_remembered_and_tried_directly_first(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[str | None] = []

    async def fake_fetch(url, request_type, proxy=None, **_kw):
        seen.append(proxy)
        return _ok() if proxy is None else _failed(scraper.FailureReason.PROXY_ERROR)

    monkeypatch.setenv("DATACENTER_PROXIES", "http://p1,http://p2")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr("matrx_utils.vcprint", lambda *a, **k: None)

    await scraper.fetch_normally_with_proxy("https://www.sec.gov/edgar")
    seen.clear()
    await scraper.fetch_normally_with_proxy("https://www.sec.gov/another")

    assert seen == [None], "a known-refused host must not pay for the pool again"


@pytest.mark.asyncio
async def test_a_site_that_rejects_us_is_never_retried_directly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The surviving half of the old proxy-only rule: a wall the SITE put up is
    the site's answer, and must not become a reason to expose our host IP."""
    seen: list[str | None] = []

    async def fake_fetch(url, request_type, proxy=None, **_kw):
        seen.append(proxy)
        return _failed(scraper.FailureReason.BAD_STATUS)

    monkeypatch.setenv("DATACENTER_PROXIES", "http://p1,http://p2")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr("matrx_utils.vcprint", lambda *a, **k: None)

    await scraper.fetch_normally_with_proxy("https://example.com")

    assert None not in seen


@pytest.mark.asyncio
async def test_direct_fallback_can_be_turned_off(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[str | None] = []

    async def fake_fetch(url, request_type, proxy=None, **_kw):
        seen.append(proxy)
        return _failed(scraper.FailureReason.PROXY_ERROR)

    monkeypatch.setenv("DATACENTER_PROXIES", "http://p1")
    monkeypatch.setenv("SCRAPER_DIRECT_FALLBACK", "0")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr("matrx_utils.vcprint", lambda *a, **k: None)
    monkeypatch.setattr("matrx_utils.capture_error", _noop_capture)

    await scraper.fetch_normally_with_proxy("https://example.com")

    assert None not in seen


async def _noop_capture(*_a: Any, **_k: Any) -> None:
    return None


def test_proxy_health_publishes_the_signal_that_was_missing() -> None:
    proxy_health.record_attempt(proxied=True)
    proxy_health.record_proxy_refusal("https://www.osha.gov/laws-regs", "proxy_error")
    proxy_health.record_direct_fallback(rescued=True)

    snapshot = proxy_health.proxy_health_snapshot()

    assert snapshot["proxy_refusals"] == 1
    assert snapshot["direct_fallback_rescues"] == 1
    assert snapshot["refused_hosts"] == ["www.osha.gov"]
    # Never a proxy URL: those carry the vendor username and password.
    assert all("@" not in host for host in snapshot["refused_hosts"])


# ───────────────── 4. OCR is a host capability, not a document property ─────


def test_ocr_availability_is_decided_by_the_ENGINE_not_the_import(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The production image had `pytesseract` and no `tesseract` binary, so an
    import check said OCR was available and every scanned PDF died with a raw
    `TesseractNotFoundError`."""
    import pytesseract

    from matrx_scraper import ocr_health

    def _boom():
        raise pytesseract.TesseractNotFoundError()

    monkeypatch.setattr(pytesseract, "get_tesseract_version", _boom)
    status = ocr_health.ocr_status(refresh=True)
    try:
        assert status.available is False
        assert status.reason and "tesseract" in status.reason.lower()
        assert "PATH" in status.reason or "path" in status.reason
    finally:
        ocr_health.ocr_status(refresh=True)


def test_a_scanned_pdf_on_an_ocr_less_host_blames_the_host_not_the_document(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper import extractors, ocr_health

    monkeypatch.setattr(
        ocr_health,
        "ocr_status",
        lambda refresh=False: ocr_health.OcrStatus(
            available=False, reason="the tesseract OCR engine binary is missing"
        ),
    )
    monkeypatch.setattr(extractors, "ocr_status", ocr_health.ocr_status)
    monkeypatch.setattr(
        "matrx_files.specific_handlers.pdf_handler.extract_text_from_pdf_bytes_sync",
        lambda _bytes, force_ocr=False, use_ocr_threshold=0: "",
    )

    text, reason = extractors.extract_text_from_pdf_bytes_or_reason(b"%PDF-1.4")

    assert text is None
    assert reason and "this host cannot OCR it" in reason


@pytest.mark.asyncio
async def test_the_browser_leg_skips_a_proxy_the_pool_already_refused() -> None:
    """Found by the 60-URL battery itself: the HTTP leg was rescued by going
    direct, then the browser leg navigated through the SAME refused proxy and
    died with `net::ERR_TUNNEL_CONNECTION_FAILED` — our own outage defeating
    our own rescue."""
    blocked = _result(success=False, failure_reason="bad_status")
    blocked.proxy_bypassed = True
    seen: list[str | None] = []

    class _RecordingPool(_Pool):
        async def fetch(self, url: str, **kwargs: Any):
            seen.append(kwargs.get("proxy"))
            return await super().fetch(url, **kwargs)

    got = await orchestrator._maybe_escalate_to_browser(
        blocked,
        url="https://www.sec.gov/edgar",
        use_proxy=True,
        fast=False,
        browser_pool=_RecordingPool(),
        user_agent=None,
        escalate=True,
    )

    assert seen == [None], "the browser must not re-enter a refused tunnel"
    assert got.escalated is True


@pytest.mark.asyncio
async def test_the_browser_leg_still_uses_the_proxy_when_the_pool_is_healthy() -> None:
    """The skip is narrow: only a REFUSED destination goes direct. Everything
    else keeps the proxy, or this fix would quietly retire the proxy policy."""
    blocked = _result(success=False, failure_reason="bad_status")
    seen: list[str | None] = []

    class _RecordingPool(_Pool):
        async def fetch(self, url: str, **kwargs: Any):
            seen.append(kwargs.get("proxy"))
            return await super().fetch(url, **kwargs)

    import os

    os.environ["DATACENTER_PROXIES"] = "http://p1"
    try:
        await orchestrator._maybe_escalate_to_browser(
            blocked,
            url="https://example.com/page",
            use_proxy=True,
            fast=False,
            browser_pool=_RecordingPool(),
            user_agent=None,
            escalate=True,
        )
    finally:
        os.environ.pop("DATACENTER_PROXIES", None)

    assert seen == ["http://p1"]
