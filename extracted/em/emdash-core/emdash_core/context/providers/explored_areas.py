"""ExploredAreasProvider - Context from agent exploration with tool-based relevance."""

from dataclasses import asdict
from typing import Optional, Union

from ..models import ContextItem, ContextProviderSpec
from ..tool_relevance import (
    TOOL_RELEVANCE,
    SEARCH_TOOLS,
    TOP_RESULTS_LIMIT,
    NON_TOP_RESULT_MULTIPLIER,
    get_tool_relevance,
    is_search_tool,
)
from .base import ContextProvider
from ..registry import ContextProviderRegistry
from ...graph.connection import KuzuConnection
from ...utils.logger import log


class ExploredAreasProvider(ContextProvider):
    """Context provider that extracts entities from agent exploration.

    Analyzes the steps recorded during an agent session and assigns
    relevance scores based on the tool type used to discover each entity.

    Scoring is defined in tool_relevance.py:
    - Highest: Code modifications (write_to_file, apply_diff)
    - High: Deliberate investigation (expand_node, get_callers, read_file)
    - Medium: Targeted search (semantic_search, text_search, grep)
    - Low: Broad discovery (list_files, graph algorithms)
    """

    def __init__(self, connection: KuzuConnection, config: Optional[dict] = None):
        super().__init__(connection, config)
        self._neighbor_cache: dict[str, list[str]] = {}

    @property
    def spec(self) -> ContextProviderSpec:
        return ContextProviderSpec(
            name="explored_areas",
            description="Context from agent exploration with tool-based relevance",
            requires_graph=False,  # Uses session data, not graph queries
        )

    def extract_context(self, exploration_steps: list) -> list[ContextItem]:
        """Extract context items from exploration steps.

        Args:
            exploration_steps: List of ExplorationStep objects or dicts from AgentSession

        Returns:
            Context items with relevance-based scores
        """
        if not exploration_steps:
            return []

        # Track best score for each entity
        entity_scores: dict[str, tuple[float, Optional[str], Optional[str]]] = {}

        for step in exploration_steps:
            # Handle both ExplorationStep objects and dicts
            if hasattr(step, "tool_name"):
                tool_name = step.tool_name
                entities = step.entities_discovered
            else:
                tool_name = step.get("tool_name", "")
                entities = step.get("entities_discovered", [])

            # Get base relevance score for this tool
            base_score = get_tool_relevance(tool_name)

            # For search tools, only top results are highly relevant
            if is_search_tool(tool_name):
                # Process top results with full score, others with reduced score
                for i, entity in enumerate(entities):
                    qname = self._extract_qualified_name(entity)
                    if not qname:
                        continue

                    # Top results get full score, others get reduced
                    if i < TOP_RESULTS_LIMIT:
                        score = base_score
                    else:
                        score = base_score * NON_TOP_RESULT_MULTIPLIER

                    self._update_entity_score(entity_scores, qname, score, entity)
            else:
                # Non-search tools: all entities get the same score
                for entity in entities:
                    qname = self._extract_qualified_name(entity)
                    if not qname:
                        continue
                    self._update_entity_score(entity_scores, qname, base_score, entity)

        # Convert to ContextItems
        items = []
        for qname, (score, entity_type, file_path) in entity_scores.items():
            # Skip file: prefix for display if it's a File type
            display_name = qname
            if qname.startswith("file:"):
                display_name = qname[5:]  # Remove "file:" prefix

            # Fetch neighbors from graph
            neighbors = self._fetch_neighbors(display_name, entity_type)

            items.append(
                ContextItem(
                    qualified_name=display_name,
                    entity_type=entity_type or "Unknown",
                    file_path=file_path,
                    score=score,
                    neighbors=neighbors,
                )
            )

        log.info(
            f"ExploredAreasProvider: extracted {len(items)} context items "
            f"from {len(exploration_steps)} exploration steps"
        )
        return items

    def _extract_qualified_name(self, entity: Union[str, dict]) -> Optional[str]:
        """Extract qualified name from entity (string or dict)."""
        if isinstance(entity, str):
            return entity
        if isinstance(entity, dict):
            return entity.get("qualified_name")
        return None

    def _update_entity_score(
        self,
        entity_scores: dict,
        qname: str,
        score: float,
        entity: Union[str, dict],
    ) -> None:
        """Update entity score, keeping the highest score."""
        current = entity_scores.get(qname)
        if current is None or score > current[0]:
            entity_type = self._infer_type(entity)
            file_path = self._infer_file(entity)
            entity_scores[qname] = (score, entity_type, file_path)

    def _infer_type(self, entity: Union[str, dict]) -> Optional[str]:
        """Infer entity type from entity data."""
        if isinstance(entity, dict):
            return entity.get("type") or entity.get("entity_type")
        # Try to infer from qualified name pattern
        if isinstance(entity, str):
            if "." in entity:
                parts = entity.split(".")
                # If last part starts with uppercase, likely a class
                if parts[-1] and parts[-1][0].isupper():
                    return "Class"
            return "Function"  # Default assumption
        return None

    def _infer_file(self, entity: Union[str, dict]) -> Optional[str]:
        """Infer file path from entity data."""
        if isinstance(entity, dict):
            return entity.get("file_path") or entity.get("path")
        return None

    def _fetch_neighbors(
        self, qualified_name: str, entity_type: Optional[str], limit: int = 5
    ) -> list[str]:
        """Fetch neighbors (callers/callees) from the graph.

        Args:
            qualified_name: The entity's qualified name
            entity_type: The entity type (Function, Class, File)
            limit: Maximum number of neighbors to return

        Returns:
            List of neighbor qualified names
        """
        # Check cache first
        if qualified_name in self._neighbor_cache:
            return self._neighbor_cache[qualified_name]

        # Files don't have caller/callee relationships in the same way
        if entity_type == "File" or not self.connection:
            self._neighbor_cache[qualified_name] = []
            return []

        neighbors = []
        try:
            conn = self.connection.connect()

            # Query for callers and callees
            if entity_type in ("Function", "Class"):
                # Get callees (what this entity calls)
                callees_query = f"""
                    MATCH (n:{entity_type} {{qualified_name: $qname}})-[:CALLS]->(m)
                    RETURN m.qualified_name
                    LIMIT $limit
                """
                result = conn.execute(callees_query, {"qname": qualified_name, "limit": limit})
                while result.has_next():
                    row = result.get_next()
                    if row[0]:
                        neighbors.append(row[0])

                # Get callers (what calls this entity)
                remaining = limit - len(neighbors)
                if remaining > 0:
                    callers_query = f"""
                        MATCH (n)-[:CALLS]->(m:{entity_type} {{qualified_name: $qname}})
                        RETURN n.qualified_name
                        LIMIT $limit
                    """
                    result = conn.execute(callers_query, {"qname": qualified_name, "limit": remaining})
                    while result.has_next():
                        row = result.get_next()
                        if row[0] and row[0] not in neighbors:
                            neighbors.append(row[0])

        except Exception as e:
            log.debug(f"Failed to fetch neighbors for {qualified_name}: {e}")

        self._neighbor_cache[qualified_name] = neighbors
        return neighbors


# Auto-register provider
ContextProviderRegistry.register("explored_areas", ExploredAreasProvider)
