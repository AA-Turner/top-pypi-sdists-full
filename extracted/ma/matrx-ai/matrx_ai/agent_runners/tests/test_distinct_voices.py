"""THE INVARIANT: two speakers in one podcast episode never share a voice.

A two-host episode rendered in ONE voice is indistinguishable, to a listener,
from a model failure — which is why this is enforced by construction rather
than left to the draw. The pool draw prefers unused voices, but EXPLICIT pins
(the studio voice picker, a request body) bypassed it entirely until 2026-08-10.

These tests run against the curated fallback pool, whose gender labels are kept
in sync with the live ``ai.voices`` catalog (verified 2026-08-10: 14 female /
16 male enabled Google voices).
"""

from __future__ import annotations

import pytest

import matrx_ai.agent_runners.podcast_generator as pg


@pytest.fixture(autouse=True)
def _real_google_pool():
    pg._GOOGLE_VOICE_POOL = list(pg._GOOGLE_VOICE_POOL_FALLBACK)
    pg._rebuild_google_derived()
    yield


def _voices(specs) -> list[str]:
    return [s.voice for s in specs]


def test_same_voice_pinned_to_both_speakers_is_repaired():
    """The exact shape that ships a 'two host' episode in one voice."""
    out = pg._assign_dialogue_voices(
        ["Sarah", "David"],
        {"Sarah": "kore", "David": "kore"},
        {"Sarah": "female", "David": "male"},
        seed="dup-pin",
        provider="google",
    )
    voices = _voices(out)
    assert len(set(voices)) == 2, f"speakers share a voice: {voices}"
    # The first speaker keeps the pinned voice; the collider is re-drawn.
    assert out[0].voice == "kore"
    # And the repair respects the collider's DECLARED gender.
    assert pg._GOOGLE_VOICE_GENDER[out[1].voice] == "male"


def test_repair_prefers_declared_gender():
    out = pg._assign_dialogue_voices(
        ["A", "B"],
        {"A": "orus", "B": "orus"},
        {"A": "male", "B": "female"},
        seed="dup-pin-female",
        provider="google",
    )
    assert pg._GOOGLE_VOICE_GENDER[out[1].voice] == "female"
    assert out[0].voice != out[1].voice


@pytest.mark.parametrize("seed", [f"seed-{i}" for i in range(12)])
def test_rotation_never_repeats_a_voice_within_an_episode(seed):
    """Rotation exists so episodes differ; it must never differ INTO a collision."""
    out = pg._assign_dialogue_voices(
        ["Alex", "Sam"], {}, {"Alex": "female", "Sam": "male"},
        seed=seed, provider="google",
    )
    voices = _voices(out)
    assert len(set(voices)) == 2, f"seed {seed} collided: {voices}"
    assert pg._GOOGLE_VOICE_GENDER[out[0].voice] == "female"
    assert pg._GOOGLE_VOICE_GENDER[out[1].voice] == "male"


def test_two_host_default_cast_is_mixed_gender():
    """A 2-host default cast draws one male and one female — never two of one."""
    for i in range(12):
        cast = pg._default_cast(2, seed=f"cast-{i}")
        genders = {g for _n, g in cast}
        assert genders == {"male", "female"}, f"seed {i} gave {cast}"


def test_large_cast_may_share_only_past_the_provider_cap():
    """Sharing is legitimate ONLY when the cast exceeds the provider's cap."""
    names = [f"S{i}" for i in range(6)]
    genders = {n: ("female" if i % 2 == 0 else "male") for i, n in enumerate(names)}
    out = pg._assign_dialogue_voices(names, {}, genders, seed="six", provider="elevenlabs")
    voices = _voices(out)
    assert len(set(voices)) == len(voices), f"under the cap, voices must be distinct: {voices}"
