"""Layer 1 regression: UnifiedMessage.get_output() must return the ANSWER only.

Thinking/reasoning welded into result.output was the root of two failures:
(1) reasoning surfaced as undifferentiated plain text in non-streaming
consumers, and (2) a JSON draft written inside the model's thinking outranked
the real final answer during extraction. get_output() now excludes
ThinkingContent; get_thinking() is the deliberate opt-in for reasoning.

    uv run pytest packages/matrx-ai/matrx_ai/config/tests/test_get_output_excludes_thinking.py
"""

from __future__ import annotations

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.config.enums import Role


def _msg() -> UnifiedMessage:
    return UnifiedMessage(
        role=Role.ASSISTANT,
        content=[
            ThinkingContent(text="Let me draft: {\"set_title\": \"DRAFT\"}", provider="google"),
            ThinkingContent(text="Now finalize.", provider="google"),
            TextContent(text='{"set_title": "FINAL", "cards": []}'),
        ],
    )


def test_get_output_excludes_thinking() -> None:
    out = _msg().get_output()
    assert out == '{"set_title": "FINAL", "cards": []}'
    assert "DRAFT" not in out
    assert "finalize" not in out.lower()


def test_get_thinking_returns_only_reasoning() -> None:
    thinking = _msg().get_thinking()
    assert "DRAFT" in thinking
    assert "Now finalize." in thinking
    assert "FINAL" not in thinking


def test_get_output_pure_text_unchanged() -> None:
    msg = UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="hello")])
    assert msg.get_output() == "hello"
    assert msg.get_thinking() == ""
