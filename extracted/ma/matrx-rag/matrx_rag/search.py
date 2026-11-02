"""Hybrid retrieval — vector + lexical + entity, RRF-fused, optionally reranked.

Pipeline::

    query
      → embed (per provider; one query → one query vector per index)
      → vector recall (top 100, HNSW cosine, ACL-filtered)
      → lexical recall (top 100, websearch_to_tsquery + ts_rank, ACL-filtered)
      → entity recall (KG entity match → chunk co-occurrence, org-visible only)
      → RRF fusion (rank-based, k=60, per-lane weights)
      → optional host cross-encoder rerank over fused candidates → reordered top N
      → entity map sidecar (per-hit entity names + condensed map for agents)
      → audit row written to rag.retrieval_audit

The fusion uses **Reciprocal Rank Fusion** (Cormack et al. 2009):

    score(d) = Σ over rankers r:  1 / (k + rank_r(d))

with k=60. This sidesteps score-normalization issues between cosine
similarity (0..1) and ts_rank (unbounded). RRF is the SoTA default.

Reranking: when the host wires a cross-encoder reranker, the top ~50 fused
candidates are sent to the host-selected model and the cross-encoder relevance
score replaces the RRF score for the final ordering. If that optional host
capability is absent or errors, fusion ranking stands.

ACL: ``build_visibility_predicate`` — rebased on the kernel (2026-09-27): a chunk is
readable when ``iam.accessible_entity_ids`` / ``iam.has_access_for`` says its document
is, plus the global library lane and data-store grants. The selected organization never
decides reach (2026-09-23).

Trash: the recall doors (``rag.recall_*``) never return a chunk whose origin record or Source
is in Trash — ``rag._chunk_trash_predicate_sql``, derived from the registry, decided at read
time so a restore brings it back (2026-10-04; guard
``tests/test_trashed_records_leave_passage_search_live.py``).
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

from matrx_orm import (
    Case,
    Cast,
    ColumnComparison,
    F,
    Is,
    Projection,
    Sum,
    When,
    acquire_connection,
)
from matrx_utils import capture_error, supervised_task

from matrx_rag._ext import get_db_model, get_reranker
from matrx_rag.db import PACKAGE_DB_NAME
from matrx_rag.embeddings import (
    default_text_model,
    embed,
    spec_for,
)
from matrx_rag.llm import expand_query, hyde_passage
from matrx_rag.rerank_cache import cached_rerank

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Tunables
# ---------------------------------------------------------------------------

VECTOR_RECALL_K = 100
LEXICAL_RECALL_K = 100
RRF_K = 60
RERANK_INPUT = 50  # Cohere rerank input cap
DEFAULT_LIMIT = 20
MAX_LIMIT = 100
# HyDE blend weight in RRF — the hypothetical answer is plausible-but-
# fabricated content, so its ranking gets ~3x less influence than the
# raw query and multi-query paraphrases (which preserve user intent
# verbatim). Tuned in code, not via env: the RAG_HYDE_RRF_WEIGHT override
# was deliberately removed from the prod path so a stray env var can never
# silently re-tune retrieval. Change it here and push.
HYDE_RRF_WEIGHT_DEFAULT = 0.3

# Entity recall lane tunables.
# Weight applied to the entity-recall ranking in RRF fusion. Lower than
# the default 1.0 so entity co-occurrence boosts but does not dominate
# vector/lexical intent signals.
_ENTITY_LANE_RRF_WEIGHT = 0.8
# Max entities matched from kg_entities for a single query.
_ENTITY_MATCH_LIMIT = 20
# Cluster-expansion cap: when expand_entity_clusters is on, at most this many
# same-kind sibling entities (from the matched entities' clusters) are added to
# the chunk-co-occurrence step. Bounded so a large theme cluster can't flood the
# entity lane. Recall-broadening — OFF by default (per-request opt-in) because
# turning it on for everyone is an eval decision, not a blind default.
_ENTITY_CLUSTER_EXPANSION_CAP = 40
# Max chunks pulled from kg_chunk_entities for all matched entities.
_ENTITY_CHUNK_LIMIT = 100
# Minimum token length to be included in the term set for entity matching.
_ENTITY_MIN_TERM_LEN = 3
# Maximum number of query tokens to use for entity matching (ordered, deduped).
_ENTITY_MAX_TERMS = 8
# Minimum chunk body length (chars) for the entity-recall lane. The lane ranks
# by entity co-occurrence COUNT, so a 3-word title ("Review the contract") that
# merely mentions a matched entity scores identically to a 1500-char passage
# that mentions it — and, with no tiebreak, could sort ABOVE it non-
# deterministically and reach the rerank window. Gating on a small minimum keeps
# trivial titles out of the lane entirely; substantive content still surfaces via
# the entity lane, and a short-but-relevant chunk can still arrive via the
# vector / lexical lanes.
_ENTITY_MIN_CONTENT_CHARS = 40

# Entity map sidecar tunables.
# Max entities in the condensed map returned alongside hits.
_ENTITY_MAP_LIMIT = 15
# Max linked neighbour entities per map entry (top-N by edge weight).
_ENTITY_MAP_LINKS = 3
# Max entity names attached to each SearchHit (top-N by per-chunk mention count).
_HIT_ENTITY_LIMIT = 5

# Entity importance reranking — Phase 3.0 (Stage 3 of the knowledge pipeline).
# After RRF fusion + priority boost, chunks carrying high-importance entities
# get a multiplicative score boost. The boost sum is capped so a single
# very-important entity can't overwhelm text-relevance signals entirely.
#
# Formula (per chunk):
#   boosted_score = score * (1 + _IMPORTANCE_RERANK_SCALE * min(boost_sum, 3.0))
#   where boost_sum = sum(entity.importance for entity in chunk.entities)
#
# This is a strict NO-OP when importance is NULL or 0 (newly-ingested, unscored
# entities) — those chunks are unaffected.
_IMPORTANCE_RERANK_SCALE = 0.15
_IMPORTANCE_BOOST_CAP = 3.0

# Scope pairing: chunk source_kind -> the platform.associations.source_type tokens a
# scope edge may carry for a chunk of that kind.
#
# DERIVED, never hand-listed (2026-09-26: the hand list keyed "scraped" while web
# chunks carry "scrape_parsed_page"/"web_page", so every scoped search silently
# dropped all ~19k web chunks). Every kind a chunk can carry pairs with ITSELF —
# a registry kind's chunk kind IS its platform.entity_types token — plus the
# legacy spellings older clients wrote. ``CHUNK_SOURCE_KINDS`` is the database's
# kg_chunks ``source_kind_known`` CHECK set; the host test
# ``tests/test_scope_filter_covers_every_chunk_kind.py`` fails when that CHECK, the
# Sources door's landable kinds, or this pairing drift apart.
#
# cx_message is deliberately unlinked: scope edges tag the conversation while
# chunks carry message ids — a correct join goes through the message's
# conversation_id and was deferred.
#: Source kinds the landing door writes onto processed documents (legacy ∪ registry
#: kinds; the host's ``landing_types.DOCUMENT_SOURCE_KINDS``).
DOCUMENT_CHUNK_SOURCE_KINDS: frozenset[str] = frozenset(
    {"cld_file", "inline", "legacy", "external_url", "note", "code_file",
     "scrape_parsed_page", "web_page", "transcript"}
)


def _package_written_kinds() -> frozenset[str]:
    import typing

    from matrx_rag.sources import SourceKind

    return frozenset(typing.get_args(SourceKind))


#: Every kind a chunk row may carry (== the ``kg_chunks_source_kind_known`` CHECK).
CHUNK_SOURCE_KINDS: frozenset[str] = DOCUMENT_CHUNK_SOURCE_KINDS | _package_written_kinds()

_SCOPE_UNLINKED_CHUNK_KINDS: frozenset[str] = frozenset({"cx_message"})

#: Extra (legacy / plural / predecessor) tokens scope edges were written with.
_SCOPE_LEGACY_ALIAS_TOKENS: dict[str, tuple[str, ...]] = {
    "note": ("notes",),
    "cld_file": ("file", "files", "user_files"),
    "transcript": ("transcripts",),
    "task": ("ctx_tasks", "tasks"),
    "project": ("ctx_projects", "projects"),
    "scraped": ("scrape_parsed_page",),
    "scrape_parsed_page": ("scraped",),
}

_SCOPE_ENTITY_TYPE_ALIASES: dict[str, tuple[str, ...]] = {
    kind: (kind, *_SCOPE_LEGACY_ALIAS_TOKENS.get(kind, ()))
    for kind in sorted(CHUNK_SOURCE_KINDS - _SCOPE_UNLINKED_CHUNK_KINDS)
}

#: A Source (``docproc.processed_documents`` row) tagged into a scope. It reaches its
#: chunks by ``c.processed_document_id`` AND by its origin (source_kind, source_id) —
#: re-landing the same origin mints a sibling document whose chunks carry the origin.
SCOPE_SOURCE_DOCUMENT_TOKEN = "processed_document"


def _hyde_rrf_weight() -> float:
    # Code constant — env override intentionally removed (see HYDE_RRF_WEIGHT_DEFAULT).
    return HYDE_RRF_WEIGHT_DEFAULT


# Cohere rerank confidence floor. The cross-encoder is authoritative for
# ORDERING GOOD candidates, but when the best score in the whole window is
# below this floor the query matched nothing well — and the relative order of
# uniformly-bad candidates is noise, not judgment. In that regime a
# superficial keyword overlap (e.g. a title containing one query word) can
# "win" at 0.10 and override a saner RRF order. Below the floor we keep the
# fused RRF ordering and report reranker_model=None (rerank was attempted but
# not used). Cohere rerank scores are normalized to [0,1]; < 0.25 across an
# entire 50-candidate window reliably means "no confident match". Floor was
# tuned on v3.5's distribution — after the v4.0-pro upgrade, re-check against
# rag.retrieval_audit rerank_scores and adjust if v4 calibrates differently.
#
# Deliberately NOT paired with an entry floor on the rerank window: cutting
# low-RRF candidates out of Cohere's input would amputate the reranker's whole
# job (rescuing chunks the bi-encoder/lexical lanes underrated). The observed
# entity-lane failure mode is handled at the source (_ENTITY_MIN_CONTENT_CHARS)
# plus this output-side floor.
RERANK_CONFIDENCE_FLOOR = 0.25


def _rerank_is_confident(
    rerank_scores: dict[str, float],
    *,
    floor: float = RERANK_CONFIDENCE_FLOOR,
) -> bool:
    """True when the rerank window contains at least one confident match —
    i.e. Cohere's ordering is worth overriding the fused RRF order for."""
    if not rerank_scores:
        return False
    return max(rerank_scores.values()) >= floor


# THE HONESTY FLOOR (law: "nothing fails silently"). RERANK_CONFIDENCE_FLOOR
# above only decides whether to TRUST Cohere's ordering; it never decided what
# to RETURN, so an out-of-domain query still got the top-k of whatever corpus
# the caller could see, dressed as a success. That is the defect class behind
# feedback 2985b3aa (a Telegram/MEXC trading-bot query answered with NIST CSF
# 2.0 PDF chunks, re-called 19 times in one turn because every "success" was
# useless). Below this floor the honest answer is an EMPTY result that states
# the floor — never a ranked list of the least-bad garbage.
#
# Calibrated 2026-09-09 against the live corpus (rerank-v4.0-pro), read-only:
#   out-of-domain  "parse_signal" vs the NIST/CISA library ......... 0.342-0.364
#   out-of-domain  "templates index.html balance" vs same ......... 0.246-0.261
#   out-of-domain  "telegram_worker.py main loop ..." vs same ..... 0.0156-0.0164
#   IN-domain      "incident response log sources ..." vs same .... 0.786-0.920
#   IN-domain      "parse_signal" vs the trading-bot case corpus .. 0.901-0.936
# 0.45 sits in the empty band between the out-of-domain ceiling (0.364) and the
# in-domain floor (0.786), with margin on both sides.
#
# KNOB: a behavioral choice, so it belongs in the unified settings platform as
# an org-configurable row ("opinions become knobs"). Until that registration
# lands it is this constant — the starting value an agent set, not taste baked
# into the engine forever. Per-call override: search(relevance_floor=...).
RELEVANCE_FLOOR = 0.45

# What the relevance gate concluded, surfaced on SearchResponse so every caller
# can tell the three cases apart instead of guessing from an empty hit list:
#   "scored"              - hits were graded by the cross-encoder and survived
#                           the floor; what you got is genuinely relevant.
#   "no_relevant_matches" - hits were graded and NONE reached the floor. The
#                           corpus has nothing for this query. Re-calling with
#                           the same query returns the same nothing.
#   "unscored"            - no cross-encoder score was available (rerank
#                           disabled, no host reranker is wired, or the call errored),
#                           so relevance could not be judged and the floor was
#                           NOT applied. Results are fused-rank order only.
RELEVANCE_VERDICT_SCORED = "scored"
RELEVANCE_VERDICT_NONE = "no_relevant_matches"
RELEVANCE_VERDICT_UNSCORED = "unscored"
#   "weak_matches_only"   - hits were graded and NONE reached the floor, and the
#                           caller asked to keep the best few anyway
#                           (``search(keep_weak=N)``): every hit carries
#                           ``weak=True``. Never the default — an agent caller
#                           keeps the honest empty result (feedback 2985b3aa).
RELEVANCE_VERDICT_WEAK = "weak_matches_only"


def _apply_relevance_floor(
    ordered: list[str],
    relevance_scores: dict[str, float],
    *,
    floor: float,
    limit: int,
) -> tuple[list[str], str, float | None, int]:
    """Gate the final ordering on calibrated relevance.

    Returns ``(ordered, verdict, floor_applied, dropped_from_window)``. With no
    cross-encoder scores the gate is a NO-OP that says so (``unscored``) rather
    than silently pretending the results were vetted.
    """
    if not relevance_scores:
        return (ordered, RELEVANCE_VERDICT_UNSCORED, None, 0)
    kept = [cid for cid in ordered if relevance_scores.get(cid, 0.0) >= floor]
    kept_set = set(kept)
    pre_floor_window = ordered[:limit]
    dropped = sum(1 for cid in pre_floor_window if cid not in kept_set)
    verdict = RELEVANCE_VERDICT_SCORED if kept else RELEVANCE_VERDICT_NONE
    return (kept, verdict, floor, dropped)


def _keep_weak_matches(
    pre_floor: list[str],
    kept: list[str],
    verdict: str,
    *,
    keep_weak: int,
) -> tuple[list[str], str, set[str]]:
    """When the floor dropped EVERY graded candidate and the caller asked, keep the best few.

    Live 2026-10-24 (Memory search): scores of 0.56 vs 0.67 against the floor decided between
    0 and 20 rows, so one query showed nothing and the same words reordered showed a page. A
    person-facing caller asks for the best ``keep_weak`` back, each marked weak, instead of
    nothing. Returns ``(ordered, verdict, weak_ids)``.
    """
    if verdict != RELEVANCE_VERDICT_NONE or keep_weak <= 0 or not pre_floor:
        return (kept, verdict, set())
    weak = pre_floor[:keep_weak]
    return (weak, RELEVANCE_VERDICT_WEAK, set(weak))


MMR_DEFAULT_THRESHOLD = 0.72  # Jaccard similarity above this → drop as duplicate
# Phase 2.0b — priority-aware ranking. priority=0 (the default for raw
# chunks) leaves scores unchanged, so this is identity for any chunk
# that hasn't been written by an agent-extract pipeline. Tunable per-
# Tuned in code (constant below), not via env. Set to 0 to disable the scale.
PRIORITY_BOOST_SCALE_DEFAULT = 0.05
# FEATURE TOGGLE (code-reviewed, not an env var): priority-aware rerank.
# Default ON; the identity case (all priority=0) is a strict no-op, so flipping
# off only matters if a regression introduces drift. (Was RAG_USE_PRIORITY_BOOST.)
PRIORITY_BOOST_ENABLED: bool = True
# Cap on how many fused candidates we look up priorities for. We only
# need priorities for chunks that COULD enter the rerank window. Because
# stage-1 boost can promote a chunk by ~2x, a chunk at fused rank
# RERANK_INPUT*2 could plausibly leap into the top-50 — call it 4x for
# headroom. PRIORITY_FETCH_CAP = max(RERANK_INPUT * 4, 200) gives 200
# today and scales if the rerank window grows.
PRIORITY_FETCH_CAP = max(RERANK_INPUT * 4, 200)


def _priority_boost_scale() -> float:
    return PRIORITY_BOOST_SCALE_DEFAULT


def _priority_boost_enabled() -> bool:
    return PRIORITY_BOOST_ENABLED


def _apply_priority(score: float, priority: int) -> float:
    """Multiply a similarity / rerank score by ``1 + scale * priority``.

    Priority 0 returns ``score`` unchanged. Positive priority boosts the
    score; negative demotes. Scale is small (0.05) so priority=20 yields
    a 2x boost — large enough to flip ties, small enough that a
    significantly more-relevant raw chunk still wins.
    """
    if not priority:
        return score
    if not _priority_boost_enabled():
        return score
    scale = _priority_boost_scale()
    return score * (1.0 + scale * float(priority))


def _apply_entity_importance(score: float, importance_sum: float) -> float:
    """Multiply a fused score by the entity-importance boost factor.

    Formula: score * (1 + _IMPORTANCE_RERANK_SCALE * min(importance_sum, cap))

    A chunk dense with high-importance (distinctive) entities outranks a
    marginally-closer generic passage — the "trust-weighted + entity-weighted"
    retrieval vision.

    Strict NO-OP when importance_sum is 0 (NULL-importance entities or a chunk
    with no KG entities). This preserves existing behavior for newly-ingested
    unscored content.
    """
    if not importance_sum:
        return score
    boost_sum = min(importance_sum, _IMPORTANCE_BOOST_CAP)
    return score * (1.0 + _IMPORTANCE_RERANK_SCALE * boost_sum)


# ---------------------------------------------------------------------------
# Scope filter helpers
# ---------------------------------------------------------------------------


_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def _validate_scope_ids(scope_ids: list[str] | None) -> list[str] | None:
    """Drop any id that is not a valid UUID. Returns None if input is None."""
    if scope_ids is None:
        return None
    valid = [sid for sid in scope_ids if _UUID_RE.match(sid)]
    return valid if valid else []


def _normalize_source_ids(source_ids: list[str] | None) -> list[str] | None:
    """Trim/dedupe source_ids, dropping blanks. Returns None if input is None.

    Unlike scope_ids these are NOT required to be UUIDs (source_id is a text column
    that can carry non-UUID ids for some source kinds), so we only strip + dedupe.
    Returns [] when a non-None input had no usable ids → fail-closed empty response.
    """
    if source_ids is None:
        return None
    out: list[str] = []
    seen: set[str] = set()
    for sid in source_ids:
        s = str(sid).strip()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out  # may be [] → caller short-circuits to an empty response


def _normalize_processed_document_ids(
    processed_document_ids: list[str] | None,
) -> list[str] | None:
    """Validate/dedupe processed-document UUIDs; invalid explicit scope fails closed."""
    if processed_document_ids is None:
        return None
    out: list[str] = []
    seen: set[str] = set()
    for value in processed_document_ids:
        document_id = str(value).strip()
        if _UUID_RE.match(document_id) and document_id not in seen:
            seen.add(document_id)
            out.append(document_id)
    return out


def _build_scope_filter_predicate(
    scope_ids: list[str], document_ids: list[str] | None = None
):
    from matrx_orm import ArrayAny, Cast, Compare, Exists, OuterRef

    # Every chunk column is named through the ``c`` alias, never OuterRef: in the
    # vector lane the base table is the embedding table (kg_chunks is joined as
    # ``c``), and a bare OuterRef renders against the base — every scoped vector
    # search crashed on "embeddings_*.source_id does not exist" (2026-09-27).
    Associations = get_db_model("Associations")
    kind_predicate = None
    for source_kind, entity_types in _SCOPE_ENTITY_TYPE_ALIASES.items():
        branch = Compare(F("c.source_kind"), "=", source_kind) & ArrayAny(
            F("source_type"), list(entity_types), cast="text[]"
        )
        kind_predicate = branch if kind_predicate is None else kind_predicate | branch
    assert kind_predicate is not None
    direct_edge = Exists(
        Associations.filter(
            Compare(F("target_type"), "=", "scope"),
            ArrayAny(F("target_id"), scope_ids, cast="uuid[]"),
            Compare(Cast(F("source_id"), "text"), "=", F("c.source_id")),
            Is(
                F("deleted_at"), None
            ),  # live edges only — a tombstoned edge (endpoint trashed) is not a link (D135)
            kind_predicate,
        )
    )

    def _document_edge():
        return Associations.filter(
            Compare(F("target_type"), "=", "scope"),
            ArrayAny(F("target_id"), scope_ids, cast="uuid[]"),
            Compare(F("source_type"), "=", SCOPE_SOURCE_DOCUMENT_TOKEN),
            Is(F("deleted_at"), None),
        )

    # A scoped Source reaches the chunks written for it ...
    document_by_id = Exists(
        _document_edge().filter(
            Compare(F("source_id"), "=", F("c.processed_document_id"))
        )
    )
    # ... and the chunks of its origin (a re-landed origin mints a sibling document).
    ProcessedDocuments = get_db_model("ProcessedDocuments")
    document_by_origin = Exists(
        ProcessedDocuments.filter(
            Compare(F("source_kind"), "=", F("c.source_kind")),
            Compare(F("source_id"), "=", F("c.source_id")),
            Is(F("deleted_at"), None),
            Exists(_document_edge().filter(Compare(F("source_id"), "=", OuterRef("id")))),
        )
    )
    predicate = direct_edge | document_by_id | document_by_origin
    if not scope_ids:
        predicate = None
    if document_ids:
        # Sources named directly (filed under the caller's project): their own
        # chunks, and the chunks of their origin, like a scoped Source.
        named = ArrayAny(F("c.processed_document_id"), document_ids, cast="uuid[]") | Exists(
            ProcessedDocuments.filter(
                Compare(F("source_kind"), "=", F("c.source_kind")),
                Compare(F("source_id"), "=", F("c.source_id")),
                Is(F("deleted_at"), None),
                ArrayAny(F("id"), document_ids, cast="uuid[]"),
            )
        )
        predicate = named if predicate is None else predicate | named
    assert predicate is not None, "scope filter needs scope ids or document ids"
    return predicate


def _source_id_predicate(source_ids: list[str]):
    """Build the file-scoped filter clause restricting to specific source rows.

    Restricts kg_chunks to those whose ``source_id`` (text) is in ``source_ids`` —
    e.g. cld_file file_ids for a thread's attached files. source_kind-agnostic by
    design (a file_id only matches its own chunks), AND-ed with the ACL so a source the
    caller can't see is still never returned. The id array is a bound param — never
    interpolated.

    Returns ``(sql_fragment, params)`` where the fragment references ``${next_param_idx}``.
    """
    from matrx_orm import ArrayAny

    return ArrayAny(F("c.source_id"), source_ids, cast="text[]")


def _processed_document_id_predicate(processed_document_ids: list[str]):
    """Bound filter for the exact base/derivative document family requested."""
    from matrx_orm import ArrayAny

    return ArrayAny(F("c.processed_document_id"), processed_document_ids, cast="uuid[]")


def _leaf_chunk_predicate(*, chunk_alias: str = "c"):
    from matrx_orm import Compare, Exists

    KgChunks = get_db_model("KgChunks")
    child_exists = Exists(
        KgChunks.filter(
            # Vector recall starts from an embedding table and joins chunks as
            # ``c``. An unqualified OuterRef("id") binds to that embedding
            # table, which has ``chunk_id`` but deliberately has no ``id``.
            Compare(F("parent_chunk_id"), "=", F(f"{chunk_alias}.id")),
            Is(F("valid_to"), None),
            Is(F("deleted_at"), None),
        ).from_alias("ch")
    )
    return Is(F("c.parent_chunk_id"), None, negated=True) | ~child_exists


# ---------------------------------------------------------------------------
# Data shapes
# ---------------------------------------------------------------------------


@dataclass
class SearchHit:
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
    metadata: dict[str, object] = field(default_factory=dict)
    # Phase 2.0 provenance + priority — populated for chunks produced by
    # agent-extract pipelines; None / 0 for legacy raw chunks. The FE can
    # use these to render distinct cards for agent-extracted hits and to
    # link back to the source extraction run.
    priority: int = 0
    derivation_kind: str = "initial_extract"
    agent_id: str | None = None
    extraction_run_id: str | None = None
    extraction_result_id: str | None = None
    processed_document_id: str | None = None
    primary_page_id: str | None = None
    page_numbers: list[int] = field(default_factory=list)
    # KG entity lane — populated when entity recall is active.
    entity_rank: int | None = None
    # Top entity names (by mention count) present in this chunk.
    entities: list[str] = field(default_factory=list)
    # The Source's name (processed document), read in the same batched candidate read.
    source_name: str | None = None
    # The heading the chunk sits under (its primary page's section title), same read.
    section_title: str | None = None
    # True when the relevance gate graded this hit below the floor and it is shown only because
    # nothing passed and the caller asked for the best few (``search(keep_weak=N)``).
    weak: bool = False
    # The same passage text found in OTHER sources, collapsed into this hit (best-ranked kept):
    # ``{chunk_id, source_kind, source_id, processed_document_id, source_name}`` each.
    also_in: list[dict[str, object]] = field(default_factory=list)


@dataclass
class EntityMapLink:
    """A linked neighbour entity in the condensed entity map."""

    entity_id: str
    name: str
    kind: str
    weight: float


@dataclass
class EntityMapEntry:
    """One entity in the condensed entity map sidecar."""

    entity_id: str
    name: str
    kind: str
    mention_count: int
    artifact_count: int
    source_kind_counts: dict[str, int]
    top_chunk_id: str | None
    linked: list[EntityMapLink]
    # Stage 3 importance — org-percentile distinctiveness score in [0, 1].
    # NULL until score_importance_for_org has run for the org. Defaults
    # here are backward-compatible (existing callers see 0-scored entities
    # rather than errors; the API layer threads these through separately).
    importance: float | None = None
    is_concept: bool = False


@dataclass
class SearchResponse:
    query: str
    hits: list[SearchHit]
    total_candidates: int
    embedding_model: str
    reranker_model: str | None
    latency_ms: int
    # KG entity lane — names matched by the entity recall lane (empty when
    # no entity queries were made or no entities matched).
    matched_entities: list[str] = field(default_factory=list)
    # Condensed entity map for agents. Empty when include_entity_map=False
    # or when entity map queries fail.
    entity_map: list[EntityMapEntry] = field(default_factory=list)
    # Per-lane recall sizes (distinct chunk candidates each lane surfaced
    # BEFORE fusion). Real counts — the diagnostics UI shows these so the
    # "see every layer" promise is honest rather than echoing total_candidates
    # back as a fake per-lane number. 0 when the lane found nothing / ran.
    vector_candidates: int = 0
    lexical_candidates: int = 0
    entity_candidates: int = 0
    # What happened to the rerank stage, so callers can distinguish the ways
    # reranker_model can be None instead of guessing:
    #   "applied"        — Cohere ran and its ordering was used
    #   "low_confidence" — Cohere ran but every candidate scored below
    #                      RERANK_CONFIDENCE_FLOOR; fused RRF order kept
    #   "failed"         — host reranker call errored; fused RRF order kept
    #   "timeout"        — the caller's rerank_timeout_s passed; fused RRF order kept
    #   "off"            — rerank disabled / no host reranker / no candidates
    rerank_status: str = "off"
    # Why rerank did not apply when rerank_status is "failed" / "timeout" (a sentence).
    rerank_error: str | None = None
    # THE HONESTY CONTRACT (see RELEVANCE_FLOOR). `hits` is already gated on
    # relevance; these three say WHY it looks the way it does, so no caller has
    # to guess whether an empty list means "nothing relevant exists" or "the
    # search broke". One of RELEVANCE_VERDICT_{SCORED,NONE,UNSCORED}.
    relevance_verdict: str = RELEVANCE_VERDICT_UNSCORED
    # The floor actually applied, or None when relevance could not be judged.
    relevance_floor: float | None = None
    # How many candidates in the pre-floor top-`limit` window were dropped for
    # scoring below the floor — the count of garbage hits we used to return.
    below_floor_dropped: int = 0


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


#: Query embeddings, remembered briefly so the submit that follows as-you-type reuses the
#: vectors instead of paying the embedding round trip again (Knowledge Hub H1). A query
#: vector is a pure function of (model, text) — nothing access-sensitive is cached.
_QUERY_EMBED_TTL_S = 300.0
_QUERY_EMBED_MAX = 512
_query_embed_cache: dict[tuple[str, tuple[str, ...]], tuple[float, list[list[float]]]] = {}


async def _embed_query_cached(
    model: str, texts: list[str], *, organization_id: str | None
) -> list[list[float]]:
    key = (model, tuple(texts))
    now = time.monotonic()
    hit = _query_embed_cache.get(key)
    if hit is not None and hit[0] > now:
        return hit[1]
    vecs = await embed(model, texts, input_type="query", organization_id=organization_id)
    if vecs:
        if len(_query_embed_cache) >= _QUERY_EMBED_MAX:
            for stale in sorted(_query_embed_cache, key=lambda k: _query_embed_cache[k][0])[: _QUERY_EMBED_MAX // 4]:
                _query_embed_cache.pop(stale, None)
        _query_embed_cache[key] = (now + _QUERY_EMBED_TTL_S, vecs)
    return vecs


async def search(
    query: str,
    *,
    user_id: str | None,
    organization_id: str | None = None,
    source_kinds: list[str] | None = None,
    include_sources: list[dict[str, str]] | None = None,
    limit: int = DEFAULT_LIMIT,
    embedding_models: list[str] | None = None,
    rerank: bool = True,
    only_children: bool = True,
    record_audit: bool = True,
    use_mmr: bool = True,
    mmr_threshold: float = MMR_DEFAULT_THRESHOLD,
    multi_query: int = 1,
    use_hyde: bool = False,
    library_filter: str = "any",  # "any" | "library_only" | "exclude_library"
    is_admin: bool = False,
    admin_bypass_acl: bool = False,
    scope_ids: list[str] | None = None,
    source_ids: list[str] | None = None,
    processed_document_ids: list[str] | None = None,
    scope_document_ids: list[str] | None = None,
    include_entity_map: bool = True,
    expand_entity_clusters: bool = False,
    relevance_floor: float | None = None,
    readable: ReadableDocuments | None = None,
    on_fused: Any = None,
    rerank_timeout_s: float | None = None,
    rerank_input_large: int | None = None,
    rerank_input: int | None = None,
    keep_weak: int = 0,
) -> SearchResponse:
    """Run hybrid retrieval for ``query``.

    Parameters
    ----------
    user_id : str | None
        Required for any retrieval: reach is this person's ownership, her
        memberships (every organization she belongs to), grants and the global lane.
    organization_id : str | None
        The organization this search is ATTRIBUTED to (embedding spend, audit).
        It never narrows or widens what the person may reach (2026-09-23).
    source_kinds : list[str] | None
        e.g. ``["note", "code_file"]``. None = all sources.
    include_sources : list[dict[str, str]] | None
        Hard-scope to specific (source_kind, source_id) pairs. Each dict
        has ``source_kind`` + ``source_id``. Used by the data-stores tool
        to bound retrieval to a curated bucket. Combines with ACL — a
        member you can't see still won't be returned. AND-ed with
        source_kinds when both are present.
    embedding_models : list[str] | None
        Which embedding tables to query against. Defaults to all known
        tables that have rows for this scope. Multiple models = multiple
        vector recalls fused together.
    rerank : bool
        If False or no host reranker is configured, fusion order stands.
    only_children : bool
        Limit to leaf (small) chunks. Parent expansion is the caller's
        responsibility (the chunk's ``parent_chunk_id`` is on each hit).
    scope_ids : list[str] | None
        Structural filter — restrict results to chunks whose source is
        assigned to at least one of these scopes (the platform.associations
        spine, target_type='scope').
        Non-UUID values are silently dropped. If all provided ids are invalid
        UUIDs, or if none of the valid ids are visible to the caller, an empty
        SearchResponse is returned immediately (fail-closed).
    source_ids : list[str] | None
        Hard-scope retrieval to chunks whose ``source_id`` is one of these — e.g.
        cld_file file_ids for a thread's attached files. None = unscoped (default).
        Blanks are dropped; an explicit non-None list with no usable ids returns an
        empty SearchResponse immediately (fail-closed). Combines (AND) with
        source_kinds / scope_ids / include_sources and ALWAYS with the user/org ACL —
        a source the caller can't see is never returned.
    processed_document_ids : list[str] | None
        Hard-scope every recall lane to the specified processed-document rows.
        Callers can pass a base document plus any sibling/child derivatives to
        search the complete selected family without widening to unrelated chunks.
        Invalid or empty explicit lists return an empty response (fail-closed).
    include_entity_map : bool
        Whether to build and return the entity map sidecar. Default True.
        Disable for latency-sensitive callers that don't use the map.
    rerank_timeout_s : float | None
        Bound on the cross-encoder call; past it the fused order stands and
        ``rerank_status`` is ``"timeout"``.
    rerank_input : int | None
        The cross-encoder window (at most ``RERANK_INPUT``) for every call.
    rerank_input_large : int | None
        A smaller cross-encoder window used when the fused set is large
        (more than ``2 * RERANK_INPUT`` candidates).
    on_fused : async callable(list[SearchHit]) | None
        Called once with the fused (pre-rerank) top hits when a rerank will run, so a
        streaming caller can show results before the cross-encoder answers.
    readable : ReadableDocuments | None
        The kernel's readable-document set for ``user_id`` when the caller already
        holds it; otherwise it is resolved here, concurrently with the embedding.
    relevance_floor : float | None
        Per-call override for ``RELEVANCE_FLOOR`` — the minimum cross-encoder
        score a hit must reach to be returned at all. None = the module
        default. 0.0 returns everything the ranker surfaced (and still reports
        the verdict honestly). Raise it for a caller that would rather get
        nothing than get something tangential.
    keep_weak : int
        When the relevance gate graded candidates and dropped them ALL, return the
        best ``keep_weak`` anyway, each ``weak=True``, verdict ``weak_matches_only``.
        0 (the default) keeps the honest empty result — what an agent caller wants.
    """
    # Fail closed: user_id is required unless the caller is an admin
    # explicitly bypassing ACL. A None user_id would otherwise silently
    # expose is_public=true notes and global library content.
    if not user_id and not (is_admin and admin_bypass_acl):
        raise ValueError(
            "matrx_rag.search: user_id is required (per-user ownership contract); "
            "admin_bypass_acl+is_admin is the only exception"
        )

    started = time.perf_counter()
    limit = max(1, min(MAX_LIMIT, limit))
    embedding_models = embedding_models or [default_text_model()]

    # An all-whitespace query embeds to a zero vector (garbage cosine results)
    # and produces a NULL tsquery (silently drops the lexical lane). The HTTP
    # layer rejects empty strings, but agent-tool / internal callers can still
    # pass blanks — fail fast with an empty result rather than retrieve noise.
    query = query.strip()
    if not query:
        return SearchResponse(
            query=query,
            hits=[],
            total_candidates=0,
            embedding_model=embedding_models[0],
            reranker_model=None,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    # Sources filed under what the caller is working in (a project) widen the
    # scope filter as a UNION with the scopes: "what this conversation is
    # attached to" is its scopes AND the Sources filed under its project.
    scope_document_ids = _normalize_processed_document_ids(scope_document_ids) or None

    # -----------------------------------------------------------------------
    # Scope validation — fail-closed structural filter.
    # -----------------------------------------------------------------------
    validated_scope_ids: list[str] | None = _validate_scope_ids(scope_ids)
    if validated_scope_ids is not None and len(validated_scope_ids) == 0:
        # Caller passed scope_ids but NONE are valid UUIDs → empty response.
        return SearchResponse(
            query=query,
            hits=[],
            total_candidates=0,
            embedding_model=embedding_models[0],
            reranker_model=None,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    if validated_scope_ids:
        # Access check — keep only scopes the caller can actually see.
        # Fail-closed: if NONE survive the access check, return empty.
        validated_scope_ids = await _check_scope_access(
            scope_ids=validated_scope_ids,
            user_id=user_id,
        )
        if not validated_scope_ids and not scope_document_ids:
            return SearchResponse(
                query=query,
                hits=[],
                total_candidates=0,
                embedding_model=embedding_models[0],
                reranker_model=None,
                latency_ms=int((time.perf_counter() - started) * 1000),
            )

    # -----------------------------------------------------------------------
    # Source-id validation — fail-closed file-scoped filter.
    # -----------------------------------------------------------------------
    validated_source_ids: list[str] | None = _normalize_source_ids(source_ids)
    if validated_source_ids is not None and len(validated_source_ids) == 0:
        # Caller passed source_ids but NONE were usable → empty response (don't
        # silently widen to an unscoped search). The ACL still bounds matches even
        # when ids ARE present, so no extra access check is needed here.
        return SearchResponse(
            query=query,
            hits=[],
            total_candidates=0,
            embedding_model=embedding_models[0],
            reranker_model=None,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    validated_processed_document_ids = _normalize_processed_document_ids(processed_document_ids)
    if validated_processed_document_ids is not None and len(validated_processed_document_ids) == 0:
        return SearchResponse(
            query=query,
            hits=[],
            total_candidates=0,
            embedding_model=embedding_models[0],
            reranker_model=None,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    # The kernel's readable-document set rides beside the embedding round trip.
    import asyncio as _asyncio

    readable_task = None
    if readable is None and user_id and not (is_admin and admin_bypass_acl):
        readable_task = _asyncio.ensure_future(
            resolve_readable_documents(str(user_id), source_kinds=readable_source_kinds_for(source_kinds))
        )

    # 0. Expand the query (multi-query rewriting) + optional HyDE.
    # These are best-effort LLM calls — a failure must DEGRADE (fall back to the
    # raw query / skip HyDE), never abort the whole search. In the OpenAI-only
    # deployment these are the fragile external dependencies.
    query_variants: list[str] = [query]
    if multi_query and multi_query > 1:
        try:
            query_variants = await expand_query(query, n=multi_query)
        except Exception as exc:
            logger.warning("rag.search: query expansion failed, using raw query: %s", exc)
            query_variants = [query]
    hyde_text: str = ""
    if use_hyde:
        try:
            hyde_text = await hyde_passage(query)
        except Exception as exc:
            logger.warning("rag.search: HyDE generation failed, skipping: %s", exc)
            hyde_text = ""

    # 1. Embed every (variant + optional HyDE) against every provider.
    # Each (model, variant) pair contributes one ranking to the fusion.
    # HyDE text rides the same embedding API call as the query variants
    # (one round-trip per model) but its ranking is tagged with a
    # ``#hyde`` suffix so the fuser can blend it at a lower weight than
    # the raw / paraphrased query rankings (HyDE is fabricated content;
    # we trust it less than the user's actual words).
    query_vectors: dict[str, list[list[float]]] = {}
    hyde_vector_idx: int | None = None
    for model in embedding_models:
        texts = list(query_variants)
        if hyde_text:
            hyde_vector_idx = len(texts)
            texts.append(hyde_text)
        # Embedding is an external API call (OpenAI). On failure, skip this
        # model's vector lane and let lexical + entity recall carry the search,
        # rather than failing the whole request. If EVERY model fails,
        # query_vectors stays empty and fusion runs on lexical + entity alone.
        try:
            # Provenance on the shared embedding cache: the organization this
            # search is scoped to. A personal-scope query carries none, and the
            # cache row is cross-tenant by design, so None is the ANSWER here —
            # said explicitly rather than defaulted.
            vecs = await _embed_query_cached(model, texts, organization_id=organization_id)
        except Exception as exc:
            logger.warning(
                "rag.search: embedding failed for model %s; skipping its vector lane: %s",
                model,
                exc,
            )
            vecs = None
        if vecs:
            query_vectors[model] = vecs

    if readable_task is not None:
        readable = await readable_task

    # 2. Recall — vector + lexical + entity in parallel where possible.
    # One connection shared across all three recall lanes (avoids 3 separate
    # pool checkouts per search() call) via the ORM's own acquire_connection
    # primitive; every lane composes its query through typed ORM expressions.
    async with acquire_connection(database=PACKAGE_DB_NAME) as conn:
        vector_rankings: dict[str, list[str]] = {}
        # Per-ranking RRF weights. Defaults to 1.0; HyDE rankings get the
        # configured (lower) weight.
        ranking_weights: dict[str, float] = {}
        hyde_weight = _hyde_rrf_weight()

        # THE THREE LANES RUN CONCURRENTLY, each ONE statement through its recall door
        # (rag.recall_vector / recall_lexical / recall_entities + recall_entity_chunks,
        # migrations 1398/1405) on a pooled connection. The doors apply exactly the
        # read-access rule and filters the ORM lanes built (144/144 lane answers identical
        # on the clone, three users, four filter variants, 2026-09-27); the readable set
        # is computed once per request and bound into each call.
        filters = recall_filters(
            only_children=only_children,
            source_kinds=source_kinds,
            include_sources=include_sources,
            library_filter=library_filter,
            source_ids=validated_source_ids,
            processed_document_ids=validated_processed_document_ids,
            scope_ids=validated_scope_ids,
            scope_document_ids=scope_document_ids,
            admin_bypass_acl=bool(is_admin and admin_bypass_acl),
        )

        async def _vector_lane() -> None:
            async def one(model: str, variant_idx: int, qvec: list[float]) -> None:
                ranking = await _recall_vector_door(
                    spec_for(model).table, qvec, user_id=user_id, readable=readable,
                    k=VECTOR_RECALL_K, filters=filters,
                )
                is_hyde = hyde_vector_idx is not None and variant_idx == hyde_vector_idx
                key = f"{model}#v{variant_idx}{'#hyde' if is_hyde else ''}"
                vector_rankings[key] = ranking
                ranking_weights[key] = hyde_weight if is_hyde else 1.0

            jobs = [
                (model, variant_idx, qvec)
                for model, vecs in query_vectors.items()
                for variant_idx, qvec in enumerate(vecs)
            ]
            await _asyncio.gather(*(one(*job) for job in jobs))
            # Keep the fusion's key order identical to the serial loop it replaced.
            ordered = {f"{m}#v{i}{'#hyde' if (hyde_vector_idx is not None and i == hyde_vector_idx) else ''}": None for m, i, _ in jobs}
            for key in list(ordered):
                ordered[key] = vector_rankings.pop(key)
            vector_rankings.update(ordered)

        async def _lexical_lane() -> list[str]:
            return await _recall_lexical_door(
                query, user_id=user_id, readable=readable, k=LEXICAL_RECALL_K, filters=filters
            )

        # 2c. Entity recall lane — KG entity match → chunk co-occurrence. Admin-bypass
        # callers get no entity lane (unchanged).
        async def _entity_lane():
            return await _recall_entity_door(
                query,
                user_id=user_id,
                readable=readable,
                filters=filters,
                expand_clusters=expand_entity_clusters,
            )

        _, lexical_ranking, (entity_ranking, matched_entity_ids, matched_entity_names) = (
            await _asyncio.gather(_vector_lane(), _lexical_lane(), _entity_lane())
        )

        # Real per-lane recall sizes (distinct candidates each lane surfaced
        # before fusion). Surfaced on SearchResponse for the diagnostics UI.
        vector_candidates = len({cid for r in vector_rankings.values() for cid in r})
        lexical_candidates = len(lexical_ranking)
        entity_candidates = len(entity_ranking)

        # 3. RRF fusion with per-ranking weights — HyDE blends at 0.3,
        # entity lane blends at _ENTITY_LANE_RRF_WEIGHT.
        additional_rankings: dict[str, list[str]] = {}
        if entity_ranking:
            additional_rankings["entity_lane"] = entity_ranking
            ranking_weights["entity_lane"] = _ENTITY_LANE_RRF_WEIGHT

        fused = _rrf_fuse(
            {**vector_rankings, **additional_rankings},
            lexical_ranking,
            ranking_weights=ranking_weights,
        )
        if not fused:
            # Zero candidates recalled across every lane — there is definitively
            # nothing relevant, which is a real answer and must be stated as one
            # (not left as "unscored", which would read as "we didn't check").
            return SearchResponse(
                query=query,
                hits=[],
                total_candidates=0,
                embedding_model=embedding_models[0],
                reranker_model=None,
                latency_ms=int((time.perf_counter() - started) * 1000),
                matched_entities=matched_entity_names,
                vector_candidates=vector_candidates,
                lexical_candidates=lexical_candidates,
                entity_candidates=entity_candidates,
                relevance_verdict=RELEVANCE_VERDICT_NONE,
            )

        # 3b. ONE BATCHED READ after the lanes (Knowledge Hub H1, 2026-09-27): chunk bodies,
        # priority, the entity-importance sum and the Source's name for every fusion
        # candidate, in a single round trip. It replaced three serial reads (priorities,
        # importance, hydration) plus the Source-name read the Knowledge service made.
        #
        # Phase 2.0b priority boost and Phase 3.0 entity-importance boost are applied
        # from it exactly as before: priority first (missing/0 = no boost), then
        # importance (NULL/0 = no boost), both before the RERANK_INPUT cutoff.
        candidate_rows = await _hydrate_candidates(conn, [cid for cid, _ in fused[:PRIORITY_FETCH_CAP]])
        priority_lookup, importance_lookup = _boost_lookups(candidate_rows)
        if priority_lookup:
            fused = sorted(
                (
                    (cid, _apply_priority(rrf_score, priority_lookup.get(cid, 0)))
                    for cid, rrf_score in fused
                ),
                key=lambda kv: kv[1],
                reverse=True,
            )
        if importance_lookup:
            fused = sorted(
                (
                    (cid, _apply_entity_importance(rrf_score, importance_lookup.get(cid, 0.0)))
                    for cid, rrf_score in fused
                ),
                key=lambda kv: kv[1],
                reverse=True,
            )

    # Build entity rank lookup (1-based position in entity_ranking list).
    entity_rank_lookup: dict[str, int] = {
        cid: rank for rank, cid in enumerate(entity_ranking, start=1)
    }

    # 4. The top-N candidates' rows come from the same batched read (boosted ordering is
    # applied in Python from ``fused``). A candidate beyond PRIORITY_FETCH_CAP cannot reach
    # the RERANK_INPUT window (RERANK_INPUT <= PRIORITY_FETCH_CAP).
    candidate_ids = [chunk_id for chunk_id, _ in fused[:RERANK_INPUT]]
    chunk_rows = [candidate_rows[cid] for cid in candidate_ids if cid in candidate_rows]

    def _as_text(v: object) -> str | None:
        return str(v) if v is not None else None

    rows_by_id: dict[str, dict[str, Any]] = {}
    for r in chunk_rows:
        cid_text = _as_text(r["id"])
        if cid_text is None:
            continue
        rows_by_id[cid_text] = {
            "chunk_id": cid_text,
            "source_kind": r["source_kind"],
            "source_id": r["source_id"],
            "field_id": r["field_id"],
            "parent_chunk_id": _as_text(r["parent_chunk_id"]),
            "chunk_kind": r["chunk_kind"],
            "content_text": r["content_text"],
            "metadata": r["metadata"],
            "priority": r["priority"],
            "derivation_kind": r["derivation_kind"],
            "agent_id": _as_text(r["agent_id"]),
            "extraction_run_id": _as_text(r["extraction_run_id"]),
            "extraction_result_id": _as_text(r["extraction_result_id"]),
            "processed_document_id": _as_text(r["processed_document_id"]),
            "primary_page_id": _as_text(r["primary_page_id"]),
            "page_numbers": r["page_numbers"],
            "source_name": r.get("source_name"),
            "page_section_title": r.get("page_section_title"),
        }

    # 5. Optional rerank.
    reranker_model: str | None = None
    rerank_scores: dict[str, float] = {}
    # The RAW cross-encoder scores, kept whatever we decide about the ORDERING.
    # rerank_scores is cleared when we distrust Cohere's ordering
    # (RERANK_CONFIDENCE_FLOOR) — but "we won't reorder on these" and "these
    # tell us nothing about relevance" are different statements, and conflating
    # them is what let a low-confidence search still return its garbage. The
    # relevance gate reads THIS dict.
    relevance_scores: dict[str, float] = {}
    rerank_status = "off"
    vector_rank_lookup = {
        cid: rank
        for ranking in vector_rankings.values()
        for rank, cid in enumerate(ranking, start=1)
    }
    lexical_rank_lookup = {cid: rank for rank, cid in enumerate(lexical_ranking, start=1)}
    fused_score_lookup = dict(fused)

    def _hit_for(cid: str, reranked: bool) -> SearchHit:
        row = rows_by_id[cid]
        meta = _coerce_metadata(row["metadata"])
        # `row` is either a real asyncpg Record or a dict (in tests).
        # asyncpg Records support __getitem__ for known columns — and
        # every column below is present in the hydration SELECT, so
        # bracket access is always safe. We avoid `.get()` because some
        # Record versions don't expose it.
        priority_val = int(row["priority"] or 0)
        # Score semantics:
        #   - With Cohere rerank: the Cohere score IS the exposed score.
        #     Priority is a tiebreak in ordering, not a multiplier on
        #     the user-facing score. This preserves Cohere's calibrated
        #     output for FE comparisons across deploys.
        #   - Without Cohere: the boosted RRF score (already boosted at
        #     stage 1) is exposed. Priority influences both rank and
        #     reported score in this path.
        if reranked:
            base_score = rerank_scores.get(cid)
            if base_score is None:
                base_score = 0.0
        else:
            base_score = fused_score_lookup.get(cid, 0.0)
        page_numbers_val = row["page_numbers"]
        if page_numbers_val is None:
            page_numbers_val = []
        return (
            SearchHit(
                chunk_id=cid,
                source_kind=row["source_kind"],
                source_id=row["source_id"],
                field_id=row["field_id"],
                parent_chunk_id=row["parent_chunk_id"],
                chunk_kind=row["chunk_kind"],
                content_text=row["content_text"],
                score=base_score,
                vector_rank=vector_rank_lookup.get(cid),
                lexical_rank=lexical_rank_lookup.get(cid),
                rerank_score=rerank_scores.get(cid) if reranked else None,
                metadata=meta,
                priority=priority_val,
                derivation_kind=row["derivation_kind"] or "initial_extract",
                agent_id=row["agent_id"],
                extraction_run_id=row["extraction_run_id"],
                extraction_result_id=row["extraction_result_id"],
                processed_document_id=row["processed_document_id"],
                primary_page_id=row["primary_page_id"],
                page_numbers=list(page_numbers_val),
                entity_rank=entity_rank_lookup.get(cid),
                source_name=row.get("source_name") if isinstance(row, dict) else None,
                section_title=row.get("page_section_title") if isinstance(row, dict) else None,
                weak=cid in weak_ids,
                also_in=[_also_in_entry(o) for o in also_in_ids.get(cid, [])],
            )
        )

    def _also_in_entry(other: str) -> dict[str, object]:
        r = rows_by_id[other]
        return {
            "chunk_id": other,
            "source_kind": r["source_kind"],
            "source_id": r["source_id"],
            "processed_document_id": r["processed_document_id"],
            "source_name": r.get("source_name") if isinstance(r, dict) else None,
        }

    weak_ids: set[str] = set()
    also_in_ids: dict[str, list[str]] = {}

    # THE FUSED ORDER FIRST (Knowledge Hub H1, 2026-09-27): a caller that renders as the
    # lanes finish gets the fused, MMR-filtered top hits BEFORE the cross-encoder runs
    # (≈1–2 s), then this function's return value carries the reranked order.
    if on_fused is not None and rerank and get_reranker() is not None and rows_by_id:
        preview = _drop_exact_text_duplicates([cid for cid, _ in fused if cid in rows_by_id], rows_by_id)
        preview, also_in_ids = _collapse_cross_source_duplicates(preview, rows_by_id)
        if use_mmr and len(preview) > 1:
            preview = _mmr_filter(preview, rows_by_id, threshold=mmr_threshold, keep=limit * 3)
        try:
            await on_fused([_hit_for(cid, False) for cid in preview[:limit]])
        except Exception as exc:  # noqa: BLE001 — a preview consumer never breaks the search
            logger.warning("rag.search: on_fused consumer failed (search continues): %s", exc)

    reranker = get_reranker()
    # The cross-encoder window: RERANK_INPUT, or the caller's smaller window when the fused
    # set is large (a latency-bounded caller trades a little recall for a faster answer).
    rerank_window = RERANK_INPUT
    if rerank_input is not None:
        rerank_window = max(1, min(RERANK_INPUT, int(rerank_input)))
    if rerank_input_large is not None and len(fused) > RERANK_INPUT * 2:
        rerank_window = max(1, min(rerank_window, int(rerank_input_large)))
    rerank_error: str | None = None
    if rerank and reranker is not None and rows_by_id:
        documents = [
            rows_by_id[cid]["content_text"] for cid, _ in fused[:rerank_window] if cid in rows_by_id
        ]
        cand_ids = [cid for cid, _ in fused[:rerank_window] if cid in rows_by_id]
        try:
            # The durable rerank cache (matrx_rag.rerank_cache): the same model, query and
            # passage contents return the stored scores, so identical searches give identical
            # hits and a run-once step downstream can reuse. Only the live call is time-bounded.
            async def _live_rerank():
                if rerank_timeout_s is not None:
                    return await _asyncio.wait_for(
                        reranker.rerank(query, documents), timeout=rerank_timeout_s
                    )
                return await reranker.rerank(query, documents)

            rerank_result, _rerank_cache_hit = await cached_rerank(
                reranker,
                query,
                documents,
                organization_id=organization_id,
                user_id=user_id,
                rerank_call=_live_rerank,
            )
            reranker_model = rerank_result.model
            scores = rerank_result.scores
            rerank_status = "applied"
            for cid, s in zip(cand_ids, scores, strict=True):
                rerank_scores[cid] = s
                relevance_scores[cid] = s
        except TimeoutError as exc:
            # Bounded by the caller: the fused order stands, the status says why, and the
            # miss is RECORDED as a provider incident — never a silent permanent fallback.
            logger.warning("rag.search: rerank exceeded %.2fs, keeping RRF order", rerank_timeout_s or 0.0)
            reranker_model = None
            rerank_status = "timeout"
            rerank_error = f"The reranker took longer than {rerank_timeout_s:g} s."
            await capture_error(
                exc,
                kind="rag_rerank_timeout",
                context={"documents": len(documents), "timeout_s": rerank_timeout_s},
            )
        except Exception as exc:
            logger.warning("rag.search: host reranker failed, keeping RRF order: %s", exc)
            reranker_model = None
            rerank_status = "failed"
            rerank_error = f"{type(exc).__name__}: {str(exc)[:240]}"
            await capture_error(
                exc,
                kind="rag_rerank_provider_failed",
                context={"documents": len(documents)},
            )
        # Confidence floor — when even the BEST candidate scores below the
        # floor, Cohere found no confident match and its ordering of uniformly
        # weak candidates is noise. Keep the fused RRF order instead (and
        # report reranker_model=None / rerank_score=None: rerank was attempted
        # but not used). See RERANK_CONFIDENCE_FLOOR. Note this says nothing
        # about whether the candidates get RETURNED — `relevance_scores` is
        # deliberately NOT cleared here, and the relevance gate below (which
        # uses a strictly higher floor) is what decides that.
        if reranker_model and not _rerank_is_confident(rerank_scores):
            logger.info(
                "rag.search: rerank low-confidence (max=%.3f < %.2f) for %r — keeping RRF order",
                max(rerank_scores.values()) if rerank_scores else 0.0,
                RERANK_CONFIDENCE_FLOOR,
                query[:80],
            )
            reranker_model = None
            rerank_scores = {}
            rerank_status = "low_confidence"

    # 6. Build the final ordering. Phase 2.0b — priority is applied
    # DIFFERENTLY at each stage to avoid double-boosting Cohere's
    # judgment:
    #
    #   Stage 1 (already done above): boost on RRF scores governs which
    #   chunks reach the rerank window. Multiplicative boost is safe
    #   here because RRF values are small and similar in magnitude.
    #
    #   Stage 2 (here): when Cohere is in the loop, its cross-encoder
    #   score is authoritative for relative quality. Priority becomes a
    #   PURE TIEBREAK via a composite key — we do NOT multiply the
    #   Cohere score by the boost, which would over-weight metadata
    #   against text relevance. Two chunks tied at the same Cohere
    #   score break by priority; otherwise Cohere wins.
    if reranker_model:
        ordered = sorted(
            (cid for cid, _ in fused[:rerank_window] if cid in rows_by_id),
            key=lambda cid: (
                rerank_scores.get(cid, -1.0),
                int(rows_by_id[cid]["priority"]) if "priority" in rows_by_id[cid] else 0,
            ),
            reverse=True,
        )
    else:
        ordered = [cid for cid, _ in fused if cid in rows_by_id]

    # 6a. ONE DOCUMENT NEVER RETURNS THE SAME TEXT TWICE — regardless of MMR, its
    # threshold or snippet length (MMR waves short snippets through). A parent that
    # was too small to split carries the exact text of its one child (2,089 such
    # pairs were live on 2026-10-11; the chunker no longer emits them).
    ordered = _drop_exact_text_duplicates(ordered, rows_by_id)
    # 6a-2. ONE TEXT, ONE HIT ACROSS SOURCES — the same passage stored as a PDF and as the notes
    # derived from it shows once, best-ranked kept, naming the others (``SearchHit.also_in``).
    ordered, also_in_ids = _collapse_cross_source_duplicates(ordered, rows_by_id)

    # 6b. MMR — drop near-duplicate candidates so top-k spans diverse
    # content. Token-Jaccard is a fast, no-extra-fetch proxy for cosine
    # similarity; good enough for dedup.
    if use_mmr and len(ordered) > 1:
        ordered = _mmr_filter(
            ordered,
            rows_by_id,
            threshold=mmr_threshold,
            keep=limit * 3,  # leave headroom past `limit` for downstream consumers
        )

    # 6b-2. THE RELEVANCE GATE — the last thing between the caller and a
    # confidently-worded pile of irrelevant chunks. Everything above this line
    # only ever ORDERED candidates; nothing asked whether the best one was
    # actually about the query. See RELEVANCE_FLOOR.
    pre_floor = ordered
    ordered, relevance_verdict, relevance_floor_applied, below_floor_dropped = (
        _apply_relevance_floor(
            ordered,
            relevance_scores,
            floor=relevance_floor if relevance_floor is not None else RELEVANCE_FLOOR,
            limit=limit,
        )
    )
    ordered, relevance_verdict, weak_ids = _keep_weak_matches(
        pre_floor, ordered, relevance_verdict, keep_weak=keep_weak
    )
    if relevance_verdict == RELEVANCE_VERDICT_NONE:
        logger.info(
            "rag.search: no relevant matches for %r — best cross-encoder score "
            "%.4f < floor %.2f; returning an honest empty result instead of the "
            "top-%d (library_filter=%s, %d candidates fused)",
            query[:80],
            max(relevance_scores.values()) if relevance_scores else 0.0,
            relevance_floor_applied if relevance_floor_applied is not None else 0.0,
            limit,
            library_filter,
            len(fused),
        )

    hits: list[SearchHit] = [_hit_for(cid, bool(reranker_model)) for cid in ordered[:limit]]

    # 6c. Entity map sidecar — build after final hits are chosen.
    entity_map: list[EntityMapEntry] = []
    if include_entity_map and hits:
        try:
            async with acquire_connection(database=PACKAGE_DB_NAME) as map_conn:
                entity_map, hits = await _build_entity_map(
                    map_conn,
                    hits=hits,
                )
        except Exception as exc:
            logger.warning(
                "rag.search: entity map build failed (non-fatal, returning empty map): %s",
                exc,
            )
            await capture_error(
                exc,
                kind="rag_entity_map_failed",
                context={"organization_id": organization_id, "hit_count": len(hits)},
            )
            entity_map = []

    elapsed_ms = int((time.perf_counter() - started) * 1000)

    if record_audit and organization_id is None:
        # A search made with no organization selected reads across every
        # organization the person belongs to (reach never depends on the
        # selection). There is no single organization to file its audit row in,
        # and the writer never infers one — so no row is written, said here
        # rather than raised as a system error on every legitimate search.
        logger.info(
            "rag.search: no organization selected — searched every membership; "
            "retrieval audit row not written (it needs one organization to belong to)"
        )
    elif record_audit:
        # Fire-and-forget: per repo rule, DB writes inside request flow must
        # not block the response. Exceptions are logged so failures are
        # visible without propagating to the caller.
        supervised_task(
            _write_audit(
                query=query,
                user_id=user_id,
                organization_id=organization_id,
                returned_chunk_ids=[h.chunk_id for h in hits],
                rerank_scores=[h.rerank_score for h in hits] if reranker_model else None,
                latency_ms=elapsed_ms,
                pipeline={
                    "embedding_models": embedding_models,
                    "source_kinds": source_kinds,
                    "rerank_model": reranker_model,
                    "limit": limit,
                    "only_children": only_children,
                    # Phase 2.0b — record how priority influenced this query
                    # so future ranking changes can be reasoned about with
                    # the audit log. Includes the policy params + a per-hit
                    # priority array so "why did chunk X rank where it did"
                    # is answerable retroactively.
                    "priority_boost_enabled": _priority_boost_enabled(),
                    "priority_boost_scale": _priority_boost_scale(),
                    "n_priority_chunks_in_window": (
                        sum(1 for v in priority_lookup.values() if v) if priority_lookup else 0
                    ),
                    "returned_priorities": [h.priority for h in hits],
                    # Entity lane observability.
                    "entity_lane": bool(entity_ranking),
                    "expand_entity_clusters": expand_entity_clusters,
                    "scope_ids": len(validated_scope_ids) if validated_scope_ids else 0,
                    # Relevance gate observability — so "why did this query
                    # return nothing" is answerable from the audit log alone.
                    "library_filter": library_filter,
                    "relevance_verdict": relevance_verdict,
                    "relevance_floor": relevance_floor_applied,
                    "below_floor_dropped": below_floor_dropped,
                },
            ),
            kind="rag_retrieval_audit_failed",
            name="rag-retrieval-audit",
            context={"organization_id": organization_id, "user_id": user_id},
        )

    return SearchResponse(
        query=query,
        hits=hits,
        total_candidates=len(fused),
        embedding_model=embedding_models[0],
        reranker_model=reranker_model,
        latency_ms=elapsed_ms,
        matched_entities=matched_entity_names,
        entity_map=entity_map,
        vector_candidates=vector_candidates,
        lexical_candidates=lexical_candidates,
        entity_candidates=entity_candidates,
        rerank_status=rerank_status,
        rerank_error=rerank_error,
        relevance_verdict=relevance_verdict,
        relevance_floor=relevance_floor_applied,
        below_floor_dropped=below_floor_dropped,
    )


# ---------------------------------------------------------------------------
# Scope access check
# ---------------------------------------------------------------------------


async def _check_scope_access(
    *,
    scope_ids: list[str],
    user_id: str | None,
) -> list[str]:
    """Return the subset of scope_ids the caller can see.

    A scope is a Record of the host's record store, so the HOST answers, through the
    ``scope_access`` seam (``matrx_rag.configure(scope_access=...)``): the store's own ladder,
    as this person. This package owns no scope table and reads none (lane SCOPES-READS-SERVER).
    Returns ``scope_ids`` unchanged when ``user_id`` is None (admin-bypass callers skip this);
    with a person and no seam wired it REFUSES, by name — never a guessed "all visible".
    """
    if not user_id or not scope_ids:
        return scope_ids
    from matrx_rag._ext import get_ext

    access = get_ext("scope_access")
    if access is None:
        raise RuntimeError(
            "matrx_rag: a search narrowed to scopes needs the host's scope_access seam "
            "(matrx_rag.configure(scope_access=...)); nothing was searched."
        )
    allowed = {str(s) for s in await access([str(s) for s in scope_ids], str(user_id))}
    return [s for s in scope_ids if str(s) in allowed]


# ---------------------------------------------------------------------------
# Recall queries
# ---------------------------------------------------------------------------


def _active_membership_predicate(*, user_id: str, organization: object):
    from matrx_orm import Compare

    return (
        Compare(F("iam.memberships.user_id"), "=", user_id)
        & Compare(F("iam.memberships.organization_id"), "=", organization)
        & Compare(F("iam.memberships.container_type"), "=", "organization")
        & Compare(F("iam.memberships.status"), "=", "active")
        & Is(F("iam.memberships.deleted_at"), None)
    )


@dataclass(frozen=True)
class ReadableDocuments:
    """The kernel's readable-document set for ONE person — the input the ACL needs.

    ``processed_document_ids`` is ``iam.accessible_entity_ids('processed_document')``
    asked as that person: every Source she may read, by every lane the kernel knows.
    Built once per search by :func:`resolve_readable_documents` (it costs one kernel
    call) and handed to :func:`build_visibility_predicate`, which is synchronous.

    ``source_ids`` (READABLE SOURCES, 2026-10-15) is, per chunk kind the recall doors
    otherwise decide row by row with ``iam.has_access_for``, the ids of that kind she may
    read that have passages without a Source (``rag.readable_sources``). The doors test
    membership in it instead of calling the kernel once per candidate row; a kind it does
    not carry keeps the per-row check.
    """

    user_id: str
    processed_document_ids: tuple[str, ...]
    source_ids: dict[str, tuple[str, ...]] = field(default_factory=dict)


#: The chunk kinds the search asks ``rag.readable_sources`` for. ``cld_file`` is left to
#: the doors' per-row check on purpose: the file set costs ~5 s for a member of many
#: organizations, and file passages without a Source are rare (~200 rows, 2026-10-15).
READABLE_SOURCE_KINDS: tuple[str, ...] = ("note", "task", "project", "library_doc", "document")


def readable_source_kinds_for(source_kinds: list[str] | None) -> tuple[str, ...]:
    """The kinds worth a readable-source set for one search: every one, or only those
    its ``source_kinds`` narrowing keeps."""
    if not source_kinds:
        return READABLE_SOURCE_KINDS
    wanted = set(source_kinds)
    return tuple(k for k in READABLE_SOURCE_KINDS if k in wanted)


async def resolve_readable_documents(
    user_id: str, *, source_kinds: tuple[str, ...] | list[str] = ()
) -> ReadableDocuments:
    """Ask the kernel which Sources ``user_id`` may read — ONCE per search, never cached
    across requests (a grant or revocation reaches search immediately) — and, for each
    of ``source_kinds`` in :data:`READABLE_SOURCE_KINDS`, which Source-less records of
    that kind (concurrently). Raises on failure — never empty-by-error."""
    import asyncio as _asyncio

    from matrx_orm import platform_accessible_ids

    kinds = tuple(k for k in dict.fromkeys(source_kinds) if k in READABLE_SOURCE_KINDS)
    docs = platform_accessible_ids(str(user_id), "processed_document", "viewer")
    if not kinds:
        return ReadableDocuments(user_id=str(user_id), processed_document_ids=tuple(await docs))
    ids, sources = await _asyncio.gather(docs, _readable_sources(str(user_id), kinds))
    return ReadableDocuments(user_id=str(user_id), processed_document_ids=tuple(ids), source_ids=sources)


async def _readable_sources(user_id: str, kinds: tuple[str, ...]) -> dict[str, tuple[str, ...]]:
    """``rag.readable_sources`` asked as ``user_id``: every requested kind must come back."""
    from matrx_orm import ArrayArg
    from matrx_orm.core.db_function import call_function_as

    answer = await call_function_as(
        user_id, PACKAGE_DB_NAME, "rag", "readable_sources", ArrayArg(list(kinds), "text"), mode="scalar"
    )
    if not isinstance(answer, dict) or any(not isinstance(answer.get(k), list) for k in kinds):
        raise RuntimeError(
            f"rag.readable_sources answered {type(answer).__name__} without every kind of {list(kinds)}"
        )
    return {k: tuple(str(i) for i in answer[k]) for k in kinds}


#: A chunk with no Source (``processed_document_id`` NULL) is decided by the kernel on
#: the row its ``source_id`` names. source_kind → entity token.
_ROW_KERNEL_TOKENS: dict[str, str] = {
    "note": "note",
    "task": "task",
    "project": "project",
    "cld_file": "file",
    "library_doc": "library_doc",
    # content.document (Spaces pages, annotations, notes, …): the kernel decides on the row,
    # so an organization-shared page reaches its members and a personal one only its owner.
    "document": "document",
    # workbench.udt_workbooks / udt_documents: the kernel decides on the row, same as notes.
    "workbook": "workbook",
    "udt_document": "udt_document",
}


def build_visibility_predicate(
    *,
    user_id: str | None,
    organization_id: str | None,
    is_admin: bool = False,
    admin_bypass_acl: bool = False,
    chunk_alias: str,
    readable: ReadableDocuments | None = None,
    lanes_only: bool = False,
):
    """Build the complete typed read-access predicate for ``rag.kg_chunks``.

    ``lanes_only=True`` returns the named lanes (``{name: predicate}``) the predicate is
    the OR of — what the search lab counts per route, so its breakdown can never
    describe a lane the filter does not have.

    🚨 REBASED ON THE KERNEL (Knowledge Hub H1, 2026-09-27). A chunk is readable when
    the kernel says its document is:

    * a chunk of a Source (``processed_document_id`` set — 97% of chunks) → the Source
      is in ``readable.processed_document_ids`` (``iam.accessible_entity_ids``);
    * a chunk of a note / task / project / file / library doc with no Source →
      ``iam.has_access_for(person, token, source_id, 'viewer')`` on that row;
    * any other kind (no entity token) → only its creator.

    Two sharing lanes the kernel does not model on the document row stay: the global
    library lane (content owned by a ``global_readable`` system org) and data-store
    grants. The hand-written note/file/org-member rules this replaced are gone: they
    handed every member of an organization every chunk in it, whatever the document's
    own access said.

    ``readable`` is REQUIRED for a person (build it with
    :func:`resolve_readable_documents`); ``chunk_alias`` names how the calling query
    refers to the chunk row (``"c"`` in search()'s joined queries, the chunk table's
    qualified name for a plain ``KgChunks.filter(...)``). ``organization_id`` decides
    nothing (2026-09-23).
    """
    del organization_id
    from matrx_orm import (
        ArrayAny,
        Compare,
        ConstantPredicate,
        DbFunction,
        Exists,
        JsonPath,
        OuterRef,
        TupleInArrays,
        Value,
    )

    if is_admin and admin_bypass_acl:
        return ConstantPredicate(True)
    if user_id is None:
        return ConstantPredicate(False)
    if readable is None or str(readable.user_id) != str(user_id):
        raise ValueError(
            "build_visibility_predicate: the kernel's readable-document set for this person "
            "is required — await resolve_readable_documents(user_id) and pass readable=."
        )

    Memberships = get_db_model("Memberships")
    DataStoreMembers = get_db_model("DataStoreMembers")
    DataStoreGrants = get_db_model("DataStoreGrants")
    OrgIndustries = get_db_model("OrgIndustries")
    SystemOrgs = get_db_model("SystemOrgs")

    pd_col = F(f"{chunk_alias}.processed_document_id")
    if readable.processed_document_ids:
        source_lane = Is(pd_col, None, negated=True) & TupleInArrays(
            (pd_col,), (list(readable.processed_document_ids),), array_types=("uuid[]",)
        )
    else:
        source_lane = ConstantPredicate(False)

    def kernel_row(kind: str, token: str):
        # A kind the readable-source set carries is tested by membership, exactly as the
        # recall doors do — a kernel call per row on ~14k note passages timed the search
        # lab inventory out at 30 s (2026-10-24). A kind it does not carry keeps the row check.
        if kind in readable.source_ids:
            ids = list(readable.source_ids[kind])
            if not ids:
                return ConstantPredicate(False)
            return Compare(F(f"{chunk_alias}.source_kind"), "=", kind) & ArrayAny(
                F(f"{chunk_alias}.source_id"), ids, cast="text[]"
            )
        return Compare(F(f"{chunk_alias}.source_kind"), "=", kind) & Compare(
            DbFunction(
                "iam.has_access_for",
                Cast(Value(str(user_id)), "uuid"),
                Value(token),
                Cast(F(f"{chunk_alias}.source_id"), "uuid"),
                Cast(Value("viewer"), "permission_level"),
            ),
            "=",
            True,
        )

    row_kinds = list(_ROW_KERNEL_TOKENS)
    row_lane = kernel_row(row_kinds[0], _ROW_KERNEL_TOKENS[row_kinds[0]])
    for kind in row_kinds[1:]:
        row_lane = row_lane | kernel_row(kind, _ROW_KERNEL_TOKENS[kind])
    untyped_owner = ~ArrayAny(F(f"{chunk_alias}.source_kind"), row_kinds, cast="text[]") & Compare(
        F(f"{chunk_alias}.created_by"), "=", user_id
    )

    # THE GLOBAL LANE (db-rules §6e): content owned by a `global_readable` system org.
    global_org = Exists(
        SystemOrgs.filter(
            Compare(
                F("iam.system_orgs.organization_id"),
                "=",
                F(f"{chunk_alias}.organization_id"),
            )
            & Compare(F("iam.system_orgs.global_readable"), "=", True)
        )
    )
    global_doc = Compare(F(f"{chunk_alias}.source_kind"), "=", "library_doc") & global_org
    global_file = (
        Compare(F(f"{chunk_alias}.source_kind"), "=", "cld_file")
        & global_org
        & Is(
            JsonPath(F(f"{chunk_alias}.metadata"), "source", "library_short_code"),
            None,
            negated=True,
        )
    )

    # A library grant to an organization (or an industry) reaches every member of
    # THAT organization, whichever one she has selected.
    org_grant = Compare(F("audience"), "=", "organization") & Exists(
        Memberships.filter(
            _active_membership_predicate(
                user_id=user_id,
                organization=OuterRef("organization_id"),
            )
        )
    )
    industry_grant = Compare(F("audience"), "=", "industry") & Exists(
        OrgIndustries.filter(
            Compare(F("industry_id"), "=", OuterRef("industry_id")),
            Exists(
                Memberships.filter(
                    _active_membership_predicate(
                        user_id=user_id,
                        organization=OuterRef("organization_id"),
                    )
                )
            ),
        )
    )
    grant_exists = Exists(
        DataStoreMembers.filter(
            Compare(
                F("rag.data_store_members.source_kind"),
                "=",
                F(f"{chunk_alias}.source_kind"),
            ),
            Compare(
                F("rag.data_store_members.source_id"),
                "=",
                F(f"{chunk_alias}.source_id"),
            ),
            Is(F("rag.data_store_members.deleted_at"), None),
            Exists(
                DataStoreGrants.filter(
                    Compare(
                        F("rag.data_store_grants.data_store_id"),
                        "=",
                        OuterRef("data_store_id"),
                    ),
                    Compare(F("rag.data_store_grants.audience"), "=", "global")
                    | org_grant
                    | industry_grant,
                )
            ),
        )
    )

    lanes = {
        "source": source_lane,
        "row_kernel": Is(pd_col, None) & row_lane,
        "owned_untyped": Is(pd_col, None) & untyped_owner,
        "library_doc": global_doc,
        "library_short_code": global_file,
        "data_store_grant": grant_exists,
    }
    if lanes_only:
        return lanes
    combined = None
    for lane in lanes.values():
        combined = lane if combined is None else combined | lane
    return combined


async def visibility_predicate_for(
    *,
    user_id: str | None,
    organization_id: str | None,
    chunk_alias: str,
    is_admin: bool = False,
    admin_bypass_acl: bool = False,
    source_kinds: tuple[str, ...] | list[str] = (),
):
    """``build_visibility_predicate`` with the kernel set resolved — the one door for callers.

    Every chunk read outside ``search()`` (the chunk loaders, the search lab's counts)
    awaits this instead of building the predicate by hand, so no caller can reach the
    chunks without the kernel having answered for the person first.

    ``source_kinds`` (usually :data:`READABLE_SOURCE_KINDS`) also fetches those kinds'
    readable-source sets, so the predicate tests them by membership: a read that scans
    the whole chunk table passes it; a lookup of a few chunk ids keeps the cheaper
    per-row check.
    """
    readable = None
    if user_id and not (is_admin and admin_bypass_acl):
        readable = await resolve_readable_documents(str(user_id), source_kinds=source_kinds)
    return build_visibility_predicate(
        user_id=user_id,
        organization_id=organization_id,
        is_admin=is_admin,
        admin_bypass_acl=admin_bypass_acl,
        chunk_alias=chunk_alias,
        readable=readable,
    )


_build_visibility_clause = build_visibility_predicate


# ── THE RECALL DOORS (rag.recall_*, migrations 1398/1405) ─────────────────────────────────
# Each recall lane is ONE statement on a pooled connection: the read-access rule and the
# search() filters live in the database function (inline column predicates, so the index
# path holds), the HNSW settings travel inside it, and the caller's readable-Source set is
# bound once. The functions are server-only (service role) and return only chunks the
# person may read (guard test on the clone, DB lane).


def recall_filters(
    *,
    only_children: bool,
    source_kinds: list[str] | None,
    include_sources: list[dict[str, str]] | None,
    library_filter: str,
    source_ids: list[str] | None,
    processed_document_ids: list[str] | None,
    scope_ids: list[str] | None,
    scope_document_ids: list[str] | None,
    admin_bypass_acl: bool,
) -> dict[str, object]:
    """search()'s options as the doors' ``p_filters`` — keys present exactly when the old
    query builder added the clause (an empty list is "no filter", as it always was)."""
    f: dict[str, object] = {"leaf_only": bool(only_children)}
    if source_kinds:
        f["source_kinds"] = list(source_kinds)
    if include_sources:
        f["include_sources"] = [
            {"source_kind": m.get("source_kind"), "source_id": m.get("source_id")} for m in include_sources
        ]
    if library_filter in ("library_only", "exclude_library"):
        f["library_filter"] = library_filter
    if source_ids:
        f["source_ids"] = list(source_ids)
    if processed_document_ids:
        f["processed_document_ids"] = list(processed_document_ids)
    if scope_ids or scope_document_ids:
        f["scope_ids"] = list(scope_ids or [])
        if scope_document_ids:
            f["scope_document_ids"] = list(scope_document_ids)
        f["scope_kind_aliases"] = {k: list(v) for k, v in _SCOPE_ENTITY_TYPE_ALIASES.items()}
    if admin_bypass_acl:
        f["admin_bypass_acl"] = True
    return f


def _readable_ids(readable: ReadableDocuments | None) -> list[str]:
    return list(readable.processed_document_ids) if readable is not None else []


def _door_filters(filters: dict[str, object], readable: ReadableDocuments | None) -> dict[str, object]:
    """The doors' ``p_filters`` with the readable-source sets this search holds, so each
    kind they carry is tested by membership instead of a kernel call per row. A caller that
    hands ``search()`` its own ``readable`` without ``source_ids`` keeps the per-row check:
    same answers, slower — build it with ``resolve_readable_documents(..., source_kinds=...)``."""
    if readable is None or not readable.source_ids:
        return filters
    return {**filters, "readable_sources": {k: list(v) for k, v in readable.source_ids.items()}}


async def _door(function: str, *args: object) -> list[dict[str, object]]:
    from matrx_orm import ArrayArg, call_function

    bound = [ArrayArg(a.values, a.pg_type) if isinstance(a, _Uuids) else a for a in args]
    return await call_function(PACKAGE_DB_NAME, "rag", function, *bound, mode="rows")


@dataclass(frozen=True)
class _Uuids:
    values: list[str]
    pg_type: str = "uuid"


async def _recall_vector_door(
    embedding_table: str,
    qvec: list[float],
    *,
    user_id: str | None,
    readable: ReadableDocuments | None,
    k: int,
    filters: dict[str, object],
) -> list[str]:
    table = embedding_table.split(".")[-1]
    rows = await _door(
        "recall_vector",
        table,
        "[" + ",".join(repr(float(x)) for x in qvec) + "]",
        user_id,
        _Uuids(_readable_ids(readable)),
        k,
        _door_filters(filters, readable),
        40,
    )
    return [str(r["chunk_id"]) for r in rows]


async def _recall_lexical_door(
    query: str, *, user_id: str | None, readable: ReadableDocuments | None, k: int, filters: dict[str, object]
) -> list[str]:
    rows = await _door(
        "recall_lexical", query, user_id, _Uuids(_readable_ids(readable)), k, _door_filters(filters, readable)
    )
    return [str(r["chunk_id"]) for r in rows]


async def _recall_entity_door(
    query: str,
    *,
    user_id: str | None,
    readable: ReadableDocuments | None,
    filters: dict[str, object],
    expand_clusters: bool = False,
) -> tuple[list[str], list[str], list[str]]:
    """Entity lane: names/aliases of the caller's organizations' entities, then the chunks
    that mention them — two doors, the same answers as the ORM lane they replace."""
    if not user_id:
        return [], [], []
    tokens, phrase = _tokenize_query(query)
    if not tokens and not phrase:
        return [], [], []
    from matrx_orm import ArrayArg

    entity_rows = await _door("recall_entities", user_id, ArrayArg(tokens, "text"), phrase, _ENTITY_MATCH_LIMIT)
    if not entity_rows:
        return [], [], []
    matched_entity_ids = [str(r["entity_id"]) for r in entity_rows]
    matched_entity_names = [str(r["name"]) for r in entity_rows]
    chunk_entity_ids = matched_entity_ids
    if expand_clusters:
        cluster_ids = list({str(r["cluster_id"]) for r in entity_rows if r.get("cluster_id")})
        org_ids = list({str(r["organization_id"]) for r in entity_rows if r.get("organization_id")})
        if cluster_ids and org_ids:
            KgEntities = get_db_model("KgEntities")
            sibling_rows = await (
                KgEntities.filter(cluster_id__in=cluster_ids, organization_id__in=org_ids)
                .limit(_ENTITY_CLUSTER_EXPANSION_CAP + len(matched_entity_ids))
                .values("id")
            )
            matched = set(matched_entity_ids)
            siblings = [str(r["id"]) for r in sibling_rows if str(r["id"]) not in matched]
            if siblings:
                chunk_entity_ids = matched_entity_ids + siblings[:_ENTITY_CLUSTER_EXPANSION_CAP]
    entity_filters = {k: v for k, v in filters.items() if k != "admin_bypass_acl"}
    rows = await _door(
        "recall_entity_chunks",
        user_id,
        _Uuids(_readable_ids(readable)),
        _Uuids(chunk_entity_ids),
        _ENTITY_CHUNK_LIMIT,
        _ENTITY_MIN_CONTENT_CHARS,
        _door_filters(entity_filters, readable),
    )
    return [str(r["chunk_id"]) for r in rows], matched_entity_ids, matched_entity_names


def _tokenize_query(query: str) -> tuple[list[str], str]:
    """Tokenize query for entity matching.

    Splits on non-alphanumeric characters, lowercases, keeps tokens of
    length >= _ENTITY_MIN_TERM_LEN, deduplicates preserving first-seen
    order, caps at _ENTITY_MAX_TERMS.

    Also appends the full lowercased query as a phrase term (last element).
    """
    tokens: list[str] = []
    seen: set[str] = set()
    for tok in re.split(r"[^a-z0-9]+", query.lower()):
        if len(tok) >= _ENTITY_MIN_TERM_LEN and tok not in seen:
            seen.add(tok)
            tokens.append(tok)
            if len(tokens) >= _ENTITY_MAX_TERMS:
                break
    phrase = query.lower().strip()
    return tokens, phrase


# Both steps are ORM. Step 1 (entity match against rag.kg_entities +
# rag.kg_entity_aliases) uses the typed `Case`/`When` primitive for the
# exact-match-first ordering with a bound query value
# (matrx_orm.core.expressions, grown for exactly this gap — see the
# kg_edges site in _build_entity_map for the JOIN-ON sibling usage).
# Step 2 (chunk co-occurrence: rag.kg_chunk_entities JOIN rag.kg_chunks,
# read-access/leaf/scope/source filters, GROUP BY + ORDER BY count(*)/max(len))
# is ORM — see the join()+annotate()+group_by()+fetch_via() below.
async def _build_entity_map(
    conn: Any,
    *,
    hits: list[SearchHit],
) -> tuple[list[EntityMapEntry], list[SearchHit]]:
    """Build the condensed entity map and attach per-hit entity names.

    Flat-rows + Python aggregation approach: one query returns
    (chunk_id, entity_id, name, kind, source_kind, source_id) for all
    hit chunks, then Python aggregates mention counts, artifact counts,
    source-kind breakdowns, and top_chunk_id.

    Returns (entity_map, updated_hits) — hits gain .entities lists.
    """
    from matrx_orm import ArrayAny

    hit_ids = [h.chunk_id for h in hits]
    if not hit_ids:
        return [], hits

    # Hit order lookup (0-based position for top_chunk_id selection).
    hit_order: dict[str, int] = {cid: i for i, cid in enumerate(hit_ids)}

    # ---- Step 1: flat entity rows for all hit chunks ----
    # Also select e.importance and e.is_concept for entity map ordering and
    # surface in EntityMapEntry (Stage 3 — importance-aware entity map).
    # Flat 3-table JOIN (no GROUP BY at the SQL level — aggregation happens in
    # Python below), fully ORM-expressible: KgChunkEntities.join(KgEntities)
    # .join(KgChunks) + an explicit column list (aliased to the exact keys
    # the Python aggregation reads). fetch_via() keeps this on the same
    # connection the caller passed in (matrx-orm owns the conn.fetch call).
    KgChunkEntities = get_db_model("KgChunkEntities")
    KgEntities = get_db_model("KgEntities")
    KgChunks = get_db_model("KgChunks")
    flat_rows = await (
        KgChunkEntities.filter(chunk_id__in=hit_ids)
        .join(
            KgEntities,
            on=ColumnComparison(F("rag.kg_entities.id"), "=", F("rag.kg_chunk_entities.entity_id")),
        )
        .join(
            KgChunks,
            on=ColumnComparison(F("rag.kg_chunks.id"), "=", F("rag.kg_chunk_entities.chunk_id")),
        )
        .fetch_via(
            conn,
            Projection(F("rag.kg_chunk_entities.chunk_id"), "chunk_id"),
            Projection(F("rag.kg_entities.id"), "entity_id"),
            Projection(F("rag.kg_entities.name"), "entity_name"),
            Projection(F("rag.kg_entities.kind"), "entity_kind"),
            Projection(F("rag.kg_entities.importance"), "importance"),
            Projection(F("rag.kg_entities.is_concept"), "is_concept"),
            Projection(F("rag.kg_chunks.source_kind"), "source_kind"),
            Projection(F("rag.kg_chunks.source_id"), "source_id"),
        )
    )

    if not flat_rows:
        return [], hits

    # Aggregate in Python.
    # entity_id → {name, kind, mention_count, artifact_count,
    #               source_kind_counts, best_chunk_id (lowest hit_order)}
    entity_agg: dict[str, dict[str, Any]] = {}
    # chunk_id → {entity_id → mention count}
    chunk_entity_counts: dict[str, dict[str, int]] = {}

    for row in flat_rows:
        eid = row["entity_id"]
        cid = row["chunk_id"]
        src_kind = row["source_kind"]
        src_id = row["source_id"]
        artifact_key = f"{src_kind}:{src_id}"

        if eid not in entity_agg:
            entity_agg[eid] = {
                "name": row["entity_name"],
                "kind": row["entity_kind"],
                "importance": float(row["importance"]) if row["importance"] is not None else None,
                "is_concept": bool(row["is_concept"]),
                "mention_count": 0,
                "artifact_ids": set(),
                "source_kind_counts": {},
                "best_chunk_id": cid,
                "best_chunk_order": hit_order.get(cid, 999999),
            }
        agg = entity_agg[eid]
        agg["mention_count"] += 1
        agg["artifact_ids"].add(artifact_key)
        agg["source_kind_counts"][src_kind] = agg["source_kind_counts"].get(src_kind, 0) + 1
        # Track the chunk that appears earliest in hit order for top_chunk_id.
        chunk_order = hit_order.get(cid, 999999)
        if chunk_order < agg["best_chunk_order"]:
            agg["best_chunk_order"] = chunk_order
            agg["best_chunk_id"] = cid

        # Per-chunk mention counts for hit entity attachment.
        if cid not in chunk_entity_counts:
            chunk_entity_counts[cid] = {}
        chunk_entity_counts[cid][eid] = chunk_entity_counts[cid].get(eid, 0) + 1

    # Sort entities by importance DESC (Stage 3 — importance-aware map),
    # falling back to mention_count when importance is NULL (unscored). This
    # ensures the entity map "sidecar" leads with what matters most in the org
    # rather than what was simply mentioned most in this result set.
    # NULL importance sorts below any scored entity (treated as -1.0 for
    # sorting purposes — unscored entities are newly ingested, not meaningless,
    # but they haven't been evaluated yet).
    top_entities = sorted(
        entity_agg.items(),
        key=lambda kv: (
            kv[1]["importance"] if kv[1]["importance"] is not None else -1.0,
            kv[1]["mention_count"],
        ),
        reverse=True,
    )[:_ENTITY_MAP_LIMIT]
    top_entity_ids = [eid for eid, _ in top_entities]

    # ---- Step 2: linked entities from kg_edges ----
    linked_rows: list[Any] = []
    if top_entity_ids:
        # Direction-agnostic partner selection via the `Case`/`When` ORM
        # primitive (matrx_orm.core.expressions, grown for exactly this gap):
        # `ON e2.id = CASE WHEN ed.src_id = ANY($1::uuid[]) THEN ed.dst_id
        # ELSE ed.src_id END`. `Case.render()` supplies the typed expression
        # to the join.
        #
        # ⚠️ LATENT QUIRK — PRESERVED, NOT FIXED (parity is the contract):
        # when BOTH endpoints of an edge are in top_entity_ids, the CASE
        # always resolves partner = dst_id (the WHEN branch fires first), so
        # the edge contributes exactly ONE row, attributed to
        # entity_links[src] AND (via the `dst in top_entity_set` check below)
        # also entity_links[dst] — using the SAME partner_id (dst_id) for
        # both, i.e. dst's own linked list gets an entry pointing at dst_id
        # itself. A two-query "src∈set" / "dst∈set∧src∉set" union would
        # silently FIX this (each top-entity gets its own correctly-
        # attributed partner) — that is a behavior change, not something this
        # conversion is authorized to make. Flagged separately for a product
        # decision; do not "fix" it here.
        KgEdges = get_db_model("KgEdges")
        partner_case = Case(
            When(
                ArrayAny(F("ed.src_id"), top_entity_ids, cast="uuid[]"),
                then=F("ed.dst_id"),
            ),
            default=F("ed.src_id"),
        )
        linked_rows = await (
            KgEdges.filter(kind="co_occurs_with")
            .from_alias("ed")
            .join(
                KgEntities,
                on=ColumnComparison(F("e2.id"), "=", partner_case),
                alias="e2",
            )
            .filter(
                ArrayAny(F("ed.src_id"), top_entity_ids, cast="uuid[]")
                | ArrayAny(F("ed.dst_id"), top_entity_ids, cast="uuid[]")
            )
            .annotate(total_weight=Sum("ed.weight"))
            .group_by("ed.src_id", "ed.dst_id", "e2.id", "e2.name", "e2.kind")
            .fetch_via(
                conn,
                Projection(Cast(F("ed.src_id"), "text"), "src_id"),
                Projection(Cast(F("ed.dst_id"), "text"), "dst_id"),
                Projection(Cast(F("e2.id"), "text"), "partner_id"),
                Projection(F("e2.name"), "partner_name"),
                Projection(F("e2.kind"), "partner_kind"),
                "total_weight",
            )
        )

    # Build per-entity → [(partner_id, name, kind, weight)] map.
    # An edge may appear once as src→dst and once as dst→src; we bucket
    # it under whichever endpoint is in our top_entity_ids set.
    top_entity_set = set(top_entity_ids)
    entity_links: dict[str, list[tuple[str, str, str, float]]] = {eid: [] for eid in top_entity_ids}
    for row in linked_rows:
        src = row["src_id"]
        dst = row["dst_id"]
        partner_id = row["partner_id"]
        partner_name = row["partner_name"]
        partner_kind = row["partner_kind"]
        weight = float(row["total_weight"] or 0)
        # Attribute to the endpoint(s) in our set.
        if src in top_entity_set:
            entity_links[src].append((partner_id, partner_name, partner_kind, weight))
        if dst in top_entity_set and dst != src:
            entity_links[dst].append((partner_id, partner_name, partner_kind, weight))

    # ---- Step 3: build EntityMapEntry list ----
    entity_map: list[EntityMapEntry] = []
    for eid, agg in top_entities:
        # Top-_ENTITY_MAP_LINKS partners by weight.
        partners = sorted(entity_links.get(eid, []), key=lambda t: t[3], reverse=True)
        linked = [
            EntityMapLink(entity_id=pid, name=pname, kind=pkind, weight=pw)
            for pid, pname, pkind, pw in partners[:_ENTITY_MAP_LINKS]
        ]
        entity_map.append(
            EntityMapEntry(
                entity_id=eid,
                name=agg["name"],
                kind=agg["kind"],
                mention_count=agg["mention_count"],
                artifact_count=len(agg["artifact_ids"]),
                source_kind_counts=dict(agg["source_kind_counts"]),
                top_chunk_id=agg["best_chunk_id"],
                linked=linked,
                # Stage 3 fields — importance and concept flag from kg_entities.
                # importance=None when entity hasn't been scored yet (newly ingested).
                importance=agg["importance"],
                is_concept=agg["is_concept"],
            )
        )

    # ---- Step 4: attach entity names to each hit ----
    # Top-_HIT_ENTITY_LIMIT entity names per chunk, ordered by per-chunk mention count.
    entity_name_by_id = {eid: agg["name"] for eid, agg in entity_agg.items()}
    updated_hits: list[SearchHit] = []
    for hit in hits:
        per_chunk = chunk_entity_counts.get(hit.chunk_id, {})
        if per_chunk:
            top_eids = sorted(per_chunk.items(), key=lambda kv: kv[1], reverse=True)
            hit.entities = [
                entity_name_by_id[eid]
                for eid, _ in top_eids[:_HIT_ENTITY_LIMIT]
                if eid in entity_name_by_id
            ]
        updated_hits.append(hit)

    return entity_map, updated_hits


# ---------------------------------------------------------------------------
# RRF fusion
# ---------------------------------------------------------------------------


def _rrf_fuse(
    vector_rankings: dict[str, list[str]],
    lexical_ranking: list[str],
    *,
    ranking_weights: dict[str, float] | None = None,
    lexical_weight: float = 1.0,
) -> list[tuple[str, float]]:
    """Weighted Reciprocal Rank Fusion.

    ``ranking_weights`` maps a vector-ranking key to its weight in the
    sum. Missing keys default to 1.0 so callers that don't care about
    weighting behave exactly as before. ``lexical_weight`` weights the
    lexical ranking the same way.

    Used by HyDE blending — the hypothetical-answer ranking is weighted
    at ~0.3 while the raw query and multi-query paraphrases stay at 1.0.
    Also used by the entity recall lane (weight _ENTITY_LANE_RRF_WEIGHT).
    """
    score: dict[str, float] = {}
    for key, ranking in vector_rankings.items():
        weight = 1.0
        if ranking_weights is not None and key in ranking_weights:
            weight = ranking_weights[key]
        for rank, cid in enumerate(ranking, start=1):
            score[cid] = score.get(cid, 0.0) + weight / (RRF_K + rank)
    for rank, cid in enumerate(lexical_ranking, start=1):
        score[cid] = score.get(cid, 0.0) + lexical_weight / (RRF_K + rank)
    return sorted(score.items(), key=lambda kv: kv[1], reverse=True)


def _boost_lookups(rows: dict[str, dict[str, Any]]) -> tuple[dict[str, int], dict[str, float]]:
    """Priority and entity-importance inputs from the batched candidate rows. A 0 or
    NULL priority is no boost (missing key); a NULL importance sum is no boost."""
    priority = {cid: int(r["priority"]) for cid, r in rows.items() if r.get("priority")}
    importance = {
        cid: float(r["importance_sum"]) for cid, r in rows.items() if r.get("importance_sum") is not None
    }
    return priority, importance


async def _hydrate_candidates(conn: Any, chunk_ids: list[str]) -> dict[str, dict[str, Any]]:
    """Every fusion candidate's row in ONE statement on the recall connection: the chunk's
    own columns, ``importance_sum`` (SUM of its entities' positive importance — the
    Phase 3.0 boost input), ``source_name`` (its Source's name, for display) and
    ``page_section_title`` (the heading its primary page sits under — part of its locator).
    Empty input skips the round trip."""
    if not chunk_ids:
        return {}
    from matrx_orm import Compare, OuterRef, Subquery

    KgChunks = get_db_model("KgChunks")
    KgChunkEntities = get_db_model("KgChunkEntities")
    KgEntities = get_db_model("KgEntities")
    ProcessedDocuments = get_db_model("ProcessedDocuments")
    ProcessedDocumentPages = get_db_model("ProcessedDocumentPages")
    importance = (
        KgChunkEntities.filter(
            Compare(F("rag.kg_chunk_entities.chunk_id"), "=", OuterRef("id")),
            Is(F("rag.kg_entities.importance"), None, negated=True),
            Compare(F("rag.kg_entities.importance"), ">", 0),
        )
        .join(
            KgEntities,
            on=ColumnComparison(F("rag.kg_entities.id"), "=", F("rag.kg_chunk_entities.entity_id")),
        )
        .annotate(s=Sum("rag.kg_entities.importance"))
        .select("s")
    )
    source_name = ProcessedDocuments.filter(id=OuterRef("processed_document_id")).select("name")
    # The heading a chunk sits under (its primary page's section title) — part of its locator.
    page_section = ProcessedDocumentPages.filter(id=OuterRef("primary_page_id")).select("section_title")
    rows = await (
        KgChunks.filter(id__in=chunk_ids, deleted_at__isnull=True)
        .annotate(
            importance_sum=Subquery(importance),
            source_name=Subquery(source_name),
            page_section_title=Subquery(page_section),
        )
        .fetch_via(
            conn,
            "id",
            "source_kind",
            "source_id",
            "field_id",
            "parent_chunk_id",
            "chunk_kind",
            "content_text",
            "metadata",
            "priority",
            "derivation_kind",
            "agent_id",
            "extraction_run_id",
            "extraction_result_id",
            "processed_document_id",
            "primary_page_id",
            "page_numbers",
            "importance_sum",
            "source_name",
            "page_section_title",
        )
    )
    return {str(r["id"]): dict(r) for r in rows}


# ---------------------------------------------------------------------------
# MMR — token-Jaccard greedy diversification
# ---------------------------------------------------------------------------


def _token_set(text: str) -> set[str]:
    # Lowercased word tokens, length >= 3, dedup by string form.
    return {t for t in (s.lower().strip(".,;:()[]{}\"'`") for s in text.split()) if len(t) >= 3}


# Cross-GRANULARITY variants of one passage from the SAME source are deduped at
# a LOWER Jaccard bar than ordinary pairs: the multigranularity pipeline emits
# `chunked_fine` windows that overlap the standard `child` chunk of the same
# page (Jaccard ~0.45–0.6), so they slip past the diversity threshold (0.72) and
# the user sees the same passage twice. The tighter bar applies ONLY when the
# two chunks share a source AND differ in granularity (chunk_kind /
# derivation_kind) — two DISTINCT sections of the same document at the same
# granularity keep the normal 0.72 bar, so dense docs aren't over-collapsed.
_MMR_SAME_SOURCE_VARIANT_THRESHOLD = 0.45


def _drop_exact_text_duplicates(ordered_ids: list[str], rows_by_id: dict) -> list[str]:
    """Keep the first (best-ranked) hit per (document, whitespace-normalized text)."""
    kept: list[str] = []
    seen: set[tuple[object, ...]] = set()
    for cid in ordered_ids:
        row = rows_by_id.get(cid)
        if row is None:
            continue
        doc = row["processed_document_id"] if "processed_document_id" in row else None
        owner: tuple[object, ...] = (
            ("doc", str(doc))
            if doc
            else ("src", row["source_kind"] if "source_kind" in row else None, row["source_id"] if "source_id" in row else None)
        )
        key = (*owner, " ".join(str(row["content_text"] or "").split()))
        if key in seen:
            continue
        seen.add(key)
        kept.append(cid)
    return kept


#: A passage whose distinct words are this share contained in a better-ranked passage of ANOTHER
#: source is the same text stored twice (a PDF and the notes derived from it) — collapsed into it.
CROSS_SOURCE_DUPLICATE_CONTAINMENT = 0.9


def _owner_key(row) -> tuple[object, ...]:
    doc = row["processed_document_id"] if "processed_document_id" in row else None
    if doc:
        return ("doc", str(doc))
    return ("src", row["source_kind"] if "source_kind" in row else None, row["source_id"] if "source_id" in row else None)


def _collapse_cross_source_duplicates(
    ordered_ids: list[str],
    rows_by_id: dict,
    *,
    containment: float = CROSS_SOURCE_DUPLICATE_CONTAINMENT,
) -> tuple[list[str], dict[str, list[str]]]:
    """ONE TEXT, ONE HIT — across sources. Walks the ranked ids; a passage whose word set is
    ``containment`` contained in (or contains) a kept passage of a DIFFERENT source collapses into
    the kept one. Returns ``(ordered, also_in)`` — ``also_in[kept_id]`` = the collapsed ids, best
    first. Same-source pairs are left to ``_drop_exact_text_duplicates`` and MMR; passages under 8
    distinct words always stay (too short to call the same)."""
    kept: list[str] = []
    kept_tokens: list[set[str]] = []
    kept_owner: list[tuple[object, ...]] = []
    also_in: dict[str, list[str]] = {}
    for cid in ordered_ids:
        row = rows_by_id.get(cid)
        if row is None:
            continue
        tokens = _token_set(str(row["content_text"] or ""))
        owner = _owner_key(row)
        into: str | None = None
        if len(tokens) >= 8:
            for kid, ktok, kown in zip(kept, kept_tokens, kept_owner):
                if kown == owner or len(ktok) < 8:
                    continue
                if len(tokens & ktok) / min(len(tokens), len(ktok)) >= containment:
                    into = kid
                    break
        if into is not None:
            also_in.setdefault(into, []).append(cid)
            continue
        kept.append(cid)
        kept_tokens.append(tokens)
        kept_owner.append(owner)
    return (kept, also_in)


def _mmr_filter(
    ordered_ids: list[str],
    rows_by_id: dict,
    *,
    threshold: float,
    keep: int,
) -> list[str]:
    """Greedy MMR by token Jaccard. Walks ``ordered_ids`` (already in
    relevance order), keeping each candidate only if its Jaccard overlap
    with every previously-kept candidate is below ``threshold``.

    Granularity-aware: when a candidate overlaps a previously-kept chunk from
    the SAME source but a DIFFERENT granularity (a `child` chunk vs the
    `chunked_fine` window of the same page), the effective threshold drops to
    ``_MMR_SAME_SOURCE_VARIANT_THRESHOLD`` so the duplicate collapses to one
    hit. Distinct sections of the same document (same granularity) are untouched.

    Empty / very short snippets (< 8 unique tokens) always pass — Jaccard on a
    handful of tokens is noise, and a short snippet may be a unique identifier.
    """
    kept: list[str] = []
    kept_tokensets: list[set[str]] = []
    # Per-kept (source_id, chunk_kind, derivation_kind) for granularity-aware dedup.
    kept_meta: list[tuple[str | None, object, object]] = []

    def _meta(row: dict) -> tuple[str | None, object, object]:
        # Bracket access guarded by membership — asyncpg Records don't expose .get().
        return (
            row["source_id"] if "source_id" in row else None,
            row["chunk_kind"] if "chunk_kind" in row else None,
            row["derivation_kind"] if "derivation_kind" in row else None,
        )

    for cid in ordered_ids:
        row = rows_by_id.get(cid)
        if row is None:
            continue
        tokens = _token_set(row["content_text"] or "")
        meta = _meta(row)
        if len(tokens) < 8:
            kept.append(cid)
            kept_tokensets.append(tokens)
            kept_meta.append(meta)
            if len(kept) >= keep:
                break
            continue
        source_id, chunk_kind, derivation_kind = meta
        drop = False
        for prior_tokens, (p_src, p_kind, p_deriv) in zip(kept_tokensets, kept_meta):
            if not prior_tokens:
                continue
            inter = len(tokens & prior_tokens)
            if inter == 0:
                continue
            union = len(tokens | prior_tokens)
            sim = inter / union if union else 0.0
            same_source_variant = (
                source_id is not None
                and source_id == p_src
                and (chunk_kind != p_kind or derivation_kind != p_deriv)
            )
            eff_threshold = _MMR_SAME_SOURCE_VARIANT_THRESHOLD if same_source_variant else threshold
            if sim >= eff_threshold:
                drop = True
                break
        if not drop:
            kept.append(cid)
            kept_tokensets.append(tokens)
            kept_meta.append(meta)
        if len(kept) >= keep:
            break
    return kept


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------


async def _write_audit(
    *,
    query: str,
    user_id: str | None,
    organization_id: str | None,
    returned_chunk_ids: list[str],
    rerank_scores: list[float | None] | None,
    latency_ms: int,
    pipeline: dict[str, object],
) -> None:
    """Insert one retrieval-audit row via the ORM model.

    Best-effort by contract: called via asyncio.create_task so failures
    are logged but never propagate to the search caller. Columns omitted
    here (id, created_at, metadata) fall to their DB defaults, exactly
    as the old raw INSERT left them out.
    """
    if organization_id is None:
        exc = ValueError(
            "rag.search audit requires the initiating organization_id; "
            "the audit writer never infers or database-assigns organization scope"
        )
        logger.error("rag.search: refusing NULL-org audit write")
        await capture_error(
            exc,
            kind="rag_retrieval_audit_missing_org",
            context={"user_id": user_id},
        )
        return

    try:
        RetrievalAudit = get_db_model("RetrievalAudit")
        qhash = hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()
        await RetrievalAudit.create(
            organization_id=organization_id,
            created_by=user_id,
            query=query,
            query_hash=qhash,
            pipeline_config=pipeline,
            returned_chunk_ids=returned_chunk_ids,
            rerank_scores=[s for s in (rerank_scores or []) if s is not None] or None,
            latency_ms=latency_ms,
        )
    except Exception as exc:
        logger.warning("rag.search: audit write failed (best-effort): %s", exc)
        await capture_error(
            exc,
            kind="rag_retrieval_audit_failed",
            context={"organization_id": organization_id, "user_id": user_id},
        )


def _coerce_metadata(value: object) -> dict[str, object]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
            return decoded if isinstance(decoded, dict) else {}
        except Exception:
            return {}
    return {}


__all__ = [
    "SearchHit",
    "SearchResponse",
    "EntityMapEntry",
    "EntityMapLink",
    "search",
    "_build_visibility_clause",
    "build_visibility_predicate",
    "visibility_predicate_for",
    "ReadableDocuments",
    "resolve_readable_documents",
    "DEFAULT_LIMIT",
    "MAX_LIMIT",
]
