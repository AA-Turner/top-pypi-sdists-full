"""Abstract database backend interface for InnoDay."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from sqlmodel import Session

logger = logging.getLogger(__name__)


class DatabaseBackend(ABC):
    """Abstract base class for database backends.

    This interface provides a unified API for different database implementations,
    allowing InnoDay to work with both local databases (SQLite/PostgreSQL) and
    cloud-based solutions (Supabase) while maintaining feature parity where possible.
    """

    def __init__(self, connection_string: str, **kwargs):
        """Initialize the database backend.

        Args:
            connection_string: Database connection string or URL
            **kwargs: Additional backend-specific configuration
        """
        self.connection_string = connection_string
        self.config = kwargs

    @abstractmethod
    async def get_session(self) -> Session:
        """Get a database session for SQLModel operations.

        Returns:
            Session: SQLModel database session
        """

    @abstractmethod
    async def create_tables(self) -> None:
        """Initialize database schema and create tables.

        This method should create all necessary tables and indexes
        for the InnoDay application.
        """

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check database backend health and connectivity.

        Returns:
            Dict containing health status, version info, and performance metrics
        """

    # Search operations
    @abstractmethod
    async def search_tickets(
        self,
        query: str,
        organization_id: str,
        limit: int = 10,
        include_similarity: bool = False,
    ) -> List[Dict[str, Any]]:
        """Search tickets with backend-specific optimization.

        Args:
            query: Search query string
            organization_id: Organization UUID for scoping
            limit: Maximum number of results
            include_similarity: Whether to include similarity scores (vector search only)

        Returns:
            List of ticket dictionaries with optional similarity scores
        """

    @abstractmethod
    async def search_repositories(
        self,
        query: str,
        organization_id: str,
        limit: int = 10,
        include_similarity: bool = False,
    ) -> List[Dict[str, Any]]:
        """Search repositories with backend-specific optimization.

        Args:
            query: Search query string
            organization_id: Organization UUID for scoping
            limit: Maximum number of results
            include_similarity: Whether to include similarity scores (vector search only)

        Returns:
            List of repository dictionaries with optional similarity scores
        """

    @abstractmethod
    async def search_all_content(
        self,
        query: str,
        organization_id: str,
        content_types: Optional[List[str]] = None,
        limit: int = 10,
        include_similarity: bool = False,
    ) -> Dict[str, Any]:
        """Search across multiple content types.

        Args:
            query: Search query string
            organization_id: Organization UUID for scoping
            content_types: List of content types to search (tickets, repositories)
            limit: Maximum number of results per content type
            include_similarity: Whether to include similarity scores

        Returns:
            Dictionary with search results grouped by content type
        """

    # Vector search capabilities
    def supports_vector_search(self) -> bool:
        """Check if backend supports vector search operations.

        Returns:
            True if vector search is supported, False otherwise
        """
        return False

    async def generate_embeddings(
        self, content: str, content_type: str
    ) -> Optional[List[float]]:
        """Generate vector embeddings for content.

        Args:
            content: Text content to embed
            content_type: Type of content (ticket, repository, readme)

        Returns:
            Vector embedding as list of floats, None if not supported
        """
        return None

    async def store_embedding(
        self, content_id: str, content_type: str, embedding: List[float]
    ) -> bool:
        """Store vector embedding for content.

        Args:
            content_id: Unique identifier for the content
            content_type: Type of content (ticket, repository)
            embedding: Vector embedding to store

        Returns:
            True if successful, False otherwise
        """
        return False

    async def find_similar_content(
        self,
        embedding: List[float],
        content_type: str,
        organization_id: str,
        threshold: float = 0.7,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Find similar content using vector similarity.

        Args:
            embedding: Query vector embedding
            content_type: Type of content to search
            organization_id: Organization UUID for scoping
            threshold: Minimum similarity threshold
            limit: Maximum number of results

        Returns:
            List of similar content with similarity scores
        """
        return []

    # Bulk operations for embeddings
    async def get_missing_embeddings(
        self, content_type: str, organization_id: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get content that doesn't have embeddings yet.

        Args:
            content_type: Type of content (ticket, repository)
            organization_id: Optional organization UUID for scoping
            limit: Maximum number of items to return

        Returns:
            List of content items missing embeddings
        """
        return []

    async def get_outdated_embeddings(
        self,
        content_type: str,
        max_age_hours: int = 24,
        organization_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get content with outdated embeddings.

        Args:
            content_type: Type of content (ticket, repository)
            max_age_hours: Maximum age of embeddings in hours
            organization_id: Optional organization UUID for scoping
            limit: Maximum number of items to return

        Returns:
            List of content items with outdated embeddings
        """
        return []

    # Real-time features
    def supports_real_time_subscriptions(self) -> bool:
        """Check if backend supports real-time data subscriptions.

        Returns:
            True if real-time subscriptions are supported, False otherwise
        """
        return False

    async def subscribe_to_changes(
        self, table_name: str, organization_id: str, callback: callable
    ) -> Optional[str]:
        """Subscribe to real-time changes for a table.

        Args:
            table_name: Name of the table to monitor
            organization_id: Organization UUID for scoping
            callback: Function to call when changes occur

        Returns:
            Subscription ID if successful, None if not supported
        """
        return None

    async def unsubscribe_from_changes(self, subscription_id: str) -> bool:
        """Unsubscribe from real-time changes.

        Args:
            subscription_id: ID of the subscription to cancel

        Returns:
            True if successful, False otherwise
        """
        return False

    # Analytics and insights
    async def get_search_analytics(
        self,
        organization_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get search analytics for the organization.

        Args:
            organization_id: Organization UUID
            start_date: Start date for analytics (ISO format)
            end_date: End date for analytics (ISO format)

        Returns:
            Dictionary with search analytics data
        """
        return {}

    async def get_embedding_statistics(
        self, organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get statistics about embeddings in the database.

        Args:
            organization_id: Optional organization UUID for scoping

        Returns:
            Dictionary with embedding statistics
        """
        return {
            "total_embeddings": 0,
            "tickets_with_embeddings": 0,
            "repositories_with_embeddings": 0,
            "last_updated": None,
        }

    # Utility methods
    def get_backend_type(self) -> str:
        """Get the type of database backend.

        Returns:
            String identifier for the backend type
        """
        return self.__class__.__name__.lower().replace("databasebackend", "")

    def get_features(self) -> Dict[str, bool]:
        """Get a dictionary of supported features.

        Returns:
            Dictionary mapping feature names to support status
        """
        return {
            "vector_search": self.supports_vector_search(),
            "real_time_subscriptions": self.supports_real_time_subscriptions(),
            "full_text_search": True,  # All backends should support basic text search
            "analytics": True,
            "bulk_operations": True,
        }

    async def close(self) -> None:
        """Close database connections and cleanup resources."""

    def __str__(self) -> str:
        """String representation of the backend."""
        return f"{self.get_backend_type().title()}DatabaseBackend"

    def __repr__(self) -> str:
        """Detailed string representation of the backend."""
        return (
            f"{self.__class__.__name__}(connection_string='{self.connection_string}')"
        )
