import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.logger import AbstraLogger
from abstra_internals.usage import editor_usage


def get_editor_bp(controller: MainController):
    bp = flask.Blueprint("editor_code_markers", __name__)

    @bp.post("/lint")
    @editor_usage
    def _lint_code():
        if flask.request.json is None:
            flask.abort(400)

        code = flask.request.json.get("code", "")
        file_type = flask.request.json.get("file_type", "python")

        try:
            markers = controller.code_markers_repository.get_markers(code, file_type)
            return flask.jsonify([m.to_dict() for m in markers])
        except Exception as e:
            AbstraLogger.error(f"Error getting code markers: {e}")
            return flask.jsonify([])

    return bp
