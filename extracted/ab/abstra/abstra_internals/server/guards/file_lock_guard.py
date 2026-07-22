from pathlib import Path
from typing import Optional, Tuple

import flask

from abstra_internals.controllers.file_locks import (
    FileLockController,
    FileLockedException,
)
from abstra_internals.environment import EDITOR_MODE, PROJECT_ID
from abstra_internals.services import mcp_context
from abstra_internals.services.jwt import decode_jwt
from abstra_internals.settings import Settings


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


def _requester_email() -> str:
    if not flask.has_request_context():
        return ""
    identity = current_editor_user()
    return identity[0] if identity else ""


def check_file_lock(*file_paths: str) -> Optional[flask.Response]:
    if mcp_context.current_message_id() is not None:
        return None

    email = _requester_email()

    for file_path in file_paths:
        normalized = file_path.replace("\\", "/")
        blocking = FileLockController.find_blocking_lock(normalized, email)
        if blocking is not None:
            return flask.make_response(
                {"error": "file_locked", "holder": blocking.to_dict()}, 423
            )
    return None


def raise_if_file_locked(file_path: Path) -> None:
    if mcp_context.current_message_id() is not None:
        return

    try:
        relative = file_path.resolve().relative_to(Settings.root_path.resolve())
    except ValueError:
        return

    email = _requester_email()
    blocking = FileLockController.find_blocking_lock(relative.as_posix(), email)
    if blocking is not None:
        raise FileLockedException(blocking)
