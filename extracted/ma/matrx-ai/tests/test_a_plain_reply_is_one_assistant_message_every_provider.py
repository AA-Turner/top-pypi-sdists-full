"""GUARD: one model turn -> ONE assistant-side message, for every non-OpenAI translator.

Sibling sweep of test_a_plain_reasoning_reply_is_one_assistant_row (OpenAI fixed
2026-10-12 589eba28a4). A translator that splits one provider reply (thinking + answer,
search/hosted-tool blocks + answer) into several UnifiedMessages makes the loop announce
several assistant rows; the client streams the answer onto the first reservation and the
finished reply renders blank. Captured-shape responses below; each asserts exactly one
message with thinking BEFORE the answer (provider replay order).
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace as NS

from matrx_ai.config.message_config import ThinkingContent, TextContent


def _kinds(msgs):
    assert len(msgs) == 1, [(m.role, [type(c).__name__ for c in m.content]) for m in msgs]
    assert getattr(msgs[0].role, "value", msgs[0].role) == "assistant"
    return [type(c).__name__ for c in msgs[0].content]


def _chat_response(reasoning_field: str):
    msg = NS(content="ok", tool_calls=None, role="assistant", annotations=None)
    setattr(msg, reasoning_field, "thinking about it")
    usage = NS(prompt_tokens=5, completion_tokens=3, prompt_tokens_details=None,
               completion_tokens_details=None, total_tokens=8)
    return NS(id="r1", model="m", choices=[NS(message=msg, finish_reason="stop")], usage=usage)


def test_anthropic_thinking_search_and_answer_is_one_message():
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    resp = {
        "id": "msg_1", "role": "assistant", "stop_reason": "end_turn",
        "content": [
            {"type": "thinking", "thinking": "hmm", "signature": "sig"},
            {"type": "server_tool_use", "id": "srv_1", "name": "web_search", "input": {"query": "q"}},
            {"type": "web_search_tool_result", "tool_use_id": "srv_1", "content": []},
            {"type": "text", "text": "ok"},
        ],
        "usage": {"input_tokens": 5, "output_tokens": 3},
    }
    out = AnthropicTranslator().from_anthropic(resp, "claude-test")
    kinds = _kinds(out.messages)
    assert kinds[0] == "ThinkingContent" and kinds[-1] == "TextContent", kinds


def test_cerebras_reasoning_and_answer_is_one_message():
    from matrx_ai.providers.cerebras.translator import CerebrasTranslator

    out = CerebrasTranslator().from_cerebras(_chat_response("reasoning"))
    assert _kinds(out.messages) == ["ThinkingContent", "TextContent"]


def test_groq_reasoning_and_answer_is_one_message():
    from matrx_ai.providers.groq.translator import GroqTranslator

    out = GroqTranslator().from_groq(_chat_response("reasoning"))
    assert _kinds(out.messages) == ["ThinkingContent", "TextContent"]


def test_together_reasoning_and_answer_is_one_message():
    from matrx_ai.providers.together.translator import TogetherTranslator

    out = TogetherTranslator().from_together(_chat_response("reasoning_content"))
    assert _kinds(out.messages) == ["ThinkingContent", "TextContent"]


def test_generic_openai_reasoning_and_answer_is_one_message():
    from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator

    out = GenericOpenAITranslator().from_generic_openai(_chat_response("reasoning_content"))
    assert _kinds(out.messages) == ["ThinkingContent", "TextContent"]


def test_xai_reasoning_and_answer_is_one_message():
    from matrx_ai.providers.xai.translator import XAITranslator

    resp = NS(reasoning_content="thinking", content="ok", tool_calls=[], usage=None, id="r1", proto=NS(model="grok"), finish_reason="REASON_STOP")
    out = XAITranslator().from_xai(resp)
    assert _kinds(out.messages) == ["ThinkingContent", "TextContent"]


def test_google_thought_search_and_answer_is_one_message():
    from google.genai import types as gt
    from matrx_ai.providers.google.translator import GoogleTranslator

    cand = gt.Candidate(
        content=gt.Content(role="model", parts=[
            gt.Part(text="thinking", thought=True),
            gt.Part(text="ok", thought_signature=b"sig"),
        ]),
        finish_reason=gt.FinishReason.STOP,
        grounding_metadata=gt.GroundingMetadata(web_search_queries=["q"]),
    )
    chunk = gt.GenerateContentResponse(
        candidates=[cand], model_version="gemini-3", response_id="r",
        usage_metadata=gt.GenerateContentResponseUsageMetadata(
            prompt_token_count=5, candidates_token_count=3, total_token_count=8),
    )
    out = asyncio.run(GoogleTranslator().from_google_async([chunk], "gemini-test"))
    kinds = _kinds(out.messages)
    assert "TextContent" in kinds and kinds[-1] == "TextContent", kinds
