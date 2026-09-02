"""Google multi-speaker TTS speaker-name adoption + validation.

The script is the source of truth for who speaks; the configured speaker NAMES
are arbitrary labels bound to voices. When the script's labels differ from the
configured names (the script and audio agents don't coordinate names), the voice
CONFIG adopts the script's names — keeping each voice — and the transcript is
NEVER modified. These tests pin that direction (and that a correctly-named
speaker's voice is never swapped), plus robustness to a leading preamble line and
the real test-mode failure (one turn per host).
"""

from __future__ import annotations

import pytest
from matrx_ai.config.tts_config import TTSSpeaker, TTSVoiceConfig


def _contents(text: str) -> list[dict]:
    return [{"role": "user", "parts": [{"text": text}]}]


def _text(contents: list[dict]) -> str:
    return contents[0]["parts"][0]["text"]


def _names(cfg: TTSVoiceConfig) -> list[str]:
    return [s.name for s in cfg.speakers]


def _voices(cfg: TTSVoiceConfig) -> list[str]:
    return [s.voice for s in cfg.speakers]


def _persian() -> TTSVoiceConfig:
    # Distinct voices so a wrong adoption would be observable as a voice swap.
    return TTSVoiceConfig(speakers=[TTSSpeaker("کیان", "kore"), TTSSpeaker("نیکا", "puck")])


def test_truncated_non_latin_drift_is_adopted():
    """THE reported bug: one turn per host, host 2 drifted (سارا not نیکا). The
    config adopts the script's name; the transcript is untouched."""
    cfg = _persian()
    original = "کیان: درود بر همگی، امروز درباره فناوری.\n\nسارا: بله، موضوع جالبی است."
    contents = _contents(original)
    cfg.adopt_script_speaker_names(contents)
    cfg.validate_speaker_names(contents)  # must not raise
    assert _text(contents) == original  # transcript NEVER modified
    assert _names(cfg) == ["کیان", "سارا"]  # config adopted the script's names
    assert _voices(cfg) == ["kore", "puck"]  # voices preserved exactly


def test_reversed_order_does_not_swap_the_anchor():
    """Drifted speaker first, correctly-named second — the anchor keeps its voice
    (a blind positional rename would swap it)."""
    cfg = _persian()
    original = "سارا: حرف اول را من می‌زنم.\n\nکیان: بعد من."
    contents = _contents(original)
    cfg.adopt_script_speaker_names(contents)
    cfg.validate_speaker_names(contents)
    assert _text(contents) == original
    # کیان stays bound to kore; only the drifted نیکا->سارا entry changed.
    assert _names(cfg) == ["کیان", "سارا"]
    assert _voices(cfg) == ["kore", "puck"]


def test_full_dialogue_drift_still_adopted():
    """The recurrence path (>=2 turns each) adopts the same way."""
    cfg = _persian()
    original = "کیان: درود.\nسارا: بله.\nکیان: عالی.\nسارا: موافقم."
    contents = _contents(original)
    cfg.adopt_script_speaker_names(contents)
    cfg.validate_speaker_names(contents)
    assert _text(contents) == original
    assert _names(cfg) == ["کیان", "سارا"]


def test_correct_names_leave_config_untouched():
    cfg = _persian()
    original = "کیان: درود.\n\nنیکا: سلام."
    contents = _contents(original)
    cfg.adopt_script_speaker_names(contents)
    cfg.validate_speaker_names(contents)
    assert _text(contents) == original
    assert _names(cfg) == ["کیان", "نیکا"]  # already correct — nothing adopted


def test_total_drift_adopts_positionally():
    cfg = _persian()
    original = "الکس: سلام.\n\nسارا: درود."
    contents = _contents(original)
    cfg.adopt_script_speaker_names(contents)
    cfg.validate_speaker_names(contents)
    assert _text(contents) == original
    assert _names(cfg) == ["الکس", "سارا"]  # first->first, second->second
    assert _voices(cfg) == ["kore", "puck"]


def test_english_truncated_drift_adopted():
    cfg = TTSVoiceConfig(speakers=[TTSSpeaker("Alex", "kore"), TTSSpeaker("Sarah", "puck")])
    original = "Alex: Hi there.\n\nMike: Hello."
    contents = _contents(original)
    cfg.adopt_script_speaker_names(contents)
    cfg.validate_speaker_names(contents)
    assert _text(contents) == original
    assert _names(cfg) == ["Alex", "Mike"]  # Alex anchored, Sarah->Mike


def test_leading_preamble_label_is_skipped():
    """A leading non-speaker colon line (a phantom label) is ignored — the real
    transcript comes last, so the speakers are the final N distinct labels."""
    cfg = _persian()
    original = "موضوع: فناوری\n\nکیان: درود\n\nسارا: بله"
    contents = _contents(original)
    cfg.adopt_script_speaker_names(contents)
    cfg.validate_speaker_names(contents)
    assert _text(contents) == original  # preamble + transcript untouched
    assert _names(cfg) == ["کیان", "سارا"]


def test_google_tts_current_date_prepend_is_handled():
    """Defense-in-depth: even if the folded 'Current date: …' system preamble
    reaches adoption, the leading phantom is skipped and the transcript stays."""
    cfg = TTSVoiceConfig(speakers=[TTSSpeaker("Alex", "orus"), TTSSpeaker("Sarah", "kore")])
    original = (
        "Current date: 2026-06-12\n\n"
        "Please read aloud the following in a Educational Podcast style:\n\n"
        "Jake: Welcome back, everybody.\n\nChloe: I feel like a mad libs prompt."
    )
    contents = _contents(original)
    cfg.adopt_script_speaker_names(contents)
    cfg.validate_speaker_names(contents)
    assert _text(contents) == original  # nothing rewritten
    assert _names(cfg) == ["Jake", "Chloe"]
    assert _voices(cfg) == ["orus", "kore"]


def test_too_few_distinct_speakers_bails_and_rejects():
    """Genuinely can't reconstruct a missing speaker: a transcript with fewer
    distinct labels than configured speakers leaves the config alone, and
    validation honestly rejects rather than mislabelling."""
    cfg = _persian()
    contents = _contents("کیان: درود\n\nکیان: باز هم من صحبت می‌کنم")
    cfg.adopt_script_speaker_names(contents)  # bails — only 1 distinct label, need 2
    assert _names(cfg) == ["کیان", "نیکا"]  # unchanged
    with pytest.raises(ValueError):
        cfg.validate_speaker_names(contents)


def test_to_google_adopts_names_keeps_transcript():
    """End-to-end through the real translator: a script that drifts the speaker
    names (Jake/Chloe) vs configured voices (Alex/Sarah). The voice config adopts
    the script's names and the transcript is untouched. (Date/decoration cleaning
    now happens at request-prep, not in the translator — see the capability gate
    tests.)"""
    from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.providers.google.translator import GoogleTranslator
    from matrx_ai.testing.profile_factory import make_profile

    transcript = "Jake: Welcome back, everybody.\n\nChloe: I feel like a mad libs prompt."
    config = UnifiedConfig(
        model="gemini-2.5-pro-preview-tts",
        messages=[UnifiedMessage(role="user", content=[TextContent(text=transcript)])],
        system_instruction="Please read aloud the following in a Educational Podcast style:",
        tts_voice=[{"name": "Alex", "voice": "orus"}, {"name": "Sarah", "voice": "kore"}],
    )
    result = GoogleTranslator().to_google(
        config,
        make_profile(
            model_name="gemini-2.5-flash-preview-tts",
            wire_format="google_chat",
            capabilities={
                "input": ["text"],
                "output": ["audio"],
                "features": [],
                "interaction": "turn",
                "multilingual": True,
            },
        ),
    )
    text = result["contents"][0]["parts"][0]["text"]

    # Transcript labels are NOT rewritten — the script is canonical.
    assert "Jake: Welcome back, everybody." in text
    assert "Chloe: I feel like a mad libs prompt." in text
    assert "Alex:" not in text and "Sarah:" not in text

    # And the voice config adopted the script's names (so Google maps them).
    speakers = [
        s.speaker
        for s in result["config"].speech_config.multi_speaker_voice_config.speaker_voice_configs
    ]
    assert speakers == ["Jake", "Chloe"]


def test_single_speaker_config_is_noop():
    cfg = TTSVoiceConfig(voice="kore")  # not multi-speaker
    contents = _contents("Anything: here.")
    cfg.adopt_script_speaker_names(contents)  # returns immediately
    cfg.validate_speaker_names(contents)  # returns immediately
    assert _text(contents) == "Anything: here."
