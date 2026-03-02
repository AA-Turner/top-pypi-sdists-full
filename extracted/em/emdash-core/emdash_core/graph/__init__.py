"""Graph module for Kuzu database operations.

Note: Kuzu is an optional dependency. Check KUZU_AVAILABLE before using
graph features, or install with: pip install 'emdash-ai[graph]'
"""

from .connection import (
    KuzuConnection,
    get_connection,
    set_connection,
    close_connection,
    KUZU_AVAILABLE,
)
from .schema import SchemaManager, initialize_database
from .builder import GraphBuilder
from .writer import GraphWriter

__all__ = [
    # Availability check
    "KUZU_AVAILABLE",
    # Connection
    "KuzuConnection",
    "get_connection",
    "set_connection",
    "close_connection",
    # Schema
    "SchemaManager",
    "initialize_database",
    # Builder
    "GraphBuilder",
    # Writer
    "GraphWriter",
]
