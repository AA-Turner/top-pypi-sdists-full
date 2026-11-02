"""
Host-injection registry for matrx-rag.

The package is standalone; the host application (aidream for the cloud
server, matrx-local for the desktop app) wires concrete implementations
via :func:`configure` at startup. Inside the package, code reads back
via :func:`get_ext` or one of the typed accessors below.

Phase 2b introduces five injection seams. All five are now in place
(2b/i: ``DocumentWriter`` + ``AuthMode``; 2b/ii: ``EmbeddingProvider``;
2b/iii: ``LLMProvider``; 2b/iv: ``VectorStore``). The Phase 2b/iv
``VectorStore`` ships the protocol and a default ``_PgVectorStoreDelegate``
wrapper; the existing aidream call sites continue to use their inline
asyncpg queries today, and incremental migration to the seam lands in
Phase 2b/iv follow-on commits.

Default behavior — what happens when a host has NOT configured a seam:

* ``DocumentWriter``: a no-op writer that warns once and skips all
  writes. This is the right default for matrx-local where local RAG
  doesn't need to persist into aidream's processed_documents tables.
  Aidream's bootstrap MUST install the real DocumentWriter — failure
  to do so degrades the PDF pipeline to "extract + chunk + embed
  succeeds, but processed_documents stays empty," which manifests as
  null page-level provenance on later searches.

* ``AuthMode``: defaults to ``user_jwt``. The cloud server explicitly
  upgrades to ``service_role`` during bootstrap; local clients leave
  it at the default.
"""

from __future__ import annotations

import enum
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


# ── AuthMode enum ───────────────────────────────────────────────────────


class AuthMode(str, enum.Enum):
    """How RAG ingest / write paths handle database authentication.

    * ``service_role`` — backend bypasses RLS via a service-role key.
      Used by aidream's scanner/runner and bulk ingest jobs.
    * ``user_jwt`` — every write goes through a per-request user-scoped
      client; RLS is the single line of authority. The default for
      matrx-local and for aidream's user-facing endpoints.
    * ``none`` — no auth context (test harnesses, local-only flows).
    """

    SERVICE_ROLE = "service_role"
    USER_JWT = "user_jwt"
    NONE = "none"


# ── DocumentWriter protocol ─────────────────────────────────────────────


@runtime_checkable
class DocumentWriter(Protocol):
    """Persists processed_documents + per-page rows during RAG ingest.

    Hosts that own the `processed_documents` schema (aidream) inject
    a writer that delegates to their persistence layer. Hosts that
    don't (matrx-local in local-RAG mode) use the no-op default.

    All methods are async to match the call sites inside the RAG
    pipelines, which run inside asyncio loops.
    """

    async def persist_processed_document(
        self,
        *,
        owner_id: str,
        organization_id: str | None,
        source_kind: str,
        source_id: str,
        name: str,
        pdf_result: Any,
        options: Any | None = None,
        storage_uri: str | None = None,
        derivation_kind: str = "initial_extract",
        derivation_metadata: dict[str, Any] | None = None,
        parent_processed_id: str | None = None,
        extra_metadata: dict[str, Any] | None = None,
        method: str | None = None,
    ) -> str:
        """Create or upsert a processed_documents row + child page rows.

        Returns the row id (UUID string). The contract matches aidream's
        ``aidream.services.documents.persistence.persist_processed_document``
        signature so the existing call sites in matrx_rag can pass
        through unchanged.
        """
        ...

    async def update_clean_content(self, doc_id: str, clean_content: str, owner_id: str) -> None:
        """Write the joined clean_content body onto a processed_documents row."""
        ...

    async def update_page_cleanup(
        self,
        *,
        doc_id: str,
        page_index: int,
        cleaned_text: str,
        section_kind: str | None = None,
        section_subtype: str | None = None,
        section_title: str | None = None,
        is_continuation: bool = False,
        extraction_confidence: float | None = None,
    ) -> None:
        """Write per-page cleanup fields."""
        ...

    async def ensure_derivative(
        self,
        *,
        intent: str,
        parent_processed_id: str,
        derivation_kind: str,
        agent_id: str | None,
        agent_version: int | str | None,
        params: dict[str, Any],
        name: str | None = None,
        rag_boost: int = 0,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        """Create or reuse a derivative ``processed_documents`` row.

        Returns an object with ``.id`` and ``.outcome`` attributes
        (matching aidream's ``DedupResult``). matrx-local's no-op
        writer returns a synthetic placeholder so callers don't crash.

        See aidream.services.documents.dedup_service.ensure_derivative
        for the canonical intent contract:
          - ``create_derivative``  -> 201 or DerivativeExistsError
          - ``get_or_create_derivative`` -> reuse or create
        """
        ...


# Exception classes that callers may want to catch. matrx_rag exposes
# them as module-level so callers can ``from matrx_rag import NotFoundError``
# without reaching into aidream's dedup_service. Aidream's bootstrap
# replaces these with its real subclasses; the package's defaults are
# usable as standalone exceptions for matrx-local.
class RagDocumentError(Exception):
    """Base class for DocumentWriter errors raised through this seam."""


class NotFoundError(RagDocumentError):
    """Raised when a referenced processed_documents row is missing."""


class DerivativeExistsError(RagDocumentError):
    """Raised by intent='create_derivative' when a matching row exists."""


# ── DerivativeIntent enum ──────────────────────────────────────────────


class DerivativeIntent(str, enum.Enum):
    """Strict-intent contract for derivative writes. Matches
    aidream.services.documents.dedup_service.DerivativeIntent."""

    CREATE_DERIVATIVE = "create_derivative"
    GET_OR_CREATE_DERIVATIVE = "get_or_create_derivative"


@dataclass(frozen=True)
class DerivativeResult:
    """Minimal result envelope mirroring aidream's DedupResult shape."""

    outcome: str
    id: str


def compute_params_hash(params: dict[str, Any] | None) -> str:
    """SHA-256 of canonical-JSON-serialized params. Order-independent.

    Same algorithm as aidream's dedup_service for byte-identical results.
    """
    import hashlib
    import json

    if not params:
        return hashlib.sha256(b"{}").hexdigest()
    canonical = json.dumps(params, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class NoOpDocumentWriter:
    """Default DocumentWriter used when no host has configured one.

    Logs a single warning the first time anything is called so
    operators see they need to wire a real writer; every subsequent
    call is silent so the log isn't spammed. Returns plausible
    placeholders so callers don't crash.
    """

    _warned = False

    def _warn_once(self, method: str) -> None:
        if not NoOpDocumentWriter._warned:
            NoOpDocumentWriter._warned = True
            logger.warning(
                "matrx_rag.DocumentWriter not configured — %s() is a no-op. "
                "Call matrx_rag.configure(document_writer=...) at host startup.",
                method,
            )

    async def persist_processed_document(
        self,
        *,
        owner_id: str,
        organization_id: str | None,
        source_kind: str,
        source_id: str,
        name: str,
        pdf_result: Any,
        options: Any | None = None,
        storage_uri: str | None = None,
        derivation_kind: str = "initial_extract",
        derivation_metadata: dict[str, Any] | None = None,
        parent_processed_id: str | None = None,
        extra_metadata: dict[str, Any] | None = None,
        method: str | None = None,
    ) -> str:
        self._warn_once("persist_processed_document")
        # Return a synthetic id so the caller can continue. The chunk
        # writes downstream will reference this id but no row exists —
        # callers that actually need processed_documents rows must wire
        # a real writer.
        import uuid as _uuid

        return str(_uuid.uuid4())

    async def update_clean_content(self, doc_id: str, clean_content: str, owner_id: str) -> None:
        self._warn_once("update_clean_content")

    async def update_page_cleanup(
        self,
        *,
        doc_id: str,
        page_index: int,
        cleaned_text: str,
        section_kind: str | None = None,
        section_subtype: str | None = None,
        section_title: str | None = None,
        is_continuation: bool = False,
        extraction_confidence: float | None = None,
    ) -> None:
        self._warn_once("update_page_cleanup")

    async def ensure_derivative(
        self,
        *,
        intent: str,
        parent_processed_id: str,
        derivation_kind: str,
        agent_id: str | None,
        agent_version: int | str | None,
        params: dict[str, Any],
        name: str | None = None,
        rag_boost: int = 0,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        self._warn_once("ensure_derivative")
        import uuid as _uuid

        return DerivativeResult(outcome="created", id=str(_uuid.uuid4()))


# ── EmbeddingProvider protocol ──────────────────────────────────────────


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Computes embeddings for chunk text or query strings.

    Aidream's default uses OpenAI (text) + Voyage (code). matrx-local
    swaps in a local provider (fastembed / sentence-transformers /
    ONNX) so PDF processing and search can run on the user's machine
    at zero per-call cost.

    The protocol is intentionally narrow: caller passes a model name +
    a list of texts, gets back vectors. Asymmetric models (Voyage) get
    a hint via ``input_type`` ('query' | 'document'). The provider is
    responsible for batching, retries, rate limiting, and per-key auth.
    """

    async def embed(
        self,
        model: str,
        texts: list[str],
        *,
        input_type: str | None = None,
    ) -> list[list[float]]:
        """Return one vector per input text. Empty strings get a zero
        vector of the model's dimensionality so callers can keep a 1:1
        index mapping. Order is preserved.
        """
        ...

    def spec_for(self, model: str) -> Any:
        """Return an ``EmbeddingSpec`` (or compatible shape) for the
        model: ``name``, ``dim``, ``table``, ``batch_size``. The
        ``table`` field is the per-model pgvector table name that the
        VectorStore writes/reads. Local providers can return any
        table name string the configured VectorStore expects."""
        ...

    def default_text_model(self) -> str:
        """Canonical 'provider:model' name to use for prose embeddings."""
        ...

    def default_code_model(self) -> str:
        """Canonical 'provider:model' name to use for code embeddings."""
        ...

    def known_models(self) -> list[str]:
        """List of accepted model names (for diagnostics + tooling)."""
        ...


# ── LLMProvider protocol ───────────────────────────────────────────────


@runtime_checkable
class LLMProvider(Protocol):
    """Chat-completion provider used by the RAG package for the remaining
    direct (non-agent, non-embedding) LLM work: NER grounding judgment in the
    NER engine. (The four RAG LLM jobs — PDF cleanup, contextualize,
    query-expand, HyDE — no longer use this; they go through the required
    ``RagAgentRunner``.)

    Aidream's default uses OpenAI directly (gpt-4o-mini). matrx-local replaces
    this with a local llama-server / Ollama adapter that speaks the same shape
    so the grounding call runs offline.

    ``chat`` is required; ``chat_stream`` is optional (callers degrade to
    ``chat`` when a provider omits it). Per-call model selection stays in
    ``matrx_rag.llm`` so the seam stays narrow.

    **The provider owns sampling-param policy, not the caller.** A provider that
    routes through a real model catalog (aidream's matrx-ai bridge) drops
    ``temperature``/``top_p``/``top_k`` for api_classes that reject them — the
    adaptive Anthropic models (claude 4.6+ / the claude-5 family) hard-400 on
    ANY sampling param. Callers therefore pass ``temperature`` freely and NEVER
    branch on a model name. (The old ``supports_sampling_params`` probe existed
    only because grounding.py talked to the Anthropic SDK directly; it doesn't
    anymore, so the probe is gone.)
    """

    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: str | None = None,  # 'json' | 'text' | None
        timeout: float | None = None,
        purpose: str | None = None,
        offered: dict[str, Any] | None = None,
        offering_id: str | None = None,
    ) -> str:
        """Return the assistant's message content as a string. For
        ``response_format='json'`` the string IS the JSON object
        returned by the model (the caller is responsible for parsing).

        ``purpose`` is an optional free-form tag the caller passes
        ("pdf_cleanup", "contextual_retrieval", "hyde", "multi_query",
        "ner_postprocess") so the default observability layer can label
        each chat round-trip in the operator-visible trace. Custom
        providers MAY honor or ignore it.

        ``offered`` is the call's data BY NAME (``{"answer": ...}``,
        ``{"passages": ..., "claims": ...}``, ``{"image": {"file_id": ...}}``)
        — the same values ``messages`` carries composed. A host that holds the
        call by a mandate hands them to whatever fills it, so a workflow Holder
        receives named inputs instead of one composed turn it cannot split.
        Optional: callers pass it through :func:`provider_call_kwargs`, which
        leaves it out for a provider whose signature does not take it.

        ``offering_id`` is the chosen CLASS of ``model`` (its serving endpoint,
        e.g. "Matrx Fast" / "Matrx Lightning" — an id the host's catalog knows).
        It belongs to ``model`` only; ``None`` = the model's preferred class.
        Passed through :func:`provider_call_kwargs` as well.
        """
        ...

    async def chat_stream(
        self,
        messages: list[dict[str, str]],
        *,
        model: str,
        on_delta: Callable[[str], Awaitable[None]],
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: str | None = None,
        timeout: float | None = None,  # noqa: ASYNC109 — part of the LLMProvider seam contract
        purpose: str | None = None,
        offered: dict[str, Any] | None = None,
        offering_id: str | None = None,
    ) -> str:
        """OPTIONAL. Same as :meth:`chat`, but invokes ``on_delta(text)`` for
        each token as it arrives, and returns the full assistant text.

        This exists so a caller can report REAL incremental progress — the
        grounding judge parses each verdict object out of the streaming JSON
        array the moment it completes, rather than faking a burst of progress
        after the call returns.

        Providers MAY omit this. Callers MUST degrade gracefully to ``chat``
        (and accept that progress then arrives in one batch)."""
        ...


def provider_call_kwargs(
    method: Any,
    offered: dict[str, Any] | None,
    *,
    offering_id: str | None = None,
) -> dict[str, Any]:
    """``{"offered": ..., "offering_id": ...}`` — each only when ``method`` accepts it.

    ``offered`` joined the seam on 2026-09-26 and ``offering_id`` (the model's
    chosen class) on 2026-10-02; a provider written before either
    (matrx-local's local-model adapter, a third-party host) keeps working
    unchanged — it simply does not receive them. A class the provider cannot
    take is announced, never silently lost.
    """
    if not offered and not offering_id:
        return {}
    import inspect

    try:
        params = inspect.signature(method).parameters
    except (TypeError, ValueError):
        params = {}
    takes_any = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())
    out: dict[str, Any] = {}
    if offered and ("offered" in params or takes_any):
        out["offered"] = dict(offered)
    if offering_id:
        if "offering_id" in params or takes_any:
            out["offering_id"] = str(offering_id)
        else:
            logger.warning(
                "matrx_rag: the configured llm_provider does not accept offering_id — "
                "class %s cannot ride this call; the model runs its preferred class.",
                offering_id,
            )
    return out


# ── RagAgentRunner protocol ─────────────────────────────────────────────


@runtime_checkable
class RagAgentRunner(Protocol):
    """Runs the RAG pipeline's LLM jobs through the HOST's agent system
    (``agx_agent`` + matrx-ai's UnifiedAIClient) instead of a raw provider
    call, so every call gets cost/usage attribution, version pinning, and
    admin-editable prompts.

    matrx-rag MUST NOT import matrx-ai (package independence), so this is the
    injection seam: the host wires an implementation via
    ``configure(rag_agent_runner=...)`` that delegates to four pinned
    ``NamedAgent``s. This runner is REQUIRED — ``matrx_rag.llm`` runs its LLM
    jobs exclusively through it. When nothing is injected,
    ``matrx_rag.llm._require_runner()`` raises loudly (a host-config error);
    there is no raw-provider fallback.

    Contract: each method runs ONE agent and returns the post-parse value.
    Shared assembly (prepend original query, dedup, cap-to-n, field
    normalization) stays in ``matrx_rag.llm`` so it lives in exactly one
    place. A method RAISES on agent failure; ``matrx_rag.llm`` catches and
    applies a loud fallback (raw text for the cleaner, empty for the others)
    so an incomplete result is never silent.
    """

    async def clean_page(self, raw_text: str, *, timeout: float | None = None) -> dict[str, Any]:
        """Run the page-cleaner agent. Returns the parsed object with keys
        ``text``, ``section_kind``, ``section_subtype``, ``section_title``,
        ``is_continuation`` (values as the model produced them; the caller
        normalizes). Raises on failure."""
        ...

    async def contextualize(
        self, document: str, chunk: str, *, timeout: float | None = None
    ) -> str:
        """Run the chunk-contextualizer agent. Returns the prefix string
        (already stripped). Raises on failure."""
        ...

    async def expand_query(
        self, query: str, *, n: int = 3, timeout: float | None = None
    ) -> list[str]:
        """Run the query-expander agent. Returns the model's paraphrase lines
        (NOT including the original query, NOT yet deduped/capped — the caller
        assembles). Raises on failure."""
        ...

    async def hyde(self, query: str, *, timeout: float | None = None) -> str:
        """Run the HyDE agent. Returns the hypothetical passage (already
        stripped). Raises on failure."""
        ...


@runtime_checkable
class Reranker(Protocol):
    """Host-owned cross-encoder reranker.

    RAG owns candidate selection and score application, while the host owns
    the provider client, credential lifecycle, SDK dependency, and model
    selection. An absent reranker deliberately means that search keeps its
    fused order.

    ``model`` (optional attribute) names the model ``rerank`` will use. A host
    that declares it gets the durable rerank-result cache
    (``matrx_rag.rerank_cache``): the same model, query and passage contents
    return the stored scores instead of a fresh, drifting provider call. A
    reranker without it reranks live every time.
    """

    async def rerank(self, query: str, documents: list[str]) -> RerankResult:
        """Return host-selected model metadata and scores in input order."""
        ...


@dataclass(frozen=True)
class RerankResult:
    """Scores from a host-owned reranker and the model that produced them."""

    scores: list[float]
    model: str


# ── VectorStore protocol ────────────────────────────────────────────────


@runtime_checkable
class VectorStore(Protocol):
    """Backend for storing + querying chunks and their embeddings.

    Aidream's default uses pgvector (one ``rag.embeddings_*`` table per
    embedding model) with hybrid retrieval (vector + lexical). matrx-
    local with a bundled Postgres uses the same default. matrx-local
    running purely offline can plug in sqlite-vss / DuckDB / chroma /
    in-memory faiss without touching any RAG call site.

    Phase 2b/iv scope note
    ----------------------
    The protocol is defined here; the call-site migrations land in
    follow-on commits as the matrx-local local-RAG MVP develops
    concrete usage patterns. Today, aidream's call sites continue
    to use their inline asyncpg SQL — the default VectorStore is a
    thin wrapper for hosts that want to opt in NOW; pgvector remains
    the canonical implementation.
    """

    async def upsert_chunks(
        self,
        *,
        chunks: list[Any],  # list[matrx_rag.chunking.Chunk]
        embeddings: list[list[float]],
        embedding_model: str,
        scope: dict[str, Any],  # {organization_id, owner_id, source_kind,
        #  source_id, field_id, source_hash, mime_type,
        #  processed_document_id, page_id_lookup}
    ) -> int:
        """Replace prior chunks for the source identity then write the
        new set + their embedding rows. Returns the count of chunks
        written. Idempotent on the source identity tuple."""
        ...

    async def vector_recall(
        self,
        *,
        query_vector: list[float],
        embedding_model: str,
        organization_id: str | None,
        owner_id: str | None,
        source_kinds: list[str] | None = None,
        include_sources: list[dict[str, str]] | None = None,
        only_children: bool = True,
        library_filter: str = "any",
        limit: int = 100,
    ) -> list[str]:
        """Return chunk_ids ranked by vector similarity, top-N."""
        ...

    async def lexical_recall(
        self,
        *,
        query: str,
        organization_id: str | None,
        owner_id: str | None,
        source_kinds: list[str] | None = None,
        include_sources: list[dict[str, str]] | None = None,
        only_children: bool = True,
        library_filter: str = "any",
        limit: int = 100,
    ) -> list[str]:
        """Return chunk_ids ranked by lexical (BM25 / ts_rank) score."""
        ...

    async def delete_by_source(
        self,
        *,
        source_kind: str,
        source_id: str,
        field_id: str | None = None,
    ) -> int:
        """Hard-delete all chunks (+ cascading embedding rows) for a
        given source identity. Used during re-extraction."""
        ...


class _PgVectorStoreDelegate:
    """Default VectorStore — delegates to the existing aidream/matrx-rag
    inline asyncpg SQL paths.

    The aidream pgvector-backed call sites haven't been migrated yet
    (Phase 2b/iv follow-on); this class exists so hosts that want a
    typed VectorStore accessor can use it, AND so the protocol has a
    runtime-checkable default. Each method imports the relevant
    package module lazily and delegates.

    matrx-local can implement its own VectorStore against any local
    backend without depending on the asyncpg pool.
    """

    async def upsert_chunks(self, *, chunks, embeddings, embedding_model, scope):
        # Phase 2b/iv follow-on — the existing matrx_rag.ingestion.upsert_chunks
        # signature takes a fully-resolved ``ResolvedSource`` (with text +
        # language fields used during chunking metadata composition).
        # Mapping the narrow ``scope`` dict onto that shape requires the
        # call-site migration that lands in the follow-on commit; until
        # then, hosts that want this seam wired must supply their own
        # VectorStore impl.
        raise NotImplementedError(
            "VectorStore.upsert_chunks: default delegate not yet wired "
            "to matrx_rag.ingestion.upsert_chunks; coming in Phase 2b/iv "
            "follow-on alongside the search-path migration. Override by "
            "configuring a custom VectorStore via "
            "matrx_rag.configure(vector_store=...)."
        )

    async def vector_recall(self, **kwargs):
        # Phase 2b/iv follow-on — wire to matrx_rag.search._vector_recall
        # when the migration commits land. Until then this is a stub
        # that callers don't yet hit (search.py still uses its inline
        # asyncpg query directly).
        raise NotImplementedError(
            "VectorStore.vector_recall: default delegate not yet wired "
            "to matrx_rag.search._vector_recall; coming in Phase 2b/iv "
            "follow-on. Override by configuring a custom VectorStore."
        )

    async def lexical_recall(self, **kwargs):
        raise NotImplementedError(
            "VectorStore.lexical_recall: default delegate not yet wired "
            "to matrx_rag.search._lexical_recall; coming in Phase 2b/iv "
            "follow-on. Override by configuring a custom VectorStore."
        )

    async def delete_by_source(self, *, source_kind, source_id, field_id=None):
        # NOTE: this uses the package's service-role ORM model, not an
        # auth-mode-aware client. Callers running under
        # ``AuthMode.USER_JWT`` who need RLS-scoped deletes must supply
        # their own VectorStore. The default is appropriate for aidream's
        # service-role ingest paths.
        #
        # ``delete_where(field_id=None)`` renders ``field_id IS NULL`` and
        # ``delete_where(field_id=x)`` renders ``field_id = x`` — equivalent to
        # the historical raw ``IS NOT DISTINCT FROM`` for both cases
        # (verified against matrx_orm.query.executor._build_condition).
        KgChunks = get_db_model("KgChunks")
        # hard-delete-ok: derived search chunks, rebuilt on re-ingest of their source
        return await KgChunks.delete_where(
            source_kind=source_kind,
            source_id=source_id,
            field_id=field_id,
        )


# ── Registry ────────────────────────────────────────────────────────────


# Lazy-importing default — avoids loading the openai/voyageai SDKs at
# module-import time. Hosts that configure their own provider never
# pay the SDK import cost.
_default_embedding_provider_singleton: Any = None
_default_vector_store_singleton: Any = None


def _default_embedding_provider() -> Any:
    """Return the cached default OpenAI+Voyage provider, building it
    on first access. matrx-local that wants to skip the cloud SDKs
    must call configure(embedding_provider=...) BEFORE anything in
    the package tries to embed."""
    global _default_embedding_provider_singleton
    if _default_embedding_provider_singleton is None:
        # Local import keeps openai/voyageai import work off the
        # _ext module load path; matters when matrx-local replaces
        # the provider before anything triggers embed.
        from matrx_rag.embeddings import DefaultOpenAIVoyageProvider

        _default_embedding_provider_singleton = DefaultOpenAIVoyageProvider()
    return _default_embedding_provider_singleton


class LLMProviderNotConfigured(RuntimeError):
    """No host LLM provider was injected, so matrx-rag refuses the call.

    There is deliberately NO default. matrx-rag used to fall back to a raw
    OpenAI chat client with code-chosen models (BYPASS-CENSUS aidream, 2026-09-25):
    a paid intelligence call no mandate held and no catalog priced. A host
    supplies the provider — aidream's ``MatrxAILLMProvider`` holds every call
    through its mandate; matrx-local injects its local-model adapter.
    """

    def __init__(self) -> None:
        super().__init__(
            "matrx-rag has no LLM provider: call matrx_rag.configure(llm_provider=<your "
            "LLMProvider>) at startup. There is no built-in default — a raw provider "
            "client would run intelligence no mandate holds."
        )


def _default_vector_store() -> Any:
    """Cached default ``_PgVectorStoreDelegate``. Lazy so matrx-local with
    a non-pgvector backend never imports asyncpg / aidream's pool."""
    global _default_vector_store_singleton
    if _default_vector_store_singleton is None:
        _default_vector_store_singleton = _PgVectorStoreDelegate()
    return _default_vector_store_singleton


_registry: dict[str, Any] = {
    "document_writer": NoOpDocumentWriter(),
    "auth_mode": AuthMode.USER_JWT,
    # SourceKind values that the DocumentWriter accepts; mirrored from
    # aidream's enum so call sites can compose DocSourceKind.cld_file
    # etc. Hosts may override with their own enum-like.
    "source_kind_cld_file": "cld_file",
    "source_kind_note": "note",
    "source_kind_code_file": "code_file",
    "source_kind_inline": "inline",
    "source_kind_external_url": "external_url",
    "source_kind_legacy": "legacy",
    # embedding_provider is None until first get_embedding_provider()
    # call so we can lazy-import openai/voyageai only when needed.
    "embedding_provider": None,
    # llm_provider is None until first get_llm_provider() call. Default
    # routes through the same lazy AsyncOpenAI client as embeddings.
    "llm_provider": None,
    # rag_agent_runner is None until the host injects an agent-backed runner
    # (aidream wires aidream/services/rag_agents.py). When set, matrx_rag.llm
    # routes PDF cleanup / contextualization / query expansion / HyDE through
    # the host's agx agent system (cost + version tracking). When None, llm.py
    # uses the raw llm_provider path — standalone / matrx-local behavior.
    "rag_agent_runner": None,
    # Provider SDKs never live in matrx-rag. Hosts that want cross-encoder
    # reranking inject a Reranker; an absent seam leaves fusion order intact.
    "reranker": None,
    # vector_store is None until first get_vector_store() call. Default
    # is the pgvector delegate — usable by hosts that opt in. The bulk
    # of aidream's call sites still go through inline asyncpg SQL today
    # (Phase 2b/iv migration is incremental).
    "vector_store": None,
    # embedding_cache is None until the host wires matrx-batch in. When
    # injected, embeddings.embed() routes per-text reads/writes through
    # the cache before paying the provider call. Phase A of the KG plan.
    "embedding_cache": None,
    # ner_extractor is None until the host wires it (aidream injects an
    # adapter that runs the kg_ner_extractor_v1 agent via matrx-ai). matrx-rag
    # MUST NOT import matrx-ai (not a dependency), so NER extraction is
    # injection-only: with no extractor wired, ner.extract_entities is a clean
    # no-op (NerResult with skipped="no_extractor"). Phase C of the KG plan.
    "ner_extractor": None,
    # ner_finisher is None until the host injects a big-model post-processor.
    # When set, ``ner.extract_entities`` calls it ONCE per source between
    # tier A (parallel span extraction) and tier B (entity dedup/persist),
    # passing the union of normalized spans from every chunk. The finisher
    # returns a curated span list (deduped, canonicalised, cross-chunk
    # grouped). When None, the raw tier-A output is used as-is — the
    # current GLiNER-only behavior. Phase C+ of the KG plan.
    "ner_finisher": None,
    # page_image_renderer is None until the host injects an async callable that
    # rasterizes one page of a stored document to an image row. When None,
    # figure-caption derivation simply SKIPS auto-render and captions only the
    # pages that already have images — a degraded capability, never a crash.
    "page_image_renderer": None,
    # default_vision_model is None until the host names the model its
    # llm_provider should use for figure/image captioning. It is a HOST
    # CATALOG identifier (an id or a name the host's provider resolves) —
    # there is no universal default, so matrx-rag ships none.
    "default_vision_model": None,
    # cloud_file_manager_provider is None until the host injects a zero-arg
    # callable returning its cloud-enabled FileManager (aidream wires
    # common.cloud_files.get_cloud_file_manager). matrx-rag MUST NOT import
    # aidream, so cld_file byte resolution (PDF/table/image derivation paths)
    # is injection-only: get_cloud_file_manager() raises RagNotConfiguredError
    # when unconfigured — never a silent fallback.
    "cloud_file_manager_provider": None,
    # ``human_authored_text`` is the projection that answers "what did the
    # HUMAN actually say on this stored message row". On a role='user' row,
    # ``content`` is the complete provider payload (an agent definition's
    # seeded opening turn + resolved launch variables + what the person
    # typed, merged so model replay stays lossless) and ``user_content`` is
    # the authorship record. Indexing ``content`` for a user row therefore
    # lets a seeded template or a host-injected notice be retrieved and
    # quoted back as the person's words (D327). matrx-rag sits BELOW matrx-ai
    # in the dependency graph and cannot import matrx-ai's
    # ``human_authored_text``, so the host injects it here; unconfigured, the
    # package applies its own implementation of the same rule
    # (``default_human_authored_text`` below). Never a silent "index
    # everything" fallback.
    "human_authored_text": None,
    # ``univer_text_renderer`` renders a Univer snapshot (the stored body of a
    # workbook or a cloud document) to plain text: ``(kind, snapshot) -> str``
    # with kind ``"workbook"`` | ``"udt_document"``. The Univer model lives in
    # the host (aidream.services.udt_content); matrx-rag cannot import it, so
    # the host injects its ONE renderer. Unconfigured, resolving those kinds
    # raises RagNotConfiguredError — never a silent empty body.
    "univer_text_renderer": None,
    # ``univer_current_reader`` answers what a co-edited workbook or cloud
    # document holds NOW (its live room folded past the last save):
    # ``async (kind, source_id, user_id) -> (snapshot, staleness) | None``;
    # ``None`` means no live room, so the latest snapshot is current. Optional:
    # unconfigured, the latest snapshot is read (and says nothing more).
    "univer_current_reader": None,
    # ── Database injection (mirrors matrx-ai's db._registry pattern) ─────
    # ``db_config_name`` is the matrx-orm pool identifier the host registered
    # via ``matrx_orm.register_database_from_env(...)``. Hosts (aidream)
    # inject their name here so matrx-rag never has to know it — exactly
    # like matrx-ai injects its DB models via configure(). Standalone
    # consumers (matrx-local, tests) either inject their own pool name or
    # set the ``MATRX_DB_CONFIG_NAME`` env var; if neither is provided, the
    # accessor raises a clear RagNotConfiguredError instead of falling back
    # to an aidream-specific default that would silently misroute in other
    # hosts. Aidream-specific names belong in aidream/package_integration.py.
    "db_config_name": None,
    # ``db_models`` is a host-provided map of name → matrx-orm Model class
    # for the rag.* schema (KgChunks, KgEntities, etc.). matrx-rag itself
    # uses raw asyncpg today; this slot is the seam for the incremental
    # ORM migration. New code that wants ORM access in matrx-rag reads via
    # get_db_model("KgChunks") so the model can be injected by the host
    # without matrx-rag importing aidream's db/models_rag.py.
    "db_models": {},
    # ``clean_single_flight`` is None until the host injects
    # ``(processed_document_id) -> async context manager``. Every page clean of a
    # document (``stages.run_clean``, the pdf_pipeline clean step) runs inside it,
    # so the host can guarantee ONE clean per document across every replica
    # (aidream: a durable claim row). The manager raises to refuse a duplicate;
    # it must be re-entrant for a flow that already holds the document. Unset =
    # no cross-process guard (standalone / matrx-local single-process use).
    "clean_single_flight": None,
    # ``clean_fence`` is None until the host injects
    # ``async (processed_document_id) -> None`` that RAISES when the clean hold this
    # flow entered through ``clean_single_flight`` is no longer its own (lease lost
    # / taken over). Called before every page clean (LLM spend) and every
    # page/document write of a held clean, so a driver that lost its hold stops
    # instead of cleaning and writing alongside the one that took over. Unset =
    # no-op (standalone single-process use).
    "clean_fence": None,
    # ``clean_follow`` is None until the host injects
    # ``async (processed_document_id, run, *, resume=False) -> result``: run a clean
    # and, when ANOTHER driver holds the document, wait for that holder instead of
    # failing (aidream: ``documents.clean_claim.clean_following_holder``). Server-
    # internal pipeline cleans (``run_all``, the PDF ingest) go through it; unset =
    # ``await run()`` (the single-flight seam's refusal propagates).
    "clean_follow": None,
}
_configured = False


class RagNotConfiguredError(RuntimeError):
    pass


@runtime_checkable
class NerExtractor(Protocol):
    """Runs the host's NER extractor agent against one chunk of text and
    returns the parsed entity list.

    matrx-rag owns the schema + the dedup/mention/edge write path, but the
    LLM call itself lives in the host (aidream runs the seeded
    ``kg_ner_extractor_v1`` agent through matrx-ai and parses its output with
    the one-funnel ``parse_agent_output``). The host injects an implementation
    of this protocol via ``configure(ner_extractor=...)``.

    The implementation MUST:
      * run the extractor agent with ``chunk`` bound to ``text``,
      * parse the structured output via ``parse_agent_output`` (NEVER a
        hand-rolled JSON scraper — the one-funnel rule),
      * return a list of ``{kind, canonical_name, span_start, span_end,
        confidence, attrs?}`` dicts (already validated against the agent's
        ``output_schema``), and
      * return an empty list (never raise) when nothing was extractable, so a
        single bad chunk never aborts an ingest.
    """

    async def extract(
        self,
        text: str,
        *,
        organization_id: str | None,
        user_id: str,
        source_kind: str | None = None,
        source_id: str | None = None,
    ) -> list[dict[str, Any]]: ...


def decode_content_blocks(value: Any) -> Any:
    """Normalize a stored ``content`` / ``user_content`` JSONB value to blocks.

    asyncpg decodes JSONB as a Python list, a dict, or a raw JSON *string*
    depending on codec registration. Every projection downstream expects the
    block list, and handing a raw JSON string to a text projection makes it
    return the JSON source itself — which would be embedded and retrieved as
    if a person had typed it. Normalizing here is what makes the injected
    host projection safe to call.

    Returns the block list, or ``None`` when the value is SQL NULL (which
    ``human_authored_text`` reads as "this row predates the authorship
    contract"), or ``[]`` when the value is present but unusable.
    """
    if value is None:
        return None
    if isinstance(value, str):
        import json as _json

        try:
            value = _json.loads(value)
        except Exception:
            return []
        if value is None:
            # A JSONB 'null' literal is still the absence of authorship.
            return None
    if isinstance(value, dict):
        # Anthropic single-block shorthand: {"type": "text", "text": "..."}
        return [value]
    if isinstance(value, list):
        return value
    return []


def content_blocks_to_text(blocks: Any) -> str:
    """Text blocks only, joined with blank lines. Tool machinery is not speech.

    Blocks of any other type (tool_use, tool_result, image, …) are skipped —
    they carry no human-readable text to embed.
    """
    if not isinstance(blocks, list):
        return ""
    parts: list[str] = []
    for block in blocks:
        if isinstance(block, str):
            text = block.strip()
            if text:
                parts.append(text)
            continue
        if not isinstance(block, dict):
            continue
        if block.get("type", "text") in ("text", "input_text"):
            text = (block.get("text") or "").strip()
            if text:
                parts.append(text)
    return "\n\n".join(parts).strip()


def default_human_authored_text(role: Any, content: Any, user_content: Any) -> str:
    """The package's own implementation of the authorship projection (D327).

    Identical in rule to the host's (matrx-ai's ``human_authored_text``);
    only the text flattening is matrx-rag's own, so an unconfigured host
    still never indexes a seeded template as the person's words:

      * a non-user row is never a human turn under this contract → its
        ``content`` is returned as-is;
      * a user row with ``user_content`` NOT NULL → exactly that, even when
        it is empty (empty means the human wrote nothing — a host-injected
        turn, which must project to "" and be dropped by the caller);
      * a user row with ``user_content`` NULL → ``content``, because NULL
        means the row predates this contract, not that the input was empty.
    """
    role_value = getattr(role, "value", role)
    if str(role_value) == "user" and user_content is not None:
        return content_blocks_to_text(user_content)
    return content_blocks_to_text(content)


def get_univer_text_renderer() -> Any:
    """Return the host's Univer snapshot renderer, ``(kind, snapshot) -> str``.

    Raises :class:`RagNotConfiguredError` when the host never injected one —
    a workbook or cloud document is never indexed as an empty body.
    """
    renderer = _registry.get("univer_text_renderer")
    if renderer is None:
        raise RagNotConfiguredError(
            "matrx-rag univer_text_renderer is not configured: workbooks and cloud "
            "documents cannot be read. Call matrx_rag.configure(univer_text_renderer=...)."
        )
    return renderer


def get_univer_current_reader() -> Any:
    """The host's co-editing reader, ``async (kind, source_id, user_id) -> (snapshot, staleness) | None``, or None."""
    return _registry.get("univer_current_reader")


def get_human_authored_text() -> Any:
    """Return the configured authorship projection, or the package default.

    Signature: ``(role, content, user_content) -> str``, taking the already
    decoded block lists (see :func:`decode_content_blocks`).
    """
    projection = _registry.get("human_authored_text")
    if projection is None:
        return default_human_authored_text
    return projection


async def get_typed_chat_policy() -> Any:
    """The host's :class:`~matrx_rag.chat_authorship.TypedChatPolicy`, read fresh.

    Raises :class:`RagNotConfiguredError` when the host injected none: whose words a chat holds
    is the host's ruling, never a package default."""
    provider = _registry.get("typed_chat_policy")
    if provider is None:
        raise RagNotConfiguredError(
            "matrx-rag typed_chat_policy is not configured: a conversation cannot be read as the "
            "person's typed words. Call matrx_rag.configure(typed_chat_policy=...)."
        )
    return await provider()


def configure(
    *,
    document_writer: DocumentWriter | None = None,
    embedding_provider: EmbeddingProvider | None = None,
    llm_provider: LLMProvider | None = None,
    rag_agent_runner: RagAgentRunner | None = None,
    reranker: Reranker | None = None,
    vector_store: VectorStore | None = None,
    embedding_cache: Any | None = None,
    ner_extractor: NerExtractor | None = None,
    ner_finisher: Any | None = None,
    page_image_renderer: Any | None = None,
    default_vision_model: str | None = None,
    cloud_file_manager_provider: Any | None = None,
    human_authored_text: Any | None = None,
    typed_chat_policy: Any | None = None,
    univer_text_renderer: Any | None = None,
    univer_current_reader: Any | None = None,
    auth_mode: AuthMode | str | None = None,
    source_kind_aliases: dict[str, str] | None = None,
    not_found_error_class: type[Exception] | None = None,
    derivative_exists_error_class: type[Exception] | None = None,
    db_config_name: str | None = None,
    db_models: dict[str, Any] | None = None,
    scope_access: Any | None = None,
    embedding_spend_sink: Any | None = None,
    clean_single_flight: Any | None = None,
    clean_follow: Any | None = None,
    clean_fence: Any | None = None,
) -> None:
    """Wire host-supplied seams. Call once at app startup.

    ``scope_access`` — ``async (scope_ids, user_id) -> [scope ids the person may open]``. The
    host answers from its record store (a scope is a Record there); this package owns no scope
    table and never reads one, so a scope-narrowed search with no seam wired refuses by name.

    Args:
        document_writer: an object implementing the
            :class:`DocumentWriter` protocol. Aidream injects its
            ``aidream.services.documents.persistence`` adapter; matrx-
            local uses the default no-op for local-RAG mode (matrx-
            local doesn't write to aidream's processed_documents).
        embedding_provider: an object implementing the
            :class:`EmbeddingProvider` protocol. Aidream uses the
            built-in OpenAI+Voyage default; matrx-local injects a
            local provider (fastembed / sentence-transformers / ONNX)
            so embeddings run on the user's machine at zero cost.
        llm_provider: an object implementing the :class:`LLMProvider`
            protocol. Aidream uses the built-in OpenAI default; matrx-
            local injects a local llama-server / Ollama adapter so the
            remaining direct chat call (NER grounding in the NER engine)
            runs offline. (The four RAG LLM jobs no longer use this — they
            go through ``rag_agent_runner``.)
        rag_agent_runner: an object implementing the :class:`RagAgentRunner`
            protocol. REQUIRED for ``matrx_rag.llm`` — the four RAG LLM jobs
            (PDF cleanup, contextualize, query-expand, HyDE) route through
            the host's agx agent system for cost/usage tracking and version
            pinning. If not injected, those jobs raise loudly at first call;
            there is no raw-provider fallback.
        reranker: host-owned cross-encoder adapter. This package never imports
            a reranking SDK; without this seam, optional reranking is off.
        vector_store: an object implementing the :class:`VectorStore`
            protocol. Aidream uses the built-in pgvector delegate;
            matrx-local without a Postgres can plug in sqlite-vss /
            DuckDB / in-memory faiss without touching any call site.
        human_authored_text: the host's authorship projection,
            ``(role, content, user_content) -> str`` over decoded content
            blocks. Aidream injects ``matrx_ai.config.human_authored_text``
            so this package and the rest of the platform read a stored
            message's human words through the SAME rule (D327). Omit it and
            the package applies its own implementation of that rule
            (:func:`default_human_authored_text`) — never a fallback that
            indexes the whole provider payload as the person's words.
        typed_chat_policy: ``async () -> matrx_rag.chat_authorship.TypedChatPolicy`` — the
            host's thresholds for whose words a chat holds (conversation types, origin classes,
            mirror apps, template repetition). Read on every typed-chat resolve; without it a
            conversation never resolves (refused by name — no package guess decides whose
            words are indexed).
        univer_text_renderer: ``(kind, snapshot) -> str`` rendering a
            workbook (``kind="workbook"``) or cloud document
            (``kind="udt_document"``) Univer snapshot to text. Aidream injects
            its udt_content renderer; without it those kinds cannot resolve.
        univer_current_reader: ``async (kind, source_id, user_id) ->
            (snapshot, staleness) | None`` — the content of a record people are
            co-editing now (its room folded to head); ``None`` = no live room.
        auth_mode: controls how DB writes authenticate. Default
            :attr:`AuthMode.USER_JWT`. Aidream may upgrade to
            :attr:`AuthMode.SERVICE_ROLE` for backend ingest paths.
        source_kind_aliases: override the source-kind enum values
            (e.g., if a host's SourceKind enum uses different string
            values for 'cld_file' etc.). Rarely needed.
        not_found_error_class: when the host has its own NotFoundError
            class that downstream callers do ``except NotFoundError``
            against (aidream does), pass it here so matrx-rag raises
            an instance of THAT class instead of the package's
            default. Preserves existing isinstance/except contracts.
        derivative_exists_error_class: same idea for the 'derivative
            already exists' error type.
        db_config_name: matrx-orm pool identifier the host registered
            via ``matrx_orm.register_database_from_env(...)``. Passing it
            also binds the package's own model classes to that pool — a
            matrx-orm name alias maps ``"matrx_rag"`` (the ``_database``
            every packaged model bakes) onto the host's config, so hosted
            runs share ONE physical pool. Aidream injects
            ``"supabase_automation_matrix"``; other hosts inject their own
            name (or set ``MATRX_DB_CONFIG_NAME``). Standalone installs skip
            this and call ``matrx_rag.db.bootstrap_db()`` instead. Hosts
            using a non-postgres VectorStore never need either.
        db_models: optional host-provided map of name → matrx-orm Model
            class — an OVERRIDE for hosts whose database genuinely
            diverges from the canonical Matrx schema. The package ships
            its own canonical model classes (``matrx_rag.db.models_docproc`` /
            ``matrx_rag.db.models_rag``); normal hosts should NOT pass
            this. Injected entries win over the registry lookup in
            ``get_db_model``/``try_get_db_model``.
    """
    global _configured
    if document_writer is not None:
        _registry["document_writer"] = document_writer
    if embedding_provider is not None:
        _registry["embedding_provider"] = embedding_provider
    if llm_provider is not None:
        _registry["llm_provider"] = llm_provider
    if rag_agent_runner is not None:
        _registry["rag_agent_runner"] = rag_agent_runner
    if reranker is not None:
        _registry["reranker"] = reranker
    if vector_store is not None:
        _registry["vector_store"] = vector_store
    if embedding_cache is not None:
        _registry["embedding_cache"] = embedding_cache
    if ner_extractor is not None:
        _registry["ner_extractor"] = ner_extractor
    if ner_finisher is not None:
        _registry["ner_finisher"] = ner_finisher
    if page_image_renderer is not None:
        _registry["page_image_renderer"] = page_image_renderer
    if default_vision_model is not None:
        _registry["default_vision_model"] = default_vision_model
    if cloud_file_manager_provider is not None:
        _registry["cloud_file_manager_provider"] = cloud_file_manager_provider
    if human_authored_text is not None:
        _registry["human_authored_text"] = human_authored_text
    if typed_chat_policy is not None:
        _registry["typed_chat_policy"] = typed_chat_policy
    if univer_text_renderer is not None:
        _registry["univer_text_renderer"] = univer_text_renderer
    if univer_current_reader is not None:
        _registry["univer_current_reader"] = univer_current_reader
    if scope_access is not None:
        _registry["scope_access"] = scope_access
    if embedding_spend_sink is not None:
        # ``(provider, model, tokens, cost_usd, cost_is_exact, input_type, batch_size) -> None``,
        # SYNC, called once per successful embeddings call with its measured cost. The package's
        # direct OpenAI / Voyage calls spend outside any host billing seam; this is how the host
        # bills the person and organization the call served. Must never raise into the call.
        _registry["embedding_spend_sink"] = embedding_spend_sink
    if clean_single_flight is not None:
        _registry["clean_single_flight"] = clean_single_flight
    if clean_follow is not None:
        _registry["clean_follow"] = clean_follow
    if clean_fence is not None:
        _registry["clean_fence"] = clean_fence
    if db_config_name is not None:
        _registry["db_config_name"] = db_config_name
        # Bind the package's model classes to the host's pool now when the
        # host already registered it (the normal startup order). If the pool
        # isn't registered yet, the bind happens lazily on first get_pool().
        try:
            from matrx_orm import is_database_registered

            if is_database_registered(db_config_name):
                from matrx_rag.db import bind_to_host

                bind_to_host(db_config_name)
        except ImportError:
            # matrx-orm absent (pure VectorStore-delegate hosts) — nothing to bind.
            pass
    if db_models:
        _registry["db_models"].update(db_models)
    if auth_mode is not None:
        _registry["auth_mode"] = (
            auth_mode if isinstance(auth_mode, AuthMode) else AuthMode(auth_mode)
        )
    if source_kind_aliases:
        for k, v in source_kind_aliases.items():
            _registry[f"source_kind_{k}"] = v
    if not_found_error_class is not None:
        # Rebind the module-level NotFoundError so any
        # ``from matrx_rag._ext import NotFoundError`` resolves to the
        # host's class, AND any internal ``raise NotFoundError(...)``
        # inside matrx_rag instantiates the host's class.
        import matrx_rag._ext as _self_module

        _self_module.NotFoundError = not_found_error_class
        # Also push into matrx_rag.extraction_indexing's namespace
        # since it imported NotFoundError eagerly at module load.
        import matrx_rag.extraction_indexing as _ei

        _ei.NotFoundError = not_found_error_class
    if derivative_exists_error_class is not None:
        import matrx_rag._ext as _self_module

        _self_module.DerivativeExistsError = derivative_exists_error_class
    _configured = True


def is_configured() -> bool:
    return _configured


def get_ext(key: str, *, required: bool = False, default: Any = None) -> Any:
    if key in _registry:
        return _registry[key]
    if required:
        raise RagNotConfiguredError(
            f"matrx-rag dependency '{key}' is not configured. "
            "Call matrx_rag.configure(...) at host startup."
        )
    return default


# ── Typed accessors ────────────────────────────────────────────────────


def clean_single_flight(processed_document_id: str) -> Any:
    """The async context manager every page clean of a document runs inside
    (host-injected; a no-op ``nullcontext`` when unconfigured)."""
    import contextlib

    factory = _registry.get("clean_single_flight")
    if factory is None:
        return contextlib.nullcontext()
    return factory(str(processed_document_id))


async def ensure_clean_held(processed_document_id: str | None) -> None:
    """The fence: raise (host's error) when this flow's clean hold on the document
    is no longer its own. Call before every page clean and every page/document
    write of a held clean. No-op when unconfigured or no document id."""
    if not processed_document_id:
        return
    fence = _registry.get("clean_fence")
    if fence is None:
        return
    await fence(str(processed_document_id))


async def follow_clean(processed_document_id: str, run: Any, *, resume: bool = False) -> Any:
    """Run ``run()`` (a zero-arg coroutine factory that cleans the document) and,
    when another driver already holds the document's clean, follow that holder
    through the host seam. Unconfigured = plain ``await run()``."""
    follower = _registry.get("clean_follow")
    if follower is None:
        return await run()
    return await follower(str(processed_document_id), run, resume=resume)


def get_document_writer() -> DocumentWriter:
    """Return the configured DocumentWriter (or the no-op default)."""
    return _registry["document_writer"]


def get_embedding_provider() -> EmbeddingProvider:
    """Return the configured EmbeddingProvider.

    Falls back to the lazy-instantiated DefaultOpenAIVoyageProvider on
    first access. matrx-local that wants to skip the cloud SDKs MUST
    call ``configure(embedding_provider=...)`` before any code in the
    package triggers an embed call.
    """
    provider = _registry["embedding_provider"]
    if provider is None:
        provider = _default_embedding_provider()
        _registry["embedding_provider"] = provider
    return provider


def get_llm_provider() -> LLMProvider:
    """Return the configured LLMProvider.

    Raises :class:`LLMProviderNotConfigured` when no host injected one —
    there is no built-in default. matrx-local injects a local llama-server /
    Ollama adapter via ``configure(llm_provider=...)`` so PDF cleanup,
    contextualization, HyDE, etc. run offline.
    """
    provider = _registry["llm_provider"]
    if provider is None:
        raise LLMProviderNotConfigured()
    return provider


def try_get_llm_provider() -> LLMProvider | None:
    """Return the configured LLMProvider WITHOUT instantiating the default.

    Unlike :func:`get_llm_provider`, a missing provider returns ``None`` instead
    of building (and caching) the default OpenAI provider. Use it to ask "is a
    provider injected?" without forcing construction as a side effect.

    Currently unused inside the package — its one caller was the grounding
    judge's sampling-capability probe, deleted when grounding moved onto the
    seam (the provider owns sampling policy now). Kept as the symmetric
    accessor to :func:`get_llm_provider` and because it is exported."""
    return _registry["llm_provider"]


def get_rag_agent_runner() -> RagAgentRunner | None:
    """Return the host-injected agent-backed RAG runner, or ``None``.

    When ``None`` (no host wired one — standalone / matrx-local, or the
    aidream code switch is OFF), ``matrx_rag.llm`` runs the raw
    ``LLMProvider`` path. When set, the four RAG LLM jobs route through the
    host's agx agent system for cost/usage tracking and version pinning.
    """
    return _registry.get("rag_agent_runner")


def get_reranker() -> Reranker | None:
    """Return the host-owned reranker, if that host enables one."""
    return _registry.get("reranker")


def get_vector_store() -> VectorStore:
    """Return the configured VectorStore.

    Falls back to the lazy-instantiated ``_PgVectorStoreDelegate`` on
    first access. matrx-local without a Postgres MUST call
    ``configure(vector_store=...)`` before any code path that touches
    the store.
    """
    store = _registry["vector_store"]
    if store is None:
        store = _default_vector_store()
        _registry["vector_store"] = store
    return store


def get_auth_mode() -> AuthMode:
    """Return the configured AuthMode (defaults to USER_JWT)."""
    return _registry["auth_mode"]


def get_embedding_cache() -> Any | None:
    """Return the configured embedding cache, or None when no host has
    wired matrx-batch. embed() short-circuits on the None path and goes
    straight to the provider — back-compat.
    """
    return _registry.get("embedding_cache")


def get_ner_extractor() -> NerExtractor | None:
    """Return the configured NER extractor, or None when no host has wired one.
    ner.extract_entities short-circuits to a clean no-op on the None path —
    matrx-rag never imports matrx-ai, so without injection there is no LLM
    available and NER simply does not run.
    """
    return _registry.get("ner_extractor")


def get_ner_finisher() -> Any | None:
    """Return the configured big-model NER post-processor, or None.

    When wired, the finisher receives the union of normalized spans from
    every chunk in a single ``extract_entities`` pass and returns a
    curated list — deduped, canonicalised, with cross-chunk references
    merged. The contract:

        async def finisher(
            spans: list[dict[str, Any]],
            chunks: list[dict[str, Any]],
            *,
            organization_id: str | None,
            user_id: str,
            source_kind: str | None,
            source_id: str | None,
        ) -> list[dict[str, Any]]

    Each input span: ``{"chunk_id", "kind", "name", "span_start",
    "span_end", "confidence", "attrs"}``. Each chunk: ``{"chunk_id",
    "content_text"}``. The finisher returns the SAME shape, after
    canonicalisation — it may merge, drop, or rename, but the schema
    is identical.

    When ``None``, the raw tier-A output goes straight to tier B
    (current GLiNER-only behavior). A finisher that raises is logged
    and matrx-rag falls back to the raw spans rather than failing the
    whole NER pass.
    """
    return _registry.get("ner_finisher")


def get_default_vision_model() -> str:
    """The host's vision model for image/figure captioning.

    This is a HOST CATALOG identifier — an id or name that the injected
    ``llm_provider`` knows how to resolve. matrx-rag used to hardcode one of
    OUR ``ai.model_definition`` row UUIDs as the package default, which is
    meaningless in any other database. There is no portable default, so the
    host names it: ``matrx_rag.configure(default_vision_model=...)``.
    """
    model = _registry.get("default_vision_model")
    if not model:
        raise RagNotConfiguredError(
            "matrx-rag default_vision_model is not configured — image/figure "
            "captioning needs a vision model your llm_provider can resolve. "
            "Call matrx_rag.configure(default_vision_model='<model id or "
            "name>') at host startup, or pass vision_model=... explicitly."
        )
    return str(model)


def get_page_image_renderer() -> Any | None:
    """Return the host's page-image renderer, or None when none is wired.

    Contract::

        async def render_page_image(
            *, processed_document_id: str, page_index: int, dpi: int, user_id: str
        ) -> Any    # truthy when a page image row now exists, falsy otherwise

    Rasterizing a stored document page is a HOST capability (it needs the
    host's document storage + file pipeline), so matrx-rag does not implement
    it and MUST NOT import one. When unconfigured, figure-caption derivation
    skips auto-render and captions only pages that already carry an image —
    the feature degrades, it never fails.
    """
    return _registry.get("page_image_renderer")


def get_cloud_file_manager() -> Any:
    """Return the host's cloud-enabled FileManager via the injected provider.

    The provider is a zero-arg callable wired at host startup via
    ``configure(cloud_file_manager_provider=...)`` (aidream injects
    ``common.cloud_files.get_cloud_file_manager`` from
    ``aidream/package_integration.py``). matrx-rag must not import aidream,
    and there is deliberately NO fallback: an unconfigured host that reaches
    a cld_file byte-resolution path is a wiring bug and raises loudly.
    """
    provider = _registry.get("cloud_file_manager_provider")
    if provider is None:
        raise RagNotConfiguredError(
            "matrx-rag cloud_file_manager_provider is not configured — a "
            "cld_file byte-resolution path (PDF/table/image derivation) needs "
            "the host's FileManager. Call matrx_rag.configure("
            "cloud_file_manager_provider=<zero-arg callable returning a "
            "FileManager>) at host startup (aidream wires "
            "common.cloud_files.get_cloud_file_manager in "
            "aidream/package_integration.py)."
        )
    return provider()


def get_db_config_name() -> str:
    """Return the host-injected matrx-orm pool identifier.

    Resolution order:
      1. The name passed to ``configure(db_config_name=...)``.
      2. The ``MATRX_DB_CONFIG_NAME`` env var — escape hatch for standalone
         scripts / tests that don't have a host integration layer.
      3. RagNotConfiguredError — with the call site that pinned the
         hardcoded ``"supabase_automation_matrix"`` removed, there is no
         silent fallback. The error message points at ``configure()``.

    A host is REQUIRED to wire this if anything in matrx-rag goes through
    ``get_pool`` (i.e., any pgvector-backed code path). matrx-local that
    uses a sqlite VectorStore never calls get_pool and so never trips
    this accessor.
    """
    import os

    from matrx_orm import HOST_DB_CONFIG_NAME_ENV

    name = _registry.get("db_config_name")
    if name:
        return name
    # ONE canonical name platform-wide (was MATRX_RAG_DB_NAME until 2026-08-09;
    # scraper and runtime each had their own too — three names for one concept).
    # A matrx-orm CONFIG NAME, not a connection: it aliases onto the pool the
    # host already opened and can never point at a different database.
    env_name = os.environ.get(HOST_DB_CONFIG_NAME_ENV)
    if env_name:
        return env_name
    raise RagNotConfiguredError(
        "matrx-rag db_config_name is not configured. Hosted: call "
        "matrx_rag.configure(db_config_name='<matrx-orm pool name>') at host "
        "startup (aidream injects 'supabase_automation_matrix' from "
        "aidream/package_integration.py). Standalone: call "
        "matrx_rag.db.bootstrap_db() with the ONE database's SUPABASE_MATRIX_* "
        f"env vars set, or set {HOST_DB_CONFIG_NAME_ENV} to an already-registered "
        "config name."
    )


def get_db_model(name: str, schema: str | None = None) -> Any:
    """Return the matrx-orm Model class matrx-rag should use for *name*.

    Resolution order:
      1. A host-injected override from ``configure(db_models={...})`` — the
         rare "my DB genuinely differs" escape hatch.
      2. ``matrx_orm.model_registry`` — the canonical path. The package's own
         rag.* classes land there via ``bind_to_host``/``bootstrap_db``
         (``matrx_rag.db.models_rag``); docproc.* names (ProcessedDocuments,
         ProcessedDocumentPages) resolve to the HOST's classes when hosted and
         to the package's (``matrx_rag.db.models_docproc``) when standalone.

    ``schema`` is optional: matrx-rag's own names are unique so the bare-name
    lookup resolves, but the registry is now keyed on ``(schema, name)`` — pass
    ``schema`` to disambiguate a name that a host happens to share across
    schemas.

    Raises ``RagNotConfiguredError`` when nothing resolves — never returns
    ``None`` so call sites don't need to ``if model is None`` everywhere.
    """
    cls = try_get_db_model(name, schema=schema)
    if cls is None:
        raise RagNotConfiguredError(
            f"matrx-rag DB model '{name}' not found. Hosted: call "
            f"matrx_rag.configure(db_config_name=...) at startup so the "
            f"package's models register. Standalone: call "
            f"matrx_rag.db.bootstrap_db(). A divergent host may inject "
            f"configure(db_models={{'{name}': <Model class>}}) as an override."
        )
    return cls


def try_get_db_model(name: str, schema: str | None = None) -> Any | None:
    """Return the Model class for *name*, or ``None`` when unresolvable.

    The non-raising sibling of :func:`get_db_model` (same resolution order:
    injected override → ``matrx_orm.model_registry``). ``None`` means no
    binding has happened yet (configure/bootstrap not called) or the name is
    simply unknown — callers treat it as "ORM unavailable" and may fall back
    to raw asyncpg.

    ``schema`` scopes the registry lookup to an exact ``(schema, name)``. With
    it omitted the registry resolves a name that lives in a single schema and
    RAISES on a cross-schema collision; we honor this function's non-raising
    contract by turning that ambiguity into a loud warning + ``None`` (matrx-rag
    names are unique, so this only fires on a genuine host clash).
    """
    override = (_registry.get("db_models") or {}).get(name)
    if override is not None:
        return override
    try:
        from matrx_orm import model_registry
    except ImportError:
        return None
    try:
        return model_registry.get_model(name, schema=schema)
    except ValueError:
        from matrx_utils import vcprint

        vcprint(
            f"[matrx-rag] db model '{name}' is ambiguous across schemas — pass "
            f"schema= to disambiguate. Treating as unresolved.",
            color="red",
        )
        return None


def get_db_models() -> dict[str, Any]:
    """Return the full host-injected db_models map (read-only view).

    Useful when matrx-rag wants to introspect which rag.* models the host
    has wired (e.g., to conditionally turn on ORM paths).
    """
    return dict(_registry.get("db_models") or {})


# ── Test / reset helpers ───────────────────────────────────────────────


# Capture the original exception classes at module-load time so
# _reset_for_tests can restore them if a test rebound them.
_DEFAULT_NOT_FOUND_ERROR = NotFoundError
_DEFAULT_DERIVATIVE_EXISTS_ERROR = DerivativeExistsError


def _reset_for_tests() -> None:
    """Reset the registry to its default state.

    Intended for tests that need a clean slate between cases. Do NOT
    call from production code.
    """
    global _configured, NotFoundError, DerivativeExistsError
    _registry.clear()
    _registry.update(
        {
            "document_writer": NoOpDocumentWriter(),
            "auth_mode": AuthMode.USER_JWT,
            "source_kind_cld_file": "cld_file",
            "source_kind_note": "note",
            "source_kind_code_file": "code_file",
            "source_kind_inline": "inline",
            "source_kind_external_url": "external_url",
            "source_kind_legacy": "legacy",
            "embedding_provider": None,
            "llm_provider": None,
            "rag_agent_runner": None,
            "reranker": None,
            "vector_store": None,
            "embedding_cache": None,
            "ner_extractor": None,
            "ner_finisher": None,
            "page_image_renderer": None,
            "default_vision_model": None,
            "cloud_file_manager_provider": None,
            "univer_text_renderer": None,
            "univer_current_reader": None,
            "db_config_name": None,
            "db_models": {},
            "clean_single_flight": None,
            "clean_follow": None,
            "clean_fence": None,
        }
    )
    _configured = False
    NoOpDocumentWriter._warned = False
    # Reset the lazy default singletons so future get calls rebuild them.
    global _default_embedding_provider_singleton
    global _default_vector_store_singleton
    _default_embedding_provider_singleton = None
    _default_vector_store_singleton = None
    # Restore module-level exception class bindings to defaults.
    NotFoundError = _DEFAULT_NOT_FOUND_ERROR
    DerivativeExistsError = _DEFAULT_DERIVATIVE_EXISTS_ERROR
    # Restore eagerly-imported names in the modules that did
    # ``from matrx_rag._ext import NotFoundError`` at module load.
    try:
        import matrx_rag.extraction_indexing as _ei

        _ei.NotFoundError = _DEFAULT_NOT_FOUND_ERROR
    except ImportError:
        pass


__all__ = [
    "clean_single_flight",
    "ensure_clean_held",
    "follow_clean",
    "AuthMode",
    "DocumentWriter",
    "EmbeddingProvider",
    "LLMProvider",
    "RagAgentRunner",
    "RerankResult",
    "Reranker",
    "VectorStore",
    "NerExtractor",
    "NoOpDocumentWriter",
    "RagNotConfiguredError",
    "RagDocumentError",
    "NotFoundError",
    "DerivativeExistsError",
    "DerivativeIntent",
    "DerivativeResult",
    "compute_params_hash",
    "configure",
    "is_configured",
    "get_ext",
    "get_document_writer",
    "get_embedding_provider",
    "get_llm_provider",
    "try_get_llm_provider",
    "get_rag_agent_runner",
    "get_reranker",
    "get_vector_store",
    "get_auth_mode",
    "get_embedding_cache",
    "get_ner_extractor",
    "get_page_image_renderer",
    "get_default_vision_model",
    "get_cloud_file_manager",
    "get_db_config_name",
    "get_db_model",
    "get_db_models",
]
