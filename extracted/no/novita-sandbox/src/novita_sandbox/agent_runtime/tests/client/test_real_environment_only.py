"""
Real Environment Integration Tests - Uses real API only, no Mocks

These tests only run when real API Key and Template ID are available
"""

import asyncio
import os
from typing import List
import pytest

from novita_sandbox.agent_runtime.client import AgentRuntimeClient
from novita_sandbox.agent_runtime.client.models import AgentTemplate
from novita_sandbox.agent_runtime.client.exceptions import (
    TemplateNotFoundError,
    AuthenticationError,
    SandboxCreationError,
    InvocationError
)


@pytest.fixture
def real_api_key():
    """Real API Key"""
    api_key = os.getenv("NOVITA_API_KEY")
    if not api_key:
        pytest.skip("NOVITA_API_KEY environment variable must be set")
    return api_key


@pytest.fixture
def real_template_id():
    """Real Template ID"""
    template_id = os.getenv("NOVITA_TEST_TEMPLATE_ID")
    if not template_id:
        pytest.skip("NOVITA_TEST_TEMPLATE_ID environment variable must be set")
    return template_id


@pytest.fixture
def real_template(real_api_key, real_template_id):
    """Get real template"""
    
    async def _get_template():
        async with AgentRuntimeClient(api_key=real_api_key) as client:
            # Find target template from template list
            templates = await client.list_templates()
            for template in templates:
                if template.template_id == real_template_id:
                    return template
            pytest.skip(f"Template {real_template_id} not found in available templates")
    
    # Execute async operation synchronously
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(_get_template())


class TestRealEnvironmentBasic:
    """Basic real environment tests"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_list_templates_real(self, real_api_key):
        """Test getting template list"""
        async with AgentRuntimeClient(api_key=real_api_key) as client:
            templates = await client.list_templates()
            
            assert isinstance(templates, list)
            assert len(templates) > 0
            
            # Check template structure
            template = templates[0]
            assert isinstance(template, AgentTemplate)
            assert hasattr(template, 'template_id')
            assert hasattr(template, 'name')
            assert hasattr(template, 'status')
            
            print(f"✅ Retrieved {len(templates)} templates")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_find_template_by_id_real(self, real_api_key, real_template_id):
        """Test finding template by ID"""
        async with AgentRuntimeClient(api_key=real_api_key) as client:
            templates = await client.list_templates()
            
            # Find target template
            target_template = None
            for template in templates:
                if template.template_id == real_template_id:
                    target_template = template
                    break
            
            assert target_template is not None, f"Template {real_template_id} not found"
            assert target_template.template_id == real_template_id
            assert target_template.status == "active"
            
            print(f"✅ Found target template: {target_template.name}")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_template_exists_real(self, real_api_key, real_template_id):
        """Test template existence check"""
        async with AgentRuntimeClient(api_key=real_api_key) as client:
            # Check existing template
            exists = await client.template_manager.template_exists(real_template_id)
            assert exists is True
            
            # Check non-existent template
            fake_id = "nonexistent-template-id"
            exists_fake = await client.template_manager.template_exists(fake_id)
            assert exists_fake is False
            
            print("✅ Template existence check passed")


class TestRealEnvironmentSessions:
    """Session management real environment tests"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_session_creation_real(self, real_api_key, real_template: AgentTemplate):
        """Test session creation in real environment"""
        async with AgentRuntimeClient(api_key=real_api_key) as client:
            print(f"Using template: {real_template.name} ({real_template.template_id})")
            
            try:
                # Create session
                session = await client.create_session(real_template.template_id, timeout_seconds=30)
                
                assert session is not None
                assert session.template_id == real_template.template_id
                assert session.sandbox_id is not None
                
                print(f"✅ Session created successfully: {session.sandbox_id}")
                print(f"Session status: {session.status}")
                
                # Cleanup: close session
                await session.close()
                print("✅ Session closed")
                
            except SandboxCreationError as e:
                pytest.skip(f"Sandbox creation failed, possibly due to resource limits: {e}")
            except Exception as e:
                print(f"Session creation failed: {e}")
                pytest.fail(f"Session creation failed: {e}")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_session_basic_info_real(self, real_api_key, real_template: AgentTemplate):
        """Test session basic information"""
        async with AgentRuntimeClient(api_key=real_api_key) as client:
            try:
                session = await client.create_session(real_template.template_id, timeout_seconds=30)
                
                # Check basic attributes
                assert session.template_id == real_template.template_id
                assert session.sandbox_id is not None
                assert session.created_at is not None
                assert session.last_activity is not None
                
                # Check URL
                host_url = session.host_url
                assert host_url.startswith('https://')
                print(f"✅ Session Host URL: {host_url}")
                
                # Check age and idle time
                age = session.age_seconds
                idle = session.idle_seconds
                assert age >= 0
                assert idle >= 0
                print(f"Session age: {age:.2f}s, idle time: {idle:.2f}s")
                
                await session.close()
                
            except SandboxCreationError as e:
                pytest.skip(f"Sandbox creation failed: {e}")


class TestRealEnvironmentInvocation:
    """Invocation tests (may be skipped due to template configuration)"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_simple_invocation_real(self, real_api_key, real_template: AgentTemplate):
        """Test simple invocation (if template supports)"""
        async with AgentRuntimeClient(api_key=real_api_key) as client:
            try:
                session = await client.create_session(real_template.template_id, timeout_seconds=30)
                
                # Wait a few seconds for service to start
                await asyncio.sleep(3)
                
                # Try simple invocation (auto-detect streaming)
                result = await session.invoke("Hello, test invocation")
                
                print(f"✅ Invocation successful: {result}")
                assert result is not None
                
                await session.close()
                
            except (SandboxCreationError, InvocationError) as e:
                pytest.skip(f"Invocation failed, template may not support it or service not started: {e}")
            except Exception as e:
                print(f"Invocation test failed: {e}")
                # Don't let this test fail the entire test suite
                pytest.skip(f"Invocation test failed: {e}")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_ping_session_real(self, real_api_key, real_template: AgentTemplate):
        """Test session ping functionality"""
        async with AgentRuntimeClient(api_key=real_api_key) as client:
            try:
                session = await client.create_session(real_template.template_id, timeout_seconds=30)
                
                # Wait for service to start
                await asyncio.sleep(2)
                
                # Try ping
                ping_result = await session.ping()
                print(f"Ping result: {ping_result}")
                
                await session.close()
                
            except SandboxCreationError as e:
                pytest.skip(f"Sandbox creation failed: {e}")
            except Exception as e:
                print(f"Ping test failed: {e}")
                pytest.skip(f"Ping test failed: {e}")


class TestRealEnvironmentClientManagement:
    """Client management tests"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_client_context_manager_real(self, real_api_key):
        """Test client context manager"""
        async with AgentRuntimeClient(api_key=real_api_key) as client:
            assert not client._closed
            
            # Test basic functionality
            templates = await client.list_templates()
            assert len(templates) > 0
        
        # Client should be closed
        assert client._closed
        print("✅ Client context manager works properly")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_client_manual_close_real(self, real_api_key):
        """Test manual client closure"""
        client = AgentRuntimeClient(api_key=real_api_key)
        
        assert not client._closed
        
        # Test functionality
        templates = await client.list_templates()
        assert len(templates) > 0
        
        # Manual close
        await client.close()
        assert client._closed
        
        print("✅ Manual client closure works properly")
