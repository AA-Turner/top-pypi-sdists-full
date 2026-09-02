import asyncio
from datetime import datetime
import traceback
import socket
from asyncdb import AsyncDB
from ...conf import (
    ENVIRONMENT,
    TASK_EXEC_BACKEND,
    TASK_EXEC_CREDENTIALS,
    TASK_EVENT_TABLE,
    INFLUX_DATABASE,
    TASK_EXEC_TABLE,
    USE_TASK_EVENT,
)
from ...utils.json import json_encoder
from .abstract import AbstractEvent

EVENT_HOST = socket.gethostbyname(socket.gethostname())


class LogExecution(AbstractEvent):
    """LogExecution.

    Log the execution of a Task into a InfluxDB measurement bucket.
    """

    def get_influx(self):
        return AsyncDB(
            TASK_EXEC_BACKEND,
            params=TASK_EXEC_CREDENTIALS,
            loop=asyncio.get_event_loop(),
        )

    async def __call__(self, *args, **kwargs):
        status = kwargs.pop("status", "event")
        task = kwargs.pop("task", None)
        cls = kwargs.pop("cls", None)
        msg = kwargs.pop("message", str(cls))
        if self.disable_notification is True:
            return
        if USE_TASK_EVENT is True:
            try:
                task_id = task.task_id
                task_name = task.taskname
                program = task.getProgram()
            except (AttributeError, TypeError):
                task_id = None
                task_name = None
                program = None
            async with await self.get_influx().connection() as conn:
                try:
                    # saving the log into metric database:
                    start_time = datetime.utcnow()
                    data = {
                        "measurement": TASK_EXEC_TABLE,
                        "location": ENVIRONMENT,
                        "timestamp": start_time,
                        "fields": {"status": status},
                        "tags": {
                            "host": EVENT_HOST,
                            "region": ENVIRONMENT,
                            "start_time": start_time,
                            "tenant": program,
                            "task": task_name,
                            "task_id": str(task_id),
                            "message": msg,
                            "traceback": str(traceback.format_exc()),
                        },
                    }
                    await conn.write(data, bucket=INFLUX_DATABASE)
                except Exception as e:
                    self._logger.error(f"Flowtask: Error saving Task Execution: {e}")


class SaveExecution(LogExecution):
    async def __call__(self, *args, **kwargs):
        status = kwargs.pop("status", "event")
        task = kwargs.pop("task", None)
        cls = kwargs.pop("error", None)
        err = getattr(cls, "message", str(cls))
        msg = kwargs.pop("message", err)
        if self.disable_notification is True:
            return
        if USE_TASK_EVENT is True:
            try:
                stat = task.stats  # getting the stat object:
            except AttributeError:
                stats = None
            if stat:
                stats = json_encoder(stat.to_json())
                start_time = stat.start_time
                end_time = stat.finish_time
                duration = stat.duration
            else:
                stats = {}
                start_time = None
                end_time = datetime.utcnow()
                duration = None
            async with await self.get_influx().connection() as conn:
                try:
                    data = {
                        "measurement": TASK_EVENT_TABLE,
                        "location": ENVIRONMENT,
                        "timestamp": end_time,
                        "fields": {"status": status},
                        "tags": {
                            "host": EVENT_HOST,
                            "region": ENVIRONMENT,
                            "stats": stats,
                            "start_time": start_time,
                            "finish_time": end_time,
                            "duration": duration,
                            "tenant": task.getProgram(),
                            "task": task.taskname,
                            "id": task.task_id,
                            "traceback": traceback.format_exc(),
                            "message": msg,
                        },
                    }
                    await conn.write(data, bucket=INFLUX_DATABASE)
                except Exception as e:
                    self._logger.error(
                        f"FlowTask: Error saving Task Execution: {e}"
                    )
