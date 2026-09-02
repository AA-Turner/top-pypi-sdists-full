"""Speaker-name adoption must never invert genders.

Adoption re-points the configured VOICES at the script's speaker labels. Doing
that positionally preserved the voice palette and destroyed the name↔gender
pairing: config [Sarah→female voice, Owen→male voice] against script
[Marcus, Elena] produced Marcus speaking with a female voice and Elena with a
male one — in an episode where the hosts say each other's names out loud.

These tests pin the fix: gender decides the pairing, position is only the
tiebreak when neither side resolves a gender, and where no same-gender pairing
exists a correct-gender voice is re-drawn from the injected pool.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.tts_config import (
    _VOICE_GENDER,
    _VOICES_BY_GENDER,
    TTSSpeaker,
    TTSVoiceConfig,
    configure_multi_speaker_voice_pool,
)

# A miniature Google-shaped pool: two female voices, two male.
_POOL = [("kore", "female"), ("leda", "female"), ("puck", "male"), ("orus", "male")]


@pytest.fixture
def pool():
    """Inject the pool for one test and restore the ambient one afterwards."""
    saved_gender = dict(_VOICE_GENDER)
    saved_by = {k: list(v) for k, v in _VOICES_BY_GENDER.items()}
    configure_multi_speaker_voice_pool(_POOL)
    yield
    configure_multi_speaker_voice_pool([(v, g) for v, g in saved_gender.items()])
    _VOICES_BY_GENDER.update(saved_by)


@pytest.fixture
def no_pool():
    """No pool injected — pairing still runs, repair cannot and must not crash."""
    saved_gender = dict(_VOICE_GENDER)
    saved_by = {k: list(v) for k, v in _VOICES_BY_GENDER.items()}
    _VOICE_GENDER.clear()
    _VOICES_BY_GENDER["male"] = []
    _VOICES_BY_GENDER["female"] = []
    yield
    _VOICE_GENDER.update(saved_gender)
    _VOICES_BY_GENDER.update(saved_by)


def _contents(text: str) -> list[dict]:
    return [{"role": "user", "parts": [{"text": text}]}]


def _by_name(cfg: TTSVoiceConfig) -> dict[str, str]:
    return {s.name: s.voice for s in cfg.speakers}


def _mixed_cast() -> TTSVoiceConfig:
    return TTSVoiceConfig(
        speakers=[
            TTSSpeaker("Sarah", "kore", "female"),
            TTSSpeaker("Owen", "puck", "male"),
        ]
    )


# ── THE INVERSION ───────────────────────────────────────────────────────────


def test_total_drift_pairs_by_gender_not_position(no_pool):
    """The reported defect. Script order is [Marcus, Elena]; config order is
    [Sarah(female), Owen(male)]. Positional pairing gave Marcus the female voice.
    Gender pairing gives Marcus the male voice and Elena the female one."""
    cfg = _mixed_cast()
    original = "Marcus: Welcome back.\n\nElena: Glad to be here."
    contents = _contents(original)
    cfg.adopt_script_speaker_names(contents)
    cfg.validate_speaker_names(contents)

    assert contents[0]["parts"][0]["text"] == original  # transcript untouched
    assert _by_name(cfg) == {"Marcus": "puck", "Elena": "kore"}


def test_gender_pairing_survives_a_declared_gender_that_beats_the_name(no_pool):
    """A caller-declared gender wins over the name table — the same chain the
    podcast pipeline resolves with."""
    cfg = TTSVoiceConfig(
        speakers=[
            # Name says male, the caller says otherwise; the caller is right.
            TTSSpeaker("Alex", "kore", "female"),
            TTSSpeaker("Ben", "puck", "male"),
        ]
    )
    cfg.adopt_script_speaker_names(_contents("Marcus: One.\n\nElena: Two."))
    assert _by_name(cfg) == {"Marcus": "puck", "Elena": "kore"}


def test_anchored_speaker_keeps_voice_while_the_other_pairs_by_gender(no_pool):
    """One configured name survives in the script; only the other is re-pointed."""
    cfg = _mixed_cast()
    cfg.adopt_script_speaker_names(_contents("Sarah: Hi.\n\nMarcus: Hello."))
    assert _by_name(cfg) == {"Sarah": "kore", "Marcus": "puck"}


def test_three_speakers_pair_by_gender_across_positions(no_pool):
    cfg = TTSVoiceConfig(
        speakers=[
            TTSSpeaker("Sarah", "kore", "female"),
            TTSSpeaker("Owen", "puck", "male"),
            TTSSpeaker("Maria", "leda", "female"),
        ]
    )
    cfg.adopt_script_speaker_names(
        _contents("Marcus: A.\n\nElena: B.\n\nPriya: C.\n\nMarcus: D.\n\nElena: E.\n\nPriya: F.")
    )
    assert _by_name(cfg)["Marcus"] == "puck"
    assert set(_by_name(cfg)) == {"Marcus", "Elena", "Priya"}
    assert {_by_name(cfg)["Elena"], _by_name(cfg)["Priya"]} == {"kore", "leda"}


# ── POSITIONAL FALLBACK — unchanged where gender can't decide ───────────────


def test_unknown_genders_fall_back_to_position(no_pool):
    """Non-Latin names resolve to no gender on either side; the previous
    first-appearance pairing is exactly what should still happen."""
    cfg = TTSVoiceConfig(speakers=[TTSSpeaker("کیان", "kore"), TTSSpeaker("نیکا", "puck")])
    cfg.adopt_script_speaker_names(_contents("الکس: سلام.\n\nسارا: درود."))
    assert [s.name for s in cfg.speakers] == ["الکس", "سارا"]
    assert [s.voice for s in cfg.speakers] == ["kore", "puck"]


def test_known_label_gender_with_unknown_config_gender_still_pairs_positionally(no_pool):
    """Gender on ONE side can't pair anything — falling back is correct, and the
    repair pass (pool injected) is what fixes the voice afterwards."""
    cfg = TTSVoiceConfig(speakers=[TTSSpeaker("کیان", "kore"), TTSSpeaker("نیکا", "puck")])
    cfg.adopt_script_speaker_names(_contents("Elena: One.\n\nMarcus: Two."))
    assert [s.name for s in cfg.speakers] == ["Elena", "Marcus"]
    assert [s.voice for s in cfg.speakers] == ["kore", "puck"]  # already correct by luck


# ── REPAIR — a correct-gender voice beats a curated one ────────────────────


def test_same_gender_script_redraws_a_correct_gender_voice(pool):
    """Both script labels are male, the config holds one male + one female voice.
    No pairing can fix that, so the female voice is REPLACED with an unused male
    one rather than shipping a man voiced as a woman."""
    cfg = _mixed_cast()
    cfg.adopt_script_speaker_names(_contents("Marcus: A.\n\nDavid: B."))
    voices = _by_name(cfg)
    assert set(voices) == {"Marcus", "David"}
    assert all(_VOICE_GENDER[v] == "male" for v in voices.values())
    assert len(set(voices.values())) == 2  # never two speakers on one voice


def test_repair_is_skipped_without_an_injected_pool(no_pool):
    """No pool → adoption still happens and nothing crashes; the mismatched
    voice is kept because nothing can prove it wrong."""
    cfg = _mixed_cast()
    cfg.adopt_script_speaker_names(_contents("Marcus: A.\n\nDavid: B."))
    assert sorted(s.name for s in cfg.speakers) == ["David", "Marcus"]
    assert sorted(s.voice for s in cfg.speakers) == ["kore", "puck"]


def test_repair_never_touches_an_anchored_speaker(pool):
    """A speaker the script already names keeps the voice upstream cast for it,
    even if this layer would judge it mismatched."""
    cfg = TTSVoiceConfig(
        speakers=[
            TTSSpeaker("Sarah", "puck", "female"),  # deliberately mismatched pin
            TTSSpeaker("Owen", "orus", "male"),
        ]
    )
    cfg.adopt_script_speaker_names(_contents("Sarah: Hi.\n\nMarcus: Hello."))
    assert _by_name(cfg)["Sarah"] == "puck"


# ── SERIALISATION ──────────────────────────────────────────────────────────


def test_gender_round_trips_and_stays_optional():
    assert TTSSpeaker.from_dict({"name": "Sarah", "voice": "kore"}).gender == ""
    assert TTSSpeaker("Sarah", "kore").to_dict() == {"name": "Sarah", "voice": "kore"}
    spoken = TTSSpeaker.from_dict({"name": "Sarah", "voice": "kore", "gender": "female"})
    assert spoken.gender == "female"
    assert spoken.to_dict() == {"name": "Sarah", "voice": "kore", "gender": "female"}


def test_to_google_still_sends_only_name_and_voice(pool):
    """Gender is an internal pairing signal — it must never reach the provider."""
    pytest.importorskip("google.genai")
    cfg = _mixed_cast()
    speech = cfg.to_google(_contents("Marcus: A.\n\nElena: B."))
    configs = speech.multi_speaker_voice_config.speaker_voice_configs
    assert {c.speaker for c in configs} == {"Marcus", "Elena"}
    assert not any(hasattr(c, "gender") for c in configs)
