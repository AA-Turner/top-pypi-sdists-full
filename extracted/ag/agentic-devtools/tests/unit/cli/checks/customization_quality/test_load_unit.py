"""Tests for ``load_unit``."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.checks.customization_quality import load_unit
from tests.unit.cli.checks.customization_quality._support import write_file


class TestLoadUnit:
    def test_parses_frontmatter_body_listing_and_kind(self, tmp_path: Path) -> None:
        """A skill entry file is parsed into frontmatter, body, listing and kind."""
        write_file(
            tmp_path,
            ".agents/skills/demo/SKILL.md",
            "---\nname: demo\ndescription: Does a thing, use when asked.\n---\n# Demo\n",
        )

        unit = load_unit(tmp_path, ".agents/skills/demo/SKILL.md")

        assert unit.path == ".agents/skills/demo/SKILL.md"
        assert unit.listing == ".agents/skills"
        assert unit.kind == "skill"
        assert unit.frontmatter["name"] == "demo"
        assert unit.body.strip() == "# Demo"
        assert unit.size_bytes > 0

    def test_normalizes_the_supplied_path(self, tmp_path: Path) -> None:
        """A ``./``-prefixed or Windows-separated path is normalized."""
        write_file(tmp_path, "docs/agent-customization/standard.md", "# Standard\n")

        unit = load_unit(tmp_path, "./docs\\agent-customization/standard.md")

        assert unit.path == "docs/agent-customization/standard.md"
        assert unit.listing == "docs/agent-customization"
        assert unit.kind == "document"

    def test_rejects_a_path_outside_the_selection(self, tmp_path: Path) -> None:
        """Loading a legacy file raises rather than silently reading it."""
        write_file(tmp_path, ".github/agents/agdt.legacy.agent.md", "x")

        with pytest.raises(ValueError, match="outside the agent-customization selection"):
            load_unit(tmp_path, ".github/agents/agdt.legacy.agent.md")

    @pytest.mark.parametrize(
        ("content", "expected_body"),
        [
            ("# No frontmatter\n", "# No frontmatter\n"),
            ("---\nname: demo\n", "---\nname: demo\n"),
            ("----\nname: demo\n---\n# Thematic break\n", "----\nname: demo\n---\n# Thematic break\n"),
        ],
    )
    def test_treats_absent_or_unterminated_frontmatter_as_empty(
        self, tmp_path: Path, content: str, expected_body: str
    ) -> None:
        """Without a closed frontmatter block the whole file is the body."""
        write_file(tmp_path, "docs/agent-customization/a.md", content)

        unit = load_unit(tmp_path, "docs/agent-customization/a.md")

        assert unit.frontmatter == {}
        assert unit.body == expected_body

    @pytest.mark.parametrize(
        "content",
        [
            "---\n\n---\n# Empty block\n",
            "---\n: : :\n---\n# Malformed YAML\n",
            "---\njust a string\n---\n# Not a mapping\n",
        ],
    )
    def test_treats_empty_malformed_or_non_mapping_frontmatter_as_empty(self, tmp_path: Path, content: str) -> None:
        """Unusable frontmatter never blocks the remaining rules."""
        write_file(tmp_path, "docs/agent-customization/a.md", content)

        unit = load_unit(tmp_path, "docs/agent-customization/a.md")

        assert unit.frontmatter == {}
        assert unit.body.startswith("#")

    def test_rejects_a_symlink_that_escapes_the_repository_root(self, tmp_path: Path) -> None:
        """A symlink pointing outside the repository root raises ValueError."""
        outside = tmp_path / "outside" / "secret.md"
        outside.parent.mkdir()
        outside.write_text("secret", encoding="utf-8")
        repo = tmp_path / "repo"
        repo.mkdir()
        skill_dir = repo / ".agents" / "skills" / "demo"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").symlink_to(outside)

        with pytest.raises(ValueError, match="resolves outside the repository root"):
            load_unit(repo, ".agents/skills/demo/SKILL.md")

    def test_rejects_a_symlink_to_an_excluded_file_inside_the_repository(self, tmp_path: Path) -> None:
        """A selected alias cannot read a file that the selection predicate excludes."""
        repo = tmp_path / "repo"
        repo.mkdir()
        excluded = repo / ".github" / "agents" / "legacy.md"
        excluded.parent.mkdir(parents=True)
        excluded.write_text("legacy", encoding="utf-8")
        selected = repo / ".github" / "instructions" / "alias.instructions.md"
        selected.parent.mkdir(parents=True)
        selected.symlink_to(excluded)

        with pytest.raises(ValueError, match="outside the agent-customization selection"):
            load_unit(repo, ".github/instructions/alias.instructions.md")

    @pytest.mark.parametrize(
        ("rel_path", "content", "expected_kind"),
        [
            (".agents/skills/demo/helper.agent.md", "---\nname: demo\n---\n", "agent"),
            (".agents/skills/demo/reference.md", "# Reference\n", "document"),
            (".github/instructions/a.instructions.md", "# A\n", "always_loaded"),
            (".github/instructions/b.instructions.md", '---\napplyTo: "**"\n---\n', "always_loaded"),
            (".github/instructions/c.instructions.md", '---\napplyTo: "**/*.py"\n---\n', "scoped"),
        ],
    )
    def test_classifies_the_size_budget_kind(
        self, tmp_path: Path, rel_path: str, content: str, expected_kind: str
    ) -> None:
        """Each path/frontmatter combination maps to its Q5 size-budget kind."""
        write_file(tmp_path, rel_path, content)

        assert load_unit(tmp_path, rel_path).kind == expected_kind

    def test_size_bytes_reflects_crlf_line_endings(self, tmp_path: Path) -> None:
        """``size_bytes`` counts the actual file bytes, including CRLF sequences."""
        path = tmp_path / "docs" / "agent-customization" / "crlf.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        crlf_content = b"# Title\r\nLine two\r\n"
        path.write_bytes(crlf_content)

        unit = load_unit(tmp_path, "docs/agent-customization/crlf.md")

        assert unit.size_bytes == len(crlf_content)
