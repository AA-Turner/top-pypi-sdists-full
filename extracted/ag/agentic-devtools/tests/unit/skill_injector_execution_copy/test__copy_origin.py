"""Tests for copying one planned source."""

from pathlib import Path

from agentic_devtools.skill_injector_execution_copy import _copy_origin


def test_skips_copy_when_source_resolves_to_destination(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    source = target / "existing.md"
    source.write_text("existing", encoding="utf-8")

    _copy_origin("agents", target, source.name, source, None, [])

    assert source.read_text(encoding="utf-8") == "existing"


def test_copies_skill_source_to_validated_nested_destination(tmp_path: Path) -> None:
    source = tmp_path / "source" / "my-skill" / "guide.md"
    source.parent.mkdir(parents=True)
    source.write_text("guide", encoding="utf-8")
    target = tmp_path / "target"
    created: list[Path] = []

    _copy_origin("skills", target, "my-skill/guide.md", source, None, created)

    assert (target / "my-skill" / "guide.md").read_text(encoding="utf-8") == "guide"
    assert created == [target / "my-skill" / "guide.md"]


def test_dispatches_case_rename_to_temporary_name_copy(tmp_path: Path) -> None:
    source = tmp_path / "source" / "my-skill" / "guide.md"
    source.parent.mkdir(parents=True)
    source.write_text("new", encoding="utf-8")
    target_skill = tmp_path / "target" / "my-skill"
    target_skill.mkdir(parents=True)
    old = target_skill / "Guide.md"
    old.write_text("old", encoding="utf-8")

    _copy_origin(
        "skills",
        target_skill.parent,
        "my-skill/guide.md",
        source,
        "my-skill/Guide.md",
        [],
    )

    assert not old.exists()
    assert (target_skill / "guide.md").read_text(encoding="utf-8") == "new"
