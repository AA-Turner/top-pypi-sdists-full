"""Behavioral tests for merged phase-3 (plan + tasks + analyze) idempotency checks."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "check-idempotency.sh"
BASH_PATH = shutil.which("bash")
HAS_BASH = BASH_PATH is not None


def _run_phase3_check(specs_dir: Path, output_path: Path, level: str = "feature") -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["SPEC_BASE_PATH"] = str(specs_dir)
    env["GITHUB_OUTPUT"] = str(output_path)
    return subprocess.run(  # noqa: S603
        [BASH_PATH or "bash", str(SCRIPT_PATH), "1234", "--phase", "3", "--level", level],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )


@pytest.mark.skipif(not HAS_BASH, reason="bash is required for phase-3 idempotency shell tests")
class TestCheckIdempotencyPhase3:
    """Validate legacy-diagnostic migration during phase-3 idempotency checks."""

    def test_migrates_all_legacy_diagnostics_when_canonical_report_already_exists(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        spec_dir = specs_dir / "1234-feature"
        generated_dir = spec_dir / "generated"
        generated_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (spec_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
        (generated_dir / "analysis-report.md").write_text("current-report", encoding="utf-8")
        (spec_dir / "analysis-report.md").write_text("stale-report", encoding="utf-8")
        (spec_dir / "fr-coverage.json").write_text('{"legacy": true}\n', encoding="utf-8")
        (spec_dir / "test-coverage.json").write_text('{"legacy": true}\n', encoding="utf-8")
        output_path = tmp_path / "github-output.txt"

        result = _run_phase3_check(specs_dir, output_path)

        assert "Phase 3 artifact already exists" in result.stdout
        assert not (spec_dir / "analysis-report.md").exists()
        assert not (spec_dir / "fr-coverage.json").exists()
        assert not (spec_dir / "test-coverage.json").exists()
        assert (generated_dir / "analysis-report.md").read_text(encoding="utf-8") == "current-report"
        assert (generated_dir / "fr-coverage.json").read_text(encoding="utf-8") == '{"legacy": true}\n'
        assert (generated_dir / "test-coverage.json").read_text(encoding="utf-8") == '{"legacy": true}\n'
        assert output_path.read_text(encoding="utf-8").splitlines() == [
            "migration_done=true",
            "skipped=true",
            f"existing_spec={generated_dir / 'analysis-report.md'}",
            f"spec_dir={spec_dir}",
        ]

    def test_does_not_skip_when_only_the_plan_artifact_exists(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        spec_dir = specs_dir / "1234-feature"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (spec_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
        output_path = tmp_path / "github-output.txt"

        result = _run_phase3_check(specs_dir, output_path)

        assert "Phase 3 artifacts not found" in result.stdout
        assert output_path.read_text(encoding="utf-8").splitlines() == ["skipped=false"]

    def test_feature_level_errors_when_analysis_report_exists_without_tasks(self, tmp_path: Path) -> None:
        """Feature: analysis-report.md without tasks.md is an inconsistent state → exit 1."""
        specs_dir = tmp_path / "specs"
        spec_dir = specs_dir / "1234-feature"
        generated_dir = spec_dir / "generated"
        generated_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (spec_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
        (generated_dir / "analysis-report.md").write_text("report", encoding="utf-8")
        # tasks.md deliberately absent
        output_path = tmp_path / "github-output.txt"

        result = subprocess.run(  # noqa: S603
            [BASH_PATH or "bash", str(SCRIPT_PATH), "1234", "--phase", "3", "--level", "feature"],
            capture_output=True,
            text=True,
            env={**os.environ, "SPEC_BASE_PATH": str(specs_dir), "GITHUB_OUTPUT": str(output_path)},
        )

        assert result.returncode == 1
        assert "Missing: " in result.stderr
        assert "tasks.md" in result.stderr

    def test_epic_level_errors_when_analysis_report_exists_without_plan(self, tmp_path: Path) -> None:
        """Epic: analysis-report.md without plan.md is an inconsistent state → exit 1."""
        specs_dir = tmp_path / "specs"
        spec_dir = specs_dir / "1234-epic"
        generated_dir = spec_dir / "generated"
        generated_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (generated_dir / "analysis-report.md").write_text("report", encoding="utf-8")
        # plan.md deliberately absent
        output_path = tmp_path / "github-output.txt"

        result = subprocess.run(  # noqa: S603
            [BASH_PATH or "bash", str(SCRIPT_PATH), "1234", "--phase", "3", "--level", "epic"],
            capture_output=True,
            text=True,
            env={**os.environ, "SPEC_BASE_PATH": str(specs_dir), "GITHUB_OUTPUT": str(output_path)},
        )

        assert result.returncode == 1
        assert "Missing: " in result.stderr
        assert "plan.md" in result.stderr

    def test_epic_level_skips_when_analysis_report_exists_with_plan(self, tmp_path: Path) -> None:
        """Epic: analysis-report.md plus plan.md is complete and should short-circuit."""
        specs_dir = tmp_path / "specs"
        spec_dir = specs_dir / "1234-epic"
        generated_dir = spec_dir / "generated"
        generated_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (spec_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
        (generated_dir / "analysis-report.md").write_text("report", encoding="utf-8")
        output_path = tmp_path / "github-output.txt"

        result = _run_phase3_check(specs_dir, output_path, level="epic")

        assert "Phase 3 artifact already exists" in result.stdout
        assert output_path.read_text(encoding="utf-8").splitlines() == [
            "migration_done=false",
            "skipped=true",
            f"existing_spec={generated_dir / 'analysis-report.md'}",
            f"spec_dir={spec_dir}",
        ]

    def test_task_level_skips_once_the_tasks_artifact_exists(self, tmp_path: Path) -> None:
        specs_dir = tmp_path / "specs"
        spec_dir = specs_dir / "1234-task"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
        output_path = tmp_path / "github-output.txt"

        result = _run_phase3_check(specs_dir, output_path, level="task")

        assert "Phase 3 artifact already exists" in result.stdout
        assert output_path.read_text(encoding="utf-8").splitlines() == [
            "migration_done=false",
            "skipped=true",
            f"existing_spec={spec_dir / 'tasks.md'}",
            f"spec_dir={spec_dir}",
        ]

    def test_task_level_skips_for_nested_numeric_path(self, tmp_path: Path) -> None:
        """Nested task dirs (specs/{epic}/{feature}/{task}) have no spec.md but must still be found."""
        specs_dir = tmp_path / "specs"
        # Simulate the nested numeric layout used by the hierarchy path resolver
        task_dir = specs_dir / "10" / "42" / "1234"
        task_dir.mkdir(parents=True)
        (task_dir / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
        output_path = tmp_path / "github-output.txt"

        result = _run_phase3_check(specs_dir, output_path, level="task")

        assert "Phase 3 artifact already exists" in result.stdout
        assert output_path.read_text(encoding="utf-8").splitlines() == [
            "migration_done=false",
            "skipped=true",
            f"existing_spec={task_dir / 'tasks.md'}",
            f"spec_dir={task_dir}",
        ]

    def test_task_level_does_not_skip_for_nested_numeric_path_without_tasks(self, tmp_path: Path) -> None:
        """Nested task dir exists but tasks.md is absent — must not skip (partial run)."""
        specs_dir = tmp_path / "specs"
        task_dir = specs_dir / "10" / "42" / "1234"
        task_dir.mkdir(parents=True)
        # No tasks.md — phase 3 has not completed yet
        output_path = tmp_path / "github-output.txt"

        result = _run_phase3_check(specs_dir, output_path, level="task")

        assert "Phase 3 artifacts not found" in result.stdout
        assert output_path.read_text(encoding="utf-8").splitlines() == ["skipped=false"]

    def test_unknown_level_skips_with_complete_feature_artifact_set(self, tmp_path: Path) -> None:
        """'unknown' is remapped to 'feature' for artifact detection; a complete feature set must skip."""
        specs_dir = tmp_path / "specs"
        spec_dir = specs_dir / "1234-unknown"
        generated_dir = spec_dir / "generated"
        generated_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (spec_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
        (generated_dir / "analysis-report.md").write_text("report", encoding="utf-8")
        output_path = tmp_path / "github-output.txt"

        result = _run_phase3_check(specs_dir, output_path, level="unknown")

        assert "Phase 3 artifact already exists" in result.stdout
        assert output_path.read_text(encoding="utf-8").splitlines() == [
            "migration_done=false",
            "skipped=true",
            f"existing_spec={generated_dir / 'analysis-report.md'}",
            f"spec_dir={spec_dir}",
        ]

    def test_unknown_level_does_not_skip_for_incomplete_artifact_set(self, tmp_path: Path) -> None:
        """'unknown' remapped to 'feature': an incomplete artifact set (no tasks.md) must not skip."""
        specs_dir = tmp_path / "specs"
        spec_dir = specs_dir / "1234-unknown"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (spec_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
        # tasks.md intentionally absent — phase 3 has not completed
        output_path = tmp_path / "github-output.txt"

        result = _run_phase3_check(specs_dir, output_path, level="unknown")

        assert "Phase 3 artifacts not found" in result.stdout
        assert output_path.read_text(encoding="utf-8").splitlines() == ["skipped=false"]

    def test_task_level_errors_for_ambiguous_nested_numeric_paths(self, tmp_path: Path) -> None:
        """Multiple nested dirs with the same issue number must be rejected to avoid non-deterministic selection."""
        specs_dir = tmp_path / "specs"
        task_dir_a = specs_dir / "10" / "42" / "1234"
        task_dir_b = specs_dir / "11" / "99" / "1234"
        task_dir_a.mkdir(parents=True)
        task_dir_b.mkdir(parents=True)
        output_path = tmp_path / "github-output.txt"

        result = subprocess.run(  # noqa: S603
            [BASH_PATH or "bash", str(SCRIPT_PATH), "1234", "--phase", "3", "--level", "task"],
            capture_output=True,
            text=True,
            env={**os.environ, "SPEC_BASE_PATH": str(specs_dir), "GITHUB_OUTPUT": str(output_path)},
        )

        assert result.returncode == 1
        assert "Found multiple nested spec directories" in result.stderr
