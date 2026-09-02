"""tts_voice / audio_format are translator-STRUCTURAL keys — the outbound scalar
param seam must never emit them, even when a TTS offering's control rules declare
them ``supported:true`` with a ``default`` (which makes ``controls.outbound``
inject the default value).

Regression for the 2026-07 Education-Hub audio outage: the live
gemini-*-tts offering declares ``tts_voice`` (default "kore") and
``audio_format`` (default "wav") in ai.offering.override.params, so
``resolve_outbound_params`` injected those defaults into the resolved params, the
Google chat translator merged them blind into ``types.GenerateContentConfig``,
and the SDK 400'd every TTS request with "2 validation errors ... Extra inputs".
The translator consumes both structurally (tts_voice → speech_config,
audio_format → output transcode), so they must be stripped at the seam.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers.outbound_params import (
    _STRUCTURAL_CANONICAL_KEYS,
    resolve_outbound_params,
)


def _compiled(rules: dict[str, dict]) -> CompiledControlsMap:
    return CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()},
        value_orders={},
    )


def test_structural_set_declares_tts_keys():
    assert "tts_voice" in _STRUCTURAL_CANONICAL_KEYS
    assert "audio_format" in _STRUCTURAL_CANONICAL_KEYS
    assert "response_format" in _STRUCTURAL_CANONICAL_KEYS


def test_tts_offering_defaults_never_reach_provider_params():
    # Mirrors the live gemini-*-tts offering: tts_voice + audio_format are
    # supported with a default (→ outbound injects them when canonical is unset),
    # temperature is unsupported, and a benign supported key rides through.
    controls = _compiled(
        {
            "tts_voice": {"default": "kore"},
            "audio_format": {"default": "wav"},
            "temperature": {"supported": False},
            "max_output_tokens": {"supported": False},
        }
    )
    # A TTS UnifiedConfig-shaped object: tts_voice/audio_format are set on the
    # config (consumed structurally elsewhere) but the canonicalizer does not
    # extract them — the leak comes purely from the offering's default rules.
    config = SimpleNamespace(
        model="gemini-3.1-flash-tts-preview",
        tts_voice=[{"name": "Alex", "voice": "Orus"}],
        audio_format="wav",
    )

    params = resolve_outbound_params(config, controls)

    assert "tts_voice" not in params, params
    assert "audio_format" not in params, params
