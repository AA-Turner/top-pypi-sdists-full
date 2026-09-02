from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_scraper.features import mcp_tool_helpers as helpers


@pytest.mark.asyncio
async def test_expected_single_url_failure_is_informational(monkeypatch) -> None:
    async def _failed_fetch(url: str):
        return SimpleNamespace(
            content="",
            content_bytes=None,
            failed=True,
            failed_primary_reason="low_text_content",
        )

    emitted: list[tuple[str, str | None]] = []
    monkeypatch.setattr(helpers, "fetch_normally_with_proxy", _failed_fetch)
    monkeypatch.setattr(
        helpers,
        "vcprint",
        lambda message, **kwargs: emitted.append((message, kwargs.get("color"))),
    )

    result = await helpers.scrape_url_core("https://example.com/thin")

    assert result is None
    assert emitted == [("SCRAPE SKIPPED: https://example.com/thin (low_text_content)", "cyan")]


@pytest.mark.asyncio
async def test_empty_candidate_batch_is_the_warning_boundary(monkeypatch) -> None:
    async def _failed_scrape(*args, **kwargs):
        return None

    emitted: list[tuple[str, str | None]] = []
    monkeypatch.setattr(helpers, "scrape_url_core", _failed_scrape)
    monkeypatch.setattr(
        helpers,
        "vcprint",
        lambda message, **kwargs: emitted.append((message, kwargs.get("color"))),
    )
    search_result = {
        "web": {
            "results": [
                {"url": "https://example.com/a"},
                {"url": "https://example.com/b"},
            ]
        }
    }

    result = await helpers.scrape_urls_from_search_result(search_result, set())

    assert result == []
    assert emitted == [("SCRAPE BATCH EMPTY: all 2 candidate URLs failed", "yellow")]
