"""Helper to handle fire-and-forget tasks, keeping them in scope until done"""

from typing import MutableMapping, Any, Optional, ClassVar, Coroutine, Union, Sequence, cast
import asyncio
import logging
from dataclasses import dataclass, field


LOGGER = logging.getLogger(__name__)


@dataclass
class TaskMaster:
    """Create tasks, keep them in scope until done"""

    _tasks: MutableMapping[str, "asyncio.Task[Any]"] = field(init=False, default_factory=dict)
    _singleton: ClassVar[Optional["TaskMaster"]] = None

    @classmethod
    def singleton(cls) -> "TaskMaster":
        """Return singleton"""
        if not TaskMaster._singleton:
            TaskMaster._singleton = TaskMaster()
        return TaskMaster._singleton

    def exists(self, taskname: str) -> bool:
        """Check if given task already exists without having to access private property from outside"""
        return taskname in self._tasks

    async def wait_current(self, timeout: Optional[float] = None) -> Sequence[Union[Any, Exception]]:
        """Wait for all *current* tasks to complete, task exceptions are returned. If timeout is given TimeoutError
        is raised when time runs out"""

        async def inner() -> Sequence[Union[Any, Exception]]:
            """Inner function so we can use wait_for"""
            return cast(
                Sequence[Union[Any, Exception]], await asyncio.gather(*(self._tasks.values()), return_exceptions=True)
            )

        return await asyncio.wait_for(asyncio.shield(inner()), timeout=timeout)

    async def wait_all(self, timeout: Optional[float] = None) -> Sequence[Union[Any, Exception]]:
        """Wait until no tasks remain, task exceptions are returned. If timeout is given TimeoutError
        is raised when time runs out"""

        async def inner() -> Sequence[Union[Any, Exception]]:
            """Inner function so we can use wait_for"""
            ret = []
            while self._tasks:
                ret += await asyncio.gather(*(self._tasks.values()), return_exceptions=True)
            return ret

        return await asyncio.wait_for(asyncio.shield(inner()), timeout=timeout)

    def create_task(self, coro: Coroutine[Any, Any, Any], *, name: Optional[str] = None) -> "asyncio.Task[Any]":
        """Helper to wrap asyncios create_task so that we always handle the exception and track long-running tasks"""
        if name and name in self._tasks:
            raise ValueError(f"name {name} is already tracked")
        task = asyncio.get_event_loop().create_task(coro, name=name)

        def report_error_remove_tracking(task: "asyncio.Task[Any]") -> None:
            """done callback to bubble up errors and remove tracking"""
            # Remove from tracking (we monkeypatched get_name above)
            name = task.get_name()
            del self._tasks[name]
            # Bubble up any exceptions
            try:
                exc = task.exception()
                if exc:
                    LOGGER.error("Task {} raised exception {}".format(task, exc))
                    raise exc
            except asyncio.CancelledError:
                LOGGER.error("Task {} did not handle cancellation".format(task))

        self._tasks[task.get_name()] = task
        task.add_done_callback(report_error_remove_tracking)
        return task

    async def stop_named_task_graceful(self, taskname: str, *, warn: bool = True) -> Optional[Any]:
        """cancel the named task if it is running and return the result"""
        if taskname not in self._tasks:
            if warn:
                LOGGER.warning("task {} not found".format(taskname), stack_info=True)
            return None
        task = self._tasks[taskname]
        return await self.stop_task_graceful(task)

    async def stop_task_graceful(self, task: "asyncio.Task[Any]") -> Any:
        """cancel the given task if it is running and return the result"""
        if not task.done():
            LOGGER.info("Cancelling task {}".format(task))
            task.cancel()
        try:
            return await task
        except asyncio.CancelledError:
            LOGGER.error("Task {} did not handle cancellation".format(task))

    async def stop_lingering_tasks(self) -> None:
        """Stop all still lingering tasks and fetch their results"""
        # we modify the dictionary during iteration, make a copy of the values
        for task in list(self._tasks.values()):
            try:
                await self.stop_task_graceful(task)
                LOGGER.info("Task {} stopped".format(task))
            except Exception:  # pylint: disable=W0703
                LOGGER.exception("Task {} returned exception".format(task))
