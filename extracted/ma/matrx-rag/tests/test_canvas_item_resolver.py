"""The canvas resolver: a canvas item's title, description and every string its content carries.

Runs the REAL ``matrx_rag.sources.resolve("canvas_item", …)`` over a faked model that honours
the resolver's filters. Before 2026-10-25 the kind did not exist (``resolve`` raised
``Unknown source_kind``), so every case here failed then.
"""

from __future__ import annotations

import json

import pytest
from matrx_rag import sources

OWNER = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
CANVAS = "55555555-5555-5555-5555-555555555555"


class _Q:
    def __init__(self, rows):
        self._rows = rows

    async def values(self, *fields):
        return [{f: r.get(f) for f in fields} for r in self._rows]


class _Canvas:
    def __init__(self, rows):
        self._rows = rows

    def filter(self, *, id, created_by, deleted_at__isnull):
        return _Q([r for r in self._rows if r["id"] == id and r["created_by"] == created_by and r["deleted_at"] is None])


def _row(**kw):
    row = {
        "id": CANVAS, "created_by": OWNER, "organization_id": "org", "title": "Polyatomic ions",
        "description": None, "type": "flashcards", "conversation_id": "conv", "source_type": "model_direct",
        "deleted_at": None,
        "content": {"type": "flashcards", "metadata": {"model": "x"}, "data": {"cards": [
            {"front": "What is NO3-?", "back": "nitrate", "tags": ["chemistry"]}]}},
    }
    row.update(kw)
    return row


@pytest.fixture
def wire(monkeypatch):
    def _wire(rows):
        monkeypatch.setattr(sources, "get_db_model", lambda name, schema=None: {"CanvasItems": _Canvas(rows)}[name])

    return _wire


@pytest.mark.asyncio
async def test_canvas_text_is_title_and_content_strings(wire):
    wire([_row()])
    r = await sources.resolve("canvas_item", CANVAS, None, user_id=OWNER)
    assert r is not None and r.source_kind == "canvas_item"
    assert r.text.splitlines()[0] == "Polyatomic ions"
    assert "What is NO3-?" in r.text and "nitrate" in r.text and "chemistry" in r.text
    assert '"model"' not in r.text and "flashcards" not in r.text
    assert r.metadata["conversation_id"] == "conv"


@pytest.mark.asyncio
async def test_canvas_content_stored_as_a_json_string_is_decoded(wire):
    wire([_row(content=json.dumps({"data": "| a | b |"}))])
    r = await sources.resolve("canvas_item", CANVAS, None, user_id=OWNER)
    assert r is not None and r.text.endswith("| a | b |") and "{" not in r.text


@pytest.mark.asyncio
async def test_someone_elses_or_trashed_canvas_is_absent(wire):
    wire([_row(created_by="other")])
    assert await sources.resolve("canvas_item", CANVAS, None, user_id=OWNER) is None
    wire([_row(deleted_at="2026-10-01")])
    assert await sources.resolve("canvas_item", CANVAS, None, user_id=OWNER) is None
    assert await sources.resolve("canvas_item", CANVAS, None, user_id=None) is None
