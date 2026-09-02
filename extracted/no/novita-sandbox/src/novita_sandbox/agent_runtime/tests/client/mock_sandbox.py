"""
Mock Sandbox instance

Simulates Sandbox instance behavior for unit testing
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from unittest.mock import Mock, AsyncMock
from novita_sandbox.agent_runtime.client.models import SessionStatus


class MockSandbox:
    """Mock Sandbox instance"""
    
    def __init__(self, sandbox_id: str = "mock-sandbox-123"):
        self.id = sandbox_id
        self.sandbox_id = sandbox_id
        self.created_at = datetime.now()
        self.status = "running"
        self.template_id = "test-template-123"
        self.host = "mock-sandbox.novita.ai"
        self.port = 8080
        
        # Simulated state
        self._paused = False
        self._closed = False
        self._error = None
        
        # Operation history
        self.operation_history = []
    
    def get_host(self, port: int = 8080) -> str:
        """Get host address"""
        self._record_operation("get_host", {"port": port})
        if self._closed:
            raise Exception("Sandbox is closed")
        return f"{self.host}:{port}"
    
    async def pause(self):
        """Pause Sandbox"""
        self._record_operation("pause")
        if self._closed:
            raise Exception("Cannot pause closed sandbox")
        
        await asyncio.sleep(0.01)  # Simulate operation delay
        self._paused = True
        self.status = "paused"
    
    async def resume(self):
        """Resume Sandbox"""
        self._record_operation("resume")
        if self._closed:
            raise Exception("Cannot resume closed sandbox")
        
        await asyncio.sleep(0.01)  # Simulate operation delay
        self._paused = False
        self.status = "running"
    
    async def close(self):
        """Close Sandbox"""
        self._record_operation("close")
        await asyncio.sleep(0.01)  # Simulate operation delay
        self._closed = True
        self.status = "closed"
    
    async def kill(self):
        """Force terminate Sandbox"""
        self._record_operation("kill")
        await asyncio.sleep(0.01)  # Simulate operation delay
        self._closed = True
        self.status = "killed"
    
    def is_paused(self) -> bool:
        """Check if paused"""
        return self._paused
    
    def is_closed(self) -> bool:
        """Check if closed"""
        return self._closed
    
    def set_error(self, error: Exception):
        """Set error state"""
        self._error = error
        self.status = "error"
    
    def _record_operation(self, operation: str, params: Optional[Dict[str, Any]] = None):
        """Record operation history"""
        self.operation_history.append({
            "operation": operation,
            "timestamp": datetime.now(),
            "params": params or {}
        })
    
    def get_operation_count(self, operation: str) -> int:
        """Get call count for specific operation"""
        return sum(1 for op in self.operation_history if op["operation"] == operation)
    
    def clear_history(self):
        """Clear operation history"""
        self.operation_history = []


class MockAsyncSandbox(MockSandbox):
    """Async Mock Sandbox - corresponds to novita_sandbox.core.AsyncSandbox"""
    
    def __init__(self, template_id: str = "test-template-123", **kwargs):
        # Generate unique sandbox_id to avoid ID conflicts in concurrent tests
        import uuid
        unique_id = f"mock-sandbox-{str(uuid.uuid4())[:8]}"
        super().__init__(sandbox_id=unique_id)
        self.template_id = template_id
        self.api_key = kwargs.get("api_key", "test-api-key")
        self.timeout = kwargs.get("timeout", 300)
        self.memory_mb = kwargs.get("memory_mb", 1024)
        self.cpu_count = kwargs.get("cpu_count", 1)
        
        # Startup state
        self._started = False
    
    async def start(self):
        """Start Sandbox"""
        self._record_operation("start")
        if self._closed:
            raise Exception("Cannot start closed sandbox")
        
        await asyncio.sleep(0.05)  # Simulate startup delay
        self._started = True
        self.status = "running"
    
    async def stop(self):
        """Stop Sandbox"""
        self._record_operation("stop")
        await asyncio.sleep(0.02)  # Simulate stop delay
        self._started = False
        self.status = "stopped"
    
    def is_started(self) -> bool:
        """Check if started"""
        return self._started


class MockSandboxFactory:
    """Mock Sandbox factory"""
    
    def __init__(self):
        self.created_sandboxes = []
        self.creation_delay = 0.1
        self.creation_error = None
    
    async def create_sandbox(self, template_id: str, **kwargs) -> MockAsyncSandbox:
        """Create Sandbox instance"""
        if self.creation_error:
            raise self.creation_error
        
        await asyncio.sleep(self.creation_delay)
        
        sandbox = MockAsyncSandbox(template_id=template_id, **kwargs)
        await sandbox.start()
        
        self.created_sandboxes.append(sandbox)
        return sandbox
    
    def set_creation_delay(self, delay: float):
        """Set creation delay"""
        self.creation_delay = delay
    
    def set_creation_error(self, error: Exception):
        """Set creation error"""
        self.creation_error = error
    
    def get_sandbox_count(self) -> int:
        """Get count of created Sandboxes"""
        return len(self.created_sandboxes)
    
    def get_active_sandboxes(self) -> list:
        """Get active Sandboxes"""
        return [s for s in self.created_sandboxes if not s.is_closed()]
    
    def close_all_sandboxes(self):
        """Close all Sandboxes"""
        async def _close_all():
            for sandbox in self.created_sandboxes:
                if not sandbox.is_closed():
                    await sandbox.close()
        
        return _close_all()


# =============================================================================
# Predefined Mock instances
# =============================================================================

def create_healthy_sandbox(sandbox_id: str = "healthy-sandbox") -> MockSandbox:
    """Create healthy Sandbox"""
    sandbox = MockSandbox(sandbox_id)
    sandbox.status = "running"
    return sandbox


def create_paused_sandbox(sandbox_id: str = "paused-sandbox") -> MockSandbox:
    """Create paused Sandbox"""
    sandbox = MockSandbox(sandbox_id)
    sandbox._paused = True
    sandbox.status = "paused"
    return sandbox


def create_error_sandbox(sandbox_id: str = "error-sandbox") -> MockSandbox:
    """Create Sandbox in error state"""
    sandbox = MockSandbox(sandbox_id)
    sandbox.set_error(Exception("Simulated sandbox error"))
    return sandbox


def create_slow_sandbox(sandbox_id: str = "slow-sandbox", delay: float = 1.0) -> MockSandbox:
    """Create slow-responding Sandbox"""
    sandbox = MockSandbox(sandbox_id)
    
    # Override async methods to add delay
    original_pause = sandbox.pause
    original_resume = sandbox.resume
    original_close = sandbox.close
    
    async def slow_pause():
        await asyncio.sleep(delay)
        return await original_pause()
    
    async def slow_resume():
        await asyncio.sleep(delay)
        return await original_resume()
    
    async def slow_close():
        await asyncio.sleep(delay)
        return await original_close()
    
    sandbox.pause = slow_pause
    sandbox.resume = slow_resume
    sandbox.close = slow_close
    
    return sandbox


# =============================================================================
# Test utility functions
# =============================================================================

def assert_sandbox_state(sandbox: MockSandbox, expected_status: str):
    """Assert Sandbox state"""
    assert sandbox.status == expected_status


def assert_operation_called(sandbox: MockSandbox, operation: str, times: int = 1):
    """Assert operation was called specified number of times"""
    actual_times = sandbox.get_operation_count(operation)
    assert actual_times == times, f"Expected {operation} to be called {times} times, but was called {actual_times} times"


def assert_sandbox_not_closed(sandbox: MockSandbox):
    """Assert Sandbox is not closed"""
    assert not sandbox.is_closed(), "Sandbox should not be closed"


def assert_sandbox_closed(sandbox: MockSandbox):
    """Assert Sandbox is closed"""
    assert sandbox.is_closed(), "Sandbox should be closed"
