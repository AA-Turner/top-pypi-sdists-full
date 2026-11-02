"""Tests for ``build_combined_graph`` (FR-014, FR-015, issue #2118)."""

from __future__ import annotations

from agentic_devtools.epic_tree.dependencies import build_combined_graph
from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, SubtaskNode


def _tree_with_blocking() -> EpicTree:
    s1 = SubtaskNode(ref="s1", title="S1", body="", blockedBy=("s2",))
    s2 = SubtaskNode(ref="s2", title="S2", body="")
    f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1, s2))
    epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
    return EpicTree(schemaVersion="1.0", epic=epic)


class TestBuildCombinedGraph:
    def test_combines_hierarchy_and_blocking(self):
        tree = _tree_with_blocking()
        graph = build_combined_graph(tree)
        # Hierarchy: e1 -> f1 -> {s1, s2}
        assert "f1" in graph["e1"]
        assert {"s1", "s2"} <= graph["f1"]
        # Blocking: s2 blocks s1 (s2 -> s1)
        assert "s1" in graph["s2"]
