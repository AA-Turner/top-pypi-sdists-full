from importlib.metadata import PackageNotFoundError

import flask

from abstra_internals.contracts_generated import (
    AbstraLibApiEditorWorkspaceTestDataPostRequest,
    AbstraLibApiEditorWorkspaceTestDataPostResponse,
    AbstraLibApiEditorWorkspaceVersionGetResponse,
)
from abstra_internals.controllers.main import MainController
from abstra_internals.settings import Settings
from abstra_internals.usage import editor_usage
from abstra_internals.utils.packages import get_local_package_version


def get_editor_bp(controller: MainController):
    bp = flask.Blueprint("editor_workspace", __name__)

    @bp.get("/")
    @editor_usage
    def _get_workspace():
        return controller.get_workspace().as_dict

    @bp.put("/")
    @editor_usage
    def _update_workspace():
        if not flask.request.json:
            flask.abort(400)
        controller.update_workspace(flask.request.json)
        return controller.get_workspace().as_dict

    @bp.get("/root")
    @editor_usage
    def _get_workspace_root_path():
        return str(Settings.root_path.absolute())

    @bp.get("/version")
    def _get_abstra_version():
        try:
            version = str(get_local_package_version("abstra"))
        except PackageNotFoundError:
            version = "0.0.0"
        return AbstraLibApiEditorWorkspaceVersionGetResponse(version=version).to_dict()

    @bp.get("/read-test-data")
    @editor_usage
    def _read_test_data():
        return controller.read_test_data()

    @bp.post("/write-test-data")
    @editor_usage
    def _write_test_data():
        if not flask.request.json:
            flask.abort(400)
        req = AbstraLibApiEditorWorkspaceTestDataPostRequest.from_dict(
            flask.request.json
        )
        controller.write_test_data(req.test_data)
        return AbstraLibApiEditorWorkspaceTestDataPostResponse(success=True).to_dict()

    return bp
