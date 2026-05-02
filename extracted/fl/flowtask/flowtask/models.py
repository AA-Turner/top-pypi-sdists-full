"""Task Models.

Models for Tasks/Jobs structure.
"""
import asyncio
import os
from datetime import datetime
import uuid
from enum import Enum
from asyncpg.exceptions import InterfaceError
from navconfig.logging import logging
from asyncdb.models import Model, Column
from asyncdb import AsyncDB
from asyncdb.exceptions import NoDataFound, ModelError
from querysource.types.validators import Entity
from querysource.conf import default_dsn


class TaskState(Enum):
    IDLE = (0, "Idle")
    PENDING = (1, "Pending")
    STARTED = (2, "Started")
    RUNNING = (3, "Task Running")
    STOPPED = (4, "Task Stopped")
    DONE = (5, "Done")
    DONE_WITH_NODATA = (6, "Done (No Data)")
    NOT_FOUND = (7, "Not Found")
    FAILED = (9, "Task Failed")
    DONE_WITH_WARNINGS = (10, "Warning")
    SKIPPED = (11, "Skipped")
    ERROR = (12, "Task Error")
    DISCARDED = (13, "Discarded")
    EXCEPTION = (98, "Task Exception")
    CLOSED = (99, "Closed")

    def __init__(self, value, label):
        self._value_ = value
        self._label = label

    @property
    def label(self):
        return self._label

    def __int__(self):
        return self._value_


def at_now():
    return datetime.now()


class TaskModel(Model):
    task: str = Column(required=True, primary_key=True)
    task_id: uuid.UUID = Column(required=False)
    task_function: str = Column(required=False)
    task_path: str = Column(required=False)
    task_definition: dict = Column(required=False, db_type="jsonb")
    url: str = Column(required=False)
    url_response: str = Column(required=False, default="json")
    attributes: dict = Column(required=False, db_type="jsonb")
    params: dict = Column(required=False, db_type="jsonb")
    enabled: bool = Column(required=False, default=True)
    is_coroutine: bool = Column(required=False, default=False)
    executor: str = Column(required=False, default="default")
    last_started_time: datetime = Column(required=False)
    last_exec_time: datetime = Column(required=False)
    last_done_time: datetime = Column(required=False)
    created_at: datetime = Column(required=False, default=at_now(), db_default="now()")
    updated_at: datetime = Column(required=False, default=at_now(), db_default="now()")
    program_id: int = Column(required=False, default=1)
    program_slug: str = Column(required=False, default="navigator")
    is_queued: bool = Column(required=False, default=False)
    task_state: TaskState = Column(required=False, default=TaskState.IDLE)
    traceback: str = Column(required=False)
    file_id: int = Column(required=False)
    storage: str = Column(required=False, default="default", comment="Task Storage")

    class Meta:
        driver = "pg"
        name = "tasks"
        schema = os.environ.get("DB_SCHEMA", "troc")
        app_label = os.environ.get("DB_SCHEMA", "troc")
        strict = True
        frozen = False
        remove_nulls = True  # Auto-remove nullable (with null value) fields


async def setTaskState(task, message, **kwargs):
    """
    Set the task state on Task Table:
    """
    exec_time = datetime.now()
    state = task.getState()
    taskinfo = {"program_slug": task.getProgram(), "task": task.taskname}
    data = {"task_state": int(state)}
    _new = False
    if state == TaskState.STARTED:
        data["last_started_time"] = exec_time
        data["traceback"] = None
    elif state == TaskState.RUNNING:
        data["traceback"] = None
    elif state == TaskState.STOPPED:
        data["last_exec_time"] = exec_time
        data["traceback"] = f"{message!s}"
    elif state in (TaskState.FAILED, TaskState.ERROR, TaskState.EXCEPTION):
        data["last_exec_time"] = exec_time
        if "cls" in kwargs:
            e = str(kwargs["cls"]).replace("'", "")
            data["traceback"] = f"{e!s}"
        elif "trace" in kwargs:
            data["traceback"] = f"{kwargs['trace']!s}"
        elif "error" in kwargs:
            data["traceback"] = f"{kwargs['error']!s}"
        else:
            data["traceback"] = f"{message!s}"
    elif state in (
        TaskState.DONE,
        TaskState.DONE_WITH_NODATA,
        TaskState.DONE_WITH_WARNINGS,
    ):
        if "cls" in kwargs:
            data["traceback"] = f"{kwargs['cls']!s}"
        elif "error" in kwargs:
            data["traceback"] = f"{kwargs['error']!s}"
        else:
            data["traceback"] = f"{message!s}"
        data["last_exec_time"] = exec_time
        data["last_done_time"] = exec_time
    if schema := task.schema():
        # is a database-based task #
        dsn = default_dsn
        if not dsn:
            logging.warning(":: Missing DSN required for Task State")
        try:
            evt = asyncio.get_event_loop()
        except RuntimeError:
            evt = asyncio.new_event_loop()
            _new = True
        db = AsyncDB("pg", dsn=dsn, loop=evt)
        try:
            async with await db.connection() as conn:  # pylint: disable=E1101
                TaskModel.Meta.schema = schema
                TaskModel.Meta.connection = conn
                try:
                    tsk = await TaskModel.get(**taskinfo)
                    for key, val in data.items():
                        setattr(tsk, key, val)
                    result = await tsk.update()
                    # we can return the related task to used someone else #
                    return result
                except NoDataFound as err:
                    logging.error(err)
                    # task doesn't exists
                    return None
        except (RuntimeError, InterfaceError, ModelError) as err:
            # there is no table tasks on this tenant:
            if "does not exist" in str(err):
                logging.warning(f"Table Task not found: {err}")
                return None
            # Another operation is in progress, create a new Connection:
            logging.error(err)
            db = AsyncDB("pg", dsn=dsn, loop=evt)
            async with await db.connection() as conn:  # pylint: disable=E1101
                ## Running Update manually:
                program = task.getProgram()
                msg = data["traceback"]
                trace = Entity.escapeString(msg)
                query = f"""
                    UPDATE {schema}.tasks SET
                    task_state = {state.value}, traceback = '{trace}',
                    last_exec_time = now()
                    WHERE program_slug = '{program}'
                    AND task = '{task.taskname}'
                """
                print(query)
                result, error = await conn.execute(query)
                if error:
                    logging.error(error)
                return None
        except Exception as err:
            logging.error(err)
            raise RuntimeError(f"Model Error: {err!s}") from err
        finally:
            TaskModel.Meta.connection = None
            try:
                if _new is True:
                    evt.close()
            except Exception:
                pass
    else:
        # sending "data" to logging info
        data = {**taskinfo, **data}
        logging.info(data)
        return data
