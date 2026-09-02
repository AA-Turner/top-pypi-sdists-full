"""Tests for the Q2 name rule."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import check_name
from tests.unit.cli.checks.customization_quality._support import make_unit


class TestCheckName:
    def test_accepts_a_legal_slug_equal_to_the_parent_directory(self) -> None:
        """A lowercase, dot-free slug matching its directory passes."""
        unit = make_unit(path=".agents/skills/release-notes/SKILL.md", frontmatter={"name": "release-notes"})

        assert check_name(unit) == []

    def test_flags_a_missing_name_on_a_unit_that_requires_metadata(self) -> None:
        """Skills and agents must declare a name."""
        violations = check_name(make_unit(frontmatter={}))

        assert [v.rule for v in violations] == ["Q2"]
        assert "missing" in violations[0].message

    def test_ignores_a_missing_name_on_other_kinds(self) -> None:
        """A plain document is not required to declare a name."""
        unit = make_unit(path="docs/agent-customization/a.md", kind="document", listing="docs/agent-customization")

        assert check_name(unit) == []

    def test_flags_a_non_string_name_on_any_kind(self) -> None:
        """A declared name with the wrong type fails Q2 regardless of kind."""
        unit = make_unit(
            path="docs/agent-customization/a.md",
            kind="document",
            listing="docs/agent-customization",
            frontmatter={"name": 42},
        )

        violations = check_name(unit)

        assert [v.rule for v in violations] == ["Q2"]
        assert "unexpected type" in violations[0].message

    def test_flags_a_slug_containing_dots(self) -> None:
        """The legacy ``agdt.x.y`` convention is illegal as a skill name."""
        unit = make_unit(path=".agents/skills/agdt.x.y/SKILL.md", frontmatter={"name": "agdt.x.y"})

        assert any("legal slug" in v.message for v in check_name(unit))

    def test_flags_a_name_over_the_length_cap(self) -> None:
        """A slug longer than 64 characters is rejected."""
        name = "a" * 65
        unit = make_unit(path=f".agents/skills/{name}/SKILL.md", frontmatter={"name": name})

        assert any("over the 64-char cap" in v.message for v in check_name(unit))

    def test_flags_a_name_that_differs_from_its_directory(self) -> None:
        """The slug must equal the parent directory name."""
        unit = make_unit(path=".agents/skills/release-notes/SKILL.md", frontmatter={"name": "notes"})

        assert any("parent directory" in v.message for v in check_name(unit))
