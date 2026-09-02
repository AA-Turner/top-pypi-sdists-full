"""Unit tests for Deployment model (T018, T020, T035, T036).

Tests:
- T018: Deployment model including metadata and artifacts_source
- T020: Deployment status polling
- T035: cancel method (US2)
- T036: stream_logs method (US2)
"""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from novita_sandbox.artifact_hosting.client import DeploymentClient
from novita_sandbox.artifact_hosting.exceptions import CancellationError
from novita_sandbox.artifact_hosting.models.deployment import Deployment
from novita_sandbox.artifact_hosting.models.enums import (
    CANCELLABLE_STATES,
    DeploymentStatus,
    TERMINAL_STATES,
)
from novita_sandbox.artifact_hosting.models.nested import (
    AccountInfo,
    ArtifactsSource,
    DeploymentMetadata,
    ReplicaSpec,
)
from novita_sandbox.artifact_hosting.models.project import Project


class TestDeploymentModel:
    """T018: Test Deployment model with nested objects."""
    
    def test_from_dict_basic(self, sample_deployment_data):
        """Should parse basic deployment data."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        deployment = Deployment.from_dict(sample_deployment_data, mock_client)
        
        assert deployment.id == "dep_xxx"
        assert deployment.project_id == "proj_xxx"
        assert deployment.status == DeploymentStatus.QUEUED
        assert deployment.message == "Initial deployment"
        assert deployment.error_message is None
    
    def test_from_dict_status_as_integer(self, sample_deployment_data):
        """Should parse integer status."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        data = sample_deployment_data.copy()
        data["status"] = 6  # RUNNING
        
        deployment = Deployment.from_dict(data, mock_client)
        
        assert deployment.status == DeploymentStatus.RUNNING
    
    def test_from_dict_status_as_string(self, sample_deployment_data):
        """Should parse string status."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        data = sample_deployment_data.copy()
        data["status"] = "BUILDING"
        
        deployment = Deployment.from_dict(data, mock_client)
        
        assert deployment.status == DeploymentStatus.BUILDING
    
    def test_from_dict_nested_account_info(self, sample_deployment_data):
        """Should parse nested accountInfo."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        deployment = Deployment.from_dict(sample_deployment_data, mock_client)
        
        assert isinstance(deployment.account_info, AccountInfo)
        assert deployment.account_info.account_id == "acc_xxx"
    
    def test_from_dict_nested_artifacts_source(self, sample_deployment_data):
        """Should parse nested artifactsSource."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        deployment = Deployment.from_dict(sample_deployment_data, mock_client)
        
        assert isinstance(deployment.artifacts_source, ArtifactsSource)
        assert deployment.artifacts_source.sandbox_id == "sbx_xxx"
        assert deployment.artifacts_source.path == "/app/source"
    
    def test_from_dict_nested_metadata(self, sample_deployment_data):
        """Should parse nested metadata."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        deployment = Deployment.from_dict(sample_deployment_data, mock_client)
        
        assert isinstance(deployment.metadata, DeploymentMetadata)
        assert deployment.metadata.http_port == 3000
        assert deployment.metadata.environment_variables == {"NODE_ENV": "production"}
    
    def test_from_dict_nested_replica_spec(self, sample_deployment_data):
        """Should parse nested replicaSpec."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        deployment = Deployment.from_dict(sample_deployment_data, mock_client)
        
        assert isinstance(deployment.metadata.replica_spec, ReplicaSpec)
        assert deployment.metadata.replica_spec.cpu == "1"
        assert deployment.metadata.replica_spec.memory == "1Gi"
        assert deployment.metadata.replica_spec.max_replicas == 1
        assert deployment.metadata.replica_spec.min_replicas == 0
    
    def test_from_dict_datetime_parsing(self, sample_deployment_data):
        """Should parse datetime fields."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        deployment = Deployment.from_dict(sample_deployment_data, mock_client)
        
        assert isinstance(deployment.created_at, datetime)
    
    def test_convenience_properties(self, sample_deployment_data):
        """Should provide convenience properties from metadata."""
        mock_client = MagicMock(spec=DeploymentClient)
        deployment = Deployment.from_dict(sample_deployment_data, mock_client)
        
        assert deployment.cpu == "1"
        assert deployment.memory == "1Gi"
        assert deployment.max_replicas == 1
        assert deployment.min_replicas == 0
        assert deployment.http_port == 3000
        assert deployment.environment_variables == {"NODE_ENV": "production"}
    
    def test_is_terminal_property(self, sample_deployment_data):
        """Should check if deployment is in terminal state."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        # QUEUED is not terminal
        data = sample_deployment_data.copy()
        data["status"] = 1  # QUEUED
        deployment = Deployment.from_dict(data, mock_client)
        assert deployment.is_terminal is False
        
        # RUNNING is terminal
        data["status"] = 6  # RUNNING
        deployment = Deployment.from_dict(data, mock_client)
        assert deployment.is_terminal is True
        
        # BUILD_FAILED is terminal
        data["status"] = 3  # BUILD_FAILED
        deployment = Deployment.from_dict(data, mock_client)
        assert deployment.is_terminal is True
    
    def test_is_successful_property(self, sample_deployment_data):
        """Should check if deployment completed successfully."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        data = sample_deployment_data.copy()
        
        # RUNNING is successful
        data["status"] = 6  # RUNNING
        deployment = Deployment.from_dict(data, mock_client)
        assert deployment.is_successful is True
        
        # BUILD_FAILED is not successful
        data["status"] = 3  # BUILD_FAILED
        deployment = Deployment.from_dict(data, mock_client)
        assert deployment.is_successful is False
    
    def test_is_cancellable_property(self, sample_deployment_data):
        """Should check if deployment can be cancelled."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        data = sample_deployment_data.copy()
        
        # QUEUED is cancellable
        data["status"] = 1  # QUEUED
        deployment = Deployment.from_dict(data, mock_client)
        assert deployment.is_cancellable is True
        
        # BUILDING is cancellable
        data["status"] = 2  # BUILDING
        deployment = Deployment.from_dict(data, mock_client)
        assert deployment.is_cancellable is True
        
        # RUNNING is not cancellable
        data["status"] = 6  # RUNNING
        deployment = Deployment.from_dict(data, mock_client)
        assert deployment.is_cancellable is False


class TestDeploymentStatusPolling:
    """T020: Test deployment status polling logic."""
    
    def test_terminal_states_defined(self):
        """Should have terminal states defined."""
        assert DeploymentStatus.RUNNING in TERMINAL_STATES
        assert DeploymentStatus.IDLE in TERMINAL_STATES
        assert DeploymentStatus.INACTIVE in TERMINAL_STATES
        assert DeploymentStatus.BUILD_FAILED in TERMINAL_STATES
        assert DeploymentStatus.DEPLOY_FAILED in TERMINAL_STATES
        assert DeploymentStatus.CANCELLED in TERMINAL_STATES
        # 6 terminal states total
        assert len(TERMINAL_STATES) == 6
    
    def test_cancellable_states_defined(self):
        """Should have cancellable states defined."""
        assert DeploymentStatus.QUEUED in CANCELLABLE_STATES
        assert DeploymentStatus.BUILDING in CANCELLABLE_STATES
        assert DeploymentStatus.DEPLOYING in CANCELLABLE_STATES
        assert len(CANCELLABLE_STATES) == 3


class TestCancel:
    """T035: Test cancel method."""
    
    @pytest.fixture
    def mock_deployment_queued(self, sample_deployment_data):
        """Create QUEUED deployment with mocked client."""
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        
        data = sample_deployment_data.copy()
        data["status"] = 1  # QUEUED - cancellable
        
        return Deployment.from_dict(data, mock_client)
    
    @pytest.fixture
    def mock_deployment_building(self, sample_deployment_data):
        """Create BUILDING deployment with mocked client."""
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        
        data = sample_deployment_data.copy()
        data["status"] = 2  # BUILDING - cancellable
        
        return Deployment.from_dict(data, mock_client)
    
    @pytest.fixture
    def mock_deployment_running(self, sample_deployment_data):
        """Create RUNNING deployment with mocked client."""
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        
        data = sample_deployment_data.copy()
        data["status"] = 6  # RUNNING - not cancellable
        
        return Deployment.from_dict(data, mock_client)
    
    def test_cancel_queued_deployment(self, mock_deployment_queued):
        """Should cancel QUEUED deployment successfully."""
        mock_deployment_queued._client._http.post.return_value = {
            "projectId": "proj_xxx",
            "deploymentId": "dep_xxx",
            "previousStatus": 1,  # QUEUED
            "currentStatus": 9,  # CANCELLED
        }
        
        result = mock_deployment_queued.cancel(reason="Test cancellation")
        
        mock_deployment_queued._client._http.post.assert_called_once_with(
            "/projects/proj_xxx/deployments/dep_xxx/cancel",
            json={"reason": "Test cancellation"},
            context="Cancel deployment",
        )
        assert result.status == DeploymentStatus.CANCELLED
    
    def test_cancel_building_deployment(self, mock_deployment_building):
        """Should cancel BUILDING deployment successfully."""
        mock_deployment_building._client._http.post.return_value = {
            "projectId": "proj_xxx",
            "deploymentId": "dep_xxx",
            "previousStatus": 2,  # BUILDING
            "currentStatus": 9,  # CANCELLED
        }
        
        result = mock_deployment_building.cancel()
        
        # Without reason, should send empty payload
        mock_deployment_building._client._http.post.assert_called_once_with(
            "/projects/proj_xxx/deployments/dep_xxx/cancel",
            json={},
            context="Cancel deployment",
        )
        assert result.status == DeploymentStatus.CANCELLED

    def test_cancel_handles_string_status(self, mock_deployment_building):
        """Should update local status when backend returns string status."""
        mock_deployment_building._client._http.post.return_value = {
            "projectId": "proj_xxx",
            "deploymentId": "dep_xxx",
            "previousStatus": "DEPLOYMENT_STATUS_BUILDING",
            "currentStatus": "DEPLOYMENT_STATUS_CANCELLED",
        }

        result = mock_deployment_building.cancel()

        assert result.status == DeploymentStatus.CANCELLED
    
    def test_cancel_running_deployment_raises_error(self, mock_deployment_running):
        """Should raise error when trying to cancel RUNNING deployment."""
        from novita_sandbox.artifact_hosting.exceptions import DeploymentError
        
        with pytest.raises(DeploymentError) as exc_info:
            mock_deployment_running.cancel()
        
        assert "cannot be cancelled" in str(exc_info.value)
        assert "RUNNING" in str(exc_info.value)


class TestStreamLogs:
    """T036: Test stream_logs method - SSE log streaming."""
    
    @pytest.fixture
    def mock_deployment(self, sample_deployment_data):
        """Create deployment with mocked client."""
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        
        return Deployment.from_dict(sample_deployment_data, mock_client)
    
    def test_stream_logs_calls_correct_endpoint(self, mock_deployment):
        """Should call the correct SSE endpoint."""
        # Setup mock to return empty iterator (complete event)
        mock_deployment._client._http.stream_sse_events.return_value = iter([
            ("complete", "")
        ])
        
        # Call stream_logs
        list(mock_deployment.stream_logs())
        
        # Verify endpoint called
        mock_deployment._client._http.stream_sse_events.assert_called_once()
        call_args = mock_deployment._client._http.stream_sse_events.call_args
        path = call_args[0][0]
        assert f"/projects/{mock_deployment.project_id}/deployments/{mock_deployment.id}/logs/stream" in path
    
    def test_stream_logs_yields_log_entries(self, mock_deployment):
        """Should yield LogEntry objects from 'log' SSE events."""
        log_json = '{"line": "Building..."}'
        mock_deployment._client._http.stream_sse_events.return_value = iter([
            ("connected", '{"deployment_id": "test-id"}'),
            ("log", log_json),
            ("complete", '{"status": "IDLE"}'),
        ])
        
        logs = list(mock_deployment.stream_logs())
        
        assert len(logs) == 1
        assert logs[0].message == "Building..."
    
    def test_stream_logs_handles_connected_event(self, mock_deployment):
        """Should handle 'connected' event without yielding."""
        mock_deployment._client._http.stream_sse_events.return_value = iter([
            ("connected", '{"deployment_id": "test-id"}'),
            ("complete", '{"status": "IDLE"}'),
        ])
        
        logs = list(mock_deployment.stream_logs())
        
        assert len(logs) == 0
    
    def test_stream_logs_stops_on_complete_event(self, mock_deployment):
        """Should stop iteration on 'complete' event."""
        mock_deployment._client._http.stream_sse_events.return_value = iter([
            ("log", '{"line": "Done"}'),
            ("complete", '{"status": "IDLE"}'),
            ("log", '{"line": "Should not appear"}'),
        ])
        
        logs = list(mock_deployment.stream_logs())
        
        # Should only have the first log, not the one after complete
        assert len(logs) == 1
        assert logs[0].message == "Done"
    
    def test_stream_logs_raises_on_error_event(self, mock_deployment):
        """Should raise DeploymentError on 'error' event."""
        from novita_sandbox.artifact_hosting.exceptions import DeploymentError
        
        mock_deployment._client._http.stream_sse_events.return_value = iter([
            ("error", "Build failed: out of memory"),
        ])
        
        with pytest.raises(DeploymentError) as exc_info:
            list(mock_deployment.stream_logs())
        
        assert "out of memory" in str(exc_info.value)
    
    def test_stream_logs_handles_invalid_json(self, mock_deployment):
        """Should skip invalid JSON in 'log' events."""
        mock_deployment._client._http.stream_sse_events.return_value = iter([
            ("log", "not valid json"),
            ("log", '{"line": "Valid"}'),
            ("complete", '{"status": "IDLE"}'),
        ])
        
        logs = list(mock_deployment.stream_logs())
        
        # Should only yield the valid entry
        assert len(logs) == 1
        assert logs[0].message == "Valid"
