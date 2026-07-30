from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from datahub.ingestion.graph.client import DataHubGraph
from datahub.utilities.str_enum import StrEnum


class TraverseDirection(StrEnum):
    OUTGOING = "OUTGOING"
    INCOMING = "INCOMING"
    UNDIRECTED = "UNDIRECTED"


class TraverseLineageDirection(StrEnum):
    UPSTREAM = "UPSTREAM"
    DOWNSTREAM = "DOWNSTREAM"
    BOTH = "BOTH"


@dataclass
class TraversedRelationship:
    relationship_type: str
    entity_type: str
    urn: str
    degree: int
    degrees: Optional[List[int]] = None
    direction_mode: Optional[str] = None
    transitive: bool = False
    reverse_display_name: Optional[str] = None


@dataclass
class TraverseResult:
    count: int
    total: int
    relationships: List[TraversedRelationship] = field(default_factory=list)
    partial: Optional[bool] = None


# Add other graph mixins here when applicable
class AcrylGraph(DataHubGraph):
    def traverse_relationships(
        self,
        *,
        urn: str,
        relationship_types: Optional[List[str]] = None,
        direction: TraverseDirection = TraverseDirection.OUTGOING,
        max_hops: int = 1,
        entity_types: Optional[List[str]] = None,
        include_lineage: bool = False,
        lineage_direction: Optional[TraverseLineageDirection] = None,
        resolve_equivalents: bool = False,
    ) -> TraverseResult:
        """Multi-hop relationship walk via the OpenAPI v3 /relationship/traverse endpoint.

        Walks the graph from ``urn`` up to ``max_hops`` hops over an arbitrary set of
        relationship types -- built-in names (e.g. ``DownstreamOf``) and/or
        relationshipType URNs (e.g. ``urn:li:relationshipType:governedBy``)
        traversed uniformly. A structuredProperty URN (e.g.
        ``urn:li:structuredProperty:governedBy``) is also accepted and resolves to
        the relationshipType its settings point at. Unlike ``get_related_entities``
        (single-hop), this walk is transitive.

        Args:
            urn: The start entity of the walk.
            relationship_types: Relationship types to traverse. Required unless
                ``include_lineage`` is True.
            direction: Traversal direction (OUTGOING / INCOMING / UNDIRECTED).
            max_hops: Maximum traversal depth (server enforces 1-20).
            entity_types: Optional constraint on the entity types visited.
            include_lineage: When True, also traverse the full native-lineage edge set
                in the same walk, without enumerating lineage relationship types.
            lineage_direction: Lineage direction to include when ``include_lineage``
                is True (UPSTREAM / DOWNSTREAM / BOTH); server defaults to BOTH.
            resolve_equivalents: When True, a requested type that is a
                standard-vocabulary predicate a relationship declares itself
                equivalent to (e.g. ``skos:broader``) is expanded to the
                relationship-type URN(s) that declared it before traversal.

        Returns:
            A TraverseResult with every entity reached (the endpoint is unpaginated;
            the walk is bounded only by the server's impact maxRelations/timeout
            limits, surfaced via ``partial``), its hop distance (``degree``, per-path
            ``degrees``), and the resolved relationship-type semantics
            (``direction_mode``, ``transitive``, ``reverse_display_name``).
        """
        params: Dict[str, Any] = {
            "urn": urn,
            "direction": direction.value,
            "maxHops": max_hops,
        }
        if relationship_types:
            params["relationshipTypes"] = relationship_types
        if entity_types:
            params["entityTypes"] = entity_types
        if include_lineage:
            params["includeLineage"] = "true"
            if lineage_direction is not None:
                params["lineageDirection"] = lineage_direction.value
        if resolve_equivalents:
            params["resolveEquivalents"] = "true"

        response = self._get_generic(
            url=f"{self._gms_server}/openapi/v3/relationship/traverse", params=params
        )
        relationships = [
            TraversedRelationship(
                relationship_type=rel["relationshipType"],
                entity_type=rel["entityType"],
                urn=rel["urn"],
                degree=rel["degree"],
                degrees=rel.get("degrees"),
                direction_mode=rel.get("directionMode"),
                transitive=rel.get("transitive", False),
                reverse_display_name=rel.get("reverseDisplayName"),
            )
            for rel in response.get("relationships", [])
        ]
        return TraverseResult(
            count=response.get("count", 0),
            total=response.get("total", 0),
            relationships=relationships,
            partial=response.get("partial"),
        )
