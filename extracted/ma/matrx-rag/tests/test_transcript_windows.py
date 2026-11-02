"""Transcript chunks are windows, not caption lines (audit 2026-09-26: median 9 tokens; 24,624 of
26,021 transcript chunks under 20 tokens). Consecutive timed segments merge into ~250–400 token
windows that respect speaker turns and carry t0_ms of the first segment and t1_ms of the last, so
"Play from" still lands on the right moment."""

from __future__ import annotations

from matrx_rag.llm import CleanedPage
from matrx_rag.pdf_pipeline import (
    SEGMENT_WINDOW_MAX_TOKENS,
    SEGMENT_WINDOW_MIN_TOKENS,
    _ExtractedPage,
    _tok_len,
    chunk_portions,
)


def _transcript(n: int, turn_every: int) -> tuple[list, list, list, list]:
    pages, cleaned, kinds, locs = [], [], [], []
    for i in range(n):
        text = f"caption line number {i} says a few ordinary words here"
        pages.append(_ExtractedPage(page_index=i, text=text, used_ocr=False, char_count=len(text)))
        cleaned.append(CleanedPage(text=text))
        kinds.append("segment")
        locs.append({"t0_ms": i * 2000, "t1_ms": i * 2000 + 1800, "speaker": "A" if (i // turn_every) % 2 == 0 else "B"})
    return pages, cleaned, kinds, locs


def test_captions_become_windows_with_the_first_and_last_moment() -> None:
    pages, cleaned, kinds, locs = _transcript(300, turn_every=1000)  # one speaker throughout
    chunks = chunk_portions(pages, cleaned, kinds, locs)
    assert len(chunks) < 300 / 10, f"{len(chunks)} chunks for 300 caption lines"
    for c in chunks[:-1]:
        assert SEGMENT_WINDOW_MIN_TOKENS <= _tok_len(c.content_text) <= SEGMENT_WINDOW_MAX_TOKENS
    first = chunks[0].metadata
    assert first["t0_ms"] == 0 and first["first_page"] == 0
    assert first["t1_ms"] == locs[first["last_page"]]["t1_ms"]
    assert chunks[1].metadata["t0_ms"] == locs[chunks[1].metadata["first_page"]]["t0_ms"]


def test_a_speaker_turn_closes_a_window_once_it_is_big_enough() -> None:
    pages, cleaned, kinds, locs = _transcript(300, turn_every=40)
    chunks = chunk_portions(pages, cleaned, kinds, locs)
    for c in chunks:
        first, last = c.metadata["first_page"], c.metadata["last_page"]
        speakers = {locs[i]["speaker"] for i in range(first, last + 1)}
        if len(speakers) > 1:
            # Only allowed while the window had not yet reached the minimum at the turn.
            turn = next(i for i in range(first + 1, last + 1) if locs[i]["speaker"] != locs[i - 1]["speaker"])
            before = "\n".join(pages[j].text for j in range(first, turn))
            assert _tok_len(before) < SEGMENT_WINDOW_MIN_TOKENS
