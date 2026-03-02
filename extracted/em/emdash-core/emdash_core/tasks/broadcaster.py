"""Event broadcasting for task updates."""

import asyncio
from typing import Callable, Awaitable
from datetime import datetime

from .models import TaskEvent


# Type alias for event handlers
EventHandler = Callable[[TaskEvent], Awaitable[None]]


class TaskEventBroadcaster:
    """
    Broadcasts task events to registered handlers.

    This provides a pub/sub mechanism for task updates, allowing components
    like TaskWaiter to react to task completions without tight coupling.

    Usage:
        # Register a handler
        async def my_handler(event: TaskEvent):
            print(f"Task {event.task_id} {event.type}")

        TaskEventBroadcaster.subscribe(my_handler)

        # Publish an event
        await TaskEventBroadcaster.publish(TaskEvent(
            type="task_completed",
            task_list_id="my-list",
            task_id="task-123",
        ))
    """

    _handlers: list[EventHandler] = []
    _lock = asyncio.Lock()

    # Event type constants
    TASK_ADDED = "task_added"
    TASK_UPDATED = "task_updated"
    TASK_COMPLETED = "task_completed"
    TASK_CLAIMED = "task_claimed"
    TASK_RELEASED = "task_released"
    TASK_DELETED = "task_deleted"
    TASK_LIST_UPDATED = "task_list_updated"

    @classmethod
    def subscribe(cls, handler: EventHandler) -> None:
        """
        Register an event handler.

        Handlers are called in order of registration for each event.
        """
        if handler not in cls._handlers:
            cls._handlers.append(handler)

    @classmethod
    def unsubscribe(cls, handler: EventHandler) -> None:
        """Remove an event handler."""
        if handler in cls._handlers:
            cls._handlers.remove(handler)

    @classmethod
    async def publish(cls, event: TaskEvent) -> None:
        """
        Broadcast an event to all registered handlers.

        Handlers are called concurrently. Errors in one handler don't
        prevent others from being called.
        """
        if not cls._handlers:
            return

        # Call all handlers concurrently
        tasks = []
        for handler in cls._handlers:
            tasks.append(asyncio.create_task(cls._safe_call(handler, event)))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    @classmethod
    async def _safe_call(cls, handler: EventHandler, event: TaskEvent) -> None:
        """Call a handler safely, catching exceptions."""
        try:
            await handler(event)
        except Exception:
            # Log but don't propagate - one bad handler shouldn't break others
            pass

    @classmethod
    def publish_sync(cls, event: TaskEvent) -> None:
        """
        Synchronous publish for use from non-async contexts.

        This schedules the publish to run in the event loop if one exists,
        otherwise creates a new loop to run it.
        """
        try:
            loop = asyncio.get_running_loop()
            # We're in an async context - schedule it
            asyncio.create_task(cls.publish(event))
        except RuntimeError:
            # No running loop - create one to publish
            try:
                asyncio.run(cls.publish(event))
            except RuntimeError:
                # Can't create event loop in this thread - skip
                pass

    @classmethod
    def clear_handlers(cls) -> None:
        """Remove all handlers (mainly for testing)."""
        cls._handlers.clear()

    @classmethod
    def create_event(
        cls,
        event_type: str,
        task_list_id: str,
        task_id: str | None = None,
        **data,
    ) -> TaskEvent:
        """Helper to create a TaskEvent with common fields."""
        return TaskEvent(
            type=event_type,
            task_list_id=task_list_id,
            task_id=task_id,
            data=data,
            timestamp=datetime.utcnow().isoformat(),
        )
