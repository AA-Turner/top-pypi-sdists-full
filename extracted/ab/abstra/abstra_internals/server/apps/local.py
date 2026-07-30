import threading
from urllib.parse import quote

import flask
import flask_cors

from abstra_internals.controllers.main import MainController
from abstra_internals.environment import (
    CLOUD_CONSOLE_URL,
    EDITOR_MODE,
    EXTERNAL_PLAYER_URL,
    PROJECT_ID,
)
from abstra_internals.server.blueprints.editor import (
    get_editor_auth_bp,
    get_editor_bp,
    set_editor_auth_cookie,
)
from abstra_internals.server.blueprints.player import get_player_bp
from abstra_internals.server.utils import send_from_dist
from abstra_internals.services.editor_auth import EditorAuthRenewer
from abstra_internals.services.jwt import decode_jwt


def _console_web_editor_url() -> str:
    url = f"{CLOUD_CONSOLE_URL}/projects/{PROJECT_ID}/web-editor"
    path = flask.request.full_path.rstrip("?")
    if path.startswith("/") and not path.startswith("//"):
        url += f"?redirect={quote(path, safe='')}"
    return url


def _guard():
    if EDITOR_MODE == "local":
        return None  # No guard for local development

    token = flask.request.cookies.get("editor_auth")

    if token and decode_jwt(token, aud=f"web-editor-{PROJECT_ID}"):
        return None

    # Missing/expired token on a browser navigation: send the user back to
    # the console, which re-mints the token and redirects into the editor at
    # the same path — instead of leaving them on a broken session. XHR/fetch
    # callers keep getting JSON errors.
    accept = flask.request.headers.get("Accept", "")
    if flask.request.method == "GET" and accept.startswith("text/html"):
        return flask.redirect(_console_web_editor_url())

    if not token:
        return flask.make_response({"ok": False, "error": "No token provided"}, 401)

    return flask.make_response({"ok": False, "error": "Invalid token"}, 403)


def _register_editor_auth_renewal(app: flask.Flask, controller: MainController) -> None:
    """Sliding renewal of the editor_auth cookie (web editor only).

    When the request's token has less than RENEW_THRESHOLD_SECONDS left, a
    background renewal is kicked off; once it completes, the next response
    re-sets the cookie with the fresh token. Active users therefore never hit
    the 7-day expiration."""
    renewer = EditorAuthRenewer(
        renew_fn=controller.repositories.editor_auth.renew_token
    )

    @app.after_request
    def _renew_editor_auth(response: flask.Response) -> flask.Response:
        if EDITOR_MODE == "local":
            return response

        token = flask.request.cookies.get("editor_auth")
        if not token:
            return response

        fresh_token = renewer.fresh_token_for(token)
        if fresh_token:
            set_editor_auth_cookie(response, fresh_token)
            return response

        claims = decode_jwt(token, aud=f"web-editor-{PROJECT_ID}")
        exp = claims.get("exp") if claims else None
        if exp:
            renewer.maybe_renew(token, exp)

        return response


def get_local_app(controller: MainController) -> flask.Flask:
    app = flask.Flask(__name__)
    app.config["SOCK_SERVER_OPTIONS"] = {"subprotocols": ["default"]}
    app.url_map.strict_slashes = False
    flask_cors.CORS(app, supports_credentials=True)

    @app.route("/_healthcheck")
    def _healthcheck():
        return "ok"

    # Must be public
    editor_auth = get_editor_auth_bp()
    app.register_blueprint(editor_auth, url_prefix="/_editor/auth")

    editor = get_editor_bp(controller)
    editor.before_request(lambda: _guard())
    app.register_blueprint(editor, url_prefix="/_editor")

    # Web editor with an external (cloud-api-served) player: the pod serves only
    # editor routes — player traffic goes to ABSTRA_EXTERNAL_PLAYER_URL instead
    # of competing with the editor for this pod's resources.
    if not (EDITOR_MODE == "web" and EXTERNAL_PLAYER_URL):
        player = get_player_bp(controller)
        player.before_request(lambda: _guard())
        app.register_blueprint(player)
    else:
        # The editor SPA (served at /_editor) references its bundle at
        # root-absolute /assets/{hash} — historically served by the player
        # blueprint's catch-all. Keep a minimal statics route for it; missing
        # files 404 (no HTML fallback) so the pod's proxy can distinguish
        # editor assets from player-SPA assets.
        @app.get("/assets/<path:filename>")
        def _dist_assets(filename: str):
            return send_from_dist(f"assets/{filename}")

    _register_editor_auth_renewal(app, controller)

    @app.before_request
    def rename_thread():
        curr = threading.current_thread()
        curr.name = f"FlaskThread[{flask.request.path}]"

    return app
