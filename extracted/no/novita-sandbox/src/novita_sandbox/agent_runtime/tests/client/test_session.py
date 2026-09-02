"""
SandboxSession unit tests

Tests Sandbox session management functionality
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

from novita_sandbox.agent_runtime.client.session import SandboxSession
from novita_sandbox.agent_runtime.client.models import (
    InvocationRequest,
    SessionStatus,
    PingResponse,
    PingStatus
)
from novita_sandbox.agent_runtime.client.exceptions import (
    InvocationError,
    NetworkError,
    SandboxOperationError,
    SessionNotFoundError
)

from .mock_sandbox import (
    create_healthy_sandbox,
    create_paused_sandbox,
    create_error_sandbox,
    assert_sandbox_state,
    assert_operation_called
)


class TestSandboxSessionInit:
    """SandboxSession initialization tests"""
    
    @pytest.mark.unit
    def test_session_init(self, mock_sandbox, sample_template):
        """Test session initialization"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        assert session.template_id == sample_template.template_id
        assert session.sandbox is mock_sandbox
        assert session._client_ref is mock_client
        assert session.status == SessionStatus.ACTIVE
        assert isinstance(session.created_at, datetime)
        assert isinstance(session.last_activity, datetime)
    
    @pytest.mark.unit
    def test_session_properties(self, mock_sandbox, sample_template):
        """Test session properties"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        assert session.sandbox_id == mock_sandbox.id
        assert session.session_id == mock_sandbox.id  # Backward compatibility
        assert session.host_url.startswith("https://")
        assert session.is_active is True
        assert session.is_paused is False
        assert session.age_seconds >= 0
        assert session.idle_seconds >= 0


class TestSandboxSessionInvoke:
    """SandboxSession invocation tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_invoke_success_dict(self, mock_sandbox, sample_template):
        """Test successful invocation - dict format request"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        # Mock HTTP response
        mock_http_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={"result": "success response"})
        mock_http_client.post.return_value = mock_response
        
        with patch.object(session, '_get_http_client', return_value=mock_http_client):
            result = await session.invoke({"prompt": "test"})
        
        assert result == {"result": "success response"}
        assert mock_http_client.post.called
        
        # Verify last activity time was updated
        assert session.last_activity > session.created_at
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_invoke_success_string(self, mock_sandbox, sample_template):
        """Test successful invocation - string format request"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        mock_http_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={"result": "string response"})
        mock_http_client.post.return_value = mock_response
        
        with patch.object(session, '_get_http_client', return_value=mock_http_client):
            result = await session.invoke("test prompt")
        
        assert result == {"result": "string response"}
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_invoke_session_not_active(self, mock_sandbox, sample_template):
        """Test invocation when session is not active"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        session.status = SessionStatus.CLOSED
        
        with pytest.raises(SessionNotFoundError) as exc_info:
            await session.invoke("test")
        
        assert "is not active" in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_invoke_http_error(self, mock_sandbox, sample_template):
        """Test HTTP error"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        mock_http_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_http_client.post.return_value = mock_response
        
        with patch.object(session, '_get_http_client', return_value=mock_http_client):
            with pytest.raises(InvocationError) as exc_info:
                await session.invoke("test")
        
        assert "status 500" in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_invoke_network_error(self, mock_sandbox, sample_template):
        """Test network error"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        mock_http_client = AsyncMock()
        mock_http_client.post.side_effect = Exception("Connection timeout")
        
        with patch.object(session, '_get_http_client', return_value=mock_http_client):
            with pytest.raises(NetworkError) as exc_info:
                await session.invoke("test")
        
        assert "Network error" in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_invoke_invalid_request_format(self, mock_sandbox, sample_template):
        """Test invalid request format"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        with pytest.raises(InvocationError) as exc_info:
            await session.invoke(123)  # Invalid type
        
        assert "Invalid request format" in str(exc_info.value)


class TestSandboxSessionLifecycle:
    """SandboxSession lifecycle tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_pause_success(self, sample_template):
        """Test successful pause"""
        sandbox = create_healthy_sandbox()
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=sandbox,
            client=mock_client
        )
        
        await session.pause()
        
        assert session.status == SessionStatus.PAUSED
        assert_operation_called(sandbox, "pause", 1)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_resume_success(self, sample_template):
        """Test successful resume"""
        sandbox = create_paused_sandbox()
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=sandbox,
            client=mock_client
        )
        session.status = SessionStatus.PAUSED
        
        await session.resume()
        
        assert session.status == SessionStatus.ACTIVE
        assert_operation_called(sandbox, "resume", 1)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_pause_error(self, sample_template):
        """Test pause error"""
        sandbox = create_error_sandbox()
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=sandbox,
            client=mock_client
        )
        
        with patch.object(sandbox, 'pause', side_effect=Exception("Pause failed")):
            with pytest.raises(SandboxOperationError) as exc_info:
                await session.pause()
        
        assert "Failed to pause sandbox" in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_close_success(self, sample_template):
        """Test successful close"""
        sandbox = create_healthy_sandbox()
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=sandbox,
            client=mock_client
        )
        
        await session.close()
        
        assert session.status == SessionStatus.CLOSED
        assert_operation_called(sandbox, "close", 1)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_close_error(self, sample_template):
        """Test close error"""
        sandbox = create_healthy_sandbox()
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=sandbox,
            client=mock_client
        )
        
        with patch.object(sandbox, 'close', side_effect=Exception("Close failed")):
            with pytest.raises(SandboxOperationError) as exc_info:
                await session.close()
        
        assert "Failed to close session" in str(exc_info.value)
        assert session.status == SessionStatus.ERROR


class TestSandboxSessionPing:
    """SandboxSession health check tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_ping_success(self, mock_sandbox, sample_template):
        """Test successful health check"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        mock_http_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            "status": "healthy",
            "message": "Service running",
            "timestamp": "2024-01-01T00:00:00Z"
        })
        mock_http_client.get.return_value = mock_response
        
        with patch.object(session, '_get_http_client', return_value=mock_http_client):
            ping_response = await session.ping()
        
        assert isinstance(ping_response, PingResponse)
        assert ping_response.status == PingStatus.HEALTHY  # Use enum object comparison
        assert ping_response.message == "Service running"
        assert ping_response.timestamp == "2024-01-01T00:00:00Z"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_ping_unhealthy(self, mock_sandbox, sample_template):
        """Test unhealthy status"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        mock_http_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Error"
        mock_http_client.get.return_value = mock_response
        
        with patch.object(session, '_get_http_client', return_value=mock_http_client):
            ping_response = await session.ping()
        
        assert ping_response.status == PingStatus.HEALTHY_BUSY  # HTTP 500 error returns HEALTHY_BUSY status
        assert "HTTP 500" in ping_response.message
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_ping_network_error(self, mock_sandbox, sample_template):
        """Test ping network error"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        mock_http_client = AsyncMock()
        mock_http_client.get.side_effect = Exception("Connection failed")
        
        with patch.object(session, '_get_http_client', return_value=mock_http_client):
            with pytest.raises(NetworkError) as exc_info:
                await session.ping()
        
        assert "Network error during ping" in str(exc_info.value)


class TestSandboxSessionStatus:
    """SandboxSession state management tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_get_status_active(self, mock_sandbox, sample_template):
        """Test getting active status"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        # Mock ping returns healthy status
        with patch.object(session, 'ping', return_value=PingResponse(status="Healthy")):
            status = await session.get_status()
        
        assert status == SessionStatus.ACTIVE
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_get_status_paused(self, mock_sandbox, sample_template):
        """Test getting paused status"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        session.status = SessionStatus.PAUSED
        
        # Mock ping returns healthy status, but session is in paused state
        with patch.object(session, 'ping', return_value=PingResponse(status="Healthy")):
            status = await session.get_status()
        
        assert status == SessionStatus.PAUSED
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_get_status_error(self, mock_sandbox, sample_template):
        """Test getting error status"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        # Mock ping throws exception
        with patch.object(session, 'ping', side_effect=Exception("Ping failed")):
            status = await session.get_status()
        
        assert status == SessionStatus.ERROR
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_refresh(self, mock_sandbox, sample_template):
        """Test refreshing session"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        old_activity = session.last_activity
        await asyncio.sleep(0.01)  # Ensure time difference
        
        await session.refresh()
        
        assert session.last_activity > old_activity


class TestSandboxSessionProperties:
    """SandboxSession properties tests"""
    
    @pytest.mark.unit
    def test_host_url_with_get_host(self, sample_template):
        """Test host_url with get_host method"""
        sandbox = Mock()
        sandbox.id = "test-sandbox-123"
        sandbox.get_host.return_value = "test-host.example.com"
        
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=sandbox,
            client=mock_client
        )
        
        assert session.host_url == "https://test-host.example.com"
        sandbox.get_host.assert_called_with(8080)
    
    @pytest.mark.unit
    def test_host_url_without_get_host(self, sample_template):
        """Test host_url without get_host method"""
        sandbox = Mock()
        sandbox.id = "test-sandbox-123"
        del sandbox.get_host  # Remove get_host method
        
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=sandbox,
            client=mock_client
        )
        
        assert session.host_url.startswith("https://session-")
        assert "test-sandbox-123" in session.host_url
    
    @pytest.mark.unit
    def test_sandbox_id_variants(self, sample_template):
        """Test different ways of getting sandbox_id"""
        # Has id attribute
        sandbox1 = Mock()
        sandbox1.id = "sandbox-with-id"
        
        session1 = SandboxSession(sample_template.template_id, sandbox1, Mock())
        assert session1.sandbox_id == "sandbox-with-id"
        
        # Has sandbox_id attribute
        sandbox2 = Mock()
        del sandbox2.id
        sandbox2.sandbox_id = "sandbox-with-sandbox-id"
        
        session2 = SandboxSession(sample_template.template_id, sandbox2, Mock())
        assert session2.sandbox_id == "sandbox-with-sandbox-id"
        
        # Has neither, use fallback
        sandbox3 = Mock(spec=[])  # Empty spec ensures no predefined attributes
        
        session3 = SandboxSession(sample_template.template_id, sandbox3, Mock())
        assert session3.sandbox_id.startswith("sandbox-")
    
    @pytest.mark.unit
    def test_time_properties(self, mock_sandbox, sample_template):
        """Test time-related properties"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        # When just created
        assert session.age_seconds >= 0
        assert session.age_seconds < 1
        assert session.idle_seconds >= 0
        assert session.idle_seconds < 1
        
        # Update activity time
        import time
        time.sleep(0.01)
        session.last_activity = datetime.now()
        
        assert session.age_seconds > 0
        assert session.idle_seconds >= 0


class TestSandboxSessionIntegration:
    """SandboxSession integration tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_session_lifecycle_complete(self, sample_template):
        """Test complete session lifecycle"""
        sandbox = create_healthy_sandbox()
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=sandbox,
            client=mock_client
        )
        
        # 1. Initial state
        assert session.status == SessionStatus.ACTIVE
        assert session.is_active
        
        # 2. Execute invocation
        mock_http_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={"result": "success"})
        mock_http_client.post.return_value = mock_response
        
        with patch.object(session, '_get_http_client', return_value=mock_http_client):
            result = await session.invoke("test")
            assert result["result"] == "success"
        
        # 3. Pause
        await session.pause()
        assert session.status == SessionStatus.PAUSED
        assert session.is_paused
        
        # 4. Resume
        await session.resume()
        assert session.status == SessionStatus.ACTIVE
        assert session.is_active
        
        # 5. Close
        await session.close()
        assert session.status == SessionStatus.CLOSED
        assert not session.is_active
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    @pytest.mark.asyncio

    async def test_concurrent_operations(self, mock_sandbox, sample_template):
        """Test concurrent operations"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        # Mock HTTP client
        mock_http_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={"result": "concurrent"})
        mock_http_client.post.return_value = mock_response
        mock_http_client.get.return_value = mock_response
        
        with patch.object(session, '_get_http_client', return_value=mock_http_client):
            # Execute multiple operations concurrently
            tasks = [
                session.invoke(f"request-{i}")
                for i in range(5)
            ]
            tasks.append(session.ping())
            tasks.append(session.refresh())
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Verify results
            assert len(results) == 7
            for i in range(5):
                assert results[i]["result"] == "concurrent"
    
    @pytest.mark.unit
    def test_session_representation(self, mock_sandbox, sample_template):
        """Test session string representation"""
        mock_client = Mock()
        session = SandboxSession(
            template_id=sample_template.template_id,
            sandbox=mock_sandbox,
            client=mock_client
        )
        
        repr_str = repr(session)
        assert "SandboxSession" in repr_str
        assert session.sandbox_id in repr_str
        assert str(session.status) in repr_str  # SessionStatus.ACTIVE instead of 'active'
        assert session.template_id in repr_str
