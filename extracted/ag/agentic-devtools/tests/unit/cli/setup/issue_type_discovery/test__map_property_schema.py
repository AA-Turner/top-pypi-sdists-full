"""Tests for _map_property_schema in issue_type_discovery."""

from __future__ import annotations

from agentic_devtools.adapters.types import PropertySchema
from agentic_devtools.cli.setup.issue_type_discovery import _map_property_schema


class TestMapPropertySchema:
    """Tests for the _map_property_schema helper."""

    def test_basic_mapping(self) -> None:
        """Maps all fields from PropertySchema to PropertyEntry."""
        schema = PropertySchema(
            name="summary",
            type="string",
            required=True,
            allowed_values=None,
        )
        result = _map_property_schema(schema)
        assert result["name"] == "summary"
        assert result["type"] == "string"
        assert result["required"] is True
        assert result["allowed_values"] is None
        assert result["included_in_template"] is True
        assert result["display_name"] == "Summary"

    def test_allowed_values_as_list(self) -> None:
        """allowed_values list is preserved."""
        schema = PropertySchema(
            name="priority",
            type="string",
            required=False,
            allowed_values=["High", "Medium", "Low"],
        )
        result = _map_property_schema(schema)
        assert result["allowed_values"] == ["High", "Medium", "Low"]

    def test_allowed_values_none_becomes_null(self) -> None:
        """allowed_values=None is preserved as None (JSON null)."""
        schema = PropertySchema(
            name="description",
            type="string",
            required=False,
            allowed_values=None,
        )
        result = _map_property_schema(schema)
        assert result["allowed_values"] is None

    def test_required_true(self) -> None:
        """required=True is preserved."""
        schema = PropertySchema(name="title", type="string", required=True, allowed_values=None)
        result = _map_property_schema(schema)
        assert result["required"] is True

    def test_required_false(self) -> None:
        """required=False is preserved."""
        schema = PropertySchema(name="labels", type="array", required=False, allowed_values=None)
        result = _map_property_schema(schema)
        assert result["required"] is False

    def test_included_in_template_always_true(self) -> None:
        """included_in_template is always True regardless of input."""
        schema = PropertySchema(name="x", type="number", required=False, allowed_values=None)
        result = _map_property_schema(schema)
        assert result["included_in_template"] is True

    def test_display_name_title_casing_with_underscores(self) -> None:
        """display_name applies title-casing with underscores."""
        schema = PropertySchema(
            name="story_points",
            type="number",
            required=False,
            allowed_values=None,
        )
        result = _map_property_schema(schema)
        assert result["display_name"] == "Story Points"
