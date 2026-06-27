import re
from typing import Optional

from flask import g, has_request_context

USER_MESSAGE_ID_HEADER = "X-Abstra-User-Message-Id"
_MESSAGE_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
_FLASK_G_KEY = "abstra_user_message_id"


def is_valid_message_id(message_id: Optional[str]) -> bool:
    return bool(message_id) and bool(_MESSAGE_ID_RE.fullmatch(message_id))


def set_current_message_id(message_id: Optional[str]) -> None:
    if has_request_context():
        safe_value = message_id if is_valid_message_id(message_id) else None
        setattr(g, _FLASK_G_KEY, safe_value)


def current_message_id() -> Optional[str]:
    if not has_request_context():
        return None
    return getattr(g, _FLASK_G_KEY, None)
