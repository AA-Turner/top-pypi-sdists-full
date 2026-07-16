import flask
import flask_sock

from abstra_internals.controllers.editor_status_events import (
    EditorStatusEventController,
)
from abstra_internals.controllers.editor_update import EditorUpdateController
from abstra_internals.server.socket_listener import serve_listener_websocket
from abstra_internals.usage import editor_usage


def get_editor_bp():
    bp = flask.Blueprint("editor_status", __name__)
    sock = flask_sock.Sock(bp)

    @sock.route("/events")
    def _editor_status_websocket(ws: flask_sock.Server):
        def _send_initial(ws: flask_sock.Server) -> None:
            ws.send(EditorStatusEventController.build_payload())

        serve_listener_websocket(
            ws,
            thread_name="EditorStatusWebSocket",
            registry=EditorStatusEventController,
            on_registered=_send_initial,
        )

    @bp.post("/update-abstra")
    @editor_usage
    def _update_abstra():
        # Upgrade the abstra package (or, on Windows, open the release notes).
        # On non-Windows this restarts the editor, so the process may exit
        # before responding — the frontend expects the drop and reconnects.
        EditorUpdateController.trigger_update()
        return {"success": True}

    return bp
