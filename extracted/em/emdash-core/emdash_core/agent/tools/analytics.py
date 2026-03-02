"""Analytics tools for code graph metrics."""

from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


class GetAreaImportanceTool(BaseTool):
    """Get importance metrics for code areas."""

    name = "get_area_importance"
    description = """Get importance metrics for areas of the codebase.
Shows which directories or modules are most central to the codebase.
Sort by 'focus' for recent activity or 'importance' for overall historical importance."""
    category = ToolCategory.ANALYTICS

    def execute(
        self,
        area_type: str = "directory",
        sort: str = "focus",
        depth: int = 2,
        days: int = 30,
        limit: int = 10,
        files: bool = False,
    ) -> ToolResult:
        """Get area importance metrics.

        Args:
            area_type: Type of area (directory, module)
            sort: Sort by 'focus' (recent activity) or 'importance' (overall)
            depth: Directory depth for grouping (default 2)
            days: Time window for recent activity (default 30)
            limit: Maximum areas to return
            files: If True, return file-level instead of directory-level

        Returns:
            ToolResult with importance metrics
        """
        try:
            # Aggregate importance by directory
            # Note: Using range() and list comprehension instead of [0..-1] slice
            # because Memgraph doesn't support negative slice indices
            cypher = """
            MATCH (f:File)
            WHERE f.file_path IS NOT NULL AND f.file_path CONTAINS '/'
            WITH split(f.file_path, '/') as parts, f
            WITH [i IN range(0, size(parts)-2) | parts[i]] as dir_parts, f
            WITH reduce(s = '', p IN dir_parts | s + '/' + p) as directory, count(f) as file_count
            WHERE directory <> ''
            RETURN directory, file_count
            ORDER BY file_count DESC
            LIMIT $limit
            """

            areas = []
            with self.connection.session() as session:
                result = session.run(cypher, limit=limit)
                for record in result:
                    areas.append({
                        "directory": record["directory"],
                        "file_count": record["file_count"],
                    })

            return ToolResult.success_result(
                data={
                    "area_type": area_type,
                    "areas": areas,
                    "count": len(areas),
                },
            )

        except Exception as e:
            log.exception("Get area importance failed")
            return ToolResult.error_result(f"Failed: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "area_type": {
                    "type": "string",
                    "enum": ["directory", "module"],
                    "description": "Type of area to analyze",
                    "default": "directory",
                },
                "sort": {
                    "type": "string",
                    "enum": ["focus", "importance"],
                    "description": "Sort by 'focus' (recent hot spots) or 'importance' (overall activity)",
                    "default": "focus",
                },
                "depth": {
                    "type": "integer",
                    "description": "Directory depth for grouping",
                    "default": 2,
                },
                "days": {
                    "type": "integer",
                    "description": "Time window for recent activity",
                    "default": 30,
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum areas to return",
                    "default": 10,
                },
                "files": {
                    "type": "boolean",
                    "description": "If true, return file-level instead of directory-level",
                    "default": False,
                },
            },
            required=[],
        )


class GetTopPageRankTool(BaseTool):
    """Get entities with highest PageRank centrality."""

    name = "get_top_pagerank"
    description = """Get the most central/important code entities by PageRank.
PageRank identifies code that is most connected and depended upon.
High PageRank entities are often critical infrastructure."""
    category = ToolCategory.ANALYTICS

    def execute(
        self,
        entity_types: Optional[list[str]] = None,
        limit: int = 10,
    ) -> ToolResult:
        """Get top PageRank entities.

        Args:
            entity_types: Types to include (Function, Class, File)
            limit: Maximum results

        Returns:
            ToolResult with PageRank results
        """
        try:
            # Check if pagerank property exists
            check_query = """
            MATCH (n)
            WHERE n.pagerank IS NOT NULL
            RETURN count(n) as count
            LIMIT 1
            """

            has_pagerank = False
            with self.connection.session() as session:
                result = session.run(check_query)
                record = result.single()
                has_pagerank = record and record["count"] > 0

            if not has_pagerank:
                # Fall back to degree centrality
                return self._get_by_degree(entity_types, limit)

            # Get by PageRank
            type_filter = ""
            if entity_types:
                type_filter = "WHERE " + " OR ".join([f"n:{t}" for t in entity_types])

            cypher = f"""
            MATCH (n)
            {type_filter}
            {'AND' if type_filter else 'WHERE'} n.pagerank IS NOT NULL
            RETURN n.qualified_name as qualified_name,
                   n.file_path as file_path,
                   labels(n)[0] as node_type,
                   n.pagerank as pagerank
            ORDER BY n.pagerank DESC
            LIMIT $limit
            """

            results = []
            with self.connection.session() as session:
                result = session.run(cypher, limit=limit)
                for record in result:
                    results.append({
                        "qualified_name": record["qualified_name"],
                        "file_path": record["file_path"],
                        "node_type": record["node_type"],
                        "pagerank": record["pagerank"],
                    })

            return ToolResult.success_result(
                data={
                    "results": results,
                    "count": len(results),
                    "metric": "pagerank",
                },
            )

        except Exception as e:
            log.exception("Get top PageRank failed")
            return ToolResult.error_result(f"Failed: {str(e)}")

    def _get_by_degree(
        self,
        entity_types: Optional[list[str]],
        limit: int,
    ) -> ToolResult:
        """Fall back to degree centrality."""
        try:
            type_filter = ""
            if entity_types:
                type_filter = "WHERE " + " OR ".join([f"n:{t}" for t in entity_types])

            cypher = f"""
            MATCH (n)
            {type_filter}
            WITH n, size((n)--()) as degree
            WHERE degree > 0
            RETURN n.qualified_name as qualified_name,
                   n.file_path as file_path,
                   labels(n)[0] as node_type,
                   degree
            ORDER BY degree DESC
            LIMIT $limit
            """

            results = []
            with self.connection.session() as session:
                result = session.run(cypher, limit=limit)
                for record in result:
                    results.append({
                        "qualified_name": record["qualified_name"],
                        "file_path": record["file_path"],
                        "node_type": record["node_type"],
                        "degree": record["degree"],
                    })

            return ToolResult.success_result(
                data={
                    "results": results,
                    "count": len(results),
                    "metric": "degree",
                    "note": "PageRank not computed, using degree centrality",
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "entity_types": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["Function", "Class", "File"]},
                    "description": "Types to include",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results",
                    "default": 10,
                },
            },
            required=[],
        )


class GetCommunitiesTool(BaseTool):
    """Get code communities (clusters) in the graph."""

    name = "get_communities"
    description = """Get code communities (clusters) detected in the codebase.
Communities are groups of closely related code entities.
Useful for understanding code organization and module boundaries."""
    category = ToolCategory.ANALYTICS

    def execute(
        self,
        limit: int = 10,
        include_members: bool = False,
    ) -> ToolResult:
        """Get code communities.

        Args:
            limit: Maximum communities to return
            include_members: Whether to include sample members

        Returns:
            ToolResult with community information
        """
        try:
            # Check if community property exists
            check_query = """
            MATCH (n)
            WHERE n.community IS NOT NULL
            RETURN count(n) as count
            LIMIT 1
            """

            has_communities = False
            with self.connection.session() as session:
                result = session.run(check_query)
                record = result.single()
                has_communities = record and record["count"] > 0

            if not has_communities:
                return ToolResult.success_result(
                    data={
                        "communities": [],
                        "count": 0,
                        "note": "Community detection not run",
                    },
                    suggestions=["Run analytics to detect communities"],
                )

            # Get community counts
            cypher = """
            MATCH (n)
            WHERE n.community IS NOT NULL
            WITH n.community as community, count(n) as size,
                 collect(n.qualified_name)[0..5] as sample
            RETURN community, size, sample
            ORDER BY size DESC
            LIMIT $limit
            """

            communities = []
            with self.connection.session() as session:
                result = session.run(cypher, limit=limit)
                for record in result:
                    comm = {
                        "community_id": record["community"],
                        "size": record["size"],
                    }
                    if include_members:
                        comm["sample_members"] = [m for m in record["sample"] if m]
                    communities.append(comm)

            return ToolResult.success_result(
                data={
                    "communities": communities,
                    "count": len(communities),
                },
            )

        except Exception as e:
            log.exception("Get communities failed")
            return ToolResult.error_result(f"Failed: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "limit": {
                    "type": "integer",
                    "description": "Maximum communities to return",
                    "default": 10,
                },
                "include_members": {
                    "type": "boolean",
                    "description": "Include sample member names",
                    "default": False,
                },
            },
            required=[],
        )


class GetCommunityMembersTool(BaseTool):
    """Get members of a specific community."""

    name = "get_community_members"
    description = """Get all members of a specific code community.
Useful for understanding what code belongs to a detected cluster."""
    category = ToolCategory.ANALYTICS

    def execute(
        self,
        community_id: int,
        limit: int = 50,
    ) -> ToolResult:
        """Get community members.

        Args:
            community_id: Community ID
            limit: Maximum members to return

        Returns:
            ToolResult with member information
        """
        try:
            cypher = """
            MATCH (n)
            WHERE n.community = $community_id
            RETURN n.qualified_name as qualified_name,
                   n.file_path as file_path,
                   labels(n)[0] as node_type
            LIMIT $limit
            """

            members = []
            with self.connection.session() as session:
                result = session.run(cypher, community_id=community_id, limit=limit)
                for record in result:
                    members.append({
                        "qualified_name": record["qualified_name"],
                        "file_path": record["file_path"],
                        "node_type": record["node_type"],
                    })

            return ToolResult.success_result(
                data={
                    "community_id": community_id,
                    "members": members,
                    "count": len(members),
                },
            )

        except Exception as e:
            log.exception("Get community members failed")
            return ToolResult.error_result(f"Failed: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "community_id": {
                    "type": "integer",
                    "description": "Community ID to get members for",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum members to return",
                    "default": 50,
                },
            },
            required=["community_id"],
        )
