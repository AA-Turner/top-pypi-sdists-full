"""
cvc.agent.telepathy_executor - Hermes-parity parallel tool dispatch for CVC.

v1 (original): spawned a CVC branch per tool call and ran them via
``asyncio.gather``. Two fatal flaws:

  1. **Race condition.** Each task set ``engine._active_branch`` independently,
     so N concurrent branches clobbered each other's state.
  2. **Absurd overhead.** Five concurrent ``read_file`` calls spawned 5
     branches, 5 commits, 5 merges — and the parallel writes raced on the
     shared SQLite DB handle.

v2 (this version): ports Hermes Agent's guardrails.

  • Read-only calls (``read_file``, ``web_search``, ``session_search`` …) run
    in a plain ``asyncio.gather`` thread-pool — no branch, no commit, no merge.
    This is 99% of the parallel case.
  • Mutating calls (``write_file``, ``patch_file``) are partitioned: parallel
    only when they target different paths; otherwise sequential.
  • Interactive / global-state calls (``clarify``, ``terminal``, ``cvc_commit``)
    force the entire batch sequential.
  • The CVC-branch fan-out is reserved for genuinely heavy sub-computations
    (future: parallel sub-agents that need cognitive isolation).

The safety classification lives in ``cvc.agent.parallel_safety``.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any

from cvc.agent.executor import ToolExecutor
from cvc.agent.parallel_safety import (
    partition_for_parallel,
    ParallelPartition,
)
from cvc.core.models import CVCBranchRequest, CVCCommitRequest, CVCMergeRequest, CommitType
from cvc.operations.engine import CVCEngine

logger = logging.getLogger("cvc.agent.telepathy")

#: Maximum concurrent workers for parallel dispatch (mirrors Hermes' 8).
_MAX_PARALLEL_WORKERS = 8


class TelepathicToolExecutor:
    """
    Executes multiple tool calls in parallel with Hermes-grade guardrails.

    Decision tree per batch:

      1. Partition via ``parallel_safety.partition_for_parallel``.
      2. If all calls are parallel-safe → ``asyncio.gather`` thread-pool, no
         CVC branches.
      3. If any call is BLOCK or path-conflict → run entire batch sequentially
         via ``_run_sequential``.
      4. (Reserved) Heavy cognitive fan-out can still request explicit branches
         via ``_run_with_branches``.
    """

    def __init__(self, base_executor: ToolExecutor, engine: CVCEngine) -> None:
        self.base_executor = base_executor
        self.engine = engine

    # ── Public API ──────────────────────────────────────────────────────────

    async def execute_parallel(
        self, tool_calls: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Execute a batch of tool calls with safety-aware parallelism.

        Returns one result dict per input call, preserving order.
        Each result: ``{tool_name, success, output, call_id, mode}`` where
        ``mode`` is ``"parallel"`` | ``"sequential"``.
        """
        if not tool_calls:
            return []

        # Single call — fast path, no partition overhead
        if len(tool_calls) == 1:
            tc = tool_calls[0]
            out = await self._run_one(tc)
            return [self._format_result(tc, out, mode="single")]

        # Partition: decide what can run concurrently
        partition = partition_for_parallel(tool_calls)

        if partition.parallel and not partition.sequential and not partition.conflicts:
            # All-safe — run concurrently without CVC branches
            logger.debug(
                "telepathy: %d tools all-safe → parallel (no branches)",
                len(tool_calls),
            )
            return await self._run_threaded_parallel(tool_calls)

        # Mixed or unsafe — run sequentially
        logger.debug(
            "telepathy: %d tools → sequential (%d blocks, %d conflicts)",
            len(tool_calls),
            sum(1 for d in partition.decisions if d.decision == "block"),
            len(partition.conflicts),
        )
        return await self._run_sequential(tool_calls)

    # ── Execution paths ────────────────────────────────────────────────────

    async def _run_threaded_parallel(
        self, tool_calls: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Run all calls in a thread pool — NO CVC branches.
        Safe because ``partition_for_parallel`` already verified every call
        is either read-only or non-conflicting path-scoped.
        """
        semaphore = asyncio.Semaphore(_MAX_PARALLEL_WORKERS)

        async def _guarded(tc: dict[str, Any]) -> dict[str, Any]:
            async with semaphore:
                out = await self._run_one(tc)
                return self._format_result(tc, out, mode="parallel")

        # ``asyncio.gather`` preserves input order in the returned list
        return await asyncio.gather(*(_guarded(tc) for tc in tool_calls))

    async def _run_sequential(
        self, tool_calls: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Run calls one-by-one in input order."""
        results: list[dict[str, Any]] = []
        for tc in tool_calls:
            out = await self._run_one(tc)
            results.append(self._format_result(tc, out, mode="sequential"))
        return results

    async def _run_one(self, tc: dict[str, Any]) -> tuple[str, bool]:
        """
        Execute a single tool call off-thread.

        Returns ``(output_str, success_bool)``.
        The base executor is synchronous (subprocess, file I/O, network) so we
        offload via ``run_in_executor`` to keep the event loop responsive.
        """
        tool_name = tc.get("name", "")
        arguments = tc.get("args", {}) or {}
        loop = asyncio.get_running_loop()
        try:
            raw = await loop.run_in_executor(
                None, self.base_executor.execute, tool_name, arguments
            )
            success = not (isinstance(raw, str) and raw.startswith("Error:"))
            return (str(raw), success)
        except Exception as exc:
            logger.warning("telepathy: %s raised %s", tool_name, exc, exc_info=True)
            return (f"Tool execution failed: {exc}", False)

    # ── Formatting ─────────────────────────────────────────────────────────

    @staticmethod
    def _format_result(
        tc: dict[str, Any], outcome: tuple[str, bool], *, mode: str
    ) -> dict[str, Any]:
        output, success = outcome
        return {
            "tool_name": tc.get("name", ""),
            "success": success,
            "output": output,
            "call_id": tc.get("id") or uuid.uuid4().hex[:6],
            "mode": mode,
        }

    # ── Reserved: cognitive fan-out via CVC branches ───────────────────────
    #
    # The original branch-per-call behaviour is preserved here for future use
    # (e.g. parallel sub-agents that need cognitive isolation). It is NOT used
    # for ordinary tool dispatch because of the overhead + race risk.
    #
    # To use: the caller must explicitly request cognitive branching and
    # serialise the branch-create / commit / merge steps with a lock.

    async def _run_with_branches(
        self, tool_calls: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        [RESERVED] Original telepathy behaviour — one CVC branch per call.

        Kept for future parallel sub-agent work. Has known constraints:
          • Branch creation, commit, and merge must hold the engine lock.
          • Only safe when each call produces a large output worth distilling.
        """
        base_branch = self.engine.active_branch
        results: list[dict[str, Any]] = []

        # Serialise engine-state mutation; parallelise only the tool I/O.
        async with asyncio.Lock():
            for tc in tool_calls:
                tool_name = tc.get("name", "")
                call_id = tc.get("id") or uuid.uuid4().hex[:6]
                branch_name = f"telepathy-{tool_name}-{call_id}"

                try:
                    self.engine.branch(
                        CVCBranchRequest(
                            name=branch_name,
                            source_commit=None,
                            description=f"Executing {tool_name}",
                        )
                    )
                    self.engine._active_branch = branch_name

                    loop = asyncio.get_running_loop()
                    raw = await loop.run_in_executor(
                        None,
                        self.base_executor.execute,
                        tool_name,
                        tc.get("args", {}) or {},
                    )
                    success = True
                except Exception as exc:
                    raw = f"Tool execution failed: {exc}"
                    success = False

                self.engine.commit(
                    CVCCommitRequest(
                        message=f"Raw output of {tool_name}",
                        commit_type=CommitType.TOOL_CALL,
                    )
                )
                self.engine._active_branch = base_branch
                self.engine.merge(
                    CVCMergeRequest(
                        source_branch=branch_name, target_branch=base_branch
                    ),
                    synthesized_summary=(
                        f"Telepathic Tool Sync: {tool_name} completed. "
                        f"Output length: {len(str(raw))}"
                    ),
                )
                results.append(
                    {
                        "tool_name": tool_name,
                        "success": success,
                        "output": raw,
                        "call_id": call_id,
                        "mode": "branch",
                    }
                )

        return results


__all__ = ["TelepathicToolExecutor"]
