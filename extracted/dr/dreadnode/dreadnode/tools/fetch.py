"""URL fetching tool with HTML-to-markdown conversion."""

import re
import typing as t
from urllib.parse import urlparse

import httpx
from loguru import logger

from dreadnode.agents.tools import tool

MAX_RESPONSE_SIZE = 5 * 1024 * 1024  # 5 MB
"""Hard limit on raw response body before processing."""

MAX_OUTPUT_LENGTH = 50_000
"""Character limit on returned content (after conversion)."""

DEFAULT_TIMEOUT = 30
MAX_TIMEOUT = 120

_ACCEPT_HEADERS: dict[str, str] = {
    "markdown": "text/markdown;q=1.0, text/x-markdown;q=0.9, text/plain;q=0.8, text/html;q=0.7, */*;q=0.1",
    "text": "text/plain;q=1.0, text/markdown;q=0.9, text/html;q=0.8, */*;q=0.1",
    "html": "text/html;q=1.0, application/xhtml+xml;q=0.9, text/plain;q=0.8, */*;q=0.1",
}


class FetchResponse(t.TypedDict):
    success: bool
    url: str
    final_url: str
    status_code: int
    content_type: str
    format: str
    title: str | None
    content_length: int
    truncated: bool
    content: str


# ---------------------------------------------------------------------------
# HTML converters
# ---------------------------------------------------------------------------


def _html_to_markdown(html: str) -> str:
    """Convert HTML to markdown using markdownify."""
    from bs4 import BeautifulSoup
    from markdownify import markdownify

    # Remove non-content elements before conversion.
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "meta", "link", "nav", "footer", "header"]):
        tag.decompose()

    md: str = markdownify(str(soup), heading_style="ATX", bullets="-")

    # Collapse runs of 3+ blank lines down to 2.
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def _html_to_text(html: str) -> str:
    """Convert HTML to plain text, stripping all tags."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()

    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def _truncate(content: str, limit: int) -> tuple[str, bool]:
    """Truncate content to *limit* characters if it exceeds that length."""
    if len(content) <= limit:
        return content, False
    return content[:limit] + "\n\n[Content truncated...]", True


def _extract_title(html: str) -> str | None:
    """Extract the HTML ``<title>`` content when present."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
        return title or None
    return None


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------


@tool
async def fetch(
    url: t.Annotated[str, "The URL to fetch content from"],
    *,
    format: t.Annotated[
        t.Literal["markdown", "text", "html"],
        "Output format: 'markdown' (default — converts HTML to markdown), "
        "'text' (plain text, tags stripped), or 'html' (raw HTML).",
    ] = "markdown",
    timeout: t.Annotated[int, "Request timeout in seconds (max 120)"] = DEFAULT_TIMEOUT,  # noqa: ASYNC109
    headers: t.Annotated[
        dict[str, str] | None, "Custom HTTP headers to send with the request"
    ] = None,
) -> FetchResponse:
    """
    Fetch content from a URL and return it in the requested format.

    - Fetches any HTTP/HTTPS URL and returns the content
    - HTML is converted to **markdown** by default (best for reading docs, articles, etc.)
    - Use ``format="text"`` for plain text extraction (no formatting)
    - Use ``format="html"`` for raw HTML (useful for inspecting structure)
    - Responses larger than 5 MB are rejected; output is capped at ~50 000 characters
    - Follows redirects (up to 5 hops)
    - This tool is **read-only** and does not modify any files

    Usage notes:
      - The URL must start with ``http://`` or ``https://``
      - For JSON APIs, use ``format="text"`` — markdown conversion is for HTML
      - If the page is behind authentication or a paywall, the fetch will likely
        return a login page or an error — check the output
      - IMPORTANT: if another tool offers better web fetching capabilities for
        the specific task, prefer that tool over this one
    """
    return await _fetch_single_url(url, format=format, timeout=timeout, headers=headers)


async def _fetch_single_url(
    url: str,
    *,
    format: t.Literal["markdown", "text", "html"] = "markdown",
    timeout: int = DEFAULT_TIMEOUT,  # noqa: ASYNC109
    headers: dict[str, str] | None = None,
) -> FetchResponse:
    """Fetch a single URL and return the normalized response payload."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid URL scheme: {parsed.scheme!r}. Use http:// or https://.")

    effective_timeout = min(timeout, MAX_TIMEOUT)

    logger.info(f"Fetching: {url} (format={format})")

    request_headers: dict[str, str] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/143.0.0.0 Safari/537.36"
        ),
        "Accept": _ACCEPT_HEADERS.get(format, "*/*"),
        "Accept-Language": "en-US,en;q=0.9",
    }
    if headers:
        request_headers.update(headers)

    async with httpx.AsyncClient(
        timeout=effective_timeout,
        follow_redirects=True,
        max_redirects=5,
    ) as client:
        response = await client.get(url, headers=request_headers)
        response.raise_for_status()

        # Enforce size limit.
        raw = response.content
        if len(raw) > MAX_RESPONSE_SIZE:
            raise ValueError(f"Response too large ({len(raw)} bytes, limit is {MAX_RESPONSE_SIZE})")

        content_type = response.headers.get("content-type", "")
        raw_text = response.text

        logger.debug(f"Fetched {len(raw)} bytes, content-type: {content_type}")

        is_html = "html" in content_type.lower()
        title = _extract_title(raw_text) if is_html else None
        content = raw_text

        if format == "markdown" and is_html:
            content = _html_to_markdown(content)
        elif format == "text" and is_html:
            content = _html_to_text(content)
        # format == "html" or non-HTML content → return as-is.

        content, truncated = _truncate(content, MAX_OUTPUT_LENGTH)

        return {
            "success": True,
            "url": url,
            "final_url": str(response.url),
            "status_code": response.status_code,
            "content_type": content_type,
            "format": format,
            "title": title,
            "content_length": len(content),
            "truncated": truncated,
            "content": content,
        }
