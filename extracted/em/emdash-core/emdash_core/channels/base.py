"""Channel ABC and shared data types for bidirectional agent communication."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import AsyncIterator


@dataclass
class ImageAttachment:
    """Base64-encoded image attached to a channel message."""

    data: str  # Base64-encoded image bytes
    format: str = "jpg"  # Image format (jpg, png, etc.)


@dataclass
class ChannelMessage:
    """Inbound message from any channel."""

    content: str
    sender_id: str
    message_id: str = ""
    metadata: dict = field(default_factory=dict)
    images: list[ImageAttachment] = field(default_factory=list)


@dataclass
class ChannelEvent:
    """Outbound event to deliver to user."""

    type: str  # "text", "thinking", "tool", "error"
    content: str
    is_update: bool = False
    metadata: dict = field(default_factory=dict)


@dataclass
class DeliveryResult:
    """Result of delivering an event to a channel."""

    success: bool
    channel: str
    message_id: str = ""
    error: str = ""


class Channel(ABC):
    """Abstract base class for bidirectional agent communication channels.

    Captures the shared poll -> route -> stream -> format -> deliver pattern
    used by Telegram bridge, CLI interactive, and future channels.
    """

    name: str = ""

    # -- Lifecycle --

    async def start(self) -> None:
        """Initialize the channel (connect, authenticate, etc.)."""

    async def stop(self) -> None:
        """Gracefully shut down the channel."""

    async def is_available(self) -> bool:
        """Return True if the channel is ready to deliver messages."""
        return True

    # -- Inbound --

    @abstractmethod
    def poll_messages(self) -> AsyncIterator[ChannelMessage]:
        """Yield inbound messages from the channel's transport.

        Concrete implementations should be async generators.
        """
        ...

    async def check_authorization(self, sender_id: str) -> bool:
        """Return True if sender_id is allowed to interact."""
        return True

    # -- Outbound --

    @abstractmethod
    async def send_event(
        self, sender_id: str, event: ChannelEvent
    ) -> DeliveryResult:
        """Deliver an outbound event to the user."""
        ...

    async def update_event(
        self, sender_id: str, message_id: str, event: ChannelEvent
    ) -> DeliveryResult:
        """Edit a previously-sent message (default: send as new)."""
        return await self.send_event(sender_id, event)

    # -- Activity indicator --

    async def notify_activity(self, sender_id: str) -> None:
        """Signal that the agent is working (e.g. typing indicator).

        Called when the stream starts and when events are suppressed.
        Default implementation is a no-op.
        """

    # -- SSE formatting --

    def format_sse_event(
        self, event_type: str, data: dict
    ) -> ChannelEvent | None:
        """Convert a raw SSE event into a ChannelEvent for this channel.

        Return None to skip the event.
        """
        content = data.get("content") or data.get("message") or data.get("text", "")
        if not content:
            return None
        return ChannelEvent(type=event_type, content=str(content))

    # -- Session tracking --

    def get_session_id(self, sender_id: str) -> str | None:
        """Return the active session_id for this sender, if any."""
        return getattr(self, "_sessions", {}).get(sender_id)

    def set_session_id(self, sender_id: str, session_id: str) -> None:
        """Associate a session_id with a sender."""
        if not hasattr(self, "_sessions"):
            self._sessions: dict[str, str] = {}
        self._sessions[sender_id] = session_id

    def clear_session(self, sender_id: str) -> None:
        """Remove session tracking for a sender."""
        if hasattr(self, "_sessions"):
            self._sessions.pop(sender_id, None)

    # -- Interactive events --

    async def handle_pending_interaction(
        self, sender_id: str, interaction_type: str, data: dict
    ) -> str:
        """Handle an interactive event (clarification, plan approval, etc.).

        Returns the user's response text.
        """
        return ""

    # -- Local command routing --

    async def route_message(self, message: ChannelMessage) -> bool:
        """Handle local commands (slash commands, etc.).

        Return True if the message was handled locally and should not be
        forwarded to the agent.
        """
        return False
