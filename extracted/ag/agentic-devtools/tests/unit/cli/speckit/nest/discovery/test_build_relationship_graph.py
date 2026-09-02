"""Tests for build_relationship_graph in nest/discovery.py."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.nest.discovery import (
    ChildRef,
    FlatSpec,
    RelationshipDiscovery,
    build_relationship_graph,
)


def _make_spec(number: int) -> FlatSpec:
    return FlatSpec(issue_number=number, path=Path(f"/specs/{number}-slug"), slug="slug")


def _metadata(
    parent: int | None,
    children: list[SimpleNamespace] | None = None,
    informational_children: list[SimpleNamespace] | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        parent=parent,
        children=children or [],
        informational_children=informational_children or [],
    )


def _child(number: int, title: str = "", order: int | None = None) -> SimpleNamespace:
    return SimpleNamespace(number=number, title=title or f"Issue #{number}", order=order)


class TestBuildRelationshipGraph:
    """Tests for build_relationship_graph."""

    def test_returns_empty_discovery_for_empty_input(self) -> None:
        """Empty flat_specs list produces an empty RelationshipDiscovery."""
        result = build_relationship_graph("owner", "repo", [])
        assert isinstance(result, RelationshipDiscovery)
        assert result.graph == {}
        assert result.warnings == []

    def test_builds_graph_from_single_spec_no_parent_no_children(self) -> None:
        """A standalone issue is stored with parent=None and no children."""
        spec = _make_spec(100)
        meta = _metadata(parent=None)

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.build_metadata.return_value = meta
            result = build_relationship_graph("owner", "repo", [spec])

        assert result.graph == {100: (None, [])}
        assert result.warnings == []

    def test_builds_graph_with_parent_and_children(self) -> None:
        """Parent/child relationships populate the graph correctly."""
        specs = [_make_spec(100), _make_spec(101)]
        meta_100 = _metadata(parent=None, children=[_child(101, "Child issue", order=0)])
        meta_101 = _metadata(parent=100)

        side_effects = [meta_100, meta_101]

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.build_metadata.side_effect = side_effects
            result = build_relationship_graph("owner", "repo", specs)

        assert result.graph[100] == (None, [ChildRef(number=101, title="Child issue", order=0)])
        assert result.graph[101] == (100, [])
        assert result.warnings == []

    def test_records_warning_and_skips_spec_on_404(self) -> None:
        """A 404-like exception causes the spec to be skipped with a warning."""
        spec = _make_spec(200)

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.build_metadata.side_effect = RuntimeError("HTTP 404")
            result = build_relationship_graph("owner", "repo", [spec])

        assert 200 not in result.graph
        assert len(result.warnings) == 1
        assert "#200" in result.warnings[0]

    def test_records_warning_for_not_found_text(self) -> None:
        """A 'not found' exception also triggers the skipping warning."""
        spec = _make_spec(201)

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.build_metadata.side_effect = RuntimeError("issue not found")
            result = build_relationship_graph("owner", "repo", [spec])

        assert 201 not in result.graph
        assert any("201" in w for w in result.warnings)

    def test_propagates_non_404_exception(self) -> None:
        """Non-404 exceptions are re-raised without any warning."""
        spec = _make_spec(300)

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.build_metadata.side_effect = RuntimeError("permission denied")
            with pytest.raises(RuntimeError, match="permission denied"):
                build_relationship_graph("owner", "repo", [spec])

    def test_propagates_repo_level_404(self) -> None:
        """A repo-level 404 from validate_repository_access is propagated."""
        spec = _make_spec(400)

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.validate_repository_access.side_effect = RuntimeError(
                "Repository 'owner/nonexistent' is inaccessible or does not exist."
            )
            with pytest.raises(RuntimeError, match="inaccessible"):
                build_relationship_graph("owner", "nonexistent", [spec])

    def test_batches_specs_in_groups_of_batch_size(self) -> None:
        """Specs are processed in bounded batches (all complete)."""
        # Create BATCH_SIZE + 2 specs to span two batches.
        from agentic_devtools.cli.speckit.nest.discovery import BATCH_SIZE

        specs = [_make_spec(i) for i in range(BATCH_SIZE + 2)]
        meta = _metadata(parent=None)

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.build_metadata.return_value = meta
            result = build_relationship_graph("owner", "repo", specs)

        assert len(result.graph) == BATCH_SIZE + 2

    def test_deduplicates_children_and_uses_position_when_order_is_none(self) -> None:
        """Duplicate children are deduplicated; None order is replaced by position."""
        spec = _make_spec(10)
        # Two children: first with explicit order, second with order=None (ambiguous).
        # Also a duplicate of the first child that must be skipped.
        c1 = _child(11, "Alpha", order=5)
        c2 = _child(12, "Beta", order=None)
        c_dup = _child(11, "Alpha duplicate", order=None)
        meta = _metadata(parent=None, children=[c1, c2, c_dup])

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.build_metadata.return_value = meta
            result = build_relationship_graph("owner", "repo", [spec])

        children = result.graph[10][1]
        numbers = [c.number for c in children]
        assert numbers == [11, 12]
        # c1 keeps its explicit order=5; c2 gets position 1 (it's index 1 after dedup).
        assert children[0].order == 5
        assert children[1].order == 1
        # Ordering-ambiguous warning should fire for c2 when total children > 1.
        assert any("10" in w and "order" in w.lower() for w in result.warnings)

    def test_no_ordering_warning_when_single_child_has_none_order(self) -> None:
        """A single child with order=None does not emit an ordering warning."""
        spec = _make_spec(10)
        meta = _metadata(parent=None, children=[_child(11, "Only child", order=None)])

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.build_metadata.return_value = meta
            result = build_relationship_graph("owner", "repo", [spec])

        assert result.warnings == []

    def test_excludes_informational_children_from_graph(self) -> None:
        """Informational children (depth-capped) are NOT added to graph edges.

        They remain flat and must not appear in hierarchy.yml, so they must not
        be present in the relationship graph at all.
        """
        spec = _make_spec(20)
        direct = [_child(21, "Direct", order=0)]
        informational = [_child(22, "Informational", order=1)]
        meta = _metadata(parent=None, children=direct, informational_children=informational)

        with patch("agentic_devtools.cli.speckit.nest.discovery.GitHubHierarchyDetector") as MockDetector:
            MockDetector.return_value.build_metadata.return_value = meta
            result = build_relationship_graph("owner", "repo", [spec])

        numbers = [c.number for c in result.graph[20][1]]
        assert numbers == [21]
