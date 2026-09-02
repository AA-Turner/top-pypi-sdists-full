# Copyright (C) 2018-present Jesus Lara
#
"""Local (in-process) job executor for the flowtask executor framework."""
from __future__ import annotations
import asyncio
import uuid
from flowtask.executors.base import AbstractJobExecutor
from flowtask.executors.models import (
    ExecutorConfig,
    ExecutorType,
    ExecutionHandle,
    TaskResult,
)
from flowtask.executors.events import ExecutorLifecyclePublisher
from flowtask.executors.registry import register_executor


@register_executor("local")
class LocalJobExecutor(AbstractJobExecutor):
    """Runs flowtask tasks in-process (no worker queue).

    This is the direct replacement for the ``no_worker=True`` code path
    that existed in all 4 dispatch sites.  It instantiates a :class:`Task`
    (or :class:`Command` for command-type tasks), calls ``start()`` /
    ``run()`` / ``close()`` in sequence, and returns the result.

    Args:
        config: ExecutorConfig with ``type=LOCAL``.
        **kwargs: Passed through to the base constructor.
    """

    def __init__(self, config: ExecutorConfig, **kwargs) -> None:
        super().__init__(config, **kwargs)
        self._publisher = ExecutorLifecyclePublisher()

    @classmethod
    def name(cls) -> str:
        """Return registry name.

        Returns:
            ``"local"``
        """
        return "local"

    async def dispatch(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> ExecutionHandle:
        """Fire-and-forget: start the task in a background asyncio task.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Passed through to the Task constructor.

        Returns:
            An ExecutionHandle identifying the background task.
        """
        channel = f"FLOWTASK:EXEC:{task_id}"
        handle = ExecutionHandle(
            executor_type=ExecutorType.LOCAL,
            execution_id=task_id,
            task_program=program,
            task_name=task,
            channel=channel,
        )

        await self._publisher.publish(
            "dispatched", program, task, task_id
        )

        # Fire-and-forget in background task
        asyncio.create_task(
            self._run_task(program, task, task_id, **kwargs),
            name=f"local-executor-{task_id[:8]}",
        )

        return handle

    async def run(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> TaskResult:
        """Run the task in-process and wait for completion.

        This replicates the current ``no_worker=True`` execution path
        in ``flowtask/services/tasks/tasks.py``.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Forwarded to the Task constructor (e.g. userid, ENV, debug).

        Returns:
            TaskResult with status, result, and stats.
        """
        await self._publisher.publish("started", program, task, task_id)
        result = await self._run_task(program, task, task_id, **kwargs)
        return result

    async def _run_task(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> TaskResult:
        """Internal: instantiate, run, and close a task; return TaskResult.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Forwarded to the Task constructor.

        Returns:
            TaskResult with status, result, stats, and error on failure.
        """
        # Lazy import to avoid circular dependencies at module level
        from flowtask.tasks.task import Task

        task_obj = Task(
            task=task,
            program=program,
            **kwargs,
        )
        execution_id = str(task_id) if task_id else str(uuid.uuid4())

        try:
            await task_obj.start()
        except Exception as exc:
            self.logger.error(
                "Task %s.%s failed during start(): %s", program, task, exc
            )
            await self._publisher.publish(
                "failed", program, task, task_id, error=str(exc)
            )
            return TaskResult(
                status="failed",
                error=str(exc),
                execution_id=execution_id,
            )

        try:
            state = await task_obj.run()

            # Collect stats.  Return the full TaskMonitor object (not the flat
            # ``.stats`` dict) so the per-step breakdown (StepMonitor list) is
            # preserved for in-process callers that print ``runner.stats``.
            # Remote executors serialise their own dict separately.
            try:
                stats = task_obj.stats
            except AttributeError:
                stats = None

            await self._publisher.publish(
                "completed", program, task, task_id
            )
            return TaskResult(
                status="success",
                result=state,
                stats=stats,
                execution_id=execution_id,
            )

        except Exception as exc:
            self.logger.error(
                "Task %s.%s failed during run(): %s", program, task, exc
            )
            await self._publisher.publish(
                "failed", program, task, task_id, error=str(exc)
            )
            # Preserve the per-step breakdown on failure too: the task's
            # TaskMonitor already holds the StepMonitor list for the steps that
            # ran before the error, so callers printing ``runner.stats`` still
            # see which steps executed (matching the success path).
            try:
                stats = task_obj.stats
            except AttributeError:
                stats = None
            return TaskResult(
                status="failed",
                error=str(exc),
                stats=stats,
                execution_id=execution_id,
            )

        finally:
            try:
                await task_obj.close()
            except Exception as exc:
                self.logger.warning(
                    "Task %s.%s raised during close(): %s", program, task, exc
                )

    async def close(self) -> None:
        """Close the lifecycle publisher.

        Args: none.
        """
        await self._publisher.close()
