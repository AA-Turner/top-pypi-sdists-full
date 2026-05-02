from typing import Union
import asyncio
from concurrent.futures import ThreadPoolExecutor
import jsonpickle
import pandas as pd
from navconfig import config as ENV
from navconfig.logging import logging

# Queue Worker Client:
from qw.client import QClient
from qw.wrappers import TaskWrapper
from ...conf import DEBUG, WORKER_LIST, WORKER_HIGH_LIST, WORKERS_LIST
from ...exceptions import (
    NotSupported,
    TaskNotFound,
    TaskFailed,
    FileError,
    FileNotFound,
    DataNotFound,
)
from ...tasks.task import Task


if WORKER_LIST:
    QW = QClient(worker_list=WORKER_LIST)
    QW_high = QClient(worker_list=WORKER_HIGH_LIST)
else:
    QW = QClient()  # auto-discovering of workers
    QW_high = QW


async def launch_task(
    program_slug: str,
    task_id: str,
    loop: asyncio.AbstractEventLoop = None,
    task_uuid: str = None,
    queued: bool = False,
    no_worker: bool = False,
    priority: str = "low",
    userid: Union[int, str] = None,
    **kwargs,
):
    """launch_task.
    Runs (or queued) a Task from Task Monitor.
    """
    state = None
    result = {}

    if no_worker is True:
        # Running task in Local
        print(f"RUNNING TASK {program_slug}.{task_id}")
        task = Task(
            task=task_id,
            program=program_slug,
            loop=loop,
            ignore_results=False,
            ENV=ENV,
            debug=DEBUG,
            userid=userid,
            **kwargs,
        )
        try:
            state = await task.start()
            if not state:
                logging.warning(
                    f"Task {program_slug}.{task_id} return False on Start Time."
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
            return (state, "Executed", result)
        except DataNotFound as err:
            raise
        except NotSupported as err:
            raise
        except TaskNotFound as err:
            raise TaskNotFound(f"Task: {task_id}: {err}") from err
        except TaskFailed as err:
            raise TaskFailed(f"Task {task_id} failed: {err}") from err
        except FileNotFound:
            raise
        except FileError as err:
            raise FileError(f"Task {task_id}, File Not Found error: {err}") from err
        except Exception as err:
            raise TaskFailed(f"Error: Task {task_id} failed: {err}") from err
        finally:
            await task.close()
    else:
        if queued:
            action = "Queued"
        else:
            action = "Dispatched"
    # Task:
    print(' Pre Wrapper: ', kwargs, type(kwargs))
    task = TaskWrapper(
        program=program_slug,
        task=task_id,
        ignore_results=True,
        userid=userid,
        **kwargs
    )
    ### TODO: Add Publish into Broker
    logging.info(
        f":::: Calling Task {program_slug}.{task_id}: priority {priority!s}"
    )
    if action == "Queued":
        if priority == "high":
            result = await asyncio.wait_for(QW_high.queue(task), timeout=10)
        elif priority == "low":
            result = await asyncio.wait_for(QW.queue(task), timeout=10)
        elif priority == "pub":
            result = await asyncio.wait_for(QW.publish(task))
        else:
            try:
                w = WORKERS_LIST[priority]
                print('W > ', w)
                worker = QClient(worker_list=w)
            except KeyError:
                worker = QW
            result = await asyncio.wait_for(
                worker.queue(task),
                timeout=10
            )
        try:
            result["message"] = result["message"].decode("utf-8")
        except (TypeError, KeyError):
            result["message"] = None
        print(f"Task Queued: {result!s}")
        return (task_uuid, action, result)
    else:
        try:
            result = await QW_high.run(task) if priority == "high" else await QW.run(task)
            if isinstance(result, str):
                # check if can we unserialize the jsonpickle
                try:
                    result = jsonpickle.decode(result)
                except (TypeError, KeyError, ValueError, AttributeError) as ex:
                    result = {"message": result, "error": ex}
            logging.debug(f"Executed Task: {result!s}")
            try:
                result["message"] = result["message"].decode("utf-8")
            except (TypeError, KeyError):
                result["message"] = None
            except AttributeError:
                pass
            return (task_uuid, action, result)
        except (NotSupported, TaskNotFound, TaskFailed, FileNotFound, FileError) as ex:
            logging.error(ex)
            raise
        except Exception as exc:
            logging.error(exc)
            raise TaskFailed(f"Error: Task {task_id} failed: {exc}") from exc
