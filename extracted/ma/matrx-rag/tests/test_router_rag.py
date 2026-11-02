"""Phase 2d — matrx_rag.api.router_rag tests.

Covers the three endpoints in the package's HTTP router (search,
ingest, health) using a FastAPI TestClient. The underlying matrx_rag
service functions are stubbed via dependency_overrides + module-level
monkeypatching so the router can be tested without a live database.

Auth shape: every endpoint uses ``Depends(context_dep)`` from
matrx-connect. The tests override ``context_dep`` with a stub that
returns a synthetic AppContext-shaped object carrying user_id +
organization_id. A request that hits the unauth path is exercised by
overriding the dep to return a ctx with user_id=None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import matrx_rag.api as rag_api
from fastapi import FastAPI
from fastapi.testclient import TestClient
from matrx_connect import context_dep, iter_api_routes, mounted_api_paths

# ---------------------------------------------------------------------------
# Stubs
# ---------------------------------------------------------------------------


@dataclass
class _StubCtx:
    """Minimal AppContext duck-type for the router's use of
    ctx.user_id / ctx.organization_id / ctx.is_admin."""

    user_id: str | None
    organization_id: str | None = None
    is_admin: bool = False


def _make_app(ctx: _StubCtx) -> FastAPI:
    app = FastAPI()
    rag_api.include_routers(app, prefix="/rag")
    app.dependency_overrides[context_dep] = lambda: ctx
    return app


def test_knowledge_alias_mounts_the_same_contract() -> None:
    app = FastAPI()
    rag_api.include_knowledge_routers(app)
    paths = mounted_api_paths(app)
    assert "/knowledge/search" in paths
    assert "/knowledge/ingest" in paths
    assert "/knowledge/health" in paths


@dataclass
class _StubHit:
    chunk_id: str
    source_kind: str
    source_id: str
    field_id: str | None
    parent_chunk_id: str | None
    chunk_kind: str
    content_text: str
    score: float
    vector_rank: int | None
    lexical_rank: int | None
    rerank_score: float | None
    metadata: dict[str, Any]
    processed_document_id: str | None = None
    primary_page_id: str | None = None
    page_numbers: list[int] | None = None


@dataclass
class _StubResponse:
    query: str
    hits: list
    total_candidates: int
    embedding_model: str
    reranker_model: str | None
    latency_ms: int


@dataclass
class _StubIngestResult:
    source_kind: str
    source_id: str
    field_id: str | None
    chunks_written: int
    embeddings_written: int
    skipped_unchanged: bool
    embedding_model: str
    error: str | None = None


# ---------------------------------------------------------------------------
# /rag/search
# ---------------------------------------------------------------------------


def test_search_unauthenticated_returns_401(monkeypatch):
    """No user_id on the context → 401."""
    app = _make_app(_StubCtx(user_id=None))
    client = TestClient(app)
    resp = client.post("/rag/search", json={"query": "hello"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "rag.search requires an authenticated user"


def test_search_happy_path_returns_hits(monkeypatch):
    """A valid query with a stubbed search() returns the hits projected
    into the SearchHitOut shape."""
    recorded = {}

    async def fake_search(query, **kwargs):
        recorded["query"] = query
        recorded["kwargs"] = kwargs
        return _StubResponse(
            query=query,
            hits=[
                _StubHit(
                    chunk_id="chunk-1",
                    source_kind="note",
                    source_id="src-1",
                    field_id=None,
                    parent_chunk_id="parent-1",
                    chunk_kind="text",
                    content_text="hello from the chunk",
                    score=0.95,
                    vector_rank=1,
                    lexical_rank=2,
                    rerank_score=0.88,
                    metadata={"role": "child"},
                )
            ],
            total_candidates=1,
            embedding_model="openai:text-embedding-3-small",
            reranker_model="rerank-v3.5",
            latency_ms=42,
        )

    # Patch the symbol the router imported.
    import matrx_rag.api.router_rag as router_mod

    monkeypatch.setattr(router_mod, "search", fake_search)

    app = _make_app(_StubCtx(user_id="user-1", organization_id="org-1"))
    client = TestClient(app)
    resp = client.post("/rag/search", json={"query": "hello world"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["query"] == "hello world"
    assert body["embedding_model"] == "openai:text-embedding-3-small"
    assert body["latency_ms"] == 42
    assert len(body["hits"]) == 1
    hit = body["hits"][0]
    assert hit["chunk_id"] == "chunk-1"
    assert hit["snippet"] == "hello from the chunk"
    assert hit["score"] == 0.95
    assert hit["rerank_score"] == 0.88

    # Wire-through: user_id and organization_id passed into search().
    assert recorded["kwargs"]["user_id"] == "user-1"
    assert recorded["kwargs"]["organization_id"] == "org-1"


def test_search_organization_override_is_refused_for_everyone_including_admins(monkeypatch):
    """THE ADMIN LANE (Arman, 2026-09-25): "Admin privileges cannot ever extend
    beyond the admin sections of the system... The difference can only work in
    the admin apps." ``/rag/search`` is a normal user route (mounted for every
    signed-in person, not an admin app), so an admin caller here is an ordinary
    person: ``filters.organization_id`` is ignored exactly the same way for an
    admin as for a non-admin, and search always runs at ``ctx.organization_id``.

    This replaces the old ``test_search_admin_can_override_organization_id``,
    which asserted the opposite (admin override honored) — that power was
    deliberately removed (common-docs/policies/our-own-admin-database-access.md
    "The admin lane"). The admin-only escape hatch for this package's search
    surface — an ACL bypass, not an organization_id override — lives in
    aidream's own admin-app-only door
    (``aidream/api/routers/admin_user_surfaces.py``'s
    ``/admin/rag/search-lab/inventory`` + ``/admin/rag/search-lab/diagnose``,
    gated on ``matrx_connect.admin_surface_active()``), which is outside this
    package and covered by aidream's own tests — this package's router has no
    admin-route equivalent to exercise."""
    captured = []

    async def fake_search(query, **kwargs):
        captured.append(kwargs["organization_id"])
        return _StubResponse(
            query=query,
            hits=[],
            total_candidates=0,
            embedding_model="m",
            reranker_model=None,
            latency_ms=0,
        )

    import matrx_rag.api.router_rag as router_mod

    monkeypatch.setattr(router_mod, "search", fake_search)

    # Non-admin: override is ignored.
    app = _make_app(_StubCtx(user_id="u", organization_id="ctx-org", is_admin=False))
    client = TestClient(app)
    client.post(
        "/rag/search",
        json={"query": "q", "filters": {"organization_id": "spoofed-org"}},
    )
    assert captured[-1] == "ctx-org"

    # Admin: override is ALSO ignored — an admin is an ordinary person on a
    # user route. Same request, same result as the non-admin case above.
    app2 = _make_app(_StubCtx(user_id="u", organization_id="ctx-org", is_admin=True))
    client2 = TestClient(app2)
    client2.post(
        "/rag/search",
        json={"query": "q", "filters": {"organization_id": "spoofed-org"}},
    )
    assert captured[-1] == "ctx-org"


def test_search_include_sources_passed_through(monkeypatch):
    """include_sources in the request body becomes a list of dicts in the
    underlying search() call."""
    captured = {}

    async def fake_search(query, **kwargs):
        captured.update(kwargs)
        return _StubResponse(
            query=query,
            hits=[],
            total_candidates=0,
            embedding_model="m",
            reranker_model=None,
            latency_ms=0,
        )

    import matrx_rag.api.router_rag as router_mod

    monkeypatch.setattr(router_mod, "search", fake_search)

    app = _make_app(_StubCtx(user_id="u"))
    client = TestClient(app)
    client.post(
        "/rag/search",
        json={
            "query": "q",
            "include_sources": [
                {"source_kind": "note", "source_id": "n1"},
                {"source_kind": "cld_file", "source_id": "f2"},
            ],
        },
    )
    assert captured["include_sources"] == [
        {"source_kind": "note", "source_id": "n1"},
        {"source_kind": "cld_file", "source_id": "f2"},
    ]


def test_search_validates_query_required():
    """Empty query string fails Pydantic validation → 422."""
    app = _make_app(_StubCtx(user_id="u"))
    client = TestClient(app)
    resp = client.post("/rag/search", json={"query": ""})
    assert resp.status_code == 422


def test_search_data_store_id_returns_501():
    """data_store_id is accepted in the schema (cloud-shape parity) but
    the package router does not yet resolve it — returns 501 explicitly
    rather than silently widening scope."""
    app = _make_app(_StubCtx(user_id="u"))
    client = TestClient(app)
    resp = client.post(
        "/rag/search",
        json={"query": "q", "data_store_id": "store-1"},
    )
    assert resp.status_code == 501
    assert "data_store_id" in resp.json()["detail"]


def test_search_hit_source_ref_for_cld_file(monkeypatch):
    """cld_file hits get a MediaRef in source_ref so the FE can render
    citations without branching on which host served the request.
    Non-cld_file hits get source_ref=None."""

    async def fake_search(query, **kwargs):
        return _StubResponse(
            query=query,
            hits=[
                _StubHit(
                    chunk_id="c1",
                    source_kind="cld_file",
                    source_id="file-abc",
                    field_id=None,
                    parent_chunk_id=None,
                    chunk_kind="text",
                    content_text="from a file",
                    score=0.9,
                    vector_rank=1,
                    lexical_rank=None,
                    rerank_score=None,
                    metadata={},
                    processed_document_id="doc-1",
                    primary_page_id="page-78",
                    page_numbers=[78, 79, 80],
                ),
                _StubHit(
                    chunk_id="c2",
                    source_kind="note",
                    source_id="note-xyz",
                    field_id=None,
                    parent_chunk_id=None,
                    chunk_kind="text",
                    content_text="from a note",
                    score=0.8,
                    vector_rank=2,
                    lexical_rank=None,
                    rerank_score=None,
                    metadata={},
                ),
            ],
            total_candidates=2,
            embedding_model="m",
            reranker_model=None,
            latency_ms=1,
        )

    import matrx_rag.api.router_rag as router_mod

    monkeypatch.setattr(router_mod, "search", fake_search)

    app = _make_app(_StubCtx(user_id="u"))
    client = TestClient(app)
    resp = client.post("/rag/search", json={"query": "q"})
    body = resp.json()
    cld_hit, note_hit = body["hits"]
    assert cld_hit["source_ref"] == {"file_id": "file-abc"}
    assert cld_hit["processed_document_id"] == "doc-1"
    assert cld_hit["primary_page_id"] == "page-78"
    assert cld_hit["page_numbers"] == [78, 79, 80]
    assert note_hit["source_ref"] is None
    assert note_hit["page_numbers"] == []


# ---------------------------------------------------------------------------
# /rag/ingest
# ---------------------------------------------------------------------------


def test_ingest_unauthenticated_returns_401():
    app = _make_app(_StubCtx(user_id=None))
    client = TestClient(app)
    resp = client.post(
        "/rag/ingest",
        json={"source_kind": "note", "source_id": "abc"},
    )
    assert resp.status_code == 401


def test_ingest_happy_path(monkeypatch):
    """A valid ingest request delegates to ingest_source() and returns
    the IngestionResult projected into IngestResponse."""
    captured = {}

    async def fake_ingest(source_kind, source_id, field_id, *, force=False, emitter=None):
        captured["source_kind"] = source_kind
        captured["source_id"] = source_id
        captured["field_id"] = field_id
        captured["force"] = force
        return _StubIngestResult(
            source_kind=source_kind,
            source_id=source_id,
            field_id=field_id,
            chunks_written=12,
            embeddings_written=12,
            skipped_unchanged=False,
            embedding_model="openai:text-embedding-3-small",
            error=None,
        )

    import matrx_rag.api.router_rag as router_mod

    monkeypatch.setattr(router_mod, "ingest_source", fake_ingest)

    app = _make_app(_StubCtx(user_id="u"))
    client = TestClient(app)
    resp = client.post(
        "/rag/ingest",
        json={
            "source_kind": "note",
            "source_id": "note-1",
            "force": True,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["source_kind"] == "note"
    assert body["source_id"] == "note-1"
    assert body["chunks_written"] == 12
    assert body["error"] is None

    assert captured["source_kind"] == "note"
    assert captured["source_id"] == "note-1"
    assert captured["force"] is True


def test_ingest_rejects_unknown_source_kind():
    """The IngestRequest Literal type rejects out-of-set values → 422."""
    app = _make_app(_StubCtx(user_id="u"))
    client = TestClient(app)
    resp = client.post(
        "/rag/ingest",
        json={"source_kind": "nonsense", "source_id": "x"},
    )
    assert resp.status_code == 422


def test_ingest_returns_error_field_when_source_resolution_fails(monkeypatch):
    """A source-resolution failure returns 200 with the error string in
    the response body (matches aidream's existing contract)."""

    async def fake_ingest(source_kind, source_id, field_id, *, force=False, emitter=None):
        return _StubIngestResult(
            source_kind=source_kind,
            source_id=source_id,
            field_id=field_id,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model="",
            error="source_not_found_or_unsupported_mime",
        )

    import matrx_rag.api.router_rag as router_mod

    monkeypatch.setattr(router_mod, "ingest_source", fake_ingest)

    app = _make_app(_StubCtx(user_id="u"))
    client = TestClient(app)
    resp = client.post(
        "/rag/ingest",
        json={"source_kind": "note", "source_id": "missing"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["chunks_written"] == 0
    assert body["error"] == "source_not_found_or_unsupported_mime"


# ---------------------------------------------------------------------------
# /rag/health
# ---------------------------------------------------------------------------


def test_health_unauthenticated_returns_401():
    app = _make_app(_StubCtx(user_id=None))
    client = TestClient(app)
    resp = client.get("/rag/health")
    assert resp.status_code == 401


def test_health_returns_counts(monkeypatch):
    """A working DB + schema returns the chunk/source counts in the
    caller's scope."""

    class _FakeQuery:
        def __init__(self, filters):
            self.filters = filters

        def filter(self, **filters):
            self.filters.update(filters)
            return self

        async def aggregate(self, **kwargs):
            assert self.filters.get("created_by") == "00000000-0000-0000-0000-000000000001"
            return {"distinct_sources": 7}

    class _FakeKgChunks:
        _database = "matrx_rag"

        @staticmethod
        async def count(**filters):
            assert filters.get("created_by") == "00000000-0000-0000-0000-000000000001"
            return 42

        @staticmethod
        def filter(**filters):
            return _FakeQuery(dict(filters))

    import matrx_rag.api.router_rag as router_mod

    monkeypatch.setattr(router_mod, "get_db_model", lambda name: _FakeKgChunks)

    async def fake_schema_exists(database, schema):
        assert database == "matrx_rag"
        assert schema == "rag"
        return True

    import matrx_orm

    monkeypatch.setattr(matrx_orm, "schema_exists", fake_schema_exists)

    app = _make_app(_StubCtx(user_id="00000000-0000-0000-0000-000000000001"))
    client = TestClient(app)
    resp = client.get("/rag/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["schema_ok"] is True
    assert body["chunks_in_scope"] == 42
    assert body["distinct_sources"] == 7


def test_health_returns_zero_when_schema_missing(monkeypatch):
    """A missing rag schema short-circuits to schema_ok=false with zero
    counts (rather than blowing up on a missing-table SQL error)."""

    class _FakeKgChunks:
        _database = "matrx_rag"

        @staticmethod
        async def count(**filters):
            raise RuntimeError("must not be called when schema_ok=false")

        @staticmethod
        def filter(**filters):
            raise RuntimeError("must not be called when schema_ok=false")

    import matrx_rag.api.router_rag as router_mod

    monkeypatch.setattr(router_mod, "get_db_model", lambda name: _FakeKgChunks)

    async def fake_schema_exists(database, schema):
        return False

    import matrx_orm

    monkeypatch.setattr(matrx_orm, "schema_exists", fake_schema_exists)

    app = _make_app(_StubCtx(user_id="00000000-0000-0000-0000-000000000001"))
    client = TestClient(app)
    resp = client.get("/rag/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["schema_ok"] is False
    assert body["chunks_in_scope"] == 0
    assert body["distinct_sources"] == 0


# ---------------------------------------------------------------------------
# include_routers helper
# ---------------------------------------------------------------------------


def test_include_routers_default_prefix():
    """The package's include_routers helper mounts the router at /rag
    by default."""
    app = FastAPI()
    rag_api.include_routers(app)

    paths = mounted_api_paths(app)
    assert "/rag/search" in paths
    assert "/rag/ingest" in paths
    assert "/rag/health" in paths


def test_include_routers_custom_prefix():
    """The prefix is overridable so two RAG instances can be mounted at
    different paths if a host wants."""
    app = FastAPI()
    rag_api.include_routers(app, prefix="/local-rag")
    paths = mounted_api_paths(app)
    assert "/local-rag/search" in paths
    assert "/rag/search" not in paths


# ---------------------------------------------------------------------------
# The guard: the RAG router is actually ON the app and actually REACHABLE
# ---------------------------------------------------------------------------

#: Every method+path the package's HTTP surface promises, at the default mount.
RAG_CONTRACT: frozenset[tuple[str, str]] = frozenset(
    {
        ("POST", "/rag/search"),
        ("POST", "/rag/ingest"),
        ("GET", "/rag/health"),
    }
)


def test_rag_router_is_present_on_the_app_and_reachable() -> None:
    """Fails when the RAG router is absent from the app.

    Two legs, because each catches a failure the other cannot:

    1. STRUCTURE — every promised method+path is mounted, walked with the one
       walker that recurses into included routers. An assertion built on
       ``app.routes`` alone cannot see them at all on FastAPI >= 0.139, which
       is how three tests here came to claim ZERO RAG routes were registered
       while the routes were mounted and serving fine.
    2. REACHABILITY — a mounted path that does not actually route is worse than
       an absent one, so each promised path is called and must NOT 404. Any
       other status (401/422/500) still proves the route is wired.
    """
    app = FastAPI()
    rag_api.include_routers(app)

    mounted = {(method, m.path) for m in iter_api_routes(app) for method in m.methods}
    missing = RAG_CONTRACT - mounted
    assert not missing, f"RAG routes absent from the app: {sorted(missing)}"

    client = TestClient(app, raise_server_exceptions=False)
    for method, path in sorted(RAG_CONTRACT):
        response = client.request(method, path, json={})
        assert response.status_code != 404, f"{method} {path} is mounted but does not route (404)"
