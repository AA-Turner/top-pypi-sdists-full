"""GUARD: a plain reply from an OpenAI reasoning model is ONE assistant message.

Live 2026-10-12 (gpt-5-mini "Reply with the word ok", admin@admin.com): the stream announced
TWO assistant rows -- the loop-start reservation (position 1) and a late
``iteration_persist`` row (position 2) -- because the translator split the reasoning
item (role='output') and the answer text into two messages. The client streams the answer
onto the FIRST reservation, so the finished turn rendered blank until a reload.

A turn produces exactly the rows it fills: reasoning + answer share one assistant message;
tool calls keep their own LAST message (their ordering rule is unchanged).
"""

from __future__ import annotations

from openai.types.responses import (
    ResponseFunctionToolCall,
    ResponseOutputMessage,
    ResponseOutputText,
    ResponseReasoningItem,
)

from matrx_ai.providers.openai.translator import OpenAITranslator


def _reasoning(i: str = "rs_1"):
    return ResponseReasoningItem(type="reasoning", id=i, summary=[], encrypted_content="enc")


def _message(text: str):
    return ResponseOutputMessage(
        type="message",
        id="msg_1",
        role="assistant",
        status="completed",
        content=[ResponseOutputText(type="output_text", text=text, annotations=[])],
    )


def _call():
    return ResponseFunctionToolCall(
        type="function_call", id="fc_1", call_id="call_1", name="t", arguments="{}", status="completed"
    )


def _roles(items):
    msgs = OpenAITranslator()._build_unified_messages(items)
    return [(getattr(m.role, "value", m.role), [type(c).__name__ for c in m.content]) for m in msgs]


def test_reasoning_then_answer_is_one_assistant_message():
    out = _roles([_reasoning(), _message("ok")])
    assert out == [("assistant", ["ThinkingContent", "TextContent"])], out


def test_tool_calls_keep_their_own_last_message():
    out = _roles([_reasoning(), _message("working"), _call()])
    assert [r for r, _ in out] == ["assistant", "assistant"], out
    assert out[-1][1] == ["ToolCallContent"], out
