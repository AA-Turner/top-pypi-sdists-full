"""Tests for get_first_child function."""

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyLevel,
    HierarchyNode,
    get_first_child,
)


class TestGetFirstChild:
    """Tests for get_first_child."""

    def test_empty_children_returns_none(self):
        """Returns None when no children exist."""
        node = HierarchyNode(title="Root", level=HierarchyLevel.EPIC, children=[])
        assert get_first_child(node) is None

    def test_single_child(self):
        """Returns the only child's key."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[ChildEntry(key="10", title="Only", order=1)],
        )
        assert get_first_child(node) == "10"

    def test_returns_lowest_order(self):
        """Returns key of child with lowest order value."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.FEATURE,
            children=[
                ChildEntry(key="3", title="Third", order=3),
                ChildEntry(key="1", title="First", order=1),
                ChildEntry(key="2", title="Second", order=2),
            ],
        )
        assert get_first_child(node) == "1"

    def test_gaps_in_order(self):
        """Handles gaps in order sequence (1, 5, 8)."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="a", title="A", order=5),
                ChildEntry(key="b", title="B", order=8),
                ChildEntry(key="c", title="C", order=1),
            ],
        )
        assert get_first_child(node) == "c"

    def test_duplicate_order_tiebreaker_numeric_key(self):
        """Duplicate orders are resolved by numeric key value."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="20", title="Twenty", order=1),
                ChildEntry(key="5", title="Five", order=1),
            ],
        )
        # Tiebreaker: numeric key 5 < 20
        assert get_first_child(node) == "5"

    def test_non_numeric_keys_sort_after_numeric(self):
        """Non-numeric keys sort after numeric keys at same order."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="abc", title="Alpha", order=1),
                ChildEntry(key="2", title="Two", order=1),
            ],
        )
        # Numeric key sorts before non-numeric at same order
        assert get_first_child(node) == "2"

    def test_missing_order_appears_after_explicit(self):
        """Children with None order appear after all explicitly-ordered children."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="100", title="No order", order=None),
                ChildEntry(key="1", title="First", order=1),
            ],
        )
        assert get_first_child(node) == "1"

    def test_all_missing_order(self):
        """All-missing-order children sort by key tiebreaker."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="30", title="Thirty", order=None),
                ChildEntry(key="5", title="Five", order=None),
                ChildEntry(key="10", title="Ten", order=None),
            ],
        )
        # All get effective order 1 (max=0, +1=1), tiebreaker by numeric key
        assert get_first_child(node) == "5"

    def test_pure_function_no_side_effects(self):
        """Function does not mutate the input node."""
        children = [
            ChildEntry(key="2", title="B", order=2),
            ChildEntry(key="1", title="A", order=1),
        ]
        node = HierarchyNode(title="Root", level=HierarchyLevel.EPIC, children=children)
        original_order = [c.key for c in node.children]
        get_first_child(node)
        assert [c.key for c in node.children] == original_order
