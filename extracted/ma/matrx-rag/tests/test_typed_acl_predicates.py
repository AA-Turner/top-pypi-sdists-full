from __future__ import annotations

import re

from matrx_files.db.models_files import Files
from matrx_rag import data_stores, search
from matrx_rag.db.models_docproc import ProcessedDocuments
from matrx_rag.db.models_rag import DataStoreGrants, DataStoreMembers, KgChunks

from db.models.iam import Memberships, OrgIndustries, Permissions, SystemOrgs
from db.models.platform import Associations
from db.models.workbench import Notes

_MODELS = {
    model.__name__: model
    for model in (
        Associations,
        DataStoreGrants,
        DataStoreMembers,
        Files,
        KgChunks,
        Memberships,
        Notes,
        OrgIndustries,
        Permissions,
        ProcessedDocuments,
        SystemOrgs,
    )
}


def _resolve_model(name: str, schema: str | None = None):
    return _MODELS[name]


def _assert_dense_params(sql: str, params: list[object]) -> None:
    refs = {int(value) for value in re.findall(r"\$(\d+)", sql)}
    assert refs == set(range(1, len(params) + 1))


_USER = "11111111-1111-4111-8111-111111111111"
_DOC = "44444444-4444-4444-8444-444444444444"


def _readable(ids=(_DOC,)):
    return search.ReadableDocuments(user_id=_USER, processed_document_ids=tuple(ids))


def test_visibility_acl_is_the_kernel_set_not_hand_written_rules(monkeypatch):
    """REBASED ON THE KERNEL (Knowledge Hub H1, 2026-09-27).

    A chunk of a Source is readable when the Source is in the person's kernel set
    (``iam.accessible_entity_ids``); a chunk with no Source asks
    ``iam.has_access_for`` about the row its ``source_id`` names. The hand-written
    lanes it replaced — every member of the chunk's organization, note/file share
    rules re-derived from ``iam.permissions`` — must never come back: the org lane
    handed colleagues each other's personal notes (measured on the clone,
    2026-09-27: 43 chunks of 32 personal notes to test@test.com)."""
    monkeypatch.setattr(search, "get_db_model", _resolve_model)
    predicate = search._build_visibility_clause(
        user_id=_USER, organization_id=None, chunk_alias="c", readable=_readable()
    )
    params: list[object] = []
    sql = predicate.as_sql(params, current_table="c")

    _assert_dense_params(sql, params)
    # The Source lane: a hashed semi-join over the kernel set, never = ANY per row.
    assert "(c.processed_document_id) IN (SELECT * FROM unnest(" in sql
    assert [_DOC] in params
    # Rows without a Source: the kernel, per row, with the person passed explicitly.
    assert "iam.has_access_for(CAST($" in sql
    assert "CAST(c.source_id AS uuid)" in sql
    for token in ("note", "task", "project", "file", "library_doc"):
        assert token in params
    # The hand-written rules are gone.
    assert "iam.permissions" not in sql
    assert "workbench.notes" not in sql
    assert "files.files" not in sql
    assert "iam.memberships.organization_id = c.organization_id" not in sql
    # The two sharing lanes the kernel does not model on the document row stay.
    assert "rag.data_store_members.source_id = c.source_id" in sql
    assert (
        "rag.data_store_grants.data_store_id = "
        "rag.data_store_members.data_store_id"
    ) in sql
    # THE GLOBAL LANE IS THE SYSTEM-ORG TEST, NEVER A NULL TEST (db-rules §2/§6e).
    assert "iam.system_orgs.organization_id = c.organization_id" in sql
    assert "iam.system_orgs.global_readable" in sql
    assert "c.organization_id IS NULL" not in sql


def test_visibility_acl_refuses_without_the_kernel_set(monkeypatch):
    """No caller reaches chunks without the kernel having answered for the person."""
    import pytest

    monkeypatch.setattr(search, "get_db_model", _resolve_model)
    with pytest.raises(ValueError, match="readable-document set"):
        search._build_visibility_clause(user_id=_USER, organization_id=None, chunk_alias="c")
    other = search.ReadableDocuments(user_id="99999999-9999-4999-8999-999999999999", processed_document_ids=())
    with pytest.raises(ValueError, match="readable-document set"):
        search._build_visibility_clause(
            user_id=_USER, organization_id=None, chunk_alias="c", readable=other
        )


def test_empty_kernel_set_reads_no_sources(monkeypatch):
    monkeypatch.setattr(search, "get_db_model", _resolve_model)
    params: list[object] = []
    sql = search._build_visibility_clause(
        user_id=_USER, organization_id=None, chunk_alias="c", readable=_readable(())
    ).as_sql(params, current_table="c")
    _assert_dense_params(sql, params)
    assert "unnest(" not in sql
    assert "FALSE" in sql


def test_vector_acl_correlates_to_joined_chunk_not_embedding_table(monkeypatch):
    """The vector query starts FROM an embedding table and JOINs chunks AS c.

    Chunk correlations inside ACL EXISTS clauses must name ``c`` explicitly;
    an unqualified OuterRef binds to the embedding table and generates a live
    ``embeddings_*.source_id does not exist`` failure.
    """
    monkeypatch.setattr(search, "get_db_model", _resolve_model)
    predicate = search._build_visibility_clause(
        user_id=_USER, organization_id=None, chunk_alias="c", readable=_readable()
    )
    params: list[object] = []
    embedding_table = "rag.embeddings_voyage_4_large_1024"
    sql = predicate.as_sql(params, current_table=embedding_table)

    _assert_dense_params(sql, params)
    assert "rag.data_store_members.source_kind = c.source_kind" in sql
    assert "rag.data_store_members.source_id = c.source_id" in sql
    assert "(c.processed_document_id) IN" in sql
    assert f"{embedding_table}.source_id" not in sql
    assert f"{embedding_table}.processed_document_id" not in sql


def test_vector_leaf_filter_correlates_to_joined_chunk_not_embedding_table(monkeypatch):
    """The child-existence check must correlate to ``c.id`` in vector recall."""
    monkeypatch.setattr(search, "get_db_model", _resolve_model)
    params: list[object] = []
    embedding_table = "rag.embeddings_voyage_4_large_1024"
    sql = search._leaf_chunk_predicate().as_sql(
        params,
        current_table=embedding_table,
    )

    _assert_dense_params(sql, params)
    assert "parent_chunk_id = c.id" in sql
    assert f"{embedding_table}.id" not in sql


def test_scope_predicate_keeps_alias_pairs_and_correlates_source_id(monkeypatch):
    monkeypatch.setattr(search, "get_db_model", _resolve_model)
    params: list[object] = []
    sql = search._build_scope_filter_predicate(
        ["22222222-2222-4222-8222-222222222222"]
    ).as_sql(params, current_table="c")

    _assert_dense_params(sql, params)
    assert "CAST(source_id AS text) = c.source_id" in sql
    for source_kind, entity_types in search._SCOPE_ENTITY_TYPE_ALIASES.items():
        assert source_kind in params
        assert list(entity_types) in params
    # A scoped Source (processed document) reaches its chunks by id and by origin.
    assert search.SCOPE_SOURCE_DOCUMENT_TOKEN in params
    assert "source_id = c.processed_document_id" in sql
    assert "source_kind = c.source_kind AND source_id = c.source_id" in sql
    assert "source_id = docproc.processed_documents.id" in sql


def test_scope_predicate_correlates_to_the_chunk_inside_the_vector_lane(monkeypatch):
    """The vector lane's base table is the embedding table, with kg_chunks joined
    as ``c``. A bare OuterRef renders against the BASE table, so every scoped
    vector search crashed live (2026-09-27: "column
    embeddings_voyage_4_large_1024.source_id does not exist"). Rendered in the
    vector lane's frame, the predicate must name only ``c.`` columns."""
    monkeypatch.setattr(search, "get_db_model", _resolve_model)
    embedding_table = "rag.embeddings_voyage_4_large_1024"
    params: list[object] = []
    sql = search._build_scope_filter_predicate(
        ["22222222-2222-4222-8222-222222222222"]
    ).as_sql(params, current_table=embedding_table)

    _assert_dense_params(sql, params)
    assert f"{embedding_table}." not in sql
    assert "= c.source_id" in sql
    assert "= c.processed_document_id" in sql
    assert "= c.source_kind" in sql


def test_a_person_with_no_organization_still_sees_global_grants_and_never_binds_none(monkeypatch):
    """`_grant_acl_predicate(org)` was replaced (e6b100cb65) by the set-based `_entitled_store_ids`.
    The class it guarded survives: a missing organization must never reach the grant query as a
    bound ``None`` / ``IS NULL`` comparison — it reads ``global`` grants only."""
    import asyncio

    seen: list[object] = []

    class _Grants:
        def filter(self, *args, **kwargs):
            seen.append((args, kwargs))
            return self

        def distinct(self):
            return self

        def limit(self, _n):
            return self

        async def values(self, *_fields):
            return [{"data_store_id": "store-global"}]

    class _NoIndustries:
        def filter(self, *a, **k):
            raise AssertionError("industry grants need an organization; none was given")

    def _models(name, schema=None):
        return {"DataStoreGrants": _Grants(), "OrgIndustries": _NoIndustries()}[name]

    monkeypatch.setattr(data_stores, "get_db_model", _models)
    ids = asyncio.run(data_stores._entitled_store_ids([None]))
    assert ids == ["store-global"]
    assert len(seen) == 1
    assert "None" not in repr(seen[0]).replace("Q(", "")


def test_scope_filter_unions_sources_filed_under_the_project(monkeypatch):
    """A conversation attached to a project searches the project's scopes AND
    the Sources filed under it (2026-09-27) — a union, never an intersection."""
    monkeypatch.setattr(search, "get_db_model", _resolve_model)
    doc = "33333333-3333-4333-8333-333333333333"
    params: list[object] = []
    sql = search._build_scope_filter_predicate(
        ["22222222-2222-4222-8222-222222222222"], [doc]
    ).as_sql(params, current_table="rag.embeddings_voyage_4_large_1024")
    _assert_dense_params(sql, params)
    assert [doc] in params
    assert "c.processed_document_id = ANY" in sql
    assert ") OR (" in sql or " OR " in sql

    params = []
    only_docs = search._build_scope_filter_predicate([], [doc]).as_sql(
        params, current_table="c"
    )
    assert "target_type" not in only_docs
    assert [doc] in params


async def test_query_vectors_are_reused_for_the_submit_that_follows_typing(monkeypatch):
    calls: list = []

    async def fake_embed(model, texts, *, input_type, organization_id):
        calls.append((model, tuple(texts), input_type))
        return [[0.1, 0.2]]

    monkeypatch.setattr(search, "embed", fake_embed)
    search._query_embed_cache.clear()
    first = await search._embed_query_cached("m", ["grant budget"], organization_id=None)
    second = await search._embed_query_cached("m", ["grant budget"], organization_id="o")
    await search._embed_query_cached("m", ["other"], organization_id=None)
    assert first == second == [[0.1, 0.2]]
    assert calls == [("m", ("grant budget",), "query"), ("m", ("other",), "query")]


async def test_the_kernel_set_is_asked_fresh_for_every_search(monkeypatch):
    """No cross-request cache: a grant or revocation reaches search immediately."""
    import matrx_orm

    asks: list = []

    async def fake_ids(user_id, token, level):
        asks.append(user_id)
        return ["d1"] if len(asks) == 1 else ["d1", "d2"]

    monkeypatch.setattr(matrx_orm, "platform_accessible_ids", fake_ids)
    first = await search.resolve_readable_documents("u1")
    second = await search.resolve_readable_documents("u1")
    assert asks == ["u1", "u1"]
    assert first.processed_document_ids == ("d1",)
    assert second.processed_document_ids == ("d1", "d2")
    assert not hasattr(search, "_readable_cache")


async def test_each_recall_lane_is_one_door_call_with_the_readable_set_and_filters(monkeypatch):
    calls: list = []

    async def fake_door(function, *args):
        calls.append((function, args))
        if function == "recall_entities":
            return [{"entity_id": "e1", "name": "Acme", "kind": "org", "cluster_id": None, "organization_id": "o1"}]
        return [{"chunk_id": "k1"}]

    monkeypatch.setattr(search, "_door", fake_door)
    readable = search.ReadableDocuments(user_id=_USER, processed_document_ids=("d1", "d2"))
    filters = {"leaf_only": True, "source_ids": ["f1"], "admin_bypass_acl": True}
    assert await search._recall_vector_door(
        "rag.embeddings_voyage_4_large_1024", [0.5, 0.25], user_id=_USER, readable=readable, k=100, filters=filters
    ) == ["k1"]
    assert await search._recall_lexical_door("acme", user_id=_USER, readable=readable, k=100, filters=filters) == ["k1"]
    ranking, ids, names = await search._recall_entity_door("acme corp", user_id=_USER, readable=readable, filters=filters)
    assert (ranking, ids, names) == (["k1"], ["e1"], ["Acme"])
    by = {f: a for f, a in calls}
    assert [f for f, _ in calls] == ["recall_vector", "recall_lexical", "recall_entities", "recall_entity_chunks"]
    table, vector, user, ready, k, fil, ef = by["recall_vector"]
    assert table == "embeddings_voyage_4_large_1024" and vector == "[0.5,0.25]" and user == _USER
    assert ready.values == ["d1", "d2"] and k == 100 and fil is filters and ef == 40
    assert by["recall_lexical"][2].values == ["d1", "d2"] and by["recall_lexical"][4] is filters
    # The entity lane never runs with the admin bypass (unchanged from the ORM lane).
    assert "admin_bypass_acl" not in by["recall_entity_chunks"][5]
    assert by["recall_entity_chunks"][2].values == ["e1"]


def test_rerank_bound_and_small_window_are_wired_into_the_cross_encoder_call():
    """The rerank call is bounded by rerank_timeout_s (status 'timeout', fused order kept)
    and uses the smaller window when the fused set is large."""
    import inspect

    from matrx_utils.source_guard import stable_source

    params = inspect.signature(search.search).parameters
    assert "rerank_timeout_s" in params and "rerank_input_large" in params
    src = stable_source(search.search)
    assert "_asyncio.wait_for(" in src and 'rerank_status = "timeout"' in src
    assert "fused[:rerank_window]" in src and "len(fused) > RERANK_INPUT * 2" in src
    # A miss is RECORDED as a provider incident, never a silent permanent fallback.
    assert 'kind="rag_rerank_timeout"' in src and 'kind="rag_rerank_provider_failed"' in src
    assert "rerank_input" in params and "rerank_error=rerank_error" in src
