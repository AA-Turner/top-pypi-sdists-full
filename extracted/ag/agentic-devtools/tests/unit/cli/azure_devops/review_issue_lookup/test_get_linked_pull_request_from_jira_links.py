"""Tests for the review_issue_lookup module and helper functions."""


class TestGetLinkedPullRequestFromJira:
    def test_returns_pr_id_from_remote_links(self):
        """Test extracts PR ID from remote links."""
        from unittest.mock import MagicMock, patch

        issue_response = MagicMock()
        issue_response.status_code = 200

        links_response = MagicMock()
        links_response.status_code = 200
        links_response.json.return_value = [
            {"object": {"url": "https://dev.azure.com/org/project/_git/repo/pullrequest/456"}}
        ]

        def mock_get(url, **kwargs):
            if "remotelink" in url:
                return links_response
            return issue_response

        with patch("requests.get", side_effect=mock_get):
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
                        assert result == 456

    def test_returns_pr_id_from_visualstudio_url(self):
        """Test extracts PR ID from visualstudio.com URL."""
        from unittest.mock import MagicMock, patch

        issue_response = MagicMock()
        issue_response.status_code = 200

        links_response = MagicMock()
        links_response.status_code = 200
        links_response.json.return_value = [
            {"object": {"url": "https://org.visualstudio.com/project/_git/repo/pullrequests/789"}}
        ]

        def mock_get(url, **kwargs):
            if "remotelink" in url:
                return links_response
            return issue_response

        with patch("requests.get", side_effect=mock_get):
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
                        assert result == 789

    def test_returns_none_when_remote_links_status_not_200(self):
        """Test returns None when remote links endpoint returns non-200.

        Covers branch 88->104.
        """
        from unittest.mock import MagicMock, patch

        issue_response = MagicMock()
        issue_response.status_code = 200

        links_response = MagicMock()
        links_response.status_code = 403

        def mock_get(url, **kwargs):
            if "remotelink" in url:
                return links_response
            return issue_response

        with patch("requests.get", side_effect=mock_get):
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

    def test_returns_none_when_azure_url_has_no_pr_pattern(self):
        """Test returns None when Azure DevOps URL exists but has no pullrequest path.

        Covers branch 99->95 (loop continues past non-matching Azure URL).
        """
        from unittest.mock import MagicMock, patch

        issue_response = MagicMock()
        issue_response.status_code = 200

        links_response = MagicMock()
        links_response.status_code = 200
        links_response.json.return_value = [
            {"object": {"url": "https://dev.azure.com/org/project/_git/repo/commit/abc123"}},
        ]

        def mock_get(url, **kwargs):
            if "remotelink" in url:
                return links_response
            return issue_response

        with patch("requests.get", side_effect=mock_get):
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

    def test_returns_none_when_no_matching_links(self):
        """Test returns None when no Azure DevOps PR links found."""
        from unittest.mock import MagicMock, patch

        issue_response = MagicMock()
        issue_response.status_code = 200

        links_response = MagicMock()
        links_response.status_code = 200
        links_response.json.return_value = [
            {"object": {"url": "https://github.com/org/repo/pull/123"}}  # Not Azure DevOps
        ]

        def mock_get(url, **kwargs):
            if "remotelink" in url:
                return links_response
            return issue_response

        with patch("requests.get", side_effect=mock_get):
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
