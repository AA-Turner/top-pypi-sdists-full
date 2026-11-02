"""Tests for counting selected skill entry files."""

from pathlib import Path

from agentic_devtools.skill_injector_prepare_skills import _count_selected_skills


def test_counts_distinct_skill_entry_files() -> None:
    origins = {
        "one/SKILL.md": Path("one/SKILL.md"),
        "one/guide.md": Path("one/guide.md"),
        "two/SKILL.md": Path("two/SKILL.md"),
    }

    assert _count_selected_skills(origins) == 2


def test_returns_zero_when_no_entry_files_are_selected() -> None:
    assert _count_selected_skills({"one/guide.md": Path("one/guide.md")}) == 0
