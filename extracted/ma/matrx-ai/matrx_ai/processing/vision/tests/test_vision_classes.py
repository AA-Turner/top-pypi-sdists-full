"""Forcing-function tests for the vision-class registry.

The registry resolution rules drive every image variant render in the
system. A bug in ``resolve_vision_class`` means images for OpenAI hit
Anthropic's encoder and vice-versa — silently. These tests pin the
behaviour by asserting concrete (model, wire_format) -> class-name
mappings; a single-line resolver bug fails one of them.

A vision class is a RE-ENCODING profile, never a capability. "Can this model
see" is ``ResolvedModelCapabilities.supports_vision`` (the model's own jsonb),
resolved by the caller BEFORE it ever reaches this registry.
"""

from __future__ import annotations

import pytest

from matrx_ai.processing.vision import (
    MODEL_TO_VISION_CLASS,
    VISION_API_CLASSES,
    WIRE_FORMAT_DEFAULT_VISION_CLASS,
    is_known_vision_class,
    resolve_vision_class,
)


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        ("claude-opus-4-7", "anthropic_opus_hires"),
        ("claude-opus-4-5", "anthropic_opus_hires"),
        ("claude-sonnet-4-6", "anthropic_sonnet_default"),
        ("claude-haiku-4-5", "anthropic_haiku_default"),
        ("gpt-5.5", "openai_original"),
        ("gpt-5.4", "openai_original"),
        ("gpt-5", "openai_high"),
        ("gpt-5-nano", "openai_low"),
        ("gemini-3-pro", "gemini3_high"),
        ("gemini-2.5-flash", "gemini25_default"),
    ],
)
def test_resolve_vision_class_matches_known_models(model: str, expected: str) -> None:
    cls = resolve_vision_class(model)
    assert cls.name == expected
    assert cls is VISION_API_CLASSES[expected]


def test_resolve_vision_class_uses_longest_prefix_when_no_exact_match() -> None:
    """A versioned model id like ``claude-opus-4-7-20251201`` has no exact
    entry — the resolver must pick the longest matching prefix
    (``claude-opus-4-7``), not a shorter one (``claude-opus-4-5``)."""
    cls = resolve_vision_class("claude-opus-4-7-20251201")
    assert cls.name == "anthropic_opus_hires"


def test_resolve_vision_class_is_case_insensitive() -> None:
    cls = resolve_vision_class("Claude-Opus-4-7")
    assert cls.name == "anthropic_opus_hires"


def test_resolve_vision_class_falls_back_to_wire_format() -> None:
    cls = resolve_vision_class(model=None, wire_format="anthropic_chat")
    assert cls.name == "anthropic_sonnet_default"


def test_resolve_vision_class_unknown_model_uses_wire_format() -> None:
    """Unknown model name + known wire route — the route's profile wins, not
    unknown_default."""
    cls = resolve_vision_class(model="some-unreleased-model-9000", wire_format="google_chat")
    assert cls.name == "gemini25_default"


def test_resolve_vision_class_unknown_everything_falls_to_unknown_default() -> None:
    cls = resolve_vision_class(model=None, wire_format=None)
    assert cls.name == "unknown_default"
    cls2 = resolve_vision_class(model="totally-fake", wire_format="bogus_wire_format")
    assert cls2.name == "unknown_default"


def test_resolve_vision_class_model_takes_precedence_over_wire_format() -> None:
    """Model-name match must beat the route default. If a Sonnet model name comes in
    on the Google route, the resolver must still return anthropic_sonnet_default."""
    cls = resolve_vision_class(model="claude-sonnet-4-6", wire_format="google_chat")
    assert cls.name == "anthropic_sonnet_default"


@pytest.mark.parametrize(
    "wire_format",
    [
        "openai_image",
        "google_image",
        "google_video",
        "xai_video",
        "replicate_image",
        "elevenlabs_chat",
        "extraction_gliner",
        "xai_realtime",
    ],
)
def test_non_chat_routes_have_no_reencode_profile(wire_format: str) -> None:
    """A route that never carries image INPUT has no default profile — it falls to
    ``unknown_default`` and nothing is re-encoded for it. (The image/video GENERATION
    routes take a prompt, not an image the model must see.)"""
    assert wire_format not in WIRE_FORMAT_DEFAULT_VISION_CLASS
    cls = resolve_vision_class(model="anything-unknown", wire_format=wire_format)
    assert cls.name == "unknown_default"


def test_cerebras_route_uses_the_openai_profile() -> None:
    """Cerebras is OpenAI-wire-compatible, so its images re-encode with the OpenAI
    profile — and gemma-4-31b (its ONE image-input model) pins the same."""
    assert resolve_vision_class("some-cerebras-model", "cerebras_chat").name == "openai_high"
    assert resolve_vision_class("gemma-4-31b", "cerebras_chat").name == "openai_high"


def test_is_known_vision_class_matches_registry_keys() -> None:
    for name in VISION_API_CLASSES:
        assert is_known_vision_class(name)
    assert not is_known_vision_class("not_a_real_class")
    assert not is_known_vision_class(None)
    assert not is_known_vision_class("")


def test_registry_invariants() -> None:
    """The registry is the source of truth for downstream encoders.
    These invariants prevent silent regressions:

    - Every entry's ``name`` matches its key.
    - Every ``MODEL_TO_VISION_CLASS`` value points at a known class.
    - Every ``WIRE_FORMAT_DEFAULT_VISION_CLASS`` value points at a known class.
    - ``unknown_default`` is always present (the resolver falls back to it).
    - Every class has positive ``long_edge``, ``quality`` in (0, 100],
      ``max_bytes`` > 0.
    - No class carries a capability flag — capabilities live in the model's jsonb.
    """
    for key, cls in VISION_API_CLASSES.items():
        assert cls.name == key, f"{key}: name {cls.name!r} != key"
        assert cls.long_edge > 0
        assert 0 < cls.quality <= 100
        assert 0 < cls.min_quality <= cls.quality
        assert cls.max_bytes > 0
        assert cls.format.upper() in ("JPEG", "WEBP", "PNG")
        assert not hasattr(cls, "supports_vision")

    for model, target in MODEL_TO_VISION_CLASS.items():
        assert target in VISION_API_CLASSES, (
            f"MODEL_TO_VISION_CLASS[{model!r}]={target!r} not in VISION_API_CLASSES"
        )

    for wf, target in WIRE_FORMAT_DEFAULT_VISION_CLASS.items():
        assert target in VISION_API_CLASSES, (
            f"WIRE_FORMAT_DEFAULT_VISION_CLASS[{wf!r}]={target!r} not in VISION_API_CLASSES"
        )

    assert "unknown_default" in VISION_API_CLASSES
    assert "text_only" not in VISION_API_CLASSES  # capability, not a re-encode profile
