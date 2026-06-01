"""
Base Callback Infrastructure

This module provides the base classes and types for Aigie callbacks,
following the pattern established by LiteLLM's CustomLogger.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class CallbackEventType(Enum):
    """Types of callback events."""

    # Trace lifecycle
    TRACE_START = "trace_start"
    TRACE_END = "trace_end"
    TRACE_ERROR = "trace_error"

    # Span lifecycle
    SPAN_START = "span_start"
    SPAN_END = "span_end"
    SPAN_ERROR = "span_error"

    # LLM-specific events
    LLM_START = "llm_start"
    LLM_END = "llm_end"
    LLM_ERROR = "llm_error"
    LLM_STREAM_CHUNK = "llm_stream_chunk"

    # Tool events
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    TOOL_ERROR = "tool_error"

    # Agent events
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"
    AGENT_STEP = "agent_step"

    # Drift events
    DRIFT_DETECTED = "drift_detected"

    # Remediation events
    REMEDIATION_START = "remediation_start"
    REMEDIATION_END = "remediation_end"
    REMEDIATION_FAILED = "remediation_failed"

    # Evaluation events
    EVALUATION_START = "evaluation_start"
    EVALUATION_END = "evaluation_end"


@dataclass
class CallbackEvent:
    """
    Standard event structure passed to callbacks.

    This provides a consistent interface for all callback events,
    similar to LiteLLM's StandardLoggingPayload.
    """

    # Event identification
    event_type: CallbackEventType
    event_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # Context
    trace_id: str | None = None
    span_id: str | None = None
    parent_span_id: str | None = None

    # LLM details
    provider: str | None = None
    model: str | None = None

    # Request/Response
    messages: list[dict[str, Any]] | None = None
    response: dict[str, Any] | None = None
    response_text: str | None = None

    # Metrics
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    cost: float | None = None
    latency_ms: float | None = None

    # Status
    status: str = "success"  # "success", "error", "pending"
    error: str | None = None
    error_type: str | None = None

    # Additional data
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    # Drift/Remediation specific
    drift_score: float | None = None
    drift_type: str | None = None
    remediation_applied: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary for serialization."""
        return {
            "event_type": self.event_type.value,
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "provider": self.provider,
            "model": self.model,
            "messages": self.messages,
            "response": self.response,
            "response_text": self.response_text,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "cost": self.cost,
            "latency_ms": self.latency_ms,
            "status": self.status,
            "error": self.error,
            "error_type": self.error_type,
            "metadata": self.metadata,
            "tags": self.tags,
            "drift_score": self.drift_score,
            "drift_type": self.drift_type,
            "remediation_applied": self.remediation_applied,
        }

    @classmethod
    def from_span_data(
        cls,
        event_type: CallbackEventType,
        span_data: dict[str, Any],
    ) -> "CallbackEvent":
        """Create CallbackEvent from span data dictionary."""
        return cls(
            event_type=event_type,
            event_id=span_data.get("id", span_data.get("span_id", "")),
            trace_id=span_data.get("trace_id"),
            span_id=span_data.get("id", span_data.get("span_id")),
            parent_span_id=span_data.get("parent_id", span_data.get("parent_span_id")),
            provider=span_data.get("provider"),
            model=span_data.get("model"),
            messages=span_data.get("input", {}).get("messages"),
            response=span_data.get("output"),
            prompt_tokens=span_data.get("usage", {}).get("prompt_tokens"),
            completion_tokens=span_data.get("usage", {}).get("completion_tokens"),
            total_tokens=span_data.get("usage", {}).get("total_tokens"),
            cost=span_data.get("cost"),
            latency_ms=span_data.get("latency_ms"),
            status=span_data.get("status", "success"),
            error=span_data.get("error"),
            metadata=span_data.get("metadata", {}),
            tags=span_data.get("tags", []),
        )


class BaseCallback(ABC):
    """
    Base class for Aigie callbacks.

    Subclass this to create custom callback handlers that receive
    events during tracing.

    Similar to LiteLLM's CustomLogger, this provides hooks for
    different stages of the request lifecycle.
    """

    def __init__(self, name: str | None = None):
        """
        Initialize the callback.

        Args:
            name: Optional name for this callback instance
        """
        self.name = name or self.__class__.__name__
        self._enabled = True

    @property
    def enabled(self) -> bool:
        """Check if callback is enabled."""
        return self._enabled

    def enable(self) -> None:
        """Enable this callback."""
        self._enabled = True

    def disable(self) -> None:
        """Disable this callback."""
        self._enabled = False

    # ========== Abstract Methods ==========

    @abstractmethod
    async def on_event(self, event: CallbackEvent) -> None:
        """
        Called for every callback event.

        This is the main entry point for processing events.
        Override this method to handle all events in a unified way.

        Args:
            event: The callback event with all relevant data
        """
        pass

    # ========== Optional Hooks (can be overridden) ==========

    async def on_trace_start(self, event: CallbackEvent) -> None:
        """Called when a trace starts."""
        await self.on_event(event)

    async def on_trace_end(self, event: CallbackEvent) -> None:
        """Called when a trace ends."""
        await self.on_event(event)

    async def on_span_start(self, event: CallbackEvent) -> None:
        """Called when a span starts."""
        await self.on_event(event)

    async def on_span_end(self, event: CallbackEvent) -> None:
        """Called when a span ends."""
        await self.on_event(event)

    async def on_llm_start(self, event: CallbackEvent) -> None:
        """Called before an LLM call."""
        await self.on_event(event)

    async def on_llm_end(self, event: CallbackEvent) -> None:
        """Called after an LLM call completes."""
        await self.on_event(event)

    async def on_llm_error(self, event: CallbackEvent) -> None:
        """Called when an LLM call errors."""
        await self.on_event(event)

    async def on_tool_start(self, event: CallbackEvent) -> None:
        """Called before a tool call."""
        await self.on_event(event)

    async def on_tool_end(self, event: CallbackEvent) -> None:
        """Called after a tool call completes."""
        await self.on_event(event)

    async def on_drift_detected(self, event: CallbackEvent) -> None:
        """Called when drift is detected."""
        await self.on_event(event)

    async def on_remediation_start(self, event: CallbackEvent) -> None:
        """Called when remediation starts."""
        await self.on_event(event)

    async def on_remediation_end(self, event: CallbackEvent) -> None:
        """Called when remediation ends."""
        await self.on_event(event)

    # ========== Lifecycle ==========

    async def initialize(self) -> None:
        """
        Initialize the callback.

        Override this for any async initialization needed.
        """
        pass

    async def shutdown(self) -> None:
        """
        Shutdown the callback.

        Override this for cleanup (closing connections, flushing buffers, etc.)
        """
        pass

    async def flush(self) -> None:
        """
        Flush any buffered events.

        Override this if the callback buffers events.
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, enabled={self.enabled})"
