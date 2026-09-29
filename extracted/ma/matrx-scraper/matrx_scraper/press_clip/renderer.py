"""Render a live article into a press clip: PDF + preview + page rasters (no model).

A port of newsjack ``skills/press-clip/clip.mjs`` @092d882, in its order:

1. block ad / recirculation / comment / video networks at the request level
   (``blocked_hosts.json``);
2. load the page, scroll it to trigger lazy content;
3. resolve the outlet logo BEFORE surgery (``logo.resolve_logo``);
4-8. the in-page surgery (``clip_page.js``): structural container pick, ancestor
   chain kept + siblings removed, high-confidence junk + caller ``drop`` removed
   (never ``keep``), optional section scope, empty-placeholder sweep with every
   removal logged, logo stamped large at the top;
9. white background, A4 PDF with printed backgrounds, full-page preview PNG,
   and every PDF page rasterized (every page borders a page break, the last page
   included) so a reviewer inspects what actually printed.

WHY an ephemeral headless Chromium and not the person's persistent profile run:
``page.pdf`` exists only in headless Chromium, while a persistent run can be
headed for handoff (S2 §12.1: the mode is fixed at bootstrap); request-level
blocking needs a route on the browser context, which the S2 worker protocol
does not carry; and a clip must never be rendered with a person's cookies. The
browser is still ours and still fenced — the SSRF egress guard from
``matrx_scraper.ai_browser.url_guard`` is installed on the context before the
first page, exactly as for every other server browser. This module never
fetches a URL itself; every byte comes through the browser.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .hosts import is_blocked_host
from .logo import LogoResolution, resolve_logo
from matrx_scraper.utils.proxy import redact_url_secrets

logger = logging.getLogger("matrx_scraper.press_clip.renderer")

CLIP_PAGE_JS: str = Path(__file__).with_name("clip_page.js").read_text()

VIEWPORT = {"width": 1180, "height": 1600}
DEVICE_SCALE_FACTOR = 2
NAV_TIMEOUT_MS = 60_000
SETTLE_AFTER_LOAD_MS = 3_500
SETTLE_AFTER_SCROLL_MS = 1_500
HOME_SETTLE_MS = 2_000
RASTER_DPI = 110
MAX_RASTER_PAGES = 40

_WHITE_PAGE_CSS = (
    "html,body{background:#fff !important}@media print{html,body{background:#fff !important}}"
)


@dataclass
class BlockCounter:
    count: int = 0
    hosts: set[str] = field(default_factory=set)


async def install_block_route(target: Any, counter: BlockCounter) -> None:
    """Abort requests to blocked hosts; hand every other request to the next route.

    Register it AFTER the egress guard: Playwright runs the most recently
    registered handler first, and ``fallback()`` passes the request on, so the
    guard still judges everything that is not an ad network.
    """

    async def _route(route: Any) -> None:
        try:
            host = urlparse(route.request.url).hostname or ""
        except Exception:  # noqa: BLE001 — an unparsable URL is the guard's to judge
            host = ""
        if host and is_blocked_host(host):
            counter.count += 1
            counter.hosts.add(host)
            await route.abort()
            return
        await route.fallback()

    await target.route("**/*", _route)


@dataclass
class RenderedClip:
    pdf: bytes
    preview_png: bytes
    page_rasters: list[bytes]
    logo: LogoResolution
    meta: dict[str, Any]
    report: dict[str, Any]
    blocked_request_count: int
    blocked_hosts: list[str]
    scope_applied: str
    final_url: str
    notes: list[str]


def rasterize_pdf(
    pdf: bytes, *, dpi: int = RASTER_DPI, max_pages: int = MAX_RASTER_PAGES
) -> list[bytes]:
    """Every page of the PDF as PNG, in order. Past ``max_pages`` the first
    pages give way so the LAST page is always included."""
    import pymupdf

    doc = pymupdf.open(stream=pdf, filetype="pdf")
    try:
        indices = list(range(doc.page_count))
        if len(indices) > max_pages:
            indices = indices[: max_pages - 1] + [indices[-1]]
        return [doc[i].get_pixmap(dpi=dpi).tobytes("png") for i in indices]
    finally:
        doc.close()


async def _scroll_for_lazy_content(page: Any) -> None:
    await page.evaluate(
        """async () => {
          for (let y = 0; y < document.body.scrollHeight; y += 800) {
            window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80));
          }
          window.scrollTo(0, 0);
        }"""
    )


async def render_clip_document(
    *,
    url: str,
    client_name: str,
    scope: str = "whole",
    section_heading: str | None = None,
    drop: list[str] | None = None,
    keep: list[str] | None = None,
    root: str | None = None,
    logo_url: str | None = None,
) -> RenderedClip:
    from playwright.async_api import async_playwright

    from matrx_scraper.ai_browser.url_guard import guard_target, install_egress_guard

    await guard_target(url)
    notes: list[str] = []
    counter = BlockCounter()
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=True)
    try:
        # bypass_csp: the surgery and the white-page style are OUR code in the
        # page; a site's CSP must not be able to refuse them.
        context = await browser.new_context(
            viewport=VIEWPORT, device_scale_factor=DEVICE_SCALE_FACTOR, bypass_csp=True
        )
        await install_egress_guard(context)
        await install_block_route(context, counter)
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
        await page.wait_for_timeout(SETTLE_AFTER_LOAD_MS)
        await page.evaluate(CLIP_PAGE_JS)
        # Pick the container BEFORE scrolling: infinite-scroll templates append the
        # next stories into the same <main> once scrolled.
        await page.evaluate("(r) => window.__pressClip.markContainer(r)", (root or "").strip())
        await _scroll_for_lazy_content(page)
        await page.wait_for_timeout(SETTLE_AFTER_SCROLL_MS)
        meta = await page.evaluate("() => window.__pressClip.readMeta()")

        async def article_masthead() -> tuple[str, str]:
            got = await page.evaluate("() => window.__pressClip.detectMastheadLogo()")
            return got.get("logoSrc") or "", got.get("logoSvg") or ""

        async def home_masthead() -> tuple[str, str]:
            parsed = urlparse(page.url or url)
            home = await context.new_page()
            try:
                await home.goto(
                    f"{parsed.scheme}://{parsed.netloc}/",
                    wait_until="domcontentloaded",
                    timeout=NAV_TIMEOUT_MS,
                )
                await home.wait_for_timeout(HOME_SETTLE_MS)
                await home.evaluate(CLIP_PAGE_JS)
                got = await home.evaluate("() => window.__pressClip.detectMastheadLogo()")
                return got.get("logoSrc") or "", got.get("logoSvg") or ""
            finally:
                await home.close()

        async def fallback() -> str:
            return await page.evaluate("() => window.__pressClip.detectLogoFallback()") or ""

        logo = await resolve_logo(
            explicit_url=logo_url,
            article_masthead=article_masthead,
            home_masthead=home_masthead,
            fallback=fallback,
        )
        notes.extend(logo.notes)

        heading = ""
        if scope == "section":
            heading = (section_heading or client_name or "").strip()
        report = await page.evaluate(
            "(o) => window.__pressClip.clip(o)",
            {
                "clientName": client_name,
                "sectionHeading": heading,
                "keep": [s for s in (keep or []) if s.strip()],
                "drop": [s for s in (drop or []) if s.strip()],
                "root": (root or "").strip(),
                "logoSrc": logo.url or "",
                "logoSvg": logo.svg or "",
            },
        )
        scope_applied = "section" if report.get("section_applied") else "whole"
        if scope == "section" and scope_applied != "section":
            notes.append(
                f"No heading in the article starts with {heading!r}, so section scope could not "
                "apply; the clip is the whole article."
            )
        if root and report.get("root_override_matched") is False:
            notes.append(
                f"root {root!r} matched nothing on the page; the container was picked automatically."
            )
        if report.get("invalid_selectors"):
            notes.append(f"Ignored invalid selectors: {report['invalid_selectors']}")
        if not client_name.strip():
            notes.append(
                "No client name was given, so client_found_in_text is false by definition."
            )

        await page.add_style_tag(content=_WHITE_PAGE_CSS)
        await page.wait_for_timeout(600)
        late = await page.evaluate(
            "(k) => window.__pressClip.finalSweep(k)", [s for s in (keep or []) if s.strip()]
        )
        if late:
            notes.append(f"Removed {len(late)} late overlay(s) before printing: {late}")
        preview = await page.screenshot(full_page=True, type="png")
        pdf = await page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "10mm", "bottom": "12mm", "left": "8mm", "right": "8mm"},
        )
        final_url = page.url
    finally:
        await browser.close()
        await pw.stop()

    rasters = await asyncio.to_thread(rasterize_pdf, pdf)
    if report.get("removed_placeholders"):
        logger.info(
            "press clip %s: swept %d empty placeholder(s): %s",
            redact_url_secrets(url),
            len(report["removed_placeholders"]),
            report["removed_placeholders"],
        )
    return RenderedClip(
        pdf=pdf,
        preview_png=preview,
        page_rasters=rasters,
        logo=logo,
        meta=meta,
        report=report,
        blocked_request_count=counter.count,
        blocked_hosts=sorted(counter.hosts),
        scope_applied=scope_applied,
        final_url=final_url,
        notes=notes,
    )


__all__ = [
    "CLIP_PAGE_JS",
    "BlockCounter",
    "RenderedClip",
    "install_block_route",
    "rasterize_pdf",
    "render_clip_document",
]
