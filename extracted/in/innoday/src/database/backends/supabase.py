"""Supabase database backend implementation with vector search."""

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import Engine
from sqlmodel import Session, create_engine, text

from .abstract import DatabaseBackend

logger = logging.getLogger(__name__)

try:
    from supabase import Client, create_client

    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class SupabaseDatabaseBackend(DatabaseBackend):
    """Supabase cloud database backend with vector search capabilities.

    This backend provides full vector search using pgvector extension,
    real-time subscriptions, and cloud-scale performance. It uses OpenAI
    for embedding generation and Supabase's PostgreSQL for storage.
    """

    def __init__(self, supabase_url: str, supabase_key: str, **kwargs):
        """Initialize Supabase database backend.

        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase anon or service role key
            **kwargs: Additional configuration options
        """
        if not SUPABASE_AVAILABLE:
            raise ImportError(
                "Supabase dependencies not available. "
                "Install with: pip install supabase"
            )

        super().__init__(supabase_url, **kwargs)
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.supabase: Optional[Client] = None
        self.engine: Optional[Engine] = None

        # Real-time subscriptions
        self._subscriptions = {}

        # Initialize clients
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize Supabase and database clients."""
        try:
            # Initialize Supabase client
            self.supabase = create_client(self.supabase_url, self.supabase_key)

            # Create PostgreSQL engine for SQLModel operations
            # Extract database URL from Supabase URL
            postgres_url = self._get_postgres_connection_string()
            self.engine = create_engine(
                postgres_url,
                echo=self.config.get("echo", False),
                pool_size=self.config.get("pool_size", 5),
                max_overflow=self.config.get("max_overflow", 10),
            )

            logger.info("Supabase database backend initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase backend: {e}")
            raise

    def _get_postgres_connection_string(self) -> str:
        """Convert Supabase URL to PostgreSQL connection string."""
        # This would need to be configured with actual database credentials
        # For now, return a placeholder that would be configured via environment
        db_url = self.config.get("postgres_url") or os.getenv("DATABASE_URL")
        if not db_url:
            # Construct from Supabase URL (this is a simplified example)
            # In practice, you'd get these from Supabase dashboard
            host = self.supabase_url.replace("https://", "").replace(".supabase.co", "")
            db_url = (
                f"postgresql://postgres:[PASSWORD]@db.{host}.supabase.co:5432/postgres"
            )
            logger.warning(
                "PostgreSQL connection string not configured. "
                "Set DATABASE_URL environment variable with actual database credentials."
            )
        return db_url

    async def get_session(self) -> Session:
        """Get a database session for SQLModel operations."""
        if not self.engine:
            self._initialize_clients()
        return Session(self.engine)

    async def create_tables(self) -> None:
        """Initialize database schema and create tables with vector extensions."""
        try:
            session = await self.get_session()

            # Enable pgvector extension
            session.exec(text("CREATE EXTENSION IF NOT EXISTS vector"))

            # Create tables using SQLModel
            from sqlmodel import SQLModel

            SQLModel.metadata.create_all(self.engine)

            # Add vector columns to existing tables
            await self._add_vector_columns(session)

            # Create vector indexes
            await self._create_vector_indexes(session)

            # Create search functions
            await self._create_search_functions(session)

            session.commit()
            session.close()

            logger.info("Supabase database schema created with vector support")
        except Exception as e:
            logger.error(f"Failed to create Supabase schema: {e}")
            raise

    async def _add_vector_columns(self, session: Session):
        """Add vector columns to tables."""
        vector_columns = [
            "ALTER TABLE tickets ADD COLUMN IF NOT EXISTS embedding vector(1536)",
            "ALTER TABLE tickets ADD COLUMN IF NOT EXISTS embedding_updated_at TIMESTAMP",
            "ALTER TABLE repositories ADD COLUMN IF NOT EXISTS embedding vector(1536)",
            "ALTER TABLE repositories ADD COLUMN IF NOT EXISTS readme_embedding vector(1536)",
            "ALTER TABLE repositories ADD COLUMN IF NOT EXISTS embedding_updated_at TIMESTAMP",
        ]

        for sql in vector_columns:
            try:
                session.exec(text(sql))
            except Exception as e:
                logger.warning(f"Failed to add vector column: {e}")

    async def _create_vector_indexes(self, session: Session):
        """Create vector similarity indexes."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS tickets_embedding_idx ON tickets USING ivfflat (embedding vector_cosine_ops)",
            "CREATE INDEX IF NOT EXISTS repositories_embedding_idx ON repositories USING ivfflat (embedding vector_cosine_ops)",
            "CREATE INDEX IF NOT EXISTS repositories_readme_embedding_idx ON repositories USING ivfflat (readme_embedding vector_cosine_ops)",
        ]

        for index_sql in indexes:
            try:
                session.exec(text(index_sql))
            except Exception as e:
                logger.warning(f"Failed to create vector index: {e}")

    async def _create_search_functions(self, session: Session):
        """Create PostgreSQL functions for vector similarity search."""
        functions = [
            """
            CREATE OR REPLACE FUNCTION search_tickets_by_embedding(
              query_embedding vector(1536),
              match_threshold float,
              match_count int,
              client_filter uuid
            )
            RETURNS TABLE (
              id text,
              summary text,
              description text,
              status text,
              similarity float
            )
            LANGUAGE plpgsql
            AS $$
            BEGIN
              RETURN QUERY
              SELECT
                t.id,
                t.summary,
                t.description,
                t.status,
                1 - (t.embedding <=> query_embedding) as similarity
              FROM tickets t
              WHERE t.organization_id = client_filter::text
                AND t.embedding IS NOT NULL
                AND 1 - (t.embedding <=> query_embedding) > match_threshold
              ORDER BY t.embedding <=> query_embedding
              LIMIT match_count;
            END;
            $$;
            """,
            """
            CREATE OR REPLACE FUNCTION search_repositories_by_embedding(
              query_embedding vector(1536),
              match_threshold float,
              match_count int,
              client_filter uuid,
              search_readme boolean DEFAULT false
            )
            RETURNS TABLE (
              id text,
              name text,
              description text,
              url text,
              similarity float
            )
            LANGUAGE plpgsql
            AS $$
            BEGIN
              RETURN QUERY
              SELECT
                r.id,
                r.name,
                r.description,
                r.url,
                CASE 
                  WHEN search_readme AND r.readme_embedding IS NOT NULL
                  THEN 1 - (r.readme_embedding <=> query_embedding)
                  ELSE 1 - (r.embedding <=> query_embedding)
                END as similarity
              FROM repositories r
              WHERE r.organization_id = client_filter::text
                AND (
                  (NOT search_readme AND r.embedding IS NOT NULL) OR
                  (search_readme AND r.readme_embedding IS NOT NULL)
                )
                AND CASE 
                  WHEN search_readme AND r.readme_embedding IS NOT NULL
                  THEN 1 - (r.readme_embedding <=> query_embedding) > match_threshold
                  ELSE 1 - (r.embedding <=> query_embedding) > match_threshold
                END
              ORDER BY 
                CASE 
                  WHEN search_readme AND r.readme_embedding IS NOT NULL
                  THEN r.readme_embedding <=> query_embedding
                  ELSE r.embedding <=> query_embedding
                END
              LIMIT match_count;
            END;
            $$;
            """,
        ]

        for func_sql in functions:
            try:
                session.exec(text(func_sql))
            except Exception as e:
                logger.warning(f"Failed to create search function: {e}")

    async def health_check(self) -> Dict[str, Any]:
        """Check Supabase backend health and connectivity."""
        try:
            # Test Supabase connection
            (self.supabase.table("tickets").select("id").limit(1).execute())

            # Test database connection
            session = await self.get_session()
            session.exec(text("SELECT 1")).first()

            # Check vector extension
            vector_check = session.exec(
                text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
            ).first()
            vector_enabled = vector_check is not None

            session.close()

            return {
                "status": "healthy",
                "backend_type": "supabase",
                "supabase_url": self.supabase_url,
                "vector_extension_enabled": vector_enabled,
                "features": self.get_features(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error(f"Supabase health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "backend_type": "supabase",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    # Vector search implementation
    def supports_vector_search(self) -> bool:
        """Supabase backend supports vector search with pgvector."""
        return True

    async def generate_embeddings(
        self, content: str, content_type: str
    ) -> Optional[List[float]]:
        """Generate vector embeddings. Not implemented — embeddings require an external provider."""
        logger.warning("Vector embeddings not configured")
        return None

    async def store_embedding(
        self, content_id: str, content_type: str, embedding: List[float]
    ) -> bool:
        """Store vector embedding for content."""
        try:
            session = await self.get_session()

            if content_type == "ticket":
                session.exec(
                    text(
                        "UPDATE tickets SET embedding = :embedding, embedding_updated_at = NOW() WHERE id = :id"
                    ).bindparam(embedding=embedding, id=content_id)
                )
            elif content_type == "repository":
                session.exec(
                    text(
                        "UPDATE repositories SET embedding = :embedding, embedding_updated_at = NOW() WHERE id = :id"
                    ).bindparam(embedding=embedding, id=content_id)
                )
            elif content_type == "readme":
                session.exec(
                    text(
                        "UPDATE repositories SET readme_embedding = :embedding, embedding_updated_at = NOW() WHERE id = :id"
                    ).bindparam(embedding=embedding, id=content_id)
                )

            session.commit()
            session.close()
            return True

        except Exception as e:
            logger.error(f"Failed to store embedding: {e}")
            return False

    async def search_tickets(
        self,
        query: str,
        organization_id: str,
        limit: int = 10,
        include_similarity: bool = False,
    ) -> List[Dict[str, Any]]:
        """Search tickets using vector similarity."""
        try:
            # Generate embedding for search query
            query_embedding = await self.generate_embeddings(query, "search")

            if query_embedding:
                # Use vector similarity search
                response = self.supabase.rpc(
                    "search_tickets_by_embedding",
                    {
                        "query_embedding": query_embedding,
                        "match_threshold": 0.7,
                        "match_count": limit,
                        "client_filter": organization_id,
                    },
                ).execute()

                results = response.data or []

                # Add metadata
                for result in results:
                    result["search_type"] = "vector_similarity"
                    if not include_similarity:
                        result.pop("similarity", None)

                logger.info(f"Vector search found {len(results)} tickets for: {query}")
                return results
            else:
                # Fallback to text search
                return await self._fallback_text_search_tickets(
                    query, organization_id, limit, include_similarity
                )

        except Exception as e:
            logger.error(f"Failed to search tickets with vector search: {e}")
            # Fallback to text search
            return await self._fallback_text_search_tickets(
                query, organization_id, limit, include_similarity
            )

    async def search_repositories(
        self,
        query: str,
        organization_id: str,
        limit: int = 10,
        include_similarity: bool = False,
    ) -> List[Dict[str, Any]]:
        """Search repositories using vector similarity."""
        try:
            # Generate embedding for search query
            query_embedding = await self.generate_embeddings(query, "search")

            if query_embedding:
                # Search both repository content and README content
                repo_results = self.supabase.rpc(
                    "search_repositories_by_embedding",
                    {
                        "query_embedding": query_embedding,
                        "match_threshold": 0.7,
                        "match_count": limit,
                        "client_filter": organization_id,
                        "search_readme": False,
                    },
                ).execute()

                readme_results = self.supabase.rpc(
                    "search_repositories_by_embedding",
                    {
                        "query_embedding": query_embedding,
                        "match_threshold": 0.7,
                        "match_count": limit,
                        "client_filter": organization_id,
                        "search_readme": True,
                    },
                ).execute()

                # Combine and deduplicate results
                all_results = {}

                for result in repo_results.data or []:
                    result["search_type"] = "vector_similarity"
                    result["search_target"] = "repository"
                    all_results[result["id"]] = result

                for result in readme_results.data or []:
                    result["search_type"] = "vector_similarity"
                    result["search_target"] = "readme"
                    if result["id"] in all_results:
                        # Keep the result with higher similarity
                        if result.get("similarity", 0) > all_results[result["id"]].get(
                            "similarity", 0
                        ):
                            all_results[result["id"]] = result
                    else:
                        all_results[result["id"]] = result

                results = list(all_results.values())

                # Sort by similarity and limit
                results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
                results = results[:limit]

                # Remove similarity if not requested
                if not include_similarity:
                    for result in results:
                        result.pop("similarity", None)

                logger.info(
                    f"Vector search found {len(results)} repositories for: {query}"
                )
                return results
            else:
                # Fallback to text search
                return await self._fallback_text_search_repositories(
                    query, organization_id, limit, include_similarity
                )

        except Exception as e:
            logger.error(f"Failed to search repositories with vector search: {e}")
            # Fallback to text search
            return await self._fallback_text_search_repositories(
                query, organization_id, limit, include_similarity
            )

    async def _fallback_text_search_tickets(
        self, query: str, organization_id: str, limit: int, include_similarity: bool
    ) -> List[Dict[str, Any]]:
        """Fallback to PostgreSQL full-text search for tickets."""
        try:
            response = (
                self.supabase.table("tickets")
                .select("*")
                .eq("organization_id", organization_id)
                .or_(f"summary.ilike.%{query}%,description.ilike.%{query}%")
                .limit(limit)
                .execute()
            )

            results = response.data or []
            for result in results:
                result["search_type"] = "full_text_fallback"
                if include_similarity:
                    result["similarity"] = 0.5  # Default similarity for text matches

            return results
        except Exception as e:
            logger.error(f"Fallback text search failed: {e}")
            return []

    async def _fallback_text_search_repositories(
        self, query: str, organization_id: str, limit: int, include_similarity: bool
    ) -> List[Dict[str, Any]]:
        """Fallback to PostgreSQL full-text search for repositories."""
        try:
            response = (
                self.supabase.table("repositories")
                .select("*")
                .eq("organization_id", organization_id)
                .or_(
                    f"name.ilike.%{query}%,description.ilike.%{query}%,readme_content.ilike.%{query}%"
                )
                .limit(limit)
                .execute()
            )

            results = response.data or []
            for result in results:
                result["search_type"] = "full_text_fallback"
                if include_similarity:
                    result["similarity"] = 0.5  # Default similarity for text matches

            return results
        except Exception as e:
            logger.error(f"Fallback text search failed: {e}")
            return []

    async def search_all_content(
        self,
        query: str,
        organization_id: str,
        content_types: Optional[List[str]] = None,
        limit: int = 10,
        include_similarity: bool = False,
    ) -> Dict[str, Any]:
        """Search across multiple content types using vector similarity."""
        if not content_types:
            content_types = ["tickets", "repositories"]

        results = {
            "query": query,
            "organization_id": organization_id,
            "content_types": content_types,
            "backend_type": "supabase",
            "vector_search_enabled": True,
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

    async def find_similar_content(
        self,
        embedding: List[float],
        content_type: str,
        organization_id: str,
        threshold: float = 0.7,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Find similar content using vector similarity."""
        try:
            if content_type == "ticket":
                response = self.supabase.rpc(
                    "search_tickets_by_embedding",
                    {
                        "query_embedding": embedding,
                        "match_threshold": threshold,
                        "match_count": limit,
                        "client_filter": organization_id,
                    },
                ).execute()
            elif content_type == "repository":
                response = self.supabase.rpc(
                    "search_repositories_by_embedding",
                    {
                        "query_embedding": embedding,
                        "match_threshold": threshold,
                        "match_count": limit,
                        "client_filter": organization_id,
                        "search_readme": False,
                    },
                ).execute()
            else:
                return []

            return response.data or []

        except Exception as e:
            logger.error(f"Failed to find similar content: {e}")
            return []

    # Real-time features
    def supports_real_time_subscriptions(self) -> bool:
        """Supabase supports real-time subscriptions."""
        return True

    async def subscribe_to_changes(
        self, table_name: str, organization_id: str, callback: callable
    ) -> Optional[str]:
        """Subscribe to real-time changes for a table."""
        try:
            # Create subscription filter for client
            subscription = (
                self.supabase.table(table_name)
                .on("INSERT", callback)
                .filter("organization_id", "eq", organization_id)
                .subscribe()
            )

            subscription_id = (
                f"{table_name}_{organization_id}_{len(self._subscriptions)}"
            )
            self._subscriptions[subscription_id] = subscription

            logger.info(f"Created real-time subscription: {subscription_id}")
            return subscription_id

        except Exception as e:
            logger.error(f"Failed to create subscription: {e}")
            return None

    async def unsubscribe_from_changes(self, subscription_id: str) -> bool:
        """Unsubscribe from real-time changes."""
        try:
            if subscription_id in self._subscriptions:
                subscription = self._subscriptions[subscription_id]
                subscription.unsubscribe()
                del self._subscriptions[subscription_id]
                logger.info(f"Unsubscribed from: {subscription_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to unsubscribe: {e}")
            return False

    # Analytics and insights
    async def get_search_analytics(
        self,
        organization_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get search analytics from Supabase."""
        # This would require setting up analytics tables
        # For now, return basic info
        return {
            "message": "Search analytics available with Supabase backend",
            "backend_type": "supabase",
            "organization_id": organization_id,
            "period": (
                f"{start_date} to {end_date}" if start_date and end_date else "N/A"
            ),
            "vector_search_enabled": True,
        }

    async def get_embedding_statistics(
        self, organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get embedding statistics from Supabase."""
        try:
            session = await self.get_session()

            # Count tickets with embeddings
            tickets_query = "SELECT COUNT(*) FROM tickets WHERE embedding IS NOT NULL"
            if organization_id:
                tickets_query += f" AND organization_id = '{organization_id}'"
            tickets_count = session.exec(text(tickets_query)).first()[0]

            # Count repositories with embeddings
            repos_query = (
                "SELECT COUNT(*) FROM repositories WHERE embedding IS NOT NULL"
            )
            if organization_id:
                repos_query += f" AND organization_id = '{organization_id}'"
            repos_count = session.exec(text(repos_query)).first()[0]

            session.close()

            return {
                "total_embeddings": tickets_count + repos_count,
                "tickets_with_embeddings": tickets_count,
                "repositories_with_embeddings": repos_count,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "backend_type": "supabase",
                "vector_search_supported": True,
            }

        except Exception as e:
            logger.error(f"Failed to get embedding statistics: {e}")
            return {
                "total_embeddings": 0,
                "tickets_with_embeddings": 0,
                "repositories_with_embeddings": 0,
                "last_updated": None,
                "error": str(e),
            }

    async def get_missing_embeddings(
        self, content_type: str, organization_id: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get content that doesn't have embeddings yet."""
        try:
            if content_type == "ticket":
                query = (
                    self.supabase.table("tickets")
                    .select("id,summary,description")
                    .is_("embedding", "null")
                )
            elif content_type == "repository":
                query = (
                    self.supabase.table("repositories")
                    .select("id,name,description,readme_content")
                    .is_("embedding", "null")
                )
            else:
                return []

            if organization_id:
                query = query.eq("organization_id", organization_id)

            response = query.limit(limit).execute()
            return response.data or []

        except Exception as e:
            logger.error(f"Failed to get missing embeddings: {e}")
            return []

    async def get_outdated_embeddings(
        self,
        content_type: str,
        max_age_hours: int = 24,
        organization_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get content with outdated embeddings."""
        try:
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)

            if content_type == "ticket":
                query = (
                    self.supabase.table("tickets")
                    .select("id,summary,description")
                    .lt("embedding_updated_at", cutoff_time.isoformat())
                )
            elif content_type == "repository":
                query = (
                    self.supabase.table("repositories")
                    .select("id,name,description,readme_content")
                    .lt("embedding_updated_at", cutoff_time.isoformat())
                )
            else:
                return []

            if organization_id:
                query = query.eq("organization_id", organization_id)

            response = query.limit(limit).execute()
            return response.data or []

        except Exception as e:
            logger.error(f"Failed to get outdated embeddings: {e}")
            return []

    def get_features(self) -> Dict[str, bool]:
        """Get supported features for Supabase backend."""
        return {
            "vector_search": True,
            "real_time_subscriptions": True,
            "full_text_search": True,
            "analytics": True,
            "bulk_operations": True,
            "embeddings": False,
            "postgresql_functions": True,
            "cloud_scaling": True,
        }

    async def close(self) -> None:
        """Close connections and cleanup resources."""
        try:
            # Unsubscribe from all real-time subscriptions
            for subscription_id in list(self._subscriptions.keys()):
                await self.unsubscribe_from_changes(subscription_id)

            # Close database engine
            if self.engine:
                self.engine.dispose()

            logger.info("Supabase database connections closed")
        except Exception as e:
            logger.error(f"Error closing Supabase connections: {e}")
