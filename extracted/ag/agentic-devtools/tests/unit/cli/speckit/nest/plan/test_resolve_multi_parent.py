"""Tests for resolve_multi_parent in nest/plan.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.nest.discovery import ChildRef
from agentic_devtools.cli.speckit.nest.plan import resolve_multi_parent


def _cr(number: int) -> ChildRef:
    return ChildRef(number=number, title=f"Issue #{number}")


class TestResolveMultiParent:
    """Tests for resolve_multi_parent."""

    def test_returns_empty_when_no_multi_parent_issues(self) -> None:
        """No multi-parent issues means an empty selection dict."""
        graph = {
            100: (None, [_cr(101)]),
            101: (100, []),
        }
        assert resolve_multi_parent(graph) == {}

    def test_selects_lowest_numbered_parent(self) -> None:
        """The lowest-numbered parent is selected when a child has multiple."""
        graph = {
            50: (None, [_cr(200)]),
            100: (None, [_cr(200)]),
            200: (50, []),
        }
        selections = resolve_multi_parent(graph)
        assert selections[200] == 50

    def test_multiple_children_each_with_multiple_parents(self) -> None:
        """Each multi-parent child independently selects the lowest parent."""
        graph = {
            10: (None, [_cr(100), _cr(101)]),
            20: (None, [_cr(100), _cr(101)]),
            100: (10, []),
            101: (10, []),
        }
        selections = resolve_multi_parent(graph)
        assert selections[100] == 10
        assert selections[101] == 10

    def test_ignores_children_not_present_in_graph(self) -> None:
        """Children absent from the graph (issue 999) are not considered."""
        graph: dict[int, tuple[int | None, list[ChildRef]]] = {
            10: (None, [_cr(999)]),
            20: (None, [_cr(999)]),
        }
        assert resolve_multi_parent(graph) == {}

    def test_single_parent_child_not_included_in_selections(self) -> None:
        """A child with exactly one parent does not appear in selections."""
        graph = {
            10: (None, [_cr(20)]),
            30: (None, [_cr(20)]),
            20: (10, []),
        }
        # 20 has two parents (10, 30); only 20 should appear.
        selections = resolve_multi_parent(graph)
        assert 20 in selections
        # 10 and 30 each have only one parent (None), so they are absent.
        assert 10 not in selections
        assert 30 not in selections
