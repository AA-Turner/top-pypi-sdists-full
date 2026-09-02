"""
Mock Agent Functions

Provides various types of Mock Agent functions for testing.
"""

import asyncio
import time
from typing import Any, Dict, List, Optional, Generator, AsyncGenerator
from unittest.mock import Mock, AsyncMock

from novita_sandbox.agent_runtime.runtime.context import RequestContext


class MockAgentFunctions:
    """Mock Agent function collection"""
    
    @staticmethod
    def simple_sync_agent(request: dict) -> dict:
        """Simple synchronous Agent function"""
        return {
            "response": f"Processed: {request.get('prompt', '')}",
            "status": "success",
            "type": "sync"
        }
    
    @staticmethod
    async def simple_async_agent(request: dict) -> dict:
        """Simple asynchronous Agent function"""
        await asyncio.sleep(0.01)  # Simulate async operation
        return {
            "response": f"Async processed: {request.get('prompt', '')}",
            "status": "success",
            "type": "async"
        }
    
    @staticmethod
    def agent_with_context(request: dict, context: RequestContext) -> dict:
        """Agent function with context"""
        return {
            "response": f"Processed: {request.get('prompt', '')}",
            "sandbox_id": context.sandbox_id,
            "request_id": context.request_id,
            "headers_count": len(context.headers),
            "type": "with_context"
        }
    
    @staticmethod
    async def async_agent_with_context(request: dict, context: RequestContext) -> dict:
        """Async Agent function with context"""
        await asyncio.sleep(0.01)
        return {
            "response": f"Async processed: {request.get('prompt', '')}",
            "sandbox_id": context.sandbox_id,
            "request_id": context.request_id,
            "session_id": context.session_id,  # Test backward compatibility
            "type": "async_with_context"
        }
    
    @staticmethod
    def streaming_agent(request: dict) -> Generator[str, None, None]:
        """Synchronous streaming Agent function"""
        prompt = request.get("prompt", "")
        chunk_count = request.get("chunks", 3)
        
        for i in range(chunk_count):
            time.sleep(0.01)  # Simulate processing time
            yield f"Chunk {i+1}: Processing '{prompt}'"
        
        yield f"Final: Completed processing '{prompt}'"
    
    @staticmethod
    async def async_streaming_agent(request: dict) -> AsyncGenerator[str, None]:
        """Asynchronous streaming Agent function"""
        prompt = request.get("prompt", "")
        chunk_count = request.get("chunks", 3)
        
        for i in range(chunk_count):
            await asyncio.sleep(0.01)  # Simulate async processing time
            yield f"Async Chunk {i+1}: Processing '{prompt}'"
        
        yield f"Async Final: Completed processing '{prompt}'"
    
    @staticmethod
    def slow_agent(request: dict) -> dict:
        """Slow Agent function (for timeout testing)"""
        delay = request.get("delay", 1.0)
        time.sleep(delay)
        return {
            "response": f"Slow processed after {delay}s",
            "delay": delay
        }
    
    @staticmethod
    async def slow_async_agent(request: dict) -> dict:
        """Slow asynchronous Agent function"""
        delay = request.get("delay", 1.0)
        await asyncio.sleep(delay)
        return {
            "response": f"Slow async processed after {delay}s",
            "delay": delay
        }
    
    @staticmethod
    def error_agent(request: dict) -> dict:
        """Agent function that raises exceptions"""
        error_type = request.get("error_type", "ValueError")
        error_message = request.get("error_message", "Test error")
        
        if error_type == "ValueError":
            raise ValueError(error_message)
        elif error_type == "RuntimeError":
            raise RuntimeError(error_message)
        elif error_type == "KeyError":
            raise KeyError(error_message)
        else:
            raise Exception(error_message)
    
    @staticmethod
    async def async_error_agent(request: dict) -> dict:
        """Async Agent function that raises exceptions"""
        await asyncio.sleep(0.01)
        error_type = request.get("error_type", "ValueError")
        error_message = request.get("error_message", "Async test error")
        
        if error_type == "ValueError":
            raise ValueError(error_message)
        elif error_type == "RuntimeError":
            raise RuntimeError(error_message)
        else:
            raise Exception(error_message)
    
    @staticmethod
    def data_processing_agent(request: dict) -> dict:
        """Data processing Agent function"""
        data = request.get("data", {})
        operation = request.get("operation", "count")
        
        if operation == "count":
            result = len(data) if isinstance(data, (list, dict, str)) else 0
        elif operation == "sum" and isinstance(data, list):
            result = sum(x for x in data if isinstance(x, (int, float)))
        elif operation == "keys" and isinstance(data, dict):
            result = list(data.keys())
        else:
            result = "unknown_operation"
        
        return {
            "operation": operation,
            "result": result,
            "input_type": type(data).__name__
        }
    
    @staticmethod
    def large_response_agent(request: dict) -> dict:
        """Agent function that returns large amounts of data"""
        size = request.get("size", 1000)
        return {
            "response": "Large data response",
            "data": [f"item_{i}" for i in range(size)],
            "size": size
        }
    
    @staticmethod
    def conditional_agent(request: dict) -> dict:
        """Agent function that returns different results based on input conditions"""
        condition = request.get("condition", "default")
        
        if condition == "success":
            return {"status": "success", "message": "Operation completed"}
        elif condition == "warning":
            return {"status": "warning", "message": "Operation completed with warnings"}
        elif condition == "error":
            return {"status": "error", "message": "Operation failed"}
        else:
            return {"status": "unknown", "message": "Unknown condition"}


class MockHealthChecks:
    """Mock health check function collection"""
    
    @staticmethod
    def healthy_ping() -> dict:
        """Healthy ping function"""
        return {
            "status": "Healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "service": "mock_agent"
        }
    
    @staticmethod
    def busy_ping() -> dict:
        """Busy state ping function"""
        return {
            "status": "HealthyBusy",
            "message": "System under load",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    
    @staticmethod
    async def async_ping() -> dict:
        """Asynchronous ping function"""
        await asyncio.sleep(0.01)
        return {
            "status": "Healthy",
            "async": True,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    
    @staticmethod
    def error_ping() -> dict:
        """Ping function that raises exceptions"""
        raise RuntimeError("Health check failed")
    
    @staticmethod
    def custom_ping_with_metrics() -> dict:
        """Custom ping function with metrics"""
        return {
            "status": "Healthy",
            "metrics": {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "active_connections": 15
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }


class MockMiddlewares:
    """Mock middleware function collection"""
    
    @staticmethod
    async def logging_middleware(request, call_next):
        """Logging middleware"""
        start_time = time.time()
        
        # Log request start
        print(f"Request started: {request.url}")
        
        # Call next middleware or handler
        response = await call_next(request)
        
        # Log request completion
        duration = time.time() - start_time
        print(f"Request completed in {duration:.4f}s")
        
        return response
    
    @staticmethod
    async def auth_middleware(request, call_next):
        """Authentication middleware"""
        # Check authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            from starlette.responses import JSONResponse
            return JSONResponse(
                {"error": "Missing or invalid authorization"},
                status_code=401
            )
        
        return await call_next(request)
    
    @staticmethod
    async def cors_middleware(request, call_next):
        """CORS middleware"""
        response = await call_next(request)
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        
        return response
    
    @staticmethod
    async def error_handling_middleware(request, call_next):
        """Error handling middleware"""
        try:
            return await call_next(request)
        except Exception as e:
            from starlette.responses import JSONResponse
            return JSONResponse(
                {"error": str(e), "type": type(e).__name__},
                status_code=500
            )
    
    @staticmethod
    async def request_modification_middleware(request, call_next):
        """Middleware that modifies requests"""
        # Modify request (needs careful handling in actual implementation)
        # This just simulates adding some metadata
        
        response = await call_next(request)
        
        # Modify response
        if hasattr(response, 'headers'):
            response.headers["X-Processed-By"] = "MockMiddleware"
        
        return response


class MockAgentFactory:
    """Mock Agent factory class"""
    
    @classmethod
    def create_configurable_agent(cls, config: dict):
        """Create configurable Agent function"""
        def configurable_agent(request: dict) -> dict:
            # Generate response using config and request
            response_template = config.get("response_template", "Processed: {prompt}")
            prompt = request.get("prompt", "")
            
            result = {
                "response": response_template.format(prompt=prompt),
                "config": config,
                "request_id": request.get("request_id")
            }
            
            # If config requires delay
            if config.get("delay"):
                time.sleep(config["delay"])
            
            # If config requires raising exception
            if config.get("raise_error"):
                raise ValueError(config.get("error_message", "Configured error"))
            
            return result
        
        return configurable_agent
    
    @classmethod
    def create_streaming_agent(cls, chunk_count: int = 5, delay: float = 0.01):
        """Create streaming Agent function"""
        async def streaming_agent(request: dict) -> AsyncGenerator[str, None]:
            prompt = request.get("prompt", "")
            for i in range(chunk_count):
                await asyncio.sleep(delay)
                yield f"Stream chunk {i+1}/{chunk_count}: {prompt}"
        
        return streaming_agent
    
    @classmethod
    def create_mock_with_validation(cls, required_fields: List[str]):
        """Create Mock Agent with input validation"""
        def validating_agent(request: dict) -> dict:
            # Validate required fields
            missing_fields = [field for field in required_fields if field not in request]
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")
            
            return {
                "response": "Validation passed",
                "validated_fields": required_fields,
                "request_data": request
            }
        
        return validating_agent


# Predefined common Mock Agent instances
MOCK_AGENTS = {
    "simple": MockAgentFunctions.simple_sync_agent,
    "async": MockAgentFunctions.simple_async_agent,
    "streaming": MockAgentFunctions.streaming_agent,
    "async_streaming": MockAgentFunctions.async_streaming_agent,
    "with_context": MockAgentFunctions.agent_with_context,
    "error": MockAgentFunctions.error_agent,
    "slow": MockAgentFunctions.slow_agent,
    "data_processing": MockAgentFunctions.data_processing_agent,
}

MOCK_HEALTH_CHECKS = {
    "healthy": MockHealthChecks.healthy_ping,
    "busy": MockHealthChecks.busy_ping,
    "async": MockHealthChecks.async_ping,
    "error": MockHealthChecks.error_ping,
    "metrics": MockHealthChecks.custom_ping_with_metrics,
}

MOCK_MIDDLEWARES = {
    "logging": MockMiddlewares.logging_middleware,
    "auth": MockMiddlewares.auth_middleware,
    "cors": MockMiddlewares.cors_middleware,
    "error_handling": MockMiddlewares.error_handling_middleware,
    "request_modification": MockMiddlewares.request_modification_middleware,
}