"""Tests for agentic_devtools.tools.jira.create_subtask."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.tools.jira import JiraConfig, create_subtask


class TestCreateSubtask:
    """Tests for the create_subtask convenience wrapper."""

    def _make_config(self, mock_requests=None):
        return JiraConfig(
            base_url="https://jira.example.com",
            headers={"Authorization": "Basic xxx"},
            ssl_verify=False,
            requests_module=mock_requests or MagicMock(),
        )

    def test_calls_create_issue_with_subtask_type(self):
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "PROJ-11"}
        mock_requests.post.return_value = mock_response
        config = self._make_config(mock_requests)

        result = create_subtask(
            config=config,
            project_key="PROJ",
            summary="My Subtask",
            description="Subtask description",
            labels=["sub"],
            parent_key="PROJ-10",
        )

        assert result["issue_key"] == "PROJ-11"
        payload = mock_requests.post.call_args[1]["json"]
        assert payload["fields"]["issuetype"]["name"] == "Sub-task"
        assert payload["fields"]["parent"]["key"] == "PROJ-10"

    @patch("agentic_devtools.tools.jira.create_issue")
    def test_delegates_to_create_issue(self, mock_create_issue):
        mock_create_issue.return_value = {
            "issue_key": "PROJ-2",
            "url": "https://jira.example.com/browse/PROJ-2",
            "raw_response": {},
        }
        config = self._make_config()

        create_subtask(
            config=config,
            project_key="PROJ",
            summary="Subtask",
            description="Desc",
            labels=[],
            parent_key="PROJ-1",
        )

        mock_create_issue.assert_called_once_with(
            config=config,
            project_key="PROJ",
            summary="Subtask",
            issue_type="Sub-task",
            description="Desc",
            labels=[],
            parent_key="PROJ-1",
        )

    @patch("agentic_devtools.tools.jira.create_issue")
    def test_delegates_custom_issue_type_to_create_issue(self, mock_create_issue):
        """Custom subtask type is forwarded to create_issue."""
        mock_create_issue.return_value = {
            "issue_key": "PROJ-2",
            "url": "https://jira.example.com/browse/PROJ-2",
            "raw_response": {},
        }
        config = self._make_config()

        create_subtask(
            config=config,
            project_key="PROJ",
            summary="Subtask",
            description="Desc",
            labels=[],
            parent_key="PROJ-1",
            issue_type="Unteraufgabe",
        )

        mock_create_issue.assert_called_once_with(
            config=config,
            project_key="PROJ",
            summary="Subtask",
            issue_type="Unteraufgabe",
            description="Desc",
            labels=[],
            parent_key="PROJ-1",
        )

    @patch("agentic_devtools.tools.jira.create_issue")
    def test_strips_custom_issue_type_before_delegating(self, mock_create_issue):
        """Whitespace around a custom issue type is removed before delegation."""
        mock_create_issue.return_value = {
            "issue_key": "PROJ-2",
            "url": "https://jira.example.com/browse/PROJ-2",
            "raw_response": {},
        }
        config = self._make_config()

        create_subtask(
            config=config,
            project_key="PROJ",
            summary="Subtask",
            description="Desc",
            labels=[],
            parent_key="PROJ-1",
            issue_type="  Unteraufgabe  ",
        )

        mock_create_issue.assert_called_once_with(
            config=config,
            project_key="PROJ",
            summary="Subtask",
            issue_type="Unteraufgabe",
            description="Desc",
            labels=[],
            parent_key="PROJ-1",
        )

    def test_raises_when_parent_key_is_empty(self):
        """Validate that an empty parent_key raises ValueError independently of issue type."""
        config = self._make_config()

        with pytest.raises(ValueError, match="parent_key is required"):
            create_subtask(
                config=config,
                project_key="PROJ",
                summary="Subtask",
                description="Desc",
                labels=[],
                parent_key="",
                issue_type="Unteraufgabe",
            )

    def test_raises_when_issue_type_is_blank(self):
        """Validate that a blank custom issue type is rejected before the Jira call."""
        config = self._make_config()

        with pytest.raises(ValueError, match="issue_type is required"):
            create_subtask(
                config=config,
                project_key="PROJ",
                summary="Subtask",
                description="Desc",
                labels=[],
                parent_key="PROJ-1",
                issue_type="   ",
            )

    def test_raises_when_issue_type_is_not_a_string(self):
        """Validate that non-string issue types fail with a type-specific error."""
        config = self._make_config()

        with pytest.raises(ValueError, match="issue_type must be a string"):
            create_subtask(
                config=config,
                project_key="PROJ",
                summary="Subtask",
                description="Desc",
                labels=[],
                parent_key="PROJ-1",
                issue_type=None,
            )

    def test_raises_when_parent_key_is_empty_for_default_type(self):
        """Validate that an empty parent_key raises ValueError for the default Sub-task type."""
        config = self._make_config()

        with pytest.raises(ValueError, match="parent_key is required"):
            create_subtask(
                config=config,
                project_key="PROJ",
                summary="Subtask",
                description="Desc",
                labels=[],
                parent_key="",
            )

    def test_raises_when_parent_key_is_whitespace_only(self):
        """Validate that a blank parent key is rejected before the Jira call."""
        config = self._make_config()

        with pytest.raises(ValueError, match="parent_key is required"):
            create_subtask(
                config=config,
                project_key="PROJ",
                summary="Subtask",
                description="Desc",
                labels=[],
                parent_key="   ",
            )

    def test_raises_when_parent_key_is_not_a_string(self):
        """Validate that non-string parent keys fail with a type-specific error."""
        config = self._make_config()

        with pytest.raises(ValueError, match="parent_key must be a string"):
            create_subtask(
                config=config,
                project_key="PROJ",
                summary="Subtask",
                description="Desc",
                labels=[],
                parent_key=None,
            )
