"""Strands HookProvider that emits Aigie spans (L3 binding, callback-driven)."""

from __future__ import annotations

from contextlib import suppress
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from aigie.auto_instrument.trace import get_or_create_trace_sync
from aigie.context_manager import merge_metadata
from aigie.integrations.strands import _spans
from aigie.tracing.span_event_handler import SpanEventHandler
from aigie.tracing.trace_state import (
    close_ambient,
    current_trace_id,
    is_inside_traced_run,
    open_ambient,
)


@dataclass
class _Boundary:
    trace_id: str
    root_inv_key: str | None = None
    ambient_token: Any = None


_boundary: ContextVar[_Boundary | None] = ContextVar("_aigie_strands_boundary", default=None)
_model_stack: ContextVar[tuple[str, ...]] = ContextVar("_aigie_strands_model_stack", default=())

_BASE_META = {"framework": "strands", "type": "strands"}
_NODE_META = {**_BASE_META, "kind": "node"}


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
        self.spans.open_span(
            run_id=key,
            parent_run_id=None,
            name=name,
            span_type="workflow" if is_root else "agent",
            input=_spans.messages_to_input(messages, self._limit())
            if self._flag("capture_inputs")
            else None,
            metadata=merge_metadata(_BASE_META),
            span_id=boundary.trace_id if is_root else None,
        )

    def _on_after_invocation(self, event: Any) -> None:
        if not self._flag("trace_agents"):
            return
        boundary = _boundary.get()
        if boundary is None:
            return
        key = f"inv:{id(event.agent)}"
        self._reassert_ambient()
        result = getattr(event, "result", None)
        self.spans.close_span(
            run_id=key,
            output=_spans.result_output(result, self._limit())
            if self._flag("capture_outputs")
            else None,
            metadata_updates=_spans.usage_metadata(result),
        )
        if key == boundary.root_inv_key:
            self._finalize_trace()

    # -- Model call ------------------------------------------------------------

    def _on_before_model(self, event: Any) -> None:
        if not self._flag("trace_model_calls"):
            return
        boundary = _boundary.get()
        if boundary is None:
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
        if not self._flag("trace_model_calls"):
            return
        stack = _model_stack.get()
        if _boundary.get() is None or not stack:
            return
        run_id = stack[-1]
        _model_stack.set(stack[:-1])
        self._reassert_ambient()
        exc = getattr(event, "exception", None)
        if exc is not None:
            self.spans.fail_span(run_id=run_id, error=exc)
            return
        stop = getattr(event, "stop_response", None)
        output = None
        if stop is not None and self._flag("capture_outputs"):
            output = _spans.truncate(getattr(stop, "message", None), self._limit())
        self.spans.close_span(run_id=run_id, output=output)

    # -- Tool call -------------------------------------------------------------

    def _on_before_tool(self, event: Any) -> None:
        if not self._flag("trace_tools") or _boundary.get() is None:
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
        if not self._flag("trace_tools") or _boundary.get() is None:
            return
        run_id = event.tool_use["toolUseId"]
        self._reassert_ambient()
        exc = getattr(event, "exception", None)
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
        self.spans.close_span(run_id=key, output=None)
        if key == boundary.root_inv_key:
            self._finalize_trace()

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
        if not self._flag("trace_multi_agent") or _boundary.get() is None:
            return
        node_id = event.node_id
        self._reassert_ambient()
        self.spans.close_span(run_id=f"node:{node_id}", output=None)

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
