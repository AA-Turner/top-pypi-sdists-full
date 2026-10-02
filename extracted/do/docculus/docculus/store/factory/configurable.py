r"""Provide a configurable factory for docculus ``BaseDocumentStore``
instances."""

from __future__ import annotations

__all__ = ["ConfigurableDocumentStoreFactory"]

from typing import Any

from coola.display import MultilineDisplayMixin
from coola.factory import resolve_object

from docculus.store.base import BaseDocumentStore
from docculus.store.factory.base import BaseDocumentStoreFactory


class ConfigurableDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete document store factory that accepts either a pre-built
    :class:`~docculus.store.BaseDocumentStore` instance or a
    configuration dictionary.

    When a dict is provided it is resolved at each
    :meth:`make_document_store` call via
    :func:`~coola.factory.resolve_object`,
    which uses ``objectory`` to instantiate the configured class.
    When an instance is provided it is returned as-is.

    Args:
        document_store: A fully configured
            :class:`~docculus.store.BaseDocumentStore`
            instance, or a :class:`dict` containing an ``objectory``
            factory specification (must include a ``"_target_"`` key
            pointing to the fully-qualified class name).

    Example:
        ```pycon
        >>> from docculus.store import InMemoryDocumentStore
        >>> from docculus.store.factory import ConfigurableDocumentStoreFactory
        >>> factory = ConfigurableDocumentStoreFactory(InMemoryDocumentStore())
        >>> store = factory.make_document_store()

        ```
    """

    def __init__(self, document_store: BaseDocumentStore | dict[str, Any]) -> None:
        self._document_store = document_store

    def make_document_store(self) -> BaseDocumentStore:
        return resolve_object(self._document_store, cls=BaseDocumentStore)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"document_store": self._document_store}
