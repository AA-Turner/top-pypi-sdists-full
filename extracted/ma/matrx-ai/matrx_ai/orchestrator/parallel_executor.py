"""Parallel AI Execution — run multiple independent AI requests under a single
user request context.

All calls share the same ``AppContext`` (same ``conversation_id`` and
``request_id``), so every ``cx_request`` row they produce is aggregated under
the single ``cx_user_request`` row that the boundary layer created.

Usage (batch script or workflow)::

    from matrx_ai.orchestrator.parallel_executor import parallel_execute

    results = await parallel_execute(configs)
    for r in results:
        if r.error:
            print(f"Failed: {r.error}")
        else:
            print(r.output)

Design decisions:

- ``asyncio.create_task()`` is used (not ``gather()`` on bare coroutines) so
  that Python copies the ContextVar snapshot at task-creation time.  All tasks
  share the same AppContext value, but each task is independently cancellable.

- Every independent task is created immediately. Provider admission, cooldown,
  and rate-limit adaptation are enforced centrally by ``UnifiedAIClient``.

- Results are always returned in the same order as ``configs`` so callers
  can zip inputs and outputs safely.

- Per-item errors are captured and returned as ``ParallelResult(error=...)``
  entries rather than aborting the whole batch.  The caller inspects
  ``result.error`` to detect failures.
"""

from __future__ import annotations

import asyncio
import traceback
from dataclasses import dataclass
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.orchestrator.requests import CompletedRequest


@dataclass
class ParallelResult:
    """Outcome of one parallel AI execution."""

    index: int
    completed: CompletedRequest | None = None
    error: str | None = None
    error_traceback: str | None = None

    @property
    def success(self) -> bool:
        return self.completed is not None and self.error is None

    @property
    def output(self) -> str | None:
        if self.completed and self.completed.request:
            return self.completed.request.config.get_last_output()
        return None


async def parallel_execute(
    configs: list[UnifiedConfig],
    *,
    concurrency: int | None = None,
    rate_limit_delay: float | None = None,
    metadata: dict[str, Any] | None = None,
) -> list[ParallelResult]:
    """Execute multiple AI configs concurrently under a single user request.

    The boundary layer MUST have already called ``ensure_user_request_exists()``
    before calling this function.  All results share the same ``cx_user_request``
    row and their costs are aggregated into it.

    Args:
        configs: One ``UnifiedConfig`` per independent AI call.
        concurrency: Deprecated compatibility argument. Ignored; provider
            admission belongs to the central provider dispatch boundary.
        rate_limit_delay: Deprecated compatibility argument. Ignored; provider
            cooldowns belong to the central provider dispatch boundary.
        metadata: Optional metadata forwarded to every ``execute_ai_request()``
            call.

    Returns:
        A list of ``ParallelResult`` objects in the same order as ``configs``.
        Inspect ``result.success`` and ``result.error`` for per-item outcomes.
    """
    from matrx_ai.orchestrator.executor import execute_ai_request

    if not configs:
        return []

    total = len(configs)
    results: list[ParallelResult | None] = [None] * total
    if concurrency is not None or rate_limit_delay is not None:
        vcprint(
            "[ParallelExecutor] caller-side concurrency/rate delay is deprecated "
            "and ignored; central provider admission owns throttling",
            color="yellow",
        )

    async def _run_one(idx: int, config: UnifiedConfig) -> None:
        try:
            vcprint(
                f"[ParallelExecutor] Starting [{idx + 1}/{total}]",
                color="cyan",
            )
            completed = await execute_ai_request(config, metadata=metadata or {})
            results[idx] = ParallelResult(index=idx, completed=completed)
            vcprint(
                f"[ParallelExecutor] Done [{idx + 1}/{total}]",
                color="green",
            )
        except Exception as exc:
            tb = traceback.format_exc()
            vcprint(
                f"[ParallelExecutor] Failed [{idx + 1}/{total}]: {exc}",
                color="red",
            )
            results[idx] = ParallelResult(
                index=idx,
                error=str(exc),
                error_traceback=tb,
            )

    # asyncio.create_task() copies the ContextVar snapshot — all tasks
    # inherit the current AppContext (same conversation_id, request_id, emitter).
    tasks: list[asyncio.Task] = []
    for idx, config in enumerate(configs):
        task = asyncio.create_task(_run_one(idx, config))
        tasks.append(task)

    await asyncio.gather(*tasks, return_exceptions=False)

    return [r for r in results if r is not None]
