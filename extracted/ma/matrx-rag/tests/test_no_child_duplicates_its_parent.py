"""A chunk never duplicates its parent, and search never returns one text twice per document.

Live data (2026-10-11): 2,089 parent/child pairs in ``rag.kg_chunks`` had identical
text — a parent block too small to split got ONE child equal to itself — and the
recall doors return parents and children alike, so search could show the same
passage twice for one document (MMR waves short snippets through and is optional).
Forcing function: before the fix ``chunk_text`` emitted the identical child and
``search`` had no exact-text dedupe.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

from matrx_rag import search as search_mod
from matrx_rag.chunking import chunk_code, chunk_text


def _identical_children(chunks):
    by_id = {c.chunk_id: c for c in chunks}
    return [
        c
        for c in chunks
        if c.parent_chunk_id
        and " ".join(c.content_text.split()) == " ".join(by_id[c.parent_chunk_id].content_text.split())
    ]


def test_a_small_parent_gets_no_identical_child():
    chunks = chunk_text("The lease renews every March. Rent rises three percent each year.")
    assert len(chunks) == 1 and chunks[0].parent_chunk_id is None
    assert _identical_children(chunks) == []


def test_a_large_parent_still_splits_into_children():
    para = "Clause {n}: the tenant shall maintain the premises in good repair and order. "
    text = "".join(para.format(n=i) for i in range(400))
    chunks = chunk_text(text)
    assert any(c.parent_chunk_id for c in chunks), "parent-context retrieval needs children on big parents"
    assert _identical_children(chunks) == []


def test_a_short_code_window_gets_no_identical_child():
    chunks = chunk_code("def renew(lease):\n    return lease.extend(months=12)\n", language="python")
    assert _identical_children(chunks) == []
    assert len(chunks) == 1


def _row(doc: str, text: str) -> dict:
    return {"processed_document_id": doc, "source_kind": "cld_file", "source_id": "s-" + doc, "content_text": text}


def test_search_keeps_one_hit_per_document_text():
    rows = {
        "parent": _row("d1", "Rent rises three percent."),
        "child": _row("d1", "Rent  rises three\npercent."),
        "other_doc": _row("d2", "Rent rises three percent."),
        "distinct": _row("d1", "The lease renews every March."),
    }
    kept = search_mod._drop_exact_text_duplicates(["parent", "child", "other_doc", "distinct"], rows)
    assert kept == ["parent", "other_doc", "distinct"]


def test_search_applies_the_dedupe_on_the_returned_order():
    src = stable_source(search_mod.search)
    assert "ordered = _drop_exact_text_duplicates(ordered, rows_by_id)" in src
