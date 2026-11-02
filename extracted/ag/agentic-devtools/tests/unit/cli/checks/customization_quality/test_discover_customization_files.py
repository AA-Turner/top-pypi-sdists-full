"""Tests for ``discover_customization_files``."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.checks.customization_quality import discover_customization_files
from tests.unit.cli.checks.customization_quality._support import write_file


class TestDiscoverCustomizationFiles:
    def test_returns_only_the_canonical_tree_sorted(self, tmp_path: Path) -> None:
        """Files under the three canonical roots are returned; legacy paths are not."""
        write_file(tmp_path, "docs/agent-customization/standard.md", "x")
        write_file(tmp_path, ".agents/skills/demo/SKILL.md", "x")
        write_file(tmp_path, ".github/instructions/python.instructions.md", "x")
        write_file(tmp_path, ".github/agents/agdt.legacy.agent.md", "x")
        write_file(tmp_path, ".github/prompts/agdt.legacy.prompt.md", "x")
        write_file(tmp_path, ".github/copilot-instructions.md", "x")
        write_file(tmp_path, "docs/other/readme.md", "x")

        assert discover_customization_files(tmp_path) == [
            ".agents/skills/demo/SKILL.md",
            ".github/instructions/python.instructions.md",
            "docs/agent-customization/standard.md",
        ]

    def test_skips_missing_roots(self, tmp_path: Path) -> None:
        """A repository without the canonical roots yields no files."""
        assert discover_customization_files(tmp_path) == []

    def test_skips_directories_whose_name_ends_in_md(self, tmp_path: Path) -> None:
        """A directory named ``*.md`` is not a customization file."""
        (tmp_path / ".agents/skills/notes.md").mkdir(parents=True)

        assert discover_customization_files(tmp_path) == []
