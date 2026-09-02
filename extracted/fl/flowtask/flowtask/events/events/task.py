import asyncio
import pandas as pd
from navconfig import DEBUG
from navconfig.logging import logging
from .abstract import AbstractEvent
from ...exceptions import (
    NotSupported,
    TaskNotFound,
    TaskFailed,
    FileError,
    FileNotFound,
    DataNotFound,
)


class RunTask(AbstractEvent):
    def __init__(self, *args, **kwargs):
        super(RunTask, self).__init__(*args, **kwargs)
        self.program = kwargs.pop("program", None)
        self.task = kwargs.pop("task", None)

    def run_task_in_thread(self, task_coroutine):
        loop = asyncio.new_event_loop()  # Create a new event loop for the thread
        asyncio.set_event_loop(loop)
        loop.run_until_complete(task_coroutine)
        loop.close()

    async def task_execution(self):
        # avoid circular import
        from flowtask.tasks.task import Task  # noqa

        result = {}
        task = Task(
            task=self.task,
            program=self.program,
            loop=asyncio.get_event_loop(),
            enable_stat=False,
            ignore_results=True,
            debug=DEBUG,
        )
        try:
            state = await task.start()
            if not state:
                logging.warning(
                    f"Task {self.program}.{self.task} return False on Start Time."
                )
        except Exception as err:
            logging.error(err)
            raise
        try:
            state = await task.run()
            try:
                result["stats"] = task.stats.stats
            except Exception as err:
                result["stats"] = None
                result["error"] = err
            ### gettting the result of Task execution
            if isinstance(state, pd.DataFrame):
                numrows = len(state.index)
                columns = list(state.columns)
                num_cols = len(columns)
                state = {
                    "type": "Dataframe",
                    "numrows": numrows,
                    "columns": columns,
                    "num_cols": num_cols,
                }
            else:
                state = f"{state!r}"
            result["result"] = state
            await task.close()
            return result
        except DataNotFound as err:
            raise
        except NotSupported as err:
            raise
        except TaskNotFound as err:
            raise TaskNotFound(f"Task: {self.task}: {err}") from err
        except TaskFailed as err:
            raise TaskFailed(f"Task {self.task} failed: {err}") from err
        except FileNotFound:
            raise
        except FileError as err:
            raise FileError(f"Task {self.task}, File Not Found error: {err}") from err
        except Exception as err:
            raise TaskFailed(f"Error: Task {self.task} failed: {err}") from err

    async def __call__(self, *args, **kwargs):
        self._logger.debug(f":: Running Task: {self.program}.{self.task}")
        return await self.task_execution()
        # task_coroutine = self.task_execution()
        # task_thread = threading.Thread(
        #     target=self.run_task_in_thread,
        #     args=(task_coroutine,)
        # )
        # task_thread.start()
        # task_thread.join()  # Wait for the thread to finish
