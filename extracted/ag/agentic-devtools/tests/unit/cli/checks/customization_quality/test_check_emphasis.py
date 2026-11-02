"""Tests for the Q9 emphasis rule."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import check_emphasis
from tests.unit.cli.checks.customization_quality._support import make_unit


class TestCheckEmphasis:
    def test_accepts_one_emphatic_directive_per_file(self) -> None:
        """A single emphatic directive is within the ration."""
        unit = make_unit(body="You MUST rerun the check because the cache is stale.\n")

        assert check_emphasis([unit], {unit.path}) == []

    def test_flags_a_file_over_the_emphasis_cap(self) -> None:
        """Counting CRITICAL, MUST, NEVER, ALWAYS and the warning emoji together."""
        unit = make_unit(body="CRITICAL: you MUST act.\nNEVER wait.\nALWAYS check.\n\u26a0 careful.\n")

        violations = check_emphasis([unit], {unit.path})

        assert [v.rule for v in violations] == ["Q9"]
        assert "5 emphatic directives" in violations[0].message

    def test_flags_an_emphatic_line_shared_by_two_files(self) -> None:
        """A repeated emphatic line, whitespace aside, is reported against each file."""
        first = make_unit(path=".agents/skills/a/SKILL.md", body="MUST run the gate\n")
        second = make_unit(path=".agents/skills/b/SKILL.md", body="  MUST   run the gate  \n")

        violations = check_emphasis([first, second], {first.path, second.path})

        assert {v.path for v in violations} == {first.path, second.path}
        assert all("emphatic line also appears in" in v.message for v in violations)

    def test_reads_the_whole_corpus_but_reports_only_the_changed_file(self) -> None:
        """An unchanged file supplies the collision but is not reported against."""
        changed = make_unit(path=".agents/skills/a/SKILL.md", body="MUST run the gate\n")
        unchanged = make_unit(path=".agents/skills/b/SKILL.md", body="MUST run the gate\n")

        violations = check_emphasis([changed, unchanged], {changed.path})

        assert [v.path for v in violations] == [changed.path]
        assert unchanged.path in violations[0].message

    def test_ignores_a_line_that_repeats_within_one_file(self) -> None:
        """The cross-file part of the rule needs two distinct files."""
        unit = make_unit(body="MUST run the gate\nMUST run the gate\n")

        violations = check_emphasis([unit], {unit.path})

        assert [v.message for v in violations] == ["2 emphatic directives, over the cap of 1"]
