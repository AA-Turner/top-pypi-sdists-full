"""``ai.util.format_scraped_content`` must read the pages it is actually given.

It read ``page["content"]`` — a key nothing in the scrape pipeline produces —
so "Combine Web Pages" returned "" for the real output of "Read Many Web
Pages", and the run died two steps later inside the model call with
"prompt: String should have at least 1 character". The shape below is copied
from a live ``scraper.scrape_many`` result.
"""

from __future__ import annotations

import pytest

from matrx_ai.graph_nodes.util_action import (
    FormatScrapedContentInput,
    ai_util_format_scraped_content,
)


def page(**overrides):
    """One page in the canonical `scraper.scrape` / `scrape_many` shape."""
    base = {
        "url": "https://example.com/a",
        "text": "Standing desks reduce sedentary time.",
        "markdown": "# Standing desks\n\nStanding desks reduce sedentary time.",
        "title": "Standing desks",
        "success": True,
        "status_code": 200,
    }
    base.update(overrides)
    return base


async def run(**kwargs):
    return await ai_util_format_scraped_content(None, FormatScrapedContentInput(**kwargs))


@pytest.mark.asyncio
async def test_reads_the_text_a_scraped_page_actually_carries() -> None:
    result = await run(values=[page()])
    assert result.status == "success"
    assert "Standing desks reduce sedentary time." in result.result.formatted_text


@pytest.mark.asyncio
async def test_falls_back_to_markdown_when_there_is_no_plain_text() -> None:
    result = await run(values=[page(text="")])
    assert result.status == "success"
    assert "# Standing desks" in result.result.formatted_text


@pytest.mark.asyncio
async def test_still_accepts_a_caller_that_really_sends_content() -> None:
    """The old key keeps working — this is a widening, not a swap."""
    result = await run(values=[{"content": "legacy body"}])
    assert result.status == "success"
    assert result.result.formatted_text == "legacy body"


@pytest.mark.asyncio
async def test_joins_pages_with_real_newlines() -> None:
    """The separator was an escaped literal, so pages were divided by the
    visible characters ``\\n---\\n`` inside the text handed to the model."""
    result = await run(values=[page(text="one"), page(text="two")])
    assert result.result.formatted_text == "one\n---\ntwo"
    assert "\\n" not in result.result.formatted_text


@pytest.mark.asyncio
async def test_skips_pages_the_scraper_could_not_load() -> None:
    result = await run(
        values=[
            page(text="", markdown=None, success=False, status_code=403),
            page(text="the good one"),
        ]
    )
    assert result.status == "success"
    assert result.result.formatted_text == "the good one"


@pytest.mark.asyncio
async def test_fails_loudly_when_every_page_failed_to_load() -> None:
    """Silence here becomes an unexplainable error two steps downstream."""
    result = await run(
        values=[page(text="", markdown=None, success=False) for _ in range(3)]
    )
    assert result.status == "error"
    assert result.error.code == "no_readable_content"
    assert "all 3 of them failed to load" in result.error.message


@pytest.mark.asyncio
async def test_fails_loudly_when_pages_loaded_but_carried_no_text() -> None:
    result = await run(values=[page(text="   ", markdown="")])
    assert result.status == "error"
    assert "none of them carried any readable text" in result.error.message


@pytest.mark.asyncio
async def test_no_pages_at_all_is_not_a_failure() -> None:
    """Nothing in means nothing out — that is the caller's business, not ours."""
    result = await run(values=[])
    assert result.status == "success"
    assert result.result.formatted_text == ""


@pytest.mark.asyncio
async def test_each_page_is_capped() -> None:
    result = await run(values=[page(text="x" * 5000)], max_chars_per_page=100)
    assert len(result.result.formatted_text) == 100
