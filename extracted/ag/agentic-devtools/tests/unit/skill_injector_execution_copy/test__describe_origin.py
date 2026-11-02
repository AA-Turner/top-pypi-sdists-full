"""Tests for deriving origin descriptions for the managed manifest."""

from pathlib import Path

from agentic_devtools.skill_injector_execution_copy import _describe_origin


def test_uses_cached_frontmatter(tmp_path: Path) -> None:
    source = tmp_path / "SKILL.md"

    description, readable = _describe_origin(source, "skills", {source: {"description": "Cached"}})

    assert description == "Cached"
    assert readable is True


def test_uses_resource_filename_as_description(tmp_path: Path) -> None:
    source = tmp_path / "guide.md"

    description, readable = _describe_origin(source, "skills", {})

    assert description == "guide.md"
    assert readable is True


def test_parses_uncached_frontmatter(tmp_path: Path) -> None:
    source = tmp_path / "agent.md"
    source.write_text("---\ndescription: Agent help\n---\n", encoding="utf-8")

    description, readable = _describe_origin(source, "agents", {})

    assert description == "Agent help"
    assert readable is True


def test_parses_uncached_skill_entry_frontmatter(tmp_path: Path) -> None:
    source = tmp_path / "SKILL.md"
    source.write_text("---\ndescription: Skill help\n---\n", encoding="utf-8")

    description, readable = _describe_origin(source, "skills", {})

    assert description == "Skill help"
    assert readable is True


def test_reports_non_utf8_source_as_unreadable(tmp_path: Path) -> None:
    source = tmp_path / "agent.md"
    source.write_bytes(b"\xff")

    description, readable = _describe_origin(source, "agents", {})

    assert description == "Non-UTF-8 source; description unavailable."
    assert readable is False
