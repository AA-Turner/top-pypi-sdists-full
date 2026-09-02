"""Tests for the ``validate`` entry point."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.checks.customization_quality import validate
from tests.unit.cli.checks.customization_quality._support import write_file

CLEAN_SKILL = """---
name: release-notes
description: Publishes the changelog for a tagged build, use when a version tag lands on main.
---

# Release notes

1. Read the tag.
2. Publish the changelog entry.
"""


class TestValidate:
    def test_is_the_check_customization_quality_function(self) -> None:
        """``validate`` is the canonical entry point required by issue #3757."""
        from agentic_devtools.cli.checks.customization_quality import check_customization_quality

        assert validate is check_customization_quality

    def test_accepts_an_iterable_of_changed_files(self, tmp_path: Path) -> None:
        """``validate`` accepts any iterable (e.g. a generator) for changed_files."""
        write_file(tmp_path, ".agents/skills/release-notes/SKILL.md", CLEAN_SKILL)

        result = validate(tmp_path, iter([".agents/skills/release-notes/SKILL.md"]))

        assert result.violations == []
        assert result.checked_files == [".agents/skills/release-notes/SKILL.md"]
