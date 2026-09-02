"""Database factory for creating appropriate database backend instances."""

import logging
import os
from typing import Any, Dict, Optional

from .backends.abstract import DatabaseBackend
from .backends.local import LocalDatabaseBackend

logger = logging.getLogger(__name__)

# Global backend instance for dependency injection
_current_backend: Optional[DatabaseBackend] = None


class DatabaseFactory:
    """Factory for creating appropriate database backend instances.

    The factory automatically selects the best available backend based on
    configuration and available dependencies.
    """

    @staticmethod
    def create_backend(
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
        local_database_url: Optional[str] = None,
        **kwargs,
    ) -> DatabaseBackend:
        """Create the appropriate database backend.

        Priority order:
        1. Supabase (if URL and key are provided and dependencies are available)
        2. Local database (SQLite or PostgreSQL)

        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase anon or service role key
            local_database_url: Local database connection string
            **kwargs: Additional backend-specific configuration

        Returns:
            DatabaseBackend: Configured database backend instance

        Raises:
            ValueError: If no valid backend configuration is found
        """
        # Use Supabase Python client only when explicitly requested and DATABASE_URL is absent.
        # SUPABASE_URL/SUPABASE_KEY in env are for optional vector search, not primary DB access.
        use_supabase_backend = kwargs.pop("use_supabase_backend", False)
        if (
            use_supabase_backend
            and supabase_url
            and supabase_key
            and not local_database_url
        ):
            try:
                from .backends.supabase import SupabaseDatabaseBackend

                logger.info("Creating Supabase database backend")
                return SupabaseDatabaseBackend(
                    supabase_url=supabase_url, supabase_key=supabase_key, **kwargs
                )
            except ImportError as e:
                logger.warning(
                    f"Supabase dependencies not available ({e}). "
                    "Install with: pip install supabase"
                )
            except Exception as e:
                logger.error(f"Failed to create Supabase backend: {e}")
                logger.info("Falling back to local database backend")

        # Fallback to local database
        database_url = local_database_url or "sqlite:///./innoday.db"
        logger.info(f"Creating local database backend: {database_url}")
        return LocalDatabaseBackend(database_url, **kwargs)

    @staticmethod
    def from_environment(**kwargs) -> DatabaseBackend:
        """Create database backend from environment variables.

        Environment variables checked:
        - SUPABASE_URL: Supabase project URL
        - SUPABASE_KEY: Supabase anon or service role key
        - DATABASE_URL: PostgreSQL connection string (for both local and Supabase)
        Args:
            **kwargs: Additional backend-specific configuration

        Returns:
            DatabaseBackend: Configured database backend instance
        """
        # Supabase configuration
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        # Local database configuration
        local_database_url = os.getenv("DATABASE_URL")

        # Additional configuration from environment
        config = {
            "postgres_url": os.getenv("DATABASE_URL"),
            "echo": os.getenv("DATABASE_ECHO", "false").lower() == "true",
            **kwargs,
        }

        # Remove None values
        config = {k: v for k, v in config.items() if v is not None}

        logger.info("Creating database backend from environment configuration")
        return DatabaseFactory.create_backend(
            supabase_url=supabase_url,
            supabase_key=supabase_key,
            local_database_url=local_database_url,
            **config,
        )

    @staticmethod
    def get_available_backends() -> Dict[str, Dict[str, Any]]:
        """Get information about available database backends.

        Returns:
            Dict mapping backend names to their availability and features
        """
        backends = {
            "local": {
                "available": True,
                "description": "Local SQLite or PostgreSQL database",
                "features": {
                    "vector_search": False,
                    "real_time_subscriptions": False,
                    "full_text_search": True,
                    "analytics": False,
                    "cloud_scaling": False,
                },
                "requirements": ["sqlmodel", "sqlalchemy"],
            }
        }

        # Check Supabase availability
        try:
            pass

            backends["supabase"] = {
                "available": True,
                "description": "Supabase cloud database with vector search",
                "features": {
                    "vector_search": True,
                    "real_time_subscriptions": True,
                    "full_text_search": True,
                    "analytics": True,
                    "cloud_scaling": True,
                },
                "requirements": ["supabase", "sqlmodel"],
            }
        except ImportError:
            backends["supabase"] = {
                "available": False,
                "description": "Supabase cloud database with vector search",
                "error": "Dependencies not installed (pip install supabase)",
                "requirements": ["supabase", "sqlmodel"],
            }

        return backends

    @staticmethod
    def validate_configuration(
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
        local_database_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Validate database configuration.

        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase anon or service role key
            local_database_url: Local database connection string

        Returns:
            Dict with validation results and recommendations
        """
        validation = {
            "valid": False,
            "backend_type": None,
            "warnings": [],
            "errors": [],
            "recommendations": [],
        }

        # Check Supabase configuration
        if supabase_url and supabase_key:
            try:
                pass

                validation["valid"] = True
                validation["backend_type"] = "supabase"

                # Check database URL
                if not os.getenv("DATABASE_URL"):
                    validation["warnings"].append(
                        "DATABASE_URL not set - using default connection string"
                    )

            except ImportError:
                validation["errors"].append(
                    "Supabase dependencies not available. Install with: pip install supabase"
                )

        # Check local database configuration
        elif local_database_url or os.getenv("DATABASE_URL"):
            validation["valid"] = True
            validation["backend_type"] = "local"

            db_url = local_database_url or os.getenv("DATABASE_URL")
            if "sqlite" in db_url.lower():
                validation["recommendations"].append(
                    "Consider PostgreSQL for better performance and full-text search"
                )

        else:
            # Default SQLite
            validation["valid"] = True
            validation["backend_type"] = "local"
            validation["warnings"].append(
                "Using default SQLite database - consider configuring PostgreSQL or Supabase for production"
            )

        return validation


# Dependency injection functions
def set_database_backend(backend: DatabaseBackend) -> None:
    """Set the global database backend instance.

    Args:
        backend: Database backend to use globally
    """
    global _current_backend
    _current_backend = backend
    logger.info(f"Set global database backend: {backend}")


def get_database_backend() -> DatabaseBackend:
    """Get the current global database backend instance.

    If no backend is set, creates one from environment configuration.

    Returns:
        DatabaseBackend: Current global database backend
    """
    global _current_backend

    if _current_backend is None:
        _current_backend = DatabaseFactory.from_environment()
        logger.info("Created database backend from environment")

    return _current_backend


async def initialize_database() -> DatabaseBackend:
    """Initialize the database backend and create tables.

    Returns:
        DatabaseBackend: Initialized database backend
    """
    backend = get_database_backend()

    try:
        # Create tables and schema
        await backend.create_tables()

        # Health check
        health = await backend.health_check()
        if health.get("status") == "healthy":
            logger.info(f"Database backend initialized successfully: {backend}")
        else:
            logger.warning(f"Database backend health check failed: {health}")

        return backend

    except Exception as e:
        logger.error(f"Failed to initialize database backend: {e}")
        raise


async def close_database() -> None:
    """Close the current database backend and cleanup resources."""
    global _current_backend

    if _current_backend:
        try:
            await _current_backend.close()
            logger.info("Database backend closed successfully")
        except Exception as e:
            logger.error(f"Error closing database backend: {e}")
        finally:
            _current_backend = None


# Utility functions for FastAPI dependency injection
async def get_db_session():
    """FastAPI dependency for getting database session.

    Yields:
        Session: Database session
    """
    backend = get_database_backend()
    session = await backend.get_session()
    try:
        yield session
    finally:
        session.close()


def get_db_backend() -> DatabaseBackend:
    """FastAPI dependency for getting database backend.

    Returns:
        DatabaseBackend: Current database backend
    """
    return get_database_backend()
