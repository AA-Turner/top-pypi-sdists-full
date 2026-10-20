"""`POST /api/scraper/browser-inspect` with inline `html` + `measure_script`.

Two layers, deliberately:
* endpoint tests against a fake pool pin the wire contract (exactly one of url/html,
  fields forwarded, per-capture error shape, no 500s);
* real-Chromium tests pin the thing that matters — a script really runs in the page
  and its JSON comes back per width x theme, and a throwing script is an error
  capture, never an empty result. Skipped only when Chromium is not installed.
Against the old code every test here fails (no `html`, no `captures`).
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from matrx_scraper.inline_inspect import InlineCapture, wrap_html

mod = importlib.import_module("matrx_scraper.api.scrape_router")

_PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8

TWO_TEXTS_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="100">'
    '<text id="a" x="10" y="50" font-size="30">Overlap</text>'
    '<text id="b" x="14" y="52" font-size="30">Overlap</text></svg>'
)


class _FakePool:
    def __init__(self, captures: list[InlineCapture] | None = None, raises: BaseException | None = None):
        self.calls: list[dict[str, Any]] = []
        self._raises = raises
        self._captures = captures or [
            InlineCapture(
                width=1440, theme="light", viewport_height=900,
                measurements={"textCount": 2}, screenshot_png=_PNG, screenshot_width=1, screenshot_height=1,
            )
        ]

    async def inspect_inline(self, html: str, **kwargs: Any):
        self.calls.append({"html": html, **kwargs})
        if self._raises:
            raise self._raises
        return self._captures


def _install(monkeypatch: pytest.MonkeyPatch, pool: Any) -> None:
    import matrx_scraper._ext as ext

    monkeypatch.setattr(ext, "has_ext", lambda name: name == "browser_pool")
    monkeypatch.setattr(ext, "get_ext", lambda name: pool)


@pytest.mark.asyncio
async def test_inline_round_trip_forwards_inputs_and_returns_measurements(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = _FakePool()
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(
        mod.BrowserInspectRequest(
            html=TWO_TEXTS_SVG, measure_script="document.querySelectorAll('text').length",
            widths=[1440], themes=["light"],
        ),
        ctx=None,
    )
    assert result.success is True
    assert pool.calls[0]["measure_script"] == "document.querySelectorAll('text').length"
    assert pool.calls[0]["widths"] == [1440] and pool.calls[0]["themes"] == ["light"]
    (cap,) = result.captures
    assert cap.measurements == {"textCount": 2}
    assert cap.error is None and cap.viewport.w == 1440
    assert cap.screenshot is not None and cap.screenshot.image_base64


@pytest.mark.asyncio
async def test_defaults_are_1440_light(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = _FakePool()
    _install(monkeypatch, pool)
    await mod.browser_inspect(mod.BrowserInspectRequest(html="<svg/>"), ctx=None)
    assert pool.calls[0]["widths"] == [1440] and pool.calls[0]["themes"] == ["light"]


@pytest.mark.asyncio
async def test_a_script_error_reaches_the_caller_as_error_text(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = _FakePool(captures=[InlineCapture(width=800, theme="dark", viewport_height=900, error="measure_script threw: boom")])
    _install(monkeypatch, pool)
    result = await mod.browser_inspect(mod.BrowserInspectRequest(html="<svg/>", measure_script="x"), ctx=None)
    assert result.success is True
    assert result.captures[0].error == "measure_script threw: boom"
    assert result.captures[0].measurements is None


@pytest.mark.asyncio
@pytest.mark.parametrize("body", [{}, {"url": "https://example.com/a", "html": "<svg/>"}])
async def test_exactly_one_of_url_or_html(monkeypatch: pytest.MonkeyPatch, body: dict[str, Any]) -> None:
    from fastapi import HTTPException

    _install(monkeypatch, _FakePool())
    with pytest.raises(HTTPException) as excinfo:
        await mod.browser_inspect(mod.BrowserInspectRequest(**body), ctx=None)
    assert excinfo.value.status_code == 422


@pytest.mark.asyncio
async def test_bad_width_is_a_structured_failure_not_a_500(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch, _FakePool(raises=ValueError("width 10 outside 240..3840")))
    result = await mod.browser_inspect(mod.BrowserInspectRequest(html="<svg/>", widths=[10]), ctx=None)
    assert result.success is False and "width 10" in (result.error or "") and result.retryable is False


def test_request_caps() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        mod.BrowserInspectRequest(html="<svg/>", widths=[400] * (mod.INLINE_MAX_WIDTHS + 1))
    with pytest.raises(ValidationError):
        mod.BrowserInspectRequest(html="<svg/>", themes=["sepia"])


def test_wrap_html_wraps_fragments_and_keeps_documents() -> None:
    assert wrap_html("<svg/>").startswith("<!doctype html>")
    doc = "<!DOCTYPE html><html><body>x</body></html>"
    assert wrap_html(doc) == doc
    assert wrap_html("<html><body>x</body></html>").startswith("<html>")


# --- real Chromium ---------------------------------------------------------------


@pytest.fixture
async def real_pool():
    from matrx_scraper.browser_pool import PlaywrightBrowserPool

    pool = PlaywrightBrowserPool(pool_size=1)
    try:
        await pool.start()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"chromium not available: {exc}")
    try:
        yield pool
    finally:
        await pool.stop()


@pytest.mark.asyncio
async def test_real_browser_runs_the_script_per_width_and_theme(real_pool: Any) -> None:
    script = """
      const boxes = [...document.querySelectorAll('text')].map(t => {
        const r = t.getBoundingClientRect(); return {id: t.id, x: r.x, y: r.y, w: r.width, h: r.height};
      });
      return {textCount: boxes.length, boxes, innerWidth: window.innerWidth,
              dark: matchMedia('(prefers-color-scheme: dark)').matches};
    """
    caps = await real_pool.inspect_inline(
        TWO_TEXTS_SVG, measure_script=script, widths=[400, 1000], themes=["light", "dark"]
    )
    assert [(c.theme, c.width) for c in caps] == [("light", 400), ("light", 1000), ("dark", 400), ("dark", 1000)]
    for cap in caps:
        assert cap.error is None
        assert cap.measurements["textCount"] == 2
        assert cap.measurements["innerWidth"] == cap.width
        assert cap.measurements["dark"] is (cap.theme == "dark")
        assert cap.screenshot_png and cap.screenshot_png.startswith(b"\x89PNG")
    a, b = caps[0].measurements["boxes"]
    # the two <text> elements really overlap — the thing the caller wants to detect
    assert a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and a["y"] < b["y"] + b["h"]


@pytest.mark.asyncio
async def test_real_browser_expression_form_returns_a_count(real_pool: Any) -> None:
    (cap,) = await real_pool.inspect_inline(
        TWO_TEXTS_SVG, measure_script="({textCount: document.querySelectorAll('text').length})",
        widths=[1440], themes=["light"],
    )
    assert cap.measurements == {"textCount": 2} and cap.error is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("script", "needle"),
    [
        ("throw new Error('kaboom')", "kaboom"),
        ("return nonexistentThing.x", "nonexistentThing"),
        ("const a = 1;", "undefined"),
        ("return (() => { const o = {}; o.o = o; return o; })()", "JSON-serialisable"),
        ("this is not javascript (", "does not parse"),
    ],
)
async def test_real_browser_failing_script_is_an_error_capture(real_pool: Any, script: str, needle: str) -> None:
    caps = await real_pool.inspect_inline(
        "<svg/>", measure_script=script, widths=[500, 600], themes=["light"]
    )
    assert len(caps) == 2  # one bad script does not abort the other captures
    for cap in caps:
        assert cap.measurements is None
        assert cap.error and needle in cap.error
