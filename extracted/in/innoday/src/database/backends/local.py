"""Local database backend implementation for SQLite and PostgreSQL."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import Engine
from sqlmodel import Session, and_, create_engine, or_, select, text

from src.domain.repository import Repository
from src.domain.ticket import Ticket

from .abstract import DatabaseBackend

logger = logging.getLogger(__name__)


class LocalDatabaseBackend(DatabaseBackend):
    """Local database backend for SQLite and PostgreSQL.

    This backend provides full-text search capabilities using SQL LIKE queries
    for SQLite and PostgreSQL's built-in full-text search for PostgreSQL.
    Vector search is not supported but gracefully degrades to text search.
    """

    def __init__(self, connection_string: str, **kwargs):
        """Initialize local database backend.

        Args:
            connection_string: Database URL (sqlite:// or postgresql://)
            **kwargs: Additional configuration options
        """
        super().__init__(connection_string, **kwargs)
        self.engine: Optional[Engine] = None
        self.is_postgresql = "postgresql" in connection_string.lower()
        self.is_sqlite = "sqlite" in connection_string.lower()

        # Initialize engine
        self._create_engine()

    def _create_engine(self):
        """Create SQLAlchemy engine with appropriate configuration."""
        try:
            if self.is_sqlite:
                # SQLite configuration
                self.engine = create_engine(
                    self.connection_string,
                    echo=self.config.get("echo", False),
                    connect_args={"check_same_thread": False},
                )
            else:
                # PostgreSQL configuration - check for psycopg2
                try:
                    pass

                    self.engine = create_engine(
                        self.connection_string,
                        echo=self.config.get("echo", False),
                        pool_size=self.config.get("pool_size", 5),
                        max_overflow=self.config.get("max_overflow", 10),
                    )
                except ImportError:
                    logger.warning(
                        "psycopg2 not available - PostgreSQL connections will fail"
                    )
                    raise ImportError(
                        "PostgreSQL driver (psycopg2) not installed. Install with: pip install psycopg2-binary"
                    )
            logger.info(f"Created {self.get_backend_type()} database engine")
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            raise

    async def get_session(self) -> Session:
        """Get a database session for SQLModel operations."""
        if not self.engine:
            self._create_engine()
        return Session(self.engine)

    async def create_tables(self) -> None:
        """Initialize database schema and create tables."""
        try:
            from sqlmodel import SQLModel

            SQLModel.metadata.create_all(self.engine)

            # Create full-text search indexes for PostgreSQL
            if self.is_postgresql:
                await self._create_postgresql_indexes()

            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise

    async def _create_postgresql_indexes(self):
        """Create PostgreSQL-specific full-text search indexes."""
        try:
            session = await self.get_session()

            # Create GIN indexes for full-text search
            indexes = [
                """
                CREATE INDEX IF NOT EXISTS tickets_search_idx 
                ON tickets USING gin(
                    to_tsvector('english', summary || ' ' || COALESCE(description, ''))
                )
                """,
                """
                CREATE INDEX IF NOT EXISTS repositories_search_idx 
                ON repositories USING gin(
                    to_tsvector('english', 
                        name || ' ' || 
                        COALESCE(description, '') || ' ' || 
                        COALESCE(readme_content, '')
                    )
                )
                """,
            ]

            for index_sql in indexes:
                session.exec(text(index_sql))

            session.commit()
            session.close()
            logger.info("PostgreSQL full-text search indexes created")
        except Exception as e:
            logger.warning(f"Failed to create PostgreSQL indexes: {e}")

    async def health_check(self) -> Dict[str, Any]:
        """Check database backend health and connectivity."""
        try:
            session = await self.get_session()

            # Test connection with a simple query
            session.exec(text("SELECT 1")).first()

            # Get database version
            if self.is_postgresql:
                version_result = session.exec(text("SELECT version()")).first()
                db_version = version_result[0] if version_result else "Unknown"
            else:
                version_result = session.exec(text("SELECT sqlite_version()")).first()
                db_version = (
                    f"SQLite {version_result[0]}" if version_result else "Unknown"
                )

            session.close()

            return {
                "status": "healthy",
                "backend_type": self.get_backend_type(),
                "database_version": db_version,
                "connection_string": self.connection_string.split("@")[
                    -1
                ],  # Hide credentials
                "features": self.get_features(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "backend_type": self.get_backend_type(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def search_tickets(
        self,
        query: str,
        organization_id: str,
        limit: int = 10,
        include_similarity: bool = False,
    ) -> List[Dict[str, Any]]:
        """Search tickets using full-text search."""
        try:
            session = await self.get_session()

            if self.is_postgresql:
                # Use PostgreSQL full-text search
                search_query = (
                    select(Ticket)
                    .where(
                        and_(
                            Ticket.organization_id == organization_id,
                            text(
                                "to_tsvector('english', summary || ' ' || COALESCE(description, '')) "
                                "@@ plainto_tsquery('english', :query)"
                            ).bindparam(query=query),
                        )
                    )
                    .limit(limit)
                )
            else:
                # Use LIKE search for SQLite
                search_query = (
                    select(Ticket)
                    .where(
                        and_(
                            Ticket.organization_id == organization_id,
                            or_(
                                Ticket.summary.ilike(f"%{query}%"),
                                Ticket.description.ilike(f"%{query}%"),
                            ),
                        )
                    )
                    .limit(limit)
                )

            results = session.exec(search_query).all()
            session.close()

            # Convert to dictionaries
            ticket_dicts = []
            for ticket in results:
                ticket_dict = ticket.model_dump()
                # Add search metadata
                ticket_dict["search_type"] = "full_text"
                if include_similarity:
                    # Simulate similarity score for consistency
                    ticket_dict["similarity"] = self._calculate_text_similarity(
                        query, ticket
                    )
                ticket_dicts.append(ticket_dict)

            logger.info(f"Found {len(ticket_dicts)} tickets for query: {query}")
            return ticket_dicts

        except Exception as e:
            logger.error(f"Failed to search tickets: {e}")
            return []

    async def search_repositories(
        self,
        query: str,
        organization_id: str,
        limit: int = 10,
        include_similarity: bool = False,
    ) -> List[Dict[str, Any]]:
        """Search repositories using full-text search."""
        try:
            session = await self.get_session()

            if self.is_postgresql:
                # Use PostgreSQL full-text search
                search_query = (
                    select(Repository)
                    .where(
                        and_(
                            Repository.organization_id == organization_id,
                            text(
                                "to_tsvector('english', "
                                "name || ' ' || COALESCE(description, '') || ' ' || COALESCE(readme_content, '')) "
                                "@@ plainto_tsquery('english', :query)"
                            ).bindparam(query=query),
                        )
                    )
                    .limit(limit)
                )
            else:
                # Use LIKE search for SQLite
                search_query = (
                    select(Repository)
                    .where(
                        and_(
                            Repository.organization_id == organization_id,
                            or_(
                                Repository.name.ilike(f"%{query}%"),
                                Repository.description.ilike(f"%{query}%"),
                                Repository.readme_content.ilike(f"%{query}%"),
                            ),
                        )
                    )
                    .limit(limit)
                )

            results = session.exec(search_query).all()
            session.close()

            # Convert to dictionaries
            repo_dicts = []
            for repo in results:
                repo_dict = repo.model_dump()
                # Add search metadata
                repo_dict["search_type"] = "full_text"
                if include_similarity:
                    # Simulate similarity score for consistency
                    repo_dict["similarity"] = self._calculate_text_similarity(
                        query, repo
                    )
                repo_dicts.append(repo_dict)

            logger.info(f"Found {len(repo_dicts)} repositories for query: {query}")
            return repo_dicts

        except Exception as e:
            logger.error(f"Failed to search repositories: {e}")
            return []

    async def search_all_content(
        self,
        query: str,
        organization_id: str,
        content_types: Optional[List[str]] = None,
        limit: int = 10,
        include_similarity: bool = False,
    ) -> Dict[str, Any]:
        """Search across multiple content types."""
        if not content_types:
            content_types = ["tickets", "repositories"]

        results = {
            "query": query,
            "organization_id": organization_id,
            "content_types": content_types,
            "backend_type": self.get_backend_type(),
            "vector_search_enabled": False,
            "results": [],
            "total_results": 0,
        }

        try:
            # Search tickets
            if "tickets" in content_types:
                ticket_results = await self.search_tickets(
                    query, organization_id, limit, include_similarity
                )
                for result in ticket_results:
                    result["content_type"] = "ticket"
                results["results"].extend(ticket_results)

            # Search repositories
            if "repositories" in content_types:
                repo_results = await self.search_repositories(
                    query, organization_id, limit, include_similarity
                )
                for result in repo_results:
                    result["content_type"] = "repository"
                results["results"].extend(repo_results)

            results["total_results"] = len(results["results"])

            # Sort by similarity if requested
            if include_similarity:
                results["results"].sort(
                    key=lambda x: x.get("similarity", 0), reverse=True
                )

            return results

        except Exception as e:
            logger.error(f"Failed to search all content: {e}")
            results["error"] = str(e)
            return results

    def _calculate_text_similarity(self, query: str, content_obj) -> float:
        """Calculate a simple text similarity score for consistency with vector search."""
        query_lower = query.lower()

        # Get searchable text from the object
        if hasattr(content_obj, "summary"):
            # Ticket
            searchable_text = (
                f"{content_obj.summary} {content_obj.description or ''}".lower()
            )
        else:
            # Repository
            searchable_text = (
                f"{content_obj.name} {content_obj.description or ''} "
                f"{content_obj.readme_content or ''}".lower()
            )

        # Simple scoring based on query term matches
        query_terms = query_lower.split()
        matches = sum(1 for term in query_terms if term in searchable_text)

        if not query_terms:
            return 0.0

        # Base similarity on term match ratio
        base_score = matches / len(query_terms)

        # Boost score for exact phrase matches
        if query_lower in searchable_text:
            base_score += 0.3

        # Boost score for title/name matches
        if hasattr(content_obj, "summary"):
            if query_lower in content_obj.summary.lower():
                base_score += 0.2
        else:
            if query_lower in content_obj.name.lower():
                base_score += 0.2

        return min(1.0, base_score)

    # Vector search methods (not supported - return defaults)
    def supports_vector_search(self) -> bool:
        """Local database does not support vector search."""
        return False

    async def generate_embeddings(
        self, content: str, content_type: str
    ) -> Optional[List[float]]:
        """Vector embeddings not supported in local backend."""
        return None

    async def store_embedding(
        self, content_id: str, content_type: str, embedding: List[float]
    ) -> bool:
        """Vector embedding storage not supported in local backend."""
        return False

    async def find_similar_content(
        self,
        embedding: List[float],
        content_type: str,
        organization_id: str,
        threshold: float = 0.7,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Vector similarity search not supported in local backend."""
        return []

    # Real-time features (not supported)
    def supports_real_time_subscriptions(self) -> bool:
        """Local database does not support real-time subscriptions."""
        return False

    async def subscribe_to_changes(
        self, table_name: str, organization_id: str, callback: callable
    ) -> Optional[str]:
        """Real-time subscriptions not supported in local backend."""
        return None

    async def unsubscribe_from_changes(self, subscription_id: str) -> bool:
        """Real-time subscriptions not supported in local backend."""
        return False

    # Analytics and statistics
    async def get_search_analytics(
        self,
        organization_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get basic search analytics for local backend."""
        return {
            "message": "Search analytics not available for local backend",
            "backend_type": self.get_backend_type(),
            "organization_id": organization_id,
            "period": (
                f"{start_date} to {end_date}" if start_date and end_date else "N/A"
            ),
        }

    async def get_embedding_statistics(
        self, organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get embedding statistics (always zero for local backend)."""
        return {
            "total_embeddings": 0,
            "tickets_with_embeddings": 0,
            "repositories_with_embeddings": 0,
            "last_updated": None,
            "backend_type": self.get_backend_type(),
            "vector_search_supported": False,
        }

    async def get_missing_embeddings(
        self, content_type: str, organization_id: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """No missing embeddings in local backend (not supported)."""
        return []

    async def get_outdated_embeddings(
        self,
        content_type: str,
        max_age_hours: int = 24,
        organization_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """No outdated embeddings in local backend (not supported)."""
        return []

    def get_features(self) -> Dict[str, bool]:
        """Get supported features for local backend."""
        return {
            "vector_search": False,
            "real_time_subscriptions": False,
            "full_text_search": True,
            "analytics": False,
            "bulk_operations": True,
            "postgresql_fts": self.is_postgresql,
            "sqlite_like_search": self.is_sqlite,
        }

    async def close(self) -> None:
        """Close database connections and cleanup resources."""
        if self.engine:
            self.engine.dispose()
            logger.info("Local database connections closed")
