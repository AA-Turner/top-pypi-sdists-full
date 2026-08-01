import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.controllers.web_editor import WebEditorController


def get_web_editor_bp(main_controller: MainController):
    bp = flask.Blueprint("webEditor", __name__)
    editorAuthController = WebEditorController()

    @bp.get("/")
    def _inspect():
        return editorAuthController.inspect().to_dict()

    @bp.post("/repair-api-key")
    def _repair_api_key():
        # This blueprint is mounted under the guarded editor blueprint, so the
        # cookie has already been validated; it is read here to forward the
        # session identity to cloud-api, which is the only credential the pod can
        # still prove when its API key is the revoked one.
        repaired = editorAuthController.repair_api_key(
            flask.request.cookies.get("editor_auth")
        )
        if not repaired:
            return {"repaired": False}, 502
        return {"repaired": True}

    return bp
