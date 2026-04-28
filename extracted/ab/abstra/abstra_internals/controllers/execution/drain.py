import json
import time
from typing import Any, Optional

from abstra_internals.controllers.execution.connection_protocol import (
    ConnectionProtocol,
)
from abstra_internals.entities.execution_context import Response
from abstra_internals.environment import DRAIN_RESPONSE_TIMEOUT_SECONDS

_INTERNAL_MESSAGE_TYPES = frozenset(
    {
        "execution:started",
        "execution:ended",
        "stdio",
        "stdio_batch",
    }
)


def drain_until_response(
    connection: ConnectionProtocol,
    timeout: float = DRAIN_RESPONSE_TIMEOUT_SECONDS,
) -> Optional[Any]:
    """Drain intermediate stdio/stdio_batch messages from the connection
    until a real response (Response, non-stdio dict, or unparseable string)
    is found, or timeout is exceeded.

    Returns the first non-stdio message, or None on timeout/closed connection.
    """
    deadline = time.monotonic() + timeout
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None
        if not connection.poll(timeout=remaining):
            return None
        msg = connection.recv()
        if msg is None:
            return None
        if isinstance(msg, str):
            try:
                msg = json.loads(msg)
            except (json.JSONDecodeError, TypeError):
                return msg
        if isinstance(msg, Response):
            return msg
        if isinstance(msg, dict):
            if msg.get("type") in ("stdio", "stdio_batch"):
                continue
            return msg
        return msg


def normalize_response(msg: Any) -> Optional[Response]:
    """Convert a raw message into a Response object.

    - Response → returned as-is
    - str → generic 500 (avoids leaking internal details like tracebacks)
    - dict → converted to Response using headers/status/body keys with defaults
    - None or unexpected type → returns None (caller should abort 500)
    """
    if msg is None:
        return None
    if isinstance(msg, Response):
        return msg
    if isinstance(msg, str):
        return Response(headers={}, status=500, body="Internal Server Error")
    if isinstance(msg, dict):
        if msg.get("type") in _INTERNAL_MESSAGE_TYPES:
            return Response(headers={}, status=500, body="Internal Server Error")
        return Response(
            headers=msg.get("headers", {}),
            status=msg.get("status", 200),
            body=msg.get("body", ""),
        )
    return None
