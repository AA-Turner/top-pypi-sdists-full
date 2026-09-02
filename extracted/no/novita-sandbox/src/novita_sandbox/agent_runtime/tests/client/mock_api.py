"""
Mock API responses

Simulates HTTP API responses for unit testing
"""

import asyncio
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, AsyncMock
from .test_fixtures import (
    create_mock_template_list_response,
    create_mock_template_response,
    create_mock_agent_response,
    create_mock_ping_response,
    create_auth_error_response,
    create_template_not_found_response,
    create_streaming_chunks
)


class MockHTTPClient:
    """Mock HTTP client"""
    
    def __init__(self):
        self.request_history = []
        self.response_status = 200
        self.response_data = {}
        self.simulate_delay = 0.0
        self.simulate_error = None
        
        # Add call tracking for test assertion compatibility
        self.get = AsyncMock(side_effect=self._get_impl)
        self.post = AsyncMock(side_effect=self._post_impl)
    
    async def _get_impl(self, url: str, **kwargs) -> Mock:
        """Mock GET request"""
        await self._simulate_request_delay()
        
        if self.simulate_error:
            raise self.simulate_error
        
        # Record request history
        self.request_history.append({
            "method": "GET",
            "url": url,
            "kwargs": kwargs
        })
        
        # Return different responses based on URL path
        response = Mock()
        response.status_code = self.response_status
        
        if "/v1/templates/agents/" in url and url.split("/")[-1] != "agents":
            # Single template query
            template_id = url.split("/")[-1]
            if self.response_status == 404:
                response.text = "Template not found"
                response.json = AsyncMock(side_effect=Exception("404 Not Found"))
            else:
                response.json = AsyncMock(return_value=create_mock_template_response(template_id))
        elif "/v1/templates/agents" in url:
            # Template list query
            if self.response_status == 401:
                response.text = "Unauthorized"
                response.json = AsyncMock(side_effect=Exception("401 Unauthorized"))
            else:
                response.json = AsyncMock(return_value=create_mock_template_list_response())
        elif "/ping" in url:
            # Health check
            response.json = AsyncMock(return_value=create_mock_ping_response())
        else:
            # Default response
            response.json = AsyncMock(return_value=self.response_data)
        
        return response
    
    async def _post_impl(self, url: str, **kwargs) -> Mock:
        """Mock POST request"""
        await self._simulate_request_delay()
        
        if self.simulate_error:
            raise self.simulate_error
        
        # Record request history
        self.request_history.append({
            "method": "POST",
            "url": url,
            "kwargs": kwargs
        })
        
        response = Mock()
        response.status_code = self.response_status
        
        if "/invocations" in url:
            # Agent invocation
            if self.response_status == 401:
                response.text = "Unauthorized"
                response.json = AsyncMock(side_effect=Exception("401 Unauthorized"))
            else:
                response.json = AsyncMock(return_value=create_mock_agent_response())
        else:
            # Default response
            response.json = AsyncMock(return_value=self.response_data)
        
        return response
    
    async def stream(self, method: str, url: str, **kwargs):
        """Mock streaming request"""
        await self._simulate_request_delay()
        
        if self.simulate_error:
            raise self.simulate_error
        
        # Record request history
        self.request_history.append({
            "method": f"STREAM_{method}",
            "url": url,
            "kwargs": kwargs
        })
        
        return MockStreamingResponse()
    
    async def aclose(self):
        """Mock close client"""
        pass
    
    async def _simulate_request_delay(self):
        """Simulate request delay"""
        if self.simulate_delay > 0:
            await asyncio.sleep(self.simulate_delay)
    
    def set_response(self, status_code: int, data: Dict[str, Any]):
        """Set response data"""
        self.response_status = status_code
        self.response_data = data
    
    def set_error(self, error: Exception):
        """Set simulated error"""
        self.simulate_error = error
    
    def set_delay(self, delay: float):
        """Set request delay"""
        self.simulate_delay = delay
    
    def clear_history(self):
        """Clear request history"""
        self.request_history = []


class MockStreamingResponse:
    """Mock streaming response"""
    
    def __init__(self):
        self.status_code = 200
        self.chunks = create_streaming_chunks()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def aiter_text(self):
        """Async iterate text chunks"""
        for chunk in self.chunks:
            await asyncio.sleep(0.01)  # Simulate network delay
            yield chunk
    
    async def aread(self):
        """Read complete response"""
        return "Error response content"


# =============================================================================
# Predefined Mock configurations
# =============================================================================

def create_success_mock_client() -> MockHTTPClient:
    """Create Mock client with success response"""
    client = MockHTTPClient()
    client.set_response(200, {})
    return client


def create_auth_error_mock_client() -> MockHTTPClient:
    """Create Mock client with authentication error"""
    client = MockHTTPClient()
    client.set_response(401, create_auth_error_response())
    return client


def create_template_not_found_mock_client() -> MockHTTPClient:
    """Create Mock client with template not found error"""
    client = MockHTTPClient()
    client.set_response(404, create_template_not_found_response())
    return client


def create_network_error_mock_client() -> MockHTTPClient:
    """Create Mock client with network error"""
    client = MockHTTPClient()
    client.set_error(Exception("Network connection failed"))
    return client


def create_slow_mock_client(delay: float = 1.0) -> MockHTTPClient:
    """Create Mock client with slow response"""
    client = MockHTTPClient()
    client.set_delay(delay)
    return client


# =============================================================================
# aioresponses integration
# =============================================================================

def setup_template_responses(mock_client, base_url: str = "https://api.test.novita.ai"):
    """Setup template-related Mock responses"""
    # Template list
    mock_client.get(
        f"{base_url}/v1/templates/agents",
        payload=create_mock_template_list_response()
    )
    
    # Single template
    mock_client.get(
        f"{base_url}/v1/templates/agents/test-template-123",
        payload=create_mock_template_response("test-template-123")
    )
    
    # Template not found
    mock_client.get(
        f"{base_url}/v1/templates/agents/non-existent",
        status=404,
        payload=create_template_not_found_response()
    )


def setup_agent_responses(mock_client, base_url: str = "https://test-sandbox.novita.ai"):
    """Setup Agent-related Mock responses"""
    # Successful invocation
    mock_client.post(
        f"{base_url}/invocations",
        payload=create_mock_agent_response()
    )
    
    # Health check
    mock_client.get(
        f"{base_url}/ping",
        payload=create_mock_ping_response()
    )


def setup_error_responses(mock_client):
    """Setup error responses"""
    # Authentication error
    mock_client.get(
        "https://api.test.novita.ai/v1/templates/agents",
        status=401,
        payload=create_auth_error_response()
    )
    
    # Agent invocation error
    mock_client.post(
        "https://test-sandbox.novita.ai/invocations",
        status=500,
        payload={
            "error": "Internal server error",
            "error_code": "AGENT_ERROR",
            "message": "Agent execution failed"
        }
    )
