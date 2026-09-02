"""
Mock Server

Provides tools for simulating HTTP servers and network requests.
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional, Callable, Union
from unittest.mock import Mock, AsyncMock, MagicMock
from contextlib import asynccontextmanager

import httpx
from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route


class MockHTTPServer:
    """Mock HTTP server"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8999):
        self.host = host
        self.port = port
        self.app = None
        self.server = None
        self.responses = {}
        self.request_log = []
        
    def setup_response(self, path: str, method: str = "POST", 
                      response_data: Dict = None, status_code: int = 200,
                      delay: float = 0):
        """Setup response for specific path"""
        self.responses[f"{method.upper()}:{path}"] = {
            "data": response_data or {"message": "mock response"},
            "status_code": status_code,
            "delay": delay
        }
    
    def create_app(self) -> Starlette:
        """Create Starlette application"""
        async def handle_request(request):
            # Log request
            request_info = {
                "method": request.method,
                "path": request.url.path,
                "headers": dict(request.headers),
                "timestamp": time.time()
            }
            
            # Try to read request body
            try:
                if request.method in ["POST", "PUT", "PATCH"]:
                    request_info["body"] = await request.json()
            except:
                request_info["body"] = None
            
            self.request_log.append(request_info)
            
            # Find preset response
            key = f"{request.method}:{request.url.path}"
            if key in self.responses:
                response_config = self.responses[key]
                
                # Simulate delay
                if response_config["delay"] > 0:
                    await asyncio.sleep(response_config["delay"])
                
                return JSONResponse(
                    response_config["data"],
                    status_code=response_config["status_code"]
                )
            
            # Default response
            return JSONResponse(
                {"error": "Mock server - no response configured"},
                status_code=404
            )
        
        # Create generic routes
        routes = [
            Route("/{path:path}", handle_request, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
        ]
        
        return Starlette(routes=routes)
    
    async def start(self):
        """Start server"""
        import uvicorn
        self.app = self.create_app()
        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="error")
        self.server = uvicorn.Server(config)
        await self.server.serve()
    
    def get_request_log(self) -> List[Dict]:
        """Get request log"""
        return self.request_log.copy()
    
    def clear_request_log(self):
        """Clear request log"""
        self.request_log.clear()
    
    @property
    def base_url(self) -> str:
        """Get server base URL"""
        return f"http://{self.host}:{self.port}"


class MockAgentRuntimeServer:
    """Mock Agent Runtime server"""
    
    def __init__(self):
        self.invocation_responses = []
        self.ping_responses = []
        self.request_count = 0
        self.error_responses = {}
        
    def setup_invocation_response(self, response_data: Dict, delay: float = 0):
        """Setup invocation response"""
        self.invocation_responses.append({
            "data": response_data,
            "delay": delay
        })
    
    def setup_ping_response(self, response_data: Dict, delay: float = 0):
        """Setup ping response"""
        self.ping_responses.append({
            "data": response_data,
            "delay": delay
        })
    
    def setup_error_response(self, path: str, status_code: int, error_message: str):
        """Setup error response"""
        self.error_responses[path] = {
            "status_code": status_code,
            "message": error_message
        }
    
    async def handle_invocation(self, request_data: Dict) -> Dict:
        """Handle invocation request"""
        self.request_count += 1
        
        # Check for error response configuration
        if "/invocations" in self.error_responses:
            error_config = self.error_responses["/invocations"]
            raise httpx.HTTPStatusError(
                f"HTTP {error_config['status_code']}",
                request=None,
                response=Mock(status_code=error_config['status_code'])
            )
        
        # Use preset response or default response
        if self.invocation_responses:
            response_config = self.invocation_responses.pop(0)
            
            if response_config["delay"] > 0:
                await asyncio.sleep(response_config["delay"])
            
            return response_config["data"]
        
        # Default response
        return {
            "result": f"Mock response for: {request_data.get('prompt', '')}",
            "status": "success",
            "duration": 0.1,
            "metadata": {"mock": True, "request_count": self.request_count}
        }
    
    async def handle_ping(self) -> Dict:
        """Handle ping request"""
        # Check for error response configuration
        if "/ping" in self.error_responses:
            error_config = self.error_responses["/ping"]
            raise httpx.HTTPStatusError(
                f"HTTP {error_config['status_code']}",
                request=None,
                response=Mock(status_code=error_config['status_code'])
            )
        
        # Use preset response or default response
        if self.ping_responses:
            response_config = self.ping_responses.pop(0)
            
            if response_config["delay"] > 0:
                await asyncio.sleep(response_config["delay"])
            
            return response_config["data"]
        
        # Default response
        return {
            "status": "Healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "mock": True
        }
    
    def create_starlette_app(self) -> Starlette:
        """Create complete Mock Starlette application"""
        async def handle_root(request):
            return JSONResponse({
                "service": "Mock Agent Runtime",
                "status": "running",
                "mock": True
            })
        
        async def handle_ping_endpoint(request):
            try:
                result = await self.handle_ping()
                return JSONResponse(result)
            except httpx.HTTPStatusError as e:
                return JSONResponse(
                    {"error": "Mock ping error"},
                    status_code=e.response.status_code
                )
        
        async def handle_invocations_endpoint(request):
            try:
                request_data = await request.json()
                result = await self.handle_invocation(request_data)
                
                # Check if it's a streaming request
                if request_data.get("stream", False):
                    return StreamingResponse(
                        self._create_stream_response(result),
                        media_type="text/plain"
                    )
                
                return JSONResponse(result)
            except httpx.HTTPStatusError as e:
                return JSONResponse(
                    {"error": "Mock invocation error"},
                    status_code=e.response.status_code
                )
            except Exception as e:
                return JSONResponse(
                    {"error": str(e)},
                    status_code=500
                )
        
        routes = [
            Route("/", handle_root, methods=["GET"]),
            Route("/ping", handle_ping_endpoint, methods=["GET"]),
            Route("/invocations", handle_invocations_endpoint, methods=["POST"])
        ]
        
        return Starlette(routes=routes)
    
    async def _create_stream_response(self, result: Dict):
        """Create streaming response"""
        # Simulate streaming data
        chunks = [
            "Starting processing...",
            f"Processing: {result.get('result', '')}",
            "Finalizing...",
            "Done!"
        ]
        
        for chunk in chunks:
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.01)


class MockHTTPClient:
    """Mock HTTP client"""
    
    def __init__(self):
        self.responses = {}
        self.request_history = []
        self.default_response = {"mock": True}
        
    def setup_response(self, method: str, url: str, 
                      response_data: Any = None, 
                      status_code: int = 200,
                      headers: Dict = None):
        """Setup response for specific request"""
        key = f"{method.upper()}:{url}"
        self.responses[key] = {
            "data": response_data or self.default_response,
            "status_code": status_code,
            "headers": headers or {}
        }
    
    def create_mock_client(self) -> Mock:
        """Create Mock HTTP client"""
        mock_client = Mock()
        
        # Simulate async context manager
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        
        # Setup HTTP methods
        for method in ["get", "post", "put", "delete", "patch"]:
            setattr(mock_client, method, self._create_method_mock(method.upper()))
        
        return mock_client
    
    def _create_method_mock(self, method: str):
        """Create Mock for specific HTTP method"""
        async def method_mock(url: str, **kwargs):
            # Log request
            request_info = {
                "method": method,
                "url": url,
                "kwargs": kwargs,
                "timestamp": time.time()
            }
            self.request_history.append(request_info)
            
            # Find preset response
            key = f"{method}:{url}"
            if key in self.responses:
                response_config = self.responses[key]
                
                # Create response Mock
                response_mock = Mock()
                response_mock.status_code = response_config["status_code"]
                response_mock.headers = response_config["headers"]
                response_mock.json = AsyncMock(return_value=response_config["data"])
                response_mock.text = json.dumps(response_config["data"])
                
                return response_mock
            
            # Default response
            default_mock = Mock()
            default_mock.status_code = 200
            default_mock.headers = {}
            default_mock.json = AsyncMock(return_value=self.default_response)
            default_mock.text = json.dumps(self.default_response)
            
            return default_mock
        
        return AsyncMock(side_effect=method_mock)
    
    def get_request_history(self) -> List[Dict]:
        """Get request history"""
        return self.request_history.copy()
    
    def clear_request_history(self):
        """Clear request history"""
        self.request_history.clear()


class MockNetworkScenarios:
    """Mock network scenarios"""
    
    @staticmethod
    def create_timeout_client(timeout_delay: float = 5.0):
        """Create client that times out"""
        async def timeout_method(*args, **kwargs):
            await asyncio.sleep(timeout_delay)
            raise httpx.TimeoutException("Request timed out")
        
        mock_client = Mock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        
        for method in ["get", "post", "put", "delete"]:
            setattr(mock_client, method, AsyncMock(side_effect=timeout_method))
        
        return mock_client
    
    @staticmethod
    def create_network_error_client(error_type: str = "ConnectionError"):
        """Create client with network errors"""
        def error_method(*args, **kwargs):
            if error_type == "ConnectionError":
                raise httpx.ConnectError("Connection failed")
            elif error_type == "DNSError":
                raise httpx.ConnectError("DNS resolution failed")
            else:
                raise httpx.RequestError("Network error")
        
        mock_client = Mock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        
        for method in ["get", "post", "put", "delete"]:
            setattr(mock_client, method, AsyncMock(side_effect=error_method))
        
        return mock_client
    
    @staticmethod
    def create_rate_limited_client(limit_after: int = 3):
        """Create rate-limited client"""
        request_count = {"count": 0}
        
        async def rate_limited_method(*args, **kwargs):
            request_count["count"] += 1
            if request_count["count"] > limit_after:
                # Simulate 429 Too Many Requests
                response_mock = Mock()
                response_mock.status_code = 429
                raise httpx.HTTPStatusError(
                    "429 Too Many Requests",
                    request=None,
                    response=response_mock
                )
            
            # Normal response
            response_mock = Mock()
            response_mock.status_code = 200
            response_mock.json = AsyncMock(return_value={"success": True})
            return response_mock
        
        mock_client = Mock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        
        for method in ["get", "post", "put", "delete"]:
            setattr(mock_client, method, AsyncMock(side_effect=rate_limited_method))
        
        return mock_client


# Predefined Mock server configurations
MOCK_SERVER_CONFIGS = {
    "healthy_agent": {
        "invocation_response": {
            "result": "Healthy agent response",
            "status": "success",
            "duration": 0.1
        },
        "ping_response": {
            "status": "Healthy",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    },
    "slow_agent": {
        "invocation_response": {
            "result": "Slow agent response",
            "status": "success", 
            "duration": 2.0
        },
        "invocation_delay": 2.0
    },
    "error_agent": {
        "error_responses": {
            "/invocations": {
                "status_code": 500,
                "message": "Internal server error"
            }
        }
    }
}