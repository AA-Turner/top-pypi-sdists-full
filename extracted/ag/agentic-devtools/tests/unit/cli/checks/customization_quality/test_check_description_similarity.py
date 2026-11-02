"""Tests for the Q3 description-similarity rule."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import check_description_similarity
from tests.unit.cli.checks.customization_quality._support import make_unit

RELEASE = "Publishes release notes for a tagged build, use when a release tag lands."
NEARLY_RELEASE = "Publishes release notes for a tagged build, use when a release tag arrives."
DISTINCT = "Rotates the signing certificate, use when the expiry warning fires."


class TestCheckDescriptionSimilarity:
    def test_accepts_distinct_descriptions(self) -> None:
        """Descriptions about different jobs stay below the Jaccard cap."""
        units = [
            make_unit(path=".agents/skills/a/SKILL.md", frontmatter={"description": RELEASE}),
            make_unit(path=".agents/skills/b/SKILL.md", frontmatter={"description": DISTINCT}),
        ]

        assert check_description_similarity(units, {u.path for u in units}) == []

    def test_flags_confusable_descriptions_on_both_files(self) -> None:
        """A near-duplicate pair is reported against each changed member."""
        units = [
            make_unit(path=".agents/skills/a/SKILL.md", frontmatter={"description": RELEASE}),
            make_unit(path=".agents/skills/b/SKILL.md", frontmatter={"description": NEARLY_RELEASE}),
        ]

        violations = check_description_similarity(units, {u.path for u in units})

        assert {v.path for v in violations} == {".agents/skills/a/SKILL.md", ".agents/skills/b/SKILL.md"}
        assert all(v.rule == "Q3" for v in violations)

    def test_reads_the_whole_corpus_but_reports_only_the_changed_file(self) -> None:
        """An unchanged sibling still supplies the collision."""
        changed = make_unit(path=".agents/skills/a/SKILL.md", frontmatter={"description": RELEASE})
        unchanged = make_unit(path=".agents/skills/b/SKILL.md", frontmatter={"description": NEARLY_RELEASE})

        violations = check_description_similarity([changed, unchanged], {changed.path})

        assert [v.path for v in violations] == [changed.path]

    def test_compares_only_within_one_listing(self) -> None:
        """Descriptions in different listings are never confusable with each other."""
        units = [
            make_unit(path=".agents/skills/a/SKILL.md", frontmatter={"description": RELEASE}),
            make_unit(
                path="docs/agent-customization/b.md",
                listing="docs/agent-customization",
                kind="document",
                frontmatter={"description": NEARLY_RELEASE},
            ),
        ]

        assert check_description_similarity(units, {u.path for u in units}) == []

    def test_skips_units_without_usable_descriptions(self) -> None:
        """Missing and content-word-free descriptions take part in no pair."""
        units = [
            make_unit(path=".agents/skills/a/SKILL.md", frontmatter={}),
            make_unit(path=".agents/skills/b/SKILL.md", frontmatter={"description": "the and for"}),
            make_unit(path=".agents/skills/c/SKILL.md", frontmatter={"description": RELEASE}),
        ]

        assert check_description_similarity(units, {u.path for u in units}) == []
