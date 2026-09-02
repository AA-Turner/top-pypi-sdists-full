"""
Data Model Unit Tests

Tests validation, serialization and deserialization functionality of Pydantic data models.
"""

import pytest
from datetime import datetime
from typing import Dict, Any
from pydantic import ValidationError

from novita_sandbox.agent_runtime.runtime.models import (
    AgentConfig,
    AgentMetadata,
    AgentSpec,
    AgentStatus,
    RuntimeSpec,
    SandboxSpec,
    RuntimeConfig,
    DeploymentPhase,
    InvocationResponse,
    PingResponse,
    PingStatus,
)


class TestAgentMetadata:
    """AgentMetadata model tests"""
    
    @pytest.mark.unit
    def test_valid_metadata_creation(self):
        """Test valid metadata creation"""
        metadata = AgentMetadata(
            name="test-agent",
            version="1.0.0",
            author="test@example.com",
            description="Test agent",
            created="2024-01-01T00:00:00Z"
        )
        
        assert metadata.name == "test-agent"
        assert metadata.version == "1.0.0"
        assert metadata.author == "test@example.com"
        assert metadata.description == "Test agent"
        assert metadata.created == "2024-01-01T00:00:00Z"
    
    @pytest.mark.unit
    def test_minimal_metadata(self):
        """Test minimal metadata (only required fields)"""
        metadata = AgentMetadata(
            name="minimal-agent",
            version="1.0.0",
            author="minimal@example.com"
        )
        
        assert metadata.name == "minimal-agent"
        assert metadata.version == "1.0.0"
        assert metadata.author == "minimal@example.com"
        assert metadata.description is None
        assert metadata.created is None
    
    @pytest.mark.unit
    def test_missing_required_fields(self):
        """Test missing required fields"""
        with pytest.raises(ValidationError):
            AgentMetadata(version="1.0.0")  # Missing name and author


class TestRuntimeSpec:
    """RuntimeSpec model tests"""
    
    @pytest.mark.unit
    def test_valid_runtime_spec(self):
        """Test valid runtime spec"""
        spec = RuntimeSpec(
            timeout=300,
            memory_limit="1Gi",
            cpu_limit="1"
        )
        
        assert spec.timeout == 300
        assert spec.memory_limit == "1Gi"
        assert spec.cpu_limit == "1"
    
    @pytest.mark.unit
    def test_timeout_validation(self):
        """Test timeout validation"""
        # Valid timeout values
        RuntimeSpec(timeout=1)  # Minimum value
        RuntimeSpec(timeout=3600)  # Maximum value
        RuntimeSpec(timeout=300)  # Middle value
        
        # Invalid timeout values
        with pytest.raises(ValidationError):
            RuntimeSpec(timeout=0)  # Less than minimum
        
        with pytest.raises(ValidationError):
            RuntimeSpec(timeout=3601)  # Greater than maximum
    
    @pytest.mark.unit
    def test_optional_fields(self):
        """Test optional fields"""
        spec = RuntimeSpec()
        
        assert spec.timeout is None
        assert spec.memory_limit is None
        assert spec.cpu_limit is None


class TestAgentSpec:
    """AgentSpec model tests"""
    
    @pytest.mark.unit
    def test_valid_agent_spec(self):
        """Test valid Agent spec"""
        spec = AgentSpec(
            entrypoint="agent.py",
            runtime=RuntimeSpec(timeout=300),
            sandbox=SandboxSpec(template_id="tmpl_123")
        )
        
        assert spec.entrypoint == "agent.py"
        assert spec.runtime.timeout == 300
        assert spec.sandbox.template_id == "tmpl_123"
    
    @pytest.mark.unit
    def test_entrypoint_validation(self):
        """Test entrypoint file validation"""
        # Valid Python files
        AgentSpec(entrypoint="agent.py")
        AgentSpec(entrypoint="my_agent.py")
        AgentSpec(entrypoint="path/to/agent.py")
        
        # Invalid file extensions
        with pytest.raises(ValidationError):
            AgentSpec(entrypoint="agent.js")
        
        with pytest.raises(ValidationError):
            AgentSpec(entrypoint="agent")
        
        with pytest.raises(ValidationError):
            AgentSpec(entrypoint="agent.txt")


class TestAgentConfig:
    """AgentConfig model tests"""
    
    @pytest.mark.unit
    def test_complete_agent_config(self):
        """Test complete Agent configuration"""
        config = AgentConfig(
            apiVersion="v1",
            kind="Agent",
            metadata=AgentMetadata(
                name="test-agent",
                version="1.0.0",
                author="test@example.com",
                description="Test Agent"
            ),
            spec=AgentSpec(
                entrypoint="agent.py",
                runtime=RuntimeSpec(
                    timeout=300,
                    memory_limit="1Gi",
                    cpu_limit="1"
                ),
                sandbox=SandboxSpec(template_id="tmpl_123")
            ),
            status=AgentStatus(
                phase=DeploymentPhase.DEPLOYED,
                template_id="tmpl_123",
                last_deployed="2024-01-01T00:00:00Z"
            )
        )
        
        assert config.apiVersion == "v1"
        assert config.kind == "Agent"
        assert config.metadata.name == "test-agent"
        assert config.spec.entrypoint == "agent.py"
        assert config.status.phase == DeploymentPhase.DEPLOYED
    
    @pytest.mark.unit
    def test_minimal_agent_config(self):
        """Test minimal Agent configuration"""
        config = AgentConfig(
            metadata=AgentMetadata(
                name="minimal-agent",
                version="1.0.0",
                author="minimal@example.com"
            ),
            spec=AgentSpec(entrypoint="agent.py")
        )
        
        assert config.apiVersion == "v1"  # Default value
        assert config.kind == "Agent"  # Default value
        assert config.status is None  # Optional


class TestRuntimeConfig:
    """RuntimeConfig model tests"""
    
    @pytest.mark.unit
    def test_default_runtime_config(self):
        """Test default runtime configuration"""
        config = RuntimeConfig()
        
        assert config.host == "0.0.0.0"
        assert config.port == 8080
        assert config.debug is False
        assert config.timeout == 300
        assert config.max_request_size == 1024 * 1024
        assert config.cors_origins == ["*"]
        assert config.enable_metrics is True
        assert config.enable_middleware is True


class TestInvocationResponse:
    """InvocationResponse model tests"""
    
    @pytest.mark.unit
    def test_successful_response(self):
        """Test successful response"""
        response = InvocationResponse(
            result={"output": "test result"},
            status="success",
            duration=1.5,
            metadata={"processed": True}
        )
        
        assert response.result == {"output": "test result"}
        assert response.status == "success"
        assert response.duration == 1.5
        assert response.metadata == {"processed": True}
        assert response.error is None


class TestPingResponse:
    """PingResponse model tests"""
    
    @pytest.mark.unit
    def test_healthy_ping_response(self):
        """Test healthy Ping response"""
        response = PingResponse(
            status=PingStatus.HEALTHY,
            message="All systems operational",
            timestamp="2024-01-01T00:00:00Z"
        )
        
        assert response.status == PingStatus.HEALTHY
        assert response.message == "All systems operational"
        assert response.timestamp == "2024-01-01T00:00:00Z"
    
    @pytest.mark.unit
    def test_default_ping_response(self):
        """Test default Ping response"""
        response = PingResponse()
        
        assert response.status == PingStatus.HEALTHY
        assert response.message is None
        assert response.timestamp is None


class TestModelSerialization:
    """Model serialization tests"""
    
    @pytest.mark.unit
    def test_agent_config_serialization(self):
        """Test AgentConfig serialization"""
        config = AgentConfig(
            metadata=AgentMetadata(
                name="test-agent",
                version="1.0.0",
                author="test@example.com"
            ),
            spec=AgentSpec(entrypoint="agent.py")
        )
        
        # Serialize to dictionary
        config_dict = config.dict()
        assert isinstance(config_dict, dict)
        assert config_dict["apiVersion"] == "v1"
        assert config_dict["kind"] == "Agent"
        assert config_dict["metadata"]["name"] == "test-agent"
        
        # Deserialize from dictionary
        new_config = AgentConfig(**config_dict)
        assert new_config.metadata.name == config.metadata.name
        assert new_config.spec.entrypoint == config.spec.entrypoint
    
    @pytest.mark.unit
    def test_json_serialization(self):
        """Test JSON serialization"""
        response = InvocationResponse(
            result="Test",
            status="success",
            duration=1.0,
            metadata={"key": "value"}
        )
        
        # Test JSON serialization
        json_str = response.json()
        assert isinstance(json_str, str)
        assert "Test" in json_str
        assert "success" in json_str
        
        # Test deserialization from JSON
        parsed = InvocationResponse.parse_raw(json_str)
        assert parsed.result == response.result
        assert parsed.status == response.status
        assert parsed.duration == response.duration