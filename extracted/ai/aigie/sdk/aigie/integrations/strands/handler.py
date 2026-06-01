"""
Strands Agents hook handler for Aigie SDK.

Implements HookProvider to automatically trace Strands agent invocations,
tool calls, LLM calls, and multi-agent orchestrations.

Includes comprehensive error detection and drift monitoring.
"""

from __future__ import annotations

import contextlib
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from .error_detection import (
    DetectedError,
    ErrorDetector,
)
from .drift_detection import DriftDetector
from .config import StrandsConfig

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    with contextlib.suppress(ImportError):
        from strands.hooks import HookRegistry


class StrandsHandler:
    """
    Strands Agents handler for Aigie tracing.

    Implements HookProvider to automatically trace:
    - Agent invocations (BeforeInvocationEvent → AfterInvocationEvent)
    - Tool calls (BeforeToolCallEvent → AfterToolCallEvent)
    - LLM calls (BeforeModelCallEvent → AfterModelCallEvent)
    - Multi-agent orchestrations (BeforeMultiAgentInvocationEvent → AfterMultiAgentInvocationEvent)
    - Node executions (BeforeNodeCallEvent → AfterNodeCallEvent)

    Example:
        >>> from strands import Agent
        >>> from aigie.integrations.strands import StrandsHandler
        >>>
        >>> handler = StrandsHandler()
        >>> agent = Agent(tools=[...], hooks=[handler])
        >>> result = agent("What is the capital of France?")
    """

    def __init__(
        self,
        config: StrandsConfig | None = None,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        """Initialize Strands handler. See class docstring for trace semantics."""
        self._init_identity(config, trace_name, metadata, tags, user_id, session_id)
        self._init_span_state()
        self._init_runtime_components()

    def _init_identity(
        self,
        config: StrandsConfig | None,
        trace_name: str | None,
        metadata: dict[str, Any] | None,
        tags: list[str] | None,
        user_id: str | None,
        session_id: str | None,
    ) -> None:
        self.config = config or StrandsConfig.from_env()
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id

    def _init_span_state(self) -> None:
        self._init_trace_and_span_ids()
        self._init_span_maps()
        self._init_parent_chain()
        self._init_streaming_state()
        self._init_counters()
        self._init_invocation_state()

    def _init_trace_and_span_ids(self) -> None:
        self.trace_id: str | None = None
        self._is_trace_owner: bool = False
        self.agent_span_id: str | None = None
        self.model_span_id: str | None = None
        self.model_start_time: datetime | None = None

    def _init_span_maps(self) -> None:
        self.tool_map: dict[str, dict[str, Any]] = {}
        self.model_call_map: dict[str, dict[str, Any]] = {}
        # orchestrator_id (int) -> span data; node_id type varies across strands versions.
        self.multi_agent_map: dict[int, dict[str, Any]] = {}
        self.node_map: dict[Any, dict[str, Any]] = {}
        self._span_depth_map: dict[str, int] = {}

    def _init_parent_chain(self) -> None:
        self._current_parent_span_id: str | None = None
        self._parent_span_stack: list[str] = []
        self._aigie = None

    def _init_streaming_state(self) -> None:
        self._bidi_span_id: str | None = None
        self._bidi_start_time: datetime | None = None

    def _init_counters(self) -> None:
        self._total_tool_calls = 0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_cost = 0.0
        self._model_call_start_tokens: dict[str, int] | None = None
        self._pending_llm_span: dict[str, Any] | None = None
        self._llm_call_count: int = 0

    def _init_invocation_state(self) -> None:
        self._has_errors = False
        self._error_messages: list[str] = []
        self._detected_errors: list[DetectedError] = []
        self._invocation_start_time: datetime | None = None
        self._messages_start_index: int = 0
        self._agent_span_data: dict[str, Any] | None = None
        self._subagent_types: dict[str, str] = {}

    def register_subagent_tool(self, tool_name: str, subagent_type: str | None = None) -> None:
        """Mark a tool as a subagent dispatch so failures route to subagent-aware detection.

        Why: Strands surfaces nested agent invocations through the regular tool path,
        so without an explicit hint we cannot tell a subagent failure from any other
        tool failure. Callers who wrap an Agent as a tool can register the tool's name
        here to opt in to ``detect_from_subagent_result`` (richer source tagging,
        severity elevation, transient classification). ``subagent_type`` defaults to
        the tool name; pass it only when you want a distinct display label.
        """
        self._subagent_types[tool_name] = subagent_type or tool_name

    def record_detection(self, detected: DetectedError | None) -> None:
        """Append a typed detection to the per-invocation list, no-op on None.

        All hook modules go through this so the list mutation stays encapsulated
        and detection-recording stays a single line at each call site.
        """
        if detected is not None:
            self._detected_errors.append(detected)

    def _init_runtime_components(self) -> None:
        self._error_detector = ErrorDetector()
        self._drift_detector = DriftDetector()
        self._remediation_engine = None
        self._intervention_dispatcher = None
        if not self.config.enable_realtime_remediation:
            return
        aigie = self._get_aigie()
        if not (aigie and aigie._initialized):
            return
        api_url = getattr(aigie, "_api_url", None) or getattr(aigie, "api_url", None)
        api_key = getattr(aigie, "_api_key", None) or getattr(aigie, "api_key", None)
        if api_url:
            from ...realtime.remediation_engine import RemediationEngine

            self._remediation_engine = RemediationEngine(
                api_url=api_url,
                api_key=api_key or "",
                query_timeout=self.config.remediation_query_timeout,
            )
        self._intervention_dispatcher = getattr(aigie, "_intervention_dispatcher", None)

    def _get_depth_for_parent(self, parent_id: str | None) -> int:
        """Calculate depth based on parent span's depth."""
        if not parent_id:
            return 0  # Root level
        parent_depth = self._span_depth_map.get(parent_id, 0)
        return parent_depth + 1

    def _register_span_depth(self, span_id: str, parent_id: str | None) -> int:
        """Register a span's depth and return it."""
        depth = self._get_depth_for_parent(parent_id)
        self._span_depth_map[span_id] = depth
        return depth

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    def register_hooks(self, registry: HookRegistry) -> None:
        """Register hook callbacks with the Strands hook registry.

        Each callback is bound to the relevant free function in ``hooks.*`` via
        ``functools.partial`` so the handler instance carries shared state but
        the hook bodies live in their own modules.
        """
        if not self.config.enabled:
            return

        try:
            from strands import hooks as sh
        except ImportError:
            logger.warning("[AIGIE] Strands hooks not available - cannot register callbacks")
            return

        from functools import partial

        from .hooks import lifecycle, lifecycle_after, llm, multi_agent, streaming, tools

        groups = [
            (
                self.config.trace_agents,
                [
                    (sh.BeforeInvocationEvent, partial(lifecycle.on_before_invocation, self)),
                    (sh.AfterInvocationEvent, partial(lifecycle_after.on_after_invocation, self)),
                    (sh.MessageAddedEvent, partial(lifecycle.on_message_added, self)),
                ],
            ),
            (
                self.config.trace_tools,
                [
                    (sh.BeforeToolCallEvent, partial(tools.on_before_tool_call, self)),
                    (sh.AfterToolCallEvent, partial(tools.on_after_tool_call, self)),
                ],
            ),
            (
                self.config.trace_llm_calls,
                [
                    (sh.BeforeModelCallEvent, partial(llm.on_before_model_call, self)),
                    (sh.AfterModelCallEvent, partial(llm.on_after_model_call, self)),
                ],
            ),
            (
                self.config.trace_multi_agent,
                [
                    (
                        sh.BeforeMultiAgentInvocationEvent,
                        partial(multi_agent.on_before_multi_agent, self),
                    ),
                    (
                        sh.AfterMultiAgentInvocationEvent,
                        partial(multi_agent.on_after_multi_agent, self),
                    ),
                    (sh.BeforeNodeCallEvent, partial(multi_agent.on_before_node_call, self)),
                    (sh.AfterNodeCallEvent, partial(multi_agent.on_after_node_call, self)),
                ],
            ),
        ]
        for enabled, callbacks in groups:
            if enabled:
                for event_type, cb in callbacks:
                    registry.add_callback(event_type, cb)

        if self.config.trace_streaming:
            streaming.register_streaming_hooks(self, registry)
