"""Tests for HierarchyNode dataclass."""

from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.speckit.hierarchy import (
    ChildEntry,
    HierarchyLevel,
    HierarchyNode,
    HierarchyValidationError,
)


class TestHierarchyNode:
    """Tests for HierarchyNode dataclass."""

    def test_basic_construction(self):
        """Test constructing a HierarchyNode with required fields."""
        node = HierarchyNode(title="My Epic", level=HierarchyLevel.EPIC)
        assert node.title == "My Epic"
        assert node.level is HierarchyLevel.EPIC
        assert node.parent is None
        assert node.children == []
        assert node.processed_at is None

    def test_full_construction(self):
        """Test constructing with all fields specified."""
        ts = datetime(2024, 1, 15, 10, 30, 0, tzinfo=UTC)
        children = [ChildEntry(key="10", title="Child 1", order=1)]
        node = HierarchyNode(
            title="Feature X",
            level=HierarchyLevel.FEATURE,
            parent="42",
            children=children,
            processed_at=ts,
        )
        assert node.parent == "42"
        assert len(node.children) == 1
        assert node.processed_at == ts

    def test_parent_int_normalized_to_string(self):
        """Test that integer parent is normalized to string."""
        node = HierarchyNode(title="Task", level=HierarchyLevel.TASK, parent=99)  # type: ignore[arg-type]
        assert node.parent == "99"
        assert isinstance(node.parent, str)

    def test_empty_title_raises(self):
        """Test that empty titles are rejected."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            HierarchyNode(title="", level=HierarchyLevel.TASK)
        assert exc_info.value.field_name == "title"

    def test_level_non_enum_raises(self):
        """Test that level must be a HierarchyLevel."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            HierarchyNode(title="X", level="task")  # type: ignore[arg-type]
        assert exc_info.value.field_name == "level"

    def test_parent_bool_true_raises(self):
        """Test that boolean True parent raises HierarchyValidationError."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            HierarchyNode(title="X", level=HierarchyLevel.TASK, parent=True)  # type: ignore[arg-type]
        assert exc_info.value.field_name == "parent"

    def test_parent_bool_false_raises(self):
        """Test that boolean False parent raises HierarchyValidationError."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            HierarchyNode(title="X", level=HierarchyLevel.TASK, parent=False)  # type: ignore[arg-type]
        assert exc_info.value.field_name == "parent"

    def test_parent_float_raises(self):
        """Test that non-string, non-integer parents are rejected."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            HierarchyNode(title="X", level=HierarchyLevel.TASK, parent=3.14)  # type: ignore[arg-type]
        assert exc_info.value.field_name == "parent"

    def test_children_non_childentry_raises(self):
        """Test that children entries must be ChildEntry instances."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            HierarchyNode(
                title="X",
                level=HierarchyLevel.TASK,
                children=[{"key": "1", "title": "Child", "order": 1}],  # type: ignore[list-item]
            )
        assert exc_info.value.field_name == "children.0"

    def test_children_non_list_raises(self):
        """Test that children must be provided as a list."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            HierarchyNode(
                title="X",
                level=HierarchyLevel.TASK,
                children=(ChildEntry(key="1", title="Child", order=1),),  # type: ignore[arg-type]
            )
        assert exc_info.value.field_name == "children"

    def test_processed_at_string_raises(self):
        """Test that processed_at must be a datetime when provided."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            HierarchyNode(
                title="X",
                level=HierarchyLevel.TASK,
                processed_at="2024-01-01T00:00:00Z",  # type: ignore[arg-type]
            )
        assert exc_info.value.field_name == "processed_at"

    def test_to_dict_canonical_order(self):
        """Test to_dict produces canonical key order."""
        node = HierarchyNode(title="Task", level=HierarchyLevel.TASK, parent="5")
        result = node.to_dict()
        assert list(result.keys()) == [
            "title",
            "level",
            "parent",
            "children",
            "processed_at",
        ]

    def test_to_dict_values(self):
        """Test to_dict serializes values correctly."""
        ts = datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC)
        node = HierarchyNode(
            title="Epic",
            level=HierarchyLevel.EPIC,
            parent=None,
            children=[ChildEntry(key="1", title="C1", order=0)],
            processed_at=ts,
        )
        d = node.to_dict()
        assert d["title"] == "Epic"
        assert d["level"] == "epic"
        assert d["parent"] is None
        assert d["children"] == [{"key": "1", "title": "C1", "order": 0}]
        assert d["processed_at"] == "2024-06-01T12:00:00+00:00"

    def test_to_dict_processed_at_none(self):
        """Test to_dict serializes None processed_at as None."""
        node = HierarchyNode(title="X", level=HierarchyLevel.TASK)
        assert node.to_dict()["processed_at"] is None

    def test_to_dict_normalizes_naive_processed_at_to_utc(self):
        """Test to_dict normalizes naive processed_at to UTC."""
        node = HierarchyNode(
            title="X",
            level=HierarchyLevel.TASK,
            processed_at=datetime(2024, 6, 1, 12, 0, 0),
        )

        assert node.to_dict()["processed_at"] == "2024-06-01T12:00:00+00:00"

    def test_equality(self):
        """Test that equal nodes compare equal."""
        a = HierarchyNode(title="A", level=HierarchyLevel.EPIC)
        b = HierarchyNode(title="A", level=HierarchyLevel.EPIC)
        assert a == b
