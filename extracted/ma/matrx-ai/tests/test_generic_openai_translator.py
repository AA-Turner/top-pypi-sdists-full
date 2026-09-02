"""Phase 3b — GenericOpenAITranslator vision support tests.

Locks the contract for routing ImageContent through llama-server /
Ollama / vLLM / LocalAI:

* When a message has ImageContent + TextContent, the translator emits
  the OpenAI Chat Completions multimodal content array
  (``[{"type": "text", "text": ...}, {"type": "image_url", "image_url": {"url": ...}}]``).
* When a message has TextContent only, the translator keeps the
  legacy string-content path (backwards-compat for text-only models).
* URLs go through unchanged; base64_data becomes a ``data:`` URI with
  the correct mime type.
* file_uri / file_id without a resolved url/base64 get dropped (and
  logged) — matches the existing drop-on-unresolvable behavior of
  ``ImageContent.to_openai`` / ``to_anthropic``.
"""

from __future__ import annotations

import types

import pytest

from matrx_ai.config import (
    ModelPricing,
    PricingTier,
    TextContent,
    ThinkingContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.config.media_config import ImageContent, VideoContent
from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator
from matrx_ai.testing.profile_factory import make_profile


def test_response_preserves_provider_charge_evidence_from_usage() -> None:
    response = types.SimpleNamespace(
        id="response-1",
        model="gateway/model",
        usage=types.SimpleNamespace(
            prompt_tokens=100,
            completion_tokens=20,
            cost=0.0042,
        ),
        choices=[
            types.SimpleNamespace(
                finish_reason="stop",
                message=types.SimpleNamespace(content="done", tool_calls=None),
            )
        ],
    )

    result = GenericOpenAITranslator().from_generic_openai(response, "gateway")

    assert result.usage is not None
    assert result.usage.raw_usage == {
        "prompt_tokens": 100,
        "completion_tokens": 20,
        "cost": 0.0042,
    }
    assert result.usage.provider_charge is not None
    assert result.usage.provider_charge.authoritative_usd == 0.0042


def test_response_uses_canonical_model_name_for_pricing() -> None:
    response = types.SimpleNamespace(
        id="response-1",
        model="provider-specific-id",
        usage=types.SimpleNamespace(prompt_tokens=100, completion_tokens=20),
        choices=[
            types.SimpleNamespace(
                finish_reason="stop",
                message=types.SimpleNamespace(content="done", tool_calls=None),
            )
        ],
    )

    result = GenericOpenAITranslator().from_generic_openai(
        response,
        "moonshot",
        matrx_model_name="moonshotai/Kimi-K3",
    )

    assert result.usage is not None
    assert result.usage.matrx_model_name == "moonshotai/Kimi-K3"
    assert result.usage.provider_model_name == "provider-specific-id"


def test_moonshot_cache_usage_uses_the_discounted_catalog_rate() -> None:
    response = types.SimpleNamespace(
        id="response-1",
        model="kimi-k3",
        usage=types.SimpleNamespace(
            prompt_tokens=1_000_000,
            completion_tokens=1_000_000,
            prompt_tokens_details=types.SimpleNamespace(cached_tokens=500_000),
        ),
        choices=[
            types.SimpleNamespace(
                finish_reason="stop",
                message=types.SimpleNamespace(content="done", tool_calls=None),
            )
        ],
    )

    result = GenericOpenAITranslator().from_generic_openai(
        response,
        "moonshot",
        matrx_model_name="moonshotai/Kimi-K3",
    )

    assert result.usage is not None
    assert result.usage.input_tokens == 500_000
    assert result.usage.cached_input_tokens == 500_000
    assert result.usage.calculate_cost(
        {
            "moonshotai/Kimi-K3": ModelPricing(
                model_name="moonshotai/Kimi-K3",
                api="moonshot",
                tiers=[PricingTier(None, 3.0, 15.0, 0.3)],
            )
        }
    ) == pytest.approx(16.65)


def test_moonshot_partial_mode_is_a_message_extension() -> None:
    config = UnifiedConfig(
        model="kimi-k3",
        messages=[
            UnifiedMessage(role="user", content=[TextContent(text="Continue this")]),
            UnifiedMessage(
                role="assistant",
                content=[
                    TextContent(text="The answer is "),
                    ThinkingContent(text="I should continue the prefix."),
                ],
                metadata={"partial": True},
            ),
        ],
    )
    profile = make_profile(
        model_name="moonshotai/Kimi-K3",
        wire_format="moonshot_chat",
        vendor="moonshot",
    )

    request = GenericOpenAITranslator().to_generic_openai(config, profile)

    assert request["messages"][-1] == {
        "role": "assistant",
        "content": "The answer is ",
        "partial": True,
        "reasoning_content": "I should continue the prefix.",
    }


def test_stream_defaults_are_sent_from_the_catalog_profile() -> None:
    config = UnifiedConfig(
        model="kimi-k3",
        stream=True,
        messages=[UnifiedMessage(role="user", content=[TextContent(text="hello")])],
    )
    profile = make_profile(
        model_name="moonshotai/Kimi-K3",
        wire_format="moonshot_chat",
        vendor="moonshot",
        request_defaults={"stream_options": {"include_usage": True}},
    )

    request = GenericOpenAITranslator().to_generic_openai(config, profile)

    assert request["stream"] is True
    assert request["stream_options"] == {"include_usage": True}


# ---------------------------------------------------------------------------
# ImageContent.to_openai_chat() — shared primitive for every OpenAI-compatible
# Chat Completions translator (Cerebras, Groq, xAI, Together, generic_openai).
# ---------------------------------------------------------------------------


def test_image_with_url_emits_image_url_with_url():
    img = ImageContent(url="https://example.com/photo.jpg", mime_type="image/jpeg")
    part = img.to_openai_chat()
    assert part == {
        "type": "image_url",
        "image_url": {"url": "https://example.com/photo.jpg"},
    }


def test_image_with_base64_emits_data_uri():
    img = ImageContent(base64_data="AAAA", mime_type="image/png")
    part = img.to_openai_chat()
    assert part == {
        "type": "image_url",
        "image_url": {"url": "data:image/png;base64,AAAA"},
    }


def test_image_with_base64_defaults_to_image_png_when_mime_missing():
    """When the upstream resolver couldn't detect a mime, default to
    image/png so the request is still well-formed."""
    img = ImageContent(base64_data="AAAA")
    # __post_init__ auto-detects; force the field back to None.
    img.mime_type = None
    part = img.to_openai_chat()
    assert part is not None
    assert part["image_url"]["url"].startswith("data:image/png;base64,")


def test_image_with_only_file_uri_drops_and_returns_none():
    """file_uri (gs:// and similar native URIs) is not consumable by local
    OpenAI servers. The boundary normaliser should have resolved it;
    if we still see it here, the part is dropped."""
    img = ImageContent(file_uri="gs://bucket/path/img.png", mime_type="image/png")
    img.url = None
    img.base64_data = None
    part = img.to_openai_chat()
    assert part is None


def test_image_with_only_file_id_drops_and_returns_none():
    img = ImageContent(file_id="00000000-0000-4000-8000-000000000001")
    img.url = None
    img.base64_data = None
    img.file_uri = None
    part = img.to_openai_chat()
    assert part is None


# ---------------------------------------------------------------------------
# Full translator — to_generic_openai end-to-end
# ---------------------------------------------------------------------------


def _make_config(messages: list[UnifiedMessage]) -> UnifiedConfig:
    return UnifiedConfig(
        model="llama_cpp/qwen2.5-vl-7b",
        messages=messages,
    )


def test_text_only_message_uses_string_content():
    """Backwards compat: a text-only message must continue to emit
    ``content: "..."`` (string), not the multimodal array."""
    msg = UnifiedMessage(
        role="user",
        content=[TextContent(text="hello world")],
    )
    out = GenericOpenAITranslator(debug=False).to_generic_openai(_make_config([msg]))
    assert len(out["messages"]) == 1
    sent = out["messages"][0]
    assert sent["role"] == "user"
    assert sent["content"] == "hello world"


def test_text_plus_image_emits_multimodal_array():
    """Mixed text + image must emit the Chat Completions content array
    with text first, then image. Order matters for some vision models'
    grounding (text describes what to look for in the image)."""
    msg = UnifiedMessage(
        role="user",
        content=[
            TextContent(text="What's in this image?"),
            ImageContent(url="https://example.com/cat.jpg", mime_type="image/jpeg"),
        ],
    )
    out = GenericOpenAITranslator(debug=False).to_generic_openai(_make_config([msg]))
    sent = out["messages"][0]
    assert sent["role"] == "user"
    assert sent["content"] == [
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": "https://example.com/cat.jpg"}},
    ]


def test_image_only_message_omits_text_part():
    """An image-only message should emit a content array with just the
    image entry — no empty text part."""
    msg = UnifiedMessage(
        role="user",
        content=[ImageContent(url="https://example.com/img.png", mime_type="image/png")],
    )
    out = GenericOpenAITranslator(debug=False).to_generic_openai(_make_config([msg]))
    sent = out["messages"][0]
    assert sent["content"] == [
        {"type": "image_url", "image_url": {"url": "https://example.com/img.png"}},
    ]


def test_base64_image_becomes_data_uri_in_array():
    msg = UnifiedMessage(
        role="user",
        content=[
            TextContent(text="Describe this:"),
            ImageContent(base64_data="QkFTRTY0", mime_type="image/jpeg"),
        ],
    )
    out = GenericOpenAITranslator(debug=False).to_generic_openai(_make_config([msg]))
    sent = out["messages"][0]
    assert sent["content"] == [
        {"type": "text", "text": "Describe this:"},
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,QkFTRTY0"}},
    ]


def test_moonshot_image_requires_boundary_resolved_bytes():
    msg = UnifiedMessage(
        role="user",
        content=[ImageContent(url="https://example.com/image.png", mime_type="image/png")],
    )
    profile = make_profile(
        model_name="moonshotai/Kimi-K3",
        wire_format="moonshot_chat",
        vendor="moonshot",
    )
    with pytest.raises(ValueError, match="resolved base64 data"):
        GenericOpenAITranslator(debug=False).to_generic_openai(_make_config([msg]), profile)


def test_moonshot_video_becomes_data_uri_in_array():
    msg = UnifiedMessage(
        role="user",
        content=[
            TextContent(text="Describe this video:"),
            VideoContent(base64_data="VklERU8=", mime_type="video/mp4"),
        ],
    )
    profile = make_profile(
        model_name="moonshotai/Kimi-K3",
        wire_format="moonshot_chat",
        vendor="moonshot",
    )
    out = GenericOpenAITranslator(debug=False).to_generic_openai(
        _make_config([msg]), profile
    )
    assert out["messages"][0]["content"] == [
        {"type": "text", "text": "Describe this video:"},
        {"type": "video_url", "video_url": {"url": "data:video/mp4;base64,VklERU8="}},
    ]


def test_multiple_images_in_one_message():
    """Multiple images in one user turn — all get appended in order
    after the text part."""
    msg = UnifiedMessage(
        role="user",
        content=[
            TextContent(text="Compare these:"),
            ImageContent(url="https://example.com/a.jpg"),
            ImageContent(url="https://example.com/b.jpg"),
        ],
    )
    out = GenericOpenAITranslator(debug=False).to_generic_openai(_make_config([msg]))
    sent = out["messages"][0]
    parts = sent["content"]
    assert len(parts) == 3
    assert parts[0]["type"] == "text"
    assert parts[1]["image_url"]["url"] == "https://example.com/a.jpg"
    assert parts[2]["image_url"]["url"] == "https://example.com/b.jpg"


def test_unresolvable_image_is_dropped_from_array():
    """An image with no url/base64/file_uri/file_id gets dropped silently.
    The message still goes through with whatever resolvable content is
    left — never crashes the request."""
    bad_image = ImageContent()
    bad_image.url = None
    bad_image.base64_data = None
    bad_image.file_uri = None
    bad_image.file_id = None
    msg = UnifiedMessage(
        role="user",
        content=[
            TextContent(text="Will this work?"),
            bad_image,
        ],
    )
    out = GenericOpenAITranslator(debug=False).to_generic_openai(_make_config([msg]))
    sent = out["messages"][0]
    # With no usable images, the message degrades to the text-only
    # string-content path so the request is still well-formed.
    assert sent["content"] == "Will this work?"


def test_image_metadata_alt_does_not_corrupt_content_array():
    """ImageContent's __post_init__ moves ``alt`` into metadata. Make
    sure that side-effect doesn't leak into the multimodal content
    array — vision servers only want type+image_url."""
    img = ImageContent(url="https://example.com/x.png", alt="A cat")
    msg = UnifiedMessage(role="user", content=[img])
    out = GenericOpenAITranslator(debug=False).to_generic_openai(_make_config([msg]))
    sent = out["messages"][0]
    image_part = sent["content"][0]
    # Only type + image_url at the top of the part.
    assert set(image_part.keys()) == {"type", "image_url"}
    # And image_url only has 'url' (no alt, no metadata).
    assert set(image_part["image_url"].keys()) == {"url"}
