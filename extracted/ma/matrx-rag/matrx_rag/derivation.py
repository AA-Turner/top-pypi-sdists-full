"""
Generic derivation primitive — one source document into a named, retrievable
*derived chunk set*.

A "Knowledge Asset" is one source (``cld_file``) -> an ``initial_extract``
``processed_document`` -> a chain of DERIVED representations, each its own
``derivation_kind`` with its own ``rag.kg_chunks`` set::

    source (cld_file)
     └─ processed_document (initial_extract)            <- the parent
         ├─ derivation_kind='clean_v1'        -> chunks  (U3 canonical clean)
         ├─ derivation_kind='table_row'       -> chunks  (U1 one chunk / row)
         ├─ derivation_kind='page_image_caption' -> chunks (U2 captions)
         ├─ derivation_kind='section_summary' -> chunks  (U5)
         ├─ derivation_kind='synthetic_qa'    -> chunks  (U6)
         └─ derivation_kind='chunked_{coarse,normal,fine}' -> chunks (U7)

Every representation is its own retrievable set scoped by
``(processed_document_id = derivative, derivation_kind)`` so search blends them
and re-deriving one never disturbs another.

``derive_chunk_set`` is the platform primitive extracted from
``extraction_indexing.py`` (which handled only the ``agent_structured_json``
case). It does the shared mechanics ONCE:

  1. ``ensure_derivative`` — create/reuse the derivative ``processed_document``
     (idempotent on parent + ``derivation_kind`` + identity ``params``).
  2. embed the chunk texts in one batched call.
  3. advisory-lock the derivative, DELETE prior chunks **of this kind**, INSERT
     the new set with full provenance (source columns inherited from the
     parent so chunks trace to the original ``cld_file``; page anchoring;
     priority; ``derivation_kind``; optional agent / run / result identity).
  4. write the embedding rows (idempotent, self-healing on the next ingest).

Each utility supplies only a list of :class:`ChunkSpec` (text + metadata +
page anchoring) — the *generator*. The table / image / summary / Q&A /
multi-granularity utilities are all thin generators on top of this; the
agent-extraction indexer (:mod:`matrx_rag.extraction_indexing`) is the first
consumer and delegates its write path here.

Re-running with the same ``parent_processed_id`` + ``derivation_kind`` +
``identity`` reuses the derivative row and REPLACES its chunk set — safe to
call repeatedly.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from typing import Any

from matrx_orm import ConflictTarget, Count, JsonText, locked_transaction

from matrx_rag._ext import (
    DerivativeIntent,
    NotFoundError,
    get_db_model,
    get_document_writer,
)
from matrx_rag.db import PACKAGE_DB_NAME
from matrx_rag.embeddings import default_text_model, embed, spec_for

log = logging.getLogger(__name__)


# ── Inputs / outputs ─────────────────────────────────────────────────────


@dataclass
class ChunkSpec:
    """One chunk to materialize in a derived set.

    The generator (table extractor, summarizer, …) produces these; the
    primitive handles embedding + provenance + persistence.
    """

    content_text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    chunk_index: int = 0
    # Page anchoring back to the parent document's pages. ``page_numbers`` are
    # 1-based page_number values; ``primary_page_number`` is the canonical
    # page (defaults to the first of page_numbers). Both optional — a chunk
    # with no page anchor (e.g. a whole-doc summary) is allowed.
    page_numbers: list[int] = field(default_factory=list)
    primary_page_number: int | None = None
    # Defaults to the set's derivation_kind. Override when the chunk-level
    # kind differs (rare).
    chunk_kind: str | None = None
    language: str | None = None
    # Extraction-case provenance (None for non-agent derivations).
    extraction_result_id: str | None = None


@dataclass(frozen=True)
class DeriveResult:
    parent_processed_id: str
    derivative_id: str
    derivation_kind: str
    derivative_outcome: str  # "created" | "reused"
    chunks_written: int
    priority_applied: int
    embedding_model: str


# ── ORM read/write shapes ────────────────────────────────────────────────
#
# docproc.processed_documents is read via the shared matrx_orm model_registry
# (get_db_model("ProcessedDocuments")) — the SAME global registry the host
# (aidream) registers its docproc.* models into at startup, so this resolves
# whether matrx-rag is hosted or standalone (matrx-rag CLAUDE.md rule 4).
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


# Kind-scoped conflict target for the derived-chunk write below: a derived
# chunk row's identity is (processed_document_id, chunk_index,
# derivation_kind) — the partial unique index kg_chunks_derivation_set_uidx
# (excludes derivation_kind='initial_extract'). ON CONFLICT DO NOTHING makes
# a batch RETRY after its chunk-tx committed a no-op instead of a
# double-insert (kg_038, 2026-07-07), which is what lets the flush callers
# self-heal with retry_on_transient.
# `deleted_at IS NULL` is part of the index predicate, so it is part of the
# inference specification too: ON CONFLICT can only infer a partial index whose
# predicate the target implies. Drop this line and every derived-chunk insert
# raises 42P10 "no unique or exclusion constraint matching the ON CONFLICT
# specification" (kg_chunks_derivation_set_uidx became partial 2026-09-20 so a
# REMOVED chunk stops blocking its own re-derivation).
_CHUNK_CONFLICT_TARGET = ConflictTarget.partial(
    ["processed_document_id", "chunk_index", "derivation_kind"],
    where_not_equals={"derivation_kind": "initial_extract"},
    where_is_null=("deleted_at",),
)


# ── Helpers ──────────────────────────────────────────────────────────────


def token_estimate(text: str) -> int:
    """Cheap approximation: ~1 token per 4 chars. Generators choose chunk
    granularity, so exact tokenization isn't needed here."""
    return max(1, len(text) // 4)


def format_vector(values: list[float]) -> str:
    """Format a float list as a pgvector literal."""
    return "[" + ",".join(f"{v:.7g}" for v in values) + "]"


# ── Primitive ─────────────────────────────────────────────────────────────


async def derive_chunk_set(
    *,
    parent_processed_id: str,
    derivation_kind: str,
    chunks: list[ChunkSpec],
    identity: dict[str, Any],
    name: str | None = None,
    rag_boost: int = 0,
    metadata: dict[str, Any] | None = None,
    embedding_model: str | None = None,
    agent_id: str | None = None,
    agent_version: int = 0,
    extraction_run_id: str | None = None,
    chunker_name: str | None = None,
    chunker_version: str = "v1",
    replace: bool = True,
) -> DeriveResult:
    """Materialize ``chunks`` as the ``derivation_kind`` chunk set of
    ``parent_processed_id``.

    ``identity`` keys the derivative row's idempotency (e.g. ``{"run_id": …}``
    or ``{"source": "table_extract"}``). Re-running with the same parent +
    kind + identity reuses the derivative and REPLACES its chunk set.

    ``replace`` (default True) controls the DELETE-prior step. The default is
    the original REPLACE-the-whole-set semantics: the prior chunks of this kind
    are deleted before the new set lands. Pass ``replace=False`` for a PURE
    APPEND — no delete, the new chunks are added to whatever already exists.
    This is what makes INCREMENTAL, resumable derivations possible: a generator
    can flush successive batches (each ``replace=False``) and money already
    spent is durable the moment each batch commits, instead of being held in
    memory until one final replace-everything write. The caller owns the
    "clear once at the start" decision (call once with ``replace=True`` and an
    empty list) when it wants a clean rebuild.

    Provenance: each chunk inherits ``source_kind / source_id / mime_type /
    source_hash / organization_id / created_by`` from the parent document, so it
    traces back to the original ``cld_file``; ``processed_document_id`` is the
    derivative; ``derivation_kind`` tags the set.

    Raises ``NotFoundError`` if the parent is missing or archived.
    """
    embedding_model = embedding_model or default_text_model()

    ProcessedDocuments = get_db_model("ProcessedDocuments")
    parent_rows = await ProcessedDocuments.filter(id=parent_processed_id).values(
        *_PARENT_DOC_COLUMNS
    )
    parent_doc = parent_rows[0] if parent_rows else None
    if parent_doc is None:
        raise NotFoundError(f"parent processed_document {parent_processed_id} not found")
    if parent_doc["archived_at"] is not None:
        raise NotFoundError(
            f"parent processed_document {parent_processed_id} is archived; "
            "cannot derive against archived content"
        )
    pages = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=parent_processed_id)
        .values("id", "page_number", "page_index")
    )

    # EVERY rag.kg_chunks row MUST carry a non-NULL organization_id (a NULL org
    # is the 2026-06-03 "NULL org => globally visible" leak), and the derivative
    # inherits the PARENT's — the record it is derived from, set at the ingest
    # boundary. A parent that carries none is a defect at that boundary, and the
    # answer is a refusal naming it: until 2026-09-17 this resolved the owner's
    # personal organization instead, which silently moved a team document's
    # chunks into one person's workspace
    # (common-docs/policies/context-is-carried-never-rebuilt.md rule 4 — the
    # personal organization answers only "this user's OWN workspace").
    organization_id = parent_doc["organization_id"]
    if organization_id is None:
        raise ValueError(
            f"derive: parent processed_document {parent_processed_id} (owner "
            f"{parent_doc['created_by']!r}) carries no organization_id, so a "
            "derivative has no organization to inherit. A chunk's organization "
            "is read off its parent record and is never resolved from the "
            "owner — give the parent document its "
            "organization at the ingest boundary and re-run the derivation."
        )

    page_id_by_number: dict[int, str] = {int(p["page_number"]): str(p["id"]) for p in pages}

    derivative = await get_document_writer().ensure_derivative(
        intent=DerivativeIntent.GET_OR_CREATE_DERIVATIVE,
        parent_processed_id=str(parent_processed_id),
        derivation_kind=derivation_kind,
        agent_id=agent_id,
        agent_version=agent_version,
        params=identity,
        name=name or f"{parent_doc['name']} ({derivation_kind})",
        rag_boost=rag_boost,
        metadata=(metadata or {}) | {"chunk_count": len(chunks)},
    )
    derivative_id = derivative.id

    # Empty set: derivative row exists (catalog shows it). When replacing, wipe
    # any prior chunks of this kind so a re-derive that produced nothing leaves
    # nothing — and this is also the "clear once" path a resumable rebuild uses
    # (replace=True, chunks=[]). When appending (replace=False), an empty batch
    # is a NO-OP: never delete, so a remainder-flush of nothing can't wipe the
    # batches already persisted in this run.
    if not chunks:
        if replace:
            await get_db_model("KgChunks").delete_where(
                processed_document_id=derivative_id, derivation_kind=derivation_kind
            )
        log.info(
            "[derive] parent=%s kind=%s -> derivative=%s (no chunks, replace=%s)",
            parent_processed_id,
            derivation_kind,
            derivative_id,
            replace,
        )
        return DeriveResult(
            parent_processed_id=str(parent_processed_id),
            derivative_id=derivative_id,
            derivation_kind=derivation_kind,
            derivative_outcome=derivative.outcome,
            chunks_written=0,
            priority_applied=rag_boost,
            embedding_model=embedding_model,
        )

    # Embed in one batch.
    embedding_texts = [c.content_text for c in chunks]
    embeddings = await embed(
        embedding_model,
        embedding_texts,
        input_type="document",
        # Provenance on the shared embedding cache: the parent document's
        # organization, refused above when the record carries none.
        organization_id=organization_id,
    )

    info = spec_for(embedding_model)
    # Defensive: catch a wrong-shaped vector before it blows up mid-transaction
    # against a fixed-dimension embedding table.
    if embeddings and len(embeddings[0]) != info.dim:
        raise ValueError(
            f"embedding dim mismatch: got {len(embeddings[0])} from model "
            f"{embedding_model!r}; spec table {info.table} expects {info.dim}"
        )

    written = await _write_chunks(
        derivative_id=derivative_id,
        derivation_kind=derivation_kind,
        parent_doc=parent_doc,
        organization_id=organization_id,
        chunks=chunks,
        embeddings=embeddings,
        embedding_table=info.table,
        priority=rag_boost,
        agent_id=agent_id,
        extraction_run_id=extraction_run_id,
        chunker_name=chunker_name or f"derive:{derivation_kind}",
        chunker_version=chunker_version,
        page_id_by_number=page_id_by_number,
        replace=replace,
    )

    log.info(
        "[derive] parent=%s kind=%s -> derivative=%s chunks=%d priority=%d replace=%s",
        parent_processed_id,
        derivation_kind,
        derivative_id,
        written,
        rag_boost,
        replace,
    )
    return DeriveResult(
        parent_processed_id=str(parent_processed_id),
        derivative_id=derivative_id,
        derivation_kind=derivation_kind,
        derivative_outcome=derivative.outcome,
        chunks_written=written,
        priority_applied=rag_boost,
        embedding_model=embedding_model,
    )


async def _write_chunks(
    *,
    derivative_id: str,
    derivation_kind: str,
    parent_doc: Any,
    organization_id: str,
    chunks: list[ChunkSpec],
    embeddings: list[list[float]],
    embedding_table: str,
    priority: int,
    agent_id: str | None,
    extraction_run_id: str | None,
    chunker_name: str,
    chunker_version: str,
    page_id_by_number: dict[int, str],
    replace: bool = True,
) -> int:
    """Write this set's chunks on the derivative, then write the embedding rows.
    Holds a transaction-scoped advisory lock keyed on the derivative so
    concurrent re-derivations serialize at the DB.

    When ``replace`` (default), the prior chunks of this kind are DELETED first
    — the original replace-the-whole-set semantics. When ``replace=False`` this
    is a PURE APPEND: no delete, the rows are simply added. The advisory lock is
    held in BOTH modes, so concurrent appends/replaces of the same derivative
    still serialize.

    IDEMPOTENT: the INSERT is keyed on the set identity
    ``(processed_document_id, chunk_index, derivation_kind)`` with ON CONFLICT
    DO NOTHING (index ``kg_chunks_derivation_set_uidx``, kg_038) — re-running a
    batch whose chunk transaction already committed lands ZERO new rows instead
    of double-inserting, so a transient-failure retry is safe. Embedding rows
    are written only for the ids that actually landed. Returns the number of
    rows that actually landed (0 on a full-conflict retry)."""
    if len(chunks) != len(embeddings):
        raise ValueError(f"length mismatch: chunks={len(chunks)} embeddings={len(embeddings)}")

    def _page_columns(spec: ChunkSpec) -> tuple[str | None, list[int], list[dict[str, Any]]]:
        # Coerce page numbers defensively (generators may smuggle strings).
        source_pages: list[int] = []
        for p in spec.page_numbers or []:
            try:
                source_pages.append(int(p))
            except (TypeError, ValueError):
                log.warning("[derive] non-int page %r dropped", p)
        canonical = spec.primary_page_number
        if canonical is None and source_pages:
            canonical = source_pages[0]
        try:
            canonical_int = int(canonical) if canonical is not None else None
        except (TypeError, ValueError):
            canonical_int = None
        primary = page_id_by_number.get(canonical_int) if canonical_int else None
        spans = [{"page_number": p, "page_index": p - 1 if p else None} for p in source_pages]
        return primary, source_pages, spans

    KgChunks = get_db_model("KgChunks")

    chunk_ids: list[str] = []
    chunk_rows: list[dict[str, Any]] = []
    for spec in chunks:
        primary, page_numbers, spans = _page_columns(spec)
        text = spec.content_text
        chunk_id = str(uuid.uuid4())
        chunk_ids.append(chunk_id)
        chunk_rows.append(
            {
                "id": chunk_id,
                "organization_id": organization_id,
                "created_by": parent_doc["created_by"],
                "source_kind": parent_doc["source_kind"],
                "source_id": parent_doc["source_id"],
                "field_id": None,
                "parent_chunk_id": None,
                "chunk_index": spec.chunk_index,
                "chunk_kind": spec.chunk_kind or derivation_kind,
                "content_text": text,
                "token_count": token_estimate(text),
                "language": spec.language,
                "mime_type": parent_doc["mime_type"],
                "source_hash": parent_doc["source_hash"],
                "chunker_name": chunker_name,
                "chunker_version": chunker_version,
                "metadata": spec.metadata or {},
                "processed_document_id": derivative_id,
                "primary_page_id": primary,
                "page_numbers": page_numbers,
                "page_spans": spans,
                "token_estimate": token_estimate(text),
                "priority": priority,
                "derivation_kind": derivation_kind,
                "agent_id": agent_id,
                "extraction_run_id": extraction_run_id,
                "extraction_result_id": spec.extraction_result_id,
            }
        )

    # Advisory-lock transaction: lock + (replace-mode) bulk chunk DELETE +
    # conflict-safe bulk INSERT share ONE connection via matrx_orm.transaction()
    # (ContextVar-bound), so the DELETE-then-INSERT idempotency contract holds
    # exactly like the old hand-rolled pool.acquire()+conn.transaction() block.
    async with locked_transaction(derivative_id, database=PACKAGE_DB_NAME):
        # Replace mode wipes the prior set first; append mode (replace=False)
        # must NOT delete — that is the whole point of incremental writing.
        if replace:
            # hard-delete-ok: derived search chunks, rebuilt on re-ingest of their source
            await KgChunks.delete_where(
                processed_document_id=derivative_id, derivation_kind=derivation_kind
            )

        # One set-based INSERT; ON CONFLICT DO NOTHING + RETURNING gives us
        # exactly the ids that landed (a retried, already-committed batch
        # returns none — the idempotency contract).
        landed_ids: set[str] = set(
            await KgChunks.bulk_insert_ignore(
                chunk_rows, on_conflict=_CHUNK_CONFLICT_TARGET, returning="id"
            )
        )
        skipped = len(chunk_rows) - len(landed_ids)
        if skipped:
            log.warning(
                "[derive] derivative=%s kind=%s: %d/%d chunk(s) already existed "
                "(idempotent retry of a committed batch — no double-insert).",
                derivative_id,
                derivation_kind,
                skipped,
                len(chunk_rows),
            )

    # Embeddings AFTER the lock transaction commits — idempotent
    # (ON CONFLICT DO NOTHING). Chunks are durable regardless; a failure
    # here self-heals on the next ingest (ingestion._unembedded_chunk_ids).
    # Only chunks that actually landed get an embedding row — a
    # conflict-skipped chunk's row would orphan against the FK.
    from matrx_rag.ingestion import _write_embedding_rows

    # ingestion._write_embedding_rows is fully ORM (bulk_insert_ignore on the
    # resolved embedding Model) — it takes no connection at all, so there is
    # nothing for this call site to hand it.
    await _write_embedding_rows(
        embedding_table,
        [
            (
                chunk_ids[i],
                organization_id,
                parent_doc["created_by"],
                format_vector(v),
            )
            for i, v in enumerate(embeddings)
            if chunk_ids[i] in landed_ids
        ],
    )
    return len(landed_ids)


# ── Resume support ─────────────────────────────────────────────────────────


# Find the derivative processed_document ids for (parent, derivation_kind) so
# the resume readers can scope chunks to exactly this derivation. There can be
# more than one derivative for a parent+kind (distinct identity params), so
# this returns the full id set. Reads through the shared matrx_orm
# model_registry (get_db_model("ProcessedDocuments")) — the SAME global
# registry the host registers its docproc.* models into (matrx-rag CLAUDE.md
# rule 4); it resolves whether matrx-rag is hosted or standalone.
async def _derivative_ids(parent_processed_id: str, derivation_kind: str) -> list[str]:
    rows = (
        await get_db_model("ProcessedDocuments")
        .filter(parent_processed_id=parent_processed_id, derivation_kind=derivation_kind)
        .values("id")
    )
    return [str(r["id"]) for r in rows]


async def _existing_metadata_ints(
    parent_processed_id: str, derivation_kind: str, *, key: str
) -> set[int]:
    """The DISTINCT set of int values at ``metadata->>key`` across this
    derivation's chunks (parent + kind).

    ORM port of the former raw kg_chunks JOIN + jsonb projection: load the
    derivative ``processed_document`` ids then the kind-tagged chunks'
    ``metadata`` through the injected ORM (``KgChunks.filter(...).values
    ("metadata")``), and project ``key`` in Python. ``metadata ? key`` becomes
    ``key in md``; the caller's ``is not None`` guard becomes the per-value int
    coercion — same set either way.

    This lookup is deliberately fail-closed. Returning an empty set after a DB
    error would make a resume silently redo every paid model call. A temporary
    read failure is cheaper and safer to surface than destroying the only
    trustworthy record of completed work."""
    derivative_ids = await _derivative_ids(parent_processed_id, derivation_kind)
    if not derivative_ids:
        return set()

    KgChunks = get_db_model("KgChunks")
    chunk_rows = await KgChunks.filter(
        processed_document_id__in=derivative_ids,
        derivation_kind=derivation_kind,
    ).values("metadata")

    out: set[int] = set()
    for row in chunk_rows:
        raw = (row.get("metadata") or {}).get(key)
        if raw is None:
            continue
        try:
            out.add(int(raw))
        except (TypeError, ValueError):
            continue
    return out


async def count_existing_metadata_ints(
    parent_processed_id: str, derivation_kind: str, *, key: str
) -> int:
    """Count distinct persisted resume keys without transferring every chunk.

    This is the rollup/preflight companion to ``_existing_metadata_ints``.
    Runners need the full set in order to skip exact items; status surfaces only
    need the count, so PostgreSQL performs ``COUNT(DISTINCT metadata->>key)``.
    Like the set reader, this fails closed on read errors.
    """
    derivative_ids = await _derivative_ids(parent_processed_id, derivation_kind)
    if not derivative_ids:
        return 0

    KgChunks = get_db_model("KgChunks")
    rows = await (
        KgChunks.filter(
            processed_document_id__in=derivative_ids,
            derivation_kind=derivation_kind,
        )
        .annotate(completed_items=Count(JsonText("metadata", key), distinct=True))
        .values("completed_items")
    )
    return int(rows[0]["completed_items"] or 0) if rows else 0


async def existing_max_chunk_index(parent_processed_id: str, derivation_kind: str) -> int:
    """The highest ``chunk_index`` already persisted for this derivation
    (parent + kind), or ``-1`` when none exist.

    Resume support for generators whose chunk_index is a RUNNING COUNTER
    (synthetic Q&A pairs, figure captions): a resumed run must continue from
    ``max + 1``, never restart at 0 — with the kg_038 unique set identity
    ``(derivative, chunk_index, kind)``, a restarted counter would collide with
    the previous run's rows and the idempotent INSERT would silently skip NEW
    paid content. (Live evidence: one document's caption resume produced
    index-0/1 collisions on 2026-06-25, repaired by the kg_038 migration.)

    Like the skip-set readers this RAISES on failure: a wrong ``-1`` would cause
    exactly the collision described above, so a resume that cannot read the
    prior max must stop, not guess."""
    derivative_ids = await _derivative_ids(parent_processed_id, derivation_kind)
    if not derivative_ids:
        return -1

    KgChunks = get_db_model("KgChunks")
    chunk_rows = await KgChunks.filter(
        processed_document_id__in=derivative_ids,
        derivation_kind=derivation_kind,
    ).values("chunk_index")
    indexes = [int(r["chunk_index"]) for r in chunk_rows if r.get("chunk_index") is not None]
    return max(indexes) if indexes else -1


async def existing_section_indexes(parent_processed_id: str, derivation_kind: str) -> set[int]:
    """The set of 0-based ``section_index`` values already persisted for this
    derivation (parent + kind). Used by resumable generators to SKIP sections
    whose chunks already exist — so an interrupted, partly-paid run is never
    re-paid on the next attempt.

    Fails closed if prior state cannot be read; otherwise a transient read
    failure could make a paid resume start again from section zero."""
    return await _existing_metadata_ints(parent_processed_id, derivation_kind, key="section_index")


async def existing_page_numbers(parent_processed_id: str, derivation_kind: str) -> set[int]:
    """The set of 1-based ``page_number`` values already persisted for this
    page-keyed derivation (parent + kind). The page analog of
    :func:`existing_section_indexes` — used by the figure-caption generator to
    SKIP pages whose caption chunks already exist (no vision call → no re-spend
    on a resumed run).

    Fails closed if prior state cannot be read; otherwise a transient read
    failure could make a paid resume start again from page one."""
    return await _existing_metadata_ints(parent_processed_id, derivation_kind, key="page_number")


__all__ = [
    "ChunkSpec",
    "DeriveResult",
    "derive_chunk_set",
    "existing_section_indexes",
    "existing_page_numbers",
    "existing_max_chunk_index",
    "count_existing_metadata_ints",
    "token_estimate",
    "format_vector",
]
