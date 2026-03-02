"""Graph traversal tools for exploring code relationships.

Note: These tools are now primarily provided by the emdash-graph MCP server.
This file contains fallback implementations for when MCP is not available.
"""

from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


class ExpandNodeTool(BaseTool):
    """Expand a node to see its context and relationships."""

    name = "expand_node"
    description = """Get detailed information about a code entity and its immediate relationships.
Shows the entity's properties, connected nodes, and relevant context.
Useful for understanding what a function/class does and how it connects to other code."""
    category = ToolCategory.TRAVERSAL

    def execute(
        self,
        node_type: str,
        identifier: str,
        max_hops: int = 1,
    ) -> ToolResult:
        """Expand a node to see relationships.

        Args:
            node_type: Type of node (Function, Class, File)
            identifier: Qualified name or file path
            max_hops: How many relationship hops to include

        Returns:
            ToolResult with node details and relationships
        """
        try:
            # Query for the node and its relationships
            if node_type == "File":
                cypher = """
                MATCH (n:File {file_path: $identifier})
                OPTIONAL MATCH (n)-[r]->(m)
                RETURN n, collect({type: type(r), target: m}) as relationships
                """
            else:
                cypher = """
                MATCH (n {qualified_name: $identifier})
                WHERE $node_type IN labels(n)
                OPTIONAL MATCH (n)-[r]->(m)
                RETURN n, collect({type: type(r), target: m}) as relationships
                """

            with self.connection.session() as session:
                result = session.run(cypher, {
                    "identifier": identifier,
                    "node_type": node_type,
                })
                record = result.single()

                if not record:
                    return ToolResult.error_result(
                        f"{node_type} '{identifier}' not found",
                        suggestions=["Try semantic_search to find similar entities"],
                    )

                node = dict(record["n"])
                relationships = []

                for rel in record["relationships"]:
                    if rel["target"]:
                        target = dict(rel["target"])
                        relationships.append({
                            "type": rel["type"],
                            "target_name": target.get("qualified_name") or target.get("file_path"),
                            "target_type": target.get("node_type"),
                        })

                return ToolResult.success_result(
                    data={
                        "root_node": {
                            "qualified_name": node.get("qualified_name"),
                            "file_path": node.get("file_path"),
                            "node_type": node_type,
                            "docstring": node.get("docstring"),
                            "start_line": node.get("start_line"),
                            "end_line": node.get("end_line"),
                        },
                        "relationships": relationships,
                        "summary": {
                            "relationship_count": len(relationships),
                        },
                    },
                )

        except Exception as e:
            log.exception("Expand node failed")
            return ToolResult.error_result(f"Expansion failed: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "node_type": {
                    "type": "string",
                    "enum": ["Function", "Class", "File"],
                    "description": "Type of node to expand",
                },
                "identifier": {
                    "type": "string",
                    "description": "Qualified name (for functions/classes) or file path (for files)",
                },
                "max_hops": {
                    "type": "integer",
                    "description": "How many relationship hops to include",
                    "default": 1,
                },
            },
            required=["node_type", "identifier"],
        )


class GetCallersTool(BaseTool):
    """Find functions that call a given function."""

    name = "get_callers"
    description = """Find all functions that call the specified function.
Useful for understanding the impact of changes and finding usage patterns."""
    category = ToolCategory.TRAVERSAL

    def execute(
        self,
        qualified_name: str,
        limit: int = 20,
    ) -> ToolResult:
        """Get callers of a function.

        Args:
            qualified_name: Qualified name of the function
            limit: Maximum callers to return

        Returns:
            ToolResult with caller information
        """
        try:
            cypher = """
            MATCH (caller:Function)-[:CALLS]->(callee:Function {qualified_name: $qualified_name})
            RETURN caller.qualified_name as qualified_name,
                   caller.file_path as file_path
            LIMIT $limit
            """

            callers = []
            with self.connection.session() as session:
                result = session.run(cypher, {
                    "qualified_name": qualified_name,
                    "limit": limit,
                })
                for record in result:
                    callers.append({
                        "qualified_name": record["qualified_name"],
                        "file_path": record["file_path"],
                    })

            return ToolResult.success_result(
                data={
                    "function": qualified_name,
                    "callers": callers,
                    "count": len(callers),
                },
            )

        except Exception as e:
            log.exception("Get callers failed")
            return ToolResult.error_result(f"Failed to get callers: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "qualified_name": {
                    "type": "string",
                    "description": "Qualified name of the function",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum callers to return",
                    "default": 20,
                },
            },
            required=["qualified_name"],
        )


class GetCalleesTool(BaseTool):
    """Find functions called by a given function."""

    name = "get_callees"
    description = """Find all functions that the specified function calls.
Useful for understanding a function's dependencies."""
    category = ToolCategory.TRAVERSAL

    def execute(
        self,
        qualified_name: str,
        limit: int = 20,
    ) -> ToolResult:
        """Get callees of a function.

        Args:
            qualified_name: Qualified name of the function
            limit: Maximum callees to return

        Returns:
            ToolResult with callee information
        """
        try:
            cypher = """
            MATCH (caller:Function {qualified_name: $qualified_name})-[:CALLS]->(callee:Function)
            RETURN callee.qualified_name as qualified_name,
                   callee.file_path as file_path
            LIMIT $limit
            """

            callees = []
            with self.connection.session() as session:
                result = session.run(cypher, {
                    "qualified_name": qualified_name,
                    "limit": limit,
                })
                for record in result:
                    callees.append({
                        "qualified_name": record["qualified_name"],
                        "file_path": record["file_path"],
                    })

            return ToolResult.success_result(
                data={
                    "function": qualified_name,
                    "callees": callees,
                    "count": len(callees),
                },
            )

        except Exception as e:
            log.exception("Get callees failed")
            return ToolResult.error_result(f"Failed to get callees: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "qualified_name": {
                    "type": "string",
                    "description": "Qualified name of the function",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum callees to return",
                    "default": 20,
                },
            },
            required=["qualified_name"],
        )


class GetClassHierarchyTool(BaseTool):
    """Get the inheritance hierarchy for a class."""

    name = "get_class_hierarchy"
    description = """Get the inheritance hierarchy for a class.
Shows parent classes (bases) and child classes (subclasses)."""
    category = ToolCategory.TRAVERSAL

    def execute(
        self,
        class_name: str,
    ) -> ToolResult:
        """Get class hierarchy.

        Args:
            class_name: Qualified name of the class

        Returns:
            ToolResult with hierarchy information
        """
        try:
            # Get bases (parents)
            bases_query = """
            MATCH (c:Class {qualified_name: $class_name})-[:INHERITS_FROM]->(base:Class)
            RETURN base.qualified_name as qualified_name
            """

            # Get subclasses (children)
            children_query = """
            MATCH (child:Class)-[:INHERITS_FROM]->(c:Class {qualified_name: $class_name})
            RETURN child.qualified_name as qualified_name
            """

            bases = []
            children = []

            with self.connection.session() as session:
                result = session.run(bases_query, {"class_name": class_name})
                for record in result:
                    bases.append(record["qualified_name"])

                result = session.run(children_query, {"class_name": class_name})
                for record in result:
                    children.append(record["qualified_name"])

            return ToolResult.success_result(
                data={
                    "class": class_name,
                    "bases": bases,
                    "subclasses": children,
                },
            )

        except Exception as e:
            log.exception("Get class hierarchy failed")
            return ToolResult.error_result(f"Failed to get hierarchy: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "class_name": {
                    "type": "string",
                    "description": "Qualified name of the class",
                },
            },
            required=["class_name"],
        )


class GetFileDependenciesTool(BaseTool):
    """Get import/export dependencies for a file."""

    name = "get_file_dependencies"
    description = """Get the import and export dependencies for a file.
Shows which files this file imports from and which files import from it."""
    category = ToolCategory.TRAVERSAL

    def execute(
        self,
        file_path: str,
    ) -> ToolResult:
        """Get file dependencies.

        Args:
            file_path: Path to the file

        Returns:
            ToolResult with dependency information
        """
        try:
            # Get imports (files this file depends on)
            imports_query = """
            MATCH (f:File {file_path: $file_path})-[:IMPORTS]->(imported:File)
            RETURN imported.file_path as file_path
            """

            # Get importers (files that depend on this file)
            importers_query = """
            MATCH (importer:File)-[:IMPORTS]->(f:File {file_path: $file_path})
            RETURN importer.file_path as file_path
            """

            imports = []
            importers = []

            with self.connection.session() as session:
                result = session.run(imports_query, {"file_path": file_path})
                for record in result:
                    imports.append(record["file_path"])

                result = session.run(importers_query, {"file_path": file_path})
                for record in result:
                    importers.append(record["file_path"])

            return ToolResult.success_result(
                data={
                    "file": file_path,
                    "imports": imports,
                    "imported_by": importers,
                },
            )

        except Exception as e:
            log.exception("Get file dependencies failed")
            return ToolResult.error_result(f"Failed to get dependencies: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "file_path": {
                    "type": "string",
                    "description": "Path to the file",
                },
            },
            required=["file_path"],
        )


class GetImpactAnalysisTool(BaseTool):
    """Analyze the impact of changing a code entity."""

    name = "get_impact_analysis"
    description = """Analyze the potential impact of changing a code entity.
Shows affected files, callers, and risk assessment."""
    category = ToolCategory.TRAVERSAL

    def execute(
        self,
        entity_type: str,
        identifier: str,
        depth: int = 2,
    ) -> ToolResult:
        """Analyze change impact.

        Args:
            entity_type: Type of entity (Function, Class, File)
            identifier: Qualified name or file path
            depth: How many levels of dependencies to analyze

        Returns:
            ToolResult with impact analysis
        """
        try:
            affected_files = set()
            affected_functions = set()

            # Simple impact analysis based on callers
            if entity_type == "Function":
                cypher = """
                MATCH (caller)-[:CALLS*1..%d]->(f:Function {qualified_name: $identifier})
                RETURN DISTINCT caller.file_path as file_path,
                       caller.qualified_name as qualified_name
                """ % depth

                with self.connection.session() as session:
                    result = session.run(cypher, {"identifier": identifier})
                    for record in result:
                        if record["file_path"]:
                            affected_files.add(record["file_path"])
                        if record["qualified_name"]:
                            affected_functions.add(record["qualified_name"])

            # Determine risk level
            num_affected = len(affected_files) + len(affected_functions)
            if num_affected > 20:
                risk_level = "high"
            elif num_affected > 5:
                risk_level = "medium"
            else:
                risk_level = "low"

            return ToolResult.success_result(
                data={
                    "entity": identifier,
                    "affected_files": list(affected_files)[:50],
                    "affected_functions": list(affected_functions)[:50],
                    "risk_level": risk_level,
                    "total_affected": num_affected,
                },
            )

        except Exception as e:
            log.exception("Impact analysis failed")
            return ToolResult.error_result(f"Impact analysis failed: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "entity_type": {
                    "type": "string",
                    "enum": ["Function", "Class", "File"],
                    "description": "Type of entity to analyze",
                },
                "identifier": {
                    "type": "string",
                    "description": "Qualified name or file path",
                },
                "depth": {
                    "type": "integer",
                    "description": "Levels of dependencies to analyze",
                    "default": 2,
                },
            },
            required=["entity_type", "identifier"],
        )


class GetNeighborsTool(BaseTool):
    """Get immediate neighbors of a node in the graph."""

    name = "get_neighbors"
    description = """Get all immediate neighbors of a node in the code graph.
Shows all directly connected entities regardless of relationship type."""
    category = ToolCategory.TRAVERSAL

    def execute(
        self,
        node_type: str,
        identifier: str,
        limit: int = 30,
    ) -> ToolResult:
        """Get node neighbors.

        Args:
            node_type: Type of node
            identifier: Qualified name or file path
            limit: Maximum neighbors to return

        Returns:
            ToolResult with neighbor information
        """
        try:
            if node_type == "File":
                cypher = """
                MATCH (n:File {file_path: $identifier})-[r]-(neighbor)
                RETURN DISTINCT type(r) as relationship,
                       labels(neighbor)[0] as neighbor_type,
                       neighbor.qualified_name as qualified_name,
                       neighbor.file_path as file_path
                LIMIT $limit
                """
            else:
                cypher = """
                MATCH (n {qualified_name: $identifier})-[r]-(neighbor)
                WHERE $node_type IN labels(n)
                RETURN DISTINCT type(r) as relationship,
                       labels(neighbor)[0] as neighbor_type,
                       neighbor.qualified_name as qualified_name,
                       neighbor.file_path as file_path
                LIMIT $limit
                """

            neighbors = []
            with self.connection.session() as session:
                result = session.run(cypher, {
                    "identifier": identifier,
                    "node_type": node_type,
                    "limit": limit,
                })
                for record in result:
                    neighbors.append({
                        "relationship": record["relationship"],
                        "type": record["neighbor_type"],
                        "identifier": record["qualified_name"] or record["file_path"],
                    })

            return ToolResult.success_result(
                data={
                    "node": identifier,
                    "neighbors": neighbors,
                    "count": len(neighbors),
                },
            )

        except Exception as e:
            log.exception("Get neighbors failed")
            return ToolResult.error_result(f"Failed to get neighbors: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "node_type": {
                    "type": "string",
                    "enum": ["Function", "Class", "File"],
                    "description": "Type of node",
                },
                "identifier": {
                    "type": "string",
                    "description": "Qualified name or file path",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum neighbors to return",
                    "default": 30,
                },
            },
            required=["node_type", "identifier"],
        )
