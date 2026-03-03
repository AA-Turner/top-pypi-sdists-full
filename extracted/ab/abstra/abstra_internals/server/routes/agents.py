import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.usage import editor_usage


def get_editor_bp(controller: MainController):
    bp = flask.Blueprint("editor_agents", __name__)

    @bp.get("/")
    @editor_usage
    def _get_agents():
        # Agents have been migrated to scripts via Migration018.
        # This endpoint is kept for backward compatibility but returns empty.
        return []

    @bp.get("/<path:id>")
    @editor_usage
    def _get_agent(id: str):
        flask.abort(404)

    @bp.post("/")
    @editor_usage
    def _create_agent():
        flask.abort(410)

    @bp.put("/<path:id>")
    @editor_usage
    def _update_agent(id: str):
        flask.abort(410)

    @bp.delete("/<path:id>")
    @editor_usage
    def _delete_agent(id: str):
        flask.abort(410)

    @bp.post("/<path:id>/run")
    @editor_usage
    def _run_agent(id: str):
        flask.abort(410)

    return bp
