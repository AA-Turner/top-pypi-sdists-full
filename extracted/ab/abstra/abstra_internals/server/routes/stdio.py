import flask
import flask_sock

from abstra_internals.controllers.execution.execution_stdio import BroadcastController
from abstra_internals.server.socket_listener import serve_listener_websocket


def get_editor_bp(_):
    bp = flask.Blueprint("editor_stdio", __name__)
    sock = flask_sock.Sock(bp)

    @sock.route("/listen")
    def _websocket(ws: flask_sock.Server):
        serve_listener_websocket(
            ws,
            thread_name="StdioWebSocket",
            registry=BroadcastController,
        )

    return bp
