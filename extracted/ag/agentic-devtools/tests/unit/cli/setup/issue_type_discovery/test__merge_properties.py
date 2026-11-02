"""Tests for _merge_properties in issue_type_discovery."""

from __future__ import annotations

from agentic_devtools.cli.config.project_config import PropertyEntry
from agentic_devtools.cli.setup.issue_type_discovery import _merge_properties


def _prop(
    name: str,
    *,
    type_: str = "string",
    required: bool = False,
    allowed_values: list[str] | None = None,
    included_in_template: bool = True,
    display_name: str | None = None,
) -> PropertyEntry:
    """Helper to build a PropertyEntry for testing."""
    return PropertyEntry(
        name=name,
        display_name=display_name or name.replace("_", " ").title(),
        type=type_,
        required=required,
        allowed_values=allowed_values,
        included_in_template=included_in_template,
    )


class TestMergeProperties:
    """Tests for the _merge_properties helper."""

    def test_all_new_properties_no_existing(self) -> None:
        """When no existing properties, new properties are returned as-is."""
        new = [_prop("summary", required=True), _prop("priority")]
        result = _merge_properties(new, [])
        assert len(result) == 2
        assert result[0]["name"] == "summary"
        assert result[0]["included_in_template"] is True
        assert result[1]["name"] == "priority"

    def test_preserves_included_in_template_false(self) -> None:
        """Existing property with included_in_template=False is preserved on merge."""
        existing = [_prop("priority", included_in_template=False)]
        new = [_prop("priority", required=True)]
        result = _merge_properties(new, existing)
        assert len(result) == 1
        assert result[0]["name"] == "priority"
        assert result[0]["included_in_template"] is False
        # But other fields are updated from new data
        assert result[0]["required"] is True

    def test_new_property_gets_included_in_template_true(self) -> None:
        """A property not in existing gets included_in_template=True."""
        existing = [_prop("summary")]
        new = [_prop("summary"), _prop("security_classification")]
        result = _merge_properties(new, existing)
        assert len(result) == 2
        assert result[1]["name"] == "security_classification"
        assert result[1]["included_in_template"] is True

    def test_updates_type_required_allowed_values_display_name(self) -> None:
        """Fields type, required, allowed_values, display_name are updated from new data."""
        existing = [
            _prop(
                "priority",
                type_="string",
                required=False,
                allowed_values=["High", "Low"],
                included_in_template=False,
                display_name="Priority",
            )
        ]
        new = [
            _prop(
                "priority",
                type_="enum",
                required=True,
                allowed_values=["High", "Medium", "Low"],
                display_name="Priority Level",
            )
        ]
        result = _merge_properties(new, existing)
        assert result[0]["type"] == "enum"
        assert result[0]["required"] is True
        assert result[0]["allowed_values"] == ["High", "Medium", "Low"]
        assert result[0]["display_name"] == "Priority Level"
        # Preserved from existing
        assert result[0]["included_in_template"] is False

    def test_property_removed_from_adapter_response(self) -> None:
        """A property removed from adapter (not in new) is not in result."""
        existing = [_prop("summary"), _prop("deprecated_field")]
        new = [_prop("summary")]
        result = _merge_properties(new, existing)
        assert len(result) == 1
        assert result[0]["name"] == "summary"

    def test_empty_new_list(self) -> None:
        """Empty new list returns empty result."""
        existing = [_prop("summary")]
        result = _merge_properties([], existing)
        assert result == []

    def test_empty_existing_list(self) -> None:
        """Empty existing list returns new properties unchanged."""
        new = [_prop("summary"), _prop("priority")]
        result = _merge_properties(new, [])
        assert len(result) == 2
        assert all(p["included_in_template"] is True for p in result)
