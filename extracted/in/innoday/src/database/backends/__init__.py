"""Database backend implementations for InnoDay."""

from .abstract import DatabaseBackend
from .local import LocalDatabaseBackend

__all__ = ["DatabaseBackend", "LocalDatabaseBackend"]

# Supabase backend is imported conditionally to avoid dependency issues
try:
    from .supabase import SupabaseDatabaseBackend

    __all__.append("SupabaseDatabaseBackend")
except ImportError:
    # Supabase dependencies not available
    SupabaseDatabaseBackend = None
