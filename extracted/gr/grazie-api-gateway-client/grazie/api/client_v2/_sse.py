import json
from typing import Any, Dict, Optional

from .exceptions import SSERequestFailedError, SSEResponseParseError


def _decode_sse_line(line: str) -> Optional[Dict[str, Any]]:
    """
    The decoding algorithm is greatly simplified and ignores all messages
    that don't start with "data:". It also assumes, that all messages have
    the following format:
    ```
        data: {"event_type": "data|error", ...}
    ```
    """
    line = line.strip()

    if len(line) == 0:
        return None

    if not line.startswith("data:"):
        return None

    content = line[5:].strip()
    if content == "end":
        return None

    try:
        content_data = json.loads(content)
    except json.JSONDecodeError as e:
        raise SSEResponseParseError("SSE content is not a valid JSON") from e

    event_type = content_data.get("event_type")
    if event_type == "data":
        content_data.pop("event_type")
        return content_data
    elif event_type == "error":
        error_message = content_data.get("error_message", "unknown")
        error_details = f"Server error: {error_message!r}"
        raise SSERequestFailedError(error_details)
    else:
        raise SSEResponseParseError(
            f"Expected all data parts of sse response to be of event_type data or error, but got {event_type}. "
            "The client should be updated to the latest api version."
        )
