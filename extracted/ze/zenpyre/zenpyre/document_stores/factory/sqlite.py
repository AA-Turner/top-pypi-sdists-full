r"""Provide a concrete factory that creates a SQLite-backed
BaseDocumentStore."""

from __future__ import annotations

__all__ = ["SQLiteDocumentStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from coola.utils.path import sanitize_path

from zenpyre.document_stores import SQLiteDocumentStore
from zenpyre.document_stores.factory.base import BaseDocumentStoreFactory

if TYPE_CHECKING:
    from pathlib import Path

    from zenpyre.document_stores.base import BaseDocumentStore


class SQLiteDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete BaseDocumentStore factory that builds a
    :class:`~zenpyre.document_stores.SQLiteDocumentStore` backed by a
    SQLite file at a given path.

    Use this when you want a factory that lazily constructs a
    fresh :class:`~zenpyre.document_stores.SQLiteDocumentStore` at
    ``path`` (via
    :meth:`~zenpyre.document_stores.SQLiteDocumentStore.from_path`)
    each time :meth:`make_document_store` is called, rather than
    wrapping an already-instantiated store.

    Args:
        path: The path to the SQLite file used to back the document
            store, or ``":memory:"`` for an in-memory database.
        read_only: If ``True``, open the database in read-only mode.
            The database file must already exist.
        **kwargs: Additional keyword arguments forwarded to
            :meth:`~zenpyre.document_stores.SQLiteDocumentStore.from_path`.

    Example:
        ```pycon
        >>> from pathlib import Path
        >>> from zenpyre.document_stores.factory import SQLiteDocumentStoreFactory
        >>> factory = SQLiteDocumentStoreFactory(Path("/tmp/my_app/documents.sqlite"))
        >>> document_store = factory.make_document_store()  # doctest: +SKIP

        ```
    """

    def __init__(self, path: Path | str, read_only: bool = False, **kwargs: Any) -> None:
        self._path = sanitize_path(path) if str(path) != ":memory:" else path
        self._read_only = read_only
        self._kwargs = kwargs

    def make_document_store(self) -> BaseDocumentStore:
        return SQLiteDocumentStore.from_path(self._path, read_only=self._read_only, **self._kwargs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"path": self._path, "read_only": self._read_only} | self._kwargs
