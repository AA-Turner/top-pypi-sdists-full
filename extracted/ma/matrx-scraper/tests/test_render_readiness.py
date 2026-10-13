"""A slow-painting page is waited for, and a blank frame is never accepted quietly.

Real Chromium against a local server whose homepage commits at once but only
paints its content a few seconds later (as a slow WordPress/Elementor site
does). The test fails if the capture fires at DOMContentLoaded.
"""

from __future__ import annotations

import asyncio
import http.server
import threading

import pytest

pytest.importorskip("playwright")

from matrx_scraper.browser_pool import capture_screenshots  # noqa: E402
from matrx_scraper.render_readiness import png_looks_blank, wait_until_painted  # noqa: E402

SLOW_PAGE = b"""<!doctype html><html><head><title>slow</title>
<style>body{margin:0;font:32px sans-serif} #hero{opacity:0;transition:opacity .2s}
#hero.on{opacity:1}</style></head>
<body><div id="nav" style="background:#111;height:40px"></div>
<div id="hero"><h1>Discover our services</h1>
<p>Personalized property search across every agency in Spain, matched to your budget and your preferences, with bank accounts and mortgage services arranged for you.</p></div>
<script>setTimeout(function(){document.getElementById('hero').className='on'}, 3500)</script>
</body></html>"""

BLANK_PAGE = b"<!doctype html><html><body style='background:#fff'></body></html>"


class _Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        body = SLOW_PAGE if self.path == "/slow" else BLANK_PAGE
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # noqa: D401
        return


@pytest.fixture()
def server():
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()


async def _with_page(fn):
    from playwright.async_api import async_playwright

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        try:
            context = await browser.new_context(viewport={"width": 1366, "height": 768})
            page = await context.new_page()
            return await fn(page)
        finally:
            await browser.close()


def test_capture_waits_for_slow_paint_and_is_not_blank(server):
    async def run(page):
        await page.goto(f"{server}/slow", wait_until="commit")
        await page.wait_for_load_state("domcontentloaded")
        shots = await capture_screenshots(page, kinds=["viewport_desktop"])
        text = await page.evaluate("document.getElementById('hero').className")
        return shots[0], text

    shot, hero_class = asyncio.run(_with_page(run))
    assert hero_class == "on", "captured before the content painted"
    assert not png_looks_blank(shot.bytes, shot.width, shot.height)


def test_wait_reports_unready_blank_page_without_raising(server):
    async def run(page):
        await page.goto(f"{server}/blank", wait_until="load")
        return await wait_until_painted(page, max_ms=1500)

    report = asyncio.run(_with_page(run))
    assert report["ready"] is False
    assert report["visible_chars"] == 0


def test_blank_detector_flags_flat_frame_and_not_content(server):
    async def run(page):
        await page.goto(f"{server}/blank", wait_until="load")
        blank = await page.screenshot(type="png")
        await page.goto(f"{server}/slow", wait_until="load")
        await page.wait_for_timeout(4000)
        full = await page.screenshot(type="png")
        return blank, full

    blank, full = asyncio.run(_with_page(run))
    assert png_looks_blank(blank, 1366, 768) is True
    assert png_looks_blank(full, 1366, 768) is False
