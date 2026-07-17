"""The trace's root (workflow) span, framework-neutral.

``span_id == trace_id``, so the finalized root carries trace identity. Two usage
shapes, one span:

- deferred (Strands): open with no input, then ``note_input`` / ``note_output``
  from invocations (stashed on the span's shared open-state so they survive
  worker threads) and ``close()`` with no args.
- direct (LangChain / LangGraph): open with the root event's input, then
  ``close(output=..., error=..., metadata_updates=...)``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aigie.context_manager import merge_metadata

if TYPE_CHECKING:
    from aigie.tracing.span_event_handler import SpanEventHandler

_PENDING_OUTPUT = "_workflow_pending_output"
_UNSET = object()  # "output not supplied" — fall back to the stashed note_output


class WorkflowRoot:
    def __init__(
        self,
        spans: SpanEventHandler,
        name: str,
        *,
        trace_id: str,
        framework: str,
        input: Any = None,
        extras: dict[str, Any] | None = None,
        run_id: str | None = None,
    ) -> None:
        self._spans = spans
        # run_id is an in-memory key only (never on the wire); callers that track
        # their own root run_id (LangChain's "__workflow__") pass it through.
        self._run_id = run_id or f"__workflow_root__:{trace_id}"
        self._closed = False
        spans.open_span(
            run_id=self._run_id,
            parent_run_id=None,
            name=name,
            span_type="workflow",
            input=input,
            metadata=merge_metadata(
                {"chain_type": "workflow", "framework": framework, "type": framework}
            ),
            extras=extras,
            span_id=trace_id,
        )

    def note_input(self, value: Any) -> None:
        """Set the root input from the first invocation that has one."""
        if value is None:
            return
        state = self._spans.get_state(self._run_id)
        if state is not None and not state.get("input"):
            state["input"] = value

    def note_output(self, value: Any) -> None:
        """Remember the latest invocation output; the last one lands on close."""
        if value is None:
            return
        state = self._spans.get_state(self._run_id)
        if state is not None:
            state[_PENDING_OUTPUT] = value

    def close(
        self,
        *,
        output: Any = _UNSET,
        error: BaseException | None = None,
        status: str | None = None,
        metadata_updates: dict[str, Any] | None = None,
    ) -> None:
        if self._closed:
            return
        self._closed = True
        if output is _UNSET:
            state = self._spans.get_state(self._run_id)
            output = state.get(_PENDING_OUTPUT) if state else None
        # ``status`` lets the caller finalize an abandoned run as "interrupted"
        # rather than as an error; default infers error/success from ``error``.
        if status is None:
            status = "error" if error is not None else "success"
        if status == "error" and error is not None:
            self._spans.fail_span(
                run_id=self._run_id, error=error, metadata_updates=metadata_updates
            )
        else:
            self._spans.close_span(
                run_id=self._run_id,
                output=output,
                metadata_updates=metadata_updates,
                status=status,
            )
