"""Guards for the long-transcript TTS segmentation in ``google_api.py``.

The 2026-07-10 incident: a single Gemini-TTS stream over a full multi-turn
education-deck script streamed ~4449 chunks over 367s, then went silent and
tripped the 250s stall watchdog — discarding ~6 min of billed audio and
producing zero episodes. The fix splits a long transcript into several short
TTS calls. These tests lock down the two properties that make that safe:

1. Every emitted segment carries EVERY declared speaker label, so a
   multi-speaker Gemini request never gets a segment missing a speaker
   (which mis-renders / 400s).
2. Splitting never drops or reorders transcript content — the concatenated
   segments reproduce the original text exactly.

Plus: a transcript that already fits is returned unchanged (the original
single-call path is byte-for-byte preserved for short scripts).
"""

from __future__ import annotations

from matrx_ai.providers.google.google_api import (
    _iter_tts_user_text,
    _required_speaker_labels,
    _split_tts_text,
)


def _two_host_dialogue(turns: int) -> str:
    lines: list[str] = []
    for i in range(turns):
        lines.append(f"Alex: This is turn {i} spoken by Alex, with enough words to have real length.")
        lines.append(f"Jordan: And Jordan answers turn {i} with an equally substantial reply here.")
    return "\n".join(lines)


def test_long_dialogue_splits_and_every_segment_has_all_speakers() -> None:
    dialogue = _two_host_dialogue(60)
    segments = _split_tts_text(dialogue, ["Alex", "Jordan"], max_chars=2000)

    assert len(segments) > 1, "a long transcript must be split into multiple calls"
    for i, seg in enumerate(segments):
        assert "Alex" in seg and "Jordan" in seg, f"segment {i} is missing a declared speaker"


def test_split_preserves_all_content_in_order() -> None:
    dialogue = _two_host_dialogue(60)
    segments = _split_tts_text(dialogue, ["Alex", "Jordan"], max_chars=2000)
    assert "\n".join(segments) == dialogue


def test_short_transcript_is_unchanged_single_call() -> None:
    short = "Alex: Hello there.\nJordan: Hi Alex."
    assert _split_tts_text(short, ["Alex", "Jordan"], max_chars=2000) == [short]


def test_single_voice_has_no_label_constraint_but_still_windows() -> None:
    text = "\n".join(f"Line number {i} of a solo narration with some length." for i in range(200))
    segments = _split_tts_text(text, [], max_chars=2000)
    assert len(segments) > 1
    assert "\n".join(segments) == text


def test_trailing_remainder_missing_a_speaker_merges_back() -> None:
    # A long balanced body followed by a lone trailing Alex turn: the remainder
    # lacks "Jordan", so it must merge into the previous segment, never ship alone.
    dialogue = _two_host_dialogue(50) + "\nAlex: One final orphaned closing thought from Alex only."
    segments = _split_tts_text(dialogue, ["Alex", "Jordan"], max_chars=2000)
    for seg in segments:
        assert "Alex" in seg and "Jordan" in seg
    assert "\n".join(segments) == dialogue


def test_iter_tts_user_text_reads_dict_contents() -> None:
    contents = [{"role": "user", "parts": [{"text": "Alex: hi"}, {"text": "Jordan: hey"}]}]
    assert _iter_tts_user_text(contents) == "Alex: hi\nJordan: hey"


def test_required_speaker_labels_from_multi_speaker_config() -> None:
    class _SVC:
        def __init__(self, name: str) -> None:
            self.speaker = name

    class _Multi:
        speaker_voice_configs = [_SVC("Alex"), _SVC("Jordan")]

    class _Speech:
        multi_speaker_voice_config = _Multi()

    class _Cfg:
        speech_config = _Speech()

    assert _required_speaker_labels(_Cfg()) == ["Alex", "Jordan"]

    class _CfgSingle:
        speech_config = None

    assert _required_speaker_labels(_CfgSingle()) == []
