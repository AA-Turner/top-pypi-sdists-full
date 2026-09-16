"""FEAT-555 — runs the reserved continuations of a finished Task.

`Task` is imported lazily inside methods (the pattern at
flowtask/executors/local.py:128): task.py imports this module, so a module-scope
import would be a cycle.
"""
from __future__ import annotations

import asyncio
import copy
import logging
import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from ..conf import NEXTTASK_MAX_DEPTH
from ..executors.models import ExecutorType  # verified: executors/models.py:11
from ..executors.resolver import (
    resolve_executor,  # verified: flowtask/executors/resolver.py:15
)
from ..models import TaskState  # verified: flowtask/models.py:19
from .chain import (
    ChainEncodingError,
    ChainHopResult,
    ChainLineageEntry,
    ChainMetadata,
    ChainPayload,
    Continuation,
)
from .exchange import ResultExchange

if TYPE_CHECKING:                                # import-time safe: not evaluated at runtime
    from .task import Task

logger = logging.getLogger(__name__)

INLINE: str = "inline"
#: Executors that document **kwargs as "reserved" and therefore drop chain
#: kwargs entirely (docker.py:171, k8s.py:208) — hops naming them are refused.
_NON_FORWARDING: frozenset[str] = frozenset(
    {ExecutorType.DOCKER.value, ExecutorType.K8S.value}
)


class TaskChainer:
    """Runs the reserved continuations of a finished Task. Never raises."""

    def __init__(
        self, task: Task, exchange: ResultExchange | None = None
    ) -> None:
        """Args:
            task: The finished origin task, at close() time.
            exchange: Injected for tests; a ResultExchange is created on demand.
        """
        self.task = task
        self._exchange = exchange
        self.logger = logger

    @property
    def exchange(self) -> ResultExchange:
        """The Redis exchange, created on first use (remote hops only)."""
        if self._exchange is None:
            self._exchange = ResultExchange()
        return self._exchange

    def build_payload(self) -> ChainPayload:
        """Snapshot what the origin hands to its continuations.

        Returns:
            A ChainPayload whose ``result`` is the origin's result ONLY when the
            origin ended in ``TaskState.DONE`` (A2/AC-25), whose ``variables``
            are a copy of the origin's end-of-run variables, and whose metadata
            carries the lineage with the origin appended last.
        """
        # Result is the origin's result ONLY when the origin ended in TaskState.DONE (A2/AC-25)
        result = self.task._resultset if self.task._state is TaskState.DONE else None
        
        # Variables are a shallow copy (fan-out isolation, A6; spec Module 6:
        # `variables = dict(task._variables)`). A deep copy would raise
        # TypeError on any value that can't be pickled (a lock, open
        # socket/file, DB connection, ...) — plausible in `_variables` for a
        # long-running pipeline — and that exception would propagate out of
        # `run_continuations()`'s catch-all, silently skipping every
        # continuation for that run.
        variables = dict(self.task._variables)
        
        # Inherited lineage
        if hasattr(self.task, '_chain') and self.task._chain is not None:
            inherited_lineage = self.task._chain.metadata.lineage
        else:
            inherited_lineage = []
            
        # Append the origin itself to the lineage
        lineage = inherited_lineage + [
            ChainLineageEntry(
                task_id=str(self.task.task_id),
                program=self.task._program,
                task=self.task._taskname
            )
        ]
        
        # Stats summary - only when task.stats is not None
        stats_summary = None
        if self.task.stats is not None:
            stats_summary = self.task.stats.to_json()
            
        # Build metadata
        metadata = ChainMetadata(
            origin_task_id=str(self.task.task_id),
            origin_program=self.task._program,
            origin_task=self.task._taskname,
            origin_state=self.task._state.name,
            finished_at=datetime.now(UTC).isoformat(),
            stats_summary=stats_summary,
            lineage=lineage
        )
        
        return ChainPayload(
            result=result,
            variables=variables,
            metadata=metadata
        )

    def _forwards_kwargs(self, executor: str | dict[str, Any]) -> bool:
        """Whether an executor forwards chain kwargs to the hop task.

        Args:
            executor: A registered executor name or a full executor dict.

        Returns:
            False only for the docker and k8s backends (A1); True otherwise,
            including for unknown/custom executor names.
        """
        # Resolve the type name - a str is the name itself, a dict uses its "type" key
        if isinstance(executor, str):
            executor_type = executor
        elif isinstance(executor, dict):
            executor_type = executor.get("type", "local")
        else:
            # Default to local for unknown types
            executor_type = "local"
            
        # Compare the lowercased name against _NON_FORWARDING
        # Default to True so custom executors are not refused
        return executor_type.lower() not in _NON_FORWARDING

    def eligible(
        self, cont: Continuation, payload: ChainPayload
    ) -> tuple[bool, str | None]:
        """Decide whether one continuation may run.

        Args:
            cont: The continuation under consideration.
            payload: The payload built by :meth:`build_payload`.

        Returns:
            ``(True, None)`` when the hop may run, else ``(False, reason)``
            where reason is one of the documented strings.
        """
        # 1. cont.step_name in task.ignore_steps -> (False, "ignored: ignore_steps")
        if cont.step_name in self.task.ignore_steps:
            return (False, "ignored: ignore_steps")
            
        # 2. task.run_only non-empty and step not in it -> (False, "ignored: run_only")
        if len(self.task.run_only) > 0 and cont.step_name not in self.task.run_only:
            return (False, "ignored: run_only")
            
        # 3. not cont.on.matches(task._state) -> (False, f"policy: on={cont.on.value} state={task._state.name}")
        if not cont.on.matches(self.task._state):
            return (False, f"policy: on={cont.on.value} state={self.task._state.name}")
            
        # 4. target "<program>.<task>" already in payload.metadata.lineage -> (False, f"refused: cycle {target}")
        target_program = cont.program or self.task._program
        target = f"{target_program}.{cont.task}"
        for entry in payload.metadata.lineage:
            if f"{entry.program}.{entry.task}" == target:
                return (False, f"refused: cycle {target}")
                
        # 5. payload.metadata.depth >= NEXTTASK_MAX_DEPTH -> (False, f"refused: depth {depth} >= {NEXTTASK_MAX_DEPTH}")
        if payload.metadata.depth >= NEXTTASK_MAX_DEPTH:
            return (False, f"refused: depth {payload.metadata.depth} >= {NEXTTASK_MAX_DEPTH}")
            
        # 6. not self._forwards_kwargs(cont.executor) and cont.executor != INLINE -> (False, "refused: executor does not forward chain kwargs")
        if not self._forwards_kwargs(cont.executor) and cont.executor != INLINE:
            return (False, "refused: executor does not forward chain kwargs")
            
        # Else (True, None)
        return (True, None)

    def _result_for(
        self, cont: Continuation, payload: ChainPayload, inline_consumers: int
    ) -> Any:
        """The result object to hand to one hop, isolated as needed.

        Args:
            cont: The continuation.
            payload: The shared payload.
            inline_consumers: How many eligible INLINE hops will consume the
                result in this run.

        Returns:
            None when ``cont.result`` is False; the payload result by reference
            when at most one inline hop consumes it; an independent copy when two
            or more do (A6/AC-28).
        """
        # Return None when not cont.result
        if not cont.result:
            return None
            
        # When inline_consumers <= 1 return payload.result unchanged
        if inline_consumers <= 1:
            return payload.result
            
        # Otherwise copy: use .copy() when the object exposes a callable `copy` attribute
        # (covers pandas DataFrame and dict/list), else copy.deepcopy
        try:
            if hasattr(payload.result, 'copy') and callable(payload.result.copy):
                return payload.result.copy()
            else:
                return copy.deepcopy(payload.result)
        except (TypeError, AttributeError) as e:
            # If copying raises, log a warning and fall back to the shared reference
            self.logger.warning(
                "Failed to copy result for multiple consumers, falling back to shared reference: %s",
                e
            )
            return payload.result

    # ------------------------------------------------------------------
    # Execution layer — implemented by TASK-226. Do not implement here.
    # ------------------------------------------------------------------

    def _hop_kwargs(
        self, cont: Continuation, payload: ChainPayload
    ) -> dict[str, Any]:
        """Kwargs shared by inline and remote hops.

        Returns:
            A dict carrying ``variables`` (origin variables, then the step's
            overrides, then the reserved ``chain_*`` names), the inherited-or-
            overridden ``storage``/``filestore`` NAMES, ``debug`` and
            ``ignore_results=True``. Never ``params``/``attributes``/``arguments``.
        """
        variables = {
            **payload.variables,
            **cont.variables,
            **payload.as_variables(),
        }
        storage = cont.storage or getattr(self.task, "_storage", "default")
        filestore = cont.filestore or getattr(self.task, "_filestore_name", None)
        debug = getattr(self.task, "_debug", False)
        
        return {
            "variables": variables,
            "storage": storage,
            "filestore": filestore,
            "debug": debug,
            "ignore_results": True,
        }

    async def _run_inline(
        self, cont: Continuation, payload: ChainPayload, result: Any
    ) -> ChainHopResult:
        """Run one hop in-process, on the origin's event loop.

        Args:
            cont: The continuation.
            payload: The shared payload.
            result: The result object for THIS hop (already isolated by
                :meth:`_result_for`).

        Returns:
            A ChainHopResult; failures are captured, never raised.
        """
        from .task import Task
        hop_id = str(uuid.uuid4())
        program = cont.program or self.task._program
        chain_input = payload.model_copy(update={"result": result})
        
        kwargs = self._hop_kwargs(cont, payload)
        task_instance = Task(
            task_id=hop_id,
            task=cont.task,
            program=program,
            loop=self.task._loop,
            chain_input=chain_input,
            **kwargs
        )
        try:
            await task_instance.start()
            await task_instance.run()
            return ChainHopResult(
                step_name=cont.step_name,
                program=program,
                task=cont.task,
                status="success",
                mode="inline",
                hop_task_id=hop_id,
            )
        except Exception as exc:  # noqa: BLE001 — a failing hop must never abort the run (AC-13)
            return ChainHopResult(
                step_name=cont.step_name,
                program=program,
                task=cont.task,
                status="failed",
                mode="inline",
                hop_task_id=hop_id,
                reason=str(exc),
            )
        finally:
            await task_instance.close()

    async def _dispatch_remote(
        self, index: int, cont: Continuation, payload: ChainPayload, result: Any
    ) -> ChainHopResult:
        """Stage the payload in Redis and fire the hop through an executor.

        Args:
            index: The hop's index among the origin's continuations (key suffix).
            cont: The continuation.
            payload: The shared payload.
            result: The result object for this hop (may be None).

        Returns:
            A ChainHopResult carrying the ExecutionHandle's execution_id.
        """
        program = cont.program or self.task._program
        try:
            staged = payload.model_copy(update={"result": result})
            try:
                key = await self.exchange.put(staged, str(self.task.task_id), index)
            except ChainEncodingError as exc:
                return ChainHopResult(
                    step_name=cont.step_name,
                    program=program,
                    task=cont.task,
                    status="failed",
                    mode="remote",
                    reason=f"Encoding failure: {exc}",
                )
            
            executor = resolve_executor({"executor": cont.executor}, None)
            hop_id = str(uuid.uuid4())
            
            kwargs = self._hop_kwargs(cont, payload)
            # Only pass `priority` when the step set one explicitly. Passing
            # `priority=None` unconditionally shadows the KEY itself in
            # **kwargs, so `QworkerJobExecutor.dispatch`'s
            # `kwargs.pop("priority", self._config.priority)` (qworker.py)
            # returns None instead of falling back to the executor's own
            # configured default priority.
            if cont.priority is not None:
                kwargs["priority"] = cont.priority
            handle = await executor.dispatch(
                program,
                cont.task,
                hop_id,
                chain_key=key,
                **kwargs
            )
            
            executor_type_name = getattr(executor, "type", "unknown")
            if hasattr(executor_type_name, "value"):
                executor_type_name = executor_type_name.value
                
            return ChainHopResult(
                step_name=cont.step_name,
                program=program,
                task=cont.task,
                status="success",
                mode=f"remote:{executor_type_name}",
                hop_task_id=hop_id,
                execution_id=handle.execution_id,
            )
        except Exception as exc:  # noqa: BLE001 — a failing hop must never abort the run (AC-13)
            return ChainHopResult(
                step_name=cont.step_name,
                program=program,
                task=cont.task,
                status="failed",
                mode="remote",
                reason=str(exc),
            )

    async def _run_hop(
        self, index: int, cont: Continuation, payload: ChainPayload, result: Any
    ) -> ChainHopResult:
        """Route one hop to the inline or the remote path."""
        if cont.executor == INLINE:
            return await self._run_inline(cont, payload, result)
        else:
            return await self._dispatch_remote(index, cont, payload, result)

    async def _refusal_result(self, cont: Continuation, reason: str) -> ChainHopResult:
        """Build the result for a hop that will not run, and log/notify it."""
        is_refusal = reason.startswith("refused:")
        status = "refused" if is_refusal else "skipped"

        target_program = cont.program or self.task._program
        target = f"{target_program}.{cont.task}"

        if is_refusal:
            self.logger.warning(
                "Hop %s (%s) refused: %s",
                cont.step_name,
                target,
                reason
            )
            if not getattr(self.task, "_no_events", False):
                try:
                    # NotifyEvent is a plain, awaitable callable (flowtask/events/events/notify_event.py) —
                    # Task normally attaches it to a named EventManager slot (e.g.
                    # `self._events.data_not_found += NotifyEvent(event="warning")`,
                    # task.py:167) and fires it via that slot. There is no pre-wired
                    # slot for a refused NextTask hop, and `Task`/`AbstractTask` has
                    # no `emit_event` method, so construct and await one directly
                    # instead — `__call__` expects `task` (the real Task object, for
                    # `task.getProgram()`/`task.taskname`), `component`, and
                    # `message`, exactly as passed here.
                    from ..events import NotifyEvent
                    event = NotifyEvent(event="warning")
                    await event(
                        task=self.task,
                        component=cont.step_name,
                        message=f"Hop {cont.step_name} ({target}) refused: {reason}",
                    )
                except Exception as exc:  # noqa: BLE001 — notifying must never abort the run (AC-13)
                    self.logger.warning("Failed to emit refusal notification: %s", exc)
        else:
            self.logger.info(
                "Hop %s (%s) skipped: %s",
                cont.step_name,
                target,
                reason
            )
            
        return ChainHopResult(
            step_name=cont.step_name,
            program=target_program,
            task=cont.task,
            status=status,
            mode="inline" if cont.executor == INLINE else "remote",
            reason=reason,
        )

    async def run(self) -> list[ChainHopResult]:
        """Run every eligible continuation of the origin task.

        Returns:
            One ChainHopResult per declared continuation, in declaration order.
            Ordinary exceptions never propagate; asyncio.CancelledError does,
            after the pending hops are marked ``cancelled``.
        """
        try:
            return await self._run()
        finally:
            # `self.exchange` (the property) lazily creates a ResultExchange
            # on first use by a remote hop; nothing else in this class ever
            # closed it, leaking a Redis client/connection per run that
            # dispatches at least one remote hop. Only close it when it was
            # actually created — a run with no remote hops never touches
            # Redis at all.
            if self._exchange is not None:
                await self._exchange.close()

    async def _run(self) -> list[ChainHopResult]:
        """The real body of :meth:`run`, wrapped there for exchange cleanup."""
        payload = self.build_payload()
        continuations = getattr(self.task, "_continuations", [])
        
        # 1. Evaluate eligibility for all continuations first
        eligibility_results = []
        eligible_hops = []  # list of (index, cont, result_obj)
        
        # Count eligible inline consumers with cont.result truthy
        inline_consumers = 0
        for index, cont in enumerate(continuations):
            eligible, reason = self.eligible(cont, payload)
            if eligible:
                if cont.executor == INLINE and cont.result:
                    inline_consumers += 1
                eligibility_results.append((True, None))
            else:
                eligibility_results.append((False, reason))
                
        # 2. Build isolated results for eligible hops
        for index, cont in enumerate(continuations):
            eligible, reason = eligibility_results[index]
            if eligible:
                res_obj = self._result_for(cont, payload, inline_consumers)
                eligible_hops.append((index, cont, res_obj))
                
        # 3. Split eligible hops into batch 1 and batch 2
        # batch 1: eligible remote hops + eligible inline hops whose program == task._program
        # batch 2: remaining inline hops (cross-program)
        batch1 = []
        batch2 = []
        for index, cont, res_obj in eligible_hops:
            cont_program = cont.program or self.task._program
            if cont.executor != INLINE or cont_program == self.task._program:
                batch1.append((index, cont, res_obj))
            else:
                batch2.append((index, cont, res_obj))
                
        # We will store results by index
        final_results: dict[int, ChainHopResult] = {}
        
        # Fill in refused/skipped results immediately
        for index, cont in enumerate(continuations):
            eligible, reason = eligibility_results[index]
            if not eligible:
                final_results[index] = await self._refusal_result(cont, reason)
                
        # 4. Execute batches
        try:
            # Batch 1: concurrent execution
            if batch1:
                tasks = [
                    self._run_hop(index, cont, payload, res_obj)
                    for index, cont, res_obj in batch1
                ]
                batch1_results = await asyncio.gather(*tasks, return_exceptions=True)
                for (index, cont, res_obj), res in zip(batch1, batch1_results):
                    if isinstance(res, asyncio.CancelledError):
                        # gather(return_exceptions=True) returns a per-child
                        # CancelledError as a plain value rather than raising
                        # it — CancelledError is a BaseException, not an
                        # Exception, so it must be checked before the
                        # Exception branch below or it would fall through
                        # to `else` and store the raw exception object where
                        # a ChainHopResult is required (AC-28).
                        final_results[index] = ChainHopResult(
                            step_name=cont.step_name,
                            program=cont.program or self.task._program,
                            task=cont.task,
                            status="cancelled",
                            mode="inline" if cont.executor == INLINE else "remote",
                            reason="Hop cancelled",
                        )
                    elif isinstance(res, Exception):
                        final_results[index] = ChainHopResult(
                            step_name=cont.step_name,
                            program=cont.program or self.task._program,
                            task=cont.task,
                            status="failed",
                            mode="inline" if cont.executor == INLINE else "remote",
                            reason=str(res),
                        )
                    else:
                        final_results[index] = res
                        
            # Batch 2: sequential execution
            for index, cont, res_obj in batch2:
                try:
                    res = await self._run_hop(index, cont, payload, res_obj)
                    final_results[index] = res
                except Exception as exc:  # noqa: BLE001 — a failing hop must never abort the run (AC-13)
                    final_results[index] = ChainHopResult(
                        step_name=cont.step_name,
                        program=cont.program or self.task._program,
                        task=cont.task,
                        status="failed",
                        mode="inline",
                        reason=str(exc),
                    )
        except asyncio.CancelledError:
            # Mark all hops that don't have a result yet as cancelled
            for index, cont in enumerate(continuations):
                if index not in final_results:
                    final_results[index] = ChainHopResult(
                        step_name=cont.step_name,
                        program=cont.program or self.task._program,
                        task=cont.task,
                        status="cancelled",
                        mode="inline" if cont.executor == INLINE else "remote",
                        reason="Task execution cancelled",
                    )
            raise
            
        # Return in declaration order
        return [final_results[i] for i in range(len(continuations))]