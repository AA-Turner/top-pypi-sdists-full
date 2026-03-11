import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.usage import editor_usage


def get_editor_bp(controller: MainController):
    bp = flask.Blueprint("editor_stages", __name__)

    @bp.get("/")
    @editor_usage
    def _get_stages():
        return [f.editor_dto for f in controller.list_all_stages()]

    return bp
