"""Tests for _get_graph_api_root function."""

from agentic_devtools.cli.azure_devops.mark_reviewed import _get_graph_api_root


class TestGetGraphApiRoot:
    """Tests for _get_graph_api_root."""

    def test_transforms_dev_azure_url(self):
        """Replaces dev.azure.com with vssps.dev.azure.com."""
        result = _get_graph_api_root("https://dev.azure.com/example-org")
        assert result == "https://vssps.dev.azure.com/example-org"

    def test_preserves_non_dev_azure_url(self):
        """Returns URL unchanged for non-dev.azure.com URLs."""
        result = _get_graph_api_root("https://acme.visualstudio.com")
        assert result == "https://acme.visualstudio.com"

    def test_transforms_http_dev_azure_url(self):
        """Handles http:// prefix."""
        result = _get_graph_api_root("http://dev.azure.com/org")
        assert result == "https://vssps.dev.azure.com/org"
