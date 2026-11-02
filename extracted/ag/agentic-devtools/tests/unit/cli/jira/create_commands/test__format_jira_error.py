"""Tests for _format_jira_error helper."""

from unittest.mock import MagicMock

from agentic_devtools.cli.jira import create_commands


class TestFormatJiraError:
    """Tests for the _format_jira_error helper function."""

    def test_format_jira_error_includes_details(self):
        """Test helper includes Jira API error messages and errors in the formatted output."""
        exc = RuntimeError("400 Client Error")
        response = MagicMock()
        response.json.return_value = {
            "errorMessages": [],
            "errors": {"issuetype": "The issue type selected is invalid."},
        }
        response.text = "{}"
        exc.response = response

        assert "Messages: []" in create_commands._format_jira_error(exc)
        assert "Errors: {'issuetype': 'The issue type selected is invalid.'}" in create_commands._format_jira_error(exc)

    def test_format_jira_error_uses_plain_text_when_details_are_missing(self):
        """Test helper falls back to the exception text when no structured details exist."""
        exc = RuntimeError("400 Client Error")
        response = MagicMock()
        response.json.side_effect = ValueError("bad json")
        response.text = ""
        exc.response = response

        assert create_commands._format_jira_error(exc) == "400 Client Error"

    def test_format_jira_error_uses_text_when_structured_details_are_missing(self):
        """Test helper falls back to the response text when structured details are not available."""
        exc = RuntimeError("400 Client Error")
        response = MagicMock()
        response.json.return_value = {"errorMessages": "not-a-list", "errors": "not-a-dict"}
        response.text = "fallback"
        exc.response = response

        assert create_commands._format_jira_error(exc) == "400 Client Error — fallback"
