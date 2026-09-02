"""
Decorator functionality unit tests

Tests the functionality and behavior of decorators in AgentRuntimeApp.
"""

import pytest
import asyncio
import inspect
from typing import Generator, AsyncGenerator

from novita_sandbox.agent_runtime.runtime.app import AgentRuntimeApp
from novita_sandbox.agent_runtime.runtime.context import RequestContext
from novita_sandbox.agent_runtime.runtime.models import RuntimeConfig, PingStatus


class TestEntrypointDecorator:
    """@entrypoint decorator tests"""
    
    @pytest.mark.unit
    def test_sync_function_decoration(self):
        """Test synchronous function decoration"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        def sync_agent(request: dict) -> dict:
            return {"response": "sync", "input": request.get("prompt", "")}
        
        # Verify function is properly registered
        assert app._entrypoint_func is not None
        assert app._entrypoint_func == sync_agent
        
        # Verify decorator doesn't change the function itself
        assert sync_agent.__name__ == "sync_agent"
        assert callable(sync_agent)
    
    @pytest.mark.unit
    def test_async_function_decoration(self):
        """Test asynchronous function decoration"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        async def async_agent(request: dict) -> dict:
            await asyncio.sleep(0.01)
            return {"response": "async", "input": request.get("prompt", "")}
        
        # Verify function is properly registered
        assert app._entrypoint_func is not None
        assert app._entrypoint_func == async_agent
        assert inspect.iscoroutinefunction(async_agent)
    
    @pytest.mark.unit
    def test_function_with_context_decoration(self):
        """Test function decoration with context parameter"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        def agent_with_context(request: dict, context: RequestContext) -> dict:
            return {
                "response": "with_context",
                "sandbox_id": context.sandbox_id,
                "request_id": context.request_id
            }
        
        # Verify function is properly registered
        assert app._entrypoint_func is not None
        assert app._entrypoint_func == agent_with_context
        
        # Verify function signature
        sig = inspect.signature(agent_with_context)
        params = list(sig.parameters.keys())
        assert "request" in params
        assert "context" in params
    
    @pytest.mark.unit
    def test_sync_generator_decoration(self):
        """Test synchronous generator function decoration"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        def streaming_agent(request: dict) -> Generator[str, None, None]:
            for i in range(3):
                yield f"chunk_{i}: {request.get('prompt', '')}"
        
        # Verify function is properly registered
        assert app._entrypoint_func is not None
        assert app._entrypoint_func == streaming_agent
        
        # Verify return value is a generator
        result = streaming_agent({"prompt": "test"})
        assert inspect.isgenerator(result)
        
        # Verify generator content
        chunks = list(result)
        assert len(chunks) == 3
        assert chunks[0] == "chunk_0: test"
    
    @pytest.mark.unit
    def test_multiple_entrypoint_registration(self):
        """Test multiple entrypoint registration (should override)"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        def first_agent(request: dict) -> dict:
            return {"agent": "first"}
        
        assert app._entrypoint_func == first_agent
        
        @app.entrypoint
        def second_agent(request: dict) -> dict:
            return {"agent": "second"}
        
        # Second should override first
        assert app._entrypoint_func == second_agent
        assert app._entrypoint_func != first_agent


class TestPingDecorator:
    """@ping decorator tests"""
    
    @pytest.mark.unit
    def test_sync_ping_decoration(self):
        """Test synchronous ping function decoration"""
        app = AgentRuntimeApp()
        
        @app.ping
        def custom_ping() -> dict:
            return {"status": "healthy", "service": "test"}
        
        # Verify function is properly registered
        assert app._ping_func is not None
        assert app._ping_func == custom_ping
    
    @pytest.mark.unit
    def test_async_ping_decoration(self):
        """Test asynchronous ping function decoration"""
        app = AgentRuntimeApp()
        
        @app.ping
        async def async_ping() -> dict:
            await asyncio.sleep(0.01)
            return {"status": "healthy", "service": "async_test"}
        
        # Verify function is properly registered
        assert app._ping_func is not None
        assert app._ping_func == async_ping
        assert inspect.iscoroutinefunction(async_ping)


class TestMiddlewareDecorator:
    """@middleware decorator tests"""
    
    @pytest.mark.unit
    def test_middleware_registration(self):
        """Test middleware registration"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.middleware
        async def test_middleware(request, call_next):
            # Simulate middleware logic
            response = await call_next(request)
            return response
        
        # Verify server is created and middleware is registered
        assert app._server is not None
        # Decorator should return the original function
        assert test_middleware.__name__ == "test_middleware"


class TestDecoratorCombination:
    """Decorator combination tests"""
    
    @pytest.mark.unit
    def test_all_decorators_together(self):
        """Test all decorators used together"""
        config = RuntimeConfig(debug=True)
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def main_agent(request: dict, context: RequestContext) -> dict:
            return {
                "response": "main",
                "sandbox_id": context.sandbox_id
            }
        
        @app.ping
        def health_check() -> dict:
            return {"status": "healthy", "timestamp": "2024-01-01"}
        
        @app.middleware
        async def logging_middleware(request, call_next):
            # Simulate logging
            response = await call_next(request)
            return response
        
        # Verify all functions are properly registered
        assert app._entrypoint_func == main_agent
        assert app._ping_func == health_check
        assert app._server is not None


class TestDecoratorErrorHandling:
    """Decorator error handling tests"""
    
    @pytest.mark.unit
    def test_entrypoint_function_with_exceptions(self):
        """Test entrypoint function throwing exceptions"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        def error_agent(request: dict) -> dict:
            if request.get("error"):
                raise ValueError("Test error")
            return {"response": "success"}
        
        # Normal invocation
        result = error_agent({"prompt": "test"})
        assert result == {"response": "success"}
        
        # Exception invocation
        with pytest.raises(ValueError, match="Test error"):
            error_agent({"error": True})