import mimetypes
from typing import Optional

import flask
import jwt as pyjwt

from abstra_internals.controllers.main import MainController
from abstra_internals.entities.execution_context import (
    extract_flask_request,
)
from abstra_internals.environment import CLOUD_API_PROD_SHARED_TOKEN
from abstra_internals.repositories.project.project import PageStage
from abstra_internals.server.routes.page_preview import build_standalone_preview_html
from abstra_internals.settings import Settings
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

        position: Optional[tuple[int, int]] = None
        if data.get("position") and len(data["position"]) >= 2:
            position = (int(data["position"][0]), int(data["position"][1]))

        page = controller.create_stage(
            "page", data["title"], data["file"], position, data.get("id")
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

    @bp.get("/<path:id>/run/<path:filename>")
    def _page_static(id: str, filename: str):
        token = flask.request.args.get("token")
        if not token:
            flask.abort(403)

        try:
            payload = pyjwt.decode(
                token, key=CLOUD_API_PROD_SHARED_TOKEN, algorithms=["HS256"]
            )
        except (pyjwt.ExpiredSignatureError, pyjwt.InvalidTokenError):
            flask.abort(403)

        if payload.get("asset") != filename:
            flask.abort(403)

        file_path = (Settings.root_path / filename).resolve()
        if not file_path.is_relative_to(Settings.root_path) or not file_path.is_file():
            flask.abort(404)

        mimetypes.add_type("application/javascript", ".js")
        mimetypes.add_type("text/css", ".css")
        return flask.send_file(file_path)

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

        body = result["body"]
        content_type = (result["headers"] or {}).get("Content-Type", "") or ""
        if "text/html" in content_type:
            endpoint = flask.request.full_path.rstrip("?")
            body = build_standalone_preview_html(
                body,
                auth_token=user_jwt,
                endpoint=endpoint,
                execution_id=result.get("executionId"),
            )

        resp = flask.Response(
            status=result["status"],
            response=body,
            headers=result["headers"],
        )
        if result.get("executionId"):
            resp.headers["X-Execution-Id"] = result["executionId"]
        return resp

    return bp
