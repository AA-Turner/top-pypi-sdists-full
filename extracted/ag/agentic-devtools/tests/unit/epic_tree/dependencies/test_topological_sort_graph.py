"""Tests for ``topological_sort_graph`` (FR-003, FR-004, issue #2118)."""

from __future__ import annotations

import pytest

from agentic_devtools.epic_tree.dependencies import (
    build_combined_graph,
    topological_sort_graph,
)
from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, SubtaskNode
from agentic_devtools.epic_tree.ordering import creation_sequence


def _tree_with_blocking() -> EpicTree:
    s1 = SubtaskNode(ref="s1", title="S1", body="", blockedBy=("s2",))
    s2 = SubtaskNode(ref="s2", title="S2", body="")
    f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1, s2))
    epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
    return EpicTree(schemaVersion="1.0", epic=epic)


class TestTopologicalSortGraph:
    def test_orders_blocker_before_blocked(self):
        tree = _tree_with_blocking()
        graph = build_combined_graph(tree)
        order = topological_sort_graph(graph, creation_sequence(tree))
        refs = [node.ref for node in order]
        assert refs.index("e1") < refs.index("f1")
        assert refs.index("f1") < refs.index("s1")
        assert refs.index("f1") < refs.index("s2")
        # s2 blocks s1, so s2 precedes s1.
        assert refs.index("s2") < refs.index("s1")

    def test_deterministic_across_calls(self):
        tree = _tree_with_blocking()
        graph = build_combined_graph(tree)
        seq = creation_sequence(tree)
        first = topological_sort_graph(graph, seq)
        second = topological_sort_graph(graph, seq)
        assert first == second

    def test_uses_creation_sequence_position_as_tiebreak(self):
        # Two independent siblings — order must follow creation-sequence order.
        graph = {"f1": set(), "f2": set()}
        nodes = [
            FeatureNode(ref="f1", title="F1", body="", subtasks=()),
            FeatureNode(ref="f2", title="F2", body="", subtasks=()),
        ]
        assert topological_sort_graph(graph, nodes) == nodes
        reversed_nodes = [nodes[1], nodes[0]]
        assert topological_sort_graph(graph, reversed_nodes) == reversed_nodes

    def test_accepts_issue_nodes_in_sequence(self):
        tree = _tree_with_blocking()
        graph = build_combined_graph(tree)
        order = topological_sort_graph(graph, list(creation_sequence(tree)))
        assert {node.ref for node in order} == {"e1", "f1", "s1", "s2"}

    def test_raises_on_cycle_reporting_all(self):
        graph = {"s1": {"s2"}, "s2": {"s1"}, "s3": {"s4"}, "s4": {"s3"}}
        with pytest.raises(ValueError) as exc_info:
            nodes = [SubtaskNode(ref=ref, title=ref, body="") for ref in graph]
            topological_sort_graph(graph, nodes)
        message = str(exc_info.value)
        # Every cycle is reported.
        assert "s1" in message and "s2" in message
        assert "s3" in message and "s4" in message

    def test_nodes_absent_from_graph_are_not_dropped(self):
        # graph only mentions f1; f2 is absent from graph but present in sequence.
        # Both nodes must appear in the result.
        graph: dict[str, set[str]] = {"f1": set()}
        nodes = [
            FeatureNode(ref="f1", title="F1", body="", subtasks=()),
            FeatureNode(ref="f2", title="F2", body="", subtasks=()),
        ]
        result = topological_sort_graph(graph, nodes)
        assert {n.ref for n in result} == {"f1", "f2"}

    def test_refs_absent_from_sequence_use_fallback_position(self):
        graph = {"s1": {"s2"}, "s2": set()}
        # "s2" is not in creation sequence, so no node can be returned for it.
        node = SubtaskNode(ref="s1", title="S1", body="")
        with pytest.raises(ValueError, match="absent"):
            topological_sort_graph(graph, [node])
