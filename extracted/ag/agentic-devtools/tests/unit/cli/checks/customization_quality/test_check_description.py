"""Tests for the Q1 description rule."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import DESCRIPTION_MAX_CHARS, check_description
from tests.unit.cli.checks.customization_quality._support import make_unit

GOOD = "Publishes the release notes for a tagged build, use when a release tag lands on main."


class TestCheckDescription:
    def test_accepts_a_description_that_says_what_and_when(self) -> None:
        """A description with an invocation clause and fresh words passes."""
        unit = make_unit(frontmatter={"description": GOOD})

        assert check_description(unit) == []

    def test_flags_a_missing_description_on_a_unit_that_requires_metadata(self) -> None:
        """Skills and agents must carry a description."""
        violations = check_description(make_unit(frontmatter={}))

        assert [v.rule for v in violations] == ["Q1"]
        assert "missing" in violations[0].message

    def test_ignores_a_missing_description_on_other_kinds(self) -> None:
        """A plain document is not required to declare a description."""
        unit = make_unit(path="docs/agent-customization/a.md", kind="document", listing="docs/agent-customization")

        assert check_description(unit) == []

    def test_flags_a_non_string_description_on_any_kind(self) -> None:
        """A declared description with the wrong type fails Q1 regardless of kind."""
        unit = make_unit(
            path="docs/agent-customization/a.md",
            kind="document",
            listing="docs/agent-customization",
            frontmatter={"description": 12},
        )

        violations = check_description(unit)

        assert [v.rule for v in violations] == ["Q1"]
        assert "unexpected type" in violations[0].message

    def test_flags_a_blank_description_once(self) -> None:
        """A whitespace-only description reports exactly one violation."""
        violations = check_description(make_unit(frontmatter={"description": "   "}))

        assert len(violations) == 1
        assert "empty" in violations[0].message

    def test_flags_a_description_over_the_char_cap(self) -> None:
        """A description longer than 1024 characters is over budget."""
        long_description = f"{GOOD} " + "release cadence detail " * 60

        violations = check_description(make_unit(frontmatter={"description": long_description}))

        assert [v.message for v in violations if str(DESCRIPTION_MAX_CHARS) in v.message]

    def test_flags_a_description_without_an_invocation_clause(self) -> None:
        """A description must say when the unit applies."""
        violations = check_description(make_unit(frontmatter={"description": "Publishes the release notes swiftly."}))

        assert any("invocation clause" in v.message for v in violations)

    def test_flags_a_description_that_only_restates_the_filename(self) -> None:
        """A description must add more than three content words beyond the filename."""
        unit = make_unit(
            path=".agents/skills/release-notes/SKILL.md",
            frontmatter={"description": "Release notes skill, use when release notes."},
        )

        violations = check_description(unit)

        assert any("content words beyond the filename" in v.message for v in violations)
