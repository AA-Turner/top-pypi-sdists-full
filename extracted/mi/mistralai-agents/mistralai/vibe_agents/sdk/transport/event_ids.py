"""Event ids of the Vibe Agents transport.

The transport names each event it relays with one, and the Session v1 projection names a
Turn's start position with one, so both build them here.
"""

import base64

_CURSOR_PREFIX = "vibe-agents:"
_EMPTY_CURSOR = f"{_CURSOR_PREFIX}none"


def _encode_base64url(value: str) -> str:
    return base64.urlsafe_b64encode(value.encode()).decode().rstrip("=")


def _encode_event_id(product_cursor: str, *, subevent_index: int | None = None) -> str:
    suffix = "" if subevent_index is None else f".{subevent_index}"
    return f"{_CURSOR_PREFIX}{_encode_base64url(product_cursor)}{suffix}"
