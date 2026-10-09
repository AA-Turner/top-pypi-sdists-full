"""``scraper.scrape_many`` can read best-first until N good pages are in hand.

The workflow used to scrape a fixed 2x buffer once and keep whatever read: a bad
first wave left a keyword short of pages, a good one wasted fetches. The research
code path walks the ranked list in waves until the target is met
(``research/scraper.py::scrape_keyword_sources``) — gap (c) of the 2026-10-07
code-vs-workflow Deep Research comparison."""

from __future__ import annotations

from typing import Any

import pytest

import matrx_scraper
from matrx_scraper.graph_nodes import scrape_actions
from matrx_scraper.graph_nodes.scrape_actions import (
    ScrapedPageItem,
    ScrapeManyInput,
    scraper_scrape_many,
)

# url -> characters of readable text (0 = failed read)
_SIZES = {"a": 5000, "b": 0, "c": 200, "d": 3000, "e": 4000, "f": 9000}


@pytest.fixture
def waves(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    seen: list[list[str]] = []

    async def _fake_scrape_many(*, urls: list[str], **_: Any) -> list[ScrapedPageItem]:
        seen.append(list(urls))
        return [
            ScrapedPageItem(url=u, text="x" * _SIZES[u], success=_SIZES[u] > 0,
                            failure_reason=None if _SIZES[u] else "blocked")
            for u in urls
        ]

    monkeypatch.setattr(matrx_scraper, "scrape_many", _fake_scrape_many)
    monkeypatch.setattr(scrape_actions, "_scrape_result_to_page", lambda r: r)
    return seen


@pytest.mark.asyncio
async def test_reads_in_waves_until_the_target_then_stops(waves: list[list[str]]) -> None:
    res = await scraper_scrape_many(
        None,  # type: ignore[arg-type]
        ScrapeManyInput(urls=list("abcdef"), stop_after_good=3, good_min_chars=1000),
    )
    out = res.result
    assert waves == [["a", "b", "c"], ["d", "e"]]
    assert [p.url for p in out.good_pages] == ["a", "d", "e"]
    assert out.good == 3
    assert out.not_attempted == 1
    assert len(out.pages) == 5 and out.failed == 1


@pytest.mark.asyncio
async def test_runs_dry_honestly_when_the_list_cannot_meet_the_target(waves: list[list[str]]) -> None:
    res = await scraper_scrape_many(
        None,  # type: ignore[arg-type]
        ScrapeManyInput(urls=list("abc"), stop_after_good=3, good_min_chars=1000),
    )
    out = res.result
    assert [p.url for p in out.good_pages] == ["a"]
    assert out.good == 1 and out.not_attempted == 0


@pytest.mark.asyncio
async def test_without_a_target_reads_everything_once(waves: list[list[str]]) -> None:
    res = await scraper_scrape_many(None, ScrapeManyInput(urls=list("abcdef")))  # type: ignore[arg-type]
    assert waves == [list("abcdef")]
    assert res.result.good == 5  # every successful read; no length floor


@pytest.mark.asyncio
async def test_each_page_says_whether_it_is_good_and_how_long_it_is(waves: list[list[str]]) -> None:
    """A workflow saving every page (research.rs_content is_good_scrape and
    char_count) reads the verdict off the page itself, not by re-deriving it."""
    res = await scraper_scrape_many(
        None,  # type: ignore[arg-type]
        ScrapeManyInput(urls=list("abc"), good_min_chars=1000),
    )
    pages = {p.url: p for p in res.result.pages}
    assert {u: p.is_good for u, p in pages.items()} == {"a": True, "b": False, "c": False}


def test_page_projection_counts_characters() -> None:
    page = scrape_actions._scrape_result_to_page(
        {"url": "u", "success": True, "main_content_text": "hello world"}
    )
    assert page.char_count == 11
