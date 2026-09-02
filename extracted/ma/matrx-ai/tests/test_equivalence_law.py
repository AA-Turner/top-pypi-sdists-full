"""THE EQUIVALENCE LAW — a setting converts to the target's nearest equivalent,
and is dropped ONLY when the target has no equivalent.

Arman, 2026-08-17: any config from any provider must convert when you point it
at any other model, "without anything being dropped or lost — unless it's an
additive configuration offering something that the given new model does not
support." Measured before this landed: `on_unmapped` defaulted to "drop" and
135 of 135 live value_map rules took that default — 1,132 (value x model)
combinations discarded instead of converted.
"""

from __future__ import annotations

import pytest

from matrx_ai.catalog.controls import CompiledControlsMap, validate_rules_against_settings
from matrx_ai.catalog.equivalence import nearest_equivalent
from matrx_ai.catalog.models import CatalogSetting, ControlRule

EFFORT_ORDER = ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"]


class TestConversionIsTheDefault:
    def test_on_unmapped_defaults_to_nearest(self):
        # The whole point: conversion is the default posture; dropping is the
        # thing a rule must explicitly declare.
        assert ControlRule().on_unmapped == "nearest"

    def test_an_unmapped_effort_converts_instead_of_vanishing(self):
        compiled = CompiledControlsMap(
            rules={
                "reasoning_effort": ControlRule.model_validate(
                    {"value_map": {"low": "low", "high": "high"}}
                )
            },
            value_orders={"reasoning_effort": EFFORT_ORDER},
        )
        out, adj = compiled.outbound({"reasoning_effort": "max"})
        assert out == {"reasoning_effort": "high"}  # not dropped
        assert adj[0].action == "mapped"

    def test_a_declared_drop_is_still_honoured(self):
        compiled = CompiledControlsMap(
            rules={
                "reasoning_effort": ControlRule.model_validate(
                    {"value_map": {"low": "low"}, "on_unmapped": "drop"}
                )
            },
            value_orders={"reasoning_effort": EFFORT_ORDER},
        )
        out, adj = compiled.outbound({"reasoning_effort": "max"})
        assert out == {}
        assert adj[0].action == "dropped"


class TestAspectRatioConvertsByGeometry:
    @pytest.mark.parametrize(
        "asked,expected",
        [("21:9", "16:9"), ("16:10", "16:9"), ("4:3", "1:1"), ("9:16", "9:16")],
    )
    def test_nearest_by_ratio_not_list_position(self, asked, expected):
        got = nearest_equivalent("aspect_ratio", asked, {"16:9", "1:1", "9:16"})
        assert got == expected

    def test_orientation_is_never_flipped(self):
        # A portrait request must not resolve to a landscape crop of itself.
        assert nearest_equivalent("aspect_ratio", "9:21", {"16:9", "9:16"}) == "9:16"
        assert nearest_equivalent("aspect_ratio", "21:9", {"16:9", "9:16"}) == "16:9"


class TestFormatFamilies:
    def test_same_format_different_parameterisation_wins(self):
        assert nearest_equivalent("audio_format", "mp3", {"mp3_44100_128", "wav"}) == "mp3_44100_128"

    def test_lossy_converts_within_its_family_before_leaving_it(self):
        assert nearest_equivalent("output_format", "webp", {"png", "jpeg"}) == "png"
        assert nearest_equivalent("audio_format", "opus", {"wav", "aac"}) == "aac"

    def test_unrelated_format_has_no_equivalent(self):
        # output_format (still images) has NO cross-family fallback — that
        # step is an audio_format-only carve-out, so this must stay None.
        assert nearest_equivalent("output_format", "webp", {"mp3"}) is None

    def test_telephony_synonyms_unify(self):
        # mulaw/ulaw_8000 are the SAME codec spelled two ways, as are
        # alaw/alaw_8000 — either spelling must find the other.
        assert nearest_equivalent("audio_format", "ulaw_8000", {"mulaw"}) == "mulaw"
        assert nearest_equivalent("audio_format", "mulaw", {"ulaw_8000"}) == "ulaw_8000"
        assert nearest_equivalent("audio_format", "alaw", {"alaw_8000"}) == "alaw_8000"
        assert nearest_equivalent("audio_format", "alaw_8000", {"alaw"}) == "alaw"

    def test_parameterised_member_reaches_a_different_base_in_its_family(self):
        # wav_24000's base (wav) isn't offered at all, but pcm is — same
        # lossless family, and the target set carries a SAMPLE RATE match.
        assert nearest_equivalent("audio_format", "wav_24000", {"pcm_24000", "pcm_8000"}) == "pcm_24000"

    def test_sample_rate_preference_falls_back_when_no_rate_matches(self):
        assert nearest_equivalent("audio_format", "wav_24000", {"pcm_8000", "pcm_16000"}) == "pcm_16000"

    def test_same_family_always_wins_over_cross_family(self):
        # opus (lossy) must land on aac (lossy), never alaw (telephony), even
        # though alaw is offered too — same family is tried FIRST, always.
        assert nearest_equivalent("audio_format", "opus_48000_128", {"aac", "alaw"}) == "aac"

    def test_cross_family_last_resort_prefers_lossless_then_lossy_then_telephony(self):
        # wav's own family (lossless) has nothing on the target; the fallback
        # reaches lossy (mp3) before it would ever consider telephony (alaw).
        assert nearest_equivalent("audio_format", "wav", {"mp3", "alaw"}) == "mp3"
        # mp3's own family (lossy) has nothing; telephony is the only thing
        # left, and audio_format is allowed to reach it as a last resort —
        # some audio beats the setting silently vanishing.
        assert nearest_equivalent("audio_format", "mp3", {"alaw_8000"}) == "alaw_8000"
        # mulaw's own family (telephony) has nothing; lossless is offered
        # ahead of lossy in the fallback order.
        assert nearest_equivalent("audio_format", "mulaw", {"mp3", "wav"}) == "wav"

    def test_unclassified_audio_base_still_refuses_to_guess(self):
        # A base outside the three known audio families (lossy/lossless/
        # telephony) has no honest equivalence to measure — even though a
        # candidate exists, forcing a cross-family guess here would be the
        # "converting WRONG" violation (law rule 4), not a fix.
        assert nearest_equivalent("audio_format", "some_bogus_codec", {"wav"}) is None

    def test_empty_candidate_set_has_no_equivalent(self):
        assert nearest_equivalent("audio_format", "aac", set()) is None


class TestNoDishonestConversion:
    def test_a_voice_has_no_nearest(self):
        # A voice is an identity, not a degree — inventing one is worse than a
        # loud drop. Pending a product ruling on per-provider defaults.
        assert nearest_equivalent("tts_voice", "alloy", {"kore", "puck"}) is None

    def test_house_postures_are_never_the_equivalent_of_a_degree(self):
        # "minimal" must never resolve to "none" (think a little -> do not think).
        got = nearest_equivalent("reasoning_effort", "minimal", {"none", "high"}, EFFORT_ORDER)
        assert got == "high"

    def test_an_unregistered_setting_refuses_to_guess(self):
        assert nearest_equivalent("some_new_enum", "a", {"b", "c"}) is None


class TestPostureToPosture:
    def test_a_posture_may_resolve_to_another_posture(self):
        # The house filter guards INTENSITY -> posture, not posture -> posture:
        # an offering that expresses "no reasoning" as an omitted key is a valid
        # translation of "none". (Caught by test_catalog_rule_vocabulary, not by
        # the first cut of this file.)
        assert nearest_equivalent("reasoning_effort", "none", {"auto"}, EFFORT_ORDER) == "auto"


# ── LAW RULE 5: voice gender is load-bearing; identity usually is not ────────
VOICE_GENDERS = {
    "kore": "female",
    "aoede": "female",
    "puck": "male",
    "charon": "male",
    "alloy": "unknown",
    "ash": "unknown",
}


class TestVoiceGender:
    def test_female_resolves_to_female(self):
        got = nearest_equivalent(
            "tts_voice", "kore", {"puck", "charon", "aoede"}, genders=VOICE_GENDERS
        )
        assert VOICE_GENDERS[got] == "female"

    def test_male_resolves_to_male(self):
        got = nearest_equivalent(
            "tts_voice", "puck", {"kore", "aoede", "charon"}, genders=VOICE_GENDERS
        )
        assert VOICE_GENDERS[got] == "male"

    def test_gender_is_NEVER_crossed(self):
        # A podcast that silently swaps its male host for a female voice is
        # worse than one that says it could not cast the part.
        assert (
            nearest_equivalent("tts_voice", "puck", {"kore", "aoede"}, genders=VOICE_GENDERS)
            is None
        )

    def test_a_genderless_voice_is_a_wildcard_target(self):
        got = nearest_equivalent("tts_voice", "puck", {"kore", "alloy"}, genders=VOICE_GENDERS)
        assert got == "alloy"

    def test_a_genderless_request_accepts_anything(self):
        got = nearest_equivalent("tts_voice", "alloy", {"kore", "puck"}, genders=VOICE_GENDERS)
        assert got in {"kore", "puck"}

    def test_selection_is_deterministic(self):
        # The same request must never cast a different voice run to run.
        picks = {
            nearest_equivalent(
                "tts_voice", "kore", {"aoede", "charon", "puck"}, genders=VOICE_GENDERS
            )
            for _ in range(25)
        }
        assert len(picks) == 1

    def test_without_gender_data_it_refuses_rather_than_casting_blind(self):
        assert nearest_equivalent("tts_voice", "kore", {"puck"}) is None


# ── LAW RULE 3: converting to a default is legal ONLY when EXPLICIT ──────────
class TestExplicitDefault:
    def test_a_declared_value_resolves_to_the_default(self):
        compiled = CompiledControlsMap(
            rules={
                "reasoning_effort": ControlRule.model_validate(
                    {
                        "to_default": ["xhigh"],
                        "default": "medium",
                    }
                )
            },
        )
        out, adj = compiled.outbound({"reasoning_effort": "xhigh"})
        assert out == {"reasoning_effort": "medium"}
        assert adj[0].action == "to_default"
        assert adj[0].canonical_value == "xhigh"
        assert adj[0].sent_value == "medium"
        assert adj[0].expected is True

    def test_to_default_takes_precedence_over_value_map(self):
        # A value_map entry that WOULD convert "xhigh" is present, but
        # to_default is a declared decision and wins — it must never be
        # silently overridden by an inferred conversion.
        compiled = CompiledControlsMap(
            rules={
                "reasoning_effort": ControlRule.model_validate(
                    {
                        "value_map": {"xhigh": "high"},
                        "to_default": ["xhigh"],
                        "default": "medium",
                    }
                )
            },
        )
        out, adj = compiled.outbound({"reasoning_effort": "xhigh"})
        assert out == {"reasoning_effort": "medium"}
        assert len(adj) == 1
        assert adj[0].action == "to_default"

    def test_a_value_not_in_to_default_still_converts_normally(self):
        compiled = CompiledControlsMap(
            rules={
                "reasoning_effort": ControlRule.model_validate(
                    {
                        # NOTE: "high" maps to a DIFFERENT provider word on purpose.
                        # An identity mapping (high -> high) is not an Adjustment —
                        # nothing of the user's was changed — so asserting one here
                        # would be asserting a bug.
                        "value_map": {"low": "low", "high": "maximum"},
                        "to_default": ["xhigh"],
                        "default": "medium",
                    }
                )
            },
            value_orders={"reasoning_effort": EFFORT_ORDER},
        )
        out, adj = compiled.outbound({"reasoning_effort": "high"})
        assert out == {"reasoning_effort": "maximum"}  # converted, not defaulted
        assert [a.action for a in adj] == ["mapped"]
        assert not any(a.action == "to_default" for a in adj)

    def test_no_default_set_omits_the_key(self):
        compiled = CompiledControlsMap(
            rules={"reasoning_effort": ControlRule.model_validate({"to_default": ["xhigh"]})},
        )
        out, adj = compiled.outbound({"reasoning_effort": "xhigh"})
        assert out == {}
        assert adj[0].action == "to_default"
        assert adj[0].sent_value is None
        assert adj[0].expected is True

    def test_validation_rejects_a_to_default_value_outside_canonical_values(self):
        settings = {
            "reasoning_effort": CatalogSetting(
                key="reasoning_effort",
                value_type="enum",
                canonical_values=["low", "high"],
            )
        }
        rules = {
            "reasoning_effort": ControlRule.model_validate(
                {"to_default": ["xhigh"], "default": "high"}
            )
        }
        errors = validate_rules_against_settings(rules, settings)
        assert any("to_default" in e and "xhigh" in e for e in errors)

    def test_validation_rejects_a_value_in_both_to_default_and_value_map(self):
        settings = {
            "reasoning_effort": CatalogSetting(
                key="reasoning_effort",
                value_type="enum",
                canonical_values=["low", "high", "xhigh"],
            )
        }
        rules = {
            "reasoning_effort": ControlRule.model_validate(
                {
                    "value_map": {"xhigh": "high"},
                    "to_default": ["xhigh"],
                    "default": "high",
                }
            )
        }
        errors = validate_rules_against_settings(rules, settings)
        assert any("BOTH to_default and value_map" in e for e in errors)
