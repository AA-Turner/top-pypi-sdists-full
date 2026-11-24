"""A chunk past the context window is situated against its own part of the document, and says so.

Break this guards: ``contextualize_chunk`` sent ``document[:60_000]`` — a chunk at character
150,000 was "situated" against text that does not contain it, and nothing recorded that its
context was cut. Now the contextualizer receives the document head plus the chunk's own
neighbourhood with every omission marked, and the chunk carries ``metadata['context_window']``.
"""

from __future__ import annotations

import pytest

import matrx_rag._ext as ext
import matrx_rag.llm as llm_mod
from matrx_rag.chunking import Chunk
from matrx_rag.ingestion import attach_context_prefixes


def _chunk(chunk_id: str, text: str, parent: str | None) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        parent_chunk_id=parent,
        chunk_index=0,
        chunk_kind="parent" if parent is None else "child",
        content_text=text,
        token_count=0,
        metadata={},
    )


def _document() -> tuple[str, str]:
    """200,000 chars: a titled head, filler, one distinctive passage at 150,000, filler."""
    head = "Annual Report of the Riverside Water Authority. " * 50
    passage = "Section 9: the treatment plant on Mill Road was rebuilt in 2019 after the flood."
    filler = "x" * (150_000 - len(head))
    tail = "y" * (200_000 - 150_000 - len(passage))
    return head + filler + passage + tail, passage


class _Runner:
    def __init__(self) -> None:
        self.seen: list[str] = []

    async def contextualize(self, document: str, chunk: str, *, timeout: float | None = None) -> str:
        self.seen.append(document)
        return "From the plant history section."


@pytest.fixture
def runner(monkeypatch):
    r = _Runner()
    monkeypatch.setattr(llm_mod, "_require_runner", lambda: r)
    monkeypatch.delitem(ext._registry, "context_window_chars", raising=False)
    return r


async def test_a_late_chunk_gets_its_neighbourhood_and_the_head_marked(runner) -> None:
    document, passage = _document()
    prefix = await llm_mod.contextualize_chunk(document, passage)
    sent = runner.seen[0]
    assert prefix == "From the plant history section."
    assert passage in sent  # head-only (the old cut) never contains it
    assert sent.startswith("[Document head: characters 1-15,000 of 200,000]\nAnnual Report")
    # Worked example: 15,000 head + a 45,000 neighbourhood centred on the passage at 150,000.
    assert "[... characters 15,001-127,540 omitted ...]" in sent
    assert "[The part of the document around this passage: characters 127,541-172,540 of 200,000]" in sent
    assert sent.endswith("[... characters 172,541-200,000 omitted ...]")
    assert len(sent) < 61_000


async def test_a_short_document_is_sent_whole_and_unmarked(runner) -> None:
    await llm_mod.contextualize_chunk("A short note about tides.", "about tides")
    assert runner.seen == ["A short note about tides."]


async def test_the_chunk_records_that_its_context_was_windowed(runner) -> None:
    document, passage = _document()
    parent = _chunk("p1", document, None)
    child = _chunk("c1", passage, "p1")
    short_parent = _chunk("p2", "Tides rise twice a day.", None)
    short_child = _chunk("c2", "twice a day", "p2")
    await attach_context_prefixes([parent, child, short_parent, short_child])
    window = child.metadata["context_window"]
    assert window["document_chars"] == 200_000
    assert window["head_chars"] == 15_000
    assert window["span_start"] <= 150_000 < window["span_end"]
    assert window["chunk_located"] is True
    assert "context_window" not in short_child.metadata


async def test_the_host_window_knob_is_honoured(runner, monkeypatch) -> None:
    document, passage = _document()

    async def _ten_thousand() -> int:
        return 10_000

    monkeypatch.setitem(ext._registry, "context_window_chars", _ten_thousand)
    await llm_mod.contextualize_chunk(document, passage)
    assert passage in runner.seen[0]
    assert runner.seen[0].startswith("[Document head: characters 1-2,500 of 200,000]")
