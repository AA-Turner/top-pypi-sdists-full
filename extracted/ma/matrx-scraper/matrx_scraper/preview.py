"""Quick site preview — used by the dashboard's New Crawl form.

When the user blurs the URL field, the dashboard fires this endpoint and we:
  1. Normalise whatever was typed to https://...
  2. Fetch /robots.txt + the homepage in parallel
  3. Run the SEO audit on the homepage HTML
  4. Take a single desktop-viewport screenshot via Playwright (best-effort)

Returns a JSON payload the UI can render as a tiny "what we'll be crawling"
preview card. Bounded by tight timeouts so the user gets feedback in <5s
even on slow sites.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import time
from dataclasses import dataclass, field
from typing import Any

import httpx

from matrx_scraper.seo_audit import audit_html, build_page_check_report, evidence_from_audit
from matrx_scraper.url_utils import normalize_url
from matrx_scraper.utils.url import validate_public_http_url

logger = logging.getLogger(__name__)


@dataclass
class _Fetched:
    """One fetch, with the transport facts the per-page checks need.

    A field that stays at its "not captured" value (``0`` status / ``None``
    latency) makes its check answer ``n_a``, never a silent pass.
    """

    status: int = 0
    text: str = ""
    final_url: str | None = None
    # Oldest first, final URL last — the hop shape web_crawl persists.
    redirect_chain: list[dict[str, Any]] = field(default_factory=list)
    response_bytes: int | None = None
    response_time_ms: int | None = None
    ttfb_ms: int | None = None


async def _fetch_text(client: httpx.AsyncClient, url: str) -> _Fetched:
    started = time.perf_counter()
    try:
        async with client.stream("GET", url) as r:
            # Entering a streamed response means the final response headers
            # arrived; the body has not been consumed. This is true TTFB,
            # unlike Response.elapsed after client.get(), which includes the body.
            ttfb_ms = int((time.perf_counter() - started) * 1000)
            content = await r.aread()
    except Exception as exc:
        logger.info("preview fetch %s failed: %s", url, exc)
        return _Fetched()
    # SSRF gate, part 2 — the client follows redirects, so a public URL can
    # land on an internal host. Never return a body read off a non-public
    # address; the caller gets the same shape as a failed fetch.
    try:
        await validate_public_http_url(str(r.url))
    except Exception as exc:
        logger.warning("preview discarded a non-public final url for %s: %s", url, exc)
        return _Fetched()
    chain = [{"status": h.status_code, "url": str(h.url)} for h in r.history]
    chain.append({"status": r.status_code, "url": str(r.url)})
    return _Fetched(
        status=r.status_code,
        text=r.text,
        final_url=str(r.url),
        redirect_chain=chain,
        response_bytes=len(content),
        response_time_ms=int((time.perf_counter() - started) * 1000),
        ttfb_ms=ttfb_ms,
    )


def _summarise_robots(text: str) -> dict[str, Any]:
    if not text:
        return {
            "present": False,
            "lines": 0,
            "user_agents": [],
            "sitemaps": [],
            "disallow_count": 0,
        }
    user_agents: list[str] = []
    sitemaps: list[str] = []
    disallow_count = 0
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        lower = s.lower()
        if lower.startswith("user-agent:"):
            user_agents.append(s.split(":", 1)[1].strip())
        elif lower.startswith("sitemap:"):
            sitemaps.append(s.split(":", 1)[1].strip())
        elif lower.startswith("disallow:"):
            disallow_count += 1
    # Dedup user agents preserving order
    seen: set[str] = set()
    user_agents = [u for u in user_agents if not (u in seen or seen.add(u))]
    return {
        "present": True,
        "lines": len(text.splitlines()),
        "user_agents": user_agents[:10],
        "sitemaps": sitemaps[:10],
        "disallow_count": disallow_count,
    }


async def _take_homepage_screenshot(url: str) -> dict[str, Any] | None:
    """Best-effort Playwright capture. Returns a base64-encoded PNG.

    Three-phase wait so hero videos, lazy-loaded images, and client-side
    rendered content actually appear in the frame:

      1. ``wait_until="load"`` — DOM + linked resources finished loading
         (vs ``domcontentloaded`` which fires before scripts/images settle).
      2. Best-effort ``networkidle`` — typically lets late XHR/fetch
         requests complete (lazy image loaders, video poster fetches).
         Bounded so an analytics beacon that never closes can't hang us.
      3. A small explicit pause for client-side animations + first paint
         of <video> posters that come in *after* networkidle.

    Worst case ~9s, typical ~2-3s. Outer quick_preview() timeout is 20s.
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            try:
                ctx = await browser.new_context(
                    viewport={"width": 1366, "height": 768},
                    user_agent="MatrxScraperBot/preview (+https://aimatrx.com)",
                )
                # /preview renders an arbitrary caller-supplied URL. The target
                # is address-gated, but a public page's own scripts can fetch an
                # internal host and paint the response into the screenshot we
                # hand back. Same guard, same reason.
                from matrx_scraper.ai_browser.url_guard import install_egress_guard

                await install_egress_guard(ctx)
                page = await ctx.new_page()
                try:
                    # Phase 1 — DOM + linked resources loaded.
                    await page.goto(url, timeout=15_000, wait_until="load")
                    # Phase 2 — network quiet. Bounded; many sites keep
                    # long-poll / analytics sockets open so we can't wait
                    # forever. 5s is enough for typical hero images / video
                    # posters to fetch.
                    try:
                        await page.wait_for_load_state("networkidle", timeout=5_000)
                    except Exception:
                        pass  # not-quiet network is fine, we proceed
                    # Phase 3 — final settle for client-side animations and
                    # lazy <video> elements that swap in their poster after
                    # the first paint.
                    await asyncio.sleep(1.5)
                    # SSRF gate, part 2 — a screenshot of an internal page is
                    # the same disclosure as its HTML, and the browser follows
                    # redirects the pre-gate never saw.
                    try:
                        await validate_public_http_url(page.url)
                    except Exception as exc:
                        logger.warning(
                            "preview discarded a screenshot taken on a non-public url: %s",
                            exc,
                        )
                        return None
                    png = await page.screenshot(full_page=False, type="png")
                    return {
                        "kind": "viewport_desktop",
                        "width": 1366,
                        "height": 768,
                        "bytes": len(png),
                        "data_url": "data:image/png;base64,"
                        + base64.b64encode(png).decode("ascii"),
                    }
                finally:
                    await page.close()
                    await ctx.close()
            finally:
                await browser.close()
    except Exception as exc:
        logger.info("preview screenshot failed for %s: %s", url, exc)
        return None


async def quick_preview(raw_url: str) -> dict[str, Any]:
    """Normalize, fetch robots + homepage, audit, screenshot. Returns JSON."""
    try:
        url = normalize_url(raw_url)
    except ValueError as exc:
        return {"ok": False, "error": str(exc), "input": raw_url}

    # SSRF gate, part 1 — this renders and reads an arbitrary URL from INSIDE
    # the scraper network. The rejection reason names the resolved address, so
    # it is logged and never echoed: it would make any authenticated caller an
    # internal-network resolution oracle.
    try:
        url = await validate_public_http_url(url)
    except Exception as exc:
        logger.warning("preview BLOCKED target %r: %s", raw_url, exc)
        return {
            "ok": False,
            "error": "url must be a publicly routable http(s) address",
            "input": raw_url,
        }

    from urllib.parse import urlparse, urljoin

    parsed = urlparse(url)
    homepage_url = f"{parsed.scheme}://{parsed.netloc}/"
    robots_url = urljoin(homepage_url, "/robots.txt")

    headers = {"User-Agent": "MatrxScraperBot/preview (+https://aimatrx.com)"}
    async with httpx.AsyncClient(timeout=8.0, follow_redirects=True, headers=headers) as client:
        robots_task = asyncio.create_task(_fetch_text(client, robots_url))
        home_task = asyncio.create_task(_fetch_text(client, url))
        robots_fetch = await robots_task
        home_fetch = await home_task

    robots_status, robots_text = robots_fetch.status, robots_fetch.text
    home_status, home_html = home_fetch.status, home_fetch.text

    homepage_summary: dict[str, Any] = {"status": home_status}
    if home_html and home_status and 200 <= home_status < 400:
        audit = audit_html(home_html, url)
        # The measurements say what the page IS; the checks say whether that is
        # GOOD. Both go out — the owner reading this card is not an SEO expert
        # and cannot turn "title_length: 74" into a decision. Every verdict
        # comes from seo_audit.PAGE_CHECKS; nothing is re-derived here.
        evidence = evidence_from_audit(
            audit,
            http_status=home_status,
            redirect_chain=home_fetch.redirect_chain,
            final_url=home_fetch.final_url,
            response_bytes=home_fetch.response_bytes,
            response_time_ms=home_fetch.response_time_ms,
            ttfb_ms=home_fetch.ttfb_ms,
        )
        homepage_summary["checks"] = build_page_check_report(evidence).model_dump()
        homepage_summary.update(
            {
                "title": audit.title,
                "title_length": audit.title_length,
                "meta_description": audit.meta_description,
                "meta_description_length": audit.meta_description_length,
                "lang": audit.lang,
                "canonical": audit.canonical,
                "h1": audit.h1[:5],
                "schema_types": audit.schema_types[:8],
                "word_count": audit.word_count,
                "link_count": audit.link_count,
                "internal_links": audit.internal_links,
                "external_links": audit.external_links,
                "images_total": audit.images_total,
                "images_missing_alt": audit.images_missing_alt,
                "flesch_reading_ease": audit.flesch_reading_ease,
                "og": dict(list(audit.og.items())[:8]),
            }
        )

    robots_summary = (
        _summarise_robots(robots_text)
        if robots_status and 200 <= robots_status < 400
        else {"present": False}
    )

    # Screenshot capped at ~20s; if it times out we still return the rest.
    # The three-phase wait inside _take_homepage_screenshot can take up to
    # ~9s on slow sites; 20s gives headroom for the browser cold-start cost
    # too. If it times out the UI just shows "screenshot timed out" and the
    # title / robots / metadata still render.
    try:
        screenshot = await asyncio.wait_for(_take_homepage_screenshot(url), timeout=20.0)
    except TimeoutError:
        screenshot = None
    except Exception:
        screenshot = None

    return {
        "ok": True,
        "input": raw_url,
        "normalized_url": url,
        "homepage_url": homepage_url,
        "robots_url": robots_url,
        "robots": robots_summary,
        "homepage": homepage_summary,
        "screenshot": screenshot,
    }


__all__ = ["quick_preview"]
