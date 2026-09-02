"""Convert Matrx messages to ``matrx_ai.memory.Message`` dataclasses.

The OM system strictly expects its own Message dataclass. Matrx AI uses
``UnifiedMessage`` with a list of typed content parts. This module bridges
the two while preserving tool-call / tool-result context, which the
Observer LLM needs to extract meaningful observations.
"""
from __future__ import annotations

import hashlib
import json
import logging
from datetime import UTC, datetime
from typing import Any, Iterable

from .types import Message, MessageRole, TextPart, ToolCallPart, ToolResultPart

logger = logging.getLogger(__name__)


_ROLE_MAP = {
    "user": MessageRole.USER,
    "assistant": MessageRole.ASSISTANT,
    "model": MessageRole.ASSISTANT,
    "system": MessageRole.SYSTEM,
    "tool": MessageRole.TOOL,
    "function": MessageRole.TOOL,
}


def _stable_id(thread_id: str, index: int, role: str, text_digest: str) -> str:
    h = hashlib.sha1(f"{thread_id}|{index}|{role}|{text_digest}".encode()).hexdigest()[:16]
    return f"om-{h}"


def _render_text_from_unified_content(content: Any) -> tuple[list[TextPart | ToolCallPart | ToolResultPart], str]:
    """Flatten UnifiedMessage.content (or dict form) to parts + a digest.

    Returns (parts, text_for_digest). The digest is used to build a stable
    message id — NOT for display.
    """
    parts: list[TextPart | ToolCallPart | ToolResultPart] = []
    digest_parts: list[str] = []

    items: Iterable[Any] = content if isinstance(content, (list, tuple)) else [content]
    for item in items:
        if isinstance(item, str):
            parts.append(TextPart(text=item))
            digest_parts.append(item)
            continue
        # UnifiedContent dataclass OR raw dict
        type_name = None
        if hasattr(item, "type"):
            type_name = getattr(item, "type", None)
        elif isinstance(item, dict):
            type_name = item.get("type")
        type_name = (type_name or "text").lower()

        if type_name == "text":
            text_val = getattr(item, "text", None) if not isinstance(item, dict) else item.get("text")
            text_val = text_val or ""
            if text_val:
                parts.append(TextPart(text=text_val))
                digest_parts.append(text_val)
        elif type_name in ("tool_use", "tool_call"):
            call_id = (
                getattr(item, "id", None) if not isinstance(item, dict) else item.get("id")
            ) or (getattr(item, "tool_call_id", None) if not isinstance(item, dict) else item.get("tool_call_id")
            ) or (getattr(item, "call_id", None) if not isinstance(item, dict) else item.get("call_id"))
            tool_name = (
                getattr(item, "name", None) if not isinstance(item, dict) else item.get("name")
            ) or (getattr(item, "tool_name", None) if not isinstance(item, dict) else item.get("tool_name"))
            args = (
                getattr(item, "input", None) if not isinstance(item, dict) else item.get("input")
            ) or (getattr(item, "args", None) if not isinstance(item, dict) else item.get("args")) or {}
            parts.append(ToolCallPart(
                tool_call_id=str(call_id or ""),
                tool_name=str(tool_name or ""),
                args=args if isinstance(args, dict) else {"value": args},
            ))
            digest_parts.append(f"toolcall:{tool_name}")
        elif type_name in ("tool_result", "tool_response"):
            call_id = (
                getattr(item, "tool_call_id", None) if not isinstance(item, dict) else item.get("tool_call_id")
            ) or (getattr(item, "id", None) if not isinstance(item, dict) else item.get("id")
            ) or (getattr(item, "call_id", None) if not isinstance(item, dict) else item.get("call_id"))
            tool_name = (
                getattr(item, "tool_name", None) if not isinstance(item, dict) else item.get("tool_name")
            ) or ""
            content_val = (
                getattr(item, "content", None) if not isinstance(item, dict) else item.get("content")
            )
            is_error = bool(
                getattr(item, "is_error", False) if not isinstance(item, dict) else item.get("is_error", False)
            )
            parts.append(ToolResultPart(
                tool_call_id=str(call_id or ""),
                tool_name=str(tool_name),
                result=content_val,
                is_error=is_error,
            ))
            digest_parts.append(f"toolresult:{tool_name}")
        else:
            # Image/audio/video/document — render as a placeholder so the
            # observer at least sees "user attached an image" rather than
            # silently dropping.
            parts.append(TextPart(text=f"[{type_name} content]"))
            digest_parts.append(type_name)

    return parts, "\n".join(digest_parts)[:512]


def convert_to_om_messages(
    raw_messages: Any,
    *,
    thread_id: str,
    resource_id: str,
) -> list[Message]:
    """Convert a MessageList / list[UnifiedMessage] / list[dict] into OM Messages.

    Unknown roles are mapped to USER by default (rarely triggered; mostly a
    safety net for transport quirks).
    """
    messages: list[Message] = []

    # MessageList has an iter protocol — normalize to a list.
    if raw_messages is None:
        return []
    if hasattr(raw_messages, "items"):
        items = list(raw_messages.items)
    elif hasattr(raw_messages, "__iter__") and not isinstance(raw_messages, (str, bytes)):
        items = list(raw_messages)
    else:
        return []

    for idx, msg in enumerate(items):
        role_raw: Any
        content_raw: Any
        msg_id: Any
        if isinstance(msg, dict):
            role_raw = msg.get("role", "user")
            content_raw = msg.get("content", "")
            msg_id = msg.get("id")
        else:
            role_raw = getattr(msg, "role", "user")
            content_raw = getattr(msg, "content", "")
            msg_id = getattr(msg, "id", None)

        role_str = str(role_raw or "user").lower()
        # Skip system messages — OM injects its own system message; the
        # agent's base system instruction lives on UnifiedConfig.system_instruction,
        # which we never translate into a user-facing Message.
        if role_str == "system":
            continue

        mapped_role = _ROLE_MAP.get(role_str, MessageRole.USER)
        parts, digest = _render_text_from_unified_content(content_raw)
        if not parts:
            continue

        effective_id = str(msg_id) if msg_id else _stable_id(thread_id, idx, role_str, digest)
        messages.append(Message(
            id=effective_id,
            thread_id=thread_id,
            resource_id=resource_id,
            role=mapped_role,
            content=parts,
            created_at=datetime.now(UTC),
        ))

    return messages


def extract_om_system_extra(augmented_messages: list[Message]) -> str | None:
    """Pull the ``om-context`` system message prepended by ``process_input_step``.

    Returns the raw text, or None if it's absent (no active observations yet).
    """
    for msg in augmented_messages:
        if msg.role == MessageRole.SYSTEM and msg.id == "om-context":
            if isinstance(msg.content, str):
                return msg.content
            return "\n".join(
                part.text if isinstance(part, TextPart) else ""
                for part in msg.content
            )
    return None
