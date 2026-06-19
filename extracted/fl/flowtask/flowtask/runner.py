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
        from flowtask.executors.resolver import resolve_executor, determine_execution_mode
        try:
            # Build a minimal task definition for the resolver
            task_def = {"executor": getattr(self._options, "executor", None) or "default"}
            executor = resolve_executor(task_def, self._options)
            mode = determine_execution_mode(self._options)
            # The executor builds a fresh Task WITHOUT the CLI parser, so options
            # that the Task only reads from the parser (run_only, ignore,
            # override_attributes, variables, conditions) would be silently lost
            # — breaking flags like --run_only.  Forward them as serialisable
            # kwargs (NOT the parser object, which remote executors can't
            # serialise) so the Task picks them up via its kwargs fallbacks.
            for _opt_attr, _kw_name in (
                ("run_only", "run_only"),
                ("ignore", "ignore_steps"),
                ("override_attributes", "override_attributes"),
                ("variables", "variables"),
                ("conditions", "conditions"),
                ("masks", "masks"),
                ("args", "args"),
                ("arguments", "arguments"),
                # The executor builds a fresh Task that re-resolves its storage
                # from kwargs; without forwarding the selected task/file storage
                # the new Task silently falls back to "default" (TASK_PATH),
                # breaking --storage=<name> (e.g. private).
                ("storage", "storage"),
                ("filestore", "filestore"),
            ):
                _val = getattr(self._options, _opt_attr, None)
                if _val:
                    self._kwargs.setdefault(_kw_name, _val)
            if mode == "dispatch":
                handle = await executor.dispatch(
                    self._program,
                    self._taskname,
                    str(self.task_id),
                    debug=self._debug,
                    no_events=self.no_events,
                    **self._kwargs,
                )
                self._result = {"handle": handle.execution_id}
            else:
                task_result = await executor.run(
                    self._program,
                    self._taskname,
                    str(self.task_id),
                    debug=self._debug,
                    no_events=self.no_events,
                    **self._kwargs,
                )
                if task_result.status == "failed":
                    from flowtask.exceptions import TaskFailed
                    raise TaskFailed(task_result.error or "Task execution failed")
                self._result = task_result.result
                # Propagate the executor task's full TaskMonitor (with per-step
                # stats) so ``runner.stats`` reflects the real execution instead
                # of the runner's placeholder monitor.  Local (in-process) runs
                # return the live TaskMonitor; remote executors return a
                # serialised dict, which we leave on self.stat untouched.
                if isinstance(task_result.stats, TaskMonitor):
                    try:
                        await self.stat.stop()  # stop placeholder's sampler
                    except Exception:  # pylint: disable=W0718
                        pass
                    self.stat = task_result.stats
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
