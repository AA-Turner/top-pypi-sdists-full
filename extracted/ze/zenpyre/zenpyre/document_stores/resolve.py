r"""Provide a resolution utility for creating zenpyre BaseDocumentStore
models."""

from __future__ import annotations

__all__ = ["resolve_document_store"]

from typing import TYPE_CHECKING, Any

from zenpyre.document_stores.base import BaseDocumentStore
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from zenpyre.utils.config import BaseConfig


def resolve_document_store(
    document_store: BaseDocumentStore | dict[str, Any] | BaseConfig,
) -> BaseDocumentStore:
    """Resolve a
    :class:`~zenpyre.document_stores.base.BaseDocumentStore` instance
    from an existing object, a configuration dictionary, or a
    :class:`~zenpyre.utils.config.BaseConfig`.

    If ``document_store`` is already a
    :class:`~zenpyre.document_stores.base.BaseDocumentStore` instance
    it is returned as-is.  If it is a :class:`dict` or a
    :class:`~zenpyre.utils.config.BaseConfig`, it is treated as an
    ``objectory`` factory configuration and instantiated via
    :func:`objectory.factory`. See
    :func:`~zenpyre.utils.resolve.resolve_object` for details.

    Args:
        document_store: Either a fully configured
            :class:`~zenpyre.document_stores.base.BaseDocumentStore`
            instance, a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name), or a
            :class:`~zenpyre.utils.config.BaseConfig` whose
            ``to_kwargs()`` includes a ``"_target_"`` key.

    Returns:
        A configured
        :class:`~zenpyre.document_stores.base.BaseDocumentStore`
        instance.

    Raises:
        TypeError: If the resolved object is not a
            :class:`~zenpyre.document_stores.base.BaseDocumentStore`
            instance.

    Example:
        ```pycon
        >>> from zenpyre.document_stores import InMemoryDocumentStore, resolve_document_store
        >>> # From an existing instance:
        >>> document_store = resolve_document_store(InMemoryDocumentStore())
        >>> # From a configuration dictionary:
        >>> document_store = resolve_document_store(
        ...     {"_target_": "zenpyre.document_stores.InMemoryDocumentStore"}
        ... )

        ```
    """
    return resolve_object(document_store, cls=BaseDocumentStore)
