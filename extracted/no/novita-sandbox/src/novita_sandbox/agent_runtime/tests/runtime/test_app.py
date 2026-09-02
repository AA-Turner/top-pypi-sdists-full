"""
AgentRuntimeApp unit tests

Tests the complete functionality of the AgentRuntimeApp class, including initialization, configuration, decorator integration, lifecycle management, etc.
"""

import pytest
import asyncio
import inspect
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Generator, AsyncGenerator

from novita_sandbox.agent_runtime.runtime.app import AgentRuntimeApp
from novita_sandbox.agent_runtime.runtime.server import AgentRuntimeServer
from novita_sandbox.agent_runtime.runtime.context import RequestContext, AgentRuntimeContext
from novita_sandbox.agent_runtime.runtime.models import RuntimeConfig, PingStatus


class TestAgentRuntimeAppInitialization:
    """AgentRuntimeApp initialization tests"""
    
    @pytest.mark.unit
    def test_default_initialization(self):
        """Test default initialization"""
        app = AgentRuntimeApp()
        
        # Verify default configuration
        assert app.config is not None
        assert isinstance(app.config, RuntimeConfig)
        assert app.config.host == "0.0.0.0"
        assert app.config.port == 8080
        assert app.config.debug is False
        
        # Verify initial state
        assert app._server is None
        assert app._entrypoint_func is None
        assert app._ping_func is None
        
    @pytest.mark.unit
    def test_custom_config_initialization(self):
        """Test custom configuration initialization"""
        config = RuntimeConfig(
            host="127.0.0.1",
            port=9000,
            debug=True,
            timeout=600,
            max_request_size=2 * 1024 * 1024
        )
        
        app = AgentRuntimeApp(config=config)
        
        assert app.config.host == "127.0.0.1"
        assert app.config.port == 9000
        assert app.config.debug is True
        assert app.config.timeout == 600
        assert app.config.max_request_size == 2 * 1024 * 1024
    
    @pytest.mark.unit
    def test_debug_flag_initialization(self):
        """Test debug flag initialization"""
        app = AgentRuntimeApp(debug=True)
        
        assert app.config.debug is True
        
        # Test debug flag overriding configuration
        config = RuntimeConfig(debug=False)
        app = AgentRuntimeApp(config=config, debug=True)
        
        assert app.config.debug is True


class TestAgentRuntimeAppDecorators:
    """AgentRuntimeApp decorator integration tests"""
    
    @pytest.mark.unit
    def test_entrypoint_decorator_integration(self):
        """Test entrypoint decorator integration"""
        app = AgentRuntimeApp()
        
        # Test synchronous function
        @app.entrypoint
        def sync_agent(request: dict) -> dict:
            return {"response": "sync", "data": request}
        
        assert app._entrypoint_func is sync_agent
        
        # Test asynchronous function
        @app.entrypoint
        async def async_agent(request: dict) -> dict:
            return {"response": "async", "data": request}
        
        assert app._entrypoint_func is async_agent
        assert inspect.iscoroutinefunction(async_agent)
    
    @pytest.mark.unit
    def test_ping_decorator_integration(self):
        """Test ping decorator integration"""
        app = AgentRuntimeApp()
        
        @app.ping
        def custom_ping() -> dict:
            return {"status": "healthy", "service": "test"}
        
        assert app._ping_func is custom_ping
        
        # Test invocation
        result = custom_ping()
        assert result["status"] == "healthy"
        assert result["service"] == "test"
    
    @pytest.mark.unit
    def test_middleware_decorator_integration(self):
        """Test middleware decorator integration"""
        app = AgentRuntimeApp()
        
        # Middleware decorator should create server instance
        assert app._server is None
        
        @app.middleware
        async def test_middleware(request, call_next):
            response = await call_next(request)
            return response
        
        # After registering middleware, should have server instance
        assert app._server is not None
        assert isinstance(app._server, AgentRuntimeServer)


class TestAgentRuntimeAppContextAccess:
    """AgentRuntimeApp context access tests"""
    
    def teardown_method(self):
        """Clear context after each test method"""
        AgentRuntimeContext.clear_current_context()
    
    @pytest.mark.unit
    def test_context_property_access(self):
        """Test context property access"""
        app = AgentRuntimeApp()
        
        # No context in initial state
        assert app.context is None
        
        # Set context
        test_context = RequestContext(
            sandbox_id="test-sandbox",
            request_id="test-request"
        )
        AgentRuntimeContext.set_current_context(test_context)
        
        # Access context through application
        retrieved_context = app.context
        assert retrieved_context is not None
        assert retrieved_context.sandbox_id == "test-sandbox"
        assert retrieved_context.request_id == "test-request"
    
    @pytest.mark.unit
    def test_context_in_agent_function(self):
        """Test accessing context in Agent function"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        def context_aware_agent(request: dict) -> dict:
            # Access context in Agent function
            current_context = app.context
            return {
                "response": "context_aware",
                "has_context": current_context is not None,
                "sandbox_id": current_context.sandbox_id if current_context else None
            }
        
        # Set context and invoke
        test_context = RequestContext(sandbox_id="test-ctx")
        AgentRuntimeContext.set_current_context(test_context)
        
        result = context_aware_agent({"test": "data"})
        
        assert result["has_context"] is True
        assert result["sandbox_id"] == "test-ctx"


class TestAgentRuntimeAppServerManagement:
    """AgentRuntimeApp server management tests"""
    
    @pytest.mark.unit
    def test_lazy_server_creation(self):
        """Test lazy server creation"""
        app = AgentRuntimeApp()
        
        # No server in initial state
        assert app._server is None
        
        # Registering entrypoint doesn't create server
        @app.entrypoint
        def test_agent(request: dict) -> dict:
            return {"response": "test"}
        
        assert app._server is None
        
        # Registering middleware creates server
        @app.middleware
        async def test_middleware(request, call_next):
            return await call_next(request)
        
        assert app._server is not None
    
    @pytest.mark.unit
    @patch('novita_sandbox.agent_runtime.runtime.server.AgentRuntimeServer.run')
    def test_run_method_basic(self, mock_server_run):
        """Test basic run method"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        def test_agent(request: dict) -> dict:
            return {"response": "test"}
        
        # Test running
        app.run(port=8888, host="localhost")
        
        # Verify configuration update
        assert app.config.port == 8888
        assert app.config.host == "localhost"
        
        # Verify server is created and run
        assert app._server is not None
        mock_server_run.assert_called_once_with(8888, "localhost")
    
    @pytest.mark.unit
    def test_run_without_entrypoint_raises_error(self):
        """Test running without entrypoint raises error"""
        app = AgentRuntimeApp()
        
        with pytest.raises(RuntimeError) as exc_info:
            app.run()
        
        assert "No entrypoint function registered" in str(exc_info.value)


class TestAgentRuntimeAppErrorHandling:
    """AgentRuntimeApp error handling tests"""
    
    @pytest.mark.unit
    def test_agent_function_exceptions(self):
        """Test Agent function exception handling"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        def error_agent(request: dict) -> dict:
            if request.get("should_error"):
                raise ValueError("Test error from agent")
            return {"response": "success"}
        
        # Normal invocation
        result = error_agent({"data": "test"})
        assert result["response"] == "success"
        
        # Exception invocation
        with pytest.raises(ValueError, match="Test error from agent"):
            error_agent({"should_error": True})
    
    @pytest.mark.unit
    def test_decorator_function_preservation(self):
        """Test decorator preserves function attributes"""
        app = AgentRuntimeApp()
        
        @app.entrypoint
        def documented_agent(request: dict) -> dict:
            """This is a documented Agent function."""
            return {"response": "documented"}
        
        # Verify function attributes are preserved
        assert documented_agent.__name__ == "documented_agent"
        assert "This is a documented Agent function" in documented_agent.__doc__
        
        # Verify function can still be invoked normally
        result = documented_agent({"test": "input"})
        assert result["response"] == "documented"