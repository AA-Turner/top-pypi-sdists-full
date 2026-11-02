"""Tests for the ``verify_artifacts_command()`` CLI entry point."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.verify_artifacts import verify_artifacts_command

_SPEC = "# Feature\n\n- **FR-001**: Do a thing.\n"


def _spec_dir(tmp_path: Path) -> Path:
    spec_dir = tmp_path / "specs" / "001-x"
    spec_dir.mkdir(parents=True)
    return spec_dir


class TestVerifyArtifactsCommandExitCodes:
    """Exit codes: 0 pass, 1 violations, 2 operational error."""

    def test_exits_0_when_every_check_passes(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "spec.md").write_text(_SPEC, encoding="utf-8")

        with pytest.raises(SystemExit) as exc_info:
            verify_artifacts_command(["--spec-dir", str(spec_dir), "--repo-root", str(tmp_path)])

        assert exc_info.value.code == 0

    def test_exits_1_when_a_violation_is_found(self, tmp_path: Path) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "plan.md").write_text("Update `pkg/absent.py`.\n", encoding="utf-8")

        with pytest.raises(SystemExit) as exc_info:
            verify_artifacts_command(["--spec-dir", str(spec_dir), "--repo-root", str(tmp_path)])

        assert exc_info.value.code == 1

    def test_exits_2_when_the_spec_directory_is_missing(self, tmp_path: Path, capsys) -> None:
        with pytest.raises(SystemExit) as exc_info:
            verify_artifacts_command(["--spec-dir", str(tmp_path / "absent")])

        assert exc_info.value.code == 2
        assert "not found" in capsys.readouterr().err

    def test_exits_2_when_verification_raises(self, tmp_path: Path, capsys) -> None:
        spec_dir = _spec_dir(tmp_path)

        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.verify_artifacts",
            side_effect=RuntimeError("boom"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                verify_artifacts_command(["--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert "boom" in capsys.readouterr().err


class TestVerifyArtifactsCommandOutput:
    """Human-readable and JSON output modes."""

    def test_prints_a_human_readable_summary_by_default(self, tmp_path: Path, capsys) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "plan.md").write_text("Update `pkg/absent.py`.\n", encoding="utf-8")

        with pytest.raises(SystemExit):
            verify_artifacts_command(["--spec-dir", str(spec_dir), "--repo-root", str(tmp_path)])

        out = capsys.readouterr().out
        assert "## SpecKit Artifact Verification" in out
        assert "pkg/absent.py" in out

    def test_emits_json_when_requested(self, tmp_path: Path, capsys) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "plan.md").write_text("Update `pkg/absent.py`.\n", encoding="utf-8")

        with pytest.raises(SystemExit):
            verify_artifacts_command(["--spec-dir", str(spec_dir), "--repo-root", str(tmp_path), "--json"])

        payload = json.loads(capsys.readouterr().out)
        assert payload["passed"] is False
        assert payload["violations"][0]["check"] == "referenced-path"

    def test_phase_restricts_the_checks_that_run(self, tmp_path: Path, capsys) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "plan.md").write_text("Update `pkg/absent.py`.\n", encoding="utf-8")

        with pytest.raises(SystemExit) as exc_info:
            verify_artifacts_command(
                ["--spec-dir", str(spec_dir), "--phase", "1", "--repo-root", str(tmp_path), "--json"]
            )

        assert exc_info.value.code == 0
        assert json.loads(capsys.readouterr().out)["checks_run"] == []

    def test_repo_root_defaults_to_the_working_directory(self, tmp_path: Path, capsys) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "plan.md").write_text("Update `pkg/absent.py`.\n", encoding="utf-8")

        with pytest.raises(SystemExit):
            verify_artifacts_command(["--spec-dir", str(spec_dir), "--json"])

        assert json.loads(capsys.readouterr().out)["passed"] is False


class TestVerifyArtifactsCommandSpecContext:
    """--spec-context wires a parent spec to the FR and test-task checks."""

    def test_spec_context_enables_fr_violation_for_task_level(self, tmp_path: Path, capsys) -> None:
        spec_dir = _spec_dir(tmp_path)
        spec_context = tmp_path / "parent-spec.md"
        spec_context.write_text(_SPEC, encoding="utf-8")
        (spec_dir / "tasks.md").write_text("T001 covers FR-099.\n", encoding="utf-8")

        with pytest.raises(SystemExit) as exc_info:
            verify_artifacts_command(
                [
                    "--spec-dir",
                    str(spec_dir),
                    "--repo-root",
                    str(tmp_path),
                    "--spec-context",
                    str(spec_context),
                    "--json",
                ]
            )

        assert exc_info.value.code == 1
        payload = json.loads(capsys.readouterr().out)
        assert any("FR-099" in v["detail"] for v in payload["violations"])

    def test_exits_2_when_spec_context_file_is_missing(self, tmp_path: Path, capsys) -> None:
        spec_dir = _spec_dir(tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            verify_artifacts_command(
                [
                    "--spec-dir",
                    str(spec_dir),
                    "--spec-context",
                    str(tmp_path / "absent-spec.md"),
                ]
            )

        assert exc_info.value.code == 2
        assert "not found" in capsys.readouterr().err

    def test_exits_2_when_tasks_exist_without_spec_or_spec_context(self, tmp_path: Path, capsys) -> None:
        spec_dir = _spec_dir(tmp_path)
        (spec_dir / "tasks.md").write_text("- [ ] T001 Add unit test for FR-001.\n", encoding="utf-8")

        with pytest.raises(SystemExit) as exc_info:
            verify_artifacts_command(["--spec-dir", str(spec_dir), "--phase", "4"])

        assert exc_info.value.code == 2
        assert "no specification context is available" in capsys.readouterr().err
