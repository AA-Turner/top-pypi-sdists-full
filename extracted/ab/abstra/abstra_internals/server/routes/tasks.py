import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.controllers.tasks import DataRequest, TasksController
from abstra_internals.usage import editor_usage


def get_editor_bp(main_controller: MainController) -> flask.Blueprint:
    controller = TasksController(repositories=main_controller.repositories)
    bp = flask.Blueprint("tasks", __name__)

    @bp.post("/list")
    def _get_all_tasks():
        if flask.request.json is None:
            flask.abort(400)
        req = DataRequest.from_dict(flask.request.json)
        result = controller.list_tasks(
            stage_ids=req.filter.stage,
            status=req.filter.status,
            start_date=req.filter.start_date,
            end_date=req.filter.end_date,
            limit=req.limit,
            offset=req.offset,
        )
        return {
            "tasks": [task.dump() for task in result["tasks"]],
            "totalCount": result["total"],
        }

    @bp.get("/<stage_id>")
    @editor_usage
    def _get_tasks(stage_id: str):
        result = controller.list_tasks(stage_ids=[stage_id], direction="sent_to")
        return {
            "tasks": [task.dump() for task in result["tasks"]],
            "totalCount": result["total"],
        }

    @bp.get("/<stage_id>/sent")
    def _get_sent_tasks(stage_id: str):
        result = controller.list_tasks(stage_ids=[stage_id], direction="sent_by")
        return {
            "tasks": [task.dump() for task in result["tasks"]],
            "totalCount": result["total"],
        }

    @bp.put("/<task_id>/status")
    @editor_usage
    def _update_task_status(task_id: str):
        if not flask.request.json:
            flask.abort(400)
        status = flask.request.json.get("status")
        controller.update_task_status(task_id, status)
        return {"success": True}

    @bp.post("/")
    @editor_usage
    def _create_task():
        if not flask.request.json:
            flask.abort(400)
        stage_id = flask.request.json.get("stage_id")
        payload = flask.request.json.get("payload")
        name = flask.request.json.get("name")
        task = controller.create_task(name, stage_id, payload)
        return task.dump()

    @bp.delete("/clear")
    @editor_usage
    def _clear_tasks():
        controller.clear_tasks()
        return {"success": True}

    return bp
