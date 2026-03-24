"""Workflow runner registry, execution, and result normalization.

Runner execution is domain-neutral. The engine calls execute_agent_runner()
or execute_opaque_runner() with generic parameters. Domain-specific behavior
(what prompt to send, what command to run) is defined in the workflow YAML,
not here.
"""

from __future__ import annotations

import asyncio
import logging
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Protocol


class TranscriptCallback(Protocol):
    """Callback signature for emitting transcript events."""

    def __call__(self, event_type: str, step_id: str | None, payload: dict[str, Any]) -> None: ...


logger = logging.getLogger(__name__)

_DEFAULT_WORKFLOW_AGENT_MAX_ITERATIONS = 100


def _trim_transcript_value(value: Any, max_chars: int) -> Any:
    """Preserve tool result structure while trimming oversized string leaves."""
    if isinstance(value, str):
        return value[:max_chars]
    if isinstance(value, dict):
        return {k: _trim_transcript_value(v, max_chars) for k, v in value.items()}
    if isinstance(value, list):
        return [_trim_transcript_value(item, max_chars) for item in value]
    return value


@dataclass(frozen=True)
class RunnerResult:
    """Normalized output from any runner type."""

    status: str  # "success", "failed", "blocked"
    summary: str = ""
    raw_output_path: str | None = None
    artifacts: dict[str, Any] = field(default_factory=dict)
    findings: list[dict[str, Any]] = field(default_factory=list)
    duration_ms: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "summary": self.summary,
            "raw_output_path": self.raw_output_path,
            "artifacts": self.artifacts,
            "findings": self.findings,
            "duration_ms": self.duration_ms,
        }


VALID_RESULT_STATUSES = frozenset({"success", "failed", "blocked"})

AGENT_RUNNER_TYPES = frozenset({"cli_claude", "cli_codex"})
OPAQUE_RUNNER_TYPES = frozenset({"shell", "python_script", "stub"})


class RunnerRegistry:
    """Registry for workflow runner types."""

    def __init__(self) -> None:
        self._runners: dict[str, str] = {}

    def register(self, runner_type: str, category: str = "opaque") -> None:
        if category not in ("agent", "opaque"):
            raise ValueError(f"Invalid runner category: {category!r}. Must be 'agent' or 'opaque'")
        self._runners[runner_type] = category

    def get_category(self, runner_type: str) -> str | None:
        return self._runners.get(runner_type)

    def is_agent_runner(self, runner_type: str) -> bool:
        return self._runners.get(runner_type) == "agent"

    def is_opaque_runner(self, runner_type: str) -> bool:
        return self._runners.get(runner_type) == "opaque"

    def is_registered(self, runner_type: str) -> bool:
        return runner_type in self._runners

    def list_runners(self) -> dict[str, str]:
        return dict(self._runners)


def create_default_registry() -> RunnerRegistry:
    """Create a registry with the four built-in V1 runner types."""
    registry = RunnerRegistry()
    registry.register("cli_claude", "agent")
    registry.register("cli_codex", "agent")
    registry.register("shell", "opaque")
    registry.register("python_script", "opaque")
    return registry


def create_stub_registry() -> RunnerRegistry:
    """Create a registry with only the stub runner for simulation (#968)."""
    registry = RunnerRegistry()
    registry.register("stub", "opaque")
    registry.register("shell", "opaque")
    registry.register("python_script", "opaque")
    registry.register("cli_claude", "agent")
    registry.register("cli_codex", "agent")
    return registry


# ---------------------------------------------------------------------------
# Runner execution (domain-neutral)
# ---------------------------------------------------------------------------


async def execute_agent_runner(
    *,
    prompt: str,
    system_prompt: str | None = None,
    tools_filter: list[str] | None = None,
    timeout: int = 300,
    max_iterations: int = _DEFAULT_WORKFLOW_AGENT_MAX_ITERATIONS,
    ai_service: Any | None = None,
    tool_executor: Any | None = None,
    tools_openai: list[dict[str, Any]] | None = None,
    pause_signal: Any | None = None,
    confirm_callback: Any | None = None,
    model: str | None = None,
    transcript_cb: TranscriptCallback | None = None,
    transcript_max_assistant_chars: int = 4000,
    transcript_max_tool_output_chars: int = 2000,
    step_id: str | None = None,
) -> RunnerResult:
    """Execute an agent runner step through Anteroom's agent loop.

    Each invocation gets a fresh, independent message list (session isolation).
    Uses serialize_tools=True so the pause signal can be checked between
    tool calls. The agent runner is one runner category among equals — shell
    and python_script runners are equally first-class.
    """
    start = time.monotonic()

    if ai_service is None or tool_executor is None:
        raise RuntimeError(
            "Agent runner requires ai_service and tool_executor. "
            "Configure the WorkflowEngine with AI service dependencies."
        )

    from .agent_loop import run_agent_loop

    # Fresh message list — session isolation per step (FR-006)
    messages: list[dict[str, Any]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    # Wrap tool_executor to inject confirm_callback if provided (#950)
    actual_executor = tool_executor
    if confirm_callback is not None:

        async def _wrapped_executor(name: str, args: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
            return await tool_executor(name, args, confirm_callback=confirm_callback, **kwargs)

        actual_executor = _wrapped_executor

    assistant_content = ""
    turn_content = ""  # per-turn accumulator for transcript
    tool_outputs: list[dict[str, Any]] = []
    paused = False
    total_prompt_tokens = 0
    total_completion_tokens = 0
    turn_tokens = 0  # tokens for current turn

    if transcript_cb is not None and prompt.strip():
        transcript_cb(
            "transcript_prompt",
            step_id,
            {
                "content": prompt,
                "chars": len(prompt),
            },
        )

    def _flush_turn() -> None:
        """Emit transcript_assistant for accumulated turn text."""
        nonlocal turn_content, turn_tokens
        if transcript_cb is not None and turn_content:
            transcript_cb(
                "transcript_assistant",
                step_id,
                {
                    "content": turn_content[:transcript_max_assistant_chars],
                    "tokens": turn_tokens,
                    "model": model or "",
                },
            )
        turn_content = ""
        turn_tokens = 0

    async for event in run_agent_loop(
        ai_service=ai_service,
        messages=messages,
        tool_executor=actual_executor,
        tools_openai=tools_openai,
        serialize_tools=True,
        pause_signal=pause_signal,
        max_iterations=max_iterations,
    ):
        if event.kind == "token":
            content = event.data.get("content", "")
            assistant_content += content
            turn_content += content
        elif event.kind == "tool_call_end":
            tool_outputs.append(event.data)
            if transcript_cb is not None:
                tc_name = event.data.get("tool_name", "")
                tc_output = _trim_transcript_value(event.data.get("output", ""), transcript_max_tool_output_chars)
                transcript_cb(
                    "transcript_tool_result",
                    step_id,
                    {
                        "tool_name": tc_name,
                        "status": event.data.get("status", ""),
                        "output": tc_output,
                    },
                )
        elif event.kind == "tool_call_start":
            # Flush assistant turn before tool call — preserves chronology
            _flush_turn()
            if transcript_cb is not None:
                transcript_cb(
                    "transcript_tool_call",
                    step_id,
                    {
                        "tool_name": event.data.get("tool_name", ""),
                        "arguments": str(event.data.get("arguments", "")),
                    },
                )
        elif event.kind == "usage":
            total_prompt_tokens += event.data.get("prompt_tokens", 0)
            total_completion_tokens += event.data.get("completion_tokens", 0)
            turn_tokens += event.data.get("completion_tokens", 0)
            if transcript_cb is not None:
                transcript_cb(
                    "transcript_usage",
                    step_id,
                    {
                        "prompt_tokens": event.data.get("prompt_tokens", 0),
                        "completion_tokens": event.data.get("completion_tokens", 0),
                        "total_tokens": event.data.get("total_tokens", 0),
                    },
                )
        elif event.kind == "workflow_pause":
            paused = True
            break
        elif event.kind == "error":
            _flush_turn()
            duration_ms = int((time.monotonic() - start) * 1000)
            return RunnerResult(
                status="failed",
                summary=event.data.get("message", "Agent loop error"),
                duration_ms=duration_ms,
            )

    # Flush any remaining assistant text from the final turn
    _flush_turn()
    duration_ms = int((time.monotonic() - start) * 1000)

    if paused:
        return RunnerResult(
            status="blocked",
            summary="Paused for approval",
            duration_ms=duration_ms,
        )

    return RunnerResult(
        status="success",
        summary=assistant_content[:2000] if assistant_content else "Agent completed",
        artifacts={
            "tool_call_count": len(tool_outputs),
            "prompt_tokens": total_prompt_tokens,
            "completion_tokens": total_completion_tokens,
            "total_tokens": total_prompt_tokens + total_completion_tokens,
            "model": model or "",
        },
        findings=[{"tool": tc.get("tool_name", ""), "status": tc.get("status", "")} for tc in tool_outputs],
        duration_ms=duration_ms,
    )


async def execute_opaque_runner(
    *,
    mode: str,
    command: str,
    argv: list[str] | None = None,
    env: dict[str, str] | None = None,
    working_dir: str | None = None,
    timeout: int = 300,
    transcript_cb: TranscriptCallback | None = None,
    transcript_max_stdout_chars: int = 4000,
    transcript_max_stderr_chars: int = 4000,
    step_id: str | None = None,
) -> RunnerResult:
    """Execute an opaque runner step as a subprocess.

    mode="shell": command is passed to /bin/sh -c via create_subprocess_shell().
    mode="exec": command is a script path, argv is positional args, via create_subprocess_exec().

    Domain-neutral — the engine doesn't know or care what the subprocess does.
    """
    from pathlib import Path

    start = time.monotonic()

    if working_dir and not Path(working_dir).is_dir():
        return RunnerResult(
            status="failed",
            summary=f"Working directory does not exist: {working_dir}",
            duration_ms=0,
        )

    import os
    import signal

    # Always build merged_env so we can inject PYTHONUNBUFFERED=1.
    # This forces Python subprocesses to flush stdout/stderr per-line
    # instead of block-buffering when connected to a pipe.
    merged_env = {**os.environ, "PYTHONUNBUFFERED": "1", **(env or {})}
    spawn_kwargs: dict[str, Any] = {}
    if os.name != "nt":
        spawn_kwargs["start_new_session"] = True

    try:
        if mode == "shell":
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
                env=merged_env,
                **spawn_kwargs,
            )
        elif mode == "exec":
            exec_args = [sys.executable, command, *(argv or [])]
            proc = await asyncio.create_subprocess_exec(
                *exec_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
                env=merged_env,
                **spawn_kwargs,
            )
        else:
            raise ValueError(f"Unknown opaque runner mode: {mode!r}")

        stdout_lines: list[str] = []
        stderr_lines: list[str] = []

        async def _read_stream(
            stream: asyncio.StreamReader | None,
            lines: list[str],
            event_type: str,
            max_chars: int,
        ) -> None:
            if stream is None:
                return
            while True:
                line_bytes = await stream.readline()
                if not line_bytes:
                    break
                line = line_bytes.decode("utf-8", errors="replace").rstrip("\n").rstrip("\r")
                lines.append(line)
                if transcript_cb is not None:
                    transcript_cb(
                        event_type,
                        step_id,
                        {"content": line[:max_chars]},
                    )

        try:
            await asyncio.wait_for(
                asyncio.gather(
                    _read_stream(proc.stdout, stdout_lines, "transcript_stdout", transcript_max_stdout_chars),
                    _read_stream(proc.stderr, stderr_lines, "transcript_stderr", transcript_max_stderr_chars),
                ),
                timeout=timeout,
            )
            await proc.wait()
        except asyncio.TimeoutError:
            if os.name != "nt":
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                proc.kill()
            await proc.wait()
            duration_ms = int((time.monotonic() - start) * 1000)
            return RunnerResult(
                status="failed",
                summary=f"Timed out after {timeout}s",
                duration_ms=duration_ms,
            )

        duration_ms = int((time.monotonic() - start) * 1000)
        stdout = "\n".join(stdout_lines).strip()
        stderr = "\n".join(stderr_lines).strip()

        if proc.returncode == 0:
            return RunnerResult(
                status="success",
                summary=stdout[:2000] if stdout else "Completed successfully",
                artifacts={"exit_code": 0},
                findings=[{"type": "stderr", "content": stderr}] if stderr else [],
                duration_ms=duration_ms,
            )
        else:
            return RunnerResult(
                status="failed",
                summary=stderr[:2000] if stderr else f"Exit code {proc.returncode}",
                artifacts={"exit_code": proc.returncode},
                findings=[{"type": "stdout", "content": stdout}] if stdout else [],
                duration_ms=duration_ms,
            )

    except Exception as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        return RunnerResult(
            status="failed",
            summary=f"Runner error: {exc}",
            duration_ms=duration_ms,
        )
