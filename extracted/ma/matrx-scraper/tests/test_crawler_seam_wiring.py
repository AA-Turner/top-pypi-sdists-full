"""The canonical crawler must actually receive the host-configured seams.

`SiteCrawler` accepts optional collaborators (domain_config, cache,
recipe_backend, extractor_runner). Each one that the web-crawl service fails to
pass produces NO error and NO log — the crawl just silently runs without that
capability. That is exactly how per-host domain policy stayed dark: the
domain-rules UI wrote `scraper.scrape_domain` rows, the quick-scrape lane
honoured them, and every site crawl ignored them for months.

These tests pin the wiring so a future refactor of `_build_crawler` cannot drop
a seam quietly.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_scraper._ext import configure_ext
from matrx_scraper.web_crawl.broker import CrawlEventBroker
from matrx_scraper.web_crawl.contracts import CrawlStartRequest
from matrx_scraper.web_crawl.persistence import CrawlPersistenceState
from matrx_scraper.web_crawl.service import PreparedCrawl, WebCrawlService


def _prepared() -> PreparedCrawl:
    return PreparedCrawl(
        site_id="site-1",
        session_id="session-1",
        root_url="https://acme.example/",
        request=CrawlStartRequest(
            max_pages=5,
            max_depth=1,
            capture_screenshots=False,
            screenshot_kinds=[],
        ),
        repository=SimpleNamespace(persist_event=AsyncMock()),
        state=CrawlPersistenceState(
            site_id="site-1",
            session_id="session-1",
            user_id="user-1",
            organization_id="org-1",
            file_owner_id="user-1",
            coverage_qualified=False,
        ),
        broker=CrawlEventBroker("session-1"),
    )


@pytest.fixture
def restore_ext():
    """Snapshot/restore the process-wide ext registry around a test."""
    from matrx_scraper import _ext

    saved = dict(_ext._registry)
    # _build_crawler always builds a body persister, which wraps the file
    # manager in a matrx-files FileService. That is not what these tests are
    # about — supply the minimum shape FileService validates.
    configure_ext(file_manager=SimpleNamespace(sync_engine=SimpleNamespace()))
    yield
    _ext._registry.clear()
    _ext._registry.update(saved)


@pytest.mark.asyncio
async def test_domain_config_reaches_the_crawler(restore_ext):
    """A host-configured domain_config must be handed to SiteCrawler.

    Without this the crawler's `get_proxy_type` branch and the per-host parse
    policy it forwards into `scrape()` are unreachable, so every domain rule a
    user authors is ignored on every site crawl.
    """
    sentinel = SimpleNamespace(get_proxy_type=lambda url: "none", healthy=True)
    configure_ext(domain_config=sentinel)

    service = WebCrawlService()
    crawler, _persister = await service._build_crawler(_prepared(), sink=AsyncMock())

    assert crawler.domain_config is sentinel


@pytest.mark.asyncio
async def test_page_cache_is_deliberately_not_wired(restore_ext):
    """A site crawl must never serve a cached parse.

    A crawl reports the site's CURRENT state; a cache hit would make a re-crawl
    silently report stale content and defeat change detection. The L2 cache
    belongs to the quick-scrape lane. This is a decision, not an oversight — if
    you are here because you want caching in crawls, that needs an owner ruling.
    """
    configure_ext(cache=SimpleNamespace())

    service = WebCrawlService()
    crawler, _persister = await service._build_crawler(_prepared(), sink=AsyncMock())

    assert crawler.cache is None


@pytest.mark.asyncio
async def test_the_requested_user_agent_reaches_the_crawler(restore_ext):
    """`CrawlStartRequest.user_agent` must survive `_build_crawler`.

    Dropping it here is silent: the crawl runs, every page is fetched, and the
    caller's chosen identity — the whole reason a customer's WAF was going to
    let us through — simply never reaches the wire.
    """
    override = "MatrxCrawlerTest/9.9 (+https://aimatrx.com/test)"
    prepared = _prepared()
    prepared.request = prepared.request.model_copy(update={"user_agent": override})

    service = WebCrawlService()
    crawler, _persister = await service._build_crawler(prepared, sink=AsyncMock())

    assert crawler.config.user_agent_override == override
    assert crawler.user_agent == override


@pytest.mark.asyncio
async def test_no_requested_user_agent_leaves_the_crawler_on_its_default(restore_ext):
    service = WebCrawlService()
    crawler, _persister = await service._build_crawler(_prepared(), sink=AsyncMock())

    assert crawler.config.user_agent_override is None
    assert crawler._user_agent_override is None
