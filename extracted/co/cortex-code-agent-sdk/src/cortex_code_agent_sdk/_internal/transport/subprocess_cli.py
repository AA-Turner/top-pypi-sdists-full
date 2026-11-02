"""Subprocess-based transport for Cortex Code CLI."""

from __future__ import annotations

import asyncio
import atexit
import json
import logging
import os
import platform
import re
import shutil
import signal
import sys
import threading
from collections.abc import AsyncIterator
from contextlib import suppress
from pathlib import Path
from subprocess import PIPE
from typing import Any

from ..._errors import (
    CLIConnectionError,
    CLINotFoundError,
    InvalidOptionValueError,
    ProcessError,
)
from ..._errors import CLIJSONDecodeError as SDKJSONDecodeError
from ...types import CortexCodeAgentOptions
from . import Transport

logger = logging.getLogger(__name__)

_DEFAULT_MAX_BUFFER_SIZE = 1024 * 1024  # 1MB buffer limit
_CLOSE_WAIT_TIMEOUT_SECONDS = 5.0

MINIMUM_CLI_VERSION = "1.0.35"

# Identifier for telemetry: marks outbound Cortex Code traffic originating
# from this SDK in request logs so it can be distinguished from direct CLI
# use. The CLI reads this via `CORTEX_CODE_ENTRYPOINT` and surfaces it as
# the nested `CodingAgent.Entrypoint` field on agent:run requests.
# OriginApplication stays pinned to "cortex-code-cli" (the whole app
# family), while Entrypoint identifies the specific client library.
# Naming mirrors the Claude Code CLI's `CLAUDE_CODE_ENTRYPOINT` convention.
SDK_ENTRYPOINT = "sdk-python"


class SubprocessCLITransport(Transport):
    """Transport that communicates with the Cortex Code CLI via subprocess stdin/stdout."""

    def __init__(
        self,
        options: CortexCodeAgentOptions,
    ):
        self._options = options
        self._cli_path = (
            str(self._options.cli_path)
            if self._options.cli_path is not None
            else self._find_cli()
        )
        self._cwd = str(self._options.cwd) if self._options.cwd else None
        self._process: asyncio.subprocess.Process | None = None
        self._ready = False
        self._exit_error: Exception | None = None
        self._write_lock = asyncio.Lock()
        self._stderr_task: asyncio.Task[None] | None = None
        self._max_buffer_size = (
            self._options.max_buffer_size
            if self._options.max_buffer_size is not None
            else _DEFAULT_MAX_BUFFER_SIZE
        )
        self._atexit_registered = False

    def _find_cli(self) -> str:
        """Find the Cortex Code CLI binary."""
        env_cli = os.environ.get("CORTEX_CODE_CLI_PATH")
        if env_cli:
            resolved_env_cli = Path(env_cli).expanduser()
            if resolved_env_cli.exists() and resolved_env_cli.is_file():
                return str(resolved_env_cli)
            raise CLINotFoundError(
                f"CORTEX_CODE_CLI_PATH points to a missing Cortex Code executable: {resolved_env_cli}"
            )

        # First, check for bundled CLI
        bundled_cli = self._find_bundled_cli()
        if bundled_cli:
            return bundled_cli

        # Fall back to system-wide search
        if cli := shutil.which("cortex"):
            return cli

        # Check default install location from install.sh
        default_bin = Path.home() / ".local" / "bin" / "cortex"
        if default_bin.exists() and default_bin.is_file():
            return str(default_bin)

        raise CLINotFoundError(
            "Cortex Code not found. Install with:\n"
            "  curl -LsS https://ai.snowflake.com/static/cc-scripts/install.sh | sh\n"
            "\nOr provide the executable path via CORTEX_CODE_CLI_PATH or CortexCodeAgentOptions:\n"
            "  CORTEX_CODE_CLI_PATH=/path/to/cortex\n"
            "  CortexCodeAgentOptions(cli_path='/path/to/cortex')"
        )

    def _find_bundled_cli(self) -> str | None:
        """Find bundled CLI binary if it exists."""
        # Determine the CLI binary name based on platform
        cli_name = "cortex.exe" if platform.system() == "Windows" else "cortex"

        # Get the path to the bundled CLI
        # The _bundled directory is in the same package as this module
        bundled_path = Path(__file__).parent.parent.parent / "_bundled" / cli_name

        if bundled_path.exists() and bundled_path.is_file():
            logger.info(f"Using bundled Cortex Code CLI: {bundled_path}")
            return str(bundled_path)

        return None

    @staticmethod
    def _safe_opt(name: str, value: object) -> str:
        """G-051: Reject option values that the CLI would re-parse as a flag."""
        if not isinstance(value, str) or not value or value.startswith("-"):
            raise InvalidOptionValueError(name, value)
        return value

    def _build_command(self) -> list[str]:
        """Build CLI command with arguments."""
        cmd = [
            self._cli_path,
            "--output-format", "stream-json",
            "--input-format", "stream-json",
        ]

        if self._cwd:
            cmd.extend(["--workdir", self._safe_opt("cwd", self._cwd)])

        # Handle permission modes properly
        # Validate permission options
        if self._options.permission_mode == "bypassPermissions":
            if not self._options.allow_dangerously_skip_permissions:
                raise ValueError(
                    "Must set allow_dangerously_skip_permissions=True "
                    "when using permission_mode='bypassPermissions'"
                )

        # Only bypass when explicitly requested with bypassPermissions mode.
        if self._options.permission_mode == "bypassPermissions":
            cmd.append("--dangerously-allow-all-tool-calls")

        # TODO: add --verbose support to coco CLI
        # TODO: add --system-prompt support to coco CLI
        # if self._options.system_prompt is None:
        #     cmd.extend(["--system-prompt", ""])
        # elif isinstance(self._options.system_prompt, str):
        #     cmd.extend(["--system-prompt", self._options.system_prompt])
        # else:
        #     if (
        #         self._options.system_prompt.get("type") == "preset"
        #         and "append" in self._options.system_prompt
        #     ):
        #         cmd.extend(
        #             ["--append-system-prompt", self._options.system_prompt["append"]]
        #         )

        # TODO: add --tools support to coco CLI
        # if self._options.tools is not None:
        #     tools = self._options.tools
        #     if isinstance(tools, list):
        #         if len(tools) == 0:
        #             cmd.extend(["--tools", ""])
        #         else:
        #             cmd.extend(["--tools", ",".join(tools)])
        #     else:
        #         cmd.extend(["--tools", "default"])

        # coco uses --allowed-tools (array) not --allowedTools (comma-sep)
        if self._options.allowed_tools:
            for tool in self._options.allowed_tools:
                cmd.extend(["--allowed-tools", self._safe_opt("allowed_tools", tool)])

        # coco uses --disallowed-tools (array) not --disallowedTools (comma-sep)
        if self._options.disallowed_tools:
            for tool in self._options.disallowed_tools:
                cmd.extend(
                    ["--disallowed-tools", self._safe_opt("disallowed_tools", tool)]
                )

        if self._options.max_turns is not None:
            cmd.extend(["--max-turns", str(self._options.max_turns)])

        if self._options.model:
            cmd.extend(["--model", self._safe_opt("model", self._options.model)])

        if self._options.permission_prompt_tool_name:
            cmd.extend(
                ["--permission-prompt-tool", self._options.permission_prompt_tool_name]
            )

        if self._options.permission_mode == "plan":
            cmd.append("--plan")
        elif self._options.permission_mode == "autoAcceptPlans":
            cmd.append("--auto-accept-plans")

        if self._options.continue_conversation:
            cmd.append("--continue")

        if self._options.resume:
            cmd.extend(["--resume", self._safe_opt("resume", self._options.resume)])

        if self._options.add_dirs:
            for d in self._options.add_dirs:
                cmd.extend(["--add-dir", self._safe_opt("add_dirs", str(d))])

        if self._options.mcp_servers and isinstance(self._options.mcp_servers, dict):
            servers_for_cli: dict[str, Any] = {}
            for name, config in self._options.mcp_servers.items():
                if isinstance(config, dict) and config.get("type") == "sdk":
                    sdk_config: dict[str, object] = {
                        k: v for k, v in config.items() if k != "instance"
                    }
                    servers_for_cli[name] = sdk_config
                else:
                    servers_for_cli[name] = config
            if servers_for_cli:
                cmd.extend(
                    ["--mcp-config", json.dumps({"mcpServers": servers_for_cli})]
                )

        if self._options.include_partial_messages:
            cmd.append("--include-partial-messages")

        if self._options.fork_session:
            cmd.append("--fork-session")

        if self._options.resume_session_at:
            cmd.extend(
                [
                    "--resume-session-at",
                    self._safe_opt(
                        "resume_session_at", self._options.resume_session_at
                    ),
                ]
            )

        if self._options.no_mcp:
            cmd.append("--no-mcp")

        if self._options.connection:
            cmd.extend(
                ["--connection", self._safe_opt("connection", self._options.connection)]
            )

        if self._options.profile:
            cmd.extend(
                ["--profile", self._safe_opt("profile", self._options.profile)]
            )

        if self._options.session_id:
            cmd.extend(
                ["--session-id", self._safe_opt("session_id", self._options.session_id)]
            )

        if self._options.setting_sources is not None:
            cmd.extend(["--setting-sources", ",".join(self._options.setting_sources)])

        # Add plugin directories
        if self._options.plugins:
            for plugin in self._options.plugins:
                if plugin["type"] == "local":
                    cmd.extend(
                        ["--plugin-dir", self._safe_opt("plugins.path", plugin["path"])]
                    )
                else:
                    raise ValueError(f"Unsupported plugin type: {plugin['type']}")

        # Add extra args for future CLI flags
        for key, value in self._options.extra_args.items():
            if value is None:
                cmd.append(f"--{key}")
            else:
                cmd.extend([f"--{key}", str(value)])

        if self._options.effort is not None:
            cmd.extend(["--effort", self._options.effort])

        if (
            self._options.output_format is not None
            and isinstance(self._options.output_format, dict)
            and self._options.output_format.get("type") == "json_schema"
        ):
            schema = self._options.output_format.get("schema")
            if schema is not None:
                cmd.extend(["--json-schema", json.dumps(schema)])

        if (
            self._options.snowflake_sandbox is not None
            and self._options.snowflake_sandbox.enabled
        ):
            cmd.append("--snowflake-sandbox")

        return cmd

    def _build_env(self) -> dict[str, str]:
        """Build the environment for the spawned CLI."""
        auto_env: dict[str, str] = {}
        if (
            self._options.snowflake_sandbox is not None
            and self._options.snowflake_sandbox.enabled
        ):
            auto_env["ENABLE_COCO_CNG_SANDBOX"] = "1"

        return {
            **os.environ,
            **auto_env,
            **self._options.env,
            "CORTEX_CODE_ENTRYPOINT": SDK_ENTRYPOINT,
        }

    async def connect(self) -> None:
        """Start subprocess."""
        if self._process:
            return

        if not os.environ.get("CORTEX_CODE_AGENT_SDK_SKIP_VERSION_CHECK"):
            await self._check_coco_version()

        cmd = self._build_command()
        try:
            process_env = self._build_env()

            if self._cwd:
                process_env["PWD"] = self._cwd

            # Pipe stderr if we have a callback OR debug mode is enabled
            should_pipe_stderr = (
                self._options.stderr is not None
                or "debug-to-stderr" in self._options.extra_args
            )

            stderr_dest = PIPE if should_pipe_stderr else None

            self._process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=stderr_dest,
                cwd=self._cwd,
                env=process_env,
                user=self._options.user,
            )

            if should_pipe_stderr and self._process.stderr:
                self._stderr_task = asyncio.create_task(self._handle_stderr())

            self._ready = True
            self._register_cleanup()

        except FileNotFoundError as e:
            if self._cwd and not Path(self._cwd).exists():
                error = CLIConnectionError(
                    f"Working directory does not exist: {self._cwd}"
                )
                self._exit_error = error
                raise error from e
            error = CLINotFoundError(f"Cortex Code not found at: {self._cli_path}")
            self._exit_error = error
            raise error from e
        except Exception as e:
            error = CLIConnectionError(f"Failed to start Cortex Code: {e}")
            self._exit_error = error
            raise error from e

    def _cleanup_process(self) -> None:
        """Kill the child process synchronously (for use in atexit/signal handlers)."""
        if self._process and self._process.returncode is None:
            with suppress(ProcessLookupError, OSError):
                self._process.kill()

    def _register_cleanup(self) -> None:
        """Register atexit and signal handlers to kill the child process on exit."""
        if self._atexit_registered:
            return
        atexit.register(self._cleanup_process)
        self._atexit_registered = True

    def _unregister_cleanup(self) -> None:
        """Remove the atexit handler after a clean close."""
        if not self._atexit_registered:
            return
        with suppress(Exception):
            atexit.unregister(self._cleanup_process)
        self._atexit_registered = False

    async def _handle_stderr(self) -> None:
        """Handle stderr stream - read and invoke callbacks."""
        if not self._process or not self._process.stderr:
            return
        try:
            while True:
                line = await self._process.stderr.readline()
                if not line:
                    break
                line_str = line.decode(errors="replace").rstrip()
                if not line_str:
                    continue

                # Call the stderr callback if provided
                if self._options.stderr:
                    self._options.stderr(line_str)
        except Exception:
            pass

    async def _check_coco_version(self) -> None:
        """Check Cortex Code CLI version and warn if below minimum."""
        version_process = None
        try:
            version_process = await asyncio.wait_for(
                asyncio.create_subprocess_exec(
                    self._cli_path, "-v",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                ),
                timeout=2.0,
            )
            if version_process.stdout:
                stdout_bytes = await asyncio.wait_for(
                    version_process.stdout.read(), timeout=2.0
                )
                version_output = stdout_bytes.decode().strip()
                match = re.match(r"([0-9]+\.[0-9]+\.[0-9]+)", version_output)
                if match:
                    version = match.group(1)
                    version_parts = [int(x) for x in version.split(".")]
                    # Dev builds use 0.YY.MMDD versioning (see
                    # coco/src/utils/version.ts). Skip the minimum-version
                    # check for them — a developer running their own build is
                    # by definition opting in to a pre-release version.
                    if version_parts[0] == 0:
                        return
                    min_parts = [int(x) for x in MINIMUM_CLI_VERSION.split(".")]
                    if version_parts < min_parts:
                        raise CLINotFoundError(
                            f"Cortex Code v{version} is too old. "
                            f"Minimum required: v{MINIMUM_CLI_VERSION}. "
                            f"Update with:\n"
                            f"  curl -LsS https://ai.snowflake.com/static/cc-scripts/install.sh | CORTEX_CHANNEL=beta sh"
                        )
        except Exception:
            pass
        finally:
            if version_process:
                with suppress(Exception):
                    version_process.terminate()
                with suppress(Exception):
                    await version_process.wait()

    async def write(self, data: str) -> None:
        """Write data to stdin."""
        async with self._write_lock:
            if not self._ready or not self._process or not self._process.stdin:
                raise CLIConnectionError("ProcessTransport is not ready for writing")

            if self._process.returncode is not None:
                raise CLIConnectionError(
                    f"Cannot write to terminated process (exit code: {self._process.returncode})"
                )

            if self._exit_error:
                raise CLIConnectionError(
                    f"Cannot write to process that exited with error: {self._exit_error}"
                ) from self._exit_error

            try:
                self._process.stdin.write(data.encode())
                await self._process.stdin.drain()
            except Exception as e:
                self._ready = False
                self._exit_error = CLIConnectionError(
                    f"Failed to write to process stdin: {e}"
                )
                raise self._exit_error from e

    def read_messages(self) -> AsyncIterator[dict[str, Any]]:
        """Read and parse messages from the transport."""
        return self._read_messages_impl()

    async def _read_messages_impl(self) -> AsyncIterator[dict[str, Any]]:
        """Internal implementation of read_messages."""
        if not self._process or not self._process.stdout:
            raise CLIConnectionError("Not connected")

        json_buffer = ""

        # Process stdout messages
        try:
            while True:
                chunk = await self._process.stdout.read(65536)
                if not chunk:
                    break
                line_str = chunk.decode().strip()
                if not line_str:
                    continue

                # Accumulate partial JSON until we can parse it.
                # Note: reads can truncate long lines, so we need to buffer
                # and speculatively parse until we get a complete JSON object.
                json_lines = line_str.split("\n")

                for json_line in json_lines:
                    json_line = json_line.strip()
                    if not json_line:
                        continue

                    # Keep accumulating partial JSON until we can parse it
                    json_buffer += json_line

                    if len(json_buffer) > self._max_buffer_size:
                        buffer_length = len(json_buffer)
                        json_buffer = ""
                        raise SDKJSONDecodeError(
                            f"JSON message exceeded maximum buffer size of {self._max_buffer_size} bytes",
                            ValueError(
                                f"Buffer size {buffer_length} exceeds limit {self._max_buffer_size}"
                            ),
                        )

                    try:
                        data = json.loads(json_buffer)
                        json_buffer = ""
                        yield data
                    except json.JSONDecodeError:
                        # We are speculatively decoding the buffer until we get
                        # a full JSON object. If there is an actual issue, we
                        # raise an error after exceeding the configured limit.
                        continue

        except GeneratorExit:
            # Client disconnected
            pass

        # Check process completion and handle errors
        try:
            returncode = await self._process.wait()
        except Exception:
            returncode = -1

        # Use exit code for error detection
        if returncode is not None and returncode != 0:
            self._exit_error = ProcessError(
                f"Command failed with exit code {returncode}",
                exit_code=returncode,
                stderr="Check stderr output for details",
            )
            raise self._exit_error

    async def close(self) -> None:
        """Close the transport and clean up resources."""
        if not self._process:
            self._ready = False
            return

        # Cancel stderr task if active
        if self._stderr_task:
            self._stderr_task.cancel()
            try:
                await self._stderr_task
            except (asyncio.CancelledError, Exception):
                pass
            self._stderr_task = None

        # Close stdin (acquire lock to prevent race with concurrent writes)
        async with self._write_lock:
            self._ready = False  # Set inside lock to prevent TOCTOU with write()
            if self._process and self._process.stdin:
                with suppress(Exception):
                    self._process.stdin.close()

        # Give the CLI a short window to exit on its own — it needs time to
        # flush session metadata to disk (see streamJsonHandler.flushAllWrites).
        # If it hasn't exited by then, fall through to terminate().
        if self._process.returncode is None:
            with suppress(asyncio.TimeoutError, Exception):
                await asyncio.wait_for(self._process.wait(), timeout=2.0)

        # Terminate and wait for process
        if self._process.returncode is None:
            with suppress(ProcessLookupError):
                self._process.terminate()
                try:
                    await asyncio.wait_for(
                        self._process.wait(),
                        timeout=_CLOSE_WAIT_TIMEOUT_SECONDS,
                    )
                except (asyncio.TimeoutError, ProcessLookupError):
                    with suppress(ProcessLookupError):
                        self._process.kill()
                    with suppress(Exception):
                        await asyncio.wait_for(
                            self._process.wait(),
                            timeout=_CLOSE_WAIT_TIMEOUT_SECONDS,
                        )

        self._process = None
        self._exit_error = None
        self._unregister_cleanup()

    @property
    def pid(self) -> int | None:
        """Process ID of the underlying CLI process."""
        if self._process and self._process.pid is not None:
            return self._process.pid
        return None

    def is_ready(self) -> bool:
        """Check if transport is ready for communication."""
        return self._ready

    async def end_input(self) -> None:
        """End the input stream (close stdin)."""
        async with self._write_lock:
            if self._process and self._process.stdin:
                with suppress(Exception):
                    self._process.stdin.close()
