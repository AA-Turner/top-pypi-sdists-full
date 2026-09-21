"""A DRIVER'S TEXT IS NEVER THE SENTENCE A PERSON READS.

The guard for the fourteenth cold walk's second "no" (2026-09-20,
``common-docs/projects/masterwork-methods-census/jobs-bar-2026-09-16/cold-walk-14``):
``/acquisition`` printed, inside a block row, as the person-facing account of what
happened to a first-time Expert's file::

    Matrx ORM  |  QueryTimeoutError Query timed out during execute_query
    Operation: execute_query Query:     INSERT INTO docproc.processed_documents
    (id, organization_id, owner_id, …) VALUES ($1, $2, $…
    Args: ('03e3dab7-…', '5dc930e9-…', '87a6e699-…', 'cld_file', …)

The string below is the LIVE one, read back out of
``platform.acquisition_block.error_sentence`` for row
``f0f4b90d-de6e-4e66-a35d-7424d3da1f60`` — not one an author invented to pass.

The guard is on the SEAM, not on the caller that did it: ``error_sentence`` is a
person-facing column with ~14 callers, and the next bad ``except`` must not be able
to reach a screen either. It fails against the seam as it stood before this fix
(the raw string was written straight through) and passes after it.
"""

from __future__ import annotations

import re
from typing import Any

import pytest

from matrx_scraper.blocks.record import record_block

#: Read from the live database, 2026-09-20, truncated exactly as the column holds it.
LIVE_LEAK = (
    "Matrx ORM  |  QueryTimeoutError Query timed out during execute_query "
    "Operation: execute_query Query:     INSERT INTO docproc.processed_documents "
    "(id, organization_id, owner_id, source_kind, source_id, derivation_kind, "
    "derivation_metadata, name, mime_type, total_pages, source_hash, content, "
    "structured_json, metadata, created_at, updated_at, extractor_name, "
    "extractor_version, rag_boost) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, "
    "$11, $12, $13, $14, $15, $16, $17, $18, $19) "
    "Args: ('03e3dab7-1f1c-4d2e-9f40-3a7f6b2c0d11', "
    "'5dc930e9-bd65-44a1-8369-af773f6e1a5b', "
    "'87a6e699-3622-4869-8843-d0867456c0dd', 'cld_file', …)"
)

#: What must never appear in a sentence a person reads. Each shape was seen live.
FORBIDDEN = (
    re.compile(r"INSERT\s+INTO", re.I),
    re.compile(r"\$\d+\s*,\s*\$\d+"),
    re.compile(r"\bArgs\s*:"),
    re.compile(r"\bQuery\s*:"),
    re.compile(r"Matrx ORM\s*\|"),
    re.compile(r"Traceback \(most recent call last\)"),
    re.compile(r"\bdocproc\.processed_documents\b"),
)


class _Recorder:
    """The one ``BlockStore`` call the seam makes, captured."""

    def __init__(self) -> None:
        self.created: dict[str, Any] | None = None

    async def get_many(self, **_: Any) -> list[Any]:
        return []

    async def find_open(self, **_: Any) -> Any | None:
        return None

    async def create(self, **fields: Any) -> Any:
        self.created = fields
        return type("Row", (), {"id": "11111111-1111-1111-1111-111111111111"})()

    async def update(self, block_id: str, **fields: Any) -> Any:  # pragma: no cover
        raise AssertionError("this test never takes the dedupe path")


async def _record(sentence: str, store: _Recorder) -> dict[str, Any]:
    await record_block(
        organization_id="5dc930e9-bd65-44a1-8369-af773f6e1a5b",
        input_ref="37af3c33-df85-4ad0-a4e6-a7a52424e826",
        input_label="page_03 (1).jpg",
        source_type="file",
        engine="file_reader",
        error_class="processing_failed",
        error_sentence=sentence,
        detail={"stage": "materialize", "file_name": "page_03 (1).jpg"},
        store=store,  # type: ignore[arg-type]
    )
    assert store.created is not None, "the seam recorded nothing at all"
    return store.created


@pytest.mark.asyncio
async def test_the_live_leak_never_becomes_the_sentence() -> None:
    row = await _record(LIVE_LEAK, _Recorder())
    sentence = str(row["error_sentence"])
    for shape in FORBIDDEN:
        assert not shape.search(sentence), (
            f"{shape.pattern!r} reached the person-facing sentence: {sentence!r}"
        )


@pytest.mark.asyncio
async def test_the_sentence_names_the_cause_and_carries_a_remedy() -> None:
    row = await _record(LIVE_LEAK, _Recorder())
    sentence = str(row["error_sentence"]).lower()
    # The classified cause: our database, not their file.
    assert "database" in sentence
    # Law #4 — a stand-in without a remedy is a dead end wearing a sentence.
    assert "try it again" in sentence or "with the team" in sentence


@pytest.mark.asyncio
async def test_the_raw_text_is_kept_in_the_diagnostic_field() -> None:
    row = await _record(LIVE_LEAK, _Recorder())
    detail = row["detail"]
    assert detail["stage"] == "materialize", "the caller's own detail survives"
    assert "INSERT INTO" in detail["diagnostic"]["raw_error"], (
        "the raw text must be KEPT — the rule moves it out of the sentence, it does "
        "not throw the diagnosis away"
    )


@pytest.mark.asyncio
async def test_a_sentence_written_for_a_person_is_left_exactly_alone() -> None:
    """The other half of the rule, and the one a blunt filter would break.

    A codec's careful refusal must survive the seam word for word. Over-cleaning
    a real sentence is the same lie in the other direction.
    """
    honest = (
        "“03-protected-handbook.epub” is copy-protected (Adobe ADEPT), so we cannot "
        "read it — and we will never strip a publisher’s protection. What does work: "
        "a DRM-free copy from the publisher, or the library’s own reader."
    )
    row = await _record(honest, _Recorder())
    assert row["error_sentence"] == honest
    assert "diagnostic" not in row["detail"]


@pytest.mark.asyncio
async def test_a_bare_exception_class_is_not_a_sentence_either() -> None:
    row = await _record("QueryTimeoutError", _Recorder())
    sentence = str(row["error_sentence"])
    assert sentence != "QueryTimeoutError"
    assert "database" in sentence.lower()
    assert row["detail"]["diagnostic"]["raw_error"] == "QueryTimeoutError"
