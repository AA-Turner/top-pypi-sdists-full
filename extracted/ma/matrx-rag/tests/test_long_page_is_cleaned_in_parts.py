"""A page whose cleaned answer would pass the model's output limit is cleaned in parts.

Live 2026-10: ``rag.pdf_page_cleaner`` (model max 16,384 out) was asked to clean a
95,926-token page (answer 22,939 tokens) and, twice on 2026-10-28, ran away on a
2,380-token index page until it hit 16,384 and was cut off.

Forcing function (each leg fails on the pre-fix source):
- a page over PAGE_CLEAN_MAX_INPUT_TOKENS is sent to the cleaner in several calls, none
  over the limit, and the cleaned parts join back in page order;
- a short page whose answer is cut off (PageOutputTruncated) is halved and retried;
- a part that never fits fails the whole page by name (degraded), never half-cleaned.
"""

from __future__ import annotations

import asyncio

import matrx_rag.llm as llm_mod
from matrx_rag.llm import PAGE_CLEAN_MAX_INPUT_TOKENS, PageOutputTruncated
from matrx_utils.splitting import count_tokens


def _page(words: int) -> str:
    return "\n\n".join(f"Paragraph {i} of the deposition transcript, page text." for i in range(words))


def _runner(monkeypatch, calls: list[str], *, truncate_over: int | None = None, always_truncate=False):
    class _Runner:
        async def clean_page(self, raw: str, **_kw: object):
            calls.append(raw)
            if always_truncate or (truncate_over is not None and count_tokens(raw) > truncate_over):
                raise PageOutputTruncated("cut off")
            return {"text": raw.upper(), "section_kind": "transcript", "section_title": f"t{len(calls)}"}

    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Runner())
    monkeypatch.setattr(llm_mod, "vcprint", lambda *a, **kw: None)


def test_oversized_page_is_split_and_joined_in_order(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, calls)
    raw = _page(2600)
    assert count_tokens(raw) > PAGE_CLEAN_MAX_INPUT_TOKENS
    out = asyncio.run(llm_mod.clean_pdf_text(raw))

    assert len(calls) >= 2, "a too-long page must not go to the cleaner in one call"
    assert all(count_tokens(c) <= PAGE_CLEAN_MAX_INPUT_TOKENS for c in calls)
    assert not out.degraded
    nums = [int(w) for w in __import__("re").findall(r"PARAGRAPH (\d+)", out.text)]
    assert nums == list(range(2600)), "parts must join back in page order, nothing lost or repeated"
    assert out.section_title == "t1", "the first part names the page"


def test_short_page_cut_off_is_halved_and_retried(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, calls, truncate_over=1500)
    raw = _page(400)
    assert 1500 < count_tokens(raw) < PAGE_CLEAN_MAX_INPUT_TOKENS
    out = asyncio.run(llm_mod.clean_pdf_text(raw))

    assert len(calls) >= 3, "one cut-off call, then the halves"
    assert not out.degraded
    nums = [int(w) for w in __import__("re").findall(r"PARAGRAPH (\d+)", out.text)]
    assert nums == list(range(400))


def test_a_part_that_never_fits_fails_the_page_by_name(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, calls, always_truncate=True)
    out = asyncio.run(llm_mod.clean_pdf_text(_page(400)))

    assert out.degraded, "never persisted as cleaned"
    assert isinstance(out.failure, PageOutputTruncated)
    assert len(calls) < 40, "halving is bounded"
