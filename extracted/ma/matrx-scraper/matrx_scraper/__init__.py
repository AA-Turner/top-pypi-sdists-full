"""matrx-scraper — Web scraping engine, HTML parsing, and search integration.

The top-level `matrx_scraper` namespace exposes a wide surface (orchestrator,
crawler, search, parsers, AI browser primitives, etc.). To avoid forcing
heavy optional dependencies (Playwright, Selenium fallbacks, etc.) on
consumers that only use a slice of the API (e.g. `matrx_scraper.search` or
`matrx_scraper.queue_backend` from aidream), we resolve top-level names
lazily via PEP 562 `__getattr__`.

Submodule imports (`from matrx_scraper.search import ...`,
`from matrx_scraper.ai_browser import ...`, etc.) bypass this lazy layer
and load only what the caller actually needs.
"""

# ruff: noqa: F401 — the TYPE_CHECKING block below re-exports every name in
# _LAZY_IMPORTS for type checkers; ruff cannot see the dynamic __all__ and
# would flag all of them as unused.

from __future__ import annotations

from typing import TYPE_CHECKING

_LAZY_IMPORTS: dict[str, str] = {
    "scrape": "matrx_scraper.orchestrator",
    "scrape_many": "matrx_scraper.orchestrator",
    "scrape_many_stream": "matrx_scraper.orchestrator",
    "ScrapeResult": "matrx_scraper.orchestrator",
    "ScrapeService": "matrx_scraper.service",
    # Options + the field filter come from the dependency-free module so a
    # consumer without matrx-connect / matrx-orm can still use them.
    "ScrapeOptions": "matrx_scraper.scrape_options",
    "apply_field_flags": "matrx_scraper.scrape_options",
    "crawl_site": "matrx_scraper.crawler",
    "SiteCrawler": "matrx_scraper.crawler",
    "SiteCrawlerConfig": "matrx_scraper.crawler",
    "CrawlEventSink": "matrx_scraper.crawler",
    "PersistRequest": "matrx_scraper.crawler",
    "PersistResult": "matrx_scraper.crawler",
    "BodyPersister": "matrx_scraper.crawler",
    "RENDER_HTTP_ONLY": "matrx_scraper.crawler",
    "RENDER_HTTP_FIRST": "matrx_scraper.crawler",
    "RENDER_BROWSER_ALWAYS": "matrx_scraper.crawler",
    "RENDER_BROWSER_WITH_SCREENSHOT": "matrx_scraper.crawler",
    "VALID_RENDER_MODES": "matrx_scraper.crawler",
    "QueueBackend": "matrx_scraper.queue_backend",
    "QueueItem": "matrx_scraper.queue_backend",
    "InMemoryQueueBackend": "matrx_scraper.queue_backend",
    "HostRateLimiter": "matrx_scraper.rate_limiter",
    "audit_html": "matrx_scraper.seo_audit",
    "SeoAuditResult": "matrx_scraper.seo_audit",
    "extract_structured_data": "matrx_scraper.structured_data",
    "StructuredDataBlock": "matrx_scraper.structured_data",
    "CrawlEvent": "matrx_scraper.events",
    "CrawlEventType": "matrx_scraper.events",
    "CrawlStartedEvent": "matrx_scraper.events",
    "CrawlPageDiscoveredEvent": "matrx_scraper.events",
    "CrawlPageFetchedEvent": "matrx_scraper.events",
    "CrawlPageParsedEvent": "matrx_scraper.events",
    "CrawlPageFailedEvent": "matrx_scraper.events",
    "CrawlProgressEvent": "matrx_scraper.events",
    "CrawlIssueDetectedEvent": "matrx_scraper.events",
    "CrawlWarningEvent": "matrx_scraper.events",
    "CrawlCompletedEvent": "matrx_scraper.events",
    "PageSummary": "matrx_scraper.events",
    "parse_html": "matrx_scraper.parser",
    "ParserOrchestrator": "matrx_scraper.parser",
    "LinkExtractor": "matrx_scraper.parser.link_extractor",
    "NoiseRemover": "matrx_scraper.parser.noise_remover",
    "NoiseRemoverConfig": "matrx_scraper.parser.noise_config",
    "MainContentFinder": "matrx_scraper.parser.main_content",
    "compute_hashes": "matrx_scraper.parser.hashing",
    "compute_minhash_from_text": "matrx_scraper.parser.hashing",
    "compute_simhash": "matrx_scraper.parser.hashing",
    "BraveSearchClient": "matrx_scraper.search",
    "async_brave_search": "matrx_scraper.search",
    "configure_client": "matrx_scraper.search",
    "extract_urls_from_search_results": "matrx_scraper.search",
    "CacheBackend": "matrx_scraper.cache",
    "MemoryCache": "matrx_scraper.cache",
    "TwoTierCache": "matrx_scraper.cache",
    "DomainConfigBackend": "matrx_scraper.domain_config",
    "PostgresDomainConfigStore": "matrx_scraper.domain_config",
    "StaticDomainConfigStore": "matrx_scraper.domain_config",
    "PlaywrightBrowserPool": "matrx_scraper.browser_pool",
    "URLInfo": "matrx_scraper.utils",
    "get_url_info": "matrx_scraper.utils",
    "normalize_url": "matrx_scraper.url_utils",
    "compute_link_scores": "matrx_scraper.pagerank",
    "PageRankEdge": "matrx_scraper.pagerank",
    "CustomExtractor": "matrx_scraper.custom_extractors",
    "find_extractors_for_url": "matrx_scraper.custom_extractors",
    "run_custom_extractors": "matrx_scraper.custom_extractors",
    "run_custom_extractor": "matrx_scraper.custom_extractors",
    "CrawlRecipe": "matrx_scraper.recipes",
    "RecipeAction": "matrx_scraper.recipes",
    "RecipeBackend": "matrx_scraper.recipes",
    "StaticRecipeBackend": "matrx_scraper.recipes",
    "DEFAULT_RECIPES": "matrx_scraper.recipes",
    "CapturedScreenshot": "matrx_scraper.browser_pool",
    "PageInspection": "matrx_scraper.browser_pool",
    "BrowserInspectTimeout": "matrx_scraper.browser_pool",
    "capture_screenshots": "matrx_scraper.browser_pool",
    "execute_directives": "matrx_scraper.recipe_runtime",
    "PsiClient": "matrx_scraper.performance",
    "PsiSnapshot": "matrx_scraper.performance",
    "GscClient": "matrx_scraper.performance",
    "GscErrorCode": "matrx_scraper.performance",
    "GscPageSnapshot": "matrx_scraper.performance",
    "GscQueryRow": "matrx_scraper.performance",
    "quick_preview": "matrx_scraper.preview",
    "BrowserSession": "matrx_scraper.ai_browser",
    "BrowserSessionManager": "matrx_scraper.ai_browser",
    "get_browser_session_manager": "matrx_scraper.ai_browser",
    "RemoteBrowserClient": "matrx_scraper.ai_browser",
    "BrowserClientError": "matrx_scraper.ai_browser",
    "ToolSpec": "matrx_scraper.ai_tools",
    "BROWSER_TOOLS": "matrx_scraper.ai_tools",
    "SCRAPE_TOOLS": "matrx_scraper.ai_tools",
    "ALL_TOOLS": "matrx_scraper.ai_tools",
}


def configure_db(db_config_name: str) -> None:
    """Bind matrx-scraper's ``scraper.*`` and ``web.*`` models to a host pool.

    The host (aidream) calls this once at startup with the name of a pool it
    registered via ``register_database_from_env`` — today
    ``"supabase_automation_matrix"``, later a Coolify-local-Postgres pool. Aliases
    the package's ``"matrx_scraper"`` config name onto it and registers the models
    (the matrx-rag/runtime pattern). Requires the ``[db]`` extra (matrx-orm).
    matrx-orm is imported lazily here so a no-DB consumer never pays for it.
    """
    from matrx_scraper.db import bind_to_host
    from matrx_scraper.db._config import set_db_config_name
    from matrx_scraper.db.web import bind_web_to_host

    set_db_config_name(db_config_name)
    bind_to_host(db_config_name)
    bind_web_to_host(db_config_name)


def __getattr__(name: str):
    """PEP 562 module-level lazy attribute resolution."""
    module_path = _LAZY_IMPORTS.get(name)
    if module_path is None:
        raise AttributeError(f"module 'matrx_scraper' has no attribute {name!r}")
    import importlib

    module = importlib.import_module(module_path)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LAZY_IMPORTS))


if TYPE_CHECKING:
    from matrx_scraper.ai_browser import (
        BrowserClientError,
        BrowserSession,
        BrowserSessionManager,
        RemoteBrowserClient,
        get_browser_session_manager,
    )
    from matrx_scraper.ai_tools import (
        ALL_TOOLS,
        BROWSER_TOOLS,
        SCRAPE_TOOLS,
        ToolSpec,
    )
    from matrx_scraper.browser_pool import (
        BrowserInspectTimeout,
        CapturedScreenshot,
        PageInspection,
        PlaywrightBrowserPool,
        capture_screenshots,
    )
    from matrx_scraper.cache import CacheBackend, MemoryCache, TwoTierCache
    from matrx_scraper.crawler import (
        RENDER_BROWSER_ALWAYS,
        RENDER_BROWSER_WITH_SCREENSHOT,
        RENDER_HTTP_FIRST,
        RENDER_HTTP_ONLY,
        VALID_RENDER_MODES,
        BodyPersister,
        CrawlEventSink,
        PersistRequest,
        PersistResult,
        SiteCrawler,
        SiteCrawlerConfig,
        crawl_site,
    )
    from matrx_scraper.custom_extractors import (
        Extractor as CustomExtractor,
    )
    from matrx_scraper.custom_extractors import (
        find_for_url as find_extractors_for_url,
    )
    from matrx_scraper.custom_extractors import (
        run_all as run_custom_extractors,
    )
    from matrx_scraper.custom_extractors import (
        run_extractor as run_custom_extractor,
    )
    from matrx_scraper.domain_config import (
        DomainConfigBackend,
        PostgresDomainConfigStore,
        StaticDomainConfigStore,
    )
    from matrx_scraper.events import (
        CrawlCompletedEvent,
        CrawlEvent,
        CrawlEventType,
        CrawlIssueDetectedEvent,
        CrawlPageDiscoveredEvent,
        CrawlPageFailedEvent,
        CrawlPageFetchedEvent,
        CrawlPageParsedEvent,
        CrawlProgressEvent,
        CrawlStartedEvent,
        CrawlWarningEvent,
        PageSummary,
    )
    from matrx_scraper.orchestrator import (
        ScrapeResult,
        scrape,
        scrape_many,
        scrape_many_stream,
    )
    from matrx_scraper.pagerank import Edge as PageRankEdge
    from matrx_scraper.pagerank import compute_link_scores
    from matrx_scraper.parser import ParserOrchestrator, parse_html
    from matrx_scraper.parser.hashing import (
        compute_hashes,
        compute_minhash_from_text,
        compute_simhash,
    )
    from matrx_scraper.parser.link_extractor import LinkExtractor
    from matrx_scraper.parser.main_content import MainContentFinder
    from matrx_scraper.parser.noise_config import NoiseRemoverConfig
    from matrx_scraper.parser.noise_remover import NoiseRemover
    from matrx_scraper.performance import (
        GscClient,
        GscErrorCode,
        GscPageSnapshot,
        GscQueryRow,
        PsiClient,
        PsiSnapshot,
    )
    from matrx_scraper.preview import quick_preview
    from matrx_scraper.queue_backend import (
        InMemoryQueueBackend,
        QueueBackend,
        QueueItem,
    )
    from matrx_scraper.rate_limiter import HostRateLimiter
    from matrx_scraper.recipe_runtime import execute_directives
    from matrx_scraper.recipes import (
        DEFAULT_RECIPES,
        CrawlRecipe,
        RecipeAction,
        RecipeBackend,
        StaticRecipeBackend,
    )
    from matrx_scraper.scrape_options import ScrapeOptions, apply_field_flags
    from matrx_scraper.search import (
        BraveSearchClient,
        async_brave_search,
        configure_client,
        extract_urls_from_search_results,
    )
    from matrx_scraper.seo_audit import SeoAuditResult, audit_html
    from matrx_scraper.service import ScrapeService
    from matrx_scraper.url_utils import normalize_url
    from matrx_scraper.utils import URLInfo, get_url_info


__all__ = sorted(set(_LAZY_IMPORTS) | {"configure_db"})
