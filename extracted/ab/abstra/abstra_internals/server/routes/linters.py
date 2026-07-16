import flask
import flask_sock

from abstra_internals.contracts_generated import AbstraLibApiEditorLintersFixResponse
from abstra_internals.controllers.linter_events import LinterEventController
from abstra_internals.controllers.main import MainController
from abstra_internals.server.socket_listener import serve_listener_websocket
from abstra_internals.usage import editor_usage


def get_editor_bp(controller: MainController):
    bp = flask.Blueprint("editor_linters", __name__)
    sock = flask_sock.Sock(bp)

    @bp.get("/check")
    def _check_linters():
        checks = controller.linter_repository.find_issues_in_codebase()
        return [check.to_dict() for check in checks]

    @sock.route("/events")
    def _linter_events_websocket(ws: flask_sock.Server):
        def _send_initial_checks(ws: flask_sock.Server) -> None:
            # Send cached checks immediately (no expensive recomputation)
            cached_checks = controller.linter_repository.checks
            ws.send(LinterEventController.build_payload(cached_checks))

        serve_listener_websocket(
            ws,
            thread_name="LinterEventsWebSocket",
            registry=LinterEventController,
            on_registered=_send_initial_checks,
        )

    @bp.post("/fix/<rule_name>/<fix_name>")
    @editor_usage
    def _fix_linter(rule_name: str, fix_name: str):
        controller.linter_repository.fix_issue_in_codebase(rule_name, fix_name)
        LinterEventController.broadcast(
            controller.linter_repository.find_issues_in_codebase()
        )
        return AbstraLibApiEditorLintersFixResponse(success=True).to_dict()

    @bp.post("/fix-all")
    @editor_usage
    def _fix_all_linters():
        controller.linter_repository.fix_all_linters()
        checks = controller.linter_repository.update_checks()
        LinterEventController.broadcast(checks)
        return AbstraLibApiEditorLintersFixResponse(success=True).to_dict()

    @bp.post("/refresh")
    @editor_usage
    def _refresh_linters():
        # An explicit user refresh revalidates rule-level network caches
        # (e.g. the PyPI latest-version cache) instead of trusting TTLs.
        checks = controller.linter_repository.update_checks(revalidate_caches=True)
        LinterEventController.broadcast(checks)
        return AbstraLibApiEditorLintersFixResponse(success=True).to_dict()

    return bp
