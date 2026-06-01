"""Lifecycle hook bodies (BeforeInvocation/AfterInvocation/MessageAdded)."""

from __future__ import annotations

import contextlib
import json
import logging
import uuid
from typing import TYPE_CHECKING, Any

from ...._legacy_stubs import DriftDetector, ErrorDetector  # legacy autonomous-mode shim
from ....buffer import EventType
from ....context_manager import merge_metadata
from ._shared import utc_now
from .usage import extract_model_id


# Minimal no-op stubs (autonomous error/drift detection removed)
class _NoOpPlan:
    model: str | None = None
    expected_tools: set = set()


class ErrorDetector:
    def __init__(self, *a: Any, **kw: Any) -> None:
        pass

    def __getattr__(self, _name: str):
        return lambda *a, **kw: None


class DriftDetector:
    def __init__(self, *a: Any, **kw: Any) -> None:
        self.plan = _NoOpPlan()

    def __getattr__(self, _name: str):
        return lambda *a, **kw: None


if TYPE_CHECKING:
    from ..handler import StrandsHandler

    with contextlib.suppress(ImportError):
        from strands.hooks import BeforeInvocationEvent, MessageAddedEvent


class _SimpleTraceContext:
    """Minimal trace context for ContextVar propagation before full trace creation."""

    def __init__(self, trace_id: str, trace_name: str):
        self.id = trace_id
        self.name = trace_name


logger = logging.getLogger(__name__)


def _find_existing_trace_id(event: BeforeInvocationEvent) -> tuple[str | None, Any, Any]:
    """Search the four propagation tiers for an existing trace_id.

    Returns ``(trace_id_or_None, trace_attrs, invocation_state)`` so the caller
    can update them when assigning a new id (tier-3 / tier-2 fallback).
    """
    from ....auto_instrument.trace import get_current_trace, get_thread_local_trace_id

    trace_attrs = getattr(event.agent, "trace_attributes", None)
    existing = trace_attrs.get("aigie_trace_id") if isinstance(trace_attrs, dict) else None
    invocation_state = getattr(event, "invocation_state", None)
    if not existing and isinstance(invocation_state, dict):
        existing = invocation_state.get("aigie_trace_id")
    if not existing:
        ambient = get_current_trace()
        existing = getattr(ambient, "id", None) if ambient else None
    if not existing:
        existing = get_thread_local_trace_id()
    return existing, trace_attrs, invocation_state


def _resolve_or_create_trace(handler: StrandsHandler, event: BeforeInvocationEvent) -> bool:
    """Set ``handler.trace_id`` (joining or creating) and return ``trace_already_exists``."""
    from ....auto_instrument.trace import set_current_trace, set_thread_local_trace_id

    existing_id, trace_attrs, invocation_state = _find_existing_trace_id(event)
    if existing_id:
        handler.trace_id = existing_id
        handler._is_trace_owner = False
        if isinstance(trace_attrs, dict) and "aigie_trace_id" not in trace_attrs:
            trace_attrs["aigie_trace_id"] = handler.trace_id
        return True
    handler.trace_id = str(uuid.uuid4())
    handler._is_trace_owner = True
    if isinstance(invocation_state, dict):
        invocation_state["aigie_trace_id"] = handler.trace_id
    if isinstance(trace_attrs, dict):
        trace_attrs["aigie_trace_id"] = handler.trace_id
    set_current_trace(_SimpleTraceContext(handler.trace_id, ""))
    set_thread_local_trace_id(handler.trace_id)
    return False


def _reset_counters(handler: StrandsHandler) -> None:
    handler._has_errors = False
    handler._error_messages = []
    handler._total_tool_calls = 0
    handler._total_input_tokens = 0
    handler._total_output_tokens = 0
    handler._total_cost = 0.0


def _reset_span_pointers_and_maps(handler: StrandsHandler) -> None:
    handler.agent_span_id = None
    handler.model_span_id = None
    handler.model_start_time = None
    handler._model_call_start_tokens = None
    handler._pending_llm_span = None
    handler._llm_call_count = 0
    handler.tool_map.clear()
    handler.model_call_map.clear()
    handler.multi_agent_map.clear()
    handler.node_map.clear()


def _reset_parent_chain(handler: StrandsHandler, trace_already_exists: bool) -> None:
    from ....auto_instrument.trace import get_thread_local_parent_span_id

    ambient_parent = get_thread_local_parent_span_id()
    handler._current_parent_span_id = (
        ambient_parent if (trace_already_exists and ambient_parent) else None
    )
    handler._parent_span_stack.clear()


def _reset_runtime_detectors(handler: StrandsHandler) -> None:
    if handler._remediation_engine:
        handler._remediation_engine.reset()
    handler._error_detector = ErrorDetector()
    handler._drift_detector = DriftDetector()
    handler._detected_errors = []


def _reset_invocation_state(handler: StrandsHandler, trace_already_exists: bool) -> None:
    """Clear per-invocation counters/maps; inherit ambient parent if joining a trace."""
    _reset_counters(handler)
    _reset_span_pointers_and_maps(handler)
    _reset_parent_chain(handler, trace_already_exists)
    _reset_runtime_detectors(handler)


async def _emit_trace_create(
    handler: StrandsHandler,
    aigie: Any,
    event: BeforeInvocationEvent,
    agent_name: str,
    trace_name: str,
) -> None:
    """Send TRACE_CREATE for a newly-owned trace, populate context, and flush."""
    from ....auto_instrument.trace import set_current_trace

    trace_data: dict[str, Any] = {
        "id": handler.trace_id,
        "name": trace_name,
        "metadata": merge_metadata(
            {
                "framework": "strands",
                "agent_id": getattr(event.agent, "agent_id", None),
                "agent_name": agent_name,
                **handler.metadata,
            }
        ),
        "tags": handler.tags,
        "start_time": utc_now().isoformat(),
    }
    if handler.user_id:
        trace_data["user_id"] = handler.user_id
    if handler.session_id:
        trace_data["session_id"] = handler.session_id
    if aigie._buffer:
        await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)
    try:
        set_current_trace(_SimpleTraceContext(handler.trace_id or "", trace_name))
    except Exception as e:
        logger.debug(f"[AIGIE] Could not set trace in context: {e}")
    await aigie._buffer.flush()


def _coerce_tools_iterable(agent_tools: Any) -> Any:
    """Best-effort flatten of Strands' various tool-registry shapes into an iterable."""
    tools_list: Any = agent_tools
    if hasattr(agent_tools, "values"):
        tools_list = agent_tools.values()
    elif hasattr(agent_tools, "get_tools"):
        tools_list = agent_tools.get_tools()
    try:
        iter(tools_list)
    except TypeError:
        if hasattr(tools_list, "to_dict"):
            return tools_list.to_dict().values()
        if hasattr(tools_list, "registry"):
            return tools_list.registry.values()
        return []
    return tools_list


def _build_tool_definition(tool: Any) -> dict[str, Any]:
    defn: dict[str, Any] = {}
    name = getattr(tool, "name", None) or getattr(tool, "tool_name", None)
    if name:
        defn["name"] = name
    desc = getattr(tool, "description", None)
    if desc:
        defn["description"] = desc
    schema = getattr(tool, "input_schema", None) or getattr(tool, "schema", None)
    if schema:
        defn["input_schema"] = schema
    return defn


def _collect_available_tools(event: BeforeInvocationEvent) -> list[dict[str, Any]]:
    """Walk agent.tools / tool_registry and return a list of tool definitions."""
    agent_tools = getattr(event.agent, "tools", None) or getattr(event.agent, "tool_registry", None)
    if not agent_tools:
        return []
    return [
        defn
        for defn in (_build_tool_definition(t) for t in _coerce_tools_iterable(agent_tools))
        if defn
    ]


def _capture_drift_baseline(handler: StrandsHandler, event: BeforeInvocationEvent) -> str | None:
    """Capture system prompt + model_id into the drift detector. Returns the prompt."""
    system_prompt = getattr(event.agent, "system_prompt", None)
    if system_prompt:
        handler._drift_detector.capture_system_prompt(str(system_prompt))
    if hasattr(event.agent, "model"):
        model_id = extract_model_id(event.agent.model)
        if model_id:
            handler._drift_detector.plan.model = model_id
    return str(system_prompt) if system_prompt else None


def _build_agent_span_data(
    handler: StrandsHandler,
    event: BeforeInvocationEvent,
    agent_name: str,
    agent_depth: int,
    available_tools: list[dict[str, Any]],
    system_prompt: str | None,
) -> dict[str, Any]:
    """Build the agent SPAN_CREATE payload (without input — added separately)."""
    metadata = merge_metadata(
        {
            "framework": "strands",
            "agent_id": getattr(event.agent, "agent_id", None),
            "agent_name": agent_name,
            "depth": agent_depth,
        }
    )
    if available_tools:
        metadata["available_tools"] = available_tools
    if system_prompt:
        metadata["system_prompt"] = system_prompt

    span: dict[str, Any] = {
        "id": handler.agent_span_id,
        "trace_id": handler.trace_id,
        "parent_id": handler._current_parent_span_id or None,
        "name": f"Agent: {agent_name}",
        "type": "agent",
        "start_time": handler._invocation_start_time.isoformat()
        if handler._invocation_start_time
        else utc_now().isoformat(),
        "metadata": metadata,
        "tags": handler.tags,
        "depth": agent_depth,
    }
    if handler.user_id:
        span["user_id"] = handler.user_id
    if handler.session_id:
        span["session_id"] = handler.session_id
    return span


def _serialize_input_messages(handler: StrandsHandler, input_messages: Any) -> str:
    """Serialize agent input messages to JSON, falling back to repr on errors."""
    try:
        if isinstance(input_messages, list):
            serializable = [
                msg if isinstance(msg, dict) else {"role": "user", "content": str(msg)}
                for msg in input_messages
            ]
            payload: Any = serializable
        else:
            payload = str(input_messages)
        out = json.dumps(payload, default=str)
    except Exception:
        out = str(input_messages)
    if len(out) > handler.config.max_content_length:
        out = out[: handler.config.max_content_length] + "..."
    return out


def _attach_input_to_agent_span(
    handler: StrandsHandler, event: BeforeInvocationEvent, agent_span_data: dict[str, Any]
) -> None:
    """Capture event/agent messages into agent span input (and cached agent_span_data)."""
    if not handler.config.capture_inputs:
        return
    input_messages: Any = None
    if event.messages:
        input_messages = event.messages
    elif hasattr(event, "agent") and hasattr(event.agent, "messages") and event.agent.messages:
        input_messages = event.agent.messages
    if not input_messages:
        return
    rendered = _serialize_input_messages(handler, input_messages)
    agent_span_data["input"] = rendered
    if handler._agent_span_data is not None:
        handler._agent_span_data["input"] = rendered


def _snapshot_messages_start_index(handler: StrandsHandler, event: BeforeInvocationEvent) -> None:
    try:
        existing_msgs = getattr(event.agent, "messages", None)
        handler._messages_start_index = len(existing_msgs) if isinstance(existing_msgs, list) else 0
    except Exception:
        handler._messages_start_index = 0


async def _emit_agent_span_create(
    handler: StrandsHandler, aigie: Any, event: BeforeInvocationEvent, agent_name: str
) -> None:
    """Allocate the agent span_id, build its payload, and emit SPAN_CREATE."""
    handler.agent_span_id = str(uuid.uuid4())
    handler._invocation_start_time = utc_now()
    _snapshot_messages_start_index(handler, event)
    agent_depth = handler._register_span_depth(handler.agent_span_id, None)
    system_prompt = _capture_drift_baseline(handler, event)
    available_tools = _collect_available_tools(event)
    handler._agent_span_data = {
        "agent_name": agent_name,
        "agent_id": getattr(event.agent, "agent_id", None),
        "depth": agent_depth,
    }
    agent_span_data = _build_agent_span_data(
        handler, event, agent_name, agent_depth, available_tools, system_prompt
    )
    _attach_input_to_agent_span(handler, event, agent_span_data)
    if aigie._buffer:
        await aigie._buffer.add(EventType.SPAN_CREATE, agent_span_data)
    handler._current_parent_span_id = handler.agent_span_id
    if handler._intervention_dispatcher and handler.trace_id:
        handler._intervention_dispatcher.subscribe_trace(handler.trace_id)


async def on_before_invocation(handler: StrandsHandler, event: BeforeInvocationEvent) -> None:
    """Handle BeforeInvocationEvent - create trace and agent span."""
    if not handler.config.enabled or not handler.config.trace_agents:
        return
    aigie = handler._get_aigie()
    if not aigie or not aigie._initialized:
        return
    try:
        trace_already_exists = _resolve_or_create_trace(handler, event)
        _reset_invocation_state(handler, trace_already_exists)
        agent_name = getattr(event.agent, "name", "Strands Agent")
        trace_name = handler.trace_name or agent_name
        if not trace_already_exists:
            await _emit_trace_create(handler, aigie, event, agent_name, trace_name)
        else:
            logger.debug(f"[AIGIE] Reusing existing trace: {handler.trace_id}")
        await _emit_agent_span_create(handler, aigie, event, agent_name)
        logger.debug(f"[AIGIE] Trace started: {trace_name} (id={handler.trace_id})")
    except Exception as e:
        logger.error(f"[AIGIE] Error in on_before_invocation: {e}", exc_info=True)


async def on_message_added(handler: StrandsHandler, event: MessageAddedEvent) -> None:
    """Placeholder for fine-grained per-message tracking (currently a no-op)."""
    return
