r"""Provide a SQLite-backed store for LangChain documents with JSON
metadata."""

from __future__ import annotations

__all__ = ["BaseSQLiteDocumentStore", "SQLiteDocumentStore"]

import json
import logging
import sqlite3
from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from langchain_core.documents import Document
from typing_extensions import Self

from zenpyre.document_stores.base import BaseDocumentStore

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)


class BaseSQLiteDocumentStore(BaseDocumentStore, MultilineDisplayMixin):
    r"""Define a base class for SQLite-backed store for LangChain
    documents.

    The constructor mirrors :func:`sqlite3.connect`: the first
    positional argument is the ``database`` argument accepted by
    ``sqlite3.connect`` (a path, ``":memory:"``, or a ``file:`` URI
    when ``uri=True`` is passed), and any additional keyword
    arguments are forwarded as-is.  Use :meth:`SQLiteDocumentStore.from_path`
    for a more convenient constructor that builds the appropriate URI
    for you, including read-only access.

    Args:
        database: The ``database`` argument passed to
            ``sqlite3.connect`` (path, ``":memory:"``, or ``file:`` URI).
        **kwargs: Additional keyword arguments to pass to
            ``sqlite3.connect`` (e.g. ``uri=True``, ``timeout``,
            ``check_same_thread``).
    """

    def __init__(self, database: Path | str, **kwargs: Any) -> None:
        self._database = database
        self._kwargs = kwargs
        self._closed = False
        self._conn = sqlite3.connect(database, **kwargs)

    def _ensure_schema(self) -> None:
        """Recreate the store's table schema on a fresh connection.

        Called once from ``__init__`` and again each time the store is
        reopened via :meth:`__enter__` after being closed. A
        ``:memory:`` database starts empty every time it is
        (re)connected to, so this is what makes reopening a closed in-
        memory store behave like a reset rather than resuming where it
        left off. The default implementation does nothing; subclasses
        override it.
        """

    def close(self) -> None:
        if self._closed:
            return
        logger.info("Closing SQLite at %s", self._database)
        self._conn.close()
        self._closed = True

    def delete(self, doc_id: str) -> None:
        self._conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        self._conn.commit()

    def delete_many(self, doc_ids: list[str]) -> None:
        if not doc_ids:
            return
        placeholders = ", ".join("?" * len(doc_ids))
        self._conn.execute(
            f"DELETE FROM documents WHERE id IN ({placeholders})",  # noqa: S608
            doc_ids,
        )
        self._conn.commit()

    def count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]

    def get_columns_info(self) -> dict[str, str]:
        """Return the column names and types of the documents table.

        Returns:
            A mapping of column name to SQLite declared type.
        """
        rows = self._conn.execute("PRAGMA table_info(documents)").fetchall()
        # PRAGMA table_info columns: cid, name, type, notnull, dflt_value, pk
        return {row[1]: row[2] for row in rows}

    def show_columns_info(self) -> None:
        """Print the documents table's column names and types to stdout.

        This is a convenience wrapper around :meth:`get_columns_info`
        for interactive/debugging use. For programmatic access, use
        :meth:`get_columns_info` instead.
        """
        for name, dtype in self.get_columns_info().items():
            print(f"{name}\t{dtype}")  # noqa: T201

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"count": self.count(), "database": self._database} | self._kwargs

    def __enter__(self) -> Self:
        if self._closed:
            self._conn = sqlite3.connect(self._database, **self._kwargs)
            self._closed = False
            self._ensure_schema()
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


_CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS documents (
        id           TEXT PRIMARY KEY,
        page_content TEXT NOT NULL,
        metadata     JSON
    )
"""


class SQLiteDocumentStore(BaseSQLiteDocumentStore):
    """A SQLite-backed store for LangChain
    :class:`~langchain_core.documents.Document` objects.

    Persists documents to a SQLite database and supports adding,
    retrieving, filtering, and deleting documents.  All metadata is
    stored as a JSON column (using SQLite's built-in ``json1``
    functions), which provides flexibility for arbitrary metadata
    fields without requiring a fixed schema.

    The constructor mirrors :func:`sqlite3.connect` directly. For the
    common case of opening a file by path (optionally read-only), use
    :meth:`from_path` instead.

    Args:
        database: The ``database`` argument passed to
            ``sqlite3.connect`` (path, ``":memory:"``, or ``file:`` URI).
        **kwargs: Additional keyword arguments to pass to
            ``sqlite3.connect``.

    Example:
        ```pycon
        >>> from zenpyre.document_stores import SQLiteDocumentStore
        >>> from langchain_core.documents import Document
        >>> store = SQLiteDocumentStore(":memory:")
        >>> docs = [
        ...     Document(
        ...         id="1",
        ...         page_content="Intro to Python",
        ...         metadata={"author": "Alice", "category": "Programming"},
        ...     ),
        ...     Document(
        ...         id="2",
        ...         page_content="Advanced Python",
        ...         metadata={"author": "Alice", "category": "Programming"},
        ...     ),
        ...     Document(
        ...         id="3",
        ...         page_content="History of Rome",
        ...         metadata={"author": "Bob", "category": "History"},
        ...     ),
        ... ]
        >>> store.add_documents(docs)
        >>> len(store.filter(author="Alice"))
        2
        >>> len(store.filter(author="Alice", category="Programming"))
        2
        >>> len(store.filter(category="History"))
        1

        ```
    """

    def __init__(self, database: Path | str = ":memory:", **kwargs: Any) -> None:
        super().__init__(database, **kwargs)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        try:
            self._conn.execute(_CREATE_TABLE)
            self._conn.commit()
        except sqlite3.OperationalError:
            # Connection is read-only (e.g. opened via a `mode=ro` URI);
            # assume the table already exists.
            pass

    @classmethod
    def from_path(
        cls, path: Path | str, *, read_only: bool = False, **kwargs: Any
    ) -> SQLiteDocumentStore:
        """Construct a :class:`SQLiteDocumentStore` from a file path.

        Builds the appropriate ``file:`` URI for ``sqlite3.connect``,
        including read-only access, so callers don't need to
        construct SQLite URIs themselves.

        Args:
            path: Path to the SQLite file, or ``":memory:"`` for an
                in-memory database (useful for testing).
            read_only: If ``True``, open the database in read-only
                mode. The database file must already exist.
            **kwargs: Additional keyword arguments to pass to
                ``sqlite3.connect``.

        Returns:
            A new :class:`SQLiteDocumentStore` connected to ``path``.
        """
        if str(path) == ":memory:":
            uri = "file::memory:?cache=shared"
        elif read_only:
            uri = f"file:{path}?mode=ro"
        else:
            uri = f"file:{path}?mode=rwc"
        return cls(uri, uri=True, **kwargs)

    def add_documents(self, docs: list[Document]) -> None:
        for doc in docs:
            if doc.id is None:
                msg = "All documents must have an id. Assign one before adding"
                raise ValueError(msg)

        if docs:
            self._conn.executemany(
                "INSERT OR REPLACE INTO documents VALUES (?, ?, ?)",
                [(doc.id, doc.page_content, json.dumps(doc.metadata)) for doc in docs],
            )
            self._conn.commit()
        logger.info("Added %s documents", f"{len(docs):,}")

    def get(self, doc_id: str) -> Document | None:
        row = self._conn.execute(
            "SELECT id, page_content, metadata FROM documents WHERE id = ?",
            (doc_id,),
        ).fetchone()
        return self._row_to_doc(row) if row else None

    def get_many(self, doc_ids: list[str]) -> list[Document | None]:
        placeholders = ", ".join("?" * len(doc_ids))
        rows = self._conn.execute(
            f"SELECT id, page_content, metadata FROM documents WHERE id IN ({placeholders})",  # noqa: S608
            doc_ids,
        ).fetchall()
        by_id = {row[0]: self._row_to_doc(row) for row in rows}
        return [by_id.get(doc_id) for doc_id in doc_ids]

    def filter(self, **metadata_filters: Any) -> list[Document]:
        if not metadata_filters:
            return self.all()

        conditions = [f"json_extract(metadata, '$.{key}') = ?" for key in metadata_filters]
        where = " AND ".join(conditions)
        rows = self._conn.execute(
            f"SELECT id, page_content, metadata FROM documents WHERE {where}",  # noqa: S608
            list(metadata_filters.values()),
        ).fetchall()
        return [self._row_to_doc(row) for row in rows]

    def check_ids(self, doc_ids: list[str]) -> tuple[list[str], list[str]]:
        if not doc_ids:
            return [], []
        placeholders = ", ".join("?" * len(doc_ids))
        existing = {
            row[0]
            for row in self._conn.execute(
                f"SELECT id FROM documents WHERE id IN ({placeholders})",  # noqa: S608
                doc_ids,
            ).fetchall()
        }
        found = [i for i in doc_ids if i in existing]
        missing = [i for i in doc_ids if i not in existing]
        return found, missing

    def all(self) -> list[Document]:
        rows = self._conn.execute("SELECT id, page_content, metadata FROM documents").fetchall()
        return [self._row_to_doc(row) for row in rows]

    def iter_batches(self, batch_size: int = 32) -> Generator[list[Document], None, None]:
        if batch_size < 1:
            msg = f"batch_size must be a positive integer, got {batch_size}"
            raise ValueError(msg)

        cursor = self._conn.cursor()
        cursor.execute("SELECT id, page_content, metadata FROM documents")
        while rows := cursor.fetchmany(batch_size):
            yield [self._row_to_doc(row) for row in rows]

    # ---------------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------------

    @staticmethod
    def _row_to_doc(row: tuple) -> Document:
        """Convert a raw database row to a Document."""
        doc_id, page_content, metadata_json = row
        return Document(
            id=doc_id,
            page_content=page_content,
            metadata=json.loads(metadata_json) if metadata_json else {},
        )
