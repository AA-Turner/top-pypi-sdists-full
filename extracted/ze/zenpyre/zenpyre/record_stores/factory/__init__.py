r"""Contain factories for record stores."""

from __future__ import annotations

__all__ = [
    "BaseRecordStoreFactory",
    "ConfigurableRecordStoreFactory",
    "DuckDBRecordStoreFactory",
    "InMemoryRecordStoreFactory",
    "RecordStoreFactory",
    "SQLiteRecordStoreFactory",
    "TypedDuckDBRecordStoreFactory",
    "TypedSQLiteRecordStoreFactory",
]

from zenpyre.record_stores.factory.base import BaseRecordStoreFactory
from zenpyre.record_stores.factory.configurable import ConfigurableRecordStoreFactory
from zenpyre.record_stores.factory.duckdb import DuckDBRecordStoreFactory
from zenpyre.record_stores.factory.in_memory import InMemoryRecordStoreFactory
from zenpyre.record_stores.factory.sqlite import SQLiteRecordStoreFactory
from zenpyre.record_stores.factory.typed_duckdb import TypedDuckDBRecordStoreFactory
from zenpyre.record_stores.factory.typed_sqlite import TypedSQLiteRecordStoreFactory
from zenpyre.record_stores.factory.vanilla import RecordStoreFactory
