"""
Streaming Response Integration Tests

Tests end-to-end streaming response functionality, including handling of synchronous 
and asynchronous generators, Server-Sent Events (SSE) format validation, etc.

Note: As of the latest version, streaming behavior is automatically determined by the 
return type of the entrypoint function. If the function returns a generator or async 
generator, the response will be streamed via SSE regardless of the 'stream' field in 
the request (which is now deprecated).
"""

import asyncio
import json
import threading
import time
import requests
import pytest
from typing import Generator, AsyncGenerator

from novita_sandbox.agent_runtime.runtime.app import AgentRuntimeApp
from novita_sandbox.agent_runtime.runtime.context import RequestContext
from novita_sandbox.agent_runtime.runtime.models import RuntimeConfig


def assert_sse_response(response) -> None:
    """Assert response uses SSE streaming."""
    content_type = response.headers.get("content-type", "")
    assert content_type.startswith("text/event-stream")


class TestStreamingBasicFlow:
    """Streaming response basic flow tests"""
    
    def _parse_sse_events(self, response) -> list:
        """Parse Server-Sent Events response"""
        sse_events = []
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_content = line_str[6:]  # Remove "data: " prefix
                    try:
                        # Content is JSON encoded, needs to be decoded
                        event_data = json.loads(data_content)
                        sse_events.append(event_data)
                    except json.JSONDecodeError:
                        sse_events.append(data_content)
        return sse_events
    
    def setup_method(self, method):
        """Setup before each test method"""
        # Assign different ports for each test method
        port_map = {
            "test_sync_generator_streaming_e2e": 8920,
            "test_async_generator_streaming_e2e": 8921,
            "test_large_data_streaming_e2e": 8922,
            "test_streaming_with_context_e2e": 8923
        }
        self.test_port = port_map.get(method.__name__, 8924)
        self.base_url = f"http://localhost:{self.test_port}"
        self.server_thread = None
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Clean up any running servers
        if self.server_thread and self.server_thread.is_alive():
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
    def test_sync_generator_streaming_e2e(self):
        """Test end-to-end streaming response with synchronous generator"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def streaming_agent(request: dict) -> Generator[str, None, None]:
            data = request.get('data', {})
            prompt = data.get('prompt', 'test')
            count = data.get('count', 3)
            
            for i in range(count):
                yield f"Chunk {i+1}/{count}: Processing '{prompt}'"
                time.sleep(0.05)  # Simulate processing time
            yield f"Final: Completed processing '{prompt}'"
        
        self.start_server_in_thread(app)
        
        request_data = {
            "data": {"prompt": "streaming test", "count": 3},
            "sandbox_id": "streaming-test",
            "stream": True  # Enable streaming response
        }
        
        # Send streaming request
        start_time = time.time()
        response = requests.post(
            f"{self.base_url}/invocations",
            json=request_data,
            headers={"Content-Type": "application/json"},
            stream=True  # Enable streaming reception
        )
        end_time = time.time()
        
        assert response.status_code == 200
        assert_sse_response(response)
        
        # Verify streaming data (SSE format)
        sse_events = self._parse_sse_events(response)
        
        assert len(sse_events) == 4  # 3 processing chunks + 1 final chunk
        assert "Chunk 1/3: Processing 'streaming test'" in sse_events[0]
        assert "Chunk 2/3: Processing 'streaming test'" in sse_events[1]
        assert "Chunk 3/3: Processing 'streaming test'" in sse_events[2]
        assert "Final: Completed processing 'streaming test'" in sse_events[3]
        
        # Streaming response time assertion is relatively loose, as network transmission can be fast
        # Main verification is that chunked data was actually received
        assert len(sse_events) > 1  # Ensure it was transmitted in chunks
    
    @pytest.mark.integration
    def test_async_generator_streaming_e2e(self):
        """Test end-to-end streaming response with asynchronous generator"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        async def async_streaming_agent(request: dict) -> AsyncGenerator[str, None]:
            data = request.get('data', {})
            prompt = data.get('prompt', 'test')
            count = data.get('count', 3)
            
            for i in range(count):
                await asyncio.sleep(0.05)  # Async delay
                yield f"AsyncChunk {i+1}/{count}: '{prompt}' processed"
            yield f"AsyncFinal: All '{prompt}' processing complete"
        
        self.start_server_in_thread(app)
        
        request_data = {
            "data": {"prompt": "async streaming", "count": 3},
            "sandbox_id": "async-streaming-test",
            "stream": True
        }
        
        start_time = time.time()
        response = requests.post(
            f"{self.base_url}/invocations",
            json=request_data,
            headers={"Content-Type": "application/json"},
            stream=True
        )
        end_time = time.time()
        
        assert response.status_code == 200
        
        # Verify async streaming data (SSE format)
        sse_events = self._parse_sse_events(response)
        
        assert len(sse_events) == 4
        assert "AsyncChunk 1/3: 'async streaming' processed" in sse_events[0]
        assert "AsyncFinal: All 'async streaming' processing complete" in sse_events[3]
        
        # Ensure it was transmitted in chunks
        assert len(sse_events) > 1
    
    @pytest.mark.integration
    def test_large_data_streaming_e2e(self):
        """Test large data streaming transfer"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def large_data_agent(request: dict) -> Generator[str, None, None]:
            data = request.get('data', {})
            size = data.get('chunk_size', 1024)
            count = data.get('chunk_count', 5)
            
            for i in range(count):
                # Generate data chunks of specified size
                chunk_data = "x" * size
                yield f"Chunk_{i+1}_Size_{size}: {chunk_data}"
        
        self.start_server_in_thread(app)
        
        request_data = {
            "data": {"chunk_size": 512, "chunk_count": 5},
            "sandbox_id": "large-data-test",
            "stream": True
        }
        
        response = requests.post(
            f"{self.base_url}/invocations",
            json=request_data,
            stream=True
        )
        
        assert response.status_code == 200
        
        # Verify large data stream (SSE format)
        sse_events = self._parse_sse_events(response)
        
        assert len(sse_events) == 5
        # Verify data integrity
        for i, event_data in enumerate(sse_events):
            assert f"Chunk_{i+1}_Size_512" in event_data
            assert "x" * 512 in event_data
    
    @pytest.mark.integration
    def test_streaming_with_context_e2e(self):
        """Test streaming response with context"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def context_streaming_agent(request: dict, context: RequestContext) -> Generator[str, None, None]:
            data = request.get('data', {})
            message = data.get('message', 'test')
            
            # First chunk contains context information
            yield f"Context: sandbox_id={context.sandbox_id}, request_id={context.request_id}"
            
            # Processing data chunks
            for i in range(3):
                yield f"Processing_{i+1}: {message} in {context.sandbox_id}"
            
            # Final chunk
            yield f"Completed: {message} processing in {context.sandbox_id}"
        
        self.start_server_in_thread(app)
        
        request_data = {
            "data": {"message": "context streaming test"},
            "sandbox_id": "context-streaming-sandbox",
            "stream": True
        }
        
        response = requests.post(
            f"{self.base_url}/invocations",
            json=request_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "StreamingTestClient/1.0"
            },
            stream=True
        )
        
        assert response.status_code == 200
        
        sse_events = self._parse_sse_events(response)
        
        assert len(sse_events) == 5  # 1 context + 3 processing + 1 completion
        
        # Verify context information
        context_event = sse_events[0]
        assert "sandbox_id=context-streaming-sandbox" in context_event
        assert "request_id=" in context_event
        
        # Verify processing chunks
        for i in range(1, 4):
            processing_event = sse_events[i]
            assert f"Processing_{i}: context streaming test in context-streaming-sandbox" == processing_event
        
        # Verify completion chunk
        final_event = sse_events[4]
        assert "Completed: context streaming test processing in context-streaming-sandbox" == final_event


class TestStreamingErrorHandling:
    """Streaming response error handling tests"""
    
    def _parse_sse_events(self, response) -> list:
        """Parse Server-Sent Events response"""
        sse_events = []
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_content = line_str[6:]
                    try:
                        event_data = json.loads(data_content)
                        sse_events.append(event_data)
                    except json.JSONDecodeError:
                        sse_events.append(data_content)
        return sse_events
    
    def setup_method(self, method):
        """Setup"""
        port_map = {
            "test_streaming_error_handling_e2e": 8930,
            "test_streaming_interruption_e2e": 8931,
        }
        self.test_port = port_map.get(method.__name__, 8932)
        self.base_url = f"http://localhost:{self.test_port}"
        self.server_thread = None
    
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
    def test_streaming_error_handling_e2e(self):
        """Test error handling in streaming responses"""
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def error_streaming_agent(request: dict) -> Generator[str, None, None]:
            data = request.get('data', {})
            should_error = data.get('should_error', False)
            
            yield "Chunk 1: Starting processing"
            yield "Chunk 2: Processing continues"
            
            if should_error:
                raise ValueError("Error during streaming")
            
            yield "Chunk 3: Processing completed successfully"
        
        self.start_server_in_thread(app)
        
        # Test normal streaming processing
        normal_request = {
            "data": {"should_error": False},
            "sandbox_id": "normal-streaming",
            "stream": True
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=normal_request, stream=True)
        
        assert response.status_code == 200
        
        chunks = []
        for line in response.iter_lines():
            if line:
                chunks.append(line.decode('utf-8'))
        
        assert len(chunks) == 3
        assert "Chunk 1: Starting processing" in chunks[0]
        assert "Chunk 3: Processing completed successfully" in chunks[2]
        
        # Test error during streaming processing
        error_request = {
            "data": {"should_error": True},
            "sandbox_id": "error-streaming",
            "stream": True
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=error_request, stream=True)
        
        # Errors in streaming responses usually occur after transmission has started, so status code may still be 200
        # But should see partial data, then connection will be interrupted
        chunks = []
        try:
            for line in response.iter_lines():
                if line:
                    chunks.append(line.decode('utf-8'))
        except requests.exceptions.ChunkedEncodingError:
            # This is expected, because an error occurred during streaming
            pass
        
        # Should receive at least the first two chunks
        assert len(chunks) >= 2
        assert "Chunk 1: Starting processing" in chunks[0]
        assert "Chunk 2: Processing continues" in chunks[1]
    
    @pytest.mark.integration
    def test_generator_always_returns_streaming(self):
        """Test that generator functions always return streaming responses
        
        Note: The 'stream' field in request is now deprecated.
        Streaming behavior is automatically determined by the return type.
        If a function returns a generator, it will always stream via SSE.
        """
        config = RuntimeConfig()
        app = AgentRuntimeApp(config=config)
        
        @app.entrypoint
        def generator_agent(request: dict) -> Generator[str, None, None]:
            data = request.get('data', {})
            message = data.get('message', 'test')
            
            for i in range(3):
                yield f"Part {i+1}: {message}"
        
        self.start_server_in_thread(app)
        
        # Test with stream=False - should still return streaming because function returns generator
        request_without_stream = {
            "data": {"message": "test1"},
            "sandbox_id": "test1",
            "stream": False  # Ignored - streaming determined by return type
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=request_without_stream, stream=True)
        
        assert response.status_code == 200
        assert_sse_response(response)
        
        chunks = []
        for line in response.iter_lines():
            if line:
                chunks.append(line.decode('utf-8'))
        
        assert len(chunks) == 3
        assert "Part 1: test1" in chunks[0]
        assert "Part 2: test1" in chunks[1]
        assert "Part 3: test1" in chunks[2]
        
        # Test with stream=True - should also return streaming (same behavior)
        request_with_stream = {
            "data": {"message": "test2"},
            "sandbox_id": "test2",
            "stream": True  # Redundant - streaming determined by return type
        }
        
        response = requests.post(f"{self.base_url}/invocations", json=request_with_stream, stream=True)
        
        assert response.status_code == 200
        assert_sse_response(response)
        
        chunks = []
        for line in response.iter_lines():
            if line:
                chunks.append(line.decode('utf-8'))
        
        assert len(chunks) == 3
        assert "Part 1: test2" in chunks[0]
        assert "Part 2: test2" in chunks[1]
        assert "Part 3: test2" in chunks[2]
