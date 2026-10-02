r"""Provide document store factories for the ready-to-use ``persista``-
backed document stores."""

from __future__ import annotations

__all__ = [
    "DuckDBDocumentStoreFactory",
    "InMemoryDocumentStoreFactory",
    "SQLiteDocumentStoreFactory",
    "TypedDuckDBDocumentStoreFactory",
    "TypedSQLiteDocumentStoreFactory",
]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from docculus.store.custom import (
    DuckDBDocumentStore,
    InMemoryDocumentStore,
    SQLiteDocumentStore,
    TypedDuckDBDocumentStore,
    TypedSQLiteDocumentStore,
)
from docculus.store.factory.base import BaseDocumentStoreFactory
from docculus.utils.imports import check_persista

if TYPE_CHECKING:
    from pathlib import Path


class DuckDBDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    r"""Implement a document store factory that builds a new
    :class:`~docculus.store.DuckDBDocumentStore` on each call.

    Args:
        database: The path to the DuckDB database file, or
            ``":memory:"`` for an in-memory database.
        **kwargs: Additional keyword arguments passed to
            :class:`~docculus.store.DuckDBDocumentStore`.

    Example:
        ```pycon
        >>> from docculus.store.factory import DuckDBDocumentStoreFactory
        >>> factory = DuckDBDocumentStoreFactory()
        >>> store = factory.make_document_store()

        ```
    """

    def __init__(self, database: Path | str = ":memory:", **kwargs: Any) -> None:
        check_persista()
        self._database = database
        self._kwargs = kwargs

    def make_document_store(self) -> DuckDBDocumentStore:
        return DuckDBDocumentStore(self._database, **self._kwargs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"database": self._database, **self._kwargs}


class TypedDuckDBDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    r"""Implement a document store factory that builds a new
    :class:`~docculus.store.TypedDuckDBDocumentStore` on each call.

    Args:
        database: The path to the DuckDB database file, or
            ``":memory:"`` for an in-memory database.
        metadata_schema: A mapping from metadata field name to its SQL
            column type declaration (e.g. ``{"author": "TEXT"}``).
            ``None`` is equivalent to an empty mapping, i.e. no
            metadata columns beyond ``page_content``.
        **kwargs: Additional keyword arguments passed to
            :class:`~docculus.store.TypedDuckDBDocumentStore`.

    Example:
        ```pycon
        >>> from docculus.store.factory import TypedDuckDBDocumentStoreFactory
        >>> factory = TypedDuckDBDocumentStoreFactory(metadata_schema={"author": "TEXT"})
        >>> store = factory.make_document_store()

        ```
    """

    def __init__(
        self,
        database: Path | str = ":memory:",
        metadata_schema: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        check_persista()
        self._database = database
        self._metadata_schema = metadata_schema
        self._kwargs = kwargs

    def make_document_store(self) -> TypedDuckDBDocumentStore:
        return TypedDuckDBDocumentStore(
            self._database, metadata_schema=self._metadata_schema, **self._kwargs
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "database": self._database,
            "metadata_schema": self._metadata_schema,
            **self._kwargs,
        }


class InMemoryDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    r"""Implement a document store factory that builds a new
    :class:`~docculus.store.InMemoryDocumentStore` on each call.

    Example:
        ```pycon
        >>> from docculus.store.factory import InMemoryDocumentStoreFactory
        >>> factory = InMemoryDocumentStoreFactory()
        >>> store = factory.make_document_store()

        ```
    """

    def __init__(self) -> None:
        check_persista()

    def make_document_store(self) -> InMemoryDocumentStore:
        return InMemoryDocumentStore()

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {}


class SQLiteDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    r"""Implement a document store factory that builds a new
    :class:`~docculus.store.SQLiteDocumentStore` on each call.

    Args:
        database: The path to the SQLite database file, or
            ``":memory:"`` for an in-memory database.
        **kwargs: Additional keyword arguments passed to
            :class:`~docculus.store.SQLiteDocumentStore`.

    Example:
        ```pycon
        >>> from docculus.store.factory import SQLiteDocumentStoreFactory
        >>> factory = SQLiteDocumentStoreFactory()
        >>> store = factory.make_document_store()

        ```
    """

    def __init__(self, database: Path | str = ":memory:", **kwargs: Any) -> None:
        check_persista()
        self._database = database
        self._kwargs = kwargs

    def make_document_store(self) -> SQLiteDocumentStore:
        return SQLiteDocumentStore(self._database, **self._kwargs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"database": self._database, **self._kwargs}


class TypedSQLiteDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    r"""Implement a document store factory that builds a new
    :class:`~docculus.store.TypedSQLiteDocumentStore` on each call.

    Args:
        database: The path to the SQLite database file, or
            ``":memory:"`` for an in-memory database.
        metadata_schema: A mapping from metadata field name to its SQL
            column type declaration (e.g. ``{"author": "TEXT"}``).
            ``None`` is equivalent to an empty mapping, i.e. no
            metadata columns beyond ``page_content``.
        **kwargs: Additional keyword arguments passed to
            :class:`~docculus.store.TypedSQLiteDocumentStore`.

    Example:
        ```pycon
        >>> from docculus.store.factory import TypedSQLiteDocumentStoreFactory
        >>> factory = TypedSQLiteDocumentStoreFactory(metadata_schema={"author": "TEXT"})
        >>> store = factory.make_document_store()

        ```
    """

    def __init__(
        self,
        database: Path | str = ":memory:",
        metadata_schema: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        check_persista()
        self._database = database
        self._metadata_schema = metadata_schema
        self._kwargs = kwargs

    def make_document_store(self) -> TypedSQLiteDocumentStore:
        return TypedSQLiteDocumentStore(
            self._database, metadata_schema=self._metadata_schema, **self._kwargs
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "database": self._database,
            "metadata_schema": self._metadata_schema,
            **self._kwargs,
        }
