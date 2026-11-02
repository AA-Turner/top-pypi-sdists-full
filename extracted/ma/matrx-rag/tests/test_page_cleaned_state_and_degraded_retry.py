"""A page the cleaner emptied is CLEANED; a page the cleaner failed on is NOT.

Two defects, one state question (2026-10-06):

1. The batch lane (``rag_batch.page_clean``) and the live resume
   (``stages.run_clean``) treated ``cleaned_text == ""`` as "never cleaned".
   The cleaner legitimately returns ``""`` for an ``illegible_scan`` page, so
   every batch resume re-queued those pages — 280-330 times per page on live
   documents — and the document's joined clean/chunk step was never reached.
   ``cleaned_text`` is NOT NULL, so only ``section_kind`` (NULL until the
   cleaner writes the page) can tell the two apart: ``page_is_cleaned``.

2. When the cleaner call failed, ``clean_pdf_pages`` persisted the RAW text as
   ``cleaned_text`` (``degraded=True``), so every resume counted the page as
   done and it was never retried — with only a print to show for it.

Forcing function: before the fix ``page_is_cleaned`` did not exist, the resume
lookups used ``.exclude(cleaned_text="")``, and a degraded page reached
``persist_one`` with no ``system_error`` recorded.
"""

from __future__ import annotations

import asyncio
from matrx_utils.source_guard import stable_source
from pathlib import Path
from typing import Any

import matrx_orm
import matrx_rag.llm as llm_mod
from matrx_rag.llm import page_is_cleaned

PKG = Path(__file__).resolve().parents[1] / "matrx_rag"


def test_page_is_cleaned_truth_table():
    assert page_is_cleaned("", None) is False  # never touched by the cleaner
    assert page_is_cleaned("", "illegible_scan") is True  # cleaned to nothing
    assert page_is_cleaned("", "blank_or_garbage") is True
    assert page_is_cleaned("Chapter 1", "section") is True
    assert page_is_cleaned("Chapter 1", "") is True  # cleaned, unclassified
    assert page_is_cleaned(None, None) is False


def test_no_resume_lookup_tests_cleaned_text_emptiness():
    """Every "which pages are already cleaned?" site in this package uses the
    ONE predicate (the host's batch-lane sites are guarded host-side)."""
    for rel in ("stages.py", "pdf_pipeline.py"):
        src = (PKG / rel).read_text()
        assert 'exclude(cleaned_text="")' not in src, rel
        assert 'row["cleaned_text"] or "").strip()' not in src, rel
        assert "page_is_cleaned(" in src, rel


def _runner(monkeypatch, fail: set[int]) -> None:
    class _Runner:
        async def clean_page(self, raw: str, *, timeout: float | None = None):
            idx = int(raw.split("-")[1])
            if idx in fail:
                raise RuntimeError("provider 529 overloaded")
            return {"text": f"cleaned-{idx}", "section_kind": "letter"}

    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Runner())
    monkeypatch.setattr(llm_mod, "vcprint", lambda *a, **kw: None)


def test_degraded_page_is_not_persisted_and_files_a_system_error(monkeypatch):
    _runner(monkeypatch, fail={1})
    recorded: list[dict[str, Any]] = []

    async def _record_error(exc: BaseException, **kw: Any) -> None:
        recorded.append({"exc": exc, **kw})

    monkeypatch.setattr(matrx_orm, "record_error", _record_error)
    persisted: list[int] = []

    async def _persist(idx: int, _cleaned: Any) -> None:
        persisted.append(idx)

    out = asyncio.run(
        llm_mod.clean_pdf_pages(
            ["page-0", "page-1", "page-2"],
            persist_one=_persist,
            error_context={"processed_document_id": "d" * 36, "owner_id": "u" * 36},
        )
    )

    # This run still carries the raw text downstream ...
    assert out[1].degraded and out[1].text == "page-1"
    # ... but the DB never records it as cleaned, so the next run retries it.
    assert sorted(persisted) == [0, 2]
    assert len(recorded) == 1
    row = recorded[0]
    assert row["kind"] == "rag_page_clean_degraded"
    assert row["context"]["degraded_page_indexes"] == [1]
    assert row["context"]["processed_document_id"] == "d" * 36
    assert row["user_id"] == "u" * 36


def test_healthy_run_records_nothing(monkeypatch):
    _runner(monkeypatch, fail=set())
    recorded: list[Any] = []

    async def _record_error(exc: BaseException, **kw: Any) -> None:
        recorded.append(exc)

    monkeypatch.setattr(matrx_orm, "record_error", _record_error)
    asyncio.run(llm_mod.clean_pdf_pages(["page-0", "page-1"]))
    assert recorded == []


def test_run_clean_passes_its_document_to_the_error_record():
    from matrx_rag import stages

    # run_clean is the single-flight wrapper; the page clean itself lives in _run_clean_held.
    src = stable_source(stages._run_clean_held)
    assert "error_context=" in src
