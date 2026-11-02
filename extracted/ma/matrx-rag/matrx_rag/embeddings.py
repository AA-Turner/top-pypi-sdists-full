"""Embedding seam — module-level facade over the configured provider.

Phase 2b/ii — the actual embedding work moves behind an
:class:`EmbeddingProvider` protocol so matrx-local can swap to a local
provider (fastembed / sentence-transformers / ONNX) without touching
any RAG call site. The default :class:`DefaultOpenAIVoyageProvider`
ships in this module and exactly reproduces the pre-Phase-2b behavior.

Wire shape (unchanged, ALL callers continue to work):

* ``embed(model, texts, *, input_type=None) -> list[list[float]]``
* ``spec_for(model) -> EmbeddingSpec``
* ``default_text_model() -> str``  / ``default_code_model() -> str``
* ``SPECS``  -- mapping of canonical model name to ``EmbeddingSpec``

Behavior:

* Voyage ``voyage:voyage-4-large`` (1024d) is the prose default (2026-07;
  RTEB leader). OpenAI ``openai:text-embedding-3-small`` stays registered for
  the legacy table until its backfill-replacement is verified + dropped.
* Voyage ``voyage:voyage-code-3`` (1024d) is the code default.
* ``input_type='query' | 'document'`` is honored by Voyage's asymmetric
  embedding models; OpenAI ignores it.
* Empty texts get a zero-vector slot so callers keep a 1:1 mapping.

Hosts override via :func:`matrx_rag.configure(embedding_provider=...)`.
"""

from __future__ import annotations

import asyncio
import os
import re
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, nullcontext
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# SQL-injection defense — table name validation
# ---------------------------------------------------------------------------

# Embedding table names are host-injected (custom providers can supply their
# own spec.table values). Validate them before interpolating into SQL.
# Only fully-qualified "schema.table" identifiers with safe identifier chars
# are accepted (e.g. the OPENAI_TABLE constant below).
_SAFE_TABLE_RE = re.compile(r"^[a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*$")


def validate_table_name(table: str) -> None:
    """Raise ValueError if ``table`` is not a safe 'schema.table' identifier.

    Called at every SQL use-site where spec.table is interpolated. Defense-
    in-depth: a host-injected provider supplying a malicious table name is
    caught before the query runs.
    """
    if not _SAFE_TABLE_RE.match(table):
        raise ValueError(
            f"matrx_rag: unsafe embedding table name {table!r}. "
            "Must match schema.table with lowercase letters, digits, underscores only."
        )


# ---------------------------------------------------------------------------
# Constants — default OpenAI + Voyage adapters
# ---------------------------------------------------------------------------

# Legacy prose model — superseded by voyage-4-large (2026-07 upgrade). Kept
# registered so historical rows in its table stay searchable via explicit
# ``embedding_models=[...]`` until the backfill is verified and the table is
# dropped in a follow-up migration.
OPENAI_MODEL = "text-embedding-3-small"
OPENAI_DIM = 1536
OPENAI_BATCH = 96
OPENAI_TABLE = "rag.embeddings_oai_3_small_1536"

VOYAGE_MODEL = "voyage-code-3"
VOYAGE_DIM = 1024
VOYAGE_BATCH = 128
VOYAGE_TABLE = "rag.embeddings_voyage_code_3_1024"

# Prose default since 2026-07: voyage-4-large — the top general-purpose
# retrieval model (RTEB leader; supersedes voyage-3-large, outperforms both
# OpenAI 3-small and 3-large). 1024d default keeps HNSW well under pgvector's
# index limit at a quarter of 3-large's storage. Table: migration 0136.
VOYAGE4_MODEL = "voyage-4-large"
VOYAGE4_DIM = 1024
VOYAGE4_BATCH = 128
VOYAGE4_TABLE = "rag.embeddings_voyage_4_large_1024"


@dataclass(frozen=True)
class EmbeddingSpec:
    name: str  # canonical "<provider>:<model>" identifier
    dim: int
    table: str  # pgvector table name (or whatever the configured
    # VectorStore expects to find embeddings in)
    batch_size: int
    # Name of the matrx-orm Model class that owns ``table``, resolved through
    # ``matrx_rag.get_db_model(...)``. THE single source of truth for the
    # table → ORM model mapping (stages.py and ingestion.py each used to keep
    # their own hand-maintained dict; they drifted). A spec whose table has no
    # packaged model leaves this empty — ORM writes to it then fail loudly.
    orm_model: str = ""


# The default specs map. Custom providers can either reuse these names
# (recommended — keeps the pgvector table names stable) or add their
# own. ``spec_for`` reads from the configured provider's ``SPECS``,
# not from this constant, so hosts can ship their own spec dict.
SPECS: dict[str, EmbeddingSpec] = {
    f"openai:{OPENAI_MODEL}": EmbeddingSpec(
        name=f"openai:{OPENAI_MODEL}",
        dim=OPENAI_DIM,
        table=OPENAI_TABLE,
        batch_size=OPENAI_BATCH,
        orm_model="EmbeddingsOai3Small1536",
    ),
    f"voyage:{VOYAGE_MODEL}": EmbeddingSpec(
        name=f"voyage:{VOYAGE_MODEL}",
        dim=VOYAGE_DIM,
        table=VOYAGE_TABLE,
        batch_size=VOYAGE_BATCH,
        orm_model="EmbeddingsVoyageCode31024",
    ),
    f"voyage:{VOYAGE4_MODEL}": EmbeddingSpec(
        name=f"voyage:{VOYAGE4_MODEL}",
        dim=VOYAGE4_DIM,
        table=VOYAGE4_TABLE,
        batch_size=VOYAGE4_BATCH,
        orm_model="EmbeddingsVoyage4Large1024",
    ),
}


# ---------------------------------------------------------------------------
# DefaultOpenAIVoyageProvider — preserves the pre-Phase-2b behavior
# ---------------------------------------------------------------------------


class DefaultOpenAIVoyageProvider:
    """The aidream default. OpenAI for prose, Voyage for code.

    Imports the SDK clients lazily on first use, so a host that
    replaces the provider before any embed call never pays the SDK
    import cost (matters for matrx-local with a local fastembed
    replacement).
    """

    def __init__(
        self,
        admission: Callable[[str], AbstractAsyncContextManager[object]] | None = None,
    ) -> None:
        self._openai_client: object | None = None
        self._voyage_client: object | None = None
        self._admission = admission

    def _admit(self, model: str) -> AbstractAsyncContextManager[object]:
        if self._admission is None:
            return nullcontext()
        return self._admission(model)

    # ── Provider interface ──────────────────────────────────────────

    def known_models(self) -> list[str]:
        return list(SPECS.keys())

    def spec_for(self, model: str) -> EmbeddingSpec:
        if model not in SPECS:
            raise ValueError(f"Unknown embedding model {model!r}. Known: {sorted(SPECS.keys())}")
        return SPECS[model]

    def default_text_model(self) -> str:
        return f"voyage:{VOYAGE4_MODEL}"

    def default_code_model(self) -> str:
        return f"voyage:{VOYAGE_MODEL}"

    async def embed(
        self,
        model: str,
        texts: list[str],
        *,
        input_type: str | None = None,
    ) -> list[list[float]]:
        if not texts:
            return []

        info = self.spec_for(model)
        # Filter empties; keep their positions for zero-vector backfill.
        nonempty: list[tuple[int, str]] = [(i, t) for i, t in enumerate(texts) if t.strip()]
        if not nonempty:
            return [[0.0] * info.dim] * len(texts)

        indexes = [i for i, _ in nonempty]
        payload = [t for _, t in nonempty]

        if model.startswith("openai:"):
            vectors = await self._embed_openai(payload, info)
        elif model.startswith("voyage:"):
            vectors = await self._embed_voyage(payload, info, input_type=input_type)
        else:
            raise ValueError(f"No embedding adapter for model {model!r}")

        out: list[list[float]] = [[0.0] * info.dim] * len(texts)
        for i, vec in zip(indexes, vectors, strict=True):
            out[i] = vec
        return out

    # ── Lazy SDK clients ────────────────────────────────────────────

    def _openai(self):
        # No lock needed: asyncio is single-threaded. Both the `if` check
        # and the client construction are synchronous — there is no `await`
        # between the check and the assignment, so no other coroutine can
        # interleave. A threading.Lock would only be needed if this ran on
        # a thread pool (it does not).
        if self._openai_client is None:
            # Lazy import: matrx-local with its own provider never
            # pays the openai SDK import cost.
            from openai import AsyncOpenAI  # noqa: PLC0415

            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY not set")
            self._openai_client = AsyncOpenAI(api_key=api_key)
        return self._openai_client

    def _voyage(self):
        # No lock needed — same reasoning as _openai above.
        if self._voyage_client is None:
            import voyageai  # type: ignore[import-untyped]  # noqa: PLC0415

            api_key = os.environ.get("VOYAGE_API_KEY")
            if not api_key:
                raise RuntimeError("VOYAGE_API_KEY not set")
            self._voyage_client = voyageai.AsyncClient(api_key=api_key)
        return self._voyage_client

    # ── Adapter implementations ─────────────────────────────────────

    async def _embed_openai(self, texts: list[str], info: EmbeddingSpec) -> list[list[float]]:
        from matrx_rag._observability import announce_embedding_call  # noqa: PLC0415

        client = self._openai()

        async def embed_batch(chunk: list[str]) -> list[list[float]]:
            # Every batch is its own observable AI call. Multi-batch jobs
            # produce one START/DONE pair per batch so the operator can
            # see exactly how many round-trips the request cost.
            async with self._admit(info.name):
                with announce_embedding_call(
                    provider="openai",
                    model=OPENAI_MODEL,
                    texts=chunk,
                ) as state:
                    resp = await client.embeddings.create(model=OPENAI_MODEL, input=chunk)
                    vectors = [d.embedding for d in resp.data]
                    state["vectors_returned"] = len(vectors)
                    usage = getattr(resp, "usage", None)
                    state["actual_tokens"] = int(getattr(usage, "total_tokens", 0) or 0)
                return vectors

        results = await asyncio.gather(*map(embed_batch, _batches(texts, info.batch_size)))
        return [vector for batch in results for vector in batch]

    async def _embed_voyage(
        self,
        texts: list[str],
        info: EmbeddingSpec,
        *,
        input_type: str | None,
    ) -> list[list[float]]:
        from matrx_rag._observability import announce_embedding_call  # noqa: PLC0415

        client = self._voyage()
        voyage_input_type = None
        if input_type in ("document", "query"):
            voyage_input_type = input_type

        # The Voyage model comes from the SPEC, not a module constant — this
        # provider now serves multiple Voyage models (voyage-4-large prose,
        # voyage-code-3 code). Hardcoding VOYAGE_MODEL here silently embedded
        # every request with voyage-code-3 regardless of the requested model.
        voyage_model = info.name.split(":", 1)[1]

        async def embed_batch(chunk: list[str]) -> list[list[float]]:
            async with self._admit(info.name):
                with announce_embedding_call(
                    provider="voyage",
                    model=voyage_model,
                    texts=chunk,
                    input_type=voyage_input_type,
                ) as state:
                    resp = await client.embed(
                        chunk,
                        model=voyage_model,
                        input_type=voyage_input_type,
                    )
                    state["vectors_returned"] = len(resp.embeddings)
                    state["actual_tokens"] = int(getattr(resp, "total_tokens", 0) or 0)
                return list(resp.embeddings)

        results = await asyncio.gather(*map(embed_batch, _batches(texts, info.batch_size)))
        return [vector for batch in results for vector in batch]


def _batches(items: list[str], size: int) -> list[list[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


# ---------------------------------------------------------------------------
# Module-level facade — every existing call site keeps working.
# Each fn delegates to the configured EmbeddingProvider via _ext.
# ---------------------------------------------------------------------------


def spec_for(model: str) -> EmbeddingSpec:
    """Return the EmbeddingSpec for ``model`` from the configured provider."""
    from matrx_rag._ext import get_embedding_provider  # noqa: PLC0415

    spec = get_embedding_provider().spec_for(model)
    # Class-of-failure guard. We had a recurring bug where a caller built
    # SQL like ``INSERT INTO rag.{spec.table}`` while ``spec.table`` was
    # already ``"rag.embeddings_oai_3_small_1536"``, producing the
    # three-part identifier ``rag.rag.embeddings_oai_3_small_1536`` and
    # the Postgres "cross-database references are not implemented" error.
    # The contract is: ``spec.table`` is ALWAYS the fully-qualified
    # ``schema.table`` name. Callers MUST embed it verbatim (no schema
    # prefix). A spec that violates this contract is a programmer error
    # we want to catch loudly at boot, not silently at the first embed.
    if "." not in spec.table or spec.table.count(".") != 1:
        raise RuntimeError(
            f"EmbeddingSpec.table must be a fully-qualified 'schema.table' "
            f"identifier (got {spec.table!r}). Callers must use the qualified "
            "table value verbatim and never add another schema prefix."
        )
    return spec


def orm_model_name_for_table(table: str) -> str | None:
    """Return the matrx-orm Model class name that owns the embedding *table*,
    or ``None`` when the configured provider has no packaged model for it.

    The ONE table → ORM model lookup for the package. It reads the configured
    provider's own specs, so a host that ships custom embedding tables declares
    the mapping once (on its ``EmbeddingSpec``) instead of patching a dict in
    every writer. Replaced the twin hand-maintained registries that used to
    live in ``stages.py`` and ``ingestion.py`` (they drifted — the 2026-07-08
    content-processing embed failure)."""
    from matrx_rag._ext import get_embedding_provider  # noqa: PLC0415

    provider = get_embedding_provider()
    for model in provider.known_models():
        spec = provider.spec_for(model)
        if getattr(spec, "table", None) == table:
            return getattr(spec, "orm_model", "") or None
    return None


def default_text_model() -> str:
    from matrx_rag._ext import get_embedding_provider  # noqa: PLC0415

    return get_embedding_provider().default_text_model()


def default_code_model() -> str:
    from matrx_rag._ext import get_embedding_provider  # noqa: PLC0415

    return get_embedding_provider().default_code_model()


async def embed(
    model: str,
    texts: list[str],
    *,
    organization_id: str | None,
    input_type: str | None = None,
) -> list[list[float]]:
    """Embed a list of texts via the configured provider.

    Empty texts get a zero-vector of the model's dim so callers
    preserve a 1:1 index mapping with their input list.

    Cost shield (Phase A — Knowledge Graph plan)
    --------------------------------------------
    When a host has injected a content-addressable embedding cache via
    ``matrx_rag.configure(embedding_cache=...)`` (matrx-batch's
    ``EmbeddingCache``), each text is looked up in the cache first.
    Cache hits skip the provider call. Cache misses go to the provider
    in one batch, then their results are written back to the cache for
    future reuse.

    The ``input_type='document' | 'query'`` hint is honored by Voyage's
    asymmetric models but does NOT participate in the cache key —
    cached vectors are deterministic given (model, text). Hosts that
    mix asymmetric variants for the same text under one model should
    inject their own embedding_provider that varies the model name.

    ``organization_id`` is a REQUIRED keyword and is written onto the cache row
    as provenance: the organization whose run paid for this vector, read off the
    record being ingested (never resolved here). The cache is one cross-tenant
    row per text, so a platform-wide reindex has no tenant — that is the system
    org (the same id as ``ingestion.SYSTEM_ORG_ID``), never SQL NULL.
    """
    from matrx_rag._ext import get_embedding_cache, get_embedding_provider  # noqa: PLC0415

    provider = get_embedding_provider()
    cache = get_embedding_cache()
    if cache is None:
        return await provider.embed(model, texts, input_type=input_type)
    stamped_org = organization_id or "39c38960-d30c-4840-b0c1-c9960de95582"

    # ── Cache-aware path ────────────────────────────────────────────
    info = provider.spec_for(model)
    dim = getattr(info, "dim", None)

    # First pass — gather cache hits, identify misses.
    results: list[list[float] | None] = [None] * len(texts)
    miss_indexes: list[int] = []
    miss_texts: list[str] = []
    hit_count = 0
    hit_chars = 0

    for i, text in enumerate(texts):
        if not text or not text.strip():
            results[i] = [0.0] * (dim or 0)
            continue
        try:
            hit = await cache.get_cached(text, model)
        except Exception:
            # Cache failures must NEVER block embedding. Degrade to the
            # uncached path for this index.
            hit = None
        if hit is not None:
            results[i] = hit
            hit_count += 1
            hit_chars += len(text)
        else:
            miss_indexes.append(i)
            miss_texts.append(text)

    # Make cache hits OBSERVABLE. Without this, a fully-cached run reports
    # "$0 / 0 calls" for embeddings — which reads identically to "the
    # embeddings never ran" and triggers false alarms. The hits were paid
    # for once, in a prior run; record them (and the list-price avoided).
    if hit_count:
        from matrx_rag._observability import (  # noqa: PLC0415
            record_embedding_cache_hits,
        )

        provider_name = model.split(":", 1)[0] if ":" in model else "embedding"
        record_embedding_cache_hits(
            provider=provider_name,
            model=model,
            hits=hit_count,
            input_chars=hit_chars,
            input_type=input_type,
        )

    # Second pass — one batched provider call for all misses.
    if miss_texts:
        miss_vectors = await provider.embed(model, miss_texts, input_type=input_type)
        # Write-back. Each cache insert is independent — one failure
        # does not bring down the next.
        for idx, vec, text in zip(miss_indexes, miss_vectors, miss_texts, strict=True):
            results[idx] = vec
            try:
                # The EmbeddingCache.get_or_compute path doesn't fit here
                # (we already have the vector); fall back to the private
                # _insert if present, otherwise compute via get_or_compute
                # with an embedder shim that returns the precomputed vec.
                insert_fn = getattr(cache, "_insert", None)
                if insert_fn is not None:
                    await insert_fn(
                        _cache_key(text, model),
                        model,
                        vec,
                        organization_id=stamped_org,
                    )
                else:

                    async def _const_embedder(_t: str, _m: str) -> list[float]:
                        return vec

                    await cache.get_or_compute(
                        text,
                        model,
                        embedder=_const_embedder,
                        organization_id=stamped_org,
                    )
            except Exception:
                # Cache-write failure is non-fatal — the next call will
                # retry. Don't propagate.
                pass

    # results must now be fully populated.
    return [r if r is not None else [0.0] * (dim or 0) for r in results]


def _cache_key(text: str, model: str) -> str:
    """Local mirror of matrx_batch.compute_cache_key — kept here so
    matrx-rag never has to import matrx-batch at module load. Identical
    SHA256(`f"{model}::{text}"`) shape.
    """
    import hashlib

    return hashlib.sha256(f"{model}::{text}".encode()).hexdigest()




__all__ = [
    "EmbeddingSpec",
    "SPECS",
    "DefaultOpenAIVoyageProvider",
    "_SAFE_TABLE_RE",
    "validate_table_name",
    "default_code_model",
    "default_text_model",
    "embed",
    "orm_model_name_for_table",
    "spec_for",
]
