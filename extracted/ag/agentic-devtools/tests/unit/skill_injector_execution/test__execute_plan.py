"""Tests for executing one planned injection kind."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector_execution import _execute_plan
from agentic_devtools.skill_injector_models import InjectionPlan


def _plan(kind: str, *, deleted: tuple[str, ...] = (), renames: tuple[tuple[str, str], ...] = ()) -> InjectionPlan:
    return InjectionPlan(kind, (), (), deleted, renames)


def test_writes_manifest_using_cached_metadata(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("source", encoding="utf-8")
    target = tmp_path / "target"
    destination_name = "agdt.agent.md"

    success = _execute_plan(
        _plan("agents"),
        target,
        {destination_name: source},
        {source: {"description": "Cached description"}},
    )

    assert success is True
    assert (target / destination_name).read_text(encoding="utf-8") == "source"
    assert "Cached description" in (target / "agdt.README.md").read_text(encoding="utf-8")


def test_decodes_uncached_source_and_reports_binary_markdown(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_bytes(b"\xff")

    success = _execute_plan(_plan("agents"), tmp_path / "target", {"agdt.binary.md": source}, {})

    assert success is False
    assert "Non-UTF-8 source" in (tmp_path / "target" / "agdt.README.md").read_text(encoding="utf-8")


def test_skips_copy_when_source_is_already_the_destination(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    source = target / "agdt.source.md"
    source.write_text("# Source", encoding="utf-8")

    assert _execute_plan(_plan("agents"), target, {source.name: source}, {}) is True
    assert source.read_text(encoding="utf-8") == "# Source"


def test_copies_binary_skill_resources_and_removes_retired_skill_directory(tmp_path: Path) -> None:
    source = tmp_path / "source" / "kept-skill" / "icon.png"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"\x89PNG")
    target = tmp_path / "target"
    retired = target / "retired-skill"
    retired.mkdir(parents=True)
    (retired / "gone.md").write_text("gone", encoding="utf-8")

    result = _execute_plan(
        _plan("skills", deleted=("retired-skill/gone.md",)),
        target,
        {"kept-skill/icon.png": source},
        {},
    )

    assert result is True
    assert (target / "kept-skill" / "icon.png").read_bytes() == b"\x89PNG"
    assert not retired.exists()
    manifest = (target / "agdt.README.md").read_text(encoding="utf-8")
    assert "kept-skill/icon.png" in manifest
    assert "icon.png" in manifest


def test_removes_legacy_directory_before_writing_manifest(tmp_path: Path) -> None:
    target = tmp_path / "target"
    old = target / ".agdt"
    old.mkdir(parents=True)
    (old / "old.md").write_text("old", encoding="utf-8")

    assert _execute_plan(_plan("agents", deleted=(".agdt/",)), target, {}, {}) is True
    assert not old.exists()


def test_ignores_missing_legacy_directory(tmp_path: Path) -> None:
    target = tmp_path / "target"

    assert _execute_plan(_plan("agents", deleted=(".agdt/",)), target, {}, {}) is True
    assert (target / "agdt.README.md").is_file()


def test_removes_legacy_symlink_without_removing_its_target(tmp_path: Path) -> None:
    target = tmp_path / "target"
    outside = tmp_path / "outside"
    outside.mkdir()
    marker = outside / "marker"
    marker.write_text("keep", encoding="utf-8")
    target.mkdir()
    link = target / ".agdt"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks are not supported")

    assert _execute_plan(_plan("agents", deleted=(".agdt/",)), target, {}, {}) is True
    assert not link.is_symlink()
    assert marker.read_text(encoding="utf-8") == "keep"


def test_performs_case_rename_through_temporary_name(tmp_path: Path) -> None:
    source = tmp_path / "source" / "my-skill" / "guide.md"
    source.parent.mkdir(parents=True)
    source.write_text("new guide", encoding="utf-8")
    target = tmp_path / "target" / "my-skill"
    target.mkdir(parents=True)
    old = target / "Guide.md"
    old.write_text("old guide", encoding="utf-8")

    assert _execute_plan(
        _plan("skills", renames=(("my-skill/Guide.md", "my-skill/guide.md"),)),
        target.parent,
        {"my-skill/guide.md": source},
        {},
    )
    assert not old.exists()
    assert (target / "guide.md").read_text(encoding="utf-8") == "new guide"


def test_case_rename_falls_back_when_old_path_is_missing(tmp_path: Path) -> None:
    source = tmp_path / "source" / "my-skill" / "guide.md"
    source.parent.mkdir(parents=True)
    source.write_text("new", encoding="utf-8")
    target = tmp_path / "target"

    assert _execute_plan(
        _plan("skills", renames=(("my-skill/Guide.md", "my-skill/guide.md"),)),
        target,
        {"my-skill/guide.md": source},
        {},
    )
    assert (target / "my-skill" / "guide.md").read_text(encoding="utf-8") == "new"


def test_case_rename_fallback_overwrites_existing_destination(tmp_path: Path) -> None:
    source = tmp_path / "source" / "my-skill" / "guide.md"
    source.parent.mkdir(parents=True)
    source.write_text("new", encoding="utf-8")
    target = tmp_path / "target" / "my-skill"
    target.mkdir(parents=True)
    destination = target / "guide.md"
    destination.write_text("old", encoding="utf-8")

    assert _execute_plan(
        _plan("skills", renames=(("my-skill/Guide.md", "my-skill/guide.md"),)),
        target.parent,
        {"my-skill/guide.md": source},
        {},
    )
    assert destination.read_text(encoding="utf-8") == "new"


def test_failed_manifest_write_rolls_back_new_files(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("source", encoding="utf-8")
    target = tmp_path / "target"
    with patch("agentic_devtools.skill_injector_execution.os.replace", side_effect=OSError("disk full")):
        with pytest.raises(OSError, match="disk full"):
            _execute_plan(_plan("agents"), target, {"agdt.source.md": source}, {})

    assert not (target / "agdt.source.md").exists()
    assert not (target / "agdt.README.md").exists()


def test_rollback_ignores_unlink_error_for_new_file(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("source", encoding="utf-8")
    target = tmp_path / "target"
    with (
        patch("agentic_devtools.skill_injector_execution.os.replace", side_effect=OSError("disk full")),
        patch("pathlib.Path.unlink", side_effect=OSError("cannot remove")),
        pytest.raises(OSError, match="disk full"),
    ):
        _execute_plan(_plan("agents"), target, {"agdt.source.md": source}, {})


def test_case_rename_restores_old_name_when_copy_fails(tmp_path: Path) -> None:
    source = tmp_path / "source" / "my-skill" / "guide.md"
    source.parent.mkdir(parents=True)
    source.write_text("new", encoding="utf-8")
    target = tmp_path / "target" / "my-skill"
    target.mkdir(parents=True)
    old = target / "Guide.md"
    old.write_text("old", encoding="utf-8")

    with (
        patch("agentic_devtools.skill_injector_execution_copy.shutil.copy2", side_effect=OSError("copy failed")),
        pytest.raises(OSError, match="copy failed"),
    ):
        _execute_plan(
            _plan("skills", renames=(("my-skill/Guide.md", "my-skill/guide.md"),)),
            target.parent,
            {"my-skill/guide.md": source},
            {},
        )

    assert old.read_text(encoding="utf-8") == "old"
    assert not (target / "guide.md").exists()


def test_case_rename_suppresses_restore_error_after_copy_failure(tmp_path: Path) -> None:
    source = tmp_path / "source" / "my-skill" / "guide.md"
    source.parent.mkdir(parents=True)
    source.write_text("new", encoding="utf-8")
    target = tmp_path / "target" / "my-skill"
    target.mkdir(parents=True)
    old = target / "Guide.md"
    old.write_text("old", encoding="utf-8")
    real_replace = os.replace
    replace_calls = 0

    def replace_side_effect(src: str | Path, dst: str | Path) -> None:
        nonlocal replace_calls
        replace_calls += 1
        if replace_calls == 2:
            raise OSError("restore failed")
        real_replace(src, dst)

    with (
        patch("agentic_devtools.skill_injector_execution_copy.os.replace", side_effect=replace_side_effect),
        patch("agentic_devtools.skill_injector_execution_copy.shutil.copy2", side_effect=OSError("copy failed")),
        pytest.raises(OSError, match="copy failed"),
    ):
        _execute_plan(
            _plan("skills", renames=(("my-skill/Guide.md", "my-skill/guide.md"),)),
            target.parent,
            {"my-skill/guide.md": source},
            {},
        )


def test_normal_copy_overwrites_existing_destination(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("new", encoding="utf-8")
    target = tmp_path / "target"
    target.mkdir()
    destination = target / "agdt.source.md"
    destination.write_text("old", encoding="utf-8")

    assert _execute_plan(_plan("agents"), target, {destination.name: source}, {})
    assert destination.read_text(encoding="utf-8") == "new"


def test_stale_flat_file_does_not_remove_target_directory(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    stale = target / "agdt.old.md"
    stale.write_text("stale", encoding="utf-8")

    assert _execute_plan(_plan("agents", deleted=(stale.name,)), target, {}, {})
    assert not stale.exists()
    assert target.is_dir()


def test_failed_tempfile_cleanup_is_suppressed(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("source", encoding="utf-8")
    target = tmp_path / "target"
    real_unlink = os.unlink

    def unlink_side_effect(path: str | Path) -> None:
        if ".agdt.README." in str(path):
            raise OSError("cleanup failed")
        real_unlink(path)

    with (
        patch("agentic_devtools.skill_injector_execution.os.replace", side_effect=OSError("write failed")),
        patch("agentic_devtools.skill_injector_execution.os.unlink", side_effect=unlink_side_effect),
        pytest.raises(OSError, match="write failed"),
    ):
        _execute_plan(_plan("agents"), target, {"agdt.source.md": source}, {})

    assert not (target / "agdt.source.md").exists()


def test_failed_write_removes_new_nested_skill_directory(tmp_path: Path) -> None:
    source = tmp_path / "source" / "my-skill" / "guide.md"
    source.parent.mkdir(parents=True)
    source.write_text("guide", encoding="utf-8")
    target = tmp_path / "target"

    with (
        patch("agentic_devtools.skill_injector_execution.os.replace", side_effect=OSError("disk full")),
        pytest.raises(OSError, match="disk full"),
    ):
        _execute_plan(_plan("skills"), target, {"my-skill/guide.md": source}, {})

    assert not (target / "my-skill").exists()


def test_rollback_stops_pruning_when_nested_directory_cannot_be_removed(tmp_path: Path) -> None:
    source = tmp_path / "source" / "my-skill" / "guide.md"
    source.parent.mkdir(parents=True)
    source.write_text("guide", encoding="utf-8")
    target = tmp_path / "target"

    with (
        patch("agentic_devtools.skill_injector_execution.os.replace", side_effect=OSError("disk full")),
        patch("pathlib.Path.rmdir", side_effect=OSError("directory busy")),
        pytest.raises(OSError, match="disk full"),
    ):
        _execute_plan(_plan("skills"), target, {"my-skill/guide.md": source}, {})
