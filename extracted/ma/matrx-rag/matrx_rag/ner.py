"""LLM-driven NER → kg_entities widening (Phase C of the Knowledge-Graph plan).

After chunking + embedding, the ingest pipeline calls :func:`extract_entities`
for the chunks that are NEW this run (reused chunks already carry their
``kg_chunk_entities`` mentions from a prior run — the cost-reuse contract:
re-NER'ing them would re-pay the LLM cost for unchanged content).

The pipeline is a ``matrx_orm.session``-style coordinator: writes are
collected, sorted by dependency, and executed in tiers. The original
"per-chunk transaction with an advisory lock around entity dedup" shape
deadlocked under speed (GLiNER finishes in tens of milliseconds, so all
chunks land in the persist phase at nearly the same instant — every parallel
transaction grabbed advisory locks in dataflow order, which is
non-deterministic, and two coordinators picking opposite orders trip a
classic lock-ordering cycle). The shape now is:

  Tier A — extract  (parallel, semaphore-bounded — LLM/GLiNER call dominates)
            Collect ``[(chunk_id, [normalised_entities])]`` per chunk. NO DB
            writes yet. A bad chunk lands its error in ``result.errors`` and
            the rest continue; an empty chunk is marked ``succeeded`` (a
            valid completed outcome, see the cost-reuse contract).

  Tier B — resolve entities  (SERIAL coordinator, sorted, race-tolerant)
            Build the distinct ``(kind, lower(name))`` set across every
            chunk of this source. Sort it. Resolve the whole set in ONE
            ``KgEntities.bulk_upsert`` whose ``ConflictTarget`` renders the
            ``kg_entities_ner_canonical_idx`` partial expression unique
            index. No advisory locks: the index is the storage-layer source
            of truth — if a parallel coordinator wins the race for a bucket,
            ON CONFLICT resolves to the winner's row and RETURNING hands us
            its id.

  Tier C — write mentions + edges  (parallel per chunk)
            Each chunk's writes happen in its own transaction. Entity ids
            are already resolved (from tier B) so no entity-dedup
            contention is possible. Distinct entity-id pairs for the
            co-occurrence edges are iterated in sorted order — every
            transaction touches the same row-locks in the same canonical
            order, so cross-chunk edge writes can't form a cycle. Mention rows
            go in tier-B bucket order then span (``_mention_rows_in_lock_order``)
            so two runs over the same chunk never cycle, and the whole per-chunk
            transaction re-runs under ``retry_on_transient`` on a residual
            40P01/timeout; a chunk that never lands stays unmarked for re-NER.

  Tier D — recompute confidence_avg  (SERIAL, sorted)
            Once per source, recompute the mean over all mentions for each
            entity touched in this batch — sorted entity ids → no row-lock
            cycle vs. any other coordinator running concurrently. Pulling
            this out of tier C also avoids the per-chunk redundant
            recompute when a hot entity appears in many chunks.

Why this is the ORM way: ``matrx_orm.session.dag.tier_ops`` does exactly
this for generated Model classes — FK-dependency-sorted, deterministic
within-tier order. matrx-rag ships its own rag.* model classes
(``matrx_rag.db.models_rag``, bound at runtime via ``configure``/
``bootstrap_db``) and resolves them through ``get_db_model``, so every
tier writes through matrx-orm primitives. The same correctness arguments
apply.

Ownership: every mention + entity carries ``organization_id``; the chunk it
points at carries ``created_by`` (the user). ``user_id`` is required and threaded
through so the extractor honors per-user scoping.

Visibility: defense-in-depth. The auto-ingest router (Phase B) already drops
``is_visible_to_model=false`` cx_message chunks upstream; we filter again here
keyed off the model-view flag (never ``status``) so a future ingest path that
bypasses the router still can't feed hidden content to the model.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import UUID

from matrx_orm import (
    LockContentionError,
    PoolAcquireTimeoutError,
    QueryTimeoutError,
    retry_on_transient,
    transaction,
)
from matrx_utils import vcprint

from matrx_rag._ext import (
    get_db_model,
    get_ner_extractor,
    get_ner_finisher,
)
from matrx_rag.db import PACKAGE_DB_NAME

logger = logging.getLogger(__name__)


# When this fraction (percent) of a document's chunks fail extraction even
# after the provider's own retries, escalate the summary log from WARNING to
# ERROR — at that point the NER pass is degraded, not merely lossy.
_NER_FAILURE_ALERT_PCT = 25.0


# NER fan-out / cap tunables — code-reviewed constants, not env vars. (Were
# MATRX_RAG_NER_CONCURRENCY / _PERSIST_CONCURRENCY / _MAX_CHUNKS_PER_SOURCE.)
#  * EXTRACT cap: the LLM call dominates per-chunk latency, so a 200-chunk doc
#    finishes in <1 min when overlapped; cap the fan-out so a big doc can't open
#    hundreds of concurrent provider requests and trip rate limits.
#  * PERSIST cap: the DB pool (not the LLM) is the bottleneck; capping at 8
#    keeps ~8 active transactions far below pool saturation (the 2026-06-03
#    pool-exhaustion incident hit this with 171 chunks firing in parallel).
#  * MAX_CHUNKS: an anti-runaway shield, NOT a per-document size limit. The
#    canonical wired extractor is LOCAL GLiNER2 (no per-chunk API billing — see
#    package_integration.py), so the old "don't fire 500+ API calls" rationale
#    doesn't apply. The real workload here is scanned legal PDFs averaging
#    250-350 pages (~500-700 leaf chunks) and ranging up to 4,000+ pages
#    (~6,000+ leaf chunks); a 500 cap silently produced ZERO knowledge graph for
#    the *typical* document (2026-06-13: a 381-page / 559-leaf-chunk upload got
#    clean+chunk+embed but NER refused outright). The cap now covers that real
#    range and only trips on genuinely pathological fan-out. A larger batch
#    backfill still raises it explicitly.
NER_PERSIST_CONCURRENCY: int = 8
NER_MAX_CHUNKS_PER_SOURCE: int = 12000
# Whole-transaction attempts for one chunk's tier-C write when Postgres breaks
# a lock collision (40P01/40001/55P03) or a timeout fires. The lock order below
# removes the known cycles; this absorbs any residual one.
NER_PERSIST_ATTEMPTS: int = 4


def _ner_persist_concurrency() -> int:
    return NER_PERSIST_CONCURRENCY


def _ner_max_chunks_per_source() -> int:
    return NER_MAX_CHUNKS_PER_SOURCE


# The NER kinds the extractor agent + the ``kg_entities_ner_canonical_idx``
# partial unique index recognize (kg_004's eight, widened by kg_042 with the
# kinds a person's own material is about: products, places, subjects and
# recurring activities). A row whose kind is outside this set is dropped (the
# model occasionally invents a kind) so it can never collide with the
# code-symbol entities that dedup on canonical_id instead.
NER_KINDS: frozenset[str] = frozenset(
    {
        "person",
        "organization",
        "address",
        "phone",
        "email",
        "url",
        "date",
        "concept",
        "product",
        "place",
        "subject",
        "activity",
    }
)

# Kinds that are thematic ideas, not named things with identity (STOP rule 7):
# they get ``kg_entities.is_concept = true`` and are never scope-linked.
CONCEPT_KINDS: frozenset[str] = frozenset({"concept", "subject", "activity"})

_ORG_SENTINEL = "00000000-0000-0000-0000-000000000000"


@dataclass
class NerChunkInput:
    """The minimal per-chunk shape :func:`extract_entities` needs. Built by the
    ingest pipeline from the freshly-inserted chunks (reused chunks are NOT
    passed in — the caller filters them out per the cost-reuse contract)."""

    chunk_id: str
    content_text: str
    # is_visible_to_model defaults True for every non-cx_message source. The
    # cx_message ingest path (Phase C+) sets it explicitly so a hidden message
    # body never reaches the extractor.
    is_visible_to_model: bool = True


@dataclass
class NerResult:
    """Typed outcome of one NER pass over a batch of new chunks."""

    chunks_processed: int = 0
    chunks_skipped: int = 0
    # Chunks whose extractor call RAISED (after the provider's own retries) and
    # therefore contributed ZERO entities. Tracked as a first-class counter so
    # the aggregate failure rate is loud, not buried in per-chunk warnings — a
    # high value means the document was silently gutted (the 2026-06-09 75%-drop
    # incident) and the caller must treat the NER pass as degraded.
    extractor_failures: int = 0
    entities_written: int = 0  # new kg_entities rows created
    entities_reused: int = 0  # existing kg_entities rows deduped onto
    mentions_written: int = 0  # kg_chunk_entities rows
    edges_written: int = 0  # co_occurs_with rows created/incremented
    skipped_reason: Literal["no_extractor", "no_chunks"] | None = None
    errors: list[str] = field(default_factory=list)
    # chunk_ids whose NER pass fully SUCCEEDED this run — extractor returned AND
    # (no entities OR persist landed). A chunk that found zero entities counts as
    # succeeded (a valid completed outcome). The caller stamps the completion
    # marker (rag.kg_chunks.ner_extracted_at) for exactly these so they are never
    # re-NER'd, while a chunk that errored stays unmarked and retries next run.
    succeeded_chunk_ids: set[str] = field(default_factory=set)


def _coerce_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_conf(value: Any) -> float:
    try:
        c = float(value)
    except (TypeError, ValueError):
        return 0.5
    if c < 0.0:
        return 0.0
    if c > 1.0:
        return 1.0
    return c


def _bucket_key(ent: dict[str, Any]) -> tuple[str, str]:
    """The dedup key matching ``kg_entities_ner_canonical_idx``: ``(kind, lower(name))``.

    organization_id is held constant by the caller (one extract_entities call =
    one organization), so it's not part of the in-batch key. Two raw entities
    with the same key dedup onto the same kg_entities row.
    """
    return (ent["kind"], ent["name"].lower())


def _mention_rows_in_lock_order(
    *,
    chunk_id: str,
    organization_id: str | None,
    mentions: list[tuple[dict[str, Any], str]],
    metadata: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """kg_chunk_entities rows for one chunk, in THE lock order every writer
    uses: tier B's bucket key ``(kind, lower(name))`` (the order tier B locks
    kg_entities rows), then span, then entity id. Within one organization the
    bucket key maps 1:1 to ``entity_id``, so this is also a total order over
    the ``(chunk_id, entity_id, span_start)`` conflict key — two concurrent
    writers of the same chunk wait on each other, never cycle."""

    def _key(item: tuple[dict[str, Any], str]) -> tuple[Any, ...]:
        ent, eid = item
        return (_bucket_key(ent), ent["span_start"], ent["span_end"], eid)

    return [
        {
            "chunk_id": chunk_id,
            "entity_id": eid,
            "organization_id": organization_id,
            "span_start": ent["span_start"],
            "span_end": ent["span_end"],
            "confidence": ent["confidence"],
            "attrs": ent["attrs"],
            "metadata": metadata or {},
        }
        for ent, eid in sorted(mentions, key=_key)
    ]


def _collapse_overlapping_spans(spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep at most one span per (span_start, span_end) position, preferring
    the highest-confidence variant.

    Why: GLiNER routinely emits two spans at the *exact* same position with
    different ``kind`` (e.g. ``(organization, "Postgres", 546–554, 0.55)`` and
    ``(concept, "Postgres", 546–554, 0.51)``). Tier-B keys on
    ``(kind, lower(name))`` BEFORE the LLM finisher's reclassification mapping
    is applied, so two same-position spans with different kinds always create
    two distinct ``kg_entities`` rows downstream — exactly once per overlap.
    The LLM finisher cannot fix this; it sees the two pairs as distinct
    inputs and at best maps both to the same canonical target (which still
    requires the *target* bucket to dedupe against existing rows, which it
    doesn't reliably do because the org-Postgres span was never reclassified
    in the input record itself).

    Rule (deterministic, no model required):
      * Group by ``(span_start, span_end)``.
      * Keep the highest-confidence member of each group.
      * Tie-break by ``kind`` alphabetical, then ``name`` alphabetical (so
        runs that re-extract the same chunk produce byte-identical norm
        lists — important for the existing ``valid_to IS NULL`` dedup logic).
      * Spans without a valid range (``span_start >= span_end`` or both 0)
        are NEVER grouped: they pass through untouched. Some extractors
        legitimately emit position-less spans for source-level entities; we
        don't want to over-merge them.

    The finisher still runs after this; it just sees one pair per overlap
    instead of two, which is what the LLM expected to see in the first
    place.
    """
    if len(spans) < 2:
        return spans
    by_pos: dict[tuple[int, int], dict[str, Any]] = {}
    unpositioned: list[dict[str, Any]] = []
    for s in spans:
        a = s.get("span_start") or 0
        b = s.get("span_end") or 0
        if a >= b:
            unpositioned.append(s)
            continue
        prev = by_pos.get((a, b))
        if prev is None:
            by_pos[(a, b)] = s
            continue
        prev_conf = float(prev.get("confidence") or 0.0)
        cur_conf = float(s.get("confidence") or 0.0)
        if cur_conf > prev_conf:
            by_pos[(a, b)] = s
            continue
        if cur_conf == prev_conf:
            prev_key = (str(prev.get("kind") or ""), str(prev.get("name") or ""))
            cur_key = (str(s.get("kind") or ""), str(s.get("name") or ""))
            if cur_key < prev_key:
                by_pos[(a, b)] = s
    return list(by_pos.values()) + unpositioned


@dataclass(frozen=True)
class NerEngineStamp:
    """Which engine produced a chunk's entities — stamped on the chunk
    (``kg_chunks.metadata.ner``) and on every mention it wrote
    (``kg_chunk_entities.metadata.engine``). ``version`` is the engine's own
    identity of its current behaviour (a GLiNER model + threshold, an agent
    definition + version): a consumer that skips "already done" chunks compares
    BOTH, so a changed engine re-extracts."""

    name: str
    version: str = ""


@dataclass(frozen=True)
class NerEngine:
    """The engine one :func:`extract_entities` pass runs: its stamp and the
    extractor that answers it. A host that chooses the engine per call (org,
    person, source kind) installs ONE extractor with a ``resolve_engine``
    method (see :func:`resolve_ner_engine`)."""

    stamp: NerEngineStamp
    extractor: Any


@dataclass
class ChunkExtraction:
    """One chunk's raw extractor answer, ready for :func:`persist_chunk_entities`.

    ``entities`` is the extractor's own output shape — ``{kind, canonical_name,
    span_start, span_end, confidence, attrs?}`` per item — exactly what
    :meth:`NerExtractor.extract` returns and what the ``kg.ner_extractor``
    mandate's ``entities`` artifact holds, so a live pass and a batched one
    persist through the same code."""

    chunk_id: str
    content_text: str
    entities: list[dict[str, Any]] = field(default_factory=list)


async def resolve_ner_engine(
    extractor: Any,
    *,
    organization_id: str,
    user_id: str,
    source_kind: str | None,
) -> NerEngine:
    """The engine for one pass. A dispatching extractor answers through its
    ``resolve_engine(organization_id=, user_id=, source_kind=)`` (returning a
    :class:`NerEngine`); a plain one IS the engine, stamped with its
    ``engine_name`` / ``engine_version`` attributes (class name when unnamed)."""
    resolver = getattr(extractor, "resolve_engine", None)
    if callable(resolver):
        engine = await resolver(
            organization_id=organization_id, user_id=user_id, source_kind=source_kind
        )
        if not isinstance(engine, NerEngine):
            raise TypeError(
                f"resolve_engine returned {type(engine).__name__}, expected matrx_rag.ner.NerEngine"
            )
        return engine
    return NerEngine(
        stamp=NerEngineStamp(
            name=str(getattr(extractor, "engine_name", "") or type(extractor).__name__),
            version=str(getattr(extractor, "engine_version", "") or ""),
        ),
        extractor=extractor,
    )


async def extract_entities(
    chunks: list[NerChunkInput],
    *,
    organization_id: str | None,
    user_id: str,
    source_kind: str | None = None,
    source_id: str | None = None,
) -> NerResult:
    """Run NER over NEW chunks and populate kg_entities / kg_chunk_entities /
    kg_edges. Never raises — a single bad chunk is recorded in ``errors`` and
    the rest proceed. Returns a typed :class:`NerResult`.

    This is tier A (extraction) only; every write — normalisation, the
    finisher, tiers B–D and the completion stamp — is
    :func:`persist_chunk_entities`, the same function a host's batch lane calls
    when the extractor's answers arrive later.

    Extraction here is always INLINE: the save-time engine (the host's choice
    per call, GLiNER by default) runs per chunk. A batched engine belongs in the
    HOST beside the other batch consumers, which collects answers and calls
    :func:`persist_chunk_entities` itself.
    """
    result = NerResult()
    if not user_id:
        # Ownership contract — refuse rather than write unattributable rows.
        result.skipped_reason = "no_chunks"
        result.errors.append("extract_entities: missing user_id")
        return result

    if not organization_id:
        # 2026-06-03 incident fix — the four KG tables must never get NULL
        # organization_id. Refuse loudly here rather than silently writing
        # rows that would later leak across users via kg_graph's read-access
        # predicate. The caller carries the organization.
        result.skipped_reason = "no_chunks"
        result.errors.append(
            "extract_entities: missing organization_id (the caller carries the "
            "organization of the record it is extracting)"
        )
        return result

    extractor = get_ner_extractor()
    if extractor is None:
        # No host wired an extractor (e.g. matrx-local local-RAG, or a test
        # that didn't inject). Clean no-op — NER simply does not run.
        result.skipped_reason = "no_extractor"
        return result

    # Visibility filter (defense-in-depth — see module docstring).
    visible = [c for c in chunks if c.is_visible_to_model and (c.content_text or "").strip()]
    result.chunks_skipped = len(chunks) - len(visible)
    if not visible:
        result.skipped_reason = "no_chunks"
        return result

    # Hard chunk-count cap (cost shield). A pass with more visible chunks than
    # the cap would fire that many extractor calls (one per chunk), which is
    # exactly the unbounded-fan-out failure mode we never want to discover by
    # reading the invoice. Refuse loudly with zero extractor calls.
    chunk_cap = _ner_max_chunks_per_source()
    if len(visible) > chunk_cap:
        logger.error(
            "ner.extract_entities: REFUSING to run NER on %d chunks for "
            "%s/%s (cap=%d). Either chunk the source more aggressively, "
            "raise NER_MAX_CHUNKS_PER_SOURCE for a batch job, "
            "or fix the upstream chunker. No extractor calls were made.",
            len(visible),
            source_kind,
            source_id,
            chunk_cap,
        )
        result.errors.append(f"chunk_cap_exceeded: {len(visible)} > {chunk_cap}")
        result.skipped_reason = "no_chunks"
        return result

    # The engine for THIS pass (one source, one organization, one person). A
    # host that cannot answer which engine runs is a failure to say out loud —
    # the chunks stay unmarked and retry, never extracted by a guess.
    try:
        engine = await resolve_ner_engine(
            extractor,
            organization_id=organization_id,
            user_id=user_id,
            source_kind=source_kind,
        )
    except Exception as exc:  # noqa: BLE001 — never raises; the error is the result
        logger.error(
            "ner.extract_entities: could not resolve the NER engine for %s/%s (org %s): %s",
            source_kind,
            source_id,
            organization_id,
            exc,
        )
        result.errors.append(f"engine_resolution_error: {exc}")
        return result

    # ─── Tier A: parallel extraction per chunk ─────────────────────────────
    # The LLM/GLiNER call dominates per-chunk latency, so every independent
    # extraction is dispatched immediately. NO database writes happen in this
    # tier — the only mutation is appending to ``extractions`` and bumping the
    # typed result counters, both single-threaded-event-loop safe.
    extractions: list[ChunkExtraction] = []

    async def _extract_one(chunk: NerChunkInput) -> None:
        try:
            extracted = await engine.extractor.extract(
                chunk.content_text,
                organization_id=organization_id,
                user_id=user_id,
                source_kind=source_kind,
                source_id=source_id,
            )
        except Exception as exc:  # noqa: BLE001 — one bad chunk must not abort the run
            result.extractor_failures += 1
            logger.error(
                "ner.extract_entities: extractor FAILED for chunk %s (%s/%s, %d chars): %s",
                chunk.chunk_id,
                source_kind,
                source_id,
                len(chunk.content_text or ""),
                exc,
            )
            vcprint(
                {
                    "chunk_id": chunk.chunk_id,
                    "source": f"{source_kind}/{source_id}",
                    "chars": len(chunk.content_text or ""),
                    "error": str(exc),
                    "preview": (chunk.content_text or "")[:200],
                },
                "NER EXTRACTOR FAILED — chunk dropped, entities MISSING",
                color="red",
            )
            result.errors.append(f"{chunk.chunk_id}: extractor_error: {exc}")
            return
        extractions.append(
            ChunkExtraction(
                chunk_id=chunk.chunk_id,
                content_text=chunk.content_text,
                entities=[e for e in (extracted or []) if isinstance(e, dict)],
            )
        )

    # return_exceptions=True is belt-and-suspenders: every coroutine already
    # catches its own failures, but this guarantees one unexpected raise can
    # never cancel its siblings mid-flight.
    await asyncio.gather(*(_extract_one(c) for c in visible), return_exceptions=True)

    # Surface the aggregate extractor failure rate LOUDLY. A handful of dropped
    # chunks is normal; a large fraction means the extraction provider is
    # shedding load DESPITE the provider's retries, and the document is being
    # silently gutted — exactly the 2026-06-09 75%-drop that used to hide
    # behind per-chunk warnings + a tally.
    attempted = len(visible)
    if result.extractor_failures and attempted:
        fail_pct = 100.0 * result.extractor_failures / attempted
        logger.error(
            "ner.extract_entities: %d/%d chunks (%.1f%%) FAILED extraction for "
            "%s/%s after provider retries — these contributed ZERO entities. "
            "%sInvestigate the provider/chunker; central provider admission owns pacing.",
            result.extractor_failures,
            attempted,
            fail_pct,
            source_kind,
            source_id,
            "PROVIDER LIKELY SHEDDING LOAD. " if fail_pct >= _NER_FAILURE_ALERT_PCT else "",
        )
        vcprint(
            {
                "source": f"{source_kind}/{source_id}",
                "failed_chunks": result.extractor_failures,
                "attempted": attempted,
                "fail_pct": round(fail_pct, 1),
                "errors": result.errors[:10],
            },
            "NER PASS DEGRADED — chunks dropped, document partially gutted",
            color="red",
        )

    if not extractions:
        return result
    return await persist_chunk_entities(
        extractions,
        organization_id=organization_id,
        user_id=user_id,
        engine=engine.stamp,
        source_kind=source_kind,
        source_id=source_id,
        result=result,
    )


def _normalize_extracted(entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The extractor's answer → the persisted span shape. A kind outside
    :data:`NER_KINDS` or a nameless row is dropped (the model occasionally
    invents a kind), then same-position spans collapse to one."""
    norm: list[dict[str, Any]] = []
    for ent in entities or []:
        if not isinstance(ent, dict):
            continue
        kind = str(ent.get("kind") or "").strip().lower()
        name = str(ent.get("canonical_name") or ent.get("name") or "").strip()
        if kind not in NER_KINDS or not name:
            continue
        norm.append(
            {
                "kind": kind,
                "name": name,
                "span_start": _coerce_int(ent.get("span_start")),
                "span_end": _coerce_int(ent.get("span_end")),
                "confidence": _coerce_conf(ent.get("confidence")),
                "attrs": ent.get("attrs") if isinstance(ent.get("attrs"), dict) else {},
            }
        )
    # Overlap-collapse: when GLiNER (or any extractor) emits multiple spans at
    # the same position with different kinds, keep one, before tier B keys on
    # (kind, lower(name)) and would make two entities of it.
    return _collapse_overlapping_spans(norm)


async def persist_chunk_entities(
    extractions: list[ChunkExtraction],
    *,
    organization_id: str,
    user_id: str,
    engine: NerEngineStamp,
    source_kind: str | None = None,
    source_id: str | None = None,
    result: NerResult | None = None,
) -> NerResult:
    """Write extractor answers for these chunks: tiers A.5 (the optional
    finisher), B (entities), C (mentions + edges) and D (confidence_avg), then
    stamp every chunk that landed.

    The ONE write path for entity extraction — the inline pass
    (:func:`extract_entities`) and a host's batch lane both end here, so a
    batched answer is persisted exactly as a live one.

    * A chunk's mentions and co-occurrence edges are REPLACED, not appended:
      the previous engine's mentions (and edges) of that chunk are deleted in
      the same transaction that writes the new ones. A re-delivered answer
      (at-least-once handlers) therefore converges instead of double-counting
      edge weights, and an engine switch leaves only the new engine's view.
    * Every mention carries ``metadata.engine`` / ``metadata.engine_version``.
    * Every chunk that landed — including one whose answer held no entity —
      gets ``ner_extracted_at`` and ``metadata.ner = {engine, version, at}``.
      A chunk whose write failed stays unmarked and retries.

    ``organization_id`` is the tenant every row is written into; the caller
    carries it (one call = one organization). Never raises: failures are on
    the returned :class:`NerResult`.
    """
    result = result if result is not None else NerResult()
    if not user_id or not organization_id:
        result.errors.append("persist_chunk_entities: organization_id and user_id are required")
        return result
    if not engine.name:
        result.errors.append("persist_chunk_entities: the engine must be named")
        return result

    per_chunk_norm: list[tuple[str, list[dict[str, Any]]]] = []
    empty_chunk_ids: list[str] = []
    texts: dict[str, str] = {}
    for ex in extractions:
        texts[ex.chunk_id] = ex.content_text or ""
        norm = _normalize_extracted(ex.entities)
        result.chunks_processed += 1
        if norm:
            per_chunk_norm.append((ex.chunk_id, norm))
        else:
            empty_chunk_ids.append(ex.chunk_id)

    # ─── Tier A.5: big-model finisher (optional, host-injected) ───────────
    # If a host wires a finisher via ``matrx_rag.configure(ner_finisher=...)``
    # we hand it the union of normalized spans from EVERY chunk in this batch
    # along with each chunk's content (for context). The finisher gets ONE
    # shot per call — never one call per chunk — to canonicalise, dedup, and
    # merge cross-chunk co-references. Failure modes are tolerated: if the
    # finisher raises or returns a malformed shape we log loudly and fall back
    # to the raw tier-A spans. NEVER crash a NER pass because the finisher
    # misbehaved.
    finisher = get_ner_finisher()
    if finisher is not None and per_chunk_norm:
        all_spans_in: list[dict[str, Any]] = []
        for chunk_id, norm in per_chunk_norm:
            for ent in norm:
                all_spans_in.append({"chunk_id": chunk_id, **ent})
        chunk_texts = [
            {"chunk_id": cid, "content_text": texts.get(cid, "")} for cid, _ in per_chunk_norm
        ]
        try:
            curated: list[dict[str, Any]] = await finisher(
                all_spans_in,
                chunk_texts,
                organization_id=organization_id,
                user_id=user_id,
                source_kind=source_kind,
                source_id=source_id,
            )
            if not isinstance(curated, list):
                raise TypeError(f"finisher returned {type(curated).__name__}, expected list")
            regrouped: dict[str, list[dict[str, Any]]] = {}
            for ent in curated:
                if not isinstance(ent, dict) or not ent.get("chunk_id"):
                    continue
                kind = str(ent.get("kind") or "").strip().lower()
                name = str(ent.get("name") or ent.get("canonical_name") or "").strip()
                if kind not in NER_KINDS or not name:
                    continue
                regrouped.setdefault(str(ent["chunk_id"]), []).append(
                    {
                        "kind": kind,
                        "name": name,
                        "span_start": _coerce_int(ent.get("span_start")),
                        "span_end": _coerce_int(ent.get("span_end")),
                        "confidence": _coerce_conf(ent.get("confidence")),
                        "attrs": ent.get("attrs") if isinstance(ent.get("attrs"), dict) else {},
                    }
                )
            # A chunk whose finisher output is empty had every span judged
            # noise — it completed with nothing to keep (stamped, never re-run).
            kept: list[tuple[str, list[dict[str, Any]]]] = []
            for cid, _ in per_chunk_norm:
                if regrouped.get(cid):
                    kept.append((cid, regrouped[cid]))
                else:
                    empty_chunk_ids.append(cid)
            per_chunk_norm = kept
        except Exception as exc:  # noqa: BLE001 — finisher failure NEVER aborts the run
            logger.warning(
                "ner.persist_chunk_entities: ner_finisher failed (%s); falling "
                "back to raw tier-A spans for %s/%s",
                exc,
                source_kind,
                source_id,
            )
            result.errors.append(f"finisher_failed: {exc}")

    # ─── Tier B: bulk entity resolution against the partial expression index ─
    # Collect distinct dedup buckets across every chunk in this batch and
    # resolve them in ONE ``KgEntities.bulk_upsert`` whose ``ConflictTarget``
    # renders the ``kg_entities_ner_canonical_idx`` partial expression unique
    # index (see ``_resolve_entities_via_orm``). Sorting buckets
    # deterministically keeps tier-B writes lock-ordered across parallel
    # coordinators.
    distinct_buckets: dict[tuple[str, str], dict[str, Any]] = {}
    for _, norm in per_chunk_norm:
        for ent in norm:
            # First-wins: keep the earliest-seen sample (preserves its attrs).
            distinct_buckets.setdefault(_bucket_key(ent), ent)
    sorted_keys = sorted(distinct_buckets.keys())

    # bucket-key → kg_entities.id. Filled by tier B, read by tier C.
    resolved: dict[tuple[str, str], str] = {}
    if sorted_keys:
        ok = await _resolve_entities_via_orm(
            sorted_keys=sorted_keys,
            distinct_buckets=distinct_buckets,
            organization_id=organization_id,
            created_by=user_id,
            result=result,
            resolved=resolved,
        )
        if not ok:
            # The bulk_upsert raised; the error is on result.errors. Nothing is
            # written and nothing is stamped — every chunk retries.
            return result
        total_raw = sum(len(norm) for _, norm in per_chunk_norm)
        result.entities_reused += max(0, total_raw - result.entities_written)

    # ─── Tier C: parallel per-chunk writes (replace mentions + edges) ─────
    # Each chunk has its own transaction. Entity ids are pre-resolved, so
    # there's no entity-dedup work — only DELETE the chunk's previous mentions
    # and edges, INSERT the new mentions and UPSERT the new edges, touching
    # row-locks scoped to this chunk. Distinct edge pairs are visited in sorted
    # order, so cross-chunk transactions can't form a lock cycle.
    #
    # CONCURRENCY CAP: bounds the number of connections held simultaneously
    # (the 2026-06-03 pool-saturation incident; see _ner_persist_concurrency).
    persist_semaphore = asyncio.Semaphore(_ner_persist_concurrency())
    mention_meta = {"engine": engine.name, "engine_version": engine.version}
    displaced_entity_ids: set[str] = set()
    landed: set[str] = set()

    async def _persist_one_chunk(chunk_id: str, norm: list[dict[str, Any]]) -> None:
        # Map this chunk's entities to ids, dropping any whose bucket failed
        # to resolve in tier B (errored buckets are already in result.errors).
        entity_ids: list[str] = []
        kept_norm: list[dict[str, Any]] = []
        for ent in norm:
            eid = resolved.get(_bucket_key(ent))
            if eid is None:
                continue
            entity_ids.append(eid)
            kept_norm.append(ent)

        # LOCK ORDER (live 40P01, 2026-10-01 22:29Z, chunk a59fb1ff…): two
        # writers of the SAME chunk inserted identical (chunk_id, entity_id,
        # span_start) keys in extractor/span order; each waited on the other's
        # uncommitted key and Postgres killed one. One global order satisfies
        # every writer: the tier-B bucket key, then span.
        mention_rows = _mention_rows_in_lock_order(
            chunk_id=chunk_id,
            organization_id=organization_id,
            mentions=list(zip(kept_norm, entity_ids, strict=True)),
            metadata=mention_meta,
        )
        # Co-occurrence edges — one per unordered distinct-entity pair, sorted
        # (src_id, dst_id): every chunk visits edge rows in the same order.
        distinct_ids = sorted(set(entity_ids))
        pairs: list[tuple[str, str]] = [
            (distinct_ids[a], distinct_ids[b])
            for a in range(len(distinct_ids))
            for b in range(a + 1, len(distinct_ids))
        ]

        async def _write_chunk_once() -> tuple[int, set[str]]:
            # matrx_orm.transaction() binds one connection for the block, so
            # the replace (delete old + write new) lands together or not at
            # all. The semaphore is taken per ATTEMPT so a retry's backoff
            # never holds a slot.
            async with persist_semaphore, transaction(PACKAGE_DB_NAME):
                previous = await _replace_chunk_writes(chunk_id)
                inserted = await _bulk_insert_mentions(mention_rows)
                if pairs:
                    await _bulk_upsert_co_occurs_edges(
                        organization_id=organization_id,
                        source_chunk_id=chunk_id,
                        pairs=pairs,
                    )
                return inserted, previous

        try:
            # The whole transaction is all-or-nothing and idempotent, so a
            # residual lock collision / timeout re-runs it whole.
            inserted_mentions, previous_ids = await retry_on_transient(
                _write_chunk_once,
                attempts=NER_PERSIST_ATTEMPTS,
                base_backoff=0.2,
                jitter_ratio=1.0,
                retry_on=(LockContentionError, QueryTimeoutError, PoolAcquireTimeoutError),
                label=f"ner.persist chunk {chunk_id}",
            )
        except Exception as exc:  # noqa: BLE001
            # Loud, and the chunk stays OUT of succeeded_chunk_ids, so its
            # ner_extracted_at stays NULL and the next run re-extracts it.
            logger.exception(
                "ner.persist_chunk_entities: persist failed for chunk %s (left unmarked "
                "for re-extraction): %s",
                chunk_id,
                exc,
            )
            result.errors.append(f"{chunk_id}: persist_error: {exc}")
            return
        displaced_entity_ids.update(previous_ids)
        result.mentions_written += inserted_mentions
        result.edges_written += len(pairs)
        landed.add(chunk_id)

    await asyncio.gather(
        *(_persist_one_chunk(cid, norm) for cid, norm in per_chunk_norm),
        *(_persist_one_chunk(cid, []) for cid in empty_chunk_ids),
        return_exceptions=True,
    )

    # ─── Tier D: SERIAL confidence_avg recompute (sorted, idempotent) ─────
    # One UPDATE per distinct entity touched in this batch — the new mentions'
    # entities AND the entities whose mentions were replaced — in sorted id
    # order. Recomputing the mean over all mentions is idempotent and
    # path-independent; each entity's UPDATE is its own statement so one
    # failure never orphans the rest (confidence_avg is a cache).
    touched_entity_ids = sorted(set(resolved.values()) | displaced_entity_ids)
    for eid in touched_entity_ids:
        try:
            await _bump_confidence_avg(entity_id=eid)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "ner.persist_chunk_entities: tier-D confidence_avg recompute "
                "failed for entity %s: %s",
                eid,
                exc,
            )
            result.errors.append(f"confidence_avg_error:{eid}: {exc}")

    # ─── Stamp: the chunks that landed are done, by this engine ───────────
    if landed:
        try:
            await _stamp_chunks(sorted(landed), engine)
        except Exception as exc:  # noqa: BLE001
            # The writes landed but the marker did not: the chunks re-extract
            # next run and converge (the replace makes a second pass a no-op in
            # effect). Said out loud, never swallowed.
            logger.exception(
                "ner.persist_chunk_entities: %d chunk(s) landed but could not be stamped "
                "(they will re-extract): %s",
                len(landed),
                exc,
            )
            result.errors.append(f"stamp_error: {exc}")
            return result
        result.succeeded_chunk_ids.update(landed)
    return result


async def _replace_chunk_writes(chunk_id: str) -> set[str]:
    """Delete one chunk's previous mentions and the co-occurrence edges it
    produced, inside the caller's transaction. Returns the entity ids those
    mentions pointed at (tier D recomputes them)."""
    KgChunkEntities = get_db_model("KgChunkEntities")
    KgEdges = get_db_model("KgEdges")
    rows = await KgChunkEntities.filter(chunk_id=chunk_id).values("entity_id")
    previous = {str(r["entity_id"]) for r in rows if r.get("entity_id") is not None}
    if previous:
        await KgChunkEntities.delete_where(chunk_id=chunk_id)
    await KgEdges.delete_where(source_chunk_id=chunk_id, kind="co_occurs_with")
    return previous


async def _stamp_chunks(chunk_ids: list[str], engine: NerEngineStamp) -> None:
    """``ner_extracted_at`` + ``metadata.ner = {engine, version, at}`` on every
    landed chunk — one atomic shallow merge (``JsonbMerge``), sibling metadata
    keys untouched."""
    from datetime import UTC, datetime

    from matrx_orm import JsonbMerge

    now = datetime.now(UTC)
    KgChunks = get_db_model("KgChunks")
    await KgChunks.update_where(
        {"id__in": chunk_ids},
        ner_extracted_at=now,
        metadata=JsonbMerge(
            "metadata",
            {"ner": {"engine": engine.name, "version": engine.version, "at": now.isoformat()}},
        ),
    )


# ── Partial-index ConflictTarget for kg_entities_ner_canonical_idx ──────────
# The partial expression unique index lives in
# ``packages/matrx-rag/matrx_rag/migrations/kg_004_kg_widening.sql``, its
# predicate widened by ``kg_042_ner_kinds_widened.sql``:
#
#   CREATE UNIQUE INDEX kg_entities_ner_canonical_idx
#       ON rag.kg_entities (
#           COALESCE(organization_id, '00000000-...::uuid),
#           kind,
#           lower(name)
#       )
#       WHERE kind IN (<NER_KINDS>);
#
# The ON CONFLICT predicate below names every kind in ``NER_KINDS``; Postgres
# picks an arbiter index only when that predicate IMPLIES the index's own, so
# the live index must list at least these kinds (kg_042 does; the guard is
# aidream ``tests/test_ner_kinds_match_the_live_index.py``).
#
# ``ConflictTarget`` (matrx-orm 2026-06-04) renders the WHERE predicate +
# expression list into the ON CONFLICT clause so ``bulk_upsert`` targets this
# exact index. The list of kinds matches ``NER_KINDS`` above by construction.
async def _resolve_entities_via_orm(
    *,
    sorted_keys: list[tuple[str, str]],
    distinct_buckets: dict[tuple[str, str], dict[str, Any]],
    organization_id: str | None,
    created_by: str | None,
    result: NerResult,
    resolved: dict[tuple[str, str], str],
) -> bool:
    """ORM path for tier B — the only path (the per-bucket SELECT-or-INSERT
    loop it replaced is gone; the package binds its own ``KgEntities``).

    Returns:
        ``True``  — ORM upsert succeeded; ``resolved`` is filled, counters bumped.
        ``False`` — ORM upsert was attempted but raised; ``result.errors`` has
        the detail. Caller should bail out before tier C/D.

    Raises ``RagNotConfiguredError`` (from ``get_db_model``) only when the app
    never configured/bootstrapped matrx-rag at all — loud and correct.
    """
    if not sorted_keys:
        return True

    KgEntities = get_db_model("KgEntities")

    from matrx_orm import ConflictTarget  # noqa: PLC0415

    bucket_rows: list[dict[str, Any]] = []
    for k in sorted_keys:
        sample = distinct_buckets[k]
        bucket_rows.append(
            {
                "organization_id": organization_id,
                # Insert-only (update_fields below is ["kind"]): the person the
                # extraction runs for; the stamp trigger cannot see them here.
                "created_by": created_by,
                "kind": sample["kind"],
                "name": sample["name"],
                "attrs": sample["attrs"] or {},
                # Entity/concept split (STOP rule 7): derive on write so the
                # column is NEVER NULL for a new row. A NULL is_concept silently
                # broke concept-dampening (importance) AND scope-sweep selection
                # (`is_concept = false` skips NULLs) — bug 8ab3572e. Set on
                # INSERT only (kept out of update_fields) so a later refinement
                # pass that deliberately diverges from `kind` is preserved; a DB
                # DEFAULT + trigger backstop covers any writer that forgets.
                "is_concept": sample["kind"] in CONCEPT_KINDS,
            }
        )

    # Pre-query: which buckets already exist? One round-trip per distinct kind
    # lets us report ``entities_written`` / ``entities_reused`` accurately
    # (the old code tracked this via the INSERT-vs-23505-fallback branch).
    # Postgres's ``xmax = 0`` discriminator on RETURNING would let us avoid
    # the pre-query but matrx-orm's bulk_upsert doesn't expose system columns
    # yet; that extension is tracked as a follow-up.
    pre_existing_keys: set[tuple[str, str]] = set()
    try:
        kind_to_lnames: dict[str, list[str]] = {}
        for kind, lname in sorted_keys:
            kind_to_lnames.setdefault(kind, []).append(lname)
        # Per-kind queries keep the SQL simple and let Postgres use the partial
        # index efficiently. Each query is small (one kind per round-trip).
        for kind, lnames in kind_to_lnames.items():
            qb = KgEntities.filter(kind=kind)
            if organization_id is None:
                qb = qb.filter(organization_id__isnull=True)
            else:
                qb = qb.filter(organization_id=organization_id)
            rows = await qb.values("name")
            existing_lowers = {str(r["name"]).lower() for r in rows}
            for lname in lnames:
                if lname in existing_lowers:
                    pre_existing_keys.add((kind, lname))
    except Exception as exc:  # noqa: BLE001
        # Pre-query failed but it's not fatal — the bulk_upsert below is still
        # correct, we just lose accurate written/reused split. Log + continue.
        logger.warning(
            "ner.extract_entities: tier-B preflight count failed (%s); "
            "entities_written counter will approximate",
            exc,
        )

    target = ConflictTarget.partial(
        ["organization_id", "kind", "name"],
        coalesce={"organization_id": UUID(_ORG_SENTINEL)},
        lower=("name",),
        where_in={"kind": tuple(sorted(NER_KINDS))},
    )
    try:
        # ``update_fields=["kind"]`` is a true no-op: ``kind`` is part of the
        # conflict target so EXCLUDED.kind ≡ kg_entities.kind for any conflict.
        # We need DO UPDATE (not DO NOTHING) so RETURNING gives us the row.
        upserted = await KgEntities.bulk_upsert(
            objects_data=bucket_rows,
            update_fields=["kind"],
            on_conflict=target,
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception(
            "ner.extract_entities: ORM tier-B bulk_upsert failed: %s",
            exc,
        )
        result.errors.append(f"resolve_tier_error: {exc}")
        return False

    # Map upserted rows back to the bucket keys we sent in. PostgreSQL
    # preserves VALUES order in RETURNING, so a positional zip is correct.
    for key, row in zip(sorted_keys, upserted):
        if row is None:
            continue
        # Model attribute access — ``id`` is hydrated from RETURNING *.
        resolved[key] = str(getattr(row, "id"))
        if key not in pre_existing_keys:
            result.entities_written += 1
    return True


async def _bump_confidence_avg(*, entity_id: str) -> None:
    """Recompute confidence_avg as the mean confidence across all mentions of
    the entity. Cheap (entities have few mentions); always correct vs. an
    incremental running-average that drifts when mentions are deleted on
    re-ingest CASCADE.

    Single-statement atomicity (the SELECT and the SET must not be split
    into a read-then-write — a concurrent mention write between the two
    would race) via the ``update(col=Subquery(...))`` primitive
    (``matrx_orm.query.executor`` + ``BASE_CLASS_METHODS.md``): renders
    ``UPDATE rag.kg_entities SET confidence_avg = (SELECT avg(confidence)
    FROM rag.kg_chunk_entities WHERE entity_id = kg_entities.id AND
    confidence IS NOT NULL) WHERE id = $1`` — identical shape to the raw SQL
    it replaces.
    """
    from matrx_orm import Avg, Now, OuterRef, Subquery  # noqa: PLC0415

    KgEntities = get_db_model("KgEntities")
    KgChunkEntities = get_db_model("KgChunkEntities")

    avg_subq = Subquery(
        KgChunkEntities.filter(entity_id=OuterRef("id"), confidence__isnull=False)
        .annotate(avg_conf=Avg("confidence"))
        .select("avg_conf")
    )
    await KgEntities.update_where(
        {"id": entity_id},
        confidence_avg=avg_subq,
        updated_at=Now(),
    )


async def _bulk_insert_mentions(
    rows: list[dict[str, Any]],
) -> int:
    """Bulk INSERT every ``kg_chunk_entities`` row for one chunk in one
    round-trip. Returns the count of rows that actually landed.

    Idempotency: ``ON CONFLICT (chunk_id, entity_id, span_start) DO NOTHING``
    handles the kg_006 re-NER path — if the prior NER pass already wrote a
    subset of rows before failing, the second pass silently skips those.
    The conflict shape matches ``UNIQUE (chunk_id, entity_id, span_start)``
    declared in ``0003_rag_schema.sql``.
    """
    if not rows:
        return 0

    # No explicit connection= — the caller wraps this call in
    # ``async with transaction(PACKAGE_DB_NAME):``, which binds the active
    # connection to a ContextVar that AsyncDatabaseManager.execute_write
    # reads automatically. So atomicity (mentions + edges land together),
    # the sorted-pair lock ordering, and the persist-semaphore connection
    # bound (the 2026-06-03 pool-saturation guard) are ALL preserved
    # byte-for-byte vs. the raw SQL this replaced.
    KgChunkEntities = get_db_model("KgChunkEntities")
    await KgChunkEntities.bulk_insert_ignore(
        objects_data=rows,
        on_conflict=["chunk_id", "entity_id", "span_start"],
    )
    # Approximate count (pre-ON-CONFLICT filter) — re-NER collisions are rare
    # enough that this is fine for the result-summary use case.
    return len(rows)


async def _bulk_upsert_co_occurs_edges(
    *,
    organization_id: str | None,
    source_chunk_id: str,
    pairs: list[tuple[str, str]],
) -> None:
    """Bulk-upsert every ``co_occurs_with`` edge for one chunk in a single
    round-trip.

    The ``kg_007_co_occurs_unique`` partial unique index on
    ``(source_chunk_id, src_id, dst_id) WHERE kind='co_occurs_with'`` lets us
    fold the old O(N²) per-pair ``UPDATE`` then ``INSERT`` pattern into one
    ``INSERT ... VALUES (...), (...), ...`` with ``ON CONFLICT ... DO UPDATE
    SET weight = weight + 1``. The semantics are identical: the first pass
    inserts with weight=1; a subsequent pass for the same chunk (re-NER
    scenario) bumps weight, never duplicating the row.

    Lock ordering: the pair list MUST be sorted by ``(src_id, dst_id)`` before
    calling this (the caller does so). All chunks then touch the same edge
    row-locks in canonical order, so concurrent chunks can't cycle on each
    other.
    """
    if not pairs:
        return

    # As with mentions, no explicit connection= — the caller's
    # ``transaction(PACKAGE_DB_NAME)`` block binds the active connection, so
    # the weight bump stays atomic with the mentions write and the
    # sorted-pair lock order (set by the caller) is unchanged. The
    # partial-index ConflictTarget mirrors ``kg_007_co_occurs_unique`` (the
    # same index the raw SQL it replaced targeted).
    KgEdges = get_db_model("KgEdges")
    from matrx_orm import ConflictTarget  # noqa: PLC0415

    edge_rows = [
        {
            "organization_id": organization_id,
            "src_id": src_id,
            "dst_id": dst_id,
            "kind": "co_occurs_with",
            "weight": 1,
            "source_chunk_id": source_chunk_id,
            "attrs": {},
        }
        for (src_id, dst_id) in pairs
    ]
    await KgEdges.bulk_upsert_increment(
        objects_data=edge_rows,
        on_conflict=ConflictTarget.partial(
            ["source_chunk_id", "src_id", "dst_id"],
            where_equals={"kind": "co_occurs_with"},
        ),
        increments={"weight": 1},
    )


__all__ = [
    "CONCEPT_KINDS",
    "NER_KINDS",
    "ChunkExtraction",
    "NerChunkInput",
    "NerEngine",
    "NerEngineStamp",
    "NerResult",
    "extract_entities",
    "persist_chunk_entities",
    "resolve_ner_engine",
]
