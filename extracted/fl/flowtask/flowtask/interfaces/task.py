"""
Flowtask Task Execution.
"""
from typing import Optional
from abc import ABC
import asyncio
import uuid as uuid_lib
from navconfig.logging import logging
from ..exceptions import FlowTaskError, TaskFailed


class TaskSupport(ABC):
    def __init__(self, *args, **kwargs):
        self._name_ = self.__class__.__name__
        self.program: str = kwargs.pop("program", "navigator")
        self.task: str = kwargs.pop('task')
        # No worker (legacy flag — kept for backward compat):
        self._no_worker: bool = kwargs.pop("no_worker", False)
        # Executor override (new-style):
        self._executor_name: Optional[str] = kwargs.pop("executor", None)
        self.priority = kwargs.pop("priority", None)
        self.logger = logging.getLogger(
            f"Task.{self.program}.{self.task}"
        )
        self._args = args
        self._kwargs = kwargs
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Action.Task>: {self.program}.{self.task}"

    def _resolve_executor(self):
        """Resolve the executor instance using current options."""
        from flowtask.executors.resolver import resolve_executor

        class _Opts:
            pass

        opts = _Opts()
        opts.executor = self._executor_name
        opts.executor_image = None
        opts.executor_namespace = None
        opts.no_worker = self._no_worker
        # Dispatch (fire-and-forget) only when explicitly queued via priority flag.
        opts.queued = (
            self.priority in ("pub", "high", "low")
            and not self._no_worker
            and not self._executor_name  # explicit executor bypasses priority-based mode selection
        )

        task_def: dict = {}
        if self._executor_name:
            task_def["executor"] = self._executor_name
        elif self._no_worker:
            task_def["executor"] = "local"

        return resolve_executor(task_def, opts)

    async def run(self, *args, **kwargs):
        executor = self._resolve_executor()
        task_uuid = str(uuid_lib.uuid4())
        try:
            task_result = await executor.run(
                self.program,
                self.task,
                task_uuid,
                priority=self.priority,
                **self._kwargs,
            )
            if task_result.status == "failed":
                raise TaskFailed(
                    f"Error: Task {self.program}.{self.task} failed: {task_result.error}"
                )
            return task_result.result
        except TaskFailed:
            raise
        except asyncio.TimeoutError:
            raise
        except Exception as exc:
            self.logger.error(f"{exc}")
            raise TaskFailed(f"Error: Task {self.program}.{self.task} failed: {exc}") from exc

    async def close(self):
        pass

    async def open(self):
        """Prepare the executor for this task (no-op; executor is resolved lazily in run())."""
        try:
            # Eagerly resolve the executor so configuration errors surface early.
            self._resolve_executor()
        except Exception as exc:
            self.logger.exception(str(exc), stack_info=True)
            raise FlowTaskError(f"Error: {exc}") from exc
