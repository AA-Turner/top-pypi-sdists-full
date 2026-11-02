"""Workbook + cloud-document resolvers — their CONTENT becomes searchable passages.

Verifies ``matrx_rag.sources._resolve_udt`` for ``workbook`` (workbench.udt_workbooks) and
``udt_document`` (workbench.udt_documents, Univer docs):

* the body is the LATEST snapshot, rendered through the host's ``univer_text_renderer`` seam;
* the row's name is the title, its description rides along;
* a row the caller did not create, a trashed row, and an anonymous call resolve to ``None``;
* an unconfigured renderer is loud (``RagNotConfiguredError``), never an empty body;
* both kinds are chunk kinds with a kernel read lane in search.

Fakes ``get_db_model`` with the resolver's ORM filter/order_by/limit/values chain; no live DB.
"""

from __future__ import annotations

import typing

import pytest
from matrx_rag import _ext, sources

OWNER = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
OTHER = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
ORG = "cccccccc-cccc-cccc-cccc-cccccccccccc"


class _Q:
    def __init__(self, rows):
        self._rows = rows

    def order_by(self, field):
        key = field.lstrip("-")
        return _Q(sorted(self._rows, key=lambda r: r.get(key), reverse=field.startswith("-")))

    def limit(self, n):
        return _Q(self._rows[:n])

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


def _row(id, name_col, name, **kw):
    return {
        "id": id, "created_by": OWNER, "organization_id": ORG, name_col: name,
        "description": "", "visibility": "internal", "metadata": {}, "deleted_at": None, **kw,
    }


def _render(kind, snapshot):
    return f"[{kind}] {snapshot['body']}"


@pytest.fixture
def models(monkeypatch):
    m = {
        "UdtWorkbooks": _Model([
            _row("wb-1", "workbook_name", "Q3 budget", description="Marketing spend"),
            _row("wb-gone", "workbook_name", "Trashed", deleted_at="2026-10-01"),
            {**_row("wb-other", "workbook_name", "Not mine"), "created_by": OTHER},
            _row("wb-empty", "workbook_name", "Blank"),
        ]),
        "UdtWorkbookSnapshots": _Model([
            {"id": "s-old", "workbook_id": "wb-1", "created_at": "2026-10-01", "snapshot": {"body": "OLD CELLS"}},
            {"id": "s-new", "workbook_id": "wb-1", "created_at": "2026-10-13", "snapshot": {"body": "Coffee\t4.5"}},
            {"id": "s-g", "workbook_id": "wb-gone", "created_at": "2026-10-13", "snapshot": {"body": "x"}},
            {"id": "s-o", "workbook_id": "wb-other", "created_at": "2026-10-13", "snapshot": {"body": "x"}},
        ]),
        "UdtDocuments": _Model([_row("doc-1", "document_name", "Kiln manual")]),
        "UdtDocumentSnapshots": _Model([
            {"id": "d-new", "document_id": "doc-1", "created_at": "2026-10-13",
             "snapshot": {"body": "# Firing\nCone 6 bisque"}},
        ]),
    }
    monkeypatch.setattr(sources, "get_db_model", lambda name, schema=None: m[name])
    monkeypatch.setitem(_ext._registry, "univer_text_renderer", _render)
    return m


@pytest.mark.asyncio
async def test_a_workbook_is_its_name_description_and_latest_snapshot(models):
    r = await sources.resolve("workbook", "wb-1", user_id=OWNER)
    assert r is not None and r.source_kind == "workbook"
    assert r.text == "# Q3 budget\n\nMarketing spend\n\n[workbook] Coffee\t4.5"
    assert "OLD CELLS" not in r.text
    assert r.owner_id == OWNER and r.organization_id == ORG
    assert r.metadata["snapshot_id"] == "s-new" and r.metadata["title"] == "Q3 budget"


@pytest.mark.asyncio
async def test_a_cloud_document_renders_through_the_host_renderer(models):
    r = await sources.resolve("udt_document", "doc-1", user_id=OWNER)
    assert r is not None and r.source_kind == "udt_document"
    assert r.text == "# Kiln manual\n\n[udt_document] # Firing\nCone 6 bisque"
    assert r.mime_type == "text/markdown"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kind,item,user",
    [("workbook", "wb-other", OWNER), ("workbook", "wb-1", OTHER), ("workbook", "wb-gone", OWNER),
     ("workbook", "wb-1", None), ("udt_document", "doc-1", None), ("workbook", "wb-empty", OWNER)],
)
async def test_unreadable_trashed_anonymous_or_empty_resolve_to_nothing(models, kind, item, user):
    assert await sources.resolve(kind, item, user_id=user) is None


@pytest.mark.asyncio
async def test_an_unconfigured_renderer_is_loud(models, monkeypatch):
    monkeypatch.setitem(_ext._registry, "univer_text_renderer", None)
    with pytest.raises(_ext.RagNotConfiguredError):
        await sources.resolve("workbook", "wb-1", user_id=OWNER)


def test_both_kinds_are_chunk_kinds_with_a_kernel_read_lane():
    from matrx_rag import search

    for kind in ("workbook", "udt_document"):
        assert kind in typing.get_args(sources.SourceKind)
        assert kind in search.CHUNK_SOURCE_KINDS
        assert search._ROW_KERNEL_TOKENS[kind] == kind


@pytest.mark.asyncio
async def test_a_record_people_are_co_editing_indexes_what_they_see_now(models, monkeypatch):
    """COLLAB-DESIGN C7: a live room's folded content, not the last save, and the staleness rides along."""
    calls = []

    async def current(kind, source_id, user_id):
        calls.append((kind, source_id, user_id))
        return {"body": "LIVE CELLS"}, {"source": "folded", "rev": 9, "head_rev": 9, "checkpoint_rev": 4}

    monkeypatch.setitem(_ext._registry, "univer_current_reader", current)
    r = await sources.resolve("workbook", "wb-1", user_id=OWNER)
    assert "LIVE CELLS" in r.text and "OLD CELLS" not in r.text
    assert r.metadata["collab"]["rev"] == 9
    assert calls == [("workbook", "wb-1", OWNER)]

    async def no_room(kind, source_id, user_id):
        return None

    monkeypatch.setitem(_ext._registry, "univer_current_reader", no_room)
    r2 = await sources.resolve("workbook", "wb-1", user_id=OWNER)
    assert "LIVE CELLS" not in r2.text and "collab" not in r2.metadata
