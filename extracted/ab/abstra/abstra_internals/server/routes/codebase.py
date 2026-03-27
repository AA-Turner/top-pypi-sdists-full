import json
import os

import flask
import flask_sock

from abstra_internals.contracts_generated import (
    AbstraLibApiEditorCodebaseCheckFileGetResponse,
    AbstraLibApiEditorCodebaseCheckFilesPostRequest,
    AbstraLibApiEditorCodebaseFilesPatchRequest,
    AbstraLibApiEditorCodebaseFilesPutRequest,
    AbstraLibApiEditorCodebaseInitFilePostRequest,
    AbstraLibApiEditorCodebaseInitFilePostResponse,
    AbstraLibApiEditorCodebaseTypeCheckPostResponse,
)
from abstra_internals.controllers.codebase import CodebaseController
from abstra_internals.controllers.codebase_events import CodebaseEventController
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.factory import Repositories
from abstra_internals.repositories.project.project import Project
from abstra_internals.settings import Settings
from abstra_internals.utils.code_check import code_check
from abstra_internals.utils.zip import zip_folder_to_buffer


def get_editor_bp(repos: Repositories):
    bp = flask.Blueprint("editor_files", __name__)
    controller = CodebaseController(repos)
    sock = flask_sock.Sock(bp)

    def _wait_inactivity(ws: flask_sock.Server):
        keep_alive_interval = 30
        while True:
            try:
                msg = ws.receive(timeout=keep_alive_interval + 10)
                if msg is None:
                    break
            except Exception:
                break

    @sock.route("/events")
    def _websocket(ws: flask_sock.Server):
        try:
            ws.thread.name = "CodebaseEventsWebSocket"
            CodebaseEventController.register(ws)
            _wait_inactivity(ws)
        except Exception as e:
            AbstraLogger.capture_exception(e)
        finally:
            CodebaseEventController.unregister(ws)

    @bp.get("/files")
    def _list_files():
        path = flask.request.args.get("path")
        mode = flask.request.args.get("mode", "file")
        if mode not in {"file", "image", "python-file", "module"}:
            flask.abort(400)
        files = controller.list_files(path, mode=mode)
        return [f.to_dict() for f in files]

    @bp.get("/files-zip/<path:path>")
    def _get_folder_zip(path):
        folder = Settings.root_path / path
        resolved = folder.resolve()

        if not resolved.is_relative_to(Settings.root_path.resolve()):
            flask.abort(400, description="Path is outside project root")

        if not resolved.is_dir():
            flask.abort(404, description="Folder not found")

        buf = zip_folder_to_buffer(resolved)
        folder_name = resolved.name or "files"
        return flask.send_file(
            buf,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"{folder_name}.zip",
        )

    @bp.post("/init-file")
    def _init_file():
        if not flask.request.json:
            flask.abort(400)
        req = AbstraLibApiEditorCodebaseInitFilePostRequest.from_dict(
            flask.request.json
        )
        controller.init_file(req.path, req.type)
        return AbstraLibApiEditorCodebaseInitFilePostResponse(success=True).to_dict()

    @bp.get("/check-file")
    def _check_file():
        path = flask.request.args.get("path")
        if not path:
            flask.abort(400)
        result = controller.check_file(path)
        return AbstraLibApiEditorCodebaseCheckFileGetResponse(
            exists=result["exists"]
        ).to_dict()

    @bp.post("/check-files")
    def _check_files():
        if not flask.request.json:
            flask.abort(400)
        req = AbstraLibApiEditorCodebaseCheckFilesPostRequest.from_dict(
            flask.request.json
        )
        return controller.check_files(req.paths)

    @bp.get("/read-file")
    def _read_absolute_file():
        path = flask.request.args.get("path")
        if not path:
            flask.abort(400, description="Missing 'path' query parameter")
        return controller.get_file(path)

    @bp.get("/files/<path:path>")
    def _get_file(path):
        return controller.get_file(path)

    @bp.put("/files/<path:path>")
    def _edit_file(path):
        json = flask.request.json
        if json is None:
            flask.abort(400)
        req = AbstraLibApiEditorCodebaseFilesPutRequest.from_dict(json)

        return controller.edit_file(path, req).to_dict()

    @bp.post("/files/<path:path>")
    def _create_file(path):
        content = flask.request.get_data()
        overwrite = flask.request.args.get("overwrite", "false").lower() == "true"
        try:
            return controller.create_file(path, content, overwrite).to_dict()
        except FileExistsError as e:
            flask.abort(409, description=str(e))

    @bp.delete("/files/<path:path>")
    def _delete_file(path: str):
        parts = list(os.path.split(path))
        return controller.delete_file(parts).to_dict()

    @bp.patch("/files")
    def _rename_file():
        try:
            json = flask.request.json
            if json is None:
                AbstraLogger.error("rename_file: No JSON body in request")
                flask.abort(400, description="No JSON body provided")

            AbstraLogger.debug(f"rename_file: Received JSON: {json}")
            req = AbstraLibApiEditorCodebaseFilesPatchRequest.from_dict(json)
            result = controller.rename_file(req.path_parts, req.new_path_parts)
            return result.to_dict()
        except Exception as e:
            AbstraLogger.error(f"rename_file failed: {e}")
            flask.abort(500, description=str(e))

    @bp.post("/dir/<path:path>")
    def _mkdir(path):
        path_parts = list(os.path.split(path))
        return controller.mkdir(path_parts).to_dict()

    @bp.get("/settings")
    def _get_settings():
        return controller.settings().to_dict()

    @bp.post("/type-check/<path:path>")
    def _type_check(path: str):
        file_path = Settings.root_path.joinpath(path)
        result = code_check(file_path)
        return AbstraLibApiEditorCodebaseTypeCheckPostResponse(
            success=result.success, stdout=result.stdout, stderr=result.stderr
        ).to_dict()

    @bp.post("/validate-abstra-json")
    def _validate_abstra_json():
        content = flask.request.get_data(as_text=True)
        if not content:
            return {"valid": False, "error": "Empty content provided"}

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            return {"valid": False, "error": f"Invalid JSON syntax: {e}"}

        try:
            Project._Project__from_dict(data)  # type: ignore
            return {"valid": True, "error": None}
        except KeyError as e:
            return {"valid": False, "error": f"Missing required field: {e}"}
        except TypeError as e:
            return {"valid": False, "error": f"Invalid field type: {e}"}
        except Exception as e:
            return {"valid": False, "error": f"Invalid abstra.json structure: {e}"}

    return bp
