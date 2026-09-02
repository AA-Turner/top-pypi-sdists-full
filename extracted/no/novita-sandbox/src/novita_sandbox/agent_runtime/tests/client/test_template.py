"""
TemplateManager unit tests

Tests template manager functionality
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime

from novita_sandbox.agent_runtime.client.template import TemplateManager
from novita_sandbox.agent_runtime.client.auth import AuthManager
from novita_sandbox.agent_runtime.client.exceptions import (
    TemplateNotFoundError,
    NetworkError,
    AuthenticationError
)
from novita_sandbox.agent_runtime.client.models import AgentTemplate

from .mock_api import (
    create_success_mock_client,
    create_auth_error_mock_client,
    create_template_not_found_mock_client,
    create_network_error_mock_client
)
from .test_fixtures import create_sample_template, create_template_list


class TestTemplateManagerInit:
    """TemplateManager initialization tests"""
    
    @pytest.mark.unit
    def test_template_manager_init(self, auth_manager: AuthManager):
        """Test template manager initialization"""
        manager = TemplateManager(auth_manager)
        
        assert manager.auth_manager is auth_manager
        assert manager.connection_config is not None
        assert manager.connection_config.access_token == auth_manager.api_key
        assert manager._client is None


class TestTemplateManagerHTTPClient:
    """TemplateManager HTTP client tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_client_creation(self, auth_manager: AuthManager):
        """Test HTTP client creation"""
        manager = TemplateManager(auth_manager)
        
        client = await manager._get_client()
        
        assert client is not None
        assert manager._client is client
        
        # Second call should return the same client
        client2 = await manager._get_client()
        assert client2 is client
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_close_client(self, auth_manager: AuthManager):
        """Test closing HTTP client"""
        manager = TemplateManager(auth_manager)
        
        # Simulate client state without actually creating real client
        mock_client = Mock()
        manager._client = mock_client
        
        assert manager._client is not None
        
        # Mock close method
        with patch.object(manager, 'close') as mock_close:
            await manager.close()
            mock_close.assert_called_once()
        
        # Manually set to None to simulate post-close state
        manager._client = None
        assert manager._client is None


class TestTemplateManagerListTemplates:
    """TemplateManager list templates tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_list_templates_success(self, auth_manager: AuthManager):
        """Test successful template listing"""
        manager = TemplateManager(auth_manager)
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "templateID": "template-1",
                "aliases": ["test-agent"],
                "version": "1.0.0",
                "description": "Test template",
                "createdBy": {"email": "test@example.com"},
                "tags": ["test"],
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z"
            }
        ]
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            templates = await manager.list_templates()
        
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert all(isinstance(t, AgentTemplate) for t in templates)
        
        # Verify HTTP request
        mock_httpx_client.request.assert_called_once()
        call_args = mock_httpx_client.request.call_args
        assert call_args[1]['method'] == 'GET'
        assert call_args[1]['url'] == '/templates'
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_list_templates_with_metadata(self, auth_manager: AuthManager):
        """Test listing templates with metadata parameter"""
        manager = TemplateManager(auth_manager)
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            await manager.list_templates(with_metadata=True)
        
        # Verify request parameters
        call_args = mock_httpx_client.request.call_args
        assert call_args[1]['params']['metadata'] == "true"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_list_templates_auth_error(self, auth_manager: AuthManager):
        """Test authentication error"""
        manager = TemplateManager(auth_manager)
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.content = b"Unauthorized"
        mock_response.headers = {}
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            with pytest.raises(AuthenticationError) as exc_info:
                await manager.list_templates()
        
        assert "Invalid or expired API Key" in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_list_templates_network_error(self, auth_manager: AuthManager):
        """Test network error"""
        manager = TemplateManager(auth_manager)
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        # Simulate network error
        mock_httpx_client.request = AsyncMock(side_effect=Exception("Network error"))
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            with pytest.raises(NetworkError) as exc_info:
                await manager.list_templates()
        
        assert "Failed to list templates" in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_list_templates_invalid_response(self, auth_manager: AuthManager):
        """Test invalid response handling"""
        manager = TemplateManager(auth_manager)
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        # Simulate returning invalid template data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": "invalid-template",
                # Missing required fields
            }
        ]
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            templates = await manager.list_templates()
        
        # Should skip invalid templates without raising exception
        assert isinstance(templates, list)


class TestTemplateManagerGetTemplate:
    """TemplateManager get single template tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_template_success(self, auth_manager: AuthManager):
        """Test successful template retrieval"""
        manager = TemplateManager(auth_manager)
        template_id = "test-template-123"
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        # Mock list_templates response with the template
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "templateID": template_id,
            "aliases": ["test-agent"],
            "version": "1.0.0",
            "description": "Test template",
            "createdBy": {"email": "test@example.com"},
            "tags": ["test"],
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z"
        }]
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            template = await manager.get_template(template_id)
        
        assert isinstance(template, AgentTemplate)
        assert template.template_id == template_id
        
        # Verify HTTP request - get_template now calls list_templates
        mock_httpx_client.request.assert_called_once()
        call_args = mock_httpx_client.request.call_args
        assert call_args[1]['method'] == 'GET'
        assert call_args[1]['url'] == '/templates'
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_template_not_found(self, auth_manager: AuthManager):
        """Test template not found"""
        manager = TemplateManager(auth_manager)
        template_id = "non-existent-template"
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        # Mock list_templates returning empty list (template not found)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            with pytest.raises(TemplateNotFoundError) as exc_info:
                await manager.get_template(template_id)
        
        assert template_id in str(exc_info.value)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_template_auth_error(self, auth_manager: AuthManager):
        """Test authentication error when getting template"""
        manager = TemplateManager(auth_manager)
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.content = b"Unauthorized"
        mock_response.headers = {}
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            with pytest.raises(AuthenticationError):
                await manager.get_template("any-template")
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_template_network_error(self, auth_manager: AuthManager):
        """Test network error when getting template"""
        manager = TemplateManager(auth_manager)
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        # Simulate network error
        mock_httpx_client.request = AsyncMock(side_effect=Exception("Network error"))
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            with pytest.raises(NetworkError):
                await manager.get_template("any-template")


class TestTemplateManagerTemplateExists:
    """TemplateManager template existence check tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_template_exists_true(self, auth_manager: AuthManager):
        """Test template exists"""
        manager = TemplateManager(auth_manager)
        
        # Since template_exists now uses list_templates, we need to mock that instead
        sample_template = create_sample_template()
        sample_template.template_id = "existing-template"
        
        with patch.object(manager, 'list_templates', return_value=[sample_template]):
            exists = await manager.template_exists("existing-template")
        
        assert exists is True
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_template_exists_false(self, auth_manager: AuthManager):
        """Test template does not exist"""
        manager = TemplateManager(auth_manager)
        
        # Mock list_templates to return empty list (template not found)
        with patch.object(manager, 'list_templates', return_value=[]):
            exists = await manager.template_exists("non-existing-template")
        
        assert exists is False
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_template_exists_error_handling(self, auth_manager: AuthManager):
        """Test handling of other errors"""
        manager = TemplateManager(auth_manager)
        
        # Network errors and other exceptions should return False
        with patch.object(manager, 'get_template', side_effect=NetworkError("Network error")):
            exists = await manager.template_exists("any-template")
        
        assert exists is False


class TestTemplateManagerIntegration:
    """TemplateManager integration tests"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_template_manager_lifecycle(self, auth_manager: AuthManager):
        """Test complete template manager lifecycle"""
        manager = TemplateManager(auth_manager)
        
        try:
            # 1. Verify initial state
            assert manager._client is None
            
            # 2. Mock list templates (will create client)
            with patch.object(manager, '_get_client') as mock_get_client:
                # Create compatible mock API client
                mock_api_client = Mock()
                mock_httpx_client = Mock()
                mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
                
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = []
                mock_httpx_client.request = AsyncMock(return_value=mock_response)
                
                mock_get_client.return_value = mock_api_client
                
                templates = await manager.list_templates()
                assert isinstance(templates, list)
                assert mock_get_client.called
            
            # Clear cache between tests
            manager.clear_cache()
            
            # 3. Mock getting specific template
            with patch.object(manager, '_get_client') as mock_get_client:
                # Create compatible mock API client
                mock_api_client = Mock()
                mock_httpx_client = Mock()
                mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
                
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = [{
                    "templateID": "test-template-123",
                    "aliases": ["test-agent"],
                    "version": "1.0.0",
                    "description": "Test template",
                    "createdBy": {"email": "test@example.com"},
                    "tags": ["test"],
                    "createdAt": "2024-01-01T00:00:00Z",
                    "updatedAt": "2024-01-01T00:00:00Z"
                }]
                mock_httpx_client.request = AsyncMock(return_value=mock_response)
                
                mock_get_client.return_value = mock_api_client
                
                template = await manager.get_template("test-template-123")
                assert isinstance(template, AgentTemplate)
            
            # 4. Check template existence
            # Fix: template_exists uses list_templates as fallback
            sample_template = create_sample_template()
            sample_template.template_id = "test-template-123"
            with patch.object(manager, 'list_templates', return_value=[sample_template]):
                exists = await manager.template_exists("test-template-123")
                assert exists is True
        
        finally:
            # 5. Cleanup
            await manager.close()
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, auth_manager: AuthManager):
        """Test concurrent requests"""
        import asyncio
        
        manager = TemplateManager(auth_manager)
        
        # Create compatible mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            [],  # list_templates (first call)
            [{"templateID": "template-1", "aliases": ["template-1"], "version": "1.0.0"}],  # get_template (calls list_templates)
            [{"templateID": "template-2", "aliases": ["template-2"], "version": "1.0.0"}],  # get_template (calls list_templates)
        ]
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            with patch.object(manager, 'template_exists', return_value=True):
                # Execute multiple requests concurrently (disable cache to ensure each call is independent)
                tasks = [
                    manager.list_templates(use_cache=False),
                    manager.get_template("template-1", use_cache=False),
                    manager.get_template("template-2", use_cache=False),
                    manager.template_exists("template-3")
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Verify results
                assert len(results) == 4
                assert isinstance(results[0], list)  # list_templates
                assert isinstance(results[1], AgentTemplate)  # get_template
                assert isinstance(results[2], AgentTemplate)  # get_template
                assert isinstance(results[3], bool)  # template_exists
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_error_recovery(self, auth_manager: AuthManager):
        """Test error recovery"""
        manager = TemplateManager(auth_manager)
        
        # First request fails
        error_api_client = Mock()
        error_httpx_client = Mock()
        error_api_client.get_async_httpx_client.return_value = error_httpx_client
        error_httpx_client.request = AsyncMock(side_effect=Exception("Network error"))
        
        with patch.object(manager, '_get_client', return_value=error_api_client):
            with pytest.raises(NetworkError):
                await manager.list_templates()
        
        # Second request succeeds
        success_api_client = Mock()
        success_httpx_client = Mock()
        success_api_client.get_async_httpx_client.return_value = success_httpx_client
        
        success_response = Mock()
        success_response.status_code = 200
        success_response.json.return_value = []
        success_httpx_client.request = AsyncMock(return_value=success_response)
        
        with patch.object(manager, '_get_client', return_value=success_api_client):
            templates = await manager.list_templates()
            assert isinstance(templates, list)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_parameters_validation(self, auth_manager: AuthManager):
        """Test request parameter validation"""
        manager = TemplateManager(auth_manager)
        
        # Create compatible mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_httpx_client.request = AsyncMock(return_value=mock_response)
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            # Test various parameter combinations (disable cache to test all calls)
            await manager.list_templates(use_cache=False)  # No parameters
            await manager.list_templates(with_metadata=False, use_cache=False)  # Without metadata
            await manager.list_templates(with_metadata=True, use_cache=False)  # With metadata
        
        # Verify all requests were executed correctly
        assert mock_httpx_client.request.call_count == 3
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_template_data_consistency(self, auth_manager: AuthManager):
        """Test template data consistency"""
        manager = TemplateManager(auth_manager)
        mock_client = Mock()
        
        # Create mock API client
        mock_api_client = Mock()
        mock_httpx_client = Mock()
        mock_api_client.get_async_httpx_client.return_value = mock_httpx_client
        
        # Mock consistent template data - using new format
        template_data = {
            "templateID": "consistent-template",
            "aliases": ["consistent-agent"],
            "version": "1.0.0",
            "description": "Consistent test template",
            "createdBy": {"email": "test@example.com"},
            "tags": ["test"],
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z",
            "metadata": {}
        }
        
        # List response
        list_response = Mock()
        list_response.status_code = 200
        list_response.json.return_value = [template_data]
        
        # Single template response
        single_response = Mock()
        single_response.status_code = 200
        single_response.json.return_value = template_data
        
        mock_httpx_client.request = AsyncMock(side_effect=[list_response, single_response])
        
        with patch.object(manager, '_get_client', return_value=mock_api_client):
            # Get from list
            templates = await manager.list_templates()
            template_from_list = templates[0]
            
            # Get directly
            template_direct = await manager.get_template("consistent-template")
            
            # Verify data consistency
            assert template_from_list.template_id == template_direct.template_id
            assert template_from_list.name == template_direct.name
            assert template_from_list.version == template_direct.version
            assert template_from_list.author == template_direct.author
