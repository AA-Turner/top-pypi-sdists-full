"""
Google ADK handler for Aigie SDK.

Provides manual tracing support for Google ADK agents, capturing
agent invocations, LLM calls, tool executions, and events.
"""

import contextlib
import logging
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Optional

from .error_detection import (
    DetectedError,
    ErrorDetector,
)
from .drift_detection import DriftDetector
from ...auto_instrument.trace import set_callback_context
from ...buffer import EventType
from ...context_manager import merge_metadata
from .config import GoogleADKConfig
from .cost_tracking import calculate_google_adk_cost, get_model_pricing

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    """Get current time in UTC with timezone info."""
    return datetime.now(timezone.utc)


def _utc_isoformat() -> str:
    """Get current UTC time as ISO format string."""
    return datetime.now(timezone.utc).isoformat()


if TYPE_CHECKING:
    from .session import GoogleADKSessionContext


def _extract_text_from_contents(contents) -> str:
    """Extract readable text from ADK Content/Part objects."""
    if isinstance(contents, str):
        return contents
    if isinstance(contents, list):
        texts = []
        for item in contents:
            parts = getattr(item, "parts", None)
            if parts:
                for part in parts:
                    text = getattr(part, "text", None)
                    if text:
                        texts.append(text)
            elif isinstance(item, str):
                texts.append(item)
        return "\n".join(texts) if texts else str(contents)
    # Single Content object
    parts = getattr(contents, "parts", None)
    if parts:
        texts = [getattr(p, "text", "") for p in parts if getattr(p, "text", None)]
        return "\n".join(texts) if texts else str(contents)
    return str(contents)


def _extract_prompts_from_contents(contents) -> list:
    """Extract structured prompts from ADK Content/Part objects for LLM span input."""
    if not contents:
        return []
    prompts = []
    items = contents if isinstance(contents, list) else [contents]
    for item in items:
        role = getattr(item, "role", "user") or "user"
        parts = getattr(item, "parts", None)
        if parts:
            texts = []
            for part in parts:
                text = getattr(part, "text", None)
                if text:
                    texts.append(text)
                # Capture function calls as tool use
                fc = getattr(part, "function_call", None)
                if fc:
                    fn_name = getattr(fc, "name", "unknown")
                    fn_args = getattr(fc, "args", {})
                    texts.append(f"[function_call: {fn_name}({fn_args})]")
                # Capture function responses
                fr = getattr(part, "function_response", None)
                if fr:
                    fn_name = getattr(fr, "name", "unknown")
                    fn_response = getattr(fr, "response", {})
                    texts.append(f"[function_response: {fn_name} -> {fn_response}]")
            if texts:
                prompts.append({"role": role, "content": "\n".join(texts)})
        elif isinstance(item, str):
            prompts.append({"role": "user", "content": item})
    return prompts


class GoogleADKHandler:
    """
    Google ADK handler for Aigie tracing.

    Provides manual tracing methods for Google ADK agent workflows:
    - Runner invocations (run lifecycle)
    - Agent executions
    - LLM/model calls with token tracking
    - Tool executions

    Example:
        >>> from google.adk import Runner, LlmAgent
        >>> from aigie.integrations.google_adk import GoogleADKHandler
        >>>
        >>> handler = GoogleADKHandler(trace_name="my-agent")
        >>>
        >>> # Manual usage in custom callbacks
        >>> await handler.handle_run_start(invocation_context)
        >>> await handler.handle_agent_start(agent, callback_context)
        >>> await handler.handle_llm_start(callback_context, llm_request)
        >>> # ... agent executes
        >>> await handler.handle_llm_end(callback_context, llm_response)
        >>> await handler.handle_agent_end(agent, callback_context)
        >>> await handler.handle_run_end(invocation_context)
    """

    def __init__(
        self,
        config: GoogleADKConfig | None = None,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        session_context: Optional["GoogleADKSessionContext"] = None,
    ):
        """
        Initialize Google ADK handler.

        Args:
            config: Configuration for tracing behavior
            trace_name: Name for the trace (default: agent name)
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
            session_context: Optional session context for trace sharing
        """
        self.config = config or GoogleADKConfig.from_env()
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id

        # Session context for trace sharing
        self._session_context = session_context

        # State tracking
        self.trace_id: str | None = session_context.trace_id if session_context else None
        self.run_span_id: str | None = None
        self.agent_span_id: str | None = None
        self.llm_span_id: str | None = None
        self.tool_map: dict[str, dict[str, Any]] = {}  # function_call_id -> {spanId, startTime}
        self.agent_map: dict[str, dict[str, Any]] = {}  # agent_name -> {spanId, startTime}

        # Current context for parent relationships
        self._current_parent_span_id: str | None = None
        self._parent_span_stack: list[str] = []
        self._aigie = None

        # Depth tracking for flow view
        self._span_depth_map: dict[str, int] = {}

        # Statistics
        self._total_model_calls = 0
        self._total_tool_calls = 0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_cost = 0.0

        # Error tracking
        self._has_errors = False
        self._error_messages: list[str] = []

        # Error detection and monitoring
        self._error_detector = ErrorDetector()
        self._detected_errors: list[DetectedError] = []
        self._run_start_time: datetime | None = None

        # Drift detection - plan vs execution tracking
        self._drift_detector = DriftDetector()
        self._turn_count = 0

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    def _get_depth_for_parent(self, parent_id: str | None) -> int:
        """Calculate depth based on parent span's depth."""
        if not parent_id:
            return 0
        parent_depth = self._span_depth_map.get(parent_id, 0)
        return parent_depth + 1

    def _register_span_depth(self, span_id: str, parent_id: str | None) -> int:
        """Register a span's depth and return it."""
        depth = self._get_depth_for_parent(parent_id)
        self._span_depth_map[span_id] = depth
        return depth

    def _get_current_parent(self) -> str | None:
        """Get current parent span ID for nesting."""
        if self._session_context:
            ctx_parent = self._session_context.get_current_parent()
            if ctx_parent:
                return ctx_parent
        return self._current_parent_span_id or self.agent_span_id or self.run_span_id

    def _set_current_parent(self, span_id: str | None) -> None:
        """Set current parent span ID."""
        self._current_parent_span_id = span_id
        if self._session_context:
            self._session_context.set_current_parent(span_id)

    # ========================================================================
    # Run Lifecycle Methods
    # ========================================================================

    async def handle_run_start(
        self,
        invocation_context: Any,
        user_message: str | None = None,
    ) -> str:
        """
        Called when a Runner.run_async() starts.

        Args:
            invocation_context: The InvocationContext from ADK
            user_message: Optional user message content

        Returns:
            The trace ID
        """
        if not self.config.enabled:
            return ""

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return ""

        try:
            # Mark callback context so auto-instrumentation (e.g. _patch_gemini)
            # skips LLM calls that are already traced by this handler
            set_callback_context(True)

            # Record start time
            self._run_start_time = _utc_now()

            # Reset state
            self._has_errors = False
            self._error_messages = []
            self._total_model_calls = 0
            self._total_tool_calls = 0
            self._total_input_tokens = 0
            self._total_output_tokens = 0
            self._total_cost = 0.0
            self.tool_map.clear()
            self.agent_map.clear()
            self._detected_errors = []
            self._error_detector = ErrorDetector()
            self._drift_detector = DriftDetector()
            self._turn_count = 0

            # Get or create trace ID
            if not self.trace_id:
                if self._session_context:
                    self.trace_id = self._session_context.trace_id
                else:
                    self.trace_id = str(uuid.uuid4())

            # Extract info from invocation context
            invocation_id = getattr(invocation_context, "invocation_id", str(uuid.uuid4()))
            session = getattr(invocation_context, "session", None)
            agent = getattr(invocation_context, "agent", None)

            agent_name = getattr(agent, "name", "ADK Agent") if agent else "ADK Agent"
            trace_name = self.trace_name or agent_name

            # Capture agent instruction for drift detection
            if agent:
                instruction = getattr(agent, "instruction", None)
                if instruction:
                    self._drift_detector.capture_system_prompt(str(instruction))
                # Capture expected tools from agent's tool list
                tools = getattr(agent, "tools", None)
                if tools:
                    for tool in tools:
                        tool_name = getattr(tool, "name", None) or getattr(tool, "__name__", None)
                        if tool_name:
                            self._drift_detector.plan.expected_tools.add(tool_name)

            if user_message:
                self._drift_detector.capture_initial_prompt(user_message)

            session_user_id = getattr(session, "user_id", None) if session else None
            session_id = getattr(session, "id", None) if session else None

            # Capture available tools from agent config
            available_tools = []
            if agent:
                agent_tools = getattr(agent, "tools", None)
                if agent_tools:
                    for tool in agent_tools:
                        tool_def = {}
                        tool_name = getattr(tool, "name", None) or getattr(tool, "__name__", None)
                        if tool_name:
                            tool_def["name"] = tool_name
                        tool_desc = getattr(tool, "description", None)
                        if tool_desc:
                            tool_def["description"] = tool_desc
                        tool_schema = getattr(tool, "input_schema", None) or getattr(
                            tool, "schema", None
                        )
                        if tool_schema:
                            tool_def["input_schema"] = tool_schema
                        if tool_def:
                            available_tools.append(tool_def)

                # Capture full system prompt in metadata
                instruction = getattr(agent, "instruction", None)

            # Build metadata
            trace_metadata = merge_metadata(
                {
                    **self.metadata,
                    "framework": "google_adk",
                    "invocation_id": invocation_id,
                    "agent_name": agent_name,
                }
            )

            if available_tools:
                trace_metadata["available_tools"] = available_tools
            if agent and instruction:
                trace_metadata["system_prompt"] = str(instruction)

            # Only create trace if not already created
            should_create_trace = True
            if self._session_context and self._session_context.trace_created:
                should_create_trace = False

            if should_create_trace:
                trace_data = {
                    "id": self.trace_id,
                    "name": trace_name,
                    "type": "agent",
                    "status": "pending",
                    "tags": [*self.tags, "google_adk"],
                    "metadata": merge_metadata(trace_metadata),
                    "start_time": self._run_start_time.isoformat(),
                    "created_at": self._run_start_time.isoformat(),
                }

                if self.user_id or session_user_id:
                    trace_data["user_id"] = self.user_id or session_user_id
                if self.session_id or session_id:
                    trace_data["session_id"] = self.session_id or session_id

                if user_message and self.config.capture_inputs:
                    trace_data["input"] = {
                        "message": user_message[: self.config.max_content_length],
                    }

                await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)

                # Set process-level trace ID for OTel bridge
                try:
                    from ...auto_instrument.span_enricher import set_active_trace_id

                    set_active_trace_id(self.trace_id)
                except Exception:
                    pass

                if self._session_context:
                    self._session_context.mark_trace_created()

                # Flush to ensure trace is created before spans
                await aigie._buffer.flush()

            # Create run span
            self.run_span_id = str(uuid.uuid4())
            run_depth = self._register_span_depth(self.run_span_id, None)

            run_span_data = {
                "id": self.run_span_id,
                "trace_id": self.trace_id,
                "parent_id": None,
                "name": f"Run: {agent_name}",
                "type": "agent",
                "start_time": self._run_start_time.isoformat(),
                "metadata": merge_metadata(
                    {
                        "invocation_id": invocation_id,
                        "agent_name": agent_name,
                        "depth": run_depth,
                    }
                ),
                "tags": self.tags,
                "status": "running",
                "depth": run_depth,
            }

            if user_message and self.config.capture_inputs:
                run_span_data["input"] = {
                    "message": user_message[: self.config.max_content_length],
                }

            await aigie._buffer.add(EventType.SPAN_CREATE, run_span_data)
            self._set_current_parent(self.run_span_id)

            logger.debug(f"[AIGIE] Run started: {trace_name} (trace_id={self.trace_id})")
            return self.trace_id

        except Exception as e:
            logger.warning(f"[AIGIE] Error in handle_run_start: {e}")
            return ""

    async def handle_run_end(
        self,
        invocation_context: Any,
        error: Exception | None = None,
    ) -> None:
        """
        Called when a Runner.run_async() completes.

        Args:
            invocation_context: The InvocationContext from ADK
            error: Optional exception if the run failed
        """
        if not self.config.enabled or not self.run_span_id:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            end_time = _utc_now()
            has_error = error is not None or self._has_errors
            status = "error" if has_error else "success"

            # Calculate duration
            duration_ms = 0.0
            if self._run_start_time:
                duration_ms = (end_time - self._run_start_time).total_seconds() * 1000

            # Build error message
            error_message = None
            if error:
                error_message = str(error)[:500]
                # Detect error type
                detected_error = self._error_detector.detect_from_exception(
                    error,
                    "run",
                    {"invocation_id": getattr(invocation_context, "invocation_id", None)},
                )
                if detected_error:
                    self._detected_errors.append(detected_error)
            elif self._error_messages:
                error_message = "; ".join(self._error_messages[:3])

            # Build error details from detected errors
            error_details = []
            if self._detected_errors:
                for de in self._detected_errors:
                    error_details.append(de.to_dict())

            # Finalize drift detection
            total_tokens = self._total_input_tokens + self._total_output_tokens
            detected_drifts = self._drift_detector.finalize(
                total_duration_ms=duration_ms,
                total_tokens=total_tokens,
                total_cost=self._total_cost,
            )
            drift_summary = self._drift_detector.get_summary()
            plan_metadata = drift_summary.get("plan", {})

            # Build execution plan summary
            agent = getattr(invocation_context, "agent", None)
            agent_name = getattr(agent, "name", "ADK Agent") if agent else "ADK Agent"
            execution_plan = {
                "agent": agent_name,
                "model_calls": self._total_model_calls,
                "tool_calls": self._total_tool_calls,
                "turn_count": self._turn_count,
                "total_tokens": total_tokens,
                "total_cost": self._total_cost,
                "duration_ms": duration_ms,
                "status": status,
                "error_count": len(self._detected_errors),
                "drift_count": len(detected_drifts),
            }

            # Add plan data if extracted
            if plan_metadata.get("planned_steps"):
                execution_plan["planned_steps"] = plan_metadata["planned_steps"]
            if plan_metadata.get("expected_tools"):
                execution_plan["expected_tools"] = plan_metadata["expected_tools"]

            # Build run span metadata
            run_metadata = merge_metadata(
                {
                    "total_model_calls": self._total_model_calls,
                    "total_tool_calls": self._total_tool_calls,
                    "total_input_tokens": self._total_input_tokens,
                    "total_output_tokens": self._total_output_tokens,
                    "total_tokens": self._total_input_tokens + self._total_output_tokens,
                    "total_cost": self._total_cost,
                    "duration_ms": duration_ms,
                    "status": status,
                    "execution_plan": execution_plan,
                }
            )

            if error_details:
                run_metadata["detected_errors"] = error_details
                run_metadata["error_summary"] = {
                    "total": len(error_details),
                    "by_type": {},
                    "by_severity": {},
                }
                for de in self._detected_errors:
                    et = de.error_type.value
                    es = de.severity.value
                    run_metadata["error_summary"]["by_type"][et] = (
                        run_metadata["error_summary"]["by_type"].get(et, 0) + 1
                    )
                    run_metadata["error_summary"]["by_severity"][es] = (
                        run_metadata["error_summary"]["by_severity"].get(es, 0) + 1
                    )

            # Add drift detection data
            if detected_drifts:
                run_metadata["drift_detection"] = {
                    "drift_count": len(detected_drifts),
                    "drifts": [d.to_dict() for d in detected_drifts[:10]],
                    "has_warnings": any(
                        d.severity.value in ["warning", "alert"] for d in detected_drifts
                    ),
                }
            if plan_metadata:
                run_metadata["agent_plan"] = plan_metadata

            # Update run span
            run_update = {
                "id": self.run_span_id,
                "trace_id": self.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration_ms * 1_000_000),
                "status": status,
                "is_error": has_error,
                "metadata": merge_metadata(run_metadata),
                "prompt_tokens": self._total_input_tokens,
                "completion_tokens": self._total_output_tokens,
                "total_tokens": self._total_input_tokens + self._total_output_tokens,
                "total_cost": self._total_cost,
            }

            # Add output summary to run span
            run_update["output"] = {
                "status": status,
                "execution_plan": execution_plan,
                "token_usage": {
                    "input_tokens": self._total_input_tokens,
                    "output_tokens": self._total_output_tokens,
                    "total_tokens": self._total_input_tokens + self._total_output_tokens,
                },
                "cost": self._total_cost,
            }
            if error_details:
                run_update["output"]["errors"] = error_details[:10]
            if detected_drifts:
                run_update["output"]["drifts"] = [d.to_dict() for d in detected_drifts[:10]]
            if plan_metadata.get("planned_steps"):
                run_update["output"]["agent_plan"] = plan_metadata

            if error_message:
                run_update["error"] = error_message
                run_update["error_message"] = error_message

            await aigie._buffer.add(EventType.SPAN_UPDATE, run_update)

            # Build trace metadata
            trace_metadata = merge_metadata(
                {
                    "total_model_calls": self._total_model_calls,
                    "total_tool_calls": self._total_tool_calls,
                    "error_count": len(self._detected_errors),
                    "execution_plan": execution_plan,
                }
            )
            if error_details:
                trace_metadata["detected_errors"] = error_details[:10]
                trace_metadata["error_summary"] = run_metadata.get("error_summary")
            if detected_drifts:
                trace_metadata["drift_detection"] = run_metadata.get("drift_detection")
            if plan_metadata:
                trace_metadata["agent_plan"] = plan_metadata
            trace_metadata["turn_count"] = self._turn_count

            # Update trace (include name to restore it if backend auto-create overwrote it)
            trace_name = self.trace_name or agent_name
            trace_update = {
                "id": self.trace_id,
                "name": trace_name,
                "status": status,
                "end_time": end_time.isoformat(),
                "total_tokens": self._total_input_tokens + self._total_output_tokens,
                "prompt_tokens": self._total_input_tokens,
                "completion_tokens": self._total_output_tokens,
                "total_cost": self._total_cost,
                "metadata": merge_metadata(trace_metadata),
            }

            if error_message:
                trace_update["error"] = error_message
                trace_update["error_message"] = error_message

            await aigie._buffer.add(EventType.TRACE_UPDATE, trace_update)

            # Complete any pending spans
            await self._complete_pending_spans(end_time)

            # Flush everything, then re-send TRACE_CREATE to restore name.
            # Backend's _process_span_event_list auto-creates traces with "Auto-created..."
            # A final TRACE_CREATE after all spans ensures the correct name wins.
            await aigie._buffer.flush()
            await aigie._buffer.add(
                EventType.TRACE_CREATE, {"id": self.trace_id, "name": trace_name}
            )
            await aigie._buffer.flush()

            # Clear callback context so auto-instrumentation resumes for non-ADK calls
            set_callback_context(False)

            logger.debug(f"[AIGIE] Run completed: {self.trace_id} (status={status})")

        except Exception as e:
            # Ensure callback context is cleared even on error
            set_callback_context(False)
            logger.warning(f"[AIGIE] Error in handle_run_end: {e}")

    # ========================================================================
    # Agent Lifecycle Methods
    # ========================================================================

    async def handle_agent_start(
        self,
        agent: Any,
        callback_context: Any,
    ) -> str:
        """
        Called when an agent starts execution.

        Args:
            agent: The agent instance
            callback_context: The CallbackContext from ADK

        Returns:
            The agent span ID
        """
        if not self.config.enabled or not self.config.trace_agents:
            return ""

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        try:
            agent_name = getattr(agent, "name", "Agent")
            span_id = str(uuid.uuid4())
            start_time = _utc_now()

            parent_id = self._get_current_parent()
            agent_depth = self._register_span_depth(span_id, parent_id)

            # Store in agent map
            self.agent_map[agent_name] = {
                "spanId": span_id,
                "startTime": start_time,
                "agentName": agent_name,
                "depth": agent_depth,
            }

            span_data = {
                "id": span_id,
                "trace_id": self.trace_id,
                "parent_id": parent_id,
                "name": f"Agent: {agent_name}",
                "type": "agent",
                "start_time": start_time.isoformat(),
                "metadata": merge_metadata(
                    {
                        "agent_name": agent_name,
                        "depth": agent_depth,
                    }
                ),
                "tags": self.tags,
                "status": "running",
                "depth": agent_depth,
            }

            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

            self.agent_span_id = span_id
            self._set_current_parent(span_id)

            # Push to parent stack for nested agents
            self._parent_span_stack.append(parent_id or "")

            logger.debug(f"[AIGIE] Agent started: {agent_name} (span_id={span_id})")
            return span_id

        except Exception as e:
            logger.warning(f"[AIGIE] Error in handle_agent_start: {e}")
            return ""

    async def handle_agent_end(
        self,
        agent: Any,
        callback_context: Any,
        error: Exception | None = None,
    ) -> None:
        """
        Called when an agent completes execution.

        Args:
            agent: The agent instance
            callback_context: The CallbackContext from ADK
            error: Optional exception if the agent failed
        """
        if not self.config.enabled or not self.config.trace_agents:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            agent_name = getattr(agent, "name", "Agent")
            agent_data = self.agent_map.get(agent_name)

            if not agent_data:
                return

            end_time = _utc_now()
            duration = (end_time - agent_data["startTime"]).total_seconds()
            duration_ms = duration * 1000

            has_error = error is not None
            status = "error" if has_error else "success"

            update_data = {
                "id": agent_data["spanId"],
                "trace_id": self.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
                "status": status,
                "is_error": has_error,
                "metadata": merge_metadata(
                    {
                        "agent_name": agent_name,
                        "duration_ms": duration_ms,
                        "status": status,
                    }
                ),
            }

            if error:
                error_str = str(error)[:500]
                update_data["error"] = error_str
                update_data["error_message"] = error_str
                self._has_errors = True
                if error_str not in self._error_messages:
                    self._error_messages.append(error_str)

            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

            # Record agent execution for drift detection
            self._drift_detector.record_agent_execution(
                agent_name=agent_name,
                tool_count=self._total_tool_calls,
                is_retry=False,
            )

            # Restore parent from stack
            if self._parent_span_stack:
                prev_parent = self._parent_span_stack.pop()
                self._set_current_parent(prev_parent if prev_parent else self.run_span_id)
            else:
                self._set_current_parent(self.run_span_id)

            self.agent_span_id = None
            del self.agent_map[agent_name]

            logger.debug(f"[AIGIE] Agent completed: {agent_name} (status={status})")

        except Exception as e:
            logger.warning(f"[AIGIE] Error in handle_agent_end: {e}")

    # ========================================================================
    # LLM/Model Lifecycle Methods
    # ========================================================================

    async def handle_llm_start(
        self,
        callback_context: Any,
        llm_request: Any,
    ) -> str:
        """
        Called before an LLM call.

        Args:
            callback_context: The CallbackContext from ADK
            llm_request: The LlmRequest object

        Returns:
            The LLM span ID
        """
        if not self.config.enabled or not self.config.trace_llm_calls:
            return ""

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        try:
            span_id = str(uuid.uuid4())
            start_time = _utc_now()

            # Extract model info
            model = getattr(llm_request, "model", None)
            if not model:
                config = getattr(llm_request, "config", None)
                if config:
                    model = getattr(config, "model", None)
            model = model or "gemini"

            parent_id = self._get_current_parent()
            llm_depth = self._register_span_depth(span_id, parent_id)

            # Extract model parameters from config
            model_parameters = {}
            config = getattr(llm_request, "config", None)
            if config:
                for param in (
                    "temperature",
                    "top_p",
                    "top_k",
                    "max_output_tokens",
                    "stop_sequences",
                ):
                    val = getattr(config, param, None)
                    if val is not None:
                        model_parameters[param] = val

            span_metadata = merge_metadata(
                {
                    "model": model,
                    "model_id": model,
                    "model_name": model,
                    "agent_type": "llm",
                    "depth": llm_depth,
                }
            )
            if model_parameters:
                span_metadata["model_parameters"] = model_parameters
                span_metadata["llm_parameters"] = model_parameters

            span_data = {
                "id": span_id,
                "trace_id": self.trace_id,
                "parent_id": parent_id,
                "name": f"LLM: {model}",
                "type": "llm",
                "start_time": start_time.isoformat(),
                "metadata": merge_metadata(span_metadata),
                "tags": self.tags,
                "status": "running",
                "depth": llm_depth,
                "model": model,
            }

            if model_parameters:
                span_data["model_parameters"] = model_parameters

            # Capture input as structured JSON (matching LangGraph format)
            if self.config.capture_inputs:
                contents = getattr(llm_request, "contents", None) or getattr(
                    llm_request, "messages", None
                )
                prompts = _extract_prompts_from_contents(contents) if contents else []
                input_data = {
                    "model": model,
                    "model_id": model,
                    "prompts": prompts,
                    "prompt_count": len(prompts),
                }
                if model_parameters:
                    input_data["parameters"] = model_parameters
                span_data["input"] = input_data

            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

            self.llm_span_id = span_id
            self._llm_start_time = start_time
            self._llm_model = model
            self._llm_model_parameters = model_parameters
            self._total_model_calls += 1

            logger.debug(f"[AIGIE] LLM call started: {model} (span_id={span_id})")
            return span_id

        except Exception as e:
            logger.warning(f"[AIGIE] Error in handle_llm_start: {e}")
            return ""

    async def handle_llm_end(
        self,
        callback_context: Any,
        llm_response: Any,
        error: Exception | None = None,
    ) -> None:
        """
        Called after an LLM call completes.

        Args:
            callback_context: The CallbackContext from ADK
            llm_response: The LlmResponse object
            error: Optional exception if the call failed
        """
        if not self.config.enabled or not self.config.trace_llm_calls:
            return

        if not self.llm_span_id:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            end_time = _utc_now()
            duration = (
                (end_time - self._llm_start_time).total_seconds()
                if hasattr(self, "_llm_start_time")
                else 0
            )
            duration_ms = duration * 1000

            has_error = error is not None
            status = "error" if has_error else "success"

            # Extract token usage from response
            input_tokens = 0
            output_tokens = 0
            total_tokens_count = 0
            model = getattr(self, "_llm_model", "gemini")
            usage_details = {}

            if llm_response:
                # Google ADK uses 'usage_metadata' with prompt_token_count/candidates_token_count
                usage = getattr(llm_response, "usage_metadata", None)
                if usage:
                    input_tokens = getattr(usage, "prompt_token_count", 0) or 0
                    output_tokens = getattr(usage, "candidates_token_count", 0) or 0
                    total_tokens_count = getattr(usage, "total_token_count", 0) or 0

                    # Extract additional usage details
                    thoughts_tokens = getattr(usage, "thoughts_token_count", 0) or 0
                    cached_tokens = getattr(usage, "cached_content_token_count", 0) or 0
                    if thoughts_tokens:
                        usage_details["thoughts_token_count"] = thoughts_tokens
                    if cached_tokens:
                        usage_details["cached_content_token_count"] = cached_tokens

                # Fallback: total_token_count without breakdown
                if not input_tokens and not output_tokens and total_tokens_count:
                    input_tokens = int(total_tokens_count * 0.3)
                    output_tokens = total_tokens_count - input_tokens

                # Get model from response if available
                resp_model = getattr(llm_response, "model", None)
                if resp_model:
                    model = resp_model

                # Check for errors in response
                detected_error = self._error_detector.detect_from_llm_response(llm_response, model)
                if detected_error:
                    self._detected_errors.append(detected_error)
                    has_error = True
                    status = "error"

            # Calculate cost
            cost = calculate_google_adk_cost(model, input_tokens, output_tokens)
            input_price, output_price = get_model_pricing(model)
            input_cost = (input_tokens / 1_000_000) * input_price
            output_cost = (output_tokens / 1_000_000) * output_price

            # Update totals
            self._total_input_tokens += input_tokens
            self._total_output_tokens += output_tokens
            self._total_cost += cost

            # Extract finish reason from response candidates
            finish_reason = None
            if llm_response:
                candidates = getattr(llm_response, "candidates", None)
                if candidates and len(candidates) > 0:
                    fr = getattr(candidates[0], "finish_reason", None)
                    if fr:
                        finish_reason = str(fr).replace("FinishReason.", "")

            # Build rich metadata matching LangGraph format
            token_usage = {
                "unit": "TOKENS",
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
            }
            if usage_details:
                token_usage.update(usage_details)

            # Extract cache and reasoning tokens from Gemini format
            extracted_usage_details = {}
            if usage_details:
                # Google uses cached_content_token_count for cache reads
                cached = usage_details.get("cached_content_token_count", 0) or 0
                if cached:
                    extracted_usage_details["cache_read_input_tokens"] = cached
                # Reasoning/thinking tokens (if available)
                reasoning = (
                    usage_details.get("reasoning_tokens", 0)
                    or usage_details.get("thoughts_token_count", 0)
                    or 0
                )
                if reasoning:
                    extracted_usage_details["reasoning_tokens"] = reasoning

            llm_model_params = getattr(self, "_llm_model_parameters", {}) or {}
            span_metadata = merge_metadata(
                {
                    "model": model,
                    "model_id": model,
                    "model_name": model,
                    "agent_type": "llm",
                    "token_usage": token_usage,
                    "pricing_tier": f"google:{model}",
                    "total_tokens": input_tokens + output_tokens,
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "input_cost": input_cost,
                    "output_cost": output_cost,
                    "total_cost": cost,
                    "duration_ms": duration_ms,
                    "status": status,
                }
            )
            if finish_reason:
                span_metadata["finish_reason"] = finish_reason
            if llm_model_params:
                span_metadata["model_parameters"] = llm_model_params
                span_metadata["llm_parameters"] = llm_model_params
            if extracted_usage_details:
                span_metadata["usage_details"] = extracted_usage_details

            update_data = {
                "id": self.llm_span_id,
                "trace_id": self.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
                "status": status,
                "is_error": has_error,
                "metadata": merge_metadata(span_metadata),
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "total_cost": cost,
                "input_cost": input_cost,
                "output_cost": output_cost,
                "model": model,
                "cost_details": {
                    "input": input_cost,
                    "output": output_cost,
                    "total": cost,
                },
            }

            if usage_details:
                update_data["usage_details"] = usage_details

            # Capture output as structured JSON (matching LangGraph format)
            if self.config.capture_outputs and llm_response:
                content = getattr(llm_response, "content", None)
                response_text = _extract_text_from_contents(content) if content else ""
                output_data = {
                    "model": model,
                    "status": status,
                    "response": response_text[: self.config.max_content_length]
                    if response_text
                    else "",
                    "token_usage": token_usage,
                    "total_tokens": input_tokens + output_tokens,
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                }
                if finish_reason:
                    output_data["finish_reason"] = finish_reason
                update_data["output"] = output_data

            if error:
                error_str = str(error)[:500]
                update_data["error"] = error_str
                update_data["error_message"] = error_str
                self._has_errors = True
                if error_str not in self._error_messages:
                    self._error_messages.append(error_str)

            # Track for drift detection
            self._turn_count += 1
            if llm_response:
                content = getattr(llm_response, "content", None)
                response_text = _extract_text_from_contents(content) if content else ""
                if response_text:
                    self._drift_detector.record_llm_response(response_text, model)

            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)


            logger.debug(
                f"[AIGIE] LLM call completed: {model} (tokens={input_tokens + output_tokens}, cost=${cost:.6f})"
            )

        except Exception as e:
            logger.warning(f"[AIGIE] Error in handle_llm_end: {e}")
        finally:
            self.llm_span_id = None
            self._llm_start_time = None
            self._llm_model = None
            self._llm_model_parameters = None

    # ========================================================================
    # Tool Lifecycle Methods
    # ========================================================================

    async def handle_tool_start(
        self,
        tool: Any,
        tool_args: dict[str, Any],
        tool_context: Any,
    ) -> str:
        """
        Called before a tool execution.

        Args:
            tool: The BaseTool instance
            tool_args: Arguments passed to the tool
            tool_context: The ToolContext from ADK

        Returns:
            The tool span ID
        """
        if not self.config.enabled or not self.config.trace_tools:
            return ""

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        try:
            tool_name = getattr(tool, "name", "unknown_tool")
            function_call_id = getattr(tool_context, "function_call_id", str(uuid.uuid4()))

            span_id = str(uuid.uuid4())
            start_time = _utc_now()

            parent_id = self._get_current_parent()
            tool_depth = self._register_span_depth(span_id, parent_id)

            self.tool_map[function_call_id] = {
                "spanId": span_id,
                "startTime": start_time,
                "toolName": tool_name,
                "depth": tool_depth,
                "tool_args": tool_args,
            }

            span_data = {
                "id": span_id,
                "trace_id": self.trace_id,
                "parent_id": parent_id,
                "name": f"Tool: {tool_name}",
                "type": "tool",
                "start_time": start_time.isoformat(),
                "metadata": merge_metadata(
                    {
                        "tool_name": tool_name,
                        "function_call_id": function_call_id,
                        "framework": "google_adk",
                        "depth": tool_depth,
                    }
                ),
                "tags": self.tags,
                "status": "running",
                "depth": tool_depth,
            }

            # Add tool_category hint for component registry classification
            try:
                from ...tool_category import infer_tool_category

                category = infer_tool_category(tool_name, None)
                if category:
                    span_data["metadata"]["tool_category"] = category
            except ImportError:
                pass

            # Capture input if enabled
            if self.config.capture_inputs and tool_args:
                input_repr = str(tool_args)[: self.config.max_tool_result_length]
                span_data["input"] = input_repr

            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

            # Set process-level span ID for OTel bridge
            try:
                from ...auto_instrument.span_enricher import set_active_span_id

                set_active_span_id(span_id)
            except Exception:
                pass

            self._total_tool_calls += 1

            # Pre-tool interception signal (observe only, never blocks)
            try:
                intercept = await aigie.intercept_before_tool(
                    tool_name=tool_name,
                    tool_args=tool_args or {},
                    trace_id=self.trace_id,
                    span_id=span_id,
                )
                if intercept.get("decision") != "allow":
                    logger.info(
                        f"[AIGIE] Pre-tool signal for {tool_name}: {intercept.get('decision')}"
                    )
            except Exception:
                pass

            logger.debug(f"[AIGIE] Tool started: {tool_name} (span_id={span_id})")
            return span_id

        except Exception as e:
            logger.warning(f"[AIGIE] Error in handle_tool_start: {e}")
            return ""

    async def handle_tool_end(
        self,
        tool: Any,
        tool_args: dict[str, Any],
        tool_context: Any,
        result: Any,
        error: Exception | None = None,
    ) -> None:
        """
        Called after a tool execution completes.

        Args:
            tool: The BaseTool instance
            tool_args: Arguments passed to the tool
            tool_context: The ToolContext from ADK
            result: The tool execution result
            error: Optional exception if the tool failed
        """
        if not self.config.enabled or not self.config.trace_tools:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            function_call_id = getattr(tool_context, "function_call_id", None)
            if not function_call_id:
                return

            tool_data = self.tool_map.get(function_call_id)
            if not tool_data:
                return

            end_time = _utc_now()
            duration = (end_time - tool_data["startTime"]).total_seconds()
            duration_ms = duration * 1000

            tool_name = tool_data["toolName"]
            has_error = error is not None
            status = "error" if has_error else "success"

            # Error detection from tool result
            detected_error = self._error_detector.detect_from_tool_result(
                tool_name=tool_name,
                tool_use_id=function_call_id,
                result=result,
                is_error_flag=has_error,
                duration_ms=duration_ms,
            )
            if detected_error:
                self._detected_errors.append(detected_error)
                has_error = True
                status = "error"

            update_data = {
                "id": tool_data["spanId"],
                "trace_id": self.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
                "status": status,
                "is_error": has_error,
                "metadata": merge_metadata(
                    {
                        "tool_name": tool_name,
                        "function_call_id": function_call_id,
                        "duration_ms": duration_ms,
                        "status": status,
                    }
                ),
            }

            # Capture output if enabled
            if self.config.capture_outputs and result is not None:
                result_repr = str(result)[: self.config.max_tool_result_length]
                update_data["output"] = result_repr

            if error:
                error_str = str(error)[:500]
                update_data["error"] = error_str
                update_data["error_message"] = error_str
                self._has_errors = True
                if error_str not in self._error_messages:
                    self._error_messages.append(error_str)

            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

            # Record tool use for drift detection
            self._drift_detector.record_tool_use(
                tool_name=tool_name,
                tool_input=tool_args or {},
                duration_ms=duration_ms,
                is_error=has_error,
            )

            # Post-tool interception: report errors to backend for pattern learning
            if has_error:
                with contextlib.suppress(Exception):
                    await aigie.intercept_after_tool(
                        tool_name=tool_name,
                        result=result,
                        error=str(error) if error else None,
                        error_type=type(error).__name__ if error else None,
                        trace_id=self.trace_id,
                        span_id=tool_data["spanId"],
                        duration_ms=duration_ms,
                    )

            del self.tool_map[function_call_id]

            logger.debug(
                f"[AIGIE] Tool completed: {tool_name} (status={status}, duration_ms={duration_ms:.2f})"
            )

        except Exception as e:
            logger.warning(f"[AIGIE] Error in handle_tool_end: {e}")

    # ========================================================================
    # Event Handling
    # ========================================================================

    async def handle_event(
        self,
        invocation_context: Any,
        event: Any,
    ) -> None:
        """
        Called for each event in the Runner's event stream.

        Args:
            invocation_context: The InvocationContext from ADK
            event: The event object
        """
        if not self.config.enabled or not self.config.trace_events:
            return

        # Events are typically captured as metadata on existing spans
        # This hook can be used for fine-grained event tracking if needed
        pass

    # ========================================================================
    # Helper Methods
    # ========================================================================

    async def _complete_pending_spans(self, end_time: datetime) -> None:
        """Complete any pending spans that weren't explicitly closed."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        # Complete pending tool spans
        for _function_call_id, tool_data in list(self.tool_map.items()):
            duration = (end_time - tool_data["startTime"]).total_seconds()
            update_data = {
                "id": tool_data["spanId"],
                "trace_id": self.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
                "status": "success",
                "metadata": merge_metadata(
                    {
                        "tool_name": tool_data["toolName"],
                        "pending_cleanup": True,
                    }
                ),
            }
            with contextlib.suppress(Exception):
                await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)
        self.tool_map.clear()

        # Complete pending agent spans
        for agent_name, agent_data in list(self.agent_map.items()):
            duration = (end_time - agent_data["startTime"]).total_seconds()
            update_data = {
                "id": agent_data["spanId"],
                "trace_id": self.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
                "status": "success",
                "metadata": merge_metadata(
                    {
                        "agent_name": agent_name,
                        "pending_cleanup": True,
                    }
                ),
            }
            with contextlib.suppress(Exception):
                await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)
        self.agent_map.clear()

        # Complete pending LLM span
        if self.llm_span_id and hasattr(self, "_llm_start_time") and self._llm_start_time:
            duration = (end_time - self._llm_start_time).total_seconds()
            update_data = {
                "id": self.llm_span_id,
                "trace_id": self.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration * 1_000_000_000),
                "status": "success",
                "metadata": merge_metadata(
                    {
                        "pending_cleanup": True,
                    }
                ),
            }
            with contextlib.suppress(Exception):
                await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)
            self.llm_span_id = None

    def __repr__(self) -> str:
        return (
            f"GoogleADKHandler("
            f"trace_id={self.trace_id}, "
            f"model_calls={self._total_model_calls}, "
            f"tool_calls={self._total_tool_calls}, "
            f"tokens={self._total_input_tokens + self._total_output_tokens}, "
            f"cost=${self._total_cost:.4f})"
        )
