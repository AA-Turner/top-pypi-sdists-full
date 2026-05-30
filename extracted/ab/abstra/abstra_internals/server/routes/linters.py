import json

import flask
import flask_sock

from abstra_internals.contracts_generated import AbstraLibApiEditorLintersFixResponse
from abstra_internals.controllers.linter_events import LinterEventController
from abstra_internals.controllers.main import MainController
from abstra_internals.logger import AbstraLogger
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
        try:
            ws.thread.name = "LinterEventsWebSocket"
            LinterEventController.register(ws)
            # Send cached checks immediately (no expensive recomputation)
            cached_checks = controller.linter_repository.checks
            payload = {"checks": [c.to_dict() for c in cached_checks]}
            ws.send(json.dumps(payload))
            while True:
                try:
                    msg = ws.receive(timeout=40)
                    if msg is None:
                        break
                except Exception:
                    break
        except Exception as e:
            AbstraLogger.capture_exception(e)
        finally:
            LinterEventController.unregister(ws)

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
        checks = controller.linter_repository.update_checks()
        LinterEventController.broadcast(checks)
        return AbstraLibApiEditorLintersFixResponse(success=True).to_dict()

    return bp
