"""Tests for ``scaffold_check_prereqs_command``."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_check_prereqs import scaffold_check_prereqs_command
from agentic_devtools.cli.speckit.scaffold_common import ActiveFeature, FeatureResolutionError


def _active(tmp_path: Path) -> ActiveFeature:
    return ActiveFeature(
        repo_root=tmp_path,
        feature_dir=tmp_path / "specs" / "042-x",
        branch="042-x",
        has_git=True,
    )


class TestScaffoldCheckPrereqsCommand:
    """scaffold_check_prereqs_command wires CLI flags to check_prerequisites."""

    def test_json_output(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        (active.feature_dir / "spec.md").write_text("spec", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.scaffold_check_prereqs.resolve_active_feature", return_value=active):
            scaffold_check_prereqs_command(["--json"])

        payload = json.loads(capsys.readouterr().out)
        assert payload == {
            "FEATURE_DIR": str(active.feature_dir),
            "AVAILABLE_DOCS": ["spec.md"],
        }

    def test_text_output(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        (active.feature_dir / "spec.md").write_text("spec", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.scaffold_check_prereqs.resolve_active_feature", return_value=active):
            scaffold_check_prereqs_command([])

        out = capsys.readouterr().out
        assert f"FEATURE_DIR:{active.feature_dir}" in out
        assert "AVAILABLE_DOCS:" in out
        assert "spec.md" in out

    def test_require_tasks_flag_missing_exits_1(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.scaffold_check_prereqs.resolve_active_feature", return_value=active):
            with pytest.raises(SystemExit) as exc_info:
                scaffold_check_prereqs_command(["--require-tasks"])

        assert exc_info.value.code == 1
        assert "ERROR:" in capsys.readouterr().err

    def test_include_tasks_flag_adds_tasks_md(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        (active.feature_dir / "tasks.md").write_text("tasks", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.scaffold_check_prereqs.resolve_active_feature", return_value=active):
            scaffold_check_prereqs_command(["--json", "--include-tasks"])

        payload = json.loads(capsys.readouterr().out)
        assert "tasks.md" in payload["AVAILABLE_DOCS"]

    def test_unknown_flag_exits_2(self, tmp_path: Path) -> None:
        with pytest.raises(SystemExit) as exc_info:
            scaffold_check_prereqs_command(["--not-a-flag"])

        assert exc_info.value.code == 2

    def test_paths_only_json_skips_plan_validation(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        with patch("agentic_devtools.cli.speckit.scaffold_check_prereqs.resolve_active_feature", return_value=active):
            scaffold_check_prereqs_command(["--json", "--paths-only"])

        payload = json.loads(capsys.readouterr().out)
        assert payload == {
            "FEATURE_DIR": str(active.feature_dir),
            "AVAILABLE_DOCS": [],
        }
        assert Path(payload["FEATURE_DIR"]).is_absolute()

    def test_feature_resolution_error_exits_1(self, capsys) -> None:
        with (
            patch(
                "agentic_devtools.cli.speckit.scaffold_check_prereqs.resolve_active_feature",
                side_effect=FeatureResolutionError("ambiguous feature prefix"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            scaffold_check_prereqs_command(["--json"])

        assert exc_info.value.code == 1
        assert "ERROR: ambiguous feature prefix" in capsys.readouterr().err

    def test_paths_only_conflicts_with_tasks_flags_exit_2(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            scaffold_check_prereqs_command(["--paths-only", "--require-tasks"])

        assert exc_info.value.code == 2

    def test_symlink_validation_error_exits_1(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        with (
            patch("agentic_devtools.cli.speckit.scaffold_check_prereqs.resolve_active_feature", return_value=active),
            patch(
                "agentic_devtools.cli.speckit.scaffold_check_prereqs.check_prerequisites",
                side_effect=ValueError("Refusing symlinked plan.md"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            scaffold_check_prereqs_command(["--json"])

        assert exc_info.value.code == 1
        assert "ERROR: Refusing symlinked plan.md" in capsys.readouterr().err
