"""
Real Environment End-to-End Tests

These tests use the real Novita API for testing and require the following environment variables to be set:
- NOVITA_API_KEY: Real API Key
- NOVITA_TEST_TEMPLATE_ID: (Optional) Specified test template ID
"""

import pytest
import asyncio
from novita_sandbox.agent_runtime.client import AgentRuntimeClient
from novita_sandbox.agent_runtime.client.models import SessionStatus
from novita_sandbox.agent_runtime.client.exceptions import InvocationError


class TestRealEnvironmentE2E:
    """Real environment end-to-end tests"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    @pytest.mark.network  # Mark tests requiring network
    async def test_real_template_listing(self, real_api_key):
        """Test template listing in real environment"""
        if not real_api_key:
            pytest.skip("Real API Key required for integration testing")
        
        # Use China region API endpoint
        from novita_sandbox.agent_runtime.client.models import ClientConfig
        config = ClientConfig()
        
        async with AgentRuntimeClient(api_key=real_api_key, config=config) as client:
            templates = await client.list_templates()
            
            # Verify returned templates
            assert len(templates) > 0, "Should have at least one available template"
            
            for template in templates:
                assert hasattr(template, 'template_id'), "Template should have template_id"
                assert hasattr(template, 'name'), "Template should have name"
                assert template.template_id, "template_id should not be empty"
                print(f"Available template: {template.name} ({template.template_id})")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    @pytest.mark.network
    async def test_real_session_creation_and_invocation(self, real_api_key, real_template):
        """Test session creation and invocation in real environment"""
        if not real_api_key:
            pytest.skip("Real API Key required for integration testing")
        
        print(f"Using template: {real_template.name} ({real_template.template_id})")
        
        # Use China region API endpoint
        from novita_sandbox.agent_runtime.client.models import ClientConfig
        config = ClientConfig()
        
        async with AgentRuntimeClient(api_key=real_api_key, config=config) as client:
            # 1. Create session
            session = await client.create_session(real_template.template_id, timeout_seconds=20)
            assert session is not None, "Session creation should succeed"
            assert session.status == SessionStatus.ACTIVE, "Session should be in active state"
            print(f"Session created successfully: {session.sandbox_id}")
            
            try:
                # 2. Execute simple invocation
                response = await session.invoke("Hello, this is a test message from automated testing")
                assert response is not None, "Invocation should return response"
                print(f"Invocation response: {response}")
                
                # 3. Test health check
                ping_response = await session.ping()
                assert ping_response is not None, "Health check should succeed"
                print(f"Health check status: {ping_response.status}")
                
            finally:
                # 4. Clean up session
                await client.close_session(session.sandbox_id)
                print("Session closed")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    @pytest.mark.network
    async def test_real_convenience_method(self, real_api_key, real_template):
        """Test convenience method in real environment"""
        if not real_api_key:
            pytest.skip("Real API Key required for integration testing")
        
        print(f"Using template: {real_template.name} ({real_template.template_id})")
        
        # Use China region API endpoint
        from novita_sandbox.agent_runtime.client.models import ClientConfig
        config = ClientConfig()
        
        async with AgentRuntimeClient(api_key=real_api_key, config=config) as client:
            # Use convenience method for direct invocation
            response = await client.invoke_agent(
                template_id=real_template.template_id,
                request="Test convenience method call"
            )
            
            assert response is not None, "Convenience method invocation should succeed"
            print(f"Convenience method response: {response}")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    @pytest.mark.network 
    @pytest.mark.slow  # Mark as slow test
    async def test_real_streaming_invocation(self, real_api_key, real_template):
        """Test streaming invocation in real environment"""
        if not real_api_key:
            pytest.skip("Real API Key required for integration testing")
        
        print(f"Using template: {real_template.name} ({real_template.template_id})")
        
        # Use China region API endpoint
        from novita_sandbox.agent_runtime.client.models import ClientConfig
        config = ClientConfig()
        
        async with AgentRuntimeClient(api_key=real_api_key, config=config) as client:
            # Create session
            session = await client.create_session(real_template.template_id, timeout_seconds=20)
            
            try:
                # Invoke with auto-detection (Agent may return streaming or non-streaming)
                result = await session.invoke("Please generate a short poem about testing")
                
                # Check if streaming response
                import inspect
                if inspect.isasyncgen(result):
                    # Streaming response
                    chunks = []
                    async for chunk in result:
                        chunks.append(chunk)
                        print(f"Received streaming data: {chunk}")
                        
                        # Limit test duration to avoid excessive runtime
                        if len(chunks) >= 10:
                            break
                    
                    assert len(chunks) > 0, "Should receive at least one data chunk"
                else:
                    # Non-streaming response
                    print(f"Received non-streaming response: {result}")
                    assert result is not None, "Should receive valid response"
                
            finally:
                await client.close_session(session.sandbox_id)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    @pytest.mark.network
    async def test_real_multiple_sessions(self, real_api_key, real_template):
        """Test multiple session management in real environment"""
        if not real_api_key:
            pytest.skip("Real API Key required for integration testing")
        
        print(f"Using template: {real_template.name} ({real_template.template_id})")
        
        # Use China region API endpoint
        from novita_sandbox.agent_runtime.client.models import ClientConfig
        config = ClientConfig()
        
        async with AgentRuntimeClient(api_key=real_api_key, config=config) as client:
            sessions = []
            try:
                # Create multiple sessions
                for i in range(3):  # Limit quantity to avoid quota consumption
                    session = await client.create_session(real_template.template_id, timeout_seconds=20)
                    sessions.append(session)
                    print(f"Created session {i+1}: {session.sandbox_id}")
                
                # Verify all sessions are active
                for session in sessions:
                    assert session.status == SessionStatus.ACTIVE
                    
                    # Simple test for each session
                    response = await session.invoke(f"Test message for session {session.sandbox_id}")
                    assert response is not None
                    print(f"Session {session.sandbox_id} responded normally")
            
            finally:
                # Clean up all sessions
                for session in sessions:
                    try:
                        await client.close_session(session.sandbox_id)
                        print(f"Closed session: {session.sandbox_id}")
                    except Exception as e:
                        print(f"Failed to close session: {e}")


class TestRealEnvironmentErrorHandling:
    """Real environment error handling tests"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    @pytest.mark.network
    async def test_invalid_template_id(self, real_api_key):
        """Test handling of invalid template ID"""
        if not real_api_key:
            pytest.skip("Real API Key required for integration testing")
        
        # Use China region API endpoint
        from novita_sandbox.agent_runtime.client.models import ClientConfig
        config = ClientConfig()
        
        async with AgentRuntimeClient(api_key=real_api_key, config=config) as client:
            with pytest.raises(Exception):  # Should adjust exception type based on actual API
                await client.create_session("invalid-template-id-12345")
    
    @pytest.mark.integration  
    @pytest.mark.asyncio
    @pytest.mark.network
    async def test_invalid_api_key(self):
        """Test handling of invalid API Key"""
        async with AgentRuntimeClient(api_key="invalid-key-12345") as client:
            with pytest.raises(Exception):  # Should adjust exception type based on actual API
                await client.list_templates()
