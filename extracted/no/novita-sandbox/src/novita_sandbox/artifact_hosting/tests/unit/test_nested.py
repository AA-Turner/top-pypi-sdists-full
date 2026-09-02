"""Unit tests for nested model classes in Artifact Hosting SDK V2."""

import pytest

from novita_sandbox.artifact_hosting.models.nested import (
    AccountInfo,
    ArtifactsSource,
    DeploymentMetadata,
    Endpoint,
    EndpointConfig,
    ReplicaSpec,
)


class TestAccountInfo:
    """Tests for AccountInfo dataclass."""
    
    def test_from_dict_full(self):
        """Test creating AccountInfo from complete dictionary."""
        data = {
            "accountId": "acc-123",
            "teamId": "team-456",
            "memberId": "member-789",
        }
        
        info = AccountInfo.from_dict(data)
        
        assert info.account_id == "acc-123"
        assert info.team_id == "team-456"
        assert info.member_id == "member-789"
    
    def test_from_dict_minimal(self):
        """Test creating AccountInfo with only required fields."""
        data = {"accountId": "acc-123"}
        
        info = AccountInfo.from_dict(data)
        
        assert info.account_id == "acc-123"
        assert info.team_id is None
        assert info.member_id is None
    
    def test_from_dict_empty(self):
        """Test creating AccountInfo from empty dictionary."""
        info = AccountInfo.from_dict({})
        
        assert info.account_id == ""
        assert info.team_id is None
        assert info.member_id is None
    
    def test_to_dict_full(self):
        """Test converting AccountInfo to dictionary with all fields."""
        info = AccountInfo(
            account_id="acc-123",
            team_id="team-456",
            member_id="member-789",
        )
        
        result = info.to_dict()
        
        assert result == {
            "accountId": "acc-123",
            "teamId": "team-456",
            "memberId": "member-789",
        }
    
    def test_to_dict_minimal(self):
        """Test converting AccountInfo to dictionary with minimal fields."""
        info = AccountInfo(account_id="acc-123")
        
        result = info.to_dict()
        
        assert result == {"accountId": "acc-123"}
        assert "teamId" not in result
        assert "memberId" not in result


class TestEndpoint:
    """Tests for Endpoint dataclass."""
    
    def test_from_dict_full(self):
        """Test creating Endpoint from complete dictionary."""
        data = {
            "defaultUrl": "https://my-app.novita.space",
            "customUrl": "https://my-app.example.com",
        }
        
        endpoint = Endpoint.from_dict(data)
        
        assert endpoint.default_url == "https://my-app.novita.space"
        assert endpoint.custom_url == "https://my-app.example.com"
    
    def test_from_dict_minimal(self):
        """Test creating Endpoint with only default URL."""
        data = {"defaultUrl": "https://my-app.novita.space"}
        
        endpoint = Endpoint.from_dict(data)
        
        assert endpoint.default_url == "https://my-app.novita.space"
        assert endpoint.custom_url is None
    
    def test_from_dict_empty(self):
        """Test creating Endpoint from empty dictionary."""
        endpoint = Endpoint.from_dict({})
        
        assert endpoint.default_url is None
        assert endpoint.custom_url is None
    
    def test_to_dict(self):
        """Test converting Endpoint to dictionary."""
        endpoint = Endpoint(
            default_url="https://my-app.novita.space",
            custom_url="https://my-app.example.com",
        )
        
        result = endpoint.to_dict()
        
        assert result == {
            "defaultUrl": "https://my-app.novita.space",
            "customUrl": "https://my-app.example.com",
        }


class TestEndpointConfig:
    """Tests for EndpointConfig dataclass."""
    
    def test_from_dict_full(self):
        """Test creating EndpointConfig from complete dictionary."""
        data = {
            "customDomain": "my-app.example.com",
            "requestTimeoutSeconds": 300,
        }
        
        config = EndpointConfig.from_dict(data)
        
        assert config.custom_domain == "my-app.example.com"
        assert config.request_timeout_seconds == 300
    
    def test_from_dict_empty(self):
        """Test creating EndpointConfig from empty dictionary."""
        config = EndpointConfig.from_dict({})
        
        assert config.custom_domain is None
        assert config.request_timeout_seconds is None
    
    def test_to_dict(self):
        """Test converting EndpointConfig to dictionary."""
        config = EndpointConfig(
            custom_domain="my-app.example.com",
            request_timeout_seconds=300,
        )
        
        result = config.to_dict()
        
        assert result == {
            "customDomain": "my-app.example.com",
            "requestTimeoutSeconds": 300,
        }


class TestArtifactsSource:
    """Tests for ArtifactsSource dataclass."""
    
    def test_from_dict_full(self):
        """Test creating ArtifactsSource from complete dictionary."""
        data = {
            "sandboxId": "sbx-123",
            "path": "/app/source",
        }
        
        source = ArtifactsSource.from_dict(data)
        
        assert source.sandbox_id == "sbx-123"
        assert source.path == "/app/source"
    
    def test_from_dict_empty(self):
        """Test creating ArtifactsSource from empty dictionary."""
        source = ArtifactsSource.from_dict({})
        
        assert source.sandbox_id == ""
        assert source.path == ""
    
    def test_to_dict(self):
        """Test converting ArtifactsSource to dictionary."""
        source = ArtifactsSource(
            sandbox_id="sbx-123",
            path="/app/source",
        )
        
        result = source.to_dict()
        
        assert result == {
            "sandboxId": "sbx-123",
            "path": "/app/source",
        }


class TestReplicaSpec:
    """Tests for ReplicaSpec dataclass."""
    
    def test_from_dict_full(self):
        """Test creating ReplicaSpec from complete dictionary."""
        data = {
            "cpu": "2",
            "memory": "2Gi",
            "maxReplicas": 3,
            "minReplicas": 1,
        }
        
        spec = ReplicaSpec.from_dict(data)
        
        assert spec.cpu == "2"
        assert spec.memory == "2Gi"
        assert spec.max_replicas == 3
        assert spec.min_replicas == 1
    
    def test_from_dict_empty_uses_defaults(self):
        """Test creating ReplicaSpec from empty dictionary uses defaults."""
        spec = ReplicaSpec.from_dict({})
        
        assert spec.cpu == "1"
        assert spec.memory == "1Gi"
        assert spec.max_replicas == 1
        assert spec.min_replicas == 0
    
    def test_to_dict(self):
        """Test converting ReplicaSpec to dictionary."""
        spec = ReplicaSpec(
            cpu="2",
            memory="2Gi",
            max_replicas=3,
            min_replicas=1,
        )
        
        result = spec.to_dict()
        
        assert result == {
            "cpu": "2",
            "memory": "2Gi",
            "maxReplicas": 3,
            "minReplicas": 1,
        }
    
    def test_default_values(self):
        """Test default values for ReplicaSpec."""
        spec = ReplicaSpec()
        
        assert spec.cpu == "1"
        assert spec.memory == "1Gi"
        assert spec.max_replicas == 1
        assert spec.min_replicas == 0


class TestDeploymentMetadata:
    """Tests for DeploymentMetadata dataclass."""
    
    def test_from_dict_full(self):
        """Test creating DeploymentMetadata from complete dictionary."""
        data = {
            "environmentVariables": {"FOO": "bar", "BAZ": "qux"},
            "httpPort": 8080,
            "checkHealthPath": "/health",
            "replicaSpec": {
                "cpu": "2",
                "memory": "4Gi",
                "maxReplicas": 5,
                "minReplicas": 2,
            },
        }
        
        metadata = DeploymentMetadata.from_dict(data)
        
        assert metadata.environment_variables == {"FOO": "bar", "BAZ": "qux"}
        assert metadata.http_port == 8080
        assert metadata.check_health_path == "/health"
        assert metadata.replica_spec.cpu == "2"
        assert metadata.replica_spec.memory == "4Gi"
        assert metadata.replica_spec.max_replicas == 5
        assert metadata.replica_spec.min_replicas == 2
    
    def test_from_dict_empty_uses_defaults(self):
        """Test creating DeploymentMetadata from empty dictionary uses defaults."""
        metadata = DeploymentMetadata.from_dict({})
        
        assert metadata.environment_variables == {}
        assert metadata.http_port == 3000
        assert metadata.check_health_path is None
        assert metadata.replica_spec.cpu == "1"
        assert metadata.replica_spec.memory == "1Gi"
    
    def test_to_dict_full(self):
        """Test converting DeploymentMetadata to dictionary with all fields."""
        metadata = DeploymentMetadata(
            environment_variables={"FOO": "bar"},
            http_port=8080,
            check_health_path="/health",
            replica_spec=ReplicaSpec(cpu="2", memory="4Gi", max_replicas=3, min_replicas=1),
        )
        
        result = metadata.to_dict()
        
        assert result["httpPort"] == 8080
        assert result["environmentVariables"] == {"FOO": "bar"}
        assert result["checkHealthPath"] == "/health"
        assert result["replicaSpec"]["cpu"] == "2"
    
    def test_to_dict_minimal(self):
        """Test converting DeploymentMetadata to dictionary with minimal fields."""
        metadata = DeploymentMetadata()
        
        result = metadata.to_dict()
        
        assert result["httpPort"] == 3000
        assert "replicaSpec" in result
        assert "environmentVariables" not in result  # Empty dict not included
        assert "checkHealthPath" not in result
    
    def test_default_values(self):
        """Test default values for DeploymentMetadata."""
        metadata = DeploymentMetadata()
        
        assert metadata.environment_variables == {}
        assert metadata.http_port == 3000
        assert metadata.check_health_path is None
        assert metadata.replica_spec.cpu == "1"
