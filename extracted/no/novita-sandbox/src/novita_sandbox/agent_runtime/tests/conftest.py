"""
Shared Configuration and Fixtures for Agent Runtime Module Tests

Provides standardized configuration, Mock objects, and utility functions for testing.
"""

import asyncio
import pytest
from datetime import datetime
from typing import Dict, Any, Generator, AsyncGenerator, List
from unittest.mock import Mock, AsyncMock

from novita_sandbox.agent_runtime.runtime import (
    AgentRuntimeApp,
    AgentRuntimeServer,
    RuntimeConfig,
    AgentConfig,
    AgentMetadata,
    AgentSpec,
    RequestContext,
    InvocationResponse,
    PingStatus
)

# Import models from Client module (for client testing)
from novita_sandbox.agent_runtime.client.models import (
    PingResponse
)

from novita_sandbox.agent_runtime.client import (
    AgentRuntimeClient,
    SandboxSession,
    AuthManager,
    TemplateManager,
    AgentTemplate,
    ClientConfig,
    SandboxConfig,
    SessionStatus,
    AuthenticationError,
    TemplateNotFoundError,
    SandboxCreationError,
    SessionNotFoundError,
    InvocationError,
    NetworkError
)


# =============================================================================
# Configuration Fixtures
# =============================================================================

@pytest.fixture
def runtime_config() -> RuntimeConfig:
    """Provide runtime configuration for testing"""
    return RuntimeConfig(
        host="127.0.0.1",
        port=8888,  # Use different port to avoid conflicts
        debug=True,
        timeout=30,
        max_request_size=1024 * 512,  # 512KB
        cors_origins=["*"],
        enable_metrics=True,
        enable_middleware=True
    )


@pytest.fixture
def agent_config() -> AgentConfig:
    """Provide Agent configuration for testing"""
    return AgentConfig(
        apiVersion="v1",
        kind="Agent",
        metadata=AgentMetadata(
            name="test-agent",
            version="1.0.0",
            author="test@example.com",
            description="Test Agent for unit testing",
            created="2024-01-01T00:00:00Z"
        ),
        spec=AgentSpec(
            entrypoint="test_agent.py"
        )
    )


@pytest.fixture
def sample_request() -> dict:
    """Provide sample invocation request"""
    return {
        "prompt": "Test prompt",
        "data": {"key": "value"},
        "sandbox_id": "test-sandbox-123",
        "timeout": 30,
        "stream": False,
        "metadata": {"test": True}
    }


@pytest.fixture
def sample_context() -> RequestContext:
    """Provide sample request context"""
    return RequestContext(
        sandbox_id="test-sandbox-123",
        request_id="test-request-456",
        headers={"Content-Type": "application/json"}
    )


# =============================================================================
# Application and Server Fixtures
# =============================================================================

@pytest.fixture
def mock_app(runtime_config: RuntimeConfig) -> AgentRuntimeApp:
    """Provide Mock AgentRuntimeApp"""
    app = AgentRuntimeApp(config=runtime_config)
    
    # Register a simple test Agent
    @app.entrypoint
    def test_agent(request: dict, context: RequestContext) -> dict:
        return {
            "response": f"Processed: {request.get('prompt', '')}",
            "sandbox_id": context.sandbox_id,
            "request_id": context.request_id
        }
    
    # Register health check
    @app.ping
    def test_ping() -> dict:
        return {"status": "healthy", "service": "test-agent"}
    
    return app


@pytest.fixture
def mock_streaming_app(runtime_config: RuntimeConfig) -> AgentRuntimeApp:
    """Provide Mock AgentRuntimeApp with streaming support"""
    app = AgentRuntimeApp(config=runtime_config)
    
    # Register streaming Agent
    @app.entrypoint
    async def streaming_agent(request: dict, context: RequestContext) -> AsyncGenerator[str, None]:
        prompt = request.get('prompt', '')
        for i in range(3):
            await asyncio.sleep(0.01)  # Simulate processing time
            yield f"Chunk {i}: {prompt}"
    
    return app


@pytest.fixture
def test_server(runtime_config: RuntimeConfig) -> AgentRuntimeServer:
    """Provide test server instance"""
    server = AgentRuntimeServer(runtime_config)
    
    # Set up entrypoint function for testing
    def test_entrypoint(request: dict) -> dict:
        return {"result": "test"}
    
    server.set_entrypoint_handler(test_entrypoint)
    return server


# =============================================================================
# Agent Function Fixtures
# =============================================================================

@pytest.fixture
def sync_agent_function():
    """Synchronous Agent function"""
    def agent(request: dict, context: RequestContext) -> dict:
        return {
            "response": "sync response",
            "request_data": request,
            "context_id": context.request_id
        }
    return agent


@pytest.fixture
def async_agent_function():
    """Asynchronous Agent function"""
    async def agent(request: dict, context: RequestContext) -> dict:
        await asyncio.sleep(0.01)
        return {
            "response": "async response",
            "request_data": request,
            "context_id": context.request_id
        }
    return agent


@pytest.fixture
def sync_generator_agent():
    """Synchronous generator Agent function"""
    def agent(request: dict) -> Generator[str, None, None]:
        for i in range(3):
            yield f"sync chunk {i}"
    return agent


@pytest.fixture
def async_generator_agent():
    """Asynchronous generator Agent function"""
    async def agent(request: dict) -> AsyncGenerator[str, None]:
        for i in range(3):
            await asyncio.sleep(0.01)
            yield f"async chunk {i}"
    return agent


@pytest.fixture
def error_agent_function():
    """Agent function that throws exceptions"""
    def agent(request: dict) -> dict:
        raise ValueError("Test error")
    return agent


# =============================================================================
# Mock HTTP and Network Fixtures
# =============================================================================

@pytest.fixture
def mock_http_client():
    """Mock HTTP client"""
    client = AsyncMock()
    
    # Configure default response
    client.post.return_value.status_code = 200
    client.post.return_value.json.return_value = {
        "result": "mock response",
        "status": "success"
    }
    client.get.return_value.status_code = 200
    client.get.return_value.json.return_value = {
        "status": "healthy"
    }
    
    return client


# =============================================================================
# Test Data Fixtures
# =============================================================================

@pytest.fixture
def large_request_data() -> Dict[str, Any]:
    """Large request data (for integration testing)"""
    return {
        "prompt": "Process this large dataset",
        "data": {
            "items": [{"id": i, "value": f"item_{i}"} for i in range(1000)]
        },
        "metadata": {
            "batch_size": 1000,
            "processing_mode": "bulk"
        }
    }


@pytest.fixture
def concurrent_requests() -> list:
    """Concurrent request data set"""
    return [
        {"prompt": f"Request {i}", "data": {"id": i}}
        for i in range(100)
    ]


# =============================================================================
# Test Utility Functions
# =============================================================================

@pytest.fixture
def assert_response_format():
    """Utility function to validate response format"""
    def _assert_format(response: dict, expected_keys: list = None):
        if expected_keys is None:
            expected_keys = ["result", "status", "duration"]
        
        assert isinstance(response, dict)
        for key in expected_keys:
            assert key in response
        
        if "status" in response:
            assert response["status"] in ["success", "error"]
        
        if "duration" in response:
            assert isinstance(response["duration"], (int, float))
            assert response["duration"] >= 0
    
    return _assert_format


@pytest.fixture
def assert_ping_format():
    """Utility function to validate health check response format"""
    def _assert_format(response: dict):
        assert isinstance(response, dict)
        assert "status" in response
        assert response["status"] in ["Healthy", "HealthyBusy"]
        
        if "timestamp" in response:
            assert isinstance(response["timestamp"], str)
        
        if "message" in response:
            assert isinstance(response["message"], str)
    
    return _assert_format


# =============================================================================
# Pytest Configuration
# =============================================================================

def pytest_configure(config):
    """Pytest configuration"""
    config.addinivalue_line(
        "markers", "unit: Unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "network: Tests requiring network"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests"
    )
    config.addinivalue_line(
        "markers", "compatibility: Compatibility tests"
    )


# =============================================================================
# Asynchronous Test Support
# =============================================================================

# Remove custom event_loop fixture, let pytest-asyncio use default
# @pytest.fixture(scope="session")
# def event_loop():
#     """Provide event loop for entire test session"""
#     policy = asyncio.get_event_loop_policy()
#     loop = policy.new_event_loop()
#     yield loop
#     loop.close()


# =============================================================================
# Test Environment Cleanup
# =============================================================================

@pytest.fixture(autouse=True)
def cleanup_context():
    """Automatically clean up request context"""
    from novita_sandbox.agent_runtime.runtime.context import AgentRuntimeContext
    
    yield
    
    # Clean up context after testing
    AgentRuntimeContext.clear_current_context()


@pytest.fixture
def temp_server_port():
    """Provide temporary server port"""
    import socket
    
    # Find an available port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]
    
    return port


# =============================================================================
# Agent Runtime Client Fixtures
# =============================================================================

@pytest.fixture
def client_config() -> ClientConfig:
    """Provide client configuration for testing"""
    return ClientConfig(
        base_url="sandbox.novita.ai",
        timeout=30,
        max_retries=3,
        retry_delay=1.0,
        max_connections=50,
        max_keepalive_connections=10,
        keepalive_expiry=30.0
    )


@pytest.fixture
def sandbox_config() -> SandboxConfig:
    """Provide Sandbox configuration for testing"""
    return SandboxConfig(
        timeout_seconds=300,
        memory_limit="1Gi",
        cpu_limit="1",
        env_vars={"TEST_MODE": "true"},
        volumes=[],
        ports=[8080]
    )


@pytest.fixture
def test_api_key() -> str:
    """Provide API Key for testing"""
    return "test-api-key-12345678"


@pytest.fixture
def auth_manager(test_api_key: str) -> AuthManager:
    """Provide authentication manager for testing"""
    return AuthManager(api_key=test_api_key)


@pytest.fixture
def sample_template() -> AgentTemplate:
    """Provide sample Agent template"""
    from datetime import datetime
    return AgentTemplate(
        template_id="test-template-123",
        name="test-agent",
        version="1.0.0",
        description="Test Agent Template",
        author="test@example.com",
        tags=["test", "ai", "chat"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        status="active",
        metadata={
            "agent": {
                "apiVersion": "v1",
                "kind": "Agent",
                "metadata": {
                    "name": "test-agent",
                    "version": "1.0.0",
                    "author": "test@example.com",
                    "description": "Test Agent Template",
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
                        "template_id": "test-template-123"
                    }
                },
                "status": {
                    "phase": "deployed",
                    "template_id": "test-template-123",
                    "last_deployed": "2024-01-01T00:00:00Z",
                    "build_id": "build-123"
                }
            }
        },
        size=1024 * 1024,  # 1MB
        build_time=30.5,
        dependencies=["python:3.11", "pydantic"],
        runtime_info={"python_version": "3.11", "packages": ["pydantic"]}
    )


@pytest.fixture
def sample_templates(sample_template: AgentTemplate) -> List[AgentTemplate]:
    """Provide sample template list"""
    from datetime import datetime
    
    templates = [sample_template]
    
    # Add more test templates
    for i in range(2, 5):
        template = AgentTemplate(
            template_id=f"test-template-{i}",
            name=f"test-agent-{i}",
            version=f"{i}.0.0",
            description=f"Test Agent Template {i}",
            author="test@example.com",
            tags=["test", "ai"] if i % 2 == 0 else ["test", "chat"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status="active",
            metadata={},
            size=1024 * 512 * i,
            build_time=15.0 + i,
            dependencies=[],
            runtime_info={}
        )
        templates.append(template)
    
    return templates


@pytest.fixture
def mock_sandbox():
    """Mock Sandbox instance"""
    sandbox = Mock()
    sandbox.id = "sandbox-test-123"
    sandbox.sandbox_id = "sandbox-test-123"
    sandbox.get_host.return_value = "test-sandbox.novita.ai"
    
    # Mock async methods
    sandbox.pause = AsyncMock()
    sandbox.resume = AsyncMock()
    sandbox.close = AsyncMock()
    sandbox.kill = AsyncMock()
    
    return sandbox


@pytest.fixture
def mock_template_manager(sample_templates: List[AgentTemplate], auth_manager: AuthManager):
    """Mock TemplateManager"""
    manager = Mock(spec=TemplateManager)
    manager.auth_manager = auth_manager
    
    # Mock async methods
    manager.list_templates = AsyncMock(return_value=sample_templates)
    manager.get_template = AsyncMock(return_value=sample_templates[0])
    manager.template_exists = AsyncMock(return_value=True)
    manager.close = AsyncMock()
    
    return manager


@pytest.fixture
def mock_sandbox_session(mock_sandbox, sample_template: AgentTemplate):
    """Mock SandboxSession"""
    session = Mock(spec=SandboxSession)
    session.template_id = sample_template.template_id
    session.sandbox = mock_sandbox
    session.sandbox_id = mock_sandbox.id
    session.session_id = mock_sandbox.id
    session.status = SessionStatus.ACTIVE
    session.created_at = datetime.now()
    session.last_activity = datetime.now()
    session.host_url = "https://test-sandbox.novita.ai"
    session.is_active = True
    session.is_paused = False
    session.age_seconds = 0.0
    session.idle_seconds = 0.0
    
    # Mock async methods
    session.invoke = AsyncMock(return_value={"result": "test response"})
    session.ping = AsyncMock(return_value=PingResponse(status="Healthy"))
    session.get_status = AsyncMock(return_value=SessionStatus.ACTIVE)
    session.pause = AsyncMock()
    session.resume = AsyncMock()
    session.refresh = AsyncMock()
    session.close = AsyncMock()
    
    return session


@pytest.fixture
async def mock_agent_client(
    client_config: ClientConfig,
    auth_manager: AuthManager,
    mock_template_manager,
    mock_sandbox_session
):
    """Mock AgentRuntimeClient"""
    client = Mock(spec=AgentRuntimeClient)
    client.config = client_config
    client.auth_manager = auth_manager
    client.template_manager = mock_template_manager
    client._sessions = {mock_sandbox_session.sandbox_id: mock_sandbox_session}
    client._closed = False
    
    # Mock async methods
    client.create_session = AsyncMock(return_value=mock_sandbox_session)
    client.get_session = AsyncMock(return_value=mock_sandbox_session)
    client.list_sessions = AsyncMock(return_value=[mock_sandbox_session])
    client.close_session = AsyncMock()
    client.close_all_sessions = AsyncMock()
    client.list_templates = AsyncMock(return_value=[])
    client.get_template = AsyncMock()
    client.invoke_agent = AsyncMock(return_value=InvocationResponse(
        result="test response",
        status="success",
        duration=0.5
    ))
    client.invoke_agent_stream = AsyncMock()
    client.close = AsyncMock()
    
    return client


# =============================================================================
# HTTP Mock Fixtures for Client Testing
# =============================================================================

@pytest.fixture
def mock_httpx_client():
    """Mock httpx.AsyncClient for HTTP requests"""
    client = AsyncMock()
    
    # Mock successful template query response
    templates_response = Mock()
    templates_response.status_code = 200
    templates_response.json.return_value = {
        "templates": [
            {
                "id": "test-template-123",
                "name": "test-agent",
                "version": "1.0.0",
                "description": "Test Agent",
                "author": "test@example.com",
                "tags": ["test"],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "status": "active",
                "metadata": {},
                "size": 1024,
                "build_time": 30.0
            }
        ]
    }
    
    # Mock successful Agent invocation response
    invoke_response = Mock()
    invoke_response.status_code = 200
    invoke_response.json.return_value = {
        "result": "test response",
        "status": "success",
        "duration": 0.5
    }
    
    # Mock health check response
    ping_response = Mock()
    ping_response.status_code = 200
    ping_response.json.return_value = {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    # Configure default response
    client.get.return_value = templates_response
    client.post.return_value = invoke_response
    client.aclose = AsyncMock()
    
    return client


@pytest.fixture
def mock_streaming_response():
    """Mock streaming response"""
    async def mock_stream():
        chunks = ["chunk 1", "chunk 2", "chunk 3"]
        for chunk in chunks:
            yield chunk
    
    response = Mock()
    response.status_code = 200
    response.aiter_text = mock_stream
    
    return response


# =============================================================================
# Environment and Integration Test Fixtures
# =============================================================================

@pytest.fixture
def real_api_key():
    """Real API Key (read from environment variable)"""
    import os
    return os.getenv("NOVITA_API_KEY")


@pytest.fixture
def real_template_id():
    """Real Template ID (read from environment variable, optional)"""
    import os
    return os.getenv("NOVITA_TEST_TEMPLATE_ID")


@pytest.fixture
async def real_client(real_api_key: str):
    """Real AgentRuntimeClient (for integration testing)"""
    if not real_api_key:
        pytest.skip("NOVITA_API_KEY not set - skipping integration test")
    
    client = AgentRuntimeClient(api_key=real_api_key)
    yield client
    await client.close()


@pytest.fixture
def real_template(real_api_key, real_template_id):
    """Get real test template (synchronous fixture)"""
    if not real_api_key:
        pytest.skip("NOVITA_API_KEY not set - skipping integration test")
    
    import asyncio
    
    async def _get_template():
        try:
            async with AgentRuntimeClient(api_key=real_api_key) as client:
                if real_template_id:
                    # Use specified template ID
                    try:
                        template = await client.get_template(real_template_id)
                        return template
                    except Exception as e:
                        pytest.skip(f"Specified template {real_template_id} unavailable: {e}")
                else:
                    # Use first available template
                    templates = await client.list_templates()
                    if not templates:
                        pytest.skip("No available templates for testing")
                    return templates[0]
        except Exception as e:
            # Skip test if real API call fails
            pytest.skip(f"Unable to connect to real API for integration testing: {e}")
    
    # Run async function and return result
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(_get_template())


# =============================================================================
# Concurrent Test Fixtures
# =============================================================================

@pytest.fixture
def concurrent_requests_data():
    """Concurrent request test data"""
    return [
        {
            "prompt": f"Test request {i}",
            "data": {"id": i, "batch": "concurrent_test"},
            "metadata": {"test_id": i}
        }
        for i in range(50)
    ]


@pytest.fixture
def large_request_data_client():
    """Large request data (for client integration testing)"""
    return {
        "prompt": "Process this large dataset",
        "data": {
            "items": [
                {"id": i, "value": f"item_{i}", "data": "x" * 100}
                for i in range(1000)
            ]
        },
        "metadata": {
            "batch_size": 1000,
            "processing_mode": "bulk",
            "test": True
        },
        "timeout": 300
    }


# =============================================================================
# Test Utilities for Client
# =============================================================================

@pytest.fixture
def assert_client_response_format():
    """Utility function to validate client response format"""
    def _assert_format(response: InvocationResponse):
        assert isinstance(response, InvocationResponse)
        assert hasattr(response, 'result')
        assert hasattr(response, 'status')
        assert hasattr(response, 'duration')
        assert response.status in ["success", "error"]
        assert isinstance(response.duration, (int, float))
        assert response.duration >= 0
    
    return _assert_format


@pytest.fixture
def assert_template_format():
    """Utility function to validate template format"""
    def _assert_format(template: AgentTemplate):
        assert isinstance(template, AgentTemplate)
        assert template.template_id
        assert template.name
        assert template.version
        assert isinstance(template.tags, list)
        assert template.status
        assert isinstance(template.metadata, dict)
    
    return _assert_format


# =============================================================================
# Error Simulation Fixtures
# =============================================================================

@pytest.fixture
def mock_network_error_client():
    """HTTP client that simulates network errors"""
    client = AsyncMock()
    client.get.side_effect = Exception("Network connection failed")
    client.post.side_effect = Exception("Network connection failed")
    return client


@pytest.fixture
def mock_auth_error_client():
    """HTTP client that simulates authentication errors"""
    client = AsyncMock()
    
    error_response = Mock()
    error_response.status_code = 401
    error_response.text = "Unauthorized"
    
    client.get.return_value = error_response
    client.post.return_value = error_response
    
    return client


@pytest.fixture
def mock_template_not_found_client():
    """HTTP client that simulates template not found"""
    client = AsyncMock()
    
    # List query returns empty
    list_response = Mock()
    list_response.status_code = 200
    list_response.json.return_value = {"templates": []}
    
    # Single query returns 404
    get_response = Mock()
    get_response.status_code = 404
    get_response.text = "Template not found"
    
    client.get.side_effect = [list_response, get_response]
    
    return client
