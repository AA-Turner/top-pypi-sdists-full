"""Comprehensive tests for sage/core/errors.py - 100% coverage target."""

from unittest.mock import MagicMock, patch

import pytest

from sage.core.errors import (
    ErrorCategory,
    ErrorContext,
    ErrorFormatter,
    ErrorGuidance,
    ErrorHandler,
    ErrorRenderer,
    ErrorSeverity,
    SageError,
    SageException,
    confirm_destructive_operation,
    create_auth_error,
    create_command_blocked_error,
    create_command_not_found_error,
    create_config_error,
    create_context_overflow_error,
    create_file_not_found_error,
    create_file_permission_error,
    create_model_not_found_error,
    create_network_error,
    create_rate_limit_error,
    create_timeout_error,
    error_boundary,
    format_diff_preview,
    get_error_handler,
    handle_error,
    set_error_handler,
)


# =============================================================================
# ErrorCategory Tests
# =============================================================================


class TestErrorCategory:
    """Tests for ErrorCategory enum."""

    def test_network_categories(self):
        """Test network error categories."""
        assert ErrorCategory.NETWORK_CONNECTION.value == "network_connection"
        assert ErrorCategory.NETWORK_TIMEOUT.value == "network_timeout"
        assert ErrorCategory.NETWORK_DNS.value == "network_dns"

    def test_auth_categories(self):
        """Test authentication error categories."""
        assert ErrorCategory.AUTH_INVALID_KEY.value == "auth_invalid_key"
        assert ErrorCategory.AUTH_EXPIRED.value == "auth_expired"
        assert ErrorCategory.AUTH_RATE_LIMITED.value == "auth_rate_limited"
        assert ErrorCategory.AUTH_PERMISSION_DENIED.value == "auth_permission_denied"

    def test_validation_categories(self):
        """Test validation error categories."""
        assert ErrorCategory.VALIDATION_INPUT.value == "validation_input"
        assert ErrorCategory.VALIDATION_FILE.value == "validation_file"
        assert ErrorCategory.VALIDATION_CONFIG.value == "validation_config"

    def test_exec_categories(self):
        """Test execution error categories."""
        assert ErrorCategory.EXEC_TIMEOUT.value == "exec_timeout"
        assert ErrorCategory.EXEC_COMMAND_FAILED.value == "exec_command_failed"
        assert ErrorCategory.EXEC_BLOCKED.value == "exec_blocked"
        assert ErrorCategory.EXEC_NOT_FOUND.value == "exec_not_found"

    def test_resource_categories(self):
        """Test resource error categories."""
        assert ErrorCategory.RESOURCE_NOT_FOUND.value == "resource_not_found"
        assert ErrorCategory.RESOURCE_BUSY.value == "resource_busy"
        assert ErrorCategory.RESOURCE_EXHAUSTED.value == "resource_exhausted"

    def test_model_categories(self):
        """Test model error categories."""
        assert ErrorCategory.MODEL_NOT_FOUND.value == "model_not_found"
        assert ErrorCategory.MODEL_LOAD_FAILED.value == "model_load_failed"
        assert ErrorCategory.MODEL_CONTEXT_OVERFLOW.value == "model_context_overflow"
        assert ErrorCategory.MODEL_GENERATION_FAILED.value == "model_generation_failed"

    def test_file_categories(self):
        """Test file system error categories."""
        assert ErrorCategory.FILE_NOT_FOUND.value == "file_not_found"
        assert ErrorCategory.FILE_PERMISSION.value == "file_permission"
        assert ErrorCategory.FILE_TOO_LARGE.value == "file_too_large"
        assert ErrorCategory.FILE_INVALID.value == "file_invalid"

    def test_config_categories(self):
        """Test configuration error categories."""
        assert ErrorCategory.CONFIG_INVALID.value == "config_invalid"
        assert ErrorCategory.CONFIG_MISSING.value == "config_missing"

    def test_internal_categories(self):
        """Test internal error categories."""
        assert ErrorCategory.INTERNAL_ERROR.value == "internal_error"
        assert ErrorCategory.UNKNOWN.value == "unknown"


# =============================================================================
# ErrorSeverity Tests
# =============================================================================


class TestErrorSeverity:
    """Tests for ErrorSeverity enum."""

    def test_all_severities(self):
        """Test all severity levels."""
        assert ErrorSeverity.DEBUG.value == "debug"
        assert ErrorSeverity.INFO.value == "info"
        assert ErrorSeverity.WARNING.value == "warning"
        assert ErrorSeverity.ERROR.value == "error"
        assert ErrorSeverity.CRITICAL.value == "critical"


# =============================================================================
# ErrorContext Tests
# =============================================================================


class TestErrorContext:
    """Tests for ErrorContext dataclass."""

    def test_basic_context(self):
        """Test creating basic error context."""
        ctx = ErrorContext(operation="test_operation")
        assert ctx.operation == "test_operation"
        assert ctx.file_path is None
        assert ctx.line_number is None
        assert ctx.command is None
        assert ctx.url is None
        assert ctx.model is None
        assert ctx.additional == {}

    def test_full_context(self):
        """Test creating context with all fields."""
        ctx = ErrorContext(
            operation="execute",
            file_path="/path/to/file.py",
            line_number=42,
            command="python test.py",
            url="http://example.com",
            model="gpt-4",
            additional={"key": "value"},
        )
        assert ctx.operation == "execute"
        assert ctx.file_path == "/path/to/file.py"
        assert ctx.line_number == 42
        assert ctx.command == "python test.py"
        assert ctx.url == "http://example.com"
        assert ctx.model == "gpt-4"
        assert ctx.additional == {"key": "value"}


# =============================================================================
# ErrorGuidance Tests
# =============================================================================


class TestErrorGuidance:
    """Tests for ErrorGuidance dataclass."""

    def test_basic_guidance(self):
        """Test creating basic guidance."""
        guidance = ErrorGuidance(message="An error occurred")
        assert guidance.message == "An error occurred"
        assert guidance.suggestions == []
        assert guidance.commands == []
        assert guidance.docs_url is None
        assert guidance.related_issues == []

    def test_full_guidance(self):
        """Test creating guidance with all fields."""
        guidance = ErrorGuidance(
            message="Fix this error",
            suggestions=["Try this", "Or this"],
            commands=["cmd1", "cmd2"],
            docs_url="https://docs.example.com",
            related_issues=["#123", "#456"],
        )
        assert guidance.message == "Fix this error"
        assert len(guidance.suggestions) == 2
        assert len(guidance.commands) == 2
        assert guidance.docs_url == "https://docs.example.com"
        assert guidance.related_issues == ["#123", "#456"]


# =============================================================================
# SageError Tests
# =============================================================================


class TestSageError:
    """Tests for SageError dataclass."""

    def test_basic_error(self):
        """Test creating a basic error."""
        error = SageError(
            category=ErrorCategory.INTERNAL_ERROR,
            severity=ErrorSeverity.ERROR,
            message="Something went wrong",
            guidance=ErrorGuidance(message="Fix it"),
        )
        assert error.category == ErrorCategory.INTERNAL_ERROR
        assert error.severity == ErrorSeverity.ERROR
        assert error.message == "Something went wrong"
        assert error.context is None
        assert error.original_exception is None
        assert error.error_code is None

    def test_error_str(self):
        """Test error string representation."""
        error = SageError(
            category=ErrorCategory.FILE_NOT_FOUND,
            severity=ErrorSeverity.ERROR,
            message="File missing",
            guidance=ErrorGuidance(message="Check path"),
        )
        assert str(error) == "[file_not_found] File missing"

    def test_error_to_dict(self):
        """Test converting error to dictionary."""
        error = SageError(
            category=ErrorCategory.NETWORK_CONNECTION,
            severity=ErrorSeverity.WARNING,
            message="Connection failed",
            guidance=ErrorGuidance(
                message="Check network",
                suggestions=["Check WiFi"],
                commands=["ping google.com"],
                docs_url="https://docs.example.com",
            ),
            context=ErrorContext(
                operation="connect",
                file_path="/path/to/file",
                additional={"retries": 3},
            ),
            error_code="E001",
        )
        result = error.to_dict()

        assert result["category"] == "network_connection"
        assert result["severity"] == "warning"
        assert result["message"] == "Connection failed"
        assert result["error_code"] == "E001"
        assert result["guidance"]["message"] == "Check network"
        assert result["guidance"]["suggestions"] == ["Check WiFi"]
        assert result["guidance"]["commands"] == ["ping google.com"]
        assert result["guidance"]["docs_url"] == "https://docs.example.com"
        assert result["context"]["operation"] == "connect"
        assert result["context"]["file_path"] == "/path/to/file"
        assert result["context"]["additional"]["retries"] == 3

    def test_error_to_dict_no_context(self):
        """Test converting error without context to dictionary."""
        error = SageError(
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.INFO,
            message="Info message",
            guidance=ErrorGuidance(message="Info"),
        )
        result = error.to_dict()

        assert result["context"]["operation"] is None
        assert result["context"]["file_path"] is None
        assert result["context"]["additional"] == {}


# =============================================================================
# SageException Tests
# =============================================================================


class TestSageException:
    """Tests for SageException class."""

    def test_basic_exception(self):
        """Test creating basic exception."""
        exc = SageException("Test error")
        assert str(exc) == "Test error"
        assert exc.message == "Test error"
        assert exc.category == ErrorCategory.INTERNAL_ERROR
        assert exc.severity == ErrorSeverity.ERROR
        assert exc.context is None
        assert exc.original_exception is None

    def test_full_exception(self):
        """Test creating exception with all fields."""
        original = ValueError("Original error")
        ctx = ErrorContext(operation="test")
        exc = SageException(
            message="Custom error",
            category=ErrorCategory.FILE_NOT_FOUND,
            severity=ErrorSeverity.WARNING,
            context=ctx,
            original_exception=original,
        )
        assert exc.message == "Custom error"
        assert exc.category == ErrorCategory.FILE_NOT_FOUND
        assert exc.severity == ErrorSeverity.WARNING
        assert exc.context is ctx
        assert exc.original_exception is original

    def test_to_sage_error(self):
        """Test converting exception to SageError."""
        exc = SageException(
            message="Test error",
            category=ErrorCategory.AUTH_INVALID_KEY,
            severity=ErrorSeverity.CRITICAL,
        )
        error = exc.to_sage_error()

        assert isinstance(error, SageError)
        assert error.category == ErrorCategory.AUTH_INVALID_KEY
        assert error.severity == ErrorSeverity.CRITICAL
        assert error.message == "Test error"
        assert error.guidance.message == "An error occurred in SAGE."

    def test_exception_can_be_raised(self):
        """Test that SageException can be raised and caught."""
        with pytest.raises(SageException) as exc_info:
            raise SageException("Raised error")

        assert str(exc_info.value) == "Raised error"


# =============================================================================
# Factory Function Tests
# =============================================================================


class TestCreateNetworkError:
    """Tests for create_network_error factory."""

    def test_basic_network_error(self):
        """Test creating basic network error."""
        error = create_network_error("Connection refused")
        assert error.category == ErrorCategory.NETWORK_CONNECTION
        assert error.severity == ErrorSeverity.ERROR
        assert "Connection refused" in error.message
        assert error.error_code == "E001"

    def test_network_error_with_host(self):
        """Test network error with host."""
        error = create_network_error("Failed to connect", host="api.example.com")
        assert "api.example.com" in error.guidance.suggestions[2]
        assert "api.example.com" in error.guidance.commands[0]
        assert error.context.url == "api.example.com"

    def test_network_error_without_host(self):
        """Test network error without host."""
        error = create_network_error("Failed to connect")
        assert "Check the service URL" in error.guidance.suggestions[2]

    def test_network_error_with_original(self):
        """Test network error with original exception."""
        original = ConnectionError("Original")
        error = create_network_error("Failed", original=original)
        assert error.original_exception is original


class TestCreateTimeoutError:
    """Tests for create_timeout_error factory."""

    def test_basic_timeout_error(self):
        """Test creating basic timeout error."""
        error = create_timeout_error("API call", 30)
        assert error.category == ErrorCategory.EXEC_TIMEOUT
        assert "30s" in error.message
        assert "API call" in error.message
        assert error.error_code == "E002"
        assert error.context.additional["timeout"] == 30

    def test_timeout_error_suggests_doubled_timeout(self):
        """Test timeout error suggests doubled timeout."""
        error = create_timeout_error("operation", 60)
        assert "SAGE_TIMEOUT=120" in error.guidance.suggestions[0]


class TestCreateAuthError:
    """Tests for create_auth_error factory."""

    def test_basic_auth_error(self):
        """Test creating basic auth error."""
        error = create_auth_error("OpenAI", "Invalid API key")
        assert error.category == ErrorCategory.AUTH_INVALID_KEY
        assert "OpenAI" in error.message
        assert "Invalid API key" in error.message
        assert error.error_code == "E003"
        assert "SAGE_OPENAI_API_KEY" in error.guidance.suggestions[0]

    def test_auth_error_context(self):
        """Test auth error contains provider in context."""
        error = create_auth_error("Anthropic", "Key expired")
        assert error.context.additional["provider"] == "Anthropic"


class TestCreateRateLimitError:
    """Tests for create_rate_limit_error factory."""

    def test_basic_rate_limit(self):
        """Test creating basic rate limit error."""
        error = create_rate_limit_error("OpenAI")
        assert error.category == ErrorCategory.AUTH_RATE_LIMITED
        assert error.severity == ErrorSeverity.WARNING
        assert "OpenAI" in error.message
        assert error.error_code == "E004"

    def test_rate_limit_with_retry_after(self):
        """Test rate limit with retry after."""
        error = create_rate_limit_error("OpenAI", retry_after=60)
        assert "60s" in error.message
        assert "Wait 60 seconds" in error.guidance.suggestions[0]
        assert "sleep 60" in error.guidance.commands[0]
        assert error.context.additional["retry_after"] == 60

    def test_rate_limit_without_retry_after(self):
        """Test rate limit without retry after."""
        error = create_rate_limit_error("OpenAI")
        assert "Wait a moment" in error.guidance.suggestions[0]


class TestCreateFileNotFoundError:
    """Tests for create_file_not_found_error factory."""

    def test_basic_file_not_found(self):
        """Test creating basic file not found error."""
        error = create_file_not_found_error("/path/to/file.py")
        assert error.category == ErrorCategory.FILE_NOT_FOUND
        assert "/path/to/file.py" in error.message
        assert error.error_code == "E005"
        assert error.context.file_path == "/path/to/file.py"
        assert error.context.operation == "read"

    def test_file_not_found_with_operation(self):
        """Test file not found with custom operation."""
        error = create_file_not_found_error("/path/to/file", operation="write")
        assert error.context.operation == "write"


class TestCreateFilePermissionError:
    """Tests for create_file_permission_error factory."""

    def test_basic_permission_error(self):
        """Test creating basic permission error."""
        error = create_file_permission_error("/etc/passwd")
        assert error.category == ErrorCategory.FILE_PERMISSION
        assert "/etc/passwd" in error.message
        assert error.error_code == "E006"
        assert "write" in error.guidance.message

    def test_permission_error_with_operation(self):
        """Test permission error with custom operation."""
        error = create_file_permission_error("/file", operation="read")
        assert "read" in error.guidance.message


class TestCreateCommandNotFoundError:
    """Tests for create_command_not_found_error factory."""

    def test_basic_command_not_found(self):
        """Test creating basic command not found error."""
        error = create_command_not_found_error("unknowncmd")
        assert error.category == ErrorCategory.EXEC_NOT_FOUND
        assert "unknowncmd" in error.message
        assert error.error_code == "E007"

    def test_known_command_hints(self):
        """Test known commands get proper hints."""
        commands = {
            "git": "git-scm.com",
            "python": "python.org",
            "node": "nodejs.org",
            "npm": "nodejs.org",
            "cargo": "rustup.rs",
            "go": "golang.org",
            "pip": "Python",
            "pytest": "pip install pytest",
        }
        for cmd, expected in commands.items():
            error = create_command_not_found_error(cmd)
            assert expected in error.guidance.suggestions[0]

    def test_unknown_command_hint(self):
        """Test unknown command gets generic hint."""
        error = create_command_not_found_error("customtool")
        assert "Install customtool" in error.guidance.suggestions[0]

    def test_command_with_args(self):
        """Test command with arguments."""
        error = create_command_not_found_error("git status --short")
        assert error.context.command == "git status --short"
        # Should extract just the command name
        assert "git" in error.message

    def test_empty_command(self):
        """Test empty command."""
        error = create_command_not_found_error("")
        assert "command" in error.message


class TestCreateCommandBlockedError:
    """Tests for create_command_blocked_error factory."""

    def test_basic_blocked_error(self):
        """Test creating basic blocked error."""
        error = create_command_blocked_error("rm -rf /", "Destructive command")
        assert error.category == ErrorCategory.EXEC_BLOCKED
        assert error.severity == ErrorSeverity.WARNING
        assert "rm -rf /" in error.message
        assert error.error_code == "E008"
        assert "Destructive command" in error.guidance.message


class TestCreateModelNotFoundError:
    """Tests for create_model_not_found_error factory."""

    def test_basic_model_not_found(self):
        """Test creating basic model not found error."""
        error = create_model_not_found_error("gpt-5")
        assert error.category == ErrorCategory.MODEL_NOT_FOUND
        assert "gpt-5" in error.message
        assert error.error_code == "E009"
        assert error.context.model == "gpt-5"

    def test_model_not_found_with_available(self):
        """Test model not found with available models."""
        available = ["gpt-4", "gpt-3.5", "claude-3", "llama-3", "mixtral", "gemini"]
        error = create_model_not_found_error("gpt-5", available_models=available)
        # Should show first 5 models
        assert "gpt-4" in error.guidance.suggestions[-1]
        assert "gpt-3.5" in error.guidance.suggestions[-1]


class TestCreateContextOverflowError:
    """Tests for create_context_overflow_error factory."""

    def test_basic_context_overflow(self):
        """Test creating basic context overflow error."""
        error = create_context_overflow_error(50000, 32000)
        assert error.category == ErrorCategory.MODEL_CONTEXT_OVERFLOW
        assert "50,000" in error.message
        assert "32,000" in error.message
        assert error.error_code == "E010"
        assert error.context.additional["current_tokens"] == 50000
        assert error.context.additional["max_tokens"] == 32000


class TestCreateConfigError:
    """Tests for create_config_error factory."""

    def test_basic_config_error(self):
        """Test creating basic config error."""
        error = create_config_error("api_key", "Invalid format")
        assert error.category == ErrorCategory.CONFIG_INVALID
        assert "api_key" in error.message
        assert "Invalid format" in error.message
        assert error.error_code == "E011"


# =============================================================================
# ErrorRenderer Tests
# =============================================================================


class TestErrorRenderer:
    """Tests for ErrorRenderer class."""

    def test_init_default(self):
        """Test default initialization."""
        renderer = ErrorRenderer()
        assert renderer.console is not None

    def test_init_with_console(self):
        """Test initialization with custom console."""
        console = MagicMock()
        renderer = ErrorRenderer(console=console)
        assert renderer.console is console

    def test_render(self):
        """Test rendering an error."""
        console = MagicMock()
        renderer = ErrorRenderer(console=console)

        error = SageError(
            category=ErrorCategory.FILE_NOT_FOUND,
            severity=ErrorSeverity.ERROR,
            message="File not found",
            guidance=ErrorGuidance(
                message="Check path",
                suggestions=["Verify path"],
                commands=["ls -la", "# Comment"],
                docs_url="https://docs.example.com",
            ),
            error_code="E005",
        )
        renderer.render(error)

        # Should have called print with a Panel
        console.print.assert_called_once()

    def test_render_all_severities(self):
        """Test rendering with all severity levels."""
        console = MagicMock()
        renderer = ErrorRenderer(console=console)

        for severity in ErrorSeverity:
            error = SageError(
                category=ErrorCategory.INTERNAL_ERROR,
                severity=severity,
                message=f"Test {severity.value}",
                guidance=ErrorGuidance(message="Fix"),
            )
            renderer.render(error)

    def test_render_simple(self):
        """Test simple rendering."""
        console = MagicMock()
        renderer = ErrorRenderer(console=console)

        error = SageError(
            category=ErrorCategory.NETWORK_CONNECTION,
            severity=ErrorSeverity.ERROR,
            message="Connection failed",
            guidance=ErrorGuidance(
                message="Check network",
                suggestions=["Check WiFi"],
            ),
        )
        renderer.render_simple(error)

        assert console.print.call_count == 2

    def test_render_simple_no_suggestions(self):
        """Test simple rendering without suggestions."""
        console = MagicMock()
        renderer = ErrorRenderer(console=console)

        error = SageError(
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR,
            message="Error",
            guidance=ErrorGuidance(message="Fix"),
        )
        renderer.render_simple(error)

        assert console.print.call_count == 1

    def test_render_debug(self):
        """Test debug rendering."""
        console = MagicMock()
        renderer = ErrorRenderer(console=console)

        original = ValueError("Original error")
        error = SageError(
            category=ErrorCategory.INTERNAL_ERROR,
            severity=ErrorSeverity.ERROR,
            message="Error with debug info",
            guidance=ErrorGuidance(message="Debug"),
            context=ErrorContext(operation="test"),
            original_exception=original,
        )
        renderer.render_debug(error)

        # Should print Panel + original exception + context
        assert console.print.call_count >= 3

    def test_render_debug_no_original(self):
        """Test debug rendering without original exception."""
        console = MagicMock()
        renderer = ErrorRenderer(console=console)

        error = SageError(
            category=ErrorCategory.INTERNAL_ERROR,
            severity=ErrorSeverity.ERROR,
            message="Error",
            guidance=ErrorGuidance(message="Debug"),
        )
        renderer.render_debug(error)

        # Should just print Panel
        console.print.call_count == 1


class TestErrorFormatterAlias:
    """Test that ErrorFormatter is an alias for ErrorRenderer."""

    def test_alias(self):
        """Test ErrorFormatter is ErrorRenderer."""
        assert ErrorFormatter is ErrorRenderer


# =============================================================================
# ErrorHandler Tests
# =============================================================================


class TestErrorHandler:
    """Tests for ErrorHandler class."""

    def test_init_default(self):
        """Test default initialization."""
        handler = ErrorHandler()
        assert handler.renderer is not None
        assert handler.debug is False
        assert handler.on_error is None
        assert handler.error_log == []

    def test_init_with_params(self):
        """Test initialization with parameters."""
        renderer = MagicMock()
        on_error = MagicMock()
        handler = ErrorHandler(renderer=renderer, debug=True, on_error=on_error)

        assert handler.renderer is renderer
        assert handler.debug is True
        assert handler.on_error is on_error

    def test_handle_sage_error(self):
        """Test handling a SageError directly."""
        renderer = MagicMock()
        handler = ErrorHandler(renderer=renderer)

        error = SageError(
            category=ErrorCategory.FILE_NOT_FOUND,
            severity=ErrorSeverity.ERROR,
            message="Not found",
            guidance=ErrorGuidance(message="Check"),
        )
        result = handler.handle(error)

        assert result is error
        assert error in handler.error_log
        renderer.render.assert_called_once_with(error)

    def test_handle_with_debug(self):
        """Test handling with debug mode."""
        renderer = MagicMock()
        handler = ErrorHandler(renderer=renderer, debug=True)

        error = SageError(
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR,
            message="Test",
            guidance=ErrorGuidance(message="Fix"),
        )
        handler.handle(error)

        renderer.render_debug.assert_called_once_with(error)

    def test_handle_with_callback(self):
        """Test handling with on_error callback."""
        on_error = MagicMock()
        handler = ErrorHandler(renderer=MagicMock(), on_error=on_error)

        error = SageError(
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR,
            message="Test",
            guidance=ErrorGuidance(message="Fix"),
        )
        handler.handle(error)

        on_error.assert_called_once_with(error)

    def test_handle_regular_exception(self):
        """Test handling a regular exception."""
        renderer = MagicMock()
        handler = ErrorHandler(renderer=renderer)

        exc = ValueError("Test error")
        result = handler.handle(exc)

        assert isinstance(result, SageError)
        assert result.original_exception is exc
        assert result in handler.error_log

    def test_convert_connection_error(self):
        """Test converting connection error."""
        handler = ErrorHandler(renderer=MagicMock())

        exc = ConnectionError("Connection refused")
        result = handler._convert_exception(exc)

        assert result.category == ErrorCategory.NETWORK_CONNECTION

    def test_convert_connection_keyword(self):
        """Test converting error with connection keyword."""
        handler = ErrorHandler(renderer=MagicMock())

        exc = Exception("Unable to establish connection")
        result = handler._convert_exception(exc)

        assert result.category == ErrorCategory.NETWORK_CONNECTION

    def test_convert_timeout_error(self):
        """Test converting timeout error."""
        handler = ErrorHandler(renderer=MagicMock())

        exc = TimeoutError("Operation timed out")
        result = handler._convert_exception(exc)

        assert result.category == ErrorCategory.EXEC_TIMEOUT

    def test_convert_timeout_keyword(self):
        """Test converting error with timeout keyword."""
        handler = ErrorHandler(renderer=MagicMock())

        ctx = ErrorContext(operation="api_call")
        exc = Exception("Request timeout")
        result = handler._convert_exception(exc, ctx)

        assert result.category == ErrorCategory.EXEC_TIMEOUT

    def test_convert_file_not_found_error(self):
        """Test converting FileNotFoundError."""
        handler = ErrorHandler(renderer=MagicMock())

        ctx = ErrorContext(operation="read", file_path="/path/to/file")
        exc = FileNotFoundError("File missing")
        result = handler._convert_exception(exc, ctx)

        assert result.category == ErrorCategory.FILE_NOT_FOUND

    def test_convert_permission_error(self):
        """Test converting PermissionError."""
        handler = ErrorHandler(renderer=MagicMock())

        ctx = ErrorContext(operation="write", file_path="/etc/passwd")
        exc = PermissionError("Permission denied")
        result = handler._convert_exception(exc, ctx)

        assert result.category == ErrorCategory.FILE_PERMISSION

    def test_convert_command_not_found(self):
        """Test converting command not found error."""
        handler = ErrorHandler(renderer=MagicMock())

        ctx = ErrorContext(operation="execute", command="unknowncmd")
        exc = Exception("unknowncmd: command not found")
        result = handler._convert_exception(exc, ctx)

        assert result.category == ErrorCategory.EXEC_NOT_FOUND

    def test_convert_generic_error(self):
        """Test converting generic error."""
        handler = ErrorHandler(renderer=MagicMock())

        exc = RuntimeError("Something went wrong")
        result = handler._convert_exception(exc)

        assert result.category == ErrorCategory.INTERNAL_ERROR
        assert result.error_code == "E999"

    def test_get_error_summary(self):
        """Test getting error summary."""
        handler = ErrorHandler(renderer=MagicMock())

        errors = [
            SageError(
                category=ErrorCategory.FILE_NOT_FOUND,
                severity=ErrorSeverity.ERROR,
                message="Error 1",
                guidance=ErrorGuidance(message="Fix"),
            ),
            SageError(
                category=ErrorCategory.FILE_NOT_FOUND,
                severity=ErrorSeverity.ERROR,
                message="Error 2",
                guidance=ErrorGuidance(message="Fix"),
            ),
            SageError(
                category=ErrorCategory.NETWORK_CONNECTION,
                severity=ErrorSeverity.ERROR,
                message="Error 3",
                guidance=ErrorGuidance(message="Fix"),
            ),
        ]
        for error in errors:
            handler.handle(error)

        summary = handler.get_error_summary()

        assert summary["file_not_found"] == 2
        assert summary["network_connection"] == 1


# =============================================================================
# error_boundary Tests
# =============================================================================


class TestErrorBoundary:
    """Tests for error_boundary context manager."""

    def test_no_error(self):
        """Test context manager with no error."""
        handler = ErrorHandler(renderer=MagicMock())

        with error_boundary("test_operation", handler=handler) as ctx:
            result = 1 + 1

        assert result == 2
        assert ctx.error is None

    def test_captures_error(self):
        """Test context manager captures error."""
        handler = ErrorHandler(renderer=MagicMock())

        with error_boundary("test_operation", handler=handler) as ctx:
            raise ValueError("Test error")

        assert ctx.error is not None
        assert ctx.error.context.operation == "test_operation"

    def test_reraise_error(self):
        """Test context manager with reraise."""
        handler = ErrorHandler(renderer=MagicMock())

        with pytest.raises(ValueError):
            with error_boundary("test_operation", handler=handler, reraise=True):
                raise ValueError("Test error")

    def test_default_handler(self):
        """Test context manager with default handler."""
        with patch("sage.core.errors.ErrorHandler") as mock_handler_class:
            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler

            with error_boundary("test") as ctx:
                raise ValueError("Test")


# =============================================================================
# format_diff_preview Tests
# =============================================================================


class TestFormatDiffPreview:
    """Tests for format_diff_preview function."""

    def test_basic_diff(self):
        """Test basic diff preview."""
        old = "line1\nline2\n"
        new = "line1\nmodified\n"

        diff = format_diff_preview(old, new)

        assert "--- current" in diff
        assert "+++ new" in diff
        assert "-line2" in diff
        assert "+modified" in diff

    def test_no_changes(self):
        """Test diff with no changes."""
        content = "unchanged\n"
        diff = format_diff_preview(content, content)

        # Should produce minimal or no diff output
        assert "unchanged" not in diff or diff == ""

    def test_truncated_diff(self):
        """Test diff truncation."""
        old = "\n".join([f"line{i}" for i in range(100)])
        new = "\n".join([f"modified{i}" for i in range(100)])

        diff = format_diff_preview(old, new, max_lines=10)

        assert "more lines" in diff


# =============================================================================
# confirm_destructive_operation Tests
# =============================================================================


class TestConfirmDestructiveOperation:
    """Tests for confirm_destructive_operation function."""

    def test_confirm_yes(self):
        """Test confirming with yes."""
        console = MagicMock()
        console.input.return_value = "y"

        result = confirm_destructive_operation("Delete files", "All files will be removed", console)

        assert result is True

    def test_confirm_yes_full(self):
        """Test confirming with 'yes'."""
        console = MagicMock()
        console.input.return_value = "yes"

        result = confirm_destructive_operation("Delete", "Details", console)

        assert result is True

    def test_confirm_no(self, monkeypatch):
        """Test declining with no."""
        monkeypatch.delenv("SAGE_TESTING", raising=False)
        console = MagicMock()
        console.input.return_value = "n"

        result = confirm_destructive_operation("Delete", "Details", console)

        assert result is False

    def test_confirm_empty(self, monkeypatch):
        """Test declining with empty input."""
        monkeypatch.delenv("SAGE_TESTING", raising=False)
        console = MagicMock()
        console.input.return_value = ""

        result = confirm_destructive_operation("Delete", "Details", console)

        assert result is False

    def test_confirm_eof_error(self, monkeypatch):
        """Test handling EOFError."""
        monkeypatch.delenv("SAGE_TESTING", raising=False)
        console = MagicMock()
        console.input.side_effect = EOFError()

        result = confirm_destructive_operation("Delete", "Details", console)

        assert result is False

    def test_confirm_keyboard_interrupt(self, monkeypatch):
        """Test handling KeyboardInterrupt."""
        monkeypatch.delenv("SAGE_TESTING", raising=False)
        console = MagicMock()
        console.input.side_effect = KeyboardInterrupt()

        result = confirm_destructive_operation("Delete", "Details", console)

        assert result is False

    def test_confirm_default_console(self):
        """Test with default console.

        When `console` is omitted, confirm_destructive_operation resolves the
        SHARED console via `from sage.core.renderer import console`
        (sage/core/errors.py:848-850). It does not instantiate
        sage.core.errors.Console. This test used to patch that class, so the
        patch applied to something the code path never touches: the real
        console was used and `console.input(...)` read the process's actual
        stdin, which under pytest raises

            OSError: pytest: reading from stdin while output is captured!

        Patch the collaborator the function really uses. Because the import
        happens inside the function body, patching the module attribute takes
        effect at call time.
        """
        mock_console = MagicMock()
        mock_console.input.return_value = "y"

        with patch("sage.core.renderer.console", mock_console):
            result = confirm_destructive_operation("Delete", "Details")

        assert result is True
        # Prove the default console was genuinely consulted rather than the
        # assertion passing for some unrelated reason.
        mock_console.input.assert_called_once()


# =============================================================================
# Global Handler Tests
# =============================================================================


class TestGlobalHandler:
    """Tests for global handler functions."""

    def test_get_error_handler_creates_default(self):
        """Test get_error_handler creates default handler."""
        # Reset global handler
        import sage.core.errors as errors_module

        errors_module._global_handler = None

        handler = get_error_handler()

        assert handler is not None
        assert isinstance(handler, ErrorHandler)

    def test_get_error_handler_returns_same(self):
        """Test get_error_handler returns same instance."""
        handler1 = get_error_handler()
        handler2 = get_error_handler()

        assert handler1 is handler2

    def test_set_error_handler(self):
        """Test setting custom handler."""
        custom_handler = ErrorHandler(debug=True)
        set_error_handler(custom_handler)

        assert get_error_handler() is custom_handler

    def test_handle_error_uses_global(self):
        """Test handle_error uses global handler."""
        custom_handler = ErrorHandler(renderer=MagicMock())
        set_error_handler(custom_handler)

        error = SageError(
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.ERROR,
            message="Test",
            guidance=ErrorGuidance(message="Fix"),
        )
        result = handle_error(error)

        assert result is error
        assert error in custom_handler.error_log

    def test_handle_error_with_context(self):
        """Test handle_error with context."""
        custom_handler = ErrorHandler(renderer=MagicMock())
        set_error_handler(custom_handler)

        ctx = ErrorContext(operation="test")
        exc = ValueError("Test")
        result = handle_error(exc, ctx)

        assert isinstance(result, SageError)
