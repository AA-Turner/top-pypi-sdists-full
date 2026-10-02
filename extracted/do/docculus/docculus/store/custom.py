r"""Implement ready-to-use document stores backed by ``persista`` SQLite
stores."""

from __future__ import annotations

__all__ = [
    "DuckDBDocumentStore",
    "InMemoryDocumentStore",
    "SQLiteDocumentStore",
    "TypedDuckDBDocumentStore",
    "TypedSQLiteDocumentStore",
]

from typing import TYPE_CHECKING, Any

from docculus.store.document import _CONTENT_KEY, _METADATA_KEY, DocumentStore
from docculus.utils.imports import check_persista, is_persista_available

if TYPE_CHECKING:
    from pathlib import Path

if is_persista_available():  # pragma: no cover
    from persista.store import InMemoryStore, TypedDuckDBStore, TypedSQLiteStore


class DuckDBDocumentStore(DocumentStore):
    r"""Implement a :class:`~docculus.store.document.DocumentStore`
    backed by a DuckDB database, with document metadata stored as a
    single JSON column.

    This is a convenience wrapper around
    :class:`persista.store.TypedDuckDBStore` that configures it with
    a fixed schema suitable for storing
    :class:`~langchain_core.documents.Document` instances: a
    ``page_content`` text column and a ``metadata`` JSON column. It is
    equivalent to constructing a
    :class:`~docculus.store.document.DocumentStore` with
    ``metadata_mode="single"`` around such a store.

    Use this store when document metadata schemas vary from one
    document to another, or when the metadata fields do not need to
    be queried directly with SQL. Use
    :class:`TypedDuckDBDocumentStore` instead when metadata fields
    should be stored as their own SQL columns.

    Args:
        database: The path to the DuckDB database file, or
            ``":memory:"`` for an in-memory database.
        **kwargs: Additional keyword arguments passed to
            :class:`persista.store.TypedDuckDBStore`.

    Example:
        ```pycon
        >>> from docculus.store import DuckDBDocumentStore
        >>> from langchain_core.documents import Document
        >>> with DuckDBDocumentStore() as store:  # doctest: +SKIP
        ...     store.set_many(
        ...         [Document(id="1", page_content="hello", metadata={"author": "Alice"})]
        ...     )
        ...     store.get("1")
        ...
        Document(id='1', page_content='hello', metadata={'author': 'Alice'})

        ```
    """

    def __init__(self, database: Path | str = ":memory:", **kwargs: Any) -> None:
        check_persista()
        store = TypedDuckDBStore(
            database,
            value_schema={_CONTENT_KEY: "TEXT NOT NULL", _METADATA_KEY: "JSON"},
            **kwargs,
        )
        super().__init__(store, metadata_mode="single")


class TypedDuckDBDocumentStore(DocumentStore):
    r"""Implement a :class:`~docculus.store.document.DocumentStore`
    backed by a DuckDB database, with each document metadata field
    stored as its own typed SQL column.

    This is a convenience wrapper around
    :class:`persista.store.TypedDuckDBStore` that configures it with a
    ``page_content`` text column plus one column per metadata field
    declared in ``metadata_schema``. It is equivalent to constructing
    a :class:`~docculus.store.document.DocumentStore` with
    ``metadata_mode="flat"`` around such a store.

    Use this store when document metadata follows a known, fixed
    schema and individual metadata fields should be queryable as SQL
    columns. Use :class:`DuckDBDocumentStore` instead when documents
    may have arbitrary or varying metadata.

    Args:
        database: The path to the DuckDB database file, or
            ``":memory:"`` for an in-memory database.
        metadata_schema: A mapping from metadata field name to its SQL
            column type declaration (e.g. ``{"author": "TEXT"}``).
            ``None`` is equivalent to an empty mapping, i.e. no
            metadata columns beyond ``page_content``.
        **kwargs: Additional keyword arguments passed to
            :class:`persista.store.TypedDuckDBStore`.

    Example:
        ```pycon
        >>> from docculus.store import TypedDuckDBDocumentStore
        >>> from langchain_core.documents import Document
        >>> with TypedDuckDBDocumentStore(
        ...     metadata_schema={"author": "TEXT"}
        ... ) as store:  # doctest: +SKIP
        ...     store.set_many(
        ...         [Document(id="1", page_content="hello", metadata={"author": "Alice"})]
        ...     )
        ...     store.get("1")
        ...
        Document(id='1', page_content='hello', metadata={'author': 'Alice'})

        ```
    """

    def __init__(
        self,
        database: Path | str = ":memory:",
        metadata_schema: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        check_persista()
        store = TypedDuckDBStore(
            database,
            value_schema={_CONTENT_KEY: "TEXT NOT NULL"} | (metadata_schema or {}),
            **kwargs,
        )
        super().__init__(store, metadata_mode="flat")


class InMemoryDocumentStore(DocumentStore):
    r"""Implement a :class:`~docculus.store.document.DocumentStore`
    backed by a plain in-memory dictionary store.

    This is a convenience wrapper around
    :class:`persista.store.InMemoryStore`, useful for tests, examples,
    and other scenarios where documents do not need to be persisted
    across processes. Since the underlying store is a Python dict
    rather than a SQL database, its ``metadata_mode`` is fixed to the
    :class:`~docculus.store.document.DocumentStore` default
    (``"flat"``).

    Example:
        ```pycon
        >>> from docculus.store import InMemoryDocumentStore
        >>> from langchain_core.documents import Document
        >>> with InMemoryDocumentStore() as store:  # doctest: +SKIP
        ...     store.set_many(
        ...         [Document(id="1", page_content="hello", metadata={"author": "Alice"})]
        ...     )
        ...     store.get("1")
        ...
        Document(id='1', page_content='hello', metadata={'author': 'Alice'})

        ```
    """

    def __init__(self) -> None:
        check_persista()
        store = InMemoryStore()
        super().__init__(store)


class SQLiteDocumentStore(DocumentStore):
    r"""Implement a :class:`~docculus.store.document.DocumentStore`
    backed by a SQLite database, with document metadata stored as a
    single JSON column.

    This is a convenience wrapper around
    :class:`persista.store.TypedSQLiteStore` that configures it with
    a fixed schema suitable for storing
    :class:`~langchain_core.documents.Document` instances: a
    ``page_content`` text column and a ``metadata`` JSON column. It is
    equivalent to constructing a
    :class:`~docculus.store.document.DocumentStore` with
    ``metadata_mode="single"`` around such a store.

    Use this store when document metadata schemas vary from one
    document to another, or when the metadata fields do not need to
    be queried directly with SQL. Use
    :class:`TypedSQLiteDocumentStore` instead when metadata fields
    should be stored as their own SQL columns.

    Args:
        database: The path to the SQLite database file, or
            ``":memory:"`` for an in-memory database.
        **kwargs: Additional keyword arguments passed to
            :class:`persista.store.TypedSQLiteStore`.

    Example:
        ```pycon
        >>> from docculus.store import SQLiteDocumentStore
        >>> from langchain_core.documents import Document
        >>> with SQLiteDocumentStore() as store:  # doctest: +SKIP
        ...     store.set_many(
        ...         [Document(id="1", page_content="hello", metadata={"author": "Alice"})]
        ...     )
        ...     store.get("1")
        ...
        Document(id='1', page_content='hello', metadata={'author': 'Alice'})

        ```
    """

    def __init__(self, database: Path | str = ":memory:", **kwargs: Any) -> None:
        check_persista()
        store = TypedSQLiteStore(
            database,
            value_schema={_CONTENT_KEY: "TEXT NOT NULL", _METADATA_KEY: "JSON"},
            **kwargs,
        )
        super().__init__(store, metadata_mode="single")


class TypedSQLiteDocumentStore(DocumentStore):
    r"""Implement a :class:`~docculus.store.document.DocumentStore`
    backed by a SQLite database, with each document metadata field
    stored as its own typed SQL column.

    This is a convenience wrapper around
    :class:`persista.store.TypedSQLiteStore` that configures it with a
    ``page_content`` text column plus one column per metadata field
    declared in ``metadata_schema``. It is equivalent to constructing
    a :class:`~docculus.store.document.DocumentStore` with
    ``metadata_mode="flat"`` around such a store.

    Use this store when document metadata follows a known, fixed
    schema and individual metadata fields should be queryable as SQL
    columns. Use :class:`SQLiteDocumentStore` instead when documents
    may have arbitrary or varying metadata.

    Args:
        database: The path to the SQLite database file, or
            ``":memory:"`` for an in-memory database.
        metadata_schema: A mapping from metadata field name to its SQL
            column type declaration (e.g. ``{"author": "TEXT"}``).
            ``None`` is equivalent to an empty mapping, i.e. no
            metadata columns beyond ``page_content``.
        **kwargs: Additional keyword arguments passed to
            :class:`persista.store.TypedSQLiteStore`.

    Example:
        ```pycon
        >>> from docculus.store import TypedSQLiteDocumentStore
        >>> from langchain_core.documents import Document
        >>> with TypedSQLiteDocumentStore(
        ...     metadata_schema={"author": "TEXT"}
        ... ) as store:  # doctest: +SKIP
        ...     store.set_many(
        ...         [Document(id="1", page_content="hello", metadata={"author": "Alice"})]
        ...     )
        ...     store.get("1")
        ...
        Document(id='1', page_content='hello', metadata={'author': 'Alice'})

        ```
    """

    def __init__(
        self,
        database: Path | str = ":memory:",
        metadata_schema: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        check_persista()
        store = TypedSQLiteStore(
            database,
            value_schema={_CONTENT_KEY: "TEXT NOT NULL"} | (metadata_schema or {}),
            **kwargs,
        )
        super().__init__(store, metadata_mode="flat")
