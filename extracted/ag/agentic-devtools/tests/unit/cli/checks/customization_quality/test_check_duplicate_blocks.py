"""Tests for the cross-file duplication rule."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import FRAGMENT_MARKERS, check_duplicate_blocks
from tests.unit.cli.checks.customization_quality._support import make_unit

BLOCK = "Run the release gate before pushing the tag, then verify the build output.\n"
SHORT_BLOCK = "Run the gate.\n"


class TestCheckDuplicateBlocks:
    def test_accepts_distinct_bodies(self) -> None:
        """Files that share no block pass."""
        units = [
            make_unit(path=".agents/skills/a/SKILL.md", body=BLOCK),
            make_unit(path=".agents/skills/b/SKILL.md", body="Rotate the signing certificate every quarter.\n"),
        ]

        assert check_duplicate_blocks(units, {u.path for u in units}) == []

    def test_flags_a_block_shared_by_two_files(self) -> None:
        """A normalised block of 40+ chars in two files is a duplicate body."""
        units = [
            make_unit(path=".agents/skills/a/SKILL.md", body=BLOCK),
            make_unit(path=".agents/skills/b/SKILL.md", body=f"  {BLOCK.upper()}  "),
        ]

        violations = check_duplicate_blocks(units, {u.path for u in units})

        assert {v.path for v in violations} == {".agents/skills/a/SKILL.md", ".agents/skills/b/SKILL.md"}
        assert all(v.rule == "DUP" for v in violations)

    def test_ignores_blocks_below_the_length_floor(self) -> None:
        """Short blocks repeat too naturally to be evidence of a copied body."""
        units = [
            make_unit(path=".agents/skills/a/SKILL.md", body=SHORT_BLOCK),
            make_unit(path=".agents/skills/b/SKILL.md", body=SHORT_BLOCK),
        ]

        assert check_duplicate_blocks(units, {u.path for u in units}) == []

    def test_ignores_blocks_inside_a_fragment_marker(self) -> None:
        """A fragment is the sanctioned way to share one body."""
        start, end = FRAGMENT_MARKERS
        fragment = f"{start}\n{BLOCK}{end}\n"
        units = [
            make_unit(path=".agents/skills/a/SKILL.md", body=fragment),
            make_unit(path=".agents/skills/b/SKILL.md", body=fragment),
        ]

        assert check_duplicate_blocks(units, {u.path for u in units}) == []

    def test_reads_the_whole_corpus_but_reports_only_the_changed_file(self) -> None:
        """An unchanged file supplies the collision without being reported."""
        changed = make_unit(path=".agents/skills/a/SKILL.md", body=BLOCK)
        unchanged = make_unit(path=".agents/skills/b/SKILL.md", body=BLOCK)

        violations = check_duplicate_blocks([changed, unchanged], {changed.path})

        assert [v.path for v in violations] == [changed.path]
        assert unchanged.path in violations[0].message

    def test_ignores_a_block_repeated_within_one_file(self) -> None:
        """The rule is about two copies in two files, not one file repeating itself."""
        unit = make_unit(path=".agents/skills/a/SKILL.md", body=f"{BLOCK}\n{BLOCK}")

        assert check_duplicate_blocks([unit], {unit.path}) == []

    def test_unclosed_fragment_markers_do_not_hide_the_rest_of_the_file(self) -> None:
        """Only a matched marker pair exempts content from duplication checks."""
        start, _ = FRAGMENT_MARKERS
        body = f"{start}\n{BLOCK}"
        units = [
            make_unit(path=".agents/skills/a/SKILL.md", body=body),
            make_unit(path=".agents/skills/b/SKILL.md", body=BLOCK),
        ]

        violations = check_duplicate_blocks(units, {u.path for u in units})

        assert {v.path for v in violations} == {".agents/skills/a/SKILL.md", ".agents/skills/b/SKILL.md"}
