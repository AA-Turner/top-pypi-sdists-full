"""Thread-safe message queue for multiuser sessions.

This module provides a FIFO message queue that coordinates multiple users
sending messages while the agent processes them one at a time.
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Any

from .protocols import QueuedMessage, SharedEventType, AgentBusyError

log = logging.getLogger(__name__)


class SharedMessageQueue:
    """FIFO message queue for multiuser sessions.

    Features:
    - Thread-safe enqueueing from multiple users
    - Single dequeue by agent runner (one message at a time)
    - Priority support for urgent messages
    - Optional persistence to survive restarts
    - Async waiting for new messages

    Usage:
        queue = SharedMessageQueue(session_id)

        # User sends message
        msg = await queue.enqueue(user_id, "Hello agent")

        # Agent runner processes
        while True:
            msg = await queue.dequeue()
            if msg:
                response = agent.run(msg.content)
                await queue.complete(msg.id)
    """

    def __init__(
        self,
        session_id: str,
        storage_path: Optional[Path] = None,
        on_event: Optional[Callable[[str, dict], None]] = None,
    ):
        """Initialize the message queue.

        Args:
            session_id: Session this queue belongs to
            storage_path: Optional path for persistence
            on_event: Optional callback for queue events
        """
        self._session_id = session_id
        self._storage_path = storage_path
        self._on_event = on_event

        self._queue: list[QueuedMessage] = []
        self._lock = asyncio.Lock()
        self._agent_busy = False
        self._current_message_id: Optional[str] = None
        self._current_user_id: Optional[str] = None
        self._waiters: list[asyncio.Future] = []

        # Load from storage if exists
        if storage_path and storage_path.exists():
            self._load()

    async def enqueue(
        self,
        user_id: str,
        content: str,
        images: Optional[list[dict]] = None,
        priority: int = 0,
    ) -> QueuedMessage:
        """Add a message to the queue.

        Thread-safe, can be called concurrently from multiple users.

        Args:
            user_id: ID of the user sending the message
            content: Message content
            images: Optional list of image dicts
            priority: Priority level (higher = more urgent)

        Returns:
            The queued message with assigned ID and position
        """
        async with self._lock:
            message = QueuedMessage(
                id=str(uuid.uuid4()),
                user_id=user_id,
                content=content,
                images=images or [],
                queued_at=datetime.utcnow().isoformat(),
                priority=priority,
            )

            # Insert by priority (higher first), then by time
            inserted = False
            for i, existing in enumerate(self._queue):
                if message.priority > existing.priority:
                    self._queue.insert(i, message)
                    inserted = True
                    break
            if not inserted:
                self._queue.append(message)

            # Persist if storage configured
            await self._persist()

            # Emit event
            self._emit_event(SharedEventType.MESSAGE_QUEUED.value, {
                "message_id": message.id,
                "user_id": user_id,
                "queue_position": self._get_position_unlocked(message.id),
                "queue_length": len(self._queue),
            })

            # Wake up any waiting dequeue operations
            for waiter in self._waiters:
                if not waiter.done():
                    waiter.set_result(True)
            self._waiters.clear()

            log.debug(f"Message {message.id} queued at position {self._get_position_unlocked(message.id)}")
            return message

    async def dequeue(
        self,
        timeout: Optional[float] = None,
    ) -> Optional[QueuedMessage]:
        """Get next message from queue (agent runner only).

        Blocks until a message is available or timeout.
        Only one message can be dequeued at a time - must call complete()
        before dequeuing the next message.

        Args:
            timeout: Optional timeout in seconds (None = no wait, 0 = wait forever)

        Returns:
            Next message, or None if timeout/empty

        Raises:
            AgentBusyError: If agent is already processing a message
        """
        async with self._lock:
            if self._agent_busy:
                raise AgentBusyError(
                    f"Agent already processing message {self._current_message_id}"
                )

            if self._queue:
                return await self._dequeue_unlocked()

            if timeout is None:
                # No wait - return immediately
                return None

            # Create waiter for new messages
            loop = asyncio.get_event_loop()
            waiter = loop.create_future()
            self._waiters.append(waiter)

        # Wait outside lock
        try:
            if timeout > 0:
                await asyncio.wait_for(waiter, timeout=timeout)
            else:
                await waiter
        except asyncio.TimeoutError:
            return None
        except asyncio.CancelledError:
            return None

        # Retry dequeue (message should be available now)
        async with self._lock:
            if self._agent_busy:
                return None
            if self._queue:
                return await self._dequeue_unlocked()
            return None

    async def _dequeue_unlocked(self) -> QueuedMessage:
        """Dequeue message (must hold lock)."""
        message = self._queue.pop(0)
        self._agent_busy = True
        self._current_message_id = message.id
        self._current_user_id = message.user_id

        await self._persist()

        self._emit_event(SharedEventType.MESSAGE_DEQUEUED.value, {
            "message_id": message.id,
            "user_id": message.user_id,
            "remaining_in_queue": len(self._queue),
        })

        log.debug(f"Message {message.id} dequeued, agent now busy")
        return message

    async def complete(self, message_id: str) -> None:
        """Mark current message as completed (agent runner only).

        Must be called after processing a dequeued message before
        another message can be dequeued.

        Args:
            message_id: ID of the completed message

        Raises:
            ValueError: If message_id doesn't match current message
        """
        async with self._lock:
            if self._current_message_id != message_id:
                raise ValueError(
                    f"Message {message_id} is not current "
                    f"(current: {self._current_message_id})"
                )

            self._agent_busy = False
            completed_user = self._current_user_id
            self._current_message_id = None
            self._current_user_id = None

            await self._persist()

            self._emit_event(SharedEventType.MESSAGE_PROCESSING.value, {
                "message_id": message_id,
                "user_id": completed_user,
                "status": "completed",
                "remaining_in_queue": len(self._queue),
            })

            log.debug(f"Message {message_id} completed, agent now idle")

    async def cancel_current(self) -> Optional[QueuedMessage]:
        """Cancel the current message being processed.

        Returns the message so it can be re-queued if desired.

        Returns:
            The cancelled message, or None if none was being processed
        """
        async with self._lock:
            if not self._agent_busy:
                return None

            # Reconstruct the message (we only have ID)
            message = QueuedMessage(
                id=self._current_message_id,
                user_id=self._current_user_id or "",
                content="",  # Content not preserved
                queued_at=datetime.utcnow().isoformat(),
            )

            self._agent_busy = False
            self._current_message_id = None
            self._current_user_id = None

            await self._persist()

            log.debug(f"Message {message.id} cancelled")
            return message

    @property
    def is_agent_busy(self) -> bool:
        """Check if agent is processing a message."""
        return self._agent_busy

    @property
    def current_message_id(self) -> Optional[str]:
        """Get ID of message currently being processed."""
        return self._current_message_id

    @property
    def current_user_id(self) -> Optional[str]:
        """Get ID of user whose message is being processed."""
        return self._current_user_id

    def get_queue_position(self, message_id: str) -> Optional[int]:
        """Get position of a message in queue (0-indexed)."""
        for i, msg in enumerate(self._queue):
            if msg.id == message_id:
                return i
        return None

    def _get_position_unlocked(self, message_id: str) -> Optional[int]:
        """Get position without lock (internal use)."""
        for i, msg in enumerate(self._queue):
            if msg.id == message_id:
                return i
        return None

    def __len__(self) -> int:
        """Get number of messages in queue."""
        return len(self._queue)

    def get_state(self) -> dict[str, Any]:
        """Get queue state for serialization."""
        return {
            "queue": [m.to_dict() for m in self._queue],
            "agent_busy": self._agent_busy,
            "current_message_id": self._current_message_id,
            "current_user_id": self._current_user_id,
        }

    def restore_state(self, state: dict[str, Any]) -> None:
        """Restore queue state from serialization."""
        self._queue = [QueuedMessage.from_dict(m) for m in state.get("queue", [])]
        self._agent_busy = state.get("agent_busy", False)
        self._current_message_id = state.get("current_message_id")
        self._current_user_id = state.get("current_user_id")

    async def _persist(self) -> None:
        """Persist queue state to storage."""
        if not self._storage_path:
            return

        try:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            state = self.get_state()
            self._storage_path.write_text(json.dumps(state, indent=2))
        except Exception as e:
            log.warning(f"Failed to persist queue: {e}")

    def _load(self) -> None:
        """Load queue state from storage."""
        if not self._storage_path or not self._storage_path.exists():
            return

        try:
            state = json.loads(self._storage_path.read_text())
            self.restore_state(state)
            log.debug(f"Loaded queue with {len(self._queue)} messages")
        except Exception as e:
            log.warning(f"Failed to load queue: {e}")

    def _emit_event(self, event_type: str, data: dict) -> None:
        """Emit a queue event."""
        if self._on_event:
            try:
                self._on_event(event_type, data)
            except Exception as e:
                log.warning(f"Error in queue event handler: {e}")


class SyncedMessageQueue(SharedMessageQueue):
    """Message queue that dispatches webhooks on state changes.

    This extends SharedMessageQueue to fire webhooks when the
    queue state changes, allowing consumers to persist to
    durable storage.
    """

    def __init__(
        self,
        session_id: str,
        storage_path: Optional[Path] = None,
        on_event: Optional[Callable[[str, dict], None]] = None,
    ):
        """Initialize synced queue.

        Args:
            session_id: Session this queue belongs to
            storage_path: Optional local storage path
            on_event: Optional callback for queue events
        """
        super().__init__(session_id, storage_path, on_event)

    async def _persist(self) -> None:
        """Persist to local storage and dispatch webhook."""
        # Local persistence
        await super()._persist()

        # Dispatch webhook for consumer persistence
        try:
            from .webhooks import get_webhook_registry
            webhooks = get_webhook_registry()
            await webhooks.dispatch("session.queue_updated", {
                "session_id": self._session_id,
                "message_queue": [m.to_dict() for m in self._queue],
            })
        except Exception as e:
            log.warning(f"Failed to dispatch queue webhook: {e}")
