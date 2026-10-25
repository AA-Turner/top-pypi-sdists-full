"""Gemini thinking models hide their thoughts unless asked, so a thinking run
streamed NOTHING for up to 70s (live 2026-10-07, brand.voice_rewrite: first
content at 29-37s; with reasoning_summary "always", thought summaries from 6.4s).
A google_thinking cell declares ``processor_config.default_include_thoughts`` —
the same cell-declared NOT-SET default ``together_reasoning`` uses for
``default_effort`` — and an explicit caller choice always wins over it."""

from __future__ import annotations

import pytest

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule

CONSUMES = ["thinking_budget", "thinking_level", "include_thoughts", "reasoning_summary"]


def _wire(config: dict, canonical: dict) -> dict:
    rule = ControlRule.model_validate(
        {"processor": "google_thinking", "processor_config": {"consumes": CONSUMES, **config}}
    )
    params, _ = CompiledControlsMap(rules={"reasoning_effort": rule}).outbound(canonical)
    return params


MODES = [{"mode": "gemini_3", "family": "pro"}, {"mode": "legacy"}]


@pytest.mark.parametrize("mode", MODES)
def test_unset_canonical_takes_the_cell_default(mode: dict) -> None:
    wire = _wire({**mode, "default_include_thoughts": True}, {})
    assert wire["thinking_config"]["include_thoughts"] is True


@pytest.mark.parametrize("mode", MODES)
def test_explicit_false_wins_over_the_cell_default(mode: dict) -> None:
    wire = _wire({**mode, "default_include_thoughts": True}, {"include_thoughts": False})
    assert wire["thinking_config"]["include_thoughts"] is False


def test_reasoning_summary_never_wins_over_the_cell_default() -> None:
    wire = _wire({"mode": "gemini_3", "family": "pro", "default_include_thoughts": True}, {"reasoning_summary": "never"})
    assert wire["thinking_config"]["include_thoughts"] is False


@pytest.mark.parametrize("mode", MODES)
def test_no_cell_default_sends_nothing(mode: dict) -> None:
    wire = _wire(mode, {})
    assert "include_thoughts" not in (wire.get("thinking_config") or {})
