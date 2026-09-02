"""
End-to-end integration tests

Tests the complete Agent application workflow, including real HTTP server startup, request handling, and response validation.
"""

import asyncio
import json
import threading
import time
import requests
import pytest
from typing import Generator, AsyncGenerator
from unittest.mock import patch

from novita_sandbox.agent_runtime.runtime.app import AgentRuntimeApp
from novita_sandbox.agent_runtime.runtime.context import RequestContext
from novita_sandbox.agent_runtime.runtime.models import RuntimeConfig


class TestEndToEndBasicFlow:
    """End-to-end basic flow tests"""
    
    def setup_method(self, method):
        """Setup before each test method"""
        # Assign different ports for each test method
        port_map = {
            "test_simple_agent_end_to_end": 8901,
            "test_agent_with_context_end_to_end": 8902,
            "test_custom_ping_end_to_end": 8903,
            "test_error_handling_end_to_end": 8904
        }
        self.test_port = port_map.get(method.__name__, 8905)
        self.base_url = f"http://localhost:{self.test_port}"
        self.server_thread = None
        self.app = None
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Clean up any servers that may still be running
        if self.server_thread and self.server_thread.is_alive():
            # Send stop signal (requires server to support graceful shutdown)
            pass
    
    def start_server_in_thread(self, app: AgentRuntimeApp):
        """Start server in separate thread"""
        def run_server():
            try:
                app.run(port=self.test_port, host="127.0.0.1")
            except Exception as e:
                print(f"Server error: {e}")
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Wait for server to start
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
    def test_simple_agent_end_to_end(self):
        """Test simple Agent end-to-end flow"""
        # Create application
        config = RuntimeConfig(debug=True)
        app = AgentRuntimeApp(config=config)
        
        # Register simple Agent function
        @app.entrypoint
        def simple_agent(request: dict) -> dict:
            # Get custom data from data field
            data = request.get('data', {})
            name = data.get('name', 'World')
            return {
                "response": f"Hello, {name}!",
                "timestamp": "2024-01-01T00:00:00Z",
                "processed": True
            }
        
        # Start server
        self.start_server_in_thread(app)
        
        # Send request (using correct InvocationRequest structure)
        request_data = {
            "data": {"name": "Alice"},
            "sandbox_id": "test-sandbox-e2e"
        }
        
        response = requests.post(
            f"{self.base_url}/invocations",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Verify response
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert "result" in data
        assert data["result"]["response"] == "Hello, Alice!"
        assert data["result"]["processed"] is True
        assert "duration" in data
    
    @pytest.mark.integration
    def test_agent_with_context_end_to_end(self):
        """Test Agent with context end-to-end flow"""
        config = RuntimeConfig(debug=True)
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def context_agent(request: dict, context: RequestContext) -> dict:
            return {
                "response": "Context processed",
                "sandbox_id": context.sandbox_id,
                "request_id": context.request_id,
                "user_agent": context.headers.get("user-agent", "unknown"),
                "input_data": request
            }
        
        self.start_server_in_thread(app)
        
        request_data = {
            "data": {"message": "test with context"},
            "sandbox_id": "context-test-sandbox"
        }
        
        response = requests.post(
            f"{self.base_url}/invocations",
            json=request_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "TestClient/1.0"
            }
        )
        
        assert response.status_code == 200
        
        data = response.json()
        result = data["result"]
        assert result["sandbox_id"] == "context-test-sandbox"
        assert result["user_agent"] == "TestClient/1.0"
        assert result["input_data"]["data"]["message"] == "test with context"
        assert "request_id" in result
    
    @pytest.mark.integration
    def test_custom_ping_end_to_end(self):
        """Test custom ping handler end-to-end flow"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def dummy_agent(request: dict) -> dict:
            return {"response": "dummy"}
        
        @app.ping
        def custom_ping() -> dict:
            return {
                "status": "Healthy",  # Use valid enum value
                "message": "e2e_test_agent v1.0.0 - custom_ping,context_support",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        
        self.start_server_in_thread(app)
        
        # Test custom ping
        response = requests.get(f"{self.base_url}/ping")
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "Healthy"
        assert "e2e_test_agent v1.0.0" in data["message"]
        assert "custom_ping" in data["message"]
        assert "context_support" in data["message"]
        assert data["timestamp"] == "2024-01-01T00:00:00Z"
    
    @pytest.mark.integration
    def test_error_handling_end_to_end(self):
        """Test error handling end-to-end flow"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def error_agent(request: dict) -> dict:
            data = request.get("data", {})
            if data.get("should_error"):
                raise ValueError("Intentional test error")
            return {"response": "success"}
        
        self.start_server_in_thread(app)
        
        # Test normal request (using correct data structure)
        normal_request = {
            "data": {"should_error": False}, 
            "sandbox_id": "test"
        }
        response = requests.post(f"{self.base_url}/invocations", json=normal_request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["result"]["response"] == "success"
        
        # Test error request
        error_request = {
            "data": {"should_error": True}, 
            "sandbox_id": "test"
        }
        response = requests.post(f"{self.base_url}/invocations", json=error_request)
        
        assert response.status_code == 500
        data = response.json()
        assert data["status"] == "error"
        assert "Intentional test error" in data["error"]
        assert "duration" in data


class TestEndToEndAsyncFlow:
    """End-to-end async flow tests"""
    
    def setup_method(self, method):
        """Setup before each test method"""
        # Assign different port range for async tests
        port_map = {
            "test_async_agent_end_to_end": 8910,
        }
        self.test_port = port_map.get(method.__name__, 8911)
        self.base_url = f"http://localhost:{self.test_port}"
        self.server_thread = None
    
    def teardown_method(self):
        """Cleanup"""
        pass
    
    def start_server_in_thread(self, app: AgentRuntimeApp):
        """Start server in separate thread"""
        def run_server():
            try:
                app.run(port=self.test_port, host="127.0.0.1")
            except Exception as e:
                print(f"Server error: {e}")
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Wait for server to start
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
    def test_async_agent_end_to_end(self):
        """Test async Agent end-to-end flow"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        async def async_agent(request: dict) -> dict:
            # Simulate async operation
            await asyncio.sleep(0.1)
            data = request.get('data', {})
            input_text = data.get('input', '')
            return {
                "response": f"Async processed: {input_text}",
                "async": True,
                "delay": 0.1
            }
        
        self.start_server_in_thread(app)
        
        request_data = {
            "data": {"input": "async test data"},
            "sandbox_id": "async-test"
        }
        
        start_time = time.time()
        response = requests.post(f"{self.base_url}/invocations", json=request_data)
        end_time = time.time()
        
        assert response.status_code == 200
        
        data = response.json()
        result = data["result"]
        assert result["response"] == "Async processed: async test data"
        assert result["async"] is True
        
        # Verify async delay exists
        assert end_time - start_time >= 0.1
