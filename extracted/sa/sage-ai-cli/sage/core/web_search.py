"""Free web search via DuckDuckGo's HTML endpoint.

No API key, no account, no rate limit ceremony. The HTML endpoint
(https://html.duckduckgo.com/html/) is intended for browsers that don't
run JS — perfect for scraping titles/URLs/snippets.

Used in tandem with WebFetchTool: SEARCH_WEB returns ranked URLs, then the
agent calls WEB_FETCH on the most promising one to read the page.

This module deliberately does NOT live in tools.py to keep that file's
weight down; it's wired into ToolExecutor by importing from here.
"""

from __future__ import annotations

import re
import urllib.parse
from dataclasses import dataclass

__all__ = ["SearchResult", "WebSearchTool", "search_web"]


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str

    def to_text(self) -> str:
        return f"• {self.title}\n  {self.url}\n  {self.snippet}"


class WebSearchTool:
    """DuckDuckGo HTML scrape — no API key required."""

    ENDPOINT = "https://html.duckduckgo.com/html/"
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )

    def __init__(self, timeout: float = 8.0):
        self.timeout = timeout

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        """Return up to `limit` results. Empty list on any failure (caller decides)."""
        if not query.strip():
            return []
        try:
            import httpx
        except ImportError:
            return []

        params = {"q": query, "kl": "us-en"}
        try:
            with httpx.Client(
                timeout=self.timeout,
                headers={"User-Agent": self.USER_AGENT},
                follow_redirects=True,
            ) as client:
                resp = client.post(self.ENDPOINT, data=params)
                if resp.status_code != 200:
                    return []
                return _parse_ddg_html(resp.text, limit=limit)
        except Exception:
            return []


# DuckDuckGo's HTML markup uses class="result" containers with
# class="result__title" (anchor) and class="result__snippet" (div).
_RESULT_RE = re.compile(
    r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>'
    r'.*?'
    r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
    re.DOTALL,
)
_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(s: str) -> str:
    return _TAG_RE.sub("", s).strip()


def _unwrap_ddg_redirect(url: str) -> str:
    """DDG sometimes wraps results in /l/?uddg=<encoded>. Unwrap to real URL."""
    if "duckduckgo.com/l/" not in url and not url.startswith("//duckduckgo.com/l/"):
        return url
    parsed = urllib.parse.urlparse(url if url.startswith("http") else "https:" + url)
    qs = urllib.parse.parse_qs(parsed.query)
    real = qs.get("uddg", [None])[0]
    return urllib.parse.unquote(real) if real else url


def _parse_ddg_html(html: str, limit: int) -> list[SearchResult]:
    results: list[SearchResult] = []
    for m in _RESULT_RE.finditer(html):
        href, title_html, snippet_html = m.groups()
        url = _unwrap_ddg_redirect(href)
        title = _strip_html(title_html)
        snippet = _strip_html(snippet_html)
        if not (url and title):
            continue
        results.append(SearchResult(title=title, url=url, snippet=snippet))
        if len(results) >= limit:
            break
    return results


def search_web(query: str, limit: int = 5) -> list[SearchResult]:
    """Module-level convenience for the simple case."""
    return WebSearchTool().search(query, limit=limit)
