"""`POST /api/scraper/browser-fetch` — the stateless one-shot render.

This endpoint hands any authenticated caller an arbitrary-URL, JS-executing
fetch from INSIDE the scraper network, so its guards are the contract:
publicly-routable targets only, the FINAL url re-validated after the browser
follows redirects (with the body withheld when it isn't public), a bounded
response, and a structured result instead of a 500 on any failure.
"""

from __future__ import annotations

from typing import Any

import pytest

# `matrx_scraper.api.__init__` rebinds the name `scrape_router` to the router
# OBJECT, so a plain `import ... as mod` yields an APIRouter. Reach the module.
import importlib

mod = importlib.import_module("matrx_scraper.api.scrape_router")


class _FakePool:
    """Records what was navigated and returns a canned response."""

    def __init__(self, *, final_url: str | None = None, html: str = "<html><body>ok</body></html>"):
        self.calls: list[dict[str, Any]] = []
        self._final_url = final_url
        self._html = html

    async def fetch(self, url: str, proxy: str | None = None, timeout_ms: int = 30_000):
        self.calls.append({"url": url, "proxy": proxy, "timeout_ms": timeout_ms})
        return (
            self._html,
            self._final_url or url,
            200,
            {"content-type": "text/html; charset=utf-8"},
            "Title",
        )


def _install(monkeypatch: pytest.MonkeyPatch, pool: Any, *, allow: set[str] | None = None) -> None:
    """Wire the ext registry + SSRF validator for a test."""
    import matrx_scraper._ext as ext
    import matrx_scraper.utils.url as url_mod

    monkeypatch.setattr(ext, "has_ext", lambda name: name == "browser_pool")
    monkeypatch.setattr(ext, "get_ext", lambda name: pool)

    async def fake_validate(url: str) -> str:
        if allow is not None and url not in allow:
            raise ValueError("URL host resolves to a non-public IP address: h (10.1.2.3)")
        return url

    monkeypatch.setattr(url_mod, "validate_public_http_url", fake_validate)
    monkeypatch.setattr("matrx_scraper.scraper.get_required_random_proxy", lambda: "http://p:1")


@pytest.mark.asyncio
async def test_public_url_renders_and_returns_html(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = _FakePool()
    _install(monkeypatch, pool)
    result = await mod.browser_fetch(mod.BrowserFetchRequest(url="https://example.com/a"), ctx=None)
    assert result.success is True
    assert result.status_code == 200
    assert "ok" in result.html
    assert result.truncated is False
    # Proxy is ON by default — a rescue must not egress from the scraper's own IP.
    assert pool.calls[0]["proxy"] == "http://p:1"


@pytest.mark.asyncio
async def test_non_public_target_is_rejected_without_leaking_the_address(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from fastapi import HTTPException

    pool = _FakePool()
    _install(monkeypatch, pool, allow=set())
    with pytest.raises(HTTPException) as excinfo:
        await mod.browser_fetch(
            mod.BrowserFetchRequest(url="http://169.254.169.254/latest/meta-data/"), ctx=None
        )
    assert excinfo.value.status_code == 422
    # The validator names the resolved internal IP; echoing it turns this
    # endpoint into an internal-network resolution oracle.
    assert "10.1.2.3" not in str(excinfo.value.detail)
    assert not pool.calls, "a rejected target must never be navigated"


@pytest.mark.asyncio
async def test_redirect_to_internal_host_discards_the_body(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The browser follows redirects AFTER validation — the rendered internal
    page must never be returned to the caller."""
    pool = _FakePool(
        final_url="http://169.254.169.254/latest/meta-data/",
        html="<html><body>SECRET credentials</body></html>",
    )
    _install(monkeypatch, pool, allow={"https://public.example.com/r"})
    result = await mod.browser_fetch(
        mod.BrowserFetchRequest(url="https://public.example.com/r"), ctx=None
    )
    assert result.success is False
    assert "SECRET" not in result.html and result.html == ""
    assert "non-public" in (result.error or "")
    # The internal host is not echoed back either.
    assert "169.254.169.254" not in result.final_url


@pytest.mark.asyncio
async def test_oversized_html_is_truncated(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = _FakePool(html="x" * (mod.BROWSER_FETCH_MAX_HTML_CHARS + 5_000))
    _install(monkeypatch, pool)
    result = await mod.browser_fetch(
        mod.BrowserFetchRequest(url="https://example.com/big"), ctx=None
    )
    assert result.truncated is True
    assert len(result.html) == mod.BROWSER_FETCH_MAX_HTML_CHARS


@pytest.mark.asyncio
async def test_missing_proxy_pool_returns_a_result_not_a_500(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.scraper import ProxyConfigurationError

    pool = _FakePool()
    _install(monkeypatch, pool)

    def no_proxies() -> str:
        raise ProxyConfigurationError("DATACENTER_PROXIES is missing or empty")

    monkeypatch.setattr("matrx_scraper.scraper.get_required_random_proxy", no_proxies)
    result = await mod.browser_fetch(
        mod.BrowserFetchRequest(url="https://example.com/a", use_proxy=True), ctx=None
    )
    assert result.success is False
    assert "proxy unavailable" in (result.error or "")


@pytest.mark.asyncio
async def test_render_exception_returns_a_result_not_a_500(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ExplodingPool:
        async def fetch(self, *args: Any, **kwargs: Any):
            raise TimeoutError("navigation timed out")

    _install(monkeypatch, ExplodingPool())
    result = await mod.browser_fetch(mod.BrowserFetchRequest(url="https://example.com/a"), ctx=None)
    assert result.success is False
    assert "TimeoutError" in (result.error or "")


@pytest.mark.asyncio
async def test_no_browser_pool_is_503(monkeypatch: pytest.MonkeyPatch) -> None:
    from fastapi import HTTPException

    import matrx_scraper._ext as ext

    monkeypatch.setattr(ext, "has_ext", lambda name: False)
    with pytest.raises(HTTPException) as excinfo:
        await mod.browser_fetch(mod.BrowserFetchRequest(url="https://example.com/a"), ctx=None)
    assert excinfo.value.status_code == 503


def test_caller_cannot_hold_a_pooled_browser_indefinitely() -> None:
    """The timeout ceiling is the starvation guard: 5 pooled browsers are
    shared with live crawls, so a caller-controlled long timeout is a lever."""
    import pydantic

    assert mod.BrowserFetchRequest(url="https://x.test").timeout_ms <= 30_000
    with pytest.raises(pydantic.ValidationError):
        mod.BrowserFetchRequest(url="https://x.test", timeout_ms=120_000)
