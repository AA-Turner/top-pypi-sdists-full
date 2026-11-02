"""An all-illegible document reads as CLEANED to page verification.

Defect (2026-10-06): ``verify_processed_document`` decided "was this doc
cleaned?" from ``cleaned_text`` emptiness. A doc whose every page the cleaner
classed ``illegible_scan`` (cleaned to "") looked never-cleaned, so the
``clean_emptied`` flag — real content the cleaner blanked — was suppressed.
Forcing function: pre-fix this report has no ``clean_emptied`` flags.
"""

from __future__ import annotations

import contextlib
from typing import Any

import matrx_rag.page_verification as pv


class _Query:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def filter(self, **_kw: Any) -> _Query:
        return self

    def order_by(self, *_a: Any) -> _Query:
        return self

    async def values(self, *_cols: str) -> list[dict[str, Any]]:
        return self._rows


def _install(monkeypatch, rows: list[dict[str, Any]]) -> None:
    class _Docs:
        @staticmethod
        async def exists(**_kw: Any) -> bool:
            return True

    class _Pages:
        @staticmethod
        def filter(**_kw: Any) -> _Query:
            return _Query(rows)

        @staticmethod
        async def update_where(*_a: Any, **_kw: Any) -> None:
            return None

    monkeypatch.setattr(
        pv, "get_db_model", lambda name: _Docs if name == "ProcessedDocuments" else _Pages
    )

    @contextlib.asynccontextmanager
    async def _tx():
        yield

    monkeypatch.setattr(pv, "transaction", _tx)


def _page(n: int, cleaned: str, kind: str | None) -> dict[str, Any]:
    return {
        "page_number": n,
        "raw_text": "smudged scan text " * 20,
        "cleaned_text": cleaned,
        "section_kind": kind,
        "extraction_confidence": 0.9,
        "image_cld_file_id": None,
    }


async def test_all_illegible_doc_is_cleaned(monkeypatch):
    _install(monkeypatch, [_page(1, "", "illegible_scan"), _page(2, "", "illegible_scan")])
    report = await pv.verify_processed_document("d" * 36)
    assert report.counts.get(pv.CLEAN_EMPTIED) == 2


async def test_never_cleaned_doc_is_not_flagged_as_emptied(monkeypatch):
    _install(monkeypatch, [_page(1, "", None), _page(2, "", None)])
    report = await pv.verify_processed_document("d" * 36)
    assert pv.CLEAN_EMPTIED not in report.counts
