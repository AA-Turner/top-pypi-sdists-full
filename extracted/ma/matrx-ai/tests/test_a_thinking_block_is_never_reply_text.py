"""A model's private reasoning is never read as its reply (sweep after run 57db7ef9, 2026-10-29).

THE DEFECT CLASS. A stored ``thinking`` block keeps the model's reasoning under ``text`` — the same key
the answer uses — so a reader that takes "any block with a text field" puts the reasoning in front of
every answer. The agent-test sink did exactly that and failed the "exactly these lines" fact. These are
its siblings inside matrx-ai; each test is red when its reader goes back to reading any ``text``:

* ``content_text`` (THE one reader of a message body)       — drop the ``type`` gate;
* ``revision._text_of`` (the answer a revision is judged on)  — read ``item.text`` again;
* ``memory.llm_adapter._extract_response_text`` (Observer/Reflector output that is WRITTEN INTO MEMORY);
* ``executor._assistant_text_from_response`` (the only text a directive fence may run from — a fence in
  the model's reasoning must never execute);
* ``conversation_persistence._text_of`` (history handed back to a caller).
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config.message_config import NOT_REPLY_BLOCK_TYPES, content_text
from matrx_ai.config.unified_content import TextContent, ThinkingContent

REASONING = "I should reply with exactly two lines and never mention this."
REPLY = "Line one\nLine two"


def _typed() -> list:
    return [ThinkingContent(text=REASONING, provider="anthropic"), TextContent(text=REPLY)]


def _stored() -> list[dict]:
    return [{k: v for k, v in b.to_storage_dict().items()} for b in _typed()]


def test_content_text_reads_text_blocks_only_in_every_shape():
    assert content_text(_stored()) == REPLY
    assert content_text(_typed()) == REPLY
    for kind in NOT_REPLY_BLOCK_TYPES:
        assert content_text([{"type": kind, "text": REASONING}, {"type": "text", "text": REPLY}]) == REPLY


def test_content_text_separator_is_the_callers():
    blocks = [{"type": "text", "text": "ratios"}, {"type": "text", "text": ", and more"}]
    assert content_text(blocks, sep="") == "ratios, and more"
    assert content_text(blocks) == "ratios\n, and more"


def test_revision_answer_leaves_out_reasoning():
    from matrx_ai.revision import _text_of

    assert _text_of(SimpleNamespace(content=_typed())) == REPLY


def test_memory_output_leaves_out_reasoning():
    from matrx_ai.memory.llm_adapter import _extract_response_text

    response = SimpleNamespace(messages=[SimpleNamespace(role="assistant", content=_typed())])
    assert _extract_response_text(response) == REPLY


def test_a_directive_fence_in_reasoning_is_not_scanned():
    from matrx_ai.orchestrator.executor import _assistant_text_from_response

    fence = "```matrx\n{\"directive\": \"x\"}\n```"
    content = [ThinkingContent(text=fence, provider="anthropic"), TextContent(text="Done.")]
    response = SimpleNamespace(messages=[SimpleNamespace(role="assistant", content=content)])
    assert _assistant_text_from_response(response) == "Done."


def test_history_text_leaves_out_reasoning():
    from matrx_ai.orchestrator.conversation_persistence import _text_of

    assert _text_of(SimpleNamespace(content=_typed())) == REPLY
