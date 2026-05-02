from typing import Tuple

from flask import Blueprint, Response, jsonify

from workflow_server.config import CONCURRENCY
from workflow_server.utils.system_utils import get_active_process_count

bp = Blueprint("status", __name__)


@bp.route("/is_available", methods=["GET"])
def is_available() -> Tuple[Response, int]:
    resp = jsonify(
        available=get_active_process_count() < CONCURRENCY,
        process_count=get_active_process_count(),
        max_concurrency=CONCURRENCY,
    )

    return resp, 200
