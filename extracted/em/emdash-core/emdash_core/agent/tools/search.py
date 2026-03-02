"""Search tools for finding code in the graph."""

import subprocess
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


class SemanticSearchTool(BaseTool):
    """Search for code entities using natural language."""

    name = "semantic_search"
    description = """Search for code entities (functions, classes, files) using natural language.
Returns entities matching the semantic meaning of your query, ranked by relevance.
Useful for finding code related to concepts like "authentication", "database queries", etc."""
    category = ToolCategory.SEARCH

    def execute(
        self,
        query: str,
        entity_types: Optional[list[str]] = None,
        limit: int = 10,
        min_score: float = 0.5,
        **kwargs,  # Ignore unexpected params from LLM
    ) -> ToolResult:
        """Execute semantic search.

        Args:
            query: Natural language search query
            entity_types: Optional list of types to filter (Function, Class, File)
            limit: Maximum results to return
            min_score: Minimum similarity score (0-1)

        Returns:
            ToolResult with matching entities
        """
        try:
            from ...embeddings.indexer import EmbeddingIndexer

            indexer = EmbeddingIndexer(connection=self.connection)
            results = indexer.search(
                query=query,
                entity_types=entity_types,
                limit=limit,
                min_score=min_score,
            )

            return ToolResult.success_result(
                data={
                    "query": query,
                    "results": results,
                    "count": len(results),
                },
                suggestions=self._generate_suggestions(results),
            )

        except Exception as e:
            log.exception("Semantic search failed")
            return ToolResult.error_result(
                f"Search failed: {str(e)}",
                suggestions=["Try a different query", "Check if embeddings are indexed"],
            )

    def _generate_suggestions(self, results: list) -> list[str]:
        """Generate next step suggestions based on results."""
        if not results:
            return ["Try broader search terms", "Use text_search for exact matches"]

        suggestions = []
        top = results[0]

        if top.get("node_type") == "Function":
            suggestions.append(f"Use expand_node to see full context of {top.get('qualified_name')}")
            suggestions.append(f"Use get_callers to see who calls {top.get('qualified_name')}")
        elif top.get("node_type") == "Class":
            suggestions.append(f"Use expand_node to see methods and relationships")
        elif top.get("node_type") == "File":
            suggestions.append(f"Use expand_node to see file contents and dependencies")

        return suggestions

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "query": {
                    "type": "string",
                    "description": "Natural language search query",
                },
                "entity_types": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["Function", "Class", "File"]},
                    "description": "Types of entities to search for",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results to return",
                    "default": 10,
                },
                "min_score": {
                    "type": "number",
                    "description": "Minimum similarity score (0-1)",
                    "default": 0.5,
                },
            },
            required=["query"],
        )


class TextSearchTool(BaseTool):
    """Search for code by exact text match."""

    name = "text_search"
    description = """Search for code entities by exact text match in names.
Useful for finding specific functions, classes, or files by name.
More precise than semantic search when you know part of the name."""
    category = ToolCategory.SEARCH

    def execute(
        self,
        query: str,
        entity_types: Optional[list[str]] = None,
        limit: int = 10,
        **kwargs,  # Ignore unexpected params from LLM
    ) -> ToolResult:
        """Execute text search.

        Args:
            query: Text to search for in entity names
            entity_types: Optional types to filter
            limit: Maximum results

        Returns:
            ToolResult with matching entities
        """
        try:
            results = []

            # Search in graph
            cypher = """
            MATCH (n)
            WHERE (n:Function OR n:Class OR n:File)
            AND (
                n.qualified_name CONTAINS $query
                OR n.name CONTAINS $query
                OR n.file_path CONTAINS $query
            )
            RETURN n.qualified_name as qualified_name,
                   n.name as name,
                   n.file_path as file_path,
                   labels(n)[0] as node_type
            LIMIT $limit
            """

            with self.connection.session() as session:
                result = session.run(cypher, {"query": query, "limit": limit})
                for record in result:
                    results.append({
                        "qualified_name": record["qualified_name"],
                        "name": record["name"],
                        "file_path": record["file_path"],
                        "node_type": record["node_type"],
                    })

            # Filter by type if specified
            if entity_types:
                results = [r for r in results if r["node_type"] in entity_types]

            return ToolResult.success_result(
                data={
                    "query": query,
                    "results": results,
                    "count": len(results),
                },
            )

        except Exception as e:
            log.exception("Text search failed")
            return ToolResult.error_result(f"Search failed: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "query": {
                    "type": "string",
                    "description": "Text to search for in entity names",
                },
                "entity_types": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["Function", "Class", "File"]},
                    "description": "Types of entities to search for",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results to return",
                    "default": 10,
                },
            },
            required=["query"],
        )


class GrepTool(BaseTool):
    """Search file contents using ripgrep."""

    name = "grep"
    description = """Search file contents using ripgrep.
Fast full-text search across all files in the repository.
Useful for finding code patterns, string literals, or specific implementations."""
    category = ToolCategory.SEARCH

    def execute(
        self,
        pattern: str,
        file_pattern: Optional[str] = None,
        max_results: int = 50,
        context_lines: int = 2,
        **kwargs,  # Ignore unexpected params from LLM
    ) -> ToolResult:
        """Execute grep search.

        Args:
            pattern: Regex pattern to search for
            file_pattern: Optional glob pattern for files (e.g., "*.py")
            max_results: Maximum number of matches
            context_lines: Lines of context around matches

        Returns:
            ToolResult with grep matches
        """
        try:
            cmd = ["rg", "--json", "-C", str(context_lines), "-m", str(max_results)]

            if file_pattern:
                cmd.extend(["-g", file_pattern])

            cmd.append(pattern)

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )

            matches = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                try:
                    import json
                    data = json.loads(line)
                    if data.get("type") == "match":
                        match_data = data.get("data", {})
                        matches.append({
                            "file": match_data.get("path", {}).get("text", ""),
                            "line_number": match_data.get("line_number"),
                            "line_text": match_data.get("lines", {}).get("text", "").strip(),
                        })
                except json.JSONDecodeError:
                    continue

            return ToolResult.success_result(
                data={
                    "pattern": pattern,
                    "matches": matches,
                    "count": len(matches),
                },
            )

        except subprocess.TimeoutExpired:
            return ToolResult.error_result("Grep search timed out")
        except FileNotFoundError:
            return ToolResult.error_result(
                "ripgrep (rg) not found",
                suggestions=["Install ripgrep: brew install ripgrep"],
            )
        except Exception as e:
            log.exception("Grep search failed")
            return ToolResult.error_result(f"Grep failed: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for",
                },
                "file_pattern": {
                    "type": "string",
                    "description": "Optional glob pattern for files (e.g., '*.py')",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of matches",
                    "default": 50,
                },
                "context_lines": {
                    "type": "integer",
                    "description": "Lines of context around matches",
                    "default": 2,
                },
            },
            required=["pattern"],
        )


class GlobTool(BaseTool):
    """Find files by name/path patterns using glob."""

    name = "glob"
    description = """Find files by name or path pattern using glob syntax.
Use this to discover files matching patterns like "**/*.py" or "src/**/*.ts".
Unlike grep which searches file CONTENTS, glob searches file NAMES/PATHS.

Common patterns:
- "**/*.py" - All Python files
- "src/**/*.ts" - TypeScript files in src/
- "**/test_*.py" - Test files
- "**/*config*" - Files with 'config' in name"""
    category = ToolCategory.SEARCH

    def execute(
        self,
        pattern: str,
        max_results: int = 100,
        **kwargs,  # Ignore unexpected params from LLM
    ) -> ToolResult:
        """Execute glob search for files.

        Args:
            pattern: Glob pattern (e.g., "**/*.py", "src/**/*.ts")
            max_results: Maximum number of files to return

        Returns:
            ToolResult with matching file paths
        """
        from pathlib import Path

        try:
            # Get current working directory
            cwd = Path.cwd()

            # Execute glob
            matches = list(cwd.glob(pattern))

            # Sort by modification time (most recent first) and limit
            matches.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
            matches = matches[:max_results]

            # Convert to relative paths
            files = []
            for match in matches:
                if match.is_file():
                    try:
                        rel_path = match.relative_to(cwd)
                        files.append({
                            "path": str(rel_path),
                            "name": match.name,
                            "extension": match.suffix,
                        })
                    except ValueError:
                        files.append({
                            "path": str(match),
                            "name": match.name,
                            "extension": match.suffix,
                        })

            return ToolResult.success_result(
                data={
                    "pattern": pattern,
                    "files": files,
                    "count": len(files),
                },
                suggestions=self._generate_suggestions(files, pattern),
            )

        except Exception as e:
            log.exception("Glob search failed")
            return ToolResult.error_result(f"Glob failed: {str(e)}")

    def _generate_suggestions(self, files: list, pattern: str) -> list[str]:
        """Generate suggestions based on results."""
        if not files:
            return [
                "No files found. Try a broader pattern.",
                "Use '**/*' to match all files recursively.",
            ]

        suggestions = []
        if len(files) > 0:
            first_file = files[0]["path"]
            suggestions.append(f"Use read_file to examine '{first_file}'")
            suggestions.append(f"Use grep to search within these {len(files)} files")

        return suggestions

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern (e.g., '**/*.py', 'src/**/*.ts', '**/test_*.py')",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of files to return",
                    "default": 100,
                },
            },
            required=["pattern"],
        )
