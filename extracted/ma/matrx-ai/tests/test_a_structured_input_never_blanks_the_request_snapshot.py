"""A turn carrying a structured input (``input_notes``) still serializes for its request snapshot.

``MessageList.to_dict_list`` is what ``chat.request_snapshot.unified_payload`` stores. Its ``user_content`` line called
``to_dict()`` bare, and structured-input blocks have only ``to_storage_dict``: every such turn lost its snapshot
(``request_snapshot_capture_failure`` "'NotesInputContent' object has no attribute 'to_dict'", 2026-11-19).
"""

from __future__ import annotations

import json

from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.structured_input_config import NotesInputContent
from matrx_ai.config.unified_content import TextContent


def test_a_notes_input_in_content_and_user_content_serializes_and_reads_back() -> None:
    notes = NotesInputContent(note_ids=["note-1"])
    msg = UnifiedMessage(role="user", content=[TextContent(text="see my note"), notes], user_content=[notes])
    messages = MessageList()
    messages.append(msg)

    out = messages.to_dict_list()

    json.dumps(out)  # the snapshot writer stores it as JSON
    assert out[0]["user_content"][0]["type"] == "input_notes"
    assert out[0]["content"][1]["type"] == "input_notes"
    again = UnifiedMessage.from_dict(out[0])
    assert any(isinstance(c, NotesInputContent) and c.note_ids == ["note-1"] for c in again.user_content or [])
