"""
Storage backend factory.
Creates the appropriate storage backend based on configuration.
"""

from .base_storage import BaseStorageBackend
from .sqlite_storage import SqliteStorageBackend


def create_storage_backend(backend_type: str, **kwargs) -> BaseStorageBackend:
    """
    Create a storage backend instance.
    
    Args:
        backend_type: "sqlite" or "postgres"
        **kwargs: Backend-specific configuration
            For SQLite: db_path (str)
            For PostgreSQL: url (str), pool_size (int), max_overflow (int)
    
    Returns:
        Storage backend instance
    
    Raises:
        ValueError: If backend_type is unknown
        ImportError: If PostgreSQL backend requested but asyncpg not installed
    """
    if backend_type == "sqlite":
        db_path = kwargs.get('db_path', './data/securex.db')
        return SqliteStorageBackend(db_path=db_path)
    
    elif backend_type == "postgres":
        try:
            from .postgres_storage import PostgresStorageBackend
        except ImportError:
            raise ImportError(
                "PostgreSQL backend requires asyncpg. "
                "Install with: pip install dc-securex[postgres]"
            )
        
        url = kwargs.get('url')
        if not url:
            raise ValueError("PostgreSQL backend requires 'url' parameter")
        
        pool_size = kwargs.get('pool_size', 10)
        max_overflow = kwargs.get('max_overflow', 20)
        
        return PostgresStorageBackend(
            url=url,
            pool_size=pool_size,
            max_overflow=max_overflow
        )
    
    else:
        raise ValueError(
            f"Unknown storage backend: {backend_type}. "
            f"Supported: 'sqlite', 'postgres'"
        )
