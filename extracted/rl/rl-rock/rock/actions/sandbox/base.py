from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from .request import (
    Action,
    CloseSessionRequest,
    Command,
    CreateSessionRequest,
    ReadFileRequest,
    UploadRequest,
    WriteFileRequest,
)
from .response import (
    CloseResponse,
    CloseSessionResponse,
    CommandResponse,
    CreateSessionResponse,
    IsAliveResponse,
    Observation,
    ReadFileResponse,
    UploadResponse,
    WriteFileResponse,
)


class _ExceptionTransfer(BaseModel):
    """Helper class to transfer exception information from remote runtime to client."""

    message: str = ""
    """Exception message."""

    class_path: str = ""
    """Full class path of the exception type."""

    traceback: str = ""
    """Exception traceback information."""

    extra_info: dict[str, Any] = {}
    """Additional exception context and metadata."""


class AbstractSandbox(ABC):
    """Abstract base class for sandbox runtime implementations.

    This is the main entry point for executing commands and managing sessions
    in different sandbox environments. It provides a unified interface for
    interacting with both local and remote sandbox runtimes.

    The sandbox manages multiple sessions (individual REPLs or shells) that
    can be created, used for command execution, and closed independently.
    """

    @abstractmethod
    async def is_alive(self, *, timeout: float | None = None) -> IsAliveResponse:
        """Check if the sandbox runtime is alive and responsive.

        Args:
            timeout: Maximum time to wait for response in seconds.

        Returns:
            IsAliveResponse indicating the runtime status.
        """
        pass

    @abstractmethod
    async def create_session(self, request: CreateSessionRequest) -> CreateSessionResponse:
        """Create a new interactive session (e.g., bash shell, Python REPL).

        Args:
            request: Configuration for the new session.

        Returns:
            CreateSessionResponse with session details.
        """
        pass

    @abstractmethod
    async def run_in_session(self, action: Action) -> Observation:
        """Execute an action within an existing session.

        The target session is determined by the `session` field in the Action.

        Args:
            action: Action to execute (command, interrupt, etc.).

        Returns:
            Observation containing the execution results.
        """
        pass

    @abstractmethod
    async def close_session(self, request: CloseSessionRequest) -> CloseSessionResponse:
        """Close an existing interactive session.

        Args:
            request: Details of the session to close.

        Returns:
            CloseSessionResponse confirming session closure.
        """
        pass

    @abstractmethod
    async def execute(self, command: Command) -> CommandResponse:
        """Execute a one-time command in a subprocess.

        This is similar to `subprocess.run()` - creates a new process,
        runs the command, and returns the result.

        Args:
            command: Command to execute.

        Returns:
            CommandResponse with execution results.
        """
        pass

    @abstractmethod
    async def read_file(self, request: ReadFileRequest) -> ReadFileResponse:
        """Read file content and return as string.

        Args:
            request: File read configuration including path and encoding.

        Returns:
            ReadFileResponse containing the file content.
        """
        pass

    @abstractmethod
    async def write_file(self, request: WriteFileRequest) -> WriteFileResponse:
        """Write string content to a file.

        Args:
            request: File write configuration including path and content.

        Returns:
            WriteFileResponse confirming the write operation.
        """
        pass

    @abstractmethod
    async def upload(self, request: UploadRequest) -> UploadResponse:
        """Upload a file from local machine to the sandbox environment.

        Args:
            request: Upload configuration with source and target paths.

        Returns:
            UploadResponse confirming the upload operation.
        """
        pass

    @abstractmethod
    async def close(self) -> CloseResponse:
        """Close the sandbox runtime and clean up resources.

        Returns:
            CloseResponse confirming the runtime closure.
        """
        pass
