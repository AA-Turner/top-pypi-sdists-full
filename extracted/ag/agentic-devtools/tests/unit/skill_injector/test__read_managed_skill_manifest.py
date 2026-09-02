"""Tests for agentic_devtools.skill_injector._read_managed_skill_manifest."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector import _generate_readme, _read_managed_skill_manifest


class TestReadManagedSkillManifest:
    """Tests for the _read_managed_skill_manifest helper."""

    def test_missing_manifest_yields_empty_set(self, tmp_path: Path) -> None:
        """No manifest → nothing is managed, so nothing can be stale."""
        assert _read_managed_skill_manifest(tmp_path) == set()

    def test_non_utf8_manifest_raises_oserror(self, tmp_path: Path) -> None:
        """An undecodable manifest aborts planning instead of being trusted as empty."""
        (tmp_path / "agdt.README.md").write_bytes(b"\xff\xfe not utf-8")
        with pytest.raises(OSError, match="Unreadable managed skills manifest"):
            _read_managed_skill_manifest(tmp_path)

    def test_oserror_while_reading_manifest_raises_oserror(self, tmp_path: Path) -> None:
        """I/O failures while reading the manifest are surfaced as OSError."""
        (tmp_path / "agdt.README.md").write_text("x", encoding="utf-8")
        with patch("pathlib.Path.read_text", side_effect=PermissionError("denied")):
            with pytest.raises(OSError, match="Unreadable managed skills manifest"):
                _read_managed_skill_manifest(tmp_path)

    def test_table_rows_are_returned(self, tmp_path: Path) -> None:
        """Backtick-quoted manifest rows are returned as managed paths."""
        (tmp_path / "agdt.README.md").write_text(
            _generate_readme(
                [
                    ("my-skill/SKILL.md", "Does a thing"),
                    ("my-skill/usage guide.md", "Spaced name"),
                    ("my-skill/notes.md", "Notes"),
                ],
                "skills",
            ),
            encoding="utf-8",
        )
        assert _read_managed_skill_manifest(tmp_path) == {
            "my-skill/SKILL.md",
            "my-skill/usage guide.md",
            "my-skill/notes.md",
        }

    def test_entries_outside_the_skill_path_shape_are_ignored(self, tmp_path: Path) -> None:
        """Traversal, absolute, nested and flat entries are never treated as managed."""
        readme = _generate_readme([("ok-skill/SKILL.md", "valid")], "skills")
        (tmp_path / "agdt.README.md").write_text(
            readme
            + "| `../escape.md` | traversal |\n"
            + "| `/etc/passwd` | absolute |\n"
            + "| `skill/nested/deep.md` | too deep |\n"
            + "| `flat.md` | not inside a skill |\n"
            + "| `Upper-Case/SKILL.md` | invalid skill name |\n",
            encoding="utf-8",
        )
        assert _read_managed_skill_manifest(tmp_path) == {"ok-skill/SKILL.md"}

    def test_untrusted_manifest_without_marker_raises_oserror(self, tmp_path: Path) -> None:
        """A pre-existing table without a managed marker is refused."""
        (tmp_path / "agdt.README.md").write_text(
            "| File | Description |\n| ---- | ----------- |\n| `my-skill/SKILL.md` | x |\n",
            encoding="utf-8",
        )
        with pytest.raises(OSError, match="Refusing untrusted skills manifest"):
            _read_managed_skill_manifest(tmp_path)
