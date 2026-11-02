"""Tests for the one-time legacy .agdt migration."""

from pathlib import Path

import pytest

from agentic_devtools.skill_injector_execution import _remove_legacy_directory
from agentic_devtools.skill_injector_models import InjectionPlan


def _plan(*, deleted: tuple[str, ...]) -> InjectionPlan:
    return InjectionPlan("agents", (), (), deleted, ())


def test_does_nothing_when_migration_is_not_planned(tmp_path: Path) -> None:
    old = tmp_path / ".agdt"
    old.mkdir()

    _remove_legacy_directory(_plan(deleted=()), tmp_path)

    assert old.is_dir()


def test_removes_legacy_directory(tmp_path: Path) -> None:
    old = tmp_path / ".agdt"
    old.mkdir()

    _remove_legacy_directory(_plan(deleted=(".agdt/",)), tmp_path)

    assert not old.exists()


def test_removes_legacy_symlink_only(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    link = tmp_path / ".agdt"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks are not supported")

    _remove_legacy_directory(_plan(deleted=(".agdt/",)), tmp_path)

    assert not link.is_symlink()
    assert outside.is_dir()


def test_ignores_regular_file_named_agdt(tmp_path: Path) -> None:
    old = tmp_path / ".agdt"
    old.write_text("keep", encoding="utf-8")

    _remove_legacy_directory(_plan(deleted=(".agdt/",)), tmp_path)

    assert old.read_text(encoding="utf-8") == "keep"
