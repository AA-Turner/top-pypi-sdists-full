"""Tests for the ``CustomizationUnit`` dataclass."""

from __future__ import annotations

import dataclasses

import pytest

from agentic_devtools.cli.checks.customization_quality import CustomizationUnit


class TestCustomizationUnit:
    def test_exposes_every_field_the_rules_need(self) -> None:
        """A unit carries its path, listing, kind, frontmatter, body, size and source."""
        unit = CustomizationUnit(
            path=".agents/skills/demo/SKILL.md",
            listing=".agents/skills",
            kind="skill",
            frontmatter={"name": "demo"},
            body="body",
            size_bytes=4,
            source="---\nname: demo\n---\nbody",
        )

        assert unit.path == ".agents/skills/demo/SKILL.md"
        assert unit.listing == ".agents/skills"
        assert unit.kind == "skill"
        assert unit.frontmatter == {"name": "demo"}
        assert unit.body == "body"
        assert unit.size_bytes == 4
        assert unit.source == "---\nname: demo\n---\nbody"

    def test_is_frozen(self) -> None:
        """Units are immutable so a rule cannot mutate the parsed corpus."""
        unit = CustomizationUnit(
            path="a.md", listing=".agents/skills", kind="document", frontmatter={}, body="", size_bytes=0, source=""
        )

        with pytest.raises(dataclasses.FrozenInstanceError):
            unit.kind = "skill"  # type: ignore[misc]
