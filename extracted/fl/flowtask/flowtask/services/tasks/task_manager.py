"""
TaskManager.

Work with managing tasks, creation, deleting, listing, etc.
"""
import asyncio
import json
import os
import datetime
import uuid
from functools import partial
from uuid import UUID
import logging
import ast
from aiohttp import web
from navigator.views import DataView
from asyncdb.utils.encoders import BaseEncoder, DefaultEncoder
from querysource.utils.functions import format_date
from .tasks import task_state, execute_task, launch_task
from ...exceptions import (
    NotSupported,
    ComponentError,
    TaskNotFound,
    TaskDefinition,
    TaskFailed,
    FileError,
    FileNotFound,
)


def is_boolean(value: str) -> bool:
    if isinstance(value, bool):
        return value
    try:
        return ast.literal_eval(value)
    except ValueError:
        return False


class TaskManager(DataView):
    async def get(self):
        """
        GET Method.
        ---
        description: get all tasks, or a task by ID (or get status of execution)
        tags:
        - tasks
        - DataIntegration
        consumes:
        - application/json
        produces:
        - application/json
        responses:
            "200":
                description: Existing Task was retrieved.
            "403":
                description: Forbidden Call
            "404":
                description: No Task(s) were found
            "406":
                description: Query Error
        """
        try:
            sql = "SELECT * FROM {program}.tasks"
            await self.connect(self.request)
            params = self.get_args()
            print(params, sql)
            # try:
            #     session = self.request['session']
            # except KeyError:
            #     return self.error(request=self.request, response="Unknown User", state=403)
            try:
                program = params["program"]
            except KeyError:
                program = os.environ.get("APP_PROGRAM_SLUG", "troc")
            try:
                task = params["task_id"]
            except KeyError:
                task = None
            sql = sql.format(program=program)
            print(sql)
            if task is not None:
                sql = "{sql} WHERE task = '{id}' AND enabled = true".format(
                    sql=sql, id=task
                )
            print("SQL IS ", sql)
            try:
                result = await self.query(sql)
            except Exception as e:
                msg = {"error": str(e), "exception": str(e.__class__)}
                return self.error(
                    request=self.request, response=msg, exception=e, state=400
                )
            if result:
                data = []
                for row in result:
                    data.append(dict(row))
                for elements in data:
                    for key, value in elements.items():
                        elements[key] = (
                            str(value)
                            if isinstance(
                                value, (UUID, datetime.time, datetime.datetime)
                            )
                            else value
                        )
                headers = {"X-STATUS": "OK", "X-MESSAGE": "Tasks List"}
                return self.json_response(response=data, headers=headers)
            else:
                if self._lasterr:
                    msg = {"error": str(self._lasterr)}
                    return self.error(
                        request=self.request,
                        response=msg,
                        exception=self._lasterr,
                        state=400,
                    )
                headers = {"X-STATUS": "EMPTY", "X-MESSAGE": "Data not Found"}
                return self.no_content(headers=headers)
        except Exception as e:
            print(e)
            return self.critical(self.request, e)
        finally:
            await self.close()

    async def post(self):
        """
        POST Method.
        description: inserting or updating a Task or executing a Task
        tags:
        - tasks
        - DataIntegration
        consumes:
        - application/json
        produces:
        - application/json
        responses:
            "200":
                description: Existing Task was updated or executed.
            "201":
                description: New Task was inserted
            "202":
                description: Task was accepted to run
            "400":
                description: Task Failed to execute
            "403":
                description: Forbidden Call
            "404":
                description: No Data was found
            "406":
                description: Query Error
            "409":
                description: Conflict, a constraint was violated
        """
        # using LOCATION header to return the URL of the API
        await self.connect(self.request)
        # get the URL parameters
        params = self.get_args()
        # get post Data
        data = await self.post_data()
        # long
        longrunner = False
        try:
            program = params["program"]
            del params["program"]
        except KeyError:
            # we need a program
            try:
                program = data["program"]
            except KeyError:
                headers = {
                    "X-STATUS": "Error",
                    "X-MESSAGE": "Resource Error: We need a Program Name",
                }
                msg = {
                    "state": "Failed",
                    "message": "Error: we need a program name",
                    "status": 400,
                }
                return self.error(
                    request=self.request, response=msg, headers=headers, state=400
                )
        try:
            task_id = params["task_id"]
            del params["task_id"]
        except KeyError:
            # we need a Task ID
            try:
                task_id = data["task_id"]
            except KeyError:
                headers = {
                    "X-STATUS": "Error",
                    "X-MESSAGE": "Resource Error: We need a Task Name",
                }
                msg = {
                    "state": "Failed",
                    "message": "Error: we need a Task ID",
                    "status": 400,
                }
                return self.error(
                    request=self.request, response=msg, headers=headers, state=400
                )
        try:
            try:
                longrunner = is_boolean(data["long_running"])
                del data["long_running"]
            except KeyError:
                try:
                    longrunner = is_boolean(params["long_running"])
                    del params["long_running"]
                except KeyError:
                    longrunner = False
            try:
                no_worker = is_boolean(data["no_worker"])
                del data["no_worker"]
            except KeyError:
                no_worker = False
            logging.debug(f"Long Runner: {longrunner}, No Worker: {no_worker}")
            # cannot update or insert a Task, we need to Run that task
            status = None
            result = {}
            try:
                # TODO: passing arguments via URL to the task
                args = {}
                if isinstance(params, dict):
                    args = params
                if data:
                    args = {**args, **data}
                task_uuid = uuid.uuid4()
                status, action, result = await launch_task(
                    program_slug=program,
                    task_id=task_id,
                    loop=self._loop,
                    task_uuid=task_uuid,
                    queued=longrunner,
                    no_worker=no_worker,
                    **args,
                )
                result = {"task": f"{program}.{task_id}", "task_execution": task_uuid}
                if action == "Executed":
                    state = 200
                else:
                    state = 202
                response = {
                    "state": state,
                    "message": "Task {}.{} was {}".format(program, task_id, action),
                    **result,
                }
                headers = {
                    "X-STATUS": "Task OK",
                    "X-MESSAGE": "Execution of Task {}.{} on {}".format(
                        program, task_id, action
                    ),
                }
                return self.json_response(
                    response=response,
                    headers=headers,
                    state=response["state"],
                    cls=BaseEncoder,
                )
            except TaskNotFound as err:
                error = "Error: on Task {}.{}".format(program, task_id)
                msg = {"message": error}
                return self.error(
                    request=self.request, response=msg, exception=err, state=401
                )
            except TaskFailed as err:
                print(err)
                error = "Error: Task {} Failed".format(task_id)
                msg = {"message": error}
                return self.error(
                    request=self.request, response=msg, exception=err, state=400
                )
            except (FileNotFound, FileError) as err:
                print(err)
                error = "Error on Task {} File Not Found: {}".format(task_id, str(err))
                msg = {"message": error}
                return self.error(
                    request=self.request, response=msg, exception=err, state=404
                )
            except Exception as err:
                print(err)
                return self.critical(request=self.request, exception=err, state=500)
            headers = {"X-STATUS": "EMPTY", "X-MESSAGE": "Data not Found"}
            return self.no_content(headers=headers)
        except Exception as e:
            print(f"Generic Error on POST Method: {e}")
            return self.critical(self.request, e)
        finally:
            await self.close()

    async def put(self):
        """
        PUT Method.
        description: inserting or updating a Task
        tags:
        - tasks
        - DataIntegration
        produces:
        - application/json
        consumes:
        - application/merge-patch+json
        - application/json
        responses:
            "200":
                description: Existing Task was updated.
            "201":
                description: New Task was inserted
            "204":
                description: success execution but no content on return (resource was deleted)
            "400":
                description: Invalid resource according data schema
            "403":
                description: Forbidden Call
            "404":
                description: No Data was found
            "406":
                description: Query Error
            "409":
                description: Conflict, a constraint was violated
        """
        pass

    async def delete(self):
        """
        DELETE Method.
        description: remove resource.
        tags:
        - tasks
        - DataIntegration
        produces:
        - application/json
        responses:
            "200":
                description: Existing Task was updated.
            "201":
                description: New Task was inserted
            "403":
                description: Forbidden Call
            "404":
                description: No Data was found
            "406":
                description: Query Error
            "409":
                description: Conflict, a constraint was violated
        """
        pass

    async def patch(self):
        """
        PATCH Method.
        description: updating partially info about a Task
        tags:
        - tasks
        - DataIntegration
        produces:
        - application/json
        responses:
            "200":
                description: Existing Task was updated.
            "201":
                description: New Task was inserted
            "304":
                description: Task not modified, its currently the actual version of Task
            "403":
                description: Forbidden Call
            "404":
                description: No Data was found
            "406":
                description: Query Error
            "409":
                description: Conflict, a constraint was violated
        """
        pass

    async def head(self):
        pass
