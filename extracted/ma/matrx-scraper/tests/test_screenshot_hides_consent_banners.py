"""A cookie / consent banner is hidden (never clicked) before the homepage screenshot. Real Chromium, local page."""

from __future__ import annotations

import asyncio

import pytest

pw = pytest.importorskip("playwright.async_api")

PAGE = """<html><body style="margin:0;overflow:hidden"><h1>Brand</h1>
<div id="onetrust-banner-sdk" style="position:fixed;bottom:0;left:0;right:0;height:120px">Cookies <button id="accept">Accept</button></div>
<div style="position:fixed;top:0;left:0;width:400px;height:80px" id="unnamed">We use cookies to improve your experience. <a href="#">Learn</a><button>OK</button></div>
<nav style="position:fixed;top:100px;width:300px;height:40px"><a href="/">Home</a></nav>
</body></html>"""


def test_banners_hidden_not_clicked_nav_kept():
    from matrx_scraper.browser_pool import hide_consent_overlays

    async def run():
        async with pw.async_playwright() as p:
            try:
                browser = await p.chromium.launch()
            except Exception as exc:  # noqa: BLE001
                pytest.skip(f"no chromium: {exc}")
            page = await browser.new_page()
            await page.set_content(PAGE)
            await page.evaluate("() => { window.__clicked = false; document.getElementById('accept').addEventListener('click', () => { window.__clicked = true; }); }")
            n = await hide_consent_overlays(page)
            state = await page.evaluate("""() => ({
              known: getComputedStyle(document.getElementById('onetrust-banner-sdk')).display,
              unnamed: getComputedStyle(document.getElementById('unnamed')).display,
              nav: getComputedStyle(document.querySelector('nav')).display,
              clicked: window.__clicked, overflow: getComputedStyle(document.body).overflow})""")
            await browser.close()
            return n, state

    n, state = asyncio.run(run())
    assert n == 2
    assert state == {"known": "none", "unnamed": "none", "nav": "block", "clicked": False, "overflow": "auto"}
