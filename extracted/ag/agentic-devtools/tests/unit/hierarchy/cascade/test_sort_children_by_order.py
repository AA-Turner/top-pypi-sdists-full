"""Tests for _sort_children_by_order static method."""

from agentic_devtools.hierarchy.cascade import CascadeProcessor
from agentic_devtools.hierarchy.models import ChildInfo


class TestSortChildrenByOrder:
    """Tests for sorting children by their order field."""

    def test_sorts_by_order_field(self) -> None:
        """Children with order fields are sorted; those without go to the end."""
        children = [
            ChildInfo(number=3, title="Third", order=3),
            ChildInfo(number=1, title="First", order=1),
            ChildInfo(number=2, title="Second", order=2),
            ChildInfo(number=4, title="No order", order=None),
        ]
        sorted_children = CascadeProcessor._sort_children_by_order(children)
        assert [c.number for c in sorted_children] == [1, 2, 3, 4]

    def test_no_order_fields_preserves_original(self) -> None:
        """When no children have order, original order is preserved."""
        children = [
            ChildInfo(number=3, title="Third", order=None),
            ChildInfo(number=1, title="First", order=None),
        ]
        sorted_children = CascadeProcessor._sort_children_by_order(children)
        assert [c.number for c in sorted_children] == [3, 1]

    def test_mixed_order_and_none(self) -> None:
        """Children without order go after those with order."""
        children = [
            ChildInfo(number=5, title="No order", order=None),
            ChildInfo(number=2, title="Ordered 2", order=2),
            ChildInfo(number=1, title="Ordered 1", order=1),
        ]
        sorted_children = CascadeProcessor._sort_children_by_order(children)
        assert [c.number for c in sorted_children] == [1, 2, 5]
