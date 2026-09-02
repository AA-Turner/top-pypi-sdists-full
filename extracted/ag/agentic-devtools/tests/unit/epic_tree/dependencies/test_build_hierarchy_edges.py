"""Tests for ``build_hierarchy_edges`` (FR-005, issue #2118)."""

from __future__ import annotations

from agentic_devtools.epic_tree.dependencies import build_hierarchy_edges
from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, SubtaskNode


def _tree_with_blocking() -> EpicTree:
    s1 = SubtaskNode(ref="s1", title="S1", body="", blockedBy=("s2",))
    s2 = SubtaskNode(ref="s2", title="S2", body="")
    f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1, s2))
    epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
    return EpicTree(schemaVersion="1.0", epic=epic)


class TestBuildHierarchyEdges:
    def test_parent_before_child_edges(self):
        tree = _tree_with_blocking()
        edges = build_hierarchy_edges(tree)
        assert "f1" in edges["e1"]
        assert "s1" in edges["f1"]
        assert "s2" in edges["f1"]
        # Leaves have no children.
        assert edges["s1"] == set()
