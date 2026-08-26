"""Strands HookProvider that emits Aigie spans (L3 binding, callback-driven)."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager, suppress
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

from aigie.auto_instrument.trace import get_or_create_trace_sync
from aigie.context_manager import merge_metadata
from aigie.integrations.strands import _spans
from aigie.tracing.execution_state import build_execution_plan
from aigie.tracing.session import current_workflow_root, trace_session
from aigie.tracing.span_event_handler import SpanEventHandler
from aigie.tracing.trace_state import (
    close_ambient,
    current_trace_id,
    is_inside_traced_run,
    open_ambient,
)
from aigie.tracing.usage import llm_span_payload


@dataclass
class _Boundary:
    trace_id: str
    root_inv_key: str | None = None
    ambient_token: Any = None
    tool_catalog_stamped: bool = False
    # Run-level counters for the root's execution_plan. Strands has no
    # ExecutionState (that is the LangChain family's aggregator), so the
    # boundary — already reachable from every hook — is their home.
    turn_count: int = 0
    tool_call_count: int = 0
    errored: bool = False
    # Counted, not just flagged, so a nested orchestrator can ask "did anything
    # fail while I was open?" instead of "did the run fail?". Keyed by ma-span.
    error_count: int = 0
    ma_errors_at_open: dict[str, int] = field(default_factory=dict)

    def note_failure(self) -> None:
        self.errored = True
        self.error_count += 1

    def plan_metadata(self, name: str) -> dict[str, Any]:
        return {
            "execution_plan": build_execution_plan(
                agent=name,
                tool_calls=self.tool_call_count,
                turn_count=self.turn_count,
                status="error" if self.errored else "success",
            )
        }


_boundary: ContextVar[_Boundary | None] = ContextVar("_aigie_strands_boundary", default=None)
_model_stack: ContextVar[tuple[str, ...]] = ContextVar("_aigie_strands_model_stack", default=())

_BASE_META = {"framework": "strands", "type": "strands"}
_NODE_META = {**_BASE_META, "kind": "node"}

# A root_inv_key inside a strands_session that no real invocation key equals, so
# every invocation is a child of the session's workflow root and none finalizes.
_SESSION_SENTINEL = "__aigie_strands_session__"


class StrandsHookProvider:
    """Injected into every Agent/Swarm/Graph hook registry; one shared instance."""

    _is_aigie_handler = True

    def __init__(self, emitter: Any, *, config: Any = None) -> None:
        self._emitter = emitter
        self._config = config
        self.spans = SpanEventHandler(emitter, config=config)

    # -- HookProvider protocol -------------------------------------------------

    def register_hooks(self, registry: Any, **_: Any) -> None:
        from strands.hooks.events import (
            AfterInvocationEvent,
            AfterModelCallEvent,
            AfterToolCallEvent,
            BeforeInvocationEvent,
            BeforeModelCallEvent,
            BeforeToolCallEvent,
        )

        registry.add_callback(BeforeInvocationEvent, self._on_before_invocation)
        registry.add_callback(AfterInvocationEvent, self._on_after_invocation)
        registry.add_callback(BeforeModelCallEvent, self._on_before_model)
        registry.add_callback(AfterModelCallEvent, self._on_after_model)
        registry.add_callback(BeforeToolCallEvent, self._on_before_tool)
        registry.add_callback(AfterToolCallEvent, self._on_after_tool)
        self._register_multi_agent(registry)

    def _register_multi_agent(self, registry: Any) -> None:
        try:
            from strands.hooks.events import (
                AfterMultiAgentInvocationEvent,
                AfterNodeCallEvent,
                BeforeMultiAgentInvocationEvent,
                BeforeNodeCallEvent,
            )
        except ImportError:
            return
        registry.add_callback(BeforeMultiAgentInvocationEvent, self._on_before_multi_agent)
        registry.add_callback(AfterMultiAgentInvocationEvent, self._on_after_multi_agent)
        registry.add_callback(BeforeNodeCallEvent, self._on_before_node)
        registry.add_callback(AfterNodeCallEvent, self._on_after_node)

    # -- Trace boundary --------------------------------------------------------

    def _ensure_trace(self, name: str) -> bool:
        """Open the ambient trace for this context when this handler should emit."""
        if _boundary.get() is not None:
            return True
        if self._zero_retention():
            return False
        if is_inside_traced_run():
            return False
        trace = get_or_create_trace_sync(name=name, metadata=dict(_BASE_META))
        if trace is None:
            return False
        trace_id = str(trace.id)
        token = open_ambient(trace_id=trace_id)
        _boundary.set(_Boundary(trace_id=trace_id, ambient_token=token))
        return True

    def _finalize_trace(self) -> None:
        boundary = _boundary.get()
        if boundary is not None and boundary.ambient_token is not None:
            with suppress(ValueError, LookupError):
                close_ambient(boundary.ambient_token)
        _boundary.set(None)

    # -- Invocation (agent root) ----------------------------------------------

    def _on_before_invocation(self, event: Any) -> None:
        if not self._flag("trace_agents"):
            return
        name = _spans.agent_name(event.agent)
        if not self._ensure_trace(name):
            return
        boundary = _boundary.get()
        assert boundary is not None
        key = f"inv:{id(event.agent)}"
        if boundary.root_inv_key is None:
            boundary.root_inv_key = key
        is_root = key == boundary.root_inv_key
        messages = getattr(event, "messages", None)
        input_value = (
            _spans.messages_to_input(messages, self._limit())
            if self._flag("capture_inputs")
            else None
        )
        metadata = merge_metadata(_BASE_META)
        # Configuration rather than a message, so it belongs on the metadata envelope
        # rather than in `input`, whatever shape that takes.
        if self._flag("capture_inputs") and (
            system_prompt := _spans.agent_system_prompt(event.agent)
        ):
            metadata["system_prompt"] = system_prompt
        # In strands_session, the sentinel root is not an invocation.
        if not boundary.tool_catalog_stamped:
            self._stamp_tool_catalog(event.agent, metadata, boundary.trace_id)
            boundary.tool_catalog_stamped = True
        self.spans.open_span(
            run_id=key,
            parent_run_id=None,
            name=name,
            span_type="workflow" if is_root else "agent",
            input=input_value,
            metadata=metadata,
            span_id=boundary.trace_id if is_root else None,
        )
        if (root := current_workflow_root()) is not None:
            root.note_input(input_value)

    @staticmethod
    def _mark_errored() -> None:
        """Remember that some step failed, so the root's plan can say so.

        Strands never computes a status for its root — close_span defaults to
        "success" — and child failures are not aggregated upward. Without this
        the plan would report "success" on every failed run, which is worse for
        a goal-adherence judge than reporting nothing.
        """
        if (boundary := _boundary.get()) is not None:
            boundary.note_failure()

    def _stamp_tool_catalog(
        self, agent: Any, metadata: dict[str, Any], trace_id: str | None
    ) -> None:
        """Stamp this root span with the agent's tool catalog hash."""
        try:
            from aigie.decision.tool_catalog import stamp_tool_registry_hash

            stamp_tool_registry_hash(_spans.agent_tools(agent), metadata, trace_id)
        except Exception:  # noqa: BLE001, S110 - never break the agent run
            return

    def _on_after_invocation(self, event: Any) -> None:
        if not self._flag("trace_agents"):
            return
        boundary = _boundary.get()
        if boundary is None:
            return
        key = f"inv:{id(event.agent)}"
        self._reassert_ambient()
        result = getattr(event, "result", None)
        output_value = (
            _spans.result_output(result, self._limit()) if self._flag("capture_outputs") else None
        )
        metadata_updates = _spans.usage_metadata(result)
        is_root = key == boundary.root_inv_key
        if is_root:
            metadata_updates = {
                **(metadata_updates or {}),
                **boundary.plan_metadata(_spans.agent_name(event.agent)),
            }
        self.spans.close_span(
            run_id=key,
            output=output_value,
            metadata_updates=metadata_updates,
            # Without this the root reports "success" carrying a plan that says
            # "error" — the span and its own summary disagreeing about the run.
            status="error" if is_root and boundary.errored else "success",
        )
        if (root := current_workflow_root()) is not None:
            root.note_output(output_value)
        if is_root:
            self._finalize_trace()

    # -- Model call ------------------------------------------------------------

    def _on_before_model(self, event: Any) -> None:
        boundary = _boundary.get()
        if boundary is None:
            return
        # Counted before the flag check: trace_model_calls governs whether a
        # child span is emitted, not whether the run did the work. A judge
        # reading turn_count 0 hears "no turns", not "not tracked".
        boundary.turn_count += 1
        if not self._flag("trace_model_calls"):
            return
        self._reassert_ambient()
        run_id = f"model:{boundary.trace_id}:{id(event)}"
        _model_stack.set((*_model_stack.get(), run_id))
        self.spans.open_span(
            run_id=run_id,
            parent_run_id=None,
            name="model",
            span_type="llm",
            input=None,
            metadata=merge_metadata(
                _BASE_META, _spans.model_metadata(getattr(event, "agent", None))
            ),
        )

    def _on_after_model(self, event: Any) -> None:
        exc = getattr(event, "exception", None)
        if exc is not None:
            self._mark_errored()  # a failure is a fact about the run, not about tracing
        if not self._flag("trace_model_calls"):
            return
        stack = _model_stack.get()
        if _boundary.get() is None or not stack:
            return
        run_id = stack[-1]
        _model_stack.set(stack[:-1])
        self._reassert_ambient()
        if exc is not None:
            self.spans.fail_span(run_id=run_id, error=exc)
            return
        stop = getattr(event, "stop_response", None)
        output = None
        if stop is not None and self._flag("capture_outputs"):
            output = _spans.truncate(getattr(stop, "message", None), self._limit())
        agent = getattr(event, "agent", None)
        extras, usage_md = llm_span_payload(
            _spans.usage_mapping(stop) if stop is not None else None,
            model_id=_spans.model_id(agent),
        )
        self.spans.close_span(
            run_id=run_id, output=output, extras=extras or None, metadata_updates=usage_md or None
        )

    # -- Tool call -------------------------------------------------------------

    def _on_before_tool(self, event: Any) -> None:
        if (boundary := _boundary.get()) is None:
            return
        boundary.tool_call_count += 1  # counted even when tool spans are off
        if not self._flag("trace_tools"):
            return
        self._reassert_ambient()
        tool_use = event.tool_use
        self.spans.open_span(
            run_id=tool_use["toolUseId"],
            parent_run_id=None,
            name=_spans.tool_span_name(tool_use),
            span_type="tool",
            input=_spans.truncate(tool_use.get("input"), self._limit())
            if self._flag("capture_inputs")
            else None,
            metadata=merge_metadata(_BASE_META),
        )

    def _on_after_tool(self, event: Any) -> None:
        exc = getattr(event, "exception", None)
        if exc is not None:
            self._mark_errored()
        if not self._flag("trace_tools") or _boundary.get() is None:
            return
        run_id = event.tool_use["toolUseId"]
        self._reassert_ambient()
        if exc is not None:
            self.spans.fail_span(run_id=run_id, error=exc)
            return
        output = (
            _spans.truncate(getattr(event, "result", None), self._limit())
            if self._flag("capture_outputs")
            else None
        )
        self.spans.close_span(run_id=run_id, output=output)

    # -- Multi-agent orchestrator (Swarm/Graph) --------------------------------

    def _on_before_multi_agent(self, event: Any) -> None:
        if not self._flag("trace_multi_agent"):
            return
        if not self._ensure_trace("Strands Multi-Agent"):
            return
        boundary = _boundary.get()
        assert boundary is not None
        key = f"ma:{id(event.source)}"
        is_root = boundary.root_inv_key is None
        if is_root:
            boundary.root_inv_key = key
        boundary.ma_errors_at_open[key] = boundary.error_count
        self.spans.open_span(
            run_id=key,
            parent_run_id=None,
            name="Strands Multi-Agent",
            span_type="workflow",
            input=None,
            metadata=merge_metadata(_BASE_META),
            span_id=boundary.trace_id if is_root else None,
        )

    def _on_after_multi_agent(self, event: Any) -> None:
        if not self._flag("trace_multi_agent"):
            return
        boundary = _boundary.get()
        if boundary is None:
            return
        key = f"ma:{id(event.source)}"
        self._reassert_ambient()
        self._sweep_open_nodes(event.source)
        # Swept nodes can mark the run errored, so build the plan after the sweep.
        is_root = key == boundary.root_inv_key
        self.spans.close_span(
            run_id=key,
            output=None,
            metadata_updates=(boundary.plan_metadata("Strands Multi-Agent") if is_root else None),
            # Without a status this closes "success" over failed children; the
            # scoping keeps a clean nested orchestrator out of it.
            status="error" if self._ma_failed(boundary, key, is_root) else "success",
        )
        boundary.ma_errors_at_open.pop(key, None)
        if is_root:
            self._finalize_trace()

    @staticmethod
    def _ma_failed(boundary: _Boundary, key: str, is_root: bool) -> bool:
        """The root owns the whole run; a nested one owns only what failed
        after it opened, so a sibling's failure is not charged to it."""
        if is_root:
            return boundary.errored
        opened_at = boundary.ma_errors_at_open.get(key)
        return opened_at is not None and boundary.error_count > opened_at

    # -- Multi-agent nodes -----------------------------------------------------

    def _on_before_node(self, event: Any) -> None:
        if not self._flag("trace_multi_agent"):
            return
        boundary = _boundary.get()
        if boundary is None:
            return
        node_id = event.node_id
        self._reassert_ambient()
        self.spans.open_span(
            run_id=f"node:{node_id}",
            parent_run_id=None,
            name=str(node_id),
            span_type="subgraph_workflow",
            input=None,
            metadata=merge_metadata(_NODE_META),
        )

    def _on_after_node(self, event: Any) -> None:
        if _boundary.get() is None:
            return
        self._reassert_ambient()
        # Called even with trace_multi_agent off: close_span/fail_span no-op for a
        # span that was never opened, but the run still has to learn a node failed.
        self._finish_node(event.source, event.node_id)

    def _finish_node(self, source: Any, node_id: str) -> None:
        """Close a node span with the status Strands recorded."""
        run_id = f"node:{node_id}"
        error = _spans.node_failure(source, node_id)
        if error is not None:
            self._mark_errored()
            self.spans.fail_span(run_id=run_id, error=error)
        else:
            self.spans.close_span(run_id=run_id, output=None)

    def _sweep_open_nodes(self, source: Any) -> None:
        """Close node spans that missed an after-node event."""
        for node_id in _spans.node_ids(source):
            if self.spans.is_open(f"node:{node_id}"):
                self._finish_node(source, node_id)

    # -- helpers ---------------------------------------------------------------

    def _reassert_ambient(self) -> None:
        boundary = _boundary.get()
        if boundary and current_trace_id() != boundary.trace_id:
            open_ambient(trace_id=boundary.trace_id)

    def _limit(self) -> int:
        return getattr(self._config, "max_content_length", 10000)

    def _flag(self, name: str) -> bool:
        return bool(getattr(self._config, name, True))

    def _zero_retention(self) -> bool:
        return bool(getattr(self._config, "zero_retention", False))


# -- Session grouping ---------------------------------------------------------


def _active_provider() -> StrandsHookProvider | None:
    """The installed hook provider (holds the shared emitter), if patching is on."""
    from aigie.integrations.strands.lifecycle import active_provider

    return active_provider()


@contextmanager
def strands_session(name: str = "Strands Session") -> Iterator[str | None]:
    """Group sequential top-level Strands calls (e.g. ``agent()`` +
    ``structured_output()``) into one trace, via the shared ``trace_session``.

    The sentinel boundary makes every invocation a child of the session's
    workflow root and suppresses per-invocation finalize (no invocation key
    matches ``_SESSION_SENTINEL``).
    """
    provider = _active_provider()
    spans = provider.spans if provider is not None else None
    with trace_session(spans, name=name, framework="strands") as trace_id:
        if trace_id is None or _boundary.get() is not None:
            yield trace_id
            return
        boundary = _Boundary(trace_id=trace_id, root_inv_key=_SESSION_SENTINEL)
        token = _boundary.set(boundary)
        failure: BaseException | None = None
        try:
            yield trace_id
        except BaseException as exc:
            # Nothing inside the session reports a failure that never reached a
            # model or tool hook, so without this the root closes "success" on a
            # run the caller saw raise.
            boundary.note_failure()
            failure = exc
            raise
        finally:
            _boundary.reset(token)
            # Closed here rather than by trace_session so the root carries the
            # run summary, which is only known now. WorkflowRoot.close() is
            # idempotent, so trace_session's own close becomes a no-op.
            if (root := current_workflow_root()) is not None:
                # A tool hook can set ``errored`` without anything propagating
                # out of the session, so the status is driven by the boundary
                # rather than by ``failure`` alone — otherwise the span says
                # "success" while the plan it carries says "error".
                root.close(
                    error=failure,
                    status="error" if boundary.errored else None,
                    metadata_updates=boundary.plan_metadata(name),
                )
