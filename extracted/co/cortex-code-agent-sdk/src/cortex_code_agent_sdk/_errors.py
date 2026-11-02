"""Error types for Cortex Code SDK."""

from __future__ import annotations

from typing import Any


class CortexCodeSDKError(Exception):
    """Base exception for all Cortex Code SDK errors."""


class CLIConnectionError(CortexCodeSDKError):
    """Raised when unable to connect to Cortex Code."""


class CLINotFoundError(CLIConnectionError):
    """Raised when Cortex Code CLI is not found or not installed."""

    def __init__(
        self, message: str = "Cortex Code not found", cli_path: str | None = None
    ):
        if cli_path:
            message = f"{message}: {cli_path}"
        super().__init__(message)


class ProcessError(CortexCodeSDKError):
    """Raised when the CLI process fails."""

    def __init__(
        self, message: str, exit_code: int | None = None, stderr: str | None = None
    ):
        self.exit_code = exit_code
        self.stderr = stderr

        if exit_code is not None:
            message = f"{message} (exit code: {exit_code})"
        if stderr:
            message = f"{message}\nError output: {stderr}"

        super().__init__(message)


class CLIJSONDecodeError(CortexCodeSDKError):
    """Raised when unable to decode JSON from CLI output."""

    def __init__(self, line: str, original_error: Exception):
        self.line = line
        self.original_error = original_error
        super().__init__(f"Failed to decode JSON: {line[:100]}...")


class MessageParseError(CortexCodeSDKError):
    """Raised when unable to parse a message from CLI output."""

    def __init__(self, message: str, data: dict[str, Any] | None = None):
        self.data = data
        super().__init__(message)


class InvalidOptionValueError(CortexCodeSDKError):
    """Raised when an option value would be parsed by the CLI as a flag."""

    def __init__(self, option_name: str, value: object):
        self.option_name = option_name
        self.value = value
        super().__init__(
            f"Invalid value for option '{option_name}': must be a non-empty "
            f"string that does not start with '-'."
        )
