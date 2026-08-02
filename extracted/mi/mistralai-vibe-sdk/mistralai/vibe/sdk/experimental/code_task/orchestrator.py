"""Orchestrator — the pause/resume loop.

Simplified equivalent of the CodeTask state machine from
agentic-harness-sdk/patterns/code-task.ts.

Runs the full cycle:
1. Execute code in sandbox
2. If partial_evaluation: resolve pending tools in parallel, loop
3. If code_result or error: return
"""

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from .sandbox import run_python_code
from .types import (
    PartialEvaluation,
    PendingTool,
    RejectedTool,
    ResolvedTool,
    RunCodeResult,
    ToolDefinition,
    ToolState,
)

type ToolResolver = Callable[[str, dict[str, Any]], Awaitable[Any]]


async def orchestrate(
    code: str,
    tools: list[ToolDefinition],
    resolve_tool: ToolResolver,
    *,
    input: dict[str, Any] | None = None,
    max_iterations: int = 20,
    timeout: float = 5.0,
) -> RunCodeResult:
    """Run the full pause/resume loop until completion.

    Args:
        code: Python source code defining ``async def main()``.
        tools: Available tool definitions.
        resolve_tool: Async callable (name, args) -> result.
            Called for each pending tool. Runs in parallel for
            tools discovered in the same iteration.
        input: Optional kwargs passed to main().
        max_iterations: Safety limit on sandbox re-executions.
        timeout: Per-iteration sandbox timeout in seconds.

    Returns:
        Final RunCodeResult (code_result or error).
    """
    partial = PartialEvaluation(
        code=code,
        tool_state=[],
        input=input or {},
    )

    for _ in range(max_iterations):
        try:
            result = await run_python_code(partial, tools, timeout=timeout)
        except Exception as e:
            return RunCodeResult(type="error", error=f"{type(e).__name__}: {e}")

        if result.type != "partial_evaluation":
            return result

        pe = result.partial_evaluation
        assert pe is not None

        # Collect pending tools
        pending_indices: list[int] = []
        pending_coros: list[Awaitable[Any]] = []
        for i, ts in enumerate(pe.tool_state):
            if isinstance(ts, PendingTool):
                pending_indices.append(i)
                pending_coros.append(resolve_tool(ts.function.name, ts.function.arguments))

        if not pending_indices:
            return RunCodeResult(
                type="error",
                error="Partial evaluation with no pending tools",
            )

        # Resolve all pending tools in parallel
        resolved_values = await asyncio.gather(*pending_coros, return_exceptions=True)

        # Build new tool_state with pending -> resolved/rejected
        new_tool_state: list[ToolState] = list(pe.tool_state)
        for idx, tool_result in zip(pending_indices, resolved_values, strict=False):
            ts = pe.tool_state[idx]
            assert isinstance(ts, PendingTool)

            if isinstance(tool_result, BaseException):
                new_tool_state[idx] = RejectedTool(
                    id=ts.id,
                    function=ts.function,
                    error={
                        "name": type(tool_result).__name__,
                        "message": str(tool_result),
                    },
                )
            else:
                new_tool_state[idx] = ResolvedTool(
                    id=ts.id,
                    function=ts.function,
                    result=tool_result,
                )

        partial = PartialEvaluation(
            code=pe.code,
            tool_state=new_tool_state,
            input=pe.input,
        )

    return RunCodeResult(
        type="error",
        error=f"Max iterations ({max_iterations}) exceeded",
    )
