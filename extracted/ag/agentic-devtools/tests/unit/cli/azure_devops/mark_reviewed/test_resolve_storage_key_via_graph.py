"""Tests for _resolve_storage_key_via_graph function."""

from unittest.mock import MagicMock

from agentic_devtools.cli.azure_devops.mark_reviewed import _resolve_storage_key_via_graph


class TestResolveStorageKeyViaGraph:
    """Tests for _resolve_storage_key_via_graph."""

    def test_returns_storage_key_on_success(self):
        """Returns storageKey from Graph API response."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"storageKey": "guid-123"}
        mock_requests.get.return_value = mock_response

        result = _resolve_storage_key_via_graph(
            mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "aad.user1"
        )
        assert result == "guid-123"

    def test_returns_none_on_exception(self, capsys):
        """Returns None and prints warning on failure."""
        mock_requests = MagicMock()
        mock_requests.get.side_effect = Exception("Network error")

        result = _resolve_storage_key_via_graph(
            mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "aad.user1"
        )
        assert result is None
        captured = capsys.readouterr()
        assert "Warning" in captured.out

    def test_returns_none_when_key_missing(self):
        """Returns None when storageKey not in response."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_requests.get.return_value = mock_response

        result = _resolve_storage_key_via_graph(
            mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "aad.user1"
        )
        assert result is None
