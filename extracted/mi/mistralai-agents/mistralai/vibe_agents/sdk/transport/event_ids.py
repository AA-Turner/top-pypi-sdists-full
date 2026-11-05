"""Event ids of the Vibe Agents transport.

The transport names each event it relays with one, and the Session v1 projection names a
Turn's start position with one, so both build them here. An id names its session
(``vibe-agents:<session id>:<position>``), so another session's reader refuses it.
"""

import base64
from uuid import UUID

from mistralai.vibe_agents.sdk.authoring.errors import invalid_cursor

_CURSOR_PREFIX = "vibe-agents:"
# The position before a session's first event, as an id without a session id gave it.
_EMPTY_CURSOR = f"{_CURSOR_PREFIX}none"
_EMPTY_POSITION = "none"
# The prefix of the in-process host's ids (``local:<session id>:<number>``, ``local_record.py``).
_LOCAL_PREFIX = "local:"


def _encode_base64url(value: str) -> str:
    return base64.urlsafe_b64encode(value.encode()).decode().rstrip("=")


def _encode_event_id(session_id: UUID | str, product_cursor: str, *, subevent_index: int | None = None) -> str:
    suffix = "" if subevent_index is None else f".{subevent_index}"
    return f"{_CURSOR_PREFIX}{session_id}:{_encode_base64url(product_cursor)}{suffix}"


def _empty_cursor(session_id: UUID | str) -> str:
    return f"{_CURSOR_PREFIX}{session_id}:{_EMPTY_POSITION}"


def _split_session(event_id: str, prefix: str) -> tuple[str | None, str]:
    """The session an id of ``prefix`` names, ``None`` for an id without one, and its position.

    No position has a ``:``: the transport's is Base64url, the in-process host's a number.
    """
    owner, separator, position = event_id.removeprefix(prefix).rpartition(":")
    return (owner if separator else None), position


def _session_cursor(cursor: str, session_id: str) -> str:
    """``cursor`` as ``session_id``'s event ids name it, checked before any read.

    A cursor without a session id, as the SDK gave before ids named their session, is taken as
    this session's: a program may have stored it. Naming the session makes it equal to the id the
    host gives for the same position, so a reader that compares them stops there.

    Raises:
        InvalidCursorError: The cursor is of another session.
    """
    for prefix in (_CURSOR_PREFIX, _LOCAL_PREFIX):
        if not cursor.startswith(prefix):
            continue
        owner, position = _split_session(cursor, prefix)
        if owner is None:
            # Only a position a host gives: a cursor no host gives reaches the host as passed.
            valid = position.isdigit() if prefix == _LOCAL_PREFIX else bool(position)
            return f"{prefix}{session_id}:{position}" if valid else cursor
        if owner != session_id:
            raise invalid_cursor(cursor, session_id, owner=owner)
    return cursor
