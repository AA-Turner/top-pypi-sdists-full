"""Speech text over a provider's maximum is cut loudly, at a sentence end, never silently.

Break this guards: ``GroqTTSRegistry.validate_input_length`` returned ``text[:200]`` and
``XAITTSRegistry.validate_text_length(truncate=True)`` returned ``text[:15000]`` — the audio
stopped mid-word and nothing anywhere said the request was shortened. The cut now keeps whole
sentences, is recorded (``record_cut``), captured (``tts_input_truncated``) and its facts ride
the audio's metadata (``speech_input``).
"""

from __future__ import annotations

import pytest

import matrx_ai.config.tts_config as tts
from matrx_ai.config.tts_config import GroqTTSRegistry, XAITTSRegistry, fit_spoken_text

TEXT = (
    "Welcome to the morning update. "  # 31
    "Rain is expected after noon across the valley. "  # 47 -> 78
    "Bring an umbrella if you are heading out later today."  # 53 -> 131
)


def test_groq_text_over_the_maximum_keeps_whole_sentences_and_says_it_was_cut() -> None:
    fit = GroqTTSRegistry.fit_input(TEXT + " " + TEXT)  # 263 chars, Orpheus takes 200
    assert fit.truncated is True
    assert fit.text == TEXT + " Welcome to the morning update."
    assert fit.record() == {"truncated": True, "chars_total": 263, "chars_kept": 162, "limit": 200}


def test_a_short_limit_cut_ends_on_the_last_whole_sentence() -> None:
    fit = fit_spoken_text(TEXT, 100, provider="test")
    assert fit.text == "Welcome to the morning update. Rain is expected after noon across the valley."
    assert (fit.truncated, fit.chars_kept, fit.chars_total) == (True, 77, 131)


def test_text_within_the_maximum_is_untouched() -> None:
    fit = GroqTTSRegistry.fit_input(TEXT)
    assert (fit.text, fit.truncated) == (TEXT, False)


def test_xai_truncate_path_is_the_same_loud_cut() -> None:
    long = "One short sentence here. " * 700  # 17,500 chars over the 15,000 maximum
    out = XAITTSRegistry.validate_text_length(long, truncate=True)
    assert out.endswith("One short sentence here.")
    assert len(out) == 14_999  # 600 whole sentences, the trailing space stripped


@pytest.mark.asyncio
async def test_a_cut_is_captured_as_a_fact(monkeypatch) -> None:
    seen: list[dict] = []

    async def _capture(exc, *, kind, **fields):
        seen.append({"kind": kind, **fields})

    import matrx_connect.streaming.error_capture as ec

    monkeypatch.setattr(ec, "capture_error", _capture)
    await tts.capture_spoken_text_cut(GroqTTSRegistry.fit_input(TEXT + " " + TEXT), provider="groq", model="orpheus")
    await tts.capture_spoken_text_cut(GroqTTSRegistry.fit_input(TEXT), provider="groq", model="orpheus")
    assert seen == [
        {
            "kind": "tts_input_truncated",
            "payload": {
                "provider": "groq", "model": "orpheus",
                "truncated": True, "chars_total": 263, "chars_kept": 162, "limit": 200,
            },
        }
    ]
