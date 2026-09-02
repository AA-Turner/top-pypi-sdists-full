"""Tests for shared/hierarchy.py re-export adapter."""

from __future__ import annotations

from agentic_devtools.cli.speckit.shared.hierarchy import (
    HierarchyNode,
    load_hierarchy,
    save_hierarchy,
)


class TestHierarchyAdapter:
    """Tests for the hierarchy adapter re-exports."""

    def test_load_hierarchy_is_callable(self) -> None:
        """Test that load_hierarchy is properly re-exported."""
        assert callable(load_hierarchy)

    def test_save_hierarchy_is_callable(self) -> None:
        """Test that save_hierarchy is properly re-exported."""
        assert callable(save_hierarchy)

    def test_hierarchy_node_is_importable(self) -> None:
        """Test that HierarchyNode class is re-exported."""
        assert HierarchyNode is not None
