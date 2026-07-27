"""Pluggable web-search backend.

`core/web_search.py` ships a DuckDuckGo HTML scraper as the default. This
module abstracts that into a `SearchProvider` interface and ships three
concrete backends:

  - DuckDuckGoBackend   (default; no API key)
  - BraveBackend        (uses BRAVE_API_KEY env var)
  - SearXNGBackend      (self-hosted; uses SAGE_SEARXNG_URL env var)

The factory `make_provider(name)` lets the rest of sage swap backends
via config without touching call sites.
"""

from __future__ import annotations

import os
import urllib.parse
from dataclasses import dataclass

from sage.core.web_search import SearchResult, WebSearchTool

__all__ = [
    "SearchProvider",
    "DuckDuckGoBackend",
    "BraveBackend",
    "SearXNGBackend",
    "make_provider",
]


class SearchProvider:
    name: str = "abstract"

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        raise NotImplementedError


class DuckDuckGoBackend(SearchProvider):
    name = "duckduckgo"

    def __init__(self, timeout: float = 8.0):
        self._tool = WebSearchTool(timeout=timeout)

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        return self._tool.search(query, limit=limit)


class BraveBackend(SearchProvider):
    """Brave Search API. Free tier: 2k queries/month."""
    name = "brave"
    ENDPOINT = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self, api_key: str | None = None, timeout: float = 8.0):
        self.api_key = api_key or os.environ.get("BRAVE_API_KEY", "")
        self.timeout = timeout

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        if not self.api_key:
            return []
        try:
            import httpx
        except ImportError:
            return []
        try:
            with httpx.Client(timeout=self.timeout) as client:
                r = client.get(
                    self.ENDPOINT,
                    params={"q": query, "count": limit},
                    headers={
                        "Accept": "application/json",
                        "X-Subscription-Token": self.api_key,
                    },
                )
                if r.status_code != 200:
                    return []
                data = r.json()
        except Exception:
            return []
        results: list[SearchResult] = []
        for item in (data.get("web", {}).get("results") or [])[:limit]:
            results.append(SearchResult(
                title=item.get("title") or "",
                url=item.get("url") or "",
                snippet=item.get("description") or "",
            ))
        return results


class SearXNGBackend(SearchProvider):
    """Self-hosted SearXNG instance. Set SAGE_SEARXNG_URL to your endpoint."""
    name = "searxng"

    def __init__(self, base_url: str | None = None, timeout: float = 8.0):
        self.base_url = (base_url or os.environ.get("SAGE_SEARXNG_URL", "")).rstrip("/")
        self.timeout = timeout

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        if not self.base_url:
            return []
        try:
            import httpx
        except ImportError:
            return []
        try:
            with httpx.Client(timeout=self.timeout) as client:
                r = client.get(
                    f"{self.base_url}/search",
                    params={"q": query, "format": "json"},
                )
                if r.status_code != 200:
                    return []
                data = r.json()
        except Exception:
            return []
        results: list[SearchResult] = []
        for item in (data.get("results") or [])[:limit]:
            results.append(SearchResult(
                title=item.get("title") or "",
                url=item.get("url") or "",
                snippet=item.get("content") or "",
            ))
        return results


def make_provider(name: str = "duckduckgo") -> SearchProvider:
    name = name.lower()
    if name in ("duckduckgo", "ddg"):
        return DuckDuckGoBackend()
    if name == "brave":
        return BraveBackend()
    if name == "searxng":
        return SearXNGBackend()
    return DuckDuckGoBackend()
