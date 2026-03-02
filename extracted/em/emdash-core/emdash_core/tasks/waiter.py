"""Async task waiter for blocking until tasks complete."""

import asyncio
import time
from typing import Optional

from .models import TaskEvent


class TaskWaiter:
    """
    Allows agents to physically block until a task completes.
    Uses asyncio Futures to suspend execution without CPU usage.

    Now includes TTL-based cleanup to prevent memory leaks from
    accumulating futures for completed tasks.

    Usage:
        # Wait for a single task
        completed = await TaskWaiter.wait_for_task("task-123", timeout=300)

        # Wait for any of multiple tasks
        completed_id = await TaskWaiter.wait_for_any(["task-1", "task-2"], timeout=300)

        # Notify waiters when task completes (called by broadcaster)
        await TaskWaiter.notify_completion("task-123")

        # Clean up old futures
        await TaskWaiter.cleanup_stale(max_age_seconds=3600)
    """

    # Shared completion futures: task_id -> (Future, created_at timestamp)
    _completion_futures: dict[str, tuple[asyncio.Future, float]] = {}
    _lock = asyncio.Lock()

    # Default TTL for futures (1 hour)
    DEFAULT_TTL_SECONDS = 3600

    @classmethod
    async def wait_for_task(
        cls,
        task_id: str,
        timeout: Optional[float] = None,
    ) -> bool:
        """
        Block until task completes.

        Args:
            task_id: Task to wait for
            timeout: Max seconds to wait (None = forever)

        Returns:
            True if task completed, False if timeout
        """
        async with cls._lock:
            if task_id not in cls._completion_futures:
                loop = asyncio.get_event_loop()
                cls._completion_futures[task_id] = (
                    loop.create_future(),
                    time.time(),
                )

        future, _ = cls._completion_futures[task_id]

        # If already done, return immediately
        if future.done():
            return True

        try:
            if timeout:
                await asyncio.wait_for(asyncio.shield(future), timeout=timeout)
            else:
                await future
            return True
        except asyncio.TimeoutError:
            return False

    @classmethod
    async def notify_completion(cls, task_id: str) -> None:
        """
        Called when a task completes - wakes up all waiting agents.
        """
        async with cls._lock:
            if task_id in cls._completion_futures:
                future, _ = cls._completion_futures[task_id]
                if not future.done():
                    future.set_result(True)
                # Create new future for any future waiters (with fresh timestamp)
                loop = asyncio.get_event_loop()
                cls._completion_futures[task_id] = (
                    loop.create_future(),
                    time.time(),
                )
                # Mark the new future as done since task is already completed
                cls._completion_futures[task_id][0].set_result(True)

    @classmethod
    async def wait_for_any(
        cls,
        task_ids: list[str],
        timeout: Optional[float] = None,
    ) -> str | None:
        """
        Wait for ANY of the given tasks to complete.
        Returns the task_id that completed, or None if timeout.
        """
        if not task_ids:
            return None

        async with cls._lock:
            loop = asyncio.get_event_loop()
            for task_id in task_ids:
                if task_id not in cls._completion_futures:
                    cls._completion_futures[task_id] = (
                        loop.create_future(),
                        time.time(),
                    )

        futures = {
            asyncio.ensure_future(cls._wait_single(task_id)): task_id
            for task_id in task_ids
        }

        try:
            done, pending = await asyncio.wait(
                futures.keys(),
                timeout=timeout,
                return_when=asyncio.FIRST_COMPLETED,
            )

            # Cancel pending tasks
            for task in pending:
                task.cancel()

            if done:
                # Find which task completed
                for task in done:
                    return futures[task]

            return None
        except asyncio.CancelledError:
            # Cancel all pending
            for task in futures.keys():
                task.cancel()
            raise

    @classmethod
    async def _wait_single(cls, task_id: str) -> str:
        """Helper to wait for a single task and return its ID."""
        await cls.wait_for_task(task_id)
        return task_id

    @classmethod
    async def is_waiting(cls, task_id: str) -> bool:
        """Check if anyone is waiting for a task."""
        async with cls._lock:
            if task_id not in cls._completion_futures:
                return False
            future, _ = cls._completion_futures[task_id]
            # If there's an undone future, someone might be waiting
            return not future.done()

    @classmethod
    async def remove_task(cls, task_id: str) -> bool:
        """
        Remove a task's future from tracking.

        Call this when a task is deleted to free memory.
        Returns True if the task was being tracked, False otherwise.
        """
        async with cls._lock:
            if task_id in cls._completion_futures:
                future, _ = cls._completion_futures[task_id]
                if not future.done():
                    # Cancel any waiters
                    future.cancel()
                del cls._completion_futures[task_id]
                return True
            return False

    @classmethod
    async def cleanup_stale(
        cls,
        max_age_seconds: float | None = None,
    ) -> int:
        """
        Remove futures older than max_age_seconds that are already done.

        This prevents memory leaks from accumulating completed task futures.

        Args:
            max_age_seconds: Max age for futures. Defaults to DEFAULT_TTL_SECONDS.

        Returns:
            Number of futures removed.
        """
        if max_age_seconds is None:
            max_age_seconds = cls.DEFAULT_TTL_SECONDS

        cutoff = time.time() - max_age_seconds
        removed = 0

        async with cls._lock:
            to_remove = []
            for task_id, (future, created_at) in cls._completion_futures.items():
                # Only remove if done AND older than TTL
                if future.done() and created_at < cutoff:
                    to_remove.append(task_id)

            for task_id in to_remove:
                del cls._completion_futures[task_id]
                removed += 1

        return removed

    @classmethod
    async def get_stats(cls) -> dict:
        """
        Get statistics about tracked futures.

        Returns dict with:
        - total: Total futures tracked
        - waiting: Futures with active waiters (not done)
        - completed: Futures that are done
        - oldest_age_seconds: Age of oldest future
        """
        async with cls._lock:
            total = len(cls._completion_futures)
            waiting = 0
            completed = 0
            oldest_age = 0.0
            now = time.time()

            for task_id, (future, created_at) in cls._completion_futures.items():
                age = now - created_at
                if age > oldest_age:
                    oldest_age = age
                if future.done():
                    completed += 1
                else:
                    waiting += 1

            return {
                "total": total,
                "waiting": waiting,
                "completed": completed,
                "oldest_age_seconds": oldest_age,
            }

    @classmethod
    async def clear(cls) -> None:
        """Clear all waiting futures (for testing)."""
        async with cls._lock:
            for task_id, (future, _) in cls._completion_futures.items():
                if not future.done():
                    future.cancel()
            cls._completion_futures.clear()


# Event handler to auto-notify on task completion
async def _handle_task_event(event: TaskEvent) -> None:
    """Handle task events from the broadcaster."""
    if event.type == "task_completed" and event.task_id:
        await TaskWaiter.notify_completion(event.task_id)
    elif event.type == "task_deleted" and event.task_id:
        await TaskWaiter.remove_task(event.task_id)


def register_with_broadcaster() -> None:
    """Register TaskWaiter's event handler with the broadcaster."""
    from .broadcaster import TaskEventBroadcaster

    TaskEventBroadcaster.subscribe(_handle_task_event)


def unregister_from_broadcaster() -> None:
    """Unregister TaskWaiter's event handler from the broadcaster."""
    from .broadcaster import TaskEventBroadcaster

    TaskEventBroadcaster.unsubscribe(_handle_task_event)
