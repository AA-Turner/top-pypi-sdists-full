r"""Provide a document loader backed by a document store."""

from __future__ import annotations

__all__ = ["DocumentStoreLoader"]


from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from langchain_core.document_loaders import BaseLoader

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import TracebackType
    from typing import Self

    from docculus.store.base import BaseDocumentStore
    from langchain_core.documents import Document


class DocumentStoreLoader(BaseLoader, MultilineDisplayMixin):
    """A loader that yields documents from a :class:`BaseDocumentStore`.

    Use this when documents already live in a document store and you
    need to wrap them in a
    :class:`~langchain_core.document_loaders.BaseLoader` interface —
    for example, to feed a store's contents into a pipeline (e.g. a
    vector store indexer) that expects a loader.

    ``store`` must already be open (see :class:`BaseDocumentStore`)
    when :meth:`lazy_load`/:meth:`load` is called; this class does not
    open it itself. Use ``DocumentStoreLoader`` as a context manager
    (rather than opening/closing ``store`` directly) to be sure it's
    closed once you're done with it: ``__enter__``/``__exit__``
    delegate to ``store.open()``/``store.close()``, so
    ``with DocumentStoreLoader(store) as loader: ...`` guarantees
    ``store`` is closed on exit, even if loading raises.

    Args:
        store: The :class:`~docculus.store.base.BaseDocumentStore`
            to load documents from.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.document_loaders import DocumentStoreLoader
        >>> from docculus.store import InMemoryDocumentStore
        >>> store = InMemoryDocumentStore()
        >>> with DocumentStoreLoader(store) as loader:
        ...     store.set_many(
        ...         [Document(id="1", page_content="Hello"), Document(id="2", page_content="World")]
        ...     )
        ...     docs = loader.load()
        ...

        ```
    """

    def __init__(self, store: BaseDocumentStore) -> None:
        self._store = store

    def __enter__(self) -> Self:
        self._store.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._store.close()

    def lazy_load(self) -> Iterator[Document]:
        yield from self._store.values()

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"store": self._store}
