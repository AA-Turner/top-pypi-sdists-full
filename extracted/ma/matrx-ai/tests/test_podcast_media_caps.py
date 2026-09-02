"""Per-run media caps and speaker-aware test truncation for the podcast pipeline.

``_effective_media_count`` turns the request's ``max_images`` / ``max_videos``
into a concrete slot count (None → full, 0 → skip, 1 → one, clamped). The
speaker-aware ``_truncate_dialogue_for_testing`` keeps one turn per *distinct*
host so test mode never drops a configured speaker (which would leave the
multi-speaker TTS contract a speaker short — the other half of the non-English
test-run failure).
"""

from __future__ import annotations

from matrx_ai.agent_runners.podcast_generator import (
    PodcastRequest,
    _effective_media_count,
    _truncate_dialogue_for_testing,
)


def test_effective_media_count_resolution():
    assert _effective_media_count(None, 5) == 5  # full default
    assert _effective_media_count(0, 5) == 0  # skip
    assert _effective_media_count(1, 5) == 1  # single
    assert _effective_media_count(3, 5) == 3
    assert _effective_media_count(9, 5) == 5  # clamp above the slot maximum
    assert _effective_media_count(-2, 5) == 0  # clamp below zero


def test_request_media_caps_default_to_none():
    req = PodcastRequest(show_id="s", input_data_type="topic", podcast_type="educational")
    assert req.max_images is None
    assert req.max_videos is None


def test_truncate_keeps_one_turn_per_distinct_speaker():
    script = (
        "<podcast_dialogue>\n"
        "Alex: one.\nSarah: two.\nAlex: three.\nSarah: four.\n"
        "</podcast_dialogue>"
    )
    assert _truncate_dialogue_for_testing(script, 2) == "Alex: one.\n\nSarah: two."


def test_truncate_covers_second_host_even_when_first_opens_twice():
    # The old "first N lines" logic kept [Alex, Alex] and dropped Sarah, so the
    # configured 2nd speaker never appeared in the transcript.
    script = "<podcast_dialogue>\nAlex: one.\nAlex: two.\nSarah: three.\n</podcast_dialogue>"
    out = _truncate_dialogue_for_testing(script, 2)
    assert "Alex: one." in out
    assert "Sarah: three." in out
    assert out.count("Alex:") == 1


def test_truncate_handles_non_latin_labels():
    script = "<podcast_dialogue>\nکیان: یک.\nسارا: دو.\nکیان: سه.\n</podcast_dialogue>"
    assert _truncate_dialogue_for_testing(script, 2) == "کیان: یک.\n\nسارا: دو."
