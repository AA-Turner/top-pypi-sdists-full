"""content.document resolver — Spaces pages, annotations and notes become searchable text.

Owner ruling (Arman, 2026-10-06): agents search all three kinds of ``content.document`` row the
way old notes already are. Verifies ``matrx_rag.sources._resolve_document``:

* a Spaces page renders its CURRENT ``content.space_payload`` blocks (headings keep their level,
  to-dos / lists / quotes their markers; layout + child-page pointers add nothing);
* an annotation carries the highlighted passage, the comment and what it annotates;
* a note is title + markdown body;
* a row the caller did not create, a trashed row, and an archived row resolve to ``None``.

Fakes ``get_db_model`` with the resolver's ORM filter/values chain; no live DB.
"""

from __future__ import annotations

import pytest
from matrx_rag import sources

OWNER = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
OTHER = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
ORG = "cccccccc-cccc-cccc-cccc-cccccccccccc"
T_SPACE, T_ANN, T_NOTE = "t-space", "t-annotation", "t-note"

SNAPSHOT = {
    "v": 1,
    "blocks": [
        {"id": "h", "type": "heading", "props": {"level": 2}, "text": [{"text": "Onboarding "}, {"text": "checklist"}]},
        {"id": "c", "type": "columnList", "children": [
            {"id": "col", "type": "column", "children": [
                {"id": "t1", "type": "todo", "props": {"checked": True}, "text": [{"text": "Collect brand assets"}]},
                {"id": "t2", "type": "todo", "text": [{"text": "Book the kickoff"}]},
            ]},
        ]},
        {"id": "p", "type": "page", "props": {"spaceId": "child"}},
        {"id": "d", "type": "divider"},
        {"id": "q", "type": "quote", "text": [{"text": "The captions finally sound like me."}]},
        {"id": "db", "type": "database", "props": {"title": "Clients"}},
        {"id": "img", "type": "image", "props": {"caption": [{"text": "Studio"}]}},
        {"id": "x", "type": "text", "text": [{"text": "Cardamom buns proof overnight."}]},
    ],
}


class _Q:
    def __init__(self, rows):
        self._rows = rows

    async def values(self, *fields):
        return [{f: r.get(f) for f in fields} for r in self._rows]


class _Model:
    def __init__(self, rows):
        self.rows = rows

    def filter(self, **kw):
        def ok(r):
            for k, v in kw.items():
                if k.endswith("__isnull"):
                    if (r.get(k[: -len("__isnull")]) is None) != v:
                        return False
                elif r.get(k) != v:
                    return False
            return True

        return _Q([r for r in self.rows if ok(r)])


def _doc(id, type_id, title, body="", fmt="markdown", **kw):
    return {
        "id": id, "created_by": OWNER, "organization_id": ORG, "document_type_id": type_id,
        "title": title, "format": fmt, "body": body, "content_version": 3, "visibility": "internal",
        "metadata": {}, "deleted_at": None, "archived_at": None, **kw,
    }


@pytest.fixture
def models(monkeypatch):
    m = {
        "Document": _Model([
            _doc("space-1", T_SPACE, "Studio OS", body="stale projection", fmt="spaces"),
            _doc("space-nopayload", T_SPACE, "Fresh page", body="Body projection only", fmt="spaces"),
            _doc("ann-1", T_ANN, "Highlight: Water is an exception", body="Exam point: ice floats"),
            _doc("note-1", T_NOTE, "Kiln notes", body="Cone 6 bisque, then glaze."),
            _doc("gone", T_NOTE, "Trashed", body="x", deleted_at="2026-10-01"),
            _doc("archived", T_NOTE, "Archived", body="x", archived_at="2026-10-01"),
            {**_doc("source-doc", T_NOTE, "Chemistry chapter 3", body="..."), "created_by": OTHER},
        ]),
        "Categories": _Model([{"id": T_SPACE, "slug": "space"}, {"id": T_ANN, "slug": "annotation"}, {"id": T_NOTE, "slug": "note"}]),
        "SpacePayload": _Model([
            {"document_id": "space-1", "content_version": 2, "snapshot": {"blocks": [{"type": "text", "text": [{"text": "OLD VERSION"}]}]}},
            {"document_id": "space-1", "content_version": 3, "snapshot": SNAPSHOT},
        ]),
        "Associations": _Model([
            {"source_type": "document", "source_id": "ann-1", "role": "annotates", "deleted_at": None,
             "target_type": "document", "target_id": "source-doc",
             "payload": {"__kind": "text_anchor_set", "anchors": [{"exact": "**Water is an exception:**"}]}},
        ]),
        "Notes": _Model([]),
    }
    monkeypatch.setattr(sources, "get_db_model", lambda name, schema=None: m[name])
    return m


@pytest.mark.asyncio
async def test_a_spaces_page_renders_its_current_blocks(models):
    r = await sources.resolve("document", "space-1", user_id=OWNER)
    assert r is not None and r.source_kind == "document"
    assert r.text.startswith("# Studio OS")
    for line in ("## Onboarding checklist", "- [x] Collect brand assets", "- [ ] Book the kickoff",
                 "> The captions finally sound like me.", "Table: Clients", "Studio",
                 "Cardamom buns proof overnight."):
        assert line in r.text
    assert "OLD VERSION" not in r.text and "stale projection" not in r.text
    assert "child" not in r.text
    assert r.metadata["document_type"] == "space" and r.organization_id == ORG and r.owner_id == OWNER


@pytest.mark.asyncio
async def test_a_spaces_page_without_a_payload_falls_back_to_its_body(models):
    r = await sources.resolve("document", "space-nopayload", user_id=OWNER)
    assert r is not None and "Body projection only" in r.text


@pytest.mark.asyncio
async def test_an_annotation_carries_highlight_comment_and_what_it_annotates(models):
    r = await sources.resolve("document", "ann-1", user_id=OWNER)
    assert r is not None
    assert "> **Water is an exception:**" in r.text
    assert "Exam point: ice floats" in r.text
    assert "Annotates document: Chemistry chapter 3" in r.text
    assert r.metadata["annotates"] == [{"type": "document", "id": "source-doc"}]


@pytest.mark.asyncio
async def test_a_note_document_is_title_and_markdown(models):
    r = await sources.resolve("document", "note-1", user_id=OWNER)
    assert r is not None and r.text == "# Kiln notes\n\nCone 6 bisque, then glaze."
    assert r.mime_type == "text/markdown"


@pytest.mark.asyncio
@pytest.mark.parametrize("doc_id,user", [("note-1", OTHER), ("gone", OWNER), ("archived", OWNER), ("note-1", None)])
async def test_unreadable_trashed_archived_or_anonymous_resolve_to_nothing(models, doc_id, user):
    assert await sources.resolve("document", doc_id, user_id=user) is None


def test_the_document_kind_is_a_chunk_kind_with_a_kernel_read_lane():
    import typing

    from matrx_rag import search

    assert "document" in typing.get_args(sources.SourceKind)
    assert search._ROW_KERNEL_TOKENS["document"] == "document"
