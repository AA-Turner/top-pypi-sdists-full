"""
Storage backends for SecureX SDK.
Supports SQLite and PostgreSQL database storage.
"""

from .base_storage import BaseStorageBackend
from .sqlite_storage import SqliteStorageBackend
from .storage_factory import create_storage_backend

__all__ = [
    'BaseStorageBackend',
    'SqliteStorageBackend',
    'create_storage_backend'
]

# PostgreSQL backend is optional
try:
    from .postgres_storage import PostgresStorageBackend
    __all__.append('PostgresStorageBackend')
except ImportError:
    # asyncpg not installed, PostgreSQL support disabled
    pass
