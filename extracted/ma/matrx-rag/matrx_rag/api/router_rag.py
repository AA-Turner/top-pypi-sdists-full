"""matrx-rag HTTP router — search, ingest, health.

This is the package's own HTTP surface (Phase 2d), intended primarily
for matrx-local to mount. Aidream keeps its existing ~3,100-LOC
``aidream/api/routers/rag.py`` and is not required to mount these.

The endpoint shapes mirror aidream's existing wire format so a future
optional aidream consolidation can simply delegate.
"""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from matrx_connect import AppContext, context_dep
from pydantic import BaseModel, ConfigDict, Field

from matrx_rag._ext import get_db_model
from matrx_rag.ingestion import IngestionResult, ingest_source
from matrx_rag.search import DEFAULT_LIMIT, MAX_LIMIT, SearchHit, search

router = APIRouter()


# ---------------------------------------------------------------------------
# /rag/search
# ---------------------------------------------------------------------------


class SearchRequestFilters(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source_kinds: list[str] | None = Field(default=None)
    organization_id: str | None = Field(
        default=None,
        description=(
            "Override the active org for this query. Only honored for "
            "admins; non-admin callers always retrieve in their "
            "AppContext.organization_id scope."
        ),
    )


class SearchSourceRef(BaseModel):
    model_config = ConfigDict(extra="ignore")
    source_kind: str
    source_id: str


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    query: str = Field(min_length=1)
    filters: SearchRequestFilters | None = None
    limit: int = Field(default=DEFAULT_LIMIT, ge=1, le=MAX_LIMIT)
    rerank: bool = Field(default=True)
    only_children: bool = Field(default=True)
    include_sources: list[SearchSourceRef] | None = Field(
        default=None,
        description=(
            "Hard-pin the search to a list of (source_kind, source_id) "
            "pairs. Combines with filters.source_kinds via AND."
        ),
    )
    processed_document_ids: list[str] | None = Field(
        default=None,
        description=(
            "Hard-scope retrieval to exact base/derivative processed-document "
            "UUIDs. An explicit empty/invalid list returns no hits."
        ),
    )
    data_store_id: str | None = Field(
        default=None,
        description=(
            "Scope the search to one curated bucket (rag.data_stores.id). "
            "Aidream's router resolves this via materialize_member_filter. "
            "The matrx-rag package router does NOT yet support data stores "
            "(coming in a Phase 2d follow-on); for now, a non-null value "
            "returns 501. Accepting the field keeps cloud-shaped requests "
            "from silently widening scope due to ``extra='ignore'``."
        ),
    )
    embedding_models: list[str] | None = Field(
        default=None,
        description=(
            "Optional override; pass multiple to fan out across embedding "
            "tables and let RRF unify the rankings."
        ),
    )
    multi_query: int = Field(default=1, ge=1, le=5)
    use_hyde: bool = Field(default=False)
    use_mmr: bool = Field(default=True)


class SearchHitOut(BaseModel):
    model_config = ConfigDict(extra="ignore")

    chunk_id: str
    source_kind: str
    source_id: str
    field_id: str | None
    parent_chunk_id: str | None
    chunk_kind: str
    snippet: str
    score: float
    vector_rank: int | None
    lexical_rank: int | None
    rerank_score: float | None
    metadata: dict[str, Any]
    processed_document_id: str | None = None
    primary_page_id: str | None = None
    page_numbers: list[int] = Field(default_factory=list)
    # MediaRef for citation rendering — populated only when the hit's
    # source is a cld_file (the FE can pass this straight to
    # ``<InlineMediaRef>`` or ``upload()`` for re-resolution). For
    # non-file sources (notes, prompts, code_files, …) this stays None.
    # Wire-shape parity with aidream's router so the FE doesn't have to
    # branch on which host served the request.
    source_ref: dict[str, Any] | None = None


class SearchResponseOut(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    hits: list[SearchHitOut]
    total_candidates: int
    embedding_model: str
    reranker_model: str | None
    latency_ms: int


def _hit_to_out(h: SearchHit) -> SearchHitOut:
    source_ref = {"file_id": h.source_id} if h.source_kind == "cld_file" else None
    return SearchHitOut(
        chunk_id=h.chunk_id,
        source_kind=h.source_kind,
        source_id=h.source_id,
        field_id=h.field_id,
        parent_chunk_id=h.parent_chunk_id,
        chunk_kind=h.chunk_kind,
        snippet=h.content_text,
        score=h.score,
        vector_rank=h.vector_rank,
        lexical_rank=h.lexical_rank,
        rerank_score=h.rerank_score,
        metadata=h.metadata,
        processed_document_id=getattr(h, "processed_document_id", None),
        primary_page_id=getattr(h, "primary_page_id", None),
        page_numbers=getattr(h, "page_numbers", None) or [],
        source_ref=source_ref,
    )


@router.post("/search", response_model=SearchResponseOut)
async def rag_search_endpoint(
    body: SearchRequest,
    ctx: AppContext = Depends(context_dep),
) -> SearchResponseOut:
    """Hybrid retrieval — vector + lexical recall, RRF fusion, optional
    MMR diversification, optional Cohere rerank."""
    if not ctx.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="rag.search requires an authenticated user",
        )
    if body.data_store_id is not None:
        # Cloud-shaped requests may carry data_store_id; the package
        # router doesn't resolve it yet. Reject explicitly instead of
        # silently widening scope.
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=(
                "data_store_id scoping is not implemented in the "
                "matrx-rag package router yet (coming in a Phase 2d "
                "follow-on). Aidream's router supports it."
            ),
        )

    # The organization is the one the boundary verified. Being an admin never
    # switches tenant on a user search (THE ADMIN LANE, 2026-09-25).
    organization_id = ctx.organization_id

    source_kinds = body.filters.source_kinds if body.filters else None

    include_sources: list[dict[str, str]] | None = (
        [{"source_kind": s.source_kind, "source_id": s.source_id} for s in body.include_sources]
        if body.include_sources
        else None
    )

    response = await search(
        body.query,
        user_id=ctx.user_id,
        organization_id=organization_id,
        source_kinds=source_kinds,
        include_sources=include_sources,
        processed_document_ids=body.processed_document_ids,
        limit=body.limit,
        rerank=body.rerank,
        only_children=body.only_children,
        embedding_models=body.embedding_models,
        multi_query=body.multi_query,
        use_hyde=body.use_hyde,
        use_mmr=body.use_mmr,
    )
    return SearchResponseOut(
        query=response.query,
        hits=[_hit_to_out(h) for h in response.hits],
        total_candidates=response.total_candidates,
        embedding_model=response.embedding_model,
        reranker_model=response.reranker_model,
        latency_ms=response.latency_ms,
    )


# ---------------------------------------------------------------------------
# /rag/ingest
# ---------------------------------------------------------------------------


class IngestRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source_kind: Literal["note", "code_file", "cld_file"]
    source_id: str
    field_id: str | None = None
    force: bool = Field(
        default=False,
        description=(
            "When true, bypass the source-hash short-circuit and re-extract "
            "even if the content hash matches the prior run."
        ),
    )


class IngestResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_kind: str
    source_id: str
    field_id: str | None
    chunks_written: int
    embeddings_written: int
    skipped_unchanged: bool
    embedding_model: str
    error: str | None = None


@router.post("/ingest", response_model=IngestResponse)
async def rag_ingest_endpoint(
    body: IngestRequest,
    ctx: AppContext = Depends(context_dep),
) -> IngestResponse:
    """Synchronous one-shot ingest of a single source. For bulk or
    long-running operations, prefer the streaming variants (not yet
    exposed in the package router — coming in a Phase 2d follow-on)."""
    if not ctx.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="rag.ingest requires an authenticated user",
        )

    result: IngestionResult = await ingest_source(
        body.source_kind,
        body.source_id,
        body.field_id,
        force=body.force,
    )
    return IngestResponse(
        source_kind=result.source_kind,
        source_id=result.source_id,
        field_id=result.field_id,
        chunks_written=result.chunks_written,
        embeddings_written=result.embeddings_written,
        skipped_unchanged=result.skipped_unchanged,
        embedding_model=result.embedding_model,
        error=result.error,
    )


# ---------------------------------------------------------------------------
# /rag/health
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_ok: bool
    chunks_in_scope: int
    embeddings_in_scope: int
    distinct_sources: int


@router.get("/health", response_model=HealthResponse)
async def rag_health_endpoint(
    ctx: AppContext = Depends(context_dep),
) -> HealthResponse:
    """Schema sanity + scope-scoped counts. Cheap probe used by clients
    to detect missing-index conditions or empty scopes."""
    if not ctx.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="rag.health requires an authenticated user",
        )

    from matrx_orm import Count, schema_exists

    # information_schema.schemata existence probe — the matrx-orm
    # introspection primitive (no ORM Model surface for "does schema X
    # exist"; same class of catalog question as introspect_rls_policies).
    schema_ok = await schema_exists(get_db_model("KgChunks")._database, "rag")
    if not schema_ok:
        return HealthResponse(
            schema_ok=False,
            chunks_in_scope=0,
            embeddings_in_scope=0,
            distinct_sources=0,
        )
    # The probe counts the caller's own chunks across ALL their organizations —
    # the selected organization never narrows a read (access-belongs-to-the-person).
    chunks_in_scope = int(await get_db_model("KgChunks").count(created_by=ctx.user_id))
    # COUNT(DISTINCT (source_kind, source_id)) — the tuple-distinct count.
    # Count(*fields, distinct=True) now accepts multiple fields and renders
    # exactly this composite-DISTINCT shape (matrx-orm BASE_CLASS_METHODS.md
    # "Count — composite (multi-column) DISTINCT").
    agg = await (
        get_db_model("KgChunks")
        .filter(created_by=ctx.user_id)
        .aggregate(distinct_sources=Count("source_kind", "source_id", distinct=True))
    )
    distinct_sources = int(agg.get("distinct_sources") or 0)
    return HealthResponse(
        schema_ok=True,
        chunks_in_scope=chunks_in_scope,
        embeddings_in_scope=chunks_in_scope,  # 1:1 in kg_chunks today
        distinct_sources=distinct_sources,
    )
