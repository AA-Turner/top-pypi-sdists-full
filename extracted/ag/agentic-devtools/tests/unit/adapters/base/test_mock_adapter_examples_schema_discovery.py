"""Example tests demonstrating MockAdapter schema discovery usage.

Shows happy-path patterns for using ``get_issue_types()`` and
``get_type_properties()`` with both default and overridden schemas.
"""

from __future__ import annotations

from agentic_devtools.adapters.base import IssueTypeInfo, PropertySchema
from tests.unit.adapters.mock_adapter import MockAdapter


class TestGetIssueTypesDefaults:
    """Tests exercising get_issue_types() with default canonical types."""

    def test_returns_list(self, mock_adapter: MockAdapter) -> None:
        """get_issue_types() returns a list."""
        result = mock_adapter.get_issue_types()
        assert isinstance(result, list)

    def test_returns_three_canonical_types(self, mock_adapter: MockAdapter) -> None:
        """Default get_issue_types() returns bug, feature, task."""
        result = mock_adapter.get_issue_types()
        names = [t["name"] for t in result]
        assert names == ["bug", "feature", "task"]

    def test_each_type_has_name_and_description(self, mock_adapter: MockAdapter) -> None:
        """Each IssueTypeInfo has both name and description keys."""
        result = mock_adapter.get_issue_types()
        for type_info in result:
            assert "name" in type_info
            assert "description" in type_info
            assert isinstance(type_info["name"], str)
            assert isinstance(type_info["description"], str)


class TestGetIssueTypesOverrides:
    """Tests exercising get_issue_types() with constructor overrides."""

    def test_custom_issue_types(self) -> None:
        """Constructor override replaces default issue types."""
        custom_types: list[IssueTypeInfo] = [
            IssueTypeInfo(name="incident", description="Production incident"),
        ]
        adapter = MockAdapter(issue_types=custom_types)
        result = adapter.get_issue_types()
        assert len(result) == 1
        assert result[0]["name"] == "incident"

    def test_empty_override_returns_empty(self) -> None:
        """Empty list override returns empty list."""
        adapter = MockAdapter(issue_types=[])
        assert adapter.get_issue_types() == []


class TestGetTypePropertiesDefaults:
    """Tests exercising get_type_properties() with default schemas."""

    def test_bug_has_properties(self, mock_adapter: MockAdapter) -> None:
        """get_type_properties('bug') returns non-empty schema."""
        result = mock_adapter.get_type_properties("bug")
        assert len(result) > 0

    def test_bug_summary_is_required(self, mock_adapter: MockAdapter) -> None:
        """Bug type has a required 'summary' property."""
        result = mock_adapter.get_type_properties("bug")
        summary = next(p for p in result if p["name"] == "summary")
        assert summary["required"] is True
        assert summary["type"] == "string"

    def test_unknown_type_returns_empty(self, mock_adapter: MockAdapter) -> None:
        """Unknown type name returns empty property list."""
        result = mock_adapter.get_type_properties("nonexistent")
        assert result == []


class TestGetTypePropertiesOverrides:
    """Tests exercising get_type_properties() with constructor overrides."""

    def test_custom_properties(self) -> None:
        """Constructor override replaces default type properties."""
        custom_props: dict[str, list[PropertySchema]] = {
            "incident": [
                PropertySchema(name="severity", type="string", required=True, allowed_values=["P1", "P2", "P3"]),
            ],
        }
        adapter = MockAdapter(type_properties=custom_props)
        result = adapter.get_type_properties("incident")
        assert len(result) == 1
        assert result[0]["name"] == "severity"
        assert result[0]["allowed_values"] == ["P1", "P2", "P3"]

    def test_override_removes_default_types(self) -> None:
        """Override map does not include default types."""
        custom_props: dict[str, list[PropertySchema]] = {"custom": []}
        adapter = MockAdapter(type_properties=custom_props)
        assert adapter.get_type_properties("bug") == []
