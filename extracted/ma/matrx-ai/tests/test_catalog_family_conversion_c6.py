"""Settings-translation item C6 — K7 family conversion, the supported:false
redefinition, position-based nearest, the declared output ceiling, and the
rejection record's provenance. Pure units — no DB.

Owner's words (GROUND-TRUTH, 2026-10-02): "If I send a request to Opus with
thinking levels set to extremely high … to the image generation model. My
request should go through, and the thinking level should be converted to image
resolution."
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.catalog.canonicalize import canonical_settings_from_config
from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.families import SettingFamilies
from matrx_ai.catalog.models import CatalogSetting, CellRef, ControlRule
from matrx_ai.providers import outbound_params
from matrx_ai.providers.outbound_params import (
    drop_foreign_canonical_keys,
    resolve_outbound_params,
)

EFFORT = ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"]

# The family + position seed as it stands on the nightly clone (subset).
SETTINGS = {
    "reasoning_effort": (
        "intensity",
        "enum",
        EFFORT,
        {"minimal": 0.0, "low": 0.143, "medium": 0.429, "high": 0.571, "xhigh": 0.798, "max": 1.0},
    ),
    "thinking_level": (
        "intensity",
        "enum",
        ["minimal", "low", "medium", "high"],
        {"minimal": 0.0, "low": 0.143, "medium": 0.429, "high": 0.571},
    ),
    "thinking_budget": ("intensity", "integer", None, None),
    "quality": (
        "intensity",
        "enum",
        ["low", "medium", "high", "xhigh", "max", "auto"],
        {"low": 0.143, "medium": 0.429, "high": 0.571, "xhigh": 0.798, "max": 1.0},
    ),
    "resolution": (
        "intensity",
        "enum",
        ["480p", "720p", "1080p", "1024p", "4k", "0.5k", "1k", "2k"],
        {
            "0.5k": 0.0,
            "480p": 0.107,
            "720p": 0.302,
            "1k": 0.333,
            "1024p": 0.472,
            "1080p": 0.497,
            "2k": 0.667,
            "4k": 1.0,
        },
    ),
    "include_thoughts": ("visibility", "boolean", None, None),
    "reasoning_summary": (
        "visibility",
        "enum",
        ["auto", "concise", "detailed", "never", "always"],
        {"never": 0.0, "concise": 0.5, "detailed": 1.0, "always": 1.0},
    ),
    "temperature": ("randomness", "number", None, None),
    "top_p": ("randomness", "number", None, None),
    "max_output_tokens": ("length", "integer", None, None),
    "tts_voice": ("voice", "enum", ["kore", "puck"], None),
    "voice_settings": ("voice", "string", None, None),
    "stop_sequences": ("none", "string_array", None, None),
}


def _settings(with_families: bool = True) -> dict[str, CatalogSetting]:
    return {
        key: CatalogSetting(
            key=key,
            value_type=vt,
            canonical_values=values,
            family=fam if with_families else None,
            value_positions=pos if with_families else None,
        )
        for key, (fam, vt, values, pos) in SETTINGS.items()
    }


FAMILIES = SettingFamilies.from_settings(_settings())


def _map(rules: dict[str, dict], *, families: bool = True, **extra) -> CompiledControlsMap:
    return CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()},
        value_orders={k: v[2] for k, v in SETTINGS.items() if v[2]},
        families=FAMILIES if families else None,
        **extra,
    )


def _wire(controls: CompiledControlsMap, **config) -> dict:
    return resolve_outbound_params(SimpleNamespace(**config), controls)


def _gate(controls: CompiledControlsMap, **config):
    canonical = canonical_settings_from_config(SimpleNamespace(**config))
    gate: list = []
    drop_foreign_canonical_keys(canonical, controls, adjustments=gate)
    params, adjustments = controls.outbound(canonical)
    return params, gate + adjustments


# An image offering shaped like the clone's xAI / Imagen rows: it carries
# quality (ui_values) and resolution, and declares reasoning_effort
# supported:false (K6: "not native here — convert through the family").
IMAGE = {
    "quality": {
        "ui_values": ["auto", "low", "medium", "high"],
        "value_map": {"auto": "auto", "low": "low", "medium": "medium", "high": "high"},
        "default": "auto",
    },
    "resolution": {"value_map": {"1k": "1K", "2k": "2K"}},
    "reasoning_effort": {"supported": False},
}
# A Veo-shaped video offering: resolution only, nothing about reasoning at all.
VIDEO = {"resolution": {"value_map": {"720p": "720p", "1080p": "1080p", "4k": "4k"}}}
# A text model with reasoning_effort only.
TEXT = {
    "reasoning_effort": {
        "provider_key": "reasoning.effort",
        "value_map": {e: e for e in ("minimal", "low", "medium", "high", "xhigh")},
    },
    "temperature": {},
    "max_output_tokens": {"provider_key": "max_completion_tokens"},
}


class TestOwnerCase:
    def test_extreme_thinking_at_an_image_model_becomes_its_top_quality(self):
        params, adjustments = _gate(_map(IMAGE), reasoning_effort="max")
        assert params == {"quality": "high"}
        [conv] = [a for a in adjustments if a.converted_from]
        assert (conv.key, conv.converted_from, conv.sent_value) == (
            "quality",
            "reasoning_effort",
            "high",
        )
        assert conv.expected is True
        assert not [a for a in adjustments if not a.expected]

    def test_extreme_thinking_at_a_video_model_becomes_its_top_resolution(self):
        assert _wire(_map(VIDEO), reasoning_effort="max") == {"resolution": "4k"}

    def test_a_large_thinking_budget_converts_through_the_effort_scale(self):
        # 50,000 tokens -> xhigh (the declared default steps) -> nearest resolution
        params, _ = _gate(_map(VIDEO), thinking_budget=50000)
        assert params == {"resolution": "1080p"} or params == {"resolution": "4k"}
        params, _ = _gate(_map(IMAGE), thinking_budget=50000)
        assert params == {"quality": "high"}

    def test_no_warning_reaches_the_client(self, monkeypatch):
        sent: list = []
        monkeypatch.setattr(outbound_params, "send_client_warning", lambda p, **k: sent.append(p))
        _wire(_map(IMAGE), reasoning_effort="max")
        assert sent == []


class TestUndeclaredDropWarns:
    def test_voice_setting_at_a_text_model_drops_with_a_warning(self, monkeypatch):
        sent: list = []
        monkeypatch.setattr(outbound_params, "send_client_warning", lambda p, **k: sent.append(p))
        assert _wire(_map(TEXT), tts_voice="kore", temperature=0.2) == {"temperature": 0.2}
        [warning] = sent
        assert "tts_voice" in warning.user_message
        # the same through the gate for a voice key on the canonical dict
        canonical = {"voice_settings": "warm"}
        gate: list = []
        drop_foreign_canonical_keys(canonical, _map(TEXT), adjustments=gate)
        assert canonical == {}
        [adj] = gate
        assert adj.action == "dropped" and adj.expected is False

    def test_voice_setting_without_family_data_stays_silent(self, monkeypatch):
        sent: list = []
        monkeypatch.setattr(outbound_params, "send_client_warning", lambda p, **k: sent.append(p))
        _wire(_map(TEXT, families=False), tts_voice="kore")
        assert sent == []

    def test_a_family_with_no_carried_member_is_an_unexpected_drop(self):
        canonical = {"stop_sequences": ["x"]}
        gate: list = []
        drop_foreign_canonical_keys(canonical, _map(IMAGE), adjustments=gate)
        assert canonical == {} and gate[0].expected is False


class TestSupportedFalseRedefinition:
    def test_supported_false_converts_instead_of_dropping(self):
        rules = {**TEXT, "thinking_level": {"supported": False}}
        params, adjustments = _gate(_map(rules), thinking_level="high")
        assert params["reasoning"] == {"effort": "high"}
        [conv] = [a for a in adjustments if a.converted_from == "thinking_level"]
        assert conv.key == "reasoning_effort"

    def test_declared_drop_stays_a_silent_drop(self):
        rules = {**TEXT, "thinking_level": {"drop": True, "why": "no levels here"}}
        params, adjustments = _gate(_map(rules), thinking_level="high")
        assert "reasoning" not in params
        [adj] = [a for a in adjustments if a.key == "thinking_level"]
        assert adj.action == "dropped" and adj.expected is True

    def test_supported_false_with_nothing_to_convert_into_warns(self):
        rules = {"temperature": {"supported": False}}
        canonical = {"temperature": 0.7}
        gate: list = []
        drop_foreign_canonical_keys(canonical, _map(rules), adjustments=gate)
        assert canonical == {} and gate[0].expected is False


class TestPrecedence:
    def test_a_key_set_directly_beats_any_conversion(self):
        params, adjustments = _gate(_map(IMAGE), reasoning_effort="max", render_quality="low")
        assert params == {"quality": "low"}
        drops = [a for a in adjustments if a.key == "reasoning_effort" and a.action == "dropped"]
        assert drops and all(a.expected for a in drops)

    def test_highest_position_source_wins(self):
        rules = {**IMAGE, "thinking_level": {"supported": False}}
        canonical = {"reasoning_effort": "low", "thinking_level": "high"}
        gate: list = []
        drop_foreign_canonical_keys(canonical, _map(rules), adjustments=gate)
        assert canonical["quality"] == "high"
        [winner] = [a for a in gate if a.converted_from]
        assert winner.converted_from == "thinking_level"
        [loser] = [a for a in gate if a.key == "reasoning_effort" and a.action == "dropped"]
        assert loser.expected is True

    def test_the_budget_bridge_competes_by_position(self):
        # budget 50,000 -> xhigh beats an explicit thinking_level=low (both foreign)
        rules = {**TEXT, "thinking_budget": {"supported": False}}
        assert _wire(_map(rules), thinking_budget=50000, thinking_level="low") == {
            "reasoning": {"effort": "xhigh"}
        }


class TestOffAndVisibility:
    def test_off_never_becomes_a_degree(self):
        params, adjustments = _gate(_map(IMAGE), disable_reasoning=True)
        assert params == {"quality": "auto"}
        drops = [a for a in adjustments if a.key == "reasoning_effort"]
        assert drops and all(a.action == "dropped" and a.expected for a in drops)

    def test_a_degree_never_becomes_an_off(self):
        rules = {"reasoning_summary": {"ui_values": ["auto", "never"]}}
        canonical = {"include_thoughts": True}
        gate: list = []
        drop_foreign_canonical_keys(canonical, _map(rules), adjustments=gate)
        assert "reasoning_summary" not in canonical
        assert gate[0].expected is False

    def test_include_thoughts_reaches_a_summary(self):
        rules = {"reasoning_summary": {"ui_values": ["auto", "concise", "detailed"]}}
        canonical = {"include_thoughts": True}
        drop_foreign_canonical_keys(canonical, _map(rules))
        assert canonical == {"reasoning_summary": "detailed"}


class TestFamiliesAbsent:
    def test_behaves_exactly_as_before_c6(self):
        controls = _map(IMAGE, families=False)
        canonical = {"reasoning_effort": "max", "voice_settings": "warm"}
        gate: list = []
        removed = drop_foreign_canonical_keys(canonical, controls, adjustments=gate)
        # supported:false stays for outbound; the undeclared key drops silently
        assert removed == ["voice_settings"]
        assert canonical == {"reasoning_effort": "max"}
        assert gate[0].expected is True and gate[0].provenance == "computed"
        params, adjustments = controls.outbound(canonical)
        assert params == {"quality": "auto"}

    def test_from_settings_is_none_without_family_data(self):
        assert SettingFamilies.from_settings(_settings(with_families=False)) is None


class TestPositions:
    @pytest.mark.parametrize(
        ("asked", "sent"), [("4k", "2K"), ("1024p", "1K"), ("0.5k", "1K"), ("1080p", "1K")]
    )
    def test_resolution_nearest_is_by_position_not_list_order(self, asked, sent):
        # list order put 4k beside 0.5k, so 4k used to reach 1k
        assert _wire(
            _map({"resolution": {"value_map": {"1k": "1K", "2k": "2K"}}}), resolution=asked
        ) == {"resolution": sent}

    def test_without_families_list_order_is_kept(self):
        controls = _map({"resolution": {"value_map": {"1k": "1K", "2k": "2K"}}}, families=False)
        assert controls.outbound({"resolution": "4k"})[0] == {"resolution": "1K"}


class TestDeclaredOutputCeiling:
    RULES = {"max_output_tokens": {"provider_key": "max_tokens", "clamp": {"max": 40960}}}

    def test_offering_cell_ceiling_wins_and_is_declared(self):
        controls = _map(
            self.RULES,
            output_maximum=131072,
            cells={"max_output_tokens": CellRef(cell_id="c1", layer="offering", state="agent")},
        )
        params, adjustments = controls.outbound({"max_output_tokens": 100000})
        assert params == {"max_tokens": 40960}
        [adj] = adjustments
        assert adj.provenance == "declared" and adj.cell_id == "c1"

    def test_model_maximum_is_the_computed_safety_net_without_a_cell(self):
        controls = _map({"max_output_tokens": {"provider_key": "max_tokens"}}, output_maximum=16384)
        params, adjustments = controls.outbound({"max_output_tokens": 32000})
        assert params == {"max_tokens": 16384}
        assert adjustments[0].provenance == "computed"


class TestRejectionProvenance:
    def test_budget_only_record_names_the_converted_effort(self):
        from matrx_ai.providers.setting_rejection import build_record

        rules = {**TEXT, "thinking_budget": {"supported": False}}
        controls = _map(rules)
        config = SimpleNamespace(model="gpt-x", thinking_budget=50000)
        resolve_outbound_params(config, controls)
        info = SimpleNamespace(
            details={
                "setting_rejection": {
                    "provider": "openai",
                    "provider_param": "reasoning.effort",
                    "shape": "unsupported_value",
                }
            },
            message="bad effort",
        )
        record = build_record(
            info,
            model="gpt-x",
            profile=SimpleNamespace(controls=controls, model_name="gpt-x"),
            config=config,
            wire_payload={"reasoning": {"effort": "xhigh"}},
        )
        assert record["canonical_key"] == "reasoning_effort"
        assert record["canonical_value"] == "xhigh"
        assert record["canonical_state"] == "value"
        assert record["converted_from"] == {"key": "thinking_budget", "value": 50000}
