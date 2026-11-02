"""Tests for the ``check_customization_quality`` entry point."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.checks.customization_quality import check_customization_quality
from tests.unit.cli.checks.customization_quality._support import write_file

CLEAN_SKILL = """---
name: release-notes
description: Publishes the changelog for a tagged build, use when a version tag lands on main.
---

# Release notes

1. Read the tag.
2. Publish the changelog entry.
"""

CLEAN_SIBLING = """---
name: certificate-rotation
description: Rotates the signing certificate, use when the expiry warning fires in monitoring.
---

# Certificate rotation

1. Fetch the replacement certificate.
2. Install it on the build host.
"""

NOISY_SKILL = """---
name: agdt.noisy.thing
---

# Noisy

You MUST do this. You MUST do that. NEVER stop.
"""


class TestCheckCustomizationQuality:
    def test_passes_on_a_clean_canonical_tree(self, tmp_path: Path) -> None:
        """Two well-formed skills produce no violations."""
        write_file(tmp_path, ".agents/skills/release-notes/SKILL.md", CLEAN_SKILL)
        write_file(tmp_path, ".agents/skills/certificate-rotation/SKILL.md", CLEAN_SIBLING)

        result = check_customization_quality(tmp_path)

        assert result.violations == []
        assert result.is_valid is True
        assert result.checked_files == result.corpus_files

    def test_reports_every_rule_family_against_a_failing_file(self, tmp_path: Path) -> None:
        """A deliberately bad skill trips the per-file rules."""
        write_file(tmp_path, ".agents/skills/agdt.noisy.thing/SKILL.md", NOISY_SKILL)

        result = check_customization_quality(tmp_path)

        assert result.is_valid is False
        assert {"Q1", "Q2", "Q8", "Q9"} <= {v.rule for v in result.violations}

    def test_never_reads_the_legacy_corpus(self, tmp_path: Path) -> None:
        """Legacy agents, prompts and the always-on file are outside the selection."""
        write_file(tmp_path, ".github/agents/agdt.legacy.agent.md", NOISY_SKILL)
        write_file(tmp_path, ".github/prompts/agdt.legacy.prompt.md", NOISY_SKILL)
        write_file(tmp_path, ".github/copilot-instructions.md", NOISY_SKILL)

        result = check_customization_quality(tmp_path)

        assert result.corpus_files == []
        assert result.is_valid is True

    def test_reports_only_against_the_changed_set(self, tmp_path: Path) -> None:
        """An unchanged failing file is read but not reported against."""
        write_file(tmp_path, ".agents/skills/release-notes/SKILL.md", CLEAN_SKILL)
        write_file(tmp_path, ".agents/skills/agdt.noisy.thing/SKILL.md", NOISY_SKILL)

        result = check_customization_quality(tmp_path, [".agents/skills/release-notes/SKILL.md"])

        assert result.checked_files == [".agents/skills/release-notes/SKILL.md"]
        assert len(result.corpus_files) == 2
        assert result.violations == []

    def test_ignores_changed_files_outside_the_selection(self, tmp_path: Path) -> None:
        """A changed legacy or source file selects nothing to report against."""
        write_file(tmp_path, ".agents/skills/release-notes/SKILL.md", CLEAN_SKILL)

        result = check_customization_quality(tmp_path, [".github/copilot-instructions.md", "README.md"])

        assert result.checked_files == []
        assert result.is_valid is True

    def test_rejects_a_repo_root_that_is_not_an_existing_directory(self, tmp_path: Path) -> None:
        """A missing path or regular file is a caller error, not a clean result."""
        file_path = tmp_path / "repo.txt"
        file_path.write_text("not a repo", encoding="utf-8")

        for invalid_root in (tmp_path / "missing", file_path):
            try:
                check_customization_quality(invalid_root)
            except ValueError as exc:
                assert "existing directory" in str(exc)
            else:
                raise AssertionError("expected ValueError for invalid repo_root")

    def test_reports_a_corpus_scoped_collision_against_the_changed_file(self, tmp_path: Path) -> None:
        """A changed file colliding with an unchanged one is still caught."""
        write_file(tmp_path, ".agents/skills/release-notes/SKILL.md", CLEAN_SKILL)
        write_file(
            tmp_path,
            ".agents/skills/changelog-notes/SKILL.md",
            CLEAN_SKILL.replace("name: release-notes", "name: changelog-notes"),
        )

        result = check_customization_quality(tmp_path, [".agents/skills/changelog-notes/SKILL.md"])

        assert {v.path for v in result.violations} == {".agents/skills/changelog-notes/SKILL.md"}
        assert {"Q3", "DUP"} <= {v.rule for v in result.violations}

    def test_sorts_violations_by_path_then_rule(self, tmp_path: Path) -> None:
        """Reports are stable so a diff of two runs is meaningful."""
        write_file(tmp_path, ".agents/skills/agdt.noisy.thing/SKILL.md", NOISY_SKILL)
        write_file(tmp_path, "docs/agent-customization/notes.md", "You MUST read this.\n")

        result = check_customization_quality(tmp_path)

        keys = [(v.path, v.rule, v.message) for v in result.violations]
        assert keys == sorted(keys)
