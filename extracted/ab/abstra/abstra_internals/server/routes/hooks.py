import flask

from abstra_internals.contracts_generated import (
    AbstraLibApiEditorHooksDeleteResponse,
    AbstraLibApiEditorHooksPostRequest,
    AbstraLibApiEditorHooksPutRequest,
)
from abstra_internals.controllers.main import MainController
from abstra_internals.entities.execution_context import (
    extract_flask_request,
)
from abstra_internals.repositories.project.project import HookStage
from abstra_internals.usage import editor_usage
from abstra_internals.utils import is_it_true


def get_editor_bp(controller: MainController):
    bp = flask.Blueprint("editor_hooks", __name__)

    @bp.get("/<path:id>")
    @editor_usage
    def _get_hook(id: str):
        hook = controller.get_hook(id)
        if not hook:
            flask.abort(404)
        return hook.editor_dto

    @bp.get("/")
    @editor_usage
    def _get_hooks():
        return [f.editor_dto for f in controller.get_hooks()]

    @bp.post("/")
    @editor_usage
    def _create_hook():
        if not flask.request.json:
            flask.abort(400)
        req = AbstraLibApiEditorHooksPostRequest.from_dict(flask.request.json)

        position: tuple[int, int] = (0, 0)
        if req.position and len(req.position) >= 2:
            position = (int(req.position[0]), int(req.position[1]))

        hook = controller.create_hook(req.title, req.file, position, req.id)
        return hook.editor_dto

    @bp.put("/<path:id>")
    @editor_usage
    def _update_hook(id: str):
        if not flask.request.json:
            flask.abort(400)
        req = AbstraLibApiEditorHooksPutRequest.from_dict(flask.request.json)

        changes = req.to_dict()
        # Remove None values to avoid overwriting with None
        changes = {k: v for k, v in changes.items() if v is not None}

        # Normalize position to a tuple, matching the POST handler
        position = changes.get("position")
        if position is not None and len(position) >= 2:
            changes["position"] = (int(position[0]), int(position[1]))

        hook = controller.update_stage(id, changes)
        if isinstance(hook, HookStage):
            return hook.editor_dto
        else:
            return None

    @bp.delete("/<path:id>")
    @editor_usage
    def _delete_hook(id: str):
        remove_file = flask.request.args.get(
            "remove_file", default=False, type=is_it_true
        )
        controller.delete_stage(id, remove_file)
        return AbstraLibApiEditorHooksDeleteResponse(success=True).to_dict()

    @bp.route("/<path:id>/run", methods=["POST", "GET", "PUT", "DELETE", "PATCH"])
    @editor_usage
    def _run_hook(id: str):
        hook = controller.get_hook(id)

        if not hook:
            flask.abort(404)

        return controller.run_hook(id, extract_flask_request(flask.request))

    return bp
