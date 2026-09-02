"""Tests for topological_sort function."""

from unittest.mock import patch

import pytest

from agentic_devtools.epic_tree.dependencies import topological_sort
from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, SubtaskNode


class TestTopologicalSort:
    """Tests for global topological ordering."""

    def test_respects_dependencies(self):
        """Blocker appears before blocked in result."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        assert refs.index("f1") < refs.index("f2")

    def test_tiebreak_by_creation_sequence(self):
        """Nodes with equal in-degree use creation-sequence order as tiebreak."""
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        # creation sequence: e1, f1, f2
        assert refs == ["e1", "f1", "f2"]

    def test_all_nodes_included(self):
        """All nodes appear in result, including those without edges."""
        s1 = SubtaskNode(ref="s1", title="S1", body="")
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=(s1,))
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        assert set(refs) == {"e1", "f1", "s1"}

    def test_deterministic_output(self):
        """Same tree produces same order across 100 invocations."""
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        f3 = FeatureNode(ref="f3", title="F3", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2, f3))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        expected = [n.ref for n in topological_sort(tree)]
        for _ in range(100):
            assert [n.ref for n in topological_sort(tree)] == expected

    def test_complex_dependency_chain(self):
        """Complex chain: e1 → f1 → f2 → s1."""
        s1 = SubtaskNode(ref="s1", title="S1", body="", blockedBy=("f2",))
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=(s1,))
        epic = EpicNode(ref="e1", title="E1", body="", blocks=("f1",), features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        assert refs.index("e1") < refs.index("f1")
        assert refs.index("f1") < refs.index("f2")
        assert refs.index("f2") < refs.index("s1")

    def test_node_blocks_multiple_others(self):
        """Node blocking multiple others correctly decrements in-degrees."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2", "f3"), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        f3 = FeatureNode(ref="f3", title="F3", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2, f3))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        assert refs.index("f1") < refs.index("f2")
        assert refs.index("f1") < refs.index("f3")

    def test_in_degree_not_zero_after_decrement(self):
        """Neighbor with multiple blockers not enqueued until all resolved."""
        # f3 is blocked by both f1 and f2 - in_degree stays > 0 after first decrement
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f3",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", blocks=("f3",), subtasks=())
        f3 = FeatureNode(ref="f3", title="F3", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2, f3))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        assert refs.index("f1") < refs.index("f3")
        assert refs.index("f2") < refs.index("f3")

    def test_globally_optimal_tiebreak(self):
        """A node freed later but with higher creation-sequence priority beats
        a lower-priority node already sitting in the queue.

        Creation order: epic(0), f1(1), f2(2), f3(3), f4(4), f5(5).
        Edges: f1→f4, f1→f5, f4→f2, f5→f3.
        After processing f4, f2 (priority 2) is freed while f5 (priority 5) is
        still in the queue.  A deque-based per-batch sort yields [..., f4, f5, f2, ...]
        because f2 is appended after f5.  The correct heap-based sort yields
        [..., f4, f2, f5, ...] because f2 has global priority 2 < 5.
        """
        s1 = SubtaskNode(ref="f2", title="F2", body="")
        s2 = SubtaskNode(ref="f3", title="F3", body="")
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f4", "f5"), subtasks=())
        f4 = FeatureNode(ref="f4", title="F4", body="", blocks=("f2",), subtasks=(s1,))
        f5 = FeatureNode(ref="f5", title="F5", body="", blocks=("f3",), subtasks=(s2,))
        epic = EpicNode(ref="epic", title="Epic", body="", features=(f1, f4, f5))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        # Dependency constraints
        assert refs.index("f1") < refs.index("f4")
        assert refs.index("f1") < refs.index("f5")
        assert refs.index("f4") < refs.index("f2")
        assert refs.index("f5") < refs.index("f3")
        # Tiebreak: f2 (creation index 2) before f5 (creation index 5) because
        # once f4 is processed both f2 and f5 are available and f2 has the lower
        # creation index (higher precedence in the global ordering).
        assert refs.index("f2") < refs.index("f5")

    def test_raises_on_cycle(self):
        """Cyclic dependency graph raises a clear error with cycle chain."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blockedBy=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", blockedBy=("f1",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)

        with pytest.raises(ValueError, match="cycle") as exc_info:
            topological_sort(tree)
        message = str(exc_info.value)
        assert "→" in message
        assert "f1" in message
        assert "f2" in message

    def test_cycle_error_contains_arrow_chain(self):
        """ValueError message contains →-separated cycle chain."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", blocks=("f3",), subtasks=())
        f3 = FeatureNode(ref="f3", title="F3", body="", blockedBy=(), blocks=("f1",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2, f3))
        tree = EpicTree(schemaVersion="1.0", epic=epic)

        with pytest.raises(ValueError) as exc_info:
            topological_sort(tree)
        message = str(exc_info.value)
        # Must contain arrow-separated chain
        assert " → " in message

    def test_order_field_tiebreaker(self):
        """Nodes with explicit order precede unordered nodes (FR-005)."""
        # fx: no order, positional index 1; fy: order=1, positional index 2;
        # fz: no order, positional index 3; e1: no order, positional index 0
        # Tiebreaker keys: fy=(1,2), e1=(inf,0), fx=(inf,1), fz=(inf,3)
        # Expected order: fy first among features (explicit order=1 beats inf)
        f_x = FeatureNode(ref="fx", title="FX", body="", subtasks=())
        f_y = FeatureNode(ref="fy", title="FY", body="", order=1, subtasks=())
        f_z = FeatureNode(ref="fz", title="FZ", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f_x, f_y, f_z))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        assert refs.index("fy") < refs.index("fx")
        assert refs.index("fy") < refs.index("fz")

    def test_mixed_order_and_no_order(self):
        """Mixed order/no-order nodes resolve correctly per FR-005."""
        f1 = FeatureNode(ref="f1", title="F1", body="", order=2, subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        f3 = FeatureNode(ref="f3", title="F3", body="", order=1, subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2, f3))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        # f3 has order=1, f1 has order=2, both before f2 (no order) and e1 (no order)
        assert refs.index("f3") < refs.index("f1")
        assert refs.index("f3") < refs.index("f2")
        assert refs.index("f1") < refs.index("f2")

    def test_single_node_no_deps(self):
        """Single node produces one-element list."""
        epic = EpicNode(ref="e1", title="E1", body="", features=())
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        assert [n.ref for n in result] == ["e1"]

    def test_fully_linear_chain(self):
        """Fully linear chain produces exact order."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", blocks=("f3",), subtasks=())
        f3 = FeatureNode(ref="f3", title="F3", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", blocks=("f1",), features=(f1, f2, f3))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        assert refs.index("e1") < refs.index("f1")
        assert refs.index("f1") < refs.index("f2")
        assert refs.index("f2") < refs.index("f3")

    def test_diamond_pattern(self):
        """Diamond: A blocks B,C; B,C block D."""
        f_a = FeatureNode(ref="fa", title="FA", body="", blocks=("fb", "fc"), subtasks=())
        f_b = FeatureNode(ref="fb", title="FB", body="", blocks=("fd",), subtasks=())
        f_c = FeatureNode(ref="fc", title="FC", body="", blocks=("fd",), subtasks=())
        f_d = FeatureNode(ref="fd", title="FD", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f_a, f_b, f_c, f_d))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        assert refs.index("fa") < refs.index("fb")
        assert refs.index("fa") < refs.index("fc")
        assert refs.index("fb") < refs.index("fd")
        assert refs.index("fc") < refs.index("fd")

    def test_no_dependencies_matches_creation_sequence(self):
        """No-dependency tree matches creation-sequence order (with tiebreaker)."""
        f1 = FeatureNode(ref="f1", title="F1", body="", subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        f3 = FeatureNode(ref="f3", title="F3", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2, f3))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        result = topological_sort(tree)
        refs = [n.ref for n in result]
        # All have no order → sorted by positional index
        assert refs == ["e1", "f1", "f2", "f3"]

    def test_determinism_10_runs(self):
        """10 identical runs produce byte-identical ref-list serializations (NFR-002)."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", subtasks=())
        f3 = FeatureNode(ref="f3", title="F3", body="", subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2, f3))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        expected = [n.ref for n in topological_sort(tree)]
        for _ in range(10):
            assert [n.ref for n in topological_sort(tree)] == expected

    def test_cycle_error_unknown_when_detect_cycles_empty(self):
        """Fallback 'unknown cycle' when detect_cycles returns empty (defensive)."""
        f1 = FeatureNode(ref="f1", title="F1", body="", blocks=("f2",), subtasks=())
        f2 = FeatureNode(ref="f2", title="F2", body="", blocks=("f1",), subtasks=())
        epic = EpicNode(ref="e1", title="E1", body="", features=(f1, f2))
        tree = EpicTree(schemaVersion="1.0", epic=epic)

        with patch("agentic_devtools.epic_tree.dependencies.detect_cycles", return_value=[]):
            with pytest.raises(ValueError, match="unknown cycle"):
                topological_sort(tree)
