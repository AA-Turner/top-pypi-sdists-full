"""Message chunking for the Layer 2 map-reduce summarizer.

Pure data-shaping. Given a list of agno ``Message``-shaped objects and a
character budget per chunk, packs them into ordered groups that each fit
under the budget. Single oversized messages are paragraph-sliced (with
synthetic ``SimpleNamespace`` wrappers preserving role + tool metadata) so
the map-phase LLM call still sees one role-tagged input per call.
"""

import json
import re
from types import SimpleNamespace
from typing import Any, List


def _message_char_size(message: Any) -> int:
    """Return the approximate size of a single message in characters.

    Uses ``message.to_dict()`` when available so role, tool-call metadata and
    other structured fields are accounted for; falls back to ``str(message)``.
    """
    try:
        if hasattr(message, "to_dict"):
            return len(json.dumps(message.to_dict(), default=str, ensure_ascii=False))
    except Exception:
        pass
    try:
        return len(str(message))
    except Exception:
        return 0


def _split_oversized_message_text(text: str, char_budget: int) -> List[str]:
    """Split a single message's text into chunks that fit in *char_budget*.

    Attempts paragraph-level splits first, then line-level, then hard
    character slicing. Preserves ordering.
    """
    if char_budget <= 0:
        return [text]
    if len(text) <= char_budget:
        return [text]

    # Try paragraph split first.
    pieces: List[str] = []
    buf: List[str] = []
    buf_len = 0
    for para in text.split("\n\n"):
        piece_len = len(para) + 2
        if buf and buf_len + piece_len > char_budget:
            pieces.append("\n\n".join(buf))
            buf = [para]
            buf_len = piece_len
        elif piece_len > char_budget:
            # Paragraph itself too large — hard-slice.
            if buf:
                pieces.append("\n\n".join(buf))
                buf = []
                buf_len = 0
            for i in range(0, len(para), char_budget):
                pieces.append(para[i : i + char_budget])
        else:
            buf.append(para)
            buf_len += piece_len
    if buf:
        pieces.append("\n\n".join(buf))
    return pieces


def _split_messages_into_chunks(
    messages: List[Any],
    char_budget: int,
) -> List[List[Any]]:
    """Pack *messages* into ordered chunks whose total char size stays below
    *char_budget*. Never splits across multiple messages in the same slot.

    When a single message is itself larger than *char_budget*, the message is
    split into multiple synthetic messages (``SimpleNamespace``) at paragraph
    boundaries so ordering is preserved.
    """
    if char_budget <= 0 or not messages:
        return [list(messages)] if messages else []

    chunks: List[List[Any]] = []
    current: List[Any] = []
    current_size = 0

    def _flush():
        nonlocal current, current_size
        if current:
            chunks.append(current)
            current = []
            current_size = 0

    for msg in messages:
        size = _message_char_size(msg)

        if size > char_budget:
            # Flush what we have, then split the oversized message.
            _flush()
            text = str(getattr(msg, "content", "") or "")
            for piece_idx, piece in enumerate(
                _split_oversized_message_text(text, char_budget)
            ):
                synthetic = SimpleNamespace(
                    role=getattr(msg, "role", "user"),
                    content=piece,
                    tool_name=getattr(msg, "tool_name", None),
                    tool_call_id=getattr(msg, "tool_call_id", None),
                    _is_split_fragment=True,
                    _fragment_index=piece_idx,
                    to_dict=(
                        lambda p=piece, r=getattr(msg, "role", "user"): {
                            "role": r,
                            "content": p,
                        }
                    ),
                )
                chunks.append([synthetic])
            continue

        if current and current_size + size > char_budget:
            _flush()
        current.append(msg)
        current_size += size

    _flush()
    return chunks


# Re-exported for callers that previously imported the regex constant from
# ``context_optimizer`` directly. Currently unused outside chunking, but
# kept addressable to avoid quiet test breakage.
_FIELD_MARKER_RE = re.compile(r"\s\w+=")
