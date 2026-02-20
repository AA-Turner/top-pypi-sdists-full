import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.repositories.project.project import AgentStage
from abstra_internals.usage import editor_usage
from abstra_internals.utils import is_it_true


def get_editor_bp(controller: MainController):
    bp = flask.Blueprint("editor_agents", __name__)

    @bp.get("/")
    @editor_usage
    def _get_agents():
        return [a.editor_dto for a in controller.get_agents()]

    @bp.get("/<path:id>")
    @editor_usage
    def _get_agent(id: str):
        agent = controller.get_agent(id)
        if not agent:
            flask.abort(404)
        return agent.editor_dto

    @bp.post("/")
    @editor_usage
    def _create_agent():
        data = flask.request.json
        if not data:
            flask.abort(400)
        title = data.get("title")
        file = data.get("file")
        if not title or not file:
            flask.abort(400)
        workflow_position = data.get("position", (0, 0))
        id = data.get("id", None)
        agent = controller.create_agent(title, file, workflow_position, id)
        return agent.editor_dto

    @bp.put("/<path:id>")
    @editor_usage
    def _update_agent(id: str):
        data = flask.request.json
        if not data:
            flask.abort(400)

        agent = controller.update_stage(id, data)
        if isinstance(agent, AgentStage):
            return agent.editor_dto
        else:
            return None

    @bp.delete("/<path:id>")
    @editor_usage
    def _delete_agent(id: str):
        remove_file = flask.request.args.get(
            "remove_file", default=False, type=is_it_true
        )
        controller.delete_stage(id, remove_file)
        return {"success": True}

    @bp.post("/<path:id>/run")
    @editor_usage
    def _run_agent(id: str):
        agent = controller.get_agent(id)

        if agent is None:
            flask.abort(404)

        if flask.request.json is None or "task_id" not in flask.request.json:
            flask.abort(400)

        task_id = flask.request.json["task_id"]

        return controller.run_agent(id, task_id)

    return bp
