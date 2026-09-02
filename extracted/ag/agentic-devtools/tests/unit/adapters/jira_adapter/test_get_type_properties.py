"""Tests for JiraAdapter.get_type_properties()."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.adapters.jira_adapter import JiraAdapter
from agentic_devtools.tools.jira import JiraConfig


def _make_config(base_url: str = "https://jira.example.com") -> JiraConfig:
    """Build a JiraConfig for testing."""
    return JiraConfig(
        base_url=base_url,
        headers={"Authorization": "******"},
        ssl_verify=False,
        requests_module=MagicMock(),
    )


def _make_adapter(project_key: str = "PROJ") -> JiraAdapter:
    """Build a JiraAdapter with a mock config."""
    return JiraAdapter(config=_make_config(), project_key=project_key)


def _mock_issue_types_response() -> list[dict[str, str]]:
    """Standard issue types response for tests."""
    return [
        {"id": "1", "name": "Bug", "description": "A bug"},
        {"id": "2", "name": "Story", "description": "A user story"},
        {"id": "3", "name": "Task", "description": "A task"},
    ]


def _mock_fields_response() -> dict[str, dict[str, object]]:
    """Standard fields response for tests."""
    return {
        "summary": {
            "name": "Summary",
            "required": True,
            "schema": {"type": "string"},
            "allowedValues": None,
        },
        "priority": {
            "name": "Priority",
            "required": False,
            "schema": {"type": "priority"},
            "allowedValues": [
                {"id": "1", "name": "High"},
                {"id": "2", "name": "Medium"},
                {"id": "3", "name": "Low"},
            ],
        },
        "labels": {
            "name": "Labels",
            "required": False,
            "schema": {"type": "array", "items": "string"},
        },
    }


class TestGetTypePropertiesHappyPath:
    """Happy path tests for get_type_properties()."""

    def test_returns_property_schemas(self) -> None:
        """Returns list of PropertySchema dicts with correct fields."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = _mock_fields_response()

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert len(result) == 3
        # Field identifier (key) is used as name, not the display name
        summary = next(p for p in result if p["name"] == "summary")
        assert summary["type"] == "string"
        assert summary["required"] is True
        assert summary["allowed_values"] is None

    def test_allowed_values_populated(self) -> None:
        """Allowed values are populated from API response."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = _mock_fields_response()

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        # Field key "priority" is used as the name identifier
        priority = next(p for p in result if p["name"] == "priority")
        assert priority["allowed_values"] == ["High", "Medium", "Low"]

    def test_allowed_values_none_when_unconstrained(self) -> None:
        """Allowed values are None when field is unconstrained."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "description": {
                "name": "Description",
                "required": False,
                "schema": {"type": "string"},
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["allowed_values"] is None

    def test_allowed_values_none_when_empty_list(self) -> None:
        """Allowed values are None when API returns empty list."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "status": {
                "name": "Status",
                "required": False,
                "schema": {"type": "status"},
                "allowedValues": [],
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["allowed_values"] is None

    def test_allowed_values_uses_value_key_fallback(self) -> None:
        """Falls back to 'value' key when 'name' is not present."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                "schema": {"type": "option"},
                "allowedValues": [
                    {"id": "1", "value": "Option A"},
                    {"id": "2", "value": "Option B"},
                ],
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["allowed_values"] == ["Option A", "Option B"]

    def test_allowed_values_scalar_values(self) -> None:
        """Scalar allowed values are converted to strings."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                "schema": {"type": "option"},
                "allowedValues": ["alpha", "beta", "gamma"],
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["allowed_values"] == ["alpha", "beta", "gamma"]

    def test_allowed_values_preserves_falsey_name(self) -> None:
        """A falsey-but-valid 'name' value (e.g. 0) is not skipped."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                "schema": {"type": "option"},
                # name=0 is falsey but a valid value; value="should-not-appear"
                # is intentionally included to confirm it is NOT used when name is present.
                "allowedValues": [{"id": "1", "name": 0, "value": "should-not-appear"}],
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        # str(0) == "0"; "should-not-appear" must not be in the result
        assert result[0]["allowed_values"] == ["0"]

    def test_allowed_values_explicit_null_name_falls_back(self) -> None:
        """When 'name' is explicitly null, falls back to 'value' without producing 'None'."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                "schema": {"type": "option"},
                # name is present-but-null; value is the real label
                "allowedValues": [{"id": "1", "name": None, "value": "Active"}],
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["allowed_values"] == ["Active"]

    def test_allowed_values_all_keys_null_uses_empty_string(self) -> None:
        """When all priority keys are present-but-null, the entry is an empty string."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                "schema": {"type": "option"},
                "allowedValues": [{"id": None, "name": None, "value": None}],
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["allowed_values"] == [""]


class TestGetTypePropertiesCaseInsensitive:
    """Case-insensitive type name matching tests."""

    def test_lowercase_type_name_matches(self) -> None:
        """Lowercase type name matches issue type."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "summary": {"name": "Summary", "required": True, "schema": {"type": "string"}}
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("story")

        assert len(result) == 1
        mock_client.get_issue_type_fields.assert_called_once_with("2")

    def test_uppercase_type_name_matches(self) -> None:
        """Uppercase type name matches issue type."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "summary": {"name": "Summary", "required": True, "schema": {"type": "string"}}
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("STORY")

        assert len(result) == 1
        mock_client.get_issue_type_fields.assert_called_once_with("2")

    def test_mixed_case_type_name_matches(self) -> None:
        """Mixed case type name matches issue type."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "summary": {"name": "Summary", "required": True, "schema": {"type": "string"}}
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Story")

        assert len(result) == 1

    def test_field_name_is_field_key_identifier(self) -> None:
        """PropertySchema.name is the field key (stable identifier), not the display name."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_10001": {
                "name": "Story Points",
                "required": False,
                "schema": {"type": "number"},
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("bug")

        assert result[0]["name"] == "customfield_10001"

    def test_non_dict_items_in_issue_types_skipped(self) -> None:
        """Non-dict items in issue types response are skipped during type lookup."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            "invalid",
            None,
            {"id": "1", "name": "Bug", "description": "A bug"},
        ]
        mock_client.get_issue_type_fields.return_value = {
            "summary": {"name": "Summary", "required": True, "schema": {"type": "string"}}
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert len(result) == 1

    def test_whitespace_around_type_name_is_ignored(self) -> None:
        """Leading/trailing whitespace is removed before lookup and caching."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "summary": {"name": "Summary", "required": True, "schema": {"type": "string"}}
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result1 = adapter.get_type_properties(" Bug ")
            result2 = adapter.get_type_properties("bug")

        assert result1 == result2
        mock_client.get_issue_type_fields.assert_called_once_with("1")


class TestGetTypePropertiesValidation:
    """Validation tests for get_type_properties()."""

    def test_empty_string_raises_valueerror(self) -> None:
        """Raises ValueError for empty type name."""
        adapter = _make_adapter()
        with pytest.raises(ValueError, match="must not be empty"):
            adapter.get_type_properties("")

    def test_whitespace_only_raises_valueerror(self) -> None:
        """Raises ValueError for whitespace-only type name."""
        adapter = _make_adapter()
        with pytest.raises(ValueError, match="must not be empty"):
            adapter.get_type_properties("   ")

    def test_nonexistent_type_raises_valueerror(self) -> None:
        """Raises ValueError for type that doesn't exist in project."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(ValueError, match="not found") as exc_info:
                adapter.get_type_properties("NonExistent")

        assert "NonExistent" in str(exc_info.value)
        assert "PROJ" in str(exc_info.value)

    def test_non_list_issue_types_response_raises_valueerror(self) -> None:
        """Raises ValueError when issue types response is not a list."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = {"error": "unexpected"}

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(ValueError, match="not found"):
                adapter.get_type_properties("Bug")

    def test_no_project_key_raises_valueerror(self) -> None:
        """Raises ValueError when no project key is configured."""
        adapter = JiraAdapter(config=_make_config(), project_key="")
        with pytest.raises(ValueError, match="project_key"):
            adapter.get_type_properties("Bug")

    def test_matching_type_without_truthy_id_raises_valueerror(self) -> None:
        """Matching issue types without an id are treated as not found."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "", "name": "Bug", "description": "A bug"},
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(ValueError, match="Issue type 'Bug' not found"):
                adapter.get_type_properties("Bug")

        mock_client.get_issue_type_fields.assert_not_called()

    def test_matching_type_with_null_id_raises_valueerror(self) -> None:
        """Matching issue types with a null id are treated as not found."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": None, "name": "Bug", "description": "A bug"},
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(ValueError, match="Issue type 'Bug' not found"):
                adapter.get_type_properties("Bug")

        mock_client.get_issue_type_fields.assert_not_called()

    def test_matching_type_with_numeric_id_is_coerced_to_string(self) -> None:
        """Truthy non-string issue type IDs are coerced before field lookup."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": 123, "name": "Bug", "description": "A bug"},
        ]
        mock_client.get_issue_type_fields.return_value = {
            "summary": {"name": "Summary", "required": True, "schema": {"type": "string"}}
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["name"] == "summary"
        mock_client.get_issue_type_fields.assert_called_once_with("123")


class TestGetTypePropertiesDefaultType:
    """Tests for default type value handling."""

    def test_missing_schema_defaults_to_string(self) -> None:
        """Fields with no schema default to type 'string'."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                # No "schema" key
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["type"] == "string"

    def test_schema_not_dict_defaults_to_string(self) -> None:
        """Fields with non-dict schema default to type 'string'."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                "schema": "not-a-dict",
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["type"] == "string"

    def test_schema_type_missing_defaults_to_string(self) -> None:
        """Fields with schema but no 'type' key default to 'string'."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                "schema": {"items": "string"},  # schema present but no "type"
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["type"] == "string"

    def test_schema_type_none_defaults_to_string(self) -> None:
        """Falsey schema type values default to 'string'."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                "schema": {"type": None},
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["type"] == "string"

    def test_schema_type_is_coerced_to_string(self) -> None:
        """Truthy non-string schema type values are coerced to strings."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "customfield_100": {
                "name": "Custom Field",
                "required": False,
                "schema": {"type": 123},
            },
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["type"] == "123"


class TestGetTypePropertiesErrorHandling:
    """Error translation tests for get_type_properties()."""

    def test_timeout_error_translated(self) -> None:
        """Timeout errors are translated to RuntimeError."""
        import requests

        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.side_effect = requests.exceptions.Timeout("timed out")

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="timed out"):
                adapter.get_type_properties("Bug")

    def test_connection_error_translated(self) -> None:
        """Connection errors are translated to RuntimeError with URL info."""
        import requests

        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.side_effect = requests.exceptions.ConnectionError("refused")

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="jira.example.com"):
                adapter.get_type_properties("Bug")

    def test_http_401_error_translated(self) -> None:
        """HTTP 401 errors include authentication guidance."""
        import requests

        adapter = _make_adapter()
        mock_client = MagicMock()
        response = MagicMock()
        response.status_code = 401
        response.url = "https://jira.example.com/rest/api/2/issue/createmeta"
        err = requests.exceptions.HTTPError(response=response)
        mock_client.get_project_issueTypes.side_effect = err

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="authentication failed"):
                adapter.get_type_properties("Bug")

    def test_fields_api_error_translated(self) -> None:
        """Error during fields fetch is translated to RuntimeError."""
        import requests

        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.side_effect = requests.exceptions.Timeout("timed out")

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="timed out"):
                adapter.get_type_properties("Bug")

    def test_non_dict_field_meta_skipped(self) -> None:
        """Non-dict field metadata entries are silently skipped."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "summary": {
                "name": "Summary",
                "required": True,
                "schema": {"type": "string"},
            },
            "invalid_field": "not-a-dict",
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert len(result) == 1
        assert result[0]["name"] == "summary"

    def test_non_dict_response_returns_empty_list(self) -> None:
        """Returns empty list when fields API returns non-dict response."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = ["unexpected"]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result == []

    def test_none_issue_type_name_is_skipped_without_attribute_error(self) -> None:
        """Issue type entries with a null name are skipped safely."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "999", "name": None, "description": "bad"},
            {"id": "1", "name": "Bug", "description": "A bug"},
        ]
        mock_client.get_issue_type_fields.return_value = {
            "summary": {"name": "Summary", "required": True, "schema": {"type": "string"}}
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_type_properties("Bug")

        assert result[0]["name"] == "summary"


class TestGetTypePropertiesCaching:
    """Session-level caching tests for get_type_properties()."""

    def test_second_call_uses_cached_result(self) -> None:
        """Second call returns cached result without additional API call."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = _mock_fields_response()

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result1 = adapter.get_type_properties("Bug")
            result2 = adapter.get_type_properties("Bug")

        assert result1 == result2
        mock_client.get_issue_type_fields.assert_called_once()

    def test_cache_is_case_insensitive(self) -> None:
        """Cache key is case-insensitive so 'Bug' and 'bug' share cache."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = _mock_fields_response()

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result1 = adapter.get_type_properties("Bug")
            result2 = adapter.get_type_properties("bug")
            result3 = adapter.get_type_properties("BUG")

        assert result1 == result2 == result3
        mock_client.get_issue_type_fields.assert_called_once()

    def test_different_types_cached_separately(self) -> None:
        """Different type names have separate cache entries."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = _mock_fields_response()

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            adapter.get_type_properties("Bug")
            adapter.get_type_properties("Story")

        assert mock_client.get_issue_type_fields.call_count == 2

    def test_mutating_returned_list_does_not_corrupt_cache(self) -> None:
        """Appending to the returned list does not corrupt the internal cache."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "summary": {"name": "Summary", "required": True, "schema": {"type": "string"}}
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result1 = adapter.get_type_properties("Bug")
            result1.clear()  # mutate the returned list
            result2 = adapter.get_type_properties("Bug")

        assert len(result2) == 1
        assert result2[0]["name"] == "summary"

    def test_mutating_returned_allowed_values_does_not_corrupt_cache(self) -> None:
        """Mutating the allowed_values list in a returned item does not corrupt the cache."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = _mock_issue_types_response()
        mock_client.get_issue_type_fields.return_value = {
            "priority": {
                "name": "Priority",
                "required": False,
                "schema": {"type": "priority"},
                "allowedValues": [{"id": "1", "name": "High"}, {"id": "2", "name": "Low"}],
            }
        }

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result1 = adapter.get_type_properties("Bug")
            priority1 = next(p for p in result1 if p["name"] == "priority")
            assert priority1["allowed_values"] is not None
            priority1["allowed_values"].clear()  # mutate the allowed_values list

            result2 = adapter.get_type_properties("Bug")
            priority2 = next(p for p in result2 if p["name"] == "priority")

        assert priority2["allowed_values"] == ["High", "Low"]
