"""Tests for ChildEntry dataclass."""

import pytest

from agentic_devtools.cli.speckit.hierarchy import ChildEntry, HierarchyValidationError


class TestChildEntry:
    """Tests for ChildEntry dataclass."""

    def test_basic_construction(self):
        """Test constructing a ChildEntry with required fields."""
        entry = ChildEntry(key="42", title="Implement parser", order=1)
        assert entry.key == "42"
        assert entry.title == "Implement parser"
        assert entry.order == 1

    def test_key_int_normalized_to_string(self):
        """Test that integer key is normalized to string."""
        entry = ChildEntry(key=42, title="Test", order=0)  # type: ignore[arg-type]
        assert entry.key == "42"
        assert isinstance(entry.key, str)

    def test_key_bool_true_raises(self):
        """Test that boolean True key raises HierarchyValidationError."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            ChildEntry(key=True, title="Test", order=0)  # type: ignore[arg-type]
        assert exc_info.value.field_name == "key"

    def test_key_bool_false_raises(self):
        """Test that boolean False key raises HierarchyValidationError."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            ChildEntry(key=False, title="Test", order=0)  # type: ignore[arg-type]
        assert exc_info.value.field_name == "key"

    def test_key_float_raises(self):
        """Test that non-string, non-integer keys are rejected."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            ChildEntry(key=3.14, title="Test", order=0)  # type: ignore[arg-type]
        assert exc_info.value.field_name == "key"

    def test_empty_title_raises(self):
        """Test that empty titles are rejected."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            ChildEntry(key="42", title="", order=0)
        assert exc_info.value.field_name == "title"

    def test_order_bool_raises(self):
        """Test that boolean order values are rejected."""
        with pytest.raises(HierarchyValidationError) as exc_info:
            ChildEntry(key="42", title="Test", order=True)  # type: ignore[arg-type]
        assert exc_info.value.field_name == "order"

    def test_to_dict_canonical_order(self):
        """Test to_dict produces canonical key order."""
        entry = ChildEntry(key="10", title="Setup", order=3)
        result = entry.to_dict()
        assert list(result.keys()) == ["key", "title", "order"]
        assert result == {"key": "10", "title": "Setup", "order": 3}

    def test_equality(self):
        """Test that equal entries compare equal."""
        a = ChildEntry(key="1", title="A", order=0)
        b = ChildEntry(key="1", title="A", order=0)
        assert a == b

    def test_inequality(self):
        """Test that different entries compare unequal."""
        a = ChildEntry(key="1", title="A", order=0)
        b = ChildEntry(key="2", title="B", order=1)
        assert a != b
