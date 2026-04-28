import json
import mimetypes
from pathlib import Path

import flask
import flask_sock
import jwt as pyjwt

from abstra_internals.constants import get_public_dir
from abstra_internals.controllers.execution.drain import (
    drain_until_response,
    normalize_response,
)
from abstra_internals.controllers.main import MainController
from abstra_internals.entities.execution_context import (
    FormContext,
    HookContext,
    JobContext,
    PageContext,
    Response,
    extract_flask_request,
)
from abstra_internals.environment import (
    BUILD_ID,
    CLOUD_API_PROD_SHARED_TOKEN,
    DRAIN_START_TIMEOUT_SECONDS,
    EDITOR_MODE,
    IS_PRODUCTION,
    OIDC_AUTHORITY,
    OIDC_CLIENT_ID,
    SHOW_WATERMARK,
)
from abstra_internals.logger import AbstraLogger
from abstra_internals.server.cache.control import Cache
from abstra_internals.server.guards.role_guard import (
    Guard,
    PathArgSelector,
    QueryArgSelector,
)
from abstra_internals.server.routes import access_control as ac_router
from abstra_internals.server.routes import auth as auth_router
from abstra_internals.server.routes import workflows as workflows_router
from abstra_internals.server.utils import send_from_dist
from abstra_internals.services.jwt import USER_AUTH_HEADER_KEY
from abstra_internals.settings import Settings
from abstra_internals.usage import player_usage
from abstra_internals.utils import check_is_url, serialize
from abstra_internals.utils.file import get_tmp_upload_dir, path2module, upload_file
from abstra_internals.utils.websockets import bind_ws_with_connection


def get_player_bp(controller: MainController):
    guard = Guard(
        controller.users_repository,
        project_repository=controller.repositories.project,
        enabled=IS_PRODUCTION,
    )
    cache = Cache(enabled=IS_PRODUCTION)

    bp = flask.Blueprint("player", __name__)
    sock = flask_sock.Sock(bp)

    auth_bp = auth_router.get_player_bp(controller)
    bp.register_blueprint(auth_bp, url_prefix="/_auth")

    workflow_bp = workflows_router.get_player_bp(controller)
    bp.register_blueprint(workflow_bp, url_prefix="/_workflows")

    access_control_bp = ac_router.get_player_bp(controller)
    bp.register_blueprint(access_control_bp, url_prefix="/_access-control")

    @bp.route("/_healthcheck")
    def _healthcheck():
        return "ok"

    @bp.get("/_workspace")
    def _get_workspace():
        auth = flask.request.headers.get(USER_AUTH_HEADER_KEY)
        return guard.filtered_workspace(auth).as_dict

    def _resolve_page(path):
        form = controller.get_form_by_path(path)
        if form:
            auth = flask.request.headers.get(USER_AUTH_HEADER_KEY)
            return {
                form.type_name: {
                    **form.browser_runner_dto,
                    "workspace": guard.filtered_workspace(auth).as_dict,
                }
            }

        page = controller.get_page_stage_by_path(path)
        if page:
            auth = flask.request.headers.get(USER_AUTH_HEADER_KEY)
            return {
                "page": {
                    "id": page.id,
                    "path": page.path,
                    "title": page.title,
                    "workspace": guard.filtered_workspace(auth).as_dict,
                }
            }

        flask.abort(404)

    @bp.get("/_pages-home")
    @player_usage
    def _get_home_page():
        return _resolve_page("")

    @bp.get("/_pages/<string:path>")
    @guard.by(PathArgSelector("path"))
    @player_usage
    def _get_page(path):
        return _resolve_page(path)

    @bp.get("/_version")
    def _get_version():
        return BUILD_ID

    @bp.get("/_settings")
    def _get_settings():
        return flask.jsonify(
            {
                "show_watermark": SHOW_WATERMARK,
                "oidc_authority": OIDC_AUTHORITY(),
                "oidc_client_id": OIDC_CLIENT_ID(),
                "editor_mode": EDITOR_MODE,
                "is_production": IS_PRODUCTION,
            }
        )

    @bp.get("/_infra/worker-capacity")
    def _get_worker_capacity():
        capacity = controller.repositories.infra.get_worker_capacity()
        if capacity is None:
            return flask.jsonify(
                {"currentWorkers": 0, "maxWorkers": 0, "isAtCapacity": False}
            )
        return flask.jsonify(
            {
                "currentWorkers": capacity.current_workers,
                "maxWorkers": capacity.max_workers,
                "isAtCapacity": capacity.is_at_capacity,
            }
        )

    @sock.route("/_socket")
    @guard.socket_by(QueryArgSelector("id"))
    def _websocket(ws: flask_sock.Server):
        context = FormContext(request=extract_flask_request(flask.request))
        connection = None

        try:
            id = flask.request.args.get("id")
            if id is None:
                return

            form = controller.get_form(id)
            if not form:
                return

            connection = controller.repositories.producer.enqueue(id, context)
            bind_ws_with_connection(ws, connection, block=True)
        except Exception as e:
            AbstraLogger.capture_exception(e)
        finally:
            if connection is not None:
                try:
                    connection.close()
                except Exception as e:
                    AbstraLogger.capture_exception(e)
            ws.close(message="Done")

    @bp.put("/_files")
    @player_usage
    def _upload_file():
        files = flask.request.files
        if len(files) == 0:
            flask.abort(400)

        return [upload_file(file) for file in files.values()]

    @bp.get("/_files/<path:path>")
    def _get_file(path):
        return flask.send_from_directory(get_tmp_upload_dir(), path)

    @bp.get("/_public/<path:path>")
    def _get_public_file(path):
        return flask.send_from_directory(get_public_dir(), path)

    @bp.get("/_assets/favicon.ico")
    @cache.assets()
    def _favicon():
        favicon_path = controller.get_workspace().favicon_url
        if not favicon_path:
            return _logo()

        if check_is_url(favicon_path):
            return flask.redirect(favicon_path)

        return send_from_dist(favicon_path, dist_folder=Settings.root_path)

    @bp.get("/_assets/logo")
    @cache.assets()
    def _logo():
        logo_path = controller.get_workspace().logo_url
        if not logo_path:
            return flask.abort(404)

        if check_is_url(logo_path):
            return flask.redirect(logo_path)

        return send_from_dist(logo_path, dist_folder=Settings.root_path)

    @bp.get("/_assets/background")
    @cache.assets()
    def _background():
        background_path = controller.get_workspace().theme

        if not background_path:
            return flask.abort(404)

        if check_is_url(background_path):
            return flask.redirect(background_path)

        return send_from_dist(background_path, dist_folder=Settings.root_path)

    @bp.route("/_hooks/<path:path>", methods=["POST", "GET", "PUT", "DELETE", "PATCH"])
    def hook_runner(path):
        hook = controller.get_hook_by_path(path)

        if not hook:
            flask.abort(404)

        if not hook.file:
            flask.abort(500)

        context = HookContext(
            request=extract_flask_request(flask.request),
            response=Response(headers={}, status=200, body=""),
        )

        connection = controller.repositories.producer.enqueue(hook.id, context)

        drain_until_response(
            connection, timeout=DRAIN_START_TIMEOUT_SECONDS
        )  # ExecutionStartedMessage

        try:
            response = normalize_response(drain_until_response(connection))

            if not response:
                flask.abort(500)
        finally:
            connection.close()

        return flask.Response(
            status=response.status,
            response=response.body,
            headers=response.headers,
        )

    def _run_page(path):
        page = controller.get_page_stage_by_path(path)

        if not page:
            flask.abort(404)

        if not page.file:
            flask.abort(500)

        # POST requests from function calls include the parent page execution ID
        page_execution_id = flask.request.headers.get("X-Page-Execution-Id")

        # Extract user JWT: Authorization header first (from page function calls),
        # fall back to editor_auth cookie (from headless browser / web editor)
        auth_header = flask.request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            user_jwt = auth_header[7:]
        else:
            user_jwt = flask.request.cookies.get("editor_auth")

        context = PageContext(
            request=extract_flask_request(flask.request),
            response=Response(headers={}, status=200, body=""),
            page_path=path,
            page_execution_id=page_execution_id,
        )

        connection = controller.repositories.producer.enqueue(
            page.id, context, user_jwt=user_jwt
        )

        # First drain gets execution:started message
        start_msg = drain_until_response(
            connection, timeout=DRAIN_START_TIMEOUT_SECONDS
        )
        if not start_msg:
            connection.close()
            flask.abort(500)

        execution_id = None
        if isinstance(start_msg, dict) and start_msg.get("type") == "execution:started":
            execution_id = start_msg.get("executionId")

        msg = drain_until_response(connection)

        if not msg:
            connection.close()
            flask.abort(500)

        # Streaming response (generator functions)
        if isinstance(msg, dict) and msg.get("__page_stream__") == "start":

            def generate():
                try:
                    while True:
                        chunk = connection.recv()
                        if not isinstance(chunk, dict):
                            break
                        if chunk.get("__page_stream__") == "chunk":
                            yield json.dumps({"data": chunk["data"]}) + "\n"
                        elif chunk.get("__page_stream__") == "error":
                            yield json.dumps({"error": chunk["error"]}) + "\n"
                            break
                        elif chunk.get("__page_stream__") == "end":
                            break
                except (EOFError, BrokenPipeError):
                    pass
                finally:
                    connection.close()

            resp = flask.Response(
                status=msg["status"],
                response=generate(),
                headers=msg["headers"],
            )
            if execution_id:
                resp.headers["X-Execution-Id"] = execution_id
            if not IS_PRODUCTION:
                resp.headers["X-Abstra-Debug"] = "true"
            return resp

        # Regular response
        connection.close()

        response = normalize_response(msg)
        if not response:
            flask.abort(500)

        resp = flask.Response(
            status=response.status,
            response=response.body,
            headers=response.headers,
        )
        if execution_id:
            resp.headers["X-Execution-Id"] = execution_id
        if not IS_PRODUCTION:
            resp.headers["X-Abstra-Debug"] = "true"
        return resp

    def _serve_page_static(filename: str):
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

    @bp.get("/_page-home/<path:filename>")
    def page_home_static(filename):
        return _serve_page_static(filename)

    @bp.get("/_page/<page_path>/<path:filename>")
    def page_static(page_path, filename):
        return _serve_page_static(filename)

    @bp.route("/_page-home", methods=["GET", "POST"])
    @player_usage
    def page_home_runner():
        return _run_page("")

    @bp.route("/_page/<path:path>", methods=["GET", "POST"])
    @guard.by(PathArgSelector("path"))
    @player_usage
    def page_runner(path):
        return _run_page(path)

    @bp.post("/_logs/<execution_id>")
    def browser_logs(execution_id: str):
        """Receive browser console logs and store them as execution logs."""
        from datetime import datetime

        from abstra_internals.controllers.execution.execution_stdio import (
            BroadcastController,
        )
        from abstra_internals.repositories.execution_logs import LogEntry

        if not flask.request.json:
            flask.abort(400)

        body = flask.request.json
        logs = body.get("logs", [])
        stage_id = body.get("stageId", "")

        short_id = execution_id.split("-")[0]
        # Use high sequence base so browser logs sort after Python logs
        base_seq = 1_000_000 + controller.execution_logs_repository.get_sequence()

        for i, entry in enumerate(logs):
            level = entry.get("level", "log")
            message = entry.get("message", "")
            event = "stderr" if level in ("error", "warn") else "stdout"
            text = f"[RUN {short_id}] [BROWSER] {message}"
            controller.execution_logs_repository.save(
                LogEntry(
                    execution_id=execution_id,
                    stage_id=stage_id,
                    created_at=datetime.now(),
                    event=event,
                    payload={"text": text},
                    sequence=base_seq + i,
                )
            )
            # Broadcast directly via WebSocket (don't rely on file watcher)
            BroadcastController.broadcast(
                msg=serialize(
                    dict(
                        type="stdio",
                        payload=dict(
                            type=event,
                            log=text,
                            execution_id=execution_id,
                            stage_id=stage_id,
                        ),
                    )
                )
            )

        return {"ok": True}

    @bp.get("/_jobs")
    def list_jobs():
        if flask.request.headers.get("Shared-Token") != CLOUD_API_PROD_SHARED_TOKEN:
            flask.abort(401)

        # The scheduler needs all the jobs, including disabled ones, to schedule them.
        # The scheduler will always send the request to the lib to run the jobs, and the lib will check if the job is enabled or not.
        jobs = controller.get_jobs(include_disabled_jobs=True)

        # used by Scheduler Container - DO NOT CHANGE CONTRACT
        return [{"id": job.id, "schedule": job.schedule} for job in jobs]

    @bp.post("/_jobs/<path:id>")
    def job_runner(id):
        if flask.request.headers.get("Shared-Token") != CLOUD_API_PROD_SHARED_TOKEN:
            flask.abort(401)

        status = controller.get_job_status(id)
        if status == "not_found":
            flask.abort(404)

        if status == "disabled":
            return {"status": "disabled"}

        conn = controller.repositories.producer.enqueue(id, context=JobContext())
        try:
            conn.recv()
        finally:
            conn.close()

        return {"status": "running"}

    @bp.get("/")
    @cache.statics()
    def index():
        res = send_from_dist("player.html", "player.html")
        return res

    @bp.get("/<path:filename>")
    @cache.statics()
    def spa(filename: str):
        res = send_from_dist(filename, "player.html")
        return res

    setup_hook = Path("__setup__.py")
    if setup_hook.exists():
        module = __import__(path2module(setup_hook))
        if hasattr(module, "setup"):
            module.setup(bp)
        else:
            print(f"Could not find setup function in {setup_hook}")

    return bp
