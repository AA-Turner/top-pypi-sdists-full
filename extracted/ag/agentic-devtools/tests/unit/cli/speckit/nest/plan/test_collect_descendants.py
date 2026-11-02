"""Tests for collect_descendants in nest/plan.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.nest.discovery import ChildRef
from agentic_devtools.cli.speckit.nest.plan import collect_descendants


def _cr(number: int) -> ChildRef:
    return ChildRef(number=number, title=f"Issue #{number}")


class TestCollectDescendants:
    """Tests for collect_descendants."""

    def test_collects_direct_and_transitive_descendants(self) -> None:
        """Returns all descendants reachable from the root."""
        graph = {
            1: (None, [_cr(2)]),
            2: (1, [_cr(3)]),
            3: (2, []),
        }
        assert collect_descendants(graph, 1) == {2, 3}

    def test_ignores_children_not_in_graph(self) -> None:
        """Children whose numbers are not keys in the graph are ignored."""
        graph = {
            1: (None, [_cr(2), _cr(99)]),
            2: (1, []),
        }
        assert collect_descendants(graph, 1) == {2}

    def test_avoids_revisiting_already_discovered_descendants(self) -> None:
        """Each descendant is counted only once even with diamond patterns."""
        graph = {
            1: (None, [_cr(2), _cr(3)]),
            2: (1, [_cr(4)]),
            3: (1, [_cr(4)]),
            4: (2, []),
        }
        assert collect_descendants(graph, 1) == {2, 3, 4}

    def test_returns_empty_for_leaf_issue(self) -> None:
        """A leaf issue (no children in graph) returns an empty set."""
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {10: (None, [])}
        assert collect_descendants(graph, 10) == set()

    def test_returns_empty_for_issue_not_in_graph(self) -> None:
        """An issue not present in the graph returns an empty set."""
        assert collect_descendants({}, 99) == set()
