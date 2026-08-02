r"""Provide a concrete factory that creates a DuckDB-backed
BaseDocumentStore with typed metadata columns."""

from __future__ import annotations

__all__ = ["TypedDuckDBDocumentStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.document_stores import TypedDuckDBDocumentStore
from zenpyre.document_stores.factory.base import BaseDocumentStoreFactory
from zenpyre.utils.duckdb import prepare_duckdb_path
from zenpyre.utils.imports import check_duckdb

if TYPE_CHECKING:
    from pathlib import Path

    from zenpyre.document_stores.base import BaseDocumentStore


class TypedDuckDBDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete BaseDocumentStore factory that builds a
    :class:`~zenpyre.document_stores.TypedDuckDBDocumentStore` backed by
    a DuckDB file at a given path.

    Use this when you want a factory that lazily constructs a
    fresh :class:`~zenpyre.document_stores.TypedDuckDBDocumentStore`
    at ``path`` each time :meth:`make_document_store` is called,
    rather than wrapping an already-instantiated store.

    Args:
        path: The path to the DuckDB file used to back the document
            store.
        metadata_schema: Optional mapping of metadata field names to
            DuckDB type strings. See
            :class:`~zenpyre.document_stores.TypedDuckDBDocumentStore`'s
            docstring for details.
        **kwargs: Additional keyword arguments forwarded to
            :class:`~zenpyre.document_stores.TypedDuckDBDocumentStore`.

    Example:
        ```pycon
        >>> from pathlib import Path
        >>> from zenpyre.document_stores.factory import TypedDuckDBDocumentStoreFactory
        >>> factory = TypedDuckDBDocumentStoreFactory(Path("/tmp/my_app/documents.duckdb"))
        >>> document_store = factory.make_document_store()  # doctest: +SKIP

        ```
    """

    def __init__(
        self,
        path: Path | str,
        metadata_schema: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        check_duckdb()
        self._path = prepare_duckdb_path(path)
        self._metadata_schema = metadata_schema
        self._kwargs = kwargs

    def make_document_store(self) -> BaseDocumentStore:
        return TypedDuckDBDocumentStore(
            self._path, metadata_schema=self._metadata_schema, **self._kwargs
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"path": self._path, "metadata_schema": self._metadata_schema} | self._kwargs
