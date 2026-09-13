"""Wall W49 — an unanswered tool call is never erased in silence.

THE INCIDENT (2026-09-12, Masterwork Conductor, conversation
``a66e995b-495f-4640-a032-adc846f0cf80``): the Conductor called the
client-delegated ``apply_surface_write`` to stage a new rule. The browser tab
was on the plain ``/chat/<id>`` page — no surface handlers — so the answer never
reached the server. ``MessageList.sanitize`` then DROPPED the orphan ``tool_use``
to satisfy the provider's pairing rule; because that assistant message carried
nothing else, the message itself was dropped whole. The turn ended with NOTHING
on screen and the next turn's model had no idea its write had never happened.

These are the failing-then-passing guards for the repair. Each one FAILS against
the pre-fix sanitizer (which dropped the block) and passes now:

1. A true orphan keeps its assistant message, and gains a synthesized
   ``is_error`` tool_result whose text tells the model the call never happened.
2. The synthesized result is ADJACENT — it does not break the provider's
   pairing rule it exists to satisfy — and a real sibling result in the same
   turn still pairs.
3. The repair is loud: the guard reports it (banner + durable ERROR log).
4. It repairs ONLY true orphans, and at most once per id, so it can never mint
   the duplicate ``tool_result`` this module exists to prevent.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import TextContent


def _result_blocks(messages: list[UnifiedMessage]) -> list[ToolResultContent]:
    return [c for m in messages for c in m.content if isinstance(c, ToolResultContent)]


def _call_blocks(messages: list[UnifiedMessage]) -> list[ToolCallContent]:
    return [c for m in messages for c in m.content if isinstance(c, ToolCallContent)]


def _delegated_write_turn() -> MessageList:
    """The exact shape W49 produced: an assistant turn that is ONLY the call."""
    return MessageList(
        [
            UnifiedMessage(role=Role.USER, content=[TextContent(text="Write that rule down.")]),
            UnifiedMessage(
                role=Role.ASSISTANT,
                content=[
                    ToolCallContent(
                        id="toolu_w49",
                        name="apply_surface_write",
                        arguments={"target": "rule_draft", "value": {"mode": "new"}},
                    )
                ],
            ),
        ]
    )


def test_orphan_call_survives_with_a_synthesized_error_result() -> None:
    messages = _delegated_write_turn()
    messages.sanitize()
    out = list(messages)

    calls = _call_blocks(out)
    assert [c.id for c in calls] == ["toolu_w49"], (
        "the assistant's tool_use was erased — this is the W49 silence"
    )

    results = _result_blocks(out)
    assert len(results) == 1
    synthesized = results[0]
    assert synthesized.tool_use_id == "toolu_w49"
    assert synthesized.is_error is True
    assert synthesized.metadata.get("reason") == "orphan_tool_use"
    # The sentence must NAME the tool and say plainly that nothing happened.
    text = str(synthesized.content)
    assert "apply_surface_write" in text
    assert "Nothing was written" in text


def test_the_synthesized_result_is_adjacent_to_its_call() -> None:
    """The repair must satisfy the very rule the old drop existed to satisfy."""
    messages = _delegated_write_turn()
    messages.sanitize()
    out = list(messages)

    call_index = next(
        i for i, m in enumerate(out) if any(isinstance(c, ToolCallContent) for c in m.content)
    )
    following = out[call_index + 1]
    assert str(following.role) == str(Role.TOOL)
    assert any(
        isinstance(c, ToolResultContent) and c.tool_use_id == "toolu_w49"
        for c in following.content
    )


def test_a_real_sibling_result_still_pairs_when_one_call_goes_unanswered() -> None:
    """Two calls, one answered: the answered one keeps its REAL result."""
    messages = MessageList(
        [
            UnifiedMessage(role=Role.USER, content=[TextContent(text="go")]),
            UnifiedMessage(
                role=Role.ASSISTANT,
                content=[
                    ToolCallContent(id="answered", name="read_page", arguments={}),
                    ToolCallContent(id="never_answered", name="apply_surface_write", arguments={}),
                ],
            ),
            UnifiedMessage(
                role=Role.TOOL,
                content=[
                    ToolResultContent(
                        tool_use_id="answered", call_id="answered", name="read_page", content="ok"
                    )
                ],
            ),
        ]
    )
    messages.sanitize()
    out = list(messages)

    assert {c.id for c in _call_blocks(out)} == {"answered", "never_answered"}
    by_id = {r.tool_use_id: r for r in _result_blocks(out)}
    assert by_id["answered"].content == "ok"
    assert by_id["answered"].is_error is False
    assert by_id["never_answered"].is_error is True


def test_repair_is_reported_loudly(monkeypatch: Any) -> None:
    seen: list[list[dict[str, Any]]] = []

    import matrx_ai.config.message_config as message_config

    monkeypatch.setattr(
        message_config,
        "report_orphan_tool_uses_repaired",
        lambda *, layer, repaired: seen.append(repaired),
    )
    _delegated_write_turn().sanitize()

    assert seen, "an unanswered tool call was repaired without saying so"
    assert seen[0][0]["tool_use_id"] == "toolu_w49"
    assert seen[0][0]["name"] == "apply_surface_write"


def test_never_mints_a_second_result_for_an_answered_call() -> None:
    """The duplicate-tool_result 400 this module exists to stop, in reverse."""
    messages = MessageList(
        [
            UnifiedMessage(role=Role.USER, content=[TextContent(text="go")]),
            UnifiedMessage(
                role=Role.ASSISTANT,
                content=[ToolCallContent(id="X", name="read_page", arguments={})],
            ),
            UnifiedMessage(
                role=Role.TOOL,
                content=[
                    ToolResultContent(
                        tool_use_id="X", call_id="X", name="read_page", content="real"
                    )
                ],
            ),
        ]
    )
    messages.sanitize()
    results = _result_blocks(list(messages))
    assert len(results) == 1
    assert results[0].content == "real"


def test_a_doubly_emitted_unanswered_call_is_repaired_exactly_once() -> None:
    """Two tool_use blocks share one id and neither was answered.

    One synthetic result, never two — a second would be the exact duplicate
    that 400s the whole request.
    """
    messages = MessageList(
        [
            UnifiedMessage(role=Role.USER, content=[TextContent(text="go")]),
            UnifiedMessage(
                role=Role.ASSISTANT,
                content=[ToolCallContent(id="dup", name="apply_surface_write", arguments={})],
            ),
            UnifiedMessage(
                role=Role.ASSISTANT,
                content=[ToolCallContent(id="dup", name="apply_surface_write", arguments={})],
            ),
        ]
    )
    messages.sanitize()
    results = _result_blocks(list(messages))
    assert len(results) == 1, "a second synthetic result would 400 the whole request"
