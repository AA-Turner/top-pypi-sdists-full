"""Analytics engine for computing graph metrics."""

import os
import networkx as nx
from typing import Dict, List, Tuple, Optional, Iterable
from datetime import datetime, timedelta
from collections import defaultdict
import math
import community as community_louvain  # python-louvain

from ..graph.connection import KuzuConnection, get_connection, get_read_connection, write_lock_context
from ..agent.providers import get_provider
from ..agent.providers.factory import DEFAULT_MODEL
from ..utils.logger import log


class AnalyticsEngine:
    """Computes graph analytics metrics on the knowledge graph."""

    def __init__(self, connection: KuzuConnection = None, read_only: bool = True):
        """Initialize analytics engine.

        Args:
            connection: Kuzu connection. If None, uses appropriate global connection.
            read_only: If True and no connection provided, use read-only connection.
        """
        if connection:
            self.connection = connection
        elif read_only:
            self.connection = get_read_connection()
        else:
            self.connection = get_connection()

    def compute_pagerank(
        self,
        damping: float = 0.85,
        max_iter: int = 100,
        write_back: bool = True,
        use_ast_nodes: bool = False
    ) -> Dict[str, float]:
        """Compute PageRank scores for all code entities.

        PageRank identifies the most "important" entities based on
        how many other entities reference/call them.

        Args:
            damping: Damping parameter (default 0.85)
            max_iter: Maximum iterations
            write_back: Whether to write scores back to database
            use_ast_nodes: If True, use ASTNodes (legacy). If False (default),
                          use Function/Class nodes with CALLS relationships.

        Returns:
            Dictionary mapping entity qualified_name to PageRank score
        """
        log.info(f"Computing PageRank scores (use_ast_nodes={use_ast_nodes})...")

        # Build NetworkX graph from Kuzu
        graph = self._build_code_graph(use_ast_nodes=use_ast_nodes)

        if len(graph.nodes) == 0:
            log.warning("Graph is empty, cannot compute PageRank")
            return {}

        # Compute PageRank
        pagerank_scores = nx.pagerank(
            graph,
            alpha=damping,
            max_iter=max_iter
        )

        log.info(f"Computed PageRank for {len(pagerank_scores)} entities")

        # Write back to database
        if write_back:
            self._write_pagerank_scores(pagerank_scores, use_ast_nodes=use_ast_nodes)

        return pagerank_scores

    def compute_betweenness_centrality(
        self,
        normalized: bool = True,
        write_back: bool = True
    ) -> Dict[str, float]:
        """Compute Betweenness Centrality for all code entities.

        Betweenness identifies "bridge" entities that connect different
        parts of the codebase.

        Args:
            normalized: Whether to normalize scores
            write_back: Whether to write scores back to database

        Returns:
            Dictionary mapping entity qualified_name to betweenness score
        """
        log.info("Computing Betweenness Centrality...")

        # Build NetworkX graph from Kuzu
        graph = self._build_code_graph()

        if len(graph.nodes) == 0:
            log.warning("Graph is empty, cannot compute Betweenness")
            return {}

        # Compute Betweenness Centrality
        betweenness_scores = nx.betweenness_centrality(
            graph,
            normalized=normalized
        )

        log.info(f"Computed Betweenness for {len(betweenness_scores)} entities")

        # Write back to database
        if write_back:
            self._write_betweenness_scores(betweenness_scores)

        return betweenness_scores

    def detect_communities(
        self,
        resolution: float = 1.0,
        write_back: bool = True,
        describe: bool = False,
        describe_model: str = DEFAULT_MODEL,
        overwrite_descriptions: bool = False,
    ) -> Dict[str, int]:
        """Detect communities/clusters using Louvain algorithm.

        Identifies modules or clusters of tightly-coupled code entities.

        Args:
            resolution: Resolution parameter for Louvain algorithm
            write_back: Whether to write community IDs back to database
            describe: Whether to auto-generate community descriptions via LLM
            describe_model: LLM model to use for descriptions
            overwrite_descriptions: Whether to overwrite existing descriptions

        Returns:
            Dictionary mapping entity qualified_name to community ID
        """
        log.info("Detecting communities with Louvain algorithm...")

        # Build NetworkX graph from Kuzu (undirected for community detection)
        graph = self._build_code_graph(directed=False)

        if len(graph.nodes) == 0:
            log.warning("Graph is empty, cannot detect communities")
            return {}

        # Compute communities using Louvain
        communities = community_louvain.best_partition(
            graph,
            resolution=resolution
        )

        # Count communities
        num_communities = len(set(communities.values()))
        log.info(f"Detected {num_communities} communities")

        # Write back to database
        if write_back:
            self._write_community_assignments(communities)
            self._ensure_community_nodes(set(communities.values()))
            if describe:
                self.generate_community_descriptions(
                    community_ids=set(communities.values()),
                    model=describe_model,
                    overwrite=overwrite_descriptions,
                )

        return communities

    def get_top_pagerank(
        self,
        limit: int = 20,
        use_ast_nodes: bool = False
    ) -> List[Tuple[str, str, float]]:
        """Get top entities by PageRank score.

        Args:
            limit: Number of results to return
            use_ast_nodes: If True, query ASTNodes. If False, query Class/Function.

        Returns:
            List of (qualified_name, entity_type, score) tuples
        """
        if use_ast_nodes:
            results = self.connection.execute("""
                MATCH (n:ASTNode)
                WHERE n.pagerank IS NOT NULL
                RETURN n.id AS name,
                       n.ast_type AS type,
                       n.pagerank AS score
                ORDER BY n.pagerank DESC
                LIMIT $limit
            """, {"limit": limit})
        else:
            # Query functions and classes separately, then merge
            func_results = self.connection.execute("""
                MATCH (n:Function)
                WHERE n.pagerank IS NOT NULL
                RETURN n.qualified_name AS name,
                       'Function' AS type,
                       n.pagerank AS score
                ORDER BY n.pagerank DESC
                LIMIT $limit
            """, {"limit": limit})

            class_results = self.connection.execute("""
                MATCH (n:Class)
                WHERE n.pagerank IS NOT NULL
                RETURN n.qualified_name AS name,
                       'Class' AS type,
                       n.pagerank AS score
                ORDER BY n.pagerank DESC
                LIMIT $limit
            """, {"limit": limit})

            results = func_results + class_results
            results.sort(key=lambda x: x['score'], reverse=True)
            results = results[:limit]

        return [(r["name"], r["type"], r["score"]) for r in results]

    def get_top_betweenness(self, limit: int = 20) -> List[Tuple[str, str, float]]:
        """Get top entities by Betweenness Centrality.

        Args:
            limit: Number of results to return

        Returns:
            List of (qualified_name, entity_type, score) tuples
        """
        # Query functions and classes separately
        func_results = self.connection.execute("""
            MATCH (n:Function)
            WHERE n.betweenness IS NOT NULL
            RETURN n.qualified_name AS name,
                   'Function' AS type,
                   n.betweenness AS score
            ORDER BY n.betweenness DESC
            LIMIT $limit
        """, {"limit": limit})

        class_results = self.connection.execute("""
            MATCH (n:Class)
            WHERE n.betweenness IS NOT NULL
            RETURN n.qualified_name AS name,
                   'Class' AS type,
                   n.betweenness AS score
            ORDER BY n.betweenness DESC
            LIMIT $limit
        """, {"limit": limit})

        results = func_results + class_results
        results.sort(key=lambda x: x['score'], reverse=True)
        return [(r["name"], r["type"], r["score"]) for r in results[:limit]]

    def get_communities_summary(self, max_members: int = 5) -> List[Dict]:
        """Get summary of detected communities.

        Args:
            max_members: Maximum number of member names to return per community

        Returns:
            List of community summaries with member counts
        """
        descriptions = self._fetch_community_descriptions()

        # Query functions and classes with community assignments
        func_results = self.connection.execute("""
            MATCH (n:Function)
            WHERE n.community IS NOT NULL
            RETURN n.community AS community_id,
                   n.qualified_name AS qualified_name
        """)

        class_results = self.connection.execute("""
            MATCH (n:Class)
            WHERE n.community IS NOT NULL
            RETURN n.community AS community_id,
                   n.qualified_name AS qualified_name
        """)

        # Group by community
        communities = defaultdict(list)
        for r in func_results + class_results:
            communities[r['community_id']].append(r['qualified_name'])

        # Build summary
        summaries = []
        for community_id, members in communities.items():
            summaries.append({
                'community_id': community_id,
                'member_count': len(members),
                'sample_members': members[:max_members],
                'description': descriptions.get(community_id)
            })

        summaries.sort(key=lambda x: x['member_count'], reverse=True)
        return summaries

    def get_community_members(self, community_id: int) -> List[Dict]:
        """Get all members of a specific community.

        Args:
            community_id: The community ID to query

        Returns:
            List of member details (name, type, qualified_name)
        """
        func_results = self.connection.execute("""
            MATCH (n:Function)
            WHERE n.community = $community_id
            RETURN n.name AS name,
                   'Function' AS type,
                   n.qualified_name AS qualified_name,
                   n.file_path AS file_path
            ORDER BY n.name
        """, {"community_id": community_id})

        class_results = self.connection.execute("""
            MATCH (n:Class)
            WHERE n.community = $community_id
            RETURN n.name AS name,
                   'Class' AS type,
                   n.qualified_name AS qualified_name,
                   n.file_path AS file_path
            ORDER BY n.name
        """, {"community_id": community_id})

        return func_results + class_results

    def search_communities(
        self,
        query: Optional[str] = None,
        qualified_names: Optional[List[str]] = None,
        limit: int = 10,
        max_members: int = 5,
        min_score: float = 0.3,
    ) -> List[Dict]:
        """Search for communities by semantic similarity or member matching.

        Two search modes:
        1. Query mode: Search community descriptions by embedding similarity
        2. Member mode: Find communities containing specific code entities

        Args:
            query: Semantic search query for community descriptions
            qualified_names: List of code entity qualified names to find communities for
            limit: Maximum number of communities to return
            max_members: Maximum sample members per community
            min_score: Minimum similarity score for semantic search (0-1)

        Returns:
            List of community dicts with community_id, description, member_count, sample_members
        """
        if query:
            # Semantic search mode - search by community description embedding
            return self._search_communities_by_embedding(
                query=query,
                limit=limit,
                max_members=max_members,
                min_score=min_score,
            )
        elif qualified_names:
            # Member matching mode - find communities containing these entities
            return self._search_communities_by_members(
                qualified_names=qualified_names,
                limit=limit,
                max_members=max_members,
            )
        else:
            # No search criteria - return top communities by size
            return self.get_communities_summary(max_members=max_members)[:limit]

    def _search_communities_by_embedding(
        self,
        query: str,
        limit: int = 10,
        max_members: int = 5,
        min_score: float = 0.3,
    ) -> List[Dict]:
        """Search communities by embedding similarity on descriptions."""
        from ..embeddings.service import EmbeddingService
        from ..planning.similarity import cosine_similarity

        embedding_service = EmbeddingService()
        if not embedding_service.is_available:
            log.warning("Embedding service not available. Falling back to text search.")
            return self._fallback_community_text_search(query, limit, max_members)

        # Generate query embedding
        query_embedding = embedding_service.embed_query(query)
        if not query_embedding:
            log.error("Failed to generate query embedding")
            return []

        # Fetch all communities with embeddings
        communities = self.connection.execute("""
            MATCH (c:Community)
            WHERE c.embedding IS NOT NULL
            RETURN c.community_id AS community_id,
                   c.description AS description,
                   c.embedding AS embedding
        """)

        if not communities:
            log.warning("No communities with embeddings found. Run `emdash embed index` first.")
            return self._fallback_community_text_search(query, limit, max_members)

        # Compute similarity scores
        scored_communities = []
        for comm in communities:
            if comm.get('embedding'):
                similarity = cosine_similarity(query_embedding, comm['embedding'])
                if similarity >= min_score:
                    scored_communities.append({
                        'community_id': comm['community_id'],
                        'description': comm['description'],
                        'score': similarity,
                    })

        # Sort by score
        scored_communities.sort(key=lambda x: x['score'], reverse=True)
        scored_communities = scored_communities[:limit]

        # Enrich with member info
        for comm in scored_communities:
            members = self.get_community_members(comm['community_id'])
            comm['member_count'] = len(members)
            comm['sample_members'] = [m['qualified_name'] for m in members[:max_members]]

        return scored_communities

    def _search_communities_by_members(
        self,
        qualified_names: List[str],
        limit: int = 10,
        max_members: int = 5,
    ) -> List[Dict]:
        """Find communities containing the given code entities."""
        if not qualified_names:
            return []

        # Get community IDs for the given entities
        func_results = self.connection.execute("""
            MATCH (f:Function)
            WHERE f.qualified_name IN $names AND f.community IS NOT NULL
            RETURN f.community AS community_id, count(*) AS match_count
        """, {"names": qualified_names})

        class_results = self.connection.execute("""
            MATCH (c:Class)
            WHERE c.qualified_name IN $names AND c.community IS NOT NULL
            RETURN c.community AS community_id, count(*) AS match_count
        """, {"names": qualified_names})

        # Aggregate by community
        community_matches = {}
        for r in func_results + class_results:
            cid = r['community_id']
            community_matches[cid] = community_matches.get(cid, 0) + r['match_count']

        if not community_matches:
            return []

        # Sort by match count and fetch details
        sorted_ids = sorted(
            community_matches.keys(),
            key=lambda x: community_matches[x],
            reverse=True
        )[:limit]

        descriptions = self._fetch_community_descriptions()
        results = []
        for cid in sorted_ids:
            members = self.get_community_members(cid)
            results.append({
                'community_id': cid,
                'description': descriptions.get(cid),
                'member_count': len(members),
                'sample_members': [m['qualified_name'] for m in members[:max_members]],
                'match_count': community_matches[cid],
            })

        return results

    def _fallback_community_text_search(
        self,
        query: str,
        limit: int = 10,
        max_members: int = 5,
    ) -> List[Dict]:
        """Fallback to text-based community search."""
        results = self.connection.execute("""
            MATCH (c:Community)
            WHERE c.description IS NOT NULL
            AND lower(c.description) CONTAINS lower($query)
            RETURN c.community_id AS community_id,
                   c.description AS description
            LIMIT $limit
        """, {"query": query, "limit": limit})

        # Enrich with member info
        for comm in results:
            members = self.get_community_members(comm['community_id'])
            comm['member_count'] = len(members)
            comm['sample_members'] = [m['qualified_name'] for m in members[:max_members]]

        return results

    def get_community_description(self, community_id: int) -> Optional[str]:
        """Get a stored description for a community."""
        results = self.connection.execute("""
            MATCH (c:Community {community_id: $community_id})
            RETURN c.description AS description
        """, {"community_id": community_id})
        if not results:
            return None
        return results[0].get("description")

    def set_community_description(self, community_id: int, description: str, source: str = "manual") -> None:
        """Set or update the description for a community."""
        if description is None:
            return

        cleaned = description.strip()
        if not cleaned:
            return

        write_conn = get_connection()
        with write_lock_context("community_description"):
            write_conn.execute_write("""
                MERGE (c:Community {community_id: $community_id})
                SET c.description = $description,
                    c.source = $source
            """, {"community_id": community_id, "description": cleaned, "source": source})

    def generate_community_descriptions(
        self,
        community_ids: Optional[Iterable[int]] = None,
        model: str = DEFAULT_MODEL,
        overwrite: bool = False,
        max_members: int = 20,
        progress_callback: Optional[callable] = None,
        max_workers: int = 10,
    ) -> Dict[int, str]:
        """Generate and store LLM descriptions for communities.

        Args:
            community_ids: Specific community IDs to describe. If None, uses all.
            model: LLM model to use for generation.
            overwrite: Whether to overwrite existing descriptions.
            max_members: Max members to include in the prompt.
            progress_callback: Optional callback(current, total, community_id, description)
                              called after each community is processed.
            max_workers: Maximum parallel LLM requests (default 10).
        """
        import threading
        from concurrent.futures import ThreadPoolExecutor, as_completed

        if community_ids is None:
            community_ids = self._get_community_ids()

        community_ids = list(community_ids)
        if not community_ids:
            return {}

        existing = self._fetch_community_descriptions()
        if not overwrite:
            community_ids = [cid for cid in community_ids if not existing.get(cid)]

        if not community_ids:
            return {}

        try:
            provider = get_provider(model)
        except Exception as e:
            log.warning(f"LLM provider not available for community descriptions: {e}")
            return {}

        generated = {}
        total = len(community_ids)
        completed = [0]  # Use list for mutable counter in closure
        lock = threading.Lock()

        def process_community(community_id: int) -> tuple[int, Optional[str]]:
            """Process a single community - returns (community_id, description or None)."""
            prompt = self._build_community_description_prompt(community_id, max_members=max_members)
            if not prompt:
                return (community_id, None)

            try:
                response = provider.chat(
                    messages=[{"role": "user", "content": prompt}],
                    system=(
                        "You are a senior engineer summarizing a code community. "
                        "Write 1-2 concise sentences describing what the community does. "
                        "Use plain text only. No bullets, no prefixes, no quotes."
                    ),
                )
            except Exception as e:
                log.warning(f"Failed to generate description for community {community_id}: {e}")
                return (community_id, None)

            description = self._clean_description(response.content or "")
            if not description:
                return (community_id, None)

            if len(description) > 400:
                description = description[:397].rstrip() + "..."

            return (community_id, description)

        log.info(f"Generating descriptions for {total} communities with {max_workers} workers...")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_community, cid): cid for cid in community_ids}

            for future in as_completed(futures):
                community_id, description = future.result()

                with lock:
                    completed[0] += 1
                    current = completed[0]

                if description:
                    self.set_community_description(community_id, description, source="llm")
                    generated[community_id] = description

                if progress_callback:
                    progress_callback(current, total, community_id, description)

        log.info(f"Generated {len(generated)} community descriptions")
        return generated

    def _fetch_community_descriptions(self) -> Dict[int, Optional[str]]:
        """Fetch all stored community descriptions."""
        results = self.connection.execute("""
            MATCH (c:Community)
            RETURN c.community_id AS community_id,
                   c.description AS description
        """)
        return {row["community_id"]: row.get("description") for row in results}

    def detect_knowledge_silos(
        self,
        importance_threshold: float = 0.0001,
        max_authors: int = 2
    ) -> List[Dict]:
        """Detect knowledge silos - critical code with few maintainers.

        A knowledge silo is important code (high PageRank) that only
        1-2 people have worked on, creating a "bus factor" risk.

        Args:
            importance_threshold: Minimum PageRank score to consider
            max_authors: Maximum author count to flag as silo

        Returns:
            List of knowledge silos with risk scores
        """
        log.info("Detecting knowledge silos...")

        try:
            results = self.connection.execute("""
                MATCH (f:File)-[:CONTAINS_FUNCTION|CONTAINS_CLASS]->(entity)
                WHERE entity.pagerank IS NOT NULL
                AND entity.pagerank >= $importance_threshold
                WITH f, max(entity.pagerank) AS importance,
                     collect(entity.qualified_name)[0] AS top_entity

                MATCH (c:GitCommit)-[:COMMIT_MODIFIES]->(f)
                WITH f, importance, top_entity,
                     collect(DISTINCT c.author_email) AS authors
                WHERE size(authors) <= $max_authors

                WITH f, importance, top_entity, authors,
                     importance / size(authors) AS risk_score

                RETURN f.path AS file_path,
                       top_entity AS critical_entity,
                       importance,
                       size(authors) AS author_count,
                       authors,
                       risk_score
                ORDER BY risk_score DESC
            """, {
                "importance_threshold": importance_threshold,
                "max_authors": max_authors
            })

            silos = []
            for record in results:
                silos.append({
                    'file_path': record['file_path'],
                    'critical_entity': record['critical_entity'],
                    'importance': record['importance'],
                    'author_count': record['author_count'],
                    'authors': record['authors'],
                    'risk_score': record['risk_score']
                })

            log.info(f"Found {len(silos)} knowledge silos")
            return silos
        except Exception as e:
            log.warning(f"Failed to detect knowledge silos: {e}")
            return []

    def get_file_ownership(self, file_path: str) -> Dict:
        """Get detailed ownership information for a file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with ownership statistics
        """
        results = self.connection.execute("""
            MATCH (f:File {path: $file_path})
            OPTIONAL MATCH (c:GitCommit)-[:COMMIT_MODIFIES]->(f)
            OPTIONAL MATCH (c)-[:AUTHORED_BY]->(a:Author)

            WITH f,
                 count(DISTINCT c) AS total_commits,
                 collect(DISTINCT a.email) AS authors,
                 collect(DISTINCT a.name) AS author_names

            RETURN f.path AS file_path,
                   total_commits,
                   size(authors) AS author_count,
                   authors,
                   author_names
        """, {"file_path": file_path})

        if not results:
            return {}

        record = results[0]
        return {
            'file_path': record['file_path'],
            'total_commits': record['total_commits'],
            'author_count': record['author_count'],
            'authors': record['authors'],
            'author_names': record['author_names']
        }

    def compute_commit_importance(
        self,
        write_back: bool = True
    ) -> Dict[str, Dict]:
        """Compute file importance based on commit activity.

        Files with more commits and more authors are considered more
        important as they are actively maintained and have broader ownership.

        Args:
            write_back: Whether to write scores back to database

        Returns:
            Dictionary mapping file path to importance metrics
        """
        log.info("Computing commit-based importance...")

        results = self.connection.execute("""
            MATCH (f:File)
            OPTIONAL MATCH (c:GitCommit)-[:COMMIT_MODIFIES]->(f)
            WITH f, count(DISTINCT c) AS commit_count
            OPTIONAL MATCH (c2:GitCommit)-[:COMMIT_MODIFIES]->(f)
            OPTIONAL MATCH (c2)-[:AUTHORED_BY]->(a:Author)
            WITH f, commit_count,
                 count(DISTINCT a) AS author_count,
                 collect(DISTINCT a.email)[0:5] AS top_authors
            WHERE commit_count > 0
            RETURN f.path AS file_path,
                   commit_count,
                   author_count,
                   top_authors,
                   commit_count * (1.0 + log(author_count + 1)) AS importance_score
            ORDER BY importance_score DESC
        """)

        importance = {}
        for record in results:
            importance[record['file_path']] = {
                'commit_count': record['commit_count'],
                'author_count': record['author_count'],
                'top_authors': record['top_authors'],
                'importance_score': record['importance_score']
            }

        log.info(f"Computed importance for {len(importance)} files")

        if write_back:
            self._write_commit_importance(importance)

        return importance

    def _write_commit_importance(self, importance: Dict[str, Dict]):
        """Write commit-based importance scores to database.

        Args:
            importance: Dictionary mapping file path to importance metrics
        """
        log.info("Writing commit importance scores to database...")
        write_conn = get_connection()

        with write_lock_context("commit_importance"):
            for path, data in importance.items():
                write_conn.execute_write("""
                    MATCH (f:File {path: $path})
                    SET f.commit_importance = $importance_score,
                        f.commit_count = $commit_count,
                        f.author_count = $author_count
                """, {
                    "path": path,
                    "importance_score": data['importance_score'],
                    "commit_count": data['commit_count'],
                    "author_count": data['author_count']
                })

        log.info(f"Wrote {len(importance)} commit importance scores")

    def get_top_commit_importance(
        self,
        limit: int = 20
    ) -> List[Tuple[str, int, int, float]]:
        """Get top files by commit-based importance.

        Args:
            limit: Number of results to return

        Returns:
            List of (file_path, commit_count, author_count, importance_score) tuples
        """
        results = self.connection.execute("""
            MATCH (f:File)
            WHERE f.commit_importance IS NOT NULL
            RETURN f.path AS file_path,
                   f.commit_count AS commits,
                   f.author_count AS authors,
                   f.commit_importance AS score
            ORDER BY f.commit_importance DESC
            LIMIT $limit
        """, {"limit": limit})

        return [(r["file_path"], r["commits"], r["authors"], r["score"])
                for r in results]

    def compute_file_importance(
        self,
        days: int = 30,
        limit: int = 50
    ) -> List[Dict]:
        """Compute file importance with recency weighting.

        Args:
            days: Time window in days for recency scoring
            limit: Maximum number of files to return

        Returns:
            List of dicts with file importance metrics
        """
        log.info(f"Computing file importance with {days}-day recency window...")

        try:
            results = self.connection.execute("""
                MATCH (f:File)
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

                RETURN f.path AS file_path,
                       commit_count AS commits,
                       author_count AS authors,
                       base_importance AS importance_score
                ORDER BY importance_score DESC
                LIMIT $limit
            """, {"limit": limit})

            files = []
            for record in results:
                files.append({
                    'file_path': record['file_path'],
                    'commits': record['commits'],
                    'authors': record['authors'],
                    'recent_commits': 0,  # Simplified - recency calculation complex in Kuzu
                    'importance_score': record['importance_score']
                })

            log.info(f"Computed importance for {len(files)} files")
            return files
        except Exception as e:
            log.warning(f"Failed to compute file importance: {e}")
            return []

    def compute_area_importance(
        self,
        depth: int = 2,
        days: int = 30,
        limit: int = 20
    ) -> List[Dict]:
        """Aggregate file importance by directory.

        Args:
            depth: Directory depth for grouping
            days: Time window for recency scoring
            limit: Maximum number of areas to return

        Returns:
            List of dicts with area importance metrics
        """
        log.info(f"Computing area importance at depth {depth}...")

        # Get file importance first
        files = self.compute_file_importance(days=days, limit=500)
        if not files:
            return []

        # Find common prefix (repo root) to make paths relative
        all_paths = [f['file_path'] for f in files]
        if all_paths:
            common = os.path.commonpath(all_paths)
            if not os.path.isdir(common):
                common = os.path.dirname(common)
            repo_root = common.rstrip('/') + '/'
        else:
            repo_root = '/'

        # Group by directory
        areas = defaultdict(lambda: {
            'files': [],
            'total_commits': 0,
            'importance_sum': 0.0,
            'max_authors': 0,
            'recent_commits': 0,
        })

        total_recent = sum(f.get('recent_commits', 0) for f in files)

        for f in files:
            abs_path = f['file_path']

            if abs_path.startswith(repo_root):
                rel_path = abs_path[len(repo_root):]
            else:
                rel_path = abs_path

            parts = rel_path.split('/')

            if len(parts) > depth:
                rel_area = '/'.join(parts[:depth]) + '/'
            else:
                rel_area = '/'.join(parts[:-1]) + '/' if len(parts) > 1 else '/'

            areas[rel_area]['files'].append(f)
            areas[rel_area]['total_commits'] += f['commits']
            areas[rel_area]['importance_sum'] += f['importance_score']
            # Track max authors seen in any file (approximation for unique authors)
            areas[rel_area]['max_authors'] = max(
                areas[rel_area]['max_authors'],
                f.get('authors', 0)
            )
            areas[rel_area]['recent_commits'] += f.get('recent_commits', 0)

        # Build result list
        result_list = []
        for rel_area, data in areas.items():
            recent = data['recent_commits']
            focus_pct = round(100 * recent / total_recent, 1) if total_recent > 0 else 0.0
            result_list.append({
                'path': rel_area,
                'total_commits': data['total_commits'],
                'file_count': len(data['files']),
                'importance': data['importance_sum'],
                'unique_authors': data['max_authors'],
                'recent_commits': recent,
                'focus_pct': focus_pct,
            })

        result_list.sort(key=lambda x: x['importance'], reverse=True)
        log.info(f"Computed importance for {len(result_list)} areas")
        return result_list[:limit]

    def _build_code_graph(
        self,
        directed: bool = True,
        use_ast_nodes: bool = False
    ) -> nx.Graph:
        """Build NetworkX graph from Kuzu code entities.

        Args:
            directed: Whether to create a directed graph
            use_ast_nodes: If True, use ASTNodes with CALLS/USES relationships

        Returns:
            NetworkX graph
        """
        log.info(f"Building {'directed' if directed else 'undirected'} graph from Kuzu...")

        graph = nx.DiGraph() if directed else nx.Graph()

        if use_ast_nodes:
            # Use ASTNodes
            nodes = self.connection.execute("""
                MATCH (n:ASTNode)
                WHERE n.id IS NOT NULL
                AND NOT n.file_path CONTAINS 'venv/'
                AND NOT n.file_path CONTAINS 'node_modules/'
                RETURN n.id AS name, n.ast_type AS type
            """)

            for record in nodes:
                graph.add_node(record["name"], entity_type=record["type"])

            # Get edges (this might need adjustment based on actual schema)
            edges = self.connection.execute("""
                MATCH (a:ASTNode)-[r:CALLS]->(b:ASTNode)
                WHERE a.id IS NOT NULL AND b.id IS NOT NULL
                RETURN a.id AS source, b.id AS target, 'CALLS' AS rel_type
            """)

            for record in edges:
                if record["source"] != record["target"]:
                    graph.add_edge(
                        record["source"],
                        record["target"],
                        relationship=record["rel_type"]
                    )
        else:
            # Use Function/Class nodes
            func_nodes = self.connection.execute("""
                MATCH (n:Function)
                RETURN n.qualified_name AS name, 'Function' AS type
            """)

            class_nodes = self.connection.execute("""
                MATCH (n:Class)
                RETURN n.qualified_name AS name, 'Class' AS type
            """)

            for record in func_nodes + class_nodes:
                graph.add_node(record["name"], entity_type=record["type"])

            # Get CALLS relationships
            call_edges = self.connection.execute("""
                MATCH (a:Function)-[:CALLS]->(b:Function)
                RETURN a.qualified_name AS source,
                       b.qualified_name AS target,
                       'CALLS' AS rel_type
            """)

            for record in call_edges:
                graph.add_edge(
                    record["source"],
                    record["target"],
                    relationship=record["rel_type"]
                )

            # Get INHERITS_FROM relationships
            inherit_edges = self.connection.execute("""
                MATCH (a:Class)-[:INHERITS_FROM]->(b:Class)
                RETURN a.qualified_name AS source,
                       b.qualified_name AS target,
                       'INHERITS_FROM' AS rel_type
            """)

            for record in inherit_edges:
                graph.add_edge(
                    record["source"],
                    record["target"],
                    relationship=record["rel_type"]
                )

        log.info(f"Built graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
        return graph

    def _write_pagerank_scores(
        self,
        scores: Dict[str, float],
        use_ast_nodes: bool = False
    ):
        """Write PageRank scores back to database.

        Args:
            scores: Dictionary mapping qualified_name to PageRank score
            use_ast_nodes: Whether scores are for ASTNodes
        """
        log.info("Writing PageRank scores to database...")
        write_conn = get_connection()

        with write_lock_context("pagerank"):
            for name, value in scores.items():
                if use_ast_nodes:
                    write_conn.execute_write("""
                        MATCH (n:ASTNode {id: $name})
                        SET n.pagerank = $value
                    """, {"name": name, "value": value})
                else:
                    # Try Function first, then Class
                    write_conn.execute_write("""
                        MATCH (n:Function {qualified_name: $name})
                        SET n.pagerank = $value
                    """, {"name": name, "value": value})
                    write_conn.execute_write("""
                        MATCH (n:Class {qualified_name: $name})
                        SET n.pagerank = $value
                    """, {"name": name, "value": value})

        log.info(f"Wrote {len(scores)} PageRank scores")

    def _write_betweenness_scores(self, scores: Dict[str, float]):
        """Write Betweenness Centrality scores back to database.

        Args:
            scores: Dictionary mapping qualified_name to betweenness score
        """
        log.info("Writing Betweenness scores to database...")
        write_conn = get_connection()

        with write_lock_context("betweenness"):
            for name, value in scores.items():
                write_conn.execute_write("""
                    MATCH (n:Function {qualified_name: $name})
                    SET n.betweenness = $value
                """, {"name": name, "value": value})
                write_conn.execute_write("""
                    MATCH (n:Class {qualified_name: $name})
                    SET n.betweenness = $value
                """, {"name": name, "value": value})

        log.info(f"Wrote {len(scores)} Betweenness scores")

    def _write_community_assignments(self, communities: Dict[str, int]):
        """Write community assignments back to database.

        Args:
            communities: Dictionary mapping qualified_name to community ID
        """
        log.info("Writing community assignments to database...")

        rows = [{"name": name, "community_id": comm_id} for name, comm_id in communities.items()]
        if not rows:
            log.info("No community assignments to write")
            return

        write_conn = get_connection()
        with write_lock_context("communities"):
            write_conn.execute_write("""
                UNWIND $rows AS row
                MATCH (n:Function {qualified_name: row.name})
                SET n.community = row.community_id
            """, {"rows": rows})
            write_conn.execute_write("""
                UNWIND $rows AS row
                MATCH (n:Class {qualified_name: row.name})
                SET n.community = row.community_id
            """, {"rows": rows})

        log.info(f"Wrote {len(communities)} community assignments")

    def _ensure_community_nodes(self, community_ids: Iterable[int]) -> None:
        """Ensure community nodes exist for detected community IDs."""
        rows = [{"community_id": community_id} for community_id in community_ids]
        if not rows:
            return

        write_conn = get_connection()
        with write_lock_context("community_nodes"):
            write_conn.execute_write("""
                UNWIND $rows AS row
                MERGE (c:Community {community_id: row.community_id})
            """, {"rows": rows})

    def _get_community_ids(self) -> List[int]:
        """Fetch distinct community IDs from the graph."""
        func_results = self.connection.execute("""
            MATCH (n:Function)
            WHERE n.community IS NOT NULL
            RETURN DISTINCT n.community AS community_id
        """)
        class_results = self.connection.execute("""
            MATCH (n:Class)
            WHERE n.community IS NOT NULL
            RETURN DISTINCT n.community AS community_id
        """)
        community_ids = {row["community_id"] for row in func_results + class_results}
        return sorted(community_ids)

    def _build_community_description_prompt(self, community_id: int, max_members: int = 20) -> str:
        """Build the LLM prompt for a community description."""
        func_results = self.connection.execute("""
            MATCH (n:Function)
            WHERE n.community = $community_id
            RETURN 'Function' AS type,
                   n.name AS name,
                   n.qualified_name AS qualified_name,
                   n.file_path AS file_path,
                   n.docstring AS docstring,
                   n.pagerank AS pagerank
            ORDER BY n.pagerank DESC, n.name
            LIMIT $limit
        """, {"community_id": community_id, "limit": max_members})
        class_results = self.connection.execute("""
            MATCH (n:Class)
            WHERE n.community = $community_id
            RETURN 'Class' AS type,
                   n.name AS name,
                   n.qualified_name AS qualified_name,
                   n.file_path AS file_path,
                   n.docstring AS docstring,
                   n.pagerank AS pagerank
            ORDER BY n.pagerank DESC, n.name
            LIMIT $limit
        """, {"community_id": community_id, "limit": max_members})
        results = func_results + class_results
        results.sort(key=lambda row: (row.get("pagerank") is None, -(row.get("pagerank") or 0), row.get("name") or ""))
        results = results[:max_members]

        if not results:
            return ""

        members = []
        file_paths = []
        seen_paths = set()

        for row in results:
            name = row.get("qualified_name") or row.get("name") or "unknown"
            mtype = row.get("type") or "Entity"
            docstring = (row.get("docstring") or "").strip()
            if docstring:
                docstring = " ".join(docstring.split())
                if len(docstring) > 160:
                    docstring = docstring[:157].rstrip() + "..."
                members.append(f"- {mtype}: {name} — {docstring}")
            else:
                members.append(f"- {mtype}: {name}")

            file_path = row.get("file_path")
            if file_path:
                short_path = self._shorten_path(file_path)
                if short_path not in seen_paths:
                    seen_paths.add(short_path)
                    file_paths.append(short_path)

        prompt_sections = [
            f"Community ID: {community_id}",
            "",
            "Key members:",
            *members,
        ]

        if file_paths:
            prompt_sections.extend([
                "",
                "Representative files:",
                *[f"- {p}" for p in file_paths[:15]],
            ])

        return "\n".join(prompt_sections)

    def _shorten_path(self, path: str, max_parts: int = 3) -> str:
        """Shorten a file path to the last few segments."""
        parts = path.replace("\\", "/").split("/")
        if len(parts) <= max_parts:
            return "/".join(parts)
        return "/".join(parts[-max_parts:])

    def _clean_description(self, description: str) -> str:
        """Normalize LLM output for storage."""
        cleaned_lines = [line.strip(" -\t") for line in description.splitlines() if line.strip()]
        cleaned = " ".join(cleaned_lines).strip()
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
            cleaned = cleaned[1:-1].strip()
        return cleaned
