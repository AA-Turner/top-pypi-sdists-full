"""
TaskService.

Service for running tasks.
"""
from typing import Any
import uuid
import random
import logging
import aiofiles
from aiohttp import web
from pathlib import PurePath, PosixPath
from aiohttp.web import StreamResponse
import pandas as pd
from navigator.views import BaseView
from navigator.conf import AUTH_SESSION_OBJECT
from navigator_session import get_session
from ...exceptions import (
    TaskException,
    TaskDefinition,
    TaskParseError,
    TaskNotFound,
    DataNotFound,
    FileNotFound,
)
from ...tasks.task import Task


class TaskService(BaseView):
    """TaskService.

    Task As a Service: launch data-based tasks and returning the resultset in useful formats.
    Args:
        BaseView (_type_): _description_
    """

    def get_user(self, session, idx: str = "user_id") -> int:
        if not session:
            self.error(response={"error": "Unauthorized"}, status=403)
        try:
            if AUTH_SESSION_OBJECT in session:
                return session[AUTH_SESSION_OBJECT][idx]
            else:
                return session[idx]
        except KeyError:
            self.error(
                response={
                    "error": "Unauthorized",
                    "message": "Hint: maybe you need to pass an Authorization token.",
                },
                status=403,
            )

    async def check_task(self):
        # get the URL parameters
        params = self.get_args()
        try:
            program = params["program"]
            del params["program"]
        except (ValueError, KeyError) as ex:
            # we need a program
            raise TaskDefinition("Resource Error: We need a Program Name") from ex
        try:
            task_id = params["task_id"]
            del params["task_id"]
        except (ValueError, KeyError) as ex:
            # we need a Task ID
            raise TaskDefinition("Resource Error: We need a Task Name") from ex
        return task_id, program

    async def get_task(self, task: str, program: str, **kwargs) -> Task:
        # Task ID:
        task_id = uuid.uuid1(node=random.getrandbits(48) | 0x010000000000)
        try:
            usr = await get_session(self.request)
            user = self.get_user(usr)
        except (TypeError, ValueError):
            user = None

        try:
            task = Task(
                task_id=task_id,
                task=task,
                program=program,
                loop=self._loop,
                userid=user,
                **kwargs,
            )
            # disable statistics
            task.enable_stat = False
        except Exception as err:
            raise TaskException(err) from err
        # then, try to "start" the task:
        logging.debug(f"::::: DI: Running Task: {task!r}")
        return task

    async def launch_task(self, task: Task) -> Any:
        try:
            await task.start()
        except (TaskParseError, TaskDefinition, TaskNotFound) as ex:
            raise TaskDefinition(str(ex)) from ex
        except Exception as err:
            self.logger.error(err)
            raise TaskException(
                f"Task Error: {err}"
            ) from err
        # run task:
        try:
            return await task.run()
        except Exception as err:
            self.logger.exception(err)
            raise
        finally:
            await task.close()

    async def get(self):
        """
        GET Method.
        description: Executing a Task and returning the result
        tags:
        - tasks
        - DataIntegration
        consumes:
        - application/json
        produces:
        - application/json
        responses:
            "200":
                description: Existing Task was executed.
            "202":
                description: Task was accepted to queue (no return)
            "204":
                description: No data was found
            "400":
                description: Task Failed to execute
            "403":
                description: Forbidden Call
            "404":
                description: no Task was found.
            "406":
                description: Query Error
            "409":
                description: Task Conflict, a constraint was violated
        """
        # get query parameters
        query = self.query_parameters(request=self.request)
        # Default launch a task on Queue
        # no_worker = True
        # TODO: check for user permissions
        try:
            task, program = await self.check_task()
        except TaskDefinition as ex:
            headers = {"X-STATUS": "Error", "X-MESSAGE": ex}
            msg = {"state": "Failed", "message": f"Error: {ex}", "status": 400}
            return self.error(response=msg, headers=headers, status=400)
        try:
            task = await self.get_task(task, program, **query)
        except TaskException as ex:
            headers = {"X-STATUS": "Error", "X-MESSAGE": ex}
            msg = {"state": "Failed", "message": f"Error: {ex}", "status": 400}
            return self.error(response=msg, headers=headers, status=400)
        try:
            result = await self.launch_task(task)
            return await self.task_output(result)
        except Exception as err:  # pylint: disable=W0703
            headers = {"X-STATUS": "Error", "X-MESSAGE": err}
            msg = {"state": "Failed", "message": f"Error: {err}", "status": 400}
            return self.error(response=msg, headers=headers, status=400)

    async def post(self):
        """
        GET Method.
        description: Executing a Task and returning the result
        tags:
        - tasks
        - DataIntegration
        consumes:
        - application/json
        produces:
        - application/json
        responses:
            "200":
                description: Existing Task was executed.
            "202":
                description: Task was accepted to queue (no return)
            "204":
                description: No data was found
            "400":
                description: Task Failed to execute
            "403":
                description: Forbidden Call
            "404":
                description: no Task was found.
            "406":
                description: Query Error
            "409":
                description: Task Conflict, a constraint was violated
        """
        # get post Data
        data = await self.post_data()
        # get query parameters
        query = self.query_parameters(request=self.request)
        # flag for direct download:
        direct_download = query.get("direct_download", False)
        # Default launch a task on Queue
        # TODO: check for user permissions
        try:
            params = {**query, **data}
        except (KeyError, TypeError):
            params = data
        try:
            task, program = await self.check_task()
        except TaskDefinition as ex:
            headers = {"X-STATUS": "Error", "X-MESSAGE": ex}
            msg = {"state": "Failed", "message": f"Error: {ex}", "status": 400}
            return self.error(response=msg, headers=headers, status=400)
        try:
            task = await self.get_task(task, program, **params)
        except TaskException as ex:
            headers = {"X-STATUS": "Error", "X-MESSAGE": ex}
            msg = {"state": "Failed", "message": f"Error: {ex}", "status": 400}
            return self.error(response=msg, headers=headers, status=400)
        try:
            result = await self.launch_task(task)
            return await self.task_output(result, direct_download=direct_download)
        except (DataNotFound, FileNotFound) as ex:
            headers = {"X-STATUS": "Not Found", "X-MESSAGE": f"Data not Found: {ex}"}
            return self.no_content(headers=headers)
        except Exception as err:  # pylint: disable=W0703
            headers = {"X-STATUS": "Error", "X-MESSAGE": err}
            msg = {"state": "Failed", "message": f"Error: {err}", "status": 400}
            return self.error(response=msg, headers=headers, status=400)

    async def task_output(self, resultset: Any, direct_download: bool = False) -> web.Response:
        ## TODO: making output pluggable like QuerySource
        response = None
        buffer = None
        print(f"TaskService: task_output: {resultset!r}", type(resultset))
        if resultset is None:
            # no data found
            return self.no_content()
        elif isinstance(resultset, dict):
            # if resultset is a dict, we return it as JSON
            buffer = resultset
            response = self.get_response()
            buffer = bytes(self._json.dumps(buffer), "utf-8")
        elif isinstance(resultset, str):
            buffer = resultset
            response = self.get_response()
            buffer = bytes(buffer, "utf-8")
        elif isinstance(resultset, (PurePath, PosixPath)):
            # TODO: use Mime Type to determine the content type
            if direct_download:
                # if direct download, we need to return the file
                response = web.FileResponse(resultset)
                response.headers["Content-Disposition"] = (
                    f'attachment; filename="{resultset.name}"'
                )
            else:
                # open as bytes and send as stream
                try:
                    async with aiofiles.open(resultset, "rb") as file:
                        buffer = await file.read()
                except FileNotFoundError as ex:
                    raise FileNotFound(f"File not found: {resultset}") from ex
                response = self.get_response()
        elif isinstance(resultset, (bytes, bytearray)):
            buffer = resultset
            response = self.get_response()
        elif isinstance(resultset, pd.DataFrame):
            buffer = resultset.to_json(orient="records")
            response = self.get_response()
            buffer = bytes(buffer, "utf-8")
        return await self.stream_response(response, buffer)

    def get_response(self) -> web.Response:
        response = StreamResponse(
            status=200,
            reason="OK",
            headers={
                "Pragma": "public",  # required,
                "Expires": "0",
                "Connection": "keep-alive",
                "Cache-Control": "must-revalidate, post-check=0, pre-check=0",
                "Content-Type": "application/json",
                "X-APPLICATION": "QuerySource",
            },
        )
        response.enable_compression(force=web.ContentCoding.gzip)
        return response

    async def stream_response(
        self, response: web.StreamResponse, data: Any
    ) -> web.StreamResponse:
        content_length = len(data)
        response.content_length = content_length
        chunk_size = 16384
        response.headers["Content-Range"] = f"bytes 0-{chunk_size}/{content_length}"
        try:
            i = 0
            await response.prepare(self.request)
            while True:
                chunk = data[i: i + chunk_size]
                i += chunk_size
                if not chunk:
                    break
                await response.write(chunk)
                await response.drain()
            await response.write_eof()
            return response
        except Exception as ex:  # pylint: disable=W0703
            return self.error(
                message="Error Starting Stream Transmision", exception=ex, status=500
            )
