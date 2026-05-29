# Copyright (C) 2018-present Jesus Lara
#
"""Qworker job executor — dispatches tasks through the qw worker queue."""
from __future__ import annotations
import asyncio
import uuid
from typing import Any, Optional
from flowtask.executors.base import AbstractJobExecutor
from flowtask.executors.models import (
    ExecutorConfig,
    ExecutorType,
    ExecutionHandle,
    TaskResult,
)
from flowtask.executors.events import ExecutorLifecyclePublisher
from flowtask.executors.exceptions import ExecutorError
from flowtask.executors.registry import register_executor


@register_executor("qworker")
class QworkerJobExecutor(AbstractJobExecutor):
    """Dispatches tasks to the qw worker queue via QClient.

    This is the replacement for the ``queued=True`` / ``no_worker=False``
    code path that existed in all 4 dispatch sites.

    Priority routing:
    - ``"pub"`` → ``QClient.publish()``
    - ``"high"`` → ``QClient(worker_list=WORKER_HIGH_LIST).queue()``
    - ``"low"``/``"default"`` → ``QClient(worker_list=WORKER_LIST).queue()``
    - any key in ``WORKERS_LIST`` → ``QClient(worker_list=WORKERS_LIST[key]).queue()``
    - ``"direct"`` → ``QClient.run()`` (waits for result)

    QClient and TaskWrapper are lazy-imported to avoid loading heavy
    transitive dependencies (aiogram, etc.) at module import time.

    Args:
        config: ExecutorConfig with ``type=QWORKER`` and optional ``priority``.
        **kwargs: Passed through to the base constructor.
    """

    def __init__(self, config: ExecutorConfig, **kwargs) -> None:
        super().__init__(config, **kwargs)
        self._publisher = ExecutorLifecyclePublisher()

    @classmethod
    def name(cls) -> str:
        """Return registry name.

        Returns:
            ``"qworker"``
        """
        return "qworker"

    def _make_wrapper(
        self,
        program: str,
        task: str,
        execution_id: str,
        queued: bool = True,
        **kwargs,
    ):
        """Create a TaskWrapper for queue dispatch.

        Args:
            program: Program slug.
            task: Task identifier.
            execution_id: UUID used as the task identity inside the wrapper.
            queued: Whether this is a queued (fire-and-forget) dispatch.
            **kwargs: Forwarded to the TaskWrapper constructor.

        Returns:
            A TaskWrapper instance ready for dispatch.
        """
        from qw.wrappers import TaskWrapper  # lazy import
        wrapper = TaskWrapper(
            program=program,
            task=task,
            task_id=execution_id,
            ignore_results=True,
            **kwargs,
        )
        wrapper.queued = queued
        return wrapper

    def _get_client(self, priority: Optional[str] = None):
        """Return a QClient for the given priority.

        Args:
            priority: Queue priority key or ``None`` for default.

        Returns:
            A configured QClient instance.
        """
        from qw.client import QClient  # lazy import
        from flowtask.conf import WORKER_LIST, WORKER_HIGH_LIST, WORKERS_LIST

        if priority == "high":
            return QClient(worker_list=WORKER_HIGH_LIST)
        if priority == "low" or priority is None or priority == "default":
            return QClient(worker_list=WORKER_LIST)
        # Named worker in WORKERS_LIST dict
        if priority in WORKERS_LIST:
            worker_list = WORKERS_LIST[priority]
            return QClient(worker_list=worker_list)
        # Unknown key — fall back to default
        self.logger.warning(
            "Unknown priority '%s'; falling back to default worker list", priority
        )
        return QClient(worker_list=WORKER_LIST)

    def _parse_result(self, raw: Any, execution_id: str) -> TaskResult:
        """Normalise a raw QClient result into a TaskResult.

        Args:
            raw: The value returned by QClient.run/queue/publish.
            execution_id: The execution UUID.

        Returns:
            A TaskResult with status and result.
        """
        if isinstance(raw, BaseException):
            return TaskResult(
                status="failed",
                error=str(raw),
                execution_id=execution_id,
            )
        if isinstance(raw, dict):
            if "exception" in raw:
                return TaskResult(
                    status="failed",
                    error=str(raw.get("error", raw["exception"])),
                    execution_id=execution_id,
                )
            # Decode message bytes if present
            try:
                raw["message"] = raw["message"].decode("utf-8")
            except (TypeError, KeyError, AttributeError):
                pass
        return TaskResult(
            status="success",
            result=raw,
            execution_id=execution_id,
        )

    async def dispatch(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> ExecutionHandle:
        """Queue the task (fire-and-forget) and return immediately.

        Uses ``QClient.queue()`` by default, or ``QClient.publish()`` when
        ``priority == "pub"``.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Forwarded to TaskWrapper (userid, ENV, etc.).

        Returns:
            An ExecutionHandle with the queue message result.
        """
        execution_id = task_id or str(uuid.uuid4())
        priority: Optional[str] = kwargs.pop(
            "priority", self._config.priority
        )
        channel = f"FLOWTASK:EXEC:{execution_id}"

        await self._publisher.publish(
            "dispatched", program, task, execution_id
        )

        wrapper = self._make_wrapper(program, task, execution_id, queued=True, **kwargs)

        try:
            if priority == "pub":
                client = self._get_client(priority=None)
                result = await asyncio.wait_for(
                    client.publish(wrapper), timeout=10
                )
            else:
                client = self._get_client(priority=priority)
                result = await asyncio.wait_for(
                    client.queue(wrapper), timeout=10
                )
        except Exception as exc:
            self.logger.error(
                "QworkerExecutor dispatch failed for %s.%s: %s", program, task, exc
            )
            await self._publisher.publish(
                "failed", program, task, execution_id, error=str(exc)
            )
            raise ExecutorError(
                f"QClient dispatch failed for {program}.{task}: {exc}"
            ) from exc

        return ExecutionHandle(
            executor_type=ExecutorType.QWORKER,
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
        """Run the task via QClient and wait for the result.

        Uses ``QClient.run()`` (or ``QClient.publish()`` for priority=pub).

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Forwarded to TaskWrapper (userid, ENV, etc.).

        Returns:
            TaskResult with the worker's return value.
        """
        execution_id = task_id or str(uuid.uuid4())
        priority: Optional[str] = kwargs.pop(
            "priority", self._config.priority
        )

        await self._publisher.publish("started", program, task, execution_id)

        wrapper = self._make_wrapper(
            program, task, execution_id, queued=False, **kwargs
        )

        try:
            if priority == "pub":
                client = self._get_client(priority=None)
                raw = await client.publish(wrapper)
            elif priority == "direct":
                client = self._get_client(priority="default")
                raw = await client.run(wrapper)
            else:
                client = self._get_client(priority=priority)
                raw = await client.run(wrapper)

            task_result = self._parse_result(raw, execution_id)

            if task_result.status == "success":
                await self._publisher.publish(
                    "completed", program, task, execution_id
                )
            else:
                await self._publisher.publish(
                    "failed", program, task, execution_id, error=task_result.error
                )

            return task_result

        except Exception as exc:
            self.logger.error(
                "QworkerExecutor run failed for %s.%s: %s", program, task, exc
            )
            await self._publisher.publish(
                "failed", program, task, execution_id, error=str(exc)
            )
            return TaskResult(
                status="failed",
                error=str(exc),
                execution_id=execution_id,
            )

    async def close(self) -> None:
        """Close the lifecycle publisher.

        Args: none.
        """
        await self._publisher.close()
