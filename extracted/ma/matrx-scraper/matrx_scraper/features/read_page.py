import logging
from typing import Any

from matrx_utils import capture_error, vcprint

from matrx_scraper.scraper import fetch_normally_with_proxy, ContentType
from matrx_scraper.parser.core import parse_html
from matrx_scraper.extractors import (
    extract_text_from_pdf_bytes_async,
    extract_text_from_image_bytes_async,
    extract_text_content,
)
from matrx_scraper.features.extensions import get_condenser_1
from matrx_scraper.utils.proxy import redact_url_secrets

LOCAL_DEBUG = False


class ReadPageFetchError(RuntimeError):
    """A page-reader fetch completed without usable content."""


async def _report_fetch_failure(response: Any, *, url: str, operation: str) -> None:
    reason = getattr(getattr(response, "failed_primary_reason", None), "value", None)
    if not reason:
        reason = "empty_content"
        await capture_error(
            ReadPageFetchError("Page reader fetch completed without usable content"),
            kind="scraper_read_page_empty_content",
            context={"url": url, "operation": operation, "failure_reason": reason},
        )
    vcprint(
        f"{operation} could not access {redact_url_secrets(url)} ({reason})",
        color="yellow",
        log_level=logging.WARNING,
        stdout=False,
    )


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
            "tool_name": "web_read",
            "message": user_visible_message,
            "show_spinner": True,
            "data": step_data or {},
        }
        await stream_handler.send_tool_event(event)


async def judge_and_cover(url: str, result: dict[str, Any], verdict: Any) -> dict[str, Any]:
    """Our scraper ALWAYS reads first; this decides what a failed read carries.

    A read judged failed (``read_judge.judge_read``: strong signals only) becomes ``status="error"``
    and carries ``verdict`` + ``coverage`` (which readers could get it, speed, points). The
    organization's ``knowledge.scraper.advanced_fallback`` (host-injected, default ``off``) decides
    whether anything paid runs: ``off`` nothing; ``fast`` the fast readers; ``all`` also structured data.
    """
    from matrx_scraper import coverage as cov
    from matrx_scraper._ext import get_ext, has_ext

    if verdict is None or not verdict.failed:
        return result
    out = {**result, "status": "error", "text": "",
           "result": f"Sorry could not access this page: {verdict.detail}.", "verdict": verdict.to_dict()}
    out.pop("page", None)  # a wall is never landed as a Source
    try:
        covered = await cov.coverage_for(url) if getattr(verdict, "coverable", True) else []
    except Exception as exc:  # noqa: BLE001 - coverage is advice; the honest failure still stands
        vcprint(f"[read_page] coverage unavailable for {redact_url_secrets(url)} "
                f"({redact_url_secrets(repr(exc))})", color="yellow")
        covered = []
    out["coverage"] = [c.to_dict() for c in covered]
    mode = await cov.fallback_mode()
    if mode == "off" or not any(cov.allowed(c, mode) for c in covered) or not has_ext(cov.EXT_READER):
        return out
    if not await cov.take_run_slot():
        return out  # this run's automatic retries are spent: the page keeps its coverage note instead
    try:
        items = await get_ext(cov.EXT_READER)([url], mode)
    except Exception as exc:  # noqa: BLE001 - a refusal (points) or defect: the failed read stands, said
        out["advanced_read"] = {"url": url, "ok": False, "message": getattr(exc, "user_message", None) or str(exc)}
        return out
    item = items[0] if items else {"url": url, "ok": False, "message": "The advanced reader gave no answer."}
    if not item.get("ok"):
        out["advanced_read"] = {k: v for k, v in item.items() if k not in ("text", "markdown", "records")}
        return out
    text = item.get("text") or ""
    return {
        "status": "success",
        "result": text,
        "text": text,
        "url": url,
        "engine": "advanced_read",
        "advanced_read": {k: v for k, v in item.items() if k not in ("text", "markdown", "records")},
        "notice": item.get("message"),
        "page": {
            "success": True,
            "url": url,
            "response_url": url,
            "content_type": "text/markdown",
            "text_data": text,
            "markdown_renderable": item.get("markdown") or text,
            "ai_research_with_images": text,
            "engine": "advanced_read",
            "raw_html": None,
        },
    }


async def read_page_mcp_quick(url: str = None, stream_handler=None, call_id=None):
    if stream_handler:
        await _emit_progress(stream_handler, f"Browsing {url}", call_id=call_id)
    result, verdict = await _read_page_http_judged(url)
    return await judge_and_cover(url, result, verdict)


async def _read_page_http(url: str) -> dict[str, Any]:
    """The plain read (no judgment) — kept for callers that only want our scraper's answer."""
    result, _ = await _read_page_http_judged(url)
    return result


async def _read_page_http_judged(url: str) -> tuple[dict[str, Any], Any]:
    """Our scraper's read plus ``judge_read``'s verdict on it (``None`` = not judgeable, e.g. a video)."""
    from matrx_scraper.read_judge import judge_read

    response = await fetch_normally_with_proxy(url)
    status = int(getattr(response, "status_code", 0) or 0) or None
    title = getattr(response, "title", None)

    has_content = response.content or response.content_bytes
    if response.failed or not has_content:
        await _report_fetch_failure(response, url=url, operation="read_page_mcp_quick")
        reason = getattr(getattr(response, "failed_primary_reason", None), "value", None) or "empty_content"
        verdict = judge_read(status=status, text="", html=response.content or None, title=title,
                             fetch_failure=reason)
        return {"status": "error", "result": "Sorry could not access this page.", "text": ""}, verdict

    extracted_text = ""
    parsed: dict[str, Any] = {}
    if response.content_type == ContentType.HTML:
        parsed = await parse_html(response.content, response.response_url)
        extracted_text = parsed.get("ai_research_with_images", "")
    elif response.content_type == ContentType.PDF and response.content_bytes:
        extracted_text = await extract_text_from_pdf_bytes_async(response.content_bytes) or ""
    elif response.content_type == ContentType.IMAGE and response.content_bytes:
        extracted_text = await extract_text_from_image_bytes_async(response.content_bytes) or ""
    elif response.content_type in (
        ContentType.JSON,
        ContentType.XML,
        ContentType.MARKDOWN,
        ContentType.PLAIN_TEXT,
    ):
        extracted_text = extract_text_content(response.content, response.content_type.value) or ""
    else:
        return {
            "status": "error",
            "result": f"Unsupported content type: {response.content_type_raw}",
            "text": "",
        }, None

    html = response.content if response.content_type == ContentType.HTML else None
    if not extracted_text.strip():
        return {
            "status": "error",
            "result": "Sorry could not extract content from this page.",
            "text": "",
        }, judge_read(status=status, text="", html=html, title=title)

    # Legacy wrapped string for older callers; prefer ``text`` (raw extract).
    full_content = (
        f'Here is the content from page {url}: """\n{extracted_text}\n""". '
        "Assess if this context fully answers the user's query. "
        "Use `web_read` on any specific URLs mentioned that seem relevant to dig deeper."
    )

    # DEBUG LOG ONLY — does not change the returned payload.
    text_length = len(extracted_text)
    if text_length > 0:
        first_end = int(text_length * 0.40)
        last_start = int(text_length * 0.60)
        truncated_char_count = last_start - first_end
        log_preview = (
            f"{extracted_text[:first_end]}\n\n"
            f"[... {truncated_char_count:,} characters omitted from this LOG preview "
            f"({truncated_char_count / text_length * 100:.1f}% of extract) — "
            f"the tool result still carries the full text for the caller to window ...]\n\n"
            f"{extracted_text[last_start:]}"
        )
        vcprint(
            log_preview,
            color="magenta",
            title="read_page_mcp_quick (log preview only)",
            log_level=logging.DEBUG,
            stdout=False,
        )
        vcprint(
            f"[INFO] Extract total: {text_length:,} chars | "
            f"Log preview shows head+tail only. Callers (web tool) apply offset/chars paging.",
            title="Character Count Summary",
            color="blue",
            log_level=logging.DEBUG,
            stdout=False,
        )

    return {
        "status": "success",
        "result": full_content,
        "text": extracted_text,
        "url": url,
        # The parse, for landing the page as a Source (SOURCE-CONVERGENCE §4.5 —
        # matrx_scraper.source_landing.land_page_result reads it through from_parsed_page).
        "page": {
            **(parsed if isinstance(parsed, dict) else {}),
            "success": True,
            "url": url,
            "response_url": response.response_url or url,
            "content_type": response.content_type_raw or "",
            "text_data": extracted_text,
            "engine": "http",
            "raw_html": html,
        },
    }, judge_read(status=status, text=extracted_text, html=html, title=title)


async def read_page_mcp_summarized(
    url: str,
    instructions: str,
    queries: str = "",
    search_results: str = "",
    ctx=None,
    stream_handler=None,
    call_id=None,
):
    """Fetch a page and condense it via an AI agent.

    The condenser is optional — it must be registered at application startup
    via ``matrx_scraper.features.extensions.configure_extensions()``.  When no
    condenser has been configured this function returns the raw extracted text
    with a warning rather than raising an error, so callers in apps that do not
    have matrx_ai available still receive useful output.

    Args:
        url: The page to fetch.
        instructions: Task-specific instructions forwarded to the condenser.
        queries: The original search queries (forwarded to the condenser).
        search_results: Prior search-result text (forwarded to the condenser).
        ctx: ToolContext from matrx_ai, required by the condenser. If None and
            no condenser is registered this is silently ignored.
        stream_handler: Optional emitter for progress events.
        call_id: Identifier for the current tool call, used in progress events.
    """
    if stream_handler:
        await _emit_progress(stream_handler, f"Browsing {url}", call_id=call_id)

    response = await fetch_normally_with_proxy(url)
    has_content = response.content or response.content_bytes
    if response.failed or not has_content:
        await _report_fetch_failure(response, url=url, operation="read_page_mcp_summarized")
        return {"status": "error", "result": "Sorry could not access this page."}

    content = ""
    if response.content_type == ContentType.HTML:
        parsed = await parse_html(response.content, response.response_url)
        content = parsed.get("ai_research_with_images", "")
    elif response.content_type == ContentType.PDF and response.content_bytes:
        content = await extract_text_from_pdf_bytes_async(response.content_bytes) or ""
    elif response.content_type == ContentType.IMAGE and response.content_bytes:
        content = await extract_text_from_image_bytes_async(response.content_bytes) or ""
    elif response.content_type in (
        ContentType.JSON,
        ContentType.XML,
        ContentType.MARKDOWN,
        ContentType.PLAIN_TEXT,
    ):
        content = extract_text_content(response.content, response.content_type.value) or ""
    else:
        return {
            "status": "error",
            "result": f"Unsupported content type: {response.content_type_raw}",
        }

    if not content.strip():
        return {"status": "error", "result": "Cannot fetch content, Please try again later."}

    condenser = get_condenser_1()
    if condenser is None:
        vcprint(
            "read_page_mcp_summarized: no AI condenser registered — returning raw content. "
            "Call matrx_scraper.features.extensions.configure_extensions() at startup to enable summarization.",
            color="yellow",
            title="[matrx-scraper] condenser unavailable",
        )
        return {"status": "success", "result": content}

    result = await condenser(
        instructions=instructions,
        scraped_content=content,
        queries=queries,
        search_results=search_results,
        ctx=ctx,
    )

    if not result.success:
        vcprint(f"read_page_mcp_summarized condenser failed: {result.output}", color="red")
        return {"status": "error", "result": result.output}

    return {"status": "success", "result": result.output}
