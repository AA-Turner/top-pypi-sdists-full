import asyncio
import logging
from collections.abc import Callable
import traceback
import pprint
from asyncdb.exceptions import NoDataFound
from ..tasks.task import Task
from ..utils.functions import check_empty
from ..exceptions import (
    DataNotFound,
    NotSupported,
    ComponentError,
    TaskNotFound,
    TaskDefinition,
    TaskFailed,
    FileNotFound,
)
from .flow import FlowComponent


class SubTask(FlowComponent):
    """
    SubTask

        Overview

            The SubTask class is a component for executing a specified task as a sub-task within a workflow.
            It allows passing configurations and parameters, including conditional steps, to dynamically manage 
            and execute the named task in the specified program.

        :widths: auto

            | task           |   Yes    | The name of the task to execute as a sub-task.                            |
            | program        |   Yes    | The name of the program under which the task is defined.                  |
            | ignore_steps   |   No     | List of steps to ignore during the sub-task execution.                    |
            | run_only       |   No     | List of specific steps to run, ignoring others.                           |
            | conditions     |   No     | Dictionary of conditions to apply to the sub-task execution.              |

        Returns

            This component executes the specified task and returns the task’s output or state upon completion.
            If the task encounters an error or lacks data, an appropriate exception is raised. The component tracks 
            task and program details in the metrics, and logs the state of the task if debugging is enabled.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          SubTask:
          task: forms
          program: banco_chile
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self._params = {}
        self.task: str = ""
        self._task = None
        self.program: str = ""
        self.conditions = {}
        self._arguments = {}
        self.ignore_steps: list = []
        self.run_only: list = []
        super(SubTask, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.program = self._program

    async def start(self, **kwargs):
        program = self.program
        self._program = program
        try:
            del self._params["program"]
        except KeyError:
            pass
        try:
            # task = self.task
            del self._params["task"]
        except KeyError:
            pass
        # remove the SkipError (avoid passed to SubTask.)
        try:
            del self._params["skipError"]
        except KeyError:
            pass
        # passing variables to SubTask
        params = {
            "vars": self._vars,
            "variables": self._variables,
            "ignore_steps": self.ignore_steps,
            "run_only": self.run_only,
            "memory": self._memory,
            "attributes": self._attributes,
            "arguments": self._arguments,
            "is_subtask": True,
            "conditions": self.conditions,
            "params": self._params,
        }
        if self._debug is True:
            pp = pprint.PrettyPrinter(indent=4)
            print(" Subtask Properties ==================")
            pp.pprint(params)
            print(" ==================")
        if "debug" in self._params:
            del self._params["debug"]
        # definition of task
        try:
            self._task = Task(
                task=self.task,
                program=self.program,
                loop=self._loop,
                debug=self._debug,
                stat=self.stat.parent(),
                **params,
            )
            self.add_metric(
                "TASK", f"{self.program}.{self.task}"
            )
            try:
                if self._task:
                    prepare = await self._task.start()
                    if prepare:
                        return True
                    else:
                        return False
            except (TaskDefinition, TaskFailed) as err:
                logging.exception(err, stack_info=True)
        except TaskNotFound as err:
            logging.exception(err, stack_info=True)
        except Exception as err:
            traceback.print_exc()
            print(err, err.__class__)
            logging.exception(err, stack_info=True)

    async def close(self):
        if self._task:
            try:
                await self._task.close()
            except Exception as err:
                raise TaskFailed(
                    f"Error closing Task {self.task!s}, error: {err}"
                ) from err

    async def run(self):
        result = False
        if not self._task:
            return False
        try:
            result = await self._task.run()
        except (DataNotFound, NoDataFound, FileNotFound):
            raise
        except NotSupported as err:
            raise NotSupported(
                f"Error running Task {self.task}, error: {err}"
            ) from err
        except ComponentError:
            raise
        except Exception as err:
            print("TYPE ", err, type(err))
            raise ComponentError(
                f"Error on Task {self.task}: {err}"
            ) from err
        if check_empty(result):
            return False
        else:
            self._result = self
            return result
