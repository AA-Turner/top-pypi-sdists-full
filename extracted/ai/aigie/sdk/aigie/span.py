"""
Span Context Manager for Aigie.
"""

import logging
from typing import Any
from uuid import uuid4

import httpx

from aigie.buffer import EventBuffer
from aigie.tracing.trace_state import deregister_open_span, register_open_span

logger = logging.getLogger(__name__)


class SpanContext:
    """
    Context manager for creating and managing spans.

    Usage:
        async with trace.span("operation", type="llm") as span:
            span.set_input({"prompt": "Hello"})
            result = await llm.ainvoke("Hello")
            span.set_output({"response": result})
    """

    def __init__(
        self,
        client: httpx.AsyncClient,
        api_url: str,
        trace_id: str,
        name: str,
        span_type: str,
        parent_id: str | None = None,
        buffer: EventBuffer | None = None,
    ):
        self.client = client
        self.api_url = api_url
        self.buffer = buffer
        self.trace_id = trace_id
        self.name = name
        self.span_type = span_type
        self.parent_id = parent_id
        # Pre-generate ID so children can reference it before span is entered
        self.id: str = str(uuid4())
        self._input: dict[str, Any] = {}
        self._output: dict[str, Any] = {}
        self._metadata: dict[str, Any] = {}
        # Public property for accessing output (used by use-case apps)
        self.output: dict[str, Any] = {}

        # LLM-specific fields (for Generation/LLM spans)
        self._model: str | None = None
        self._prompt_tokens: int = 0
        self._completion_tokens: int = 0
        self._total_tokens: int = 0
        self._input_cost: float = 0.0
        self._output_cost: float = 0.0
        self._total_cost: float = 0.0
        self._level: str | None = None  # ERROR, WARNING, INFO
        self._status_message: str | None = None
        self._start_time: Any | None = None  # Set in __aenter__

        # Additional fields for observability
        self._completion_start_time: Any | None = None  # TTFT - Time to First Token
        self._model_parameters: dict[str, Any] | None = None  # Model config (temperature, etc)
        self._latency_seconds: float | None = None  # Total latency in seconds
        self._agent_type: str | None = None  # Agent type for dashboard grouping

    async def __aenter__(self):
        """Create the span when entering context."""
        from datetime import datetime, timezone

        # ID is pre-generated in __init__ so children can reference it
        # Store start_time for later use in SPAN_UPDATE
        # Use timezone-aware UTC timestamps for consistent time display.
        # Preserve a pre-set _start_time (callers like _exit_span's fallback
        # pin it to the original on_*_start time so a re-entry doesn't stamp
        # a fresh timestamp that lands the duplicate row in a different
        # RANGE(start_time) partition and yields end_time < start_time).
        if self._start_time is None:
            self._start_time = datetime.now(timezone.utc)

        # A span is built mutably in memory and emitted exactly once
        # (finalized) by __aexit__/complete — no SPAN_CREATE is sent. Register
        # a finalize callable so an unclean shutdown still ships the span
        # (interrupted). Parent resolution rides the pre-generated self.id,
        # which children already reference.
        register_open_span(self.id, self._build_interrupted_payload)
        if not self.buffer:
            logger.debug(f"No buffer configured, span open not registered for {self.id}")
        return self

    def _build_interrupted_payload(self) -> dict[str, Any]:
        """Finalize payload for the shutdown drain (status overwritten to
        ``interrupted`` by the registry)."""
        from datetime import datetime, timezone

        end_time = datetime.now(timezone.utc)
        payload: dict[str, Any] = {
            "id": self.id,
            "span_id": self.id,
            "trace_id": self.trace_id,
            "name": self.name,
            "type": self.span_type,
            "start_time": self._start_time.isoformat() if self._start_time else None,
            "end_time": end_time.isoformat(),
            "input": self._input,
            "output": self._output,
            "metadata": self._metadata,
            "status": "interrupted",
        }
        if self.parent_id:
            payload["parent_id"] = self.parent_id
        return payload

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Update the span when exiting context."""
        from datetime import datetime, timezone

        if self.id:
            status = "failure" if exc_val else "success"
            # Use timezone-aware UTC timestamps for consistent time display
            end_time = datetime.now(timezone.utc)

            data = {
                "id": self.id,  # Include ID for buffered updates
                "span_id": self.id,  # Alternative field name
                "trace_id": self.trace_id,  # Required by backend for span updates
                "name": self.name,  # Include name for merge fallback
                "type": self.span_type,  # Include type for merge fallback
                "start_time": self._start_time.isoformat()
                if self._start_time
                else None,  # For merge fallback
                "input": self._input,
                "output": self._output,
                "metadata": self._metadata,  # Include metadata
                "status": status,
                "end_time": end_time.isoformat(),
            }

            # Include parent_id for merge fallback (in case span-create wasn't processed yet)
            if self.parent_id:
                data["parent_id"] = self.parent_id

            if exc_val:
                data["error_message"] = str(exc_val)
                data["error_type"] = type(exc_val).__name__

            # Include LLM-specific fields if set
            if self._model:
                data["model"] = self._model

            # Include usage object in multiple formats for maximum compatibility
            # Different backends expect different field names
            has_usage = (
                self._prompt_tokens > 0
                or self._completion_tokens > 0
                or self._total_tokens > 0
                or self._input_cost > 0
                or self._output_cost > 0
                or self._total_cost > 0
            )
            if has_usage:
                # Format 1: usage.input/output
                data["usage"] = {
                    "input": self._prompt_tokens,
                    "output": self._completion_tokens,
                    "total": self._total_tokens,
                    "unit": "TOKENS",
                    "input_cost": self._input_cost,
                    "output_cost": self._output_cost,
                    "total_cost": self._total_cost,
                }

                # Format 2: token_usage.prompt_tokens/completion_tokens (backend extraction format)
                data["token_usage"] = {
                    "prompt_tokens": self._prompt_tokens,
                    "completion_tokens": self._completion_tokens,
                    "total_tokens": self._total_tokens,
                    "input_cost": self._input_cost,
                    "output_cost": self._output_cost,
                    "total_cost": self._total_cost,
                }

                # Direct fields for backward compatibility with older backends
                data["prompt_tokens"] = self._prompt_tokens
                data["completion_tokens"] = self._completion_tokens
                data["total_tokens"] = self._total_tokens
                data["input_cost"] = self._input_cost
                data["output_cost"] = self._output_cost
                data["total_cost"] = self._total_cost
            if self._level:
                data["level"] = self._level
            if self._status_message:
                data["status_message"] = self._status_message

            # Include additional observability fields
            if self._completion_start_time:
                data["completion_start_time"] = (
                    self._completion_start_time.isoformat()
                    if hasattr(self._completion_start_time, "isoformat")
                    else str(self._completion_start_time)
                )
                # Also calculate TTFT if we have start_time
                if self._start_time and hasattr(self._completion_start_time, "timestamp"):
                    ttft_ms = (
                        self._completion_start_time - self._start_time
                    ).total_seconds() * 1000
                    data["time_to_first_token_ms"] = ttft_ms
                    # Add to metadata for compatibility
                    if "metadata" not in data:
                        data["metadata"] = {}
                    data["metadata"]["time_to_first_token_ms"] = ttft_ms

            if self._model_parameters:
                data["model_parameters"] = self._model_parameters

            if self._latency_seconds is not None:
                data["latency_seconds"] = self._latency_seconds
                # Also add duration_ns for API compatibility
                data["duration_ns"] = int(self._latency_seconds * 1_000_000_000)
            elif self._start_time:
                # Calculate latency from start to end
                latency = (end_time - self._start_time).total_seconds()
                data["latency_seconds"] = latency
                # Also add duration_ns for API compatibility
                data["duration_ns"] = int(latency * 1_000_000_000)

            if self._agent_type:
                data["agent_type"] = self._agent_type
                # Also add to metadata for backward compatibility
                if "metadata" not in data:
                    data["metadata"] = {}
                data["metadata"]["agent_type"] = self._agent_type

            # Ensure metadata has token_usage (input_tokens, output_tokens, total_tokens)
            if self._prompt_tokens > 0 or self._completion_tokens > 0 or self._total_tokens > 0:
                if "metadata" not in data:
                    data["metadata"] = {}
                # Token usage object
                data["metadata"]["token_usage"] = {
                    "input_tokens": self._prompt_tokens,
                    "output_tokens": self._completion_tokens,
                    "total_tokens": self._total_tokens,
                    "unit": "TOKENS",
                }
                # Also add direct fields in metadata for backend extraction
                data["metadata"]["prompt_tokens"] = self._prompt_tokens
                data["metadata"]["completion_tokens"] = self._completion_tokens
                data["metadata"]["total_tokens"] = self._total_tokens
                data["metadata"]["cost"] = self._total_cost
                data["metadata"]["estimated_cost"] = self._total_cost
                data["metadata"]["input_cost"] = self._input_cost
                data["metadata"]["output_cost"] = self._output_cost
                data["metadata"]["total_cost"] = self._total_cost

            # Add model to metadata for backend extraction
            if self._model:
                if "metadata" not in data:
                    data["metadata"] = {}
                data["metadata"]["model"] = self._model

            # Add model_parameters to metadata for backend extraction
            if self._model_parameters:
                if "metadata" not in data:
                    data["metadata"] = {}
                data["metadata"]["model_parameters"] = self._model_parameters

            # Emit the single finalized event + deregister from the open-span
            # registry (the span is no longer an orphan candidate).
            deregister_open_span(self.id)
            try:
                if self.buffer:
                    await self.buffer.add(data)
                else:
                    logger.debug(f"No buffer configured, span update dropped for {self.id}")
            except Exception as e:
                # Never re-raise from __aexit__ - this would crash the caller's app
                logger.warning(f"Failed to send span update for {self.id}: {e}")

    def set_input(self, data: dict[str, Any]) -> None:
        """Set span input data."""
        self._input = data
        # Note: Input will be included in __aexit__ update
        # If immediate update needed, use await span.update_input() instead

    def set_output(self, data: dict[str, Any]) -> None:
        """Set span output data."""
        self._output = data
        self.output = data  # Update public property for local access

    def set_metadata(self, data: dict[str, Any]) -> None:
        """Set span metadata."""
        self._metadata = data

    def set_model(self, model: str) -> None:
        """Set the model name for LLM spans."""
        self._model = model

    def set_usage(
        self,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int | None = None,
        input_cost: float = 0.0,
        output_cost: float = 0.0,
        total_cost: float | None = None,
    ) -> None:
        """Set token usage and cost data for LLM spans."""
        self._prompt_tokens = prompt_tokens
        self._completion_tokens = completion_tokens
        self._total_tokens = (
            total_tokens if total_tokens is not None else (prompt_tokens + completion_tokens)
        )
        self._input_cost = input_cost
        self._output_cost = output_cost
        self._total_cost = total_cost if total_cost is not None else (input_cost + output_cost)

    def set_level(self, level: str, status_message: str | None = None) -> None:
        """Set the log level and optional status message (for errors)."""
        self._level = level
        if status_message:
            self._status_message = status_message

    def set_completion_start_time(self, completion_start_time: Any) -> None:
        """Set the completion start time (Time to First Token)."""
        self._completion_start_time = completion_start_time

    def set_model_parameters(self, parameters: dict[str, Any]) -> None:
        """Set model parameters (temperature, top_p, etc.)."""
        self._model_parameters = parameters

    def set_latency(self, latency_seconds: float) -> None:
        """Set the total latency in seconds."""
        self._latency_seconds = latency_seconds

    def set_agent_type(self, agent_type: str) -> None:
        """Set the agent type for dashboard grouping."""
        self._agent_type = agent_type

    async def update_input(self, data: dict[str, Any] | None = None) -> None:
        """Update span input immediately (if span already created)."""
        if data:
            self._input = data
        # Input rides the finalized SPAN_UPDATE emitted in __aexit__ / complete().

    async def complete(self, status: str = "success", error: Exception | None = None) -> None:
        """
        Manually complete the span.

        Args:
            status: Span status (success, failure)
            error: Optional error exception
        """
        if not self.id:
            return

        data = {
            "id": self.id,
            "span_id": self.id,
            "trace_id": self.trace_id,  # Required by backend for span updates
            "output": self._output,
            "status": status,
        }
        if self._start_time:
            data["start_time"] = self._start_time.isoformat()
        if error:
            data["error_message"] = str(error)

        # Emit the single finalized event + deregister.
        deregister_open_span(self.id)
        if self.buffer:
            await self.buffer.add(data)
        else:
            logger.debug(f"No buffer configured, span complete dropped for {self.id}")
