"""`POST /api/scraper/browser-inspect` — the stateless render CHECK.

Same threat surface as `/browser-fetch` (an arbitrary-URL, JS-executing
navigation from INSIDE the scraper network) plus pixels, so it carries the same
contract: publicly-routable targets only, the FINAL url re-validated after the
browser follows redirects with the WHOLE result withheld when it isn't public,
and a structured `success=false` instead of a 500 on any failure.

It also pins the two things that make it worth a third endpoint at all: the
console/failed-request evidence reaches the caller, and the caller's device
identity (`user_agent_suffix`) is passed through rather than dropped.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from matrx_scraper.browser_pool import (
    BrowserInspectTimeout,
    CapturedScreenshot,
    PageInspection,
    ScreenshotCaptureFailure,
)

# `matrx_scraper.api.__init__` rebinds the name `scrape_router` to the router
# OBJECT, so a plain `import ... as mod` yields an APIRouter. Reach the module.
mod = importlib.import_module("matrx_scraper.api.scrape_router")

_PNG = b"\x89PNG\r\n\x1a\nfake"


class _FakePool:
    """Records the inspect call and returns a canned inspection."""

    def __init__(self, *, result: Any = None, raises: BaseException | None = None):
        self.calls: list[dict[str, Any]] = []
        self._raises = raises
        self._result = result or PageInspection(
            http_status=200,
            final_url="https://example.com/a",
            title="Title",
            console_errors=["Uncaught: Error: boom"],
            failed_requests=["GET https://cdn/x.js — net::ERR_ABORTED"],
            dom_text_found=True,
            dom_selector_found=False,
            screenshots=[
                CapturedScreenshot(kind="viewport_desktop", width=1440, height=900, bytes=_PNG)
            ],
            screenshot_failures=[
                ScreenshotCaptureFailure(
                    kind="viewport_mobile", error_class="TimeoutError", error_message="slow"
                )
            ],
        )

    async def inspect_url(self, url: str, **kwargs: Any):
        self.calls.append({"url": url, **kwargs})
        if self._raises is not None:
            raise self._raises
        return self._result


def _install(monkeypatch: pytest.MonkeyPatch, pool: Any, *, allow: set[str] | None = None) -> None:
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
async def test_returns_the_render_evidence_the_other_endpoints_cannot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The console/pageerror + failed-request streams are the whole reason this
    endpoint exists — neither /browser-fetch nor /browser/* exposes them."""
    pool = _FakePool()
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(
            url="https://example.com/a",
            kinds=["viewport_desktop"],
            expect_text="hello",
            expect_selector="#nope",
        ),
        ctx=None,
    )
    assert result.success is True
    assert result.http_status == 200
    assert result.console_errors == ["Uncaught: Error: boom"]
    assert result.failed_requests == ["GET https://cdn/x.js — net::ERR_ABORTED"]
    assert result.expect_text_found is True
    assert result.expect_selector_found is False
    assert [(s.kind, s.width) for s in result.screenshots] == [("viewport_desktop", 1440)]
    # A dropped frame is missing EVIDENCE — it must reach the caller, not a log.
    assert [f.kind for f in result.screenshot_failures] == ["viewport_mobile"]


@pytest.mark.asyncio
async def test_proxy_is_off_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unlike /browser-fetch: a render check targets a site the caller owns."""
    pool = _FakePool()
    _install(monkeypatch, pool)
    await mod.browser_inspect(mod.BrowserInspectRequest(url="https://example.com/a"), ctx=None)
    assert pool.calls[0]["proxy"] is None


@pytest.mark.asyncio
async def test_user_agent_suffix_is_forwarded(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = _FakePool()
    _install(monkeypatch, pool)
    await mod.browser_inspect(
        mod.BrowserInspectRequest(url="https://example.com/a", user_agent_suffix="Bot/1.0"),
        ctx=None,
    )
    assert pool.calls[0]["user_agent_suffix"] == "Bot/1.0"


@pytest.mark.asyncio
async def test_non_public_target_is_rejected_without_leaking_the_address(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from fastapi import HTTPException

    pool = _FakePool()
    _install(monkeypatch, pool, allow=set())
    with pytest.raises(HTTPException) as excinfo:
        await mod.browser_inspect(mod.BrowserInspectRequest(url="http://10.1.2.3/admin"), ctx=None)
    assert excinfo.value.status_code == 422
    assert "10.1.2.3" not in str(excinfo.value.detail)
    assert not pool.calls


@pytest.mark.asyncio
async def test_redirect_onto_a_private_host_discards_everything(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The browser follows redirects, so the page actually rendered may be
    internal. By then we hold its pixels AND its DOM answers — withhold all."""
    pool = _FakePool(
        result=PageInspection(
            http_status=200,
            final_url="http://169.254.169.254/latest/meta-data",
            title="secrets",
            console_errors=["leak"],
            dom_text_found=True,
            screenshots=[
                CapturedScreenshot(kind="viewport_desktop", width=1, height=1, bytes=_PNG)
            ],
        )
    )
    _install(monkeypatch, pool, allow={"https://example.com/a"})
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(url="https://example.com/a", kinds=["viewport_desktop"]),
        ctx=None,
    )
    assert result.success is False
    assert result.screenshots == []
    assert result.console_errors == []
    assert result.title == ""
    assert "169.254" not in (result.error or "") and "169.254" not in result.final_url


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("raises", "expect_retryable"),
    [
        (BrowserInspectTimeout("budget blown"), True),
        (ValueError("unknown screenshot kind: 'nope'"), False),
        (RuntimeError("chromium exploded"), True),
    ],
)
async def test_a_render_failure_never_500s(
    monkeypatch: pytest.MonkeyPatch, raises: BaseException, expect_retryable: bool
) -> None:
    pool = _FakePool(raises=raises)
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(url="https://example.com/a"), ctx=None
    )
    assert result.success is False
    assert result.error
    assert result.retryable is expect_retryable


@pytest.mark.asyncio
async def test_no_browser_pool_is_a_503(monkeypatch: pytest.MonkeyPatch) -> None:
    from fastapi import HTTPException

    import matrx_scraper._ext as ext

    monkeypatch.setattr(ext, "has_ext", lambda name: False)
    with pytest.raises(HTTPException) as excinfo:
        await mod.browser_inspect(mod.BrowserInspectRequest(url="https://example.com/a"), ctx=None)
    assert excinfo.value.status_code == 503


def test_kinds_are_capped() -> None:
    """Every device profile in `kinds` costs its own navigation and its own
    hold on a pooled browser shared with live crawls."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        mod.BrowserInspectRequest(
            url="https://example.com/a",
            kinds=["viewport_desktop"] * (mod.BROWSER_INSPECT_MAX_KINDS + 1),
        )
