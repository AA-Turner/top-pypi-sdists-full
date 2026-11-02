"""Tests for extract_pr_id_from_development_panel function."""


class TestExtractPrIdFromDevelopmentPanel:
    """Tests for extract_pr_id_from_development_panel function."""

    def test_returns_none_for_empty_list(self):
        """Test that None is returned for empty list."""
        from agentic_devtools.cli.azure_devops.review_jira import (
            extract_pr_id_from_development_panel,
        )

        result = extract_pr_id_from_development_panel([])
        assert result is None

    def test_extracts_pr_id_from_ado_url(self):
        """Test extracting PR ID from Azure DevOps URL."""
        from agentic_devtools.cli.azure_devops.review_jira import (
            extract_pr_id_from_development_panel,
        )

        pull_requests = [{"url": "https://dev.azure.com/org/project/_git/repo/pullrequest/5678"}]

        result = extract_pr_id_from_development_panel(pull_requests)
        assert result == 5678

    def test_extracts_pr_id_from_direct_id_field(self):
        """Test extracting PR ID from direct id field."""
        from agentic_devtools.cli.azure_devops.review_jira import (
            extract_pr_id_from_development_panel,
        )

        pull_requests = [{"id": 9999}]

        result = extract_pr_id_from_development_panel(pull_requests)
        assert result == 9999

    def test_extracts_pr_id_from_string_id_field(self):
        """Test extracting PR ID from string id field like '#1234'."""
        from agentic_devtools.cli.azure_devops.review_jira import (
            extract_pr_id_from_development_panel,
        )

        pull_requests = [{"id": "#1234"}]

        result = extract_pr_id_from_development_panel(pull_requests)
        assert result == 1234

    def test_returns_first_pr_when_multiple(self):
        """Test that first PR is returned when multiple exist."""
        from agentic_devtools.cli.azure_devops.review_jira import (
            extract_pr_id_from_development_panel,
        )

        pull_requests = [
            {"url": "https://dev.azure.com/org/project/_git/repo/pullrequest/1111"},
            {"url": "https://dev.azure.com/org/project/_git/repo/pullrequest/2222"},
        ]

        result = extract_pr_id_from_development_panel(pull_requests)
        assert result == 1111

    def test_returns_none_when_no_valid_url_or_id(self):
        """Test that None is returned when no valid URL or ID exists."""
        from agentic_devtools.cli.azure_devops.review_jira import (
            extract_pr_id_from_development_panel,
        )

        pull_requests = [{"status": "OPEN", "title": "Some PR"}]

        result = extract_pr_id_from_development_panel(pull_requests)
        assert result is None

    def test_falls_through_to_id_when_url_no_match(self):
        """Test fallback to ID field when URL doesn't match ADO pattern."""
        from agentic_devtools.cli.azure_devops.review_jira import (
            extract_pr_id_from_development_panel,
        )

        pull_requests = [{"url": "https://github.com/org/repo/pull/42", "id": 7777}]

        result = extract_pr_id_from_development_panel(pull_requests)
        assert result == 7777

    def test_skips_pr_with_non_numeric_string_id(self):
        """Test that PR with non-numeric string ID is skipped."""
        from agentic_devtools.cli.azure_devops.review_jira import (
            extract_pr_id_from_development_panel,
        )

        pull_requests = [
            {"id": "no-numbers-here"},
            {"url": "https://dev.azure.com/org/project/_git/repo/pullrequest/4242"},
        ]

        result = extract_pr_id_from_development_panel(pull_requests)
        assert result == 4242
