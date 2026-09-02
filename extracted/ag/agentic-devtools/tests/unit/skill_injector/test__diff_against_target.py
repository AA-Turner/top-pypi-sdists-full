"""Tests for agentic_devtools.skill_injector._diff_against_target."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.skill_injector import _diff_against_target


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


class TestDiffAgainstTarget:
    """Tests for the _diff_against_target helper."""

    def test_missing_destination_is_an_add(self, tmp_path: Path) -> None:
        """A source without a destination file is reported as an add."""
        src = _write(tmp_path / "source" / "a.md", "a")
        added, overwritten = _diff_against_target(tmp_path / "target", {"a.md": src})
        assert (added, overwritten) == (["a.md"], [])

    def test_identical_bytes_are_reported_as_neither(self, tmp_path: Path) -> None:
        """A destination with identical content is neither an add nor an overwrite."""
        src = _write(tmp_path / "source" / "a.md", "same")
        _write(tmp_path / "target" / "a.md", "same")
        added, overwritten = _diff_against_target(tmp_path / "target", {"a.md": src})
        assert (added, overwritten) == ([], [])

    def test_different_bytes_are_an_overwrite(self, tmp_path: Path) -> None:
        """A destination with different content is reported as an overwrite."""
        src = _write(tmp_path / "source" / "a.md", "new")
        _write(tmp_path / "target" / "a.md", "old")
        added, overwritten = _diff_against_target(tmp_path / "target", {"a.md": src})
        assert (added, overwritten) == ([], ["a.md"])

    def test_nested_destination_path_is_supported(self, tmp_path: Path) -> None:
        """Nested destination keys (the skills kind) are diffed like flat ones."""
        src = _write(tmp_path / "source" / "s" / "SKILL.md", "body")
        added, overwritten = _diff_against_target(tmp_path / "target", {"s/SKILL.md": src})
        assert added == ["s/SKILL.md"]
