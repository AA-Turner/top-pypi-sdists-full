"""Trace-root + callback-driven boundary for langchain_core-callback handlers.

Mixed into :class:`~aigie.tracing.lc_callback_base.LangChainCallbackBase`. Owns
the workflow (root) span — used by both modes — plus the callback-driven trace
boundary: when ``callback_driven`` is set, the base opens the workflow span from
the first root event (capturing THAT event's input, so the trace root always
carries the invocation input) and finalizes on the matching root end.
Bridge-driven integrations (LangGraph) leave the flag False; the bridge opens
and closes the workflow span and the ``_note_*`` hooks are no-ops.
"""

from __future__ import annotations

import asyncio
import logging
import threading
from contextlib import suppress
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import UUID

from aigie.tracing.trace_state import (
    close_ambient,
    current_trace_id,
    is_inside_traced_run,
    mark_root_closed,
    open_ambient,
    root_already_closed,
)
from aigie.tracing.workflow_root import WorkflowRoot

if TYPE_CHECKING:
    from aigie.tracing.execution_state import ExecutionState
    from aigie.tracing.span_event_handler import SpanEventHandler

# A stream abandoned before exhaustion (caller breaks early, or its task is
# cancelled) raises these; finalize such a root as interrupted, not a real error.
_ABANDONED_STREAM_EXC = (GeneratorExit, asyncio.CancelledError)

_log = logging.getLogger(__name__)


_counters_lock = threading.Lock()


def trace_run_counters(trace: Any) -> dict[str, Any]:
    """The trace's own run counters — ``tool_calls`` and ``turn_count``.

    The root row is stamped ``span_id == trace_id``, so its counters describe
    the *trace*: an interrupt and its resume share that row, and so do several
    runs a caller wraps in a trace of their own. A per-handler count put
    whichever run closed first onto that row and called it the whole trace.
    Keeping the tally on the trace makes the order those runs close in
    irrelevant, and it needs no registry — it dies with the trace.
    """
    counters: dict[str, Any] | None = getattr(trace, "_aigie_run_counters", None)
    if counters is not None:
        return counters
    with _counters_lock:
        # Re-read under the lock. Two runs starting together on the same trace
        # would otherwise each attach their own dict, and the close would stamp
        # the root from whichever attached last — losing the other's counts.
        counters = getattr(trace, "_aigie_run_counters", None)
        if counters is None:
            counters = {"tool_calls": 0, "turn_count": 0}  # plus "agent"/"status" at close
            with suppress(AttributeError):
                trace._aigie_run_counters = counters
    return counters


# Worst-wins ordering for a trace that hosted more than one run: a clean run
# must not paper over a failed one, and two failures keep the more severe.
_STATUS_RANK = {"success": 0, "interrupted": 1, "error": 2}


def worst_status(current: str | None, candidate: str) -> str:
    """The more severe of two run outcomes."""
    if current is None:
        return candidate
    return max(current, candidate, key=lambda s: _STATUS_RANK.get(s, 0))


def bump(counters: dict[str, Any], key: str, delta: int = 1) -> None:
    """Move a counter, safely, with zero as the floor.

    ``d[k] += 1`` is load-add-store, so two threads can lose a step between
    them — and LangGraph dispatches node callbacks from a threadpool, while two
    runs sharing a caller's trace can finish at once. A lost ``open_runs``
    decrement would leave a completed trace reporting ``interrupted``.
    """
    with _counters_lock:
        counters[key] = max(0, counters.get(key, 0) + delta)


def record_status(counters: dict[str, Any], status: str) -> None:
    """Keep the worst outcome any run on this trace reported."""
    with _counters_lock:
        counters["status"] = worst_status(counters.get("status"), status)


class LangChainTraceBoundary:
    """Workflow-span lifecycle + opt-in callback-driven trace boundary."""

    callback_driven: bool = False

    if TYPE_CHECKING:  # host state provided by LangChainCallbackBase
        spans: SpanEventHandler
        _execution: ExecutionState
        framework_name: str
        _WORKFLOW_RUN_ID: str
        _workflow_name: str
        _suppressed: bool
        _root_run_id: str | None
        _trace_id: str | None
        _ambient_token: Any
        _workflow_root: WorkflowRoot | None
        _counters: dict[str, Any]
        _owns_trace: bool

    def _note_start(
        self,
        run_id: UUID,
        parent_run_id: UUID | None,
        name: str,
        input: Any,
        *,
        set_workflow_name: bool = True,
    ) -> bool:
        """Top of every *_start handler; True skips this event's span."""
        if not self.callback_driven:
            return False
        if self._suppressed:
            return True
        if self._root_run_id is None:
            return self._open_callback_root(
                run_id, name, input, set_workflow_name=set_workflow_name
            )
        # async dispatches each sync callback in its own copied context, so
        # re-assert the ambient trace_id here for open_span's _require_trace_id().
        if current_trace_id() != self._trace_id:
            open_ambient(trace_id=self._trace_id)  # type: ignore[arg-type]
        return False

    def _open_callback_root(
        self, run_id: UUID, name: str, input: Any, *, set_workflow_name: bool = True
    ) -> bool:
        # LangGraph runs on langchain_core, so the configure hook fires for it
        # too; stand down when its bridge already owns the ambient trace.
        if is_inside_traced_run():
            self._suppressed = True
            return True
        if set_workflow_name:
            self._workflow_name = name or self._workflow_name
        # In-function import breaks the tracing → auto_instrument → client cycle.
        from aigie.auto_instrument.trace import get_current_trace, get_or_create_trace_sync

        # A trace that is already current will be adopted rather than minted.
        adopted = get_current_trace() is not None
        trace = get_or_create_trace_sync(
            name=self._workflow_name,
            metadata={"framework": self.framework_name, "type": self.framework_name},
        )
        if trace is None:  # not initialized / zero-retention
            self._suppressed = True
            return True
        if adopted and root_already_closed(str(trace.id)):
            # Joined a finished run's trace. A root opened here is stamped
            # span_id == trace_id, so it overwrites that run's name and output
            # with this call's. Provider-level instrumentation still records
            # the call itself.
            self._suppressed = True
            return True
        self._root_run_id = str(run_id)
        self._trace_id = str(trace.id)
        self._owns_trace = not adopted
        self._counters = trace_run_counters(trace)
        # Claimed at open, not at close: a caller's ``async with`` can exit
        # before an abandoned stream tears down, and the trace close has to
        # find these already there.
        self._counters.setdefault("agent", self._workflow_name)
        bump(self._counters, "open_runs")
        self._ambient_token = open_ambient(trace_id=self._trace_id)
        self.open_workflow_span(input=input, span_id=self._trace_id)
        return False

    def _note_end(
        self, run_id: UUID, *, output: Any = None, error: BaseException | None = None
    ) -> None:
        """After every *_end / *_error; finalizes the trace on the root run end."""
        if not self.callback_driven:
            return
        if self._root_run_id is None or str(run_id) != self._root_run_id:
            return
        self.close_workflow_span(output=output, error=error)
        self._root_run_id = None
        if self._ambient_token is not None:
            # async may run this in a different copied context than the start that
            # created the token; reset() then raises — that context is discarded.
            with suppress(ValueError, LookupError):
                close_ambient(self._ambient_token)
            self._ambient_token = None

    # ------------------------------------------------------------------
    # Workflow (root) span — used by both bridge- and callback-driven modes
    # ------------------------------------------------------------------

    def open_workflow_span(self, *, input: Any, span_id: str | None = None) -> None:
        # The workflow span IS the trace root (span_id == trace_id). The shared
        # WorkflowRoot owns the span mechanics; this boundary keeps the LangChain
        # extras: ExecutionState bookkeeping + the execution-plan metadata.
        if input is None:
            # Backstop: a root with no input shows blank "user input" in the UI.
            # Structurally prevented for callback-driven integrations (the base
            # captures the root event's input); fires only on a future regression.
            _log.debug(
                "%s opened workflow root span with input=None; executions UI will show "
                "no user input",
                self.framework_name,
            )
        from aigie.context_manager import merge_tags

        tags = merge_tags()
        self._workflow_root = WorkflowRoot(
            self.spans,
            self._workflow_name,
            trace_id=span_id or current_trace_id(),  # type: ignore[arg-type]
            framework=self.framework_name,
            input=input,
            extras={"tags": tags} if tags else None,
            run_id=self._WORKFLOW_RUN_ID,
        )
        self._execution.start_span(
            name=self._workflow_name, span_type="workflow", at=datetime.now(timezone.utc)
        )

    def close_workflow_span(
        self, *, output: Any = None, error: BaseException | None = None
    ) -> None:
        now = datetime.now(timezone.utc)
        if error is None:
            status = "success"
        elif isinstance(error, _ABANDONED_STREAM_EXC):
            # Caller broke out of / cancelled a stream before it finished — the
            # run was abandoned, not a success and not a real error.
            status = "interrupted"
        else:
            status = "error"
        self._adopt_trace_counters(status)
        # Run-level data the legacy trace_update carried is folded onto the root.
        metadata_updates = self._root_metadata_updates(status)
        self._execution.end_span(
            name=self._workflow_name,
            status=status,
            at=now,
            error_message=str(error) if status == "error" else None,
        )
        root = getattr(self, "_workflow_root", None)
        if root is None:
            return
        mark_root_closed(getattr(self, "_trace_id", None) or current_trace_id())
        # Omitting a null output lets WorkflowRoot fall back to note_root_output.
        if output is None:
            root.close(error=error, status=status, metadata_updates=metadata_updates)
        else:
            root.close(output=output, error=error, status=status, metadata_updates=metadata_updates)

    def note_root_output(self, value: Any) -> None:
        """Record the framework's own final output for the run.

        A streamed run yields chunks and returns nothing for the wrapper to
        carry, but LangGraph still reports the final state on the root-level
        ``on_chain_end``. Used only as a fallback — an entrypoint return value
        wins.
        """
        root = getattr(self, "_workflow_root", None)
        if root is not None:
            root.note_output(value)

    def _adopt_trace_counters(self, status: str) -> None:
        """Take the trace's totals, and leave our labels for its close.

        That close knows the trace's counters but not which agent ran, and its
        own status says nothing about a failure the caller caught inside their
        ``async with``. First agent wins; the worst status wins.
        """
        self._execution.tool_call_count = self._counters["tool_calls"]
        self._execution.turn_count = self._counters["turn_count"]
        self._counters.setdefault("agent", self._workflow_name)
        bump(self._counters, "open_runs", -1)
        if status != "success":
            record_status(self._counters, status)

    def _root_metadata_updates(self, status: str) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "framework": self.framework_name,
            "type": self.framework_name,
            "turn_count": self._execution.turn_count,
        }
        # Only the trace's owner summarises it. Where a caller wraps several
        # runs in one trace they all write this row, and each one's totals are
        # stale the moment the next tool runs — so under a last-write-wins
        # merge whichever write lands last decides the count. The caller's own
        # close is the single writer there, and the only one that sees the
        # whole trace.
        if getattr(self, "_owns_trace", True):
            metadata["execution_plan"] = self._execution.to_execution_plan(
                agent_name=self._workflow_name, status=status
            )
        execution_data = self._execution.to_execution_data()
        if execution_data["execution_path"]:
            metadata["execution_data"] = execution_data
        catalog_hash = getattr(self, "_aigie_tool_registry_hash", None)
        if catalog_hash:
            metadata["tool_registry_hash"] = catalog_hash
        return metadata
