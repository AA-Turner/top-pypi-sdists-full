"""Tests for _get_project_id_via_api function."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.azure_devops.mark_reviewed import _get_project_id_via_api


class TestGetProjectIdViaApi:
    """Tests for _get_project_id_via_api."""

    def test_returns_project_id(self):
        """Returns project ID from API response."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "project-guid-123", "name": "MyProject"}
        mock_requests.get.return_value = mock_response

        result = _get_project_id_via_api(
            mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "MyProject"
        )
        assert result == "project-guid-123"

    def test_raises_when_id_empty(self):
        """Raises RuntimeError when project ID is empty."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "", "name": "MyProject"}
        mock_requests.get.return_value = mock_response

        with pytest.raises(RuntimeError, match="Empty project ID"):
            _get_project_id_via_api(
                mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "MyProject"
            )

    def test_raises_when_id_missing(self):
        """Raises RuntimeError when project ID key is missing."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "MyProject"}
        mock_requests.get.return_value = mock_response

        with pytest.raises(RuntimeError, match="Empty project ID"):
            _get_project_id_via_api(
                mock_requests, {"Authorization": "Basic abc"}, "https://dev.azure.com/org", "MyProject"
            )
