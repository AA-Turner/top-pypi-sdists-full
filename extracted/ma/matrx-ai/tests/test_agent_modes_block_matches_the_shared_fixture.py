"""C5: the ``<agent_modes>`` text the model receives equals the shared fixture other renderers (the builder's preview)
are checked against, case by case. The fixture is required: a missing file fails, never skips."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.config.agent_modes import normalize_modes, render_block

FIXTURE = Path(__file__).parent / "fixtures" / "agent_modes_block.json"


def _cases() -> list[dict]:
    if not FIXTURE.is_file():
        raise AssertionError(f"The shared fixture {FIXTURE} is missing; the C5 renderers are checked against it.")
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["name"])
def test_the_agent_modes_block_equals_the_fixture(case: dict) -> None:
    got = render_block(normalize_modes(case["modes"]), case["agent_mode"], case.get("person_set"))
    assert (got or "") == case["text"]


@pytest.mark.parametrize("case", [c for c in _cases() if c["text"]], ids=lambda c: c["name"])
def test_the_current_mode_and_its_instructions_are_always_there(case: dict) -> None:
    """D17: the person-set line is ADDITIONAL; ``Current mode:`` and the current mode's instructions never go."""
    from matrx_ai.config.agent_modes import current_mode

    modes = normalize_modes(case["modes"])
    current = current_mode(modes, case["agent_mode"])
    assert f"Current mode: {current['name']}." in case["text"]
    if current["instructions"]:
        assert current["instructions"] in case["text"]
