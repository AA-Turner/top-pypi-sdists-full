"""Every Anthropic request we build is legal under API version 2026-10-21.

anthropic>=2.0 sends ``anthropic-version: 2026-10-21``, which turns these into a 400
(https://platform.claude.com/docs/en/api/migration-2026-10-21):

  * ``temperature`` / ``top_p`` / ``top_k`` on ANY model (not only the adaptive ones);
  * a ``document`` block directly in an ``assistant`` message;
  * a ``text`` block with a non-empty ``citations`` array in a ``user`` message
    (``search_result`` blocks may still carry the ``{"enabled": true}`` setting).

These render real conversations — a document the person sent, an assistant answer that
carried citations, a document left on an assistant turn, a cited tool result — through the
real translator and read the payload, so the SDK bump cannot ship a request shape the new
API version refuses.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.media_config import DocumentContent
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

_CITATION = {
    "type": "web_search_result_location",
    "url": "https://example.com/a",
    "title": "A",
    "cited_text": "the sky is blue",
    "encrypted_index": "x",
}


def _pdf() -> DocumentContent:
    return DocumentContent(base64_data="JVBERi0xLjQK", mime_type="application/pdf")


def _conversation() -> list[UnifiedMessage]:
    cited = TextContent(text="The sky is blue.", metadata={"citations": [_CITATION]})
    return [
        UnifiedMessage(role="user", content=[TextContent(text="Read this."), _pdf()]),
        UnifiedMessage(role="assistant", content=[cited, _pdf()]),
        UnifiedMessage(role="user", content=[TextContent(text="Quote it back.", metadata={"citations": [_CITATION]})]),
    ]


def _build(**config_kwargs: Any) -> dict[str, Any]:
    config = UnifiedConfig(model="claude-x", messages=MessageList(_messages=_conversation()), **config_kwargs)
    profile = make_profile(model_name="claude-x", wire_format="anthropic_chat")
    prep = order_for_wire(config, profile)
    request = AnthropicTranslator().build_request(prep.wire_config if prep.wire_config is not None else config, profile)
    return request if isinstance(request, dict) else dict(request)


def _blocks(message: dict[str, Any]) -> list[dict[str, Any]]:
    content = message.get("content")
    return content if isinstance(content, list) else [{"type": "text", "text": content}]


def test_no_assistant_message_carries_a_document_block() -> None:
    for message in _build()["messages"]:
        if message["role"] == "assistant":
            assert all(b.get("type") != "document" for b in _blocks(message)), message


def test_no_user_text_block_carries_citations() -> None:
    for message in _build()["messages"]:
        if message["role"] != "user":
            continue
        for block in _blocks(message):
            if block.get("type") == "text":
                assert not block.get("citations"), block


def test_the_persons_document_still_reaches_the_model() -> None:
    first_user = next(m for m in _build()["messages"] if m["role"] == "user")
    assert any(b.get("type") == "document" for b in _blocks(first_user))


def test_the_fallback_seam_converts_a_document_on_a_claude_assistant_turn_first() -> None:
    # Layer 1: the seam (convert-to-text, notice) sees it before the translator's backstop.
    from matrx_ai.providers.provider_io_capabilities import content_needs_fallback

    assert content_needs_fallback(_pdf(), "anthropic_chat", role="assistant") is True
    assert content_needs_fallback(_pdf(), "anthropic_chat", role="user") is False
    assert content_needs_fallback(_pdf(), "google_chat", role="assistant") is False


@pytest.mark.parametrize("knob", ["temperature", "top_p", "top_k"])
def test_no_sampling_parameter_reaches_the_payload(knob: str) -> None:
    value = {"temperature": 0.2, "top_p": 0.5, "top_k": 5}[knob]
    request = _build(**{knob: value})
    assert knob not in request, request.get(knob)
    assert knob not in (request.get("extra_body") or {}), request.get("extra_body")
