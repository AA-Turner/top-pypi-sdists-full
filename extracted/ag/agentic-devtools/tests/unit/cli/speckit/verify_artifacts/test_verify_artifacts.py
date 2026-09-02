"""Tests for the ``verify_artifacts()`` orchestrator."""

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.verify_artifacts import (
    ALL_CHECKS,
    CHECK_ADVERTISED_ARTIFACT,
    CHECK_REFERENCED_PATH,
    CHECK_UNMAPPED_TEST_TASK,
    verify_artifacts,
)

_SPEC = "# Feature\n\n- **FR-001**: Do a thing.\n"


def _spec_dir(tmp_path: Path) -> Path:
    spec_dir = tmp_path / "specs" / "001-x"
    spec_dir.mkdir(parents=True)
    return spec_dir


class TestVerifyArtifactsResult:
    """Overall pass/fail behaviour."""

    def test_passes_on_a_clean_spec_directory(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "spec.md").write_text(_SPEC, encoding="utf-8")
        (spec_dir / "plan.md").write_text("Implement the thing.\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("- [ ] T001 Implement FR-001.\n", encoding="utf-8")

        result = verify_artifacts(spec_dir, tmp_path)

        assert result.passed is True
        assert result.violations == []

    def test_passes_on_an_empty_directory(self, tmp_path: Path) -> None:
        assert verify_artifacts(_spec_dir(tmp_path), tmp_path).passed is True

    def test_fails_and_aggregates_violations_across_checks(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "spec.md").write_text(_SPEC, encoding="utf-8")
        (spec_dir / "plan.md").write_text("See `research.md`.\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("- [ ] T001 Update `pkg/absent.py`.\n", encoding="utf-8")

        result = verify_artifacts(spec_dir, tmp_path)

        assert result.passed is False
        assert {v.check for v in result.violations} == {
            CHECK_REFERENCED_PATH,
            CHECK_ADVERTISED_ARTIFACT,
        }


class TestVerifyArtifactsChecksRun:
    """Which checks execute for a given phase."""

    def test_runs_every_check_when_phase_is_omitted(self, tmp_path: Path) -> None:
        result = verify_artifacts(_spec_dir(tmp_path), tmp_path)

        assert result.checks_run == list(ALL_CHECKS)

    def test_runs_no_check_for_the_specify_phase(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "plan.md").write_text("See `research.md`.\n", encoding="utf-8")

        result = verify_artifacts(spec_dir, tmp_path, phase=1)

        assert result.checks_run == []
        assert result.passed is True

    def test_plan_phase_scans_only_the_plan(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "plan.md").write_text("Update `pkg/plan_only.py`.\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("Update `pkg/tasks_only.py`.\n", encoding="utf-8")

        result = verify_artifacts(spec_dir, tmp_path, phase=3)

        assert {v.artifact for v in result.violations} == {"plan.md"}

    def test_plan_phase_does_not_require_future_phase_artifacts(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "plan.md").write_text(
            "Phase 4 will produce `tasks.md`, then phase 5 will produce `analysis-report.md`.\n",
            encoding="utf-8",
        )

        result = verify_artifacts(spec_dir, tmp_path, phase=3)

        assert all(v.check != CHECK_ADVERTISED_ARTIFACT for v in result.violations)

    def test_plan_phase_does_not_require_future_phase_generated_diagnostics(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "plan.md").write_text(
            "Phase 4 diagnostics live at `generated/fr-coverage.json` and "
            "`generated/test-coverage.json`, and phase 5 publishes "
            "`generated/analysis-report.md`.\n",
            encoding="utf-8",
        )

        result = verify_artifacts(spec_dir, tmp_path, phase=3)

        assert all(v.check != CHECK_ADVERTISED_ARTIFACT for v in result.violations)

    def test_tasks_phase_scans_only_the_tasks(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "spec.md").write_text(_SPEC, encoding="utf-8")
        (spec_dir / "plan.md").write_text("Update `pkg/plan_only.py`.\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("Update `pkg/tasks_only.py`.\n", encoding="utf-8")

        result = verify_artifacts(spec_dir, tmp_path, phase=4)

        assert {v.artifact for v in result.violations} == {"tasks.md"}

    def test_tasks_phase_includes_the_unmapped_test_task_check(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)

        result = verify_artifacts(spec_dir, tmp_path, phase=4)

        assert CHECK_UNMAPPED_TEST_TASK in result.checks_run

    def test_unknown_phase_scans_both_artifacts(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "spec.md").write_text(_SPEC, encoding="utf-8")
        (spec_dir / "plan.md").write_text("Update `pkg/plan_only.py`.\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("Update `pkg/tasks_only.py`.\n", encoding="utf-8")

        result = verify_artifacts(spec_dir, tmp_path, phase=99)

        assert {v.artifact for v in result.violations} == {"plan.md", "tasks.md"}


class TestVerifyArtifactsSpecContext:
    """spec_context supplies a parent spec.md for task-level hierarchy."""

    def test_spec_context_enables_fr_check_when_no_local_spec_md(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        spec_context = tmp_path / "parent-spec.md"
        spec_context.write_text(_SPEC, encoding="utf-8")
        (spec_dir / "tasks.md").write_text("T001 covers FR-099.\n", encoding="utf-8")

        result = verify_artifacts(spec_dir, tmp_path, spec_context=spec_context)

        assert result.passed is False
        assert any("FR-099" in v.detail for v in result.violations)

    def test_spec_context_passes_when_fr_is_defined_in_parent(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        spec_context = tmp_path / "parent-spec.md"
        spec_context.write_text(_SPEC, encoding="utf-8")
        # Use a plain prose task (no file path reference) to isolate the FR check.
        (spec_dir / "tasks.md").write_text(
            "- [ ] T001 Implement the widget described in FR-001.\n",
            encoding="utf-8",
        )

        result = verify_artifacts(spec_dir, tmp_path, spec_context=spec_context)

        assert result.passed is True

    def test_raises_when_tasks_exist_without_spec_or_spec_context(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "tasks.md").write_text("- [ ] T001 Add unit test for FR-001.\n", encoding="utf-8")

        with pytest.raises(ValueError, match="no specification context is available"):
            verify_artifacts(spec_dir, tmp_path, phase=4)

    def test_does_not_raise_when_spec_dependent_checks_are_disabled(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "tasks.md").write_text("- [ ] T001 Add unit test for FR-001.\n", encoding="utf-8")

        result = verify_artifacts(spec_dir, tmp_path, phase=3)

        assert result.checks_run == [CHECK_REFERENCED_PATH, CHECK_ADVERTISED_ARTIFACT]

    def test_raises_with_specific_error_when_spec_context_path_is_missing(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "tasks.md").write_text("- [ ] T001 Add unit test for FR-001.\n", encoding="utf-8")
        missing_spec_context = tmp_path / "missing-parent-spec.md"

        with pytest.raises(ValueError, match="provided spec-context path does not exist"):
            verify_artifacts(spec_dir, tmp_path, phase=4, spec_context=missing_spec_context)
