"""The assistant chat surface: one turn per request, streamed as SSE.

This is the command-line client for `POST /v1/assistant/chat` on
`platform/anyx-mcp`. The server keeps no transcript, so the conversation lives
here: every request carries the history back, and nothing expires.

A turn is rendered as it arrives, which is the point of the surface: a turn with
tool calls takes tens of seconds, and a spinner would hide what it is doing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterator

import httpx

#: Mirrors the server's caps, so the client trims before the server refuses.
MAX_HISTORY_MESSAGES = 40
MAX_HISTORY_CHARACTERS = 100_000

#: One turn may take a while; the gateway ceiling is higher than this.
DEFAULT_TIMEOUT = 300.0

CHAT_PATH = "/v1/assistant/chat"
MODES = ("explain", "do")


class AssistantError(Exception):
    """A request the server refused, with the reason it gave."""

    def __init__(self, status: int, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail


def chat_url(api: str) -> str:
    return api.rstrip("/") + CHAT_PATH


def make_client(cacert: str | None = None) -> httpx.Client:
    """An HTTP client that trusts the environment's CA where there is one."""
    return httpx.Client(verify=cacert or True)


def stream_events(
    client: httpx.Client,
    url: str,
    token: str,
    payload: dict[str, Any],
    timeout: float = DEFAULT_TIMEOUT,
) -> Iterator[tuple[str, dict[str, Any]]]:
    """Yield ``(event, data)`` for one turn, in the order the server sent them.

    Server-sent events are a stream of ``field: value`` lines separated by blank
    lines; ``: comment`` lines are keepalives and are dropped here rather than
    rendered, because a keepalive is not something a turn said.
    """
    headers = {
        "authorization": f"Bearer {token}",
        "accept": "text/event-stream",
        "content-type": "application/json",
    }
    with client.stream(
        "POST", url, json=payload, headers=headers, timeout=timeout
    ) as response:
        if response.status_code != 200:
            response.read()
            raise AssistantError(response.status_code, _detail_of(response))
        event = None
        data: list[str] = []
        for line in response.iter_lines():
            if line == "":
                if event is not None or data:
                    yield event or "message", _parse(data)
                event = None
                data = []
                continue
            if line.startswith(":"):
                continue
            field_name, _, value = line.partition(":")
            value = value[1:] if value.startswith(" ") else value
            if field_name == "event":
                event = value
            elif field_name == "data":
                data.append(value)
        if event is not None or data:
            yield event or "message", _parse(data)


def _parse(data: list[str]) -> dict[str, Any]:
    joined = "\n".join(data).strip()
    if not joined:
        return {}
    try:
        payload = json.loads(joined)
    except ValueError:
        return {"detail": joined}
    return payload if isinstance(payload, dict) else {"detail": joined}


def _detail_of(response: httpx.Response) -> str:
    """The server's own words for a refusal, without inventing any."""
    try:
        body = response.json()
    except ValueError:
        return response.text.strip()[:300] or response.reason_phrase
    if isinstance(body, dict):
        for key in ("detail", "error", "message", "status"):
            if body.get(key):
                return str(body[key])
    return str(body)[:300]


@dataclass
class Conversation:
    """The transcript, held by the client because the server holds none."""

    mode: str = "explain"
    conversation_id: str = ""
    history: list[dict[str, Any]] = field(default_factory=list)
    pending_approval: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.mode not in MODES:
            raise ValueError(f"mode must be one of {', '.join(MODES)}")
        if not self.conversation_id:
            import shortuuid

            self.conversation_id = shortuuid.uuid()

    def payload(self, message: str, context: dict[str, Any] | None = None) -> dict:
        return {
            "message": message,
            "mode": self.mode,
            "context": context or {},
            "history": list(self.history),
            "conversation_id": self.conversation_id,
        }

    def remember(self, role: str, content: str, tool_name: str | None = None) -> None:
        entry: dict[str, Any] = {"role": role, "content": content}
        if tool_name:
            entry["tool_name"] = tool_name
        self.history.append(entry)
        self._trim()

    def clear(self) -> None:
        self.history = []
        self.pending_approval = None

    def _trim(self) -> None:
        """Drop the oldest turns until the transcript fits what the server takes."""
        while len(self.history) > MAX_HISTORY_MESSAGES:
            self.history.pop(0)
        while (
            sum(len(entry["content"]) for entry in self.history) > MAX_HISTORY_CHARACTERS
        ):
            self.history.pop(0)
