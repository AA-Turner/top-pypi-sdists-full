"""Tests for recording and copying newly created destinations."""

from pathlib import Path

from agentic_devtools.skill_injector_execution_copy import _copy_destination


def test_copies_and_records_destination_created_by_operation(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_text("source", encoding="utf-8")
    destination = tmp_path / "destination"
    created: list[Path] = []

    _copy_destination(source, destination, created)

    assert destination.read_text(encoding="utf-8") == "source"
    assert created == [destination]


def test_overwrite_does_not_mark_destination_as_new(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_text("new", encoding="utf-8")
    destination = tmp_path / "destination"
    destination.write_text("old", encoding="utf-8")
    created: list[Path] = []

    _copy_destination(source, destination, created)

    assert destination.read_text(encoding="utf-8") == "new"
    assert created == []
