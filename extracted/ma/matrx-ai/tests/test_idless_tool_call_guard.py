"""Guards against id-less ``tool_call`` blocks (the 2026-07-18 incident).

Conversation ``e533112e``: an out-of-band writer rewrote an assistant
``cx_message`` row's content through a serializer that dropped the tool_call
block's ``call_id``. On rebuild, the block became ``ToolCallContent(id="")``,
which every sanitize pass ignored (they all key off ``c.id``), so Anthropic
received ``tool_use.id = ""`` → 400 "String should match pattern
'^[a-zA-Z0-9_-]+$'" — while the paired tool_result (still carrying the real
id) was dropped as an "orphan". Every future turn of the conversation died.

Layers covered here (each sufficient alone):

1. ``UnifiedMessage.parse_content`` — the ``call_id`` → ``id`` alias, so a
   storage-shaped dict round-trip can never strip the join key again.
2. ``MessageList.sanitize`` Pass 1.5 — repairs an id-less tool_use by
   adopting the unique matching adjacent tool_result's id; drops the block
   when no unambiguous adoption exists (an empty id must never reach a
   provider).
"""

from __future__ import annotations

from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import TextContent, reconstruct_content


def test_parse_content_preserves_call_id_alias() -> None:
    blocks = UnifiedMessage.parse_content(
        [
            {
                "type": "tool_call",
                "name": "kindcomp_get_context",
                "call_id": "toolu_ABC",
                "arguments": {"kind": "flashcard_deck"},
            }
        ]
    )
    assert len(blocks) == 1
    assert isinstance(blocks[0], ToolCallContent)
    assert blocks[0].id == "toolu_ABC"


def test_canonical_call_id_wins_when_both_keys_present() -> None:
    """``call_id`` is the canonical storage key; ``id`` is the legacy fallback.

    Both rebuild paths must agree on that precedence — a disagreement is the
    parity break that caused the 2026-07-18 outage. Pinned here and in
    ``test_content_deserializer_parity.py``.
    """
    block = {"type": "tool_call", "name": "t", "id": "toolu_LEGACY", "call_id": "toolu_CANON"}
    via_parse = UnifiedMessage.parse_content([block])[0]
    via_reconstruct = reconstruct_content(block)
    assert isinstance(via_parse, ToolCallContent)
    assert via_parse.id == "toolu_CANON"
    assert via_reconstruct.id == via_parse.id


def test_storage_roundtrip_preserves_id() -> None:
    original = ToolCallContent(id="toolu_XYZ", name="t", arguments={"a": 1})
    stored = original.to_storage_dict()
    assert stored["call_id"] == "toolu_XYZ"
    rebuilt = reconstruct_content(stored)
    assert isinstance(rebuilt, ToolCallContent)
    assert rebuilt.id == "toolu_XYZ"
    reparsed = UnifiedMessage.parse_content([stored])[0]
    assert isinstance(reparsed, ToolCallContent)
    assert reparsed.id == "toolu_XYZ"


def _convo_with_idless_call() -> MessageList:
    return MessageList(
        _messages=[
            UnifiedMessage(role="user", content=[TextContent(text="go")]),
            UnifiedMessage(
                role="assistant",
                content=[
                    TextContent(text="calling"),
                    ToolCallContent(id="", name="kindcomp_get_context", arguments={}),
                ],
            ),
            UnifiedMessage(
                role="tool",
                content=[
                    ToolResultContent(
                        tool_use_id="toolu_REAL",
                        call_id="toolu_REAL",
                        name="kindcomp_get_context",
                        content="ok",
                    )
                ],
            ),
            UnifiedMessage(role="assistant", content=[TextContent(text="done")]),
        ]
    )


def test_sanitize_repairs_idless_tool_use_from_adjacent_result() -> None:
    ml = _convo_with_idless_call()
    ml.sanitize()
    assistant = ml[1]
    calls = [c for c in assistant.content if isinstance(c, ToolCallContent)]
    assert len(calls) == 1
    assert calls[0].id == "toolu_REAL"
    # The result survives too — the pair is whole again.
    results = [c for m in ml for c in m.content if isinstance(c, ToolResultContent)]
    assert len(results) == 1
    assert results[0].tool_use_id == "toolu_REAL"


def test_sanitize_drops_idless_tool_use_when_ambiguous() -> None:
    ml = MessageList(
        _messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    TextContent(text="calling twice"),
                    ToolCallContent(id="", name="t", arguments={}),
                ],
            ),
            UnifiedMessage(
                role="tool",
                content=[
                    ToolResultContent(tool_use_id="toolu_A", name="t", content="a"),
                    ToolResultContent(tool_use_id="toolu_B", name="t", content="b"),
                ],
            ),
            UnifiedMessage(role="assistant", content=[TextContent(text="end")]),
        ]
    )
    ml.sanitize()
    # The id-less call is gone; nothing with an empty id may reach a provider.
    for msg in ml:
        for c in msg.content:
            if isinstance(c, ToolCallContent):
                assert c.id, "empty-id tool_use survived sanitize"


def test_sanitize_never_adopts_an_already_claimed_id() -> None:
    ml = MessageList(
        _messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    ToolCallContent(id="toolu_A", name="t", arguments={}),
                    ToolCallContent(id="", name="t", arguments={}),
                ],
            ),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id="toolu_A", name="t", content="a")],
            ),
            UnifiedMessage(role="assistant", content=[TextContent(text="end")]),
        ]
    )
    ml.sanitize()
    calls = [c for m in ml for c in m.content if isinstance(c, ToolCallContent)]
    ids = [c.id for c in calls]
    assert ids.count("toolu_A") == 1
    assert "" not in ids
