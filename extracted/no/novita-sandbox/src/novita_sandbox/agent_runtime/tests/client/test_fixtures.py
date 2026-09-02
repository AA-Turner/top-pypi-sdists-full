"""
Test data and fixtures

Provides fixture data and utility functions for testing
"""

from datetime import datetime
from typing import Dict, Any, List
from novita_sandbox.agent_runtime.client.models import (
    AgentTemplate,
    InvocationResponse,
    SandboxConfig,
    ClientConfig,
    SessionStatus
)


# =============================================================================
# Template test data
# =============================================================================

def create_sample_template(
    template_id: str = "test-template-123",
    name: str = "test-agent",
    version: str = "1.0.0"
) -> AgentTemplate:
    """Create sample template"""
    return AgentTemplate(
        template_id=template_id,
        name=name,
        version=version,
        description=f"Test Agent Template - {name}",
        author="test@example.com",
        tags=["test", "ai", "chat"],
        created_at=datetime(2024, 1, 1, 0, 0, 0),
        updated_at=datetime(2024, 1, 1, 0, 0, 0),
        status="active",
        metadata={
            "agent": {
                "apiVersion": "v1",
                "kind": "Agent",
                "metadata": {
                    "name": name,
                    "version": version,
                    "author": "test@example.com",
                    "description": f"Test Agent - {name}",
                    "created": "2024-01-01T00:00:00Z"
                },
                "spec": {
                    "entrypoint": "agent.py",
                    "runtime": {
                        "timeout": 60,
                        "memory_limit": "1Gi",
                        "cpu_limit": "1"
                    },
                    "sandbox": {
                        "template_id": template_id
                    }
                },
                "status": {
                    "phase": "deployed",
                    "template_id": template_id,
                    "last_deployed": "2024-01-01T00:00:00Z",
                    "build_id": f"build-{template_id}"
                }
            }
        },
        size=1024 * 1024,  # 1MB
        build_time=30.5,
        dependencies=["python:3.11", "pydantic"],
        runtime_info={"python_version": "3.11", "packages": ["pydantic"]}
    )


def create_template_list(count: int = 5) -> List[AgentTemplate]:
    """Create template list"""
    templates = []
    for i in range(1, count + 1):
        template = create_sample_template(
            template_id=f"test-template-{i}",
            name=f"test-agent-{i}",
            version=f"{i}.0.0"
        )
        # Modify some attributes for more variety in data
        template.tags = ["test", "ai"] if i % 2 == 0 else ["test", "chat"]
        template.size = 1024 * 512 * i
        template.build_time = 15.0 + i * 5
        templates.append(template)
    
    return templates


# =============================================================================
# Request/Response test data
# =============================================================================

def create_sample_request(
    prompt: str = "Test prompt",
    sandbox_id: str = "test-sandbox-123",
    stream: bool = False
) -> dict:
    """Create sample request"""
    return {
        "prompt": prompt,
        "data": {"key": "value", "test": True},
        "sandbox_id": sandbox_id,
        "timeout": 30,
        "stream": stream,
        "metadata": {"test": True, "timestamp": datetime.now().isoformat()}
    }


def create_sample_response(
    result: Any = "test response",
    status: str = "success",
    duration: float = 0.5
) -> InvocationResponse:
    """Create sample response"""
    return InvocationResponse(
        result=result,
        status=status,
        duration=duration,
        metadata={"test": True},
        processing_time=duration * 0.8,
        queue_time=duration * 0.2
    )


def create_error_response(
    error: str = "Test error",
    error_type: str = "TestError"
) -> InvocationResponse:
    """Create error response"""
    return InvocationResponse(
        result=None,
        status="error",
        duration=0.1,
        error=error,
        error_type=error_type,
        metadata={"test": True, "error_occurred": True}
    )


# =============================================================================
# Configuration test data
# =============================================================================

def create_test_client_config() -> ClientConfig:
    """Create test client configuration"""
    return ClientConfig(
        base_url="https://api.test.novita.ai",
        timeout=30,
        max_retries=3,
        retry_delay=1.0,
        max_connections=50,
        max_keepalive_connections=10,
        keepalive_expiry=30.0
    )


def create_test_sandbox_config() -> SandboxConfig:
    """Create test Sandbox configuration"""
    return SandboxConfig(
        timeout_seconds=300,
        memory_limit="1Gi",
        cpu_limit="1",
        env_vars={"TEST_MODE": "true", "DEBUG": "false"},
        volumes=[],
        ports=[8080]
    )


# =============================================================================
# HTTP response test data
# =============================================================================

def create_mock_template_list_response() -> Dict[str, Any]:
    """Create template list API response"""
    templates = create_template_list(3)
    return {
        "templates": [
            {
                "id": t.template_id,
                "name": t.name,
                "version": t.version,
                "description": t.description,
                "author": t.author,
                "tags": t.tags,
                "created_at": t.created_at.isoformat(),
                "updated_at": t.updated_at.isoformat(),
                "status": t.status,
                "metadata": t.metadata,
                "size": t.size,
                "build_time": t.build_time,
                "dependencies": t.dependencies,
                "runtime_info": t.runtime_info
            }
            for t in templates
        ]
    }


def create_mock_template_response(template_id: str = "test-template-123") -> Dict[str, Any]:
    """Create single template API response"""
    template = create_sample_template(template_id=template_id)
    return {
        "id": template.template_id,
        "name": template.name,
        "version": template.version,
        "description": template.description,
        "author": template.author,
        "tags": template.tags,
        "created_at": template.created_at.isoformat(),
        "updated_at": template.updated_at.isoformat(),
        "status": template.status,
        "metadata": template.metadata,
        "size": template.size,
        "build_time": template.build_time,
        "dependencies": template.dependencies,
        "runtime_info": template.runtime_info
    }


def create_mock_agent_response(result: str = "test response") -> Dict[str, Any]:
    """Create Agent invocation API response"""
    return {
        "result": result,
        "status": "success",
        "duration": 0.5,
        "metadata": {"test": True}
    }


def create_mock_ping_response() -> Dict[str, Any]:
    """Create health check API response"""
    return {
        "status": "healthy",
        "message": "Service is running",
        "timestamp": datetime.now().isoformat()
    }


# =============================================================================
# Error scenario data
# =============================================================================

def create_auth_error_response() -> Dict[str, Any]:
    """Create authentication error response"""
    return {
        "error": "Authentication failed",
        "error_code": "INVALID_API_KEY",
        "message": "The provided API key is invalid or expired"
    }


def create_template_not_found_response() -> Dict[str, Any]:
    """Create template not found error response"""
    return {
        "error": "Template not found",
        "error_code": "TEMPLATE_NOT_FOUND",
        "message": "The specified template does not exist"
    }


def create_network_error_response() -> Dict[str, Any]:
    """Create network error response"""
    return {
        "error": "Network error",
        "error_code": "NETWORK_ERROR",
        "message": "Failed to connect to the service"
    }


# =============================================================================
# Concurrent test data
# =============================================================================

def create_concurrent_requests(count: int = 50) -> List[dict]:
    """Create concurrent request data"""
    return [
        {
            "prompt": f"Concurrent request {i}",
            "data": {"id": i, "batch": "concurrent_test"},
            "metadata": {"test_id": i, "batch_size": count}
        }
        for i in range(count)
    ]


def create_large_request() -> dict:
    """Create large request data"""
    return {
        "prompt": "Process this large dataset",
        "data": {
            "items": [
                {
                    "id": i,
                    "value": f"item_{i}",
                    "data": "x" * 100,  # 100 characters per item
                    "metadata": {"index": i, "group": i // 100}
                }
                for i in range(1000)
            ],
            "processing_options": {
                "batch_size": 100,
                "parallel": True,
                "timeout": 300
            }
        },
        "metadata": {
            "batch_size": 1000,
            "processing_mode": "bulk",
            "test": True,
            "estimated_size": "~100KB"
        },
        "timeout": 300
    }


# =============================================================================
# Streaming response test data
# =============================================================================

def create_streaming_chunks() -> List[str]:
    """Create streaming response data chunks"""
    return [
        "Starting processing...",
        "Loading data...",
        "Processing item 1/10...",
        "Processing item 5/10...",
        "Processing item 10/10...",
        "Generating results...",
        "Finalizing...",
        "Complete!"
    ]


# =============================================================================
# Test utility functions
# =============================================================================

def assert_template_equality(template1: AgentTemplate, template2: AgentTemplate) -> None:
    """Assert two templates are equal"""
    assert template1.template_id == template2.template_id
    assert template1.name == template2.name
    assert template1.version == template2.version
    assert template1.author == template2.author
    assert template1.status == template2.status


def assert_request_equality(request1: InvocationRequest, request2: InvocationRequest) -> None:
    """Assert two requests are equal"""
    assert request1.prompt == request2.prompt
    assert request1.sandbox_id == request2.sandbox_id
    assert request1.stream == request2.stream
    assert request1.timeout == request2.timeout


def validate_template_format(template: AgentTemplate) -> None:
    """Validate template format"""
    assert template.template_id
    assert template.name
    assert template.version
    assert isinstance(template.tags, list)
    assert template.status in ["active", "inactive", "deprecated"]
    assert isinstance(template.metadata, dict)
    assert isinstance(template.size, (int, type(None)))
    assert isinstance(template.build_time, (float, type(None)))


def validate_response_format(response: InvocationResponse) -> None:
    """Validate response format"""
    assert hasattr(response, 'result')
    assert hasattr(response, 'status')
    assert hasattr(response, 'duration')
    assert response.status in ["success", "error"]
    assert isinstance(response.duration, (int, float))
    assert response.duration >= 0
