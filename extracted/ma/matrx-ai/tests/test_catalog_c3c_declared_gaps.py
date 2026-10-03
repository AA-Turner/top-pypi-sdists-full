"""Settings-translation item C3c — every capability gap is DECLARED data; a
warning means a genuine surprise; a posture that means "not set" is never a
surprise (the chair's ruling). Pure units — no DB.

Law (configuration-equivalence FEATURE, "The client's half of the law"): a
conversion is silent; a DECLARED capability gap is silent; only an UNEXPECTED
drop warns.
"""

from __future__ import annotations

from test_catalog_family_conversion_c6 import FAMILIES, IMAGE, SETTINGS, TEXT, _map

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.families import declared_value_drop
from matrx_ai.catalog.models import ControlRule
from matrx_ai.providers.outbound_params import drop_foreign_canonical_keys


def _run(controls: CompiledControlsMap, canonical: dict) -> tuple[dict, list]:
    canonical = dict(canonical)
    gate: list = []
    drop_foreign_canonical_keys(canonical, controls, adjustments=gate)
    params, adjustments = controls.outbound(canonical)
    return params, gate + adjustments


def _warnings(adjustments: list) -> list:
    return [a for a in adjustments if a.action == "dropped" and a.expected is False]


# ── 1. "auto" means unset ────────────────────────────────────────────────────
def test_auto_on_a_key_the_target_does_not_carry_is_unset_not_a_drop() -> None:
    # quality=auto at a TEXT model (no quality rule): before C3c an unexpected
    # drop ("no sibling can express 'auto'") — the client was warned.
    params, adjustments = _run(_map(TEXT), {"quality": "auto", "reasoning_effort": "high"})
    assert params == {"reasoning": {"effort": "high"}}
    assert not [a for a in adjustments if a.key == "quality"]


def test_auto_on_a_supported_false_key_is_unset_not_a_drop() -> None:
    params, adjustments = _run(_map(IMAGE), {"reasoning_effort": "auto"})
    assert "reasoning_effort" not in params
    assert not [a for a in adjustments if a.action == "dropped"]


def test_auto_on_a_declared_drop_is_unset_not_a_drop() -> None:
    rules = {**TEXT, "quality": {"drop": True, "why": "no image quality on a text model"}}
    _, adjustments = _run(_map(rules), {"quality": "auto"})
    assert not [a for a in adjustments if a.key == "quality"]


def test_auto_on_a_carried_rule_that_cannot_send_it_is_unset() -> None:
    # value_map without "auto" and on_unmapped=drop: before C3c an UNEXPECTED drop.
    rules = {
        "quality": {
            "value_map": {"low": "low", "high": "high"},
            "on_unmapped": "drop",
            "default": "high",
        }
    }
    params, adjustments = _run(_map(rules), {"quality": "auto"})
    assert params == {"quality": "high"}  # the default, exactly as for an absent key
    assert not [a for a in adjustments if a.action == "dropped"]


def test_auto_a_rule_speaks_still_goes_on_the_wire() -> None:
    params, _ = _run(_map(IMAGE), {"quality": "auto"})
    assert params == {"quality": "auto"}  # IMAGE maps auto -> auto: untouched


def test_auto_without_families_is_unchanged() -> None:
    rules = {"quality": {"value_map": {"low": "low"}, "on_unmapped": "drop"}}
    _, adjustments = _run(_map(rules, families=False), {"quality": "auto"})
    assert _warnings(adjustments)  # pre-C6 catalogs (live today): behaviour unchanged


# ── 2. a declared drop is never native ───────────────────────────────────────
def test_a_declared_drop_reads_as_unsupported_everywhere() -> None:
    rule = ControlRule.model_validate({"drop": True, "why": "tts-1 has no instructions field"})
    assert rule.supported is False  # speech compiler / translators read .supported
    # and the field stays unset, so a cell dump never grows a key it did not have
    assert "supported" not in rule.model_dump(exclude_unset=True)


# ── 3. per-value declared drops ──────────────────────────────────────────────
def test_a_value_map_null_on_a_non_native_key_is_a_declared_silent_drop() -> None:
    # reasoning_summary is not native on IMAGE; its sibling include_thoughts is
    # absent too -> without a declaration every value WARNS.
    bare = {**IMAGE, "reasoning_summary": {"supported": False}}
    _, adjustments = _run(_map(bare), {"reasoning_summary": "detailed"})
    assert _warnings(adjustments)
    declared = {
        **IMAGE,
        "reasoning_summary": {
            "supported": False,
            "value_map": {"detailed": None},
            "why": "no reasoning shown here",
        },
    }
    params, adjustments = _run(_map(declared), {"reasoning_summary": "detailed"})
    assert not _warnings(adjustments)
    dropped = [a for a in adjustments if a.key == "reasoning_summary" and a.action == "dropped"]
    assert dropped and dropped[0].provenance == "declared" and dropped[0].expected is True
    assert "reasoning_summary" not in params


def test_a_from_number_null_step_declares_a_number_drop() -> None:
    controls = _map(
        {
            "temperature": {},
            "top_p": {"supported": False, "from_number": [{"lte": None, "to": None}], "why": "x"},
        }
    )
    assert declared_value_drop(controls, "top_p", 0.5) == "x"
    assert declared_value_drop(controls, "top_p", "0.5") is None


def test_a_declared_value_never_stops_a_conversion() -> None:
    # reasoning_effort=max still converts into the image's top quality even
    # when another value of the same key is declared dropped.
    rules = {
        **IMAGE,
        "reasoning_effort": {"supported": False, "value_map": {"minimal": None}, "why": "x"},
    }
    params, adjustments = _run(_map(rules), {"reasoning_effort": "max"})
    assert params.get("quality") == "high"
    assert not _warnings(adjustments)


def test_fixture_families_loaded() -> None:
    assert FAMILIES is not None and "reasoning_effort" in SETTINGS
