"""``ai.scrape.web`` ("Fetch Page Content"): a page with no readable text is a declared failure.

Break this guards (E5): a blank page returned ``success`` with ``is_good_scrape=False``, so the
workflow carried an empty page on as content and the failure surfaced, if at all, steps later.
"""

from __future__ import annotations

import pytest

pytest.importorskip("matrx_scraper.features.read_page")

from matrx_ai.graph_nodes.scrape_action import WebScrapeInput, ai_scrape_web  # noqa: E402
from matrx_scraper.features import read_page as read_page_module  # noqa: E402


class _Channels:
    def __init__(self) -> None:
        self.written: list = []

    def write(self, name, value) -> None:
        self.written.append((name, value))


class _Ctx:
    def __init__(self) -> None:
        self.channels = _Channels()


@pytest.mark.parametrize("text", ["", "   \n\t "])
@pytest.mark.asyncio
async def test_a_blank_page_fails_with_empty_page_and_writes_nothing(monkeypatch, text) -> None:
    async def _read(**_kw):
        return {"status": "success", "text": text}

    monkeypatch.setattr(read_page_module, "read_page_mcp_quick", _read)
    ctx = _Ctx()
    out = await ai_scrape_web(ctx, WebScrapeInput(url="https://example.com/blank", channel_out="pages"))
    assert out.status == "error"
    assert out.error.code == "empty_page"
    assert out.error.details == {"url": "https://example.com/blank", "failure_reason": "empty_page"}
    assert ctx.channels.written == []


@pytest.mark.asyncio
async def test_a_page_with_text_still_succeeds(monkeypatch) -> None:
    async def _read(**_kw):
        return {"status": "success", "text": "Tide tables for the harbour."}

    monkeypatch.setattr(read_page_module, "read_page_mcp_quick", _read)
    out = await ai_scrape_web(_Ctx(), WebScrapeInput(url="https://example.com/tides"))
    assert out.status == "success"
    assert out.result.text == "Tide tables for the harbour."
    assert out.result.is_good_scrape is True
