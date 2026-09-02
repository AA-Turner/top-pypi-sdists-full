from __future__ import annotations

import asyncio
import threading

import pytest

from matrx_scraper.parser import core
from matrx_scraper import orchestrator


class _OrganizedData:
    def extract(self, *, rules):
        return {"content": "parsed", "rule_count": len(rules)}


@pytest.mark.asyncio
async def test_parse_html_offloads_the_entire_sync_pipeline(monkeypatch) -> None:
    loop_thread_id = threading.get_ident()
    parse_thread_ids: list[int] = []

    def _parse_content(self, soup, url):
        parse_thread_ids.append(threading.get_ident())
        return {"organized_data": _OrganizedData(), "links": {"internal": []}}

    monkeypatch.setattr(core.ParserOrchestrator, "parse_content", _parse_content)

    result = await core.parse_html("<html></html>", "https://example.com/page")

    assert parse_thread_ids
    assert parse_thread_ids[0] != loop_thread_id
    assert result["content"] == "parsed"
    assert result["links"] == {"internal": []}


@pytest.mark.asyncio
async def test_parse_html_keeps_event_loop_responsive(monkeypatch) -> None:
    entered = threading.Event()
    release = threading.Event()

    def _parse_content(self, soup, url):
        entered.set()
        release.wait(timeout=2)
        return {"organized_data": None, "links": {}}

    monkeypatch.setattr(core.ParserOrchestrator, "parse_content", _parse_content)
    task = asyncio.create_task(core.parse_html("<html></html>", "https://example.com"))

    assert await asyncio.to_thread(entered.wait, 1)
    await asyncio.sleep(0)
    assert not task.done()
    release.set()
    await task


@pytest.mark.asyncio
async def test_scrape_offloads_response_extraction(monkeypatch) -> None:
    loop_thread_id = threading.get_ident()
    extraction_thread_ids: list[int] = []

    async def _fetch(url, request_type, user_agent=None):
        return object()

    def _build_result(response, fast):
        extraction_thread_ids.append(threading.get_ident())
        return orchestrator.ScrapeResult(
            url="https://example.com",
            response_url="https://example.com",
            success=True,
            content_type="html",
        )

    monkeypatch.setattr(orchestrator, "fetch", _fetch)
    monkeypatch.setattr(orchestrator, "_build_result_from_response", _build_result)

    result = await orchestrator.scrape("https://example.com", use_proxy=False)

    assert result.success is True
    assert extraction_thread_ids
    assert extraction_thread_ids[0] != loop_thread_id


@pytest.mark.asyncio
async def test_browser_scrape_uses_required_proxy(monkeypatch) -> None:
    proxies: list[str | None] = []

    class _Pool:
        async def fetch(self, url, *, proxy):
            proxies.append(proxy)
            return "<html><body>ok</body></html>", url, 200, {"content-type": "text/html"}, "ok"

    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy-one")
    monkeypatch.setattr(
        orchestrator,
        "_build_result_from_response",
        lambda response, fast: orchestrator.ScrapeResult(
            url=response.request_url,
            response_url=response.response_url,
            success=True,
            content_type="html",
        ),
    )

    result = await orchestrator.scrape(
        "https://example.com",
        request_type=orchestrator.RequestType.BROWSER,
        browser_pool=_Pool(),
    )

    assert result.success is True
    assert proxies == ["http://proxy-one"]
