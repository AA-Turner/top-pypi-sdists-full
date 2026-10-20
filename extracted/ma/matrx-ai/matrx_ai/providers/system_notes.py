"""History system messages on a wire with no mid-conversation system role.

A system message kept in place in the history (carried history: data, never filled — see
``UnifiedConfig.from_dict``) must reach the model where it sits. OpenAI-shaped wires take a
``system`` role anywhere; Anthropic and Google take system text only up front. For those two,
each history system message becomes a clearly marked note in the user channel, in place:

    <system_note>
    {the message's text, exactly as stored}
    </system_note>

The text is never filled or unescaped. The translator's own same-role merge joins the note to
an adjacent user turn. A note that sits between a tool call and its results is delivered right
after those results (Anthropic requires ``tool_result`` blocks first in their user turn).

The stored ``config.messages`` is never touched: this returns a new wire-only list. Every
conversion is announced — server log, a client warning, and a note on an active Model view
capture (which equals the real request).
"""

from __future__ import annotations

import copy
from collections.abc import Iterable
from typing import Any

from matrx_utils import vcprint

SYSTEM_NOTE_OPEN = "<system_note>"
SYSTEM_NOTE_CLOSE = "</system_note>"

_SYSTEM_ROLES = frozenset({"system", "developer"})


def _role(message: Any) -> str:
    role = getattr(message, "role", None)
    return str(getattr(role, "value", role) or "")


def _carries_tool_result(message: Any) -> bool:
    """A tool result, whether the message is role "tool" or a "user" turn that carries one."""
    if _role(message) == "tool":
        return True
    from matrx_ai.config.tools_config import ToolResultContent

    return any(isinstance(c, ToolResultContent) for c in (getattr(message, "content", None) or []))


def system_note_text(text: str) -> str:
    return f"{SYSTEM_NOTE_OPEN}\n{text}\n{SYSTEM_NOTE_CLOSE}"


def _as_note(message: Any) -> Any:
    from matrx_ai.config.unified_content import TextContent

    text = "".join(c.text for c in (message.content or []) if isinstance(c, TextContent))
    others = [c for c in (message.content or []) if not isinstance(c, TextContent)]
    content = ([TextContent(text=system_note_text(text))] if text else []) + others
    note = copy.copy(message)  # shallow copy works for a dataclass today and a pydantic model after the flip
    note.role = "user"
    note.content = content
    note.metadata = dict(message.metadata or {})
    return note


def history_system_messages_as_notes(messages: Iterable[Any], *, provider: str) -> list[Any]:
    """The wire message list for a provider without a mid-list system role (see module doc)."""
    source = list(messages)
    if not any(_role(m) in _SYSTEM_ROLES for m in source):
        return source

    out: list[Any] = []
    pending: list[Any] = []  # notes waiting for a run of tool results to finish
    converted = 0
    deferred = 0
    for index, message in enumerate(source):
        role = _role(message)
        if role in _SYSTEM_ROLES:
            note = _as_note(message)
            converted += 1
            # Look PAST consecutive system messages: a result waits behind every note before it.
            ahead = index + 1
            while ahead < len(source) and _role(source[ahead]) in _SYSTEM_ROLES:
                ahead += 1
            before_results = ahead < len(source) and _carries_tool_result(source[ahead])
            if before_results or pending:
                pending.append(note)
                deferred += 1
            else:
                out.append(note)
            continue
        if pending and not _carries_tool_result(message):
            out.extend(pending)
            pending = []
        out.append(message)
    out.extend(pending)

    _announce(provider=provider, converted=converted, deferred=deferred)
    return out


def _announce(*, provider: str, converted: int, deferred: int) -> None:
    detail = (
        f"{converted} system message(s) in the conversation history sent to {provider} as "
        f"{SYSTEM_NOTE_OPEN} notes in the user turn, in place ({provider} has no "
        "mid-conversation system role); text unchanged"
    )
    if deferred:
        detail += f"; {deferred} placed right after the tool results it preceded"
    vcprint(f"[providers/system_notes] {detail}.", color="yellow")

    from matrx_ai.providers.request_capture import note_capture

    note_capture(detail + ".")

    try:
        from matrx_connect.context.events import WarningPayload

        from matrx_ai.providers.outbound_params import send_client_warning

        send_client_warning(
            WarningPayload(
                code="system_message_as_note",
                system_message=detail,
                user_message="A system message in the history was sent as a marked note.",
                level="low",
                recoverable=True,
                metadata={"provider": provider, "converted": converted, "deferred": deferred},
            ),
            name="system_note_warning",
        )
    except Exception as exc:  # noqa: BLE001 — telling the caller never breaks the send
        vcprint(f"[providers/system_notes] client warning not sent ({exc!r}).", color="yellow")
