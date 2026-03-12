from __future__ import annotations

import pytest

from plato.cli.chronos.test.config import TestPhaseConfig
from plato.cli.chronos.test.runner import select_test_phases


@pytest.fixture
def phases() -> list[TestPhaseConfig]:
    return [
        TestPhaseConfig(name="unit", command="pytest tests/unit"),
        TestPhaseConfig(name="integration", command="pytest tests/integration"),
    ]


def test_select_all(phases: list[TestPhaseConfig]) -> None:
    selected = select_test_phases(phases, "all")
    assert [p.name for p in selected] == ["unit", "integration"]


def test_select_single_phase(phases: list[TestPhaseConfig]) -> None:
    selected = select_test_phases(phases, "unit")
    assert [p.name for p in selected] == ["unit"]


def test_select_missing_phase_raises(phases: list[TestPhaseConfig]) -> None:
    with pytest.raises(ValueError, match="No phase named"):
        select_test_phases(phases, "smoke")


def test_select_custom_phase_name() -> None:
    """Custom phase names (not just unit/integration) are selectable."""
    custom_phases = [
        TestPhaseConfig(name="smoke", command="pytest tests/smoke"),
        TestPhaseConfig(name="e2e", command="pytest tests/e2e"),
    ]
    selected = select_test_phases(custom_phases, "smoke")
    assert [p.name for p in selected] == ["smoke"]

    selected_all = select_test_phases(custom_phases, "all")
    assert [p.name for p in selected_all] == ["smoke", "e2e"]
