"""The capability seam (`resolved_capabilities.py`) — the ONE derivation.

Guarantees:
  • the real ``ai.model_definition.capabilities`` jsonb shape is read correctly;
  • ``structured_output_mode`` negotiates schema > json > text off ``features``;
  • ``native_capabilities`` is a SET intersected with the known native-tool vocabulary;
  • malformed jsonb is tolerant (never raises, contributes nothing);
  • an offering's ``capabilities_override`` merges per top-level key, offering wins.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.providers.resolved_capabilities import (
    StructuredOutputMode,
    resolve_model_capabilities,
)


def _model(name, *, capabilities=None, model_class=None):
    return SimpleNamespace(
        name=name,
        model_class=model_class or name,
        capabilities=capabilities,
    )


def test_reads_real_jsonb_shapes():
    claude = _model(
        "claude-opus-4-8",
        capabilities={
            "input": ["image", "text"],
            "output": ["text"],
            "features": ["function_calling", "thinking", "structured_output", "json_mode"],
            "interaction": "turn",
        },
    )
    d = resolve_model_capabilities(claude)
    assert d.supports_vision is True
    assert d.supports_audio_input is False
    assert d.produces_image is False and d.produces_video is False and d.produces_audio is False
    assert d.supports_function_calling is True
    assert d.supports_web_search is False
    assert d.interaction == "turn"
    assert d.model_name == "claude-opus-4-8"

    gemini = _model(
        "gemini-3-flash-preview",
        capabilities={
            "input": ["text"],
            "output": ["text"],
            "features": ["function_calling", "structured_output", "web_search"],
            "interaction": "turn",
        },
    )
    g = resolve_model_capabilities(gemini)
    assert g.supports_function_calling is True and g.supports_web_search is True
    assert g.supports_vision is False

    tts = _model(
        "eleven_v3",
        capabilities={
            "input": ["text"],
            "output": ["audio"],
            "features": [],
            "interaction": "turn",
        },
    )
    assert resolve_model_capabilities(tts).produces_audio is True

    video = _model(
        "seedance",
        capabilities={"input": ["image", "text"], "output": ["video"], "features": []},
    )
    assert resolve_model_capabilities(video).produces_video is True

    realtime = _model(
        "scribe_v2_realtime",
        capabilities={"input": ["audio"], "output": ["text"], "interaction": "realtime"},
    )
    rt = resolve_model_capabilities(realtime)
    assert rt.supports_audio_input is True and rt.interaction == "realtime"

    embedding = _model(
        "text-embedding-3-large",
        capabilities={
            "input": ["text"],
            "output": ["embedding"],
            "interaction": "embedding",
        },
    )
    emb = resolve_model_capabilities(embedding)
    assert emb.interaction == "embedding"
    assert emb.produces_embedding is True
    assert emb.produces_text is False

    multi = _model(
        "gliner-multi",
        capabilities={
            "input": ["text"],
            "output": ["entities"],
            "interaction": "extraction",
            "multilingual": True,
        },
    )
    m = resolve_model_capabilities(multi)
    assert m.multilingual is True and m.interaction == "extraction"


def test_supports_dialogue_is_data_driven():
    # ElevenLabs endpoint routing: "dialogue" in `features` → text_to_dialogue;
    # absent → plain text-to-speech (eleven_flash_v2_5 rejects the dialogue API).
    v3 = _model(
        "eleven_v3",
        capabilities={"input": ["text"], "output": ["audio"], "features": ["dialogue"]},
    )
    assert resolve_model_capabilities(v3).supports_dialogue is True

    flash = _model(
        "eleven_flash_v2_5",
        capabilities={"input": ["text"], "output": ["audio"], "features": []},
    )
    assert resolve_model_capabilities(flash).supports_dialogue is False


def test_structured_output_mode_negotiates_schema_json_text():
    schema = _model("gpt-oss-120b", capabilities={"features": ["structured_output", "json_mode"]})
    assert resolve_model_capabilities(schema).structured_output_mode is StructuredOutputMode.SCHEMA

    json_only = _model("qwen3-32b", capabilities={"features": ["json_mode"]})
    assert resolve_model_capabilities(json_only).structured_output_mode is StructuredOutputMode.JSON

    text = _model("eleven_v3", capabilities={"features": []})
    assert resolve_model_capabilities(text).structured_output_mode is StructuredOutputMode.TEXT


def test_native_capabilities_is_a_set_from_features():
    # Internal/native provider tools are a SET, not a boolean — derived from the
    # jsonb `features`, intersected with the known native-tool vocabulary.
    m = _model(
        "grok-4",
        capabilities={
            "input": ["text"],
            "output": ["text"],
            "features": [
                "function_calling",
                "web_search",
                "x_search",
                "code_execution",
                "thinking",
            ],
        },
    )
    nc = resolve_model_capabilities(m).native_capabilities
    assert nc == frozenset({"web_search", "x_search", "code_execution"})
    # function_calling/thinking are model capabilities, NOT native provider tools.
    assert "function_calling" not in nc and "thinking" not in nc


def test_malformed_jsonb_is_tolerant():
    # The OLD list-shape, None, and junk all contribute nothing (no raise).
    for bad in (["text", "vision"], None, "garbage", 42, {"interaction": "bogus"}):
        d = resolve_model_capabilities(_model("x", capabilities=bad))
        assert d.interaction == "turn"  # defaulted
        assert d.supports_vision is False  # nothing declared
        assert d.structured_output_mode is StructuredOutputMode.TEXT


def test_offering_capabilities_override_merges_per_key():
    base = _model(
        "gemini-2.5-flash",
        capabilities={
            "input": ["text", "image"],
            "output": ["text"],
            "features": ["function_calling", "web_search"],
            "interaction": "turn",
        },
    )
    # An override REPLACES the named top-level key and leaves the rest alone.
    r = resolve_model_capabilities(base, capabilities_override={"features": ["structured_output"]})
    assert r.structured_output_mode is StructuredOutputMode.SCHEMA
    assert r.supports_function_calling is False  # features replaced wholesale
    assert r.supports_vision is True  # untouched key survives

    r2 = resolve_model_capabilities(base, capabilities_override={"input": ["text"]})
    assert r2.supports_vision is False
    assert r2.supports_function_calling is True  # features untouched

    # No override == plain model resolution.
    assert resolve_model_capabilities(base, capabilities_override={}) == resolve_model_capabilities(
        base
    )
