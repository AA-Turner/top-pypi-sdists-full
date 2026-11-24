"""A setting the offering has no Google field for is dropped and announced, never sent.

Live 2026-11-07/08 (feedback 33c8b277): reasoning_effort='low' reached
GenerateContentConfig and pydantic rejected the whole config (extra_forbidden).
"""

from google.genai import types

from matrx_ai.providers.google.translator import GoogleTranslator


def test_foreign_key_is_dropped_and_config_builds():
    params = {"temperature": 0.2, "reasoning_effort": "low"}
    kept = GoogleTranslator._only_google_config_fields(params, model="gemma-test")
    assert kept == {"temperature": 0.2}
    types.GenerateContentConfig(**kept)  # would raise extra_forbidden with the raw key


def test_known_keys_pass_through_untouched():
    params = {"temperature": 0.2, "thinking_config": {"thinking_level": "low"}}
    assert GoogleTranslator._only_google_config_fields(params, model="m") is params


def test_raw_key_really_is_rejected_by_the_sdk():
    import pytest

    with pytest.raises(Exception):
        types.GenerateContentConfig(reasoning_effort="low")
