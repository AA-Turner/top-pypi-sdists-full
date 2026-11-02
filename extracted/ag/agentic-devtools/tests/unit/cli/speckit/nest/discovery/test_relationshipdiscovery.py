"""Tests for RelationshipDiscovery dataclass in nest/discovery.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.nest.discovery import ChildRef, RelationshipDiscovery


class TestRelationshipDiscovery:
    """Tests for the RelationshipDiscovery dataclass."""

    def test_defaults_to_empty_graph_and_warnings(self) -> None:
        """Default-constructed instance has empty graph and warnings."""
        rd = RelationshipDiscovery()
        assert rd.graph == {}
        assert rd.warnings == []

    def test_stores_provided_graph_and_warnings(self) -> None:
        """Provided values are stored correctly."""
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {1: (None, [ChildRef(number=2, title="child")])}
        warnings = ["something ambiguous"]
        rd = RelationshipDiscovery(graph=graph, warnings=warnings)
        assert rd.graph == graph
        assert rd.warnings == warnings
