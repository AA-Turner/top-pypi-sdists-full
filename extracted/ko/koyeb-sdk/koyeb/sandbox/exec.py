# coding: utf-8

"""
Command execution utilities for Koyeb Sandbox instances
Using SandboxClient HTTP API
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from .executor_client import AsyncSandboxClient, SandboxClient
from .utils import SandboxError

if TYPE_CHECKING:
    from .sandbox import Sandbox


class CommandStatus(str, Enum):
    """Command execution status"""

    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"


@dataclass
class CommandResult:
    """Result of a command execution using Koyeb API models"""

    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    status: CommandStatus = CommandStatus.FINISHED
    duration: float = 0.0
    command: str = ""
    args: Optional[List[str]] = None

    def __post_init__(self):
        if self.args is None:
            self.args = []

    @property
    def success(self) -> bool:
        """Check if command executed successfully"""
        return self.exit_code == 0 and self.status == CommandStatus.FINISHED

    @property
    def output(self) -> str:
        """Get combined stdout and stderr output"""
        return self.stdout + (f"\n{self.stderr}" if self.stderr else "")


class SandboxCommandError(SandboxError):
    """Raised when command execution fails"""


class SandboxExecutor:
    """
    Synchronous command execution interface for Koyeb Sandbox instances.
    Bound to a specific sandbox instance.

    For async usage, use AsyncSandboxExecutor instead.
    """

    def __init__(self, sandbox: Sandbox) -> None:
        self.sandbox = sandbox

    def _get_client(self) -> SandboxClient:
        """Get or create SandboxClient instance, shared with the sandbox"""
        return self.sandbox._get_client()

    def __call__(
        self,
        command: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        on_stdout: Optional[Callable[[str], None]] = None,
        on_stderr: Optional[Callable[[str], None]] = None,
    ) -> CommandResult:
        """
        Execute a command in a shell synchronously. Supports streaming output via callbacks.

        Args:
            command: Command to execute as a string (e.g., "python -c 'print(2+2)'")
            cwd: Working directory for the command
            env: Environment variables for the command
            timeout: Command timeout in seconds (enforced for HTTP requests)
            on_stdout: Optional callback for streaming stdout chunks
            on_stderr: Optional callback for streaming stderr chunks

        Returns:
            CommandResult: Result of the command execution

        Example:
            ```python
            # Synchronous execution
            result = sandbox.exec("echo hello")

            # With streaming callbacks
            result = sandbox.exec(
                "echo hello; sleep 1; echo world",
                on_stdout=lambda data: print(f"OUT: {data}"),
                on_stderr=lambda data: print(f"ERR: {data}"),
            )
            ```
        """
        start_time = time.time()

        # Use streaming if callbacks are provided
        if on_stdout or on_stderr:
            stdout_buffer = []
            stderr_buffer = []
            exit_code = 0

            try:
                client = self._get_client()
                for event in client.run_streaming(
                    cmd=command, cwd=cwd, env=env, timeout=float(timeout)
                ):
                    if "stream" in event:
                        stream_type = event["stream"]
                        data = event["data"]

                        if stream_type == "stdout":
                            stdout_buffer.append(data)
                            if on_stdout:
                                on_stdout(data)
                        elif stream_type == "stderr":
                            stderr_buffer.append(data)
                            if on_stderr:
                                on_stderr(data)
                    elif "code" in event:
                        exit_code = event["code"]
                    elif "error" in event and isinstance(event["error"], str):
                        # Error starting command
                        return CommandResult(
                            stdout="",
                            stderr=event["error"],
                            exit_code=1,
                            status=CommandStatus.FAILED,
                            duration=time.time() - start_time,
                            command=command,
                        )

                return CommandResult(
                    stdout="".join(stdout_buffer),
                    stderr="".join(stderr_buffer),
                    exit_code=exit_code,
                    status=(
                        CommandStatus.FINISHED
                        if exit_code == 0
                        else CommandStatus.FAILED
                    ),
                    duration=time.time() - start_time,
                    command=command,
                )
            except Exception as e:
                return CommandResult(
                    stdout="",
                    stderr=f"Command execution failed: {str(e)}",
                    exit_code=1,
                    status=CommandStatus.FAILED,
                    duration=time.time() - start_time,
                    command=command,
                )

        # Use regular run for non-streaming execution
        try:
            client = self._get_client()
            response = client.run(cmd=command, cwd=cwd, env=env, timeout=float(timeout))

            stdout = response.get("stdout", "")
            stderr = response.get("stderr", "")
            exit_code = response.get("code", 0)

            return CommandResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                status=(
                    CommandStatus.FINISHED if exit_code == 0 else CommandStatus.FAILED
                ),
                duration=time.time() - start_time,
                command=command,
            )
        except Exception as e:
            return CommandResult(
                stdout="",
                stderr=f"Command execution failed: {str(e)}",
                exit_code=1,
                status=CommandStatus.FAILED,
                duration=time.time() - start_time,
                command=command,
            )


class AsyncSandboxExecutor(SandboxExecutor):
    """
    Async command execution interface for Koyeb Sandbox instances.
    Bound to a specific sandbox instance.

    Inherits from SandboxExecutor and provides async command execution
    using native async I/O via AsyncSandboxClient.
    """

    def _get_async_client(self) -> AsyncSandboxClient:
        """Get AsyncSandboxClient instance from the sandbox."""
        return self.sandbox._get_async_client()

    async def __call__(
        self,
        command: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        on_stdout: Optional[Callable[[str], None]] = None,
        on_stderr: Optional[Callable[[str], None]] = None,
    ) -> CommandResult:
        """
        Execute a command in a shell asynchronously. Supports streaming output via callbacks.

        Args:
            command: Command to execute as a string (e.g., "python -c 'print(2+2)'")
            cwd: Working directory for the command
            env: Environment variables for the command
            timeout: Command timeout in seconds (enforced for HTTP requests)
            on_stdout: Optional callback for streaming stdout chunks
            on_stderr: Optional callback for streaming stderr chunks

        Returns:
            CommandResult: Result of the command execution

        Example:
            ```python
            # Async execution
            result = await sandbox.exec("echo hello")

            # With streaming callbacks
            result = await sandbox.exec(
                "echo hello; sleep 1; echo world",
                on_stdout=lambda data: print(f"OUT: {data}"),
                on_stderr=lambda data: print(f"ERR: {data}"),
            )
            ```
        """
        start_time = time.time()

        # Use streaming if callbacks are provided
        if on_stdout or on_stderr:
            stdout_buffer: List[str] = []
            stderr_buffer: List[str] = []
            exit_code = 0

            try:
                client = self._get_async_client()

                async for event in client.run_streaming(
                    cmd=command, cwd=cwd, env=env, timeout=float(timeout)
                ):
                    if "stream" in event:
                        stream_type = event["stream"]
                        data = event["data"]

                        if stream_type == "stdout":
                            stdout_buffer.append(data)
                            if on_stdout:
                                on_stdout(data)
                        elif stream_type == "stderr":
                            stderr_buffer.append(data)
                            if on_stderr:
                                on_stderr(data)
                    elif "code" in event:
                        exit_code = event["code"]
                    elif "error" in event and isinstance(event["error"], str):
                        return CommandResult(
                            stdout="",
                            stderr=event["error"],
                            exit_code=1,
                            status=CommandStatus.FAILED,
                            duration=time.time() - start_time,
                            command=command,
                        )

                return CommandResult(
                    stdout="".join(stdout_buffer),
                    stderr="".join(stderr_buffer),
                    exit_code=exit_code,
                    status=(
                        CommandStatus.FINISHED
                        if exit_code == 0
                        else CommandStatus.FAILED
                    ),
                    duration=time.time() - start_time,
                    command=command,
                )
            except Exception as e:
                return CommandResult(
                    stdout="",
                    stderr=f"Command execution failed: {str(e)}",
                    exit_code=1,
                    status=CommandStatus.FAILED,
                    duration=time.time() - start_time,
                    command=command,
                )

        # Use native async for non-streaming execution
        try:
            client = self._get_async_client()
            response = await client.run(
                cmd=command, cwd=cwd, env=env, timeout=float(timeout)
            )

            stdout = response.get("stdout", "")
            stderr = response.get("stderr", "")
            exit_code = response.get("code", 0)

            return CommandResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                status=(
                    CommandStatus.FINISHED if exit_code == 0 else CommandStatus.FAILED
                ),
                duration=time.time() - start_time,
                command=command,
            )
        except Exception as e:
            return CommandResult(
                stdout="",
                stderr=f"Command execution failed: {str(e)}",
                exit_code=1,
                status=CommandStatus.FAILED,
                duration=time.time() - start_time,
                command=command,
            )
