"""The host's browser lane: render ONE url in the scraper service's pooled browser, as a normal ``Response``.

A blocked or empty read gets one browser render. On the aidream server there is no local browser; the lane is the
scraper service's pooled Chromium (``POST /api/scraper/browser-fetch``), which only the HOST can call. The host
registers that call as the ``browser_render`` ext (``configure_ext(browser_render=...)``): an async
``(url) -> {success, status_code, final_url, title, content_type, html, error}``.

ONE implementation for every reader: research's own browser rescue (``research/scraper.py``) and ``scraper.scrape``
in ``mode: browser`` both render here, so a workflow read and a code read of a blocked page take the same lane.
Never raises: any miss is ``None`` and a log line, and the caller keeps its original read.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from matrx_scraper._ext import get_ext, has_ext
from matrx_scraper.utils.proxy import redact_url_secrets

logger = logging.getLogger("matrx_scraper.browser_lane")

BROWSER_RENDER_EXT = "browser_render"

#: The scraper service runs a fixed, small browser pool shared with every live crawl: two renders at a time per
#: process is the opportunistic lane (moved from research/scraper.py MAX_CONCURRENT_BROWSER_RESCUES).
MAX_CONCURRENT_RENDERS = 2
_gate: asyncio.Semaphore | None = None


def _render_gate() -> asyncio.Semaphore:
    global _gate
    if _gate is None:
        _gate = asyncio.Semaphore(MAX_CONCURRENT_RENDERS)
    return _gate


def has_browser_lane() -> bool:
    return has_ext(BROWSER_RENDER_EXT)


async def render_in_browser_lane(url: str, *, trigger: str, render: Any = None) -> Any:
    """The rendered page as a ``matrx_scraper.scraper.Response`` (request type BROWSER), or ``None`` on any miss
    (no lane, render failed, not usable HTML). ``render``: the host's render call, when the caller IS the host."""
    from matrx_scraper.scraper import (
        ContentType,
        RequestType,
        Response,
        detect_response_content_type,
        extract_publication_dates_from_html,
    )

    if render is None and not has_browser_lane():
        logger.warning("[BROWSER LANE MISS] %s (%s): this host registered no browser lane", redact_url_secrets(url), trigger)
        return None
    try:
        from matrx_scraper.page_replay import replayed

        async def _render() -> Any:
            async with _render_gate():
                return await (render or get_ext(BROWSER_RENDER_EXT))(url)

        # The render's answer is a provider answer: replayed when the host records/replays page answers.
        fetched = await replayed("browser", url, _render, to_answer=lambda d: d, from_answer=lambda d: d)
        if not isinstance(fetched, dict) or not fetched.get("success"):
            error = str(fetched.get("error") or "") if isinstance(fetched, dict) else ""
            logger.warning(
                "[BROWSER RESCUE MISS] %s (%s): %s", redact_url_secrets(url), trigger, redact_url_secrets(error or "render failed")
            )
            return None
        html = str(fetched.get("html") or "")
        final_url = str(fetched.get("final_url") or url)
        try:
            status_code = int(fetched.get("status_code") or 0)
        except (TypeError, ValueError):
            status_code = 0
        content_type_raw = str(fetched.get("content_type") or "")
        content_type, _ = detect_response_content_type(url=final_url, content_type_raw=content_type_raw, content=html)
        if content_type != ContentType.HTML or not html:
            logger.warning(
                "[BROWSER RESCUE MISS] %s (%s): rendered %s — not usable HTML", redact_url_secrets(url), trigger, content_type
            )
            return None
        published_at, modified_at = extract_publication_dates_from_html(html)
        logger.info("[BROWSER RESCUE] %s (%s): rendered %s chars", redact_url_secrets(url), trigger, f"{len(html):,}")
        return Response(
            request_url=url,
            proxy_used=False,
            request_type=RequestType.BROWSER,
            content_type=content_type,
            extension="html",
            content_type_raw=content_type_raw,
            response_url=final_url,
            response_headers={},
            title=str(fetched.get("title") or "") or None,
            status_code=status_code or 200,
            content=html,
            published_at=published_at,
            modified_at=modified_at,
        )
    except Exception as exc:  # noqa: BLE001 — a lane miss, never a crash of the read it tries to save
        logger.warning(
            "[BROWSER RESCUE MISS] %s (%s): %s: %s",
            redact_url_secrets(url), trigger, type(exc).__name__, redact_url_secrets(exc), exc_info=True,
        )
        return None
