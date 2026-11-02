"""NULL-org leak guard (2026-06-03 class, re-hardened 2026-06-24;
NO NULL ORG 2026-08-21).

A ``rag.kg_chunks`` / embedding row with a NULL ``organization_id`` is
invisible to its owner AND fails closed in the read-access predicate. The
guard lives in ``upsert_chunks`` (the universal chunk-write chokepoint) so
NO source can write a NULL org regardless of entry point.

``allow_global_org=True`` no longer means "keep the NULL" — owner ruling
2026-08-21 (db-rules §2/§6e): NULL is not a scope. Genuinely GLOBAL content
(library docs) is stamped with the SYSTEM ORG, which ``iam.system_orgs``
marks ``global_readable`` and which therefore really is readable by every
authenticated user. The old NULL lane was also measurably dead — the
``organization_id IS NULL`` branches in the kg_chunks / embeddings_* RLS
policies and in ``search.py``'s ACL matched 0 of the 314 live library_doc
chunks.

Uses the in-memory fakes from test_chunk_reuse. No live DB, no network.
"""

from __future__ import annotations

import hashlib
import uuid

import pytest

try:
    from test_chunk_reuse import (  # type: ignore[import-not-found]
        _make_chunk,
        fake_db_pool,
        stub_embedding_spec,
    )
except ImportError:  # pragma: no cover - import-path resilience
    from tests.test_chunk_reuse import (  # type: ignore[import-not-found]
        _make_chunk,
    )


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _resolved(*, organization_id, owner_id, source_id: str):
    from matrx_rag.sources import ResolvedSource

    return ResolvedSource(
        source_kind="note",
        source_id=source_id,
        field_id=None,
        organization_id=organization_id,
        owner_id=owner_id,
        text="x",
        mime_type="text/plain",
        language=None,
        source_hash="h",
        metadata={},
    )


@pytest.mark.asyncio
async def test_resolve_effective_org_pure_branches():
    from matrx_rag.ingestion import resolve_effective_org

    org = str(uuid.uuid4())
    # An org already present is returned verbatim — no DB lookup.
    assert await resolve_effective_org(org, str(uuid.uuid4())) == org
    # No org AND no owner → None (caller decides global-vs-error); no DB call.
    assert await resolve_effective_org(None, None) is None
    # An OWNER is not a tenancy. A record with no organization resolves to
    # None even when its owner is known — an organization picked for the owner is
    # never borrowed to fill it (2026-09-17,
    # common-docs/policies/context-is-carried-never-rebuilt.md rule 4).
    assert await resolve_effective_org(None, str(uuid.uuid4())) is None


@pytest.mark.asyncio
async def test_an_owned_source_with_no_organization_refuses_instead_of_using_the_personal_one(
    fake_db_pool, stub_embedding_spec
):
    """The case the personal-org default used to swallow.

    A source that names no organization but HAS an owner used to be written
    into that owner's personal organization — so chunks of a team document
    landed in one person's workspace, invisible to everyone who ingested it,
    with nothing raised. It now refuses and writes nothing.
    """
    from matrx_rag.ingestion import upsert_chunks

    owner = str(uuid.uuid4())
    chunks = [_make_chunk("owned but unscoped", 0)]
    resolved = _resolved(organization_id=None, owner_id=owner, source_id="n-owned-no-org")

    with pytest.raises(ValueError, match="never"):
        await upsert_chunks(
            resolved=resolved,
            chunks=chunks,
            embedding_model="openai:text-embedding-3-small",
            embeddings=[[0.0, 0.0, 0.0, 1.0]],
            new_shas=[_sha("owned but unscoped")],
            existing_by_sha={},
        )

    assert len(fake_db_pool.chunks) == 0


@pytest.mark.asyncio
async def test_upsert_chunks_raises_on_null_org_and_owner(fake_db_pool, stub_embedding_spec):
    """An owned source with no resolvable org must FAIL LOUD, never write NULL."""
    from matrx_rag.ingestion import upsert_chunks

    chunks = [_make_chunk("orphan", 0)]
    resolved = _resolved(organization_id=None, owner_id=None, source_id="n-null")

    with pytest.raises(ValueError, match="NULL"):
        await upsert_chunks(
            resolved=resolved,
            chunks=chunks,
            embedding_model="openai:text-embedding-3-small",
            embeddings=[[0.0, 0.0, 0.0, 1.0]],
            new_shas=[_sha("orphan")],
            existing_by_sha={},
        )

    assert len(fake_db_pool.chunks) == 0


@pytest.mark.asyncio
async def test_global_content_lands_on_the_system_org(fake_db_pool, stub_embedding_spec):
    """Library/global content opts in via allow_global_org=True and is stamped
    with the SYSTEM ORG — never a NULL (db-rules §2, NO NULL ORG)."""
    from matrx_rag.ingestion import SYSTEM_ORG_ID, upsert_chunks

    chunks = [_make_chunk("global doc", 0)]
    resolved = _resolved(organization_id=None, owner_id=str(uuid.uuid4()), source_id="n-global")

    await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[[0.0, 0.0, 0.0, 1.0]],
        new_shas=[_sha("global doc")],
        existing_by_sha={},
        allow_global_org=True,
    )

    rows = list(fake_db_pool.chunks.values())
    assert len(rows) == 1
    assert rows[0]["organization_id"] == SYSTEM_ORG_ID
    assert rows[0]["organization_id"] is not None


@pytest.mark.asyncio
async def test_global_opt_in_with_no_owner_still_never_writes_null(
    fake_db_pool, stub_embedding_spec
):
    """The ownerless case is exactly where the old code kept a NULL. The system
    org does not need an owner to resolve from, so there is no lane left that
    can produce a NULL organization_id."""
    from matrx_rag.ingestion import SYSTEM_ORG_ID, upsert_chunks

    chunks = [_make_chunk("ownerless global doc", 0)]
    resolved = _resolved(organization_id=None, owner_id=None, source_id="n-global-noowner")

    await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model="openai:text-embedding-3-small",
        embeddings=[[0.0, 0.0, 0.0, 1.0]],
        new_shas=[_sha("ownerless global doc")],
        existing_by_sha={},
        allow_global_org=True,
    )

    rows = list(fake_db_pool.chunks.values())
    assert len(rows) == 1
    assert rows[0]["organization_id"] == SYSTEM_ORG_ID


@pytest.mark.asyncio
async def test_retrieval_audit_refuses_null_org(monkeypatch):
    """Audit is best-effort, but it must never persist a row with guessed scope."""
    from matrx_rag import search as search_module

    writes: list[dict[str, object]] = []
    captured: list[tuple[BaseException, str, dict[str, object]]] = []

    class FakeRetrievalAudit:
        @classmethod
        async def create(cls, **values):
            writes.append(values)

    async def fake_capture_error(exc, *, kind, context):
        captured.append((exc, kind, context))

    monkeypatch.setattr(search_module, "get_db_model", lambda _name: FakeRetrievalAudit)
    monkeypatch.setattr(search_module, "capture_error", fake_capture_error)

    await search_module._write_audit(
        query="scope must be explicit",
        user_id=str(uuid.uuid4()),
        organization_id=None,
        returned_chunk_ids=[],
        rerank_scores=None,
        latency_ms=1,
        pipeline={},
    )

    assert writes == []
    assert len(captured) == 1
    assert captured[0][1] == "rag_retrieval_audit_missing_org"
    assert "initiating organization_id" in str(captured[0][0])
