"""A 200 response whose body holds a sliver of audio is a cut-off response, not a take (2026-10-19 stub).

Production returned 2,688 bytes (0.168 s) for a 556-character script, billed all 556 characters and stored it as
the take. The adapter must raise a RETRYABLE ``incomplete_response`` carrying the billed usage, before storage.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.speech.take_check import (
    MIN_BYTES_PER_CHARACTER,
    TruncatedSpeechError,
    truncated_take_reason,
)
from matrx_ai.testing.profile_factory import make_profile

SCRIPT = (
    "Discover the Hand-painted ceramic butterfly plate from Creativity Warehouse today. "
    "This Hand-painted ceramic butterfly plate is painted by hand by our studio members inside our vibrant "
    "craft workspace. As a glazed pottery plate, it brings authentic artistic creativity straight to your home."
)


def test_the_production_stub_is_cut_off_and_a_real_take_is_not():
    assert truncated_take_reason(2688, 556) is not None  # the 2026-10-19 stub
    assert truncated_take_reason(581760, 556) is None  # the same request, healthy: 36 s of mp3
    assert truncated_take_reason(556 * MIN_BYTES_PER_CHARACTER, 556) is None
    assert truncated_take_reason(0, 3) is not None


class _Emitter:
    async def send_info(self, *_: Any, **__: Any) -> None: ...
    async def send_data(self, *_: Any, **__: Any) -> None: ...


class _Body:
    def __init__(self, size: int) -> None:
        self.content = b"\x00" * size


def _chat(monkeypatch: pytest.MonkeyPatch, body_size: int, sent: dict[str, Any]):
    from matrx_ai.config import usage_config
    from matrx_ai.providers.openai import openai_api

    class _Speech:
        async def create(self, **kwargs: Any):
            sent.update(kwargs)
            return _Body(body_size)

    class _Audio:
        speech = _Speech()

    class _Client:
        audio = _Audio()

    async def _usage(**_: Any):
        return "BILLED-USAGE"

    monkeypatch.setattr(openai_api, "stamp_call_meta", lambda **_: None)
    monkeypatch.setattr(usage_config, "build_character_billed_usage_async", _usage)
    chat = openai_api.OpenAIChat.__new__(openai_api.OpenAIChat)
    chat.client = _Client()
    return chat


def _config() -> UnifiedConfig:
    return UnifiedConfig(
        model="m",
        messages=[UnifiedMessage(role="user", content=[TextContent(text=SCRIPT)])],
        audio_format="mp3",
    )


def _profile():
    return make_profile(
        model_name="gpt-4o-mini-tts",
        wire_format="openai_chat",
        capabilities={"input": ["text"], "output": ["audio"], "features": [], "interaction": "turn"},
        rules={},
    ).model_copy(update={"tts_voice_ids": ("coral",), "tts_default_voice_id": "coral"})


@pytest.mark.asyncio
async def test_a_sliver_of_audio_is_a_retryable_billed_failure_not_a_take(monkeypatch):
    from matrx_ai.providers.errors import get_billed_usage

    sent: dict[str, Any] = {}
    chat = _chat(monkeypatch, 2688, sent)
    with pytest.raises(TruncatedSpeechError) as raised:
        await chat._execute_tts(_config(), _profile(), _Emitter(), "gpt-4o-mini-tts")
    assert sent["input"] == SCRIPT  # the full text went out; the delivery was short
    info = raised.value.error_info
    assert info.error_type == "incomplete_response" and info.is_retryable is True
    assert get_billed_usage(raised.value) == "BILLED-USAGE"  # spend is still recorded once
