"""Unit contract for derivative-aware processed-document search scoping."""

from __future__ import annotations

import inspect

from matrx_rag.search import (
    _normalize_processed_document_ids,
    _processed_document_id_predicate,
    recall_filters,
    search,
)

DOC_1 = "11111111-1111-4111-8111-111111111111"
DOC_2 = "22222222-2222-4222-8222-222222222222"


def test_processed_document_ids_are_validated_and_deduped():
    assert _normalize_processed_document_ids(None) is None
    assert _normalize_processed_document_ids([DOC_1, DOC_2, DOC_1]) == [DOC_1, DOC_2]
    assert _normalize_processed_document_ids(["", "not-a-uuid"]) == []


def test_processed_document_predicate_uses_bound_uuid_array():
    params: list[object] = []
    sql = _processed_document_id_predicate([DOC_1, DOC_2]).as_sql(
        params,
        current_table="c",
    )
    assert sql == "c.processed_document_id = ANY($1::uuid[])"
    assert params == [[DOC_1, DOC_2]]
    assert DOC_1 not in sql


def test_processed_document_filter_reaches_every_recall_lane():
    """Every lane is a recall door fed the ONE filters dict search() builds."""
    assert "processed_document_ids" in inspect.signature(search).parameters
    f = recall_filters(
        only_children=True, source_kinds=None, include_sources=None, library_filter="any",
        source_ids=None, processed_document_ids=[DOC_1], scope_ids=None, scope_document_ids=None,
        admin_bypass_acl=False,
    )
    assert f["processed_document_ids"] == [DOC_1]
