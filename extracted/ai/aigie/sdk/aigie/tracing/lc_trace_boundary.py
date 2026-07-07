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

import logging
from contextlib import suppress
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import UUID

from aigie.tracing.trace_state import (
    close_ambient,
    current_trace_id,
    is_inside_traced_run,
    open_ambient,
)
from aigie.tracing.workflow_root import WorkflowRoot

if TYPE_CHECKING:
    from aigie.tracing.execution_state import ExecutionState
    from aigie.tracing.span_event_handler import SpanEventHandler

_log = logging.getLogger(__name__)


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
        from aigie.auto_instrument.trace import get_or_create_trace_sync

        trace = get_or_create_trace_sync(
            name=self._workflow_name,
            metadata={"framework": self.framework_name, "type": self.framework_name},
        )
        if trace is None:  # not initialized / zero-retention
            self._suppressed = True
            return True
        self._root_run_id = str(run_id)
        self._trace_id = str(trace.id)
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
        status = "error" if error is not None else "success"
        # Run-level data the legacy trace_update carried is folded onto the root.
        metadata_updates = self._root_metadata_updates(status)
        if error is not None:
            self._execution.end_span(
                name=self._workflow_name, status="error", at=now, error_message=str(error)
            )
        else:
            self._execution.end_span(name=self._workflow_name, status="success", at=now)
        root = getattr(self, "_workflow_root", None)
        if root is not None:
            root.close(output=output, error=error, metadata_updates=metadata_updates)

    def _root_metadata_updates(self, status: str) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "framework": self.framework_name,
            "type": self.framework_name,
            "execution_plan": self._execution.to_execution_plan(
                agent_name=self._workflow_name, status=status
            ),
            "turn_count": self._execution.turn_count,
        }
        execution_data = self._execution.to_execution_data()
        if execution_data["execution_path"]:
            metadata["execution_data"] = execution_data
        return metadata
