"""A page the cleaner gave up on (``clean_failed``) keeps its content downstream.

Defect (2026-10-06): c5c04f871e saves a given-up page as ``cleaned_text=""`` +
``section_kind='clean_failed'``. Chunking and the joined ``clean_content`` read
``cleaned_text`` only, so that page's content vanished from retrieval.
``illegible_scan`` is genuinely empty and must STAY empty.

Forcing function: pre-fix there is no ``page_text_for_downstream`` (leg A) and
``stages._load_cleaned_pages`` returns text="" for the clean_failed page (leg B).
"""

from __future__ import annotations

import asyncio
from typing import Any

import matrx_rag.stages as stages
from matrx_rag.llm import page_text_for_downstream

ROWS = [
    {
        "page_index": 0,
        "cleaned_text": "good clean",
        "raw_text": "good raw",
        "section_kind": "body",
        "section_subtype": "",
        "section_title": None,
        "is_continuation": False,
    },
    {
        "page_index": 1,
        "cleaned_text": "",
        "raw_text": "RAW OF FAILED PAGE",
        "section_kind": "clean_failed",
        "section_subtype": "",
        "section_title": None,
        "is_continuation": False,
    },
    {
        "page_index": 2,
        "cleaned_text": "",
        "raw_text": "smudge",
        "section_kind": "illegible_scan",
        "section_subtype": "",
        "section_title": None,
        "is_continuation": False,
    },
]


class _Query:
    def filter(self, **_kw: Any) -> _Query:
        return self

    def order_by(self, *_a: Any) -> _Query:
        return self

    async def values(self, *_cols: str) -> list[dict[str, Any]]:
        return [dict(r) for r in ROWS]


class _Model(_Query):
    pass


def test_helper_falls_back_only_for_clean_failed() -> None:
    assert page_text_for_downstream(ROWS[0]) == "good clean"
    assert page_text_for_downstream(ROWS[1]) == "RAW OF FAILED PAGE"
    assert page_text_for_downstream(ROWS[2]) == ""


def test_stage_loader_keeps_failed_page_content(monkeypatch: Any) -> None:
    monkeypatch.setattr(stages, "get_db_model", lambda _name: _Model())
    pages = asyncio.run(stages._load_cleaned_pages("doc"))
    assert [p.text for p in pages] == ["good clean", "RAW OF FAILED PAGE", ""]
    assert "RAW OF FAILED PAGE" in "\n\n".join(p.text for p in pages)
