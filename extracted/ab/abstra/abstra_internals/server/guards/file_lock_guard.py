from pathlib import Path
from typing import Optional, Tuple

import flask

from abstra_internals.controllers.file_locks import (
    FileLockController,
    FileLockedException,
)
from abstra_internals.environment import EDITOR_MODE, PROJECT_ID
from abstra_internals.services.jwt import decode_jwt
from abstra_internals.settings import Settings

LOCK_SESSION_ID_HEADER = "X-Abstra-Lock-Session-Id"


def current_editor_user() -> Optional[Tuple[str, str]]:
    if EDITOR_MODE == "local":
        return "local", "local"

    token = flask.request.cookies.get("editor_auth")
    if not token:
        return None
    claims = decode_jwt(token, aud=f"web-editor-{PROJECT_ID}")
    if not claims:
        return None
    email = claims.get("email")
    if not email:
        return None
    name = claims.get("name") or email
    return email, name


def _requester_identity() -> Tuple[str, str]:
    if not flask.has_request_context():
        return "", ""
    identity = current_editor_user()
    email = identity[0] if identity else ""
    session_id = flask.request.headers.get(LOCK_SESSION_ID_HEADER) or ""
    return email, session_id


def check_file_lock(*file_paths: str) -> Optional[flask.Response]:
    email, session_id = _requester_identity()

    for file_path in file_paths:
        normalized = file_path.replace("\\", "/")
        blocking = FileLockController.find_blocking_lock(normalized, email, session_id)
        if blocking is not None:
            return flask.make_response(
                {"error": "file_locked", "holder": blocking.to_dict()}, 423
            )
    return None


def raise_if_file_locked(file_path: Path) -> None:
    try:
        relative = file_path.resolve().relative_to(Settings.root_path.resolve())
    except ValueError:
        return

    email, session_id = _requester_identity()
    blocking = FileLockController.find_blocking_lock(
        relative.as_posix(), email, session_id
    )
    if blocking is not None:
        raise FileLockedException(blocking)
