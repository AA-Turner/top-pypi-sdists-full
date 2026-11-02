"""Tests for HIERARCHY_SCHEMA validation."""

import pytest

from agentic_devtools.cli.speckit.hierarchy import HIERARCHY_SCHEMA

jsonschema = pytest.importorskip("jsonschema")


def _valid_data(**overrides):
    """Return valid hierarchy data with optional overrides."""
    base = {
        "title": "Test",
        "level": "epic",
        "parent": None,
        "children": [{"key": "1", "title": "Child", "order": 0}],
        "processed_at": "2024-01-01T00:00:00+00:00",
    }
    base.update(overrides)
    return base


class TestHierarchySchema:
    """Tests for HIERARCHY_SCHEMA JSON Schema validation."""

    def test_valid_data_passes(self):
        """Test that valid data passes schema validation."""
        jsonschema.validate(_valid_data(), HIERARCHY_SCHEMA)

    def test_all_three_levels_valid(self):
        """Test all three level values pass."""
        for level in ("epic", "feature", "task"):
            jsonschema.validate(_valid_data(level=level), HIERARCHY_SCHEMA)

    def test_invalid_level_fails(self):
        """Test that invalid level value fails schema validation."""
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(_valid_data(level="sprint"), HIERARCHY_SCHEMA)

    def test_missing_title_fails(self):
        """Test that missing title fails."""
        data = _valid_data()
        del data["title"]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, HIERARCHY_SCHEMA)

    def test_missing_level_fails(self):
        """Test that missing level fails."""
        data = _valid_data()
        del data["level"]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, HIERARCHY_SCHEMA)

    def test_missing_children_fails(self):
        """Test that missing children fails."""
        data = _valid_data()
        del data["children"]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, HIERARCHY_SCHEMA)

    def test_non_array_children_fails(self):
        """Test that non-array children fails."""
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(_valid_data(children="not_a_list"), HIERARCHY_SCHEMA)

    def test_child_missing_key_fails(self):
        """Test that child entry missing key fails."""
        children = [{"title": "X", "order": 0}]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(_valid_data(children=children), HIERARCHY_SCHEMA)

    def test_child_missing_title_fails(self):
        """Test that child entry missing title fails."""
        children = [{"key": "1", "order": 0}]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(_valid_data(children=children), HIERARCHY_SCHEMA)

    def test_child_missing_order_valid(self):
        """Test that child entry without order is valid (order is optional)."""
        children = [{"key": "1", "title": "X"}]
        jsonschema.validate(_valid_data(children=children), HIERARCHY_SCHEMA)

    def test_child_null_order_valid(self):
        """Test that child entry with null order is valid."""
        children = [{"key": "1", "title": "X", "order": None}]
        jsonschema.validate(_valid_data(children=children), HIERARCHY_SCHEMA)

    def test_parent_as_integer_valid(self):
        """Test that integer parent is valid."""
        jsonschema.validate(_valid_data(parent=42), HIERARCHY_SCHEMA)

    def test_parent_as_null_valid(self):
        """Test that null parent is valid."""
        jsonschema.validate(_valid_data(parent=None), HIERARCHY_SCHEMA)

    def test_processed_at_null_valid(self):
        """Test that null processed_at is valid."""
        jsonschema.validate(_valid_data(processed_at=None), HIERARCHY_SCHEMA)

    def test_empty_children_list_valid(self):
        """Test that empty children list is valid."""
        jsonschema.validate(_valid_data(children=[]), HIERARCHY_SCHEMA)

    def test_additional_properties_rejected(self):
        """Test that additional properties at top level are rejected."""
        data = _valid_data()
        data["extra_field"] = "bad"
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(data, HIERARCHY_SCHEMA)

    def test_child_additional_properties_rejected(self):
        """Test that additional properties in children are rejected."""
        children = [{"key": "1", "title": "X", "order": 0, "extra": "bad"}]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(_valid_data(children=children), HIERARCHY_SCHEMA)

    def test_child_key_as_integer_valid(self):
        """Test that integer child key is valid."""
        children = [{"key": 42, "title": "X", "order": 0}]
        jsonschema.validate(_valid_data(children=children), HIERARCHY_SCHEMA)
