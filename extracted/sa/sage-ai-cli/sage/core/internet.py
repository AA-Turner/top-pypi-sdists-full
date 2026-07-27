"""Unified internet facade for Sage.

Sage's existing internet capabilities are scattered (WebFetchTool in
core/tools.py, web_search.py, grounded_search.py, the model catalog
fetcher, etc.). This module is the single import-point any caller in
Sage can use for "do an internet thing safely".

Provides:
  - `Internet.search(query)`            — ranked URL list (DuckDuckGo)
  - `Internet.fetch(url)`               — page content (HTML stripped)
  - `Internet.search_and_summarize(q)`  — search top-K, fetch each, return
                                          concatenated text bounded by chars
  - `Internet.is_blocked(url)`          — share the SSRF check from WebFetchTool
  - `Internet.docs_for(library)`        — quick "find docs for X" helper

All operations honour the same SSRF/scheme/host blocklist already enforced
by WebFetchTool — there is no path here that bypasses safety. The point
is *centralization*, not loosening.

Intended usage in the agent loop:
    from sage.core.internet import Internet
    inet = Internet()
    pages = inet.search_and_summarize("react useEffect cleanup pattern", k=3)
    # → injected into model context as ground truth
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sage.core.tools import ToolContext, ToolResult, ToolStatus, WebFetchTool
from sage.core.web_search import SearchResult, WebSearchTool

__all__ = ["FetchedPage", "Internet"]


@dataclass
class FetchedPage:
    url: str
    title: str
    text: str
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


class Internet:
    def __init__(self, *, search_timeout: float = 8.0, fetch_timeout: int = 10,
                 cwd: Path | None = None):
        self._search = WebSearchTool(timeout=search_timeout)
        # WebFetchTool's ToolContext needs a cwd for path-policy checks even
        # though fetch() doesn't use it. Default to the actual cwd.
        self._fetcher = WebFetchTool(ToolContext(cwd=cwd or Path.cwd()))
        self._fetch_timeout = fetch_timeout

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        return self._search.search(query, limit=limit)

    def fetch(self, url: str) -> FetchedPage:
        result: ToolResult = self._fetcher.fetch(url, timeout=self._fetch_timeout)
        if result.status != ToolStatus.SUCCESS:
            return FetchedPage(url=url, title="", text="", error=result.error or "fetch failed")
        text = result.output or ""
        # Crude title extraction from the stripped text (first non-empty line).
        title = ""
        for line in text.splitlines():
            line = line.strip()
            if line:
                title = line[:200]
                break
        return FetchedPage(url=url, title=title, text=text)

    def is_blocked(self, url: str) -> tuple[bool, str]:
        return self._fetcher._is_blocked_url(url)

    def search_and_summarize(
        self, query: str, *, k: int = 3, max_chars_per_page: int = 4000,
    ) -> str:
        """Search → fetch top-K → return concatenated text suitable for prompt context.

        Returns empty string if everything fails (caller decides whether to
        inject "no internet results" or proceed without).
        """
        results = self.search(query, limit=k)
        if not results:
            return ""
        sections: list[str] = [f"## INTERNET SEARCH: {query!r}\n"]
        for r in results:
            page = self.fetch(r.url)
            text = page.text[:max_chars_per_page] if page.ok else f"[fetch error: {page.error}]"
            sections.append(
                f"\n### {r.title}\n{r.url}\n\n{text}\n"
            )
        return "\n".join(sections)

    def docs_for(self, library: str, *, version_hint: str = "") -> FetchedPage | None:
        """Convenience: 'find docs for <library>' → first sensible page.

        We bias toward official docs by tacking 'docs' onto the query and
        skipping Stack Overflow / GitHub if a docs site shows up.
        """
        q = f"{library} {version_hint} official documentation".strip()
        results = self.search(q, limit=8)
        for r in results:
            url_lower = r.url.lower()
            if any(host in url_lower for host in [
                "docs.", "/docs/", ".readthedocs.io", "developer.mozilla.org",
            ]):
                return self.fetch(r.url)
        if results:
            return self.fetch(results[0].url)
        return None
