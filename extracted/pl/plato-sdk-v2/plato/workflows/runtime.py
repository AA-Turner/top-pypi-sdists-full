"""Workflow runtime: the injected script primitives over an agent backend.

The runtime owns the namespace a compiled workflow script executes against:
``{"agent", "parallel", "pipeline", "phase", "log", "budget", "args"}``.

Semantics (parity with the local Claude Code Workflow tool):

* ``agent(prompt, **opts) -> str | dict | None`` — soft-fails to ``None`` for
  any agent-side problem; raises ONLY :class:`BudgetExceededError`,
  :class:`WorkflowCancelledError`, and :class:`WorkflowLimitError`.
* ``parallel(thunks)`` — barrier; a failed thunk yields ``None`` in its slot;
  agent failures never raise out of the call. Workflow-level stops DO propagate
  (cancellation, ``BudgetExceededError``, ``WorkflowLimitError``) and cancel
  sibling thunks — a budget stop is not a per-call outcome.
* ``pipeline(items, *stages)`` — NO barrier between stages: each item flows
  through all stages independently. Stage callbacks receive
  ``(prev_result, original_item, index)`` (the first stage's ``prev_result``
  is the item itself). A stage raising drops that item to ``None`` and skips
  its remaining stages.
* ``phase(title)`` — closes the previous phase span and opens a new
  ``workflow.phase`` span (attribute ``plato.workflow.phase``).
* ``log(msg)`` — narrator line on the ``plato.workflows.narrator`` logger
  (surfaced as an OTel log span by :class:`plato.otel.OTelSpanLogHandler`).
* ``budget`` — the :class:`~plato.workflows.budget.Budget` instance itself.
* ``args`` — the submission's args value, verbatim.

Concurrency: a single :class:`asyncio.Semaphore` (``max_concurrent_envs``)
wraps ``backend.run_call`` ONLY — journal cache hits and budget
rejections never touch it.
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import inspect
import json
import logging
import time
from collections.abc import Awaitable, Callable, Iterable, Sequence
from contextvars import Token
from typing import Any, Literal

from opentelemetry import context as otel_context
from opentelemetry import trace
from opentelemetry.context import Context
from pydantic import BaseModel, Field

from plato.otel import get_tracer
from plato.workflows.backend import (
    AgentBackend,
    AgentCallOpts,
    AgentCallOutcome,
    AgentCallRequest,
    canonical_json,
    derive_call_key,
)
from plato.workflows.budget import Budget
from plato.workflows.errors import (
    BudgetExceededError,
    WorkflowCancelledError,
    WorkflowError,
    WorkflowLimitError,
)
from plato.workflows.journal import Journal, JournalRecord
from plato.workflows.script import CompiledWorkflow, compile_workflow_script

logger = logging.getLogger(__name__)


def json_safe(value: Any) -> Any:
    """Return ``value`` if JSON-serializable, else a loud diagnostic placeholder.

    The script's return value is script-controlled; a non-JSON value (a set, a
    custom object, an un-awaited coroutine that slipped past the compile lint)
    must degrade to a diagnostic instead of poisoning the journal's
    workflow_result record or the world's state upload.
    """
    try:
        json.dumps(value)
    except (TypeError, ValueError):
        return {"__unserializable__": type(value).__name__, "repr": repr(value)[:2000]}
    return value


narrator = logging.getLogger("plato.workflows.narrator")

__all__ = [
    "WorkflowRuntime",
    "WorkflowStats",
    "canonical_json",
    "derive_call_key",
]


def _label_slug(value: str) -> str:
    """Checkpoint-label-safe slug for free-form text (phase titles)."""
    slug = "".join(char if char.isalnum() else "-" for char in value.lower()).strip("-")
    return slug[:60] or "phase"


class WorkflowStats(BaseModel):
    """Live counters for a single workflow run."""

    calls_total: int = 0
    calls_cached: int = 0
    calls_failed: int = 0
    phases: list[str] = Field(default_factory=list)


class WorkflowRuntime:
    """Executes one compiled workflow against a backend/journal/budget triple."""

    def __init__(
        self,
        *,
        backend: AgentBackend,
        journal: Journal,
        budget: Budget,
        args: Any,
        max_concurrent_envs: int = 30,
        max_total_calls: int = 1000,
        cancel_event: asyncio.Event | None = None,
        checkpoint_requested: Callable[[str], None] | None = None,
        on_call_complete: Callable[[], Awaitable[Any]] | None = None,
    ) -> None:
        self._backend = backend
        self._journal = journal
        self._budget = budget
        self._args = args
        self._max_total_calls = max_total_calls
        self._cancel_event = cancel_event if cancel_event is not None else asyncio.Event()
        # Non-blocking durability signal to the owner (world/service): invoked
        # with a label after phase boundaries and merged (merge_to_main)
        # call_results so the journal workspace is checkpointed promptly
        # instead of waiting out the 120s periodic sweep (spec landmine 8).
        self._checkpoint_requested = checkpoint_requested
        # Forced budget refresh after each non-cached backend outcome so a
        # completed wave re-arms the spend ceiling before the next dispatch's
        # budget.check(). Public + settable: the service assigns it after its
        # runtime factory has built the runtime.
        self.on_call_complete = on_call_complete
        self._semaphore = asyncio.Semaphore(max(1, max_concurrent_envs))
        self._stats = WorkflowStats()
        self._tracer = get_tracer("plato.workflows")

        self._call_seq = 0
        self._occurrences: dict[str, int] = {}
        # Serializes seq assignment + append so file order == seq order.
        self._journal_lock = asyncio.Lock()
        self._pending_appends: set[asyncio.Task[None]] = set()

        self._phase_span: trace.Span | None = None
        self._phase_token: Token[Context] | None = None
        self._current_phase: str | None = None

    # -- public surface ------------------------------------------------------

    @property
    def stats(self) -> WorkflowStats:
        return self._stats

    def namespace(self) -> dict[str, Any]:
        """The globals injected into the workflow script."""
        return {
            "agent": self._agent,
            "parallel": self._parallel,
            "pipeline": self._pipeline,
            "phase": self._phase,
            "log": self._log,
            "budget": self._budget,
            "args": self._args,
            "workflow": self._workflow,
        }

    async def _workflow(self, source: str, args: Any = None) -> Any:
        """Run a child workflow script inline and return its result.

        The child executes against THIS runtime — same journal (so its
        ``agent()`` calls replay content-keyed exactly like the parent's),
        same budget, semaphore, call counter, and cancellation. Only two
        globals differ: ``args`` (the child's own) and ``workflow`` (raises —
        one nesting level, matching the local Workflow tool).

        Unlike ``agent()``, this RAISES on failure: a child compile error
        raises :class:`WorkflowScriptError` and a child script exception
        propagates — composition errors are script bugs, not agent outcomes.
        """
        self._raise_if_cancelled()
        compiled = compile_workflow_script(source)
        for warning in compiled.lint_warnings:
            logger.warning("child workflow lint: %s", warning)

        async def _no_nesting(*_args: Any, **_kwargs: Any) -> Any:
            raise WorkflowError("workflow() cannot be nested more than one level deep")

        child_ns = self.namespace()
        child_ns["args"] = args
        child_ns["workflow"] = _no_nesting
        with self._tracer.start_as_current_span("workflow.child") as span:
            span.set_attribute("plato.workflow.child_script_sha256", compiled.fingerprint)
            return await compiled.run(child_ns)

    async def run(self, compiled: CompiledWorkflow) -> Any:
        """Run the compiled script to completion; returns the script's result."""
        self._raise_if_cancelled()
        for warning in compiled.lint_warnings:
            logger.warning("workflow lint: %s", warning)
        args_json = self._safe_canonical_args()
        await self._append_record(
            type="workflow_started",
            payload={
                "script_sha256": compiled.fingerprint,
                "args_sha256": hashlib.sha256(args_json.encode("utf-8")).hexdigest(),
            },
        )
        try:
            result = json_safe(await compiled.run(self.namespace()))
        except WorkflowCancelledError as exc:
            await self._finalize("cancelled", error=str(exc) or "workflow cancelled")
            raise
        except Exception as exc:
            await self._finalize("error", error=f"{type(exc).__name__}: {exc}")
            raise
        else:
            await self._finalize("ok", result=result)
            return result

    # -- injected primitives ---------------------------------------------------

    async def _agent(
        self,
        prompt: str,
        *,
        label: str | None = None,
        phase: str | None = None,
        schema: dict[str, Any] | None = None,
        agent: str = "default",
        model: str | None = None,
        effort: str | None = None,
        workspace: str | None = None,
        data: bool | list[str] = False,
        sync: Literal["publish_ref", "merge_to_main"] = "publish_ref",
        base: str | None = None,
        timeout_s: float | None = None,
    ) -> Any:
        self._raise_if_cancelled()
        if self._stats.calls_total >= self._max_total_calls:
            raise WorkflowLimitError(f"workflow exceeded max_total_calls={self._max_total_calls}")
        self._stats.calls_total += 1

        opts = AgentCallOpts(
            label=label,
            phase=phase if phase is not None else self._current_phase,
            output_schema=schema,
            agent=agent,
            model=model,
            effort=effort,
            workspace=workspace,
            data=data,
            sync=sync,
            base=base,
            timeout_s=timeout_s,
        )
        key = derive_call_key(prompt, opts)
        occurrence = self._occurrences.get(key, 0)
        self._occurrences[key] = occurrence + 1
        self._call_seq += 1
        call_id = f"c{self._call_seq:04d}-{key}"

        # Journal replay — cache hits are free (no budget check, no semaphore).
        cached = self._journal.claim_replay(key)
        if cached is not None:
            self._stats.calls_cached += 1
            narrator.info("agent call %s replayed from journal (cached_from=%s)", call_id, cached.call_id)
            await self._append_record(
                type="call_result",
                key=key,
                occurrence=occurrence,
                call_id=call_id,
                status="ok",
                result=cached.result,
                published_ref=cached.published_ref,
                merged=cached.merged,
                attempts=cached.attempts,
                cost_usd=0.0,
                cached_from=cached.call_id,
                label=opts.label,
                phase=opts.phase,
            )
            return cached.result

        self._budget.check()

        await self._append_record(
            type="call_started",
            key=key,
            occurrence=occurrence,
            call_id=call_id,
            label=opts.label,
            phase=opts.phase,
        )
        request = AgentCallRequest(
            call_id=call_id,
            workflow_id=self._journal.workflow_id,
            key=key,
            occurrence=occurrence,
            prompt=prompt,
            opts=opts,
        )

        with self._tracer.start_as_current_span("workflow.call") as span:
            span.set_attribute("plato.workflow.call_id", call_id)
            span.set_attribute("plato.workflow.key", key)
            span.set_attribute("plato.workflow.occurrence", occurrence)
            if opts.label is not None:
                span.set_attribute("plato.workflow.label", opts.label)
            if opts.phase is not None:
                span.set_attribute("plato.workflow.phase", opts.phase)
            try:
                async with self._semaphore:
                    outcome = await self._run_backend_call(request)
            except WorkflowCancelledError:
                span.set_attribute("plato.workflow.status", "cancelled")
                # _run_backend_call's finally awaited the backend teardown, so
                # any salvage the execution manager ran during the cancel
                # unwind has completed — collect its ref for the record.
                salvage_ref = self._backend.take_cancelled_salvage_ref(call_id)
                if salvage_ref:
                    span.set_attribute("plato.workflow.salvage_ref", salvage_ref)
                    narrator.info(
                        "agent call %s cancelled — git state salvaged to %s",
                        call_id,
                        salvage_ref,
                    )
                await self._append_record(
                    type="call_result",
                    key=key,
                    occurrence=occurrence,
                    call_id=call_id,
                    status="error",
                    error="workflow cancelled while call in flight",
                    salvage_ref=salvage_ref,
                    label=opts.label,
                    phase=opts.phase,
                )
                raise
            except Exception as exc:
                logger.exception("workflow call %s: backend raised", call_id)
                outcome = AgentCallOutcome(status="error", error=f"{type(exc).__name__}: {exc}")
            span.set_attribute("plato.workflow.status", outcome.status)

        result: Any = None
        if outcome.status == "ok":
            result = outcome.result_json if opts.output_schema is not None else outcome.result_text
        else:
            self._stats.calls_failed += 1
            if outcome.salvage_ref:
                narrator.info(
                    "agent call %s failed: %s (%s) — git state salvaged to %s",
                    call_id,
                    outcome.status,
                    outcome.error,
                    outcome.salvage_ref,
                )
            else:
                narrator.info("agent call %s failed: %s (%s)", call_id, outcome.status, outcome.error)

        payload = {"agent_task_span_id": outcome.agent_task_span_id} if outcome.agent_task_span_id else None
        await self._append_record(
            type="call_result",
            key=key,
            occurrence=occurrence,
            call_id=call_id,
            status=outcome.status,
            result=result,
            published_ref=outcome.published_ref,
            salvage_ref=outcome.salvage_ref,
            merged=outcome.merged,
            attempts=outcome.attempts,
            cost_usd=outcome.cost_usd,
            error=outcome.error,
            label=opts.label,
            phase=opts.phase,
            payload=payload,
        )
        if outcome.merged:
            # A merge_to_main result landed in shared main — make its journal
            # record durable promptly (spec landmine 8).
            self._request_checkpoint(f"workflow_merge_{call_id}")
        if self.on_call_complete is not None:
            # Best-effort forced budget refresh: the ceiling is enforced by the
            # dispatch-time budget.check(), this just keeps it current so the
            # next wave cannot dispatch against poll-interval-stale spend.
            try:
                await self.on_call_complete()
            except Exception:
                logger.warning("on_call_complete hook failed for %s", call_id, exc_info=True)
        return result

    async def _parallel(self, thunks: Iterable[Callable[[], Any] | Awaitable[Any]]) -> list[Any]:
        """Barrier over independent thunks; failed thunks yield None slots."""
        self._raise_if_cancelled()
        tasks = [asyncio.ensure_future(self._run_thunk(thunk)) for thunk in thunks]
        return await self._gather_or_cancel(tasks)

    async def _pipeline(
        self,
        items: Iterable[Any],
        *stages: Callable[[Any, Any, int], Any],
    ) -> list[Any]:
        """Flow each item through ``stages`` independently — no inter-stage barrier."""
        self._raise_if_cancelled()
        tasks = [
            asyncio.ensure_future(self._run_pipeline_item(item, index, stages)) for index, item in enumerate(items)
        ]
        return await self._gather_or_cancel(tasks)

    def _phase(self, title: str) -> None:
        self._raise_if_cancelled()
        self._close_phase_span()
        span = self._tracer.start_span("workflow.phase")
        span.set_attribute("plato.workflow.phase", title)
        self._phase_token = otel_context.attach(trace.set_span_in_context(span))
        self._phase_span = span
        self._current_phase = title
        self._stats.phases.append(title)
        narrator.info("phase: %s", title)
        self._schedule_append(type="phase", phase=title)
        self._request_checkpoint(f"workflow_phase_{_label_slug(title)}")

    def _log(self, msg: Any) -> None:
        narrator.info("%s", msg)

    # -- internals ---------------------------------------------------------

    def _raise_if_cancelled(self) -> None:
        if self._cancel_event.is_set():
            raise WorkflowCancelledError("workflow cancelled")

    def _request_checkpoint(self, label: str) -> None:
        """Signal the owner that a durability point was reached (best-effort)."""
        if self._checkpoint_requested is None:
            return
        try:
            self._checkpoint_requested(label)
        except Exception:
            logger.warning("checkpoint request hook failed (label=%s)", label, exc_info=True)

    def _safe_canonical_args(self) -> str:
        try:
            return canonical_json(self._args)
        except (TypeError, ValueError):
            return repr(self._args)

    async def _run_backend_call(self, request: AgentCallRequest) -> AgentCallOutcome:
        """Await the backend, racing the cancel event.

        ``call_task`` is torn down on EVERY exit path in the ``finally`` —
        including external cancellation of this coroutine (serve-loop shutdown,
        executor cancellation, sibling cancellation in ``_gather_or_cancel``):
        ``asyncio.wait`` never cancels its awaitables, so without the explicit
        cancel+await the backend call (and its agent VM) would keep running
        detached with no owner.
        """
        call_task = asyncio.ensure_future(self._backend.run_call(request))
        cancel_task = asyncio.ensure_future(self._cancel_event.wait())
        try:
            done, _ = await asyncio.wait({call_task, cancel_task}, return_when=asyncio.FIRST_COMPLETED)
            if call_task in done:
                return call_task.result()
            raise WorkflowCancelledError("workflow cancelled while agent call in flight")
        finally:
            cancel_task.cancel()
            if not call_task.done():
                call_task.cancel()
            with contextlib.suppress(Exception):
                await asyncio.gather(call_task, cancel_task, return_exceptions=True)

    async def _run_thunk(self, thunk: Callable[[], Any] | Awaitable[Any]) -> Any:
        try:
            value = thunk() if callable(thunk) else thunk
            if inspect.isawaitable(value):
                value = await value
            return value
        except (WorkflowCancelledError, asyncio.CancelledError, BudgetExceededError, WorkflowLimitError):
            # Workflow-level stops are not per-call outcomes: propagate so the
            # gather cancels siblings and the script fails fast, instead of the
            # budget stop masquerading as a wave of agent failures (None slots).
            raise
        except Exception:
            logger.warning("parallel thunk failed; yielding None", exc_info=True)
            return None

    async def _run_pipeline_item(
        self,
        item: Any,
        index: int,
        stages: Sequence[Callable[[Any, Any, int], Any]],
    ) -> Any:
        prev: Any = item
        for stage in stages:
            try:
                value = stage(prev, item, index)
                if inspect.isawaitable(value):
                    value = await value
                prev = value
            except (WorkflowCancelledError, asyncio.CancelledError, BudgetExceededError, WorkflowLimitError):
                # See _run_thunk: budget/limit stops fail the workflow, not the item.
                raise
            except Exception:
                logger.warning("pipeline item %d failed in a stage; dropping to None", index, exc_info=True)
                return None
        return prev

    async def _gather_or_cancel(self, tasks: list[asyncio.Task[Any]]) -> list[Any]:
        """gather() that cancels siblings and re-raises on workflow-level stops.

        Budget/limit stops get the same sibling cleanup as cancellation:
        gather() raises on the first propagating error WITHOUT cancelling the
        rest, and leaving them running would keep paid agent VMs in flight,
        ownerless, on a workflow that is already failing.
        """
        try:
            return list(await asyncio.gather(*tasks))
        except (WorkflowCancelledError, asyncio.CancelledError, BudgetExceededError, WorkflowLimitError):
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

    def _close_phase_span(self) -> None:
        if self._phase_token is not None:
            try:
                otel_context.detach(self._phase_token)
            except Exception:
                # Token/context mismatch (phase() called from a different task)
                # is harmless for span parenting; the span still ends below.
                logger.debug("phase span context detach failed", exc_info=True)
            self._phase_token = None
        if self._phase_span is not None:
            self._phase_span.end()
            self._phase_span = None

    def _schedule_append(self, **fields: Any) -> None:
        """Fire-and-forget journal append for sync callers (phase()).

        Scheduled appends must NOT drain other pending appends: two scheduled
        tasks each draining "pending minus self" await each other — consecutive
        phase() calls deadlocked exactly that way. Creation order == event-loop
        run order for these tasks, so their seq order matches program order
        without draining.
        """
        task = asyncio.create_task(self._append_record(drain=False, **fields))
        self._pending_appends.add(task)
        task.add_done_callback(self._pending_appends.discard)

    async def _append_record(self, drain: bool = True, **fields: Any) -> None:
        # Drain any scheduled fire-and-forget appends (phase()) that were
        # created BEFORE this awaited append: without this, `phase("X")`
        # followed by `await agent(...)` frequently journals call_started with
        # a lower seq than the phase record that precedes it in program order,
        # and seq/file-order divergence makes /events watchers skip or
        # duplicate events. Excluding the current task prevents a scheduled
        # append from deadlocking on itself.
        if drain:
            current = asyncio.current_task()
            pending = [t for t in self._pending_appends if t is not current and not t.done()]
            if pending:
                await asyncio.gather(*pending, return_exceptions=True)
        try:
            async with self._journal_lock:
                record = JournalRecord(seq=self._journal.next_seq(), ts=time.time(), **fields)
                await self._journal.append(record)
        except Exception:
            # A broken journal degrades resume but must not kill the workflow.
            logger.exception("journal append failed (type=%s)", fields.get("type"))

    async def _finalize(self, status: str, *, result: Any = None, error: str | None = None) -> None:
        self._close_phase_span()
        if self._pending_appends:
            await asyncio.gather(*list(self._pending_appends), return_exceptions=True)
        await self._append_record(
            type="workflow_result",
            status=status,
            error=error,
            payload={"result": result} if status == "ok" else None,
        )
