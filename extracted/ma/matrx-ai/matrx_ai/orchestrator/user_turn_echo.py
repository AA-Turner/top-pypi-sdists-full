"""The person's own words, echoed on their message's reservation frame.

A turn's rows are committed when the turn settles. A page that reloads
mid-answer rejoins the live NDJSON journal from frame one, and until now the
user ``record_reserved`` frame carried only ``role`` + ``position`` — so the
rejoined transcript knew a user row existed but not what it said, and showed
an empty bubble until the answer finished and the conversation was re-read.

The reservation already holds the pristine ``user_content`` (what the person
authored: their text and attachment references, never the machine template
and never inline bytes — ``TextContent.to_storage_dict`` /
``validate_message_content``). Echoing it on the frame lets every rejoining
client render the real message immediately, from server truth.

Bounded: inline bytes are stripped again here (defence in depth), and an
oversized echo is omitted rather than bloating the replay journal — the client
then shows no row until the turn's own re-read lands, never an empty box.
"""

from __future__ import annotations

import json
from typing import Any

#: Serialized-size ceiling for the echoed content (bytes of JSON).
MAX_USER_TURN_ECHO_BYTES = 64_000

_INLINE_BYTE_KEYS = frozenset({"base64_data", "base64"})


def _without_inline_bytes(block: Any) -> Any:
    if not isinstance(block, dict):
        return block
    return {k: v for k, v in block.items() if k not in _INLINE_BYTE_KEYS}


def user_turn_echo(pristine_user_content: list[Any] | None) -> dict[str, Any]:
    """Metadata keys to merge into the user message's reservation frame.

    Returns ``{"user_content": [...]}`` when the authored content is known and
    small enough to journal, else ``{}`` (the frame stays as it was).
    """
    if not pristine_user_content:
        return {}
    blocks = [_without_inline_bytes(b) for b in pristine_user_content]
    try:
        size = len(json.dumps(blocks, default=str).encode("utf-8"))
    except (TypeError, ValueError):
        return {}
    if size > MAX_USER_TURN_ECHO_BYTES:
        return {}
    return {"user_content": blocks}
