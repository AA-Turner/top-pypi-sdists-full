"""Tests for cycle detection utility."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.cycle_detection import CycleDetectedError, detect_cycles


class TestDetectCycles:
    """Verify DFS-based cycle detection and topological sort."""

    def test_simple_dag_returns_sorted_order(self):
        edges = [("A", "B"), ("B", "C")]
        result = detect_cycles(edges)
        assert result.index("A") < result.index("B")
        assert result.index("B") < result.index("C")

    def test_no_edges_returns_empty(self):
        result = detect_cycles([])
        assert result == []

    def test_simple_cycle_raises(self):
        edges = [("A", "B"), ("B", "C"), ("C", "A")]
        with pytest.raises(CycleDetectedError) as exc_info:
            detect_cycles(edges)
        assert "Circular dependency detected" in str(exc_info.value)
        assert len(exc_info.value.cycle) >= 3

    def test_self_loop_raises(self):
        edges = [("A", "A")]
        with pytest.raises(CycleDetectedError):
            detect_cycles(edges)

    def test_complex_dag_no_cycle(self):
        edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
        result = detect_cycles(edges)
        assert result.index("A") < result.index("B")
        assert result.index("A") < result.index("C")
        assert result.index("B") < result.index("D")
        assert result.index("C") < result.index("D")

    def test_complex_cycle_detected(self):
        edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "B")]
        with pytest.raises(CycleDetectedError) as exc_info:
            detect_cycles(edges)
        cycle = exc_info.value.cycle
        assert len(cycle) >= 3

    def test_performance_50_nodes_100_edges(self):
        """Verify detection returns a valid topological order for 50 nodes / 100 edges."""
        # Build a DAG with 50 nodes and ~100 edges
        edges = []
        for i in range(50):
            for j in range(i + 1, min(i + 3, 50)):
                edges.append((f"N{i}", f"N{j}"))
        edges = edges[:100]

        result = detect_cycles(edges)

        # All nodes must appear in the result
        all_nodes = {n for e in edges for n in e}
        assert set(result) == all_nodes

        # Every edge must be ordered correctly (source before target)
        result_index = {n: i for i, n in enumerate(result)}
        for source, target in edges:
            assert result_index[source] < result_index[target]

    def test_disconnected_components(self):
        edges = [("A", "B"), ("C", "D")]
        result = detect_cycles(edges)
        assert set(result) == {"A", "B", "C", "D"}
