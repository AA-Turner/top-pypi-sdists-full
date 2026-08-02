r"""Contain factories for document stores."""

from __future__ import annotations

__all__ = [
    "BaseDocumentStoreFactory",
    "ConfigurableDocumentStoreFactory",
    "DocumentStoreFactory",
    "DuckDBDocumentStoreFactory",
    "InMemoryDocumentStoreFactory",
    "SQLiteDocumentStoreFactory",
    "TypedDuckDBDocumentStoreFactory",
    "TypedSQLiteDocumentStoreFactory",
]

from zenpyre.document_stores.factory.base import BaseDocumentStoreFactory
from zenpyre.document_stores.factory.configurable import (
    ConfigurableDocumentStoreFactory,
)
from zenpyre.document_stores.factory.duckdb import DuckDBDocumentStoreFactory
from zenpyre.document_stores.factory.in_memory import InMemoryDocumentStoreFactory
from zenpyre.document_stores.factory.sqlite import SQLiteDocumentStoreFactory
from zenpyre.document_stores.factory.typed_duckdb import TypedDuckDBDocumentStoreFactory
from zenpyre.document_stores.factory.typed_sqlite import TypedSQLiteDocumentStoreFactory
from zenpyre.document_stores.factory.vanilla import DocumentStoreFactory
