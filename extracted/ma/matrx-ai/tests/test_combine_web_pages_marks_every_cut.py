""""Combine Web Pages" (``ai.util.format_scraped_content``) never cuts a page silently.

Break this guards: the node cut every page to ``max_chars_per_page`` (default 1,500) with
``content[:limit]`` — no marker in the text, nothing in the output — so the model reading the
combined text and the agent after it could not know most of a page was gone (research tool
rulings, 2026-11-08). A cut page now ends with the research cap line and its record says so.
"""

from __future__ import annotations

import pytest
from matrx_ai.graph_nodes.util_action import (
    FormatScrapedContentInput,
    ai_util_format_scraped_content,
)
from matrx_graph.actions import run_as_step

LONG_BODY = "Standing desks reduce sedentary time in office workers. " * 100  # 5,600 chars
SHORT_BODY = "Treadmill desks are a niche product."


async def _run(**kwargs):
    result = await run_as_step(ai_util_format_scraped_content, None, FormatScrapedContentInput(**kwargs))
    assert result.status == "success"
    return result.result


@pytest.mark.asyncio
async def test_a_cut_page_is_marked_in_the_text_and_in_its_record() -> None:
    out = await _run(
        values=[
            {"url": "https://example.com/long", "text": LONG_BODY},
            {"url": "https://example.com/short", "text": SHORT_BODY},
        ],
        max_chars_per_page=1000,
    )
    long_block, short_block = out.formatted_text.split("\n---\n")
    assert long_block.endswith("[Page capped: 1,000 of 5,599 characters kept]")
    assert short_block == SHORT_BODY
    assert [(p.url, p.capped, p.chars_kept, p.chars_after_cleanup) for p in out.pages] == [
        ("https://example.com/long", True, 1000, 5599),
        ("https://example.com/short", False, 36, 36),
    ]
    assert out.capped_pages == 1
    assert out.max_chars_per_page == 1000


@pytest.mark.asyncio
async def test_with_no_cap_given_a_page_gets_the_research_page_cap_not_a_paragraph() -> None:
    """The old 1,500 default kept about one paragraph; the default is now the research page cap."""
    out = await _run(values=[{"url": "https://example.com/long", "text": LONG_BODY}])
    assert out.max_chars_per_page == 20_000
    assert out.formatted_text == LONG_BODY.strip()
    assert out.capped_pages == 0
    assert out.pages[0].capped is False
