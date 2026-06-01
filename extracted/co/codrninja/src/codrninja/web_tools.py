"""Web fetch and search helpers for codrninja."""

from __future__ import annotations

import os
import re
import time
from html import unescape
from threading import Lock
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote_plus, urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - optional dependency fallback
    BeautifulSoup = None


CACHE_TTL_SECONDS = 300
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW_SECONDS = 60
DEFAULT_USER_AGENT = "codrninja/0.6.0-dev3 (+https://github.com/20ZollCoder/codrninja)"
SEARXNG_URL = os.environ.get("CODRNINJA_SEARXNG_URL", "http://localhost:8888")
EXA_URL = "https://api.exa.ai/search"

_CACHE: Dict[Tuple[Any, ...], Tuple[float, Any]] = {}
_CACHE_LOCK = Lock()
_RATE_LIMIT_STATE: Dict[str, List[float]] = {}
_RATE_LIMIT_LOCK = Lock()
_ROBOTS_CACHE: Dict[str, RobotFileParser] = {}
_ROBOTS_LOCK = Lock()


class WebToolError(Exception):
    """Raised when a web tool fails."""


def web_enabled() -> bool:
    """Return whether web access is enabled."""
    return os.environ.get("NO_WEB", "").strip().lower() not in {"1", "true", "yes", "on"}


def _check_web_enabled():
    if not web_enabled():
        raise WebToolError("Web access is disabled by NO_WEB")


def _cache_get(key: Tuple[Any, ...]) -> Optional[Any]:
    with _CACHE_LOCK:
        cached = _CACHE.get(key)
        if not cached:
            return None
        expires_at, value = cached
        if time.time() >= expires_at:
            _CACHE.pop(key, None)
            return None
        return value


def _cache_set(key: Tuple[Any, ...], value: Any, ttl: int = CACHE_TTL_SECONDS):
    with _CACHE_LOCK:
        _CACHE[key] = (time.time() + ttl, value)


def _rate_limit(source: str):
    with _RATE_LIMIT_LOCK:
        now = time.time()
        timestamps = [t for t in _RATE_LIMIT_STATE.get(source, []) if now - t < RATE_LIMIT_WINDOW_SECONDS]
        if len(timestamps) >= RATE_LIMIT_REQUESTS:
            raise WebToolError(f"Rate limit exceeded for {source}")
        timestamps.append(now)
        _RATE_LIMIT_STATE[source] = timestamps


def _session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
    return session


def _truncate_text(text: str, max_length: Optional[int] = None) -> str:
    text = text.strip()
    if max_length and max_length > 0 and len(text) > max_length:
        return text[:max_length].rstrip() + "\n... [truncated]"
    return text


def _clean_text(text: str) -> str:
    text = unescape(text or "")
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def check_robots_txt(url: str) -> bool:
    """Check whether fetching the URL is allowed by robots.txt."""
    _check_web_enabled()
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise WebToolError("Invalid URL")

    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    with _ROBOTS_LOCK:
        parser = _ROBOTS_CACHE.get(robots_url)
        if parser is None:
            parser = RobotFileParser()
            parser.set_url(robots_url)
            try:
                parser.read()
            except Exception:
                parser = None
            _ROBOTS_CACHE[robots_url] = parser  # type: ignore[assignment]

    if parser is None:
        return True

    try:
        return parser.can_fetch(DEFAULT_USER_AGENT, url)
    except Exception:
        return True


def fetch_url(url: str, timeout: int = 10) -> str:
    """Fetch raw HTML with retries and status validation."""
    _check_web_enabled()
    if not check_robots_txt(url):
        raise WebToolError(f"Fetching blocked by robots.txt: {url}")

    cache_key = ("fetch_raw", url, timeout)
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    _rate_limit("fetch")
    last_error = None
    session = _session()
    for attempt in range(3):
        try:
            response = session.get(url, timeout=timeout)
            if response.status_code != 200:
                raise WebToolError(f"HTTP {response.status_code} for {url}")
            html = response.text
            _cache_set(cache_key, html)
            return html
        except requests.Timeout as exc:
            last_error = f"Request timed out for {url}"
        except requests.RequestException as exc:
            last_error = str(exc)
        if attempt < 2:
            time.sleep(0.5 * (attempt + 1))
    raise WebToolError(last_error or f"Failed to fetch {url}")


def extract_text(html: str) -> str:
    """Convert HTML to readable text."""
    if BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text("\n")
        return _clean_text(text)

    text = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return _clean_text(text)


def search_exa(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """Search using Exa if an API key is configured."""
    _check_web_enabled()
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        raise WebToolError("EXA_API_KEY not configured")

    num_results = max(1, min(num_results, 10))
    cache_key = ("search_exa", query, num_results)
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    _rate_limit("exa")
    session = _session()
    response = session.post(
        EXA_URL,
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
        json={"query": query, "numResults": num_results},
        timeout=10,
    )
    if response.status_code != 200:
        raise WebToolError(f"Exa returned HTTP {response.status_code}")

    data = response.json()
    items = data.get("results") or data.get("data") or []
    results = []
    for item in items[:num_results]:
        results.append(
            {
                "title": (item.get("title") or "").strip() or item.get("url", ""),
                "url": item.get("url", ""),
                "snippet": _clean_text(item.get("text") or item.get("snippet") or "")[:500],
            }
        )
    _cache_set(cache_key, results)
    return results


def search_searxng(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """Search using a SearXNG instance."""
    _check_web_enabled()
    num_results = max(1, min(num_results, 10))
    cache_key = ("search_searxng", query, num_results, SEARXNG_URL)
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    _rate_limit("searxng")
    session = _session()
    response = session.get(
        f"{SEARXNG_URL.rstrip('/')}/search",
        params={"q": query, "format": "json", "language": "en"},
        timeout=10,
    )
    if response.status_code != 200:
        raise WebToolError(f"SearXNG returned HTTP {response.status_code}")

    data = response.json()
    items = data.get("results", [])
    results = []
    for item in items[:num_results]:
        results.append(
            {
                "title": (item.get("title") or "").strip(),
                "url": item.get("url") or item.get("link") or "",
                "snippet": _clean_text(item.get("content") or item.get("snippet") or "")[:500],
            }
        )
    if not results:
        raise WebToolError("SearXNG returned no results")
    _cache_set(cache_key, results)
    return results


def search_duckduckgo(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """Fallback search using DuckDuckGo HTML."""
    _check_web_enabled()
    num_results = max(1, min(num_results, 10))
    cache_key = ("search_ddg", query, num_results)
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    _rate_limit("duckduckgo")
    session = _session()
    response = session.get(
        "https://html.duckduckgo.com/html/",
        params={"q": query},
        timeout=10,
    )
    if response.status_code != 200:
        raise WebToolError(f"DuckDuckGo returned HTTP {response.status_code}")

    html = response.text
    results = []
    if BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        for result in soup.select("div.result")[:num_results]:
            link = result.select_one("a.result__a")
            snippet = result.select_one("a.result__snippet, div.result__snippet")
            if not link:
                continue
            href = link.get("href", "")
            results.append(
                {
                    "title": _clean_text(link.get_text(" ")),
                    "url": href,
                    "snippet": _clean_text(snippet.get_text(" ") if snippet else "")[:500],
                }
            )
    else:
        matches = re.findall(
            r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?(?:result__snippet[^>]*>(.*?)</)',
            html,
            re.IGNORECASE | re.DOTALL,
        )
        for href, title, snippet in matches[:num_results]:
            results.append(
                {
                    "title": _clean_text(re.sub(r"<[^>]+>", " ", title)),
                    "url": href,
                    "snippet": _clean_text(re.sub(r"<[^>]+>", " ", snippet))[:500],
                }
            )

    if not results:
        raise WebToolError("DuckDuckGo returned no results")
    _cache_set(cache_key, results)
    return results


def search_web(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """Search with smart fallback chain: Exa -> SearXNG -> DuckDuckGo."""
    _check_web_enabled()
    num_results = max(1, min(num_results, 10))
    errors = []

    for searcher in (search_exa, search_searxng, search_duckduckgo):
        try:
            results = searcher(query, num_results)
            if results:
                return results
        except Exception as exc:
            errors.append(f"{searcher.__name__}: {exc}")

    raise WebToolError("All search providers failed: " + " | ".join(errors))


def fetch_web_text(url: str, timeout: int = 10, max_length: int = 10000) -> str:
    """Fetch a URL and return cleaned text."""
    html = fetch_url(url, timeout=timeout)
    text = extract_text(html)
    return _truncate_text(text, max_length=max_length)
