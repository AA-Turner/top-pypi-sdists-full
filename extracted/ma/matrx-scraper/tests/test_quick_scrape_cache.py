"""use_cache=True on the quick-scrape path must actually hit the L2 cache.

The bug this pins: ``ScrapeService.use_cache`` was assigned from the request
and then never read — every ``scrape_many_stream`` call omitted ``cache=``,
so the L2 page cache was unreachable from the whole quick-scrape lane. The
fix threads the host-injected ``cache`` ext (``configure_ext(cache=...)``)
into each call; this test proves a repeat scrape is served from the cache
(one engine fetch, not two) and that ``use_cache=False`` still bypasses it.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_scraper import orchestrator
from matrx_scraper._ext import _registry
from matrx_scraper.cache import MemoryCache
from matrx_scraper.service import ScrapeService


class _CollectingEmitter:
    def __init__(self) -> None:
        self.payloads: list[Any] = []

    async def send_data(self, data: Any) -> None:
        self.payloads.append(data)


@pytest.fixture
def cache_ext():
    """Register a MemoryCache as the 'cache' ext; restore the registry after."""
    cache = MemoryCache()
    had_prior = "cache" in _registry
    prior = _registry.get("cache")
    _registry["cache"] = cache
    yield cache
    if had_prior:
        _registry["cache"] = prior
    else:
        _registry.pop("cache", None)


@pytest.fixture
def stub_engine(monkeypatch: pytest.MonkeyPatch):
    """Stub the fetch + parse pipeline; count real (non-cached) fetches."""
    calls: list[str] = []

    async def fake_fetch_with_proxy(url: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
        calls.append(url)
        return {"request_url": url}

    def fake_build_result(response: dict[str, Any], fast: bool) -> orchestrator.ScrapeResult:
        return orchestrator.ScrapeResult(
            url=response["request_url"],
            response_url=response["request_url"],
            success=True,
            content_type="html",
            status_code=200,
            text_data="stub page body",
        )

    monkeypatch.setattr(orchestrator, "fetch_normally_with_proxy", fake_fetch_with_proxy)
    monkeypatch.setattr(orchestrator, "_build_result_from_response", fake_build_result)
    return calls


def _service(use_cache: bool) -> tuple[ScrapeService, _CollectingEmitter]:
    emitter = _CollectingEmitter()
    service = ScrapeService(emitter=emitter)
    service.urls = ["https://example.com/cached-page"]
    service.use_cache = use_cache
    return service, emitter


@pytest.mark.asyncio
async def test_use_cache_true_serves_repeat_scrape_from_cache(
    cache_ext: MemoryCache, stub_engine: list[str]
) -> None:
    first, first_emitter = _service(use_cache=True)
    await first.quick_scrape_stream()
    assert len(stub_engine) == 1, "first scrape must reach the engine"
    assert len(first_emitter.payloads) == 1

    second, second_emitter = _service(use_cache=True)
    await second.quick_scrape_stream()
    assert len(stub_engine) == 1, "repeat scrape must be served from the L2 cache"
    assert len(second_emitter.payloads) == 1

    # The cached emit carries the same extracted content as the live one.
    cached_page = second_emitter.payloads[0].results[0]
    assert getattr(cached_page, "text_data", None) == "stub page body"
    assert cached_page.success is True


@pytest.mark.asyncio
async def test_use_cache_false_bypasses_cache(
    cache_ext: MemoryCache, stub_engine: list[str]
) -> None:
    for _ in range(2):
        service, _emitter = _service(use_cache=False)
        await service.quick_scrape_stream()
    assert len(stub_engine) == 2, "use_cache=False must never consult or populate the cache"


@pytest.mark.asyncio
async def test_use_cache_true_without_cache_ext_scrapes_uncached(
    stub_engine: list[str],
) -> None:
    """Standalone install (no host cache ext): quick-scrape still works."""
    had_prior = "cache" in _registry
    prior = _registry.get("cache")
    _registry.pop("cache", None)
    try:
        for _ in range(2):
            service, _emitter = _service(use_cache=True)
            await service.quick_scrape_stream()
        assert len(stub_engine) == 2
    finally:
        if had_prior:
            _registry["cache"] = prior
