"""Unit tests for DeploymentClient (T015, T016, T050, T051).

Tests:
- T015: DeploymentClient initialization
- T016: create_project method
- T050: list_projects method (US4)
- T051: delete_project method (US4)
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from novita_sandbox.artifact_hosting.client import DeploymentClient
from novita_sandbox.artifact_hosting.exceptions import (
    DeploymentError,
    ProjectNotFoundError,
    QuotaExceededError,
    ValidationError,
)
from novita_sandbox.artifact_hosting.models.project import Project


class TestDeploymentClientInit:
    """T015: Test DeploymentClient initialization."""
    
    def test_init_with_api_key(self):
        """Should initialize with explicit API key."""
        client = DeploymentClient(api_key="test-api-key")
        
        assert client.api_key == "test-api-key"
        assert client.base_url == "https://artifact.novita.ai/v1"
        assert client.timeout == 30.0
        
        client.close()
    
    def test_init_with_env_var(self):
        """Should read API key from NOVITA_API_KEY environment variable."""
        with patch.dict(os.environ, {"NOVITA_API_KEY": "env-api-key"}):
            client = DeploymentClient()
            
            assert client.api_key == "env-api-key"
            
            client.close()
    
    def test_init_without_api_key_raises_error(self):
        """Should raise ValueError if no API key provided."""
        with patch.dict(os.environ, {"NOVITA_API_KEY": ""}, clear=True):
            # Also clear the env var by setting it empty
            env_backup = os.environ.pop("NOVITA_API_KEY", None)
            try:
                with pytest.raises(ValueError) as exc_info:
                    DeploymentClient()
                
                assert "API key is required" in str(exc_info.value)
            finally:
                if env_backup:
                    os.environ["NOVITA_API_KEY"] = env_backup
    
    def test_init_uses_fixed_base_url(self):
        """Should use fixed base URL (not configurable)."""
        client = DeploymentClient(api_key="test-key")
        
        # URL is fixed, cannot be changed
        assert client.base_url == "https://artifact.novita.ai/v1"
        
        client.close()
    
    def test_init_with_custom_timeout(self):
        """Should accept custom timeout."""
        client = DeploymentClient(
            api_key="test-key",
            timeout=60.0,
        )
        
        assert client.timeout == 60.0
        
        client.close()
    
    def test_context_manager(self):
        """Should work as context manager."""
        with DeploymentClient(api_key="test-key") as client:
            assert client.api_key == "test-key"


class TestCreateProject:
    """T016: Test create_project method."""
    
    @pytest.fixture
    def mock_client(self, sample_project_data):
        """Create client with mocked HTTP."""
        client = DeploymentClient(api_key="test-key")
        client._http = MagicMock()
        client._http.post.return_value = sample_project_data
        return client
    
    def test_create_project_basic(self, mock_client, sample_project_data):
        """Should create project with just name."""
        project = mock_client.create_project(name="my-app")
        
        assert isinstance(project, Project)
        assert project.id == "proj_xxx"
        assert project.name == "my-app"
        
        # Verify API call
        mock_client._http.post.assert_called_once()
        call_args = mock_client._http.post.call_args
        assert call_args[0][0] == "/projects"
        assert call_args[1]["json"]["name"] == "my-app"
    
    def test_create_project_with_description(self, mock_client, sample_project_data):
        """Should create project with description."""
        project = mock_client.create_project(
            name="my-app",
            description="Test description",
        )
        
        call_args = mock_client._http.post.call_args
        assert call_args[1]["json"]["description"] == "Test description"
    
    def test_create_project_with_request_timeout(self, mock_client, sample_project_data):
        """Should create project with request timeout config (string per OpenAPI spec)."""
        project = mock_client.create_project(
            name="my-app",
            request_timeout_seconds="60",
        )
        
        call_args = mock_client._http.post.call_args
        assert call_args[1]["json"]["endpointConfig"]["requestTimeoutSeconds"] == "60"
    
    def test_create_project_validates_name(self, mock_client):
        """Should validate project name format."""
        with pytest.raises(ValueError) as exc_info:
            mock_client.create_project(name="Invalid Name!")
        
        assert "Invalid project name" in str(exc_info.value)
    
    def test_create_project_name_too_short(self, mock_client):
        """Should reject project name shorter than 3 chars."""
        with pytest.raises(ValueError) as exc_info:
            mock_client.create_project(name="ab")
        
        assert "must be between 3 and 63 characters" in str(exc_info.value)
    
    def test_create_project_name_must_start_with_letter(self, mock_client):
        """Should reject project name starting with non-letter."""
        with pytest.raises(ValueError) as exc_info:
            mock_client.create_project(name="123-app")
        
        assert "Invalid project name" in str(exc_info.value)
    
    def test_create_project_valid_names(self, mock_client, sample_project_data):
        """Should accept valid project names."""
        valid_names = [
            "abc",  # Minimum length
            "my-app",  # With hyphen
            "my-app-123",  # With numbers
            "a" + "b" * 62,  # Maximum length (63 chars)
        ]
        
        for name in valid_names:
            project = mock_client.create_project(name=name)
            assert project is not None


class TestGetProject:
    """Test get_project method."""
    
    @pytest.fixture
    def mock_client(self, sample_project_data):
        """Create client with mocked HTTP."""
        client = DeploymentClient(api_key="test-key")
        client._http = MagicMock()
        client._http.get.return_value = sample_project_data
        return client
    
    def test_get_project_by_id(self, mock_client):
        """Should get project by ID."""
        project = mock_client.get_project("proj_xxx")
        
        assert isinstance(project, Project)
        assert project.id == "proj_xxx"
        
        mock_client._http.get.assert_called_once()
        call_args = mock_client._http.get.call_args
        assert "/projects/proj_xxx" in call_args[0][0]
    
    def test_get_project_by_name(self, mock_client):
        """Should get project by name."""
        project = mock_client.get_project("my-app")
        
        call_args = mock_client._http.get.call_args
        assert "/projects/my-app" in call_args[0][0]


class TestListProjects:
    """T050: Test list_projects method."""
    
    @pytest.fixture
    def mock_client(self, sample_project_data):
        """Create client with mocked HTTP."""
        client = DeploymentClient(api_key="test-key")
        client._http = MagicMock()
        client._http.get.return_value = {
            "projects": [sample_project_data, sample_project_data]
        }
        return client
    
    def test_list_projects_returns_iterator(self, mock_client):
        """Should return iterator of projects."""
        projects = mock_client.list_projects()
        
        # Should be an iterator
        project_list = list(projects)
        assert len(project_list) == 2
        assert all(isinstance(p, Project) for p in project_list)
    
    def test_list_projects_with_status_filter(self, mock_client, sample_project_data):
        """Should filter by status."""
        list(mock_client.list_projects(status=[1, 2]))
        
        call_args = mock_client._http.get.call_args
        assert call_args[1]["params"]["filters.status"] == "1,2"
    
    def test_list_projects_handles_array_response(self, mock_client, sample_project_data):
        """Should handle direct array response wrapped in dict."""
        # Backend always returns dict, but projects might be in different keys
        mock_client._http.get.return_value = {"projects": [sample_project_data]}
        
        projects = list(mock_client.list_projects())
        assert len(projects) == 1


class TestDeleteProject:
    """T051: Test delete_project method."""
    
    @pytest.fixture
    def mock_client(self):
        """Create client with mocked HTTP."""
        client = DeploymentClient(api_key="test-key")
        client._http = MagicMock()
        client._http.delete.return_value = None
        return client
    
    def test_delete_project_basic(self, mock_client):
        """Should delete project (soft delete)."""
        mock_client.delete_project("proj_xxx")
        
        mock_client._http.delete.assert_called_once()
        call_args = mock_client._http.delete.call_args
        assert "/projects/proj_xxx" in call_args[0][0]
