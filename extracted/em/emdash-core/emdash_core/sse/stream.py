"""SSE streaming infrastructure for agent events."""

import asyncio
import json
from datetime import datetime
from enum import Enum
from typing import Any, AsyncIterator

from pydantic import BaseModel

from ..utils.logger import log


class EventType(str, Enum):
    """Types of events emitted by agents (matches emdash.agent.events.EventType)."""

    # Tool lifecycle
    TOOL_START = "tool_start"
    TOOL_RESULT = "tool_result"

    # Sub-agent lifecycle
    SUBAGENT_START = "subagent_start"
    SUBAGENT_END = "subagent_end"

    # Agent thinking/progress
    THINKING = "thinking"
    PROGRESS = "progress"

    # Output
    RESPONSE = "response"
    PARTIAL_RESPONSE = "partial_response"
    ASSISTANT_TEXT = "assistant_text"

    # Interaction
    CLARIFICATION = "clarification"
    CLARIFICATION_RESPONSE = "clarification_response"
    CHOICE_QUESTIONS = "choice_questions"
    PLAN_MODE_REQUESTED = "plan_mode_requested"
    PLAN_SUBMITTED = "plan_submitted"

    # Errors
    ERROR = "error"
    WARNING = "warning"

    # Session
    SESSION_START = "session_start"
    SESSION_END = "session_end"

    # Context
    CONTEXT_FRAME = "context_frame"

    # Multiuser events
    USER_MESSAGE = "user_message"
    PARTICIPANT_JOINED = "participant_joined"
    PARTICIPANT_LEFT = "participant_left"
    QUEUE_UPDATED = "queue_updated"
    STATE_CHANGED = "state_changed"
    PROCESS_MESSAGE_REQUEST = "process_message_request"
    USER_TYPING = "user_typing"
    USER_STOPPED_TYPING = "user_stopped_typing"

    # LLM iteration tracking
    LLM_STEP = "llm_step"

    # Architecture changes (for real-time graph feedback)
    ARCHITECTURE_CHANGE = "architecture_change"
    FILE_CHANGED = "file_changed"


class SSEEvent(BaseModel):
    """An SSE event for streaming to clients."""

    type: EventType
    data: dict[str, Any]
    timestamp: datetime
    agent_name: str | None = None

    def to_sse(self) -> str:
        """Format as SSE wire protocol.

        Returns:
            SSE formatted string: "event: {type}\ndata: {json}\n\n"
        """
        payload = {
            **self.data,
            "timestamp": self.timestamp.isoformat(),
        }
        if self.agent_name:
            payload["agent_name"] = self.agent_name

        data_json = json.dumps(payload, default=str)
        return f"event: {self.type.value}\ndata: {data_json}\n\n"


class SSEHandler:
    """Event handler that queues events for SSE streaming.

    This handler implements the EventHandler protocol and collects
    events into an async queue for streaming to HTTP clients.

    Thread-safe: can be used from both async context and thread pools.
    """

    def __init__(self, agent_name: str | None = None):
        """Initialize the handler.

        Args:
            agent_name: Optional name to tag events
        """
        # Use thread-safe queue for cross-thread communication
        import queue
        self._queue: queue.Queue[SSEEvent | None] = queue.Queue()
        self._agent_name = agent_name
        self._closed = False
        self._cancelled = False  # Set when client disconnects

    @property
    def cancelled(self) -> bool:
        """Check if the client has disconnected/cancelled.

        Agents should check this periodically and stop if True.
        """
        return self._cancelled

    def handle(self, event: Any) -> None:
        """Handle an event from the agent.

        Args:
            event: AgentEvent from the agent system
        """
        if self._closed:
            return

        # Convert event type, with error handling for unknown types
        # AgentEvent uses 'event_type' attribute, not 'type'
        raw_type = getattr(event, 'event_type', None) or getattr(event, 'type', None)
        if raw_type is None:
            log.warning(f"Event has no event_type or type attribute: {event}")
            return

        try:
            event_type = EventType(raw_type.value)
        except ValueError:
            log.warning(
                f"Unknown SSE event type: {raw_type.value} - event dropped. "
                "This may indicate EventType enum in sse/stream.py is out of sync "
                "with agent/events.py"
            )
            return

        # Convert to SSEEvent
        sse_event = SSEEvent(
            type=event_type,
            data=event.data,
            timestamp=event.timestamp,
            agent_name=event.agent_name or self._agent_name,
        )

        # Put in queue (thread-safe)
        self._queue.put(sse_event)

    def emit(self, event_type: EventType, data: dict[str, Any]) -> None:
        """Emit an event directly (thread-safe).

        Args:
            event_type: Type of event
            data: Event data
        """
        if self._closed:
            return

        sse_event = SSEEvent(
            type=event_type,
            data=data,
            timestamp=datetime.now(),
            agent_name=self._agent_name,
        )

        self._queue.put(sse_event)

    async def emit_async(self, event_type: EventType, data: dict[str, Any]) -> None:
        """Emit an event asynchronously.

        Args:
            event_type: Type of event
            data: Event data
        """
        if self._closed:
            return

        sse_event = SSEEvent(
            type=event_type,
            data=data,
            timestamp=datetime.now(),
            agent_name=self._agent_name,
        )

        self._queue.put(sse_event)

    def emit_architecture_change(
        self,
        files_changed: list[dict[str, str]],
        new_nodes: list[dict[str, Any]],
        new_edges: list[dict[str, Any]],
        impact_summary: str,
    ) -> None:
        """Emit architectural impact data after file changes.

        Args:
            files_changed: List of {path, action, lines} for changed files
            new_nodes: Graph nodes that were added/modified
            new_edges: Edges that were created/modified
            impact_summary: Human-readable summary of architectural impact
        """
        if self._closed:
            return

        sse_event = SSEEvent(
            type=EventType.ARCHITECTURE_CHANGE,
            data={
                "files_changed": files_changed,
                "new_nodes": new_nodes,
                "new_edges": new_edges,
                "impact_summary": impact_summary,
            },
            timestamp=datetime.now(),
            agent_name=self._agent_name,
        )

        self._queue.put(sse_event)

    def close(self) -> None:
        """Close the handler and signal end of stream."""
        self._closed = True
        self._queue.put(None)  # Sentinel to end iteration

    async def __aiter__(self) -> AsyncIterator[str]:
        """Iterate over SSE-formatted events.

        Yields:
            SSE formatted strings ready for HTTP streaming

        When iteration ends (client disconnects), sets cancelled=True
        so running agents can detect and stop.
        """
        import queue

        loop = asyncio.get_event_loop()
        ping_counter = 0

        try:
            while True:
                try:
                    # Run blocking queue.get in executor to not block event loop
                    try:
                        event = await loop.run_in_executor(
                            None,  # Default executor
                            lambda: self._queue.get(timeout=1.0)
                        )
                        if event is None:
                            break
                        yield event.to_sse()
                        ping_counter = 0
                    except queue.Empty:
                        ping_counter += 1
                        # Send keep-alive ping every 30 seconds
                        if ping_counter >= 30:
                            yield ": ping\n\n"
                            ping_counter = 0
                        continue
                except Exception:
                    break
        finally:
            # Mark as cancelled when client disconnects or stream ends
            self._cancelled = True
            log.debug("SSE stream ended, marking handler as cancelled")


async def create_sse_stream(handler: SSEHandler) -> AsyncIterator[str]:
    """Create an SSE stream from a handler.

    Args:
        handler: SSE handler to stream from

    Yields:
        SSE formatted event strings
    """
    async for event in handler:
        yield event
