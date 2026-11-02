"""High-level ingestion orchestration.

The matrx-graph workflow stubs in ``aidream/graph_actions/rag_actions.py``
call into this module so the end-to-end logic lives in one place and is
testable without invoking the scheduler.

Public entry points:

* ``ingest_source(kind, source_id, field_id=None, *, force=False)`` —
  one-shot resolve → chunk → embed → upsert for a single resource.
  Returns an ``IngestionResult``.
* ``upsert_chunks(...)`` — used by the workflow's ``rag.upsert`` action.

Internals are coroutine-based and use the rag asyncpg pool. Embeddings
are run via the providers in ``embeddings.py``; chunking via
``chunking.py``; source resolution via ``sources.py``.

Hash-based skip:
  Every kg_chunk row carries ``source_hash``. If the resolved source's
  current hash matches the most recent hash already on disk for this
  resource, ingestion short-circuits with ``skipped_unchanged=True``.

Chunk-level reuse (Phase A — Knowledge Graph plan):
  ``rag.kg_chunks.content_sha256`` carries the per-chunk SHA256 of
  content_text. On re-ingest, we compare each NEW chunk's SHA against
  the existing rows for the same (source_kind, source_id, chunker_version).
  Matching chunks reuse the existing row ID (and its embedding row, and
  its future kg_chunk_entities mentions). Only genuinely-changed chunks
  pay for a new embedding. Result: editing 3 words in a 10kB note
  re-embeds 1 chunk of 10, not all 10.

Re-ingest cleanup:
  Chunks whose SHA does NOT match any new chunk are deleted. CASCADE
  removes the orphan embedding rows + kg_chunk_entities + kg_edges
  automatically.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Any

from matrx_orm import ConflictTarget, Now, Value, locked_transaction
from matrx_orm.exceptions import IntegrityError, db_constraint, db_sqlstate

from matrx_rag._ext import get_db_model
from matrx_rag.chunking import (
    CHUNKER_VERSION,
    Chunk,
    chunk_code,
    chunk_text,
)
from matrx_rag.code_chunker import (
    CodeAnalysis,
    analyze_code,
    supported_languages,
)
from matrx_rag.code_map import save_code_map
from matrx_rag.embeddings import (
    default_code_model,
    default_text_model,
    embed,
    orm_model_name_for_table,
    spec_for,
)
from matrx_rag.llm import contextualize_chunk
from matrx_rag.rag_events import RagIngestError
from matrx_rag.sources import (
    ResolvedSource,
    SourceKind,
    UnsupportedMimeError,
    resolve,
)

# THE SYSTEM ORG — `matrx-system`, the platform tenant. `iam.system_orgs` marks
# it `global_readable`, which is exactly what makes a row on it readable by every
# authenticated user unless kept to its owner (db-rules §6e). Global/system
# content is owned by THIS org and never by a NULL `organization_id` (db-rules §2,
# NO NULL ORG — owner ruling 2026-08-21, settled; do not reintroduce a NULL lane).
SYSTEM_ORG_ID = "39c38960-d30c-4840-b0c1-c9960de95582"

# ── FEATURE TOGGLE (code-reviewed, NOT an env var) ───────────────────────
# Anthropic-style contextual retrieval: prefix each child chunk with a 1-2
# sentence context generated against its parent before embedding. Off until
# eval data confirms the lift on our content; flipping it on also bumps
# ``chunker_version`` to v2. Flip here and ship via git — never an env var.
# (Was RAG_CONTEXT_RETRIEVAL.) Tracked in /docs/ENV_FLAG_ERADICATION.md.
CONTEXTUAL_RETRIEVAL: bool = False


def contextual_retrieval_enabled() -> bool:
    return CONTEXTUAL_RETRIEVAL


async def attach_context_prefixes(chunks: list[Chunk], *, concurrency: int = 8) -> None:
    """Anthropic-style contextual retrieval. Generates a 1-2 sentence
    context per child chunk against its parent's text and stashes it on
    ``chunk.metadata['context_prefix']``. Mutates the chunks in place.

    Children whose parent isn't in the same batch (shouldn't happen, but
    defensive) get an empty context — they just embed normally.
    """
    parent_text_by_id: dict[str, str] = {
        c.chunk_id: c.content_text for c in chunks if c.parent_chunk_id is None
    }
    children = [c for c in chunks if c.parent_chunk_id is not None]
    if not children:
        return

    sem = asyncio.Semaphore(concurrency)

    async def one(child: Chunk) -> None:
        async with sem:
            parent_text = parent_text_by_id.get(child.parent_chunk_id or "", "")
            if not parent_text:
                return
            prefix = await contextualize_chunk(parent_text, child.content_text)
            if prefix:
                meta = dict(child.metadata or {})
                meta["context_prefix"] = prefix
                child.metadata = meta

    await asyncio.gather(*(one(c) for c in children), return_exceptions=False)


def _chunk_source_sync(
    source_kind: SourceKind,
    resolved: ResolvedSource,
) -> tuple[list[Chunk], CodeAnalysis | None]:
    """Run parser/tokenizer-heavy source chunking outside the event loop."""
    code_analysis: CodeAnalysis | None = None
    if source_kind == "code_file":
        chunks: list[Chunk] | None = None
        if resolved.language and resolved.language.lower() in supported_languages():
            code_analysis = analyze_code(resolved.text, language=resolved.language)
            if code_analysis is not None:
                chunks = code_analysis.chunks
        if not chunks:
            chunks = chunk_code(resolved.text, language=resolved.language)
        return chunks, code_analysis

    return chunk_text(resolved.text, language=resolved.language), None


async def _chunk_source(
    source_kind: SourceKind,
    resolved: ResolvedSource,
) -> tuple[list[Chunk], CodeAnalysis | None]:
    return await asyncio.to_thread(_chunk_source_sync, source_kind, resolved)


def _embed_text_for(chunk: Chunk) -> str:
    """Compose the actual string we send to the embedding API. When a
    contextual prefix is present, it goes before the chunk content.
    Storage in ``rag.kg_chunks.content_text`` stays UN-prefixed so the
    UI / agent sees the original text.
    """
    if chunk.metadata and chunk.metadata.get("context_prefix"):
        return f"{chunk.metadata['context_prefix']}\n\n{chunk.content_text}"
    return chunk.content_text


@dataclass
class IngestionResult:
    source_kind: str
    source_id: str
    field_id: str | None
    chunks_written: int
    embeddings_written: int
    skipped_unchanged: bool
    embedding_model: str
    error: str | None = None
    # Phase A — Knowledge Graph chunk-level reuse counters. Default to
    # None for back-compat with existing call sites; populated by
    # ``upsert_chunks`` when the SHA-keyed reuse path runs.
    chunks_reused: int | None = None
    chunks_deleted: int | None = None


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------


async def ingest_source(
    source_kind: SourceKind,
    source_id: str,
    field_id: str | None = None,
    *,
    force: bool = False,
    emitter: object | None = None,
    user_id: str | None = None,
    organization_id: str | None = None,
    run_ner: bool = True,
    cleanup: bool = True,
    owner_id: str | None = None,
) -> IngestionResult:
    # ``organization_id`` MUST be supplied by the host (2026-06-03 incident
    # fix). It overrides whatever the underlying source row has so the four
    # KG tables (kg_chunks / kg_entities / kg_chunk_entities / kg_edges) are
    # ALWAYS written with a non-NULL org — the platform invariant the
    # aidream auto-ingest boundary enforces via the personal-org default.
    # Keyword arg is typed Optional only for back-compat during the rollout;
    # a None gets caught with a loud error below. Once every caller has
    # migrated this becomes a required positional kwarg.
    if not organization_id:
        raise ValueError(
            "matrx_rag.ingest_source: organization_id is required. The host "
            "carries the organization from the request boundary or from the "
            "record it is ingesting and passes it here; it is never resolved "
            "or defaulted (THE REQUEST CONTEXT IS CARRIED, NEVER REBUILT). A "
            "NULL organization_id in kg_chunks / kg_entities is the leak class "
            "fixed by the 2026-06-03 incident."
        )

    # PDFs follow a richer pipeline (per-page extract → OCR fallback →
    # LLM cleanup → page-aware chunking) and dispatch to a dedicated
    # entry point. Detect them BEFORE the generic resolver, which would
    # bail on unsupported MIME types.
    if source_kind == "cld_file":
        pdf_result = await _maybe_dispatch_pdf(
            source_id,
            field_id,
            force=force,
            emitter=emitter,
            organization_id=organization_id,
            cleanup=cleanup,
        )
        if pdf_result is not None:
            # Platform fix (2026-06): PDF + image pipelines persist chunks +
            # embeddings but historically returned BEFORE NER ran, leaving
            # cld_file ingest as RAG-only while notes/tasks/projects got
            # RAG + NER. Run NER inline here so auto_ingest('cld_file', ...)
            # behaves like every other source. run_ner_for_source auto-
            # discovers org/owner from the just-persisted rag.kg_chunks rows
            # so matrx-rag doesn't have to join public.cld_files.
            if (
                run_ner
                and pdf_result.error is None
                and ((pdf_result.chunks_written or 0) or (pdf_result.chunks_reused or 0))
            ):
                try:
                    await run_ner_for_source(
                        source_kind="cld_file",
                        source_id=source_id,
                        field_id=field_id,
                        user_id=user_id,
                        organization_id=organization_id,
                    )
                except Exception:
                    # NER failures must NOT fail the ingest — retrieval is
                    # functional without entities. Errors are logged inside
                    # run_ner_for_source / the extractor.
                    pass
            return pdf_result

    try:
        resolved = await resolve(source_kind, source_id, field_id, user_id=user_id)
    except UnsupportedMimeError as exc:
        # Surface as a structured error so the FE/stream can tell the
        # user "PDF processing not wired for this MIME" (or similar)
        # rather than the document hanging at status=pending forever.
        if emitter is not None:
            try:
                await emitter.send_data(
                    RagIngestError(
                        error_type="unsupported_mime",
                        source_kind=exc.source_kind,
                        source_id=exc.source_id,
                        mime_type=exc.mime_type,
                        file_name=exc.file_name,
                        message=str(exc),
                        hint=exc.hint,
                    )
                )
            except Exception:
                pass
        return IngestionResult(
            source_kind=source_kind,
            source_id=source_id,
            field_id=field_id,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model="",
            error=f"unsupported_mime: {exc.mime_type} ({exc.hint})",
        )
    if resolved is None:
        return IngestionResult(
            source_kind=source_kind,
            source_id=source_id,
            field_id=field_id,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model="",
            error="source_not_found",
        )

    if not resolved.text.strip():
        return IngestionResult(
            source_kind=source_kind,
            source_id=resolved.source_id,
            field_id=field_id,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model="",
            error="empty_content",
        )

    # Override the resolved source's organization_id with the host-supplied
    # effective org. The resolved row may carry a NULL (notes/tasks created in
    # personal scope), but the four KG tables MUST always be written with a
    # real org — the personal-org default is the host's responsibility and
    # arrived as the ``organization_id`` parameter above. We patch the
    # dataclass in place so every downstream function (upsert_chunks, embed,
    # _run_ner_for_pending_chunks, materialize_code_graph) sees the effective
    # org without needing its own keyword arg.
    if resolved.organization_id != organization_id:
        resolved = replace(resolved, organization_id=organization_id)

    # Host-supplied chunk-owner override (Shared Knowledge Resources,
    # Decision 3 parity): library ingest of non-file sources (note |
    # transcript | scraped | research) must produce SYSTEM-owned chunks even
    # though the source row itself stays with its contributor. When set, the
    # override wins over the resolved row's owner for every downstream write
    # (chunks, embeddings, NER attribution). The cld_file/PDF path never
    # reaches here — its owner rides the (rehomed) files.files row instead.
    if owner_id is not None and resolved.owner_id != owner_id:
        resolved = replace(resolved, owner_id=owner_id)

    # Pick embedding model: code → voyage-code-3, everything else → openai.
    embedding_model = default_code_model() if source_kind == "code_file" else default_text_model()

    # The resolver names the field it read (a conversation is always ``typed``); change detection
    # and every later stage key on that, never on what the caller passed.
    field_id = resolved.field_id

    if not force:
        existing_hash = await _existing_hash(source_kind, resolved.source_id, field_id)
        if existing_hash and existing_hash == resolved.source_hash:
            # Unchanged content is only truly skippable when every chunk row
            # has its embedding row. Chunks commit BEFORE embeddings (the
            # durable-write design), so a crash between the two leaves rows
            # whose source_hash matches forever — without this probe the
            # early-exit would freeze that gap permanently. A gap (or a probe
            # failure) falls through to the full ingest: SHA-reuse keeps every
            # row and only the missing embeddings are produced and written.
            try:
                gap = await _source_has_embedding_gap(
                    spec_for(embedding_model).table,
                    source_kind,
                    resolved.source_id,
                    field_id,
                )
            except Exception:
                gap = True
            if not gap:
                return IngestionResult(
                    source_kind=source_kind,
                    source_id=resolved.source_id,
                    field_id=field_id,
                    chunks_written=0,
                    embeddings_written=0,
                    skipped_unchanged=True,
                    embedding_model=embedding_model,
                )

    # Chunk — prefer tree-sitter symbol chunking for code when a grammar
    # is available; fall back to line-window for unsupported languages
    # (or when the parser fails). When tree-sitter runs we also keep the
    # ``CodeAnalysis`` (calls / imports) for the post-upsert graph build.
    chunks, code_analysis = await _chunk_source(source_kind, resolved)

    if not chunks:
        return IngestionResult(
            source_kind=source_kind,
            source_id=resolved.source_id,
            field_id=field_id,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model=embedding_model,
            error="no_chunks_produced",
        )

    # Optional contextual retrieval — prepend a 1-2 sentence "where in the
    # document am I" prefix to each child chunk's embedding text. Adds an
    # LLM call per child but typically lifts retrieval recall@k 30%+.
    if contextual_retrieval_enabled():
        await attach_context_prefixes(chunks)

    # Phase A — Knowledge Graph chunk-level reuse.
    #
    # Compute per-chunk SHAs first. Fetch existing chunks for this source.
    # For each new chunk whose SHA matches an existing row, we'll REUSE
    # the row (and its embedding) — embed() is only called for the
    # genuinely-changed chunks.
    new_shas = [_chunk_sha256(_embed_text_for(c)) for c in chunks]
    existing_by_sha = await _existing_chunks_by_sha(
        resolved.source_kind,
        resolved.source_id,
        CHUNKER_VERSION,
    )

    # ── Durable ordering: chunk rows commit FIRST, embeddings follow ──
    # The chunk transaction is short (no provider work inside it, no giant
    # statement); embeddings are then produced and persisted in provider-
    # batch-sized sub-batches, each committed independently — paid embedding
    # work is never held hostage by one long transaction, and a crash loses
    # at most one batch (usually zero net cost, via the embedding cache).
    write_result = await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model=embedding_model,
        embeddings=None,  # deferred — _embed_and_persist_batched below
        new_shas=new_shas,
        existing_by_sha=existing_by_sha,
    )

    chunks_written = write_result.get("chunks_written", 0)
    chunks_reused = write_result.get("chunks_reused", 0)
    chunks_deleted = write_result.get("chunks_deleted", 0)

    # Embedding work list: every chunk that genuinely INSERTed this run…
    landed = set(write_result.get("inserted_chunk_ids", []))
    embed_items: list[tuple[str, str]] = [
        (c.chunk_id, _embed_text_for(c)) for c in chunks if c.chunk_id in landed
    ]

    # …plus SELF-HEAL: reused chunks whose embedding row is MISSING. A chunk
    # row without its embedding (earlier run died between the chunk commit
    # and the embedding writes) is SHA-reused forever and would otherwise
    # stay invisible to vector recall permanently. Probe failure must not
    # fail the ingest — the heal just waits for the next run.
    info = spec_for(embedding_model)
    reused_id_to_idx = {
        existing_by_sha[sha]: i for i, sha in enumerate(new_shas) if sha in existing_by_sha
    }
    try:
        missing = await _unembedded_chunk_ids(info.table, list(reused_id_to_idx))
    except Exception:
        missing = set()
    for cid in missing:
        embed_items.append((cid, _embed_text_for(chunks[reused_id_to_idx[cid]])))

    embeddings_written = await _embed_and_persist_batched(
        embedding_model=embedding_model,
        organization_id=resolved.organization_id,
        owner_id=resolved.owner_id,
        items=embed_items,
    )

    # Phase C — LLM-driven NER over chunks that have NOT yet been successfully
    # NER'd (rag.kg_chunks.ner_extracted_at IS NULL).
    #
    # The cost-reuse contract still holds: a chunk whose NER genuinely SUCCEEDED
    # carries the completion marker and is never re-NER'd — we don't re-pay the
    # LLM cost for unchanged content. But unlike the old "newly-inserted only"
    # gate, the candidate set is the DB truth, so a chunk whose earlier NER pass
    # FAILED (provider error, crash, etc.) — and which is now SHA-reused, never
    # re-inserted — is still picked up and retried. A transient NER failure
    # self-heals on the next ingest instead of leaving the chunk permanently
    # entity-less (the 2026-06-02 incident).
    #
    # We do NOT run NER on code_file sources — code symbols are handled by
    # materialize_code_graph below; running the person/org/phone extractor over
    # source code would produce noise. NER targets natural-language sources.
    # ``run_ner=False`` (the Shared Knowledge Resources "library" ingest profile)
    # also skips it: cross-tenant shared-library content has no tenant scopes or
    # entities to extract, and the post-NER agent fan-out would be wasted cost.
    if run_ner and source_kind != "code_file":
        try:
            await _run_ner_for_pending_chunks(
                resolved=resolved,
                user_id=user_id,
            )
        except Exception:
            # NER failures must NOT roll back the chunk upsert or fail the
            # ingest — retrieval works fine without the entity layer. The
            # error is logged inside _run_ner_for_pending_chunks / ner module.
            pass

    # Materialize the code knowledge graph (kg_entities + kg_edges) for
    # supported languages. Cross-file resolution is best-effort by name.
    if code_analysis is not None:
        try:
            await materialize_code_graph(
                resolved=resolved,
                analysis=code_analysis,
            )
        except Exception:
            # Graph build failures must NOT roll back the chunk upsert;
            # retrieval still works without the graph layer.
            pass

    return IngestionResult(
        source_kind=source_kind,
        source_id=resolved.source_id,
        field_id=field_id,
        chunks_written=chunks_written,
        embeddings_written=embeddings_written,
        chunks_reused=chunks_reused,
        chunks_deleted=chunks_deleted,
        skipped_unchanged=False,
        embedding_model=embedding_model,
    )


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


async def resolve_effective_org(
    organization_id: str | None,
    owner_id: str | None,
) -> str | None:
    """The org a ``kg_chunks`` / embedding row MUST carry — READ, never resolved.

    A chunk inherits the organization of the RECORD it is derived from (the
    processed_document / source). That is the only lawful source: an owner is
    NOT a tenancy, and an organization picked for the owner is the answer to "which
    organization is this user's OWN workspace", never to "this record names
    none" (common-docs/policies/context-is-carried-never-rebuilt.md rule 4).
    Until 2026-09-17 this resolved a per-user assumed organization
    for exactly that case, so chunks of a document ingested in a team
    organization could be written into the owner's personal one — where the
    people who ingested it cannot see them, with nothing raised anywhere.

    Returns ``None`` when the record names no organization; every caller then
    REFUSES, except the declared global-library path, which stamps the SYSTEM
    ORG explicitly (``upsert_chunks(allow_global_org=True)`` — never a NULL,
    db-rules §2). ``owner_id`` is kept only so a refusal can name the owner.

    This is also what closes the 2026-06-03 NULL-org leak class: a NULL org
    hides the row from its owner AND fails closed in the read-access predicate.
    """
    if organization_id is not None:
        return str(organization_id)
    return None


async def upsert_chunks(
    *,
    resolved: ResolvedSource,
    chunks: list[Chunk],
    embedding_model: str,
    embeddings: list[list[float] | None] | None,
    processed_document_id: str | None = None,
    page_id_lookup: dict[int, str] | None = None,
    new_shas: list[str] | None = None,
    existing_by_sha: dict[str, str] | None = None,
    allow_global_org: bool = False,
) -> dict[str, Any]:
    """Persist chunks for the resource with SHA-keyed reuse.

    Phase A — Knowledge Graph chunk-level reuse. The function now performs
    a partial replace:

      * Chunks whose SHA matches an existing row are REUSED — their row
        and embedding stay; we update their metadata (chunk_index,
        page_numbers, etc.) so re-ordering doesn't corrupt the picture.
      * Chunks whose SHA is new are INSERTED + embedded (caller provides
        the embedding vector for these via ``embeddings[i]``; the slot is
        ``None`` for reused chunks).
      * Existing chunks whose SHA is not in ``new_shas`` are DELETED.
        CASCADE removes their embedding rows + kg_chunk_entities + kg_edges.

    Backward compatibility: when ``new_shas`` / ``existing_by_sha`` are
    omitted, the function falls back to the legacy wipe-and-replace path.
    Existing call sites (PDF / image pipelines that build their own
    embedding list) continue to work unchanged.

    Returns a dict::

        {
          "chunks_written":  <int — total chunk rows we ended up with>,
          "chunks_inserted": <int — newly-INSERTED rows this call>,
          "chunks_reused":   <int — rows whose SHA matched and we kept>,
          "chunks_deleted":  <int — stale rows we removed>,
        }

    When ``processed_document_id`` is provided (the canonical case for
    PDFs ingested via System B) the new chunks ALSO populate the FK
    columns on rag.kg_chunks added in migration 0008.

    Durability contract (2026-06-10 redesign):

      * The chunk rows commit in ONE short advisory-locked transaction.
      * Embedding rows are written AFTER that commit, in idempotent
        sub-batches (``ON CONFLICT DO NOTHING``, :data:`EMBED_WRITE_BATCH_SIZE`
        rows per statement) — no statement is ever long enough to need a
        custom command_timeout, and a failure mid-way never rolls back the
        chunks or the batches already written.
      * ``embeddings=None`` defers embedding persistence entirely — the
        caller (``ingest_source``) embeds-and-persists incrementally via
        :func:`_embed_and_persist_batched` after this returns. A chunk row
        without its embedding is self-healing: the next ingest of the source
        detects it via :func:`_unembedded_chunk_ids` and re-embeds just the gap.
    """
    deferred = embeddings is None
    if not deferred and len(chunks) != len(embeddings):
        raise ValueError(f"chunks/embeddings length mismatch: {len(chunks)} vs {len(embeddings)}")

    info = spec_for(embedding_model)

    # NULL-org guard (2026-06-03 leak class; NO NULL ORG since 2026-08-21).
    # Every kg_chunks / embedding row this function writes below keys off
    # resolved.organization_id; a NULL there hides the row from its owner AND
    # fails closed in the read-access predicate. The organization is READ off the
    # source record upstream; DIRECT callers (the rag.upsert workflow node,
    # ad-hoc graph actions) hand us whatever org their inputs carry — and a
    # NULL one is refused below, never replaced with the owner's own workspace.
    #
    # 🚨 `allow_global_org=True` NO LONGER MEANS "keep the NULL" (db-rules §2,
    # owner ruling 2026-08-21). NULL is not a scope, and the lane it used to
    # feed was measurably DEAD: the `organization_id IS NULL` branches in the
    # kg_chunks / embeddings_* RLS policies and in search.py's ACL matched 0 of
    # the 314 live library_doc chunks. It now means what it always intended —
    # this is GLOBAL content, so it belongs to the SYSTEM ORG, which
    # `iam.system_orgs` marks global_readable and which therefore really is
    # readable by every authenticated user (§6e). Every other source must
    # already carry its own organization, so no path here can write a NULL
    # and none of them invents a tenant.
    if resolved.organization_id is None:
        if allow_global_org:
            resolved = replace(resolved, organization_id=SYSTEM_ORG_ID)
        else:
            raise ValueError(
                "upsert_chunks: refusing to write kg_chunks for source "
                f"{resolved.source_id!r} (owner {resolved.owner_id!r}): the "
                "source record names no organization, and a chunk's "
                "organization is READ off the record it comes from — never "
                "resolved from an organization picked for the owner. Give the source "
                "row its organization at the ingest boundary, or pass "
                "allow_global_org=True for genuinely global content (library "
                "docs), which stamps the system org — never a NULL "
                "(db-rules §2, NO NULL ORG)."
            )

    page_lookup = page_id_lookup or {}

    # ── Legacy wipe-and-replace fallback ───────────────────────────
    # When the caller didn't pre-compute SHAs (every existing call site
    # before this commit), behave exactly as before so PDF / image
    # pipelines + the workflow rag.upsert action don't see a behavior
    # change.
    use_sha_reuse = new_shas is not None and existing_by_sha is not None
    if not use_sha_reuse:
        # Compute SHAs ourselves so kg_chunks.content_sha256 stays
        # populated for the legacy callers too (chunk-level dedup index
        # depends on it).
        new_shas = [_chunk_sha256(_embed_text_for(c)) for c in chunks]
        existing_by_sha = {}

    def _chunk_page_columns(c: Chunk) -> tuple[str | None, list[int] | None, list[dict[str, int]] | None]:
        """Compute (primary_page_id, page_numbers, page_spans) for a
        chunk based on its metadata. Falls back gracefully when the
        chunker hasn't recorded page info."""
        meta = c.metadata or {}
        first_page = meta.get("first_page")
        last_page = meta.get("last_page", first_page)
        if first_page is None:
            return None, None, None
        try:
            fp = int(first_page)
            lp = int(last_page) if last_page is not None else fp
        except (TypeError, ValueError):
            return None, None, None
        # 0-based page_index → 1-based page_number for kg_chunks.page_numbers
        page_numbers = list(range(fp + 1, lp + 2))
        # primary_page_id only makes sense when the chunk is on a single page
        primary = page_lookup.get(fp) if fp == lp else None
        spans = [{"page_index": idx, "page_number": idx + 1} for idx in range(fp, lp + 1)]
        return primary, page_numbers, spans

    # ``actually_inserted`` is set inside the transaction to the count of
    # rows the INSERT ... ON CONFLICT DO NOTHING really landed (conflicts
    # skipped don't count). Captured here so the return dict reflects DB
    # truth rather than the optimistic target count.
    actually_inserted = 0
    # ``landed_chunk_ids`` are the chunk ids that genuinely INSERTed this run
    # (i.e. NEW content). The NER pass (Phase C) runs over exactly these — a
    # reused chunk already carries its kg_chunk_entities mentions, so re-NER'ing
    # it would re-pay the LLM cost for unchanged content (the cost-reuse
    # contract). chunk_id is client-allocated, so it equals the kg_chunks row id.
    landed_chunk_ids: list[str] = []

    # Split chunks: reuse vs insert. Recomputed under the advisory lock below
    # when the source's rows changed since the caller's snapshot.
    def _split(snapshot: dict[str, str]) -> tuple[list[int], list[int], set[str], dict[str, str]]:
        reuse: list[int] = []
        insert: list[int] = []
        keep: set[str] = set()
        remap: dict[str, str] = {}
        for i, sha in enumerate(new_shas):
            if sha in snapshot:
                reuse.append(i)
                keep.add(snapshot[sha])
                remap[chunks[i].chunk_id] = snapshot[sha]
            else:
                insert.append(i)
                remap[chunks[i].chunk_id] = chunks[i].chunk_id
        return reuse, insert, keep, remap

    reuse_indexes, insert_indexes, keep_existing_ids, chunk_id_remap = _split(existing_by_sha)

    # parent_chunk_id remap (FK kg_chunks_parent_chunk_id_fkey).
    # chunk_id / parent_chunk_id are freshly-allocated uuid4s every run, and
    # parent_chunk_id references a sibling's id within THIS batch. When a
    # parent chunk's content is unchanged it gets SHA-reused — its row keeps
    # its OLD db id and the freshly-generated uuid is never written. Any child
    # still pointing at that new uuid would dangle. We therefore rewrite every
    # parent_chunk_id through this map: a reused chunk → its existing db id; an
    # inserted chunk → its own (about-to-be-written) id. A parent id not in the
    # batch falls through unchanged (defensive — the chunkers always emit the
    # parent in the same batch). ``chunk_id_remap`` comes from ``_split`` above.

    def _effective_parent_id(c: Chunk) -> str | None:
        pid = c.parent_chunk_id
        if pid is None:
            return None
        return chunk_id_remap.get(pid, pid)

    # Verify embedding slots match expectations — only inserted chunks
    # need vectors. (Reused chunks' vectors live in the embeddings_*
    # table already; they're never re-written.) Deferred mode skips this:
    # the caller embeds-and-persists after the chunk commit.
    def _verify_insert_vectors() -> None:
        if deferred:
            return
        for i in insert_indexes:
            if embeddings[i] is None:
                raise ValueError(
                    f"upsert_chunks: chunk index {i} is being INSERTED but its "
                    f"embedding vector is None. Caller must supply vectors for "
                    f"all non-reused chunks."
                )

    _verify_insert_vectors()

    KgChunks = get_db_model("KgChunks")

    # matrx_orm.transaction() + advisory_xact_lock() — the ORM's own advisory-
    # lock primitive (packages/matrx-orm/matrx_orm/core/transaction.py). Every
    # ORM write below (delete_where / bulk_insert_ignore / bulk_update_by_pk)
    # rides the SAME connection automatically via the ContextVar
    # AsyncDatabaseManager.execute_write installs — no explicit connection=
    # plumbing needed, exactly like a hand-held asyncpg conn used to require.
    async with locked_transaction(
        f"{resolved.source_kind}:{resolved.source_id}:{resolved.field_id or ''}",
    ):
        # B.0 — concurrent-ingest race guard (FOUND_DEFECTS 2026-06-02,
        # matrx-feedback 695983de). Two simultaneous re-ingest runs for
        # the same source used to interleave their wipe-and-replace
        # transactions and collide on the unique index
        # kg_chunks_content_sha_idx → 23505. A transaction-scoped
        # advisory lock keyed on (source_kind, source_id) serializes the
        # two runs so the second waits for the first to commit, then sees
        # the rows it wrote (SHA-reuse path skips them; legacy wipe path
        # re-wipes them). The lock is released automatically at COMMIT/
        # ROLLBACK — no unlock bookkeeping, no leak on cancellation.
        #
        # We pair it with ON CONFLICT DO NOTHING on the chunk INSERT so a
        # caller that bypasses this function (or a future code path) still
        # can't raise 23505 — defense-in-depth, the class of failure is
        # structurally gone, not patched at one site.

        # B.1 — STALE-SNAPSHOT GUARD (2026-10-11). The caller read
        # ``existing_by_sha`` BEFORE this lock. Two ingests of one source a
        # moment apart (a save burst) both read the same snapshot; the first
        # commits its new chunk, the second then deleted only the rows in ITS
        # snapshot and left the first run's chunk alive beside its own — the
        # OLD text stayed searchable next to the new (live: note
        # 0a441c86…, chunk_index 0 twice). Re-read under the lock and re-split,
        # so the delete below covers every row of the source that this write
        # does not keep. The caller's dict is updated in place so its
        # post-write reuse bookkeeping sees the same truth.
        if use_sha_reuse:
            fresh = await _existing_chunks_by_sha(
                resolved.source_kind, resolved.source_id, CHUNKER_VERSION
            )
            if fresh != existing_by_sha:
                existing_by_sha.clear()
                existing_by_sha.update(fresh)
                reuse_indexes, insert_indexes, keep_existing_ids, chunk_id_remap = _split(
                    existing_by_sha
                )
                # RACE, not a caller bug: a chunk the caller saw as REUSED (so it
                # sent no vector) may now need an INSERT because the row it would
                # reuse vanished under the lock. Never raise for it and never
                # embed under the lock — its vector is fetched after the commit,
                # before any embedding row is written (below).

        # 1. Delete stale chunks (existing rows whose SHA didn't survive
        #    this re-ingest). CASCADE handles the embeddings + entity
        #    mentions + edges.
        deleted_count = 0
        if use_sha_reuse:
            # Reuse mode — delete exactly the existing-but-not-kept rows.
            stale_ids = [eid for eid in existing_by_sha.values() if eid not in keep_existing_ids]
            if stale_ids:
                # hard-delete-ok: derived search chunks, rebuilt on re-ingest of their source
                deleted_count = await KgChunks.delete_where(id__in=stale_ids)
        else:
            # Legacy mode — full wipe. Backward compat. Count is the
            # total rows that existed before the wipe. `field_id` is
            # nullable — IS NOT DISTINCT FROM parity via an explicit
            # isnull branch (a bare `field_id=None` filter would render
            # `field_id IS NULL`, which happens to match here too, but the
            # explicit branch keeps the intent obvious).
            if resolved.field_id is None:
                # hard-delete-ok: derived search chunks, rebuilt on re-ingest of their source
                deleted_count = await KgChunks.delete_where(
                    source_kind=resolved.source_kind,
                    source_id=resolved.source_id,
                    field_id__isnull=True,
                )
            else:
                # hard-delete-ok: derived search chunks, rebuilt on re-ingest of their source
                deleted_count = await KgChunks.delete_where(
                    source_kind=resolved.source_kind,
                    source_id=resolved.source_id,
                    field_id=resolved.field_id,
                )

        # Pre-compute the page-column tuple per chunk so the row builders
        # below don't recompute it.
        page_cols: list[tuple[str | None, list[int] | None, str | None]] = [
            _chunk_page_columns(c) for c in chunks
        ]

        # 2. Insert new chunks. Reuse mode → only the misses. Legacy
        #    mode → every chunk (because we wiped above).
        insert_targets = insert_indexes if use_sha_reuse else list(range(len(chunks)))

        if insert_targets:
            # ON CONFLICT DO NOTHING on the unique index
            # (source_kind, source_id, content_sha256, chunker_version):
            # under the advisory lock above this can only fire when an
            # equal-content row already exists (a concurrent run that
            # committed first, or a stale row the wipe didn't remove).
            # `returning="id"` captures the genuinely-inserted ids so the
            # embedding INSERT below only fires for rows that actually
            # landed — a skipped chunk's embedding would otherwise orphan.
            # A plain multi-row VALUES insert (not unnest()) sidesteps the
            # jagged-array problem the old unnest() write had to work
            # around for `page_numbers` (a per-row array column) — each
            # row's list binds natively to its own `int[]` placeholder.
            insert_rows = [
                {
                    "id": chunks[i].chunk_id,
                    "organization_id": resolved.organization_id,
                    "created_by": resolved.owner_id,
                    "source_kind": resolved.source_kind,
                    "source_id": resolved.source_id,
                    "field_id": resolved.field_id,
                    "parent_chunk_id": _effective_parent_id(chunks[i]),
                    "chunk_index": chunks[i].chunk_index,
                    "chunk_kind": chunks[i].chunk_kind,
                    "content_text": chunks[i].content_text,
                    "content_sha256": new_shas[i],
                    "token_count": chunks[i].token_count,
                    "language": chunks[i].language,
                    "mime_type": resolved.mime_type,
                    "source_hash": resolved.source_hash,
                    "chunker_name": "v1",
                    "chunker_version": CHUNKER_VERSION,
                    "metadata": _merge_metadata(resolved.metadata, chunks[i].metadata or {}),
                    "processed_document_id": processed_document_id,
                    "primary_page_id": page_cols[i][0],
                    "page_numbers": page_cols[i][1],
                    "page_spans": page_cols[i][2],
                    "token_estimate": chunks[i].token_count,
                }
                for i in insert_targets
            ]
            landed_ids_raw = await KgChunks.bulk_insert_ignore(
                insert_rows,
                # Partial since 2026-09-20 (`WHERE deleted_at IS NULL`), so the
                # conflict target must carry the same predicate — a bare column
                # list can no longer infer kg_chunks_content_sha_idx and every
                # chunk insert would raise 42P10.
                on_conflict=ConflictTarget.partial(
                    ["source_kind", "source_id", "content_sha256", "chunker_version"],
                    where_is_null=("deleted_at",),
                ),
                returning="id",
            )

            # Only chunks that actually landed get an embedding row. A
            # conflict-skipped chunk's embedding would orphan, so we key
            # the embedding work off the RETURNING set. The write itself
            # happens AFTER this transaction commits — see below.
            landed_ids = {str(v) for v in landed_ids_raw}
            actually_inserted = len(landed_ids)
            landed_chunk_ids = list(landed_ids)

        # 3. For reused chunks, refresh their metadata (chunk_index,
        #    page_numbers, etc.) so re-ordering / page-shift produces
        #    correct downstream behavior. content_text + sha + embedding
        #    are unchanged. deleted_at is CLEARED: a rebuild that re-affirms
        #    a previously-trashed chunk's content re-activates it — otherwise
        #    soft-delete → reprocess reports success but stays invisible.
        if use_sha_reuse and reuse_indexes:
            update_rows = [
                {
                    "id": existing_by_sha[new_shas[i]],
                    "chunk_index": chunks[i].chunk_index,
                    "parent_chunk_id": _effective_parent_id(chunks[i]),
                    "metadata": _merge_metadata(resolved.metadata, chunks[i].metadata or {}),
                    "page_numbers": page_cols[i][1],
                    "page_spans": page_cols[i][2],
                    "source_hash": resolved.source_hash,
                }
                for i in reuse_indexes
            ]
            # bulk_update_by_pk — set-based UPDATE ... FROM (VALUES ...), one
            # round trip for the whole batch (same shape as the executemany
            # it replaces, minus the N separate Execute messages).
            await KgChunks.bulk_update_by_pk(
                update_rows,
                casts={
                    "id": "uuid",
                    "chunk_index": "integer",
                    "parent_chunk_id": "uuid",
                    "metadata": "jsonb",
                    "page_numbers": "int[]",
                    "page_spans": "jsonb",
                },
                set_expressions={"updated_at": Now(), "deleted_at": Value(None)},
            )

    # ── Embedding writes — AFTER the chunk transaction committed ──
    # Idempotent sub-batches (ON CONFLICT DO NOTHING), each one bulk-insert
    # statement small enough to finish well inside the pool's default
    # command_timeout. Chunks are already durable: a failure here never rolls
    # them back, and the gap self-heals on the next ingest (see
    # _unembedded_chunk_ids). Deferred mode (embeddings=None) skips this —
    # ingest_source persists-as-it-embeds instead. Deliberately OUTSIDE the
    # advisory-locked transaction() block above (a separate connection/
    # statement per batch) — the embedding write's atomicity is per-batch,
    # never coupled to the chunk write's.
    if not deferred and landed_chunk_ids:
        id_to_target = {chunks[i].chunk_id: i for i in insert_targets}
        missing = [id_to_target[cid] for cid in landed_chunk_ids if embeddings[id_to_target[cid]] is None]
        if missing:
            # The under-lock re-split turned caller-reused chunks into inserts:
            # embed exactly those through the one embedding path (the cache makes
            # a recent identical text free), so no embedding row lacks a vector.
            fetched = await embed(
                embedding_model,
                [_embed_text_for(chunks[i]) for i in missing],
                input_type="document",
                organization_id=resolved.organization_id,
            )
            embeddings = list(embeddings)
            for i, vector in zip(missing, fetched, strict=True):
                embeddings[i] = vector
        embedding_payloads = await _format_embedding_payloads(
            landed_chunk_ids,
            [embeddings[id_to_target[cid]] for cid in landed_chunk_ids],
            organization_id=resolved.organization_id,
            owner_id=resolved.owner_id,
        )
        await _write_embedding_rows(info.table, embedding_payloads)

    return {
        "chunks_written": len(chunks),
        "chunks_inserted": actually_inserted,
        "chunks_reused": len(reuse_indexes),
        "chunks_deleted": deleted_count,
        # NEW chunk ids that landed this run — the NER pass keys off these so
        # reused chunks are never re-NER'd (cost-reuse contract).
        "inserted_chunk_ids": landed_chunk_ids,
    }


# ---------------------------------------------------------------------------
# Helpers — durable embedding persistence
# ---------------------------------------------------------------------------

# Rows per embedding-INSERT statement. Sized so one set-based unnest() write
# (≈20 KB of vector text per 1536-dim row → ~4 MB/statement) always finishes
# well inside the pool's default command_timeout — no per-statement timeout
# override, ever. Config-not-env-var per CLAUDE.md: changing it is a code push.
EMBED_WRITE_BATCH_SIZE = 200


async def _write_embedding_rows(
    embedding_table: str,
    payloads: list[tuple[str, str | None, str | None, str]],
    batch_size: int | None = None,
) -> int:
    """Write ``(chunk_id, organization_id, owner_id, vector_literal)`` rows in
    idempotent sub-batches.

    Each batch is ONE multi-row ``bulk_insert_ignore`` statement (its own
    implicit transaction); the PK-targeted ``ON CONFLICT ... DO NOTHING``
    makes retries and concurrent writers safe. Never wraps the batches in an
    outer transaction — committed batches survive a later failure (paid
    embedding work is never rolled back).

    ``embedding_table`` names one of a CLOSED, small set of per-model
    embedding tables (every registered ``EmbeddingSpec.table``) — not a truly
    dynamic/arbitrary identifier — so it's resolved to a real matrx-orm
    ``Model`` class via ``orm_model_name_for_table`` (never interpolated into
    SQL text) and written through the normal ORM bulk-write path, exactly like
    ``stages.py``'s ``emb_model.bulk_upsert(...)`` for the same table family.
    """
    if batch_size is None:
        batch_size = EMBED_WRITE_BATCH_SIZE  # read at call time (testable)

    model_name = orm_model_name_for_table(embedding_table)
    if model_name is None:
        raise ValueError(
            f"_write_embedding_rows: unrecognized embedding table {embedding_table!r} — "
            f"set orm_model on its EmbeddingSpec before writing to it."
        )
    Emb = get_db_model(model_name)

    written = 0
    for start in range(0, len(payloads), batch_size):
        batch = payloads[start : start + batch_size]
        try:
            await _insert_embedding_batch(Emb, batch)
        except IntegrityError as exc:
            # A newer save of the same source replaced these chunks between this run's chunk
            # commit and its embedding write (the embedding write is deliberately outside the
            # chunk lock). The vanished chunks need no embedding — the newer run embeds its own.
            # Write the ones that still exist; never fail the run for the others (audit
            # 2026-09-26: 54 note runs recorded as errors for exactly this).
            # The vanished-chunk case is the chunk_id foreign key (23503), by code and name.
            if db_sqlstate(exc) != "23503" or "chunk_id" not in (db_constraint(exc) or ""):
                raise
            KgChunks = get_db_model("KgChunks")
            live = {
                str(r["id"])
                for r in await KgChunks.filter(id__in=[p[0] for p in batch]).values("id")
            }
            kept = [p for p in batch if str(p[0]) in live]
            import logging as _logging

            _logging.getLogger(__name__).info(
                "_write_embedding_rows: %d of %d chunk(s) were replaced by a newer save before their "
                "embedding landed; embedding the %d that remain",
                len(batch) - len(kept),
                len(batch),
                len(kept),
            )
            if kept:
                await _insert_embedding_batch(Emb, kept)
            batch = kept
        written += len(batch)
    return written


async def _insert_embedding_batch(
    Emb: Any, batch: list[tuple[str, str | None, str | None, str]]
) -> None:
    await Emb.bulk_insert_ignore(
        [
            {"chunk_id": p[0], "organization_id": p[1], "owner_id": p[2], "embedding": p[3]}
            for p in batch
        ],
        on_conflict=["chunk_id"],
    )


async def _unembedded_chunk_ids(embedding_table: str, chunk_ids: list[str]) -> set[str]:
    """Return the subset of *chunk_ids* that have NO row in *embedding_table*.

    The self-heal probe: a chunk row without its embedding means an earlier
    run died between the chunk commit and the embedding writes. Those chunks
    are SHA-reused forever (never re-inserted), so without this check they
    would stay invisible to vector recall permanently.
    """
    if not chunk_ids:
        return set()
    model_name = orm_model_name_for_table(embedding_table)
    if model_name is None:
        return set()
    Emb = get_db_model(model_name)
    rows = await Emb.filter(chunk_id__in=chunk_ids).values("chunk_id")
    have = {str(r["chunk_id"]) for r in rows}
    return {cid for cid in chunk_ids if cid not in have}


async def _source_has_embedding_gap(
    embedding_table: str,
    source_kind: str,
    source_id: str,
    field_id: str | None,
) -> bool:
    """True when any current-chunker-version chunk of this source lacks its
    embedding row. Guards the ``skipped_unchanged`` early-exit in
    ``ingest_source`` — see the comment there. Two indexed queries."""
    KgChunks = get_db_model("KgChunks")
    filters: dict[str, Any] = {
        "source_kind": source_kind,
        "source_id": source_id,
        "chunker_version": CHUNKER_VERSION,
    }
    if field_id is None:
        filters["field_id__isnull"] = True
    else:
        filters["field_id"] = field_id
    rows = await KgChunks.filter(**filters).values("id")
    ids = [str(r["id"]) for r in rows]
    if not ids:
        return False
    return bool(await _unembedded_chunk_ids(embedding_table, ids))


async def _embed_and_persist_batched(
    *,
    embedding_model: str,
    organization_id: str | None,
    owner_id: str | None,
    items: list[tuple[str, str]],
) -> int:
    """Persist-as-you-embed: one provider batch → one committed write.

    *items* is ``(chunk_id, embed_text)``. Sub-batch size follows the
    provider's own batch size (``spec.batch_size``) so every paid provider
    call is persisted before the next one starts — a crash loses at most one
    batch of embeddings, and the embedding cache usually makes even that
    re-pay free. Returns rows written.
    """
    if not items:
        return 0
    info = spec_for(embedding_model)
    batch_size = max(1, int(getattr(info, "batch_size", EMBED_WRITE_BATCH_SIZE)))
    written = 0
    for start in range(0, len(items), batch_size):
        sub = items[start : start + batch_size]
        vectors = await embed(
            embedding_model,
            [text for _, text in sub],
            input_type="document",
            organization_id=organization_id,
        )
        payloads = await _format_embedding_payloads(
            [cid for cid, _ in sub],
            vectors,
            organization_id=organization_id,
            owner_id=owner_id,
        )
        written += await _write_embedding_rows(info.table, payloads)
    return written


# ---------------------------------------------------------------------------
# Helpers — chunk-level SHA reuse
# ---------------------------------------------------------------------------


def _chunk_sha256(text: str) -> str:
    """Hex-encoded SHA256 of a chunk's content_text. Matches the
    server-side ``encode(sha256(convert_to(content_text, 'UTF8')), 'hex')``
    used by the kg_001 migration backfill.
    """
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


async def _existing_chunks_by_sha(
    source_kind: str,
    source_id: str,
    chunker_version: str,
) -> dict[str, str]:
    """Return ``{content_sha256: chunk_id_str}`` for all existing chunks
    belonging to this source under the current chunker_version. Used by
    ``ingest_source`` to decide which chunks to reuse vs re-embed.

    Empty dict means no existing rows (first ingest of this source).
    """
    KgChunks = get_db_model("KgChunks")
    rows = await KgChunks.filter(
        source_kind=source_kind,
        source_id=source_id,
        chunker_version=chunker_version,
        content_sha256__isnull=False,
    ).values("content_sha256", "id")
    out: dict[str, str] = {}
    for r in rows:
        # If the same SHA appears multiple times (shouldn't, given the
        # unique index in kg_001), keep the first — the others are
        # leftover duplicates the migration didn't catch.
        if r["content_sha256"] not in out:
            out[r["content_sha256"]] = str(r["id"])
    return out


def _parse_delete_count(execute_result: object) -> int:
    """asyncpg returns 'DELETE N' from execute() — extract N."""
    try:
        return int(str(execute_result).split()[-1])
    except (ValueError, IndexError):
        return 0


@dataclass
class NerRunOutcome:
    """What one NER pass over a source did — so a failure is never read as "nothing found".

    ``state``: ``done`` (every pending chunk extracted, or none pending), ``failed`` (no chunk
    could be extracted — ``message`` says why in a sentence), or ``partial`` (some chunks failed;
    they retry on the next pass). ``extract_entities`` never raises, so before this the caller had
    only a silent ``None`` and a provider outage looked exactly like a document with no entities.
    """

    state: str = "done"
    message: str = ""
    attempted: int = 0
    succeeded: int = 0
    extractor_failures: int = 0


def _ner_failure_sentence(errors: list[str]) -> str:
    """The first recorded error as a sentence a person can read (chunk ids and prefixes dropped)."""
    import re as _re

    first = next((e for e in errors if e), "")
    text = _re.sub(r"^[0-9a-f-]{36}:\s*", "", first)
    text = _re.sub(r"^(extractor_error|persist_error|finisher_failed):\s*", "", text)
    text = (
        _re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text).strip()
        or "the entity extractor returned an error"
    )
    return (text[:300].rstrip(".") + ".") if text else "The entity extractor returned an error."


# One NER run per source per process at a time. Two runs over the same source
# (a save that notified twice, the content-processing orchestrator racing the
# save hook) both read the same ``ner_extracted_at IS NULL`` chunks, paid the
# extractor twice and deadlocked on each other's mention writes (live 40P01,
# 2026-10-01 22:29Z). The second run now WAITS, then re-reads the pending set
# and finds the chunks the first run stamped. Process-scoped on purpose: a
# Postgres advisory lock cannot span this run — a session lock is not a lock
# through the transaction pooler (matrx_orm.advisory_lock's affinity warning),
# and an xact lock would have to hold one transaction open across the extractor
# and tier C's own parallel transactions, past the server's 2-min idle and
# 10-min transaction timeouts. Cross-process exclusion needs a durable per-chunk
# claim (tracked as a follow-up). key -> (lock, waiters).
_NER_SOURCE_LOCKS: dict[tuple[str, str, str], list[Any]] = {}


async def run_ner_for_source(
    *,
    source_kind: str,
    source_id: str,
    field_id: str | None,
    organization_id: str,
    owner_id: str | None = None,
    user_id: str | None = None,
) -> NerRunOutcome:
    """Run NER over the source's pending chunks; see :func:`_run_ner_for_source_locked`.

    Serialized per ``(source_kind, source_id, field_id)`` (``_NER_SOURCE_LOCKS``).
    """
    key = (str(source_kind), str(source_id), str(field_id or ""))
    entry = _NER_SOURCE_LOCKS.get(key)
    if entry is None:
        entry = _NER_SOURCE_LOCKS[key] = [asyncio.Lock(), 0]
    entry[1] += 1
    try:
        async with entry[0]:
            return await _run_ner_for_source_locked(
                source_kind=source_kind,
                source_id=source_id,
                field_id=field_id,
                organization_id=organization_id,
                owner_id=owner_id,
                user_id=user_id,
            )
    finally:
        entry[1] -= 1
        if entry[1] == 0 and _NER_SOURCE_LOCKS.get(key) is entry:
            del _NER_SOURCE_LOCKS[key]


async def _run_ner_for_source_locked(
    *,
    source_kind: str,
    source_id: str,
    field_id: str | None,
    organization_id: str,
    owner_id: str | None = None,
    user_id: str | None = None,
) -> NerRunOutcome:
    """Run NER over every chunk of (source_kind, source_id, field_id) whose
    ``ner_extracted_at`` marker is still NULL — the DB-truth candidate set so
    newly-inserted AND SHA-reused-but-unextracted chunks are both covered.

    This is the canonical entry point that every ingest pipeline (note / text /
    PDF / image) calls AFTER persisting its chunks so RAG + NER stay paired.
    Code sources should NOT call this — symbols are handled by
    ``materialize_code_graph``; running the person/org/phone extractor over
    source code produces noise.

    ``organization_id`` is REQUIRED and is the tenant this NER pass runs in.
    Until 2026-09-17 it was optional and, when absent, this function read the
    organization off ``rows[0]`` — a library choosing a tenant from whichever
    chunk row came back first. The caller carries the organization (the host
    entry points all have it: ``ingest_source`` refuses without one and
    overrides the resolved source's value with it), and the chunk rows are
    VERIFIED against it below rather than trusted by comment. ``owner_id`` is
    still auto-discovered from the chunk rows, so the PDF / image dispatch path
    doesn't have to thread the cld_files row's owner all the way through (and
    matrx-rag stays standalone — no ``files.files`` join required).

    Chunks that succeed get ``ner_extracted_at`` (and ``metadata.ner``) stamped
    by ``ner.persist_chunk_entities`` so they're never re-NER'd; chunks that
    error stay NULL and retry on the next ingest. The
    extractor is host-injected; with none wired this is a clean no-op.
    """
    from matrx_rag.ner import NerChunkInput, extract_entities

    organization_id = str(organization_id or "").strip()
    if not organization_id:
        raise ValueError(
            "run_ner_for_source: organization_id is required. NER writes "
            "kg_entities rows into a tenant; the caller carries the "
            "organization (from the request boundary or the record it is "
            "ingesting) and this never picks one off a chunk row."
        )

    KgChunks = get_db_model("KgChunks")
    qb = KgChunks.filter(
        source_kind=source_kind,
        source_id=source_id,
        ner_extracted_at__isnull=True,
    )
    # Raw SQL used ``field_id IS NOT DISTINCT FROM $3`` — branch in Python so
    # a NULL field_id matches NULL rows instead of matching nothing.
    if field_id is None:
        qb = qb.filter(field_id__isnull=True)
    else:
        qb = qb.filter(field_id=field_id)
    rows = await qb.values("id", "content_text", "organization_id", "created_by")
    if not rows:
        return NerRunOutcome(state="done")

    # Skip NON-LEAF (parent) chunks. The hierarchical prose chunker emits
    # ~1500-token parents over ~300-token children; a parent's text is fully
    # covered by its children, which are each NER'd. Extracting the parent too
    # is redundant (the same text twice) AND the ~1500-token parent overflows
    # GLiNER2's much smaller window — the silent document-gutting class. So we
    # NER ONLY leaf chunks = chunks that are not the parent of any other chunk
    # in this source. Flat single-level sources (PDF/image/agent-json) have no
    # children, so their parent-less chunks ARE leaves and stay NER'd.
    #
    # Raw-SQL consumers mirror this exact rule via a NOT EXISTS parent
    # predicate — keep them in sync: scripts/backfill_kg.py (re-NER selection),
    # aidream/api/routers/kg_cost.py + aidream/services/auto_ingest/
    # heavy_hitters.py (coverage denominators).
    parent_qb = KgChunks.filter(
        source_kind=source_kind,
        source_id=source_id,
        parent_chunk_id__isnull=False,
    )
    if field_id is None:
        parent_qb = parent_qb.filter(field_id__isnull=True)
    else:
        parent_qb = parent_qb.filter(field_id=field_id)
    non_leaf_ids = {
        str(r["parent_chunk_id"])
        for r in await parent_qb.values("parent_chunk_id")
        if r["parent_chunk_id"] is not None
    }
    if non_leaf_ids:
        rows = [r for r in rows if str(r["id"]) not in non_leaf_ids]
        if not rows:
            return NerRunOutcome(state="done")

    # The organization came from the CALLER; the rows must agree with it. A
    # mixed or foreign chunk row means the source's chunks were written across
    # tenants, which is a defect to surface — never a tenant to pick.
    row_orgs = {str(r["organization_id"]) for r in rows if r["organization_id"] is not None}
    foreign = row_orgs - {organization_id}
    if foreign:
        raise ValueError(
            f"run_ner_for_source: chunks for {source_kind}/{source_id} carry "
            f"organization(s) {sorted(foreign)} but this pass was given "
            f"{organization_id}. A source's chunks belong to ONE tenant; "
            "extracting across a mix would write entities into the wrong "
            "organization. Fix the chunk rows or the caller's organization."
        )

    # owner is auto-discovered from the chunk rows so the PDF/image dispatch
    # path doesn't need to thread it through. The chunks were just persisted by
    # upsert_chunks with created_by = the authoritative source.owner_id.
    if owner_id is None:
        first_owner = rows[0]["created_by"]
        owner_id = str(first_owner) if first_owner is not None else None

    effective_user = user_id or owner_id
    if not effective_user:
        return NerRunOutcome(
            state="failed",
            message="No person owns these chunks, so entities could not be attributed to anyone.",
            attempted=len(rows),
        )

    ner_inputs = [
        NerChunkInput(chunk_id=str(r["id"]), content_text=r["content_text"]) for r in rows
    ]

    ner_result = await extract_entities(
        ner_inputs,
        organization_id=organization_id,
        user_id=effective_user,
        source_kind=source_kind,
        source_id=source_id,
    )

    # The completion marker (``ner_extracted_at`` + ``metadata.ner``) is stamped
    # by ``ner.persist_chunk_entities`` for exactly the chunks that landed.

    attempted = len(rows)
    succeeded = len(ner_result.succeeded_chunk_ids)
    if ner_result.skipped_reason == "no_extractor":
        return NerRunOutcome(
            state="failed",
            message="No entity extractor is configured on this server, so entities were not extracted.",
            attempted=attempted,
        )
    if attempted and not succeeded and (ner_result.errors or ner_result.extractor_failures):
        return NerRunOutcome(
            state="failed",
            message=_ner_failure_sentence(ner_result.errors),
            attempted=attempted,
            extractor_failures=ner_result.extractor_failures,
        )
    return NerRunOutcome(
        state="partial" if succeeded < attempted and ner_result.errors else "done",
        message=_ner_failure_sentence(ner_result.errors)
        if succeeded < attempted and ner_result.errors
        else "",
        attempted=attempted,
        succeeded=succeeded,
        extractor_failures=ner_result.extractor_failures,
    )


async def _run_ner_for_pending_chunks(
    *,
    resolved: ResolvedSource,
    user_id: str | None,
) -> None:
    """Back-compat wrapper for the original ResolvedSource-based call site.
    Forwards to ``run_ner_for_source`` which is the new canonical entry point.
    """
    await run_ner_for_source(
        source_kind=resolved.source_kind,
        source_id=resolved.source_id,
        field_id=resolved.field_id,
        organization_id=resolved.organization_id,
        owner_id=resolved.owner_id,
        user_id=user_id,
    )


async def materialize_code_graph(
    *,
    resolved: ResolvedSource,
    analysis: CodeAnalysis,
) -> None:
    """Populate rag.kg_entities and rag.kg_edges from a CodeAnalysis.

    A thin adapter: it turns the Python ingest's ResolvedSource + CodeAnalysis into the plain data
    ``matrx_rag.code_map.save_code_map`` takes — the ONE write path for a code file's map (see that
    module for what is written). The source's owner is the person the map is built for. Deleted with
    ``ingest_source``.
    """
    if not analysis or (not analysis.calls and not analysis.imports):
        return
    metadata = resolved.metadata or {}
    symbols = [
        {
            "chunk_id": c.chunk_id,
            "name": (c.metadata or {}).get("symbol_name"),
            "kind": (c.metadata or {}).get("symbol_kind"),
            "parent_symbol": (c.metadata or {}).get("parent_symbol"),
            "line_start": (c.metadata or {}).get("line_start"),
            "line_end": (c.metadata or {}).get("line_end"),
        }
        for c in analysis.chunks
        if c.metadata and c.metadata.get("symbol_name") and c.chunk_kind in ("code_symbol", "code_class")
    ]
    await save_code_map(
        organization_id=resolved.organization_id or "",
        created_by=resolved.owner_id or None,
        source_kind=resolved.source_kind,
        source_id=resolved.source_id,
        file_path=str(metadata.get("path") or metadata.get("file_path") or resolved.source_id),
        language=resolved.language,
        symbols=symbols,
        calls=[
            {
                "caller_chunk_id": c.caller_chunk_id,
                "callee_name": c.callee_name,
                "callee_chunk_id": c.callee_chunk_id,
                "line": c.line,
            }
            for c in analysis.calls
        ],
        imports=[{"module": i.module, "names": i.names, "line": i.line} for i in analysis.imports],
    )


async def _maybe_dispatch_pdf(
    source_id: str,
    field_id: str | None,
    *,
    force: bool,
    emitter: object | None = None,
    organization_id: str | None = None,
    cleanup: bool = True,
) -> IngestionResult | None:
    """If this cld_files row is a PDF or an image, route to the dedicated
    pipeline. Otherwise return None so the caller falls through to the
    generic text resolver path.

    ``organization_id`` is the host-supplied effective org (the cld_files
    row's own ``organization_id`` is overridden by this for the same
    "never write NULL to kg_chunks" reason ingest_source overrides
    ``resolved.organization_id``).
    """
    # Host-owned files.files row (post-2026-cutover home of the legacy
    # public.cld_files table — see matrx_rag/file_acl_sql.py FILES_TABLE).
    # Resolved via get_db_model("Files") — the SAME name every other
    # cld_file reader in this package already uses (sources.py, data_stores.py,
    # library.py, image_pipeline.py, processed_doc_lookup.py, stages.py); the
    # host registers this class in matrx_orm.model_registry at startup
    # (rule 4, matrx-rag/CLAUDE.md: "public.* names resolve to the HOST's
    # classes").
    Files = get_db_model("Files")
    cld_rows = await Files.filter(id=source_id, deleted_at__isnull=True).values(
        "id", "created_by", "organization_id", "file_name", "mime_type", "storage_uri", "metadata"
    )
    if not cld_rows:
        return None
    _raw = cld_rows[0]
    row: dict[str, Any] = {
        "id": str(_raw["id"]),
        # created_by is the current column name (was owner_id pre-cutover) —
        # keep the local dict's key as owner_id so every downstream read below
        # is unchanged.
        "owner_id": str(_raw["created_by"]) if _raw["created_by"] is not None else None,
        "organization_id": str(_raw["organization_id"])
        if _raw["organization_id"] is not None
        else None,
        "file_name": _raw["file_name"],
        "mime_type": _raw["mime_type"],
        "storage_uri": _raw["storage_uri"],
        "metadata": _raw["metadata"],
    }
    from matrx_rag.sources import classify_binary_pipeline, normalize_mime

    mime_type = normalize_mime(row["mime_type"])  # params stripped: 'application/pdf;x=y' is a PDF

    # ONE classifier, shared with sources._resolve_cld_file — see
    # sources.classify_binary_pipeline. Never re-derive PDF/image-ness here.
    pipeline = classify_binary_pipeline(mime_type, row["file_name"])
    if not pipeline:
        return None
    is_image = pipeline == "image"
    file_name_lower = (row["file_name"] or "").lower()

    # ─── Resolve cld_file bytes ───────────────────────────────────────
    # cld_files rows carry an `s3://bucket/<owner>/<file_path>` storage_uri.
    # `cld_files.id` is the canonical handle; `file_path` is a logical
    # display path that can drift from `storage_uri` after a folder move
    # (see aidream/api/routers/files.py::bulk_move_files which updates
    # file_path WITHOUT moving bytes). The bytes always live at
    # `storage_uri` regardless.
    #
    # Resolve bytes through the canonical FileManager.resolve_media_async
    # path so the byte cache, auth hooks, and future audit/quota hooks
    # apply. Pass MediaRef(file_id=...) so the resolver looks up the
    # authoritative cld_files row, not a (potentially stale) storage_uri.
    import os as _os
    import tempfile as _tempfile

    try:
        from matrx_files.cloud_sync.media_ref import MediaRef
        from matrx_utils.ctx import system_file_access

        from matrx_rag._ext import get_cloud_file_manager

        fm = get_cloud_file_manager()
        # Internal RAG ingest resolving a server-constructed ref — declare it.
        with system_file_access("rag-ingest-pdf"):
            resolved = await fm.resolve_media_async(MediaRef(file_id=source_id), needs_bytes=True)
        b64 = getattr(resolved, "base64_data", None) if resolved else None
        if b64:
            import base64 as _base64

            pdf_bytes = _base64.b64decode(b64)
        else:
            pdf_bytes = None
    except Exception as exc:  # noqa: BLE001
        import logging as _logging

        _logging.getLogger(__name__).warning(
            "cld_file fetch failed for source_id=%s storage_uri=%s: %s",
            source_id,
            row.get("storage_uri"),
            exc,
        )
        return IngestionResult(
            source_kind="cld_file",
            source_id=source_id,
            field_id=field_id,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model=default_text_model(),
            error=f"cld_file_fetch_failed: {exc}",
        )
    if not pdf_bytes:
        return IngestionResult(
            source_kind="cld_file",
            source_id=source_id,
            field_id=field_id,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model=default_text_model(),
            error="cld_file_fetch_failed: empty bytes",
        )

    # Pick a sensible suffix so downstream tools that key on extension
    # (PyMuPDF, image libs) get the right hint.
    suffix = ".pdf"
    fn_lower = (row["file_name"] or "").lower()
    for ext in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic", ".heif", ".bmp", ".pdf"):
        if fn_lower.endswith(ext):
            suffix = ext
            break
    with _tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as _tmp:
        _tmp.write(pdf_bytes)
        local_path = _tmp.name

    # Use the host-supplied effective org rather than the cld_files row's own
    # ``organization_id`` (the row may carry NULL for personal-scope uploads;
    # the four KG tables must never get NULL — see ingest_source docstring).
    effective_org = organization_id or row["organization_id"]

    # This function OWNS the temp file written above (created delete=False). The
    # image/PDF pipelines read it fully before returning and never delete it, so
    # release it here on EVERY exit (success, the org-missing raise below, or a
    # pipeline exception). Without this each cld_file PDF/image ingest leaks one
    # temp file. (The resumable stages path uses its own temp mechanism — this is
    # the single-shot dispatch path, so the file is dead once the call returns.)
    try:
        if not effective_org:
            raise ValueError(
                "matrx_rag._maybe_dispatch_pdf: organization_id is required and "
                "the cld_files row did not carry one either. The host must supply "
                "the personal-org default at the auto-ingest boundary."
            )

        if is_image:
            from matrx_rag.image_pipeline import ingest_image

            # Best-effort MIME detection from filename when the row column is empty.
            derived_mime = mime_type or _guess_image_mime(file_name_lower)
            return await ingest_image(
                cld_file_id=row["id"],
                organization_id=effective_org,
                owner_id=row["owner_id"],
                local_path=local_path,
                file_name=row["file_name"],
                storage_uri=row["storage_uri"],
                mime_type=derived_mime,
                force=force,
                emitter=emitter,
            )

        from matrx_rag.pdf_pipeline import ingest_pdf

        return await ingest_pdf(
            cld_file_id=row["id"],
            organization_id=effective_org,
            owner_id=row["owner_id"],
            local_path=local_path,
            file_name=row["file_name"],
            storage_uri=row["storage_uri"],
            force=force,
            emitter=emitter,
            cleanup=cleanup,
        )
    finally:
        try:
            _os.unlink(local_path)
        except OSError:
            pass


def _guess_image_mime(name: str) -> str:
    if name.endswith(".png"):
        return "image/png"
    if name.endswith(".jpg") or name.endswith(".jpeg"):
        return "image/jpeg"
    if name.endswith(".webp"):
        return "image/webp"
    if name.endswith(".gif"):
        return "image/gif"
    if name.endswith(".heic"):
        return "image/heic"
    if name.endswith(".heif"):
        return "image/heif"
    if name.endswith(".bmp"):
        return "image/bmp"
    return "image/png"


async def _existing_hash(
    source_kind: str,
    source_id: str,
    field_id: str | None,
) -> str | None:
    KgChunks = get_db_model("KgChunks")
    qb = KgChunks.filter(source_kind=source_kind, source_id=source_id)
    # Raw SQL used ``field_id IS NOT DISTINCT FROM $3`` — branch in Python so
    # a NULL field_id matches NULL rows instead of matching nothing.
    if field_id is None:
        qb = qb.filter(field_id__isnull=True)
    else:
        qb = qb.filter(field_id=field_id)
    rows = await qb.order_by("-created_at").limit(1).values("source_hash")
    return rows[0]["source_hash"] if rows else None


def _merge_metadata(
    source_meta: dict[str, object], chunk_meta: dict[str, object]
) -> dict[str, object]:
    return {"source": source_meta, **chunk_meta}


def _format_vector(values: list[float]) -> str:
    """pgvector wants either a list registered via codec OR the literal
    ``'[v1,v2,...]'`` string. We use the string form so we don't need
    per-connection codec registration on a pool that's about to grow.
    """
    return "[" + ",".join(repr(float(v)) for v in values) + "]"


def _format_embedding_payloads_sync(
    chunk_ids: list[str],
    vectors: list[list[float] | None],
    *,
    organization_id: str | None,
    owner_id: str | None,
) -> list[tuple[str, str | None, str | None, str]]:
    """Build pgvector write payloads outside the asyncio event loop."""
    payloads: list[tuple[str, str | None, str | None, str]] = []
    for chunk_id, vector in zip(chunk_ids, vectors, strict=True):
        if vector is None:
            raise ValueError(f"missing embedding vector for chunk {chunk_id}")
        payloads.append((chunk_id, organization_id, owner_id, _format_vector(vector)))
    return payloads


async def _format_embedding_payloads(
    chunk_ids: list[str],
    vectors: list[list[float] | None],
    *,
    organization_id: str | None,
    owner_id: str | None,
) -> list[tuple[str, str | None, str | None, str]]:
    return await asyncio.to_thread(
        _format_embedding_payloads_sync,
        chunk_ids,
        vectors,
        organization_id=organization_id,
        owner_id=owner_id,
    )


async def delete_source_artifacts(
    source_kind: str,
    source_id: str,
    field_id: str | None = None,
) -> int:
    """Delete a source's chunk rows (the erasure primitive) and return the count.

    Cascades (defined in 0003_rag_schema.sql) remove the embedding rows,
    ``kg_chunk_entities`` mentions, and ``kg_edges`` source-chunk evidence
    automatically. Entities themselves are NOT deleted — they may be
    shared across sources (the note-delete hook calls this; a separate
    orphan-entity sweep runs periodically).

    NULL-``field_id`` semantics (was ``IS NOT DISTINCT FROM``): a NULL
    field_id matches NULL rows; a non-NULL field_id matches only that
    field's chunks.

    Returns the number of rows deleted (0 when the source had no chunks).
    """
    KgChunks = get_db_model("KgChunks")
    field_filter = {"field_id": field_id} if field_id is not None else {"field_id__isnull": True}
    # hard-delete-ok: derived search chunks, rebuilt on re-ingest of their source
    return await KgChunks.delete_where(
        source_kind=source_kind,
        source_id=source_id,
        **field_filter,
    )


async def soft_delete_source_artifacts(source_kind: str, source_id: str) -> dict[str, int]:
    """Trash a source's rag.* artifacts so they leave retrieval but can be
    restored (soft-delete symmetry — see /Users/armanisadeghi/code/common-docs/projects/knowledge-system/README.md).

    Sets ``kg_chunks.deleted_at`` — the dedicated trash marker, distinct from
    ``valid_to`` which means bitemporal *supersession* (reprocess/replace).
    Restore clears only ``deleted_at``, so superseded chunks are never
    resurrected by a trash round-trip. Also sets
    ``data_store_members.deleted_at``. Entities are org-wide and shared;
    they are NEVER touched here (a separate orphan sweep handles those).

    Idempotent: only flips rows that are still live. Returns affected counts.
    """
    now = datetime.now(UTC)
    KgChunks = get_db_model("KgChunks")
    DataStoreMembers = get_db_model("DataStoreMembers")
    chunks = await KgChunks.update_where(
        {"source_kind": source_kind, "source_id": source_id, "deleted_at__isnull": True},
        deleted_at=now,
    )
    members = await DataStoreMembers.update_where(
        {"source_kind": source_kind, "source_id": source_id, "deleted_at__isnull": True},
        deleted_at=now,
    )
    return {
        "chunks": int(chunks.rows_affected),
        "data_store_members": int(members.rows_affected),
    }


async def restore_source_artifacts(source_kind: str, source_id: str) -> dict[str, int]:
    """Undo ``soft_delete_source_artifacts`` — bring a source's trashed rag.*
    artifacts back into retrieval. Clears ``kg_chunks.deleted_at`` and
    ``data_store_members.deleted_at`` (NEVER ``valid_to`` — superseded chunks
    stay superseded). Idempotent. Returns affected counts.
    """
    KgChunks = get_db_model("KgChunks")
    DataStoreMembers = get_db_model("DataStoreMembers")
    chunks = await KgChunks.update_where(
        {"source_kind": source_kind, "source_id": source_id, "deleted_at__isnull": False},
        deleted_at=None,
    )
    members = await DataStoreMembers.update_where(
        {"source_kind": source_kind, "source_id": source_id, "deleted_at__isnull": False},
        deleted_at=None,
    )
    return {
        "chunks": int(chunks.rows_affected),
        "data_store_members": int(members.rows_affected),
    }


async def soft_delete_document_artifacts(processed_document_id: str) -> dict[str, int]:
    """Trash ONE processed document's rag.* artifacts (per-derivation scope).

    Sets ``kg_chunks.deleted_at`` for the document's chunks and
    ``data_store_members.deleted_at`` for memberships keyed on this
    processed_document id. File-keyed memberships are NOT touched — those
    belong to the file lifecycle (``soft_delete_source_artifacts``), and a
    sibling derivation of the same file must keep its store bindings live.
    Idempotent. Returns affected counts.
    """
    now = datetime.now(UTC)
    KgChunks = get_db_model("KgChunks")
    DataStoreMembers = get_db_model("DataStoreMembers")
    chunks = await KgChunks.update_where(
        {"processed_document_id": processed_document_id, "deleted_at__isnull": True},
        deleted_at=now,
    )
    members = await DataStoreMembers.update_where(
        {
            "source_kind": "processed_document",
            "source_id": processed_document_id,
            "deleted_at__isnull": True,
        },
        deleted_at=now,
    )
    return {
        "chunks": int(chunks.rows_affected),
        "data_store_members": int(members.rows_affected),
    }


async def restore_document_artifacts(processed_document_id: str) -> dict[str, int]:
    """Undo ``soft_delete_document_artifacts`` for one processed document.
    Clears only ``deleted_at`` (never ``valid_to``). Idempotent."""
    KgChunks = get_db_model("KgChunks")
    DataStoreMembers = get_db_model("DataStoreMembers")
    chunks = await KgChunks.update_where(
        {"processed_document_id": processed_document_id, "deleted_at__isnull": False},
        deleted_at=None,
    )
    members = await DataStoreMembers.update_where(
        {
            "source_kind": "processed_document",
            "source_id": processed_document_id,
            "deleted_at__isnull": False,
        },
        deleted_at=None,
    )
    return {
        "chunks": int(chunks.rows_affected),
        "data_store_members": int(members.rows_affected),
    }


async def purge_document_artifacts(processed_document_id: str) -> dict[str, int]:
    """Hard-erase ONE processed document's rag.* artifacts (trash-empty path).

    The ONLY per-document path that runs a real DELETE on chunks — CASCADE
    removes embeddings, ``kg_chunk_entities`` mentions, and ``kg_edges``
    evidence. Also erases memberships keyed on this processed_document id.
    NOT reversible. Returns deleted counts.
    """
    KgChunks = get_db_model("KgChunks")
    DataStoreMembers = get_db_model("DataStoreMembers")
    # hard-delete-ok: retention purge primitive with no person-reachable caller
    chunks = await KgChunks.delete_where(processed_document_id=processed_document_id)
    # hard-delete-ok: retention purge primitive with no person-reachable caller
    members = await DataStoreMembers.delete_where(
        source_kind="processed_document", source_id=processed_document_id
    )
    return {"chunks": int(chunks), "data_store_members": int(members)}


async def purge_source_artifacts(source_kind: str, source_id: str) -> dict[str, int]:
    """Hard-erase ALL of a source's rag.* artifacts (the trash-empty / hard-delete
    path). Deletes every chunk for the source regardless of ``field_id`` —
    CASCADE removes the embedding rows, ``kg_chunk_entities`` mentions, and
    ``kg_edges`` source-chunk evidence — plus every data-store membership.
    Entities survive (shared). Returns deleted counts.

    Differs from ``delete_source_artifacts`` which is field-scoped (notes path).
    """
    KgChunks = get_db_model("KgChunks")
    DataStoreMembers = get_db_model("DataStoreMembers")
    # hard-delete-ok: retention purge primitive with no person-reachable caller
    chunks = await KgChunks.delete_where(source_kind=source_kind, source_id=source_id)
    # hard-delete-ok: retention purge primitive with no person-reachable caller
    members = await DataStoreMembers.delete_where(source_kind=source_kind, source_id=source_id)
    return {"chunks": int(chunks), "data_store_members": int(members)}


__all__ = [
    "IngestionResult",
    "delete_source_artifacts",
    "ingest_source",
    "purge_document_artifacts",
    "purge_source_artifacts",
    "restore_document_artifacts",
    "restore_source_artifacts",
    "soft_delete_document_artifacts",
    "soft_delete_source_artifacts",
    "upsert_chunks",
]
