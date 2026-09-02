import asyncio
import random
from typing import Any

from matrx_utils import vcprint

try:
    from matrx_connect import Emitter
except ImportError:
    from typing import Any

    Emitter = Any

from matrx_scraper.scraper import fetch_normally_with_proxy, ContentType
from matrx_scraper.parser.core import parse_html
from matrx_scraper.extractors import (
    extract_text_from_pdf_bytes_async,
    extract_text_from_image_bytes_async,
    extract_text_content,
)


LOCAL_DEBUG = False


async def _emit_progress(
    stream_handler,
    user_visible_message: str,
    call_id: str | None = None,
    step_data: dict | None = None,
) -> None:
    if stream_handler is None:
        return
    if hasattr(stream_handler, "send_function_call"):
        await stream_handler.send_function_call(
            user_visible_message=user_visible_message,
            call_id=call_id,
            step_data=step_data,
        )
    elif hasattr(stream_handler, "send_tool_event"):
        event: dict[str, Any] = {
            "event": "tool_progress",
            "call_id": call_id or "",
            "tool_name": "web_research",
            "message": user_visible_message,
            "show_spinner": True,
            "data": step_data or {},
        }
        await stream_handler.send_tool_event(event)


async def scrape_url_core(
    url: str,
    good_scrape_threshold: int = 1000,
    delay: float = 0,
    stream_handler=None,
    call_id=None,
) -> dict[str, Any] | None:
    """
    Fetch and parse a single URL, returning a lightweight page dict suitable
    for the AI tool layer.

    Returns None on failure so callers can filter with a simple list comprehension.
    """
    if delay > 0:
        await asyncio.sleep(delay)

    if stream_handler:
        await _emit_progress(stream_handler, f"Browsing {url}", call_id=call_id)

    response = await fetch_normally_with_proxy(url)

    has_content = response.content or response.content_bytes
    if response.failed or not has_content:
        failure_reason = ""
        if response.failed and response.failed_primary_reason:
            failure_reason = f" ({response.failed_primary_reason})"
        elif not has_content:
            failure_reason = " (no content)"
        vcprint(f"SCRAPE SKIPPED: {url}{failure_reason}", color="cyan")
        return None

    content = ""
    if response.content_type == ContentType.HTML:
        parsed = await parse_html(response.content, response.response_url)
        content = parsed.get("ai_research_with_images", "")
    elif response.content_type == ContentType.PDF:
        raw_bytes = response.content_bytes
        if not raw_bytes:
            vcprint(
                f"SCRAPE SKIPPED: {url} (PDF detected but no binary data captured)", color="cyan"
            )
            return None
        # 300 DPI pdfium render + pytesseract OCR per page — seconds to minutes
        # of pure CPU. On the loop it starves the podcast ticker AND the stream
        # heartbeat simultaneously, which surfaces to the user as a false
        # "connection went quiet" stall on a run that is working fine.
        content = await extract_text_from_pdf_bytes_async(raw_bytes) or ""
    elif response.content_type == ContentType.IMAGE:
        raw_bytes = response.content_bytes
        if not raw_bytes:
            vcprint(
                f"SCRAPE SKIPPED: {url} (image detected but no binary data captured)", color="cyan"
            )
            return None
        # pytesseract OCR — same starvation risk as the PDF branch above.
        content = await extract_text_from_image_bytes_async(raw_bytes) or ""
    elif response.content_type in (
        ContentType.JSON,
        ContentType.XML,
        ContentType.MARKDOWN,
        ContentType.PLAIN_TEXT,
    ):
        content = extract_text_content(response.content, response.content_type.value) or ""
    else:
        vcprint(
            f"SCRAPE SKIPPED: {url} (unsupported content type: {response.content_type_raw})",
            color="cyan",
        )
        return None

    char_count = len(content)
    is_good_scrape = char_count >= good_scrape_threshold

    if not is_good_scrape:
        vcprint(
            f"SCRAPE THIN: {url} | {char_count:,} chars (below {good_scrape_threshold:,} threshold)",
            color="yellow",
        )
    else:
        vcprint(f"SCRAPE SUCCESS: {url} | {char_count:,} chars", color="green")

    date_info = (f"Published: {response.published_at}\n" if response.published_at else "") + (
        f"Modified: {response.modified_at}\n" if response.modified_at else ""
    )

    return {
        "url": response.response_url,
        "title": response.title,
        "date_info": date_info,
        "content": content,
        "char_count": char_count,
        "is_good_scrape": is_good_scrape,
    }


async def scrape_urls_from_search_result(
    search_result: dict[str, Any],
    seen_urls: set,
    urls_per_query: int = 5,
    good_scrape_threshold: int = 1000,
    emitter: Emitter = None,
    call_id=None,
) -> list[dict[str, Any]]:
    """
    Extract URLs from a Brave Search API response dict and scrape them in
    parallel.  Updates ``seen_urls`` in-place to deduplicate across calls.
    """
    combined_results = search_result.get("web", {}).get("results", []) + search_result.get(
        "news", {}
    ).get("results", [])

    urls_to_scrape = []
    for result in combined_results[:urls_per_query]:
        url = result.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            urls_to_scrape.append(url)

    if not urls_to_scrape:
        return []

    scraping_tasks = [
        scrape_url_core(
            url,
            good_scrape_threshold=good_scrape_threshold,
            delay=idx * random.uniform(0.3, 0.7),
            stream_handler=emitter,
            call_id=call_id,
        )
        for idx, url in enumerate(urls_to_scrape)
    ]

    scraped_results = await asyncio.gather(*scraping_tasks)
    successful = [s for s in scraped_results if s is not None]
    if urls_to_scrape and not successful:
        vcprint(
            f"SCRAPE BATCH EMPTY: all {len(urls_to_scrape)} candidate URLs failed",
            color="yellow",
        )
    return successful
