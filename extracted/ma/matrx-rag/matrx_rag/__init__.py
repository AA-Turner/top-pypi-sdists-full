"""matrx-rag — multi-tenant RAG for the matrx ecosystem.

Hybrid retrieval (vector + lexical), chunking, embeddings, ingestion,
PDF + image + repo pipelines, agent-extraction indexing, priority-
aware ranking. Extracted from ``aidream/services/rag/`` in Phase 2a so
matrx-local and aidream can share the same code with host-specific
provider injection.

Public API:

* :func:`configure` — wire host-supplied seams (call at startup).

* :class:`AuthMode` — enum for DB-auth posture (service_role / user_jwt / none).

* :class:`DocumentWriter` — protocol for hosts that own the
  processed_documents schema (aidream). matrx-local uses the no-op
  default for local-RAG mode.

* The submodules continue to expose their original public surface
  (``matrx_rag.embeddings.embed``, ``matrx_rag.search.search``,
  ``matrx_rag.ingestion.ingest_source`` etc.). aidream's existing
  imports keep working via the shim at ``aidream/services/rag/``.

Injection seams (all five live as of Phase 2b/iv):

* ``DocumentWriter`` — processed_documents persistence (2b/i).
* ``EmbeddingProvider`` — local vs cloud embeddings (2b/ii).
* ``LLMProvider`` — cleanup + contextualization model routing (2b/iii).
* ``VectorStore`` — pgvector vs sqlite-vss vs duckdb (2b/iv).
* ``AuthMode`` — service-role vs user-JWT (2b/i).

Call-site migration of the existing inline asyncpg paths to the
``VectorStore`` seam is incremental and lands in Phase 2b/iv follow-on
commits.
"""

from __future__ import annotations

from matrx_rag._ext import (
    AuthMode,
    DocumentWriter,
    EmbeddingProvider,
    LLMProvider,
    NoOpDocumentWriter,
    RagAgentRunner,
    RerankResult,
    Reranker,
    RagNotConfiguredError,
    VectorStore,
    configure,
    get_auth_mode,
    get_db_config_name,
    get_db_model,
    get_db_models,
    get_document_writer,
    get_embedding_provider,
    get_ext,
    get_llm_provider,
    get_ner_extractor,
    get_ner_finisher,
    get_rag_agent_runner,
    get_reranker,
    get_vector_store,
    is_configured,
    try_get_db_model,
)
from matrx_rag._observability import (
    AICallTally,
    announce_chat_call,
    announce_embedding_call,
    announce_extraction_call,
    print_tally_summary,
    record_chat_call,
    set_ai_call_announcements,
    set_ai_call_verbose,
    tally_reset,
    tally_snapshot,
)
from matrx_rag.db import (
    PACKAGE_DB_NAME,
    bind_to_host,
    bootstrap_db,
    get_models,
)

__version__ = "0.1.0"


__all__ = [
    "__version__",
    "AuthMode",
    "DocumentWriter",
    "EmbeddingProvider",
    "LLMProvider",
    "RagAgentRunner",
    "RerankResult",
    "Reranker",
    "VectorStore",
    "NoOpDocumentWriter",
    "RagNotConfiguredError",
    "configure",
    "is_configured",
    "get_ext",
    "get_document_writer",
    "get_embedding_provider",
    "get_llm_provider",
    "get_ner_extractor",
    "get_ner_finisher",
    "get_rag_agent_runner",
    "get_reranker",
    "get_vector_store",
    "get_auth_mode",
    "get_db_config_name",
    "get_db_model",
    "get_db_models",
    "try_get_db_model",
    "PACKAGE_DB_NAME",
    "bind_to_host",
    "bootstrap_db",
    "get_models",
    "AICallTally",
    "announce_chat_call",
    "announce_embedding_call",
    "announce_extraction_call",
    "print_tally_summary",
    "record_chat_call",
    "set_ai_call_announcements",
    "set_ai_call_verbose",
    "tally_reset",
    "tally_snapshot",
]
