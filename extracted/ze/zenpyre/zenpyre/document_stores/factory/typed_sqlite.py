r"""Provide a concrete factory that creates a SQLite-backed
BaseDocumentStore with typed metadata columns."""

from __future__ import annotations

__all__ = ["TypedSQLiteDocumentStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from coola.utils.path import sanitize_path

from zenpyre.document_stores import TypedSQLiteDocumentStore
from zenpyre.document_stores.factory.base import BaseDocumentStoreFactory

if TYPE_CHECKING:
    from pathlib import Path

    from zenpyre.document_stores.base import BaseDocumentStore


class TypedSQLiteDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete BaseDocumentStore factory that builds a
    :class:`~zenpyre.document_stores.TypedSQLiteDocumentStore` backed by
    a SQLite file at a given path.

    Use this when you want a factory that lazily constructs a
    fresh :class:`~zenpyre.document_stores.TypedSQLiteDocumentStore`
    at ``path`` (via
    :meth:`~zenpyre.document_stores.TypedSQLiteDocumentStore.from_path`)
    each time :meth:`make_document_store` is called, rather than
    wrapping an already-instantiated store.

    Args:
        path: The path to the SQLite file used to back the document
            store, or ``":memory:"`` for an in-memory database.
        metadata_schema: Optional mapping of metadata field names to
            SQLite type strings. See
            :class:`~zenpyre.document_stores.TypedSQLiteDocumentStore`'s
            docstring for details.
        read_only: If ``True``, open the database in read-only mode.
            The database file must already exist.
        **kwargs: Additional keyword arguments forwarded to
            :meth:`~zenpyre.document_stores.TypedSQLiteDocumentStore.from_path`.

    Example:
        ```pycon
        >>> from pathlib import Path
        >>> from zenpyre.document_stores.factory import TypedSQLiteDocumentStoreFactory
        >>> factory = TypedSQLiteDocumentStoreFactory(Path("/tmp/my_app/documents.sqlite"))
        >>> document_store = factory.make_document_store()  # doctest: +SKIP

        ```
    """

    def __init__(
        self,
        path: Path | str,
        metadata_schema: dict[str, str] | None = None,
        read_only: bool = False,
        **kwargs: Any,
    ) -> None:
        self._path = sanitize_path(path) if str(path) != ":memory:" else path
        self._metadata_schema = metadata_schema
        self._read_only = read_only
        self._kwargs = kwargs

    def make_document_store(self) -> BaseDocumentStore:
        return TypedSQLiteDocumentStore.from_path(
            self._path,
            metadata_schema=self._metadata_schema,
            read_only=self._read_only,
            **self._kwargs,
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "path": self._path,
            "metadata_schema": self._metadata_schema,
            "read_only": self._read_only,
        } | self._kwargs
