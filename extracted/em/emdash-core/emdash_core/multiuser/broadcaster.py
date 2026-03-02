"""Event broadcaster for multiuser sessions.

This module provides the SharedEventBroadcaster which wraps the existing
AgentEventEmitter to fan out events to all connected participants.
"""

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from ..agent.events import AgentEvent, EventHandler
from ..sse.stream import EventType  # Use SSE EventType which has multiuser events
from .protocols import (
    SharedEvent,
    SharedEventHandler,
    SharedEventType,
)
from .webhooks import get_webhook_registry

log = logging.getLogger(__name__)


class SharedEventBroadcaster(EventHandler):
    """Broadcasts agent events to multiple participants.

    This class acts as a handler for the existing AgentEventEmitter and
    fans out events to all connected participants via their individual
    handlers (typically SSE connections).

    It also optionally syncs events to a remote SyncProvider for
    multi-machine synchronization.

    Usage:
        broadcaster = SharedEventBroadcaster(session_id)

        # Add participant handlers
        broadcaster.add_handler(user_a_sse_handler)
        broadcaster.add_handler(user_b_sse_handler)

        # Wire to agent emitter
        emitter = AgentEventEmitter()
        emitter.add_handler(broadcaster)

        # Events now fan out to all participants
        emitter.emit(EventType.TOOL_START, {...})
    """

    def __init__(
        self,
        session_id: str,
    ):
        """Initialize the broadcaster.

        Args:
            session_id: Session this broadcaster belongs to
        """
        self._session_id = session_id
        self._handlers: list[SharedEventHandler] = []
        self._async_handlers: list[Callable[[SharedEvent], Any]] = []
        self._sequence = 0
        self._lock = asyncio.Lock()

        # Track which user's message is being processed
        self._current_user_id: Optional[str] = None

    def set_current_user(self, user_id: Optional[str]) -> None:
        """Set the user whose message is currently being processed.

        This is used to attribute events to the correct user.

        Args:
            user_id: User ID or None if idle
        """
        self._current_user_id = user_id

    def handle(self, event: AgentEvent) -> None:
        """Handle an event from AgentEventEmitter (EventHandler protocol).

        This is called by the AgentEventEmitter for each emitted event.
        We convert it to a SharedEvent and fan out to all handlers.

        Args:
            event: The agent event to broadcast
        """
        # Convert to SharedEvent with sequence number
        shared_event = self._to_shared_event(event)

        # Fan out to all local handlers (synchronous)
        for handler in self._handlers:
            try:
                handler.handle(shared_event)
            except Exception as e:
                log.warning(f"Handler error: {e}")

        # Fan out to async handlers
        for handler in self._async_handlers:
            try:
                # Schedule async handler
                asyncio.create_task(self._call_async_handler(handler, shared_event))
            except Exception as e:
                log.warning(f"Async handler scheduling error: {e}")

        # Dispatch to webhook for persistence
        asyncio.create_task(self._dispatch_event_webhook(shared_event))

    async def _call_async_handler(
        self,
        handler: Callable[[SharedEvent], Any],
        event: SharedEvent,
    ) -> None:
        """Call an async handler safely."""
        try:
            result = handler(event)
            if asyncio.iscoroutine(result):
                await result
        except Exception as e:
            log.warning(f"Async handler error: {e}")

    def _to_shared_event(self, event: AgentEvent) -> SharedEvent:
        """Convert AgentEvent to SharedEvent."""
        self._sequence += 1
        return SharedEvent(
            id=f"{self._session_id}_{self._sequence}_{uuid.uuid4().hex[:8]}",
            session_id=self._session_id,
            event_type=event.type.value,
            data=event.data,
            timestamp=event.timestamp.isoformat(),
            source_user_id=self._current_user_id,
            sequence=self._sequence,
        )

    def add_handler(self, handler: SharedEventHandler) -> None:
        """Add a synchronous handler for shared events.

        Args:
            handler: Handler implementing SharedEventHandler protocol
        """
        if handler not in self._handlers:
            self._handlers.append(handler)
            log.debug(f"Added handler, total: {len(self._handlers)}")

    def remove_handler(self, handler: SharedEventHandler) -> None:
        """Remove a handler.

        Args:
            handler: Handler to remove
        """
        if handler in self._handlers:
            self._handlers.remove(handler)
            log.debug(f"Removed handler, total: {len(self._handlers)}")

    def add_async_handler(
        self,
        handler: Callable[[SharedEvent], Any],
    ) -> None:
        """Add an async handler for shared events.

        Args:
            handler: Async callable that receives SharedEvent
        """
        if handler not in self._async_handlers:
            self._async_handlers.append(handler)

    def remove_async_handler(
        self,
        handler: Callable[[SharedEvent], Any],
    ) -> None:
        """Remove an async handler.

        Args:
            handler: Handler to remove
        """
        if handler in self._async_handlers:
            self._async_handlers.remove(handler)

    async def broadcast(
        self,
        event_type: str,
        data: dict[str, Any],
        source_user_id: Optional[str] = None,
    ) -> SharedEvent:
        """Manually broadcast a shared event.

        Use this for multiuser-specific events (participant joined, etc.)
        that don't come from the AgentEventEmitter.

        Args:
            event_type: Event type (SharedEventType value or custom)
            data: Event data payload
            source_user_id: Optional user who triggered the event

        Returns:
            The created SharedEvent
        """
        self._sequence += 1
        event = SharedEvent(
            id=f"{self._session_id}_{self._sequence}_{uuid.uuid4().hex[:8]}",
            session_id=self._session_id,
            event_type=event_type,
            data=data,
            timestamp=datetime.now(timezone.utc).isoformat(),
            source_user_id=source_user_id,
            sequence=self._sequence,
        )

        log.info(f"[BROADCASTER] Broadcasting '{event_type}' to {len(self._handlers)} sync handlers + {len(self._async_handlers)} async handlers")

        # Fan out to handlers
        for i, handler in enumerate(self._handlers):
            try:
                log.debug(f"[BROADCASTER] Calling sync handler {i}: {type(handler).__name__}")
                handler.handle(event)
                log.debug(f"[BROADCASTER] Sync handler {i} completed")
            except Exception as e:
                log.warning(f"Handler error: {e}", exc_info=True)

        for handler in self._async_handlers:
            try:
                asyncio.create_task(self._call_async_handler(handler, event))
            except Exception as e:
                log.warning(f"Async handler error: {e}")

        # Dispatch to webhook for persistence
        await self._dispatch_event_webhook(event)

        return event

    async def broadcast_participant_joined(
        self,
        user_id: str,
        display_name: str,
    ) -> SharedEvent:
        """Broadcast that a participant joined.

        Args:
            user_id: Joining user's ID
            display_name: Joining user's display name

        Returns:
            The broadcast event
        """
        return await self.broadcast(
            SharedEventType.PARTICIPANT_JOINED.value,
            {
                "user_id": user_id,
                "display_name": display_name,
            },
            source_user_id=user_id,
        )

    async def broadcast_participant_left(
        self,
        user_id: str,
        display_name: str,
    ) -> SharedEvent:
        """Broadcast that a participant left.

        Args:
            user_id: Leaving user's ID
            display_name: Leaving user's display name

        Returns:
            The broadcast event
        """
        return await self.broadcast(
            SharedEventType.PARTICIPANT_LEFT.value,
            {
                "user_id": user_id,
                "display_name": display_name,
            },
            source_user_id=user_id,
        )

    async def broadcast_queue_update(
        self,
        queue_length: int,
        current_message_id: Optional[str] = None,
        current_user_id: Optional[str] = None,
    ) -> SharedEvent:
        """Broadcast queue status update.

        Args:
            queue_length: Number of messages in queue
            current_message_id: ID of message being processed
            current_user_id: ID of user whose message is being processed

        Returns:
            The broadcast event
        """
        return await self.broadcast(
            SharedEventType.QUEUE_UPDATED.value,
            {
                "queue_length": queue_length,
                "current_message_id": current_message_id,
                "current_user_id": current_user_id,
            },
        )

    async def broadcast_state_change(
        self,
        old_state: str,
        new_state: str,
    ) -> SharedEvent:
        """Broadcast session state change.

        Args:
            old_state: Previous state
            new_state: New state

        Returns:
            The broadcast event
        """
        return await self.broadcast(
            SharedEventType.STATE_CHANGED.value,
            {
                "old_state": old_state,
                "new_state": new_state,
            },
        )

    async def _dispatch_event_webhook(self, event: SharedEvent) -> None:
        """Dispatch event to webhook registry for persistence by consumer."""
        try:
            webhooks = get_webhook_registry()
            await webhooks.dispatch("event.pushed", {
                "session_id": self._session_id,
                "event": event.to_dict() if hasattr(event, 'to_dict') else {
                    "id": event.id,
                    "session_id": event.session_id,
                    "event_type": event.event_type,
                    "data": event.data,
                    "timestamp": event.timestamp,
                    "source_user_id": event.source_user_id,
                    "sequence": event.sequence,
                },
            })
        except Exception as e:
            log.warning(f"Failed to dispatch event webhook: {e}")

    @property
    def handler_count(self) -> int:
        """Get number of registered handlers."""
        return len(self._handlers) + len(self._async_handlers)


class SSESharedEventHandler(SharedEventHandler):
    """Adapter to send SharedEvents to an SSE handler.

    This bridges SharedEventBroadcaster with the existing SSEHandler
    infrastructure, converting SharedEvents back to a format the
    SSE handler understands.
    """

    def __init__(self, sse_handler: Any):  # SSEHandler, avoid circular import
        """Initialize with an SSE handler.

        Args:
            sse_handler: The SSEHandler to send events to
        """
        self._sse_handler = sse_handler

    def handle(self, event: SharedEvent) -> None:
        """Handle a shared event by sending to SSE.

        Args:
            event: The shared event to send
        """
        # Convert SharedEvent to format SSEHandler expects
        # The SSEHandler.emit() takes EventType and data
        try:
            # Try to map back to EventType
            event_type = EventType(event.event_type)
        except ValueError:
            # For custom multiuser events, use the string directly
            # We'll need to handle these specially
            log.debug(f"[SSE-HANDLER] Custom event type: {event.event_type}")
            event_type = EventType.PROGRESS

        # Add multiuser metadata to the event data
        # Also include the original event type for custom events
        # IMPORTANT: Include timestamp for proper message ordering across clients
        data = {
            **event.data,
            "_shared_event_id": event.id,
            "_source_user_id": event.source_user_id,
            "_sequence": event.sequence,
            "_timestamp": event.timestamp,  # For chronological ordering
            "type": event.event_type,  # Include original type for custom events
        }

        log.debug(f"[SSE-HANDLER] Emitting: {event_type.value} with source_user={event.source_user_id}")
        self._sse_handler.emit(event_type, data)


class RemoteEventReceiver:
    """Receives events from remote SyncProvider and forwards to broadcaster.

    This handles the reverse direction - events coming from other machines
    via the SyncProvider subscription.
    """

    def __init__(
        self,
        broadcaster: SharedEventBroadcaster,
        local_machine_id: str,
    ):
        """Initialize receiver.

        Args:
            broadcaster: Broadcaster to forward events to
            local_machine_id: ID of this machine (to avoid echo)
        """
        self._broadcaster = broadcaster
        self._local_machine_id = local_machine_id
        self._seen_event_ids: set[str] = set()
        self._max_seen = 1000  # Limit memory usage

    async def handle_remote_event(self, event: SharedEvent) -> None:
        """Handle an event received from remote.

        Args:
            event: Event from remote SyncProvider
        """
        # Deduplicate
        if event.id in self._seen_event_ids:
            return

        self._seen_event_ids.add(event.id)

        # Trim seen set if too large
        if len(self._seen_event_ids) > self._max_seen:
            # Remove oldest (roughly - sets aren't ordered)
            to_remove = list(self._seen_event_ids)[:self._max_seen // 2]
            for eid in to_remove:
                self._seen_event_ids.discard(eid)

        # Skip events from this machine (already handled locally)
        if event.data.get("_source_machine") == self._local_machine_id:
            return

        # Forward to local handlers
        for handler in self._broadcaster._handlers:
            try:
                handler.handle(event)
            except Exception as e:
                log.warning(f"Handler error for remote event: {e}")
