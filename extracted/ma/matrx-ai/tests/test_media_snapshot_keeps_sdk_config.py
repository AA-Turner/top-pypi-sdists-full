"""A media call's request snapshot stores an SDK config as wire JSON, never a ``<Type>`` stand-in.

Live 2026-11-10 (podcast.image_v2): the image path stored Google's ``GenerateContentConfig`` as
the string ``"<GenerateContentConfig>"``; the cache guard then read ``config`` of type ``str``
and filed ``prompt_cache_guard_blind`` (unreadable_wire_config).
"""

from __future__ import annotations

from google.genai import types

from matrx_ai.providers.base_media import snapshot_kwargs


def test_an_sdk_config_is_stored_as_its_wire_json() -> None:
    config = types.GenerateContentConfig(
        system_instruction="Draw the host.", response_modalities=["IMAGE"]
    )
    stored = snapshot_kwargs({"model": "gemini-image", "config": config, "contents": ["a cat"]})
    assert isinstance(stored["config"], dict)
    assert stored["config"]["response_modalities"] == ["IMAGE"]
    assert stored["model"] == "gemini-image"
    assert stored["contents"] == ["a cat"]


def test_a_value_with_no_wire_form_keeps_a_named_stand_in() -> None:
    class Stream:
        pass

    assert snapshot_kwargs({"body": Stream()})["body"] == "<Stream>"


def test_the_cache_guard_reads_the_stored_config() -> None:
    from matrx_ai.providers.cache_guard import wire_prefix

    config = types.GenerateContentConfig(system_instruction="Draw the host.")
    prefix = wire_prefix(snapshot_kwargs({"model": "m", "config": config, "contents": []}))
    assert prefix is not None
    assert any(label == "system" for label, _ in prefix.heads)
