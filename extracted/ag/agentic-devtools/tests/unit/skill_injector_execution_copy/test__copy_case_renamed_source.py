"""Tests for case-only path renames."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector_execution_copy import _copy_case_renamed_source


def test_moves_old_spelling_out_of_the_way_before_copy(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("new", encoding="utf-8")
    target = tmp_path / "target"
    old = target / "my-skill" / "Guide.md"
    old.parent.mkdir(parents=True)
    old.write_text("old", encoding="utf-8")
    destination = target / "my-skill" / "guide.md"

    _copy_case_renamed_source(target, "my-skill/Guide.md", source, destination, [])

    assert not old.exists()
    assert destination.read_text(encoding="utf-8") == "new"


def test_falls_back_to_copy_when_old_spelling_is_missing(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("new", encoding="utf-8")
    target = tmp_path / "target"
    destination = target / "my-skill" / "guide.md"
    destination.parent.mkdir(parents=True)
    created: list[Path] = []

    _copy_case_renamed_source(
        target,
        "my-skill/Guide.md",
        source,
        destination,
        created,
    )

    assert destination.read_text(encoding="utf-8") == "new"
    assert created == [destination]


def test_restores_old_spelling_when_copy_raises(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("new", encoding="utf-8")
    target = tmp_path / "target"
    old = target / "my-skill" / "Guide.md"
    old.parent.mkdir(parents=True)
    old.write_text("old", encoding="utf-8")

    with (
        patch("agentic_devtools.skill_injector_execution_copy.shutil.copy2", side_effect=OSError("copy failed")),
        pytest.raises(OSError, match="copy failed"),
    ):
        _copy_case_renamed_source(target, "my-skill/Guide.md", source, target / "my-skill" / "guide.md", [])

    assert old.read_text(encoding="utf-8") == "old"


def test_suppresses_error_restoring_old_spelling_after_copy_failure(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("new", encoding="utf-8")
    target = tmp_path / "target"
    old = target / "my-skill" / "Guide.md"
    old.parent.mkdir(parents=True)
    old.write_text("old", encoding="utf-8")

    with (
        patch(
            "agentic_devtools.skill_injector_execution_copy.os.replace", side_effect=[None, OSError("restore failed")]
        ),
        patch("agentic_devtools.skill_injector_execution_copy.shutil.copy2", side_effect=OSError("copy failed")),
        pytest.raises(OSError, match="copy failed"),
    ):
        _copy_case_renamed_source(target, "my-skill/Guide.md", source, target / "my-skill" / "guide.md", [])
