r"""Provide a concrete factory that creates a DuckDB-backed
BaseDocumentStore."""

from __future__ import annotations

__all__ = ["DuckDBDocumentStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.document_stores import DuckDBDocumentStore
from zenpyre.document_stores.factory.base import BaseDocumentStoreFactory
from zenpyre.utils.duckdb import prepare_duckdb_path
from zenpyre.utils.imports import check_duckdb

if TYPE_CHECKING:
    from pathlib import Path

    from zenpyre.document_stores.base import BaseDocumentStore


class DuckDBDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete BaseDocumentStore factory that builds a
    :class:`~zenpyre.document_stores.DuckDBDocumentStore` backed by a
    DuckDB file at a given path.

    Use this when you want a factory that lazily constructs a
    fresh :class:`~zenpyre.document_stores.DuckDBDocumentStore` at
    ``path`` each time :meth:`make_document_store` is called, rather
    than wrapping an already-instantiated store.

    Args:
        path: The path to the DuckDB file used to back the document
            store.
        **kwargs: Additional keyword arguments forwarded to
            :class:`~zenpyre.document_stores.DuckDBDocumentStore`.

    Example:
        ```pycon
        >>> from pathlib import Path
        >>> from zenpyre.document_stores.factory import DuckDBDocumentStoreFactory
        >>> factory = DuckDBDocumentStoreFactory(Path("/tmp/my_app/documents.duckdb"))
        >>> document_store = factory.make_document_store()  # doctest: +SKIP

        ```
    """

    def __init__(self, path: Path | str, **kwargs: Any) -> None:
        check_duckdb()
        self._path = prepare_duckdb_path(path)
        self._kwargs = kwargs

    def make_document_store(self) -> BaseDocumentStore:
        return DuckDBDocumentStore(self._path, **self._kwargs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"path": self._path} | self._kwargs
