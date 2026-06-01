"""
Aigie Tracing Processor for OpenAI Agents SDK.

Implements the TracingProcessor interface from OpenAI Agents SDK
to send traces to Aigie backend.
"""

import asyncio
import logging
import threading
import time
import uuid
from typing import Any

logger = logging.getLogger(__name__)


class AigieTracingProcessor:
    """Tracing processor that sends OpenAI Agents SDK traces to Aigie.

    This implements the TracingProcessor interface from OpenAI Agents SDK,
    allowing seamless integration with their built-in tracing system.

    Usage:
        from agents import add_trace_processor
        from aigie.integrations.openai_agents import AigieTracingProcessor

        processor = AigieTracingProcessor()
        add_trace_processor(processor)  # Additive to existing tracing

        # Now all agent operations are automatically traced to Aigie
        result = await Runner.run(agent, "Hello!")
    """

    def __init__(
        self,
        trace_name: str = "OpenAI Agents Workflow",
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        """Initialize the Aigie tracing processor."""
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id

        # State
        self._aigie: Any = None
        self._trace_id: str | None = None  # Current active aigie trace ID
        self._trace_map: dict[str, str] = {}  # Maps SDK trace IDs to Aigie trace IDs
        self._span_map: dict[str, Any] = {}  # Maps span/trace IDs to span data dicts
        self._span_start_times: dict[str, float] = {}

        # Lock for thread-safe access to shared state
        self._lock = threading.RLock()

        # Statistics
        self.total_tokens = 0
        self.total_cost = 0.0

    def _get_aigie(self) -> Any | None:
        """Lazy load Aigie client."""
        if self._aigie is None:
            try:
                from ...client import get_aigie

                self._aigie = get_aigie()
            except Exception as e:
                logger.debug(f"Could not get aigie client: {e}")
        return self._aigie

    def _schedule_async(self, coro: Any) -> None:
        """Schedule an async coroutine from sync context without blocking the agent."""

        async def _safe_run() -> None:
            try:
                await coro
            except Exception as e:
                # Tracing must never raise into the agent.
                logger.debug(f"Background tracing task failed (non-fatal): {e}")

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(_safe_run())
        except RuntimeError:
            # No running loop — run in a daemon thread.
            import threading

            threading.Thread(target=asyncio.run, args=(_safe_run(),), daemon=True).start()

    # -----------------------------------------------------------------------
    # TracingProcessor interface — handles both:
    #   SDK v0.8+ object-based calls: on_trace_start(trace_obj)
    #   Internal/test positional calls: on_trace_start(trace_id_str, name_str)
    # -----------------------------------------------------------------------

    def on_trace_start(self, trace_or_id: Any, name: Any = None) -> None:
        """Called when a new trace begins.

        Accepts both SDK object style (trace_or_id is a Trace object)
        and positional style (trace_or_id is a str trace ID, name is str).
        """
        if isinstance(trace_or_id, str):
            sdk_trace_id = trace_or_id
            trace_name = name or self.trace_name
        else:
            trace = trace_or_id
            sdk_trace_id = getattr(trace, "trace_id", str(uuid.uuid4()))
            trace_name = getattr(trace, "name", None) or self.trace_name

        aigie_trace_id = str(uuid.uuid4())
        with self._lock:
            self._trace_map[sdk_trace_id] = aigie_trace_id
            self._trace_id = aigie_trace_id
            now = time.time()
            self._span_map[aigie_trace_id] = {
                "name": trace_name,
                "start_time": now,
                "metadata": {
                    "sdk_trace_id": sdk_trace_id,
                    **self.metadata,
                },
            }

        logger.debug(f"Trace started: {trace_name} (id={sdk_trace_id})")

        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                self._schedule_async(
                    aigie._buffer.add(
                        EventType.CREATE_TRACE,
                        trace_id=aigie_trace_id,
                        name=trace_name,
                        metadata={
                            "sdk_trace_id": sdk_trace_id,
                            **self.metadata,
                        },
                        tags=self.tags,
                        user_id=self.user_id,
                        session_id=self.session_id,
                    )
                )
            except Exception as e:
                logger.debug(f"Error creating trace: {e}")

    def on_trace_end(self, trace_or_id: Any) -> None:
        """Called when a trace completes."""
        if isinstance(trace_or_id, str):
            sdk_trace_id = trace_or_id
        else:
            sdk_trace_id = getattr(trace_or_id, "trace_id", None)

        with self._lock:
            aigie_trace_id = self._trace_map.get(sdk_trace_id) if sdk_trace_id else None
        if not aigie_trace_id:
            return

        logger.debug(f"Trace ended: {sdk_trace_id}")

        # Update trace entry with end time and accumulated totals
        with self._lock:
            if aigie_trace_id in self._span_map:
                span_data = self._span_map[aigie_trace_id]
                now = time.time()
                span_data["end_time"] = now
                start_time = span_data.get("start_time", now)
                span_data["duration"] = now - start_time
                span_data["metadata"].update(
                    {
                        "total_tokens": self.total_tokens,
                        "total_cost": self.total_cost,
                    }
                )

        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                self._schedule_async(
                    aigie._buffer.add(
                        EventType.END_TRACE,
                        trace_id=aigie_trace_id,
                        metadata={
                            "total_tokens": self.total_tokens,
                            "total_cost": self.total_cost,
                        },
                    )
                )
            except Exception as e:
                logger.debug(f"Error ending trace: {e}")

        self.flush()

    def on_span_start(
        self,
        span_id: Any = None,
        trace_id: Any = None,
        parent_span_id: Any = None,
        name: Any = None,
        span_type: Any = None,
    ) -> None:
        """Called when a new span begins.

        Accepts both SDK object style (span_id is a Span object)
        and positional/keyword style (span_id is a str span ID).
        """
        if isinstance(span_id, str):
            resolved_span_id = span_id
            sdk_trace_id = trace_id
            parent_id = parent_span_id
            span_name = name or "span"
            mapped_type = self._map_span_type(span_type or "")
        else:
            span = span_id
            resolved_span_id = getattr(span, "span_id", str(uuid.uuid4()))
            sdk_trace_id = getattr(span, "trace_id", None)
            parent_id = getattr(span, "parent_id", None)
            span_data_obj = getattr(span, "span_data", None)
            span_name = (
                getattr(span_data_obj, "name", None)
                or getattr(span_data_obj, "type", "span")
                or "span"
            )
            mapped_type = self._map_span_type(getattr(span_data_obj, "type", "") or "")

        with self._lock:
            aigie_trace_id = self._trace_map.get(sdk_trace_id) if sdk_trace_id else None
            now = time.time()
            self._span_start_times[resolved_span_id] = now
            self._span_map[resolved_span_id] = {
                "name": span_name,
                "type": mapped_type,
                "start_time": now,
                "metadata": {},
            }

        logger.debug(f"Span started: {span_name} (type={mapped_type})")

        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                self._schedule_async(
                    aigie._buffer.add(
                        EventType.CREATE_SPAN,
                        trace_id=aigie_trace_id,
                        span_id=resolved_span_id,
                        parent_span_id=parent_id,
                        name=span_name,
                        span_type=mapped_type,
                        metadata={},
                    )
                )
            except Exception as e:
                logger.debug(f"Error creating span: {e}")

    def on_span_end(
        self,
        span_or_id: Any = None,
        output: Any = None,
        error: Any = None,
    ) -> None:
        """Called when a span completes.

        Accepts both SDK object style (span_or_id is a Span object)
        and positional/keyword style (span_or_id is a str span ID).
        """
        if isinstance(span_or_id, str):
            span_id = span_or_id
            span_output = output
            span_error = error
        else:
            span = span_or_id
            span_id = getattr(span, "span_id", None)
            if not span_id:
                return
            span_data_obj = getattr(span, "span_data", None)
            span_error = getattr(span, "error", None)
            span_output = getattr(span_data_obj, "output", None)

            # Extract token usage from generation spans via on_generation
            usage = getattr(span_data_obj, "usage", None)
            if usage:
                input_tokens = getattr(usage, "input_tokens", 0) or 0
                output_tokens = getattr(usage, "output_tokens", 0) or 0
                model = getattr(span_data_obj, "model", None)
                self.on_generation(
                    span_id,
                    model or "",
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                )

                # Extract cache and reasoning tokens from OpenAI usage details
                usage_details = {}
                if hasattr(usage, "prompt_tokens_details"):
                    ptd = usage.prompt_tokens_details
                    cached = getattr(ptd, "cached_tokens", 0) or 0
                    if cached:
                        usage_details["cache_read_input_tokens"] = cached
                if hasattr(usage, "completion_tokens_details"):
                    ctd = usage.completion_tokens_details
                    reasoning = getattr(ctd, "reasoning_tokens", 0) or 0
                    if reasoning:
                        usage_details["reasoning_tokens"] = reasoning
                if usage_details:
                    with self._lock:
                        if span_id in self._span_map:
                            self._span_map[span_id].setdefault("metadata", {})["usage_details"] = (
                                usage_details
                            )

        with self._lock:
            if span_id not in self._span_map:
                return
            span_data = self._span_map[span_id]
            now = time.time()
            start_time = self._span_start_times.pop(span_id, span_data.get("start_time", now))
            span_data["end_time"] = now
            span_data["duration"] = now - start_time

        status = "error" if span_error else "success"
        span_name = span_data.get("name", span_id)
        logger.debug(f"Span ended: {span_name}")

        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                from ...buffer import EventType

                metadata_payload = {
                    "error": str(span_error) if span_error else None,
                    "duration": span_data["duration"],
                }
                if "usage_details" in span_data.get("metadata", {}):
                    metadata_payload["usage_details"] = span_data["metadata"]["usage_details"]
                self._schedule_async(
                    aigie._buffer.add(
                        EventType.UPDATE_SPAN,
                        span_id=span_id,
                        output=str(span_output) if span_output is not None else None,
                        status=status,
                        metadata=metadata_payload,
                    )
                )
            except Exception as e:
                logger.debug(f"Error updating span: {e}")

    # -----------------------------------------------------------------------
    # Rich helper methods (for direct use and called from on_span_end above)
    # -----------------------------------------------------------------------

    def on_tool_call(
        self,
        span_id: str,
        tool_name: str,
        arguments: Any = None,
        result: Any = None,
    ) -> None:
        """Record a tool call within a span."""
        if span_id not in self._span_map:
            return
        metadata = self._span_map[span_id].setdefault("metadata", {})
        metadata["tool_name"] = tool_name
        metadata["arguments"] = arguments
        metadata["result"] = str(result) if result is not None else None

    def on_generation(
        self,
        span_id: str,
        model: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> None:
        """Record an LLM generation within a span, accumulating token counts."""
        total = (input_tokens or 0) + (output_tokens or 0)
        cost = 0.0
        if model:
            try:
                from .cost_tracking import get_openai_agents_cost

                cost_info = get_openai_agents_cost(model, input_tokens, output_tokens)
                if cost_info:
                    cost = cost_info.get("total_cost", 0.0)
            except Exception as e:
                logger.debug("Cost tracking error for model %s: %s", model, e)

        with self._lock:
            self.total_tokens += total
            self.total_cost += cost
            if span_id not in self._span_map:
                return
            metadata = self._span_map[span_id].setdefault("metadata", {})
            metadata["model"] = model
            metadata["input_tokens"] = input_tokens
            metadata["output_tokens"] = output_tokens
            metadata["total_tokens"] = total

    def on_handoff(self, span_id: str, source: str, target: str) -> None:
        """Record a handoff between agents."""
        if span_id not in self._span_map:
            return
        metadata = self._span_map[span_id].setdefault("metadata", {})
        metadata["handoff_source"] = source
        metadata["handoff_target"] = target

    def on_guardrail(self, span_id: str, name: str, passed: bool) -> None:
        """Record a guardrail check result."""
        if span_id not in self._span_map:
            return
        metadata = self._span_map[span_id].setdefault("metadata", {})
        metadata["guardrail_name"] = name
        metadata["guardrail_passed"] = passed

    # -----------------------------------------------------------------------
    # Utilities
    # -----------------------------------------------------------------------

    def _map_span_type(self, sdk_type: str) -> str:
        """Map SDK span type to Aigie span type."""
        type_mapping = {
            "agent": "agent",
            "llm": "llm",
            "generation": "llm",
            "response": "llm",
            "tool": "tool",
            "function": "tool",
            "handoff": "chain",
            "guardrail": "tool",
            "workflow": "chain",
            "runner": "chain",
        }
        return type_mapping.get((sdk_type or "").lower(), "chain")

    def get_statistics(self) -> dict[str, Any]:
        """Get current tracing statistics."""
        return {
            "trace_count": len(self._trace_map),
            "span_count": len(self._span_map),
            "active_traces": len(self._trace_map),
            "active_spans": len(self._span_start_times),
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
        }

    def flush(self) -> None:
        """Flush any pending traces to the backend."""
        aigie = self._get_aigie()
        if aigie and aigie._initialized:
            try:
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(self._safe_flush(aigie))
                except RuntimeError:
                    import threading

                    threading.Thread(
                        target=asyncio.run, args=(self._safe_flush(aigie),), daemon=True
                    ).start()
            except Exception as e:
                logger.debug(f"Error flushing traces: {e}")

    async def _safe_flush(self, aigie: Any) -> None:
        """Flush buffer, suppressing any errors so the agent is never affected."""
        try:
            await aigie._buffer.flush()
        except Exception as e:
            logger.debug(f"Error flushing traces (non-fatal): {e}")

    def force_flush(self) -> None:
        """Force immediate processing of any queued traces/spans."""
        self.flush()

    def shutdown(self) -> None:
        """Shutdown the processor and flush remaining traces."""
        self.flush()
        self._span_map.clear()
        self._trace_map.clear()
        self._span_start_times.clear()
