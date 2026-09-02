"""Tests for detect_cycles function."""

import os

import pytest

from agentic_devtools.epic_tree.dependencies import _canonicalize_cycle, detect_cycles


class TestDetectCycles:
    """Tests for cycle detection in dependency graphs."""

    def test_empty_graph(self):
        """Empty graph returns empty list."""
        assert detect_cycles({}) == []

    def test_no_cycle(self):
        """Acyclic graph returns empty list."""
        graph = {"a": {"b"}, "b": {"c"}, "c": set()}
        assert detect_cycles(graph) == []

    def test_self_loop(self):
        """Self-loop returns [['a', 'a']]."""
        graph = {"a": {"a"}}
        assert detect_cycles(graph) == [["a", "a"]]

    def test_two_node_cycle(self):
        """Two-node cycle returns closed chain rotated to smallest ref."""
        graph = {"a": {"b"}, "b": {"a"}}
        result = detect_cycles(graph)
        assert len(result) == 1
        chain = result[0]
        assert chain[0] == chain[-1]  # Closed
        assert chain[0] == "a"  # Rotated to smallest
        assert set(chain[:-1]) == {"a", "b"}

    def test_three_node_cycle(self):
        """Three-node cycle returns canonically rotated and directed chain."""
        graph = {"a": {"b"}, "b": {"c"}, "c": {"a"}}
        result = detect_cycles(graph)
        assert len(result) == 1
        chain = result[0]
        assert chain[0] == chain[-1]  # Closed
        assert chain[0] == "a"  # Rotated to smallest
        assert len(chain) == 4  # 3 nodes + closing

    def test_two_disjoint_cycles(self):
        """Two disjoint cycles return two chains sorted lexicographically."""
        graph = {
            "a": {"b"},
            "b": {"a"},
            "c": {"d"},
            "d": {"e"},
            "e": {"c"},
        }
        result = detect_cycles(graph)
        assert len(result) == 2
        # First chain should start with 'a' (lex smaller than 'c')
        assert result[0][0] == "a"
        assert result[1][0] == "c"

    def test_scc_selects_lexicographically_smallest_canonical_cycle(self):
        """SCC with multiple simple cycles returns exact smallest canonical representative.

        Graph has two distinct cycles within one SCC:
          - a→b→c→a  (lex chain: ['a', 'b', 'c', 'a'])
          - a→c→a    (lex chain: ['a', 'c', 'a'])

        DFS from 'a' (lex-smallest) with sorted neighbors follows 'b' first,
        yielding a→b→c→a. After canonicalization the result is ['a', 'b', 'c', 'a'],
        which is lex-smaller than ['a', 'c', 'a'] because 'b' < 'c'.
        """
        graph = {"a": {"b", "c"}, "b": {"c"}, "c": {"a"}}
        result = detect_cycles(graph)
        assert result == [["a", "b", "c", "a"]]

    def test_determinism(self):
        """10 identical runs produce identical output (NFR-002)."""
        graph = {"a": {"b"}, "b": {"c"}, "c": {"a"}, "d": {"e"}, "e": {"d"}}
        expected = detect_cycles(graph)
        for _ in range(10):
            assert detect_cycles(graph) == expected

    def test_non_cycle_ancestors_excluded(self):
        """Ancestors that lead into a cycle are not included in results."""
        # c -> a, a <-> b forms cycle; c is not part of cycle
        graph = {"a": {"b"}, "b": {"a"}, "c": {"a"}, "d": set()}
        result = detect_cycles(graph)
        assert len(result) == 1
        chain = result[0]
        all_refs_in_chains = set(chain[:-1])  # Exclude closing element
        assert "c" not in all_refs_in_chains
        assert "d" not in all_refs_in_chains

    def test_cycle_with_non_participating_nodes(self):
        """Only cycle participants are returned in chains."""
        graph = {"a": {"b"}, "b": {"a"}, "c": {"a"}, "d": set()}
        result = detect_cycles(graph)
        assert len(result) == 1
        # Only a and b form the cycle
        assert set(result[0][:-1]) == {"a", "b"}

    def test_node_with_black_neighbor(self):
        """DFS correctly skips already-explored neighbors."""
        graph = {"a": set(), "b": {"a"}, "c": {"b"}}
        result = detect_cycles(graph)
        assert result == []

    def test_cycle_detected_after_non_cycle_neighbor(self):
        """Cycle detected when node has mix of non-cycle and cycle neighbors."""
        graph = {"a": {"b", "c"}, "b": set(), "c": {"a"}}
        result = detect_cycles(graph)
        assert len(result) == 1
        assert set(result[0][:-1]) == {"a", "c"}

    def test_dfs_backtracks_when_branch_exhausted_in_scc(self):
        """DFS backtracks correctly when a branch dead-ends within the SCC.

        Graph: a→b, b→c, b→d, c→b, d→a
        All four nodes form one SCC. DFS from 'a' first follows 'b'→'c',
        but 'c' only leads back to 'b' (already visited), so DFS backtracks
        from 'c' to 'b' and then follows 'b'→'d'→'a' to find the cycle.
        """
        graph = {"a": {"b"}, "b": {"c", "d"}, "c": {"b"}, "d": {"a"}}
        result = detect_cycles(graph)
        assert len(result) == 1
        chain = result[0]
        assert chain[0] == chain[-1]  # Closed
        assert chain[0] == "a"  # Rotated to smallest ref
        assert all(node in {"a", "b", "c", "d"} for node in chain[:-1])
        # Every consecutive pair in the chain must have an edge in the graph
        for i in range(len(chain) - 1):
            assert chain[i + 1] in graph[chain[i]], f"No edge from {chain[i]!r} → {chain[i + 1]!r} in graph"


class TestCanonicalizeCycle:
    """Tests for the _canonicalize_cycle helper."""

    def test_self_loop_returned_unchanged(self):
        """A self-loop chain (length <= 2) is returned as-is (line 70 coverage)."""
        assert _canonicalize_cycle(["a", "a"]) == ["a", "a"]

    def test_single_element_returned_unchanged(self):
        """Single-element chain returned as-is."""
        assert _canonicalize_cycle(["x"]) == ["x"]

    def test_direction_preserved_not_reversed(self):
        """Canonicalization preserves edge direction; reversal must not be chosen.

        For directed cycle a→c→b→a the only valid closed chain starting at 'a'
        is ['a', 'c', 'b', 'a'].  An earlier implementation also compared with
        the reversed chain (['a', 'b', 'c', 'a']), which is lex-smaller but
        invalid because edges a→b and b→c do not exist.
        """
        graph = {"a": {"c"}, "c": {"b"}, "b": {"a"}}
        result = detect_cycles(graph)
        assert len(result) == 1
        chain = result[0]
        # Every hop must be a real edge
        for i in range(len(chain) - 1):
            assert chain[i + 1] in graph[chain[i]], f"No edge from {chain[i]!r} → {chain[i + 1]!r} in graph"


class TestDetectCyclesBenchmark:
    """Benchmark smoke test gated by env var."""

    def test_500_node_1000_edge_performance(self):
        """NFR-001: 500-node/1000-edge graph completes in < 1000ms."""
        if not os.environ.get("AGDT_RUN_BENCHMARK_SMOKE") == "1":
            pytest.skip("Set AGDT_RUN_BENCHMARK_SMOKE=1 to run this benchmark")

        import time

        # Build a 500-node graph with 1000 edges (acyclic)
        nodes = [f"node-{i:04d}" for i in range(500)]
        graph: dict[str, set[str]] = {n: set() for n in nodes}
        edge_count = 0
        for i in range(500):
            for j in range(i + 1, min(i + 5, 500)):
                if edge_count >= 1000:
                    break
                graph[nodes[i]].add(nodes[j])
                edge_count += 1
            if edge_count >= 1000:
                break

        start = time.perf_counter()
        detect_cycles(graph)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 1000, f"detect_cycles took {elapsed_ms:.1f}ms (> 1000ms guardrail)"


class TestDetectCyclesAggregateReporting:
    """Aggregate reporting of every independent cycle (FR-003)."""

    def test_reports_multiple_disjoint_cycles(self):
        graph = {
            "a": {"b"},
            "b": {"a"},
            "c": {"d"},
            "d": {"c"},
            "e": set(),
        }
        cycles = detect_cycles(graph)
        assert len(cycles) == 2
        joined = {frozenset(c) for c in cycles}
        assert frozenset({"a", "b"}) in joined
        assert frozenset({"c", "d"}) in joined

    def test_reports_three_node_cycle(self):
        graph = {"a": {"b"}, "b": {"c"}, "c": {"a"}}
        cycles = detect_cycles(graph)
        assert len(cycles) == 1
        assert set(cycles[0]) >= {"a", "b", "c"}

    def test_no_cycles_returns_empty(self):
        graph = {"a": {"b"}, "b": {"c"}, "c": set()}
        assert detect_cycles(graph) == []
