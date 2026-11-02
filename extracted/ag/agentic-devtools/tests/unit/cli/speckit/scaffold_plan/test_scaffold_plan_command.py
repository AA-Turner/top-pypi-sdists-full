"""Tests for ``scaffold_plan_command``."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import ActiveFeature, FeatureResolutionError
from agentic_devtools.cli.speckit.scaffold_plan import scaffold_plan_command


def _active(tmp_path: Path) -> ActiveFeature:
    return ActiveFeature(
        repo_root=tmp_path,
        feature_dir=tmp_path / "specs" / "042-x",
        branch="042-x",
        has_git=True,
    )


class TestScaffoldPlanCommand:
    """scaffold_plan_command reports the resolved paths as text or JSON."""

    def test_json_output(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        with (
            patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_active_feature", return_value=active),
            patch(
                "agentic_devtools.cli.speckit.scaffold_plan.prepare_plan",
                return_value=active.feature_dir / "plan.md",
            ),
        ):
            scaffold_plan_command(["--json"])

        payload = json.loads(capsys.readouterr().out)
        assert payload == {
            "FEATURE_DIR": str(active.feature_dir),
            "IMPL_PLAN": str(active.feature_dir / "plan.md"),
            "SPECS_DIR": str(active.feature_dir),
            "BRANCH": "042-x",
        }

    def test_text_output(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        with (
            patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_active_feature", return_value=active),
            patch(
                "agentic_devtools.cli.speckit.scaffold_plan.prepare_plan",
                return_value=active.feature_dir / "plan.md",
            ),
        ):
            scaffold_plan_command([])

        out = capsys.readouterr().out
        assert f"FEATURE_DIR: {active.feature_dir}" in out
        assert f"IMPL_PLAN: {active.feature_dir / 'plan.md'}" in out
        assert f"SPECS_DIR: {active.feature_dir}" in out
        assert "BRANCH: 042-x" in out

    def test_feature_resolution_error_exits_1(self, capsys) -> None:
        with (
            patch(
                "agentic_devtools.cli.speckit.scaffold_plan.resolve_active_feature",
                side_effect=FeatureResolutionError("ambiguous feature prefix"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            scaffold_plan_command([])

        assert exc_info.value.code == 1
        assert "ERROR: ambiguous feature prefix" in capsys.readouterr().err

    def test_prepare_plan_error_exits_1(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        with (
            patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_active_feature", return_value=active),
            patch(
                "agentic_devtools.cli.speckit.scaffold_plan.prepare_plan",
                side_effect=FeatureResolutionError("outside the repository root"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            scaffold_plan_command([])

        assert exc_info.value.code == 1
        assert "ERROR: outside the repository root" in capsys.readouterr().err

    def test_dry_run_text_output_does_not_create_files(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        with (
            patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_active_feature", return_value=active),
            patch("agentic_devtools.cli.speckit.scaffold_plan.is_dry_run", return_value=True),
            patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_plan_template", return_value=None),
        ):
            scaffold_plan_command([])

        out = capsys.readouterr().out
        assert "[DRY RUN]" in out
        assert not active.feature_dir.exists()

    def test_dry_run_json_output_includes_flag(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        with (
            patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_active_feature", return_value=active),
            patch("agentic_devtools.cli.speckit.scaffold_plan.is_dry_run", return_value=True),
            patch("agentic_devtools.cli.speckit.scaffold_plan.resolve_plan_template", return_value=None),
        ):
            scaffold_plan_command(["--json"])

        payload = json.loads(capsys.readouterr().out)
        assert payload["DRY_RUN"] is True
        assert not active.feature_dir.exists()
