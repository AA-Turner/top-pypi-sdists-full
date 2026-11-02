"""Tests for _get_organization_account_name function."""

from agentic_devtools.cli.azure_devops.mark_reviewed import _get_organization_account_name


class TestGetOrganizationAccountName:
    """Tests for _get_organization_account_name."""

    def test_extracts_from_path(self):
        """Extracts org name from dev.azure.com URL path."""
        result = _get_organization_account_name("https://dev.azure.com/example-org")
        assert result == "example-org"

    def test_extracts_from_multi_segment_path(self):
        """Extracts last path segment."""
        result = _get_organization_account_name("https://dev.azure.com/org/project")
        assert result == "project"

    def test_falls_back_to_hostname(self):
        """Falls back to first hostname segment when path is empty."""
        result = _get_organization_account_name("https://acme.visualstudio.com")
        assert result == "acme"

    def test_hostname_with_no_path(self):
        """Extracts from hostname when path is just '/'."""
        result = _get_organization_account_name("https://myorg.visualstudio.com/")
        assert result == "myorg"
