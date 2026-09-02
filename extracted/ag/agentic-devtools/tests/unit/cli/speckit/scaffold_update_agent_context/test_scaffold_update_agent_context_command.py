"""Tests for ``scaffold_update_agent_context_command``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_common import ActiveFeature, FeatureResolutionError
from agentic_devtools.cli.speckit.scaffold_update_agent_context import scaffold_update_agent_context_command


def _active(tmp_path: Path) -> ActiveFeature:
    return ActiveFeature(
        repo_root=tmp_path,
        feature_dir=tmp_path / "specs" / "042-x",
        branch="042-x",
        has_git=True,
    )


class TestScaffoldUpdateAgentContextCommand:
    """scaffold_update_agent_context_command wires the CLI to update_agent_context."""

    def test_success_prints_updated_path(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        with patch(
            "agentic_devtools.cli.speckit.scaffold_update_agent_context.resolve_active_feature",
            return_value=active,
        ):
            scaffold_update_agent_context_command(["copilot"])

        out = capsys.readouterr().out
        expected_path = tmp_path / ".github" / "copilot-instructions.md"
        assert f"Updated {expected_path}" in out
        assert expected_path.is_file()

    def test_missing_plan_md_exits_1(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        active.feature_dir.mkdir(parents=True)

        with patch(
            "agentic_devtools.cli.speckit.scaffold_update_agent_context.resolve_active_feature",
            return_value=active,
        ):
            with pytest.raises(SystemExit) as exc_info:
                scaffold_update_agent_context_command(["copilot"])

        assert exc_info.value.code == 1
        assert "ERROR:" in capsys.readouterr().err

    def test_malformed_existing_markers_exit_1(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").write_text("**Storage**: PostgreSQL", encoding="utf-8")
        agent_file = tmp_path / ".github" / "copilot-instructions.md"
        agent_file.parent.mkdir(parents=True, exist_ok=True)
        agent_file.write_text("# Header\n\n<!-- SPECKIT START -->\n\n# Footer", encoding="utf-8")

        with patch(
            "agentic_devtools.cli.speckit.scaffold_update_agent_context.resolve_active_feature",
            return_value=active,
        ):
            with pytest.raises(SystemExit) as exc_info:
                scaffold_update_agent_context_command(["copilot"])

        assert exc_info.value.code == 1
        assert "Malformed SpecKit marker block" in capsys.readouterr().err

    def test_unknown_agent_type_skips_with_warning(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        with patch(
            "agentic_devtools.cli.speckit.scaffold_update_agent_context.resolve_active_feature",
            return_value=active,
        ):
            scaffold_update_agent_context_command(["not-an-agent"])

        err = capsys.readouterr().err
        assert "WARNING" in err

    def test_missing_agent_type_argument_exits_2(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            scaffold_update_agent_context_command([])

        assert exc_info.value.code == 2

    def test_feature_resolution_error_exits_1(self, capsys) -> None:
        with (
            patch(
                "agentic_devtools.cli.speckit.scaffold_update_agent_context.resolve_active_feature",
                side_effect=FeatureResolutionError("ambiguous feature prefix"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            scaffold_update_agent_context_command(["copilot"])

        assert exc_info.value.code == 1
        assert "ERROR: ambiguous feature prefix" in capsys.readouterr().err

    def test_dry_run_prints_would_update_without_writing(self, tmp_path: Path, capsys) -> None:
        active = _active(tmp_path)
        active.feature_dir.mkdir(parents=True)
        (active.feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        with (
            patch(
                "agentic_devtools.cli.speckit.scaffold_update_agent_context.resolve_active_feature",
                return_value=active,
            ),
            patch("agentic_devtools.cli.speckit.scaffold_update_agent_context.is_dry_run", return_value=True),
        ):
            scaffold_update_agent_context_command(["copilot"])

        out = capsys.readouterr().out
        expected_path = tmp_path / ".github" / "copilot-instructions.md"
        assert f"[DRY RUN] Would update {expected_path}" in out
        assert not expected_path.exists()
