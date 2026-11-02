"""READABLE SOURCES, ONCE PER SEARCH (2026-10-15).

A Source-less chunk of a kernel-decided kind (note, task, project, library_doc, document) used to cost one
``iam.has_access_for`` call per candidate row inside the recall doors; a ``source_kinds=['note']`` search
walked every note chunk (~5-11 s). The search now asks ``rag.readable_sources`` once, as the person, and
hands the per-kind ids to every door in ``p_filters.readable_sources``. These tests pin the Python half:
which kinds are asked for, that the answer is complete or the search fails loudly, and that every door
carries the set. The database half (set == per-row kernel; doors answer the same) is the live guard
``tests/test_recall_readable_sources_match_the_kernel.py`` in the aidream repo.
"""

from __future__ import annotations

import pytest

from matrx_rag import search

_USER = "11111111-1111-4111-8111-111111111111"


def test_the_kinds_asked_follow_the_narrowing_and_never_include_files():
    assert search.readable_source_kinds_for(None) == search.READABLE_SOURCE_KINDS
    assert search.readable_source_kinds_for([]) == search.READABLE_SOURCE_KINDS
    assert search.readable_source_kinds_for(["note"]) == ("note",)
    assert search.readable_source_kinds_for(["document", "task", "cld_file"]) == (
        "task",
        "document",
    )
    # cld_file keeps the doors' per-row check (its set costs ~5 s; its Source-less passages are rare).
    assert search.readable_source_kinds_for(["cld_file"]) == ()
    assert "cld_file" not in search.READABLE_SOURCE_KINDS


async def test_the_sources_set_is_asked_as_the_person_beside_the_documents_set(monkeypatch):
    import matrx_orm
    from matrx_orm.core import db_function

    calls: list = []

    async def fake_ids(user_id, token, level):
        calls.append(("docs", user_id, token))
        return ["d1"]

    async def fake_as(actor, database, schema, function, *args, mode="scalar", **_kw):
        calls.append(
            ("as", actor, f"{schema}.{function}", args[0].value, args[0].element_type, mode)
        )
        return {"note": ["n1", "n2"], "task": []}

    monkeypatch.setattr(matrx_orm, "platform_accessible_ids", fake_ids)
    monkeypatch.setattr(db_function, "call_function_as", fake_as)
    readable = await search.resolve_readable_documents(
        _USER, source_kinds=("note", "task", "cld_file", "note")
    )
    assert readable.processed_document_ids == ("d1",)
    assert readable.source_ids == {"note": ("n1", "n2"), "task": ()}
    assert ("as", _USER, "rag.readable_sources", ["note", "task"], "text", "scalar") in calls

    # No kinds: the documents set alone, exactly as before.
    calls.clear()
    plain = await search.resolve_readable_documents(_USER)
    assert plain.source_ids == {} and [c[0] for c in calls] == ["docs"]


async def test_an_incomplete_sources_answer_fails_the_search_never_narrows_it(monkeypatch):
    import matrx_orm
    from matrx_orm.core import db_function

    async def fake_ids(user_id, token, level):
        return []

    async def fake_as(actor, database, schema, function, *args, mode="scalar", **_kw):
        return {"note": ["n1"]}  # "task" missing

    monkeypatch.setattr(matrx_orm, "platform_accessible_ids", fake_ids)
    monkeypatch.setattr(db_function, "call_function_as", fake_as)
    with pytest.raises(RuntimeError, match="readable_sources"):
        await search.resolve_readable_documents(_USER, source_kinds=("note", "task"))


async def test_every_recall_door_carries_the_sources_set(monkeypatch):
    calls: list = []

    async def fake_door(function, *args):
        calls.append((function, args))
        if function == "recall_entities":
            return [
                {
                    "entity_id": "e1",
                    "name": "Acme",
                    "kind": "org",
                    "cluster_id": None,
                    "organization_id": "o1",
                }
            ]
        return [{"chunk_id": "k1"}]

    monkeypatch.setattr(search, "_door", fake_door)
    readable = search.ReadableDocuments(
        user_id=_USER, processed_document_ids=("d1",), source_ids={"note": ("n1",), "document": ()}
    )
    filters = {"leaf_only": True, "source_kinds": ["note", "document"]}
    await search._recall_vector_door(
        "rag.embeddings_x", [0.5], user_id=_USER, readable=readable, k=100, filters=filters
    )
    await search._recall_lexical_door(
        "acme", user_id=_USER, readable=readable, k=100, filters=filters
    )
    await search._recall_entity_door("acme corp", user_id=_USER, readable=readable, filters=filters)
    by = {f: a for f, a in calls}
    want = {"note": ["n1"], "document": []}
    assert by["recall_vector"][5]["readable_sources"] == want
    assert by["recall_lexical"][4]["readable_sources"] == want
    assert by["recall_entity_chunks"][5]["readable_sources"] == want
    # The caller's own filters are never mutated.
    assert "readable_sources" not in filters
