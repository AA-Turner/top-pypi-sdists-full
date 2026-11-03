"""Server notices on the wire: the `X-Probe-Notices` set revision an answer carries, and the
`GET /v1/client/messages` list it points at, read into `ServerMessage`s (plan T7, R14)."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass

from .server_messages import ServerMessage, parse_server_message

#: On an authenticated answer that has notices for this client: the 16-hex revision of their set.
NOTICES_HEADER = "X-Probe-Notices"
#: Where the set is read when its revision changed (`app/capture/clients/messages/router.py`).
MESSAGES_PATH = "/v1/client/messages"
_SET_REVISION = re.compile(r"[0-9a-f]{16}")
#: The longest sentence a notice carries (contracts' `MAX_TEXT_LENGTH`).
_MAX_TEXT = 500
#: Control characters a terminal would act on (the server allows none; a self-pointed base URL could send them).
_CONTROL = re.compile(r"[\x00-\x09\x0b-\x1f\x7f-\x9f]")


@dataclass(frozen=True)
class MessageList:
    """The notices that apply to this client now, and the set revision the server named them by."""

    set_revision: str | None
    messages: tuple[ServerMessage, ...]


def read_set_revision(headers: Mapping[str, str]) -> str | None:
    """The answer's `X-Probe-Notices` value, when it is a well-formed revision."""
    value = headers.get(NOTICES_HEADER)
    return value if isinstance(value, str) and _SET_REVISION.fullmatch(value) else None


def parse_message_list(body: object) -> MessageList:
    """`ClientMessageList` JSON as read: items without an id or a sentence are left out."""
    fields = body if isinstance(body, dict) else {}
    revision = fields.get("set_revision")
    items = fields.get("messages") if isinstance(fields.get("messages"), list) else []
    messages = tuple(message for message in map(parse_client_message, items) if message is not None)
    return MessageList(revision if isinstance(revision, str) and _SET_REVISION.fullmatch(revision) else None, messages)


def parse_client_message(item: object) -> ServerMessage | None:
    """One wire `ClientMessage` (its sentence is `text`), read by the error parser's rules; None
    without a plain `message_id` or a sentence."""
    text = _CONTROL.sub("", item["text"]) if isinstance(item, dict) and isinstance(item.get("text"), str) else ""
    if not text.strip():
        return None
    message = parse_server_message(None, {**item, "detail": text[:_MAX_TEXT]})
    return message if message.is_registered else None
