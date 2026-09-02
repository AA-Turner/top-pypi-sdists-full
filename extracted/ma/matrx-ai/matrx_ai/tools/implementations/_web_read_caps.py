"""Bounded, pageable web-read windows — tool self-cap for ``web`` read/batch_read.

Matches the platform document-read paging shape (``offset`` / ``chars`` /
``has_more`` / ``next_offset`` / ``total_chars``) so agents use one interaction
pattern for long text. The whole serialized tool result is kept under the soft
size gate so ``output_self_capped=True`` is honest.
"""

from __future__ import annotations

import json
from typing import Any

from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS

DEFAULT_CHARS = 8_000
"""Default window for one page of a long URL."""

SHORT_PAGE_FULL_CHARS = 16_000
"""If the whole page fits in two default windows, return it all on first read."""

MAX_CHARS = 40_000
"""Hard max chars returned for one URL in one call."""

RESULT_BUDGET_CHARS = TOOL_RESULT_SOFT_CAP_CHARS - 5_000
"""Whole-result JSON budget (headroom under the 50k soft cap)."""

_TRUNCATION_NOTICE = (
    "Page content is paged and bounded. Call web action='read' again with the "
    "same url and next_offset as offset (optionally raise chars) to continue."
)


def clamp_chars(chars: int) -> int:
    return max(1, min(int(chars), MAX_CHARS))


def resolve_chars(
    *,
    chars: int | None,
    max_content_length: int | None,
    fields_set: set[str] | frozenset[str],
) -> int:
    """Prefer explicit ``chars``, else legacy ``max_content_length``, else default."""
    if "chars" in fields_set and chars is not None:
        return clamp_chars(chars)
    if "max_content_length" in fields_set and max_content_length is not None:
        return clamp_chars(max_content_length)
    if chars is not None and chars != DEFAULT_CHARS:
        return clamp_chars(chars)
    if max_content_length is not None and max_content_length != DEFAULT_CHARS:
        return clamp_chars(max_content_length)
    return DEFAULT_CHARS


def extract_page_text(result: Any) -> str:
    """Pull scrape text from ``read_page_mcp_quick`` (prefers raw ``text``)."""
    if not isinstance(result, dict):
        return str(result or "")
    text = result.get("text")
    if isinstance(text, str) and text.strip():
        return text
    content = result.get("content", result.get("result", ""))
    return content if isinstance(content, str) else str(content or "")


def window_page_content(
    text: str,
    *,
    url: str,
    offset: int = 0,
    chars: int = DEFAULT_CHARS,
    per_url_budget: int | None = None,
    success: bool = True,
    error: str | None = None,
) -> dict[str, Any]:
    """Return one URL's content window in the standard paging shape."""
    total_chars = len(text or "")
    start = min(max(0, int(offset)), total_chars)
    window = clamp_chars(chars)

    # Short-page rule: first read with the default window returns the whole
    # page when it fits in two pages (<16k), unless a batch budget forbids it.
    if (
        start == 0
        and total_chars <= SHORT_PAGE_FULL_CHARS
        and window == DEFAULT_CHARS
        and (per_url_budget is None or total_chars <= per_url_budget)
    ):
        window = total_chars

    if per_url_budget is not None:
        window = min(window, max(1, int(per_url_budget)))

    end = min(total_chars, start + window)
    has_more = end < total_chars
    page: dict[str, Any] = {
        "url": url,
        "content": (text or "")[start:end],
        "offset": start,
        "chars_returned": end - start,
        "total_chars": total_chars,
        "has_more": has_more,
        "next_offset": end if has_more else None,
        "success": success,
        "truncation_notice": _TRUNCATION_NOTICE if has_more else None,
    }
    if error:
        page["error"] = error
        page["success"] = False
    return page


def per_url_budget(url_count: int) -> int:
    n = max(1, int(url_count))
    return max(1_500, RESULT_BUDGET_CHARS // n)


def enforce_result_budget(
    output: dict[str, Any],
    *,
    budget: int = RESULT_BUDGET_CHARS,
) -> dict[str, Any]:
    """Trim page contents from the tail until serialized output fits ``budget``.

    Mutates ``output["pages"]`` in place and sets ``result_truncated`` when it
    had to shrink further past per-URL windowing.
    """
    pages = output.get("pages")
    if not isinstance(pages, list) or not pages:
        return output

    def _size() -> int:
        return len(json.dumps(output, default=str))

    if _size() <= budget:
        output.setdefault("result_truncated", False)
        return output

    # Progressive shrink: cut each page's content by half until under budget.
    for _ in range(12):
        if _size() <= budget:
            break
        for page in pages:
            if not isinstance(page, dict):
                continue
            content = page.get("content")
            if not isinstance(content, str) or len(content) <= 200:
                continue
            keep = max(200, len(content) // 2)
            page["content"] = content[:keep]
            page["chars_returned"] = keep
            # Offset stays; we shrank the window — has_more if page continues.
            total = int(page.get("total_chars") or 0)
            start = int(page.get("offset") or 0)
            end = start + keep
            page["has_more"] = end < total
            page["next_offset"] = end if end < total else None
            page["truncation_notice"] = (
                _TRUNCATION_NOTICE if end < total else page.get("truncation_notice")
            )
        output["result_truncated"] = True
    else:
        output["result_truncated"] = True

    if _size() > budget:
        # Last resort: keep metadata, drop remaining long content bodies.
        for page in pages:
            if not isinstance(page, dict):
                continue
            content = page.get("content")
            if isinstance(content, str) and len(content) > 0:
                total = int(page.get("total_chars") or len(content))
                start = int(page.get("offset") or 0)
                page["content"] = ""
                page["chars_returned"] = 0
                page["has_more"] = total > start
                page["next_offset"] = start if total > start else None
                page["truncation_notice"] = _TRUNCATION_NOTICE
        output["result_truncated"] = True

    return output
