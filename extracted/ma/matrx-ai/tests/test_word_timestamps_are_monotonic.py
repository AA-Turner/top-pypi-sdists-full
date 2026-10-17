"""Word timings: the Groq adapter lifts ``words`` onto STTResult, clamped monotonic."""
from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.processing.audio.stt import clamp_words_monotonic
from matrx_ai.providers.groq.stt import GroqSTT

# Real Groq shape: ends stretched to next start, a few overlaps (from the VC-S1 spike).
RAW = [
    {"word": "and", "start": 5.78, "end": 6.04},
    {"word": "I'm", "start": 5.56, "end": 6.16},  # starts before "and" ends (and is listed after)
    {"word": "going", "start": 6.10, "end": 6.40},  # overlaps I'm
    {"word": "home", "start": 7.00, "end": 6.90},  # negative duration
    {"word": " ", "start": 8.0, "end": 8.1},  # junk, dropped
]


def test_clamp_keeps_provider_order_removes_overlaps_and_negative_durations() -> None:
    words = clamp_words_monotonic(RAW)
    # Provider order is the spoken order the script ids are matched against (rule proportional@1:
    # a word starting before its predecessor is clamped into the shared span, never reordered).
    assert [w.text for w in words] == ["and", "I'm", "going", "home"]
    for prev, cur in zip(words, words[1:]):
        assert cur.start >= prev.end
    assert all(w.end >= w.start for w in words)


def test_clamp_keeps_honest_gaps() -> None:
    words = clamp_words_monotonic(
        [{"word": "a", "start": 0.0, "end": 1.0}, {"word": "b", "start": 2.5, "end": 3.0}]
    )
    assert words[1].start == 2.5


def test_groq_adapter_populates_words() -> None:
    profile = SimpleNamespace(
        offering_metadata={}, provider_model_id="whisper-large-v3-turbo",
        model_name="stt-default", vendor="groq", offering_id="", usage_basis="audio_second_input",
    )
    request = SimpleNamespace(
        language=None, operation="transcription", response_format="verbose_json"
    )
    result = GroqSTT._parse_response(
        {"text": "x", "duration": 9.0, "words": RAW},
        profile=profile, request=request, file_size_mb=0.1,
    )
    assert result.words is not None
    assert [w.text for w in result.words] == ["and", "I'm", "going", "home"]
    assert result.words[1].start >= result.words[0].end
