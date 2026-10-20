"""A Gemini 3.x model id is never in the legacy (thinking_budget) mode (lane L4d, 2026-10-18).

Found by the L4c probe: ``gemini-flash-lite-latest`` answers as ``gemini-3.5-flash-lite`` but the
catalog ran it in ``legacy`` mode. The catalog must match the truth, so the pinned cells of the
PB-03 offerings (and the sibling table below) are checked against the id's real generation.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.catalog.gemini_mode_truth import (
    GEMINI_ALIAS_RESOLUTION,
    is_gemini_3x_or_newer,
    mode_mismatch,
)

FIXTURE = Path(__file__).parent / "fixtures" / "pb03_offering_rules.json"


def test_alias_resolves_to_a_3x_model():
    assert is_gemini_3x_or_newer("gemini-flash-lite-latest")
    assert not is_gemini_3x_or_newer("gemini-2.5-flash")
    assert not is_gemini_3x_or_newer("gemini-3.1-flash-tts-preview")


def test_mode_mismatch_names_the_problem():
    assert mode_mismatch("gemini-3.5-flash", "legacy")
    assert mode_mismatch("gemini-3.5-flash", "gemini_3") is None
    assert mode_mismatch("gemini-2.5-pro", "legacy") is None


def test_pinned_gemini_offering_matches_its_real_generation():
    rules = json.loads(FIXTURE.read_text())["google_gemini_flash_lite_latest"]["rules"]
    mode = (rules["reasoning_effort"].get("processor_config") or {}).get("mode")
    assert mode_mismatch("gemini-flash-lite-latest", mode) is None, mode_mismatch("gemini-flash-lite-latest", mode)


@pytest.mark.parametrize("alias", sorted(GEMINI_ALIAS_RESOLUTION))
def test_every_alias_is_pinned_to_a_real_id(alias):
    assert GEMINI_ALIAS_RESOLUTION[alias].startswith("gemini-")
