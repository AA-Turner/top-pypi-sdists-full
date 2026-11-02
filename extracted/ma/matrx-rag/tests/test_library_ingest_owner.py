"""Shared-library ingestion must always write under a real system owner — and
under the organization the DOC ROW names, never one resolved for it.

THE REQUEST CONTEXT IS CARRIED, NEVER REBUILT (rule 3): ``ingest_library_doc``
re-enters from a durable record, so the chunks take THAT record's organization.
Until 2026-09-17 a row that answered with nothing fell through to the Matrx
Library system org, which is a tenant nobody chose; ``rag.library_docs``
.organization_id has been NOT NULL since migration 0167, so that row is broken
and the honest answer is a refusal that names it.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import matrx_rag.library as library

ROW_ORG = "5e44ec19-3965-4b12-91b2-b2bdb2712abc"


async def test_text_library_ingest_uses_the_doc_rows_organization(monkeypatch):
    captured: dict[str, object] = {}

    async def row_org(_doc_id: str) -> str:
        return ROW_ORG

    async def ingest_source(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return SimpleNamespace(error=None)

    monkeypatch.setattr(library, "_resolve_library_doc_org", row_org)
    monkeypatch.setattr(library, "ingest_source", ingest_source)

    await library.ingest_library_doc("doc-1")

    assert captured["kwargs"] == {
        "force": False,
        "emitter": None,
        "organization_id": ROW_ORG,
        "owner_id": library._system_owner_uuid(ROW_ORG),
        "run_ner": False,
    }


async def test_text_library_ingest_refuses_when_the_row_has_no_organization(monkeypatch):
    async def missing_row_org(_doc_id: str) -> None:
        return None

    async def ingest_source(*_args, **_kwargs):  # pragma: no cover — must not run
        raise AssertionError("nothing may be ingested for an organization-less row")

    monkeypatch.setattr(library, "_resolve_library_doc_org", missing_row_org)
    monkeypatch.setattr(library, "ingest_source", ingest_source)

    with pytest.raises(library.LibraryRehomeError, match="carries no"):
        await library.ingest_library_doc("doc-1")
