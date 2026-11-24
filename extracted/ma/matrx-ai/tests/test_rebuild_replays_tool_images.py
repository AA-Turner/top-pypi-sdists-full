"""A stored screenshot must replay as an IMAGE, never as its envelope's JSON text.

2026-11-01, conversation 866514a3-89f7-456b-9eff-14dce6b52987: a Matrx Extend chat
called the delegated ``computer`` tool (action=screenshot). ``POST /tool_results``
stored the canonical ``image_ref`` envelope in ``chat.tool_call.output`` (a TEXT
column) and ``/resume`` rebuilt the history from that row. The rebuild replayed
the JSON string as tool-result text, so the model said "The screenshot gave me no
readable content" — it never saw the image the live turn would have sent.

This drives the real path: the stored row text -> ``rebuild_conversation_messages``
-> the media resolver's walk + resolve -> each provider's wire block.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db._registry import configure_db

configure_db(
    models={
        "CxMessage": SimpleNamespace,
        "CxToolCall": SimpleNamespace,
        "CxMedia": SimpleNamespace,
    }
)

from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages  # noqa: E402
from matrx_ai.providers.unified_client import (  # noqa: E402
    _collect_image_shaped,
    _resolve_media_ref_item,
)

FILE_ID = "d312cb3c-a80b-44e0-9d7c-ea14ca9c30c4"
MSG_ASSISTANT = "22222222-2222-2222-2222-222222222222"
MSG_TOOL = "33333333-3333-3333-3333-333333333333"
FAKE_JPEG_B64 = "/9j/4AAQSkZJRgABAQ=="

# The production row's stored text, shape-for-shape (chat.tool_call 34911858-...).
STORED_OUTPUT = json.dumps(
    {
        "ok": True,
        "mode": "visible",
        "media_type": "image/jpeg",
        "format": "jpeg",
        "width": 2576,
        "height": 1730,
        "source_width": 3458,
        "source_height": 2322,
        "byte_length": 178418,
        "file_id": FILE_ID,
        "file_url": None,
        "captured_page_url": "https://example.com/settings/domains",
        "kind": "image_ref",
        "size_bytes": 178418,
        "media_ref": {"file_id": FILE_ID, "vision_class": None},
    }
)


def _msg(*, id: str, role: str, position: int, content: list[dict[str, Any]]) -> SimpleNamespace:
    return SimpleNamespace(
        id=id,
        role=role,
        position=position,
        content=content,
        created_at=None,
        status="active",
        metadata={},
        deleted_at=None,
        is_visible_to_model=True,
    )


def _tool_call(*, message_id: str, output: str) -> SimpleNamespace:
    return SimpleNamespace(
        id="34911858-31e8-4ee9-8b04-b54c2b9d7f54",
        call_id="toolu_01",
        message_id=message_id,
        tool_name="computer",
        output=output,
        is_error=False,
        status="completed",
        output_chars=len(output),
        output_preview=None,
        error_type=None,
        error_message=None,
        deleted_at=None,
        execution_events=None,
    )


class _FakeFileManager:
    """Stands in for FileManager.resolve_media_async: inlines bytes for OUR file id."""

    def __init__(self) -> None:
        self.resolved: list[str] = []

    async def resolve_media_async(self, ref: Any, needs_bytes: bool = False) -> None:
        assert ref.file_id == FILE_ID, f"resolver asked for the wrong identity: {ref.file_id}"
        self.resolved.append(ref.file_id)
        ref.base64_data = FAKE_JPEG_B64
        ref.mime_type = "image/jpeg"
        ref.is_resolved = True


def _assistant_call() -> dict[str, Any]:
    return {
        "type": "tool_call",
        "call_id": "toolu_01",
        "name": "computer",
        "arguments": {"action": "screenshot"},
    }


async def _rebuild_and_resolve(messages: list[Any]) -> tuple[Any, _FakeFileManager]:
    rebuilt = await rebuild_conversation_messages(
        messages, [_tool_call(message_id=messages[-1].id, output=STORED_OUTPUT)], []
    )
    tool_msgs = [m for m in rebuilt if (getattr(m.role, "value", m.role)) == "tool"]
    assert len(tool_msgs) == 1, f"expected one tool message, got {len(tool_msgs)}"
    tool_msg = tool_msgs[0]
    images: list[Any] = []
    _collect_image_shaped(tool_msg, images, set())
    for block in tool_msg.content:
        _collect_image_shaped(block, images, set())
    assert images, (
        "the rebuilt screenshot result carries NO image block — the model will be "
        "handed the image_ref envelope as JSON text (the 2026-11-01 incident)"
    )
    fm = _FakeFileManager()
    for item in images:
        await _resolve_media_ref_item(fm, item)
    return tool_msg, fm


def _persisted_tool_message() -> list[Any]:
    return [
        _msg(id=MSG_ASSISTANT, role="assistant", position=0, content=[_assistant_call()]),
        _msg(
            id=MSG_TOOL,
            role="tool",
            position=1,
            content=[
                {
                    "type": "tool_result",
                    "call_id": "toolu_01",
                    "tool_use_id": "toolu_01",
                    "name": "computer",
                    "output_chars": 0,
                }
            ],
        ),
    ]


def _suspended_round_trip() -> list[Any]:
    # The /tool_results + /resume shape: no role='tool' row yet; the result is
    # synthesized from chat.tool_call (message_id points at the assistant turn).
    return [_msg(id=MSG_ASSISTANT, role="assistant", position=0, content=[_assistant_call()])]


@pytest.mark.asyncio
@pytest.mark.parametrize("shape", [_persisted_tool_message, _suspended_round_trip])
async def test_resumed_screenshot_reaches_the_anthropic_wire_as_an_image(shape: Any) -> None:
    tool_msg, fm = await _rebuild_and_resolve(shape())
    assert fm.resolved == [FILE_ID]
    wire = tool_msg.to_anthropic_blocks()
    results = [b for b in wire if isinstance(b, dict) and b.get("type") == "tool_result"]
    assert len(results) == 1, wire
    content = results[0]["content"]
    assert isinstance(content, list), f"tool_result content is text, not blocks: {content!r}"
    image = next((b for b in content if b.get("type") == "image"), None)
    assert image is not None, f"no image block on the wire: {content}"
    assert image["source"] == {"type": "base64", "media_type": "image/jpeg", "data": FAKE_JPEG_B64}
    assert all(FILE_ID not in json.dumps(b) for b in content if b.get("type") == "text"), (
        "the envelope's JSON leaked into the model's text"
    )


@pytest.mark.asyncio
async def test_resumed_screenshot_is_typed_for_every_provider() -> None:
    tool_msg, _ = await _rebuild_and_resolve(_persisted_tool_message())
    (result,) = [c for c in tool_msg.content if getattr(c, "type", None) == "tool_result"]
    assert result.extract_image_blocks(), (
        "OpenAI/Google surface tool images via extract_image_blocks()"
    )


@pytest.mark.asyncio
async def test_non_media_output_still_replays_as_text() -> None:
    output = '{"ok": true, "tabs": 3}'
    rebuilt = await rebuild_conversation_messages(
        _persisted_tool_message(), [_tool_call(message_id=MSG_TOOL, output=output)], []
    )
    (tool_msg,) = [m for m in rebuilt if getattr(m.role, "value", m.role) == "tool"]
    (result,) = [c for c in tool_msg.content if getattr(c, "type", None) == "tool_result"]
    assert result.content == output
