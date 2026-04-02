"""Tests for ai/hume_voice.py — voice signature → Hume AI mapping."""

from __future__ import annotations

import pytest

from heylead.ai.hume_voice import (
    ALL_SLIDERS,
    _build_acting_instructions,
    _clamp,
    _map_formality_to_sliders,
    _map_style_keywords,
    _map_style_to_speed,
    _map_tone_keywords,
    create_voice_config,
    validate_voice_config,
)


# ── _clamp ──


def test_clamp_within_range():
    assert _clamp(50) == 50


def test_clamp_below_min():
    assert _clamp(-150) == -100


def test_clamp_above_max():
    assert _clamp(200) == 100


def test_clamp_edges():
    assert _clamp(-100) == -100
    assert _clamp(100) == 100


# ── _map_formality_to_sliders ──


class TestFormalityMapping:
    def test_casual_low(self):
        sliders = _map_formality_to_sliders(1)
        assert sliders["relaxedness"] == 90
        assert sliders["assertiveness"] == 20
        assert sliders["smoothness"] == 30

    def test_casual_high(self):
        sliders = _map_formality_to_sliders(3)
        assert sliders["relaxedness"] == 70
        assert sliders["assertiveness"] == 40
        assert sliders["smoothness"] == 50

    def test_balanced_low(self):
        sliders = _map_formality_to_sliders(4)
        assert sliders["relaxedness"] == 60
        assert sliders["assertiveness"] == 40
        assert sliders["smoothness"] == 50

    def test_balanced_high(self):
        sliders = _map_formality_to_sliders(6)
        assert sliders["relaxedness"] == 40
        assert sliders["assertiveness"] == 60
        assert sliders["smoothness"] == 70

    def test_formal_low(self):
        sliders = _map_formality_to_sliders(7)
        assert sliders["relaxedness"] == 40
        assert sliders["assertiveness"] == 60
        assert sliders["smoothness"] == 70

    def test_formal_high(self):
        sliders = _map_formality_to_sliders(10)
        assert sliders["relaxedness"] == 20
        assert sliders["assertiveness"] == 80
        assert sliders["smoothness"] == 90

    def test_all_sliders_present(self):
        for level in range(1, 11):
            sliders = _map_formality_to_sliders(level)
            for name in ALL_SLIDERS:
                assert name in sliders, f"Missing slider {name} at formality {level}"

    def test_clamps_input(self):
        # Out of range values should be clamped
        sliders_0 = _map_formality_to_sliders(0)
        sliders_1 = _map_formality_to_sliders(1)
        assert sliders_0 == sliders_1

        sliders_11 = _map_formality_to_sliders(11)
        sliders_10 = _map_formality_to_sliders(10)
        assert sliders_11 == sliders_10


# ── _map_tone_keywords ──


class TestToneMapping:
    def test_warm(self):
        deltas = _map_tone_keywords("Warm and approachable")
        assert deltas.get("buoyancy", 0) > 0
        assert deltas.get("enthusiasm", 0) > 0

    def test_direct(self):
        deltas = _map_tone_keywords("Direct, technical")
        assert deltas.get("assertiveness", 0) > 0
        assert deltas.get("tepidity", 0) < 0

    def test_combined_keywords(self):
        deltas = _map_tone_keywords("Direct, warm, confident")
        # All three keywords contribute
        assert deltas.get("assertiveness", 0) > 0
        assert deltas.get("buoyancy", 0) > 0
        assert deltas.get("confidence", 0) > 0

    def test_case_insensitive(self):
        deltas_lower = _map_tone_keywords("warm")
        deltas_upper = _map_tone_keywords("Warm")
        assert deltas_lower == deltas_upper

    def test_no_match(self):
        deltas = _map_tone_keywords("xyzzy gibberish")
        assert deltas == {}

    def test_empty_string(self):
        deltas = _map_tone_keywords("")
        assert deltas == {}


# ── _map_style_keywords ──


class TestStyleMapping:
    def test_analytical_style(self):
        deltas = _map_style_keywords(["analytical", "clear"])
        assert deltas.get("assertiveness", 0) > 0

    def test_empty_list(self):
        deltas = _map_style_keywords([])
        assert deltas == {}

    def test_half_weight(self):
        tone_deltas = _map_tone_keywords("warm")
        style_deltas = _map_style_keywords(["warm"])
        # Style deltas should be roughly half of tone deltas
        for key in tone_deltas:
            if key in style_deltas:
                assert abs(style_deltas[key]) <= abs(tone_deltas[key])


# ── _map_style_to_speed ──


class TestSpeedMapping:
    def test_default_speed(self):
        speed = _map_style_to_speed([], "Medium")
        assert speed == 1.0

    def test_short_sentences_faster(self):
        speed = _map_style_to_speed([], "Short (avg 8 words)")
        assert speed > 1.0

    def test_long_sentences_slower(self):
        speed = _map_style_to_speed([], "Long, compound sentences")
        assert speed < 1.0

    def test_energetic_style_faster(self):
        speed = _map_style_to_speed(["energetic", "enthusiastic"], "Medium")
        assert speed > 1.0

    def test_analytical_style_slower(self):
        speed = _map_style_to_speed(["analytical", "deliberate"], "Medium")
        assert speed < 1.0

    def test_clamped_range(self):
        # Even extreme inputs stay in [0.8, 1.2]
        speed = _map_style_to_speed(
            ["energetic", "enthusiastic", "direct", "concise"],
            "Short"
        )
        assert 0.8 <= speed <= 1.2


# ── _build_acting_instructions ──


class TestActingInstructions:
    def test_basic_output(self):
        voice = {
            "tone": "Direct, technical",
            "communication_style": ["clear", "analytical"],
            "sentence_length": "Short (avg 8 words)",
            "no_go": "Emojis, buzzwords",
        }
        instructions = _build_acting_instructions(voice)
        assert "Direct, technical" in instructions
        assert "brisk" in instructions.lower()
        assert len(instructions) <= 200

    def test_long_output_truncated(self):
        voice = {
            "tone": "A" * 100,
            "communication_style": ["B" * 50, "C" * 50, "D" * 50],
            "sentence_length": "Long compound sentences with lots of detail",
            "no_go": "E" * 100,
        }
        instructions = _build_acting_instructions(voice)
        assert len(instructions) <= 200

    def test_empty_voice(self):
        instructions = _build_acting_instructions({})
        assert isinstance(instructions, str)


# ── create_voice_config ──


class TestCreateVoiceConfig:
    def test_basic_config(self):
        voice = {
            "tone": "Direct, professional",
            "sentence_length": "Medium",
            "formality_level": 7,
            "communication_style": ["clear", "analytical"],
            "vocabulary_preferences": ["technical"],
            "no_go": "Buzzwords",
        }
        config = create_voice_config(voice)

        assert "sliders" in config
        assert "speed" in config
        assert "acting_instructions" in config
        assert config["output_format"] == "mp3"
        assert config["sample_rate"] == 48000

    def test_all_sliders_in_range(self):
        voice = {
            "tone": "Warm, enthusiastic, bold, confident, direct",
            "formality_level": 1,
            "communication_style": ["energetic", "enthusiastic"],
            "sentence_length": "Short",
        }
        config = create_voice_config(voice)
        for name, value in config["sliders"].items():
            assert -100 <= value <= 100, f"{name}={value} out of range"

    def test_nested_voice_key(self):
        # Voice signature may be nested under "voice" key
        sig = {
            "voice": {
                "tone": "Casual, friendly",
                "formality_level": 3,
                "communication_style": [],
                "sentence_length": "Medium",
            }
        }
        config = create_voice_config(sig)
        assert config["sliders"]["relaxedness"] > 50  # Casual = high relaxedness

    def test_missing_fields_use_defaults(self):
        config = create_voice_config({})
        assert "sliders" in config
        assert config["speed"] == 1.0


# ── validate_voice_config ──


class TestValidateVoiceConfig:
    def test_valid_config(self):
        config = create_voice_config({
            "tone": "Direct",
            "formality_level": 5,
            "communication_style": [],
            "sentence_length": "Medium",
        })
        valid, err = validate_voice_config(config)
        assert valid is True
        assert err == ""

    def test_missing_sliders(self):
        valid, err = validate_voice_config({"speed": 1.0})
        assert valid is False
        assert "sliders" in err.lower()

    def test_slider_out_of_range(self):
        config = create_voice_config({"formality_level": 5})
        config["sliders"]["assertiveness"] = 150
        valid, err = validate_voice_config(config)
        assert valid is False
        assert "assertiveness" in err

    def test_bad_speed(self):
        config = create_voice_config({"formality_level": 5})
        config["speed"] = 5.0
        valid, err = validate_voice_config(config)
        assert valid is False
        assert "speed" in err.lower()

    def test_not_a_dict(self):
        valid, err = validate_voice_config("not a dict")
        assert valid is False
