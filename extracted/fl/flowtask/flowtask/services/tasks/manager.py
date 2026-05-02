"""
TaskManager.

Task Management: creation, deleting, listing, etc.
"""
import re
import uuid
import io
import traceback
from contextlib import redirect_stdout
import pandas as pd
from asyncdb.exceptions import NoDataFound
from navigator_session import get_session
from navigator.views import BaseView
from navigator.responses import JSONResponse
from ...models import TaskModel
# Getting Task
from ...tasks.task import Task
from ...storages import MemoryTaskStorage
from ...utils.stats import TaskMonitor

def is_uuid(s):
    try:
        uuid.UUID(s)
        return True
    except (TypeError, ValueError):
        return False


class TaskManager(BaseView):
    """TaskManager.

    description: API Endpoint for Task Management (creation of Tasks).
    """
    def post_init(self, *args, **kwargs):
        super().post_init(*args, **kwargs)
        self.taskstorage = MemoryTaskStorage()
        self.ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    model: TaskModel = TaskModel
    _fields = [
        "task",
        "task_id",
        "task_path",
        "task_definition",
        "url",
        "attributes",
        "params",
        "enabled",
        "last_done_time",
        "last_exec_time",
        "program_id",
        "program_slug",
        "task_state",
        "traceback",
    ]

    async def session(self):
        session = None
        try:
            session = await get_session(self.request)
        except (ValueError, RuntimeError) as err:
            return self.critical(
                reason="Error Decoding Session", request=self.request, exception=err
            )
        return session

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
        qp = self.query_parameters(self.request)
        args = self.match_parameters(self.request)
        try:
            task_id = args["task_id"]
        except KeyError:
            task_id = None
        if is_uuid(task_id):
            slug = None
        else:
            slug = task_id
            task_id = None
        try:
            program_slug = args["program"]
        except KeyError:
            program_slug = None
        try:
            meta = args["meta"]
        except KeyError:
            meta = None
        try:
            if meta == ":meta":
                # returning JSON schema of Model:
                response = TaskModel.schema(as_dict=True)
                return JSONResponse(response, status=200)
        except (ValueError, TypeError) as ex:
            self.logger.warning(str(ex))
        #### getting all tasks:
        if "fields" in qp:
            args = {"fields": qp["fields"]}
        else:
            args = {"fields": self._fields}
        try:
            del qp["fields"]
        except KeyError:
            pass
        try:
            db = self.request.app["qs_connection"]
            async with await db.acquire() as conn:
                TaskModel.Meta.connection = conn
                if program_slug is not None:
                    TaskModel.Meta.schema = program_slug
                if task_id is not None:
                    result = await TaskModel.get(**{"task_id": task_id})
                elif slug and program_slug:
                    result = await TaskModel.get(
                        **{"task": slug, "program_slug": program_slug}
                    )
                elif len(qp) > 0:
                    result = await TaskModel.filter(**qp)
                else:
                    tasks = await TaskModel.all(fields=self._fields)
                    result = [row.dict() for row in tasks]
                return self.json_response(result)
        except NoDataFound as err:
            headers = {
                "X-STATUS": "EMPTY",
                "X-ERROR": str(err),
                "X-MESSAGE": f"Task {task_id}:{slug} not Found",
            }
            return self.no_content(headers=headers)
        except Exception as err:
            return self.error(reason=f"Error getting Task: {err}", exception=err)

    async def put(self):
        """
        PUT Method.
        description: Send a Task as Code directly to Task Executor.
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
                description: Task Executed
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
        try:
            body_task = await self.request.text()
            if not body_task:
                return self.no_content()
        except Exception as e:
            return self.error(
                response={
                    "message": f"Error reading body: {e}",
                    "error": e
                },
                status=400
            )
        # Then, try to validate With Task
        # generate an uuid as name:
        task_name = uuid.uuid4()
        task = Task(
            task=task_name
        )
        async with task as t:
            # Assign the Memory Storage
            t.taskstore = self.taskstorage
            stdout = io.StringIO()
            stacktrace = None
            error = None
            result = None
            stats = None
            captured_stdout = None
            if await t.start(payload=body_task):
                try:
                    with redirect_stdout(stdout):
                        # can we run the task
                        result = await t.run()
                except Exception as e:
                    result = None
                    stacktrace = traceback.format_exc()
                    error = str(e)
                captured_stdout = stdout.getvalue()
                stats = t.get_stats()
            if isinstance(result, pd.DataFrame):
                resultset = []
                resultset.append(
                    {"result": str(result)}
                )
                for column, t in result.dtypes.items():
                    resultset.append(
                        f"{column}->{t}->{result[column].iloc[0]}"
                    )
                result = resultset
            result = {
                "result": f"{result!s}",
                "error": error,
                "stacktrace": stacktrace,
                "stdout": self.ansi_escape.sub('', captured_stdout),
                "stat": stats
            }
            return JSONResponse(
                result
            )
        return self.error(
            response={
                "message": "Error reading Task body"
            },
            status=400
        )

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

    async def post(self):
        """
        PATCH Method.
        description: updating or creating tasks
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

    async def head(self):
        pass
