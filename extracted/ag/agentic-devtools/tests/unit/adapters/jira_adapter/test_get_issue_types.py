"""Tests for JiraAdapter.get_issue_types()."""

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


class TestGetIssueTypesHappyPath:
    """Happy path tests for get_issue_types()."""

    def test_returns_issue_types_for_project(self) -> None:
        """Returns list of IssueTypeInfo dicts from createmeta response."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "1", "name": "Bug", "description": "A bug"},
            {"id": "2", "name": "Story", "description": "A user story"},
            {"id": "3", "name": "Task", "description": "A task"},
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_issue_types()

        assert len(result) == 3
        assert result[0] == {"name": "Bug", "description": "A bug"}
        assert result[1] == {"name": "Story", "description": "A user story"}
        assert result[2] == {"name": "Task", "description": "A task"}

    def test_includes_custom_types(self) -> None:
        """Custom issue types are included in the result."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "1", "name": "Bug", "description": "A bug"},
            {"id": "100", "name": "Custom Widget", "description": "A custom type"},
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_issue_types()

        assert len(result) == 2
        assert result[1]["name"] == "Custom Widget"

    def test_empty_project_returns_empty_list(self) -> None:
        """Returns empty list when project has no issue types."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = []

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_issue_types()

        assert result == []

    def test_null_description_coerced_to_empty_string(self) -> None:
        """None/missing descriptions are coerced to empty string."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "1", "name": "Bug", "description": None},
            {"id": "2", "name": "Task"},  # missing description key
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_issue_types()

        assert result[0]["description"] == ""
        assert result[1]["description"] == ""

    def test_name_and_description_coerced_to_strings(self) -> None:
        """None and non-string issue type values are normalized to strings."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "1", "name": None, "description": 123},
            {"id": "2", "name": 456, "description": None},
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_issue_types()

        assert result == [
            {"name": "", "description": "123"},
            {"name": "456", "description": ""},
        ]

    def test_non_dict_items_in_response_are_skipped(self) -> None:
        """Non-dict items in the response list are silently skipped."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "1", "name": "Bug", "description": "A bug"},
            "invalid-item",
            None,
            {"id": "2", "name": "Task", "description": "A task"},
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_issue_types()

        assert len(result) == 2

    def test_non_list_response_returns_empty_list(self) -> None:
        """Returns empty list when API returns non-list response."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = {"error": "unexpected"}

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result = adapter.get_issue_types()

        assert result == []


class TestGetIssueTypesValidation:
    """Validation tests for get_issue_types()."""

    def test_raises_valueerror_when_project_key_is_none(self) -> None:
        """Raises ValueError when project_key is None."""
        adapter = JiraAdapter(config=_make_config(), project_key=None)
        with pytest.raises(ValueError, match="project_key"):
            adapter.get_issue_types()

    def test_raises_valueerror_when_project_key_is_empty(self) -> None:
        """Raises ValueError when project_key is empty string."""
        adapter = JiraAdapter(config=_make_config(), project_key="")
        with pytest.raises(ValueError, match="project_key"):
            adapter.get_issue_types()

    def test_no_api_call_on_validation_failure(self) -> None:
        """No API call is made when validation fails."""
        adapter = JiraAdapter(config=_make_config(), project_key="")
        mock_client = MagicMock()
        adapter._sdk_client = mock_client

        with pytest.raises(ValueError):
            adapter.get_issue_types()

        mock_client.get_project_issueTypes.assert_not_called()


class TestGetIssueTypesErrorHandling:
    """Error translation tests for get_issue_types()."""

    def test_import_error_when_sdk_unavailable(self) -> None:
        """Raises ImportError when atlassian-python-api is not installed."""
        adapter = _make_adapter()

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            side_effect=ImportError("atlassian-python-api is required"),
        ):
            with pytest.raises(ImportError, match="atlassian-python-api"):
                adapter.get_issue_types()

    def test_timeout_error_translated(self) -> None:
        """Timeout errors are translated to RuntimeError with guidance."""
        import requests

        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.side_effect = requests.exceptions.Timeout("timed out")

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="timed out"):
                adapter.get_issue_types()

    def test_connection_error_translated(self) -> None:
        """Connection errors are translated to RuntimeError with URL info."""
        import requests

        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.side_effect = requests.exceptions.ConnectionError("refused")

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="jira.example.com"):
                adapter.get_issue_types()

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
                adapter.get_issue_types()

    def test_http_403_error_translated(self) -> None:
        """HTTP 403 errors include authorization guidance."""
        import requests

        adapter = _make_adapter()
        mock_client = MagicMock()
        response = MagicMock()
        response.status_code = 403
        response.url = "https://jira.example.com/rest/api/2/project"
        err = requests.exceptions.HTTPError(response=response)
        mock_client.get_project_issueTypes.side_effect = err

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="authorization denied"):
                adapter.get_issue_types()

    def test_http_500_error_translated(self) -> None:
        """HTTP 5xx errors include status code."""
        import requests

        adapter = _make_adapter()
        mock_client = MagicMock()
        response = MagicMock()
        response.status_code = 500
        response.url = "https://jira.example.com/rest/api/2/issue/createmeta"
        err = requests.exceptions.HTTPError(response=response)
        mock_client.get_project_issueTypes.side_effect = err

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="500"):
                adapter.get_issue_types()

    def test_http_error_without_response_translated(self) -> None:
        """HTTPError without response object is handled gracefully."""
        import requests

        adapter = _make_adapter()
        mock_client = MagicMock()
        err = requests.exceptions.HTTPError("connection failed")
        err.response = None
        mock_client.get_project_issueTypes.side_effect = err

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="connection failed"):
                adapter.get_issue_types()

    def test_generic_exception_translated(self) -> None:
        """Generic exceptions are wrapped in RuntimeError."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.side_effect = Exception("something broke")

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            with pytest.raises(RuntimeError, match="something broke"):
                adapter.get_issue_types()

    def test_atlassian_api_error_translated(self) -> None:
        """Atlassian ApiError is translated to RuntimeError."""
        adapter = _make_adapter()
        mock_client = MagicMock()

        # Create a mock ApiError class
        mock_api_error = type("ApiError", (Exception,), {})
        err_instance = mock_api_error("Not found")
        err_instance.status_code = 404
        mock_client.get_project_issueTypes.side_effect = err_instance

        mock_errors_module = MagicMock()
        mock_errors_module.ApiError = mock_api_error

        with (
            patch.object(adapter, "_ensure_sdk_client", return_value=mock_client),
            patch.dict(
                "sys.modules",
                {"atlassian": MagicMock(errors=mock_errors_module), "atlassian.errors": mock_errors_module},
            ),
        ):
            with pytest.raises(RuntimeError, match="404"):
                adapter.get_issue_types()

    def test_atlassian_import_error_falls_through(self) -> None:
        """When atlassian.errors cannot be imported, falls through to generic handling."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.side_effect = Exception("unknown error")

        # Remove atlassian modules to force ImportError on `from atlassian import errors`
        with (
            patch.object(adapter, "_ensure_sdk_client", return_value=mock_client),
            patch.dict(
                "sys.modules",
                {"atlassian": None, "atlassian.errors": None},
            ),
        ):
            with pytest.raises(RuntimeError, match="unknown error"):
                adapter.get_issue_types()


class TestEnsureSdkClient:
    """Tests for _ensure_sdk_client() lazy initialization."""

    def test_caches_client_on_instance(self) -> None:
        """Second call returns the cached client without re-creating."""
        adapter = _make_adapter()
        mock_client = MagicMock()

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ) as mock_build:
            client1 = adapter._ensure_sdk_client()
            client2 = adapter._ensure_sdk_client()

        assert client1 is client2
        mock_build.assert_called_once()


class TestGetIssueTypesCaching:
    """Session-level caching tests for get_issue_types()."""

    def test_second_call_does_not_trigger_api_call(self) -> None:
        """Second call returns cached result without additional API call."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "1", "name": "Bug", "description": "A bug"},
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result1 = adapter.get_issue_types()
            result2 = adapter.get_issue_types()

        assert result1 == result2
        mock_client.get_project_issueTypes.assert_called_once()

    def test_cache_is_instance_scoped(self) -> None:
        """Different adapter instances have separate caches."""
        adapter1 = _make_adapter()
        adapter2 = _make_adapter()
        mock_client1 = MagicMock()
        mock_client1.get_project_issueTypes.return_value = [
            {"id": "1", "name": "Bug", "description": "A bug"},
        ]
        mock_client2 = MagicMock()
        mock_client2.get_project_issueTypes.return_value = [
            {"id": "2", "name": "Story", "description": "A story"},
        ]

        with patch.object(adapter1, "_ensure_sdk_client", return_value=mock_client1):
            result1 = adapter1.get_issue_types()
        with patch.object(adapter2, "_ensure_sdk_client", return_value=mock_client2):
            result2 = adapter2.get_issue_types()

        assert result1[0]["name"] == "Bug"
        assert result2[0]["name"] == "Story"

    def test_mutating_returned_list_does_not_corrupt_cache(self) -> None:
        """Appending to the returned list does not corrupt the internal cache."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "1", "name": "Bug", "description": "A bug"},
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result1 = adapter.get_issue_types()
            result1.clear()  # mutate the returned list
            result2 = adapter.get_issue_types()

        assert len(result2) == 1
        assert result2[0]["name"] == "Bug"

    def test_mutating_returned_item_does_not_corrupt_cache(self) -> None:
        """Mutating a returned dict item does not corrupt the internal cache."""
        adapter = _make_adapter()
        mock_client = MagicMock()
        mock_client.get_project_issueTypes.return_value = [
            {"id": "1", "name": "Bug", "description": "A bug"},
        ]

        with patch.object(adapter, "_ensure_sdk_client", return_value=mock_client):
            result1 = adapter.get_issue_types()
            result1[0]["name"] = "Modified"  # mutate a returned item
            result2 = adapter.get_issue_types()

        assert result2[0]["name"] == "Bug"
