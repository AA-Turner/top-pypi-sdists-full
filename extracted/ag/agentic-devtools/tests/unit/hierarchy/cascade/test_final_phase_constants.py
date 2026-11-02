"""Tests for FINAL_PHASE_BY_LEVEL constant values and structure (FR-001)."""

from agentic_devtools.hierarchy.cascade import FINAL_PHASE_BY_LEVEL


class TestFinalPhaseConstants:
    """Tests that FINAL_PHASE_BY_LEVEL is correctly defined."""

    def test_epic_final_phase_is_3(self) -> None:
        assert FINAL_PHASE_BY_LEVEL["epic"] == 3

    def test_feature_final_phase_is_3(self) -> None:
        assert FINAL_PHASE_BY_LEVEL["feature"] == 3

    def test_task_final_phase_is_3(self) -> None:
        assert FINAL_PHASE_BY_LEVEL["task"] == 3

    def test_all_levels_present(self) -> None:
        assert set(FINAL_PHASE_BY_LEVEL.keys()) == {"epic", "feature", "task"}

    def test_all_values_are_positive_integers(self) -> None:
        for level, phase in FINAL_PHASE_BY_LEVEL.items():
            assert isinstance(phase, int), f"{level} phase is not an int"
            assert phase > 0, f"{level} phase is not positive"
