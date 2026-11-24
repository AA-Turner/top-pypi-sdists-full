"""Feedback 67828c9c: a Brave snippet arrived entity-encoded twice ("NASA&amp;#x27;s")
and every client printed it raw. async_brave_search decodes text fields to plain text."""

from __future__ import annotations

import pytest

from matrx_scraper.search import search


@pytest.mark.asyncio
async def test_brave_results_reach_callers_as_plain_text(monkeypatch) -> None:
    class _Client:
        async def search(self, **_kw):
            return {
                "web": {"results": [{
                    "title": "NASA&#x27;s mission",
                    "description": "NASA&amp;#x27;s newest probe &amp; more",
                    "extra_snippets": ["Tom &amp;amp; Jerry"],
                }]},
                "news": {"results": [{"title": "A &quot;quote&quot;"}]},
            }

    monkeypatch.setattr(search, "get_client", lambda: _Client())
    result = await search.async_brave_search("recent space mission")
    web = result["web"]["results"][0]
    assert web["title"] == "NASA's mission"
    assert web["description"] == "NASA's newest probe & more"
    assert web["extra_snippets"] == ["Tom & Jerry"]
    assert result["news"]["results"][0]["title"] == 'A "quote"'
