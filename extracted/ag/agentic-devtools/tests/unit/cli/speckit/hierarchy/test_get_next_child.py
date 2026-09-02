"""Tests for get_next_child function."""

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyLevel,
    HierarchyNode,
    get_next_child,
)


class TestGetNextChild:
    """Tests for get_next_child."""

    def test_mid_sequence_returns_next(self):
        """Returns the next child in order after the current key."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.FEATURE,
            children=[
                ChildEntry(key="1", title="First", order=1),
                ChildEntry(key="2", title="Second", order=2),
                ChildEntry(key="3", title="Third", order=3),
            ],
        )
        assert get_next_child(node, "2") == "3"

    def test_last_child_returns_none(self):
        """Returns None when current is the last child."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="1", title="First", order=1),
                ChildEntry(key="2", title="Second", order=2),
            ],
        )
        assert get_next_child(node, "2") is None

    def test_empty_children_returns_none(self):
        """Returns None when there are no children."""
        node = HierarchyNode(title="Root", level=HierarchyLevel.EPIC, children=[])
        assert get_next_child(node, "1") is None

    def test_missing_key_returns_none(self):
        """Returns None when key is not found."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[ChildEntry(key="1", title="First", order=1)],
        )
        assert get_next_child(node, "999") is None

    def test_key_normalization_int_input(self):
        """Int input is normalized to string for matching."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="1", title="First", order=1),
                ChildEntry(key="2", title="Second", order=2),
            ],
        )
        assert get_next_child(node, 1) == "2"

    def test_gaps_in_order(self):
        """Works correctly with gaps in order values."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="a", title="A", order=1),
                ChildEntry(key="b", title="B", order=5),
                ChildEntry(key="c", title="C", order=10),
            ],
        )
        assert get_next_child(node, "a") == "b"
        assert get_next_child(node, "b") == "c"
        assert get_next_child(node, "c") is None

    def test_duplicate_order_tiebreaker(self):
        """Duplicate orders resolved by ascending numeric key."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="20", title="Twenty", order=1),
                ChildEntry(key="5", title="Five", order=1),
                ChildEntry(key="10", title="Ten", order=2),
            ],
        )
        # Sorted: 5 (order=1, key=5), 20 (order=1, key=20), 10 (order=2)
        assert get_next_child(node, "5") == "20"
        assert get_next_child(node, "20") == "10"

    def test_numeric_equal_keys_different_strings(self):
        """Keys '12' and '012' with same numeric value sort lexicographically."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="012", title="Twelve padded", order=1),
                ChildEntry(key="12", title="Twelve", order=1),
            ],
        )
        # Both parse to 12, tiebreaker is lexicographic: "012" < "12"
        assert get_next_child(node, "012") == "12"
        assert get_next_child(node, "12") is None

    def test_missing_order_at_end(self):
        """Children with None order appear after explicitly-ordered."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="50", title="No order", order=None),
                ChildEntry(key="1", title="First", order=1),
                ChildEntry(key="2", title="Second", order=2),
            ],
        )
        # Sorted: 1, 2, 50 (None → max+1=3)
        assert get_next_child(node, "1") == "2"
        assert get_next_child(node, "2") == "50"
        assert get_next_child(node, "50") is None

    def test_multiple_none_order_sorted_by_key(self):
        """Multiple None-order children sorted among themselves by key."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="30", title="Thirty", order=None),
                ChildEntry(key="10", title="Ten", order=None),
                ChildEntry(key="1", title="First", order=1),
            ],
        )
        # Sorted: 1 (order=1), 10 (None→2, key=10), 30 (None→2, key=30)
        assert get_next_child(node, "1") == "10"
        assert get_next_child(node, "10") == "30"
        assert get_next_child(node, "30") is None

    def test_pure_function_no_side_effects(self):
        """Function does not mutate the input node."""
        children = [
            ChildEntry(key="2", title="B", order=2),
            ChildEntry(key="1", title="A", order=1),
        ]
        node = HierarchyNode(title="Root", level=HierarchyLevel.EPIC, children=children)
        original_order = [c.key for c in node.children]
        get_next_child(node, "1")
        assert [c.key for c in node.children] == original_order
