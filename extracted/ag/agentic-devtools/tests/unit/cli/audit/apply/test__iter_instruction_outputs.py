"""Tests for _iter_instruction_outputs."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.audit import apply as apply_module
from agentic_devtools.cli.audit.apply import _iter_instruction_outputs


class TestIterInstructionOutputs:
    """Tests for _iter_instruction_outputs() instruction-file discovery."""

    def test_collects_nested_agents_files(self, tmp_path: Path) -> None:
        """Directory-scoped AGENTS.md files are discovered at any depth."""
        nested = tmp_path / "agentic_devtools" / "adapters"
        nested.mkdir(parents=True)
        (nested / "AGENTS.md").write_text("# Adapter rules")

        result = _iter_instruction_outputs(tmp_path)

        assert result == [nested / "AGENTS.md"]

    def test_uses_instruction_filenames_constant_for_recursive_discovery(self, tmp_path: Path) -> None:
        """Recursive discovery follows INSTRUCTION_FILENAMES instead of a hard-coded name."""
        nested = tmp_path / "agentic_devtools" / "adapters"
        nested.mkdir(parents=True)
        custom_instruction = nested / "TEAM.md"
        custom_instruction.write_text("# Adapter rules")

        with patch.object(apply_module, "INSTRUCTION_FILENAMES", ("TEAM.md",)):
            result = _iter_instruction_outputs(tmp_path)

        assert result == [custom_instruction]

    def test_collects_root_copilot_instructions(self, tmp_path: Path) -> None:
        """The repository-wide .github/copilot-instructions.md is still collected."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "copilot-instructions.md").write_text("# Root rules")

        result = _iter_instruction_outputs(tmp_path)

        assert result == [github_dir / "copilot-instructions.md"]

    def test_nested_copilot_instructions_not_collected(self, tmp_path: Path) -> None:
        """A nested copilot-instructions.md outside .github/ is not collected.

        GitHub only reads copilot-instructions.md at .github/copilot-instructions.md;
        accepting it at arbitrary depths would strand the guidance written there.
        """
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "copilot-instructions.md").write_text("# Stranded rules")

        result = _iter_instruction_outputs(tmp_path)

        assert result == []

    def test_returns_sorted_paths_across_filenames(self, tmp_path: Path) -> None:
        """Results are sorted so both filenames yield a deterministic order."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "copilot-instructions.md").write_text("# Root rules")
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "AGENTS.md").write_text("# Test rules")

        result = _iter_instruction_outputs(tmp_path)

        assert result == sorted(result)
        assert set(result) == {
            github_dir / "copilot-instructions.md",
            tests_dir / "AGENTS.md",
        }

    def test_ignores_unrelated_markdown(self, tmp_path: Path) -> None:
        """Markdown files that are not instruction files are ignored."""
        (tmp_path / "audit-summary-report.md").write_text("# Summary")

        assert _iter_instruction_outputs(tmp_path) == []
