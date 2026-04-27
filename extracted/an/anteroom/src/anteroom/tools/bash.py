"""Shell command execution tool."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
import time
from typing import TYPE_CHECKING, Any

from ..services.diagnostic_context import log_debug
from .security import (
    check_blocked_path,
    check_custom_patterns,
    check_network_command,
    check_package_install,
    sanitize_command,
)

if TYPE_CHECKING:
    from ..config import BashSandboxConfig

import re
import shutil
import tempfile

logger = logging.getLogger(__name__)
security_logger = logging.getLogger("anteroom.security")

_MAX_OUTPUT = 100_000
_DEFAULT_TIMEOUT = 120

# Regex to detect `python -c "..."` or `python3 -c '...'` with multiline content
_PYTHON_C_RE = re.compile(
    r"""^(python3?)\s+-c\s+(['"])(.*)\2\s*$""",
    re.DOTALL,
)

_working_dir: str = os.getcwd()

DEFINITION: dict[str, Any] = {
    "name": "bash",
    "description": (
        "Execute a shell command and return stdout, stderr, and exit code. "
        "Commands run in the working directory. Default timeout is 120 seconds. "
        "For commands expected to take over 30 seconds, use background: true."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "The shell command to execute"},
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds (default 120, max 600)",
                "default": 120,
            },
            "background": {
                "type": "boolean",
                "description": (
                    "Run in background and return immediately with a task ID. "
                    "Use for long-running commands like test suites."
                ),
                "default": False,
            },
        },
        "required": ["command"],
    },
}

BACKGROUND_STATUS_DEFINITION: dict[str, Any] = {
    "name": "bash_background_status",
    "description": "Check the status and output preview of a background shell task.",
    "parameters": {
        "type": "object",
        "properties": {
            "task_id": {"type": "string", "description": "Background task ID to check"},
        },
        "required": ["task_id"],
    },
}


def set_working_dir(d: str) -> None:
    global _working_dir
    _working_dir = d


def _check_sandbox(command: str, config: BashSandboxConfig) -> str | None:
    """Run all sandbox checks. Returns error message if blocked, None if allowed."""
    if not config.allow_network:
        desc = check_network_command(command)
        if desc:
            return f"Network commands are blocked ({desc})"

    if not config.allow_package_install:
        desc = check_package_install(command)
        if desc:
            return f"Package installation is blocked ({desc})"

    if config.blocked_paths:
        desc = check_blocked_path(command, config.blocked_paths)
        if desc:
            return f"Blocked: {desc}"

    if config.blocked_commands:
        desc = check_custom_patterns(command, config.blocked_commands)
        if desc:
            return f"Blocked: {desc}"

    return None


def _rewrite_python_c_for_windows(command: str) -> tuple[str, str | None]:
    """On Windows, rewrite multiline ``python -c`` to a temp .py file.

    Returns (possibly rewritten command, temp_file_path or None).
    The caller is responsible for cleaning up the temp file.
    """
    m = _PYTHON_C_RE.match(command.strip())
    if not m:
        return command, None

    python_bin = m.group(1)
    script_body = m.group(3)

    # Only rewrite if the script is multiline (contains actual newlines)
    if "\n" not in script_body:
        return command, None

    # Write to a temp file (suffix .py so Windows knows it's Python)
    fd, tmp_path = tempfile.mkstemp(suffix=".py", prefix="anteroom_")
    try:
        os.write(fd, script_body.encode("utf-8"))
    finally:
        os.close(fd)

    return f'{python_bin} "{tmp_path}"', tmp_path


def _resolve_python_binary(command: str) -> str:
    """On Windows, rewrite ``python3`` to ``python`` if python3 is not on PATH."""
    if sys.platform != "win32":
        return command
    if not command.lstrip().startswith("python3"):
        return command
    if shutil.which("python3") is not None:
        return command
    if shutil.which("python") is None:
        return command
    return re.sub(r"\bpython3\b", "python", command, count=1)


async def handle(
    command: str,
    timeout: int = _DEFAULT_TIMEOUT,
    _bypass_hard_block: bool = False,
    _sandbox_config: BashSandboxConfig | None = None,
    _env: dict[str, str] | None = None,
    _background: bool = False,
    _bg_manager: Any = None,
    _conversation_id: str = "",
    _db: Any = None,
    _cancel_event: Any = None,
    _force_cancel_event: Any = None,
    **_: Any,
) -> dict[str, Any]:
    started_at = time.monotonic()
    # Null byte check runs unconditionally — never bypassable.
    if "\x00" in command:
        log_debug(
            logger,
            "tool.bash.failure",
            lifecycle="failure",
            phase="tool_exec",
            tool_name="bash",
            status="invalid_input",
            error_class="ValueError",
            _started_at=started_at,
        )
        return {"error": "Command contains null bytes", "exit_code": -1}
    if not _bypass_hard_block:
        command, error = sanitize_command(command)
        if error:
            log_debug(
                logger,
                "tool.bash.failure",
                lifecycle="failure",
                phase="tool_exec",
                tool_name="bash",
                status="sanitized_block",
                _started_at=started_at,
            )
            return {"error": error, "exit_code": -1}

    # Apply sandbox restrictions (runs even when hard-block is bypassed)
    if _sandbox_config is not None:
        sandbox_error = _check_sandbox(command, _sandbox_config)
        if sandbox_error:
            log_debug(
                logger,
                "tool.bash.failure",
                lifecycle="failure",
                phase="tool_exec",
                tool_name="bash",
                status="sandbox_blocked",
                _started_at=started_at,
            )
            security_logger.warning("Sandbox blocked: %s — %s", sandbox_error, command[:100])
            return {"error": sandbox_error, "exit_code": -1}
        max_timeout = _sandbox_config.timeout
        max_output = _sandbox_config.max_output_chars
    else:
        max_timeout = 600
        max_output = _MAX_OUTPUT

    timeout = min(max(1, timeout), max_timeout)
    log_debug(
        logger,
        "tool.bash.start",
        lifecycle="start",
        phase="tool_exec",
        tool_name="bash",
        background=_background,
        timeout_seconds=timeout,
        working_dir_set=bool(_working_dir),
    )

    # Log command if configured
    if _sandbox_config is not None and _sandbox_config.log_all_commands:
        security_logger.info("bash command: %s", command[:500])

    # Windows: rewrite python3 → python if needed, and multiline python -c to temp file
    tmp_script: str | None = None
    if sys.platform == "win32":
        command = _resolve_python_binary(command)
        command, tmp_script = _rewrite_python_c_for_windows(command)

    # Background execution (#1311) — runs AFTER all safety checks and
    # Windows rewrites above, so the detached subprocess matches the
    # foreground path in every respect except output collection.
    if _background:
        if _bg_manager is None:
            log_debug(
                logger,
                "tool.bash.failure",
                lifecycle="failure",
                phase="tool_exec",
                tool_name="bash",
                status="background_unavailable",
                _started_at=started_at,
            )
            return {"error": "Background execution not available in this context", "exit_code": -1}
        try:
            task = _bg_manager.start_task(
                _conversation_id,
                command,
                timeout=timeout,
                env=_env,
                cwd=_working_dir,
                db=_db,
                sandbox_config=_sandbox_config,
            )
            task_result = dict(task)
            task_result["_end_turn"] = True
            log_debug(
                logger,
                "tool.bash.success",
                lifecycle="success",
                phase="tool_exec",
                tool_name="bash",
                status="background_started",
                background=True,
                _started_at=started_at,
            )
            return task_result
        except ValueError as exc:
            log_debug(
                logger,
                "tool.bash.failure",
                lifecycle="failure",
                phase="tool_exec",
                tool_name="bash",
                status="background_failed",
                error_class=type(exc).__name__,
                _started_at=started_at,
            )
            return {"error": str(exc), "exit_code": -1}

    # Set up OS-level sandbox (Win32 Job Object) if configured
    use_os_sandbox = sys.platform == "win32" and _sandbox_config is not None and _sandbox_config.sandbox.is_enabled

    try:
        # Merge per-step credential env if provided (#970)
        subprocess_env = {**os.environ, **_env} if _env else None

        proc = await asyncio.create_subprocess_shell(
            command,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=_working_dir,
            env=subprocess_env,
        )

        # Assign process to Job Object for kernel-level resource limits
        job_handle: int | None = None
        if use_os_sandbox and proc.pid is not None:
            from .sandbox_win32 import setup_job_for_process

            job_handle = setup_job_for_process(_sandbox_config.sandbox, proc.pid)  # type: ignore[union-attr]
            if job_handle is None:
                security_logger.warning("Job Object setup failed, running without OS sandbox")

        try:
            comm_task = asyncio.create_task(proc.communicate())
            wait_set: set[asyncio.Task[Any]] = {comm_task, asyncio.create_task(asyncio.sleep(timeout))}
            cancel_wait: asyncio.Task[Any] | None = None
            if _cancel_event is not None:
                cancel_wait = asyncio.create_task(_cancel_event.wait())
                wait_set.add(cancel_wait)
            done, pending = await asyncio.wait(wait_set, return_when=asyncio.FIRST_COMPLETED)
            for p in pending:
                p.cancel()
            if comm_task in done:
                stdout, stderr = comm_task.result()
            elif cancel_wait is not None and cancel_wait in done:
                log_debug(
                    logger,
                    "tool.bash.cleanup",
                    lifecycle="cleanup",
                    phase="tool_exec",
                    tool_name="bash",
                    status="cancelled",
                    _started_at=started_at,
                )
                # Soft cancel: SIGTERM, then race grace period against force-cancel
                proc.terminate()
                grace_task = asyncio.create_task(proc.communicate())
                grace_set: set[asyncio.Task[Any]] = {
                    grace_task,
                    asyncio.create_task(asyncio.sleep(2.0)),
                }
                # Race force-cancel event during SIGTERM grace window so
                # double-cancel kills immediately instead of waiting 2s
                if _force_cancel_event is not None:

                    async def _wait_force() -> None:
                        while not _force_cancel_event.is_set():
                            await asyncio.sleep(0.05)

                    grace_set.add(asyncio.create_task(_wait_force()))
                grace_done, grace_pending = await asyncio.wait(grace_set, return_when=asyncio.FIRST_COMPLETED)
                for gp in grace_pending:
                    gp.cancel()
                if grace_task not in grace_done:
                    # Process didn't exit in time or force-cancel fired — SIGKILL
                    proc.kill()
                    await proc.wait()
                return {"stdout": "", "stderr": "", "exit_code": -1, "cancelled": True}
            else:
                # Timeout
                log_debug(
                    logger,
                    "tool.bash.timeout",
                    lifecycle="timeout",
                    phase="tool_exec",
                    tool_name="bash",
                    timeout_seconds=timeout,
                    _started_at=started_at,
                )
                if job_handle is not None:
                    from .sandbox_win32 import terminate_job

                    terminate_job(job_handle)
                proc.kill()
                await proc.wait()
                return {"error": f"Command timed out after {timeout}s", "exit_code": -1}
        finally:
            if job_handle is not None:
                from .sandbox_win32 import close_job

                close_job(job_handle)

        stdout_str = stdout.decode("utf-8", errors="replace")
        stderr_str = stderr.decode("utf-8", errors="replace")

        if len(stdout_str) > max_output:
            stdout_str = stdout_str[:max_output] + "\n... (truncated)"
        if len(stderr_str) > max_output:
            stderr_str = stderr_str[:max_output] + "\n... (truncated)"

        result = {
            "stdout": stdout_str,
            "stderr": stderr_str,
            "exit_code": proc.returncode or 0,
        }
        log_debug(
            logger,
            "tool.bash.success",
            lifecycle="success",
            phase="tool_exec",
            tool_name="bash",
            exit_code=result["exit_code"],
            stdout_chars=len(stdout_str),
            stderr_chars=len(stderr_str),
            _started_at=started_at,
        )
        return result
    except OSError as e:
        log_debug(
            logger,
            "tool.bash.failure",
            lifecycle="failure",
            phase="tool_exec",
            tool_name="bash",
            error_class=type(e).__name__,
            _started_at=started_at,
        )
        return {"error": str(e), "exit_code": -1}
    finally:
        if tmp_script is not None:
            try:
                os.unlink(tmp_script)
            except OSError:
                pass


async def handle_background_status(
    task_id: str,
    _bg_manager: Any = None,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    """Check status and output preview of a background task (#1311)."""
    if _bg_manager is None:
        return {"error": "Background task inspection not available in this context"}
    task = _bg_manager.get_task(task_id, db=_db)
    if task is None:
        return {"error": f"Background task not found: {task_id}"}

    metadata = task.get("metadata") or {}
    raw_result = metadata.get("task_result")
    if raw_result is not None:
        from ..services.task_result import TaskResult

        task_result = TaskResult.from_dict(raw_result)
        result = task_result.to_llm_dict()
        result["task_id"] = task["id"]
        result["command"] = task["command"]
        result["started_at"] = task.get("started_at")
        result["completed_at"] = task.get("completed_at")
        return result

    return {
        "task_id": task["id"],
        "command": task["command"],
        "status": task["status"],
        "exit_code": task.get("exit_code"),
        "stdout_preview": task.get("stdout_preview", ""),
        "stderr_preview": task.get("stderr_preview", ""),
        "started_at": task.get("started_at"),
        "completed_at": task.get("completed_at"),
    }


# ---------------------------------------------------------------------------
# Background task output inspection (#1312)
# ---------------------------------------------------------------------------

TASK_OUTPUT_DEFINITION: dict[str, Any] = {
    "name": "bash_task_output",
    "description": (
        "Retrieve stdout or stderr output from a completed or running background task. "
        "Use tail_lines to get only the last N lines. Use stream='stderr' for error output."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "task_id": {"type": "string", "description": "The background task ID"},
            "stream": {
                "type": "string",
                "enum": ["stdout", "stderr"],
                "description": "Which output stream to read (default: stdout)",
                "default": "stdout",
            },
            "tail_lines": {
                "type": "integer",
                "description": "Return only the last N lines (optional, returns all if omitted)",
            },
        },
        "required": ["task_id"],
    },
}


async def handle_task_output(
    task_id: str,
    stream: str = "stdout",
    tail_lines: int | None = None,
    _bg_manager: Any = None,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    """Read output from a background task's captured stdout/stderr file."""
    if _bg_manager is None:
        return {"error": "Background task manager not available"}

    from ..services.task_output import read_task_output, stderr_path, stdout_path

    # Validate task exists
    task = _bg_manager.get_task(task_id, db=_db)
    if task is None:
        return {"error": f"Task '{task_id}' not found"}

    conversation_id = task.get("conversation_id", "")
    data_dir = _bg_manager.data_dir

    if stream == "stderr":
        file_path = stderr_path(data_dir, conversation_id, task_id)
    else:
        file_path = stdout_path(data_dir, conversation_id, task_id)

    content = read_task_output(file_path, tail_lines=tail_lines)

    return {
        "task_id": task_id,
        "stream": stream,
        "content": content,
        "status": task.get("status", "unknown"),
        "lines": content.count("\n") if content else 0,
    }
