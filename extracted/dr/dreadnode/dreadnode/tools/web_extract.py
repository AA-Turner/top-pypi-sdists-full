"""Web extraction tool for turning one or more URLs into comparable page records."""

import asyncio
import typing as t

import httpx

from dreadnode.agents.tools import tool
from dreadnode.tools.fetch import FetchResponse
from dreadnode.tools.fetch import _fetch_single_url as _fetch_single_url_impl

MAX_URLS = 5


class WebExtractPage(t.TypedDict):
    success: bool
    url: str
    final_url: str | None
    status_code: int | None
    content_type: str | None
    format: str
    title: str | None
    content_length: int
    truncated: bool
    content: str
    error: str | None


class WebExtractResponse(t.TypedDict):
    success: bool
    partial: bool
    requested_count: int
    extracted_count: int
    format: str
    warnings: list[str]
    results: list[WebExtractPage]


@tool
async def web_extract(
    urls: t.Annotated[list[str], "One or more HTTP(S) URLs to extract"],
    *,
    format: t.Annotated[
        t.Literal["markdown", "text", "html"],
        "Output format for each extracted page",
    ] = "markdown",
    timeout: t.Annotated[int, "Per-request timeout in seconds (max 120)"] = 30,  # noqa: ASYNC109
    headers: t.Annotated[
        dict[str, str] | None, "Custom HTTP headers to send with each request"
    ] = None,
) -> WebExtractResponse:
    """
    Extract content from multiple public URLs and return normalized page records.

    This tool is designed for research loops:
    - Use ``web_search`` to discover candidate URLs
    - Use ``web_extract`` to turn selected URLs into comparable page records
    - Compare and synthesize from the resulting ``results`` list

    Notes:
    - Supports up to 5 unique URLs per call
    - Deduplicates repeated URLs while preserving order
    - Continues on individual page failures and records the error per page
    """
    if not urls:
        raise ValueError("At least one URL is required.")

    deduped_urls, warnings = _dedupe_urls(urls)
    if len(deduped_urls) > MAX_URLS:
        raise ValueError(f"web_extract supports at most {MAX_URLS} unique URLs per call.")

    results = await asyncio.gather(
        *[
            _extract_one(url, format=format, timeout=timeout, headers=headers)
            for url in deduped_urls
        ]
    )

    extracted_count = sum(1 for result in results if result["success"])
    requested_count = len(deduped_urls)

    return {
        "success": extracted_count > 0,
        "partial": extracted_count < requested_count,
        "requested_count": requested_count,
        "extracted_count": extracted_count,
        "format": format,
        "warnings": warnings,
        "results": results,
    }


async def _fetch_single_url(
    url: str,
    *,
    format: t.Literal["markdown", "text", "html"] = "markdown",
    timeout: int = 30,  # noqa: ASYNC109
    headers: dict[str, str] | None = None,
) -> FetchResponse:
    """Shim for easier testing and future backend swaps."""
    return await _fetch_single_url_impl(url, format=format, timeout=timeout, headers=headers)


def _dedupe_urls(urls: list[str]) -> tuple[list[str], list[str]]:
    seen: set[str] = set()
    deduped: list[str] = []
    duplicate_count = 0

    for url in urls:
        cleaned = url.strip()
        if not cleaned:
            continue
        if cleaned in seen:
            duplicate_count += 1
            continue
        seen.add(cleaned)
        deduped.append(cleaned)

    warnings: list[str] = []
    if duplicate_count:
        warnings.append(f"Dropped {duplicate_count} duplicate URL.")
    return deduped, warnings


async def _extract_one(
    url: str,
    *,
    format: t.Literal["markdown", "text", "html"],
    timeout: int,  # noqa: ASYNC109
    headers: dict[str, str] | None,
) -> WebExtractPage:
    try:
        response = await _fetch_single_url(url, format=format, timeout=timeout, headers=headers)
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code if exc.response is not None else None
        return {
            "success": False,
            "url": url,
            "final_url": str(exc.response.url) if exc.response is not None else None,
            "status_code": status_code,
            "content_type": None,
            "format": format,
            "title": None,
            "content_length": 0,
            "truncated": False,
            "content": "",
            "error": f"HTTP {status_code}: {exc}",
        }
    except Exception as exc:
        return {
            "success": False,
            "url": url,
            "final_url": None,
            "status_code": None,
            "content_type": None,
            "format": format,
            "title": None,
            "content_length": 0,
            "truncated": False,
            "content": "",
            "error": str(exc),
        }

    return {
        "success": True,
        "url": response["url"],
        "final_url": response["final_url"],
        "status_code": response["status_code"],
        "content_type": response["content_type"],
        "format": response["format"],
        "title": response["title"],
        "content_length": response["content_length"],
        "truncated": response["truncated"],
        "content": response["content"],
        "error": None,
    }
