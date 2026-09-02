"""
Middleware Integration Tests

Tests the cooperation of multiple middlewares, execution order, exception propagation, and interaction with Agent functions.
"""

import asyncio
import json
import threading
import time
import requests
import pytest
from typing import Callable
from unittest.mock import Mock

from novita_sandbox.agent_runtime.runtime.app import AgentRuntimeApp
from novita_sandbox.agent_runtime.runtime.context import RequestContext
from novita_sandbox.agent_runtime.runtime.models import RuntimeConfig


class TestMiddlewareBasicFlow:
    """Middleware basic flow tests"""
    
    def setup_method(self, method):
        """Setup before each test method"""
        port_map = {
            "test_single_middleware_e2e": 8940,
            "test_multiple_middleware_execution_order": 8941,
            "test_middleware_response_modification": 8942
        }
        self.test_port = port_map.get(method.__name__, 8944)
        self.base_url = f"http://localhost:{self.test_port}"
        self.server_thread = None
        self.execution_log = []  # Used to record execution order
    
    def teardown_method(self):
        """Cleanup"""
        pass
    
    def start_server_in_thread(self, app: AgentRuntimeApp):
        """Start server in a separate thread"""
        def run_server():
            try:
                app.run(port=self.test_port, host="127.0.0.1")
            except Exception as e:
                print(f"Server error: {e}")
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        self._wait_for_server_ready()
    
    def _wait_for_server_ready(self, timeout=5):
        """Wait for server to be ready"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.base_url}/ping", timeout=1)
                if response.status_code == 200:
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(0.1)
        raise TimeoutError("Server did not start within timeout")
    
    @pytest.mark.integration
    def test_single_middleware_e2e(self):
        """Test single middleware end-to-end functionality"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def test_agent(request: dict) -> dict:
            return {"response": "agent processed", "input": request}
        
        @app.middleware
        async def logging_middleware(request, call_next):
            # Log request
            start_time = time.time()
            response = await call_next(request)
            end_time = time.time()
            
            # Modify response headers
            response.headers["X-Processing-Time"] = str(end_time - start_time)
            response.headers["X-Middleware"] = "logging"
            return response
        
        self.start_server_in_thread(app)
        
        request_data = {
            "data": {"message": "middleware test"},
            "sandbox_id": "middleware-test"
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=request_data)
        
        assert response.status_code == 200
        
        # Verify headers added by middleware
        assert "X-Processing-Time" in response.headers
        assert response.headers["X-Middleware"] == "logging"
        
        # Verify response content
        data = response.json()
        assert data["status"] == "success"
        
        # Agent function returns dictionary, should be directly available as dictionary
        result = data["result"]
        assert result["response"] == "agent processed"
    
    @pytest.mark.integration
    def test_multiple_middleware_execution_order(self):
        """Test multiple middleware execution order"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def test_agent(request: dict) -> dict:
            self.execution_log.append("agent_execution")
            return {"response": "processed"}
        
        @app.middleware
        async def middleware_1(request, call_next):
            self.execution_log.append("middleware_1_start")
            response = await call_next(request)
            self.execution_log.append("middleware_1_end")
            response.headers["X-Middleware-1"] = "executed"
            return response
        
        @app.middleware
        async def middleware_2(request, call_next):
            self.execution_log.append("middleware_2_start")
            response = await call_next(request)
            self.execution_log.append("middleware_2_end")
            response.headers["X-Middleware-2"] = "executed"
            return response
        
        @app.middleware
        async def middleware_3(request, call_next):
            self.execution_log.append("middleware_3_start")
            response = await call_next(request)
            self.execution_log.append("middleware_3_end")
            response.headers["X-Middleware-3"] = "executed"
            return response
        
        self.start_server_in_thread(app)
        
        request_data = {
            "data": {"message": "order test"},
            "sandbox_id": "order-test"
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=request_data)
        
        assert response.status_code == 200
        
        # Verify execution order: middleware executes in registration order
        expected_order = [
            "middleware_1_start", "middleware_2_start", "middleware_3_start",
            "agent_execution",
            "middleware_3_end", "middleware_2_end", "middleware_1_end"
        ]
        assert self.execution_log == expected_order
        
        # Verify all middleware were executed
        assert response.headers["X-Middleware-1"] == "executed"
        assert response.headers["X-Middleware-2"] == "executed"
        assert response.headers["X-Middleware-3"] == "executed"
    
    @pytest.mark.integration
    def test_middleware_response_modification(self):
        """Test middleware modifying response"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def test_agent(request: dict) -> dict:
            return {"response": "original", "agent": "processed"}
        
        @app.middleware
        async def response_modifier_middleware(request, call_next):
            response = await call_next(request)
            
            # Add custom response headers
            response.headers["X-Response-Modified"] = "true"
            response.headers["X-Middleware-Version"] = "1.0"
            response.headers["X-Processing-Node"] = "middleware-node-1"
            
            return response
        
        self.start_server_in_thread(app)
        
        request_data = {
            "data": {"test": "response modification"},
            "sandbox_id": "response-mod-test"
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=request_data)
        
        assert response.status_code == 200
        
        # Verify response headers added by middleware
        assert response.headers["X-Response-Modified"] == "true"
        assert response.headers["X-Middleware-Version"] == "1.0"
        assert response.headers["X-Processing-Node"] == "middleware-node-1"
        
        # Verify original response content is not corrupted
        data = response.json()
        result = data["result"]
        assert result["response"] == "original"
        assert result["agent"] == "processed"


class TestMiddlewareErrorHandling:
    """Middleware error handling tests"""
    
    def setup_method(self, method):
        """Setup"""
        port_map = {
            "test_middleware_exception_handling": 8950,
            "test_agent_error_through_middleware": 8951
        }
        self.test_port = port_map.get(method.__name__, 8952)
        self.base_url = f"http://localhost:{self.test_port}"
        self.server_thread = None
        self.error_log = []
    
    def teardown_method(self):
        """Cleanup"""
        pass
    
    def start_server_in_thread(self, app: AgentRuntimeApp):
        """Start server"""
        def run_server():
            try:
                app.run(port=self.test_port, host="127.0.0.1")
            except Exception as e:
                print(f"Server error: {e}")
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        self._wait_for_server_ready()
    
    def _wait_for_server_ready(self, timeout=5):
        """Wait for server to be ready"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.base_url}/ping", timeout=1)
                if response.status_code == 200:
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(0.1)
        raise TimeoutError("Server did not start within timeout")
    
    @pytest.mark.integration
    def test_middleware_exception_handling(self):
        """Test middleware exception handling"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def test_agent(request: dict) -> dict:
            return {"response": "should not reach here"}
        
        @app.middleware
        async def error_middleware(request, call_next):
            data = await request.json()
            if data.get("data", {}).get("should_error", False):
                raise ValueError("Middleware error")
            return await call_next(request)
        
        self.start_server_in_thread(app)
        
        # Test normal request
        normal_request = {
            "data": {"should_error": False},
            "sandbox_id": "normal-test"
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=normal_request)
        assert response.status_code == 200
        
        # Test middleware error
        error_request = {
            "data": {"should_error": True},
            "sandbox_id": "error-test"
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=error_request)
        assert response.status_code == 500
        
        data = response.json()
        assert data["status"] == "error"
        assert "Middleware error" in data["error"]
    
    @pytest.mark.integration
    def test_agent_error_through_middleware(self):
        """Test Agent error propagation through middleware"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def error_agent(request: dict) -> dict:
            data = request.get("data", {})
            if data.get("agent_error", False):
                raise ValueError("Agent processing error")
            return {"response": "success"}
        
        @app.middleware
        async def error_catching_middleware(request, call_next):
            try:
                response = await call_next(request)
                response.headers["X-Agent-Status"] = "success"
                return response
            except Exception as e:
                self.error_log.append(f"Caught agent error: {str(e)}")
                # Re-raise exception for framework to handle
                raise
        
        self.start_server_in_thread(app)
        
        # Test Agent error
        error_request = {
            "data": {"agent_error": True},
            "sandbox_id": "agent-error-test"
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=error_request)
        assert response.status_code == 500
        
        data = response.json()
        assert data["status"] == "error"
        assert "Agent processing error" in data["error"]
        
        # Verify middleware caught the error
        assert any("Caught agent error" in log for log in self.error_log)