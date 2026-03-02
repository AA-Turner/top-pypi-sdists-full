"""TouchedAreasProvider - Context from AST neighbors of modified code."""

import os
from typing import Optional

from ..models import ContextItem, ContextProviderSpec
from .base import ContextProvider
from ..registry import ContextProviderRegistry
from ...graph.connection import KuzuConnection
from ...utils.logger import log


class TouchedAreasProvider(ContextProvider):
    """Context provider that extracts AST neighbors of touched code.

    When files are modified, this provider:
    1. Finds functions/classes in those files from the Kuzu AST
    2. Gets N-hop neighbors (callers, callees, parent classes, etc.)
    3. Returns context items with descriptions and relationships
    """

    def __init__(self, connection: KuzuConnection, config: Optional[dict] = None):
        super().__init__(connection, config)
        self._neighbor_depth = int(
            config.get("neighbor_depth") if config else os.getenv("CONTEXT_NEIGHBOR_DEPTH", "2")
        )

    @property
    def spec(self) -> ContextProviderSpec:
        return ContextProviderSpec(
            name="touched_areas",
            description="AST-based context from modified code and neighbors",
            requires_graph=True,
        )

    def extract_context(self, modified_files: list[str]) -> list[ContextItem]:
        """Extract context items from modified files.

        Args:
            modified_files: List of file paths that were modified

        Returns:
            List of context items with AST neighbors
        """
        if not modified_files:
            return []

        items = []
        seen_qualified_names = set()

        for file_path in modified_files:
            # Skip non-code files
            if not self._is_code_file(file_path):
                continue

            # Normalize path to match what's in the database
            normalized_path = self._normalize_path(file_path)

            # Get entities in this file
            entities = self._get_file_entities(normalized_path)

            for entity in entities:
                qname = entity.get("qualified_name")
                if not qname or qname in seen_qualified_names:
                    continue
                seen_qualified_names.add(qname)

                # Get neighbors up to configured depth
                neighbors = self._get_neighbors(entity, depth=self._neighbor_depth)
                neighbor_names = [n.get("qualified_name") for n in neighbors if n.get("qualified_name")]

                items.append(
                    ContextItem(
                        qualified_name=qname,
                        entity_type=entity.get("type", "Unknown"),
                        description=entity.get("docstring"),
                        file_path=file_path,
                        neighbors=neighbor_names,
                    )
                )

        log.info(f"TouchedAreasProvider: extracted {len(items)} context items from {len(modified_files)} files")
        return items

    def _normalize_path(self, file_path: str) -> str:
        """Normalize file path to match database format."""
        # Convert to absolute path if relative
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        return file_path

    def _is_code_file(self, file_path: str) -> bool:
        """Check if file is a code file worth tracking.

        Filters out logs, build artifacts, and other non-code files.
        """
        if not file_path:
            return False

        lower_path = file_path.lower()

        # Skip patterns
        skip_patterns = (
            ".log", "/logs/", "/log/",
            "/node_modules/", "/__pycache__/",
            "/dist/", "/build/", "/.git/",
            ".pyc", ".pyo", ".so", ".dll",
            "/coverage/", "/.nyc_output/",
            ".env", ".lock",
        )
        if any(pattern in lower_path for pattern in skip_patterns):
            return False

        # Code file extensions
        code_extensions = (
            ".py", ".ts", ".tsx", ".js", ".jsx",
            ".java", ".go", ".rs", ".rb", ".php",
            ".c", ".cpp", ".h", ".hpp", ".cs",
            ".swift", ".kt", ".scala", ".vue",
            ".json", ".yaml", ".yml", ".toml",
            ".md", ".sql", ".graphql",
        )
        return any(lower_path.endswith(ext) for ext in code_extensions)

    def _get_file_entities(self, file_path: str) -> list[dict]:
        """Query Kuzu for functions and classes in a file.

        Args:
            file_path: Absolute path to the file

        Returns:
            List of entity dictionaries
        """
        try:
            # Try exact match first
            results = self.connection.execute(
                """
                MATCH (f:File)-[:CONTAINS_FUNCTION]->(fn:Function)
                WHERE f.path = $path
                RETURN fn.qualified_name as qualified_name,
                       'Function' as type,
                       fn.docstring as docstring,
                       fn.name as name
                """,
                {"path": file_path},
            )

            # Also get classes
            class_results = self.connection.execute(
                """
                MATCH (f:File)-[:CONTAINS_CLASS]->(c:Class)
                WHERE f.path = $path
                RETURN c.qualified_name as qualified_name,
                       'Class' as type,
                       c.docstring as docstring,
                       c.name as name
                """,
                {"path": file_path},
            )

            results.extend(class_results)

            # If no results, try ENDS WITH for partial path match
            if not results:
                filename = os.path.basename(file_path)
                results = self.connection.execute(
                    """
                    MATCH (f:File)-[:CONTAINS_FUNCTION]->(fn:Function)
                    WHERE f.path ENDS WITH $filename
                    RETURN fn.qualified_name as qualified_name,
                           'Function' as type,
                           fn.docstring as docstring,
                           fn.name as name
                    """,
                    {"filename": filename},
                )

                class_results = self.connection.execute(
                    """
                    MATCH (f:File)-[:CONTAINS_CLASS]->(c:Class)
                    WHERE f.path ENDS WITH $filename
                    RETURN c.qualified_name as qualified_name,
                           'Class' as type,
                           c.docstring as docstring,
                           c.name as name
                    """,
                    {"filename": filename},
                )
                results.extend(class_results)

            return results

        except Exception as e:
            log.debug(f"Failed to get file entities for {file_path}: {e}")
            return []

    def _get_neighbors(self, entity: dict, depth: int = 2) -> list[dict]:
        """Get N-hop neighbors of an entity.

        Traverses CALLS, INHERITS_FROM, and HAS_METHOD relationships
        to find related code entities.

        Args:
            entity: Entity dictionary with qualified_name and type
            depth: Number of hops to traverse

        Returns:
            List of neighbor entity dictionaries
        """
        qname = entity.get("qualified_name")
        entity_type = entity.get("type")

        if not qname:
            return []

        neighbors = []

        try:
            if entity_type == "Function":
                neighbors.extend(self._get_function_neighbors(qname, depth))
            elif entity_type == "Class":
                neighbors.extend(self._get_class_neighbors(qname, depth))

        except Exception as e:
            log.warning(f"Failed to get neighbors for {qname}: {e}")

        return neighbors

    def _get_function_neighbors(self, qualified_name: str, depth: int) -> list[dict]:
        """Get neighbors of a function (callers, callees)."""
        neighbors = []

        # Get direct callers (functions that call this one)
        callers = self.connection.execute(
            """
            MATCH (caller:Function)-[:CALLS]->(f:Function {qualified_name: $qname})
            RETURN caller.qualified_name as qualified_name,
                   'Function' as type,
                   caller.docstring as docstring,
                   caller.name as name
            LIMIT 20
            """,
            {"qname": qualified_name},
        )
        neighbors.extend(callers)

        # Get direct callees (functions this one calls)
        callees = self.connection.execute(
            """
            MATCH (f:Function {qualified_name: $qname})-[:CALLS]->(callee:Function)
            RETURN callee.qualified_name as qualified_name,
                   'Function' as type,
                   callee.docstring as docstring,
                   callee.name as name
            LIMIT 20
            """,
            {"qname": qualified_name},
        )
        neighbors.extend(callees)

        # If depth > 1, get 2nd hop neighbors
        if depth > 1:
            # 2-hop callers (who calls my callers)
            hop2_callers = self.connection.execute(
                """
                MATCH (caller2:Function)-[:CALLS]->(caller:Function)-[:CALLS]->(f:Function {qualified_name: $qname})
                WHERE caller2.qualified_name <> $qname
                RETURN DISTINCT caller2.qualified_name as qualified_name,
                       'Function' as type,
                       caller2.docstring as docstring,
                       caller2.name as name
                LIMIT 10
                """,
                {"qname": qualified_name},
            )
            neighbors.extend(hop2_callers)

            # 2-hop callees (who my callees call)
            hop2_callees = self.connection.execute(
                """
                MATCH (f:Function {qualified_name: $qname})-[:CALLS]->(callee:Function)-[:CALLS]->(callee2:Function)
                WHERE callee2.qualified_name <> $qname
                RETURN DISTINCT callee2.qualified_name as qualified_name,
                       'Function' as type,
                       callee2.docstring as docstring,
                       callee2.name as name
                LIMIT 10
                """,
                {"qname": qualified_name},
            )
            neighbors.extend(hop2_callees)

        return neighbors

    def _get_class_neighbors(self, qualified_name: str, depth: int) -> list[dict]:
        """Get neighbors of a class (parents, children, methods)."""
        neighbors = []

        # Get parent classes
        parents = self.connection.execute(
            """
            MATCH (c:Class {qualified_name: $qname})-[:INHERITS_FROM]->(parent:Class)
            RETURN parent.qualified_name as qualified_name,
                   'Class' as type,
                   parent.docstring as docstring,
                   parent.name as name
            LIMIT 10
            """,
            {"qname": qualified_name},
        )
        neighbors.extend(parents)

        # Get child classes
        children = self.connection.execute(
            """
            MATCH (child:Class)-[:INHERITS_FROM]->(c:Class {qualified_name: $qname})
            RETURN child.qualified_name as qualified_name,
                   'Class' as type,
                   child.docstring as docstring,
                   child.name as name
            LIMIT 10
            """,
            {"qname": qualified_name},
        )
        neighbors.extend(children)

        # Get methods of this class
        methods = self.connection.execute(
            """
            MATCH (c:Class {qualified_name: $qname})-[:HAS_METHOD]->(m:Function)
            RETURN m.qualified_name as qualified_name,
                   'Function' as type,
                   m.docstring as docstring,
                   m.name as name
            LIMIT 20
            """,
            {"qname": qualified_name},
        )
        neighbors.extend(methods)

        # If depth > 1, get grandparent/grandchild classes
        if depth > 1:
            grandparents = self.connection.execute(
                """
                MATCH (c:Class {qualified_name: $qname})-[:INHERITS_FROM]->(:Class)-[:INHERITS_FROM]->(gp:Class)
                RETURN DISTINCT gp.qualified_name as qualified_name,
                       'Class' as type,
                       gp.docstring as docstring,
                       gp.name as name
                LIMIT 5
                """,
                {"qname": qualified_name},
            )
            neighbors.extend(grandparents)

        return neighbors


# Auto-register provider
ContextProviderRegistry.register("touched_areas", TouchedAreasProvider)
