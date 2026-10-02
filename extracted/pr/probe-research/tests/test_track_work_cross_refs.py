"""Every section the track-work skill points at exists in its reference.

The skill says `reference §4`; the reference is a separate file with `## 4.`
headings and an INDEX table. Nothing else ties the two together, so a
renumber or rename in one file silently strands the pointers in the other --
the agent opens the reference and lands on the wrong section, or none.

Three checks, on the canonical copies under agent/skills/ (held byte-identical
to the shipped plugin copies by test_skills_sync.py and test_pi_skills_sync.py):

1. every `§N` the skill cites is a `## N.` heading in the reference;
2. every `§N` the reference's own INDEX cites is a `## N.` heading below it;
3. every bare `§N` in the skill (its own sections) is a `## N.` heading in the skill.

The checker is exercised on a deliberately broken pair first, so the test
cannot pass by finding nothing to check.
"""

from __future__ import annotations

import re
from pathlib import Path


AGENT_ROOT = Path(__file__).resolve().parents[1]
SKILL = AGENT_ROOT / "skills" / "track-work" / "SKILL.md"
REFERENCE = AGENT_ROOT / "skills" / "track-work" / "reference.md"

#: Only a QUALIFIED citation crosses files. A bare `§3` in the skill means the
#: skill's own section 3 -- the map's how-to column is full of them -- and
#: counting those sent the first version of this test hunting for `## 3.` in
#: the wrong file.
_CROSS = re.compile(r"reference §(\d+(?:\s*,\s*§\d+)*)", re.I)
_BARE = re.compile(r"§(\d+)")
_HEADING = re.compile(r"^## (\d+)\.", re.M)


def cited_sections(text: str) -> set[int]:
    """Sections this document points at IN THE OTHER FILE: `reference §4`, or
    `reference §1, §9`."""
    return {int(n) for run in _CROSS.findall(text) for n in _BARE.findall("§" + run)}


def numbered_headings(text: str) -> set[int]:
    return {int(n) for n in _HEADING.findall(text)}


def own_sections(text: str) -> set[int]:
    """Bare `§N` citations -- the ones that are NOT part of a `reference §N` run."""
    return {int(n) for n in _BARE.findall(_CROSS.sub("", text))}


def dangling(pointer_text: str, target_text: str) -> set[int]:
    """Cited sections with no heading to land on."""
    return cited_sections(pointer_text) - numbered_headings(target_text)


class TestTheCheckerItself:
    def test_a_stranded_pointer_is_caught(self) -> None:
        skill = "flags are in reference §4; papers in reference §5."
        reference = "## 1. ENTITY COMMANDS\n\n## 4. FILES\n"
        assert dangling(skill, reference) == {5}

    def test_a_matching_pair_is_clean(self) -> None:
        skill = "see reference §1 and reference §2, plus reference §1, §9"
        reference = "## 1. A\n\n## 2. B\n\n## 9. C\n"
        assert dangling(skill, reference) == set()

    def test_the_skills_own_section_numbers_are_not_cross_references(self) -> None:
        """`§3` alone is the skill pointing at ITSELF. Treating it as a
        cross-file citation is what made the first run of this test fail."""
        assert cited_sections("see §3 above, and reference §1") == {1}


class TestTheShippedFiles:
    def test_every_skill_pointer_lands(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        reference = REFERENCE.read_text(encoding="utf-8")
        missing = dangling(skill, reference)
        assert not missing, (
            f"SKILL.md cites reference §{sorted(missing)} but reference.md has no "
            f"such `## N.` heading -- renumbered one file and not the other?"
        )

    def test_the_skill_actually_cites_the_reference(self) -> None:
        """Without this the pair above passes on a skill that cites nothing --
        which is exactly how it passed the first time it was run."""
        cited = cited_sections(SKILL.read_text(encoding="utf-8"))
        assert cited, (
            "SKILL.md names no `reference §N` at all. Either the numbered "
            "pointers were dropped, or this guard landed before them."
        )

    def test_the_reference_index_matches_its_own_headings(self) -> None:
        reference = REFERENCE.read_text(encoding="utf-8")
        assert "## INDEX" in reference, "reference.md lost its INDEX table"
        index = reference[reference.index("## INDEX") : reference.index("## 1.")]
        # Inside the INDEX every `§N` is a row pointing down this same file.
        missing = {int(n) for n in _BARE.findall(index)} - numbered_headings(reference)
        assert not missing, f"INDEX names §{sorted(missing)} with no matching heading"

    def test_the_skills_own_section_pointers_land(self) -> None:
        """`§1 says which entity to hang it on` is the skill pointing at its own
        `## 1.`; a renumber inside the skill strands those just as quietly."""
        skill = SKILL.read_text(encoding="utf-8")
        missing = own_sections(skill) - numbered_headings(skill)
        assert not missing, f"SKILL.md cites its own §{sorted(missing)} with no such heading"

    def test_a_capitalised_citation_is_still_a_citation(self) -> None:
        assert cited_sections("Reference §3 has: how to add files") == {3}
