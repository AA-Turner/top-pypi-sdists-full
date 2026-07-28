import flask
import flask_sock

from abstra_internals.controllers.editor_restart import EditorRestartController
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
        # On web this stages the new version into an inactive slot (no restart —
        # the user restarts later via /restart). On non-web it upgrades in place
        # and restarts, so the process may exit before responding — the frontend
        # expects the drop and reconnects. On Windows it opens the release notes.
        EditorUpdateController.trigger_update()
        # Reached only on the staged (deferred) path — the immediate path exits
        # the process above. Push the fresh state so the button flips from
        # "Update Abstra" to "Restart editor" without waiting for a reconnect.
        EditorStatusEventController.broadcast()
        return {"success": True}

    @bp.post("/restart")
    @editor_usage
    def _restart():
        # Apply whatever is pending (flip the staged slot if any) and restart.
        # The process exits before responding — the frontend shows the overlay
        # and reconnects.
        EditorRestartController.restart_now()
        return {"success": True}

    return bp
