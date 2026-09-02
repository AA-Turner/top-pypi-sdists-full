# Copyright (C) 2018-present Jesus Lara
#
"""Executor lifecycle event publishing via Redis PUB/SUB."""
from __future__ import annotations
import logging
from datetime import datetime, timezone
from typing import Any
from redis import asyncio as aioredis


class ExecutorLifecyclePublisher:
    """Publishes executor lifecycle events to Redis PUB/SUB.

    Each execution's events are published to the channel
    ``FLOWTASK:EXEC:{task_id}``.  If Redis is unavailable the publish
    is silently dropped — the executor should never crash due to an
    event-publishing failure.

    Example::

        publisher = ExecutorLifecyclePublisher()
        await publisher.publish("dispatched", "my_program", "my_task", "uuid-123")
        await publisher.close()
    """

    CHANNEL_PREFIX = "FLOWTASK:EXEC"

    def __init__(self) -> None:
        self.logger = logging.getLogger("FlowTask.ExecutorLifecycle")

    async def publish(
        self,
        event_type: str,
        task_program: str,
        task_name: str,
        task_id: str,
        **data: Any,
    ) -> None:
        """Publish a lifecycle event to the task's PUB/SUB channel.

        Args:
            event_type: One of 'dispatched', 'started', 'completed', 'failed'.
            task_program: The program slug.
            task_name: The task identifier within the program.
            task_id: The unique execution UUID.
            **data: Optional extra key/value pairs included in the event payload.
        """
        channel = f"{self.CHANNEL_PREFIX}:{task_id}"
        msg: dict[str, Any] = {
            "event_type": event_type,
            "task_program": task_program,
            "task_name": task_name,
            "task_id": task_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if data:
            msg.update(data)

        from flowtask.utils.json import json_encoder  # lazy import to defer Cython type loading
        message = json_encoder(msg)

        from flowtask.conf import PUBSUB_REDIS  # lazy import to avoid circular settings chain
        redis = None
        try:
            redis = await aioredis.from_url(
                PUBSUB_REDIS,
                decode_responses=True,
            )
            await redis.publish(channel, message)
            self.logger.debug(
                "Lifecycle event '%s' published for task_id=%s", event_type, task_id
            )
        except Exception as exc:
            self.logger.warning(
                "Lifecycle event publish failed (event=%s, task_id=%s): %s",
                event_type,
                task_id,
                exc,
            )
        finally:
            if redis is not None:
                try:
                    await redis.close()
                except Exception:
                    pass
                try:
                    await redis.connection_pool.disconnect()
                except Exception:
                    pass

    async def close(self) -> None:
        """No-op — connections are closed after each publish.

        Provided for interface consistency with executors that hold
        long-lived connections.
        """
