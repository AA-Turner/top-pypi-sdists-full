"""
Flowtask Task Execution.
"""
from typing import Optional
from abc import ABC
import asyncio
from navconfig.logging import logging
# Queue Worker Client:
from qw.client import QClient
from qw.wrappers import TaskWrapper
# TODO: Dispatch tasks to docker container.
from ..tasks.task import Task
from ..exceptions import FlowTaskError, TaskFailed


class TaskSupport(ABC):
    def __init__(self, *args, **kwargs):
        self._name_ = self.__class__.__name__
        self.program: str = kwargs.pop("program", "navigator")
        self.task: str = kwargs.pop('task')
        # No worker:
        self._no_worker: bool = kwargs.pop("no_worker", False)
        if not self._no_worker:
            self.worker: QClient = QClient()  # auto-discovering of workers
        else:
            self.worker: Optional[QClient] = None
        # self.worker = worker
        self.priority = kwargs.pop("priority", None)
        self.logger = logging.getLogger(
            f"Task.{self.program}.{self.task}"
        )
        self._args = args
        self._kwargs = kwargs
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Action.Task>: {self.program}.{self.task}"

    async def run(self, *args, **kwargs):
        if self._no_worker is False:
            if self.priority == "pub":
                # Using Channel Group mechanism (avoid queueing)
                try:
                    result = await self.worker.publish(self.wrapper)
                    await asyncio.sleep(0.01)
                    return result
                except asyncio.TimeoutError:
                    raise
                except Exception as exc:
                    self.logger.error(f"{exc}")
                    raise
            else:
                try:
                    result = await self.worker.queue(self.wrapper)
                    await asyncio.sleep(0.01)
                    return result
                except asyncio.TimeoutError:
                    raise
                except Exception as exc:
                    self.logger.error(f"{exc}")
                    raise
        else:
            try:
                await self.task.start()
            except Exception as exc:
                self.logger.error(exc)
                raise TaskFailed(f"{exc!s}") from exc
            try:
                return await self.task.run()
            except Exception as err:
                raise TaskFailed(
                    f"Error: Task {self.program}.{self.task} failed: {err}"
                ) from err
            finally:
                await self.task.close()

    async def close(self):
        pass

    async def open(self):
        try:
            if self._no_worker is False:
                self.wrapper = TaskWrapper(
                    program=self.program,
                    task=self.task,
                    **self._kwargs
                )
            else:
                self.task = Task(
                    task=self.task,
                    program=self.program,
                    debug=True
                )
        except Exception as exc:
            self.logger.exception(str(exc), stack_info=True)
            raise FlowTaskError(f"Error: {exc}") from exc
