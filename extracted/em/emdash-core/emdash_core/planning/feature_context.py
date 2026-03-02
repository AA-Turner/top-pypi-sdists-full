"""Feature context builder using semantic search and AST expansion."""

from dataclasses import dataclass, field
from typing import Optional

from ..graph.connection import KuzuConnection, get_connection
from .similarity import SimilaritySearch
from .feature_expander import FeatureExpander, FeatureGraph
from ..utils.logger import log


@dataclass
class FeatureContext:
    """Complete context for a feature query."""

    query: str
    root_node: dict = field(default_factory=dict)
    feature_graph: FeatureGraph = field(default_factory=FeatureGraph)
    similar_nodes: list[dict] = field(default_factory=list)
    related_prs: list[dict] = field(default_factory=list)
    authors: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "query": self.query,
            "root_node": self.root_node,
            "feature_graph": self.feature_graph.to_dict(),
            "similar_nodes": self.similar_nodes,
            "related_prs": self.related_prs,
            "authors": self.authors,
        }


class FeatureContextBuilder:
    """Builds complete feature context from a query."""

    def __init__(
        self,
        connection: Optional[KuzuConnection] = None,
        similarity_search: Optional[SimilaritySearch] = None,
        feature_expander: Optional[FeatureExpander] = None,
    ):
        """Initialize feature context builder.

        Args:
            connection: Neo4j connection. If None, uses global connection.
            similarity_search: Similarity search instance. If None, creates new one.
            feature_expander: Feature expander instance. If None, creates new one.
        """
        self.connection = connection or get_connection()
        self.similarity_search = similarity_search or SimilaritySearch(self.connection)
        self.expander = feature_expander or FeatureExpander(self.connection)

    def build_context(
        self,
        query: str,
        max_hops: int = 2,
        include_prs: bool = True,
        include_authors: bool = True,
        use_importance_ranking: bool = True,
    ) -> FeatureContext:
        """Build full feature context.

        1. Semantic search for most relevant node (optionally importance-weighted)
        2. Expand AST graph from that node
        3. Find related PRs and authors

        Args:
            query: Feature description to search for
            max_hops: Maximum relationship hops to traverse
            include_prs: Whether to include related PRs
            include_authors: Whether to include authors
            use_importance_ranking: If True, use importance-weighted search
                                   (combines semantic + activity + PageRank)

        Returns:
            FeatureContext with expanded AST graph
        """
        log.info(f"Building feature context for: {query}")

        # Step 1: Find most relevant node via semantic search
        if use_importance_ranking:
            log.info("Using importance-weighted search (semantic + activity + PageRank)")
            similar_code = self.similarity_search.importance_weighted_search(
                query, limit=5, min_score=0.3
            )
        else:
            similar_code = self.similarity_search.find_similar_code(
                query, limit=5, min_score=0.3
            )

        if not similar_code:
            log.warning("No relevant code found via semantic search, trying text search")
            # Fall back to text search
            similar_code = self._fallback_text_search(query)

        if not similar_code:
            log.warning("No relevant code found")
            return FeatureContext(query=query)

        root = similar_code[0]
        if use_importance_ranking and "combined_score" in root:
            log.info(
                f"Found root node: {root.get('type')} - {root.get('name')} "
                f"(combined: {root.get('combined_score', 0):.2f}, "
                f"semantic: {root.get('norm_semantic', 0):.2f}, "
                f"importance: {root.get('norm_importance', 0):.2f}, "
                f"pagerank: {root.get('norm_pagerank', 0):.2f})"
            )
        else:
            log.info(f"Found root node: {root.get('type')} - {root.get('name')} (score: {root.get('score', 'N/A')})")

        # Step 2: Expand AST graph based on node type
        node_type = root.get("type", "").lower()
        qualified_name = root.get("qualified_name", "")
        file_path = root.get("file_path", "")

        if node_type == "function":
            graph = self.expander.expand_from_function(qualified_name, max_hops)
        elif node_type == "class":
            graph = self.expander.expand_from_class(qualified_name, max_hops)
        else:
            graph = self.expander.expand_from_file(file_path, max_hops)

        # Update root node in graph
        graph.root_node = root

        log.info(f"Expanded graph: {len(graph.functions)} functions, {len(graph.classes)} classes")

        # Step 3: Enrich with PR/author data
        related_prs = []
        if include_prs:
            related_prs = self._find_related_prs(graph)

        authors = []
        if include_authors:
            authors = self._find_authors(graph)

        return FeatureContext(
            query=query,
            root_node=root,
            feature_graph=graph,
            similar_nodes=similar_code[1:],
            related_prs=related_prs,
            authors=authors,
        )

    def _fallback_text_search(self, query: str) -> list[dict]:
        """Fall back to text search when vector search unavailable."""
        with self.connection.session() as session:
            # Search functions by name or docstring
            result = session.run("""
                MATCH (f:Function)
                WHERE toLower(f.name) CONTAINS toLower($query)
                   OR toLower(f.docstring) CONTAINS toLower($query)
                RETURN 'Function' as type,
                       f.name as name,
                       f.qualified_name as qualified_name,
                       f.file_path as file_path,
                       f.docstring as docstring,
                       1.0 as score
                LIMIT 5
            """, query=query)

            results = [dict(r) for r in result]

            if not results:
                # Try class search
                result = session.run("""
                    MATCH (c:Class)
                    WHERE toLower(c.name) CONTAINS toLower($query)
                       OR toLower(c.docstring) CONTAINS toLower($query)
                    RETURN 'Class' as type,
                           c.name as name,
                           c.qualified_name as qualified_name,
                           c.file_path as file_path,
                           c.docstring as docstring,
                           1.0 as score
                    LIMIT 5
                """, query=query)
                results = [dict(r) for r in result]

            return results

    def _find_related_prs(self, graph: FeatureGraph) -> list[dict]:
        """Find PRs that modified files in the feature graph."""
        if not graph.files:
            return []

        file_paths = [f.get("path") for f in graph.files if f.get("path")]
        if not file_paths:
            return []

        with self.connection.session() as session:
            result = session.run("""
                UNWIND $file_paths as fp
                MATCH (pr:PullRequest)-[:PR_MODIFIES]->(f:File)
                WHERE f.path ENDS WITH fp OR f.path = fp
                RETURN DISTINCT pr.number as number,
                       pr.title as title,
                       pr.author as author,
                       pr.state as state,
                       count(DISTINCT f) as files_touched
                ORDER BY files_touched DESC
                LIMIT 5
            """, file_paths=file_paths)

            return [dict(r) for r in result]

    def _find_authors(self, graph: FeatureGraph) -> list[dict]:
        """Find authors who worked on files in the feature graph."""
        if not graph.files:
            return []

        file_paths = [f.get("path") for f in graph.files if f.get("path")]
        if not file_paths:
            return []

        with self.connection.session() as session:
            result = session.run("""
                UNWIND $file_paths as fp
                MATCH (a:Author)<-[:AUTHORED_BY]-(c:GitCommit)-[:COMMIT_MODIFIES]->(f:File)
                WHERE f.path ENDS WITH fp OR f.path = fp
                RETURN DISTINCT a.name as name,
                       a.email as email,
                       count(DISTINCT c) as commit_count
                ORDER BY commit_count DESC
                LIMIT 5
            """, file_paths=file_paths)

            return [dict(r) for r in result]
