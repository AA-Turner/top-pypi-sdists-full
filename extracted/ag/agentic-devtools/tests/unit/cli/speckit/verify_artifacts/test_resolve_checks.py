"""Tests for ``resolve_checks()``."""

from agentic_devtools.cli.speckit.verify_artifacts import (
    ALL_CHECKS,
    CHECK_ADVERTISED_ARTIFACT,
    CHECK_CHECKLIST,
    CHECK_FR_REFERENCE,
    CHECK_REFERENCED_PATH,
    CHECK_UNMAPPED_TEST_TASK,
    resolve_checks,
)


class TestResolveChecks:
    """Mapping a pipeline phase to the checks it can satisfy."""

    def test_none_enables_every_check(self) -> None:
        assert resolve_checks(None) == list(ALL_CHECKS)

    def test_specify_phase_enables_no_checks(self) -> None:
        assert resolve_checks(1) == []

    def test_checklist_phase_enables_checklist_check(self) -> None:
        assert resolve_checks(2) == [CHECK_CHECKLIST]

    def test_plan_phase_enables_plan_scoped_checks(self) -> None:
        assert resolve_checks(3) == [CHECK_REFERENCED_PATH, CHECK_ADVERTISED_ARTIFACT]

    def test_tasks_phase_enables_task_scoped_checks(self) -> None:
        assert resolve_checks(4) == [
            CHECK_REFERENCED_PATH,
            CHECK_UNMAPPED_TEST_TASK,
            CHECK_FR_REFERENCE,
        ]

    def test_analyze_phase_enables_no_checks(self) -> None:
        assert resolve_checks(5) == []

    def test_unknown_phase_fails_closed_with_every_check(self) -> None:
        assert resolve_checks(99) == list(ALL_CHECKS)

    def test_returns_a_fresh_list_each_call(self) -> None:
        first = resolve_checks(4)
        first.append("mutated")

        assert "mutated" not in resolve_checks(4)
