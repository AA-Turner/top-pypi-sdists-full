from __future__ import annotations

import asyncio

import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from typing import Literal
from urllib.parse import urljoin, urlparse

import httpx
from pydantic import BaseModel, Field

from matrx_scraper.utils.url import validate_public_http_url

_MAX_SITEMAP_BYTES = 20 * 1024 * 1024

# Default sync bounds. Sitemap graphs in the wild contain cycles, absurd
# index nesting, and multi-million URL dumps — every walk is hard-bounded.
DEFAULT_MAX_SITEMAP_DOCS = 500
DEFAULT_MAX_SITEMAP_DEPTH = 3
DEFAULT_MAX_SITEMAP_URLS = 50_000
# All sitemap requests target the one site host; this is the per-host limit
# for the breadth-first concurrent fetch waves.
DEFAULT_SITEMAP_FETCH_CONCURRENCY = 8

SitemapKind = Literal["sitemapindex", "urlset", "unknown"]


class SitemapUrlEntry(BaseModel):
    """One <url> entry from a urlset document."""

    loc: str
    lastmod: datetime | None = None
    changefreq: str | None = None
    priority: float | None = None


class ParsedSitemap(BaseModel):
    """Result of parsing one sitemap XML document."""

    kind: Literal["sitemapindex", "urlset"]
    entries: list[SitemapUrlEntry] = Field(default_factory=list)
    child_locs: list[str] = Field(default_factory=list)


class SitemapDocumentResult(BaseModel):
    """One fetched sitemap document, successful or not."""

    url: str
    kind: SitemapKind
    parent_url: str | None = None
    status_code: int | None = None
    url_count: int = 0
    child_count: int = 0
    entries: list[SitemapUrlEntry] = Field(default_factory=list)
    fetch_error: str | None = None


class SitemapCrawl(BaseModel):
    """Bounded walk over a site's sitemap graph."""

    documents: list[SitemapDocumentResult] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    truncated: bool = False
    truncation_reasons: list[str] = Field(default_factory=list)

    @property
    def url_total(self) -> int:
        return sum(doc.url_count for doc in self.documents if doc.kind == "urlset")


async def _safe_get(
    client: httpx.AsyncClient,
    url: str,
    *,
    max_redirects: int = 5,
) -> tuple[str, httpx.Response]:
    current = url
    for _ in range(max_redirects + 1):
        await validate_public_http_url(current)
        response = await client.get(current)
        if response.status_code not in {301, 302, 303, 307, 308}:
            return current, response
        location = response.headers.get("location")
        if not location:
            return current, response
        current = urljoin(current, location)
    raise RuntimeError(f"too many redirects while fetching {url}")


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _parse_lastmod(raw: str | None) -> datetime | None:
    """Parse a W3C datetime / date. Cosmetic field — degrade to None, never raise."""

    if not raw:
        return None
    text = raw.strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed


def _parse_priority(raw: str | None) -> float | None:
    """Cosmetic field — degrade to None, never raise."""

    if not raw:
        return None
    try:
        value = float(raw.strip())
    except ValueError:
        return None
    if value != value:  # NaN
        return None
    return min(1.0, max(0.0, value))


def parse_sitemap_document(content: bytes) -> ParsedSitemap:
    """Parse one sitemap XML document into typed entries.

    Raises ``ValueError`` on oversized, malformed, or non-sitemap XML —
    callers record the failure loudly on the sitemap row; they never
    silently skip it.
    """

    if len(content) > _MAX_SITEMAP_BYTES:
        raise ValueError(f"sitemap exceeds {_MAX_SITEMAP_BYTES} bytes")
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise ValueError(f"malformed sitemap XML: {exc}") from exc
    kind = _local_name(root.tag)
    if kind not in {"sitemapindex", "urlset"}:
        raise ValueError(f"unsupported sitemap root element: {kind}")

    entries: list[SitemapUrlEntry] = []
    child_locs: list[str] = []
    for element in root:
        name = _local_name(element.tag)
        if name not in {"url", "sitemap"}:
            continue
        loc: str | None = None
        lastmod: str | None = None
        changefreq: str | None = None
        priority: str | None = None
        for child in element:
            child_name = _local_name(child.tag)
            text = (child.text or "").strip()
            if child_name == "loc" and text:
                loc = text
            elif child_name == "lastmod":
                lastmod = text
            elif child_name == "changefreq":
                changefreq = text
            elif child_name == "priority":
                priority = text
        if not loc:
            continue
        if kind == "sitemapindex":
            child_locs.append(loc)
        else:
            entries.append(
                SitemapUrlEntry(
                    loc=loc,
                    lastmod=_parse_lastmod(lastmod),
                    changefreq=(changefreq or None),
                    priority=_parse_priority(priority),
                )
            )
    return ParsedSitemap(
        kind="sitemapindex" if kind == "sitemapindex" else "urlset",
        entries=entries,
        child_locs=child_locs,
    )


async def crawl_sitemap_documents(
    base_url: str,
    *,
    user_agent: str = "MatrxScraperBot/0.1 (+https://aimatrx.com)",
    request_timeout: float = 15.0,
    max_docs: int = DEFAULT_MAX_SITEMAP_DOCS,
    max_depth: int = DEFAULT_MAX_SITEMAP_DEPTH,
    max_urls: int = DEFAULT_MAX_SITEMAP_URLS,
    fetch_concurrency: int = DEFAULT_SITEMAP_FETCH_CONCURRENCY,
) -> SitemapCrawl:
    """Discover and fetch a site's sitemap graph with hard bounds.

    Discovery starts from ``robots.txt`` ``Sitemap:`` lines plus the
    ``/sitemap.xml`` and ``/sitemap_index.xml`` conventions. Sitemap indexes
    expand recursively up to ``max_depth`` levels, ``max_docs`` documents,
    and ``max_urls`` total urlset entries; tripping any bound sets
    ``truncated`` and records the reason loudly.

    Documents are fetched breadth-first in concurrent waves bounded by
    ``fetch_concurrency`` (every request targets the one site host, so this
    is the per-host limit). Responses are processed sequentially in wave
    order, so the bounds stay deterministic and parents always precede
    their children in ``crawl.documents``.

    A candidate that returns 404/410 is simply absent — no document row and
    no error. Any other failure produces a document row with ``fetch_error``
    (so the sitemap's row keeps its identity and records the failure) plus
    an error string.
    """

    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("base_url must be an absolute HTTP(S) URL")
    origin = f"{parsed.scheme}://{parsed.netloc}"
    candidates = [f"{origin}/sitemap.xml", f"{origin}/sitemap_index.xml"]
    crawl = SitemapCrawl()
    urls_remaining = max_urls

    def _truncate(reason: str) -> None:
        crawl.truncated = True
        if reason not in crawl.truncation_reasons:
            crawl.truncation_reasons.append(reason)

    async with httpx.AsyncClient(
        timeout=request_timeout,
        follow_redirects=False,
        headers={"User-Agent": user_agent},
    ) as client:
        try:
            _, robots = await _safe_get(client, f"{origin}/robots.txt")
            if 200 <= robots.status_code < 300:
                for line in robots.text.splitlines():
                    directive = line.strip()
                    if directive.lower().startswith("sitemap:"):
                        candidate = directive.split(":", 1)[1].strip()
                        if candidate:
                            candidates.append(urljoin(origin, candidate))
        except Exception as exc:
            crawl.errors.append(f"robots.txt: {type(exc).__name__}: {exc}")

        seen: set[str] = set()
        fetched_docs = 0
        semaphore = asyncio.Semaphore(max(1, fetch_concurrency))

        async def _bounded_get(url: str) -> tuple[str, httpx.Response]:
            async with semaphore:
                return await _safe_get(client, url)

        # (url, parent_url, depth) frontier. Fetch each wave concurrently,
        # process results sequentially so bound accounting stays exact.
        frontier: list[tuple[str, str | None, int]] = [
            (candidate, None, 0) for candidate in dict.fromkeys(candidates)
        ]
        while frontier:
            if urls_remaining <= 0:
                _truncate(f"sitemap URL limit reached ({max_urls})")
                break
            wave: list[tuple[str, str | None, int]] = []
            for url, parent_url, depth in frontier:
                if url in seen:
                    continue
                if fetched_docs + len(wave) >= max_docs:
                    _truncate(f"sitemap document limit reached ({max_docs})")
                    break
                seen.add(url)
                wave.append((url, parent_url, depth))
            frontier = []
            if not wave:
                break
            results = await asyncio.gather(
                *(_bounded_get(url) for url, _, _ in wave),
                return_exceptions=True,
            )
            for (url, parent_url, depth), result in zip(wave, results, strict=True):
                status_code: int | None = None
                try:
                    if isinstance(result, BaseException):
                        raise result
                    final_url, response = result
                    status_code = response.status_code
                    if response.status_code in {404, 410}:
                        continue
                    fetched_docs += 1
                    if not (200 <= response.status_code < 300):
                        raise RuntimeError(f"HTTP {response.status_code}")
                    parsed_doc = parse_sitemap_document(response.content)
                    entries = parsed_doc.entries
                    if parsed_doc.kind == "urlset" and len(entries) > urls_remaining:
                        entries = entries[:urls_remaining]
                        _truncate(f"sitemap URL limit reached ({max_urls})")
                    urls_remaining -= len(entries)
                    document = SitemapDocumentResult(
                        url=final_url,
                        kind=parsed_doc.kind,
                        parent_url=parent_url,
                        status_code=response.status_code,
                        url_count=len(entries),
                        child_count=len(parsed_doc.child_locs),
                        entries=entries,
                    )
                    crawl.documents.append(document)
                    if parsed_doc.kind == "sitemapindex":
                        if depth >= max_depth:
                            if parsed_doc.child_locs:
                                _truncate(f"sitemap index depth limit reached ({max_depth})")
                            continue
                        for child in parsed_doc.child_locs:
                            if urls_remaining <= 0:
                                _truncate(f"sitemap URL limit reached ({max_urls})")
                                break
                            frontier.append((urljoin(final_url, child), final_url, depth + 1))
                except Exception as exc:
                    crawl.documents.append(
                        SitemapDocumentResult(
                            url=url,
                            kind="unknown",
                            parent_url=parent_url,
                            status_code=status_code,
                            fetch_error=f"{type(exc).__name__}: {exc}"[:2_000],
                        )
                    )
                    crawl.errors.append(f"{url}: {type(exc).__name__}: {exc}")

    return crawl


__all__ = [
    "DEFAULT_MAX_SITEMAP_DEPTH",
    "DEFAULT_SITEMAP_FETCH_CONCURRENCY",
    "DEFAULT_MAX_SITEMAP_DOCS",
    "DEFAULT_MAX_SITEMAP_URLS",
    "ParsedSitemap",
    "SitemapCrawl",
    "SitemapDocumentResult",
    "SitemapKind",
    "SitemapUrlEntry",
    "crawl_sitemap_documents",
    "parse_sitemap_document",
]
