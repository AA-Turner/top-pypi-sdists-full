"""
Context Management Unit Tests

Tests the functionality of RequestContext and AgentRuntimeContext.
"""

import pytest
import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from novita_sandbox.agent_runtime.runtime.context import (
    RequestContext,
    AgentRuntimeContext,
)


class TestRequestContext:
    """RequestContext model tests"""
    
    @pytest.mark.unit
    def test_basic_context_creation(self):
        """Test basic context creation"""
        context = RequestContext(
            sandbox_id="sandbox-123",
            request_id="req-456",
            headers={"Content-Type": "application/json", "User-Agent": "test"}
        )
        
        assert context.sandbox_id == "sandbox-123"
        assert context.request_id == "req-456"
        assert context.headers["Content-Type"] == "application/json"
        assert context.headers["User-Agent"] == "test"
    
    @pytest.mark.unit
    def test_minimal_context(self):
        """Test minimal context"""
        context = RequestContext()
        
        assert context.sandbox_id is None
        assert context.request_id is None
        assert context.headers == {}
    
    @pytest.mark.unit
    def test_backward_compatibility_session_id(self):
        """Test backward compatible session_id attribute"""
        context = RequestContext(sandbox_id="sandbox-123")
        
        # session_id should equal sandbox_id
        assert context.session_id == "sandbox-123"
        assert context.session_id == context.sandbox_id
        
        # Test None value
        context = RequestContext()
        assert context.session_id is None
    
    @pytest.mark.unit
    def test_extra_fields_allowed(self):
        """Test handling of extra fields (Pydantic extra="allow")"""
        context = RequestContext(
            sandbox_id="test",
            request_id="req-123",
            custom_field="custom_value",
            another_field={"nested": "data"}
        )
        
        assert context.sandbox_id == "test"
        assert context.request_id == "req-123"
        # Extra fields should be saved
        assert hasattr(context, 'custom_field')
        assert hasattr(context, 'another_field')
    
    @pytest.mark.unit
    def test_context_modification(self):
        """Test context modification"""
        context = RequestContext(sandbox_id="original")
        
        # Modify existing field
        context.sandbox_id = "modified"
        assert context.sandbox_id == "modified"
        assert context.session_id == "modified"  # Ensure backward compatible attribute is also updated
        
        # Add new headers
        context.headers["Authorization"] = "Bearer token"
        assert context.headers["Authorization"] == "Bearer token"


class TestAgentRuntimeContext:
    """AgentRuntimeContext manager tests"""
    
    def setup_method(self):
        """Setup before each test method"""
        # Ensure context is cleared at the start
        AgentRuntimeContext.clear_current_context()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Ensure context is cleaned up after tests
        AgentRuntimeContext.clear_current_context()
    
    @pytest.mark.unit
    def test_set_and_get_context(self):
        """Test setting and getting context"""
        # Initial state should have no context
        assert AgentRuntimeContext.get_current_context() is None
        
        # Create and set context
        context = RequestContext(
            sandbox_id="test-sandbox",
            request_id="test-request",
            headers={"Content-Type": "application/json"}
        )
        
        AgentRuntimeContext.set_current_context(context)
        
        # Getting context should return the same object
        retrieved_context = AgentRuntimeContext.get_current_context()
        assert retrieved_context is not None
        assert retrieved_context.sandbox_id == "test-sandbox"
        assert retrieved_context.request_id == "test-request"
        assert retrieved_context.headers["Content-Type"] == "application/json"
    
    @pytest.mark.unit
    def test_clear_context(self):
        """Test clearing context"""
        # Set context
        context = RequestContext(sandbox_id="test")
        AgentRuntimeContext.set_current_context(context)
        
        # Confirm context is set
        assert AgentRuntimeContext.get_current_context() is not None
        
        # Clear context
        AgentRuntimeContext.clear_current_context()
        
        # Confirm context is cleared
        assert AgentRuntimeContext.get_current_context() is None
    
    @pytest.mark.unit
    def test_context_override(self):
        """Test context override"""
        # Set first context
        context1 = RequestContext(sandbox_id="sandbox-1")
        AgentRuntimeContext.set_current_context(context1)
        
        assert AgentRuntimeContext.get_current_context().sandbox_id == "sandbox-1"
        
        # Set second context (overriding the first)
        context2 = RequestContext(sandbox_id="sandbox-2")
        AgentRuntimeContext.set_current_context(context2)
        
        assert AgentRuntimeContext.get_current_context().sandbox_id == "sandbox-2"
    
    @pytest.mark.unit
    def test_thread_isolation(self):
        """Test thread isolation"""
        results = {}
        
        def worker_thread(thread_id: int):
            """Worker thread function"""
            # Each thread sets its own context
            context = RequestContext(sandbox_id=f"sandbox-{thread_id}")
            AgentRuntimeContext.set_current_context(context)
            
            # Brief wait to let other threads also set context
            time.sleep(0.1)
            
            # Get context, should be the one it set
            retrieved_context = AgentRuntimeContext.get_current_context()
            results[thread_id] = retrieved_context.sandbox_id if retrieved_context else None
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify each thread has its own context
        for i in range(5):
            assert results[i] == f"sandbox-{i}"
        
        # Main thread should have no context (or its own context)
        main_context = AgentRuntimeContext.get_current_context()
        assert main_context is None  # Main thread has not set context
    
    @pytest.mark.unit
    def test_async_context_isolation(self):
        """Test async task context isolation"""
        async def async_worker(task_id: int) -> Optional[str]:
            """Async worker function"""
            # Each task sets its own context
            context = RequestContext(sandbox_id=f"async-sandbox-{task_id}")
            AgentRuntimeContext.set_current_context(context)
            
            # Async wait to give other tasks a chance to run
            await asyncio.sleep(0.1)
            
            # Get context, should be the one it set
            retrieved_context = AgentRuntimeContext.get_current_context()
            return retrieved_context.sandbox_id if retrieved_context else None
        
        async def test_async_isolation():
            # Run multiple async tasks concurrently
            tasks = [async_worker(i) for i in range(5)]
            results = await asyncio.gather(*tasks)
            
            # Verify each task has its own context
            for i, result in enumerate(results):
                assert result == f"async-sandbox-{i}"
        
        # Run async test
        asyncio.run(test_async_isolation())
    
    @pytest.mark.unit
    def test_nested_context_operations(self):
        """Test nested context operations"""
        # Set outer context
        outer_context = RequestContext(sandbox_id="outer")
        AgentRuntimeContext.set_current_context(outer_context)
        
        assert AgentRuntimeContext.get_current_context().sandbox_id == "outer"
        
        # Set inner context
        inner_context = RequestContext(sandbox_id="inner")
        AgentRuntimeContext.set_current_context(inner_context)
        
        assert AgentRuntimeContext.get_current_context().sandbox_id == "inner"
        
        # Clear context
        AgentRuntimeContext.clear_current_context()
        
        # Should be completely cleared, not returned to outer context
        assert AgentRuntimeContext.get_current_context() is None
    
    @pytest.mark.unit
    def test_context_with_executor(self):
        """Test context behavior in thread pool executor"""
        def worker_with_context(sandbox_id: str) -> Optional[str]:
            """Worker function executed in thread pool"""
            context = RequestContext(sandbox_id=sandbox_id)
            AgentRuntimeContext.set_current_context(context)
            
            # Simulate some work
            time.sleep(0.05)
            
            retrieved_context = AgentRuntimeContext.get_current_context()
            return retrieved_context.sandbox_id if retrieved_context else None
        
        # Use thread pool executor
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(worker_with_context, f"pool-sandbox-{i}")
                for i in range(5)
            ]
            
            results = [future.result() for future in futures]
        
        # Verify results
        for i, result in enumerate(results):
            assert result == f"pool-sandbox-{i}"
    
    @pytest.mark.unit
    def test_context_persistence_across_calls(self):
        """Test context persistence across multiple calls"""
        context = RequestContext(
            sandbox_id="persistent-sandbox",
            request_id="persistent-request"
        )
        
        AgentRuntimeContext.set_current_context(context)
        
        # Get context multiple times, should remain consistent
        for _ in range(10):
            retrieved_context = AgentRuntimeContext.get_current_context()
            assert retrieved_context is not None
            assert retrieved_context.sandbox_id == "persistent-sandbox"
            assert retrieved_context.request_id == "persistent-request"
        
        # Modify an attribute of the context
        retrieved_context = AgentRuntimeContext.get_current_context()
        retrieved_context.headers["Modified"] = "true"
        
        # Get again, modification should be retained
        final_context = AgentRuntimeContext.get_current_context()
        assert final_context.headers["Modified"] == "true"


class TestContextIntegration:
    """Context integration tests"""
    
    def teardown_method(self):
        """Clean up context after tests"""
        AgentRuntimeContext.clear_current_context()
    
    @pytest.mark.unit
    def test_context_in_function_calls(self):
        """Test context passing in function calls"""
        def process_request() -> Optional[str]:
            """Function simulating request processing"""
            context = AgentRuntimeContext.get_current_context()
            return context.sandbox_id if context else None
        
        def handle_request(sandbox_id: str) -> Optional[str]:
            """Main function simulating request handling"""
            context = RequestContext(sandbox_id=sandbox_id)
            AgentRuntimeContext.set_current_context(context)
            
            # Call other functions, they should be able to access the same context
            return process_request()
        
        # Test context passing in function call chain
        result = handle_request("test-sandbox")
        assert result == "test-sandbox"
    
    @pytest.mark.unit
    def test_context_error_handling(self):
        """Test context behavior during exception handling"""
        def function_that_raises():
            """Function that raises an exception"""
            context = AgentRuntimeContext.get_current_context()
            assert context is not None
            assert context.sandbox_id == "error-test"
            raise ValueError("Test error")
        
        context = RequestContext(sandbox_id="error-test")
        AgentRuntimeContext.set_current_context(context)
        
        # Even if function raises exception, context should remain unchanged
        with pytest.raises(ValueError):
            function_that_raises()
        
        # Context should still exist
        remaining_context = AgentRuntimeContext.get_current_context()
        assert remaining_context is not None
        assert remaining_context.sandbox_id == "error-test"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_async_context_propagation(self):
        """Test context propagation in async functions"""
        async def async_processor() -> Optional[str]:
            """Async processing function"""
            # Simulate async operation
            await asyncio.sleep(0.01)
            
            context = AgentRuntimeContext.get_current_context()
            return context.sandbox_id if context else None
        
        async def async_handler(sandbox_id: str) -> Optional[str]:
            """Async handler main function"""
            context = RequestContext(sandbox_id=sandbox_id)
            AgentRuntimeContext.set_current_context(context)
            
            # Call other async functions
            return await async_processor()
        
        # Test context propagation in async function chain
        result = await async_handler("async-test")
        assert result == "async-test"