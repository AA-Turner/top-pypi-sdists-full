"""Tests for _get_connection_data function."""

from unittest.mock import MagicMock

from agentic_devtools.cli.azure_devops.mark_reviewed import _get_connection_data


class TestGetConnectionData:
    """Tests for _get_connection_data."""

    def test_returns_json_response(self):
        """Returns parsed JSON from connection data endpoint."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"authenticatedUser": {"id": "user-1"}, "instanceId": "inst-1"}
        mock_requests.get.return_value = mock_response

        headers = {"Authorization": "Basic abc"}
        result = _get_connection_data(mock_requests, headers, "https://dev.azure.com/org")

        assert result == {"authenticatedUser": {"id": "user-1"}, "instanceId": "inst-1"}
        mock_requests.get.assert_called_once()
        call_args = mock_requests.get.call_args
        assert "_apis/connectionData" in call_args[0][0]
        mock_response.raise_for_status.assert_called_once()
