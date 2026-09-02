"""Unit tests for Project model (T017, T019, T033, T034, T046, T049).

Tests:
- T017: Project model including nested objects
- T019: deploy method with dockerfile path vs content detection
- T033: list_deployments method (US2)
- T034: get_deployment method (US2)
- T046: rollback method (US3)
- T049: update method (US4)
"""

from datetime import datetime
from unittest.mock import MagicMock, patch
from typing import Any, Dict

import pytest

from novita_sandbox.artifact_hosting.client import DeploymentClient
from novita_sandbox.artifact_hosting.models.deployment import Deployment
from novita_sandbox.artifact_hosting.models.enums import DeploymentStatus
from novita_sandbox.artifact_hosting.models.project import Project
from novita_sandbox.artifact_hosting.models.nested import (
    AccountInfo,
    Endpoint,
    EndpointConfig,
)


class TestProjectModel:
    """T017: Test Project model with nested objects."""
    
    def test_from_dict_basic(self, sample_project_data):
        """Should parse basic project data."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        project = Project.from_dict(sample_project_data, mock_client)
        
        assert project.id == "proj_xxx"
        assert project.name == "my-app"
        assert project.description == "A test project"
        assert project.status == 1
        assert project.deployment_count == 0
        assert project.current_deployment_id is None
    
    def test_from_dict_nested_account_info(self, sample_project_data):
        """Should parse nested accountInfo."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        project = Project.from_dict(sample_project_data, mock_client)
        
        assert isinstance(project.account_info, AccountInfo)
        assert project.account_info.account_id == "acc_xxx"
        assert project.account_info.team_id == "team_xxx"
        assert project.account_info.member_id == "member_xxx"
    
    def test_from_dict_nested_endpoint(self, sample_project_data):
        """Should parse nested endpoint."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        project = Project.from_dict(sample_project_data, mock_client)
        
        assert isinstance(project.endpoint, Endpoint)
        assert project.endpoint.default_url == "https://my-app.novita.space"
        assert project.endpoint.custom_url is None
    
    def test_from_dict_nested_endpoint_config(self, sample_project_data):
        """Should parse nested endpointConfig."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        project = Project.from_dict(sample_project_data, mock_client)
        
        assert isinstance(project.endpoint_config, EndpointConfig)
        assert project.endpoint_config.request_timeout_seconds == 30
    
    def test_from_dict_datetime_parsing(self, sample_project_data):
        """Should parse datetime fields."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        project = Project.from_dict(sample_project_data, mock_client)
        
        assert isinstance(project.created_at, datetime)
        assert isinstance(project.updated_at, datetime)
    
    def test_url_property(self, sample_project_data):
        """Should return default URL via url property."""
        mock_client = MagicMock(spec=DeploymentClient)
        project = Project.from_dict(sample_project_data, mock_client)
        
        assert project.url == "https://my-app.novita.space"
    
    def test_from_dict_with_projectId_key(self, sample_project_data):
        """Should handle projectId key from API response."""
        mock_client = MagicMock(spec=DeploymentClient)
        
        project = Project.from_dict(sample_project_data, mock_client)
        
        assert project.id == "proj_xxx"
    
    def test_from_dict_with_id_key(self):
        """Should fallback to id key if projectId not present."""
        mock_client = MagicMock(spec=DeploymentClient)
        data = {
            "id": "proj_123",
            "name": "test-app",
            "status": 1,
        }
        
        project = Project.from_dict(data, mock_client)
        
        assert project.id == "proj_123"


class TestDeployMethod:
    """T019: Test deploy method with dockerfile path vs content detection."""
    
    @pytest.fixture
    def mock_project(self, sample_project_data, sample_deployment_data):
        """Create project with mocked client."""
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        mock_client._http.post.return_value = sample_deployment_data
        
        project = Project.from_dict(sample_project_data, mock_client)
        return project
    
    def test_deploy_basic(self, mock_project):
        """Should create deployment with basic params."""
        deployment = mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            wait=False,
        )
        
        assert isinstance(deployment, Deployment)
        assert deployment.id == "dep_xxx"
        
        # Verify API call
        mock_project._client._http.post.assert_called_once()
        call_args = mock_project._client._http.post.call_args
        assert f"/projects/{mock_project.id}/deploy" in call_args[0][0]
    
    def test_deploy_with_dockerfile_content(self, mock_project):
        """Should detect dockerfile content with newline."""
        dockerfile_content = "FROM python:3.11\nRUN pip install flask"
        
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            dockerfile=dockerfile_content,
            wait=False,
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        assert payload["dockerfile"] == dockerfile_content
    
    def test_deploy_with_dockerfile_content_from_keyword(self, mock_project):
        """Should detect dockerfile content starting with FROM."""
        dockerfile_content = "FROM node:18-alpine"
        
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            dockerfile=dockerfile_content,
            wait=False,
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        assert payload["dockerfile"] == dockerfile_content
    
    def test_deploy_with_dockerfile_path(self, mock_project):
        """Should pass dockerfile path to backend."""
        dockerfile_path = "docker/Dockerfile.prod"
        
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            dockerfile=dockerfile_path,
            wait=False,
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        # Path is passed as-is, backend will resolve
        assert payload["dockerfile"] == dockerfile_path
    
    def test_deploy_with_environment_variables(self, mock_project):
        """Should include environment variables in metadata."""
        env_vars = {"NODE_ENV": "production", "DEBUG": "false"}
        
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            environment_variables=env_vars,
            wait=False,
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        assert payload["metadata"]["environmentVariables"] == env_vars
    
    def test_deploy_with_resource_config(self, mock_project):
        """Should include resource configuration."""
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            cpu="2",
            memory="2Gi",
            max_replicas=3,
            min_replicas=1,
            wait=False,
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        replica_spec = payload["metadata"]["replicaSpec"]
        
        assert replica_spec["cpu"] == "2"
        assert replica_spec["memory"] == "2Gi"
        assert replica_spec["maxReplicas"] == 3
        assert replica_spec["minReplicas"] == 1
    
    def test_deploy_with_http_port(self, mock_project):
        """Should include httpPort in metadata."""
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            http_port=8080,
            wait=False,
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        assert payload["metadata"]["httpPort"] == 8080
    
    def test_deploy_with_check_health_path(self, mock_project):
        """Should include checkHealthPath in metadata."""
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            check_health_path="/health",
            wait=False,
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        assert payload["metadata"]["checkHealthPath"] == "/health"
    
    def test_deploy_with_message(self, mock_project):
        """Should include deployment message."""
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            message="First deployment",
            wait=False,
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        assert payload["message"] == "First deployment"
    
    def test_deploy_validates_environment_variables(self, mock_project):
        """Should validate environment variable keys."""
        with pytest.raises(ValueError) as exc_info:
            mock_project.deploy(
                sandbox_id="sbx-123",
                arti_dir="/app/source",
                environment_variables={"invalid-key": "value"},
                wait=False,
            )
        
        assert "Invalid environment variable key" in str(exc_info.value)
    
    def test_deploy_artifacts_source_structure(self, mock_project):
        """Should structure artifactsSource correctly."""
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            wait=False,
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        
        assert payload["artifactsSource"]["sandboxId"] == "sbx-123"
        assert payload["artifactsSource"]["path"] == "/app/source"


class TestListDeployments:
    """T033: Test list_deployments method."""
    
    @pytest.fixture
    def mock_project(self, sample_project_data, sample_deployment_data):
        """Create project with mocked client."""
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        mock_client._http.get.return_value = {
            "deployments": [sample_deployment_data, sample_deployment_data]
        }
        
        return Project.from_dict(sample_project_data, mock_client)
    
    def test_list_deployments_returns_iterator(self, mock_project):
        """Should return iterator of deployments."""
        deployments = mock_project.list_deployments()
        
        deployment_list = list(deployments)
        assert len(deployment_list) == 2
        assert all(isinstance(d, Deployment) for d in deployment_list)
    
    def test_list_deployments_with_status_filter(self, mock_project):
        """Should filter by status."""
        list(mock_project.list_deployments(status=[0, 1]))  # QUEUED, BUILDING
        
        call_args = mock_project._client._http.get.call_args
        assert call_args[1]["params"]["filters.status"] == "0,1"


class TestGetDeployment:
    """T034: Test get_deployment method."""
    
    @pytest.fixture
    def mock_project(self, sample_project_data, sample_deployment_data):
        """Create project with mocked client."""
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        mock_client._http.get.return_value = sample_deployment_data
        
        return Project.from_dict(sample_project_data, mock_client)
    
    def test_get_deployment(self, mock_project):
        """Should get deployment by ID."""
        deployment = mock_project.get_deployment("dep_xxx")
        
        assert isinstance(deployment, Deployment)
        assert deployment.id == "dep_xxx"


class TestRollback:
    """T046: Test rollback method."""
    
    @pytest.fixture
    def mock_project(self, sample_project_data, sample_rollback_response):
        """Create project with mocked client."""
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        mock_client._http.post.return_value = sample_rollback_response
        
        return Project.from_dict(sample_project_data, mock_client)
    
    def test_rollback_returns_dict(self, mock_project):
        """Should return dictionary with IDs."""
        result = mock_project.rollback(target_deployment_id="dep_target")
        
        assert isinstance(result, dict)
        assert result["project_id"] == "proj_xxx"
        assert result["previous_deployment_id"] == "dep_old"
        assert result["current_deployment_id"] == "dep_target"
    
    def test_rollback_with_reason(self, mock_project):
        """Should include reason in request."""
        mock_project.rollback(
            target_deployment_id="dep_target",
            reason="Rollback due to bug",
        )
        
        call_args = mock_project._client._http.post.call_args
        payload = call_args[1]["json"]
        assert payload["reason"] == "Rollback due to bug"
    
    def test_rollback_updates_current_deployment_id(self, mock_project):
        """Should update local current_deployment_id."""
        mock_project.rollback(target_deployment_id="dep_target")
        
        assert mock_project.current_deployment_id == "dep_target"


class TestUpdate:
    """T049: Test update method."""
    
    @pytest.fixture
    def mock_project(self, sample_project_data):
        """Create project with mocked client."""
        updated_data = sample_project_data.copy()
        updated_data["name"] = "new-name"
        updated_data["description"] = "Updated description"
        
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        mock_client._http.patch.return_value = updated_data
        
        return Project.from_dict(sample_project_data, mock_client)
    
    def test_update_name(self, mock_project):
        """Should update project name via PATCH."""
        result = mock_project.update(name="new-name")
        
        assert result is mock_project  # Returns self
        assert mock_project.name == "new-name"
    
    def test_update_description(self, mock_project):
        """Should update description via PATCH."""
        mock_project.update(description="Updated description")
        
        assert mock_project.description == "Updated description"
    
    def test_update_request_timeout(self, mock_project):
        """Should update request timeout via PATCH."""
        mock_project._client._http.patch = mock_project._client._http.put  # Mock patch method
        mock_project.update(request_timeout_seconds="120")
        
        call_args = mock_project._client._http.patch.call_args
        payload = call_args[1]["json"]
        # Check nested payload structure per OpenAPI spec
        assert payload["payload"]["endpointConfig"]["requestTimeoutSeconds"] == "120"
    
    def test_update_validates_name(self, mock_project):
        """Should validate new name."""
        with pytest.raises(ValueError):
            mock_project.update(name="Invalid Name!")
    
    def test_update_no_changes(self, mock_project):
        """Should return self if no changes."""
        result = mock_project.update()
        
        assert result is mock_project
        mock_project._client._http.patch.assert_not_called()
