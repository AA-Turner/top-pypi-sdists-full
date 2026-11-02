"""Tests for removing files created by a failed injection."""

from pathlib import Path

from agentic_devtools.skill_injector_execution import _rollback_new_files


def test_removes_created_file_and_prunes_empty_directories(tmp_path: Path) -> None:
    target = tmp_path / "target"
    nested = target / "my-skill"
    nested.mkdir(parents=True)
    created = nested / "guide.md"
    created.write_text("new", encoding="utf-8")

    _rollback_new_files([created], target)

    assert not created.exists()
    assert not nested.exists()


def test_empty_created_file_list_is_a_noop(tmp_path: Path) -> None:
    _rollback_new_files([], tmp_path)

    assert tmp_path.is_dir()
