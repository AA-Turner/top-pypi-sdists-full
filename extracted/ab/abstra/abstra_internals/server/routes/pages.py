import flask

from abstra_internals.constants import get_public_dir
from abstra_internals.controllers.main import MainController
from abstra_internals.entities.execution_context import (
    extract_flask_request,
)
from abstra_internals.repositories.project.project import PageStage
from abstra_internals.usage import editor_usage
from abstra_internals.utils import is_it_true


def get_editor_bp(controller: MainController):
    bp = flask.Blueprint("editor_pages", __name__)

    @bp.get("/<path:id>")
    @editor_usage
    def _get_page(id: str):
        page = controller.get_page_stage(id)
        if not page:
            flask.abort(404)
        return page.editor_dto

    @bp.get("/")
    @editor_usage
    def _get_pages():
        return [u.editor_dto for u in controller.get_page_stages()]

    @bp.post("/")
    @editor_usage
    def _create_page():
        if not flask.request.json:
            flask.abort(400)
        data = flask.request.json

        position: tuple[int, int] = (0, 0)
        if data.get("position") and len(data["position"]) >= 2:
            position = (int(data["position"][0]), int(data["position"][1]))

        page = controller.create_page_stage(
            data["title"], data["file"], position, data.get("id")
        )
        return page.editor_dto

    @bp.put("/<path:id>")
    @editor_usage
    def _update_page(id: str):
        if not flask.request.json:
            flask.abort(400)
        changes = flask.request.json
        changes = {k: v for k, v in changes.items() if v is not None}

        page = controller.update_stage(id, changes)
        if isinstance(page, PageStage):
            return page.editor_dto
        else:
            return None

    @bp.delete("/<path:id>")
    @editor_usage
    def _delete_page(id: str):
        remove_file = flask.request.args.get(
            "remove_file", default=False, type=is_it_true
        )
        controller.delete_stage(id, remove_file)
        return {"success": True}

    @bp.get("/<path:id>/run/_static/<path:filename>")
    def _page_static(id: str, filename: str):
        return flask.send_from_directory(get_public_dir(), filename)

    @bp.route("/<path:id>/run", methods=["POST", "GET", "PUT", "DELETE", "PATCH"])
    @editor_usage
    def _run_page(id: str):
        page = controller.get_page_stage(id)

        if not page:
            flask.abort(404)

        # Try Authorization header first (from page function calls via meta tag),
        # fall back to editor_auth cookie (from initial page load)
        auth_header = flask.request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            user_jwt = auth_header[7:]
        else:
            user_jwt = flask.request.cookies.get("editor_auth")
        page_execution_id = flask.request.headers.get("X-Page-Execution-Id")
        result = controller.run_page_stage(
            id,
            extract_flask_request(flask.request),
            user_jwt=user_jwt,
            page_execution_id=page_execution_id,
        )

        resp = flask.Response(
            status=result["status"],
            response=result["body"],
            headers=result["headers"],
        )
        if result.get("executionId"):
            resp.headers["X-Execution-Id"] = result["executionId"]
        return resp

    return bp
