"""Tests for get_child_position function."""

import pytest

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyLevel,
    HierarchyNode,
    get_child_position,
)


class TestGetChildPosition:
    """Tests for get_child_position."""

    def test_correct_position_and_total(self):
        """Returns correct 1-indexed position and total."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="1", title="First", order=1),
                ChildEntry(key="2", title="Second", order=2),
                ChildEntry(key="3", title="Third", order=3),
            ],
        )
        assert get_child_position(node, "1") == (1, 3)
        assert get_child_position(node, "2") == (2, 3)
        assert get_child_position(node, "3") == (3, 3)

    def test_gaps_in_order(self):
        """Positions are correct with gaps in order values."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="a", title="A", order=1),
                ChildEntry(key="b", title="B", order=5),
                ChildEntry(key="c", title="C", order=10),
            ],
        )
        assert get_child_position(node, "a") == (1, 3)
        assert get_child_position(node, "b") == (2, 3)
        assert get_child_position(node, "c") == (3, 3)

    def test_missing_key_raises_valueerror(self):
        """Raises ValueError with diagnostic message for missing key."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="1", title="First", order=1),
                ChildEntry(key="2", title="Second", order=2),
            ],
        )
        with pytest.raises(ValueError, match="Key '999' not found"):
            get_child_position(node, "999")

    def test_missing_key_error_shows_available(self):
        """ValueError includes available keys for diagnostics."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="10", title="Ten", order=1),
                ChildEntry(key="20", title="Twenty", order=2),
            ],
        )
        with pytest.raises(ValueError, match="Available keys:.*10.*20"):
            get_child_position(node, "999")

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
        assert get_child_position(node, 2) == (2, 2)

    def test_duplicate_order_positions(self):
        """Positions reflect tiebreaker ordering for duplicate orders."""
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
        assert get_child_position(node, "5") == (1, 3)
        assert get_child_position(node, "20") == (2, 3)
        assert get_child_position(node, "10") == (3, 3)

    def test_missing_order_positions(self):
        """Positions account for None-order children placed at end."""
        node = HierarchyNode(
            title="Root",
            level=HierarchyLevel.EPIC,
            children=[
                ChildEntry(key="50", title="No order", order=None),
                ChildEntry(key="1", title="First", order=1),
                ChildEntry(key="2", title="Second", order=2),
            ],
        )
        # Sorted: 1, 2, 50 (None → end)
        assert get_child_position(node, "1") == (1, 3)
        assert get_child_position(node, "2") == (2, 3)
        assert get_child_position(node, "50") == (3, 3)

    def test_pure_function_no_side_effects(self):
        """Function does not mutate the input node."""
        children = [
            ChildEntry(key="2", title="B", order=2),
            ChildEntry(key="1", title="A", order=1),
        ]
        node = HierarchyNode(title="Root", level=HierarchyLevel.EPIC, children=children)
        original_order = [c.key for c in node.children]
        get_child_position(node, "1")
        assert [c.key for c in node.children] == original_order
