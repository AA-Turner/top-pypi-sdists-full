"""DataIntegration Task Runner.

This Module can run data-integration tasks, HTTP/RESTful calls
(or even any arbitrary python function),
received parametriced tasks and return the results.

Task Runner receives different command-line arguments:

--variables: override variables passed between components/processes.
--attributes: override root-level attributes of components.
--conditions: override values in components with conditions.
--params: any value in params ins passed as kwargs
--args: list of arguments to be used by some functions (like replacement of values)

* For Calling a task:
 --program=program_name --task=task_name --params
* For calling Python Functions:
 --function=path.to.python.import --params
* System Command:
 --command=path.to.command --params
* or even Calling a URL:
 --url=URI --params
"""
from typing import Any
import uuid
import random
import asyncio
import signal
from navconfig.logging import logging

# Worker: lazy-loaded to avoid importing aiogram/telegram (~18s) at startup.
# from qw.wrappers import TaskWrapper  # deferred to dispatch_to_worker()
# from qw.client import QClient  # deferred to __init__

# FlowTask
from .utils.stats import TaskMonitor
from .parsers.argparser import ConfigParser
from .exceptions import (
    TaskError,
    TaskException,
    NotSupported,
    TaskParseError,
    ConfigError
)
from .tasks.task import Task
from .tasks.command import Command


def my_handler():
    # TODO: Copying Signal-handler from Notify Worker.
    print("Stopping")
    for task in asyncio.all_tasks():
        task.cancel()

class TaskRunner:
    """
    TaskRunner.

        Execution of DataIntegration Tasks.
    """

    logger: logging.Logger = None

    def __init__(self, loop: asyncio.AbstractEventLoop = None, worker=None, **kwargs):
        """Init Method for Task Runner."""
        self._task = None
        self._command: str = None
        self._fn: str = None
        self._url: str = None
        self._taskname = ""
        self.task_type: str = "task"
        self.stat: TaskMonitor = None
        # arguments passed by command line:
        self._conditions = {}
        self._attrs = {}
        self.ignore_steps = []
        self.run_only = []
        self._stepattrs = {}
        self._kwargs = {}
        self._variables = {}
        self._result: Any = None
        if loop:
            self._loop = loop
            self.inner_evt = False
        else:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self.inner_evt = True
        self._loop.add_signal_handler(signal.SIGINT, my_handler)
        # Task ID:
        self.task_id = uuid.uuid1(node=random.getrandbits(48) | 0x010000000000)
        # argument Parser
        if "new_args" in kwargs:
            new_args = kwargs["new_args"]
            del kwargs["new_args"]
        else:
            new_args = []
        parser = ConfigParser()
        parser.parse(new_args)
        self._argparser = parser
        self._options = parser.options
        # program definition
        self._program = self._options.program
        try:
            self._program = kwargs["program"]
            del kwargs["program"]
        except KeyError:
            pass
        if not self._program:
            self._program = "navigator"
        # DEBUG
        try:
            self._debug = kwargs["debug"]
            del kwargs["debug"]
        except KeyError:
            self._debug = self._options.debug
        # logger
        self.logger = logging.getLogger("FlowTask.Runner")
        if self._debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.notice(f"Program is: > {self._program}")
        # about Worker Information:
        self.worker = worker
        ## Task Storage:
        self._taskstorage = self._options.storage
        try:
            self.no_worker = self._options.no_worker
        except (ValueError, TypeError):
            self.no_worker = False
        try:
            self.no_events = self._options.no_events
        except (ValueError, TypeError):
            self.no_events = False
        try:
            self.no_notify = self._options.no_notify
        except (ValueError, TypeError):
            self.no_notify = False
        if kwargs:
            # remain args go to kwargs:
            self._kwargs = {**kwargs}
        # Queue Worker (lazy import to avoid loading aiogram at startup):
        from qw.client import QClient
        self._qw = QClient()

    @property
    def stats(self) -> TaskMonitor:
        """stats.
        Return a TaskMonitor object with all collected stats.
        Returns:
            TaskMonitor: stat object.
        """
        return self.stat

    def options(self) -> dict:
        return self._options

    async def __aenter__(self) -> "TaskRunner":
        """Magic Context Methods"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Magic Context Methods"""
        # clean up anything you need to clean up
        await self.close()

    @property
    def result(self):
        return self._result

    async def start(self):
        # define the type of task:
        if self._options.command:
            self._command = self._options.command
            self.task_type = "command"
            self._taskname = f"{self._command!s}"
        elif self._options.function:
            self._fn = self._options.function
            self.task_type = "function"
            self._taskname = f"{self._fn!s}"
        elif self._options.task:
            self._taskname = self._options.task
            self.task_type = "task"
        else:
            raise NotSupported("Task Runner: Unknown or missing Task type.")
        # initialize the Task Monitor
        try:
            self.stat = TaskMonitor(
                name=self._taskname, program=self._program, task_id=self.task_id
            )
            await self.stat.start()
        except Exception as err:
            raise TaskError(f"Task Runner: Error on TaskMonitor: {err}") from err
        # create the task object:
        if self.task_type == "command":
            try:
                self._task = Command(
                    task_id=self.task_id,
                    task=self._command,
                    program=self._program,
                    loop=self._loop,
                    parser=self._argparser,
                    **self._kwargs,
                )
            except Exception as err:
                raise TaskException(f"{err!s}") from err
        elif self.task_type == "task":
            try:
                self._task = Task(
                    task_id=self.task_id,
                    task=self._taskname,
                    program=self._program,
                    loop=self._loop,
                    parser=self._argparser,
                    storage=self._taskstorage,
                    disable_notifications=self.no_notify,
                    no_events=self.no_events,
                    **self._kwargs,
                )
            except Exception as err:
                raise TaskException(f"{err!s}") from err
        # then, try to "start" the task:
        logging.debug(
            f"::: FlowTask: Running {self.task_type}: {self._task!r} with id: {self.task_id}"
        )
        try:
            self._task.setStat(self.stat)
            await self._task.start()
        except (ConfigError, TaskParseError, TaskError):
            raise
        except Exception as err:
            logging.error(err)
            raise TaskException(f"{err!s}") from err
        return True

    async def run(self):
        try:
            if self.no_worker:
                try:
                    self._result = await self._task.run()
                finally:
                    await self._task.close()
            else:
                # sent task to Worker
                from qw.wrappers import TaskWrapper
                task = TaskWrapper(
                    program=self._program,
                    task_id=self.task_id,
                    task=self._taskname,
                    debug=self._debug,
                    parser=self._argparser,
                    no_events=self.no_events,
                    **self._kwargs,
                )
                if self._options.queued is True:
                    task.queued = True
                    result = await self._qw.queue(task)
                else:
                    task.queued = False
                    result = await self._qw.run(task)
                if isinstance(result, BaseException):
                    raise result
                elif isinstance(result, dict):
                    if "exception" in result:
                        ex = result["exception"]
                        msg = result["error"]
                        raise ex(f"{msg!s}")
                    else:
                        self._result = result
                else:
                    self._result = result
        except Exception as err:
            logging.error(err)
            raise
        return True

    async def close(self):
        if self._debug:
            logging.debug(f"ENDING TASK {self._taskname}")
        try:
            await self.stat.stop()
        except Exception as err:  # pylint: disable=W0718
            logging.exception(err)
        finally:
            if self.inner_evt is True:
                self._loop.close()
