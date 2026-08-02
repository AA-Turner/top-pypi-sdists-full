r"""Provide a configurable factory for zenpyre BaseDocumentStore
models."""

from __future__ import annotations

__all__ = ["ConfigurableDocumentStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.document_stores.factory.base import BaseDocumentStoreFactory
from zenpyre.document_stores.resolve import resolve_document_store

if TYPE_CHECKING:
    from zenpyre.document_stores.base import BaseDocumentStore


class ConfigurableDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete BaseDocumentStore factory that accepts either a pre-
    built :class:`~zenpyre.document_stores.base.BaseDocumentStore`
    instance or a configuration dictionary.

    When a dict is provided it is resolved at each
    :meth:`make_document_store` call via
    :func:`~zenpyre.document_stores.resolve.resolve_document_store`,
    which uses ``objectory`` to instantiate the configured class.
    When an instance is provided it is returned as-is.

    Args:
        document_store: A fully configured
            :class:`~zenpyre.document_stores.base.BaseDocumentStore`
            instance, or a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name).

    Example:
        ```pycon
        >>> from zenpyre.document_stores import InMemoryDocumentStore
        >>> from zenpyre.document_stores.factory import ConfigurableDocumentStoreFactory
        >>> factory = ConfigurableDocumentStoreFactory(InMemoryDocumentStore())
        >>> document_store = factory.make_document_store()

        ```
    """

    def __init__(self, document_store: BaseDocumentStore | dict[str, Any]) -> None:
        self._document_store = document_store

    def make_document_store(self) -> BaseDocumentStore:
        return resolve_document_store(self._document_store)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"document_store": self._document_store}
