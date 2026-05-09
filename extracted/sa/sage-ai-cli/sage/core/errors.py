"""
Unified error handling system for SAGE.

P0-11 to P0-20: Comprehensive error taxonomy with actionable messages,
troubleshooting guidance, and user-friendly error handling.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# =============================================================================
# Error Categories (P0-11: Create unified error taxonomy)
# =============================================================================


class ErrorCategory(Enum):
    """Categories of errors for better organization and handling."""

    # Network errors
    NETWORK_CONNECTION = "network_connection"
    NETWORK_TIMEOUT = "network_timeout"
    NETWORK_DNS = "network_dns"

    # Authentication errors
    AUTH_INVALID_KEY = "auth_invalid_key"
    AUTH_EXPIRED = "auth_expired"
    AUTH_RATE_LIMITED = "auth_rate_limited"
    AUTH_PERMISSION_DENIED = "auth_permission_denied"

    # Validation errors
    VALIDATION_INPUT = "validation_input"
    VALIDATION_FILE = "validation_file"
    VALIDATION_CONFIG = "validation_config"

    # Execution errors
    EXEC_TIMEOUT = "exec_timeout"
    EXEC_COMMAND_FAILED = "exec_command_failed"
    EXEC_BLOCKED = "exec_blocked"
    EXEC_NOT_FOUND = "exec_not_found"

    # Resource errors
    RESOURCE_NOT_FOUND = "resource_not_found"
    RESOURCE_BUSY = "resource_busy"
    RESOURCE_EXHAUSTED = "resource_exhausted"

    # Model errors
    MODEL_NOT_FOUND = "model_not_found"
    MODEL_LOAD_FAILED = "model_load_failed"
    MODEL_CONTEXT_OVERFLOW = "model_context_overflow"
    MODEL_GENERATION_FAILED = "model_generation_failed"

    # File system errors
    FILE_NOT_FOUND = "file_not_found"
    FILE_PERMISSION = "file_permission"
    FILE_TOO_LARGE = "file_too_large"
    FILE_INVALID = "file_invalid"

    # Configuration errors
    CONFIG_INVALID = "config_invalid"
    CONFIG_MISSING = "config_missing"

    # Internal errors
    INTERNAL_ERROR = "internal_error"
    UNKNOWN = "unknown"


class ErrorSeverity(Enum):
    """Severity levels for errors."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


# =============================================================================
# Error Data Classes
# =============================================================================


@dataclass
class ErrorContext:
    """Context information about where an error occurred."""

    operation: str
    file_path: str | None = None
    line_number: int | None = None
    command: str | None = None
    url: str | None = None
    model: str | None = None
    additional: dict[str, Any] = field(default_factory=dict)


@dataclass
class ErrorGuidance:
    """Guidance for resolving an error (P0-12: Actionable remediation steps)."""

    message: str
    suggestions: list[str] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)
    docs_url: str | None = None
    related_issues: list[str] = field(default_factory=list)


@dataclass
class SageError:
    """
    Unified error representation for SAGE.

    P0-11: Create unified error taxonomy
    P0-12: Add actionable remediation steps
    P0-18: Create troubleshooting documentation links
    """

    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    guidance: ErrorGuidance
    context: ErrorContext | None = None
    original_exception: Exception | None = None
    error_code: str | None = None

    def __str__(self) -> str:
        return f"[{self.category.value}] {self.message}"

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary for logging/serialization."""
        return {
            "category": self.category.value,
            "severity": self.severity.value,
            "message": self.message,
            "error_code": self.error_code,
            "guidance": {
                "message": self.guidance.message,
                "suggestions": self.guidance.suggestions,
                "commands": self.guidance.commands,
                "docs_url": self.guidance.docs_url,
            },
            "context": {
                "operation": self.context.operation if self.context else None,
                "file_path": self.context.file_path if self.context else None,
                "additional": self.context.additional if self.context else {},
            },
        }


class SageException(Exception):
    """
    Base exception class for SAGE.

    This is a proper Python exception that can be raised and caught.
    Use this when you need to raise exceptions in SAGE code.
    """

    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.INTERNAL_ERROR,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        context: ErrorContext | None = None,
        original_exception: Exception | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.context = context
        self.original_exception = original_exception

    def to_sage_error(self) -> SageError:
        """Convert to a SageError for display."""
        return SageError(
            category=self.category,
            severity=self.severity,
            message=self.message,
            guidance=ErrorGuidance(message="An error occurred in SAGE."),
            context=self.context,
            original_exception=self.original_exception,
        )


# =============================================================================
# Error Factory Functions (P0-12: Add actionable remediation steps)
# =============================================================================


def create_network_error(
    message: str,
    host: str | None = None,
    original: Exception | None = None,
) -> SageError:
    """Create a network connection error with guidance."""
    return SageError(
        category=ErrorCategory.NETWORK_CONNECTION,
        severity=ErrorSeverity.ERROR,
        message=message,
        guidance=ErrorGuidance(
            message="Unable to connect to the server.",
            suggestions=[
                "Check your internet connection",
                "Verify the server is running",
                f"Try accessing {host} in a browser" if host else "Check the service URL",
                "Check if a firewall is blocking the connection",
            ],
            commands=[
                f"curl -I {host}" if host else "# Check network connectivity",
                "ping google.com",
                "sage config show  # Verify configuration",
            ],
            docs_url="https://sageworksai.com/#setup",
        ),
        context=ErrorContext(operation="network_request", url=host),
        original_exception=original,
        error_code="E001",
    )


def create_timeout_error(
    operation: str,
    timeout_seconds: int,
    original: Exception | None = None,
) -> SageError:
    """Create a timeout error with guidance."""
    return SageError(
        category=ErrorCategory.EXEC_TIMEOUT,
        severity=ErrorSeverity.ERROR,
        message=f"Operation timed out after {timeout_seconds}s: {operation}",
        guidance=ErrorGuidance(
            message="The operation took too long to complete.",
            suggestions=[
                f"Increase timeout: SAGE_TIMEOUT={timeout_seconds * 2}",
                "Use a faster model for quick operations",
                "Break the task into smaller steps",
                "Check if the model or service is overloaded",
            ],
            commands=[
                f"SAGE_TIMEOUT={timeout_seconds * 2} sage run",
                "sage run --model fast-model",
            ],
            docs_url="https://sageworksai.com/#setup",
        ),
        context=ErrorContext(operation=operation, additional={"timeout": timeout_seconds}),
        original_exception=original,
        error_code="E002",
    )


def create_auth_error(
    provider: str,
    reason: str,
    original: Exception | None = None,
) -> SageError:
    """Create an authentication error with guidance."""
    env_var = f"SAGE_{provider.upper()}_API_KEY"
    return SageError(
        category=ErrorCategory.AUTH_INVALID_KEY,
        severity=ErrorSeverity.ERROR,
        message=f"Authentication failed for {provider}: {reason}",
        guidance=ErrorGuidance(
            message=f"Your {provider} API key is invalid or missing.",
            suggestions=[
                f"Set your API key: export {env_var}=your-api-key",
                f"Or add to config: sage config set api_keys.{provider.lower()} YOUR_KEY",
                f"Get an API key from {provider}'s website",
                "Verify the key hasn't expired",
            ],
            commands=[
                f"export {env_var}='your-api-key'",
                f"sage config set api_keys.{provider.lower()} YOUR_KEY",
                "sage config show  # Verify configuration",
            ],
            docs_url="https://sageworksai.com/#setup",
        ),
        context=ErrorContext(operation="authentication", additional={"provider": provider}),
        original_exception=original,
        error_code="E003",
    )


def create_rate_limit_error(
    provider: str,
    retry_after: int | None = None,
    original: Exception | None = None,
) -> SageError:
    """Create a rate limit error with guidance."""
    return SageError(
        category=ErrorCategory.AUTH_RATE_LIMITED,
        severity=ErrorSeverity.WARNING,
        message=f"Rate limited by {provider}"
        + (f" (retry after {retry_after}s)" if retry_after else ""),
        guidance=ErrorGuidance(
            message="You've exceeded the API rate limit.",
            suggestions=[
                f"Wait {retry_after} seconds before retrying"
                if retry_after
                else "Wait a moment before retrying",
                "Consider upgrading your API plan",
                "Use a different provider as fallback",
                "Reduce request frequency",
            ],
            commands=[
                f"sleep {retry_after or 60} && sage run" if retry_after else "# Wait and retry",
                "sage run --model alternative-model",
            ],
            docs_url="https://sageworksai.com/#setup",
        ),
        context=ErrorContext(
            operation="api_request",
            additional={"provider": provider, "retry_after": retry_after},
        ),
        original_exception=original,
        error_code="E004",
    )


def create_file_not_found_error(
    file_path: str,
    operation: str = "read",
    original: Exception | None = None,
) -> SageError:
    """Create a file not found error with guidance."""
    return SageError(
        category=ErrorCategory.FILE_NOT_FOUND,
        severity=ErrorSeverity.ERROR,
        message=f"File not found: {file_path}",
        guidance=ErrorGuidance(
            message=f"The file '{file_path}' does not exist.",
            suggestions=[
                "Check the file path for typos",
                "Verify the file exists: ls -la path/to/file",
                "Check if you're in the correct directory",
                "The file may have been deleted or moved",
            ],
            commands=[
                f"ls -la {file_path}",
                f"find . -name '{file_path.rsplit('/', maxsplit=1)[-1]}'",
                "pwd  # Check current directory",
            ],
        ),
        context=ErrorContext(operation=operation, file_path=file_path),
        original_exception=original,
        error_code="E005",
    )


def create_file_permission_error(
    file_path: str,
    operation: str = "write",
    original: Exception | None = None,
) -> SageError:
    """Create a file permission error with guidance."""
    return SageError(
        category=ErrorCategory.FILE_PERMISSION,
        severity=ErrorSeverity.ERROR,
        message=f"Permission denied: {file_path}",
        guidance=ErrorGuidance(
            message=f"You don't have permission to {operation} '{file_path}'.",
            suggestions=[
                "Check file permissions: ls -la",
                "You may need to change ownership or permissions",
                "Verify you have write access to the directory",
                "Consider using a different directory",
            ],
            commands=[
                f"ls -la {file_path}",
                f"chmod u+w {file_path}  # Add write permission",
                f"sudo chown $USER {file_path}  # Change ownership (requires sudo)",
            ],
        ),
        context=ErrorContext(operation=operation, file_path=file_path),
        original_exception=original,
        error_code="E006",
    )


def create_command_not_found_error(
    command: str,
    original: Exception | None = None,
) -> SageError:
    """Create a command not found error with guidance."""
    install_hints = {
        "git": "Install git: https://git-scm.com/downloads",
        "python": "Install Python: https://python.org/downloads",
        "node": "Install Node.js: https://nodejs.org",
        "npm": "Install Node.js: https://nodejs.org",
        "cargo": "Install Rust: https://rustup.rs",
        "go": "Install Go: https://golang.org/dl",
        "pip": "pip comes with Python, ensure Python is installed",
        "pytest": "Install pytest: pip install pytest",
    }

    cmd_name = command.split(maxsplit=1)[0] if command else "command"
    hint = install_hints.get(cmd_name, f"Install {cmd_name} and ensure it's in your PATH")

    return SageError(
        category=ErrorCategory.EXEC_NOT_FOUND,
        severity=ErrorSeverity.ERROR,
        message=f"Command not found: {cmd_name}",
        guidance=ErrorGuidance(
            message=f"The command '{cmd_name}' is not installed or not in PATH.",
            suggestions=[
                hint,
                "Check if it's installed: which " + cmd_name,
                "Add to PATH if installed in a custom location",
                "You may need to restart your terminal",
            ],
            commands=[
                f"which {cmd_name}",
                "echo $PATH",
                f"# {hint}",
            ],
        ),
        context=ErrorContext(operation="execute_command", command=command),
        original_exception=original,
        error_code="E007",
    )


def create_command_blocked_error(
    command: str,
    reason: str,
    original: Exception | None = None,
) -> SageError:
    """Create a command blocked error with guidance."""
    return SageError(
        category=ErrorCategory.EXEC_BLOCKED,
        severity=ErrorSeverity.WARNING,
        message=f"Command blocked: {command}",
        guidance=ErrorGuidance(
            message=f"This command was blocked for safety: {reason}",
            suggestions=[
                "SAGE blocks potentially dangerous commands",
                "Review why this command is needed",
                "Consider a safer alternative",
                "If necessary, run manually in your terminal",
            ],
            commands=[
                "# Run manually if you're sure it's safe:",
                f"# {command}",
            ],
            docs_url="https://sageworksai.com/#setup",
        ),
        context=ErrorContext(
            operation="execute_command", command=command, additional={"reason": reason}
        ),
        original_exception=original,
        error_code="E008",
    )


def create_model_not_found_error(
    model_name: str,
    available_models: list[str] | None = None,
    original: Exception | None = None,
) -> SageError:
    """Create a model not found error with guidance."""
    suggestions = [
        f"Model '{model_name}' is not available",
        "Check available models: sage models",
        "Download a model: sage pull model-name",
        "Check model name spelling",
    ]

    if available_models:
        suggestions.append(f"Available models: {', '.join(available_models[:5])}")

    return SageError(
        category=ErrorCategory.MODEL_NOT_FOUND,
        severity=ErrorSeverity.ERROR,
        message=f"Model not found: {model_name}",
        guidance=ErrorGuidance(
            message=f"The model '{model_name}' could not be found.",
            suggestions=suggestions,
            commands=[
                "sage models  # List available models",
                "sage pull --list  # List downloadable models",
                f"sage pull {model_name}  # Download the model",
            ],
            docs_url="https://sageworksai.com/#setup",
        ),
        context=ErrorContext(operation="load_model", model=model_name),
        original_exception=original,
        error_code="E009",
    )


def create_context_overflow_error(
    current_tokens: int,
    max_tokens: int,
    original: Exception | None = None,
) -> SageError:
    """Create a context overflow error with guidance (P0-15: Token usage display)."""
    return SageError(
        category=ErrorCategory.MODEL_CONTEXT_OVERFLOW,
        severity=ErrorSeverity.ERROR,
        message=f"Context overflow: {current_tokens:,} tokens exceeds limit of {max_tokens:,}",
        guidance=ErrorGuidance(
            message="The conversation has exceeded the model's context window.",
            suggestions=[
                "Use /compact to summarize the conversation",
                "Start a new conversation",
                "Use a model with larger context window",
                "Be more concise in your prompts",
            ],
            commands=[
                "/compact  # Compress conversation history",
                "/clear    # Start fresh",
                "sage run --model large-context-model",
            ],
        ),
        context=ErrorContext(
            operation="generate",
            additional={"current_tokens": current_tokens, "max_tokens": max_tokens},
        ),
        original_exception=original,
        error_code="E010",
    )


def create_config_error(
    key: str,
    message: str,
    original: Exception | None = None,
) -> SageError:
    """Create a configuration error with guidance."""
    return SageError(
        category=ErrorCategory.CONFIG_INVALID,
        severity=ErrorSeverity.ERROR,
        message=f"Configuration error for '{key}': {message}",
        guidance=ErrorGuidance(
            message="There's an issue with your SAGE configuration.",
            suggestions=[
                "Review your configuration: sage config show",
                f"Reset the problematic key: sage config set {key} DEFAULT_VALUE",
                "Check config file: ~/.sage/config.json",
                "Reset to defaults: sage config reset",
            ],
            commands=[
                "sage config show",
                f"sage config set {key} VALUE",
                "cat ~/.sage/config.json",
            ],
            docs_url="https://sageworksai.com/#setup",
        ),
        context=ErrorContext(operation="load_config", additional={"key": key}),
        original_exception=original,
        error_code="E011",
    )


# =============================================================================
# Error Display (P0-13: Implement agent phase transparency)
# =============================================================================


class ErrorRenderer:
    """
    Renders errors with rich formatting.

    P0-17: Add input validation with helpful messages
    P0-18: Create troubleshooting documentation links
    P0-19: Add elapsed time to spinners (context shown in errors)
    """

    def __init__(self, console: Console | None = None):
        self.console = console or Console(stderr=True)

    def render(self, error: SageError) -> None:
        """Render an error with full guidance."""
        # Build error title
        severity_colors = {
            ErrorSeverity.DEBUG: "dim",
            ErrorSeverity.INFO: "blue",
            ErrorSeverity.WARNING: "yellow",
            ErrorSeverity.ERROR: "red",
            ErrorSeverity.CRITICAL: "red bold",
        }
        color = severity_colors.get(error.severity, "red")

        # Error message
        title = Text()
        title.append("Error", style=f"{color} bold")
        if error.error_code:
            title.append(f" [{error.error_code}]", style="dim")

        # Build content
        content = Text()
        content.append(error.message, style=color)
        content.append("\n\n")

        # Guidance
        content.append(error.guidance.message, style="white")
        content.append("\n\n")

        # Suggestions
        if error.guidance.suggestions:
            content.append("Suggestions:\n", style="bold")
            for suggestion in error.guidance.suggestions:
                content.append(f"  • {suggestion}\n", style="white")
            content.append("\n")

        # Commands
        if error.guidance.commands:
            content.append("Try:\n", style="bold")
            for cmd in error.guidance.commands:
                if cmd.startswith("#"):
                    content.append(f"  {cmd}\n", style="dim italic")
                else:
                    content.append(f"  $ {cmd}\n", style="cyan")
            content.append("\n")

        # Documentation link
        if error.guidance.docs_url:
            content.append("Documentation: ", style="dim")
            content.append(error.guidance.docs_url, style="blue underline")

        # Render panel
        self.console.print(Panel(content, title=title, border_style=color))

    def render_simple(self, error: SageError) -> None:
        """Render a simple one-line error."""
        self.console.print(f"[red]Error:[/red] {error.message}")
        if error.guidance.suggestions:
            self.console.print(f"[dim]Hint: {error.guidance.suggestions[0]}[/dim]")

    def render_debug(self, error: SageError) -> None:
        """Render error with full debug information."""
        self.render(error)

        if error.original_exception:
            self.console.print("\n[dim]Original exception:[/dim]")
            self.console.print(
                f"[dim]{type(error.original_exception).__name__}: {error.original_exception}[/dim]"
            )

            if error.context:
                self.console.print(f"\n[dim]Context: {error.context}[/dim]")


# Alias for backwards compatibility
ErrorFormatter = ErrorRenderer


# =============================================================================
# Error Handler (P0-14: Add confirmation prompts for destructive operations)
# =============================================================================


class ErrorHandler:
    """
    Central error handler for SAGE.

    Converts exceptions to SageError and handles them appropriately.
    P0-16: Add retry reason logging
    """

    def __init__(
        self,
        renderer: ErrorRenderer | None = None,
        debug: bool = False,
        on_error: Callable[[SageError], None] | None = None,
    ):
        self.renderer = renderer or ErrorRenderer()
        self.debug = debug
        self.on_error = on_error
        self.error_log: list[SageError] = []

    def handle(
        self, error: Exception | SageError, context: ErrorContext | None = None
    ) -> SageError:
        """Handle an error and return the SageError representation."""
        if isinstance(error, SageError):
            sage_error = error
        else:
            sage_error = self._convert_exception(error, context)

        # Log the error
        self.error_log.append(sage_error)

        # Render based on debug mode
        if self.debug:
            self.renderer.render_debug(sage_error)
        else:
            self.renderer.render(sage_error)

        # Call custom handler if set
        if self.on_error:
            self.on_error(sage_error)

        return sage_error

    def _convert_exception(self, exc: Exception, context: ErrorContext | None = None) -> SageError:
        """Convert a standard exception to SageError."""
        exc_type = type(exc).__name__
        exc_msg = str(exc)

        # Network errors
        if "Connection" in exc_type or "connection" in exc_msg.lower():
            return create_network_error(exc_msg, original=exc)

        if "Timeout" in exc_type or "timeout" in exc_msg.lower():
            return create_timeout_error(
                context.operation if context else "unknown",
                60,
                original=exc,
            )

        # File errors
        if isinstance(exc, FileNotFoundError):
            return create_file_not_found_error(
                context.file_path if context else exc_msg,
                original=exc,
            )

        if isinstance(exc, PermissionError):
            return create_file_permission_error(
                context.file_path if context else exc_msg,
                original=exc,
            )

        # Command errors
        if "not found" in exc_msg.lower() and context and context.command:
            return create_command_not_found_error(context.command, original=exc)

        # Default to internal error
        return SageError(
            category=ErrorCategory.INTERNAL_ERROR,
            severity=ErrorSeverity.ERROR,
            message=f"{exc_type}: {exc_msg}",
            guidance=ErrorGuidance(
                message="An unexpected error occurred.",
                suggestions=[
                    "Try the operation again",
                    "Check the logs for more details",
                    "Report this issue if it persists",
                ],
                docs_url="https://sageworksai.com/#setup",
            ),
            context=context,
            original_exception=exc,
            error_code="E999",
        )

    def get_error_summary(self) -> dict[str, int]:
        """Get summary of errors by category."""
        summary: dict[str, int] = {}
        for error in self.error_log:
            cat = error.category.value
            summary[cat] = summary.get(cat, 0) + 1
        return summary


# =============================================================================
# Context Managers
# =============================================================================


class error_boundary:
    """
    Context manager for error handling.

    Usage:
        with error_boundary("loading config"):
            load_config()
    """

    def __init__(
        self,
        operation: str,
        handler: ErrorHandler | None = None,
        reraise: bool = False,
    ):
        self.operation = operation
        self.handler = handler or ErrorHandler()
        self.reraise = reraise
        self.error: SageError | None = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            context = ErrorContext(operation=self.operation)
            self.error = self.handler.handle(exc_val, context)

            if self.reraise:
                return False  # Re-raise the exception
            return True  # Suppress the exception

        return False


# =============================================================================
# Utility Functions (P0-20: Display diff preview before file writes)
# =============================================================================


def format_diff_preview(old_content: str, new_content: str, max_lines: int = 20) -> str:
    """
    Format a diff preview for display.

    P0-20: Display diff preview before file writes
    """
    import difflib

    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="current",
            tofile="new",
            lineterm="",
        )
    )

    if len(diff) > max_lines:
        diff = diff[:max_lines] + [f"\n... and {len(diff) - max_lines} more lines ..."]

    return "".join(diff)


def confirm_destructive_operation(
    operation: str,
    details: str,
    console: Console | None = None,
) -> bool:
    """
    Prompt user to confirm a destructive operation.

    P0-14: Add confirmation prompts for destructive operations
    """
    console = console or Console()

    console.print(f"\n[yellow bold]Warning:[/yellow bold] {operation}")
    console.print(f"[dim]{details}[/dim]\n")

    try:
        response = console.input("[yellow]Continue? [y/N]: [/yellow]")
        return response.lower() in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False


# =============================================================================
# Module-level convenience
# =============================================================================

# Global error handler instance
_global_handler: ErrorHandler | None = None


def get_error_handler() -> ErrorHandler:
    """Get the global error handler."""
    global _global_handler
    if _global_handler is None:
        _global_handler = ErrorHandler()
    return _global_handler


def set_error_handler(handler: ErrorHandler) -> None:
    """Set the global error handler."""
    global _global_handler
    _global_handler = handler


def handle_error(error: Exception | SageError, context: ErrorContext | None = None) -> SageError:
    """Handle an error using the global handler."""
    return get_error_handler().handle(error, context)
