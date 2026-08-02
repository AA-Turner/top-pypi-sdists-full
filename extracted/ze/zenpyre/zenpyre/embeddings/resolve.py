r"""Provide a resolution utility for creating LangChain embedding
models."""

from __future__ import annotations

__all__ = ["resolve_embeddings"]

from typing import TYPE_CHECKING, Any

from langchain_core.embeddings import Embeddings

from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig


def resolve_embeddings(embeddings: Embeddings | dict[str, Any] | BaseConfig) -> Embeddings:
    """Resolve a LangChain
    :class:`~langchain_core.embeddings.Embeddings` instance from an
    existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``embeddings`` is already an
    :class:`~langchain_core.embeddings.Embeddings` instance it is
    returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        embeddings: Either a fully configured
            :class:`~langchain_core.embeddings.Embeddings` instance, a
            :class:`dict` containing an ``objectory`` factory
            specification (must include a ``"_target_"`` key pointing to
            the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured :class:`~langchain_core.embeddings.Embeddings`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~langchain_core.embeddings.Embeddings` instance.

    Example:
        ```pycon
        >>> from zenpyre.embeddings import resolve_embeddings
        >>> # From an existing instance:
        >>> from langchain_core.embeddings.fake import FakeEmbeddings
        >>> embeddings = resolve_embeddings(FakeEmbeddings(size=128))
        >>> # From a configuration dictionary:
        >>> embeddings = resolve_embeddings(
        ...     {"_target_": "langchain_ollama.OllamaEmbeddings", "model": "nomic-embed-text"}
        ... )

        ```
    """
    return resolve_object(embeddings, cls=Embeddings)
