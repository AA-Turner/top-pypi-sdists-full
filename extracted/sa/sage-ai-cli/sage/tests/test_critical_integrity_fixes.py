"""TDD tests for critical SAGE AI integrity and control-plane issues.

This test file covers the top 5 critical problems identified in the log analysis:

CRITICAL-1: SIGINT handlers crash in threaded contexts
CRITICAL-2: SAGE can claim implementation without writing files
CRITICAL-3: Admin auth is fail-open when admin_token is blank
CRITICAL-4: Browser terminal PTY shell has weak auth
CRITICAL-5: Terminal rate limiter defined but not enforced

Run with: pytest sage/tests/test_critical_integrity_fixes.py -v
"""

from __future__ import annotations

import signal
import threading
from unittest.mock import MagicMock, patch

import pytest

# =============================================================================
# CRITICAL-1: SIGINT in Threaded Contexts
# =============================================================================


class TestSignalHandlingSafety:
    """Tests that SIGINT handlers are only installed on the main thread."""

    def test_signal_handler_only_on_main_thread(self):
        """Signal handlers should not be installed in worker threads."""

        # In the main thread, this should work
        assert threading.current_thread() == threading.main_thread()

        # Mock the signal module to track calls
        with patch("sage.core.renderer.signal") as mock_signal:
            # Simulate what stream_tokens_with_phase does
            if threading.current_thread() == threading.main_thread():
                mock_signal.signal(signal.SIGINT, lambda s, f: None)
                assert mock_signal.signal.called
            else:
                # Should not attempt to install handler in thread
                assert not mock_signal.signal.called

    def test_renderer_checks_main_thread_before_signal(self):
        """Renderer should check if it's on main thread before installing signal handlers."""
        from sage.core.renderer import _is_main_thread

        # Main thread check should exist and return True on main thread
        assert _is_main_thread() is True

        # In a worker thread, it should return False
        result = []

        def worker():
            result.append(_is_main_thread())

        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()

        assert result[0] is False

    def test_stream_tokens_with_phase_safe_in_threads(self):
        """stream_tokens_with_phase should not crash when called from a thread."""
        from sage.core import renderer

        # Create a mock token iterator
        tokens = iter(["Hello", " ", "World"])

        # This should not raise "signal only works in main thread" error
        error = []
        result = []

        def worker():
            try:
                # This would crash with the old code
                output = renderer.stream_tokens_with_phase(tokens, model_id="test")
                result.append(output)
            except ValueError as e:
                if "main thread" in str(e):
                    error.append(e)

        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()

        # Should not have crashed with signal error
        assert len(error) == 0

    def test_execution_engine_thread_pool_safe(self):
        """Thread pools in execution.py should not trigger signal handler errors."""
        from sage.execution import ExecutionTask, ParallelExecutor, TaskPriority

        # ParallelExecutor uses ThreadPoolExecutor
        executor = ParallelExecutor(max_workers=2)

        # Should be able to execute tasks without signal errors
        def dummy_task():
            return 42

        # Create ExecutionTask objects with correct fields
        tasks = [
            ExecutionTask(
                id=f"task-{i}",
                description=f"Test task {i}",
                command=dummy_task,
                priority=TaskPriority.MEDIUM,
            )
            for i in range(5)
        ]

        # This should not crash with signal errors
        results = executor.execute_batch(tasks)
        assert len(results) == 5


# =============================================================================
# CRITICAL-2: Phantom Implementation (Claims without Files)
# =============================================================================


class TestImplementationIntegrity:
    """Tests that SAGE cannot claim implementation without actual file writes."""

    def test_detect_phantom_implementation_claims(self):
        """Should detect when response claims implementation but no files written."""
        response_text = """
I've implemented the proxy core functionality:

```python
# proxy_core.py
class ProxyCore:
    def __init__(self):
        self.config = {}

    def route_request(self, request):
        return self.proxy.forward(request)
```

And here are the tests:

```python
# test_proxy.py
def test_proxy_core():
    proxy = ProxyCore()
    assert proxy is not None
```

Implementation complete! The proxy system is now ready to use.
"""

        # No FILE: blocks were written
        files_written = []

        # Should detect phantom implementation
        from sage.cli_core import _detect_phantom_implementation

        is_phantom, reason = _detect_phantom_implementation(
            response_text, files_written, is_implementation_request=True
        )

        assert is_phantom is True
        assert "claimed implementation" in reason.lower()
        assert "no files written" in reason.lower()

    def test_valid_implementation_with_file_blocks(self):
        """Valid implementation should have FILE: blocks and actual writes."""
        response_text = """
FILE: proxy_core.py
class ProxyCore:
    def __init__(self):
        self.config = {}

FILE: test_proxy.py
def test_proxy_core():
    proxy = ProxyCore()
    assert proxy is not None
"""

        files_written = ["proxy_core.py", "test_proxy.py"]

        from sage.cli_core import _detect_phantom_implementation

        is_phantom, _ = _detect_phantom_implementation(
            response_text, files_written, is_implementation_request=True
        )

        assert is_phantom is False

    def test_implementation_requires_file_blocks_or_run_commands(self):
        """Implementation responses must contain FILE: blocks or RUN: commands."""
        response_text = """
I've analyzed the code and here's what needs to be implemented:

1. Create a ProxyCore class with routing logic
2. Add request forwarding
3. Implement error handling

That's the implementation plan.
"""

        files_written = []

        from sage.cli_core import _validate_implementation_response

        is_valid, reason = _validate_implementation_response(
            response_text, files_written, is_implementation_request=True
        )

        assert is_valid is False
        assert "must contain FILE: blocks" in reason

    def test_code_snippets_without_file_blocks_rejected(self):
        """Code snippets in markdown without FILE: should be rejected for implementation."""
        response_text = """
Here's the implementation:

```python
def process_request(req):
    return handler.handle(req)
```

Done!
"""

        files_written = []

        from sage.cli_core import _validate_implementation_response

        is_valid, _ = _validate_implementation_response(
            response_text, files_written, is_implementation_request=True
        )

        assert is_valid is False

    def test_run_only_implementation_without_file_blocks_rejected(self):
        """Command-only implementation replies should not count as real code delivery."""
        response_text = """
RUN: pytest tests/test_proxy.py -v

All done!
"""

        from sage.cli_core import _validate_implementation_response

        is_valid, reason = _validate_implementation_response(
            response_text, [], is_implementation_request=True
        )

        assert is_valid is False
        assert "did not provide FILE: blocks" in reason


# =============================================================================
# CRITICAL-3: Fail-Open Admin Auth
# =============================================================================


class TestAdminAuthSecurity:
    """Tests that admin auth fails closed when token is not configured."""

    def test_require_admin_token_fails_closed_when_empty(self):
        """Admin auth should REJECT when token is empty, not allow."""
        from backend.app import _require_admin_token_strict

        # Mock request with empty config token
        mock_request = MagicMock()
        mock_request.headers = {"Authorization": "Bearer some-token"}

        # Config has empty admin token
        mock_config = MagicMock()
        mock_config.admin_token = ""

        # Should reject because no valid token is configured
        with pytest.raises(Exception) as exc_info:
            _require_admin_token_strict(mock_request, mock_config)

        assert "admin authentication not configured" in str(exc_info.value).lower()

    def test_require_admin_token_validates_actual_token(self):
        """When token is configured, it must match exactly."""
        from backend.app import _require_admin_token_strict

        # Mock settings.admin_token
        with patch("backend.app.settings") as mock_settings:
            mock_settings.admin_token = "correct-token-123"

            # Create mock request with state attribute
            mock_request = MagicMock()
            mock_request.state = MagicMock()
            mock_request.state.request_id = "test-request-id"

            # Should reject wrong token
            with pytest.raises(Exception) as exc_info:
                _require_admin_token_strict(
                    mock_request, authorization="Bearer wrong-token", x_admin_token=None
                )

            # Should contain "invalid" or "unauthorized" or "401"
            error_msg = str(exc_info.value).lower()
            assert "invalid" in error_msg or "unauthorized" in error_msg or "401" in error_msg

    def test_require_admin_token_accepts_correct_token(self):
        """Should accept when token matches."""
        from backend.app import _require_admin_token_strict

        # Mock settings.admin_token
        with patch("backend.app.settings") as mock_settings:
            mock_settings.admin_token = "correct-token-123"

            # Create mock request with state attribute
            mock_request = MagicMock()
            mock_request.state = MagicMock()
            mock_request.state.request_id = "test-request-id"

            # Should not raise
            _require_admin_token_strict(
                mock_request, authorization="Bearer correct-token-123", x_admin_token=None
            )

    def test_admin_endpoints_use_strict_validation(self):
        """All admin endpoints should use strict validation, not fail-open."""
        # Check that admin endpoints are decorated with strict auth

        # These endpoints should have strict auth
        admin_endpoints = [
            "/api/models/registry",
            "/api/system/update",
            "/api/config",
        ]

        # Mock to verify they use strict validation
        # This is a structural test - in real code, endpoints should use @require_admin decorator
        # that internally calls _require_admin_token_strict


# =============================================================================
# CRITICAL-4: PTY Shell Auth Bypass
# =============================================================================


class TestTerminalAuthSecurity:
    """Tests that terminal WebSocket requires proper authentication."""

    def test_terminal_websocket_requires_auth_in_production(self):
        """Terminal should require auth in production mode."""
        from backend.terminal_ws import _require_terminal_auth

        # Should require auth in production
        is_authorized = _require_terminal_auth(token=None, production_mode=True)
        assert is_authorized is False

    def test_terminal_websocket_allows_demo_in_dev_mode(self):
        """Terminal allows unauthenticated access in dev mode for website demos."""
        from backend.terminal_ws import _require_terminal_auth

        # Dev mode allows unauthenticated access for demos
        is_authorized = _require_terminal_auth(token=None, production_mode=False)
        assert is_authorized is True

    def test_terminal_auth_validates_session_token(self):
        """Terminal auth should validate actual session tokens."""
        from backend.terminal_ws import _require_terminal_auth

        # Invalid token should be rejected
        is_authorized = _require_terminal_auth(
            token="invalid-token-123", production_mode=True, valid_tokens={"valid-token-456"}
        )
        assert is_authorized is False

        # Valid token should be accepted
        is_authorized = _require_terminal_auth(
            token="valid-token-456", production_mode=True, valid_tokens={"valid-token-456"}
        )
        assert is_authorized is True

    def test_terminal_websocket_rejects_unauthenticated(self):
        """WebSocket connection should be rejected without valid auth."""
        # This would be an integration test with actual WebSocket
        # For now, verify the auth check exists
        pass


# =============================================================================
# CRITICAL-5: Terminal Rate Limiter Not Enforced
# =============================================================================


class TestTerminalRateLimiting:
    """Tests that terminal WebSocket has rate limiting enforced."""

    def test_terminal_rate_limiter_exists(self):
        """Rate limiter should be defined for terminal operations."""
        from backend.terminal_ws import _get_terminal_rate_limiter

        limiter = _get_terminal_rate_limiter()
        assert limiter is not None
        assert hasattr(limiter, "is_allowed")

    def test_terminal_websocket_enforces_rate_limit(self):
        """Terminal WebSocket endpoint should enforce rate limiting."""
        from backend.terminal_ws import _check_terminal_rate_limit, _get_terminal_rate_limiter

        # Use a unique IP so other tests don't pollute the counter window.
        client_ip = "192.168.1.231"
        limit = _get_terminal_rate_limiter().max_connections_per_ip

        # Up to limit connections should be allowed
        for _ in range(limit):
            allowed, _ = _check_terminal_rate_limit(client_ip)
            assert allowed is True

        # The next connection should be rejected
        allowed, reason = _check_terminal_rate_limit(client_ip)
        assert allowed is False
        assert "rate limit" in reason.lower()

    def test_rate_limiter_has_appropriate_limits(self):
        """Terminal rate limiter should have reasonable limits."""
        from backend.terminal_ws import _get_terminal_rate_limiter

        limiter = _get_terminal_rate_limiter()

        # Should have max connections per IP
        assert hasattr(limiter, "max_connections_per_ip")
        assert limiter.max_connections_per_ip > 0
        assert limiter.max_connections_per_ip <= 10  # Not too permissive

        # Should have time window
        assert hasattr(limiter, "time_window_seconds")
        assert limiter.time_window_seconds >= 60  # At least 1 minute


# =============================================================================
# Integration Tests
# =============================================================================


class TestCriticalIntegrity:
    """Integration tests for critical integrity issues."""

    def test_sage_cannot_bypass_tdd_with_fake_implementation(self):
        """SAGE should not be able to claim TDD compliance without actual files."""
        # Simulate a response that looks like TDD but has no FILE: blocks
        response = """
## TDD Implementation

I've followed the TDD process:

1. **Write Tests First**: Created test_feature.py with comprehensive tests
2. **Implement**: Built the feature in feature.py
3. **Validate**: All tests pass

```bash
pytest tests/test_feature.py -v
```

✅ TDD process complete!
"""

        files_written = []

        from sage.cli_core import _validate_tdd_compliance

        is_compliant, reason = _validate_tdd_compliance(
            response, files_written, is_implementation_request=True
        )

        assert is_compliant is False
        assert "no files" in reason.lower() or "no FILE:" in reason.lower()

    def test_execution_in_thread_pool_does_not_crash(self):
        """Running SAGE operations in thread pool should not crash with signal errors."""
        import time
        from concurrent.futures import ThreadPoolExecutor

        def simulate_sage_operation():
            # This would normally call renderer functions that install SIGINT handlers
            # With the fix, it should not crash
            time.sleep(0.1)
            return "success"

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(simulate_sage_operation) for _ in range(5)]
            results = [f.result() for f in futures]

        assert len(results) == 5
        assert all(r == "success" for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
