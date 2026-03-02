"""Batch embedding indexer for Kuzu entities."""

from typing import Optional

from ..graph.connection import KuzuConnection, get_connection
from .service import EmbeddingService
from ..utils.logger import log


class EmbeddingIndexer:
    """Generates and stores embeddings for graph entities."""

    def __init__(
        self,
        connection: Optional[KuzuConnection] = None,
        embedding_service: Optional[EmbeddingService] = None,
    ):
        """Initialize embedding indexer.

        Args:
            connection: Kuzu connection. If None, uses global connection.
            embedding_service: Embedding service. If None, creates new one.
        """
        self.connection = connection or get_connection()
        self.embedding_service = embedding_service or EmbeddingService()

    def index_pull_requests(self, batch_size: int = 50) -> int:
        """Generate embeddings for PRs without embeddings.

        Args:
            batch_size: Number of PRs to process per batch

        Returns:
            Number of PRs indexed
        """
        if not self.embedding_service.is_available:
            log.warning("OpenAI API key not configured. Skipping PR embedding.")
            return 0

        log.info("Indexing PR embeddings...")
        indexed_count = 0

        # Get PRs without embeddings
        prs = self.connection.execute("""
            MATCH (pr:PullRequest)
            WHERE pr.embedding IS NULL
            RETURN pr.number AS number,
                   pr.title AS title,
                   pr.description AS description
            LIMIT $limit
        """, {"limit": batch_size})

        while prs:
            # Generate embeddings
            texts = [
                f"{pr['title']}\n\n{pr['description'] or ''}"
                for pr in prs
            ]
            embeddings = self.embedding_service.embed_texts(texts)

            # Update PRs with embeddings
            for pr, embedding in zip(prs, embeddings):
                if embedding:
                    self.connection.execute_write("""
                        MATCH (pr:PullRequest {number: $number})
                        SET pr.embedding = $embedding
                    """, {"number": pr['number'], "embedding": list(embedding)})
                    indexed_count += 1

            log.info(f"Indexed {indexed_count} PR embeddings...")

            # Get next batch
            prs = self.connection.execute("""
                MATCH (pr:PullRequest)
                WHERE pr.embedding IS NULL
                RETURN pr.number AS number,
                       pr.title AS title,
                       pr.description AS description
                LIMIT $limit
            """, {"limit": batch_size})

        log.info(f"Completed indexing {indexed_count} PR embeddings")
        return indexed_count

    def _build_function_text(self, func: dict) -> str:
        """Build rich text for function embedding.

        Includes file path, name, signature, and docstring for better semantic matching.
        """
        parts = []

        # File path provides directory/module context (e.g., "components/Button.tsx")
        if func.get('file_path'):
            # Use just the relative path portion
            path = func['file_path']
            if '/' in path:
                # Take last 3 parts of path for context
                path_parts = path.split('/')
                path = '/'.join(path_parts[-3:]) if len(path_parts) > 3 else path
            parts.append(f"File: {path}")

        # Function name (often descriptive: handleClick, fetchUserData, etc.)
        parts.append(f"Function: {func['name']}")

        # Signature provides parameter context
        if func.get('signature'):
            parts.append(f"Signature: {func['signature']}")

        # Docstring is the most semantic-rich when available
        if func.get('docstring'):
            parts.append(f"Description: {func['docstring']}")

        return "\n".join(parts)

    def index_functions(self, batch_size: int = 100, reindex: bool = False) -> int:
        """Generate embeddings for all functions.

        Args:
            batch_size: Number of functions to process per batch
            reindex: If True, re-generate embeddings even for functions that have them

        Returns:
            Number of functions indexed
        """
        if not self.embedding_service.is_available:
            log.warning("OpenAI API key not configured. Skipping function embedding.")
            return 0

        log.info("Indexing function embeddings (all functions)...")
        indexed_count = 0

        # Get functions without embeddings (or all if reindexing)
        where_clause = "" if reindex else "WHERE f.embedding IS NULL"
        functions = self.connection.execute(f"""
            MATCH (f:Function)
            {where_clause}
            RETURN f.qualified_name AS qualified_name,
                   f.name AS name,
                   f.docstring AS docstring,
                   f.file_path AS file_path
            LIMIT $limit
        """, {"limit": batch_size})

        while functions:
            # Generate embeddings with rich context
            texts = [self._build_function_text(func) for func in functions]
            embeddings = self.embedding_service.embed_texts(texts)

            # Update functions with embeddings
            for func, embedding in zip(functions, embeddings):
                if embedding:
                    self.connection.execute_write("""
                        MATCH (f:Function {qualified_name: $qualified_name})
                        SET f.embedding = $embedding
                    """, {"qualified_name": func['qualified_name'], "embedding": list(embedding)})
                    indexed_count += 1

            log.info(f"Indexed {indexed_count} function embeddings...")

            # Get next batch
            functions = self.connection.execute(f"""
                MATCH (f:Function)
                {where_clause}
                RETURN f.qualified_name AS qualified_name,
                       f.name AS name,
                       f.docstring AS docstring,
                       f.file_path AS file_path
                LIMIT $limit
            """, {"limit": batch_size})

        log.info(f"Completed indexing {indexed_count} function embeddings")
        return indexed_count

    def _build_class_text(self, cls: dict) -> str:
        """Build rich text for class embedding.

        Includes file path, name, and docstring for better semantic matching.
        """
        parts = []

        # File path provides directory/module context
        if cls.get('file_path'):
            path = cls['file_path']
            if '/' in path:
                path_parts = path.split('/')
                path = '/'.join(path_parts[-3:]) if len(path_parts) > 3 else path
            parts.append(f"File: {path}")

        # Class name
        parts.append(f"Class: {cls['name']}")

        # Docstring when available
        if cls.get('docstring'):
            parts.append(f"Description: {cls['docstring']}")

        return "\n".join(parts)

    def index_classes(self, batch_size: int = 100, reindex: bool = False) -> int:
        """Generate embeddings for all classes.

        Args:
            batch_size: Number of classes to process per batch
            reindex: If True, re-generate embeddings even for classes that have them

        Returns:
            Number of classes indexed
        """
        if not self.embedding_service.is_available:
            log.warning("OpenAI API key not configured. Skipping class embedding.")
            return 0

        log.info("Indexing class embeddings (all classes)...")
        indexed_count = 0

        # Get classes without embeddings (or all if reindexing)
        where_clause = "" if reindex else "WHERE c.embedding IS NULL"
        classes = self.connection.execute(f"""
            MATCH (c:Class)
            {where_clause}
            RETURN c.qualified_name AS qualified_name,
                   c.name AS name,
                   c.docstring AS docstring,
                   c.file_path AS file_path
            LIMIT $limit
        """, {"limit": batch_size})

        while classes:
            # Generate embeddings with rich context
            texts = [self._build_class_text(cls) for cls in classes]
            embeddings = self.embedding_service.embed_texts(texts)

            # Update classes with embeddings
            for cls, embedding in zip(classes, embeddings):
                if embedding:
                    self.connection.execute_write("""
                        MATCH (c:Class {qualified_name: $qualified_name})
                        SET c.embedding = $embedding
                    """, {"qualified_name": cls['qualified_name'], "embedding": list(embedding)})
                    indexed_count += 1

            log.info(f"Indexed {indexed_count} class embeddings...")

            # Get next batch
            classes = self.connection.execute(f"""
                MATCH (c:Class)
                {where_clause}
                RETURN c.qualified_name AS qualified_name,
                       c.name AS name,
                       c.docstring AS docstring,
                       c.file_path AS file_path
                LIMIT $limit
            """, {"limit": batch_size})

        log.info(f"Completed indexing {indexed_count} class embeddings")
        return indexed_count

    def _build_community_text(self, community: dict) -> str:
        """Build rich text for community embedding.

        Includes community ID and description for semantic matching.
        """
        parts = []
        parts.append(f"Community {community['community_id']}")
        if community.get('description'):
            parts.append(f"Description: {community['description']}")
        return "\n".join(parts)

    def index_communities(self, batch_size: int = 50, reindex: bool = False) -> int:
        """Generate embeddings for community descriptions.

        Args:
            batch_size: Number of communities to process per batch
            reindex: If True, re-generate embeddings even for communities that have them

        Returns:
            Number of communities indexed
        """
        if not self.embedding_service.is_available:
            log.warning("Embedding service not available. Skipping community embedding.")
            return 0

        log.info("Indexing community embeddings...")
        indexed_count = 0

        # Get communities with descriptions but without embeddings (or all if reindexing)
        where_clause = "WHERE c.description IS NOT NULL" + ("" if reindex else " AND c.embedding IS NULL")
        communities = self.connection.execute(f"""
            MATCH (c:Community)
            {where_clause}
            RETURN c.community_id AS community_id,
                   c.description AS description
            LIMIT $limit
        """, {"limit": batch_size})

        while communities:
            # Generate embeddings
            texts = [self._build_community_text(c) for c in communities]
            embeddings = self.embedding_service.embed_texts(texts)

            # Update communities with embeddings
            for community, embedding in zip(communities, embeddings):
                if embedding:
                    self.connection.execute_write("""
                        MATCH (c:Community {community_id: $community_id})
                        SET c.embedding = $embedding
                    """, {"community_id": community['community_id'], "embedding": list(embedding)})
                    indexed_count += 1

            log.info(f"Indexed {indexed_count} community embeddings...")

            # Get next batch
            communities = self.connection.execute(f"""
                MATCH (c:Community)
                {where_clause}
                RETURN c.community_id AS community_id,
                       c.description AS description
                LIMIT $limit
            """, {"limit": batch_size})

        log.info(f"Completed indexing {indexed_count} community embeddings")
        return indexed_count

    def index_all(self, reindex: bool = False) -> dict:
        """Index embeddings for all entity types.

        Args:
            reindex: If True, re-generate all embeddings (useful after improving
                    embedding quality or changing the text format)

        Returns:
            Dictionary with counts per entity type
        """
        return {
            "pull_requests": self.index_pull_requests(),
            "functions": self.index_functions(reindex=reindex),
            "classes": self.index_classes(reindex=reindex),
            "communities": self.index_communities(reindex=reindex),
        }

    def search(
        self,
        query: str,
        entity_types: list[str] | None = None,
        limit: int = 10,
        min_score: float = 0.5,
    ) -> list[dict]:
        """Search for entities using semantic similarity.

        Args:
            query: Natural language search query
            entity_types: Types to search (Function, Class, File). If None, searches all.
            limit: Maximum results
            min_score: Minimum similarity score (0-1)

        Returns:
            List of matching entities with scores
        """
        if not self.embedding_service.is_available:
            return []

        # Generate query embedding
        query_embedding = self.embedding_service.embed_query(query)
        if query_embedding is None:
            return []

        results = []
        types_to_search = entity_types or ["Function", "Class"]

        for entity_type in types_to_search:
            if entity_type == "Function":
                matches = self._search_functions(query_embedding, limit, min_score)
            elif entity_type == "Class":
                matches = self._search_classes(query_embedding, limit, min_score)
            else:
                continue
            results.extend(matches)

        # Sort by score and limit
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return results[:limit]

    def _cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import math
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def _search_functions(
        self, query_embedding: list[float], limit: int, min_score: float
    ) -> list[dict]:
        """Search functions by embedding similarity."""
        results = []

        # Get all functions with embeddings
        try:
            functions = self.connection.execute("""
                MATCH (f:Function)
                WHERE f.embedding IS NOT NULL
                RETURN f.qualified_name AS qualified_name,
                       f.name AS name,
                       f.file_path AS file_path,
                       f.docstring AS docstring,
                       f.embedding AS embedding
            """)
        except Exception:
            # Table doesn't exist or other error - return empty results
            return []

        for func in functions:
            if func.get("embedding"):
                score = self._cosine_similarity(query_embedding, func["embedding"])
                if score >= min_score:
                    results.append({
                        "qualified_name": func["qualified_name"],
                        "name": func["name"],
                        "file_path": func["file_path"],
                        "type": "Function",
                        "node_type": "Function",
                        "score": score,
                        "docstring": func.get("docstring"),
                    })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def _search_classes(
        self, query_embedding: list[float], limit: int, min_score: float
    ) -> list[dict]:
        """Search classes by embedding similarity."""
        results = []

        # Get all classes with embeddings
        try:
            classes = self.connection.execute("""
                MATCH (c:Class)
                WHERE c.embedding IS NOT NULL
                RETURN c.qualified_name AS qualified_name,
                       c.name AS name,
                       c.file_path AS file_path,
                       c.docstring AS docstring,
                       c.embedding AS embedding
            """)
        except Exception:
            # Table doesn't exist or other error - return empty results
            return []

        for cls in classes:
            if cls.get("embedding"):
                score = self._cosine_similarity(query_embedding, cls["embedding"])
                if score >= min_score:
                    results.append({
                        "qualified_name": cls["qualified_name"],
                        "name": cls["name"],
                        "file_path": cls["file_path"],
                        "type": "Class",
                        "node_type": "Class",
                        "score": score,
                        "docstring": cls.get("docstring"),
                    })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def get_embedding_stats(self) -> dict:
        """Get embedding coverage statistics.

        Returns:
            Dictionary with embedding stats per entity type
        """
        stats = {}

        # PR stats
        pr_results = self.connection.execute("""
            MATCH (pr:PullRequest)
            RETURN count(pr) AS total,
                   count(pr.embedding) AS with_embedding
        """)
        if pr_results:
            record = pr_results[0]
            stats["pull_requests"] = {
                "total": record["total"],
                "with_embedding": record["with_embedding"],
            }

        # Function stats
        func_results = self.connection.execute("""
            MATCH (f:Function)
            RETURN count(f) AS total,
                   count(f.embedding) AS with_embedding,
                   count(CASE WHEN f.docstring IS NOT NULL THEN 1 END) AS with_docstring
        """)
        if func_results:
            record = func_results[0]
            stats["functions"] = {
                "total": record["total"],
                "with_embedding": record["with_embedding"],
                "with_docstring": record["with_docstring"],
            }

        # Class stats
        class_results = self.connection.execute("""
            MATCH (c:Class)
            RETURN count(c) AS total,
                   count(c.embedding) AS with_embedding,
                   count(CASE WHEN c.docstring IS NOT NULL THEN 1 END) AS with_docstring
        """)
        if class_results:
            record = class_results[0]
            stats["classes"] = {
                "total": record["total"],
                "with_embedding": record["with_embedding"],
                "with_docstring": record["with_docstring"],
            }

        # Community stats
        community_results = self.connection.execute("""
            MATCH (c:Community)
            RETURN count(c) AS total,
                   count(c.embedding) AS with_embedding,
                   count(CASE WHEN c.description IS NOT NULL THEN 1 END) AS with_description
        """)
        if community_results:
            record = community_results[0]
            stats["communities"] = {
                "total": record["total"],
                "with_embedding": record["with_embedding"],
                "with_description": record["with_description"],
            }

        return stats
