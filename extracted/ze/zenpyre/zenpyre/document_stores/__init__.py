r"""Contain document stores."""

from __future__ import annotations

__all__ = [
    "BaseDocumentStore",
    "DuckDBDocumentStore",
    "InMemoryDocumentStore",
    "SQLiteDocumentStore",
    "TypedDuckDBDocumentStore",
    "TypedSQLiteDocumentStore",
    "resolve_document_store",
]

from zenpyre.document_stores.base import BaseDocumentStore
from zenpyre.document_stores.duckdb import DuckDBDocumentStore
from zenpyre.document_stores.in_memory import InMemoryDocumentStore
from zenpyre.document_stores.resolve import resolve_document_store
from zenpyre.document_stores.sqlite import SQLiteDocumentStore
from zenpyre.document_stores.typed_duckdb import TypedDuckDBDocumentStore
from zenpyre.document_stores.typed_sqlite import TypedSQLiteDocumentStore
