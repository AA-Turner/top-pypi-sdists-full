"""The RAG package delegates cross-encoder work to a host seam."""

from __future__ import annotations

from pathlib import Path


def test_reranker_is_optional_and_rag_never_imports_cohere():
    """A standalone RAG install can search without loading a provider SDK."""
    import matrx_rag
    import matrx_rag.search as search

    matrx_rag._ext._reset_for_tests()
    assert matrx_rag.get_reranker() is None

    source = Path(search.__file__).read_text()
    assert "import cohere" not in source
    assert "os.environ" not in source
    assert "reranker.rerank(query, documents, model=" not in source


def test_configure_installs_reranker_and_reset_removes_it():
    import matrx_rag

    matrx_rag._ext._reset_for_tests()

    class StubReranker:
        async def rerank(self, query, documents):
            return matrx_rag.RerankResult(
                scores=[0.0] * len(documents), model="host-selected-model"
            )

    reranker = StubReranker()
    matrx_rag.configure(reranker=reranker)
    assert matrx_rag.get_reranker() is reranker
    matrx_rag._ext._reset_for_tests()
    assert matrx_rag.get_reranker() is None
