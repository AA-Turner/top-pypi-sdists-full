from __future__ import annotations

import asyncio
import time
from typing import Any

from matrx_ai.tools.arg_models.shell_args import ShellExecuteArgs
from matrx_ai.tools.kinds.execution import ShellExecution
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.vfs.commands import VfsCommandRunner, load_all
from matrx_ai.tools.vfs.shell import (
    ShellEnv,
    ShellExpansionError,
    ShellParseError,
    execute,
    parse,
)
from matrx_ai.tools.vfs.workspace import get_workspace_fs

# Register every command implementation so the runner can dispatch them.
load_all()

MAX_OUTPUT_SIZE = 10_240


def _err(
    started_at: float,
    ctx: ToolContext,
    error_type: str,
    message: str,
    *,
    is_retryable: bool = False,
) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type=error_type,
            message=message,
            is_retryable=is_retryable,
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="shell_execute",
        call_id=ctx.call_id,
    )


async def shell_execute(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = ShellExecuteArgs(**args)
    vfs = await get_workspace_fs(ctx)
    runner = VfsCommandRunner(vfs)

    # The agent's home is /home/agent (mirrors the sandbox). A bare shell_execute
    # with no working_dir must land THERE, not at the durable VFS root "/" — at "/"
    # the agent sees its whole code-files library and gets lost (it once mistook it
    # for a project to reorganize). Absolute working_dir is honored as-is; a relative
    # one resolves under the home.
    _HOME = "/home/agent"
    wd = parsed.working_dir
    if wd.startswith("/"):
        cwd = wd
    elif wd in ("", ".", "./"):
        cwd = _HOME
    else:
        cwd = f"{_HOME}/{wd}"
    env = ShellEnv(cwd=cwd)

    try:
        node = parse(parsed.command)
    except ShellParseError as exc:
        return _err(
            started_at,
            ctx,
            "validation",
            f"bash: syntax error: {exc.message}",
        )

    try:
        result = await asyncio.wait_for(
            execute(node, env, runner, capture=True),
            timeout=parsed.timeout_seconds,
        )
    except TimeoutError:
        return _err(
            started_at,
            ctx,
            "timeout",
            f"Command timed out after {parsed.timeout_seconds}s",
            is_retryable=True,
        )
    except ShellExpansionError as exc:
        return _err(started_at, ctx, "validation", f"bash: {exc}")

    stdout = result.stdout[:MAX_OUTPUT_SIZE]
    stderr = result.stderr[:MAX_OUTPUT_SIZE]
    # KindModel result (KIND_TOOL_LEDGER): the durable-VFS branch returns the
    # same shell_execution shape as the sandbox and real-disk branches — the
    # live server takes THIS branch (the fs_* "module you find is not the
    # module that runs" trap), so skipping it would fail the real dispatch.
    output = ShellExecution(
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
        exit_code=result.exit_code,
    ).model_dump(mode="json")

    if result.exit_code == 0:
        return ToolResult(
            success=True,
            output=output,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="shell_execute",
            call_id=ctx.call_id,
        )

    return ToolResult(
        success=False,
        output=output,
        error=ToolError(
            error_type="exit_code",
            message=f"Command exited with code {result.exit_code}",
            is_retryable=False,
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="shell_execute",
        call_id=ctx.call_id,
    )


__all__ = ["shell_execute"]
