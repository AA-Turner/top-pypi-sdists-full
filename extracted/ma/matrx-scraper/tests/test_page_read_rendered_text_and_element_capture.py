"""F4 (get_element returned CSS + run-together cells) and F12 (screenshot ignored selector).

Both fixes live in ``ai_browser/page_read.py``; the first group needs no browser binary
(fake handles), the second runs real Chromium and skips without one.
"""

from __future__ import annotations

import importlib
import struct

import pytest

page_read = importlib.import_module("matrx_scraper.ai_browser.page_read")

INFOBOX = """
<html><body><p>Intro paragraph that fills the viewport width.</p>
<table class="infobox"><style>.infobox{color:red} .x{display:none}</style>
<tr><th>Founded</th><td>2021</td></tr>
<tr><th>Headquarters</th><td>San Francisco</td></tr></table>
<div style="height:2000px"></div></body></html>
"""


class _Handle:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def inner_text(self) -> str:
        self.calls.append("inner_text")
        return "Founded\t2021\nHeadquarters\tSan Francisco"

    async def text_content(self) -> str:  # the flawed reader: must never be used
        self.calls.append("text_content")
        return ".infobox{color:red}FoundedHeadquarters"

    async def screenshot(self, **_: object) -> bytes:
        self.calls.append("element.screenshot")
        return b"ELEMENT"


class _Page:
    def __init__(self, handle: _Handle | None) -> None:
        self.handle = handle
        self.shots: list[dict] = []

    async def query_selector(self, selector: str):
        return self.handle

    async def screenshot(self, **kw: object) -> bytes:
        self.shots.append(kw)
        return b"VIEWPORT"


@pytest.mark.asyncio
async def test_element_text_is_rendered_text_not_text_content() -> None:
    h = _Handle()
    text = await page_read.element_text(h)
    assert "color:red" not in text
    assert "Founded\t2021" in text
    assert h.calls == ["inner_text"]


@pytest.mark.asyncio
async def test_capture_with_selector_shoots_the_element_not_the_viewport() -> None:
    h = _Handle()
    page = _Page(h)
    assert await page_read.capture_png(page, selector="table.infobox") == b"ELEMENT"
    assert page.shots == []


@pytest.mark.asyncio
async def test_capture_with_unmatched_selector_raises_naming_it() -> None:
    page = _Page(None)
    with pytest.raises(page_read.SelectorNotFound, match=r"table\.nope"):
        await page_read.capture_png(page, selector="table.nope")
    assert page.shots == [], "must never fall back to a viewport shot"


@pytest.mark.asyncio
async def test_capture_without_selector_is_the_page() -> None:
    page = _Page(_Handle())
    assert await page_read.capture_png(page, full_page=True) == b"VIEWPORT"
    assert page.shots == [{"type": "png", "full_page": True}]


def _png_size(png: bytes) -> tuple[int, int]:
    return struct.unpack(">II", png[16:24])


@pytest.fixture
async def real_page():
    pytest.importorskip("playwright", reason="playwright not installed (browser extra)")
    from playwright.async_api import async_playwright

    async with async_playwright() as pw:
        try:
            browser = await pw.chromium.launch()
        except Exception as exc:  # pragma: no cover - environment probe
            pytest.skip(f"no chromium browser binary: {exc}")
        page = await browser.new_page(viewport={"width": 800, "height": 600})
        await page.set_content(INFOBOX)
        yield page
        await browser.close()


@pytest.mark.asyncio
async def test_real_chromium_infobox_text_and_element_screenshot(real_page) -> None:
    el = await real_page.query_selector("table.infobox")
    text = await page_read.element_text(el)
    assert "color:red" not in text
    assert "Founded" in text and "2021" in text
    assert "Founded2021" not in text, "cells must be separated"

    full = await page_read.capture_png(real_page)
    only = await page_read.capture_png(real_page, selector="table.infobox")
    assert _png_size(full) == (800, 600)
    w, h = _png_size(only)
    assert w < 800 and h < 600, "selector image must be the element only"
    with pytest.raises(page_read.SelectorNotFound, match="table.missing"):
        await page_read.capture_png(real_page, selector="table.missing")
