"""
Bridge: page_extraction_results -> rag.kg_chunks.

Takes the structured payloads that user-defined agents produce while
processing PDFs (page-by-page extraction jobs) and materializes them as
first-class RAG chunks with full provenance back to source pages.

The motivating case is the "WC Ellie" workflow: an agent reads pages of
a workers-comp document, extracts medical-event records (DOI, DATE,
SOURCE, DETAILS, BODY PART(S), …), and returns one structured JSON
record per source-page-range. Today those records sit in
``page_extraction_results.payload`` invisible to RAG search. This
module bridges them in.

Pipeline per run:

  1. Load run + job + parent processed_document.
  2. Resolve priority: ``job.rag_boost``  ->  ``agent.default_rag_boost``  ->  0.
  3. Create one derivative processed_document
     (``derivation_kind='agent_structured_json'``) chained to the parent
     initial_extract via ``parent_processed_id``. Idempotent via
     ``ensure_derivative(intent='get_or_create_derivative', …)`` keyed
     on (parent, kind, agent_id, agent_version, run_id-as-params).
  4. For each result row: build a chunk whose text is a flattened
     line-per-key projection of the JSON payload, attach metadata
     pointing back at the result_id, page_numbers, canonical_page.
  5. Embed all chunks in one batched call.
  6. INSERT into rag.kg_chunks with derivative-level FK provenance
     (processed_document_id = derivative, parent_chunk_id NULL,
     priority = inherited, derivation_kind = 'agent_structured_json',
     agent_id, extraction_run_id, extraction_result_id populated, plus
     page_numbers / page_spans / primary_page_id from the source pages).

Re-indexing the same run is idempotent: the orchestrator deletes any
prior chunks for the derivative's processed_document_id before writing
the new set. The derivative row itself is reused via
``ensure_derivative``'s ``get_or_create`` intent.

This module DOES NOT modify any existing extraction flow; it is a pure
read-then-derive pipeline. The auto-hook (in page_extraction.py) is
gated by the ``AUTO_INDEX_EXTRACTIONS`` constant below (a code-reviewed
toggle, not an env var) so it can be flipped without touching this code.
"""

from __future__ import annotations

import json
import logging
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

# Phase 2b — DocumentWriter injection seam replaces the previous
# eager aidream-side imports. ``NotFoundError``, ``DerivativeIntent``,
# ``compute_params_hash`` are now matrx_rag-owned types/helpers; the
# actual derivative write goes through ``get_document_writer()``.
# Aidream's bootstrap subclasses NotFoundError so existing
# isinstance() checks against aidream's error type still pass.
from matrx_orm import OrderBy, locked_transaction

from matrx_rag._ext import (
    DerivativeIntent,
    NotFoundError,
    get_db_model,
    get_document_writer,
)
from matrx_rag.chunking import Chunk
from matrx_rag.db import PACKAGE_DB_NAME
from matrx_rag.embeddings import default_text_model, embed, spec_for

log = logging.getLogger(__name__)


# Whether a COMPLETED agent-extraction run auto-indexes its structured JSON
# into RAG so it becomes searchable. ON — this is built to be used; an
# extraction the user paid for should be findable. (Was RAG_AUTO_INDEX_EXTRACTIONS,
# default-off, which silently hid extraction output from search.) Enabled
# 2026-06-12 per Arman. Manual index_extraction_run() works regardless.
AUTO_INDEX_EXTRACTIONS: bool = True


def auto_index_enabled() -> bool:
    return AUTO_INDEX_EXTRACTIONS


# ── Progress seam ────────────────────────────────────────────────────────
#
# Hosts stream this to their clients (stream-everything mandate). This
# package cannot import host event models, so the callback receives a
# package-owned dataclass and the host maps it to its typed wire events.


@dataclass(frozen=True)
class IndexingProgress:
    stage: str  # "loaded" | "chunked" | "embedding" | "writing"
    message: str = ""
    results_total: int = 0
    chunks_built: int = 0
    chunks_skipped: int = 0
    embedded: int = 0
    total_to_embed: int = 0


IndexingProgressCallback = Callable[[IndexingProgress], Awaitable[None]]

# Embedding sub-batch size for progress granularity. embed() itself handles
# provider batching/caching; slicing here only bounds how many texts settle
# between two progress emissions.
EMBED_PROGRESS_BATCH = 64


async def _notify(on_progress: IndexingProgressCallback | None, event: IndexingProgress) -> None:
    """A progress-callback failure must never fail the (paid) indexing work —
    the DB rows are the durable truth; the stream is a live view. Logged
    loudly, never silent."""
    if on_progress is None:
        return
    try:
        await on_progress(event)
    except Exception:
        log.exception("[extraction-indexing] progress callback failed (stage=%s)", event.stage)


# ── Result envelope ─────────────────────────────────────────────────────


@dataclass(frozen=True)
class IndexingResult:
    run_id: str
    job_id: str
    derivative_id: str
    derivative_outcome: str  # "created" | "reused"
    results_total: int
    chunks_written: int
    chunks_skipped: int  # empty payloads or other no-ops
    priority_applied: int
    agent_id: str | None
    embedding_model: str


# ── Payload -> text ─────────────────────────────────────────────────────


_VALUE_LIMIT = 4000  # per-field cap so a runaway nested blob doesn't explode the chunk


def payload_to_indexable_text(
    payload: Any,
    *,
    canonical_page: int | None = None,
    source_pages: list[int] | None = None,
) -> str:
    """Project an extraction result payload into embeddable text.

    Object payloads are flattened to ``KEY: value`` lines. Arrays become
    numbered lines. Scalars pass through. The canonical_page and the
    source-page range are prepended as ``PAGE: …`` so a literal
    lexical match on a page number can still pull the chunk.

    Long values are truncated at ``_VALUE_LIMIT`` to keep one chunk one
    page-record (the agent decides the granularity; we don't re-chunk).
    """
    lines: list[str] = []
    if canonical_page is not None:
        lines.append(f"PAGE: {canonical_page}")
    if source_pages:
        lines.append(f"SOURCE_PAGES: {', '.join(str(p) for p in source_pages)}")

    if isinstance(payload, dict):
        if not payload:
            return "EMPTY"
        for k, v in payload.items():
            rendered = _render_value(v)
            lines.append(f"{k}: {rendered}")
    elif isinstance(payload, list):
        if not payload:
            return "EMPTY"
        for i, item in enumerate(payload, start=1):
            lines.append(f"{i}. {_render_value(item)}")
    elif payload is None:
        return "EMPTY"
    else:
        lines.append(str(payload))

    return "\n".join(lines).strip()


def _render_value(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (str, int, float, bool)):
        out = str(v)
    else:
        out = json.dumps(v, ensure_ascii=False, default=str)
    if len(out) > _VALUE_LIMIT:
        out = out[:_VALUE_LIMIT] + "… [truncated]"
    return out


# ── Loaders ──────────────────────────────────────────────────────────────


# docproc.page_extraction_runs / _jobs / _results and agent.definition are all
# read through the shared matrx_orm model_registry — the SAME global registry
# the host (aidream) registers its docproc.*/agent.* models into at startup
# (matrx-rag CLAUDE.md rule 4); this resolves whether matrx-rag is hosted or
# standalone (this bridge is inherently an aidream-hosted feature — a bare
# matrx-rag install has no page_extraction_* tables to bridge from).
_PARENT_DOC_COLUMNS = (
    "id",
    "organization_id",
    "created_by",
    "archived_at",
    "name",
    "source_kind",
    "source_id",
    "mime_type",
    "source_hash",
)


async def _load_run_ctx(run_id: str) -> dict[str, Any] | None:
    """ORM port of the ``page_extraction_runs JOIN page_extraction_jobs LEFT
    JOIN agent.definition`` read. Three single-row lookups instead of one
    joined statement — this runs once per ``index_extraction_run`` call, not
    a hot path — preserving the LEFT JOIN semantics (missing/NULL agent ->
    ``agent_version``/``agent_default_boost`` default to 0, exactly like
    ``COALESCE(a.version, 0)`` did) and the original "row not found" contract
    (an inner-join miss on the job returns None, same as a run with no job).
    """
    PageExtractionRuns = get_db_model("PageExtractionRuns")
    PageExtractionJobs = get_db_model("PageExtractionJobs")
    # agent.definition — bare "Definition" collides with skill/tool/workflow/app
    Definition = get_db_model("Definition", schema="agent")

    # A run in Trash is not indexable — same answer as a missing run.
    run = await PageExtractionRuns.get_or_none(id=run_id, deleted_at__isnull=True)
    if run is None:
        return None
    job = await PageExtractionJobs.get_or_none(id=run.job_id)
    if job is None:
        return None

    agent_version = 0
    agent_default_boost = 0
    if job.agent_id:
        agent = await Definition.get_or_none(id=job.agent_id)
        if agent is not None:
            agent_version = int(agent.version or 0)
            agent_default_boost = int(agent.default_rag_boost or 0)

    return {
        "run_id": str(run.id),
        "job_id": str(run.job_id),
        "run_status": run.status,
        "processed_document_id": job.processed_document_id,
        "agent_id": job.agent_id,
        "job_rag_boost": job.rag_boost,
        "output_schema": job.output_schema,
        "agent_version": agent_version,
        "agent_default_boost": agent_default_boost,
    }


async def _load_results(run_id: str) -> list[dict[str, Any]]:
    rows = await (
        get_db_model("PageExtractionResults")
        .filter(run_id=run_id, deleted_at__isnull=True)
        .order_by(OrderBy("canonical_page", nulls="last"), "created_at")
        .values(
            "id",
            "run_id",
            "page_run_id",
            "job_id",
            "file_id",
            "payload",
            "source_pages",
            "canonical_page",
            "created_at",
        )
    )
    return rows


async def _resolve_effective_org(organization_id: Any, owner_id: Any) -> str:
    """The org a kg_chunks row MUST carry — READ off the parent record.

    A chunk inherits the organization of the ``processed_documents`` row it is
    extracted from. That is the only lawful source: an owner is not a tenancy,
    and an organization picked for the owner answers "which organization is this
    user's OWN workspace", never "this record names none"
    (common-docs/policies/context-is-carried-never-rebuilt.md rule 4). Until
    2026-09-17 a NULL parent org resolved a per-user assumed organization
    here, so an extraction of a team document could write its chunks into the
    owner's personal organization — invisible to everyone who ingested it, with
    nothing raised. A parent that names no organization is now a REFUSAL: fix it
    at the ingest boundary, where the organization is admitted.

    (Writing a NULL through instead is the 2026-06-03 leak class: a NULL org
    hides the row from its owner AND fails closed in the read-access predicate.)
    """
    if organization_id is not None:
        return str(organization_id)
    raise ValueError(
        "extraction_indexing: refusing to write kg_chunks — the parent "
        f"processed_document (owner {owner_id!r}) carries no organization_id. "
        "A chunk's organization is read off its parent record; it is never "
        "resolved from an organization picked for the owner. Give the parent document "
        "its organization at the ingest boundary and re-run the indexing."
    )


# ── Re-index housekeeping ────────────────────────────────────────────────


# Narrowly-scoped DELETE filter: wipes only the agent-structured-json chunks
# for THIS run on this derivative. Critical guardrail — without the
def payload_is_empty(value: Any) -> bool:
    """True when an extraction result carries no content: every value (ignoring ``__``-prefixed
    markers such as ``__kind``) is empty, recursively — including a ``__text__`` fallback whose
    text is itself an empty JSON object/list."""
    if value is None:
        return True
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return True
        if text[0] in "{[":
            try:
                return payload_is_empty(json.loads(text))
            except (json.JSONDecodeError, TypeError):
                return False
        return False
    if isinstance(value, dict):
        if "__text__" in value and len([k for k in value if not str(k).startswith("__")]) == 0:
            return payload_is_empty(value.get("__text__"))
        return all(payload_is_empty(v) for k, v in value.items() if not str(k).startswith("__"))
    if isinstance(value, (list, tuple)):
        return all(payload_is_empty(v) for v in value)
    return False


# derivation_kind + extraction_run_id filter we'd also delete future chunks
# of other kinds (summaries, manual curations, follow-on derivatives) that
# may land on the same processed_document_id.
_DERIVATION_KIND = "agent_structured_json"


# ── Main orchestrator ───────────────────────────────────────────────────


async def index_extraction_run(
    run_id: str,
    *,
    force_reindex: bool = False,
    embedding_model: str | None = None,
    on_progress: IndexingProgressCallback | None = None,
) -> IndexingResult:
    """Materialize a completed extraction run into RAG.

    Idempotent: re-running on the same ``run_id`` reuses the derivative
    row (via ``ensure_derivative`` get_or_create) and rewrites the
    chunks. ``force_reindex`` is a no-op today because the rewrite is
    unconditional; it's reserved for a future "skip if unchanged"
    optimization.

    Returns an :class:`IndexingResult` envelope. Callers can inspect
    ``chunks_written`` to confirm coverage.

    Raises ``NotFoundError`` when the run / job / parent document is
    missing, ``RuntimeError`` if the run hasn't reached a terminal
    success state and ``force_reindex`` is False.
    """
    embedding_model = embedding_model or default_text_model()

    run_ctx = await _load_run_ctx(run_id)
    if run_ctx is None:
        raise NotFoundError(f"page_extraction_run {run_id} not found")
    if run_ctx["run_status"] != "completed" and not force_reindex:
        raise RuntimeError(
            f"refusing to index run {run_id} with status="
            f"{run_ctx['run_status']!r}; pass force_reindex=True to override"
        )
    parent_doc_id = run_ctx["processed_document_id"]
    if parent_doc_id is None:
        raise NotFoundError(f"job {run_ctx['job_id']} has no processed_document_id; cannot derive")
    parent_rows = (
        await get_db_model("ProcessedDocuments")
        .filter(id=parent_doc_id)
        .values(*_PARENT_DOC_COLUMNS)
    )
    parent_doc = parent_rows[0] if parent_rows else None
    if parent_doc is None:
        raise NotFoundError(f"parent processed_document {parent_doc_id} not found")
    if parent_doc["archived_at"] is not None:
        raise NotFoundError(
            f"parent processed_document {parent_doc_id} is archived; "
            "cannot index a derivative against archived content"
        )

    results = await _load_results(run_id)
    await _notify(
        on_progress,
        IndexingProgress(
            stage="loaded",
            message=f"Loaded {len(results)} extraction result(s)",
            results_total=len(results),
        ),
    )
    pages = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=parent_doc_id)
        .values("id", "page_number", "page_index")
    )

    # Map 1-based page_number -> page row id (for primary_page_id).
    page_id_by_number: dict[int, str] = {int(p["page_number"]): str(p["id"]) for p in pages}

    # Resolve priority (per the boost chain): job override > agent default > 0.
    priority = run_ctx["job_rag_boost"]
    if priority is None:
        priority = int(run_ctx["agent_default_boost"] or 0)
    priority = int(priority)

    agent_id_str = str(run_ctx["agent_id"]) if run_ctx["agent_id"] else None
    agent_version = int(run_ctx["agent_version"] or 0)

    # Create or reuse the derivative processed_documents row. params_hash
    # is keyed on (run_id) so re-indexing the same run is a no-op for
    # the derivative row but rewrites its chunks.
    derivative_params = {"run_id": str(run_id)}
    derivative = await get_document_writer().ensure_derivative(
        intent=DerivativeIntent.GET_OR_CREATE_DERIVATIVE,
        parent_processed_id=str(parent_doc_id),
        derivation_kind="agent_structured_json",
        agent_id=agent_id_str,
        agent_version=agent_version,
        params=derivative_params,
        name=f"{parent_doc['name']} (agent extract run {str(run_id)[:8]})",
        rag_boost=priority,
        metadata={
            "job_id": str(run_ctx["job_id"]),
            "run_id": str(run_id),
            "results_total": len(results),
        },
    )
    derivative_id = derivative.id

    if not results:
        # Nothing to index; the derivative row is created (or reused)
        # so the catalog shows the run, but no chunks land.
        log.info(
            "[extraction-indexing] run=%s -> derivative=%s no results to index",
            run_id,
            derivative_id,
        )
        return IndexingResult(
            run_id=str(run_id),
            job_id=str(run_ctx["job_id"]),
            derivative_id=derivative_id,
            derivative_outcome=derivative.outcome,
            results_total=0,
            chunks_written=0,
            chunks_skipped=0,
            priority_applied=priority,
            agent_id=agent_id_str,
            embedding_model=embedding_model,
        )

    # Build chunks (one per non-empty result).
    chunks: list[Chunk] = []
    chunk_to_result: list[dict[str, Any]] = []  # parallel array of result rows
    skipped = 0
    for idx, result in enumerate(results):
        payload = result["payload"]
        if payload is None:
            skipped += 1
            continue
        try:
            decoded = json.loads(payload) if isinstance(payload, str) else payload
        except (json.JSONDecodeError, TypeError):
            decoded = payload  # already-decoded jsonb arrives as Python object
        if payload_is_empty(decoded):
            # An extraction that found nothing ({"rules": []}, a text fallback of the same, {} or
            # []) is not searchable content — indexing it put empty chunks on the Source (audit
            # 2026-09-26: 17 on one scanned PDF). Skipped, and counted.
            skipped += 1
            continue
        text = payload_to_indexable_text(
            decoded,
            canonical_page=result["canonical_page"],
            source_pages=list(result["source_pages"] or []),
        )
        if not text or text == "EMPTY":
            skipped += 1
            continue
        chunks.append(
            Chunk(
                chunk_id=str(uuid.uuid4()),
                parent_chunk_id=None,
                chunk_index=idx,
                chunk_kind="agent_structured_json",
                content_text=text,
                token_count=_token_estimate(text),
                language=None,
                metadata={
                    "role": "agent_extract",
                    "agent_id": agent_id_str,
                    "agent_version": agent_version,
                    "run_id": str(run_id),
                    "result_id": str(result["id"]),
                    "canonical_page": result["canonical_page"],
                    "source_pages": list(result["source_pages"] or []),
                    "payload": decoded,
                },
            )
        )
        chunk_to_result.append(dict(result))

    await _notify(
        on_progress,
        IndexingProgress(
            stage="chunked",
            message=f"Built {len(chunks)} chunk(s), skipped {skipped}",
            results_total=len(results),
            chunks_built=len(chunks),
            chunks_skipped=skipped,
        ),
    )

    if not chunks:
        log.info(
            "[extraction-indexing] run=%s all %d results empty/null; skipping embed",
            run_id,
            len(results),
        )
        # Still wipe any prior derivative chunks (the run may have produced
        # chunks before, and re-indexing should leave nothing behind).
        await _wipe_derivative_chunks(derivative_id, str(run_id))
        return IndexingResult(
            run_id=str(run_id),
            job_id=str(run_ctx["job_id"]),
            derivative_id=derivative_id,
            derivative_outcome=derivative.outcome,
            results_total=len(results),
            chunks_written=0,
            chunks_skipped=skipped,
            priority_applied=priority,
            agent_id=agent_id_str,
            embedding_model=embedding_model,
        )

    # Embed all chunks, in bounded sub-batches so progress streams per batch.
    embedding_texts = [c.content_text for c in chunks]
    embeddings: list[list[float]] = []
    for start in range(0, len(embedding_texts), EMBED_PROGRESS_BATCH):
        batch = embedding_texts[start : start + EMBED_PROGRESS_BATCH]
        embeddings.extend(
            await embed(
                embedding_model,
                batch,
                input_type="document",
                # Provenance on the shared embedding cache: the organization of
                # the parent document being indexed (a parent that names none
                # REFUSES here, exactly as the chunk write does below).
                organization_id=await _resolve_effective_org(
                    parent_doc["organization_id"], parent_doc["created_by"]
                ),
            )
        )
        await _notify(
            on_progress,
            IndexingProgress(
                stage="embedding",
                message=f"Embedded {len(embeddings)} / {len(embedding_texts)}",
                results_total=len(results),
                chunks_built=len(chunks),
                chunks_skipped=skipped,
                embedded=len(embeddings),
                total_to_embed=len(embedding_texts),
            ),
        )

    # Write to rag.kg_chunks with full provenance.
    await _notify(
        on_progress,
        IndexingProgress(
            stage="writing",
            message=f"Writing {len(chunks)} chunk(s) to the knowledge graph",
            results_total=len(results),
            chunks_built=len(chunks),
            chunks_skipped=skipped,
            embedded=len(embeddings),
            total_to_embed=len(embedding_texts),
        ),
    )
    chunks_written = await _upsert_derivative_chunks(
        derivative_id=derivative_id,
        parent_doc=parent_doc,
        chunks=chunks,
        embeddings=embeddings,
        embedding_model=embedding_model,
        results=chunk_to_result,
        priority=priority,
        agent_id=agent_id_str,
        run_id=str(run_id),
        page_id_by_number=page_id_by_number,
    )

    log.info(
        "[extraction-indexing] run=%s -> derivative=%s "
        "results=%d chunks=%d skipped=%d priority=%d agent=%s",
        run_id,
        derivative_id,
        len(results),
        chunks_written,
        skipped,
        priority,
        agent_id_str,
    )
    return IndexingResult(
        run_id=str(run_id),
        job_id=str(run_ctx["job_id"]),
        derivative_id=derivative_id,
        derivative_outcome=derivative.outcome,
        results_total=len(results),
        chunks_written=chunks_written,
        chunks_skipped=skipped,
        priority_applied=priority,
        agent_id=agent_id_str,
        embedding_model=embedding_model,
    )


# ── Helpers ──────────────────────────────────────────────────────────────


def _token_estimate(text: str) -> int:
    # Cheap approximation: 1 token ≈ 4 chars for English-ish text.
    # The OpenAI tokenizer in chunking.py is used for raw extracts; here we
    # don't need exact token accounting because the agent already chose the
    # granularity (one chunk per result).
    return max(1, len(text) // 4)


async def _wipe_derivative_chunks(derivative_id: str, run_id: str) -> None:
    """Wipe any agent_structured_json chunks for THIS specific run on the
    derivative. Scoped narrowly so a future writer of other chunk kinds
    on the same derivative_id is not affected.
    """
    await get_db_model("KgChunks").delete_where(
        processed_document_id=derivative_id,
        derivation_kind=_DERIVATION_KIND,
        extraction_run_id=run_id,
    )


async def _upsert_derivative_chunks(
    *,
    derivative_id: str,
    parent_doc: Any,
    chunks: list[Chunk],
    embeddings: list[list[float]],
    embedding_model: str,
    results: list[dict[str, Any]],
    priority: int,
    agent_id: str | None,
    run_id: str,
    page_id_by_number: dict[int, str],
) -> int:
    """Replace this run's chunks on the derivative with the new set, then
    insert the embedding rows. Returns count of chunks written.

    Concurrency: holds a transaction-scoped pg_advisory_xact_lock keyed on
    derivative_id so a concurrent indexer (auto-hook racing with manual
    POST /index) serializes at the DB. The DELETE+INSERT is narrowly
    scoped to ``(derivation_kind='agent_structured_json',
    extraction_run_id=run_id)`` so future chunk kinds on the same
    derivative (summaries, curations) are not affected.
    """
    if len(chunks) != len(embeddings) or len(chunks) != len(results):
        raise ValueError(
            f"length mismatch: chunks={len(chunks)} embeddings={len(embeddings)} "
            f"results={len(results)}"
        )

    info = spec_for(embedding_model)
    # Defensive: the embedding write hits a per-model table whose vector
    # column has a fixed dimension. A provider regression that returns
    # the wrong-shaped vector would otherwise blow up with an opaque pg
    # error mid-transaction. Catch it before we touch the DB.
    if embeddings and len(embeddings[0]) != info.dim:
        raise ValueError(
            f"embedding dim mismatch: got {len(embeddings[0])} from "
            f"model {embedding_model!r}; spec table {info.table} expects {info.dim}"
        )

    def _page_columns(result: dict[str, Any]) -> tuple[str | None, list[int], list[dict[str, Any]]]:
        # Normalize source_pages — agent output may smuggle strings; coerce
        # to int defensively. Drop unparseable entries with a warning.
        raw_pages = result.get("source_pages") or []
        source_pages: list[int] = []
        for p in raw_pages:
            try:
                source_pages.append(int(p))
            except (TypeError, ValueError):
                log.warning(
                    "[extraction-indexing] non-int page %r in result %s; dropping",
                    p,
                    result.get("id"),
                )
        canonical = result.get("canonical_page")
        if canonical is None and source_pages:
            canonical = source_pages[0]
        try:
            canonical_int = int(canonical) if canonical is not None else None
        except (TypeError, ValueError):
            canonical_int = None
        primary = page_id_by_number.get(canonical_int) if canonical_int else None
        spans = [{"page_number": p, "page_index": p - 1 if p else None} for p in source_pages]
        if not source_pages and canonical_int is None:
            log.warning(
                "[extraction-indexing] result %s has neither canonical_page nor "
                "source_pages; chunk will not be page-anchored",
                result.get("id"),
            )
        return primary, source_pages, spans

    KgChunks = get_db_model("KgChunks")

    # Read the parent's organization ONCE (a parent with none REFUSES) so every
    # chunk AND every embedding row below is written with the organization the
    # document really belongs to — never NULL, never a personal-org default.
    effective_org = await _resolve_effective_org(
        parent_doc["organization_id"], parent_doc["created_by"]
    )

    chunk_rows: list[dict[str, Any]] = []
    for i, chunk in enumerate(chunks):
        result = results[i]
        primary, page_numbers, spans = _page_columns(result)
        chunk_rows.append(
            {
                "id": chunk.chunk_id,
                "organization_id": effective_org,
                "created_by": parent_doc["created_by"],
                "source_kind": parent_doc["source_kind"],
                "source_id": parent_doc["source_id"],
                "field_id": None,
                "parent_chunk_id": None,
                "chunk_index": chunk.chunk_index,
                "chunk_kind": chunk.chunk_kind,
                "content_text": chunk.content_text,
                "token_count": chunk.token_count,
                "language": chunk.language,
                "mime_type": parent_doc["mime_type"],
                "source_hash": parent_doc["source_hash"],
                # chunker_name records the agent identity so callers can
                # filter "all chunks from agent X" via a single column.
                "chunker_name": f"agent:{agent_id or 'none'}",
                # chunker_version stays the canonical version constant for
                # derivative chunks. Run identity lives in extraction_run_id;
                # mixing it here defeats the column.
                "chunker_version": "v1",
                "metadata": chunk.metadata or {},
                "processed_document_id": derivative_id,
                "primary_page_id": primary,
                "page_numbers": page_numbers,
                "page_spans": spans,
                "token_estimate": chunk.token_count,
                "priority": priority,
                "derivation_kind": _DERIVATION_KIND,
                "agent_id": agent_id,
                "extraction_run_id": run_id,
                "extraction_result_id": str(result["id"]),
            }
        )

    # Advisory-lock transaction: lock + DELETE + bulk INSERT share ONE
    # connection via matrx_orm.transaction() (ContextVar-bound), so
    # concurrent indexers (auto-hook racing with manual POST /index)
    # serialize at the DB exactly like the old hand-rolled
    # pool.acquire()+conn.transaction() block did. This INSERT has no ON
    # CONFLICT — the preceding DELETE is what makes the whole-set REPLACE
    # idempotent (no dedup contract to preserve here, unlike derivation.py's
    # incremental-append writer).
    async with locked_transaction(derivative_id, database=PACKAGE_DB_NAME):
        # hard-delete-ok: derived search chunks, rebuilt on re-ingest of their source
        await KgChunks.delete_where(
            processed_document_id=derivative_id,
            derivation_kind=_DERIVATION_KIND,
            extraction_run_id=run_id,
        )
        await KgChunks.bulk_create(chunk_rows)

    # Embeddings — AFTER the advisory-lock transaction committed, in
    # idempotent set-based sub-batches (ON CONFLICT DO NOTHING). The
    # chunks are durable regardless; a failure here self-heals on the
    # next ingest of the source (ingestion._unembedded_chunk_ids).
    from matrx_rag.ingestion import _write_embedding_rows

    # ingestion._write_embedding_rows is fully ORM (bulk_insert_ignore on the
    # resolved embedding Model) — it takes no connection at all, so there is
    # nothing for this call site to hand it.
    await _write_embedding_rows(
        info.table,
        [
            (
                c.chunk_id,
                effective_org,
                parent_doc["created_by"],
                _format_vector(v),
            )
            for c, v in zip(chunks, embeddings, strict=True)
        ],
    )
    return len(chunks)


def _format_vector(values: list[float]) -> str:
    """Format a float list as a pgvector literal string."""
    return "[" + ",".join(f"{v:.7g}" for v in values) + "]"


__all__ = [
    "auto_index_enabled",
    "index_extraction_run",
    "payload_to_indexable_text",
    "IndexingProgress",
    "IndexingProgressCallback",
    "IndexingResult",
]
