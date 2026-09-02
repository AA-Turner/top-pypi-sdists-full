from collections.abc import Callable
import asyncio
from pathlib import Path
import traceback
import subprocess
from ..models import TaskState
from ..exceptions import TaskNotFound
from .abstract import AbstractTask


class Command(AbstractTask):
    """
    Command.

        Execution of Operating System commands.
    """

    def __init__(
        self,
        task_id: str = None,
        task: str = None,
        program: str = None,
        loop: asyncio.AbstractEventLoop = None,
        parser: Callable = None,
        **kwargs,
    ) -> None:
        super(Command, self).__init__(
            task_id=task_id,
            task=task,
            program=program,
            loop=loop,
            parser=parser,
            **kwargs,
        )
        self._task = task
        # can we mix args and params
        try:
            self._parameters = self._parameters + self._arguments
        except ValueError:
            pass

    async def start(self) -> bool:
        await super(Command, self).start()
        if self._taskdef:
            # we can replace the task definition from database:
            self._task = self._taskdef.task_path
            if self._taskdef.params:
                # add it to existing params:
                self._parameters = self._parameters + self._taskdef.params
                self._logger.debug(f"Command: new parameters: {self._parameters}")
        command = Path(self._task)
        if not command.exists():
            self._state = TaskState.STOPPED
            self._events.onTaskFailure(
                error=f"Command: missing or doesn't exists: {self._task}", task=self
            )
            raise TaskNotFound(f"Command: missing or doesn't exists: {self._task}")
        return True

    async def run(self) -> bool:
        self._state = TaskState.RUNNING
        self._logger.debug(
            f"Running Command {self._task!s} with params: {self._parameters!r}"
        )
        try:
            result = self.run_exec(self._task, self._parameters)
            if not result:
                self._state = TaskState.DONE_WITH_NODATA
            else:
                self._state = TaskState.DONE
            self._events.onTaskDone(
                message=f":: Command Ended: {self._taskname}", task=self
            )
            return result
        except Exception as err:
            self._state = TaskState.FAILED
            trace = traceback.format_exc()
            self._events.onTaskFailure(cls=err, trace=trace, task=self)
            return False

    async def close(self) -> None:
        pass

    def run_exec(self, path, args, shell: bool = False):
        result = None
        ex = [path]
        if args:
            ex = ex + args
        try:
            cp = subprocess.run(
                ex,
                capture_output=True,
                shell=shell,
                check=True,
                universal_newlines=True,
            )
            try:
                data = cp.stdout.decode()
                err = cp.stderr.decode()
            except (UnicodeDecodeError, AttributeError):
                data = cp.stdout
                err = cp.stderr
            if err:
                result = err
            else:
                result = data
            return result
        except subprocess.CalledProcessError as err:
            self._state = TaskState.FAILED
            self._events.onTaskFailure(
                message=f"SubProcess Call Error {err!s}",
                trace=traceback.format_exc(),
                cls=err,
                task=self,
            )
        except Exception as err:
            self._logger.exception(err)
            raise
