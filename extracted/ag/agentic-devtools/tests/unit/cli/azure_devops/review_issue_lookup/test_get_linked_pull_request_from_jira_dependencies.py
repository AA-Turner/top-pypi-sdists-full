"""Tests for the review_issue_lookup module and helper functions."""


class TestGetLinkedPullRequestFromJira:
    """Tests for _get_linked_pull_request_from_jira function."""

    def test_returns_none_when_requests_not_available(self):
        """Test returns None when requests library is not available."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_issue_lookup import (
            _get_linked_pull_request_from_jira,
        )

        with patch.dict("sys.modules", {"requests": None}):
            result = _get_linked_pull_request_from_jira("PROJECT-1234")
            assert result is None

    def test_returns_none_when_jira_module_not_available(self):
        """Test returns None when Jira module imports fail."""
        from unittest.mock import MagicMock, patch

        from agentic_devtools.cli.azure_devops.review_issue_lookup import (
            _get_linked_pull_request_from_jira,
        )

        with patch.dict("sys.modules", {"requests": MagicMock()}):
            with patch.dict("sys.modules", {"agentic_devtools.cli.jira.config": None}):
                result = _get_linked_pull_request_from_jira("PROJECT-1234")
        assert result is None

    def test_returns_none_on_issue_fetch_error(self):
        """Test returns None when Jira issue fetch fails."""
        from unittest.mock import MagicMock, patch

        mock_response = MagicMock()
        mock_response.status_code = 404

        with patch("requests.get", return_value=mock_response):
            with patch(
                "agentic_devtools.cli.jira.config.get_jira_base_url",
                return_value="https://jira.example.com",
            ):
                with patch(
                    "agentic_devtools.cli.jira.config.get_jira_headers",
                    return_value={"Authorization": "Bearer token"},
                ):
                    with patch(
                        "agentic_devtools.cli.jira.helpers._get_ssl_verify",
                        return_value=True,
                    ):
                        from agentic_devtools.cli.azure_devops.review_issue_lookup import (
                            _get_linked_pull_request_from_jira,
                        )

                        result = _get_linked_pull_request_from_jira("PROJECT-1234")
                        assert result is None

    def test_returns_none_on_network_exception(self):
        """Test returns None when network exception occurs."""
        from unittest.mock import patch

        with patch("requests.get", side_effect=Exception("Network error")):
            with patch(
                "agentic_devtools.cli.jira.config.get_jira_base_url",
                return_value="https://jira.example.com",
            ):
                with patch(
                    "agentic_devtools.cli.jira.config.get_jira_headers",
                    return_value={"Authorization": "Bearer token"},
                ):
                    with patch(
                        "agentic_devtools.cli.jira.helpers._get_ssl_verify",
                        return_value=True,
                    ):
                        from agentic_devtools.cli.azure_devops.review_issue_lookup import (
                            _get_linked_pull_request_from_jira,
                        )

                        result = _get_linked_pull_request_from_jira("PROJECT-1234")
                        assert result is None
