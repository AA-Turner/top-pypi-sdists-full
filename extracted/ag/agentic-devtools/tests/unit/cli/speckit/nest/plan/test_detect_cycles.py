"""Tests for detect_cycles in nest/plan.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.nest.discovery import ChildRef
from agentic_devtools.cli.speckit.nest.plan import detect_cycles


def _cr(number: int) -> ChildRef:
    return ChildRef(number=number, title=f"Issue #{number}")


class TestDetectCycles:
    """Tests for detect_cycles."""

    def test_no_cycles_in_tree(self) -> None:
        """A proper tree has no cycles."""
        graph = {
            100: (None, [_cr(101), _cr(102)]),
            101: (100, []),
            102: (100, []),
        }
        assert detect_cycles(graph) == []

    def test_detects_simple_two_node_cycle(self) -> None:
        """A -> B -> A forms a two-node cycle."""
        graph = {
            100: (None, [_cr(101)]),
            101: (100, [_cr(100)]),
        }
        cycles = detect_cycles(graph)
        assert len(cycles) == 1
        assert 100 in cycles[0]
        assert 101 in cycles[0]

    def test_detects_three_node_cycle(self) -> None:
        """A -> B -> C -> A forms a cycle involving all three nodes."""
        graph = {
            100: (None, [_cr(101)]),
            101: (100, [_cr(102)]),
            102: (101, [_cr(100)]),
        }
        cycles = detect_cycles(graph)
        cycle_members: set[int] = set()
        for c in cycles:
            cycle_members.update(c)
        assert {100, 101, 102}.issubset(cycle_members)

    def test_handles_disconnected_components(self) -> None:
        """Disconnected components without cycles produce an empty list."""
        graph = {
            100: (None, [_cr(101)]),
            101: (100, []),
            200: (None, [_cr(201)]),
            201: (200, []),
        }
        assert detect_cycles(graph) == []

    def test_skips_duplicate_cycle_when_already_recorded(self) -> None:
        """The same cycle is not appended twice."""
        graph = {
            100: (None, [_cr(101)]),
            101: (100, [_cr(100)]),
        }
        cycles = detect_cycles(graph)
        # There should be at most one cycle entry.
        assert len(cycles) <= 1

    def test_does_not_revisit_nodes_in_visited_set(self) -> None:
        """Nodes already fully processed (in visited) are not traversed again."""
        graph = {
            1: (None, [_cr(2)]),
            2: (1, []),
            3: (None, [_cr(2)]),
        }
        # No cycle; just confirms visited-node short-circuit does not crash.
        assert detect_cycles(graph) == []

    def test_duplicate_cycle_detection_not_appended_twice(self) -> None:
        """A cycle whose set exactly matches one already recorded is skipped."""
        # A child with the same back-edge listed twice in its children produces
        # two separate DFS paths that both try to append the same cycle set.
        graph = {
            1: (None, [_cr(2)]),
            2: (1, [_cr(1), _cr(1)]),  # duplicate back-edge → same cycle twice
        }
        cycles = detect_cycles(graph)
        # The duplicate must not have been appended.
        assert len(cycles) == 1
        assert cycles[0] == {1, 2}
