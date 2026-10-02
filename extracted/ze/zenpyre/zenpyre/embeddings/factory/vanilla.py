r"""Provide a concrete default factory for LangChain embedding
models."""

from __future__ import annotations

__all__ = ["EmbeddingsFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.embeddings.factory.base import BaseEmbeddingsFactory

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings


class EmbeddingsFactory(BaseEmbeddingsFactory, MultilineDisplayMixin):
    """A concrete embedding factory that wraps a pre-built
    :class:`~langchain_core.embeddings.Embeddings` instance.

    Use this when the embedding model is already instantiated and you
    simply want to wrap it in the :class:`~BaseEmbeddingsFactory`
    interface — for example, when injecting a fixed embedding model
    into a component that expects a factory.

    Args:
        embeddings: A fully configured
            :class:`~langchain_core.embeddings.Embeddings` instance to
            return from :meth:`make_embeddings`.

    Example:
        ```pycon
        >>> from langchain_ollama import OllamaEmbeddings
        >>> from zenpyre.embeddings.factory import EmbeddingsFactory
        >>> factory = EmbeddingsFactory(OllamaEmbeddings(model="nomic-embed-text"))
        >>> embeddings = factory.make_embeddings()

        ```
    """

    def __init__(self, embeddings: Embeddings) -> None:
        self._embeddings = embeddings

    def make_embeddings(self) -> Embeddings:
        return self._embeddings

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"embeddings": self._embeddings}
