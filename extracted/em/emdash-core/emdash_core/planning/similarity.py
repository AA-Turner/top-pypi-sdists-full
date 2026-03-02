"""Semantic similarity search using Python-based vector operations."""

from typing import Optional
from datetime import datetime, timedelta

import numpy as np
from numpy.linalg import norm

from ..graph.connection import KuzuConnection, get_connection
from ..embeddings.service import EmbeddingService
from ..utils.logger import log


def cosine_similarity(vec1: list, vec2: list) -> float:
    """Compute cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score (0-1)
    """
    if not vec1 or not vec2:
        return 0.0
    a = np.array(vec1)
    b = np.array(vec2)
    if norm(a) == 0 or norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (norm(a) * norm(b)))


class SimilaritySearch:
    """Vector similarity search using Python-based cosine similarity."""

    def __init__(
        self,
        connection: Optional[KuzuConnection] = None,
        embedding_service: Optional[EmbeddingService] = None,
    ):
        """Initialize similarity search.

        Args:
            connection: Kuzu connection. If None, uses global connection.
            embedding_service: Embedding service. If None, creates new one.
        """
        self.connection = connection or get_connection()
        self.embedding_service = embedding_service or EmbeddingService()

    def find_similar_prs(
        self,
        query: str,
        limit: int = 5,
        min_score: float = 0.5,
    ) -> list[dict]:
        """Find PRs similar to a feature description.

        Args:
            query: Feature description or search query
            limit: Maximum number of results
            min_score: Minimum similarity score (0-1)

        Returns:
            List of similar PRs with metadata and scores
        """
        if not self.embedding_service.is_available:
            log.warning("OpenAI API not available. Falling back to text search.")
            return self._fallback_pr_search(query, limit)

        # Generate query embedding
        query_embedding = self.embedding_service.embed_query(query)
        if not query_embedding:
            log.error("Failed to generate query embedding")
            return []

        try:
            # Fetch all PRs with embeddings from Kuzu
            results = self.connection.execute("""
                MATCH (pr:PullRequest)
                WHERE pr.embedding IS NOT NULL
                RETURN pr.number AS number,
                       pr.title AS title,
                       pr.description AS description,
                       pr.author AS author,
                       pr.state AS state,
                       pr.labels AS labels,
                       pr.files_changed AS files_changed,
                       pr.created_at AS created_at,
                       pr.embedding AS embedding
            """)

            # Compute cosine similarity in Python
            scored_results = []
            for row in results:
                pr_embedding = row.get('embedding')
                if pr_embedding:
                    similarity = cosine_similarity(query_embedding, pr_embedding)
                    if similarity >= min_score:
                        result = {k: v for k, v in row.items() if k != 'embedding'}
                        result['score'] = similarity
                        scored_results.append(result)

            # Sort by score and return top results
            scored_results.sort(key=lambda x: x['score'], reverse=True)
            return scored_results[:limit]

        except Exception as e:
            log.warning(f"Vector search failed: {e}")
            return self._fallback_pr_search(query, limit)

    def find_similar_code(
        self,
        query: str,
        entity_types: list[str] = None,
        limit: int = 10,
        min_score: float = 0.5,
    ) -> list[dict]:
        """Find code entities similar to a description.

        Args:
            query: Feature description or search query
            entity_types: List of entity types to search (Function, Class)
            limit: Maximum number of results
            min_score: Minimum similarity score (0-1)

        Returns:
            List of similar code entities with metadata and scores
        """
        if entity_types is None:
            entity_types = ["Function", "Class"]

        if not self.embedding_service.is_available:
            log.warning("OpenAI API not available. Falling back to text search.")
            return self._fallback_code_search(query, entity_types, limit)

        # Generate query embedding
        query_embedding = self.embedding_service.embed_query(query)
        if not query_embedding:
            log.error("Failed to generate query embedding")
            return self._fallback_code_search(query, entity_types, limit)

        results = []

        try:
            # Search functions
            if "Function" in entity_types:
                func_results = self.connection.execute("""
                    MATCH (f:Function)
                    WHERE f.embedding IS NOT NULL
                    RETURN 'Function' AS type,
                           f.name AS name,
                           f.qualified_name AS qualified_name,
                           f.docstring AS docstring,
                           f.file_path AS file_path,
                           f.embedding AS embedding
                """)

                for row in func_results:
                    func_embedding = row.get('embedding')
                    if func_embedding:
                        similarity = cosine_similarity(query_embedding, func_embedding)
                        if similarity >= min_score:
                            result = {k: v for k, v in row.items() if k != 'embedding'}
                            result['score'] = similarity
                            results.append(result)

            # Search classes
            if "Class" in entity_types:
                class_results = self.connection.execute("""
                    MATCH (c:Class)
                    WHERE c.embedding IS NOT NULL
                    RETURN 'Class' AS type,
                           c.name AS name,
                           c.qualified_name AS qualified_name,
                           c.docstring AS docstring,
                           c.file_path AS file_path,
                           c.embedding AS embedding
                """)

                for row in class_results:
                    class_embedding = row.get('embedding')
                    if class_embedding:
                        similarity = cosine_similarity(query_embedding, class_embedding)
                        if similarity >= min_score:
                            result = {k: v for k, v in row.items() if k != 'embedding'}
                            result['score'] = similarity
                            results.append(result)

        except Exception as e:
            log.warning(f"Vector search failed: {e}")
            return self._fallback_code_search(query, entity_types, limit)

        # If no results from vector search, fall back to text search
        if not results:
            log.info("No vector search results. Falling back to text search.")
            return self._fallback_code_search(query, entity_types, limit)

        # Sort by score and limit
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return results[:limit]

    def _fallback_pr_search(self, query: str, limit: int) -> list[dict]:
        """Fallback to text search when vector search is unavailable.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching PRs
        """
        # Use CONTAINS for simple text matching
        results = self.connection.execute("""
            MATCH (pr:PullRequest)
            WHERE lower(pr.title) CONTAINS lower($search_term)
               OR lower(pr.description) CONTAINS lower($search_term)
            RETURN pr.number AS number,
                   pr.title AS title,
                   pr.description AS description,
                   pr.author AS author,
                   pr.state AS state,
                   pr.labels AS labels,
                   pr.files_changed AS files_changed,
                   pr.created_at AS created_at
            ORDER BY pr.created_at DESC
            LIMIT $limit
        """, {"search_term": query, "limit": limit})

        # Add default score
        for r in results:
            r['score'] = 1.0

        return results

    def _fallback_code_search(
        self,
        query: str,
        entity_types: list[str],
        limit: int,
    ) -> list[dict]:
        """Fallback to text search when vector search is unavailable.

        Args:
            query: Search query
            entity_types: Entity types to search
            limit: Maximum number of results

        Returns:
            List of matching code entities
        """
        results = []

        if "Function" in entity_types:
            func_results = self.connection.execute("""
                MATCH (f:Function)
                WHERE lower(f.name) CONTAINS lower($search_term)
                   OR lower(f.docstring) CONTAINS lower($search_term)
                RETURN 'Function' AS type,
                       f.name AS name,
                       f.qualified_name AS qualified_name,
                       f.docstring AS docstring,
                       f.file_path AS file_path
                LIMIT $limit
            """, {"search_term": query, "limit": limit})

            for r in func_results:
                r['score'] = 1.0
            results.extend(func_results)

        if "Class" in entity_types:
            class_results = self.connection.execute("""
                MATCH (c:Class)
                WHERE lower(c.name) CONTAINS lower($search_term)
                   OR lower(c.docstring) CONTAINS lower($search_term)
                RETURN 'Class' AS type,
                       c.name AS name,
                       c.qualified_name AS qualified_name,
                       c.docstring AS docstring,
                       c.file_path AS file_path
                LIMIT $limit
            """, {"search_term": query, "limit": limit})

            for r in class_results:
                r['score'] = 1.0
            results.extend(class_results)

        return results[:limit]

    def importance_weighted_search(
        self,
        query: str,
        entity_types: list[str] = None,
        limit: int = 10,
        min_score: float = 0.3,
        days: int = 30,
        semantic_weight: float = 0.4,
        importance_weight: float = 0.35,
        pagerank_weight: float = 0.25,
    ) -> list[dict]:
        """Find code entities with importance-weighted ranking.

        Combines semantic similarity with file importance and PageRank
        to find code that is both relevant AND important to the team.

        Args:
            query: Feature description or search query
            entity_types: List of entity types to search (Function, Class)
            limit: Maximum number of results
            min_score: Minimum semantic similarity score (0-1)
            days: Time window for importance calculation
            semantic_weight: Weight for semantic similarity (0-1)
            importance_weight: Weight for file importance (0-1)
            pagerank_weight: Weight for PageRank centrality (0-1)

        Returns:
            List of code entities with combined scores, sorted by relevance
        """
        if entity_types is None:
            entity_types = ["Function", "Class"]

        # Get more candidates than needed for re-ranking
        candidates = self.find_similar_code(
            query=query,
            entity_types=entity_types,
            limit=limit * 3,  # Get extra for re-ranking
            min_score=min_score,
        )

        if not candidates:
            log.info("No semantic search results found")
            return []

        log.info(f"Found {len(candidates)} semantic candidates, fetching importance scores...")

        # Fetch importance and PageRank scores for candidates
        enriched = self._enrich_with_importance(candidates, days=days)

        # Normalize and combine scores
        ranked = self._compute_combined_scores(
            enriched,
            semantic_weight=semantic_weight,
            importance_weight=importance_weight,
            pagerank_weight=pagerank_weight,
        )

        # Sort by combined score
        ranked.sort(key=lambda x: x.get("combined_score", 0), reverse=True)

        log.info(f"Re-ranked results by combined score (semantic={semantic_weight}, importance={importance_weight}, pagerank={pagerank_weight})")

        return ranked[:limit]

    def _enrich_with_importance(
        self,
        candidates: list[dict],
        days: int = 30,
    ) -> list[dict]:
        """Enrich candidates with importance and PageRank scores.

        Args:
            candidates: List of semantic search results
            days: Time window for importance calculation

        Returns:
            Candidates enriched with importance_score and pagerank_score
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%dT%H:%M:%S")

        # Group by file path for efficient querying
        file_paths = set()
        qualified_names = set()
        for c in candidates:
            if c.get("file_path"):
                file_paths.add(c["file_path"])
            if c.get("qualified_name"):
                qualified_names.add(c["qualified_name"])

        # Fetch file importance scores
        file_importance = {}
        if file_paths:
            try:
                results = self.connection.execute("""
                    MATCH (f:File)
                    WHERE f.path IN $paths
                    OPTIONAL MATCH (c:GitCommit)-[:COMMIT_MODIFIES]->(f)
                    WITH f, collect(c) AS commits
                    WHERE size(commits) > 0

                    UNWIND commits AS commit
                    OPTIONAL MATCH (commit)-[:AUTHORED_BY]->(a:Author)
                    WITH f, commits,
                         count(DISTINCT commit) AS commit_count,
                         count(DISTINCT a) AS author_count

                    WITH f, commit_count, author_count,
                         commit_count * (1.0 + log(author_count + 1)) AS base_importance

                    RETURN f.path AS path,
                           base_importance AS importance_score,
                           commit_count AS commits,
                           author_count AS authors
                """, {"paths": list(file_paths)})

                for record in results:
                    file_importance[record["path"]] = {
                        "importance_score": record["importance_score"] or 0,
                        "commits": record["commits"] or 0,
                        "authors": record["authors"] or 0,
                    }
            except Exception as e:
                log.debug(f"Failed to fetch file importance: {e}")

        # Fetch PageRank scores for entities
        pagerank_scores = {}
        if qualified_names:
            try:
                # Query functions
                func_results = self.connection.execute("""
                    MATCH (f:Function)
                    WHERE f.qualified_name IN $names
                    RETURN f.qualified_name AS name, f.pagerank AS pagerank
                """, {"names": list(qualified_names)})

                for record in func_results:
                    if record.get("pagerank"):
                        pagerank_scores[record["name"]] = record["pagerank"]

                # Query classes
                class_results = self.connection.execute("""
                    MATCH (c:Class)
                    WHERE c.qualified_name IN $names
                    RETURN c.qualified_name AS name, c.pagerank AS pagerank
                """, {"names": list(qualified_names)})

                for record in class_results:
                    if record.get("pagerank"):
                        pagerank_scores[record["name"]] = record["pagerank"]
            except Exception as e:
                log.debug(f"Failed to fetch PageRank scores: {e}")

        # Enrich candidates
        for c in candidates:
            file_path = c.get("file_path", "")
            qualified_name = c.get("qualified_name", "")

            # Add file importance
            if file_path in file_importance:
                fi = file_importance[file_path]
                c["importance_score"] = fi["importance_score"]
                c["file_commits"] = fi["commits"]
                c["file_authors"] = fi["authors"]
            else:
                c["importance_score"] = 0
                c["file_commits"] = 0
                c["file_authors"] = 0

            # Add PageRank
            c["pagerank_score"] = pagerank_scores.get(qualified_name, 0)

        return candidates

    def _compute_combined_scores(
        self,
        candidates: list[dict],
        semantic_weight: float,
        importance_weight: float,
        pagerank_weight: float,
    ) -> list[dict]:
        """Compute combined scores for candidates.

        Normalizes each score type and combines them with weights.

        Args:
            candidates: Enriched candidates
            semantic_weight: Weight for semantic score
            importance_weight: Weight for importance score
            pagerank_weight: Weight for PageRank score

        Returns:
            Candidates with combined_score added
        """
        if not candidates:
            return candidates

        # Find max values for normalization
        max_semantic = max(c.get("score", 0) for c in candidates) or 1
        max_importance = max(c.get("importance_score", 0) for c in candidates) or 1
        max_pagerank = max(c.get("pagerank_score", 0) for c in candidates) or 1

        for c in candidates:
            # Normalize to 0-1
            norm_semantic = c.get("score", 0) / max_semantic
            norm_importance = c.get("importance_score", 0) / max_importance
            norm_pagerank = c.get("pagerank_score", 0) / max_pagerank

            # Compute combined score
            c["combined_score"] = (
                norm_semantic * semantic_weight +
                norm_importance * importance_weight +
                norm_pagerank * pagerank_weight
            )

            # Store normalized scores for debugging
            c["norm_semantic"] = round(norm_semantic, 3)
            c["norm_importance"] = round(norm_importance, 3)
            c["norm_pagerank"] = round(norm_pagerank, 3)

        return candidates
