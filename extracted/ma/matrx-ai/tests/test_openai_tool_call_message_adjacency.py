"""Every tool call in a turn must survive to ``cx_message`` (2026-08-11 incident).

Conversation ``b0562a35-786b-4508-bbc4-0e7bfad7314d``: an agent made two
``agent_call`` tool calls across two provider iterations. Both completed and
both landed in ``chat.tool_call`` with full output — but only the SECOND one
existed as a ``chat.message`` content part. Live, both cards rendered; after a
page reload the first call's work was simply gone from the transcript, and the
model never saw it in its own history on the next iteration either.

The chain:

1. ``OpenAITranslator._build_unified_messages`` grouped the turn's
   ``function_call`` blocks with the reasoning blocks in the leading ``output``
   message, then appended the assistant TEXT as a SEPARATE later message.
2. The executor appends the turn's ``role='tool'`` results after those, so the
   list read: ``output[thinking, tool_use] → assistant[text] → tool[result]``.
   A text message now sat BETWEEN a tool_use and its tool_result.
3. ``MessageList.sanitize``'s adjacency pass (correctly — Anthropic 400s a
   non-adjacent pair) dropped the tool_use as "non-adjacent", then dropped its
   now-orphaned tool_result, then dropped the emptied ``role='tool'`` message.
   Nothing remained for persistence to write.

Iteration 2 escaped only because that response happened to carry no text, so
its tool_use was already adjacent to its result.

Fix: tool calls are emitted LAST, in their own ``assistant`` message, so the
tool_use blocks are always immediately followed by their results.
"""

from __future__ import annotations

from openai.types.responses import (
    ResponseFunctionToolCall,
    ResponseOutputMessage,
    ResponseOutputText,
    ResponseReasoningItem,
)

from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.providers.openai.translator import OpenAITranslator


def _reasoning(item_id: str = "rs_1") -> ResponseReasoningItem:
    return ResponseReasoningItem(
        id=item_id, type="reasoning", summary=[], encrypted_content="enc"
    )


def _text_message(text: str = "I'll do it.", item_id: str = "msg_1") -> ResponseOutputMessage:
    return ResponseOutputMessage(
        id=item_id,
        type="message",
        role="assistant",
        status="completed",
        content=[ResponseOutputText(type="output_text", text=text, annotations=[])],
    )


def _function_call(call_id: str, item_id: str) -> ResponseFunctionToolCall:
    return ResponseFunctionToolCall(
        id=item_id,
        call_id=call_id,
        name="agent_call",
        arguments='{"agent_id": "a"}',
        type="function_call",
    )


def _content_types(messages: list[UnifiedMessage]) -> list[tuple[str, list[str]]]:
    return [
        (
            m.role.value if hasattr(m.role, "value") else str(m.role),
            [type(c).__name__ for c in m.content],
        )
        for m in messages
    ]


def _turn(messages: list[UnifiedMessage], *call_ids: str) -> MessageList:
    """The message list the executor assembles: the turn's provider messages
    followed by the ``role='tool'`` message carrying that turn's results."""
    return MessageList(
        _messages=[
            UnifiedMessage(role=Role.USER, content=[TextContent(text="do the thing")]),
            *messages,
            UnifiedMessage(
                role=Role.TOOL,
                content=[
                    ToolResultContent(
                        tool_use_id=cid, call_id=cid, name="agent_call", content="ok"
                    )
                    for cid in call_ids
                ],
            ),
        ]
    )


def _surviving_tool_use_ids(message_list: MessageList) -> set[str]:
    return {
        c.id
        for m in message_list._messages
        for c in m.content
        if isinstance(c, ToolCallContent) and c.id
    }


def _surviving_tool_result_ids(message_list: MessageList) -> set[str]:
    return {
        (c.tool_use_id or c.call_id)
        for m in message_list._messages
        for c in m.content
        if isinstance(c, ToolResultContent)
    }


# ---------------------------------------------------------------------------
# Translator — tool calls last, in their own assistant message
# ---------------------------------------------------------------------------


def test_tool_calls_are_emitted_after_the_text_message() -> None:
    """reasoning + text + function_call — the incident shape."""
    messages = OpenAITranslator()._build_unified_messages(
        [_reasoning(), _text_message(), _function_call("call_A", "fc_1")]
    )

    assert _content_types(messages) == [
        ("output", ["ThinkingContent"]),
        ("assistant", ["TextContent"]),
        ("assistant", ["ToolCallContent"]),
    ]


def test_tool_calls_last_without_reasoning() -> None:
    """text + function_call, no reasoning — the same break, one layer down."""
    messages = OpenAITranslator()._build_unified_messages(
        [_text_message(), _function_call("call_A", "fc_1")]
    )

    assert _content_types(messages) == [
        ("assistant", ["TextContent"]),
        ("assistant", ["ToolCallContent"]),
    ]


def test_parallel_tool_calls_share_one_trailing_message() -> None:
    """Parallel calls stay in ONE message so a single tool message answers them
    all — splitting them would strand every call but the last."""
    messages = OpenAITranslator()._build_unified_messages(
        [
            _reasoning(),
            _text_message(),
            _function_call("call_A", "fc_1"),
            _function_call("call_B", "fc_2"),
        ]
    )

    assert _content_types(messages) == [
        ("output", ["ThinkingContent"]),
        ("assistant", ["TextContent"]),
        ("assistant", ["ToolCallContent", "ToolCallContent"]),
    ]


def test_text_only_response_is_one_assistant_message() -> None:
    messages = OpenAITranslator()._build_unified_messages([_text_message()])
    assert _content_types(messages) == [("assistant", ["TextContent"])]


def test_reasoning_then_text_ordering_is_preserved() -> None:
    """No tool calls — reasoning must still LEAD, or the Responses API rejects a
    reasoning item that is not followed by its associated output item."""
    messages = OpenAITranslator()._build_unified_messages([_reasoning(), _text_message()])
    assert _content_types(messages) == [
        ("output", ["ThinkingContent"]),
        ("assistant", ["TextContent"]),
    ]


def test_replayed_item_order_matches_openai_output_order() -> None:
    """Flattened for the Responses API: reasoning → message → function_call."""
    messages = OpenAITranslator()._build_unified_messages(
        [_reasoning(), _text_message(), _function_call("call_A", "fc_1")]
    )
    items = [item for m in messages for item in m.to_openai_items_modified()]

    assert [item.get("type") for item in items] == ["reasoning", "message", "function_call"]


# ---------------------------------------------------------------------------
# sanitize — the turn survives the adjacency guard
# ---------------------------------------------------------------------------


def test_translated_turn_survives_sanitize() -> None:
    """THE regression: the translated turn plus its tool results must come out
    of ``sanitize`` with every tool_use and tool_result intact."""
    messages = OpenAITranslator()._build_unified_messages(
        [_reasoning(), _text_message(), _function_call("call_A", "fc_1")]
    )
    message_list = _turn(messages, "call_A")

    message_list.sanitize()

    assert _surviving_tool_use_ids(message_list) == {"call_A"}
    assert _surviving_tool_result_ids(message_list) == {"call_A"}


def test_translated_parallel_turn_survives_sanitize() -> None:
    messages = OpenAITranslator()._build_unified_messages(
        [
            _reasoning(),
            _text_message(),
            _function_call("call_A", "fc_1"),
            _function_call("call_B", "fc_2"),
        ]
    )
    message_list = _turn(messages, "call_A", "call_B")

    message_list.sanitize()

    assert _surviving_tool_use_ids(message_list) == {"call_A", "call_B"}
    assert _surviving_tool_result_ids(message_list) == {"call_A", "call_B"}


def test_multi_iteration_turn_keeps_every_tool_call() -> None:
    """Two iterations, each with reasoning + text + one call — the exact live
    conversation. Before the fix, iteration 1's call was deleted and only
    iteration 2's reached persistence."""
    translator = OpenAITranslator()
    iteration_one = translator._build_unified_messages(
        [_reasoning("rs_1"), _text_message("First.", "msg_1"), _function_call("call_A", "fc_1")]
    )
    iteration_two = translator._build_unified_messages(
        [_reasoning("rs_2"), _text_message("Second.", "msg_2"), _function_call("call_B", "fc_2")]
    )

    def tool_message(call_id: str) -> UnifiedMessage:
        return UnifiedMessage(
            role=Role.TOOL,
            content=[
                ToolResultContent(
                    tool_use_id=call_id, call_id=call_id, name="agent_call", content="ok"
                )
            ],
        )

    message_list = MessageList(
        _messages=[
            UnifiedMessage(role=Role.USER, content=[TextContent(text="do the thing")]),
            *iteration_one,
            tool_message("call_A"),
            *iteration_two,
            tool_message("call_B"),
        ]
    )

    message_list.sanitize()

    assert _surviving_tool_use_ids(message_list) == {"call_A", "call_B"}
    assert _surviving_tool_result_ids(message_list) == {"call_A", "call_B"}


def _old_translator_shape() -> MessageList:
    """What the pre-fix translator produced: tool_use grouped with the reasoning,
    the assistant text emitted after it, results after that."""
    return MessageList(
        _messages=[
            UnifiedMessage(role=Role.USER, content=[TextContent(text="do the thing")]),
            UnifiedMessage(
                role=Role.OUTPUT,
                content=[
                    ThinkingContent(text="thinking", id="rs_1"),
                    ToolCallContent(id="call_A", name="agent_call", arguments={}),
                ],
            ),
            UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="I'll do it.")]),
            UnifiedMessage(
                role=Role.TOOL,
                content=[
                    ToolResultContent(
                        tool_use_id="call_A", call_id="call_A", name="agent_call", content="ok"
                    )
                ],
            ),
        ]
    )


def test_sanitize_still_drops_a_genuinely_separated_tool_use() -> None:
    """The guard itself is unchanged — the pre-fix shape must still be caught
    rather than silently shipped to a provider that 400s on it. Pinned so a
    future 'fix' does not weaken the adjacency rule instead of fixing the
    producer."""
    message_list = _old_translator_shape()

    message_list.sanitize()

    assert _surviving_tool_use_ids(message_list) == set()
    assert _surviving_tool_result_ids(message_list) == set()


def test_separated_drop_is_not_reported_as_a_duplicate(monkeypatch) -> None:
    """The drop is classified ``separated``, not ``duplicated``.

    Mislabelling this shape a "duplicate" — telling the reader some other turn
    absorbed the tool_use, and that the adjacently-paired copy survived — is
    why 251 of these alarms in 30 days pointed at the wrong code and none of
    them got acted on.
    """
    from matrx_ai.config import message_config

    captured: list[list[dict[str, object]]] = []
    monkeypatch.setattr(
        message_config,
        "report_nonadjacent_tool_uses",
        lambda *, layer, dropped: captured.append(dropped),
    )

    _old_translator_shape().sanitize()

    assert captured, "the separated tool_use must still be reported"
    assert [d.get("reason") for d in captured[0]] == ["separated"]


def test_a_real_duplicate_is_still_classified_duplicated(monkeypatch) -> None:
    """The same id re-emitted in a later, adjacently-paired turn keeps the
    original diagnosis — the stray copy is dropped, the paired one survives."""
    from matrx_ai.config import message_config

    captured: list[list[dict[str, object]]] = []
    monkeypatch.setattr(
        message_config,
        "report_nonadjacent_tool_uses",
        lambda *, layer, dropped: captured.append(dropped),
    )

    def tool_use(call_id: str) -> ToolCallContent:
        return ToolCallContent(id=call_id, name="agent_call", arguments={})

    message_list = MessageList(
        _messages=[
            UnifiedMessage(role=Role.USER, content=[TextContent(text="do the thing")]),
            # Absorbed a tool_use belonging to the next turn.
            UnifiedMessage(role=Role.ASSISTANT, content=[tool_use("call_A"), tool_use("call_B")]),
            UnifiedMessage(
                role=Role.TOOL,
                content=[
                    ToolResultContent(
                        tool_use_id="call_A", call_id="call_A", name="agent_call", content="ok"
                    )
                ],
            ),
            UnifiedMessage(role=Role.ASSISTANT, content=[tool_use("call_B")]),
            UnifiedMessage(
                role=Role.TOOL,
                content=[
                    ToolResultContent(
                        tool_use_id="call_B", call_id="call_B", name="agent_call", content="ok"
                    )
                ],
            ),
        ]
    )

    message_list.sanitize()

    assert captured, "the stray duplicate must still be reported"
    assert [d.get("reason") for d in captured[0]] == ["duplicated"]
    # The adjacently-paired copies survive — this drop is lossless.
    assert _surviving_tool_use_ids(message_list) == {"call_A", "call_B"}
    assert _surviving_tool_result_ids(message_list) == {"call_A", "call_B"}
