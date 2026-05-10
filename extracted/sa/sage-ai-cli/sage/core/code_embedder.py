"""Code-specific embedders for RAG.

Default in `core/rag.py` is `nomic-embed-text` — a general-purpose text
embedder. For code retrieval, code-specific models retrieve better:

  - bge-code-v1     (BAAI)  — best open code embedder, 768-dim
  - unixcoder       (MS)    — multilingual code+nl, 768-dim
  - jina-embeddings-v2-base-code (Jina) — 768-dim, fast
  - code-search-net (Anthropic-style) — fallback general code

This module exposes `make_embedder(name)` that returns an `Embedder`
instance compatible with `RAGIndex(embedder=...)`. New backends can be
added without touching rag.py.
"""

from __future__ import annotations

from sage.core.rag import Embedder, OllamaEmbedder

__all__ = ["CodeEmbedderRegistry", "make_embedder"]


CodeEmbedderRegistry: dict[str, dict] = {
    # name → metadata
    "nomic-embed-text": {
        "backend": "ollama",
        "dim": 768,
        "kind": "general-text",
        "ollama_pull": "nomic-embed-text",
    },
    "bge-code-v1": {
        "backend": "ollama",  # also available as GGUF
        "dim": 768,
        "kind": "code",
        "ollama_pull": "bge-code-v1",
        "notes": "Best open code embedder as of 2025; may need manual GGUF",
    },
    "jina-code-v2": {
        "backend": "ollama",
        "dim": 768,
        "kind": "code",
        "ollama_pull": "jinaai/jina-embeddings-v2-base-code",
    },
    "unixcoder-base": {
        "backend": "huggingface",
        "dim": 768,
        "kind": "code-multilang",
        "huggingface_id": "microsoft/unixcoder-base",
        "notes": "Requires sentence-transformers, not Ollama",
    },
}


def make_embedder(name: str = "nomic-embed-text") -> Embedder:
    """Construct an Embedder for the given registry entry.

    Falls back to OllamaEmbedder(name) when the registry doesn't list it
    so users can pass any locally pulled Ollama embedding model.
    """
    meta = CodeEmbedderRegistry.get(name, {})
    backend = meta.get("backend", "ollama")
    if backend == "ollama":
        emb = OllamaEmbedder(model=name)
        if "dim" in meta:
            emb.dim = int(meta["dim"])
        return emb
    if backend == "huggingface":
        return _HuggingFaceEmbedder(meta["huggingface_id"], dim=int(meta.get("dim", 768)))
    # Unknown backend → best-effort Ollama
    return OllamaEmbedder(model=name)


class _HuggingFaceEmbedder(Embedder):
    """Embedder backed by sentence-transformers / a HF model."""

    def __init__(self, model_id: str, dim: int = 768):
        self.model_id = model_id
        self.dim = dim
        self._model = None

    def _ensure_loaded(self):
        if self._model is not None:
            return
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                f"sentence-transformers required for {self.model_id!r}. Install:\n"
                "    pip install sentence-transformers"
            ) from exc
        self._model = SentenceTransformer(self.model_id)

    def embed(self, texts: list[str]) -> list[list[float]]:
        self._ensure_loaded()
        # SentenceTransformer.encode returns numpy array; convert to lists
        vecs = self._model.encode(texts, convert_to_numpy=True)
        return [list(map(float, v)) for v in vecs]
