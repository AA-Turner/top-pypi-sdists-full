"""Soft-delete symmetry primitives — logic regression net.

Verifies the EXACT column + predicate each lifecycle primitive uses, without a
live DB: ``get_db_model`` is patched to a recording fake so we assert what SQL
the primitive would shape. The end-to-end DB behavior (search exclusion, view
filtering, restore, purge) is proven separately against the live schema; this
locks the package-side logic so a future edit can't silently confuse the trash
marker (deleted_at) with supersession (valid_to) or drop the idempotency
predicate. Wave A (2026-07-17): trash IS deleted_at — valid_to means
supersession only and must NEVER be written or cleared by trash/restore.

Contract: /Users/armanisadeghi/code/common-docs/projects/knowledge-system/README.md.
"""

from __future__ import annotations

import asyncio

import matrx_rag.ingestion as ingestion


class _UpdateResult:
    def __init__(self, n: int) -> None:
        self.rows_affected = n


class _RecordingModel:
    calls: list[tuple] = []

    @classmethod
    async def update_where(cls, filters: dict, **updates):
        cls.calls.append(("update", cls.__name__, filters, updates))
        return _UpdateResult(1)

    @classmethod
    async def delete_where(cls, **filters):
        cls.calls.append(("delete", cls.__name__, filters))
        return 1


class _KgChunks(_RecordingModel):
    pass


class _DataStoreMembers(_RecordingModel):
    pass


def _patch(monkeypatch):
    _RecordingModel.calls = []

    def _fake_get_db_model(name: str):
        return {"KgChunks": _KgChunks, "DataStoreMembers": _DataStoreMembers}[name]

    monkeypatch.setattr(ingestion, "get_db_model", _fake_get_db_model)


def test_exports_present():
    for name in (
        "soft_delete_source_artifacts",
        "restore_source_artifacts",
        "purge_source_artifacts",
    ):
        assert name in ingestion.__all__
        assert callable(getattr(ingestion, name))


def test_soft_delete_sets_deleted_at_never_valid_to(monkeypatch):
    _patch(monkeypatch)
    out = asyncio.run(ingestion.soft_delete_source_artifacts("cld_file", "f1"))
    assert out == {"chunks": 1, "data_store_members": 1}

    chunk_call = next(c for c in _RecordingModel.calls if c[1] == "_KgChunks")
    _, _, filters, updates = chunk_call
    # Chunks are trashed via the dedicated deleted_at marker, only touching
    # still-live rows. valid_to (supersession) must never appear here.
    assert filters == {"source_kind": "cld_file", "source_id": "f1", "deleted_at__isnull": True}
    assert set(updates) == {"deleted_at"} and updates["deleted_at"] is not None

    member_call = next(c for c in _RecordingModel.calls if c[1] == "_DataStoreMembers")
    _, _, mfilters, mupdates = member_call
    assert mfilters == {"source_kind": "cld_file", "source_id": "f1", "deleted_at__isnull": True}
    assert set(mupdates) == {"deleted_at"} and mupdates["deleted_at"] is not None


def test_restore_clears_only_deleted_at(monkeypatch):
    _patch(monkeypatch)
    out = asyncio.run(ingestion.restore_source_artifacts("cld_file", "f1"))
    assert out == {"chunks": 1, "data_store_members": 1}

    chunk_call = next(c for c in _RecordingModel.calls if c[1] == "_KgChunks")
    _, _, filters, updates = chunk_call
    # Restore only touches trashed rows and clears ONLY deleted_at — clearing
    # valid_to would resurrect superseded chunks.
    assert filters == {"source_kind": "cld_file", "source_id": "f1", "deleted_at__isnull": False}
    assert updates == {"deleted_at": None}

    member_call = next(c for c in _RecordingModel.calls if c[1] == "_DataStoreMembers")
    _, _, mfilters, mupdates = member_call
    assert mfilters == {"source_kind": "cld_file", "source_id": "f1", "deleted_at__isnull": False}
    assert mupdates == {"deleted_at": None}


def test_document_scoped_primitives(monkeypatch):
    _patch(monkeypatch)
    out = asyncio.run(ingestion.soft_delete_document_artifacts("pd1"))
    assert out == {"chunks": 1, "data_store_members": 1}

    chunk_call = next(c for c in _RecordingModel.calls if c[1] == "_KgChunks")
    _, _, filters, updates = chunk_call
    assert filters == {"processed_document_id": "pd1", "deleted_at__isnull": True}
    assert set(updates) == {"deleted_at"} and updates["deleted_at"] is not None

    # Doc-scoped delete only touches doc-keyed memberships — never file-keyed.
    member_call = next(c for c in _RecordingModel.calls if c[1] == "_DataStoreMembers")
    _, _, mfilters, _ = member_call
    assert mfilters == {
        "source_kind": "processed_document",
        "source_id": "pd1",
        "deleted_at__isnull": True,
    }

    _RecordingModel.calls = []
    out = asyncio.run(ingestion.restore_document_artifacts("pd1"))
    assert out == {"chunks": 1, "data_store_members": 1}
    chunk_call = next(c for c in _RecordingModel.calls if c[1] == "_KgChunks")
    _, _, filters, updates = chunk_call
    assert filters == {"processed_document_id": "pd1", "deleted_at__isnull": False}
    assert updates == {"deleted_at": None}

    _RecordingModel.calls = []
    out = asyncio.run(ingestion.purge_document_artifacts("pd1"))
    assert out == {"chunks": 1, "data_store_members": 1}
    kinds = {(c[0], c[1]) for c in _RecordingModel.calls}
    assert ("delete", "_KgChunks") in kinds and ("delete", "_DataStoreMembers") in kinds


def test_purge_hard_deletes_chunks_and_members(monkeypatch):
    _patch(monkeypatch)
    out = asyncio.run(ingestion.purge_source_artifacts("cld_file", "f1"))
    assert out == {"chunks": 1, "data_store_members": 1}

    deletes = [c for c in _RecordingModel.calls if c[0] == "delete"]
    assert len(deletes) == 2
    for _, _model, filters in deletes:
        # Purge is field-agnostic: ALL chunks/members for the source.
        assert filters == {"source_kind": "cld_file", "source_id": "f1"}
