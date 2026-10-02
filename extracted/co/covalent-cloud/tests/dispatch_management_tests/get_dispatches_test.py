# Copyright 2025 Agnostiq Inc.

"""Unit tests for get_dispatches function in dispatch management."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from covalent_cloud.dispatch_management.interface_functions import get_dispatches
from covalent_cloud.shared.classes.settings import Settings
from covalent_cloud.shared.schemas.dispatch import (
    DispatchListResponse,
    DispatchMetadata,
    DispatchRecord,
)


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = Settings()
    settings.dispatcher_uri = "https://api.dev.covalent.xyz"
    return settings


@pytest.fixture
def sample_dispatch_response():
    """Sample API response for dispatch listing."""
    return {
        "records": [
            {
                "dispatch_id": "dispatch-123",
                "name": "ML Training Workflow",
                "status": "COMPLETED",
                "created_at": "2023-01-01T10:00:00Z",
                "started_at": "2023-01-01T10:05:00Z",
                "completed_at": "2023-01-01T10:30:00Z",
                "updated_at": "2023-01-01T10:30:00Z",
                "electron_num": 5,
                "completed_task_num": 5,
                "tags": ["ml", "training"],
                "is_pinned": False,
                "redispatch_count": 0,
            },
            {
                "dispatch_id": "dispatch-456",
                "name": "Data Processing Pipeline",
                "status": "RUNNING",
                "created_at": "2023-01-01T11:00:00Z",
                "started_at": "2023-01-01T11:05:00Z",
                "completed_at": None,
                "updated_at": "2023-01-01T11:15:00Z",
                "electron_num": 8,
                "completed_task_num": 3,
                "tags": ["data", "processing"],
                "is_pinned": True,
                "redispatch_count": 1,
            },
        ],
        "metadata": {
            "total_count": 25,
            "page": 0,
            "count": 10,
            "status_count": {"COMPLETED": 15, "RUNNING": 5, "FAILED": 3, "PENDING": 2},
        },
    }


class TestGetDispatchesSuccess:
    """Test successful get_dispatches operations."""

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_default_params(
        self, mock_get_client, mock_settings, sample_dispatch_response
    ):
        """Test get_dispatches with default parameters."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_dispatch_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_dispatches(settings=mock_settings)

        assert isinstance(result, DispatchListResponse)
        assert len(result.records) == 2
        assert isinstance(result.records[0], DispatchRecord)
        assert result.records[0].dispatch_id == "dispatch-123"
        assert result.records[0].name == "ML Training Workflow"
        assert result.records[0].status == "COMPLETED"

        # Check API call parameters
        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "api/v2/lattices"

        params = call_args[1]["request_options"]["params"]
        assert params["count"] == 10
        assert params["page"] == 0
        assert params["sort"] == "created_at"
        assert params["direction"] == "desc"
        assert not params["only_root"]

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_with_filters(
        self, mock_get_client, mock_settings, sample_dispatch_response
    ):
        """Test get_dispatches with various filters."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_dispatch_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_dispatches(
            status="RUNNING",
            search="ML training",
            submitted_after="2023-01-01T09:00:00Z",
            submitted_before="2023-01-01T12:00:00Z",
            count=20,
            page=1,
            sort="name",
            direction="asc",
            pinned=True,
            only_root=True,
            settings=mock_settings,
        )

        assert isinstance(result, DispatchListResponse)

        # Verify all parameters were passed correctly
        call_args = mock_client.get.call_args
        params = call_args[1]["request_options"]["params"]

        assert params["status"] == "RUNNING"
        assert params["search"] == "ML training"
        assert params["submitted_after"] == "2023-01-01T09:00:00Z"
        assert params["submitted_before"] == "2023-01-01T12:00:00Z"
        assert params["count"] == 20
        assert params["page"] == 1
        assert params["sort"] == "name"
        assert params["direction"] == "asc"
        assert params["pinned"]
        assert params["only_root"]

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_with_dispatch_ids(
        self, mock_get_client, mock_settings, sample_dispatch_response
    ):
        """Test get_dispatches with specific dispatch IDs."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_dispatch_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        dispatch_ids = ["dispatch-123", "dispatch-456"]
        result = get_dispatches(dispatch_ids=dispatch_ids, settings=mock_settings)

        assert isinstance(result, DispatchListResponse)

        call_args = mock_client.get.call_args
        params = call_args[1]["request_options"]["params"]
        assert params["dispatch_ids"] == dispatch_ids

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_with_time_filters(
        self, mock_get_client, mock_settings, sample_dispatch_response
    ):
        """Test get_dispatches with all time-based filters."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_dispatch_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_dispatches(
            started_after="2023-01-01T10:00:00Z",
            started_before="2023-01-01T11:00:00Z",
            completed_after="2023-01-01T10:15:00Z",
            completed_before="2023-01-01T10:45:00Z",
            updated_after="2023-01-01T10:30:00Z",
            updated_before="2023-01-01T11:30:00Z",
            settings=mock_settings,
        )

        assert isinstance(result, DispatchListResponse)

        call_args = mock_client.get.call_args
        params = call_args[1]["request_options"]["params"]
        assert params["started_after"] == "2023-01-01T10:00:00Z"
        assert params["started_before"] == "2023-01-01T11:00:00Z"
        assert params["completed_after"] == "2023-01-01T10:15:00Z"
        assert params["completed_before"] == "2023-01-01T10:45:00Z"
        assert params["updated_after"] == "2023-01-01T10:30:00Z"
        assert params["updated_before"] == "2023-01-01T11:30:00Z"

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_empty_response(self, mock_get_client, mock_settings):
        """Test get_dispatches with empty response."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "records": [],
            "metadata": {"total_count": 0, "page": 0, "count": 10, "status_count": {}},
        }
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_dispatches(settings=mock_settings)

        assert isinstance(result, DispatchListResponse)
        assert len(result.records) == 0
        assert result.metadata.total_count == 0


class TestGetDispatchesErrorHandling:
    """Test error handling in get_dispatches."""

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_authentication_error(self, mock_get_client, mock_settings):
        """Test authentication error handling."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 401
        error = Exception("Unauthorized")
        error.response = mock_response
        mock_client.get.side_effect = error
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception):
            get_dispatches(settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_validation_error(self, mock_get_client, mock_settings):
        """Test validation error handling."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 400
        error = Exception("Bad request")
        error.response = mock_response
        mock_client.get.side_effect = error
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception):
            get_dispatches(settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_server_error(self, mock_get_client, mock_settings):
        """Test server error handling."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        error = Exception("Internal server error")
        error.response = mock_response
        mock_client.get.side_effect = error
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception):
            get_dispatches(settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_network_error(self, mock_get_client, mock_settings):
        """Test network error handling."""
        mock_client = MagicMock()
        mock_client.get.side_effect = ConnectionError("Network unreachable")
        mock_get_client.return_value = mock_client

        with pytest.raises(ConnectionError):
            get_dispatches(settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_timeout_error(self, mock_get_client, mock_settings):
        """Test timeout error handling."""
        mock_client = MagicMock()
        mock_client.get.side_effect = TimeoutError("Request timeout")
        mock_get_client.return_value = mock_client

        with pytest.raises(TimeoutError):
            get_dispatches(settings=mock_settings)

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_malformed_response(self, mock_get_client, mock_settings):
        """Test handling of malformed API response."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        # Missing required fields
        mock_response.json.return_value = {"records": [{"dispatch_id": "test"}]}
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception):  # Pydantic validation error
            get_dispatches(settings=mock_settings)


class TestGetDispatchesEdgeCases:
    """Test edge cases and boundary conditions."""

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_empty_dispatch_ids(
        self, mock_get_client, mock_settings, sample_dispatch_response
    ):
        """Test get_dispatches with empty dispatch_ids list."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_dispatch_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_dispatches(dispatch_ids=[], settings=mock_settings)

        # Should return valid result even with empty dispatch_ids
        assert isinstance(result, DispatchListResponse)

        # Check that API was called
        mock_client.get.assert_called_once()

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_none_values(
        self, mock_get_client, mock_settings, sample_dispatch_response
    ):
        """Test get_dispatches with explicit None values."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_dispatch_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_dispatches(status=None, search=None, pinned=None, settings=mock_settings)

        assert isinstance(result, DispatchListResponse)

        # None values should not be included in parameters
        call_args = mock_client.get.call_args
        params = call_args[1]["request_options"]["params"]
        assert "status" not in params
        assert "search" not in params
        assert "pinned" not in params

    @patch("covalent_cloud.dispatch_management.interface_functions.get_client")
    def test_get_dispatches_max_params(
        self, mock_get_client, mock_settings, sample_dispatch_response
    ):
        """Test get_dispatches with all possible parameters set."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_dispatch_response
        mock_client.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_dispatches(
            dispatch_ids=["dispatch-1", "dispatch-2"],
            status="COMPLETED",
            submitted_before="2023-01-02T00:00:00Z",
            submitted_after="2023-01-01T00:00:00Z",
            started_before="2023-01-02T01:00:00Z",
            started_after="2023-01-01T01:00:00Z",
            completed_before="2023-01-02T02:00:00Z",
            completed_after="2023-01-01T02:00:00Z",
            updated_before="2023-01-02T03:00:00Z",
            updated_after="2023-01-01T03:00:00Z",
            sort="name",
            direction="asc",
            count=50,
            page=2,
            search="workflow",
            only_root=True,
            pinned=True,
            settings=mock_settings,
        )

        assert isinstance(result, DispatchListResponse)

        # Check that major parameters are included in the request
        call_args = mock_client.get.call_args
        params = call_args[1]["request_options"]["params"]

        # Check key parameters are present
        assert params["status"] == "COMPLETED"
        assert params["count"] == 50
        assert params["page"] == 2
        assert params["direction"] == "asc"
        assert params["search"] == "workflow"
        assert params["only_root"]
        assert params["pinned"]


class TestDispatchModels:
    """Test the dispatch-related data models."""

    def test_dispatch_record_model(self):
        """Test DispatchRecord model validation."""
        record_data = {
            "dispatch_id": "dispatch-123",
            "name": "Test Workflow",
            "status": "COMPLETED",
            "created_at": datetime(2023, 1, 1, 10, 0, 0),
            "started_at": datetime(2023, 1, 1, 10, 5, 0),
            "completed_at": datetime(2023, 1, 1, 10, 30, 0),
            "updated_at": datetime(2023, 1, 1, 10, 30, 0),
            "electron_num": 5,
            "completed_task_num": 5,
            "tags": ["test"],
            "is_pinned": False,
            "redispatch_count": 0,
        }

        record = DispatchRecord(**record_data)

        assert record.dispatch_id == "dispatch-123"
        assert record.name == "Test Workflow"
        assert record.status == "COMPLETED"
        assert len(record.tags) == 1

    def test_dispatch_metadata_model(self):
        """Test DispatchMetadata model validation."""
        metadata_data = {
            "total_count": 100,
            "page": 0,
            "count": 10,
            "status_count": {"COMPLETED": 50, "RUNNING": 30, "FAILED": 20},
        }

        metadata = DispatchMetadata(**metadata_data)

        assert metadata.total_count == 100
        assert metadata.page == 0
        assert metadata.status_count["COMPLETED"] == 50

    def test_dispatch_list_response_model(self, sample_dispatch_response):
        """Test DispatchListResponse model validation."""
        response = DispatchListResponse(**sample_dispatch_response)

        assert len(response.records) == 2
        assert isinstance(response.records[0], DispatchRecord)
        assert isinstance(response.metadata, DispatchMetadata)
        assert response.metadata.total_count == 25
