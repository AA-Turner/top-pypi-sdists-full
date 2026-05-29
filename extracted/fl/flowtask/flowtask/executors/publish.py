# Copyright (C) 2018-present Jesus Lara
#
"""Publish (Redis Streams) job executor for the flowtask executor framework."""
from __future__ import annotations
import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Optional
from redis import asyncio as aioredis
from flowtask.executors.base import AbstractJobExecutor
from flowtask.executors.models import (
    ExecutorConfig,
    ExecutorType,
    ExecutionHandle,
    TaskResult,
)
from flowtask.executors.events import ExecutorLifecyclePublisher
from flowtask.executors.exceptions import ExecutorConnectionError
from flowtask.executors.registry import register_executor

# Redis Stream key where task dispatch entries are written
TASKS_STREAM_KEY = "FLOWTASK:TASKS:STREAM"
# PUB/SUB channel pattern for result notifications
RESULT_CHANNEL_PREFIX = "FLOWTASK:RESULT"


@register_executor("publish")
class PublishJobExecutor(AbstractJobExecutor):
    """Dispatches tasks by writing to a Redis Stream (XADD).

    A separate consumer-worker reads from ``FLOWTASK:TASKS:STREAM`` and
    executes the task.  For the ``run()`` mode the executor also subscribes
    to ``FLOWTASK:RESULT:{task_id}`` via PUB/SUB and waits for the result.

    Args:
        config: ExecutorConfig with ``type=PUBLISH``.
        **kwargs: Passed through to the base constructor.
    """

    def __init__(self, config: ExecutorConfig, **kwargs) -> None:
        super().__init__(config, **kwargs)
        self._publisher = ExecutorLifecyclePublisher()

    @classmethod
    def name(cls) -> str:
        """Return registry name.

        Returns:
            ``"publish"``
        """
        return "publish"

    async def _get_redis(self) -> aioredis.Redis:
        """Create an async Redis connection.

        Returns:
            An aioredis.Redis connection.

        Raises:
            ExecutorConnectionError: If Redis is unavailable.
        """
        from flowtask.conf import PUBSUB_REDIS  # lazy import to defer settings loading
        try:
            return await aioredis.from_url(
                PUBSUB_REDIS,
                decode_responses=True,
            )
        except Exception as exc:
            raise ExecutorConnectionError(
                f"PublishJobExecutor cannot connect to Redis: {exc}"
            ) from exc

    def _build_stream_entry(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs: Any,
    ) -> dict[str, str]:
        """Build the dict written to the Redis Stream.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Optional extra fields JSON-encoded into ``kwargs_json``.

        Returns:
            A flat dict of string → string suitable for XADD.
        """
        from flowtask.utils.json import json_encoder  # lazy import to defer Cython loading
        return {
            "program": program,
            "task": task,
            "task_id": task_id,
            "kwargs_json": json_encoder(kwargs) if kwargs else "{}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    async def dispatch(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> ExecutionHandle:
        """Write a task entry to the Redis Stream and return immediately.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Serialised into ``kwargs_json`` in the stream entry.

        Returns:
            An ExecutionHandle with the XADD stream entry ID.

        Raises:
            ExecutorConnectionError: If Redis is unavailable.
        """
        execution_id = task_id or str(uuid.uuid4())
        channel = f"FLOWTASK:EXEC:{execution_id}"

        await self._publisher.publish("dispatched", program, task, execution_id)

        entry = self._build_stream_entry(program, task, execution_id, **kwargs)

        redis = await self._get_redis()
        try:
            stream_id = await redis.xadd(TASKS_STREAM_KEY, entry)
            self.logger.info(
                "Task %s.%s written to stream %s (entry=%s)",
                program, task, TASKS_STREAM_KEY, stream_id,
            )
        except Exception as exc:
            self.logger.error(
                "PublishJobExecutor XADD failed for %s.%s: %s", program, task, exc
            )
            raise ExecutorConnectionError(
                f"XADD to {TASKS_STREAM_KEY} failed: {exc}"
            ) from exc
        finally:
            try:
                await redis.close()
            except Exception:
                pass
            try:
                await redis.connection_pool.disconnect()
            except Exception:
                pass

        return ExecutionHandle(
            executor_type=ExecutorType.PUBLISH,
            execution_id=execution_id,
            task_program=program,
            task_name=task,
            channel=channel,
        )

    async def run(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> TaskResult:
        """Write to the Redis Stream, then wait for the result via PUB/SUB.

        Subscribes to ``FLOWTASK:RESULT:{task_id}`` and blocks until a
        message arrives or ``config.timeout`` seconds elapse.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Serialised into ``kwargs_json`` in the stream entry.

        Returns:
            TaskResult with the consumer-worker's result, or a timeout failure.

        Raises:
            ExecutorConnectionError: If the initial Redis connection fails.
        """
        execution_id = task_id or str(uuid.uuid4())
        result_channel = f"{RESULT_CHANNEL_PREFIX}:{execution_id}"
        timeout = self._config.timeout

        await self._publisher.publish("started", program, task, execution_id)

        # Write task to stream
        entry = self._build_stream_entry(program, task, execution_id, **kwargs)
        redis_xadd = await self._get_redis()
        try:
            await redis_xadd.xadd(TASKS_STREAM_KEY, entry)
        except Exception as exc:
            raise ExecutorConnectionError(
                f"XADD to {TASKS_STREAM_KEY} failed: {exc}"
            ) from exc
        finally:
            try:
                await redis_xadd.close()
            except Exception:
                pass
            try:
                await redis_xadd.connection_pool.disconnect()
            except Exception:
                pass

        # Subscribe to result channel and wait
        redis_sub = await self._get_redis()
        pubsub = redis_sub.pubsub()
        try:
            await pubsub.subscribe(result_channel)
            self.logger.debug(
                "Subscribed to %s, waiting for result (timeout=%ss)",
                result_channel, timeout,
            )

            deadline = asyncio.get_running_loop().time() + timeout
            while True:
                remaining = deadline - asyncio.get_running_loop().time()
                if remaining <= 0:
                    await self._publisher.publish(
                        "failed", program, task, execution_id, error="timeout"
                    )
                    return TaskResult(
                        status="failed",
                        error=f"Timeout waiting for result after {timeout}s",
                        execution_id=execution_id,
                    )

                message = await asyncio.wait_for(
                    pubsub.get_message(ignore_subscribe_messages=True),
                    timeout=min(remaining, 1.0),
                )
                if message is not None and message.get("type") == "message":
                    data = message.get("data", "{}")
                    await self._publisher.publish(
                        "completed", program, task, execution_id
                    )
                    return TaskResult(
                        status="success",
                        result=data,
                        execution_id=execution_id,
                    )

        except asyncio.TimeoutError:
            await self._publisher.publish(
                "failed", program, task, execution_id, error="timeout"
            )
            return TaskResult(
                status="failed",
                error=f"Timeout waiting for result after {timeout}s",
                execution_id=execution_id,
            )
        except Exception as exc:
            self.logger.error(
                "PublishJobExecutor run failed for %s.%s: %s", program, task, exc
            )
            await self._publisher.publish(
                "failed", program, task, execution_id, error=str(exc)
            )
            return TaskResult(
                status="failed",
                error=str(exc),
                execution_id=execution_id,
            )
        finally:
            try:
                await pubsub.unsubscribe(result_channel)
                await pubsub.close()
            except Exception:
                pass
            try:
                await redis_sub.close()
            except Exception:
                pass
            try:
                await redis_sub.connection_pool.disconnect()
            except Exception:
                pass

    async def close(self) -> None:
        """Close the lifecycle publisher.

        Args: none.
        """
        await self._publisher.close()
