r"""Provide a concrete default factory for LangChain embedding
models."""

from __future__ import annotations

__all__ = ["HuggingFaceEmbeddingsFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import InlineDisplayMixin

from zenpyre.embeddings.factory.base import BaseEmbeddingsFactory
from zenpyre.utils.imports import (
    check_langchain_huggingface,
    is_langchain_huggingface_available,
)

if TYPE_CHECKING or is_langchain_huggingface_available():
    from langchain_huggingface import HuggingFaceEmbeddings
else:  # pragma: no cover
    from zenpyre.utils.fallback.langchain_huggingface import HuggingFaceEmbeddings


class HuggingFaceEmbeddingsFactory(BaseEmbeddingsFactory, InlineDisplayMixin):
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
        >>> from zenpyre.embeddings.factory import HuggingFaceEmbeddingsFactory
        >>> factory = HuggingFaceEmbeddingsFactory(model_name="all-MiniLM-L6-v2")
        >>> embeddings = factory.make_embeddings()  # doctest: +SKIP

        ```
    """

    def __init__(self, **kwargs: Any) -> None:
        check_langchain_huggingface()
        self._kwargs = kwargs

    def make_embeddings(self) -> HuggingFaceEmbeddings:
        return HuggingFaceEmbeddings(**self._kwargs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return self._kwargs
