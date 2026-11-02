"""Unit tests for the file-scoped `source_ids` retrieval filter — NO DB.

Locks the D15 contract: `search(..., source_ids=[...])` hard-scopes retrieval
to specific source rows (e.g. the cld_file file_ids attached to a thread),
fail-closed and bound-param-only. Covers the pure helpers
(`_normalize_source_ids`, `_build_source_id_clause`) and the wiring invariant
that every recall lane (vector, lexical, entity) accepts the filter — the
entity lane omission was exactly the leak class the fusion comment warns
about (an entity-lane hit surfacing a chunk outside the requested files).
"""

from __future__ import annotations

import inspect

from matrx_rag.search import (
    _normalize_source_ids,
    _source_id_predicate,
    search,
    recall_filters,
)


class TestNormalizeSourceIds:
    def test_none_passthrough(self):
        assert _normalize_source_ids(None) is None

    def test_strips_and_dedupes_preserving_order(self):
        assert _normalize_source_ids([" a ", "b", "a", "b "]) == ["a", "b"]

    def test_blanks_dropped(self):
        assert _normalize_source_ids(["", "   ", "x"]) == ["x"]

    def test_all_blank_is_empty_list_fail_closed(self):
        # [] (not None) → the caller short-circuits to an EMPTY response,
        # never silently widening to an unscoped search.
        assert _normalize_source_ids(["", "  "]) == []
        assert _normalize_source_ids([]) == []

    def test_non_uuid_ids_are_kept(self):
        # source_id is a text column — non-UUID ids are legitimate.
        assert _normalize_source_ids(["repo:main/readme.md"]) == ["repo:main/readme.md"]


class TestSourceIdPredicate:
    def test_values_are_bound(self):
        params: list[object] = []
        sql = _source_id_predicate(["f1", "f2"]).as_sql(params, current_table="c")
        assert sql == "c.source_id = ANY($1::text[])"
        assert params == [["f1", "f2"]]

    def test_ids_never_interpolated(self):
        params: list[object] = []
        sql = _source_id_predicate(["'); DROP TABLE kg_chunks; --"]).as_sql(
            params, current_table="c"
        )
        assert "DROP TABLE" not in sql
        assert sql == "c.source_id = ANY($1::text[])"


class TestSourceIdsWiring:
    def test_search_accepts_source_ids(self):
        assert "source_ids" in inspect.signature(search).parameters

    def test_every_recall_lane_accepts_source_ids(self):
        # All THREE lanes are RRF-fused doors fed the ONE filters dict; a filter
        # missing there would leak chunks from outside the requested files.
        f = _filters(source_ids=["f1"])
        assert f["source_ids"] == ["f1"]


class TestExactSourcePairWiring:
    def test_every_recall_lane_accepts_exact_source_pairs(self):
        # `include_sources` is a closed-corpus boundary for every fused lane.
        f = _filters(include_sources=[{"source_kind": "note", "source_id": "n1"}])
        assert f["include_sources"] == [{"source_kind": "note", "source_id": "n1"}]

    def test_every_recall_lane_accepts_source_kind_filter(self):
        assert _filters(source_kinds=["note"])["source_kinds"] == ["note"]
        assert "source_kinds" not in _filters(source_kinds=[])


def _filters(**kw):
    base = dict(
        only_children=True,
        source_kinds=None,
        include_sources=None,
        library_filter="any",
        source_ids=None,
        processed_document_ids=None,
        scope_ids=None,
        scope_document_ids=None,
        admin_bypass_acl=False,
    )
    base.update(kw)
    return recall_filters(**base)
