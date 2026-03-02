"""Build comprehensive planning context for feature implementation."""

from dataclasses import dataclass, field
from typing import Optional

from ..graph.connection import KuzuConnection, get_connection
from .similarity import SimilaritySearch
from ..analytics.engine import AnalyticsEngine
from ..utils.logger import log


@dataclass
class PlanningContext:
    """Complete context for feature planning."""

    query: str
    similar_prs: list[dict] = field(default_factory=list)
    affected_communities: list[dict] = field(default_factory=list)
    key_entry_points: list[dict] = field(default_factory=list)
    domain_experts: list[dict] = field(default_factory=list)
    related_files: list[str] = field(default_factory=list)
    similar_code: list[dict] = field(default_factory=list)
    suggested_tasks: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "query": self.query,
            "similar_prs": self.similar_prs,
            "affected_communities": self.affected_communities,
            "key_entry_points": self.key_entry_points,
            "domain_experts": self.domain_experts,
            "related_files": self.related_files,
            "similar_code": self.similar_code,
            "suggested_tasks": self.suggested_tasks,
        }


class ContextBuilder:
    """Builds comprehensive planning context for features."""

    def __init__(
        self,
        connection: Optional[KuzuConnection] = None,
        similarity_search: Optional[SimilaritySearch] = None,
    ):
        """Initialize context builder.

        Args:
            connection: Neo4j connection. If None, uses global connection.
            similarity_search: Similarity search service.
        """
        self.connection = connection or get_connection()
        self.similarity = similarity_search or SimilaritySearch(self.connection)

    def build_context(
        self,
        feature_description: str,
        similar_pr_limit: int = 5,
        code_limit: int = 10,
        expert_limit: int = 5,
    ) -> PlanningContext:
        """Build complete planning context for a feature.

        Args:
            feature_description: Description of the feature to implement
            similar_pr_limit: Max number of similar PRs to include
            code_limit: Max number of similar code entities to include
            expert_limit: Max number of domain experts to include

        Returns:
            PlanningContext with all relevant information
        """
        log.info(f"Building planning context for: {feature_description}")

        context = PlanningContext(query=feature_description)

        # 1. Find similar PRs
        context.similar_prs = self.similarity.find_similar_prs(
            feature_description,
            limit=similar_pr_limit,
        )
        log.info(f"Found {len(context.similar_prs)} similar PRs")

        # 2. Find similar code
        context.similar_code = self.similarity.find_similar_code(
            feature_description,
            limit=code_limit,
        )
        log.info(f"Found {len(context.similar_code)} similar code entities")

        # 3. Collect related files from similar PRs and code
        related_files = set()
        for pr in context.similar_prs:
            if pr.get("files_changed"):
                related_files.update(pr["files_changed"])
        for code in context.similar_code:
            if code.get("file_path"):
                related_files.add(code["file_path"])
        context.related_files = list(related_files)

        # 4. Find affected communities
        if context.related_files:
            context.affected_communities = self._find_affected_communities(
                context.related_files
            )

        # 5. Find key entry points
        context.key_entry_points = self._find_entry_points(context.similar_prs)

        # 6. Find domain experts
        if context.related_files:
            context.domain_experts = self._find_domain_experts(
                context.related_files,
                limit=expert_limit,
            )

        # 7. Extract suggested tasks from similar PRs
        context.suggested_tasks = self._extract_tasks_from_prs(context.similar_prs)

        return context

    def _find_affected_communities(self, file_paths: list[str]) -> list[dict]:
        """Find communities that contain the given files.

        Args:
            file_paths: List of file paths

        Returns:
            List of community summaries
        """
        if not file_paths:
            return []

        with self.connection.session() as session:
            result = session.run("""
                UNWIND $file_paths as fp
                MATCH (f:File)-[:CONTAINS_CLASS|CONTAINS_FUNCTION]->(entity)
                WHERE f.path ENDS WITH fp
                AND entity.community IS NOT NULL
                WITH entity.community as community_id, collect(DISTINCT entity.name) as members
                RETURN community_id,
                       size(members) as member_count,
                       members[0:5] as sample_members
                ORDER BY member_count DESC
                LIMIT 10
            """, file_paths=file_paths)

            return [dict(record) for record in result]

    def _find_entry_points(self, similar_prs: list[dict]) -> list[dict]:
        """Find key functions that were modified in similar PRs.

        Args:
            similar_prs: List of similar PRs

        Returns:
            List of key entry points (functions/classes)
        """
        # Collect all files from similar PRs
        all_files = set()
        for pr in similar_prs:
            if pr.get("files_changed"):
                all_files.update(pr["files_changed"])

        if not all_files:
            return []

        with self.connection.session() as session:
            # Query functions and classes separately (Kuzu doesn't support | in rel types)
            functions_result = session.run("""
                UNWIND $file_paths as fp
                MATCH (f:File)-[:CONTAINS_FUNCTION]->(entity:Function)
                WHERE f.path ENDS WITH fp
                AND entity.pagerank IS NOT NULL
                RETURN 'Function' as type,
                       entity.name as name,
                       entity.qualified_name as qualified_name,
                       entity.pagerank as pagerank,
                       f.path as file_path
            """, file_paths=list(all_files))

            classes_result = session.run("""
                UNWIND $file_paths as fp
                MATCH (f:File)-[:CONTAINS_CLASS]->(entity:Class)
                WHERE f.path ENDS WITH fp
                AND entity.pagerank IS NOT NULL
                RETURN 'Class' as type,
                       entity.name as name,
                       entity.qualified_name as qualified_name,
                       entity.pagerank as pagerank,
                       f.path as file_path
            """, file_paths=list(all_files))

            # Combine and sort by pagerank
            all_results = [dict(r) for r in functions_result] + [dict(r) for r in classes_result]
            all_results.sort(key=lambda x: x.get("pagerank", 0) or 0, reverse=True)
            return all_results[:10]

    def _find_domain_experts(
        self,
        file_paths: list[str],
        limit: int = 5,
    ) -> list[dict]:
        """Find authors with most commits to the given files.

        Args:
            file_paths: List of file paths
            limit: Maximum number of experts to return

        Returns:
            List of domain experts with commit counts
        """
        if not file_paths:
            return []

        with self.connection.session() as session:
            result = session.run("""
                UNWIND $file_paths as fp
                MATCH (f:File)<-[:COMMIT_MODIFIES]-(c:GitCommit)-[:AUTHORED_BY]->(a:Author)
                WHERE f.path ENDS WITH fp
                WITH a.name as author_name,
                     a.email as author_email,
                     count(DISTINCT c) as commit_count,
                     collect(DISTINCT f.path) as files_touched
                RETURN author_name,
                       author_email,
                       commit_count,
                       size(files_touched) as files_count,
                       files_touched[0:5] as sample_files
                ORDER BY commit_count DESC
                LIMIT $limit
            """, file_paths=file_paths, limit=limit)

            return [dict(record) for record in result]

    def _extract_tasks_from_prs(self, similar_prs: list[dict]) -> list[dict]:
        """Extract tasks from similar PRs.

        Args:
            similar_prs: List of similar PRs

        Returns:
            List of tasks from the PRs
        """
        if not similar_prs:
            return []

        pr_numbers = [pr["number"] for pr in similar_prs if pr.get("number")]

        if not pr_numbers:
            return []

        with self.connection.session() as session:
            result = session.run("""
                UNWIND $pr_numbers as pr_num
                MATCH (pr:PullRequest {number: pr_num})-[:HAS_TASK]->(t:Task)
                RETURN pr.number as pr_number,
                       pr.title as pr_title,
                       t.description as task_description,
                       t.is_completed as is_completed
                ORDER BY pr.number, t.order
            """, pr_numbers=pr_numbers)

            return [dict(record) for record in result]
