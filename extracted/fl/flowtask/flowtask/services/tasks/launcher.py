"""
TaskService.

Work with managing tasks, creation, deleting, listing, etc.
"""
import uuid
from datamodel.parsers.json import (
    json_decoder
)
from navigator_session import get_session
from navigator.views import BaseView
from navigator.responses import JSONResponse
from navigator.conf import AUTH_SESSION_OBJECT
from querysource.types import strtobool
from ...exceptions import (
    TaskNotFound,
    DataNotFound,
    TaskFailed,
    FileError,
    FileNotFound,
)
from .tasks import launch_task


def is_boolean(value: str) -> bool:
    if isinstance(value, bool):
        return value
    try:
        return strtobool(value)
    except ValueError:
        return False


class TaskLauncher(BaseView):
    _logger_name = "TaskLauncher"

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

    async def post(self):
        """
        POST Method.
        description: Executing a Task
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
        # get the URL parameters
        params = self.get_args()
        # get post Data
        if self.request.can_read_body:
            if self.request.content_type == "application/json":
                try:
                    data = await self.request.json(loads=json_decoder)
                except ValueError:
                    headers = {
                        "X-STATUS": "Error",
                        "X-MESSAGE": "Resource Error: Invalid JSON Data",
                    }
                    msg = {
                        "state": "Failed",
                        "message": "Error: Invalid JSON Data",
                        "status": 400,
                    }
                    return self.error(response=msg, headers=headers, status=400)
            else:
                data = await self.post_data()
        else:
            data = {}
        # Default launch a task on Queue
        longrunner = True
        ## Getting User Information:
        try:
            usr = await get_session(self.request)
            user = self.get_user(usr)
        except (TypeError, ValueError):
            user = None
        self.logger.notice(f"Task User: {user}")
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
                return self.error(response=msg, headers=headers, status=400)
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
                return self.error(response=msg, headers=headers, status=400)
        try:
            try:
                longrunner = is_boolean(data["long_running"])
                del data["long_running"]
            except KeyError:
                pass
            try:
                longrunner = is_boolean(params["long_running"])
                del params["long_running"]
            except KeyError:
                pass
            try:
                no_worker = is_boolean(data["no_worker"])
                del data["no_worker"]
            except KeyError:
                no_worker = False
            self.logger.debug(
                f"Long Runner: {longrunner}, No Using Workers: {no_worker}"
            )
            priority = data.pop("priority", "low")
            # cannot update or insert a Task, we need to Run that task
            result = {}
            args = {}
            if isinstance(params, dict):
                args = params
            if data:
                args = {**args, **data}
            task_uuid = uuid.uuid4()
            print('Launching Task: ', program, task_id, args)
            uid, action, result = await launch_task(
                program_slug=program,
                task_id=task_id,
                loop=self._loop,
                task_uuid=task_uuid,
                queued=longrunner,
                no_worker=no_worker,
                priority=priority,
                userid=user,
                **args,
            )
            if isinstance(result, BaseException):
                state = 400
                result = f"{result!s}"
            elif 'exception' in result:
                state = 400
                response = {
                    "message": str(result["exception"]),
                    "error": 400,
                    "task_execution": task_uuid,
                    "result": result['error'],
                    "task_uuid": uid,
                }
                headers = {
                    "X-STATUS": "Task Error",
                    "X-MESSAGE": f"Execution of Task {program}.{task_id} on {action}",
                    "X-ERROR": str(result["error"]),
                }
            else:
                if action == "Queued":
                    state = 202
                else:
                    state = 200
                response = {
                    "message": f"Task {program}.{task_id} was {action}",
                    "task": f"{program}.{task_id}",
                    "task_execution": task_uuid,
                    "result": result,
                    "task_uuid": uid,
                }
                headers = {
                    "X-STATUS": "Task OK",
                    "X-MESSAGE": f"Execution of Task {program}.{task_id} on {action}",
                }
            try:
                return JSONResponse(response, status=state, headers=headers)
            except Exception as e:
                print("ERROR: ", e)
        except DataNotFound as err:
            error = f"Error: Data not found {program}.{task_id}"
            msg = {"message": str(error), "error": 404}
            return self.error(response=msg, exception=err, status=404)
        except TaskNotFound as err:
            error = f"Error: Task not found {program}.{task_id}"
            msg = {"message": str(error)}
            return self.error(response=msg, exception=err, status=401)
        except TaskFailed as err:
            error = f"Error on Task {program}.{task_id} Failed"
            msg = {"message": str(error)}
            return self.error(response=msg, exception=err, status=406)
        except (FileNotFound, FileError) as err:
            error = f"Error on Task {program}.{task_id} File Not Found: {err}"
            msg = {"message": str(error)}
            return self.error(response=msg, exception=err, status=404)
        except Exception as err:
            error = f"Uncaught exception on Task {program}.{task_id}"
            msg = {"message": str(error)}
            return self.critical(reason=msg, exception=err, status=500)
