r"""Provide a resolution utility for creating LangChain vector store
models."""

from __future__ import annotations

__all__ = ["resolve_vector_store"]

from typing import TYPE_CHECKING, Any

from langchain_core.vectorstores import VectorStore

from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig


def resolve_vector_store(vector_store: VectorStore | dict[str, Any] | BaseConfig) -> VectorStore:
    """Resolve a LangChain
    :class:`~langchain_core.vectorstores.VectorStore` instance from an
    existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``vector_store`` is already a
    :class:`~langchain_core.vectorstores.VectorStore` instance it is
    returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        vector_store: Either a fully configured
            :class:`~langchain_core.vectorstores.VectorStore` instance,
            a :class:`dict` containing an ``objectory`` factory
            specification (must include a ``"_target_"`` key pointing to
            the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured :class:`~langchain_core.vectorstores.VectorStore`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~langchain_core.vectorstores.VectorStore` instance.

    Example:
        ```pycon
        >>> from zenpyre.vectorstores.resolve import resolve_vector_store
        >>> from langchain_core.vectorstores import InMemoryVectorStore
        >>> from langchain_core.embeddings.fake import FakeEmbeddings
        >>> # From an existing instance:
        >>> vector_store = resolve_vector_store(InMemoryVectorStore(FakeEmbeddings(size=128)))
        >>> # From a configuration dictionary:
        >>> vector_store = resolve_vector_store(  # doctest: +SKIP
        ...     {
        ...         "_target_": "langchain_core.vectorstores.InMemoryVectorStore",
        ...         "embedding": FakeEmbeddings(size=128),
        ...     }
        ... )

        ```
    """
    return resolve_object(vector_store, cls=VectorStore)
