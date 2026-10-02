r"""Provide a configurable factory for LangChain embedding models."""

from __future__ import annotations

__all__ = ["ConfigurableEmbeddingsFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.embeddings.factory.base import BaseEmbeddingsFactory
from zenpyre.embeddings.resolve import resolve_embeddings

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings


class ConfigurableEmbeddingsFactory(BaseEmbeddingsFactory, MultilineDisplayMixin):
    """A concrete embedding factory that accepts either a pre-built
    :class:`~langchain_core.embeddings.Embeddings` instance or a
    configuration dictionary.

    When a dict is provided it is resolved at each
    :meth:`make_embeddings` call via :func:`~resolve_embeddings`,
    which uses ``objectory`` to instantiate the configured class.
    When an instance is provided it is returned as-is.

    Args:
        embeddings: A fully configured
            :class:`~langchain_core.embeddings.Embeddings` instance, or
            a :class:`dict` containing an ``objectory`` factory
            specification (must include a ``"_target_"`` key pointing to
            the fully-qualified class name).

    Example:
        ```pycon
        >>> from langchain_core.embeddings.fake import FakeEmbeddings
        >>> from zenpyre.embeddings.factory import ConfigurableEmbeddingsFactory
        >>> factory = ConfigurableEmbeddingsFactory(FakeEmbeddings(size=128))
        >>> embeddings = factory.make_embeddings()

        ```
    """

    def __init__(self, embeddings: Embeddings | dict[str, Any]) -> None:
        self._embeddings = embeddings

    def make_embeddings(self) -> Embeddings:
        return resolve_embeddings(self._embeddings)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"embeddings": self._embeddings}
