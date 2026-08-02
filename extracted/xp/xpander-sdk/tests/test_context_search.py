"""Unit tests for the context-retrieve search helpers and the L1 offload hint
(size/token annotation + repeatable search advert).
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
)
from xpander_sdk.core.context_optimizer.search import bm25_rank, grep_text


# ---------------------------------------------------------------------------
# grep_text
# ---------------------------------------------------------------------------


def test_grep_text_returns_only_matching_lines_with_context():
    doc = "alpha\nbravo\ncharlie error here\ndelta\necho\nfoxtrot\ngolf error two\nhotel"
    out = grep_text(doc, "error", context_lines=1)
    assert "2 matching line(s)" in out
    assert "charlie error here" in out
    assert "golf error two" in out
    # Context lines around each match are included.
    assert "bravo" in out and "delta" in out
    assert "foxtrot" in out and "hotel" in out
    # Lines outside every context window are excluded.
    assert "alpha" not in out
    assert "echo" not in out


def test_grep_text_bad_regex_falls_back_to_substring():
    doc = "call func(x)\nother line"
    # 'func(' is an invalid regex (unbalanced paren) but a valid substring.
    out = grep_text(doc, "func(", context_lines=0)
    assert "1 matching line(s)" in out
    assert "call func(x)" in out


def test_grep_text_no_match_returns_nudge():
    out = grep_text("hello world", "zzznope")
    assert "no lines match" in out
    assert "xpworkspace-context-retrieve again" in out


def test_grep_text_clips_giant_single_line_to_window_around_match():
    # A 500K single-line JSON blob (the real failure mode) with the needle buried deep.
    needle = "NEEDLE_ORG_ID"
    blob = "x" * 250_000 + needle + "y" * 250_000
    out = grep_text(blob, needle, context_lines=0)
    assert "1 matching line(s)" in out
    # The match is returned, but the output is bounded, not the whole 500K line.
    assert needle in out
    assert len(out) < 5_000
    # Both sides were elided with a char-count marker.
    assert "chars]" in out


def test_grep_text_short_lines_unchanged():
    doc = "alpha error one\nbravo\ncharlie"
    out = grep_text(doc, "error", context_lines=0)
    assert "alpha error one" in out
    assert "[+" not in out  # nothing clipped for short lines


# ---------------------------------------------------------------------------
# bm25_rank
# ---------------------------------------------------------------------------


def test_bm25_rank_ranks_relevant_chunk_first():
    filler = "lorem ipsum dolor sit amet consectetur " * 20  # >512 chars → own chunk
    relevant = "The payment was declined by the bank because the card expired."
    other = "Weather today is sunny with a mild breeze across the valley. " * 12
    doc = f"{filler}\n\n{relevant}\n\n{other}"
    out = bm25_rank(doc, "why was the payment declined", top_n=1)
    assert "by relevance" in out
    assert "payment was declined" in out
    # The clearly-irrelevant weather chunk must not be the top result.
    assert "sunny" not in out


def test_bm25_rank_no_terms_returns_nudge():
    out = bm25_rank("some content here", "")
    assert "nothing to rank" in out


# ---------------------------------------------------------------------------
# Offload hint: size + estimated tokens + repeatable search advert
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_offload_hint_includes_tokens_and_search_advert():
    opt = XPanderContextOptimizer(
        max_content_length=100, min_content_length=10, preview_length=20
    )
    opt._save_to_workspace = AsyncMock(return_value="CONTEXT_OPTIMIZATION/abc.xp")
    replacement, _ = await opt.maybe_offload_content(
        content="z" * 800, tool_name="web_search"
    )
    assert replacement is not None
    assert "chars (~" in replacement and "tokens) total" in replacement
    assert 'query="<regex>"' in replacement
    assert 'semantic_query="<text>"' in replacement
    assert "multiple times on the same context_id" in replacement


def test_estimate_tokens_for_text_ratio():
    assert XPanderContextOptimizer._estimate_tokens_for_text("x" * 400) == int(
        400 / 4 * 1.2
    )
