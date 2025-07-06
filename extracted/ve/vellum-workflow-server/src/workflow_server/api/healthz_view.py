from typing import Tuple

from flask import Blueprint, Response, jsonify

from workflow_server.utils.oom_killer import get_is_oom_killed

bp = Blueprint("healthz", __name__)


@bp.route("", methods=["GET"])
@bp.route("/", methods=["GET"])
def healthz() -> Tuple[Response, int]:
    if get_is_oom_killed():
        return jsonify(success=False), 500

    resp = jsonify(success=True)
    return resp, 200
