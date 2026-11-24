"""MEDIA ON AN ASSISTANT TURN — carried to the person's side, never refused by the provider.

A made or edited picture is stored on the ASSISTANT message that answered with it. Most chat
APIs refuse media inside an assistant message: Anthropic ("'image' blocks are not permitted
within assistant turns", live 2026-11-10, every Claude reply after a made picture), the OpenAI
Responses API (assistant content is ``output_text`` / ``refusal`` only) and Chat Completions
(``image_url`` is a user-message part). Gemini replays pictures on ``model`` turns natively.

Two independent layers, each enough on its own:

1. ``carry_assistant_media`` — a SEND-BOUNDARY step (``send_boundary._carry_assistant_media``,
   the only caller; guard ``tests/package_host_contracts/test_send_boundary_guard.py``). On the
   WIRE copy only, each media part an assistant turn may not carry is replaced by its identity
   line, and the part itself rides a host-written user turn placed right after that assistant
   turn and its tool results — the same move the translators already make for a tool result's
   picture. The model still SEES the picture it made. Same bytes every send: cached once.
2. ``name_assistant_media`` — the translators' backstop (``BaseTranslator.messages_for_wire``).
   A part that still reaches a translator on an assistant turn is replaced by its identity line
   and staged as a media notice on the request snapshot: loud, never a 400.

What each wire style lets an assistant turn carry: ``provider_io_capabilities.assistant_turn_refuses``.
"""

from __future__ import annotations

from html import escape
from typing import Any

from matrx_utils import vcprint

#: Metadata key on the host-written user turn that carries an earlier assistant turn's media.
CARRIED_MEDIA_KEY = "assistant_media_carried"


def _role(message: Any) -> str:
    role = getattr(message, "role", None)
    return str(getattr(role, "value", role) or "").lower()


def _identity_line(content: Any, *, where: str) -> str:
    from matrx_ai.providers.provider_io_capabilities import container_for_content

    container = container_for_content(content)
    kind = container.value if container is not None else "media"
    metadata = getattr(content, "metadata", None) or {}
    name = metadata.get("file_name") if isinstance(metadata, dict) else None
    ident = getattr(content, "file_id", None) or getattr(content, "url", None) or ""
    attrs = {"kind": kind}
    if isinstance(name, str) and name.strip():
        attrs["name"] = name.strip()
    if ident:
        attrs["id"] = str(ident)
    attrs["sent"] = where
    rendered = " ".join(f'{k}="{escape(v, quote=True)}"' for k, v in attrs.items())
    return f"<attachment {rendered}/>"


def _refused_parts(message: Any, wire_format: str | None) -> list[int]:
    from matrx_ai.providers.provider_io_capabilities import assistant_turn_refuses

    return [
        index
        for index, content in enumerate(getattr(message, "content", None) or [])
        if assistant_turn_refuses(content, wire_format)
    ]


def _with_content(message: Any, content: list[Any]) -> Any:
    from copy import copy

    clone = copy(message)
    clone.content = content
    return clone


_CARRIED_LEAD = (
    "<carried_from_assistant_turn>The media below was part of the assistant's previous reply; "
    "it is shown here because this model takes media only on a user turn.</carried_from_assistant_turn>"
)


def _moved_record(content: Any, *, at: int, merged: bool) -> dict[str, Any]:
    from matrx_ai.providers.provider_io_capabilities import container_for_content

    container = container_for_content(content)
    record: dict[str, Any] = {"kind": container.value if container is not None else "media", "at": at}
    ident = getattr(content, "file_id", None)
    if ident:
        record["file_id"] = str(ident)
    if merged:
        record["merged"] = True
    return record


def carry_assistant_media(
    messages: list[Any],
    wire_format: str | None,
    *,
    strict_alternation: bool = False,
    moved_out: list[dict[str, Any]] | None = None,
) -> list[Any] | None:
    """The wire list with every refused assistant-turn media part carried to a user turn.

    ``None`` when nothing moved (the caller keeps its list). Never mutates the messages it is
    given: changed messages are shallow copies, so the stored conversation is untouched.
    An assistant turn with nothing after it (a prefill) cannot be followed by a user turn
    without ending it: its media is named in place by the translator backstop instead.

    ``strict_alternation`` (a model that refuses two user turns in a row,
    ``provider_profiles.requires_strict_role_alternation``): when the turn after the assistant
    turn and its tool results is already a user turn, the carried parts lead THAT turn instead
    of a turn of their own, so the wire still alternates (CGU-10 IMG5 #3).

    ``moved_out`` collects one record per carried part (``kind``, ``file_id``, the assistant
    turn's ``at`` index, whether it was ``merged``) for the request's audit.
    """
    from matrx_ai.config.message_config import HOST_AUTHORED_BY, TextContent, UnifiedMessage

    listed = list(messages or [])
    out: list[Any] = []
    moved = 0
    index = 0
    while index < len(listed):
        message = listed[index]
        refused = _refused_parts(message, wire_format) if _role(message) == "assistant" else []
        if not refused or index == len(listed) - 1:
            out.append(message)
            index += 1
            continue
        kept: list[Any] = []
        carried: list[Any] = []
        for at, content in enumerate(message.content):
            if at in refused:
                kept.append(TextContent(text=_identity_line(content, where="in the next user turn")))
                carried.append(content)
            else:
                kept.append(content)
        out.append(_with_content(message, kept))
        # Tool results answer this turn's tool calls and must follow it directly.
        assistant_at = index
        index += 1
        while index < len(listed) and _role(listed[index]) == "tool":
            out.append(listed[index])
            index += 1
        lead = [TextContent(text=_CARRIED_LEAD), *carried]
        merge = strict_alternation and index < len(listed) and _role(listed[index]) == "user"
        if merge:
            following = listed[index]
            merged = _with_content(following, [*lead, *(getattr(following, "content", None) or [])])
            merged.metadata = {**(getattr(following, "metadata", None) or {}), CARRIED_MEDIA_KEY: True}
            out.append(merged)
            index += 1
        else:
            out.append(
                UnifiedMessage(
                    role="user",
                    content=lead,
                    metadata={
                        "authored_by": HOST_AUTHORED_BY,
                        "authored_reason": CARRIED_MEDIA_KEY,
                        CARRIED_MEDIA_KEY: True,
                        "is_visible_to_user": False,
                    },
                )
            )
        if moved_out is not None:
            moved_out.extend(_moved_record(part, at=assistant_at, merged=merge) for part in carried)
        moved += len(carried)
    return out if moved else None


def name_assistant_media(messages: list[Any], wire_format: str | None, *, provider: str) -> list[Any]:
    """Backstop: replace any refused media part still on an assistant turn by its identity line.

    Reaching here means the send-boundary step did not run for this send (a direct client
    call, a prefill turn) — announced on the console and staged on the request snapshot.
    """
    out: list[Any] = []
    for message in messages:
        refused = _refused_parts(message, wire_format) if _role(message) == "assistant" else []
        if not refused:
            out.append(message)
            continue
        from matrx_ai.config.message_config import TextContent
        from matrx_ai.processing.media_fallback.handler import stage_media_notice

        content: list[Any] = []
        for at, part in enumerate(message.content):
            if at not in refused:
                content.append(part)
                continue
            line = _identity_line(part, where="not re-sent: assistant turn")
            content.append(TextContent(text=line))
            vcprint(
                f"[{provider}] media on an assistant turn reached the translator past the send "
                f"boundary; named instead of sent: {line}",
                color="red",
            )
            stage_media_notice(
                {
                    "media_kind": line.split('"')[1],
                    "action": "converted",
                    "user_message": "A picture from an earlier reply was referenced by name, not re-sent.",
                    "system_message": (
                        f"{provider}: media on an assistant turn reached the translator past the "
                        "send boundary's carry step"
                    ),
                    "provider": provider,
                }
            )
        out.append(_with_content(message, content))
    return out


__all__ = ["CARRIED_MEDIA_KEY", "carry_assistant_media", "name_assistant_media"]
