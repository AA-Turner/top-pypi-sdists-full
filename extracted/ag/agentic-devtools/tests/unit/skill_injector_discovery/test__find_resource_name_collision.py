"""Tests for detecting case-fold collisions among skill resources."""

from pathlib import Path

from agentic_devtools.skill_injector_discovery import _find_resource_name_collision


def test_returns_none_when_resource_names_are_distinct() -> None:
    assert _find_resource_name_collision([Path("guide.md"), Path("examples.json")]) is None


def test_returns_the_first_case_fold_collision() -> None:
    assert _find_resource_name_collision([Path("guide.md"), Path("Guide.md")]) == ("guide.md", "Guide.md")


def test_empty_resources_have_no_collision() -> None:
    assert _find_resource_name_collision([]) is None
