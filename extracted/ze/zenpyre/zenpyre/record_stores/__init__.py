r"""Contain record stores."""

from __future__ import annotations

__all__ = [
    "BaseRecordStore",
    "DuckDBRecordStore",
    "InMemoryRecordStore",
    "SQLiteRecordStore",
    "TypedDuckDBRecordStore",
    "TypedSQLiteRecordStore",
    "resolve_record_store",
]

from zenpyre.record_stores.base import BaseRecordStore
from zenpyre.record_stores.duckdb import DuckDBRecordStore
from zenpyre.record_stores.in_memory import InMemoryRecordStore
from zenpyre.record_stores.resolve import resolve_record_store
from zenpyre.record_stores.sqlite import SQLiteRecordStore
from zenpyre.record_stores.typed_duckdb import TypedDuckDBRecordStore
from zenpyre.record_stores.typed_sqlite import TypedSQLiteRecordStore
