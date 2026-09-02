"""
AgentRuntimeClient unit tests

Tests client main class functionality including AWS Agentcore compatibility
"""

import pytest
import asyncio
import uuid
from unittest.mock import Mock, AsyncMock, patch

from novita_sandbox.agent_runtime.client.client import AgentRuntimeClient
from novita_sandbox.agent_runtime.client.auth import AuthManager
from novita_sandbox.agent_runtime.client.models import (
    ClientConfig,
    SandboxConfig,
    InvocationResponse,
    AgentRuntimeRequest,
    AgentRuntimeResponse,
    StreamingChunk,
    MultimodalContent
)
from novita_sandbox.agent_runtime.client.exceptions import (
    AuthenticationError,
    SandboxCreationError,
    SessionNotFoundError,
    ValidationException,
    ResourceNotFoundException
)

from .mock_sandbox import MockAsyncSandbox
from .test_fixtures import create_sample_template


class TestAgentRuntimeClientInit:
    """AgentRuntimeClient initialization tests"""
    
    @pytest.mark.unit
    def test_client_init_with_api_key(self, test_api_key: str):
        """Test initialization with API Key"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        assert client.auth_manager.api_key == test_api_key
        assert isinstance(client.config, ClientConfig)
        assert client.template_manager is not None
        assert client._sessions == {}
        assert client._closed is False
    
    @pytest.mark.unit
    def test_client_init_simplified(self, test_api_key: str):
        """Test simplified initialization (AWS Agentcore compatible)"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        # AWS compatible client should have simplified config
        assert isinstance(client.config, ClientConfig)
        assert client.config.timeout == 300  # Default timeout
        assert client._runtime_sessions == {}
        assert client._session_mappings == {}
    
    @pytest.mark.unit
    def test_client_init_from_env(self, test_api_key: str):
        """Test initialization from environment variables"""
        with patch.dict('os.environ', {'NOVITA_API_KEY': test_api_key}):
            client = AgentRuntimeClient()
            assert client.auth_manager.api_key == test_api_key
    
    @pytest.mark.unit
    def test_client_init_without_api_key(self):
        """Test initialization fails without API Key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(AuthenticationError):
                AgentRuntimeClient()


class TestAgentRuntimeClientSessionManagement:
    """AgentRuntimeClient session management tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_internal_session_creation(self, test_api_key: str, sample_template):
        """Test internal session creation (used by invoke_agent_runtime)"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        # Mock template_manager
        with patch.object(client.template_manager, 'template_exists', return_value=True):
            with patch.object(client.template_manager, 'get_template', return_value=sample_template):
                with patch.object(client, '_create_sandbox_instance') as mock_create:
                    mock_sandbox = MockAsyncSandbox()
                    mock_create.return_value = mock_sandbox
                    
                    session = await client._create_internal_session(sample_template.template_id, 300)
        
        assert session.template_id == sample_template.template_id
        assert session.sandbox is mock_sandbox
        assert session.sandbox_id in client._sessions
        assert client._sessions[session.sandbox_id] is session
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_internal_session_template_not_found(self, test_api_key: str):
        """Test internal session creation fails when template doesn't exist"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        from novita_sandbox.agent_runtime.client.exceptions import TemplateNotFoundError
        
        with patch.object(client.template_manager, 'template_exists', return_value=False):
            with patch.object(client.template_manager, 'get_template', side_effect=TemplateNotFoundError("Template not found")):
                with pytest.raises(ResourceNotFoundException) as exc_info:
                    await client._create_internal_session("non-existent-template", 300)
        
        assert "not found" in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_internal_session_sandbox_creation_error(self, test_api_key: str, sample_template):
        """Test Sandbox creation failure"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        with patch.object(client.template_manager, 'template_exists', return_value=True):
            with patch.object(client.template_manager, 'get_template', return_value=sample_template):
                with patch.object(client, '_create_sandbox_instance', side_effect=Exception("Creation failed")):
                    with pytest.raises(SandboxCreationError) as exc_info:
                        await client._create_internal_session(sample_template.template_id, 300)
        
        assert "Failed to create sandbox session" in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_get_session_existing(self, mock_sandbox_session):
        """Test getting existing session"""
        client = AgentRuntimeClient(api_key="test-key")
        client._sessions[mock_sandbox_session.sandbox_id] = mock_sandbox_session
        
        session = await client.get_session(mock_sandbox_session.sandbox_id)
        
        assert session is mock_sandbox_session
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_get_session_not_found(self, test_api_key: str):
        """Test getting non-existent session"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        session = await client.get_session("non-existent-session")
        
        assert session is None
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_list_sessions(self, test_api_key: str, mock_sandbox_session):
        """Test listing sessions"""
        client = AgentRuntimeClient(api_key=test_api_key)
        client._sessions[mock_sandbox_session.sandbox_id] = mock_sandbox_session
        
        sessions = await client.list_sessions()
        
        assert len(sessions) == 1
        assert sessions[0] is mock_sandbox_session
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_close_session_success(self, test_api_key: str, mock_sandbox_session):
        """Test successful session closing (AWS compatible)"""
        client = AgentRuntimeClient(api_key=test_api_key)
        runtime_session_id = "runtime-session-123"
        
        # Setup runtime session mapping
        client._runtime_sessions[runtime_session_id] = mock_sandbox_session
        client._session_mappings[runtime_session_id] = mock_sandbox_session.sandbox_id
        client._sessions[mock_sandbox_session.sandbox_id] = mock_sandbox_session
        
        await client.close_session(runtime_session_id)
        
        assert runtime_session_id not in client._runtime_sessions
        assert runtime_session_id not in client._session_mappings
        assert mock_sandbox_session.sandbox_id not in client._sessions
        mock_sandbox_session.close.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_close_session_not_found(self, test_api_key: str):
        """Test closing non-existent session"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        with pytest.raises(SessionNotFoundError) as exc_info:
            await client.close_session("non-existent-session")
        
        assert "not found" in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_close_all_sessions(self, test_api_key: str):
        """Test closing all sessions"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        # Create multiple mock sessions
        sessions = []
        for i in range(3):
            session = Mock()
            session.sandbox_id = f"session-{i}"
            session.close = AsyncMock()
            client._sessions[session.sandbox_id] = session
            sessions.append(session)
        
        await client.close_all_sessions()
        
        assert len(client._sessions) == 0
        for session in sessions:
            session.close.assert_called_once()
    
    @pytest.mark.unit
    def test_extract_agent_id_simple(self, test_api_key: str):
        """Test extracting agent ID from simple format"""
        client = AgentRuntimeClient(api_key=test_api_key)
        agent_id = "customer-service-tpl_abc123"
        result = client._extract_agent_id(agent_id)
        assert result == "customer-service-tpl_abc123"
    
    @pytest.mark.unit
    def test_extract_agent_id_from_arn(self, test_api_key: str):
        """Test extracting agent ID from ARN format"""
        client = AgentRuntimeClient(api_key=test_api_key)
        arn = "arn:aws:bedrock:us-west-2:123456789012:agent/customer-service-tpl_abc123"
        result = client._extract_agent_id(arn)
        assert result == "customer-service-tpl_abc123"
    
    @pytest.mark.unit
    def test_extract_template_id_valid(self, test_api_key: str):
        """Test extracting template ID from agent ID"""
        client = AgentRuntimeClient(api_key=test_api_key)
        agent_id = "customer-service-tpl_abc123"
        result = client._extract_template_id(agent_id)
        assert result == "tpl_abc123"
    
    @pytest.mark.unit
    def test_extract_template_id_invalid(self, test_api_key: str):
        """Test extracting template ID with invalid format (no hyphen separator)"""
        client = AgentRuntimeClient(api_key=test_api_key)
        with pytest.raises(ValidationException):
            client._extract_template_id("invalidformat")
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_runtime_session_id_mapping(self, test_api_key: str):
        """Test runtime session ID to sandbox ID mapping"""
        client = AgentRuntimeClient(api_key=test_api_key)
        template_id = "tpl_123"
        user_runtime_session_id = str(uuid.uuid4())
        
        # Mock the internal session creation
        mock_session = Mock()
        mock_session.sandbox_id = "sandbox_internal_123"
        
        with patch.object(client, '_create_internal_session', return_value=mock_session):
            session, runtime_session_id = await client._get_or_create_session(
                template_id=template_id,
                runtime_session_id=user_runtime_session_id,
                timeout=300
            )
        
        # Verify mapping was created
        assert runtime_session_id == user_runtime_session_id
        assert user_runtime_session_id in client._runtime_sessions
        assert client._session_mappings[user_runtime_session_id] == "sandbox_internal_123"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_runtime_session_reuse(self, test_api_key: str):
        """Test reusing existing runtime session"""
        client = AgentRuntimeClient(api_key=test_api_key)
        template_id = "tpl_789"
        runtime_session_id = str(uuid.uuid4())
        
        mock_session = Mock()
        mock_session.sandbox_id = "sandbox_reuse_789"
        
        with patch.object(client, '_create_internal_session', return_value=mock_session):
            # First call - creates session
            session1, runtime_id1 = await client._get_or_create_session(
                template_id=template_id,
                runtime_session_id=runtime_session_id,
                timeout=300
            )
            
            # Second call - reuses existing session
            session2, runtime_id2 = await client._get_or_create_session(
                template_id=template_id,
                runtime_session_id=runtime_session_id,
                timeout=300
            )
        
        # Verify same session is returned
        assert session1 is session2
        assert runtime_id1 == runtime_id2 == runtime_session_id


class TestAgentRuntimeClientTemplateManagement:
    """AgentRuntimeClient template management tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_list_templates(self, test_api_key: str, sample_templates):
        """Test listing templates"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        with patch.object(client.template_manager, 'list_templates') as mock_list:
            mock_list.return_value = sample_templates
            templates = await client.list_templates()
        
        assert templates is sample_templates
        mock_list.assert_called_once_with(with_metadata=False)
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_list_templates_with_metadata(self, test_api_key: str, sample_templates):
        """Test listing templates with metadata"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        with patch.object(client.template_manager, 'list_templates') as mock_list:
            mock_list.return_value = sample_templates
            await client.list_templates(with_metadata=True)
        
        mock_list.assert_called_once_with(with_metadata=True)
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_get_template(self, test_api_key: str, sample_template):
        """Test getting template"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        with patch.object(client.template_manager, 'get_template') as mock_get:
            mock_get.return_value = sample_template
            template = await client.get_template(sample_template.template_id)
        
        assert template is sample_template
        mock_get.assert_called_once_with(sample_template.template_id)


class TestAgentRuntimeClientConvenienceMethods:
    """AgentRuntimeClient convenience method tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_invoke_agent_runtime_basic(self, test_api_key: str):
        """Test basic invoke_agent_runtime"""
        client = AgentRuntimeClient(api_key=test_api_key)
        agent_id = "customer-service-tpl_abc123"
        payload = b"Hello, agent!"
        
        # Mock session and invocation
        mock_session = AsyncMock()
        mock_session.sandbox_id = "sandbox_123"
        mock_session.invoke.return_value = {"response": "Hello back!"}
        
        with patch.object(client, '_get_or_create_session', 
                         return_value=(mock_session, "runtime_session_123")):
            result = await client.invoke_agent_runtime(
                agentId=agent_id,
                payload=payload
            )
        
        # Verify result structure
        assert result["response"] == {"response": "Hello back!"}
        assert result["runtimeSessionId"] == "runtime_session_123"
        assert result["status"] == "success"
        assert result["agentId"] == agent_id
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_invoke_agent_runtime_with_session_id(self, test_api_key: str):
        """Test invoke_agent_runtime with custom session ID"""
        client = AgentRuntimeClient(api_key=test_api_key)
        agent_id = "test-agent-tpl_def456"
        payload = b"Test payload"
        custom_session_id = str(uuid.uuid4())
        
        # Mock session and invocation
        mock_session = AsyncMock()
        mock_session.sandbox_id = "sandbox_456"
        mock_session.invoke.return_value = {"data": "test response"}
        
        with patch.object(client, '_get_or_create_session', 
                         return_value=(mock_session, custom_session_id)):
            result = await client.invoke_agent_runtime(
                agentId=agent_id,
                payload=payload,
                runtimeSessionId=custom_session_id
            )
        
        # Verify custom session ID is used
        assert result["runtimeSessionId"] == custom_session_id
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_invoke_agent_runtime_auto_detect_streaming(self, test_api_key: str):
        """Test invoke_agent_runtime with auto-detection of streaming response"""
        client = AgentRuntimeClient(api_key=test_api_key)
        agent_id = "streaming-agent-tpl_ghi789"
        payload = b"Stream test"
        
        # Mock streaming response (async generator)
        async def mock_stream():
            yield "chunk1"
            yield "chunk2"
            yield "chunk3"
        
        mock_session = AsyncMock()
        mock_session.sandbox_id = "sandbox_stream_789"
        mock_session.invoke.return_value = mock_stream()
        
        with patch.object(client, '_get_or_create_session', 
                         return_value=(mock_session, "stream_session_789")):
            result = await client.invoke_agent_runtime(
                agentId=agent_id,
                payload=payload
            )
            
            # Result should be an async iterator (streaming)
            import inspect
            assert inspect.isasyncgen(result), "Expected async generator for streaming response"
            
            # Consume the stream
            chunks = []
            async for chunk in result:
                chunks.append(chunk)
        
        # Verify streaming chunks
        assert len(chunks) == 3
        assert chunks[0]["chunk"] == "chunk1"
        assert chunks[0]["runtimeSessionId"] == "stream_session_789"
        assert chunks[0]["agentId"] == agent_id
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_invoke_agent_runtime_invalid_agent_id(self, test_api_key: str):
        """Test invoke_agent_runtime with invalid agent ID (no hyphen separator)"""
        client = AgentRuntimeClient(api_key=test_api_key)
        with pytest.raises(ValidationException):
            await client.invoke_agent_runtime(
                agentId="invalidformat",
                payload=b"test"
            )
    
    @pytest.mark.unit
    def test_agent_runtime_models_camel_case(self):
        """Test agent runtime models with camelCase parameters"""
        # Test AgentRuntimeRequest
        request_data = {
            "agentId": "test-agent-tpl_123",
            "payload": b"test payload",
            "runtimeSessionId": str(uuid.uuid4()),
            "timeout": 300
        }
        request = AgentRuntimeRequest(**request_data)
        assert request.agent_id == "test-agent-tpl_123"
        assert request.runtime_session_id == request_data["runtimeSessionId"]
        
        # Test AgentRuntimeResponse
        response_data = {
            "response": {"result": "success"},
            "runtimeSessionId": "session_123",
            "agentId": "test-agent-tpl_456",
            "status": "success"
        }
        response = AgentRuntimeResponse(**response_data)
        assert response.agent_id == "test-agent-tpl_456"
        assert response.runtime_session_id == "session_123"
        
        # Test StreamingChunk
        chunk_data = {
            "chunk": "partial response",
            "runtimeSessionId": "stream_session_123",
            "agentId": "streaming-agent-tpl_abc",
            "sequenceNumber": 1,
            "isFinal": False
        }
        chunk = StreamingChunk(**chunk_data)
        assert chunk.runtime_session_id == "stream_session_123"
        assert chunk.sequence_number == 1
        assert chunk.is_final is False
        
        # Test MultimodalContent
        content = MultimodalContent(
            contentType="image/png",
            data=b"fake image data",
            filename="test.png",
            metadata={"width": 800}
        )
        assert content.content_type == "image/png"


class TestAgentRuntimeClientContextManager:
    """AgentRuntimeClient context manager tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_async_context_manager(self, test_api_key: str):
        """Test async context manager"""
        async with AgentRuntimeClient(api_key=test_api_key) as client:
            assert not client._closed
            assert isinstance(client, AgentRuntimeClient)
        
        # Should be closed after exit
        assert client._closed
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_close_method(self, test_api_key: str):
        """Test close method"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        # Add some sessions
        mock_session = Mock()
        mock_session.close = AsyncMock()
        client._sessions["test-session"] = mock_session
        
        await client.close()
        
        assert client._closed is True
        assert len(client._sessions) == 0
        mock_session.close.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_close_idempotent(self, test_api_key: str):
        """Test repeated closing"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        await client.close()
        assert client._closed is True
        
        # Closing again should be fine
        await client.close()
        assert client._closed is True


class TestAgentRuntimeClientSandboxCreation:
    """AgentRuntimeClient Sandbox creation tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    
    async def test_create_sandbox_instance_success(self, test_api_key: str, sandbox_config: SandboxConfig):
        """Test successful Sandbox instance creation"""
        client = AgentRuntimeClient(api_key=test_api_key)

        with patch('novita_sandbox.agent_runtime.client.client.AsyncSandbox') as mock_async_sandbox:
            mock_instance = MockAsyncSandbox()
            # Fix: AsyncSandbox.create() is a class method, needs to return AsyncMock
            mock_async_sandbox.create = AsyncMock(return_value=mock_instance)

            sandbox = await client._create_sandbox_instance(
                template_id="test-template",
                timeout_seconds=300,
                config=sandbox_config
            )
        
        assert sandbox is mock_instance
        # Fix: Check create() class method call instead of constructor call
        mock_async_sandbox.create.assert_called_once_with(
            template="test-template",
            timeout=300,
            metadata={"created_by": "agent_runtime_client"},
            envs=sandbox_config.env_vars,
            api_key=test_api_key,
            secure=True,
        )
    
    @pytest.mark.unit
    @pytest.mark.asyncio

    async def test_create_sandbox_instance_error(self, test_api_key: str, sandbox_config: SandboxConfig):
        """Test Sandbox instance creation failure"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        with patch('novita_sandbox.core.AsyncSandbox', side_effect=Exception("Creation failed")):
            with pytest.raises(SandboxCreationError) as exc_info:
                await client._create_sandbox_instance(
                    template_id="test-template",
                    timeout_seconds=300,
                    config=sandbox_config
                )
        
        assert "Failed to create sandbox instance" in str(exc_info.value)


class TestAgentRuntimeClientIntegration:
    """AgentRuntimeClient integration tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_client_lifecycle(self, test_api_key: str, sample_template):
        """Test complete client lifecycle (AWS compatible)"""
        async with AgentRuntimeClient(api_key=test_api_key) as client:
            # 1. Verify initial state
            assert not client._closed
            assert len(client._sessions) == 0
            assert len(client._runtime_sessions) == 0
            
            # 2. Mock template exists
            with patch.object(client.template_manager, 'template_exists', return_value=True):
                with patch.object(client.template_manager, 'get_template', return_value=sample_template):
                    with patch.object(client, '_create_sandbox_instance') as mock_create:
                        mock_sandbox = MockAsyncSandbox()
                        mock_create.return_value = mock_sandbox
                        
                        # 3. Create internal session
                        session = await client._create_internal_session(sample_template.template_id, 300)
                        assert len(client._sessions) == 1
                        
                        # 4. List sessions
                        sessions = await client.list_sessions()
                        assert len(sessions) == 1
                        assert sessions[0] is session
                        
                        # 5. Get session
                        found_session = await client.get_session(session.sandbox_id)
                        assert found_session is session
                        
                        # 6. Close session by sandbox_id (using legacy method)
                        await client.close_session_by_sandbox_id(session.sandbox_id)
                        assert len(client._sessions) == 0
        
        # 7. Client should be closed
        assert client._closed
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_concurrent_session_management(self, test_api_key: str, sample_templates):
        """Test concurrent session management (AWS compatible)"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        try:
            with patch.object(client.template_manager, 'template_exists', return_value=True):
                with patch.object(client.template_manager, 'get_template', side_effect=sample_templates[:3]):
                    with patch.object(client, '_create_sandbox_instance') as mock_create:
                        # Create multiple mock sandboxes
                        mock_sandboxes = [MockAsyncSandbox() for _ in range(3)]
                        mock_create.side_effect = mock_sandboxes
                        
                        # Create sessions concurrently
                        tasks = [
                            client._create_internal_session(template.template_id, 300)
                            for template in sample_templates[:3]
                        ]
                        sessions = await asyncio.gather(*tasks)
                        
                        assert len(sessions) == 3
                        assert len(client._sessions) == 3
                        
                        # Close sessions concurrently by sandbox_id
                        close_tasks = [
                            client.close_session_by_sandbox_id(session.sandbox_id)
                            for session in sessions
                        ]
                        await asyncio.gather(*close_tasks)
                        
                        assert len(client._sessions) == 0
        
        finally:
            await client.close()
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_error_recovery(self, test_api_key: str, sample_template):
        """Test error recovery (AWS compatible)"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        try:
            # First creation fails
            with patch.object(client.template_manager, 'template_exists', return_value=True):
                with patch.object(client.template_manager, 'get_template', return_value=sample_template):
                    with patch.object(client, '_create_sandbox_instance', side_effect=Exception("First failure")):
                        with pytest.raises(SandboxCreationError):
                            await client._create_internal_session(sample_template.template_id, 300)
            
            assert len(client._sessions) == 0
            
            # Second creation succeeds
            with patch.object(client.template_manager, 'template_exists', return_value=True):
                with patch.object(client.template_manager, 'get_template', return_value=sample_template):
                    with patch.object(client, '_create_sandbox_instance') as mock_create:
                        mock_sandbox = MockAsyncSandbox()
                        mock_create.return_value = mock_sandbox
                        
                        session = await client._create_internal_session(sample_template.template_id, 300)
                        assert len(client._sessions) == 1
        
        finally:
            await client.close()
    
    @pytest.mark.unit
    def test_client_representation(self, test_api_key: str):
        """Test client string representation"""
        client = AgentRuntimeClient(api_key=test_api_key)
        
        repr_str = repr(client)
        assert "AgentRuntimeClient" in repr_str
        assert "sessions=0" in repr_str
        assert "runtime_sessions=0" in repr_str
        assert "closed=False" in repr_str
        
        client._closed = True
        repr_str = repr(client)
        assert "closed=True" in repr_str


