"""Gender-aware ElevenLabs voice assignment + per-episode rotation.

Both provider bands must hand a speaker a voice that matches its declared
gender and resolve the same cast for the same episode input (resume-safe),
while different episodes rotate across the available voice pools.
"""

from __future__ import annotations

from matrx_ai.agent_runners.podcast_generator import (
    _ELEVENLABS_BY_GENDER,
    _ELEVENLABS_VOICE_GENDER,
    _GOOGLE_VOICE_GENDER,
    PodcastRequest,
    SpeakerSpec,
    _effective_speakers,
    _normalize_gender,
)


def _dialogue(*names: str) -> str:
    body = "\n".join(f"{n}: line {i}." for i, n in enumerate(names))
    return f"<podcast_dialogue>\n{body}\n</podcast_dialogue>"


def _script(*pairs: tuple[str, str]) -> str:
    names = [p[0] for p in pairs]
    speakers = ",".join(f'{{"name":"{n}","gender":"{g}"}}' for n, g in pairs)
    return _dialogue(*names) + f'\n<speaker_settings>{{"speakers":[{speakers}]}}</speaker_settings>'


def _req(show_id: str, host_count: int) -> PodcastRequest:
    return PodcastRequest(
        show_id=show_id,
        input_data_type="topic",
        podcast_type="educational",
        host_count=host_count,
    )


def test_normalize_gender_buckets():
    assert _normalize_gender("Male") == "male"
    assert _normalize_gender("f") == "female"
    assert _normalize_gender("woman") == "female"
    assert _normalize_gender("") == "neutral"
    assert _normalize_gender(None) == "neutral"
    assert _normalize_gender("robot") == "neutral"


def test_elevenlabs_pool_is_gender_balanced():
    # The whole point of the fix: a real pool to draw from, per gender.
    assert len(_ELEVENLABS_BY_GENDER["male"]) >= 5
    assert len(_ELEVENLABS_BY_GENDER["female"]) >= 5


def test_declared_gender_drives_matching_voice():
    script = _script(("Mark", "male"), ("Sarah", "female"), ("David", "male"))
    cast = _effective_speakers(_req("show-1", 3), _dialogue("Mark", "Sarah", "David"), script)
    by_name = {s.name: s for s in cast}
    assert _ELEVENLABS_VOICE_GENDER[by_name["Mark"].voice] == "male"
    assert _ELEVENLABS_VOICE_GENDER[by_name["Sarah"].voice] == "female"
    assert _ELEVENLABS_VOICE_GENDER[by_name["David"].voice] == "male"
    # Distinct speakers → distinct voices within an episode.
    assert len({s.voice for s in cast}) == 3


def test_same_show_id_is_deterministic_resume_safe():
    script = _script(("Mark", "male"), ("Sarah", "female"), ("David", "male"))
    dlg = _dialogue("Mark", "Sarah", "David")
    a = _effective_speakers(_req("stable", 3), dlg, script)
    b = _effective_speakers(_req("stable", 3), dlg, script)
    assert [s.voice for s in a] == [s.voice for s in b]


def test_different_show_ids_vary_voices():
    script = _script(("Mark", "male"), ("Sarah", "female"), ("David", "male"))
    dlg = _dialogue("Mark", "Sarah", "David")
    seen: set[tuple[str, ...]] = set()
    for sid in ("a", "b", "c", "d", "e", "f", "g", "h"):
        cast = _effective_speakers(_req(sid, 3), dlg, script)
        seen.add(tuple(s.voice for s in cast))
    # Across several episodes we expect more than one distinct casting.
    assert len(seen) > 1


def test_explicit_pinned_voice_wins_over_pool():
    pinned = _ELEVENLABS_BY_GENDER["female"][0]
    req = _req("show-x", 3)
    req.speakers = [SpeakerSpec(name="Mark", voice=pinned, gender="male")]
    script = _script(("Mark", "male"), ("Sarah", "female"), ("David", "male"))
    cast = _effective_speakers(req, _dialogue("Mark", "Sarah", "David"), script)
    # Pinned voice is honored even though it disagrees with the declared gender.
    assert next(s.voice for s in cast if s.name == "Mark") == pinned


def test_two_host_google_path_is_gender_matched_and_resume_safe():
    script = _script(("Mark", "male"), ("Sarah", "female"))
    dialogue = _dialogue("Mark", "Sarah")
    cast = _effective_speakers(_req("anything", 2), dialogue, script)
    replay = _effective_speakers(_req("anything", 2), dialogue, script)
    assert [s.voice for s in cast] == [s.voice for s in replay]
    assert _GOOGLE_VOICE_GENDER[cast[0].voice] == "male"
    assert _GOOGLE_VOICE_GENDER[cast[1].voice] == "female"
    assert cast[0].voice != cast[1].voice
