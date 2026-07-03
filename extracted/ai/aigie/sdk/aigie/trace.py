"""
Trace Context Manager for Aigie.
"""

import logging
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from aigie.buffer import EventBuffer
from aigie.sampling import should_send_event
from aigie.span import SpanContext
from aigie.tracing.trace_state import deregister_open_span, register_open_span

logger = logging.getLogger(__name__)


class TraceContext:
    """
    Context manager for creating and managing traces.

    Usage:
        async with aigie.trace("My Workflow") as trace:
            async with trace.span("operation", type="llm") as span:
                result = await do_work()
                span.set_output({"result": result})
    """

    def __init__(
        self,
        name: str,
        metadata: dict[str, Any],
        tags: list[str],
        buffer: EventBuffer | None = None,
        sample_rate: float | None = None,
    ):
        self.buffer = buffer
        self.name = name
        self.metadata = metadata
        self.tags = tags
        self.sample_rate = sample_rate
        self.id: str | None = None
        # Captured eagerly so the trace_create wire payload carries a real
        # start_time. Without this the dispatch is fire-and-forget on the
        # event loop and span_create events (synchronous emission) reach the
        # platform first; server-side timestamping then stamps the trace
        # later than its own child spans, breaking UI duration math.
        self.start_time: datetime = datetime.now(timezone.utc)
        self._prompt: Any | None = None  # Prompt object
        self._trace_context: Any | None = None  # W3C trace context
        self._evaluation_hooks: list[Any] = []  # Evaluation hooks
        self._evaluation_results: list[dict[str, Any]] = []  # Evaluation results

    async def __aenter__(self):
        """Create the trace when entering context."""
        # Track feature usage (best-effort).
        try:
            from aigie.licensing import track_feature

            track_feature("tracing")
        except Exception as e:
            logger.debug("Feature tracking failed: %s", e)

        # Set this trace as the current trace for auto-instrumentation
        from aigie.auto_instrument.trace import set_current_trace

        set_current_trace(self)

        if not self.id:
            self.id = str(uuid4())

        enriched_metadata = self._standardize_metadata()

        # Check sampling before sending
        if not should_send_event(self.id, self.sample_rate):
            # Not sampled - skip sending but still return context for local use
            return self

        # Trace identity rides the root span (root.id == trace_id, parent None).
        # The trace is emitted exactly once on __aexit__/complete — no
        # TRACE_CREATE. Register a finalize callable so an unclean shutdown
        # still ships the root (interrupted).
        self._open_payload = self._build_open_payload(enriched_metadata)
        register_open_span(self.id, self._build_interrupted_root_payload)
        if not self.buffer:
            logger.debug(f"No buffer configured, trace open not registered for {self.id}")

        return self

    def _standardize_metadata(self) -> dict[str, Any]:
        """Normalize session/user/env/release aliases in the trace metadata."""
        enriched = dict(self.metadata)
        if "user_id" in enriched or "userId" in enriched:
            enriched["user_id"] = enriched.get("user_id") or enriched.get("userId")
        if "session_id" in enriched or "sessionId" in enriched:
            enriched["session_id"] = enriched.get("session_id") or enriched.get("sessionId")
        if "environment" in enriched or "env" in enriched:
            enriched["environment"] = enriched.get("environment") or enriched.get("env")
        if "release_version" in enriched or "version" in enriched:
            enriched["release_version"] = enriched.get("release_version") or enriched.get("version")
        return enriched

    def _build_open_payload(self, enriched_metadata: dict[str, Any]) -> dict[str, Any]:
        """Open/interrupted-root base payload built from standardized metadata."""
        payload: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "status": "running",
            "metadata": enriched_metadata,
            "tags": self.tags,
        }
        direct = {
            "user_id": enriched_metadata.get("user_id") or enriched_metadata.get("userId"),
            "session_id": enriched_metadata.get("session_id") or enriched_metadata.get("sessionId"),
            "environment": enriched_metadata.get("environment")
            or enriched_metadata.get("env", "default"),
            "release": enriched_metadata.get("release") or enriched_metadata.get("release_version"),
            "version": enriched_metadata.get("version"),
        }
        payload.update({k: v for k, v in direct.items() if v})
        for key in ("input", "output"):
            if enriched_metadata.get(key) is not None:
                payload[key] = enriched_metadata[key]
        return payload

    def _build_interrupted_root_payload(self) -> dict[str, Any]:
        """Root-span finalize payload for the shutdown drain (status
        overwritten to ``interrupted`` by the registry)."""
        base = dict(getattr(self, "_open_payload", {}) or {})
        end_time = datetime.now(timezone.utc)
        duration_ns = int((end_time - self.start_time).total_seconds() * 1_000_000_000) or 1
        base.update(
            {
                "id": self.id,
                "span_id": self.id,
                "trace_id": self.id,
                "parent_id": None,
                "name": self.name,
                "type": "workflow",
                "status": "interrupted",
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_ns": duration_ns,
            }
        )
        return base

    def update(
        self,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        name: str | None = None,
        input: Any | None = None,
        output: Any | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ) -> None:
        """Update the trace with additional metadata, tags, or fields.

        Use this to enrich an auto-instrumented trace with your own identifiers.

        Example:
            # Inside your agent handler, tag the current trace with your request ID
            trace = aigie.get_current_trace()
            trace.update(metadata={"request_id": req_id, "customer_id": cid})

        Args:
            metadata: Merge into existing trace metadata
            tags: Append to existing trace tags
            name: Override trace name
            input: Set trace input
            output: Set trace output
            user_id: Set user identifier
            session_id: Set session identifier
        """
        if metadata:
            self.metadata.update(metadata)
        if tags:
            self.tags.extend(tags)
        if name:
            self.name = name
        if input is not None:
            self.metadata["input"] = input
        if output is not None:
            self.metadata["output"] = output
        if user_id:
            self.metadata["user_id"] = user_id
        if session_id:
            self.metadata["session_id"] = session_id

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Complete the trace when exiting context."""
        # Clear current trace from context for auto-instrumentation
        from aigie.auto_instrument.trace import clear_current_trace

        clear_current_trace()

        if not self.id:
            return

        status = "failure" if exc_val else "success"
        error_data = {}
        if exc_val:
            error_data = {"error_message": str(exc_val), "error_type": type(exc_val).__name__}

        update_data = self._build_finalize_payload(status, error_data)

        deregister_open_span(self.id)
        try:
            if self.buffer:
                await self.buffer.add(update_data)
            else:
                logger.debug(f"No buffer configured, trace update dropped for {self.id}")
        except Exception as e:
            # Never re-raise from __aexit__ - this would crash the caller's app
            logger.warning(f"Failed to send trace update for {self.id}: {e}")

    def _build_finalize_payload(self, status: str, error_data: dict[str, Any]) -> dict[str, Any]:
        """Root-span finalize payload. The trace IS the root span (span_id ==
        trace_id, parent_id None) — the platform mints the trace row from it.
        Final status + end_time only; cost/token/execution rollups are derived
        server-side from child spans, never computed in the SDK."""
        end_time = datetime.now(timezone.utc)
        return {
            "id": self.id,
            "trace_id": self.id,
            "span_id": self.id,
            "parent_id": None,
            "name": self.name,
            "type": "workflow",
            "status": status,
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "metadata": dict(self.metadata),
            **error_data,
        }

    def span(
        self, name: str, type: str = "tool", parent: str | None = None, stream: bool = False
    ) -> Any:
        """
        Create a span within this trace.

        Args:
            name: Span name
            type: Span type (llm, tool, agent, chain, workflow)
            parent: Optional parent span ID (can be span ID string or SpanContext object)
            stream: Whether to enable streaming (returns StreamingSpan)

        Returns:
            SpanContext manager (or StreamingSpan if stream=True)
        """
        if not self.id:
            raise RuntimeError("Trace not created yet. Use 'async with trace:' first.")

        # Handle parent - can be span ID string or SpanContext object
        parent_id = None
        if parent:
            if isinstance(parent, str):
                parent_id = parent
            elif hasattr(parent, "id"):
                parent_id = parent.id

        span_ctx = SpanContext(
            trace_id=self.id,
            name=name,
            span_type=type,
            parent_id=parent_id,
            buffer=self.buffer,
        )

        # Return streaming span if requested
        if stream:
            from aigie.streaming import StreamingSpan

            return StreamingSpan(span_ctx, stream=True)

        return span_ctx

    def set_prompt(self, prompt: Any) -> None:
        """
        Associate a prompt with this trace.

        Args:
            prompt: Prompt object from PromptManager
        """
        self._prompt = prompt

    def set_trace_context(self, context: Any) -> None:
        """
        Set W3C trace context for distributed tracing.

        Args:
            context: TraceContext object
        """
        self._trace_context = context

    def get_trace_context(self) -> Any | None:
        """Get W3C trace context."""
        return self._trace_context

    def get_trace_headers(self) -> dict[str, str]:
        """
        Get W3C trace context headers for HTTP propagation.

        Returns:
            Dictionary of headers to add to HTTP requests
        """
        if self._trace_context:
            return self._trace_context.to_headers()
        return {}

    def add_evaluation_hook(self, hook: Any) -> None:
        """
        Add an evaluation hook to run on trace completion.

        Args:
            hook: EvaluationHook instance
        """
        self._evaluation_hooks.append(hook)

    async def run_evaluations(
        self, expected: Any, actual: Any, context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Run all evaluation hooks.

        Args:
            expected: Expected value
            actual: Actual value
            context: Optional context

        Returns:
            List of evaluation results
        """
        results = []
        for hook in self._evaluation_hooks:
            try:
                result = await hook.run(expected, actual, context)
                results.append(
                    {
                        "name": hook.name,
                        "score": result.score,
                        "score_type": result.score_type.value,
                        "metadata": result.metadata,
                        "explanation": result.explanation,
                    }
                )
            except Exception as e:
                # Don't fail trace on evaluation errors
                logger.warning(f"Evaluation hook {hook.name} failed: {e}")

        self._evaluation_results = results
        return results

    def get_evaluation_results(self) -> list[dict[str, Any]]:
        """Get evaluation results."""
        return self._evaluation_results

    async def complete(self, status: str = "success", error: Exception | None = None) -> None:
        """
        Manually complete the trace.

        Args:
            status: Trace status (success, failure, error)
            error: Optional error exception
        """
        if not self.id:
            return

        # The trace IS the root span (span_id == trace_id, parent_id None).
        data = {
            "id": self.id,
            "span_id": self.id,
            "trace_id": self.id,
            "parent_id": None,
            "name": self.name,
            "type": "workflow",
            "status": status,
        }
        if error:
            data.update({"error_message": str(error), "error_type": type(error).__name__})

        # Emit the single finalized root event + deregister.
        deregister_open_span(self.id)
        if self.buffer:
            await self.buffer.add(data)
        else:
            logger.debug(f"No buffer configured, trace complete dropped for {self.id}")


def get_current_trace() -> TraceContext | None:
    """Get the active trace from the current context.

    Returns the trace that auto-instrumentation or ``aigie.trace()`` created.
    Use this to enrich the trace with your own identifiers:

        trace = aigie.get_current_trace()
        if trace:
            trace.update(metadata={"request_id": req_id, "action_id": action_id})
    """
    from aigie.auto_instrument.trace import get_current_trace as _get

    return _get()


def update_current_trace(
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
    name: str | None = None,
    input: Any | None = None,
    user_id: str | None = None,
    session_id: str | None = None,
) -> bool:
    """Enrich the current auto-instrumented trace with custom data.

    Convenience wrapper — gets the current trace and calls ``trace.update()``.
    Returns True if a trace was found and updated, False otherwise.

    Example::

        import aigie
        aigie.update_current_trace(
            name=request_id,
            metadata={"action_id": action_id, "customer_id": customer_id},
        )
        await graph.ainvoke(...)
    """
    trace = get_current_trace()
    if trace is None:
        return False
    trace.update(
        metadata=metadata,
        tags=tags,
        name=name,
        input=input,
        user_id=user_id,
        session_id=session_id,
    )
    return True
