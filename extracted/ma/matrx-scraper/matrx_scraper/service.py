"""
ScrapeService — FastAPI adapter that connects the router to matrx_scraper.

This replaces scraper/services_v2/service.py.  It preserves the exact SSE
envelope the frontend already consumes:

  Search results:
    { "response_type": "search_results", "metadata": {"keyword": "..."}, "results": [...] }

  Scraped pages (batch):
    { "response_type": "fetch_results", "metadata": {"execution_time_ms": 123.4}, "results": [...] }

  Scraped pages (streaming — one per send_data call):
    same envelope with results containing a single page dict

Key design choices
──────────────────
• scrape_many_stream() is always used for scraping — pages are emitted the
  moment they are ready, never buffered.
• All URLs in a batch are launched in parallel (semaphore-capped); pages from
  different sites never wait on each other.
• Boolean field-flag filtering (get_overview, get_links, …) is applied here
  as a post-processing step so the package core stays generic.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal

from matrx_connect.context.data_types import FetchResultsData, SearchErrorData, SearchResultsData
from matrx_connect.context.events import InfoPayload
from matrx_utils import capture_error, supervised_task, vcprint

from matrx_scraper._ext import get_ext, has_ext
from matrx_scraper.db.models_scraper import ScrapeFailureLog, ScrapeRetryQueue
from matrx_scraper.orchestrator import ScrapeResult, scrape_many_stream
from matrx_scraper.scrape_options import ScrapeOptions, apply_field_flags
from matrx_scraper.search.search import async_brave_search

# Historical private name — this module's own call sites still read
# `_apply_field_flags`. The definition now lives in `scrape_options` so
# consumers without matrx-connect/matrx-orm can use it too.
_apply_field_flags = apply_field_flags

# ---------------------------------------------------------------------------
# Wire-format dataclasses (match frontend TypeScript types exactly)
# ---------------------------------------------------------------------------


@dataclass
class SearchResultItem:
    keyword: str
    type: Literal["web", "news", "all"]
    title: str
    url: str
    description: str
    source: str | None = None
    age: str | None = None
    thumbnail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class SearchMetadata:
    keyword: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class ScrapeMetadata:
    execution_time_ms: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


class SearchType(str, Enum):
    WEB = "web"
    NEWS = "news"
    ALL = "all"


async def _fire_and_forget_failure_log(result: ScrapeResult) -> None:
    """Log failed scrapes to DB (matrx-orm). Never blocks the stream."""
    try:
        from matrx_scraper.utils.url import extract_domain

        domain_name = extract_domain(result.url)
        failure_reason = result.failure_reason or "unknown"

        await ScrapeFailureLog.create(
            target_url=result.url,
            domain_name=domain_name,
            failure_reason=failure_reason,
            failure_category=failure_reason,
            status_code=result.status_code or None,
            proxy_used=True,
            attempt_count=1,
        )

        RETRYABLE = frozenset(
            {"cloudflare_block", "blocked", "bad_status", "request_error", "proxy_error"}
        )
        if failure_reason in RETRYABLE:
            existing = await ScrapeRetryQueue.filter(
                target_url=result.url, status__in=["pending", "claimed"]
            ).exists()
            if not existing:
                await ScrapeRetryQueue.create(
                    target_url=result.url,
                    domain_name=domain_name,
                    failure_reason=failure_reason,
                    tier="desktop",
                )
    except Exception as exc:
        # Fire-and-forget by design (must never block the scrape stream) — but
        # never SILENT: a dropped failure-log / retry-enqueue write screams
        # instead of vanishing (never-swallow-writes doctrine).
        vcprint(
            f"[ScrapeService] failure-log/retry-enqueue write dropped (best-effort) "
            f"for {result.url}: {type(exc).__name__}: {exc}",
            color="red",
        )
        await capture_error(
            exc,
            kind="scrape_failure_persistence_failed",
            context={"url": result.url, "failure_reason": result.failure_reason},
        )


# The options container (mirroring ScrapeOptionsBase from the router) is
# re-exported above from `matrx_scraper.scrape_options` — importing it from
# here keeps working for every existing caller.


# ---------------------------------------------------------------------------
# ScrapeService
# ---------------------------------------------------------------------------


class ScrapeService:
    """
    Drop-in replacement for scraper.services_v2.service.ScrapeService.

    Usage::

        service = ScrapeService(emitter=emitter)
        service.urls = request.urls
        service.use_cache = request.use_cache
        service.options = ScrapeOptions(get_text_data=True, get_links=True, ...)
        await service.quick_scrape_stream()
    """

    def __init__(self, emitter=None):
        self.emitter = emitter
        self.urls: list[str] = []
        self.use_cache: bool = True
        self.options: ScrapeOptions = ScrapeOptions()

        # Search-related state
        self.keyword: str | None = None
        self.keywords: list[str] = []
        self.country_code: str = "all"
        self.total_results_per_keyword: int = 10
        self.max_page_read: int = 10
        self.search_type: str = "all"

    def _resolve_cache(self) -> Any | None:
        """The L2 page cache for this scrape, or ``None``.

        ``use_cache`` comes straight off the request; the cache object itself
        is the host-injected ``cache`` ext (``configure_ext(cache=...)`` —
        aidream wires ``TwoTierCache``). Standalone installs without a cache
        ext simply scrape uncached — same behaviour as before.
        """
        if not self.use_cache:
            return None
        if not has_ext("cache"):
            return None
        return get_ext("cache")

    # ------------------------------------------------------------------
    # Quick-scrape — always streaming, results emitted as they finish
    # ------------------------------------------------------------------

    async def quick_scrape_stream(self) -> None:
        """
        Scrape all URLs in parallel, emitting each page the moment it is
        ready.  The caller receives one ``fetch_results`` envelope per page.
        """
        start = time.monotonic()
        async for result in scrape_many_stream(
            self.urls, use_proxy=True, cache=self._resolve_cache()
        ):
            if not result.success:
                supervised_task(
                    _fire_and_forget_failure_log(result),
                    kind="scrape_failure_logging_task_failed",
                    name="scrape-failure-log",
                    context={"url": result.url},
                )
            page = _apply_field_flags(result.to_dict(), self.options)
            elapsed_ms = round((time.monotonic() - start) * 1000, 1)
            await self.emitter.send_data(
                FetchResultsData(
                    metadata={"execution_time_ms": elapsed_ms},
                    results=[page],
                )
            )

    async def quick_scrape(self) -> None:
        """
        Scrape all URLs in parallel, but collect all results before emitting
        a single batch envelope.  Use quick_scrape_stream() instead wherever
        possible.
        """
        start = time.monotonic()
        results: list[dict[str, Any]] = []
        async for result in scrape_many_stream(
            self.urls, use_proxy=True, cache=self._resolve_cache()
        ):
            results.append(_apply_field_flags(result.to_dict(), self.options))
        elapsed_ms = round((time.monotonic() - start) * 1000, 1)
        await self.emitter.send_data(
            FetchResultsData(
                metadata={"execution_time_ms": elapsed_ms},
                results=results,
            )
        )

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    async def search_keywords(self) -> None:
        """Run each keyword sequentially (to avoid Brave rate limits) and
        stream each keyword's results the moment they arrive."""
        for keyword in self.keywords:
            try:
                await self.emitter.send_info(
                    InfoPayload(
                        code="search_progress",
                        system_message=f'Searching for "{keyword}"',
                        user_message=f'Searching for "{keyword}"...',
                    )
                )
                results = await self._brave_search(keyword)
                await self.emitter.send_data(
                    SearchResultsData(
                        metadata={"keyword": keyword},
                        results=[r.to_dict() for r in results],
                    )
                )
                # Small sleep between keywords to respect rate limits
                await asyncio.sleep(1)
            except Exception as exc:
                vcprint(f"[ScrapeService] search error for '{keyword}': {exc}", color="red")
                await capture_error(
                    exc,
                    kind="scrape_search_failed",
                    context={"keyword": keyword},
                )
                await self.emitter.send_data(
                    SearchErrorData(
                        metadata={"keyword": keyword},
                        error=str(exc),
                    )
                )

    # ------------------------------------------------------------------
    # Search + scrape
    # ------------------------------------------------------------------

    async def search_and_scrape(self) -> None:
        """
        For each keyword: search → stream search results → collect URLs →
        scrape all URLs in parallel, streaming pages as they finish.
        """
        all_urls: list[str] = []

        for keyword in self.keywords:
            try:
                await self.emitter.send_info(
                    InfoPayload(
                        code="search_progress",
                        system_message=f'Searching for "{keyword}"',
                        user_message=f'Searching for "{keyword}"...',
                    )
                )
                items = await self._brave_search(keyword)
                await self.emitter.send_data(
                    SearchResultsData(
                        metadata={"keyword": keyword},
                        results=[r.to_dict() for r in items],
                    )
                )
                all_urls.extend(r.url for r in items)
                await asyncio.sleep(1)
            except Exception as exc:
                vcprint(f"[ScrapeService] search error for '{keyword}': {exc}", color="red")

        if not all_urls:
            return

        await self.emitter.send_info(
            InfoPayload(
                code="search_progress",
                system_message=f"Scraping {len(all_urls)} pages",
                user_message="Reading pages...",
            )
        )

        start = time.monotonic()
        async for result in scrape_many_stream(
            all_urls, use_proxy=True, cache=self._resolve_cache()
        ):
            if not result.success:
                supervised_task(
                    _fire_and_forget_failure_log(result),
                    kind="scrape_failure_logging_task_failed",
                    name="scrape-failure-log",
                    context={"url": result.url},
                )
            page = _apply_field_flags(result.to_dict(), self.options)
            elapsed_ms = round((time.monotonic() - start) * 1000, 1)
            await self.emitter.send_data(
                FetchResultsData(
                    metadata={"execution_time_ms": elapsed_ms},
                    results=[page],
                )
            )

    async def search_and_scrape_limited(self) -> None:
        """
        Search for one keyword, then scrape up to ``max_page_read`` successful
        pages, streaming each page as it arrives.
        """
        fetch_count = min(self.max_page_read * 2, 20)

        await self.emitter.send_info(
            InfoPayload(
                code="search_progress",
                system_message=f'Searching for "{self.keyword}"',
                user_message=f'Searching for "{self.keyword}"...',
            )
        )

        try:
            items = await self._brave_search(self.keyword, count=fetch_count)
        except Exception as exc:
            vcprint(f"[ScrapeService] search error: {exc}", color="red")
            return

        await self.emitter.send_data(
            SearchResultsData(
                metadata={"keyword": self.keyword},
                results=[r.to_dict() for r in items],
            )
        )

        urls = [r.url for r in items]
        if not urls:
            return

        await self.emitter.send_info(
            InfoPayload(
                code="search_progress",
                system_message=f"Scraping up to {self.max_page_read} pages",
                user_message=f"Reading up to {self.max_page_read} pages...",
            )
        )

        successful = 0
        start = time.monotonic()
        async for result in scrape_many_stream(urls, use_proxy=True, cache=self._resolve_cache()):
            if not result.success:
                supervised_task(
                    _fire_and_forget_failure_log(result),
                    kind="scrape_failure_logging_task_failed",
                    name="scrape-failure-log",
                    context={"url": result.url},
                )
                continue
            successful += 1
            page = _apply_field_flags(result.to_dict(), self.options)
            elapsed_ms = round((time.monotonic() - start) * 1000, 1)
            await self.emitter.send_data(
                FetchResultsData(
                    metadata={"execution_time_ms": elapsed_ms},
                    results=[page],
                )
            )
            if successful >= self.max_page_read:
                break

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _brave_search(
        self,
        keyword: str,
        count: int | None = None,
    ) -> list[SearchResultItem]:
        count = count or self.total_results_per_keyword
        try:
            search_type = SearchType(self.search_type)
        except ValueError:
            search_type = SearchType.ALL

        country = self.country_code or "us"
        api_response = await async_brave_search(
            query=keyword,
            count=count,
            country=country,
        )
        if not api_response:
            return []
        return self._process_search(api_response, search_type, keyword)

    @staticmethod
    def _process_search(
        api_response: dict[str, Any],
        search_type: SearchType,
        keyword: str,
    ) -> list[SearchResultItem]:
        results: list[SearchResultItem] = []
        try:
            if search_type in {SearchType.NEWS, SearchType.ALL}:
                for news in api_response.get("news", {}).get("results", []):
                    results.append(
                        SearchResultItem(
                            keyword=keyword,
                            type="news",
                            title=news.get("title", ""),
                            url=news.get("url", ""),
                            description=news.get("description", ""),
                            source=news.get("source", news.get("meta_url", {}).get("hostname", "")),
                            age=news.get("page_age", news.get("age", "")),
                            thumbnail=news.get("thumbnail", {}).get("src")
                            if news.get("thumbnail")
                            else None,
                        )
                    )
            if search_type in {SearchType.WEB, SearchType.ALL}:
                for web in api_response.get("web", {}).get("results", []):
                    results.append(
                        SearchResultItem(
                            keyword=keyword,
                            type="web",
                            title=web.get("title", ""),
                            url=web.get("url", ""),
                            description=web.get("description", ""),
                            source=web.get("profile", {}).get(
                                "long_name", web.get("meta_url", {}).get("hostname", "")
                            ),
                            age=web.get("age", ""),
                            thumbnail=web.get("thumbnail", {}).get("src")
                            if web.get("thumbnail")
                            else None,
                        )
                    )
        except Exception as exc:
            vcprint(f"[ScrapeService] _process_search error for '{keyword}': {exc}", color="red")
        return results
