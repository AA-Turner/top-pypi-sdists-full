"""Regression guard: the hosted web-search tool must never be sent to a model
that can't honour it.

The incident: ``internal_web_search=True`` rode a request to ``gpt-4.1-nano``,
the OpenAI translator unconditionally appended ``{"type": "web_search_preview"}``,
and the Responses API 400'd the WHOLE request ("Tool 'web_search_preview' is not
supported with gpt-4.1-nano-2025-04-14") — discarding the turn.

The structural fix gates ``internal_web_search`` on the model's OWN declared
capability data (``capabilities.features`` contains ``web_search``). The boundary
is genuinely per-model, NOT a tier word: ``gpt-4.1-nano`` lacks it while
``gpt-5-nano`` has it, so an "all nano" rule would be wrong — and a per-model data
row is the only shape that can express it. Same for ``internal_x_search`` and its
``x_search`` member. These tests pin the resolution and the loud, in-place strip
the unified client performs before dispatch.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities
from matrx_ai.providers.unified_client import (
    _resolve_web_search_json_mode_conflict,
    _warn_and_strip_unsupported_search,
)


def _caps(name: str, *features: str):
    return resolve_model_capabilities(
        SimpleNamespace(
            name=name,
            model_class=name,
            capabilities={
                "input": ["text"],
                "output": ["text"],
                "features": ["function_calling", *features],
            },
        )
    )


# ---------------------------------------------------------------------------
# supports_web_search / native_capabilities — pure capability data
# ---------------------------------------------------------------------------


def test_web_search_declared_per_model() -> None:
    assert _caps("gpt-4o", "web_search").supports_web_search
    assert _caps("gpt-5-nano", "web_search").supports_web_search
    # Same family, no declaration — the genuine per-model exception.
    assert not _caps("gpt-4.1-nano-2025-04-14").supports_web_search
    assert not _caps("o3-mini-20250131").supports_web_search


def test_non_chat_models_declare_nothing() -> None:
    image = resolve_model_capabilities(
        SimpleNamespace(
            name="gpt-image-2",
            capabilities={"input": ["image", "text"], "output": ["image"], "features": []},
        )
    )
    assert not image.supports_web_search
    assert image.native_capabilities == frozenset()


def test_native_capabilities_carries_x_search_separately() -> None:
    grok = _caps("grok-4.3", "web_search", "x_search")
    assert grok.supports_web_search
    assert "x_search" in grok.native_capabilities
    # A web-search model that is NOT xAI hosts no X search.
    gemini = _caps("gemini-3-pro", "web_search")
    assert gemini.supports_web_search
    assert "x_search" not in gemini.native_capabilities


def test_missing_capabilities_is_unsupported() -> None:
    bare = resolve_model_capabilities(SimpleNamespace(name="mystery", capabilities=None))
    assert not bare.supports_web_search
    assert bare.native_capabilities == frozenset()


# ---------------------------------------------------------------------------
# unified_client strip gate — drops the flag in place, never silent
# ---------------------------------------------------------------------------


def test_strip_drops_web_search_for_unsupported_model() -> None:
    config = SimpleNamespace(internal_web_search=True, internal_x_search=None)

    _warn_and_strip_unsupported_search(config, _caps("gpt-4.1-nano-2025-04-14"), "openai_chat")

    assert config.internal_web_search is None


def test_strip_keeps_web_search_for_supported_model() -> None:
    config = SimpleNamespace(internal_web_search=True, internal_x_search=None)

    _warn_and_strip_unsupported_search(config, _caps("gpt-4o", "web_search"), "openai_chat")

    assert config.internal_web_search is True


def test_strip_is_noop_when_flag_unset() -> None:
    config = SimpleNamespace(internal_web_search=None, internal_x_search=None)

    _warn_and_strip_unsupported_search(config, _caps("gpt-4.1-nano"), "openai_chat")

    assert config.internal_web_search is None


def test_strip_drops_x_search_off_a_non_xai_model() -> None:
    config = SimpleNamespace(internal_web_search=None, internal_x_search=True)

    _warn_and_strip_unsupported_search(config, _caps("gemini-3-pro", "web_search"), "google_chat")

    assert config.internal_x_search is None


def test_strip_keeps_x_search_on_a_grok_model() -> None:
    config = SimpleNamespace(internal_web_search=None, internal_x_search=True)

    _warn_and_strip_unsupported_search(
        config, _caps("grok-4.3", "web_search", "x_search"), "xai_chat"
    )

    assert config.internal_x_search is True


# ---------------------------------------------------------------------------
# web search × JSON mode conflict — OpenAI 400s json_object + web_search
# ---------------------------------------------------------------------------


def test_web_search_dropped_with_json_mode_on_openai_route() -> None:
    # The incident: gpt-5.4-mini + json_object + web search → "Web Search cannot be
    # used with JSON mode." Drop web search, keep the JSON.
    config = SimpleNamespace(internal_web_search=True, response_format={"type": "json_object"})

    _resolve_web_search_json_mode_conflict(
        config, _caps("gpt-5.4-mini", "web_search"), "openai_chat"
    )

    assert config.internal_web_search is None
    assert config.response_format == {"type": "json_object"}


def test_web_search_kept_with_structured_outputs() -> None:
    # json_schema (Structured Outputs) is compatible with web search — keep both.
    config = SimpleNamespace(
        internal_web_search=True,
        response_format={"type": "json_schema", "json_schema": {"name": "x"}},
    )

    _resolve_web_search_json_mode_conflict(config, _caps("gpt-4o", "web_search"), "openai_chat")

    assert config.internal_web_search is True


def test_web_search_kept_with_text_output() -> None:
    config = SimpleNamespace(internal_web_search=True, response_format={"type": "text"})

    _resolve_web_search_json_mode_conflict(config, _caps("gpt-4o", "web_search"), "openai_chat")

    assert config.internal_web_search is True


def test_json_mode_conflict_is_noop_for_non_openai_route() -> None:
    # The limitation is OpenAI-specific; don't over-strip other providers.
    config = SimpleNamespace(internal_web_search=True, response_format={"type": "json_object"})

    _resolve_web_search_json_mode_conflict(config, _caps("grok-4.3", "web_search"), "xai_chat")

    assert config.internal_web_search is True


def test_json_mode_conflict_is_noop_when_web_search_unset() -> None:
    config = SimpleNamespace(internal_web_search=None, response_format={"type": "json_object"})

    _resolve_web_search_json_mode_conflict(config, _caps("gpt-4o", "web_search"), "openai_chat")

    assert config.internal_web_search is None
