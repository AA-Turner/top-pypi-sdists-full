"""
Session context management for LiveKit Agents integration.

Provides session context for grouping multiple interactions and
tracking session-level metadata.
"""

import logging
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


class LiveKitSessionContext:
    """
    Session context for grouping LiveKit Agents interactions.

    Tracks session metadata including room info, participant info,
    agent configurations, and cumulative metrics.

    Example:
        >>> with livekit_session("Customer Support Call", user_id="user-123") as session:
        ...     # All agent sessions within this block are grouped
        ...     session.add_metadata("room_id", "room-abc")
        ...     # ... run agents ...
        ...     print(f"Total turns: {session.total_turns}")
    """

    def __init__(
        self,
        name: str = "LiveKit Session",
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        self.name = name
        self.user_id = user_id
        self.session_id = session_id or str(uuid.uuid4())
        self.metadata = metadata or {}

        self.start_time: datetime = datetime.now(timezone.utc)
        self.end_time: datetime | None = None

        # Tracking
        self.total_turns: int = 0
        self.total_errors: int = 0
        self.agent_names: list[str] = []
        self._handlers: list[Any] = []

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the session context."""
        self.metadata[key] = value

    def record_turn(self) -> None:
        """Record a completed turn."""
        self.total_turns += 1

    def record_error(self) -> None:
        """Record an error."""
        self.total_errors += 1

    def register_handler(self, handler: Any) -> None:
        """Register a handler for this session context."""
        self._handlers.append(handler)
        if hasattr(handler, "session_id"):
            handler.session_id = self.session_id

    def close(self) -> None:
        """Close the session context."""
        self.end_time = datetime.now(timezone.utc)

    @property
    def duration_seconds(self) -> float:
        """Session duration in seconds."""
        end = self.end_time or datetime.now(timezone.utc)
        return (end - self.start_time).total_seconds()

    def to_dict(self) -> dict[str, Any]:
        """Convert session context to dictionary."""
        return {
            "session_id": self.session_id,
            "name": self.name,
            "user_id": self.user_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "total_turns": self.total_turns,
            "total_errors": self.total_errors,
            "agent_names": self.agent_names,
            "metadata": self.metadata,
        }


# Thread/async-safe session context
_current_session: ContextVar[LiveKitSessionContext | None] = ContextVar(
    "_current_session", default=None
)


def get_session_context() -> LiveKitSessionContext | None:
    """Get the current session context."""
    return _current_session.get()


def set_session_context(context: LiveKitSessionContext | None) -> None:
    """Set the current session context."""
    _current_session.set(context)


@contextmanager
def livekit_session(
    name: str = "LiveKit Session",
    user_id: str | None = None,
    metadata: dict[str, Any] | None = None,
):
    """Context manager for grouping LiveKit Agents interactions.

    Example:
        >>> with livekit_session("Support Call", user_id="u123") as session:
        ...     # Run agents here
        ...     pass
    """
    session = LiveKitSessionContext(name=name, user_id=user_id, metadata=metadata)
    token = _current_session.set(session)
    try:
        yield session
    finally:
        session.close()
        _current_session.reset(token)
