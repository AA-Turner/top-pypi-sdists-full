"""
Error handling integration tests

Tests error handling at all levels, error response format standardization, exception propagation and transformation.
"""

import asyncio
import json
import threading
import time
import requests
import pytest
from typing import Generator

from novita_sandbox.agent_runtime.runtime.app import AgentRuntimeApp
from novita_sandbox.agent_runtime.runtime.context import RequestContext
from novita_sandbox.agent_runtime.runtime.models import RuntimeConfig


class TestErrorHandlingBasicFlow:
    """Error handling basic flow tests"""
    
    def setup_method(self, method):
        """Setup before each test method"""
        port_map = {
            "test_agent_function_exceptions": 8970,
            "test_server_layer_error_handling": 8971,
            "test_async_agent_exceptions": 8972
        }
        self.test_port = port_map.get(method.__name__, 8973)
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
    def test_agent_function_exceptions(self):
        """Test Agent function exception handling"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def error_agent(request: dict) -> dict:
            data = request.get("data", {})
            error_type = data.get("error_type")
            
            if error_type == "value_error":
                raise ValueError("Invalid input value")
            elif error_type == "type_error":
                raise TypeError("Wrong type provided")
            elif error_type == "runtime_error":
                raise RuntimeError("Runtime processing error")
            
            return {"response": "success", "input": data}
        
        self.start_server_in_thread(app)
        
        # Test different types of exceptions
        error_cases = [
            ("value_error", "Invalid input value"),
            ("type_error", "Wrong type provided"),
            ("runtime_error", "Runtime processing error")
        ]
        
        for error_type, expected_message in error_cases:
            error_request = {
                "data": {"error_type": error_type},
                "sandbox_id": f"error-test-{error_type}"
            }
            
            response = requests.post(f"{self.base_url}/invocations", json=error_request)
            
            assert response.status_code == 500
            assert response.headers["content-type"] == "application/json"
            
            data = response.json()
            assert data["status"] == "error"
            assert expected_message in data["error"]
            assert "duration" in data  # Error response should also include execution time
