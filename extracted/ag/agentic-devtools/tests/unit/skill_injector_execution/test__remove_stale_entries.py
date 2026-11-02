"""Tests for deleting stale planned files."""

from pathlib import Path

from agentic_devtools.skill_injector_execution import _remove_stale_entries
from agentic_devtools.skill_injector_models import InjectionPlan


def _plan(kind: str, deleted: tuple[str, ...]) -> InjectionPlan:
    return InjectionPlan(kind, (), (), deleted, ())


def test_skips_legacy_migration_marker(tmp_path: Path) -> None:
    _remove_stale_entries(_plan("agents", (".agdt/",)), tmp_path)

    assert tmp_path.is_dir()


def test_removes_stale_flat_file_without_removing_target(tmp_path: Path) -> None:
    stale = tmp_path / "old.md"
    stale.write_text("old", encoding="utf-8")

    _remove_stale_entries(_plan("agents", (stale.name,)), tmp_path)

    assert not stale.exists()
    assert tmp_path.is_dir()


def test_removes_empty_skill_parent_after_stale_file(tmp_path: Path) -> None:
    skill = tmp_path / "my-skill"
    skill.mkdir()
    stale = skill / "old.md"
    stale.write_text("old", encoding="utf-8")

    _remove_stale_entries(_plan("skills", ("my-skill/old.md",)), tmp_path)

    assert not skill.exists()


def test_preserves_nonempty_skill_parent(tmp_path: Path) -> None:
    skill = tmp_path / "my-skill"
    skill.mkdir()
    (skill / "keep.md").write_text("keep", encoding="utf-8")
    stale = skill / "old.md"
    stale.write_text("old", encoding="utf-8")

    _remove_stale_entries(_plan("skills", ("my-skill/old.md",)), tmp_path)

    assert (skill / "keep.md").is_file()
